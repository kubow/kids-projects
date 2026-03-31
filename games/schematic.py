"""
Minimal MCEdit .schematic reader and placer for Streamlit import use.
"""

from __future__ import annotations

import gzip
import io
import struct
from collections import Counter


TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12


class NBTReader:
    def __init__(self, data: bytes):
        self.buffer = io.BytesIO(data)

    def _read(self, size: int) -> bytes:
        data = self.buffer.read(size)
        if len(data) != size:
            raise ValueError("Unexpected end of NBT data.")
        return data

    def _read_byte(self) -> int:
        return struct.unpack(">b", self._read(1))[0]

    def _read_unsigned_byte(self) -> int:
        return struct.unpack(">B", self._read(1))[0]

    def _read_short(self) -> int:
        return struct.unpack(">h", self._read(2))[0]

    def _read_int(self) -> int:
        return struct.unpack(">i", self._read(4))[0]

    def _read_long(self) -> int:
        return struct.unpack(">q", self._read(8))[0]

    def _read_float(self) -> float:
        return struct.unpack(">f", self._read(4))[0]

    def _read_double(self) -> float:
        return struct.unpack(">d", self._read(8))[0]

    def _read_string(self) -> str:
        length = self._read_short()
        return self._read(length).decode("utf-8")

    def _read_tag_payload(self, tag_type: int):
        if tag_type == TAG_BYTE:
            return self._read_byte()
        if tag_type == TAG_SHORT:
            return self._read_short()
        if tag_type == TAG_INT:
            return self._read_int()
        if tag_type == TAG_LONG:
            return self._read_long()
        if tag_type == TAG_FLOAT:
            return self._read_float()
        if tag_type == TAG_DOUBLE:
            return self._read_double()
        if tag_type == TAG_BYTE_ARRAY:
            length = self._read_int()
            return self._read(length)
        if tag_type == TAG_STRING:
            return self._read_string()
        if tag_type == TAG_LIST:
            item_type = self._read_unsigned_byte()
            length = self._read_int()
            return [self._read_tag_payload(item_type) for _ in range(length)]
        if tag_type == TAG_COMPOUND:
            result = {}
            while True:
                nested_type = self._read_unsigned_byte()
                if nested_type == TAG_END:
                    return result
                nested_name = self._read_string()
                result[nested_name] = self._read_tag_payload(nested_type)
        if tag_type == TAG_INT_ARRAY:
            length = self._read_int()
            return [self._read_int() for _ in range(length)]
        if tag_type == TAG_LONG_ARRAY:
            length = self._read_int()
            return [self._read_long() for _ in range(length)]
        raise ValueError(f"Unsupported NBT tag type: {tag_type}")

    def read_named_root(self):
        tag_type = self._read_unsigned_byte()
        if tag_type == TAG_END:
            raise ValueError("NBT root tag is empty.")
        name = self._read_string()
        payload = self._read_tag_payload(tag_type)
        return name, payload


def _decompress_schematic_bytes(data: bytes) -> bytes:
    try:
        return gzip.decompress(data)
    except OSError:
        return data


def load_schematic(file_bytes: bytes):
    raw = _decompress_schematic_bytes(file_bytes)
    _, root = NBTReader(raw).read_named_root()
    width = root.get("Width", root.get("width"))
    height = root.get("Height", root.get("height"))
    length = root.get("Length", root.get("length"))
    blocks = root.get("Blocks", root.get("blocks"))
    data = root.get("Data", root.get("data"))
    materials = root.get("Materials", root.get("materials", "Unknown"))
    add_blocks = root.get("AddBlocks", root.get("addBlocks"))

    missing = [
        key for key, value in {
            "Width": width,
            "Height": height,
            "Length": length,
            "Blocks": blocks,
            "Data": data,
        }.items()
        if value is None
    ]
    if missing:
        raise ValueError(
            "This file does not look like a supported MCEdit .schematic file. "
            f"Missing field(s): {', '.join(missing)}."
        )

    if add_blocks:
        merged_blocks = []
        for index, block_id in enumerate(blocks):
            add_byte = add_blocks[index // 2]
            add_bits = (add_byte & 0x0F) if index % 2 == 0 else (add_byte >> 4) & 0x0F
            merged_blocks.append((add_bits << 8) | block_id)
        blocks = merged_blocks
    else:
        blocks = list(blocks)

    return {
        "width": width,
        "height": height,
        "length": length,
        "materials": materials,
        "blocks": blocks,
        "data": list(data),
    }


def normalize_schematic(schematic):
    if not isinstance(schematic, dict):
        raise ValueError("Uploaded schematic data is not in the expected format.")

    normalized = {
        "width": schematic.get("width", schematic.get("Width")),
        "height": schematic.get("height", schematic.get("Height")),
        "length": schematic.get("length", schematic.get("Length")),
        "materials": schematic.get("materials", schematic.get("Materials", "Unknown")),
        "blocks": schematic.get("blocks", schematic.get("Blocks")),
        "data": schematic.get("data", schematic.get("Data")),
    }

    missing = [key for key in ("width", "height", "length", "blocks", "data") if normalized[key] is None]
    if missing:
        raise ValueError(
            "This file does not look like a supported MCEdit .schematic file. "
            f"Missing field(s): {', '.join(missing)}."
        )

    normalized["width"] = int(normalized["width"])
    normalized["height"] = int(normalized["height"])
    normalized["length"] = int(normalized["length"])
    normalized["blocks"] = list(normalized["blocks"])
    normalized["data"] = list(normalized["data"])

    expected = normalized["width"] * normalized["height"] * normalized["length"]
    if len(normalized["blocks"]) != expected or len(normalized["data"]) != expected:
        raise ValueError(
            "Schematic block data size does not match its dimensions. "
            f"Expected {expected} entries, got {len(normalized['blocks'])} blocks and {len(normalized['data'])} data values."
        )

    return normalized


def iter_schematic_blocks(schematic):
    schematic = normalize_schematic(schematic)
    width = schematic["width"]
    height = schematic["height"]
    length = schematic["length"]
    blocks = schematic["blocks"]
    data = schematic["data"]

    for y in range(height):
        for z in range(length):
            for x in range(width):
                index = x + z * width + y * width * length
                yield x, y, z, int(blocks[index]), int(data[index])


def place_schematic(mc, origin_x: int, origin_y: int, origin_z: int, schematic, allowed_block_ids, fallback_block_id):
    schematic = normalize_schematic(schematic)
    placed = 0
    replaced = 0
    skipped = 0

    for dx, dy, dz, block_id, block_data in iter_schematic_blocks(schematic):
        if block_id == 0:
            continue

        target_block_id = block_id
        target_block_data = block_data

        if block_id not in allowed_block_ids:
            if fallback_block_id is None:
                skipped += 1
                continue
            target_block_id = int(fallback_block_id)
            target_block_data = 0
            replaced += 1

        mc.setBlock(origin_x + dx, origin_y + dy, origin_z + dz, target_block_id, target_block_data)
        placed += 1

    return {
        "placed": placed,
        "replaced": replaced,
        "skipped": skipped,
    }


def summarize_schematic(schematic, allowed_block_ids):
    schematic = normalize_schematic(schematic)
    counts = Counter(block_id for block_id in schematic["blocks"] if block_id != 0)
    unsupported = {block_id: count for block_id, count in counts.items() if block_id not in allowed_block_ids}

    return {
        "dimensions": (schematic["width"], schematic["height"], schematic["length"]),
        "materials": schematic["materials"],
        "non_air_blocks": int(sum(counts.values())),
        "unique_non_air_blocks": len(counts),
        "unsupported_unique_blocks": len(unsupported),
        "unsupported_total_blocks": int(sum(unsupported.values())),
        "top_blocks": counts.most_common(10),
        "top_unsupported_blocks": sorted(unsupported.items(), key=lambda item: item[1], reverse=True)[:10],
    }
