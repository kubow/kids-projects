#!/usr/bin/env python3
"""Patch "Mr. Nido's Guns Add-on.mcaddon" (v1.0.0) for Bedrock 1.26.x.

The add-on is a cut-down copy of the author's superhero add-on and its player
files carry leftovers that flood the content log (~6M errors per session) and
break player animations / skins:

1. Resource pack reads player properties that the behavior pack never defines
   (arathnido:ability0/attacks/custom_riding/escalar/suit_ability3, nido:flying).
   A failing Molang expression evaluates to 0, so e.g. `off_riding` came out
   false. Replaced by the default value 0 (what the original add-on intended).
2. Behavior pack reads the never-defined `guns:shoot` property (replaced by
   `arathnido:animation` in the current version) -> replaced by 0, behavior
   unchanged (the transition could never fire anyway).
3. Typo `slot.weapon.maindhand` -> `slot.weapon.mainhand`.
4. Player render list references two render controllers that do not exist
   (`*.reed_richards.third_person`) -> removed.
5. 22 attachment scripts run every tick and crash with "cannot read property
   'typeId' of undefined" whenever the main hand is empty -> null check.

Version is bumped to 1.0.1 so the game does not keep a cached 1.0.0.

    python fix_nido_guns.py "Mr. Nido's Guns Add-on.mcaddon" [OUT.mcaddon]
"""

import io
import json
import re
import sys
import zipfile
from pathlib import Path

DEAD_PROPS = ["arathnido:ability0", "arathnido:attacks", "arathnido:custom_riding",
              "arathnido:escalar", "arathnido:suit_ability3", "nido:flying", "guns:shoot"]
DEAD_PROP_RE = re.compile(r"q(?:uery)?\.property\('(%s)'\)" % "|".join(map(re.escape, DEAD_PROPS)))
MISSING_RC_RE = re.compile(r"\s*\{\s*\"controller\.render\.player(?:_base)?\.reed_richards\.third_person\"[^}]*\},")


def lenient_json(text: str):
    return json.loads(re.sub(r"(?m)^\s*//.*$", "", text), strict=False)


def patch_file(name: str, text: str, stats: dict) -> str:
    orig = text
    if name.endswith(".json"):
        text, n = DEAD_PROP_RE.subn("0", text)
        stats["dead property reads -> 0"] += n
        n = text.count("slot.weapon.maindhand")
        text = text.replace("slot.weapon.maindhand", "slot.weapon.mainhand")
        stats["maindhand typo"] += n
        if name.endswith("entity/player.entity.json"):
            text, n = MISSING_RC_RE.subn("", text)
            stats["missing render controllers removed"] += n
        if name.endswith("manifest.json"):
            m = lenient_json(text)
            m["header"]["version"] = [1, 0, 1]
            for d in m.get("dependencies", []):
                if "uuid" in d:
                    d["version"] = [1, 0, 1]
            m["header"]["description"] += " (patched: 1.26 fixes)"
            text = json.dumps(m, indent=2, ensure_ascii=False) + "\n"
            stats["manifests bumped to 1.0.1"] += 1
        if text != orig:
            lenient_json(text)  # must still parse
    elif name.endswith(".js"):
        text, n = re.subn(r"if \(mainhand\.typeId ==", "if (mainhand && mainhand.typeId ==", text)
        stats["script null checks"] += n
    return text


def patch_pack(data: bytes, stats: dict) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(data)) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            raw = zin.read(info)
            if info.filename.endswith((".json", ".js")):
                text = raw.decode("utf-8-sig")
                new = patch_file(info.filename, text, stats)
                if new != text:
                    raw = new.encode()
                    stats["files changed"] += 1
            zout.writestr(info.filename, raw)
    return out.getvalue()


def main() -> None:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + " (fixed).mcaddon")
    stats: dict = {k: 0 for k in ["files changed", "dead property reads -> 0", "maindhand typo",
                                  "missing render controllers removed", "script null checks",
                                  "manifests bumped to 1.0.1"]}
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_STORED) as zout:
        for info in zin.infolist():
            data = zin.read(info)
            if info.filename.endswith(".mcpack"):
                data = patch_pack(data, stats)
            zout.writestr(info.filename, data)
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"-> {dst}")


if __name__ == "__main__":
    main()
