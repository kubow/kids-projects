"""
Minimal MCEdit .schematic reader and placer for Streamlit import use.
"""

from __future__ import annotations

import gzip
import io
import math
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


MODERN_BLOCK_MAP = {
    "minecraft:air": (0, 0),
    "minecraft:stone": (1, 0),
    "minecraft:grass_block": (2, 0),
    "minecraft:dirt": (3, 0),
    "minecraft:cobblestone": (4, 0),
    "minecraft:oak_planks": (5, 0),
    "minecraft:spruce_planks": (5, 1),
    "minecraft:birch_planks": (5, 2),
    "minecraft:jungle_planks": (5, 3),
    "minecraft:oak_sapling": (6, 0),
    "minecraft:bedrock": (7, 0),
    "minecraft:water": (8, 0),
    "minecraft:lava": (10, 0),
    "minecraft:sand": (12, 0),
    "minecraft:gravel": (13, 0),
    "minecraft:gold_ore": (14, 0),
    "minecraft:iron_ore": (15, 0),
    "minecraft:coal_ore": (16, 0),
    "minecraft:oak_log": (17, 0),
    "minecraft:spruce_log": (17, 1),
    "minecraft:birch_log": (17, 2),
    "minecraft:jungle_log": (17, 3),
    "minecraft:oak_leaves": (18, 0),
    "minecraft:spruce_leaves": (18, 1),
    "minecraft:birch_leaves": (18, 2),
    "minecraft:jungle_leaves": (18, 3),
    "minecraft:glass": (20, 0),
    "minecraft:lapis_block": (22, 0),
    "minecraft:sandstone": (24, 0),
    "minecraft:white_bed": (26, 0),
    "minecraft:cobweb": (30, 0),
    "minecraft:short_grass": (31, 1),
    "minecraft:grass": (31, 1),
    "minecraft:white_wool": (35, 0),
    "minecraft:orange_wool": (35, 1),
    "minecraft:magenta_wool": (35, 2),
    "minecraft:light_blue_wool": (35, 3),
    "minecraft:yellow_wool": (35, 4),
    "minecraft:lime_wool": (35, 5),
    "minecraft:pink_wool": (35, 6),
    "minecraft:gray_wool": (35, 7),
    "minecraft:light_gray_wool": (35, 8),
    "minecraft:cyan_wool": (35, 9),
    "minecraft:purple_wool": (35, 10),
    "minecraft:blue_wool": (35, 11),
    "minecraft:brown_wool": (35, 12),
    "minecraft:green_wool": (35, 13),
    "minecraft:red_wool": (35, 14),
    "minecraft:black_wool": (35, 15),
    "minecraft:dandelion": (37, 0),
    "minecraft:poppy": (38, 0),
    "minecraft:brown_mushroom": (39, 0),
    "minecraft:red_mushroom": (40, 0),
    "minecraft:gold_block": (41, 0),
    "minecraft:iron_block": (42, 0),
    "minecraft:double_stone_slab": (43, 0),
    "minecraft:stone_slab": (44, 0),
    "minecraft:brick_block": (45, 0),
    "minecraft:bricks": (45, 0),
    "minecraft:tnt": (46, 0),
    "minecraft:bookshelf": (47, 0),
    "minecraft:mossy_cobblestone": (48, 0),
    "minecraft:obsidian": (49, 0),
    "minecraft:torch": (50, 0),
    "minecraft:fire": (51, 0),
    "minecraft:oak_stairs": (53, 0),
    "minecraft:chest": (54, 0),
    "minecraft:diamond_ore": (56, 0),
    "minecraft:diamond_block": (57, 0),
    "minecraft:crafting_table": (58, 0),
    "minecraft:farmland": (60, 0),
    "minecraft:furnace": (61, 0),
    "minecraft:lit_furnace": (62, 0),
    "minecraft:oak_door": (64, 0),
    "minecraft:ladder": (65, 0),
    "minecraft:cobblestone_stairs": (67, 0),
    "minecraft:snow": (78, 0),
    "minecraft:ice": (79, 0),
    "minecraft:snow_block": (80, 0),
    "minecraft:cactus": (81, 0),
    "minecraft:clay": (82, 0),
    "minecraft:sugar_cane": (83, 0),
    "minecraft:fence": (85, 0),
    "minecraft:glowstone": (89, 0),
    "minecraft:stone_bricks": (98, 0),
    "minecraft:glass_pane": (102, 0),
    "minecraft:melon": (103, 0),
    "minecraft:fence_gate": (107, 0),
}


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


def _signed_to_unsigned_64(value: int) -> int:
    return value & 0xFFFFFFFFFFFFFFFF


def _decode_packed_blockstates(values, palette_size: int, total_blocks: int):
    bits_per_block = max(2, math.ceil(math.log2(max(1, palette_size))))
    mask = (1 << bits_per_block) - 1
    decoded = []
    bit_buffer = 0
    bits_in_buffer = 0

    for value in values:
        bit_buffer |= _signed_to_unsigned_64(value) << bits_in_buffer
        bits_in_buffer += 64
        while bits_in_buffer >= bits_per_block and len(decoded) < total_blocks:
            decoded.append(bit_buffer & mask)
            bit_buffer >>= bits_per_block
            bits_in_buffer -= bits_per_block

    if len(decoded) < total_blocks:
        raise ValueError("Packed schematic block states ended before filling the declared volume.")
    return decoded[:total_blocks]


def _palette_entry_to_block(entry, index: int):
    name = entry.get("Name", f"palette:{index}")
    mapped = MODERN_BLOCK_MAP.get(name)
    if mapped is not None:
        block_id, block_data = mapped
        return block_id, block_data, name
    return 1000 + index, 0, name


def _load_region_schematic(root):
    regions = root.get("Regions")
    if not regions:
        raise ValueError("Schematic contains no regions.")

    region_name, region = next(iter(regions.items()))
    size = region["Size"]
    width = abs(int(size["x"]))
    height = abs(int(size["y"]))
    length = abs(int(size["z"]))
    total_blocks = width * height * length

    palette = region["BlockStatePalette"]
    packed_states = region["BlockStates"]
    state_indices = _decode_packed_blockstates(packed_states, len(palette), total_blocks)

    palette_map = {}
    palette_names = {}
    for index, entry in enumerate(palette):
        block_id, block_data, block_name = _palette_entry_to_block(entry, index)
        palette_map[index] = (block_id, block_data)
        palette_names[block_id] = block_name

    blocks = []
    data = []
    for state_index in state_indices:
        block_id, block_data = palette_map.get(state_index, (0, 0))
        blocks.append(block_id)
        data.append(block_data)

    metadata = root.get("Metadata", {})
    return {
        "width": width,
        "height": height,
        "length": length,
        "materials": metadata.get("Name", region_name),
        "blocks": blocks,
        "data": data,
        "block_names": palette_names,
    }


def load_schematic(file_bytes: bytes):
    raw = _decompress_schematic_bytes(file_bytes)
    _, root = NBTReader(raw).read_named_root()
    if "Regions" in root:
        return _load_region_schematic(root)
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
        "block_names": {},
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
        "block_names": schematic.get("block_names", {}),
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
    normalized["block_names"] = dict(normalized["block_names"])

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
        "top_unsupported_blocks": [
            {
                "block_id": block_id,
                "count": count,
                "name": schematic["block_names"].get(block_id, "unknown"),
            }
            for block_id, count in sorted(unsupported.items(), key=lambda item: item[1], reverse=True)[:10]
        ],
    }
