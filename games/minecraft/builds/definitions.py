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


def _require_minecraftstuff(feature_name):
    if not HAS_MINECRAFT_STUFF:
        raise RuntimeError(f"{feature_name} requires the optional 'minecraftstuff' package.")


# --- Simple builds using only mcpi setBlock/setBlocks ---

def build_simple_house(mc, x, y, z, width=5, depth=4, height=3, roof_height=2):
    """A small house with walls, wooden roof, and glass."""
    x2 = x + width - 1
    z2 = z + depth - 1
    # Floor
    mc.setBlocks(x, y, z, x2, y, z2, block_constants.WOOD_PLANKS.id)
    # Walls
    mc.setBlocks(x, y + 1, z, x2, y + height, z2, block_constants.BRICK_BLOCK.id)
    # Hollow interior
    mc.setBlocks(x + 1, y + 1, z + 1, x2 - 1, y + height - 1, z2 - 1, block_constants.AIR.id)
    # Door
    mc.setBlock(x + width // 2, y + 1, z, block_constants.AIR.id)
    mc.setBlock(x + width // 2, y + 2, z, block_constants.AIR.id)
    # Windows
    mc.setBlocks(x, y + 2, z + depth // 2, x, y + 2, z + depth // 2, block_constants.GLASS.id)
    mc.setBlocks(x2, y + 2, z + depth // 2, x2, y + 2, z + depth // 2, block_constants.GLASS.id)
    # Roof (stepped pyramid)
    for i in range(roof_height):
        mc.setBlocks(x + i, y + height + i, z + i, x2 - i, y + height + i, z2 - i, block_constants.WOOD.id, 0)


def build_tower(mc, x, y, z, radius=2, height=10, material_id=None):
    """A cylindrical tower (square footprint for simplicity)."""
    bid = material_id or block_constants.STONE.id
    mc.setBlocks(x - radius, y, z - radius, x + radius, y + height - 1, z + radius, bid)
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
    _require_minecraftstuff("Sphere")
    mcdraw = _get_mcdraw(mc)
    bid = material_id or block_constants.GLOWSTONE_BLOCK.id
    mcdraw.drawSphere(x, y, z, radius, bid, material_data)


def build_hollow_sphere(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Hollow sphere (requires minecraftstuff)."""
    _require_minecraftstuff("Hollow sphere")
    mcdraw = _get_mcdraw(mc)
    bid = material_id or block_constants.GLASS.id
    mcdraw.drawHollowSphere(x, y, z, radius, bid, material_data)


def build_circle(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Vertical circle in Y plane (requires minecraftstuff)."""
    _require_minecraftstuff("Circle")
    mcdraw = _get_mcdraw(mc)
    bid = material_id or block_constants.WOOL.id
    mcdraw.drawCircle(x, y, z, radius, bid, material_data)


def build_horizontal_circle(mc, x, y, z, radius=5, material_id=None, material_data=0):
    """Horizontal circle (requires minecraftstuff)."""
    _require_minecraftstuff("Horizontal circle")
    mcdraw = _get_mcdraw(mc)
    bid = material_id or block_constants.WOOL.id
    mcdraw.drawHorizontalCircle(x, y, z, radius, bid, material_data)


def build_line(mc, x, y, z, x2=None, y2=None, z2=None, dx=10, dy=0, dz=0, material_id=None, material_data=0):
    """Line from (x,y,z) to (x2,y2,z2) or (x+dx, y+dy, z+dz) if x2 is None (requires minecraftstuff)."""
    _require_minecraftstuff("Line")
    mcdraw = _get_mcdraw(mc)
    if x2 is None:
        x2, y2, z2 = x + dx, y + dy, z + dz
    bid = material_id or block_constants.GLOWSTONE_BLOCK.id
    mcdraw.drawLine(int(x), int(y), int(z), int(x2), int(y2), int(z2), bid, material_data)


# --- Helper: place blocks from list of (dx, dy, dz, block_id, block_data) ---
def _place_blocks(mc, x, y, z, blocks):
    """Place blocks relative to (x,y,z). Each item: (dx, dy, dz, block_id) or (dx, dy, dz, block_id, data)."""
    for item in blocks:
        dx, dy, dz = item[0], item[1], item[2]
        bid = item[3]
        data = item[4] if len(item) > 4 else 0
        mc.setBlock(x + dx, y + dy, z + dz, bid, data)


# --- Statues ---

def build_statue_pillar(mc, x, y, z, height=4):
    """Classic statue: pedestal + column + head (stone/gold)."""
    # Pedestal
    mc.setBlocks(x - 1, y, z - 1, x + 1, y, z + 1, block_constants.STONE.id)
    # Column (body)
    mc.setBlocks(x, y + 1, z, x, y + height - 1, z, block_constants.STONE.id)
    # Head (slightly larger)
    mc.setBlocks(x - 1, y + height, z - 1, x + 1, y + height + 1, z + 1, block_constants.STONE.id)
    mc.setBlock(x, y + height + 2, z, block_constants.GOLD_BLOCK.id)  # Crown/top


def build_statue_steve(mc, x, y, z):
    """Blocky Steve-style figure: head (skin), body, legs, arms."""
    # Legs (blue jeans = wool 11)
    mc.setBlock(x, y, z, block_constants.WOOL.id, 11)
    mc.setBlock(x + 1, y, z, block_constants.WOOL.id, 11)
    # Body (shirt = light blue wool 3)
    mc.setBlocks(x, y + 1, z, x + 1, y + 2, z, block_constants.WOOL.id, 3)
    # Arms holding torch
    mc.setBlock(x - 1, y + 2, z, block_constants.WOOD.id)
    mc.setBlock(x + 2, y + 2, z, block_constants.TORCH.id, 5)
    # Head (skin = sandstone)
    mc.setBlocks(x, y + 3, z - 1, x + 1, y + 4, z + 1, block_constants.SANDSTONE.id)
    # Eyes
    mc.setBlock(x, y + 4, z, block_constants.COAL_ORE.id)
    mc.setBlock(x + 1, y + 4, z, block_constants.COAL_ORE.id)


def build_statue_owl(mc, x, y, z):
    """Owl statue: round head, big eyes, body, feet."""
    # Feet
    mc.setBlock(x, y, z, block_constants.WOOD.id)
    mc.setBlock(x + 2, y, z, block_constants.WOOD.id)
    # Body (brown wool 12)
    mc.setBlocks(x, y + 1, z, x + 2, y + 3, z, block_constants.WOOL.id, 12)
    mc.setBlocks(x + 1, y + 1, z - 1, x + 1, y + 2, z - 1, block_constants.WOOL.id, 12)
    # Head (wider)
    mc.setBlocks(x, y + 4, z - 1, x + 2, y + 5, z + 1, block_constants.WOOL.id, 12)
    # Eyes (glowstone)
    mc.setBlock(x, y + 5, z, block_constants.GLOWSTONE_BLOCK.id)
    mc.setBlock(x + 2, y + 5, z, block_constants.GLOWSTONE_BLOCK.id)
    # Beak
    mc.setBlock(x + 1, y + 4, z + 1, block_constants.GOLD_BLOCK.id)


def build_statue_dragon(mc, x, y, z):
    """Small dragon statue: body, wings, head, tail."""
    # Body
    mc.setBlocks(x + 1, y, z, x + 1, y + 2, z, block_constants.STONE.id)
    # Legs
    mc.setBlock(x, y, z - 1, block_constants.COBBLESTONE.id)
    mc.setBlock(x + 2, y, z - 1, block_constants.COBBLESTONE.id)
    mc.setBlock(x, y, z + 1, block_constants.COBBLESTONE.id)
    mc.setBlock(x + 2, y, z + 1, block_constants.COBBLESTONE.id)
    # Wings (wool)
    mc.setBlocks(x, y + 1, z - 2, x, y + 2, z - 2, block_constants.WOOL.id, 8)
    mc.setBlocks(x + 2, y + 1, z - 2, x + 2, y + 2, z - 2, block_constants.WOOL.id, 8)
    # Neck + head
    mc.setBlocks(x + 1, y + 3, z, x + 1, y + 4, z, block_constants.STONE.id)
    mc.setBlocks(x + 1, y + 5, z - 1, x + 1, y + 5, z + 1, block_constants.STONE.id)
    mc.setBlock(x + 1, y + 5, z, block_constants.GLOWSTONE_BLOCK.id)  # Nose/eye
    # Tail
    mc.setBlocks(x + 1, y, z + 2, x + 1, y + 1, z + 3, block_constants.STONE.id)


# --- Cars / vehicles ---

def build_car_simple(mc, x, y, z, length=4):
    """Simple blocky car: body, cabin, wheels (black wool)."""
    x2 = x + length - 1
    # Wheels (black wool 15) at corners
    mc.setBlock(x, y, z, block_constants.WOOL.id, 15)
    mc.setBlock(x2, y, z, block_constants.WOOL.id, 15)
    mc.setBlock(x, y, z + 1, block_constants.WOOL.id, 15)
    mc.setBlock(x2, y, z + 1, block_constants.WOOL.id, 15)
    # Chassis
    mc.setBlocks(x, y + 1, z, x2, y + 1, z + 1, block_constants.IRON_BLOCK.id)
    # Cabin (glass)
    cab_start = min(max(1, length // 2 - 1), max(1, length - 2))
    mc.setBlocks(x + cab_start, y + 2, z, x + cab_start + 1, y + 3, z + 1, block_constants.GLASS.id)
    # Roof
    mc.setBlocks(x + cab_start, y + 4, z, x + cab_start + 1, y + 4, z + 1, block_constants.IRON_BLOCK.id)
    # Headlights (glowstone)
    mc.setBlock(x, y + 2, z, block_constants.GLOWSTONE_BLOCK.id)
    mc.setBlock(x2, y + 2, z + 1, block_constants.GLOWSTONE_BLOCK.id)


def build_car_buggy(mc, x, y, z):
    """Small buggy: open cockpit, big wheels."""
    # Big wheels (2 blocks high)
    for dz in (0, 1):
        mc.setBlocks(x, y, z + dz, x, y + 1, z + dz, block_constants.WOOL.id, 15)
        mc.setBlocks(x + 3, y, z + dz, x + 3, y + 1, z + dz, block_constants.WOOL.id, 15)
    # Frame
    mc.setBlocks(x, y + 1, z, x + 3, y + 1, z + 1, block_constants.WOOD.id)
    # Seat area (wool orange)
    mc.setBlocks(x + 1, y + 2, z, x + 2, y + 2, z + 1, block_constants.WOOL.id, 1)
    # Roll bar / windscreen
    mc.setBlocks(x + 1, y + 3, z, x + 2, y + 3, z, block_constants.GLASS.id)


def build_rocket(mc, x, y, z, height=6):
    """Vertical rocket: body, nose, fins, flame."""
    # Fins
    mc.setBlock(x - 1, y, z, block_constants.IRON_BLOCK.id)
    mc.setBlock(x + 1, y, z, block_constants.IRON_BLOCK.id)
    mc.setBlock(x, y, z - 1, block_constants.IRON_BLOCK.id)
    mc.setBlock(x, y, z + 1, block_constants.IRON_BLOCK.id)
    # Body
    mc.setBlocks(x, y + 1, z, x, y + height - 1, z, block_constants.IRON_BLOCK.id)
    # Nose
    mc.setBlock(x, y + height, z, block_constants.GLOWSTONE_BLOCK.id)
    # Flame (orange wool)
    mc.setBlocks(x, y - 1, z, x, y - 2, z, block_constants.WOOL.id, 1)


def build_rainbow_arch(mc, x, y, z, radius=5):
    """Colorful wool arch that works like a simple rainbow tunnel."""
    colors = [14, 1, 4, 5, 3, 11, 10]
    for offset, wool_color in enumerate(colors):
        r = radius - offset
        if r < 1:
            break
        for dy in range(r + 1):
            dx = r - dy
            mc.setBlock(x - dx, y + dy, z, block_constants.WOOL.id, wool_color)
            mc.setBlock(x + dx, y + dy, z, block_constants.WOOL.id, wool_color)


def build_tree_oak(mc, x, y, z, height=5):
    """Chunky oak-style tree with a leafy canopy and a tiny apple."""
    trunk_top = y + height - 1
    mc.setBlocks(x, y, z, x, trunk_top, z, block_constants.WOOD.id)
    mc.setBlocks(x - 2, trunk_top - 1, z - 2, x + 2, trunk_top + 1, z + 2, block_constants.LEAVES.id)
    mc.setBlocks(x - 1, trunk_top + 2, z - 1, x + 1, trunk_top + 2, z + 1, block_constants.LEAVES.id)
    mc.setBlock(x + 1, trunk_top, z + 2, block_constants.WOOL.id, 14)


def build_castle_gate(mc, x, y, z, width=7, height=5):
    """Small castle gate with two towers and a central archway."""
    tower_height = height + 2
    left_x = x
    right_x = x + width - 1
    gate_left = x + 2
    gate_right = x + width - 3

    mc.setBlocks(left_x, y, z, left_x + 1, y + tower_height - 1, z + 1, block_constants.STONE_BRICK.id)
    mc.setBlocks(right_x - 1, y, z, right_x, y + tower_height - 1, z + 1, block_constants.STONE_BRICK.id)
    mc.setBlocks(gate_left, y + height - 1, z, gate_right, y + height, z + 1, block_constants.STONE_BRICK.id)
    mc.setBlocks(gate_left, y, z, gate_right, y + height - 2, z + 1, block_constants.AIR.id)
    mc.setBlocks(left_x, y + tower_height, z, left_x + 1, y + tower_height, z + 1, block_constants.STONE_SLAB.id)
    mc.setBlocks(right_x - 1, y + tower_height, z, right_x, y + tower_height, z + 1, block_constants.STONE_SLAB.id)
    mc.setBlock(left_x + 1, y + tower_height - 1, z, block_constants.TORCH.id)
    mc.setBlock(right_x - 1, y + tower_height - 1, z, block_constants.TORCH.id)


def build_smiley_pixel_art(mc, x, y, z, size=7):
    """Flat smiley face pixel art on a wool background."""
    s = max(5, size)
    x2 = x + s - 1
    y2 = y + s - 1
    mc.setBlocks(x, y, z, x2, y2, z, block_constants.WOOL.id, 4)
    mc.setBlocks(x + 1, y + 1, z, x2 - 1, y2 - 1, z, block_constants.WOOL.id, 0)

    eye_y = y + s - 3
    mc.setBlock(x + 1, eye_y, z, block_constants.WOOL.id, 15)
    mc.setBlock(x2 - 1, eye_y, z, block_constants.WOOL.id, 15)

    mouth_y = y + 1
    mc.setBlocks(x + 1, mouth_y, z, x2 - 1, mouth_y, z, block_constants.WOOL.id, 15)
    mc.setBlock(x, mouth_y + 1, z, block_constants.WOOL.id, 15)
    mc.setBlock(x2, mouth_y + 1, z, block_constants.WOOL.id, 15)


def build_campfire(mc, x, y, z):
    """Tiny campfire with logs, stones, and a warm glow."""
    mc.setBlocks(x - 1, y, z - 1, x + 1, y, z + 1, block_constants.COBBLESTONE.id)
    mc.setBlock(x, y + 1, z, block_constants.FIRE.id)
    mc.setBlock(x, y, z, block_constants.WOOD.id)
    mc.setBlock(x - 1, y, z, block_constants.WOOD.id)
    mc.setBlock(x + 1, y, z, block_constants.WOOD.id)
    mc.setBlock(x, y, z - 1, block_constants.WOOD.id)
    mc.setBlock(x, y, z + 1, block_constants.WOOD.id)
    mc.setBlock(x, y + 2, z, block_constants.TORCH.id)


# --- Mobs (blocky Minecraft-style) ---

def build_mob_creeper(mc, x, y, z):
    """Classic Creeper: green body, head with black eyes and mouth."""
    # Legs
    mc.setBlock(x, y, z, block_constants.WOOL.id, 13)  # Green
    mc.setBlock(x + 1, y, z, block_constants.WOOL.id, 13)
    mc.setBlock(x, y, z + 1, block_constants.WOOL.id, 13)
    mc.setBlock(x + 1, y, z + 1, block_constants.WOOL.id, 13)
    # Body 2x2x2
    mc.setBlocks(x, y + 1, z, x + 1, y + 2, z + 1, block_constants.WOOL.id, 13)
    # Head (green)
    mc.setBlocks(x, y + 3, z, x + 1, y + 4, z + 1, block_constants.WOOL.id, 13)
    # Face on front (z+1): eyes top, mouth bottom (black)
    mc.setBlock(x, y + 4, z + 1, block_constants.WOOL.id, 15)
    mc.setBlock(x + 1, y + 4, z + 1, block_constants.WOOL.id, 15)
    mc.setBlock(x, y + 3, z + 1, block_constants.WOOL.id, 15)
    mc.setBlock(x + 1, y + 3, z + 1, block_constants.WOOL.id, 15)


def build_mob_pig(mc, x, y, z):
    """Blocky pig: pink body, head, ears, snout."""
    # Legs (pink wool 6)
    mc.setBlock(x, y, z, block_constants.WOOL.id, 6)
    mc.setBlock(x + 2, y, z, block_constants.WOOL.id, 6)
    mc.setBlock(x, y, z + 1, block_constants.WOOL.id, 6)
    mc.setBlock(x + 2, y, z + 1, block_constants.WOOL.id, 6)
    # Body
    mc.setBlocks(x, y + 1, z, x + 2, y + 2, z + 1, block_constants.WOOL.id, 6)
    # Head
    mc.setBlocks(x + 1, y + 2, z - 1, x + 1, y + 3, z - 1, block_constants.WOOL.id, 6)
    # Snout
    mc.setBlock(x + 1, y + 2, z - 2, block_constants.WOOL.id, 6)
    # Ears (on head)
    mc.setBlock(x, y + 3, z - 1, block_constants.WOOL.id, 6)
    mc.setBlock(x + 2, y + 3, z - 1, block_constants.WOOL.id, 6)


def build_mob_sheep(mc, x, y, z, wool_color=0):
    """Sheep: white (or colored) wool body, legs, head."""
    # Legs (grey)
    for px, pz in [(x, z), (x + 1, z), (x, z + 1), (x + 1, z + 1)]:
        mc.setBlock(px, y, pz, block_constants.WOOL.id, 8)
    # Wool body (2x2x2 fluffy)
    mc.setBlocks(x, y + 1, z, x + 1, y + 2, z + 1, block_constants.WOOL.id, wool_color)
    # Head (in front)
    mc.setBlocks(x, y + 2, z + 2, x + 1, y + 3, z + 2, block_constants.WOOL.id, wool_color)
    mc.setBlock(x, y + 3, z + 2, block_constants.WOOL.id, 15)  # Eyes
    mc.setBlock(x + 1, y + 3, z + 2, block_constants.WOOL.id, 15)


def build_mob_slime(mc, x, y, z, size=2):
    """Bouncy slime: green block(s). size 1=small, 2=medium, 3=large."""
    # Lime wool 5 for slime
    s = max(1, min(3, size))
    mc.setBlocks(x, y, z, x + s - 1, y + s - 1, z + s - 1, block_constants.WOOL.id, 5)
    # Eyes
    if s >= 2:
        mc.setBlock(x, y + s - 1, z, block_constants.WOOL.id, 0)
        mc.setBlock(x + s - 1, y + s - 1, z, block_constants.WOOL.id, 0)


def build_mob_enderman(mc, x, y, z):
    """Tall Enderman-style figure: black body, purple eyes."""
    # Legs (tall - black wool 15)
    mc.setBlocks(x, y, z, x, y + 1, z, block_constants.WOOL.id, 15)
    mc.setBlocks(x + 1, y, z, x + 1, y + 1, z, block_constants.WOOL.id, 15)
    # Body
    mc.setBlocks(x, y + 2, z, x + 1, y + 4, z, block_constants.WOOL.id, 15)
    # Arms (long)
    mc.setBlocks(x - 1, y + 3, z, x - 1, y + 4, z, block_constants.WOOL.id, 15)
    mc.setBlocks(x + 2, y + 3, z, x + 2, y + 4, z, block_constants.WOOL.id, 15)
    # Head
    mc.setBlocks(x, y + 5, z - 1, x + 1, y + 6, z + 1, block_constants.WOOL.id, 15)
    # Eyes (purple wool 10)
    mc.setBlock(x, y + 6, z, block_constants.WOOL.id, 10)
    mc.setBlock(x + 1, y + 6, z, block_constants.WOOL.id, 10)


def build_mob_zombie(mc, x, y, z):
    """Zombie: green body, ragged clothes, arms out."""
    # Legs (green wool 13)
    mc.setBlock(x, y, z, block_constants.WOOL.id, 13)
    mc.setBlock(x + 1, y, z, block_constants.WOOL.id, 13)
    # Body (dirty green)
    mc.setBlocks(x, y + 1, z, x + 1, y + 2, z, block_constants.WOOL.id, 13)
    mc.setBlock(x, y + 1, z, block_constants.WOOL.id, 12)  # Brown strip
    # Arms out
    mc.setBlock(x - 1, y + 2, z, block_constants.WOOL.id, 13)
    mc.setBlock(x + 2, y + 2, z, block_constants.WOOL.id, 13)
    # Head
    mc.setBlocks(x, y + 3, z - 1, x + 1, y + 4, z + 1, block_constants.WOOL.id, 13)
    # Eyes
    mc.setBlock(x, y + 4, z, block_constants.GLOWSTONE_BLOCK.id)
    mc.setBlock(x + 1, y + 4, z, block_constants.GLOWSTONE_BLOCK.id)


# --- Terrarium (big enclosure + spawn mobs inside) ---

def build_terrarium(mc, x, y, z, width=50, depth=50, height=20):
    """Big glass terrarium: floor, ceiling, four walls, hollow inside (50×50×20 default)."""
    x2 = x + width - 1
    z2 = z + depth - 1
    y2 = y + height - 1
    # Floor (stone so it's solid)
    mc.setBlocks(x, y, z, x2, y, z2, block_constants.STONE.id)
    # Ceiling (glass)
    mc.setBlocks(x, y2, z, x2, y2, z2, block_constants.GLASS.id)
    # Four walls (glass): front and back (along x), left and right (along z)
    # Wall at z (front)
    mc.setBlocks(x, y + 1, z, x2, y2 - 1, z, block_constants.GLASS.id)
    # Wall at z + depth (back)
    mc.setBlocks(x, y + 1, z2, x2, y2 - 1, z2, block_constants.GLASS.id)
    # Wall at x (left)
    mc.setBlocks(x, y + 1, z, x, y2 - 1, z2, block_constants.GLASS.id)
    # Wall at x + width (right)
    mc.setBlocks(x2, y + 1, z, x2, y2 - 1, z2, block_constants.GLASS.id)
    # Hollow interior (air) — floor at y+1, up to y+height-1
    mc.setBlocks(x + 1, y + 1, z + 1, x2 - 1, y2 - 1, z2 - 1, block_constants.AIR.id)


# Mob build functions that can be placed inside terrarium (id, fn)
_TERRARIUM_MOB_BUILDERS = [
    ("creeper", build_mob_creeper),
    ("pig", build_mob_pig),
    ("sheep", build_mob_sheep),
    ("slime", build_mob_slime),
    ("zombie", build_mob_zombie),
    ("enderman", build_mob_enderman),
]


def populate_terrarium_mobs(mc, x, y, z, width=50, depth=50, height=20, count=15):
    """Place random mob builds (statues) inside the terrarium. MCPI has no spawn-entity API."""
    import random
    # Interior bounds: leave margin so mobs (2–4 blocks) fit
    x_min = x + 4
    x_max = x + width - 4
    z_min = z + 4
    z_max = z + depth - 4
    y_floor = y + 1
    if x_max <= x_min or z_max <= z_min:
        mc.postToChat("Terrarium too small to place mobs")
        return {"placed": 0, "failed": 0, "errors": ["Terrarium too small to place mobs."]}
    builders = list(_TERRARIUM_MOB_BUILDERS)
    placed = 0
    failures = []
    for _ in range(int(count)):
        px = random.randint(x_min, x_max)
        pz = random.randint(z_min, z_max)
        name, build_fn = random.choice(builders)
        try:
            build_fn(mc, px, y_floor, pz)
            placed += 1
        except Exception as exc:
            failures.append(f"{name} at ({px}, {y_floor}, {pz}): {exc}")
    return {"placed": placed, "failed": len(failures), "errors": failures}


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
    # --- Statues ---
    {
        "id": "statue_pillar",
        "name": "Statue (pillar)",
        "description": "Classic pedestal + column + head",
        "fn": build_statue_pillar,
        "uses_stuff": False,
        "params": [("height", "int", 4, "Column height (blocks)")],
    },
    {
        "id": "statue_steve",
        "name": "Statue (Steve)",
        "description": "Blocky Steve-style figure with torch",
        "fn": build_statue_steve,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "statue_owl",
        "name": "Statue (owl)",
        "description": "Owl with big eyes and beak",
        "fn": build_statue_owl,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "statue_dragon",
        "name": "Statue (dragon)",
        "description": "Small dragon with wings and tail",
        "fn": build_statue_dragon,
        "uses_stuff": False,
        "params": [],
    },
    # --- Cars / vehicles ---
    {
        "id": "car_simple",
        "name": "Car (simple)",
        "description": "Blocky car with cabin and wheels",
        "fn": build_car_simple,
        "uses_stuff": False,
        "params": [("length", "int", 4, "Body length (blocks)")],
    },
    {
        "id": "car_buggy",
        "name": "Buggy",
        "description": "Small open buggy with roll bar",
        "fn": build_car_buggy,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "rocket",
        "name": "Rocket",
        "description": "Vertical rocket with fins and flame",
        "fn": build_rocket,
        "uses_stuff": False,
        "params": [("height", "int", 6, "Body height (blocks)")],
    },
    {
        "id": "rainbow_arch",
        "name": "Rainbow Arch",
        "description": "Colorful wool rainbow arch",
        "fn": build_rainbow_arch,
        "uses_stuff": False,
        "params": [("radius", "int", 5, "Arch radius (blocks)")],
    },
    {
        "id": "tree_oak",
        "name": "Oak Tree",
        "description": "Chunky oak-style tree with a leafy canopy",
        "fn": build_tree_oak,
        "uses_stuff": False,
        "params": [("height", "int", 5, "Trunk height (blocks)")],
    },
    {
        "id": "castle_gate",
        "name": "Castle Gate",
        "description": "Two towers with a central gate arch",
        "fn": build_castle_gate,
        "uses_stuff": False,
        "params": [
            ("width", "int", 7, "Gate width (blocks)"),
            ("height", "int", 5, "Arch height (blocks)"),
        ],
    },
    {
        "id": "smiley_pixel_art",
        "name": "Smiley Pixel Art",
        "description": "Flat smiley face for walls or signs",
        "fn": build_smiley_pixel_art,
        "uses_stuff": False,
        "params": [("size", "int", 7, "Canvas size (blocks)")],
    },
    {
        "id": "campfire",
        "name": "Campfire",
        "description": "Small stone-ring campfire with glowing center",
        "fn": build_campfire,
        "uses_stuff": False,
        "params": [],
    },
    # --- Mobs ---
    {
        "id": "mob_creeper",
        "name": "Creeper",
        "description": "Classic Creeper (green, face on one side)",
        "fn": build_mob_creeper,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "mob_pig",
        "name": "Pig",
        "description": "Blocky pink pig",
        "fn": build_mob_pig,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "mob_sheep",
        "name": "Sheep",
        "description": "Woolly sheep (choose color)",
        "fn": build_mob_sheep,
        "uses_stuff": False,
        "params": [("wool_color", "int", 0, "Wool color 0–15 (0=white, 14=red, …)")],
    },
    {
        "id": "mob_slime",
        "name": "Slime",
        "description": "Bouncy slime (size 1–3)",
        "fn": build_mob_slime,
        "uses_stuff": False,
        "params": [("size", "int", 2, "Size: 1=small, 2=medium, 3=large")],
    },
    {
        "id": "mob_enderman",
        "name": "Enderman",
        "description": "Tall Enderman with purple eyes",
        "fn": build_mob_enderman,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "mob_zombie",
        "name": "Zombie",
        "description": "Zombie with arms out",
        "fn": build_mob_zombie,
        "uses_stuff": False,
        "params": [],
    },
    {
        "id": "terrarium",
        "name": "Terrarium",
        "description": "Big glass enclosure 50×50×20 (floor, walls, ceiling, hollow). Spawn mobs after with the Terrarium tab.",
        "fn": build_terrarium,
        "uses_stuff": False,
        "params": [
            ("width", "int", 50, "Width (blocks)"),
            ("depth", "int", 50, "Depth (blocks)"),
            ("height", "int", 20, "Height (blocks)"),
        ],
    },
]


def get_build(build_id):
    """Return build dict by id."""
    for b in BUILDS:
        if b["id"] == build_id:
            return b
    return None
