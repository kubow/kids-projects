#!/usr/bin/env python3
"""Manage Minecraft Bedrock add-ons on an Android device connected via USB.

Talks to the device over MTP through KDE KIO (`kioclient`), so it works while
Dolphin / kiod already holds the USB connection (plain libmtp tools then fail
with "device is busy").

    python addons.py list                 # installed packs, pairs, usage in worlds
    python addons.py worlds [--all]       # worlds and their active packs
    python addons.py backup [DEST]        # copy all packs from the device
    python addons.py install FILE...      # .mcaddon / .mcpack / .zip / folder
    python addons.py remove PACK          # delete pack (+ its BP/RP pair)
    python addons.py enable WORLD PACK    # activate pack (+ pair) in a world
    python addons.py disable WORLD PACK

PACK = part of the pack name or folder, or a UUID prefix.
WORLD = world folder id (e.g. "TUi39f38ZLY=") or exact world name.
Override the device path with MC_DEVICE_ROOT=mtp:/<device>/<storage>.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

GAME_DIR = "Android/data/com.mojang.minecraftpe/files/games/com.mojang"
KINDS = {"behavior_packs": "BP", "resource_packs": "RP"}
WORLD_FILES = {"behavior_packs": "world_behavior_packs.json",
               "resource_packs": "world_resource_packs.json"}
MODULE_KIND = {"resources": "resource_packs", "data": "behavior_packs",
               "script": "behavior_packs", "javascript": "behavior_packs",
               "client_data": "behavior_packs", "skin_pack": "skin_packs"}


# --------------------------------------------------------------------------- KIO

def kio(*args: str, check: bool = True) -> str:
    cmd = ["kioclient", "--noninteractive", "--platform", "offscreen", *args]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except FileNotFoundError:
        sys.exit("kioclient not found (install kde-cli-tools / kio-extras).")
    if check and res.returncode != 0:
        raise RuntimeError(f"kioclient {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout if res.returncode == 0 else ""


def seg(name: str) -> str:
    """Escape characters that would break a KIO URL path segment."""
    return name.replace("%", "%25").replace("#", "%23").replace("?", "%3F")


def ls(url: str) -> list[str]:
    return [n for n in kio("ls", url + "/", check=False).splitlines() if n not in ("", ".", "..")]


def read_json(url: str):
    text = kio("cat", url, check=False).lstrip("﻿")
    if not text.strip():
        return None
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        # some packs ship comments
        return json.loads(re.sub(r"(?m)^\s*//.*$", "", text), strict=False)


def write_json(url: str, data) -> None:
    """MTP cannot overwrite in place ("Access denied"), so delete + copy."""
    keep = Path(tempfile.mkdtemp(prefix="mc-addons-"))
    old, new = keep / "old.json", keep / url.rsplit("/", 1)[-1]
    old.write_text(kio("cat", url, check=False))
    new.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n")
    kio("remove", url, check=False)
    try:
        kio("copy", str(new), url)
    except RuntimeError as e:
        raise RuntimeError(f"{e}\nOriginal content saved in {old}") from None
    shutil.rmtree(keep)


def device_root() -> str:
    if env := os.environ.get("MC_DEVICE_ROOT"):
        return env.rstrip("/") + "/" + GAME_DIR
    devices = ls("mtp:")
    if not devices:
        sys.exit("No MTP device found. Plug the device in, unlock it and pick "
                 "'File transfer' in the USB notification.")
    if len(devices) > 1:
        sys.exit(f"Several devices found {devices}; set MC_DEVICE_ROOT.")
    dev = f"mtp:/{seg(devices[0])}"
    for storage in ls(dev):
        root = f"{dev}/{seg(storage)}/{GAME_DIR}"
        if ls(root):
            return root
    sys.exit(f"Minecraft data not found on {devices[0]}.")


# --------------------------------------------------------------------- model

def vstr(v) -> str:
    return ".".join(map(str, v)) if isinstance(v, list) else str(v or "?")


@dataclass
class Pack:
    kind: str
    folder: str
    name: str
    uuid: str
    version: list
    deps: list[str]
    pair: list["Pack"] = field(default_factory=list, repr=False)

    @property
    def label(self) -> str:
        return f"[{KINDS.get(self.kind, self.kind)}] {self.name} {vstr(self.version)}"


@dataclass
class World:
    id: str
    name: str
    active: dict[str, list[dict]]


def clean_name(name: str) -> str:
    return re.sub(r"§.", "", name or "").strip()


def parse_manifest(m: dict, kind: str, folder: str) -> Pack | None:
    h = (m or {}).get("header") or {}
    if "uuid" not in h:
        return None
    deps = [d["uuid"] for d in m.get("dependencies", []) if isinstance(d, dict) and "uuid" in d]
    return Pack(kind, folder, clean_name(h.get("name")) or folder, h["uuid"].lower(),
                h.get("version"), [d.lower() for d in deps])


def load_packs(root: str) -> list[Pack]:
    jobs = [(k, f) for k in KINDS for f in ls(f"{root}/{k}")]
    # sequential on purpose: parallel MTP reads through kiod get mixed up
    manifests = [read_json(f"{root}/{k}/{seg(f)}/manifest.json") for k, f in jobs]
    packs = [p for (k, f), m in zip(jobs, manifests) if (p := parse_manifest(m, k, f))]
    by_uuid = {p.uuid: p for p in packs}
    for p in packs:  # pair = installed packs linked by dependency, either direction
        p.pair = [by_uuid[d] for d in p.deps if d in by_uuid]
        p.pair += [q for q in packs if p.uuid in q.deps and q not in p.pair and q is not p]
    return packs


def load_worlds(root: str) -> list[World]:
    base = f"{root}/minecraftWorlds"

    def one(wid: str) -> World:
        w = f"{base}/{seg(wid)}"
        name = kio("cat", f"{w}/levelname.txt", check=False).strip() or wid
        active = {k: read_json(f"{w}/{fn}") or [] for k, fn in WORLD_FILES.items()}
        return World(wid, name, active)

    return [one(wid) for wid in ls(base)]


def usage(worlds: list[World], uuid: str) -> list[World]:
    return [w for w in worlds
            if any(e.get("pack_id", "").lower() == uuid for es in w.active.values() for e in es)]


def resolve_packs(packs: list[Pack], query: str, with_pair: bool = True) -> list[Pack]:
    q = query.lower()
    hits = [p for p in packs if p.uuid.startswith(q)] or \
           [p for p in packs if q in p.name.lower() or q in p.folder.lower()]
    if not hits:
        sys.exit(f"No pack matches '{query}'. See `addons.py list`.")
    names = {p.name for p in hits} | {p.folder for p in hits}
    groups = {frozenset([p.uuid, *(x.uuid for x in p.pair)]) for p in hits}
    if len(groups) > 1 and len(names) > 2:
        sys.exit(f"'{query}' is ambiguous:\n  " + "\n  ".join(f"{p.label}  ({p.folder})" for p in hits))
    out = list(hits)
    if with_pair:
        out += [x for p in hits for x in p.pair if x not in out]
    return out


def resolve_world(worlds: list[World], query: str) -> World:
    hits = [w for w in worlds if w.id == query] or \
           [w for w in worlds if w.name.lower() == query.lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"No world '{query}'. See `addons.py worlds --all`.")
    sys.exit(f"Several worlds are named '{query}', use the id:\n  " +
             "\n  ".join(w.id for w in hits))


def confirm(msg: str, yes: bool) -> None:
    if yes:
        return
    if input(f"{msg} [y/N] ").strip().lower() not in ("y", "yes", "a", "ano"):
        sys.exit("Aborted.")


# ------------------------------------------------------------------ commands

def cmd_list(a) -> None:
    root = device_root()
    packs = load_packs(root)
    worlds = load_worlds(root)
    installed = {p.uuid for p in packs}
    for kind in KINDS:
        print(f"\n{kind}:")
        for p in sorted((p for p in packs if p.kind == kind), key=lambda p: p.name.lower()):
            used = usage(worlds, p.uuid)
            missing = [d for d in p.deps if d not in installed]
            print(f"  {p.name:40} {vstr(p.version):9} {p.uuid[:8]}  "
                  f"worlds: {len(used) or '-':<3} folder: {p.folder}")
            if missing:
                print(f"    ! missing dependency {', '.join(m[:8] for m in missing)}")
    unknown = {e.get("pack_id", "").lower() for w in worlds for es in w.active.values() for e in es}
    unknown -= installed
    if unknown:
        print("\nWorlds reference packs that are not installed (Marketplace / removed):")
        for u in sorted(unknown):
            print(f"  {u[:8]}  in: {', '.join(w.name for w in usage(worlds, u))}")


def cmd_worlds(a) -> None:
    root = device_root()
    by_uuid = {p.uuid: p for p in load_packs(root)}
    for w in sorted(load_worlds(root), key=lambda w: w.name.lower()):
        entries = [e for es in w.active.values() for e in es]
        if not entries and not a.all:
            continue
        names = [by_uuid[e["pack_id"].lower()].label if e.get("pack_id", "").lower() in by_uuid
                 else f"? {e.get('pack_id', '')[:8]}" for e in entries]
        print(f"{w.name}  ({w.id})")
        for n in names:
            print(f"    {n}")


def cmd_backup(a) -> None:
    root = device_root()
    dest = Path(a.dest or Path.home() / "minecraft-backups" / "addons").expanduser()
    dest = dest / dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    dest.mkdir(parents=True, exist_ok=True)
    for kind in [*KINDS, "skin_packs"]:
        if ls(f"{root}/{kind}"):
            print(f"copying {kind} ...")
            kio("copy", f"{root}/{kind}", str(dest) + "/")
    print(f"Backup in {dest}")


def find_pack_dirs(src: Path, work: Path) -> list[Path]:
    """Unpack archives (also nested .mcpack in .mcaddon) and return pack folders."""
    if src.is_file():
        target = work / src.stem
        with zipfile.ZipFile(src) as z:
            z.extractall(target)
        src = target
    for inner in list(src.rglob("*")):
        if inner.suffix.lower() in (".mcpack", ".zip") and inner.is_file():
            with zipfile.ZipFile(inner) as z:
                z.extractall(inner.with_suffix(""))
            inner.unlink()
    found = []
    for mf in sorted(src.rglob("manifest.json"), key=lambda p: len(p.parts)):
        if not any(d in mf.parents for d in found):
            found.append(mf.parent)
    return found


def cmd_install(a) -> None:
    root = device_root()
    packs = load_packs(root)
    by_uuid = {p.uuid: p for p in packs}
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        todo: list[tuple[Pack, Path]] = []
        for f in a.files:
            src = Path(f).expanduser()
            if not src.exists():
                sys.exit(f"{src} does not exist")
            dirs = find_pack_dirs(src, work)
            if not dirs:
                sys.exit(f"{src}: no manifest.json found, not a Bedrock add-on")
            for d in dirs:
                m = json.loads((d / "manifest.json").read_text(encoding="utf-8-sig"), strict=False)
                types = {mod.get("type") for mod in m.get("modules", [])}
                kind = next((MODULE_KIND[t] for t in types if t in MODULE_KIND), None)
                if kind is None:
                    print(f"  skip {d.name}: unsupported pack type {types}")
                    continue
                folder = d.name if d != work / src.stem else src.stem
                if re.fullmatch(r"(?i)(bp|rp|behaviou?r(_pack)?|resources?(_pack)?|data)", folder):
                    folder = f"{src.stem}__{folder}"  # generic name -> prefix with archive
                p = parse_manifest(m, kind, re.sub(r"[^\w.-]+", "_", folder))
                todo.append((p, d))

        for p, d in todo:
            old = by_uuid.get(p.uuid)
            if old and not a.replace:
                print(f"= {p.label} already installed as {old.folder} "
                      f"(v{vstr(old.version)}); use --replace to overwrite")
                continue
            print(f"+ {p.label} -> {p.kind}/{p.folder}")
            if a.dry_run:
                continue
            if old:
                kio("remove", f"{root}/{old.kind}/{seg(old.folder)}")
            existing = set(ls(f"{root}/{p.kind}"))
            while p.folder in existing:
                p.folder += "_"
            stage = work / "stage" / p.folder
            shutil.copytree(d, stage)
            kio("copy", str(stage), f"{root}/{p.kind}/")
            shutil.rmtree(stage)
    if not a.dry_run:
        print("Done. Restart Minecraft on the device, then enable the pack in a world "
              "(game: Edit world > Behavior/Resource packs, or `addons.py enable`).")


def cmd_remove(a) -> None:
    root = device_root()
    packs = load_packs(root)
    targets = resolve_packs(packs, a.pack, with_pair=not a.keep_pair)
    worlds = load_worlds(root)
    print("Will delete from the device:")
    for p in targets:
        print(f"  {p.label}  ({p.kind}/{p.folder})")
    affected = {w.id: w for p in targets for w in usage(worlds, p.uuid)}
    if affected:
        print("and detach it from worlds: " + ", ".join(f"{w.name} ({w.id})" for w in affected.values()))
    confirm("Continue?", a.yes)
    uuids = {p.uuid for p in targets}
    for w in affected.values():
        set_world_packs(root, w, lambda es, _kind: [e for e in es if e.get("pack_id", "").lower() not in uuids])
    for p in targets:
        kio("remove", f"{root}/{p.kind}/{seg(p.folder)}")
        print(f"- removed {p.folder}")


def set_world_packs(root: str, w: World, change) -> None:
    for kind, fn in WORLD_FILES.items():
        new = change(list(w.active[kind]), kind)
        if new != w.active[kind]:
            write_json(f"{root}/minecraftWorlds/{seg(w.id)}/{fn}", new)
            w.active[kind] = new
    # the game lists packs in *_pack_history.json without an icon if they are gone
    active = {e.get("pack_id", "").lower() for es in w.active.values() for e in es}
    for fn in ("world_behavior_pack_history.json", "world_resource_pack_history.json"):
        url = f"{root}/minecraftWorlds/{seg(w.id)}/{fn}"
        hist = read_json(url)
        if not hist or "packs" not in hist:
            continue
        keep = [p for p in hist["packs"] if p.get("uuid", "").lower() in active]
        if len(keep) != len(hist["packs"]):
            write_json(url, {**hist, "packs": keep})


def cmd_enable(a, enable: bool = True) -> None:
    root = device_root()
    packs = load_packs(root)
    targets = resolve_packs(packs, a.pack)
    world = resolve_world(load_worlds(root), a.world)
    uuids = {p.uuid for p in targets}

    def change(entries: list[dict], kind: str) -> list[dict]:
        entries = [e for e in entries if e.get("pack_id", "").lower() not in uuids]
        if enable:  # new packs go on top (highest priority), like the game does
            entries = [{"pack_id": p.uuid, "version": p.version}
                       for p in targets if p.kind == kind] + entries
        return entries

    set_world_packs(root, world, change)
    verb = "enabled in" if enable else "disabled in"
    for p in targets:
        print(f"{p.label} {verb} '{world.name}' ({world.id})")
    if enable:
        print("Note: some add-ons also need experimental toggles (Edit world > Experiments).")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="installed packs").set_defaults(fn=cmd_list)
    s = sub.add_parser("worlds", help="worlds and their packs")
    s.add_argument("--all", action="store_true", help="include worlds without packs")
    s.set_defaults(fn=cmd_worlds)
    s = sub.add_parser("backup", help="copy packs from the device")
    s.add_argument("dest", nargs="?", help="default ~/minecraft-backups/addons")
    s.set_defaults(fn=cmd_backup)
    s = sub.add_parser("install", help="install .mcaddon/.mcpack/.zip/folder")
    s.add_argument("files", nargs="+")
    s.add_argument("--replace", action="store_true", help="overwrite already installed pack")
    s.add_argument("-n", "--dry-run", action="store_true")
    s.set_defaults(fn=cmd_install)
    s = sub.add_parser("remove", help="delete pack (and its pair) from the device")
    s.add_argument("pack")
    s.add_argument("--keep-pair", action="store_true", help="do not remove the paired BP/RP")
    s.add_argument("-y", "--yes", action="store_true")
    s.set_defaults(fn=cmd_remove)
    for name, en in (("enable", True), ("disable", False)):
        s = sub.add_parser(name, help=f"{name} pack (and its pair) in a world")
        s.add_argument("world")
        s.add_argument("pack")
        s.set_defaults(fn=lambda a, en=en: cmd_enable(a, en))
    a = ap.parse_args()
    try:
        a.fn(a)
    except RuntimeError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
