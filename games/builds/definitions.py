"""
Predefined build definitions for Minecraft Pi Edition API.
Uses mcpi and optionally minecraftstuff (MinecraftDrawing) for shapes.
Reference: https://pimylifeup.com/minecraft-pi-edition-api-reference/
"""

from mcpi import block as block_constants

# Optional: minecraftstuff for spheres, circles, lines
try:
    from minecraftstuff import MinecraftDrawing
    HAS_MINECRAFT_STUFF = True
except ImportError:
    HAS_MINECRAFT_STUFF = False


def _get_mcdraw(mc):
    if not HAS_MINECRAFT_STUFF:
        return None
    return MinecraftDrawing(mc)


# --- Simple builds using only mcpi setBlock/setBlocks ---

def build_simple_house(mc, x, y, z, width=5, depth=4, height=3, roof_height=2):
    """A small house with walls, wooden roof, and glass."""
    # Floor
    mc.setBlocks(x, y, z, x + width, y, z + depth, block_constants.WOOD_PLANKS.id)
    # Walls
    mc.setBlocks(x, y + 1, z, x + width, y + height, z + depth, block_constants.BRICK_BLOCK.id)
    # Hollow interior
    mc.setBlocks(x + 1, y + 1, z + 1, x + width - 1, y + height - 1, z + depth - 1, block_constants.AIR.id)
    # Door
    mc.setBlock(x + width // 2, y + 1, z, block_constants.AIR.id)
    mc.setBlock(x + width // 2, y + 2, z, block_constants.AIR.id)
    # Windows
    mc.setBlocks(x, y + 2, z + depth // 2, x, y + 2, z + depth // 2, block_constants.GLASS.id)
    mc.setBlocks(x + width, y + 2, z + depth // 2, x + width, y + 2, z + depth // 2, block_constants.GLASS.id)
    # Roof (stepped pyramid)
    for i in range(roof_height):
        mc.setBlocks(x + i, y + height + i, z + i, x + width - i, y + height + i, z + depth - i, block_constants.WOOD.id, 0)


def build_tower(mc, x, y, z, radius=2, height=10, material_id=None):
    """A cylindrical tower (square footprint for simplicity)."""
    bid = material_id or block_constants.STONE.id
    mc.setBlocks(x - radius, y, z - radius, x + radius, y + height, z + radius, bid)
    # Hollow
    mc.setBlocks(x - radius + 1, y + 1, z - radius + 1, x + radius - 1, y + height - 1, z + radius - 1, block_constants.AIR.id)


def build_wall(mc, x, y, z, length=10, height=2, material_id=None):
    """A straight wall (1 block thick)."""
    bid = material_id or block_constants.STONE.id
    mc.setBlocks(x, y, z, x, y + height - 1, z + length - 1, bid)


def build_pyramid(mc, x, y, z, base_size=5, height=None, material_id=None):
    """A stepped pyramid. height defaults to base_size."""
    bid = material_id or block_constants.SANDSTONE.id
    h = height if height is not None else base_size
    for level in range(h):
        s = base_size - level
        if s < 1:
            break
        mc.setBlocks(x - s, y + level, z - s, x + s, y + level, z + s, bid)
    # Top block
    mc.setBlock(x, y + h, z, bid)


def build_platform(mc, x, y, z, width=5, depth=5, material_id=None):
    """A flat platform."""
    bid = material_id or block_constants.WOOD_PLANKS.id
    mc.setBlocks(x, y, z, x + width - 1, y, z + depth - 1, bid)


def build_pillar(mc, x, y, z, height=6, material_id=None):
    """A single-column pillar."""
    bid = material_id or block_constants.STONE.id
    mc.setBlocks(x, y, z, x, y + height - 1, z, bid)


# --- Builds using minecraftstuff MinecraftDrawing ---

def build_sphere(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Filled sphere (requires minecraftstuff)."""
    mcdraw = _get_mcdraw(mc)
    if mcdraw is None:
        mc.postToChat("Install minecraftstuff for spheres: pip install minecraftstuff")
        return
    bid = material_id or block_constants.GLOWSTONE_BLOCK.id
    mcdraw.drawSphere(x, y, z, radius, bid, material_data)


def build_hollow_sphere(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Hollow sphere (requires minecraftstuff)."""
    mcdraw = _get_mcdraw(mc)
    if mcdraw is None:
        mc.postToChat("Install minecraftstuff for hollow spheres")
        return
    bid = material_id or block_constants.GLASS.id
    mcdraw.drawHollowSphere(x, y, z, radius, bid, material_data)


def build_circle(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Vertical circle in Y plane (requires minecraftstuff)."""
    mcdraw = _get_mcdraw(mc)
    if mcdraw is None:
        mc.postToChat("Install minecraftstuff for circles")
        return
    bid = material_id or block_constants.WOOL.id
    mcdraw.drawCircle(x, y, z, radius, bid, material_data)


def build_horizontal_circle(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Horizontal circle (requires minecraftstuff)."""
    mcdraw = _get_mcdraw(mc)
    if mcdraw is None:
        mc.postToChat("Install minecraftstuff for circles")
        return
    bid = material_id or block_constants.WOOL.id
    mcdraw.drawHorizontalCircle(x, y, z, radius, bid, material_data)


def build_line(mc, x, y, z, x2=None, y2=None, z2=None, dx=10, dy=0, dz=0, material_id=None, material_data=0):
    """Line from (x,y,z) to (x2,y2,z2) or (x+dx, y+dy, z+dz) if x2 is None (requires minecraftstuff)."""
    mcdraw = _get_mcdraw(mc)
    if mcdraw is None:
        mc.postToChat("Install minecraftstuff for lines")
        return
    if x2 is None:
        x2, y2, z2 = x + dx, y + dy, z + dz
    bid = material_id or block_constants.GLOWSTONE_BLOCK.id
    mcdraw.drawLine(int(x), int(y), int(z), int(x2), int(y2), int(z2), bid, material_data)


# --- Registry for the Streamlit UI ---

BUILDS = [
    {
        "id": "simple_house",
        "name": "Simple House",
        "description": "Small house with walls, roof, door and windows",
        "fn": build_simple_house,
        "uses_stuff": False,
        "params": [
            ("width", "int", 5, "Width (blocks)"),
            ("depth", "int", 4, "Depth (blocks)"),
            ("height", "int", 3, "Wall height"),
            ("roof_height", "int", 2, "Roof layers"),
        ],
    },
    {
        "id": "tower",
        "name": "Tower",
        "description": "Cylindrical tower (square footprint)",
        "fn": build_tower,
        "uses_stuff": False,
        "params": [
            ("radius", "int", 2, "Radius (blocks)"),
            ("height", "int", 10, "Height (blocks)"),
        ],
    },
    {
        "id": "wall",
        "name": "Wall",
        "description": "Straight wall",
        "fn": build_wall,
        "uses_stuff": False,
        "params": [
            ("length", "int", 10, "Length (blocks)"),
            ("height", "int", 2, "Height (blocks)"),
        ],
    },
    {
        "id": "pyramid",
        "name": "Pyramid",
        "description": "Stepped pyramid",
        "fn": build_pyramid,
        "uses_stuff": False,
        "params": [
            ("base_size", "int", 5, "Base half-size (blocks)"),
            ("height", "int", 5, "Height (blocks)"),
        ],
    },
    {
        "id": "platform",
        "name": "Platform",
        "description": "Flat platform",
        "fn": build_platform,
        "uses_stuff": False,
        "params": [
            ("width", "int", 5, "Width (blocks)"),
            ("depth", "int", 5, "Depth (blocks)"),
        ],
    },
    {
        "id": "pillar",
        "name": "Pillar",
        "description": "Single block pillar",
        "fn": build_pillar,
        "uses_stuff": False,
        "params": [
            ("height", "int", 6, "Height (blocks)"),
        ],
    },
    {
        "id": "sphere",
        "name": "Sphere",
        "description": "Filled sphere (minecraftstuff)",
        "fn": build_sphere,
        "uses_stuff": True,
        "params": [
            ("radius", "int", 5, "Radius (blocks)"),
        ],
    },
    {
        "id": "hollow_sphere",
        "name": "Hollow Sphere",
        "description": "Hollow sphere (minecraftstuff)",
        "fn": build_hollow_sphere,
        "uses_stuff": True,
        "params": [
            ("radius", "int", 5, "Radius (blocks)"),
        ],
    },
    {
        "id": "circle",
        "name": "Circle (vertical)",
        "description": "Circle in Y plane (minecraftstuff)",
        "fn": build_circle,
        "uses_stuff": True,
        "params": [
            ("radius", "int", 5, "Radius (blocks)"),
        ],
    },
    {
        "id": "horizontal_circle",
        "name": "Circle (horizontal)",
        "description": "Horizontal circle (minecraftstuff)",
        "fn": build_horizontal_circle,
        "uses_stuff": True,
        "params": [
            ("radius", "int", 5, "Radius (blocks)"),
        ],
    },
    {
        "id": "line",
        "name": "Line",
        "description": "Line between two points (minecraftstuff). Start = position, end = position + (dx,dy,dz)",
        "fn": build_line,
        "uses_stuff": True,
        "params": [
            ("dx", "int", 10, "End X offset (blocks)"),
            ("dy", "int", 0, "End Y offset (blocks)"),
            ("dz", "int", 0, "End Z offset (blocks)"),
        ],
    },
]


def get_build(build_id):
    """Return build dict by id."""
    for b in BUILDS:
        if b["id"] == build_id:
            return b
    return None
