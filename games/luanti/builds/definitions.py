"""Predefined builds for Luanti via Miney."""

from .blocks import NODES
from .world import LuantiWorld


def build_simple_house(world, x, y, z, width=5, depth=4, height=3, roof_height=2):
    x2 = x + width - 1
    z2 = z + depth - 1
    wood = NODES["wood"]
    brick = NODES["brick"]
    air = NODES["air"]
    glass = NODES["glass"]
    world.set_blocks(x, y, z, x2, y, z2, wood)
    world.set_blocks(x, y + 1, z, x2, y + height, z2, brick)
    world.set_blocks(x + 1, y + 1, z + 1, x2 - 1, y + height - 1, z2 - 1, air)
    world.set_block(x + width // 2, y + 1, z, air)
    world.set_block(x + width // 2, y + 2, z, air)
    world.set_block(x, y + 2, z + depth // 2, glass)
    world.set_block(x2, y + 2, z + depth // 2, glass)
    for i in range(roof_height):
        world.set_blocks(x + i, y + height + i, z + i, x2 - i, y + height + i, z2 - i, wood)


def build_tower(world, x, y, z, radius=2, height=10):
    stone = NODES["stone"]
    air = NODES["air"]
    world.set_blocks(x - radius, y, z - radius, x + radius, y + height - 1, z + radius, stone)
    world.set_blocks(
        x - radius + 1, y + 1, z - radius + 1,
        x + radius - 1, y + height - 1, z + radius - 1,
        air,
    )


def build_wall(world, x, y, z, length=10, height=2):
    world.set_blocks(x, y, z, x, y + height - 1, z + length - 1, NODES["stone"])


def build_pyramid(world, x, y, z, base_size=5, height=None):
    stone = NODES["sandstone"]
    h = height if height is not None else base_size
    for level in range(h):
        s = base_size - level
        if s < 1:
            break
        world.set_blocks(x - s, y + level, z - s, x + s, y + level, z + s, stone)
    world.set_block(x, y + h, z, stone)


def build_platform(world, x, y, z, width=5, depth=5):
    world.set_blocks(x, y, z, x + width - 1, y, z + depth - 1, NODES["wood"])


def build_pillar(world, x, y, z, height=6):
    world.set_blocks(x, y, z, x, y + height - 1, z, NODES["stone"])


def build_tree_oak(world, x, y, z, height=5):
    trunk_top = y + height - 1
    world.set_blocks(x, y, z, x, trunk_top, z, NODES["tree"])
    world.set_blocks(x - 2, trunk_top - 1, z - 2, x + 2, trunk_top + 1, z + 2, NODES["leaves"])
    world.set_blocks(x - 1, trunk_top + 2, z - 1, x + 1, trunk_top + 2, z + 1, NODES["leaves"])


def build_campfire(world, x, y, z):
    stone = NODES["cobblestone"]
    mese = NODES["mese"]
    world.set_blocks(x - 1, y, z - 1, x + 1, y, z + 1, stone)
    world.set_block(x, y + 1, z, mese)


def build_castle_gate(world, x, y, z, width=7, height=5):
    brick = NODES["stonebrick"]
    air = NODES["air"]
    torch = NODES["torch"]
    tower_height = height + 2
    left_x = x
    right_x = x + width - 1
    gate_left = x + 2
    gate_right = x + width - 3
    world.set_blocks(left_x, y, z, left_x + 1, y + tower_height - 1, z + 1, brick)
    world.set_blocks(right_x - 1, y, z, right_x, y + tower_height - 1, z + 1, brick)
    world.set_blocks(gate_left, y + height - 1, z, gate_right, y + height, z + 1, brick)
    world.set_blocks(gate_left, y, z, gate_right, y + height - 2, z + 1, air)
    world.set_block(left_x + 1, y + tower_height - 1, z, torch)
    world.set_block(right_x - 1, y + tower_height - 1, z, torch)


def build_smiley(world, x, y, z, size=7):
    s = max(5, size)
    x2 = x + s - 1
    y2 = y + s - 1
    sand = NODES["sand"]
    obsidian = NODES["obsidian"]
    world.set_blocks(x, y, z, x2, y2, z, sand)
    world.set_blocks(x + 1, y + 1, z, x2 - 1, y2 - 1, z, NODES["air"])
    eye_y = y + s - 3
    world.set_block(x + 1, eye_y, z, obsidian)
    world.set_block(x2 - 1, eye_y, z, obsidian)
    mouth_y = y + 1
    world.set_blocks(x + 1, mouth_y, z, x2 - 1, mouth_y, z, obsidian)


BUILDS = [
    {
        "id": "simple_house",
        "name": "Simple house",
        "description": "Small house with door, windows, and wooden roof",
        "fn": build_simple_house,
        "params": [],
    },
    {
        "id": "tower",
        "name": "Tower",
        "description": "Hollow stone tower",
        "fn": build_tower,
        "params": [("radius", "int", 2, "Radius"), ("height", "int", 10, "Height")],
    },
    {
        "id": "wall",
        "name": "Wall",
        "description": "Straight stone wall",
        "fn": build_wall,
        "params": [("length", "int", 10, "Length"), ("height", "int", 2, "Height")],
    },
    {
        "id": "pyramid",
        "name": "Pyramid",
        "description": "Stepped sandstone pyramid",
        "fn": build_pyramid,
        "params": [("base_size", "int", 5, "Base size")],
    },
    {
        "id": "platform",
        "name": "Platform",
        "description": "Flat wooden platform",
        "fn": build_platform,
        "params": [("width", "int", 5, "Width"), ("depth", "int", 5, "Depth")],
    },
    {
        "id": "pillar",
        "name": "Pillar",
        "description": "Single stone column",
        "fn": build_pillar,
        "params": [("height", "int", 6, "Height")],
    },
    {
        "id": "tree_oak",
        "name": "Oak tree",
        "description": "Trunk and leaf canopy",
        "fn": build_tree_oak,
        "params": [("height", "int", 5, "Trunk height")],
    },
    {
        "id": "campfire",
        "name": "Campfire",
        "description": "Stone ring with glowing center",
        "fn": build_campfire,
        "params": [],
    },
    {
        "id": "castle_gate",
        "name": "Castle gate",
        "description": "Two towers with archway",
        "fn": build_castle_gate,
        "params": [("width", "int", 7, "Width"), ("height", "int", 5, "Gate height")],
    },
    {
        "id": "smiley",
        "name": "Smiley pixel art",
        "description": "Flat smiley face on a wall",
        "fn": build_smiley,
        "params": [("size", "int", 7, "Canvas size")],
    },
]

BUILD_ICONS = {
    "simple_house": "🏠",
    "tower": "🗼",
    "wall": "🧱",
    "pyramid": "🔺",
    "platform": "📦",
    "pillar": "🪵",
    "tree_oak": "🌳",
    "campfire": "🔥",
    "castle_gate": "🏰",
    "smiley": "🙂",
}


def get_build(build_id):
    for build in BUILDS:
        if build["id"] == build_id:
            return build
    return None
