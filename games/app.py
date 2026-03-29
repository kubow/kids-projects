#!/usr/bin/env python3
"""
Streamlit UI for Minecraft Pi Edition API.
"""

import io
import logging
import random
import sys
import threading
import traceback

import streamlit as st

from builds import BUILDS, get_build, populate_terrarium_mobs
from schematic import load_schematic, place_schematic


BLOCK_REF = {
    "Air": 0,
    "Stone": 1,
    "Grass": 2,
    "Dirt": 3,
    "Cobblestone": 4,
    "Wood planks": 5,
    "Sapling": 6,
    "Bedrock": 7,
    "Water": 8,
    "Still water": 9,
    "Lava": 10,
    "Still lava": 11,
    "Sand": 12,
    "Gravel": 13,
    "Gold ore": 14,
    "Iron ore": 15,
    "Coal ore": 16,
    "Wood": 17,
    "Leaves": 18,
    "Glass": 20,
    "Lapis lazuli block": 22,
    "Sandstone": 24,
    "Bed": 26,
    "Cobweb": 30,
    "Tall grass": 31,
    "Wool": 35,
    "Yellow flower": 37,
    "Cyan flower": 38,
    "Brown mushroom": 39,
    "Red mushroom": 40,
    "Gold block": 41,
    "Iron block": 42,
    "Double slab": 43,
    "Slab": 44,
    "Brick": 45,
    "TNT": 46,
    "Bookshelf": 47,
    "Moss stone": 48,
    "Obsidian": 49,
    "Torch": 50,
    "Fire": 51,
    "Stairs (wood)": 53,
    "Chest": 54,
    "Diamond ore": 56,
    "Diamond block": 57,
    "Crafting table": 58,
    "Farmland": 60,
    "Furnace": 61,
    "Lit furnace": 62,
    "Door": 64,
    "Ladder": 65,
    "Stairs (cobblestone)": 67,
    "Snow": 78,
    "Ice": 79,
    "Snow block": 80,
    "Cactus": 81,
    "Clay": 82,
    "Sugar cane": 83,
    "Fence": 85,
    "Glowstone": 89,
    "Invisible bedrock": 95,
    "Stone brick": 98,
    "Glass pane": 102,
    "Melon": 103,
    "Fence gate": 107,
    "Glowing obsidian": 246,
    "Nether reactor core": 247,
}


BLOCK_ICONS = {
    "Air": "⬜",
    "Stone": "🪨",
    "Grass": "🌿",
    "Dirt": "🟫",
    "Cobblestone": "🪨",
    "Wood planks": "🪵",
    "Sapling": "🌱",
    "Bedrock": "⬛",
    "Water": "💧",
    "Still water": "💧",
    "Lava": "🔥",
    "Still lava": "🔥",
    "Sand": "🟨",
    "Gravel": "🪨",
    "Gold ore": "🟨",
    "Iron ore": "⛏️",
    "Coal ore": "⚫",
    "Wood": "🪵",
    "Leaves": "🍃",
    "Glass": "🪟",
    "Lapis lazuli block": "🔷",
    "Sandstone": "🟨",
    "Bed": "🛏️",
    "Cobweb": "🕸️",
    "Tall grass": "🌾",
    "Wool": "🧶",
    "Yellow flower": "🌸",
    "Cyan flower": "💠",
    "Brown mushroom": "🍄",
    "Red mushroom": "🍄",
    "Gold block": "🟨",
    "Iron block": "⬜",
    "Double slab": "🧱",
    "Slab": "🧱",
    "Brick": "🧱",
    "TNT": "🧨",
    "Bookshelf": "📚",
    "Moss stone": "🪨",
    "Obsidian": "🟪",
    "Torch": "🔦",
    "Fire": "🔥",
    "Stairs (wood)": "🪵",
    "Chest": "📦",
    "Diamond ore": "💎",
    "Diamond block": "💎",
    "Crafting table": "🛠️",
    "Farmland": "🌱",
    "Furnace": "🔥",
    "Lit furnace": "🔥",
    "Door": "🚪",
    "Ladder": "🪜",
    "Stairs (cobblestone)": "🪨",
    "Snow": "❄️",
    "Ice": "🧊",
    "Snow block": "☃️",
    "Cactus": "🌵",
    "Clay": "🟤",
    "Sugar cane": "🫚",
    "Fence": "🪵",
    "Glowstone": "✨",
    "Stone brick": "🧱",
    "Glass pane": "🪟",
    "Melon": "🍈",
    "Fence gate": "🚧",
    "Glowing obsidian": "✨",
    "Nether reactor core": "⚛️",
}


BUILD_ICONS = {
    "simple_house": "🏠",
    "tower": "🗼",
    "wall": "🧱",
    "pyramid": "🔺",
    "platform": "📦",
    "pillar": "🪵",
    "sphere": "⚽",
    "hollow_sphere": "⭕",
    "circle": "⭕",
    "horizontal_circle": "⭕",
    "line": "📏",
    "statue_pillar": "🗿",
    "statue_steve": "🧑",
    "statue_owl": "🦉",
    "statue_dragon": "🐉",
    "car_simple": "🚗",
    "car_buggy": "🚙",
    "rocket": "🚀",
    "rainbow_arch": "🌈",
    "tree_oak": "🌳",
    "castle_gate": "🏰",
    "smiley_pixel_art": "🙂",
    "campfire": "🔥",
    "mob_creeper": "💚",
    "mob_pig": "🐷",
    "mob_sheep": "🐑",
    "mob_slime": "🟢",
    "mob_enderman": "🖤",
    "mob_zombie": "🧟",
    "terrarium": "🪟",
}


MAX_BROWSER_ERRORS = 20
_LOG_CAPTURE_INSTALLED = False


def _ensure_error_state():
    if "browser_errors" not in st.session_state:
        st.session_state.browser_errors = []


def _store_browser_error(message: str):
    _ensure_error_state()
    cleaned = (message or "").strip()
    if not cleaned:
        return

    errors = st.session_state.browser_errors
    if errors and errors[-1] == cleaned:
        return

    errors.append(cleaned)
    if len(errors) > MAX_BROWSER_ERRORS:
        del errors[:-MAX_BROWSER_ERRORS]


def _format_exception(title: str, exc: BaseException) -> str:
    details = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)).strip()
    return f"{title}\n{details}"


class BrowserErrorHandler(logging.Handler):
    def emit(self, record):
        try:
            if record.levelno < logging.ERROR:
                return
            _store_browser_error(self.format(record))
        except Exception:
            pass


class TeeStderr(io.TextIOBase):
    def __init__(self, original):
        self.original = original
        self._buffer = ""

    def write(self, text):
        if self.original:
            self.original.write(text)
        if not text:
            return 0

        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                _store_browser_error(line)
        return len(text)

    def flush(self):
        if self.original:
            self.original.flush()
        if self._buffer.strip():
            _store_browser_error(self._buffer)
            self._buffer = ""


def _install_browser_error_capture():
    global _LOG_CAPTURE_INSTALLED
    _ensure_error_state()

    if not st.session_state.get("_browser_stderr_installed"):
        sys.stderr = TeeStderr(sys.stderr)
        st.session_state._browser_stderr_installed = True

    if not _LOG_CAPTURE_INSTALLED:
        handler = BrowserErrorHandler()
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logging.getLogger().addHandler(handler)
        _LOG_CAPTURE_INSTALLED = True

    def _browser_excepthook(exc_type, exc, tb):
        _store_browser_error("Uncaught exception\n" + "".join(traceback.format_exception(exc_type, exc, tb)).strip())
        if sys.__excepthook__:
            sys.__excepthook__(exc_type, exc, tb)

    def _thread_excepthook(args):
        _store_browser_error(
            "Thread exception\n"
            + "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)).strip()
        )
        if hasattr(threading, "__excepthook__"):
            threading.__excepthook__(args)

    sys.excepthook = _browser_excepthook
    if hasattr(threading, "excepthook"):
        threading.excepthook = _thread_excepthook


def _render_browser_errors():
    _ensure_error_state()
    errors = st.session_state.browser_errors
    if not errors:
        return

    header_cols = st.columns([6, 1])
    with header_cols[0]:
        st.warning(f"Console errors captured: {len(errors)}")
    with header_cols[1]:
        if st.button("Clear", key="clear_browser_errors", use_container_width=True):
            st.session_state.browser_errors = []
            st.rerun()

    with st.expander("Show console errors", expanded=False):
        st.caption("Recent stderr, logging, and uncaught Python exceptions are mirrored here.")
        for index, error in enumerate(reversed(errors), start=1):
            st.code(error, language="text")
            if index < len(errors):
                st.divider()


def connect_minecraft(host: str, port: int):
    try:
        from mcpi.minecraft import Minecraft

        st.session_state.mc = Minecraft.create(host, port)
        st.session_state.mc_error = None
        return True
    except Exception as exc:
        st.session_state.mc = None
        st.session_state.mc_error = str(exc)
        _store_browser_error(_format_exception("Minecraft connection failed", exc))
        return False


def get_mc():
    return st.session_state.get("mc")


def _get_player_tile_pos(mc):
    try:
        pos = mc.player.getTilePos()
        return int(pos.x), int(pos.y), int(pos.z)
    except Exception:
        return 0, 0, 0


def _sync_position_from_player(mc, prefix: str):
    x, y, z = _get_player_tile_pos(mc)
    st.session_state[f"{prefix}_x"] = x
    st.session_state[f"{prefix}_y"] = y
    st.session_state[f"{prefix}_z"] = z


def _position_inputs(prefix: str, defaults):
    cols = st.columns(3)
    with cols[0]:
        x = st.number_input("X", value=int(st.session_state.get(f"{prefix}_x", defaults[0])), key=f"{prefix}_x")
    with cols[1]:
        y = st.number_input("Y", value=int(st.session_state.get(f"{prefix}_y", defaults[1])), key=f"{prefix}_y")
    with cols[2]:
        z = st.number_input("Z", value=int(st.session_state.get(f"{prefix}_z", defaults[2])), key=f"{prefix}_z")
    return int(x), int(y), int(z)


def _block_display_options():
    return [f"{BLOCK_ICONS.get(name, '⬜')} {name}" for name in BLOCK_REF]


def _block_label_to_key(label):
    for key in BLOCK_REF:
        if label == f"{BLOCK_ICONS.get(key, '⬜')} {key}":
            return key
    for key in BLOCK_REF:
        if label.endswith(" " + key):
            return key
    return next(iter(BLOCK_REF))


def _sync_selected_block_defaults():
    selected_label = st.session_state.get("place_block_select")
    if not selected_label:
        return
    selected_key = _block_label_to_key(selected_label)
    if st.session_state.get("place_block_select_previous") != selected_key:
        st.session_state["place_block_id"] = BLOCK_REF[selected_key]
        st.session_state["place_block_data"] = 0
        st.session_state["place_block_select_previous"] = selected_key


def _entity_type_options(mc):
    entity_types = mc.getEntityTypes()
    return {
        f"{entity.id}: {entity.name}": entity.id
        for entity in entity_types
    }


def _fallback_block_options():
    return ["Skip unsupported blocks"] + [f"{BLOCK_ICONS.get(name, '⬜')} {name}" for name in BLOCK_REF]


def render_app():
    _render_browser_errors()

    with st.sidebar:
        st.header("⛏️ Minecraft Pi API")
        st.caption("Connect to Minecraft Pi Edition or RaspberryJuice.")

        host = st.text_input("Host", value="localhost", key="host")
        port = st.number_input("Port", min_value=1, max_value=65535, value=4711, key="port")

        if st.button("Connect", type="primary", use_container_width=True):
            with st.spinner("Connecting…"):
                connect_minecraft(host, int(port))

        mc = get_mc()
        if mc:
            st.success("Connected")
        else:
            st.warning(st.session_state.mc_error or "Not connected")

    tab_blocks, tab_builds, tab_entities, tab_player = st.tabs(["Blocks", "Builds", "Entities", "Player"])

    with tab_blocks:
        st.subheader("Blocks")
        if mc:
            default_pos = _get_player_tile_pos(mc)
            action_col, sync_col = st.columns([3, 1])
            with action_col:
                place_block_label = st.selectbox(
                    "Block type",
                    options=_block_display_options(),
                    key="place_block_select",
                    help="Choose a known block ID preset. Some blocks also use the block data value below.",
                )
            with sync_col:
                st.write("")
                st.write("")
                if st.button("Sync position", key="place_sync_btn", use_container_width=True):
                    _sync_position_from_player(mc, "place")
                    st.rerun()

            _sync_selected_block_defaults()
            place_block_key = _block_label_to_key(place_block_label)

            block_cols = st.columns(2)
            with block_cols[0]:
                place_block_id = st.number_input(
                    "Block ID",
                    min_value=0,
                    value=int(st.session_state.get("place_block_id", BLOCK_REF[place_block_key])),
                    key="place_block_id",
                )
            with block_cols[1]:
                place_block_data = st.number_input(
                    "Block data",
                    min_value=0,
                    value=int(st.session_state.get("place_block_data", 0)),
                    key="place_block_data",
                )

            place_x, place_y, place_z = _position_inputs("place", default_pos)

            spread_mode = st.checkbox("Spread mode", value=False, key="place_spread_mode")
            spread_radius = 0
            spread_count = 1
            if spread_mode:
                spread_cols = st.columns(2)
                with spread_cols[0]:
                    spread_radius = st.number_input(
                        "Radius",
                        min_value=1,
                        max_value=200,
                        value=10,
                        key="place_spread_radius",
                    )
                with spread_cols[1]:
                    spread_count = st.number_input(
                        "Brick count",
                        min_value=1,
                        max_value=1000,
                        value=25,
                        key="place_spread_count",
                    )

            if st.button("Place block", type="primary", key="place_block_btn"):
                try:
                    placed = 0
                    for _ in range(spread_count):
                        x = place_x
                        z = place_z
                        if spread_mode:
                            x += random.randint(-spread_radius, spread_radius)
                            z += random.randint(-spread_radius, spread_radius)
                        mc.setBlock(x, place_y, z, int(place_block_id), int(place_block_data))
                        placed += 1
                    st.success(f"Placed {placed} block{'s' if placed != 1 else ''}.")
                except Exception as exc:
                    _store_browser_error(_format_exception("Block placement failed", exc))
                    st.error(str(exc))
        else:
            st.info("Connect to Minecraft first.")

    with tab_builds:
        st.subheader("Builds")
        st.caption("Place a predefined build, then optionally populate a terrarium with mobs.")

        if mc:
            build_options = {
                f"{BUILD_ICONS.get(build['id'], '⬜')} {build['name']}": build["id"]
                for build in BUILDS
            }
            selected_label = st.selectbox("Build type", list(build_options.keys()))
            build_id = build_options[selected_label]
            build = get_build(build_id)

            if build:
                default_pos = _get_player_tile_pos(mc)
                action_col, sync_col = st.columns([3, 1])
                with action_col:
                    st.markdown(f"**{build['name']}**")
                    st.caption(build["description"])
                with sync_col:
                    st.write("")
                    st.write("")
                    if st.button("Sync position", key="build_sync_btn", use_container_width=True):
                        _sync_position_from_player(mc, "build")
                        st.rerun()

                build_x, build_y, build_z = _position_inputs("build", default_pos)

                extra = {}
                for param_name, param_type, default, label in build.get("params", []):
                    if param_type == "int":
                        extra[param_name] = int(
                            st.number_input(label, value=int(default), key=f"build_{build_id}_{param_name}")
                        )

                if st.button("Place build", type="primary", key="place_build_btn"):
                    try:
                        build["fn"](mc, build_x, build_y, build_z, **extra)
                        st.success(f"Placed {build['name']}.")
                    except Exception as exc:
                        _store_browser_error(_format_exception(f"Build placement failed: {build['name']}", exc))
                        st.error(str(exc))

            with st.expander("Import .schematic file"):
                st.caption("Upload a classic MCEdit .schematic file and place it in the world.")
                st.markdown("[Browse schematics on mcbuild.org](https://mcbuild.org/schematics)")

                uploaded_schematic = st.file_uploader(
                    "Schematic file",
                    type=["schematic"],
                    key="schematic_upload",
                    help="The file stays local to this session unless you place it.",
                )

                if uploaded_schematic is not None:
                    try:
                        schematic = load_schematic(uploaded_schematic.getvalue())
                        st.session_state.loaded_schematic = schematic
                        st.session_state.loaded_schematic_name = uploaded_schematic.name
                    except Exception as exc:
                        st.session_state.pop("loaded_schematic", None)
                        st.session_state.pop("loaded_schematic_name", None)
                        _store_browser_error(_format_exception("Schematic load failed", exc))
                        st.error(str(exc))

                schematic = st.session_state.get("loaded_schematic")
                schematic_name = st.session_state.get("loaded_schematic_name")

                if schematic:
                    st.info(
                        f"Loaded `{schematic_name}` "
                        f"({schematic['width']} x {schematic['height']} x {schematic['length']}, "
                        f"materials: {schematic['materials']})."
                    )

                    import_col, sync_col = st.columns([3, 1])
                    with import_col:
                        st.caption("Import position")
                    with sync_col:
                        st.write("")
                        if st.button("Sync position", key="schem_sync_btn", use_container_width=True):
                            _sync_position_from_player(mc, "schem")
                            st.rerun()

                    schem_x, schem_y, schem_z = _position_inputs("schem", _get_player_tile_pos(mc))

                    fallback_label = st.selectbox(
                        "Unsupported blocks",
                        options=_fallback_block_options(),
                        key="schematic_fallback_select",
                        help="Minecraft Pi supports only older block IDs. Unsupported blocks can be skipped or replaced.",
                    )

                    if st.button("Place schematic", type="primary", key="place_schematic_btn"):
                        try:
                            fallback_block_id = None
                            if fallback_label != "Skip unsupported blocks":
                                fallback_block_id = BLOCK_REF[_block_label_to_key(fallback_label)]

                            result = place_schematic(
                                mc,
                                schem_x,
                                schem_y,
                                schem_z,
                                schematic,
                                allowed_block_ids=set(BLOCK_REF.values()),
                                fallback_block_id=fallback_block_id,
                            )
                            st.success(f"Placed {result['placed']} schematic blocks.")
                            if result["replaced"]:
                                st.warning(f"Replaced {result['replaced']} unsupported block(s) with the fallback block.")
                            if result["skipped"]:
                                st.warning(f"Skipped {result['skipped']} unsupported block(s).")
                        except Exception as exc:
                            _store_browser_error(_format_exception("Schematic placement failed", exc))
                            st.error(str(exc))

            with st.expander("Terrarium mobs"):
                st.caption("Use this after placing the terrarium build.")
                terr_default_pos = (
                    int(st.session_state.get("build_x", _get_player_tile_pos(mc)[0])),
                    int(st.session_state.get("build_y", _get_player_tile_pos(mc)[1])),
                    int(st.session_state.get("build_z", _get_player_tile_pos(mc)[2])),
                )
                if st.button("Use build position", key="terr_use_build_pos"):
                    st.session_state["terr_x"] = int(st.session_state.get("build_x", terr_default_pos[0]))
                    st.session_state["terr_y"] = int(st.session_state.get("build_y", terr_default_pos[1]))
                    st.session_state["terr_z"] = int(st.session_state.get("build_z", terr_default_pos[2]))
                    st.rerun()

                tx, ty, tz = _position_inputs("terr", terr_default_pos)

                size_cols = st.columns(3)
                with size_cols[0]:
                    tw = st.number_input("Width", value=50, min_value=10, key="terr_w")
                with size_cols[1]:
                    td = st.number_input("Depth", value=50, min_value=10, key="terr_d")
                with size_cols[2]:
                    th = st.number_input("Height", value=20, min_value=5, key="terr_h")

                mob_count = st.slider("Mob count", min_value=1, max_value=50, value=15, key="terr_mob_count")
                if st.button("Spawn mobs", type="primary", key="terr_spawn"):
                    try:
                        result = populate_terrarium_mobs(
                            mc,
                            tx,
                            ty,
                            tz,
                            width=int(tw),
                            depth=int(td),
                            height=int(th),
                            count=mob_count,
                        )
                        placed = int(result["placed"])
                        failed = int(result["failed"])
                        errors = result["errors"]
                        if placed:
                            st.success(f"Placed {placed} mob build{'s' if placed != 1 else ''}.")
                        if failed:
                            summary = f"{failed} mob placement{'s' if failed != 1 else ''} failed."
                            _store_browser_error("Terrarium mob placement issues\n" + "\n".join(errors[:10]))
                            st.warning(summary)
                            with st.expander("Show terrarium placement errors", expanded=False):
                                for error in errors:
                                    st.code(error, language="text")
                        if not placed and not failed:
                            st.info("No mobs were placed.")
                    except Exception as exc:
                        _store_browser_error(_format_exception("Terrarium mob placement failed", exc))
                        st.error(str(exc))
        else:
            st.info("Connect to Minecraft first.")

    with tab_entities:
        st.subheader("Entities")
        st.caption("Spawn supported entities, inspect loaded entities, or remove them.")

        if mc:
            try:
                entity_options = _entity_type_options(mc)
            except Exception as exc:
                _store_browser_error(_format_exception("Entity type lookup failed", exc))
                st.error(str(exc))
                entity_options = {}

            default_pos = _get_player_tile_pos(mc)
            action_col, sync_col = st.columns([3, 1])
            with action_col:
                entity_label = st.selectbox(
                    "Entity type",
                    options=list(entity_options.keys()),
                    key="entity_type_select",
                    help="Entity IDs come from the connected server.",
                ) if entity_options else None
            with sync_col:
                st.write("")
                st.write("")
                if st.button("Sync position", key="entity_sync_btn", use_container_width=True):
                    _sync_position_from_player(mc, "entity")
                    st.rerun()

            entity_x, entity_y, entity_z = _position_inputs("entity", default_pos)

            if st.button("Spawn entity", type="primary", key="spawn_entity_btn", disabled=not entity_options):
                try:
                    entity_id = entity_options[entity_label]
                    spawned_id = mc.spawnEntity(entity_x, entity_y, entity_z, int(entity_id))
                    st.success(f"Spawned entity {entity_label} with id {spawned_id}.")
                except Exception as exc:
                    _store_browser_error(_format_exception("Entity spawn failed", exc))
                    st.error(str(exc))

            st.divider()

            list_col, filter_col = st.columns([2, 1])
            with filter_col:
                type_filter = st.checkbox("Filter by selected type", value=False, key="entity_filter_selected_type")
            with list_col:
                if st.button("Refresh loaded entities", key="refresh_entities_btn"):
                    st.session_state.pop("loaded_entities", None)

            try:
                filter_id = entity_options[entity_label] if (entity_options and entity_label and type_filter) else -1
                loaded_entities = mc.getEntities(int(filter_id))
                st.session_state.loaded_entities = loaded_entities
            except Exception as exc:
                _store_browser_error(_format_exception("Entity list failed", exc))
                st.error(str(exc))
                loaded_entities = st.session_state.get("loaded_entities", [])

            st.caption(f"Loaded entities: {len(loaded_entities)}")
            if loaded_entities:
                entity_rows = [
                    {
                        "entity_id": entity[0],
                        "type_id": entity[1],
                        "type_name": entity[2],
                        "x": entity[3],
                        "y": entity[4],
                        "z": entity[5],
                    }
                    for entity in loaded_entities
                ]
                st.dataframe(entity_rows, use_container_width=True, hide_index=True)

                remove_col, remove_type_col = st.columns(2)
                with remove_col:
                    entity_ids = [row["entity_id"] for row in entity_rows]
                    selected_remove_id = st.selectbox("Remove one entity", options=entity_ids, key="remove_entity_id")
                    if st.button("Remove selected entity", key="remove_entity_btn", use_container_width=True):
                        try:
                            removed = mc.removeEntity(int(selected_remove_id))
                            st.success(f"Removed {removed} entity.")
                        except Exception as exc:
                            _store_browser_error(_format_exception("Remove entity failed", exc))
                            st.error(str(exc))

                with remove_type_col:
                    remove_type_label = st.selectbox(
                        "Remove by type",
                        options=["All loaded entities"] + list(entity_options.keys()),
                        key="remove_entity_type_select",
                    )
                    if st.button("Remove by type", key="remove_entities_by_type_btn", use_container_width=True):
                        try:
                            remove_type_id = -1 if remove_type_label == "All loaded entities" else entity_options[remove_type_label]
                            removed = mc.removeEntities(int(remove_type_id))
                            st.success(f"Removed {removed} entit{'y' if removed == 1 else 'ies'}.")
                        except Exception as exc:
                            _store_browser_error(_format_exception("Remove entities by type failed", exc))
                            st.error(str(exc))
            else:
                st.info("No loaded entities found.")
        else:
            st.info("Connect to Minecraft first.")

    with tab_player:
        st.subheader("Player")
        if mc:
            px, py, pz = _get_player_tile_pos(mc)
            st.info(f"Current tile position: x={px}, y={py}, z={pz}")

            tx, ty, tz = _position_inputs("teleport", (px, py, pz))
            if st.button("Teleport", type="primary", key="teleport_btn"):
                try:
                    mc.player.setTilePos(tx, ty, tz)
                    st.success("Teleported.")
                except Exception as exc:
                    _store_browser_error(_format_exception("Teleport failed", exc))
                    st.error(str(exc))
        else:
            st.info("Connect to Minecraft first.")

    st.divider()
    st.caption("Minecraft Pi Edition API")


st.set_page_config(
    page_title="Minecraft Pi API",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "mc" not in st.session_state:
    st.session_state.mc = None
if "mc_error" not in st.session_state:
    st.session_state.mc_error = None

_install_browser_error_capture()

try:
    render_app()
except Exception as exc:
    _store_browser_error(_format_exception("App render failed", exc))
    st.error("The app hit an unexpected error. See the console errors panel above for details.")
