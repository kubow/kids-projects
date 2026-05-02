# Minecraft

This folder collects the Minecraft notes and the Streamlit tooling used in this repo.

## Streamlit app for Minecraft Pi / RaspberryJuice

The app in [app.py](/home/jav/Documents/kids-projects/games/minecraft/app.py) is a small web UI for the **Minecraft Pi Edition API**. It can connect either to:

- **Minecraft Pi Edition**
- **RaspberryJuice**, the compatibility plugin that exposes a similar API from a Java server

Main features:

- connect to a running Minecraft API server by host and port
- place predefined builds such as houses, towers, walls, pyramids, spheres, pixel art, statues, and simple mobs
- inspect and place blocks
- move the player and use basic camera/chat controls
- import `.schematic` files with fallback handling for unsupported blocks

Run from the repo root:

```bash
source venv/bin/activate
pip install -r requirements.txt
streamlit run games/minecraft/app.py
```

Python packages used:

- [`mcpi`](https://pypi.org/project/mcpi/)
- [`minecraftstuff`](https://pypi.org/project/minecraftstuff/)

Important note:

- This app is tied to the **old Minecraft Pi style API**.
- It is best treated as a **teaching and scripting tool**, not as a modern general Minecraft launcher.
- `RaspberryJuice` is an old compatibility plugin, so it is useful for experiments but not a clean modern foundation for up-to-date Java Minecraft.

## Minecraft versions overview

| Version | Best for | Main capabilities | Main limitations |
|---|---|---|---|
| **Minecraft Pi Edition** | Learning programming basics on Raspberry Pi | Simple block world, local building, Python/API control, easy automation, lightweight | Very old version, no modern updates, very limited blocks/features, no full Survival experience, not compatible with modern Minecraft multiplayer |
| **Minecraft Java Edition** | Maximum flexibility, mods, private servers, technical play | Full PC version, huge modding scene, custom servers, snapshots, commands, redstone/community tooling | PC only, no cross-play with Bedrock, setup can be more technical, performance depends more on the computer/modpack |
| **Minecraft Bedrock Edition** | Easy multiplayer across devices | Cross-play on many devices, Marketplace content, good controller/touch support, smoother console/mobile experience, split-screen on consoles | Limited modding compared with Java, many servers/features depend on Microsoft account/ecosystem, less open for deep customization |

### Minecraft Pi Edition

Capabilities:

- designed for Raspberry Pi and beginner programming
- lets you place and remove blocks, move the player, read positions, change the camera, and post chat messages through the API
- good for small coding projects, automation, and simple world editing
- lightweight and easy to run on low-power hardware

Limitations:

- very old and heavily cut down compared with modern Minecraft
- mostly focused on classic-style building, not the full modern game
- far fewer blocks, mechanics, mobs, biomes, and gameplay systems
- no modern cross-play, Marketplace, Realms, or current survival features

### Minecraft Java Edition

Capabilities:

- desktop version for Windows, macOS, and Linux
- supports mods, modpacks, shaders, custom maps, data packs, and large third-party servers
- strong for redstone, technical builds, commands, automation, and community tooling
- supports snapshots for testing upcoming features

Limitations:

- desktop only
- no direct cross-play with Bedrock
- modding and server setup can be more technical
- performance depends more on hardware, Java setup, and mod selection

### Minecraft Bedrock Edition

Capabilities:

- available on Windows, consoles, phones, and tablets
- supports cross-play across Bedrock devices
- easier for families and mixed-device multiplayer
- includes official services such as Marketplace content

Limitations:

- less open to community modding than Java
- more locked to the official Microsoft ecosystem
- still separate from Java Edition

## Practical recommendation for this repo

There are two distinct use cases here:

- If the goal is **programming blocks from Python**, this folder's Streamlit app plus **Minecraft Pi Edition** or **RaspberryJuice** is the right fit.
- If the goal is **playing a decluttered modern Minecraft on Linux**, prefer **Minecraft Java Edition** directly, without `mcpi`, Paper, or RaspberryJuice.

For a lightweight Linux setup, the cleanest modern path is usually:

- official Minecraft Java launcher, or
- Prism Launcher with a minimal Java instance, optionally using Fabric plus Sodium for performance

## Minecraft alternatives overview

- [Luanti (formerly Minetest)](https://github.com/luanti-org/luanti) - open source voxel game platform with easy modding and game creation
- [Luanti downloads](https://www.luanti.org/en/downloads/)
- [Terasology](https://terasology.org/)
- [Terasology downloads](https://terasology.org/downloads/)
- [Minecraft Pi: Reborn](https://gitea.thebrokenrail.com/minecraft-pi-reborn/minecraft-pi-reborn)
- [Getting Started with Minecraft Pi](https://projects.raspberrypi.org/en/projects/getting-started-with-minecraft-pi/0)
- [StanislavPetrovV/Minecraft](https://github.com/StanislavPetrovV/Minecraft) - Python and OpenGL voxel engine
- [fogleman/Craft](https://github.com/fogleman/Craft) - simple Minecraft-like clone in C and OpenGL
- [Freeminer](https://freeminer.org/)
