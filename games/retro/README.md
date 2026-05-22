# Retro games

This folder collects research on **classic games** on Linux and Raspberry Pi, focused on **RetroPie** (console/handheld emulators) and **DOSBox** (MS-DOS).

Retro gaming here means **emulation** — you provide legally obtained ROMs, disk images, or game files; this repo does not host copyrighted games.

## Retro platforms overview

| Platform | Official support | Best for | Main capabilities | Main limitations |
| --- | --- | --- | --- | --- |
| **RetroPie (full image)** | Yes (Pi-focused) | Dedicated retro console on Pi | EmulationStation front-end, many systems, controllers, kiosk-style TV setup | Replaces or dual-boots SD card; learning curve for ROM layout and scrapers |
| **RetroPie (on top of Pi OS)** | Yes | Keep Pi OS and add emulators | `retropie-setup.sh` installs cores into existing OS | More manual; version pairing with Pi OS matters |
| **DOSBox (apt on Pi OS / Linux)** | Yes | Quick DOS titles on desktop Pi or PC | `sudo apt install dosbox`, simple `mount` workflow | Performance limited on old Pi; one DOS PC at a time |
| **DOSBox-Staging / DOSBox-X** | Community | Better compatibility or Win 3.x / 9x experiments | Staging: improved DOSBox fork; X: broader PC emulation | Pi support varies; Staging on Pi 5 may need correct kernel/Mesa (see issues below) |
| **DOSBox via RetroPie** | Yes | DOS games in same UI as SNES, etc. | Install `dosbox` or `dosbox-staging` from RetroPie-Setup | Same ROM/legal rules; config split between RetroPie and DOSBox |

## RetroPie

RetroPie bundles **EmulationStation** (launcher) and **RetroArch** / standalone emulators for many consoles and computers.

### Full RetroPie image (usual Pi path)

1. Download from [retropie.org.uk](https://retropie.org.uk/).
2. Flash with [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to an SD card (use a **spare** card if Pi OS should stay untouched).
3. Boot Pi, connect gamepad, follow first-run prompts (network, controls).
4. Copy ROMs into the correct folders under `~/RetroPie/roms/` (system-specific paths — see [RetroPie docs](https://retropie.org.uk/docs/)).
5. Optional: scrape box art with built-in scraper (needs network).

**Raspberry Pi 5:** community setup notes — [raspberrypi5-retropie-setup](https://github.com/danielfreer/raspberrypi5-retropie-setup).

### RetroPie on existing Raspberry Pi OS

For Pi OS already installed, use [Manual installation](https://retropie.org.uk/docs/Manual-Installation/):

```bash
cd
git clone --depth=1 https://github.com/RetroPie/RetroPie-Setup.git
cd RetroPie-Setup
sudo ./retropie_setup.sh
```

Use the menu to install **core** packages first, then optional emulators (including DOSBox variants).

Capabilities:

- one front-end for dozens of systems (NES, SNES, Mega Drive, PlayStation, etc.)
- strong **controller-first** living-room use
- active wiki and forums

Limitations:

- ROM collection and BIOS files are your responsibility (licensing)
- Pi 3/4/5 differ in what runs full-speed (e.g. some PlayStation / N64 titles need Pi 4/5)
- updates can break individual cores until RetroPie catches up

## DOSBox

**DOSBox** emulates a DOS PC for running `.exe` / `.com` games and shareware from the 1980s–1990s.

### Standalone on Raspberry Pi OS or Linux (apt)

```bash
sudo apt update
sudo apt install dosbox
mkdir -p ~/dos-games
dosbox
```

First run creates config under `~/.dosbox/` (e.g. `dosbox-0.74.conf`). Edit with:

```bash
nano ~/.dosbox/dosbox-0.74.conf
```

Typical session inside DOSBox:

```text
mount c ~/dos-games
c:
dir
GAME.EXE
```

Controller mapping: launch DOSBox, press **Ctrl+F1**, or `dosbox -startmapper`.

Capabilities:

- lightweight; runs on older Pi models for many DOS titles
- easy to test one game without full RetroPie
- config per game possible (`dosbox -conf mygame.conf`)

Limitations:

- not all DOS games fit Pi CPU (late 90s 3D titles especially)
- manual mounting unless you script or use a front-end
- sound/CPU cycles need tuning in config for some titles

### DOSBox-Staging and DOSBox-X (optional)

| Fork | Notes |
| --- | --- |
| [DOSBox-Staging](https://www.dosbox-staging.com/) | Modern DOSBox improvements; RetroPie lists under **optional** packages |
| [DOSBox-X](https://dosbox-x.com/) | Broader PC scope (Windows 3.x / 9x); heavier; [Pi magazine walkthrough](https://magazine.raspberrypi.com/articles/build-a-dos-emulation-system) |

On **Raspberry Pi 5** with recent Pi OS, Staging may crash depending on Mesa/kernel — see [dosbox-staging #4240](https://github.com/dosbox-staging/dosbox-staging/issues/4240). Some setups need `kernel=kernel8.img` in `/boot/firmware/config.txt`; if problems persist, use stock `dosbox` from apt or RetroPie’s packaged core.

### DOSBox inside RetroPie

1. Run **RetroPie-Setup** → manage packages.
2. Install **dosbox** (core) or **dosbox-staging** (optional).
3. Place DOS games/zips in `~/RetroPie/roms/pc/` (see current [RetroPie PC / DOS docs](https://retropie.org.uk/docs/PC/)).
4. Launch from EmulationStation like other systems.

Good when you want **one UI** for DOS and console ROMs.

## Linux desktop (not only Pi)

| Tool | Use |
| --- | --- |
| **DOSBox** / **DOSBox-Staging** | `apt install dosbox` or distro package; same `~/.dosbox` config model |
| **RetroArch** | Single emulator frontend on Linux without full RetroPie image |
| **RetroPie** | Primarily Pi-oriented; on PC, Lutris, Steam retro packs, or distro emulators are common alternatives |

RetroPie itself targets the Pi ecosystem; on a Linux PC, DOSBox + RetroArch (or distro game bundles) is usually simpler than cloning RetroPie-Setup.

## ROMs, BIOS, and legal notes

- Only use **ROMs and BIOS files you are allowed to use** (your own backups, public-domain, or freeware).
- RetroPie does not ship copyrighted games.
- Keep a clear folder layout (`roms/<system>/`) and backups of `retroarch` / `~/.dosbox` configs.

## Practical recommendation for this repo

| Goal | Recommendation |
| --- | --- |
| **Living-room retro console on Pi** | Full **RetroPie** image on a dedicated SD card |
| **Keep Pi OS, add emulators** | **RetroPie-Setup** on existing Pi OS |
| **A few DOS games quickly** | `apt install dosbox` + `~/dos-games` |
| **DOS + consoles in one launcher** | RetroPie with **dosbox** core + ROM folders |
| **Hardest DOS titles / Win 9x** | Try **DOSBox-X** or PC hardware; Pi is not ideal |
| **Modern sandbox / UGC (not retro)** | [../minecraft/README.md](../minecraft/README.md), [../luanti/README.md](../luanti/README.md), etc. |


Other retro links (no dedicated folder):

- [Games on Raspberry Pi OS without emulators](https://raspberrytips.com/raspberry-pi-os-best-games/) — native/Linux ports, not emulation-focused

## Key links

### RetroPie

- [RetroPie](https://retropie.org.uk/)
- [RetroPie documentation](https://retropie.org.uk/docs/)
- [Manual installation](https://retropie.org.uk/docs/Manual-Installation/)
- [RetroPie-Setup (GitHub)](https://github.com/RetroPie/RetroPie-Setup)
- [Raspberry Pi 5 RetroPie setup (community)](https://github.com/danielfreer/raspberrypi5-retropie-setup)

### DOSBox

- [DOSBox](https://www.dosbox.com/)
- [dosbox.conf (wiki)](https://www.dosbox.com/wiki/dosbox.conf)
- [DOSBox-Staging](https://www.dosbox-staging.com/)
- [DOSBox-X](https://dosbox-x.com/)
- [DOSBox on Raspberry Pi (Pi My Life Up)](https://pimylifeup.com/raspberry-pi-dosbox/)
- [Build a DOS emulation system (Raspberry Pi magazine)](https://magazine.raspberrypi.com/articles/build-a-dos-emulation-system)
