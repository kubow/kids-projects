#!/usr/bin/env python3
"""
Streamlit UI for Minecraft Pi Edition API.
Connect to a Minecraft Pi (or RaspberryJuice) client and control the world,
player, place predefined builds, post to chat, and more.

API reference: https://pimylifeup.com/minecraft-pi-edition-api-reference/
"""

from pathlib import Path

import streamlit as st

from builds import BUILDS, get_build, build_terrarium, populate_terrarium_mobs

# Image references (no generation): local assets or URLs. Add images to games/assets/ (see assets/README.md).
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

def _block_image_path(block_key: str) -> Path:
    """Path to block image: assets/blocks/{key}.png (e.g. Stone.png, Sugar_cane.png)."""
    name = block_key.replace(" ", "_") + ".png"
    return ASSETS_DIR / "blocks" / name

def _build_image_path(build_id: str) -> Path:
    """Path to build image: assets/builds/{build_id}.png (e.g. simple_house.png)."""
    return ASSETS_DIR / "builds" / f"{build_id}.png"

def _show_image_if_exists(path: Path, width: int = 80, caption: str = ""):
    """Show image with st.image if file exists."""
    if path.exists():
        try:
            st.image(str(path), width=width, caption=caption or None)
        except Exception:
            pass

# Page config
st.set_page_config(
    page_title="Minecraft Pi API",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state for Minecraft connection
if "mc" not in st.session_state:
    st.session_state.mc = None
if "mc_error" not in st.session_state:
    st.session_state.mc_error = None


def connect_minecraft(host: str, port: int):
    """Create Minecraft connection and store in session_state."""
    try:
        from mcpi.minecraft import Minecraft
        st.session_state.mc = Minecraft.create(host, port)
        st.session_state.mc_error = None
        return True
    except Exception as e:
        st.session_state.mc = None
        st.session_state.mc_error = str(e)
        return False


def get_mc():
    """Return current Minecraft connection or None."""
    return st.session_state.get("mc")


# --- Sidebar: connection ---
with st.sidebar:
    st.header("⛏️ Minecraft Pi API")
    st.caption("Connect to Minecraft Pi Edition or RaspberryJuice (default port 4711)")

    host = st.text_input("Host", value="localhost", key="host")
    port = st.number_input("Port", min_value=1, max_value=65535, value=4711, key="port")

    if st.button("Connect", type="primary"):
        with st.spinner("Connecting…"):
            if connect_minecraft(host, int(port)):
                st.success("Connected")
            else:
                st.error(st.session_state.mc_error or "Connection failed")

    mc = get_mc()
    if mc:
        st.success("Connected")
    else:
        st.warning("Not connected. Start Minecraft Pi and click Connect.")

    st.divider()
    st.caption("Libraries: mcpi + [minecraftstuff](https://pypi.org/project/minecraftstuff/) for shapes")

# --- Main area: tabs ---
tab_world, tab_player, tab_builds, tab_terrarium, tab_chat, tab_camera, tab_blocks = st.tabs([
    "World (blocks)", "Player", "Predefined builds", "Terrarium", "Chat", "Camera", "Block events",
])

# Block IDs (Minecraft Pi / API reference). Includes plants and special blocks.
BLOCK_REF = {
    "Air": 0, "Stone": 1, "Grass": 2, "Dirt": 3, "Cobblestone": 4,
    "Wood planks": 5, "Sapling": 6, "Wood": 17, "Leaves": 18, "Glass": 20,
    "Wool": 35, "Yellow flower": 37, "Cyan flower": 38, "Brown mushroom": 39, "Red mushroom": 40,
    "Gold block": 41, "Iron block": 42, "Brick": 45, "TNT": 46, "Bookshelf": 47, "Torch": 50,
    "Sandstone": 24, "Diamond block": 57, "Sugar cane": 83, "Cactus": 81, "Clay": 82,
    "Tall grass": 31, "Melon": 103, "Glowstone": 89, "Snow": 78, "Ice": 79,
}

# Emoji icons for block list (visual representation)
BLOCK_ICONS = {
    "Air": "⬜", "Stone": "🪨", "Grass": "🌿", "Dirt": "🟫", "Cobblestone": "🪨",
    "Wood planks": "🪵", "Sapling": "🌱", "Wood": "🪵", "Leaves": "🍃", "Glass": "🪟",
    "Wool": "🧶", "Yellow flower": "🌸", "Cyan flower": "💠", "Brown mushroom": "🍄", "Red mushroom": "🍄",
    "Gold block": "🟨", "Iron block": "⬜", "Brick": "🧱", "TNT": "🧨", "Bookshelf": "📚", "Torch": "🔦",
    "Sandstone": "🟨", "Diamond block": "💎", "Sugar cane": "🫚", "Cactus": "🌵", "Clay": "🟤",
    "Tall grass": "🌾", "Melon": "🍈", "Glowstone": "✨", "Snow": "❄️", "Ice": "🧊",
}

def _block_display_options():
    """Options for selectbox: emoji + name."""
    return [f"{BLOCK_ICONS.get(n, '⬜')} {n}" for n in BLOCK_REF.keys()]

def _block_label_to_key(label):
    """From '🪨 Stone' to 'Stone'."""
    for k in BLOCK_REF:
        if label == f"{BLOCK_ICONS.get(k, '⬜')} {k}":
            return k
    for k in BLOCK_REF:
        if label.endswith(" " + k):
            return k
    return list(BLOCK_REF.keys())[0]

# Build icons for predefined builds (visual representation)
BUILD_ICONS = {
    "simple_house": "🏠", "tower": "🗼", "wall": "🧱", "pyramid": "🔺", "platform": "📦",
    "pillar": "🪵", "sphere": "⚽", "hollow_sphere": "⭕", "circle": "⭕", "horizontal_circle": "⭕", "line": "📏",
    "statue_pillar": "🗿", "statue_steve": "🧑", "statue_owl": "🦉", "statue_dragon": "🐉",
    "car_simple": "🚗", "car_buggy": "🚙", "rocket": "🚀",
    "mob_creeper": "💚", "mob_pig": "🐷", "mob_sheep": "🐑", "mob_slime": "🟢", "mob_enderman": "🖤", "mob_zombie": "🧟",
    "terrarium": "🪟",
}

with tab_world:
    st.subheader("World / blocks")
    with st.expander("Block ID reference (common) & seed blocks"):
        st.caption("Full list: [Pi My Life Up API reference](https://pimylifeup.com/minecraft-pi-edition-api-reference/)")
        cols = st.columns(4)
        for i, (name, bid) in enumerate(BLOCK_REF.items()):
            icon = BLOCK_ICONS.get(name, "⬜")
            cols[i % 4].markdown(f"{icon} **{name}**: `{bid}`")
        st.divider()
        st.markdown("**Get a block (place near you)**")
        st.caption("The MCPI API cannot add blocks to your inventory. You can place the selected block in the world next to you so you can see or use it (e.g. plants, flowers, sugar cane).")
        if mc:
            inv_block_label = st.selectbox(
                "Block to place near you",
                options=_block_display_options(),
                key="inv_block_select",
                help="Choose a block (e.g. Sugar cane, Yellow flower, Sapling)",
            )
            inv_block_key = _block_label_to_key(inv_block_label)
            _show_image_if_exists(_block_image_path(inv_block_key), width=64, caption=inv_block_key)
            inv_block_data = st.number_input("Block data (subtype)", min_value=0, value=0, key="inv_block_data", help="Use for wool colors (0–15), sapling type, etc.")
            place_at = st.radio("Where to place", ["1 block in front of me", "At my feet", "1 block above my feet"], horizontal=True, key="inv_place_at")
            if st.button("Place block near me", key="inv_place_btn"):
                try:
                    p = mc.player.getTilePos()
                    if place_at == "1 block in front of me":
                        # Place in +X direction (common default)
                        gx, gy, gz = p.x + 1, p.y, p.z
                    elif place_at == "At my feet":
                        gx, gy, gz = p.x, p.y, p.z
                    else:
                        gx, gy, gz = p.x, p.y + 1, p.z
                    bid = BLOCK_REF[inv_block_key]
                    mc.setBlock(gx, gy, gz, bid, int(inv_block_data))
                    st.success(f"Placed **{inv_block_key}** at ({gx}, {gy}, {gz}).")
                except Exception as e:
                    st.error(str(e))
        else:
            st.caption("Connect to Minecraft to place blocks near you.")
        st.divider()
        st.markdown("**Seed blocks around the map** — scatter a selected block at random positions in an area.")
        if mc:
            seed_block_label = st.selectbox(
                "Block to seed",
                options=_block_display_options(),
                key="seed_block_select",
            )
            seed_block_key = _block_label_to_key(seed_block_label)
            _show_image_if_exists(_block_image_path(seed_block_key), width=64, caption=seed_block_key)
            seed_block_id = BLOCK_REF[seed_block_key]
            use_player_center = st.checkbox("Center area on player position", value=True, key="seed_use_player")
            if use_player_center:
                try:
                    p = mc.player.getTilePos()
                    seed_cx, seed_cz = p.x, p.z
                except Exception:
                    seed_cx, seed_cz = 0, 0
            else:
                seed_cx = st.number_input("Center X", value=0, key="seed_cx")
                seed_cz = st.number_input("Center Z", value=0, key="seed_cz")
            seed_radius = st.slider("Radius (blocks) from center", min_value=5, max_value=80, value=20, key="seed_radius")
            seed_count = st.number_input("Number of blocks to place", min_value=1, max_value=500, value=30, key="seed_count")
            seed_at_surface = st.checkbox("Place on surface (use getHeight)", value=True, key="seed_at_surface")
            if not seed_at_surface:
                seed_fixed_y = st.number_input("Fixed Y level", value=0, key="seed_fixed_y")
            else:
                seed_fixed_y = 0
            if st.button("Seed blocks", type="primary", key="seed_btn"):
                import random
                placed = 0
                for _ in range(int(seed_count)):
                    rx = seed_cx + random.randint(-seed_radius, seed_radius)
                    rz = seed_cz + random.randint(-seed_radius, seed_radius)
                    if seed_at_surface:
                        try:
                            ry = mc.getHeight(rx, rz)
                        except Exception:
                            ry = 0
                    else:
                        ry = int(seed_fixed_y)
                    try:
                        mc.setBlock(rx, ry, rz, seed_block_id, 0)
                        placed += 1
                    except Exception:
                        pass
                st.success(f"Placed **{placed}** blocks of **{seed_block_key}** in the area.")
        else:
            st.caption("Connect to Minecraft to seed blocks.")
    if mc:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Get block**")
            gx = st.number_input("X", value=0, key="get_x")
            gy = st.number_input("Y", value=0, key="get_y")
            gz = st.number_input("Z", value=0, key="get_z")
            if st.button("Get block ID"):
                bid = mc.getBlock(int(gx), int(gy), int(gz))
                st.info(f"Block ID at ({gx}, {gy}, {gz}): **{bid}**")

        with c2:
            st.markdown("**Set block**")
            sx = st.number_input("X", value=0, key="set_x")
            sy = st.number_input("Y", value=0, key="set_y")
            sz = st.number_input("Z", value=0, key="set_z")
            block_id = st.number_input("Block ID", min_value=0, value=1, key="block_id")
            block_data = st.number_input("Block data (subtype)", min_value=0, value=0, key="block_data")
            if st.button("Set block"):
                mc.setBlock(int(sx), int(sy), int(sz), int(block_id), int(block_data))
                st.success("Block set")

        st.markdown("**Set cuboid (setBlocks)**")
        x1, y1, z1 = st.columns(3)
        with x1:
            cx1 = st.number_input("x1", value=0, key="cx1")
            cy1 = st.number_input("y1", value=0, key="cy1")
            cz1 = st.number_input("z1", value=0, key="cz1")
        x2, y2, z2 = st.columns(3)
        with x2:
            cx2 = st.number_input("x2", value=2, key="cx2")
            cy2 = st.number_input("y2", value=2, key="cy2")
            cz2 = st.number_input("z2", value=2, key="cz2")
        cbid = st.number_input("Block ID (cuboid)", value=1, key="cuboid_bid")
        if st.button("Fill cuboid"):
            mc.setBlocks(int(cx1), int(cy1), int(cz1), int(cx2), int(cy2), int(cz2), int(cbid))
            st.success("Cuboid filled")

        hx = st.number_input("getHeight X", value=0, key="height_x")
        hz = st.number_input("getHeight Z", value=0, key="height_z")
        if st.button("Get height"):
            hy = mc.getHeight(int(hx), int(hz))
            st.info(f"Height at ({hx}, {hz}): **{hy}**")
    else:
        st.info("Connect to Minecraft first (sidebar).")

with tab_player:
    st.subheader("Player")
    if mc:
        if st.button("Get position (float)"):
            pos = mc.player.getPos()
            st.info(f"Position: x={pos.x:.2f}, y={pos.y:.2f}, z={pos.z:.2f}")
        if st.button("Get tile position (int)"):
            t = mc.player.getTilePos()
            st.info(f"Tile: x={t.x}, y={t.y}, z={t.z}")

        st.markdown("**Teleport player**")
        px = st.number_input("X", value=0, key="tp_x")
        py = st.number_input("Y", value=0, key="tp_y")
        pz = st.number_input("Z", value=0, key="tp_z")
        use_tile = st.checkbox("Use setTilePos (integer coords)", value=False)
        if st.button("Teleport"):
            if use_tile:
                mc.player.setTilePos(int(px), int(py), int(pz))
            else:
                mc.player.setPos(float(px), float(py), float(pz))
            st.success("Teleported")
    else:
        st.info("Connect to Minecraft first.")

with tab_builds:
    st.subheader("Predefined builds")
    st.caption("Place structures at a given position. Uses [mcpi](https://pypi.org/project/mcpi/) and [minecraftstuff](https://pypi.org/project/minecraftstuff/) for shapes.")

    if mc:
        build_options = {
            f"{BUILD_ICONS.get(b['id'], '⬜')} {b['name']} — {b['description']}": b["id"]
            for b in BUILDS
        }
        selected_label = st.selectbox("Choose a build", list(build_options.keys()))
        build_id = build_options[selected_label]
        build = get_build(build_id)
        if not build:
            st.error("Unknown build")
        else:
            icon = BUILD_ICONS.get(build_id, "⬜")
            st.markdown(f"{icon} **{build['name']}**: {build['description']}")
            _show_image_if_exists(_build_image_path(build_id), width=120, caption=build["name"])
            if build.get("uses_stuff"):
                st.caption("Requires minecraftstuff library for shapes.")

            use_player_pos = st.checkbox("Use player position as origin", value=True, key="use_player_pos")
            if use_player_pos:
                try:
                    pos = mc.player.getTilePos()
                    default_x, default_y, default_z = pos.x, pos.y, pos.z
                except Exception:
                    default_x, default_y, default_z = 0, 0, 0
            else:
                default_x, default_y, default_z = 0, 0, 0
            # Sync button: refresh position from player and store in session state
            if st.button("Sync with current position", help="Update X, Y, Z to your current tile position"):
                try:
                    pos = mc.player.getTilePos()
                    st.session_state["build_x"] = pos.x
                    st.session_state["build_y"] = pos.y
                    st.session_state["build_z"] = pos.z
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
            bx = st.number_input("Position X", value=st.session_state.get("build_x", default_x), key="build_x")
            by = st.number_input("Position Y", value=st.session_state.get("build_y", default_y), key="build_y")
            bz = st.number_input("Position Z", value=st.session_state.get("build_z", default_z), key="build_z")

            extra = {}
            for param_name, param_type, default, label in build.get("params", []):
                if param_type == "int":
                    extra[param_name] = st.number_input(label, value=default, key=f"build_{build_id}_{param_name}")

            if st.button("Place build", type="primary"):
                try:
                    build["fn"](mc, int(bx), int(by), int(bz), **extra)
                    st.success(f"Placed **{build['name']}** at ({bx}, {by}, {bz})")
                except Exception as e:
                    st.error(str(e))
    else:
        st.info("Connect to Minecraft first.")

with tab_terrarium:
    st.subheader("🪟 Big terrarium (50×50×20)")
    st.caption("Build a glass enclosure, then spawn mob statues inside. MCPI has no real entity spawn — we place decorative mob builds.")
    if mc:
        st.markdown("**1. Build terrarium**")
        if st.button("Sync position with player", key="terr_sync"):
            try:
                p = mc.player.getTilePos()
                st.session_state["terr_x"] = p.x
                st.session_state["terr_y"] = p.y
                st.session_state["terr_z"] = p.z
                st.rerun()
            except Exception as e:
                st.error(str(e))
        tx = st.number_input("Origin X", value=st.session_state.get("terr_x", 0), key="terr_x")
        ty = st.number_input("Origin Y", value=st.session_state.get("terr_y", 0), key="terr_y")
        tz = st.number_input("Origin Z", value=st.session_state.get("terr_z", 0), key="terr_z")
        tw = st.number_input("Width", value=50, min_value=10, key="terr_w")
        td = st.number_input("Depth", value=50, min_value=10, key="terr_d")
        th = st.number_input("Height", value=20, min_value=5, key="terr_h")
        if st.button("Build terrarium", type="primary", key="terr_build"):
            try:
                build_terrarium(mc, int(tx), int(ty), int(tz), width=int(tw), depth=int(td), height=int(th))
                st.success(f"Built terrarium at ({tx}, {ty}, {tz}) — {tw}×{td}×{th} blocks.")
            except Exception as e:
                st.error(str(e))

        st.divider()
        st.markdown("**2. Spawn mobs inside** (after terrarium is built)")
        st.caption("Places random mob statues (creeper, pig, sheep, slime, zombie, enderman) inside the terrarium.")
        pm_x = st.number_input("Terrarium origin X", value=tx, key="terr_pm_x")
        pm_y = st.number_input("Terrarium origin Y", value=ty, key="terr_pm_y")
        pm_z = st.number_input("Terrarium origin Z", value=tz, key="terr_pm_z")
        pm_w = st.number_input("Terrarium width", value=50, min_value=10, key="terr_pm_w")
        pm_d = st.number_input("Terrarium depth", value=50, min_value=10, key="terr_pm_d")
        pm_h = st.number_input("Terrarium height", value=20, min_value=5, key="terr_pm_h")
        mob_count = st.slider("Number of mobs to place", min_value=1, max_value=50, value=15, key="terr_mob_count")
        if st.button("Spawn mobs inside terrarium", type="primary", key="terr_spawn"):
            try:
                n = populate_terrarium_mobs(mc, int(pm_x), int(pm_y), int(pm_z), width=int(pm_w), depth=int(pm_d), height=int(pm_h), count=mob_count)
                st.success(f"Placed **{n}** mobs inside the terrarium.")
            except Exception as e:
                st.error(str(e))
    else:
        st.info("Connect to Minecraft first.")

with tab_chat:
    st.subheader("Chat")
    if mc:
        st.caption("Type a message and press **Enter** to post in game chat.")
        prompt = st.chat_input("Message to post in game chat")
        if prompt:
            mc.postToChat(prompt)
            st.success("Posted to chat")
    else:
        st.info("Connect to Minecraft first.")

with tab_camera:
    st.subheader("Camera")
    if mc:
        mode = st.radio("Camera mode", ["Normal", "Fixed", "Follow entity"], horizontal=True)
        if mode == "Fixed":
            cam_x = st.number_input("Camera X", value=0, key="cam_x")
            cam_y = st.number_input("Camera Y", value=10, key="cam_y")
            cam_z = st.number_input("Camera Z", value=0, key="cam_z")
            if st.button("Set fixed camera"):
                mc.camera.setFixed()
                mc.camera.setPos(int(cam_x), int(cam_y), int(cam_z))
                st.success("Fixed camera set")
        elif mode == "Normal":
            if st.button("Set normal camera"):
                mc.camera.setNormal()
                st.success("Normal camera")
        else:
            eid = st.number_input("Entity ID to follow", value=0, key="follow_entity")
            if st.button("Set follow camera"):
                mc.camera.setFollow(int(eid))
                st.success("Following entity")
    else:
        st.info("Connect to Minecraft first.")

with tab_blocks:
    st.subheader("Block events (pollBlockHits)")
    if mc:
        if st.button("Poll block hits"):
            hits = mc.events.pollBlockHits()
            if not hits:
                st.info("No block hits since last poll.")
            else:
                for h in hits:
                    st.write(f"Pos: {h.pos.x}, {h.pos.y}, {h.pos.z} | face: {h.face} | entityId: {h.entityId}")
        if st.button("Clear all events"):
            mc.events.clearAll()
            st.success("Events cleared")
    else:
        st.info("Connect to Minecraft first.")

# Footer
st.divider()
st.caption("Minecraft Pi Edition API — [Pi My Life Up reference](https://pimylifeup.com/minecraft-pi-edition-api-reference/)")
