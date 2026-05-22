# Luanti

This folder collects research on **Luanti** (formerly **Minetest**) on Linux and Raspberry Pi: install paths, content (games/mods), servers, and modding with Lua.

Luanti is an open-source voxel **game-creation platform** — one engine, many community **games** and **mods** from [ContentDB](https://content.luanti.org/). No Microsoft or Roblox account required.

Official site: [luanti.org](https://www.luanti.org/)

## Luanti platforms overview

| Platform | Official support | Best for | Main capabilities | Main limitations |
| --- | --- | --- | --- | --- |
| **Linux (distro package)** | Yes | Easiest install on Debian/Ubuntu/Pi OS | `apt install luanti` (or `minetest`), menu launcher, ContentDB in client | Package version may lag upstream |
| **Linux (Flatpak)** | Yes | Sandboxed install, multiple arches | Flathub build when available for your arch | Check Flathub for `x86_64` / `aarch64` |
| **Linux (compile from source)** | Yes | Newest engine or Pi when packages are old | Full control, server-only builds possible | Build deps and compile time |
| **Raspberry Pi OS (arm64)** | Yes | Open voxel sandbox on Pi hardware | Often lighter than Minecraft Java; LAN server on Pi | Lower FPS; pick lightweight games/mods |
| **Windows / macOS** | Yes | Same engine as Linux | Official downloads | Separate from Pi/Linux notes here |
| **Android** | Yes | Mobile play | Official app | Not the same as desktop server worlds |
| **Dedicated server** | Yes | Family LAN or headless host | `luanti --server`, Docker (arm64 tags) | Client and server versions should match; open UDP 30000 |

Legacy paths: user data is often still under `~/.minetest` or `$MINETEST_USER_PATH`; system installs may use `/usr/share/minetest`.

## Linux: install and play

### Distribution package (recommended first try)

```bash
sudo apt update
sudo apt install luanti
# package name may still be minetest on some distros:
# sudo apt install minetest
```

Launch **Luanti** from the application menu, open **ContentDB**, and install games (e.g. MineClone-style packs) and mods.

### Flatpak

1. Install [Flatpak](https://flatpak.org/setup/).
2. Search [Flathub](https://flathub.org/) for Luanti / Minetest for your architecture.
3. Install and run from the app menu; use ContentDB inside the client.

### Compile from source

Use when packages are too old or you need a server-only build. Full guide: [Compiling on GNU/Linux](https://github.com/luanti-org/luanti/blob/master/doc/compiling/linux.md).

Debian/Ubuntu dependencies (summary):

```bash
sudo apt install g++ make libc6-dev cmake libpng-dev libjpeg-dev libgl1-mesa-dev \
  libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-gnutls-dev \
  libfreetype6-dev zlib1g-dev libgmp-dev libjsoncpp-dev libzstd-dev \
  libluajit-5.1-dev gettext libsdl2-dev git

git clone --depth 1 https://github.com/luanti-org/luanti.git
cd luanti
cmake . -DRUN_IN_PLACE=TRUE
make -j$(nproc)
./bin/luanti
```

CMake notes:

- `-DRUN_IN_PLACE=FALSE` — system-wide install
- `-DBUILD_CLIENT=FALSE -DBUILD_SERVER=TRUE` — server only

## Raspberry Pi

Luanti is one of the more realistic **3D sandbox** options on Pi compared with Minecraft Java or Roblox on Pi OS.

### Client on Raspberry Pi OS

1. Prefer **Raspberry Pi OS 64-bit**.
2. `sudo apt install luanti` (or `minetest`).
3. In settings, reduce view distance, disable heavy effects if FPS is low.
4. Install **lightweight** games/mods from ContentDB — avoid huge mod packs on Pi 3/4.

### Server on Pi or PC

- Default game port: **UDP 30000**.
- Run a world on a Pi or home PC; connect clients on the same LAN.
- Match **Luanti version** on server and clients.

Docker (arm64 supported — [linuxserver/docker-luanti](https://github.com/linuxserver/docker-luanti)):

```bash
docker run -d \
  --name=luanti \
  -e PUID=1000 -e PGID=1000 \
  -p 30000:30000/udp \
  -v /path/to/luanti-data:/config/.minetest \
  lscr.io/linuxserver/luanti:latest
```

The image may not include a default game; add one via ContentDB or copy into `/config/.minetest/games/`.

## Games, mods, and ContentDB

### ContentDB (in-client)

Capabilities:

- browse and install **games**, **mods**, and texture packs from inside Luanti
- thousands of community packages; no single official “Luanti game” required

Limitations:

- quality and kid-friendliness vary — parents should pick packs deliberately
- online ContentDB needs network access

### Lua modding

Capabilities:

- mods and subgames use **Lua** and the engine API
- good progression from playing → tweaking → writing small mods
- can publish to ContentDB when ready

Limitations:

- not the same language as Minecraft Java mods or Roblox Luau
- documentation is spread across wiki and mod examples

### MineClone-style games

Capabilities:

- community games (e.g. MineClone2) give a Minecraft-**inspired** survival/creative feel without buying Minecraft

Limitations:

- not official Minecraft; mechanics and updates differ
- heavier packs may be too much for older Pi models

## Multiplayer

| Approach | Notes |
| --- | --- |
| **Public servers** | Server list in client — review rules and chat with kids |
| **LAN / home server** | Host on Pi or PC; clients join by address |
| **Internet-hosted** | Port-forward UDP 30000 only if you understand the security trade-offs |

## Practical recommendation for this repo

| Goal | Recommendation |
| --- | --- |
| **Open voxel sandbox on Linux or Pi** | Distro `luanti` package first; ContentDB for a game pack |
| **Teach programming / modding** | Small Lua mods; later subgames on ContentDB |
| **Private family world** | Luanti server on LAN (Pi or PC) + clients on same version |
| **Python block API like this repo’s Minecraft app** | Use [../minecraft/README.md](../minecraft/README.md) — different stack |
| **Roblox-scale UGC catalog** | Use [../roblox/README.md](../roblox/README.md) |

## Related sandbox / UGC options

Platforms in this repo (see [../README.md](../README.md)):

- [Minecraft](../minecraft/README.md) — commercial sandbox; Pi Python API in this repo
- [Terasology](../terasology/README.md) — open Java modules; desktop x86_64
- [Roblox](../roblox/README.md) — commercial UGC platform

Luanti-adjacent links:

- [Freeminer](https://freeminer.org/) — fork in the Minetest / Luanti family tree
- [Minetest Game](https://github.com/minetest/minetest_game) — historical default game
- [Veloren](https://veloren.net/) — open multiplayer voxel RPG (different genre)

## Key links

### Official / upstream

- [Luanti](https://www.luanti.org/)
- [Downloads](https://www.luanti.org/downloads/)
- [GitHub — luanti-org/luanti](https://github.com/luanti-org/luanti)
- [ContentDB](https://content.luanti.org/)

### Docs and community

- [Compiling on Linux](https://github.com/luanti-org/luanti/blob/master/doc/compiling/linux.md)
- [Getting started (wiki)](https://wiki.luanti.org/Getting_Started)
- [linuxserver/docker-luanti](https://github.com/linuxserver/docker-luanti)
