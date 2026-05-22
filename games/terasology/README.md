# Terasology

This folder collects research on **Terasology** on Linux and Raspberry Pi: launcher install, modules, limits on ARM/Pi, and how it compares to other open voxel options in this repo.

**Terasology** is an open-source 3D voxel game from [MovingBlocks](https://github.com/MovingBlocks). Gameplay is built from **modules** (Java, Gradle), installed and updated through the **Terasology Launcher**.

Site: [terasology.org](https://terasology.org/)

## Terasology platforms overview

| Platform | Official support | Best for | Main capabilities | Main limitations |
| --- | --- | --- | --- | --- |
| **Linux x86_64 (launcher)** | Yes | Desktop play and module experiments | Download launcher, pick module packs, offline play after fetch | 64-bit only; needs OpenGL 3.3 GPU |
| **Windows / macOS (launcher)** | Yes | Same as Linux desktop | Official launcher archives | Not covered in depth here |
| **Linux (direct engine release)** | Yes | Developers with JDK 17+ already set up | Skip launcher workflow if you manage Java yourself | More manual than launcher |
| **Raspberry Pi OS (arm64) client** | No | — | — | LWJGL / native libs not built for ARM client ([issue #3412](https://github.com/MovingBlocks/Terasology/issues/3412)) |
| **Raspberry Pi (headless server)** | Partial | Advanced/server-only experiments | Some reports of server starting on Pi | No polished Pi gaming path; CLI-only |
| **Dedicated / multiplayer** | Yes | Module-dependent LAN or hosted worlds | Multiplayer via selected modules | Match module set and versions between host and clients |

Minimum requirements ([downloads](https://terasology.org/downloads/)): 64-bit OS, dual-core CPU, 2–4 GB RAM, GPU with **OpenGL 3.3**, ~1 GB disk; internet for first launcher download.

## Linux: install and play

### Terasology Launcher (recommended)

1. Open [terasology.org/downloads](https://terasology.org/downloads/).
2. Select **Linux (64-bit)** and download the launcher archive.
3. Extract the archive.
4. Run:

```bash
./bin/TerasologyLauncher
```

5. In the launcher, download the engine and choose **modules** / gameplay packs.
6. Play offline after assets are cached.

Launcher project: [MovingBlocks/TerasologyLauncher](https://github.com/MovingBlocks/TerasologyLauncher)

### Direct engine release (alternative)

For development or manual installs, see the engine README — **Java 17** required: [MovingBlocks/Terasology](https://github.com/MovingBlocks/Terasology/blob/develop/README.md).

Development tooling: JDK, Git, Gradle wrapper (`gradlew` tasks in launcher/engine repos).

## Raspberry Pi

### What does not work on Pi OS

- **Full game client** on Raspberry Pi OS arm64 is **not supported** in practice — native libraries have historically targeted x86, not ARM ([Crash on ARM platform #3412](https://github.com/MovingBlocks/Terasology/issues/3412)).
- Do not expect a smooth “install launcher and play” path on Pi like Luanti or Minecraft Pi API.

### What might work (limited)

- **Headless server** — may start on a Pi for CLI-only hosting; module and version matching still apply; not a kid-friendly default.
- **Practical Pi sandbox** — use [../luanti/README.md](../luanti/README.md) or [../minecraft/README.md](../minecraft/README.md) instead.

Upstream would need ARM64 builds of LWJGL and physics natives for a real Pi desktop client.

## Modules and gameplay packs

### Module packs (via launcher)

Capabilities:

- gameplay composed from **modules** (world generation, blocks, creatures, etc.)
- install and update through launcher UI
- offline play after download

Limitations:

- smaller ecosystem than Luanti ContentDB or commercial UGC platforms
- module combinations can be confusing for beginners

### Java module development

Capabilities:

- extend the engine with **Java** modules and Gradle builds
- good for learners curious about **game engine architecture**

Limitations:

- heavier than Luanti **Lua** mods — JDK, Git, Gradle required
- not a quick “first coding project” path for young kids

## Multiplayer

- Depends on **which modules** are enabled on the host world.
- Document module list and engine version when hosting for friends or family.
- Prefer LAN unless you understand port exposure and server administration.

## Practical recommendation for this repo

| Goal | Recommendation |
| --- | --- |
| **Open voxel on Raspberry Pi** | [../luanti/README.md](../luanti/README.md) |
| **Open voxel on Linux desktop (simple)** | [../luanti/README.md](../luanti/README.md) first |
| **Java modules / engine curiosity on PC** | Terasology Launcher on **x86_64 Linux** |
| **Python block coding on Pi** | [../minecraft/README.md](../minecraft/README.md) |
| **Large online UGC catalog** | [../roblox/README.md](../roblox/README.md) or Minecraft |

## Related sandbox / UGC options

Platforms in this repo (see [../README.md](../README.md)):

- [Luanti](../luanti/README.md) — open Lua mods; strong Linux and Pi support
- [Minecraft](../minecraft/README.md) — commercial sandbox; Pi Python API
- [Roblox](../roblox/README.md) — commercial UGC platform

Terasology-adjacent links:

- [Veloren](https://veloren.net/) — open multiplayer voxel RPG
- [Freeminer](https://freeminer.org/) — Minetest / Luanti family fork

## Key links

### Official / upstream

- [Terasology](https://terasology.org/)
- [Downloads / launcher](https://terasology.org/downloads/)
- [GitHub — MovingBlocks/Terasology](https://github.com/MovingBlocks/Terasology)
- [Terasology Launcher](https://github.com/MovingBlocks/TerasologyLauncher)

### Raspberry Pi / ARM

- [ARM / Raspberry Pi discussion (#3412)](https://github.com/MovingBlocks/Terasology/issues/3412)
