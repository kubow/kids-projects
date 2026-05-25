# Terasology

Open-source 3D voxel hra od [MovingBlocks](https://github.com/MovingBlocks): gameplay z **modulů** (Java, Gradle), instalace přes **Terasology Launcher**. Web: [terasology.org](https://terasology.org/).

## Platformy (vyber jeden stack)

| Stack | Platformy | Nejlepší pro | Limity |
| --- | --- | --- | --- |
| **Launcher** | Linux / Windows / macOS **x86_64** | Hraní + modulové packy | OpenGL **3.3** GPU; ~2–4 GB RAM; první běh potřebuje internet |
| **Engine release** | Desktop + **JDK 17+** | Vývoj / ruční instalace | Více práce než launcher |
| **Pi klient** | Raspberry Pi OS arm64 | — | Klient **nepodporován** ([ARM #3412](https://github.com/MovingBlocks/Terasology/issues/3412)) |
| **Pi headless server** | Pi (pokročilé) | CLI server experimenty | Ne dětská cesta k hraní |
| **Multiplayer** | LAN / hostované | Světy podle modulů | Shodný set modulů + verze engine na hostu a klientech |

**Požadavky ([downloads](https://terasology.org/downloads/)):** 64-bit OS, dual-core CPU, 2–4 GB RAM, OpenGL 3.3, ~1 GB disk.

## Linux: instalace a hraní

**Launcher (doporučeno)**

- [terasology.org/downloads](https://terasology.org/downloads/) → **Linux (64-bit)** → rozbal → `./bin/TerasologyLauncher`
- Stáhni engine + vyber **moduly** v UI; offline hra po cache
- Projekt: [TerasologyLauncher](https://github.com/MovingBlocks/TerasologyLauncher)

**Engine přímo (vývojáři)**

- [Engine README](https://github.com/MovingBlocks/Terasology/blob/develop/README.md) — **Java 17+**
- Nástroje: JDK, Git, Gradle (`gradlew` v repozitářích launcher/engine)

## Moduly

- **Hraní:** modulové packy (generování světa, bloky, tvorové) přes launcher; offline po stažení; menší ekosystém než [Luanti ContentDB](../luanti/README.md) nebo komerční UGC
- **Vývoj:** Java moduly + Gradle — vhodné pro učení engine/architektury; náročnější než Luanti **Lua** pro malé začátečníky
- **Multiplayer:** chování podle zapnutých modulů; verze zdokumentovat pro LAN/kamarády; veřejný port jen pokud chápeš rizika

## Raspberry Pi

- **Klient na Pi OS:** nepraktický — LWJGL/nativy historicky x86, ne ARM ([#3412](https://github.com/MovingBlocks/Terasology/issues/3412)); pro Pi sandbox/hraní [../luanti/README.md](../luanti/README.md) nebo [../minecraft/README.md](../minecraft/README.md) (Pi API)
- **Headless server:** může startovat jen pro experimenty (CLI, shoda verze/modulů)
- Skutečný desktop klient na Pi by potřeboval upstream ARM64 native buildy (LWJGL + fyzika)

## Co použít v tomto repu

| Cíl | Použít |
| --- | --- |
| Open voxel na **Pi** | [../luanti/README.md](../luanti/README.md) |
| Open voxel na **Linuxu** (jednoduše) | Luanti jako první |
| **Java** moduly / engine na PC | Terasology Launcher (x86_64) |
| **Python** bloky na Pi | [../minecraft/README.md](../minecraft/README.md) |
| Velký online UGC katalog | [../roblox/README.md](../roblox/README.md) nebo Minecraft |

## Související v tomto repu

- [../README.md](../README.md) — index
- [../luanti/README.md](../luanti/README.md) · [../minecraft/README.md](../minecraft/README.md) · [../roblox/README.md](../roblox/README.md) · [../retro/README.md](../retro/README.md)

## Odkazy

- [Terasology](https://terasology.org/) · [Downloads](https://terasology.org/downloads/) · [Engine](https://github.com/MovingBlocks/Terasology) · [Launcher](https://github.com/MovingBlocks/TerasologyLauncher)
- [Veloren](https://veloren.net/) · [Freeminer](https://freeminer.org/)
