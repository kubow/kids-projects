#!/usr/bin/env python3
"""Turn on the "Beta APIs" experiment in Bedrock worlds (edits level.dat).

Add-ons whose scripts depend on a `-beta` script module (e.g. ThatMob's Verity:
`@minecraft/server 2.12.0-beta`) load silently without their scripts when the
world does not have Experiments -> Beta APIs on. For Verity that means the mob
stands still and never answers in chat (all its movement/chat is scripted).

Sets experiments.gametest = 1 (+ experiments_ever_used, saved_with_toggled_experiments),
writes level.dat and level.dat_old, keeps a backup `level.dat.bak-beta-apis`.
Close Minecraft first - the game rewrites level.dat on save.

    python enable_beta_apis.py [--pc] [--dry-run] (--pack UUID | WORLD_DIR...)

    --pack UUID   all worlds that have this behavior pack enabled
    --pc          worlds dir of mcpelauncher (default when --pack is used)
"""

import argparse
import shutil
import struct
import sys
from pathlib import Path

PC_WORLDS = Path.home() / ".local/share/mcpelauncher/games/com.mojang/minecraftWorlds"

# --- minimal typed little-endian NBT (Bedrock) -------------------------------
FMT = {1: "<b", 2: "<h", 3: "<i", 4: "<q", 5: "<f", 6: "<d"}


def read(d, p, t):
    if t in FMT:
        return struct.unpack_from(FMT[t], d, p)[0], p + struct.calcsize(FMT[t])
    if t in (7, 11, 12):
        n, p = struct.unpack_from("<i", d, p)[0], p + 4
        size = {7: 1, 11: 4, 12: 8}[t]
        return d[p:p + n * size], p + n * size  # raw bytes, round-trips as-is
    if t == 8:
        n, p = struct.unpack_from("<H", d, p)[0], p + 2
        return d[p:p + n], p + n
    if t == 9:
        et, n = d[p], struct.unpack_from("<i", d, p + 1)[0]
        p += 5
        items = []
        for _ in range(n):
            v, p = read(d, p, et)
            items.append(v)
        return (et, items), p
    if t == 10:
        out = []  # list of (type, name, value) - keeps order
        while True:
            tt = d[p]
            p += 1
            if tt == 0:
                return out, p
            name, p = read(d, p, 8)
            v, p = read(d, p, tt)
            out.append([tt, name, v])
    raise ValueError(f"unknown NBT tag {t}")


def write(t, v):
    if t in FMT:
        return struct.pack(FMT[t], v)
    if t in (7, 11, 12):
        return struct.pack("<i", len(v) // {7: 1, 11: 4, 12: 8}[t]) + v
    if t == 8:
        return struct.pack("<H", len(v)) + v
    if t == 9:
        et, items = v
        return bytes([et]) + struct.pack("<i", len(items)) + b"".join(write(et, i) for i in items)
    if t == 10:
        return b"".join(bytes([tt]) + write(8, n) + write(tt, x) for tt, n, x in v) + b"\0"
    raise ValueError(t)


def load(path: Path):
    raw = path.read_bytes()
    header_ver = raw[:4]
    body = raw[8:]
    assert body[0] == 10, "level.dat root is not a compound"
    name, p = read(body, 1, 8)
    root, _ = read(body, p, 10)
    if 10 .to_bytes(1, "little") + write(8, name) + write(10, root) != body:
        raise RuntimeError("NBT round-trip mismatch, refusing to edit")
    return header_ver, name, root


def save(path: Path, header_ver, name, root):
    body = bytes([10]) + write(8, name) + write(10, root)
    path.write_bytes(header_ver + struct.pack("<i", len(body)) + body)


def set_byte(compound, key: str, value: int) -> bool:
    k = key.encode()
    for tag in compound:
        if tag[1] == k:
            changed = tag[2] != value
            tag[0], tag[2] = 1, value
            return changed
    compound.append([1, k, value])
    return True


def enable(world: Path, dry_run: bool) -> str:
    lvl = world / "level.dat"
    ver, name, root = load(lvl)
    exp = next((t for t in root if t[1] == b"experiments"), None)
    if exp is None:
        exp = [10, b"experiments", []]
        root.append(exp)
    changed = False
    for key in ("gametest", "experiments_ever_used", "saved_with_toggled_experiments"):
        changed |= set_byte(exp[2], key, 1)
    if not changed:
        return "already on"
    if dry_run:
        return "would enable"
    bak = world / "level.dat.bak-beta-apis"
    if not bak.exists():
        shutil.copy2(lvl, bak)
    save(lvl, ver, name, root)
    shutil.copy2(lvl, world / "level.dat_old")
    load(lvl)  # re-parse to be sure
    return "enabled"


def worlds_with_pack(uuid: str):
    for w in sorted(PC_WORLDS.iterdir()):
        f = w / "world_behavior_packs.json"
        if f.exists() and uuid in f.read_text(errors="replace"):
            yield w


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("worlds", nargs="*", type=Path)
    ap.add_argument("--pack")
    ap.add_argument("--pc", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    worlds = list(worlds_with_pack(a.pack)) if a.pack else [
        (PC_WORLDS / w if a.pc else w) for w in a.worlds]
    if not worlds:
        ap.error("no worlds given / found")
    for w in worlds:
        name = (w / "levelname.txt").read_text(errors="replace").strip() if (w / "levelname.txt").exists() else ""
        try:
            print(f"{w.name:15} {enable(w, a.dry_run):13} {name}")
        except Exception as e:  # keep going with other worlds
            print(f"{w.name:15} ERROR {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
