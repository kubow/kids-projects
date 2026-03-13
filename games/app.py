#!/usr/bin/env python3
"""
Streamlit UI for Minecraft Pi Edition API.
Connect to a Minecraft Pi (or RaspberryJuice) client and control the world,
player, place predefined builds, post to chat, and more.

API reference: https://pimylifeup.com/minecraft-pi-edition-api-reference/
"""

import streamlit as st

from builds import BUILDS, get_build

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
tab_world, tab_player, tab_builds, tab_chat, tab_camera, tab_blocks = st.tabs([
    "World (blocks)", "Player", "Predefined builds", "Chat", "Camera", "Block events",
])

# Common block IDs (Minecraft Pi / API reference)
BLOCK_REF = {
    "Air": 0, "Stone": 1, "Grass": 2, "Dirt": 3, "Cobblestone": 4,
    "Wood planks": 5, "Glass": 20, "Wool": 35, "Brick": 45, "TNT": 46,
    "Bookshelf": 47, "Torch": 50, "Wood": 17, "Glowstone": 89,
    "Sandstone": 24, "Gold block": 41, "Iron block": 42, "Diamond block": 57,
}

with tab_world:
    st.subheader("World / blocks")
    with st.expander("Block ID reference (common) & seed blocks"):
        st.caption("Full list: [Pi My Life Up API reference](https://pimylifeup.com/minecraft-pi-edition-api-reference/)")
        cols = st.columns(4)
        for i, (name, bid) in enumerate(BLOCK_REF.items()):
            cols[i % 4].code(f"{name}: {bid}")
        st.divider()
        st.markdown("**Seed blocks around the map** — scatter a selected block at random positions in an area.")
        if mc:
            seed_block_label = st.selectbox(
                "Block to seed",
                options=list(BLOCK_REF.keys()),
                key="seed_block_select",
            )
            seed_block_id = BLOCK_REF[seed_block_label]
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
                st.success(f"Placed **{placed}** blocks of **{seed_block_label}** in the area.")
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
        build_options = {f"{b['name']} — {b['description']}": b["id"] for b in BUILDS}
        selected_label = st.selectbox("Choose a build", list(build_options.keys()))
        build_id = build_options[selected_label]
        build = get_build(build_id)
        if not build:
            st.error("Unknown build")
        else:
            st.markdown(f"**{build['name']}**: {build['description']}")
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
