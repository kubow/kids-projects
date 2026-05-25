#!/usr/bin/env python3
"""Streamlit UI for Luanti via Miney (Python API)."""

import logging
import random
import traceback

import streamlit as st

from builds import BLOCK_ICONS, BUILDS, NODES, LuantiWorld, get_build

MAX_BROWSER_ERRORS = 20
_LOG_CAPTURE_INSTALLED = False

LANGUAGE_OPTIONS = {"cs": "Čeština", "en": "English"}

TRANSLATIONS = {
    "cs": {
        "header": "🌿 Luanti · Miney",
        "connect_caption": "Připojení k běžícímu Luanti serveru s aktivním modem **miney**.",
        "language": "Jazyk",
        "host": "Host",
        "port": "Port",
        "player": "Hráč",
        "password": "Heslo",
        "connect": "Připojit",
        "disconnect": "Odpojit",
        "connecting": "Připojování…",
        "connected": "Připojeno",
        "not_connected": "Nepřipojeno",
        "server_info": "Server: {version} · uzly: {nodes}",
        "tab_blocks": "Bloky",
        "tab_builds": "Stavby",
        "tab_player": "Hráč",
        "blocks_header": "Bloky",
        "connect_first": "Nejprve se připojte k Luanti (Miney).",
        "sync_position": "Synchronizovat pozici",
        "node_type": "Typ uzlu",
        "node_custom": "Vlastní název uzlu",
        "spread_mode": "Režim rozptylu",
        "radius": "Poloměr",
        "block_count": "Počet bloků",
        "place_block": "Umístit uzel",
        "placed_blocks": "Umístěno {count} uzlů.",
        "builds_header": "Stavby",
        "builds_caption": "Předpřipravené stavby přes Miney (uzly `default:*` — jiný game pack může vyžadovat jiné názvy).",
        "build_type": "Typ stavby",
        "place_build": "Umístit stavbu",
        "placed_build": "Stavba {name} byla umístěna.",
        "schematic_note": "Import `.schematic` z Minecraft Pi zde není — použijte [Minecraft app](../minecraft/app.py).",
        "player_header": "Hráč",
        "controlled_player": "Ovládaný hráč",
        "current_position": "Pozice: x={x:.1f}, y={y:.1f}, z={z:.1f}",
        "teleport": "Teleportovat",
        "teleported": "Hráč teleportován.",
        "chat_message": "Zpráva do chatu",
        "send_chat": "Odeslat všem",
        "chat_sent": "Zpráva odeslána.",
        "footer": "Luanti · Miney API",
        "miney_setup": "Před použitím: nainstalujte mod **miney** (ContentDB), zapněte ho ve světě a **Host server**. Viz [README](./README.md).",
        "console_errors": "Zachycené chyby: {count}",
        "show_errors": "Zobrazit chyby",
        "clear": "Vymazat",
    },
    "en": {
        "header": "🌿 Luanti · Miney",
        "connect_caption": "Connect to a running Luanti server with the **miney** mod enabled.",
        "language": "Language",
        "host": "Host",
        "port": "Port",
        "player": "Player",
        "password": "Password",
        "connect": "Connect",
        "disconnect": "Disconnect",
        "connecting": "Connecting…",
        "connected": "Connected",
        "not_connected": "Not connected",
        "server_info": "Server: {version} · nodes: {nodes}",
        "tab_blocks": "Blocks",
        "tab_builds": "Builds",
        "tab_player": "Player",
        "blocks_header": "Blocks",
        "connect_first": "Connect to Luanti (Miney) first.",
        "sync_position": "Sync position",
        "node_type": "Node type",
        "node_custom": "Custom node name",
        "spread_mode": "Spread mode",
        "radius": "Radius",
        "block_count": "Block count",
        "place_block": "Place node",
        "placed_blocks": "Placed {count} node(s).",
        "builds_header": "Builds",
        "builds_caption": "Preset builds via Miney (`default:*` nodes — other game packs may need different names).",
        "build_type": "Build type",
        "place_build": "Place build",
        "placed_build": "Placed build: {name}.",
        "schematic_note": "Minecraft Pi `.schematic` import is not supported here — use the [Minecraft app](../minecraft/app.py).",
        "player_header": "Player",
        "controlled_player": "Controlled player",
        "current_position": "Position: x={x:.1f}, y={y:.1f}, z={z:.1f}",
        "teleport": "Teleport",
        "teleported": "Player teleported.",
        "chat_message": "Chat message",
        "send_chat": "Send to all",
        "chat_sent": "Message sent.",
        "footer": "Luanti · Miney API",
        "miney_setup": "Before use: install the **miney** mod (ContentDB), enable it on your world, and **Host server**. See [README](./README.md).",
        "console_errors": "Captured errors: {count}",
        "show_errors": "Show errors",
        "clear": "Clear",
    },
}


def _t(key, **kwargs):
    lang = st.session_state.get("lang", "en")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def _format_exception(context, exc):
    return f"{context}\n{type(exc).__name__}: {exc}\n{traceback.format_exc()}"


def _store_browser_error(message):
    errors = st.session_state.setdefault("browser_errors", [])
    errors.append(message)
    if len(errors) > MAX_BROWSER_ERRORS:
        st.session_state.browser_errors = errors[-MAX_BROWSER_ERRORS:]


def _install_log_capture():
    global _LOG_CAPTURE_INSTALLED
    if _LOG_CAPTURE_INSTALLED:
        return

    class BrowserLogHandler(logging.Handler):
        def emit(self, record):
            try:
                _store_browser_error(self.format(record))
            except Exception:
                pass

    logging.getLogger().addHandler(BrowserLogHandler())
    _LOG_CAPTURE_INSTALLED = True


def _render_browser_errors():
    errors = st.session_state.get("browser_errors", [])
    if not errors:
        return
    cols = st.columns([6, 1])
    with cols[0]:
        st.warning(_t("console_errors", count=len(errors)))
    with cols[1]:
        if st.button(_t("clear"), key="clear_errors"):
            st.session_state.browser_errors = []
            st.rerun()
    with st.expander(_t("show_errors"), expanded=False):
        for err in reversed(errors):
            st.code(err, language="text")


def connect_luanti(host, port, player, password):
    try:
        import miney
        from miney.point import Point

        if st.session_state.get("lt"):
            try:
                st.session_state.lt.disconnect()
            except Exception:
                pass

        lt = miney.Luanti(
            server=host,
            port=int(port),
            playername=player or None,
            password=password,
        )
        st.session_state.lt = lt
        st.session_state.Point = Point
        st.session_state.mc_error = None
        try:
            node_names = list(lt.nodes.names)
        except Exception:
            node_names = list(NODES.values())
        st.session_state.node_names = sorted(set(node_names))
        st.session_state.server_version = getattr(lt, "version", "?")
        return True
    except Exception as exc:
        st.session_state.lt = None
        st.session_state.mc_error = str(exc)
        _store_browser_error(_format_exception("Luanti connection failed", exc))
        return False


def disconnect_luanti():
    lt = st.session_state.get("lt")
    if lt:
        try:
            lt.disconnect()
        except Exception as exc:
            _store_browser_error(_format_exception("Disconnect failed", exc))
    st.session_state.lt = None
    st.session_state.world = None
    st.session_state.mc_error = None


def get_lt():
    return st.session_state.get("lt")


def get_world():
    lt = get_lt()
    if not lt:
        return None
    if st.session_state.get("world") is None:
        st.session_state.world = LuantiWorld(lt)
    return st.session_state.world


def _controlled_player(lt):
    name = st.session_state.get("control_player")
    if name and name in lt.players:
        return lt.players[name]
    try:
        return lt.players[st.session_state.get("player", "miney")]
    except Exception:
        players = list(lt.players)
        return players[0] if players else None


def _player_tile_pos(lt):
    player = _controlled_player(lt)
    if not player:
        return 0, 0, 0
    try:
        pos = player.position
        return int(pos.x), int(pos.y), int(pos.z)
    except Exception:
        return 0, 0, 0


def _sync_position(prefix, lt):
    x, y, z = _player_tile_pos(lt)
    st.session_state[f"{prefix}_x"] = x
    st.session_state[f"{prefix}_y"] = y
    st.session_state[f"{prefix}_z"] = z


def _position_inputs(prefix, defaults):
    cols = st.columns(3)
    with cols[0]:
        x = st.number_input("X", value=int(st.session_state.get(f"{prefix}_x", defaults[0])), key=f"{prefix}_x")
    with cols[1]:
        y = st.number_input("Y", value=int(st.session_state.get(f"{prefix}_y", defaults[1])), key=f"{prefix}_y")
    with cols[2]:
        z = st.number_input("Z", value=int(st.session_state.get(f"{prefix}_z", defaults[2])), key=f"{prefix}_z")
    return int(x), int(y), int(z)


def _preset_node_options():
    return [f"{BLOCK_ICONS.get(key, '⬜')} {key}" for key in NODES]


def _label_to_preset_key(label):
    for key in NODES:
        if label.endswith(f" {key}"):
            return key
    return next(iter(NODES))


def _resolve_node_name(lt):
    use_custom = st.session_state.get("use_custom_node", False)
    if use_custom:
        custom = st.session_state.get("custom_node_name", "").strip()
        if custom:
            return custom
    label = st.session_state.get("place_node_select")
    if label:
        return NODES.get(_label_to_preset_key(label), label)
    return NODES["stone"]


def render_app():
    _render_browser_errors()
    st.info(_t("miney_setup"))

    with st.sidebar:
        st.header(_t("header"))
        st.caption(_t("connect_caption"))
        st.selectbox(_t("language"), options=list(LANGUAGE_OPTIONS.keys()),
                     format_func=lambda c: LANGUAGE_OPTIONS[c], key="lang")
        host = st.text_input(_t("host"), value="127.0.0.1", key="host")
        port = st.number_input(_t("port"), min_value=1, max_value=65535, value=30000, key="port")
        player = st.text_input(_t("player"), value="miney", key="player")
        password = st.text_input(_t("password"), value="ChangeThePassword!", type="password", key="password")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(_t("connect"), type="primary", use_container_width=True):
                with st.spinner(_t("connecting")):
                    connect_luanti(host, int(port), player, password)
        with col_b:
            if st.button(_t("disconnect"), use_container_width=True):
                disconnect_luanti()
                st.rerun()

        lt = get_lt()
        if lt:
            st.success(_t("connected"))
            st.caption(_t("server_info",
                           version=st.session_state.get("server_version", "?"),
                           nodes=len(st.session_state.get("node_names", []))))
            online = [p.name for p in lt.players if getattr(p, "is_online", True)]
            if online:
                st.selectbox(_t("controlled_player"), options=online, key="control_player")
        else:
            st.warning(st.session_state.get("mc_error") or _t("not_connected"))

    tab_blocks, tab_builds, tab_player = st.tabs([
        _t("tab_blocks"), _t("tab_builds"), _t("tab_player"),
    ])

    lt = get_lt()
    world = get_world()

    with tab_blocks:
        st.subheader(_t("blocks_header"))
        if lt and world:
            default_pos = _player_tile_pos(lt)
            action_col, sync_col = st.columns([3, 1])
            with action_col:
                st.selectbox(_t("node_type"), options=_preset_node_options(), key="place_node_select")
            with sync_col:
                st.write("")
                st.write("")
                if st.button(_t("sync_position"), key="place_sync", use_container_width=True):
                    _sync_position("place", lt)
                    st.rerun()
            st.checkbox(_t("node_custom"), key="use_custom_node")
            if st.session_state.get("use_custom_node"):
                node_options = st.session_state.get("node_names", list(NODES.values()))
                st.text_input(_t("node_custom"), value=NODES["stone"],
                              key="custom_node_name",
                              help=", ".join(node_options[:8]) + ("…" if len(node_options) > 8 else ""))
            place_x, place_y, place_z = _position_inputs("place", default_pos)
            spread = st.checkbox(_t("spread_mode"), key="place_spread")
            spread_radius, spread_count = 10, 25
            if spread:
                c1, c2 = st.columns(2)
                with c1:
                    spread_radius = st.number_input(_t("radius"), 1, 200, 10, key="place_radius")
                with c2:
                    spread_count = st.number_input(_t("block_count"), 1, 1000, 25, key="place_count")
            if st.button(_t("place_block"), type="primary", key="place_btn"):
                try:
                    node_name = _resolve_node_name(lt)
                    placed = 0
                    for _ in range(int(spread_count)):
                        x, z = place_x, place_z
                        if spread:
                            x += random.randint(-int(spread_radius), int(spread_radius))
                            z += random.randint(-int(spread_radius), int(spread_radius))
                        world.set_block(x, place_y, z, node_name)
                        placed += 1
                    st.success(_t("placed_blocks", count=placed))
                except Exception as exc:
                    _store_browser_error(_format_exception("Place node failed", exc))
                    st.error(str(exc))
        else:
            st.info(_t("connect_first"))

    with tab_builds:
        st.subheader(_t("builds_header"))
        st.caption(_t("builds_caption"))
        st.caption(_t("schematic_note"))
        if lt and world:
            from builds.definitions import BUILD_ICONS

            build_options = {
                f"{BUILD_ICONS.get(b['id'], '⬜')} {b['name']}": b["id"] for b in BUILDS
            }
            selected = st.selectbox(_t("build_type"), list(build_options.keys()))
            build = get_build(build_options[selected])
            if build:
                default_pos = _player_tile_pos(lt)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{build['name']}**")
                    st.caption(build["description"])
                with c2:
                    st.write("")
                    st.write("")
                    if st.button(_t("sync_position"), key="build_sync", use_container_width=True):
                        _sync_position("build", lt)
                        st.rerun()
                bx, by, bz = _position_inputs("build", default_pos)
                extra = {}
                for param_name, param_type, default, label in build.get("params", []):
                    if param_type == "int":
                        extra[param_name] = int(
                            st.number_input(label, value=int(default), key=f"b_{build['id']}_{param_name}")
                        )
                if st.button(_t("place_build"), type="primary", key="place_build_btn"):
                    try:
                        build["fn"](world, bx, by, bz, **extra)
                        st.success(_t("placed_build", name=build["name"]))
                    except Exception as exc:
                        _store_browser_error(_format_exception(f"Build failed: {build['name']}", exc))
                        st.error(str(exc))
        else:
            st.info(_t("connect_first"))

    with tab_player:
        st.subheader(_t("player_header"))
        if lt:
            player = _controlled_player(lt)
            if player:
                try:
                    pos = player.position
                    st.info(_t("current_position", x=pos.x, y=pos.y, z=pos.z))
                except Exception as exc:
                    st.warning(str(exc))
                tx, ty, tz = _position_inputs("tp", _player_tile_pos(lt))
                Point = st.session_state.get("Point")
                if st.button(_t("teleport"), type="primary", key="tp_btn"):
                    try:
                        if Point is None:
                            from miney.point import Point
                        player.position = Point(tx + 0.5, ty + 1.0, tz + 0.5)
                        st.success(_t("teleported"))
                    except Exception as exc:
                        _store_browser_error(_format_exception("Teleport failed", exc))
                        st.error(str(exc))
                st.divider()
                msg = st.text_input(_t("chat_message"), key="chat_msg")
                if st.button(_t("send_chat"), key="chat_btn"):
                    try:
                        if msg.strip():
                            lt.chat.send_to_all(msg.strip())
                            st.success(_t("chat_sent"))
                    except Exception as exc:
                        _store_browser_error(_format_exception("Chat failed", exc))
                        st.error(str(exc))
            else:
                st.warning(_t("not_connected"))
        else:
            st.info(_t("connect_first"))

    st.divider()
    st.caption(_t("footer"))


st.set_page_config(page_title="Luanti · Miney", page_icon="🌿", layout="wide")

if "lt" not in st.session_state:
    st.session_state.lt = None
if "mc_error" not in st.session_state:
    st.session_state.mc_error = None
if "lang" not in st.session_state:
    st.session_state.lang = "cs"

_install_log_capture()

try:
    render_app()
except Exception as exc:
    _store_browser_error(_format_exception("App render failed", exc))
    st.error(str(exc))
