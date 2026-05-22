# Roblox

This folder collects research on running and developing with **Roblox** on Linux and Raspberry Pi, plus alternatives when official support is missing.

Roblox has **no official Linux desktop client**. On PC, Roblox targets Windows and macOS. Mobile uses Android and iOS. Community projects fill the gap on Linux; Raspberry Pi needs a different approach entirely because of CPU architecture.

## Roblox platforms overview


| Platform                             | Official support | Best for                                        | Main capabilities                                                                                                            | Main limitations                                                                                  |
| ------------------------------------ | ---------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Windows / macOS**                  | Yes              | Playing and creating with the official launcher | Full player, Roblox Studio, best compatibility, official updates                                                             | Not native on Linux without workarounds                                                           |
| **Android / iOS**                    | Yes              | Phones and tablets                              | Official mobile client, touch controls, large catalog of experiences                                                         | No keyboard/mouse-first PC controls; some experiences are mobile-only                             |
| **Linux (Sober)**                    | No (unofficial)  | Playing Roblox on a normal PC running Linux     | Flatpak install, runs the Android x86_64 build in a specialized runtime, bypasses Hyperion anti-cheat issues that broke Wine | Experimental, closed source, x86_64 only, not supported by Roblox, may break after Roblox updates |
| **Linux (Vinegar)**                  | No (unofficial)  | **Roblox Studio only**                          | Flatpak, Wine-based Studio launcher maintained by VinegarHQ                                                                  | Player blocked by Hyperion; Studio UI/plugins can be buggy                                        |
| **Linux (Wine / Grapejuice)**        | No               | —                                               | Was the old community method                                                                                                 | **Blocked since ~2023** by Roblox Hyperion anti-cheat; do not use for the player                  |
| **Raspberry Pi (Raspberry Pi OS)**   | No               | General Pi projects, coding, other games        | Normal Pi desktop and tooling                                                                                                | **Sober does not run** (needs x86_64, not ARM64); no practical native Roblox on Pi OS today       |
| **Raspberry Pi (LineageOS Android)** | Via Android APK  | Dedicated “Roblox box” next to a TV             | Install Roblox from Google Play on Pi 4/5 with an Android image                                                              | Replaces Pi OS on that SD card; setup is involved; performance varies by experience               |


## Linux: playing Roblox (recommended path)

### Sober (player) — what works in 2026

**Sober** is the practical way to play Roblox on Linux today. It is maintained by the [VinegarHQ](https://vinegarhq.org/) community and distributed on [Flathub](https://flathub.org/apps/org.vinegarhq.Sober).

How it works (simplified):

- Roblox never shipped a Linux player.
- Older guides used **Wine** and wrappers like **Grapejuice**.
- Roblox added **Hyperion** (Byfron) anti-cheat, which detects and blocks Wine for the **player**.
- Sober runs the **official Android x86_64 APK** inside a specialized runtime, not Wine, so Hyperion does not apply the same way.

Important caveats:

- **Unofficial research software** — Roblox may block it at any time.
- **Closed source** (VinegarHQ cites reducing abuse that could get the project blocked).
- **Experimental** — expect bugs, version mismatches, or install hiccups after Roblox updates.
- **Flatpak only** — reproducible runtime; no native `.deb` / `.rpm` from the Sober team.

### System requirements (Sober)

From [Vinegar Sober installation docs](https://vinegarhq.org/Sober/Installation.html):


|                                     | Requirement                                                                      |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| OS                                  | Linux kernel **≥ 5.11**                                                          |
| CPU                                 | **x86_64 / AMD64** with **SSE4.1** (SSE4.2 recommended)                          |
| Graphics                            | OpenGL ES 3.0 capable (Vulkan 1.1 recommended)                                   |
| ARM (Pi, Apple Silicon Linux, etc.) | **Not supported** at time of writing (ARM is experimental, not production-ready) |


Check CPU features:

```bash
grep -o sse4_1 /proc/cpuinfo | head -1
grep -o sse4_2 /proc/cpuinfo | head -1
```

Check architecture (Pi will show `aarch64`, which Sober cannot use yet):

```bash
uname -m
# PC: x86_64
# Raspberry Pi 64-bit OS: aarch64 (arm64)
```

### Install Sober

1. Install [Flatpak](https://flatpak.org/setup/) for your distribution.
2. Install Sober:

```bash
flatpak install flathub org.vinegarhq.Sober
```

1. Launch Sober from the app menu.
2. On first run, allow **automatic** Roblox APK installation unless you know you need manual APK install.
3. Sign in (Quick Sign-in is often more reliable than embedded web login).
4. Open a game from the browser or in-app — Sober should attach to the experience.

Uninstall:

```bash
flatpak uninstall org.vinegarhq.Sober
# Full reset including data:
flatpak uninstall --delete-data org.vinegarhq.Sober
```

Configuration (death sound, server region hints, graphics tweaks): [Sober configuration](https://vinegarhq.org/Sober/Configuration/index.html)

Troubleshooting: [Sober troubleshooting](https://vinegarhq.org/Sober/Troubleshooting.html)

### Linux alternatives to Sober (player)


| Method                           | Status                       | Notes                                                                                  |
| -------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------- |
| **Waydroid** (Android container) | Can work                     | More setup (kernel modules, Wayland-focused); mouse/capture quirks; heavier than Sober |
| **Wine / Grapejuice / Lutris**   | **Does not work** for player | Blocked by Hyperion                                                                    |
| **Virtual machine with Windows** | Works but heavy              | Needs Windows license, GPU passthrough for good FPS, lots of RAM/disk                  |
| **Cloud gaming / remote PC**     | Works                        | Play on another machine via Moonlight, Steam Link, etc. — Pi can be a thin client      |


## Linux: Roblox Studio (creating games)

Studio is separate from the player anti-cheat story. Use **Vinegar** for Studio on Linux:

```bash
flatpak install flathub org.vinegarhq.Vinegar
flatpak run org.vinegarhq.Vinegar studio
```

Docs: [Vinegar installation](https://vinegarhq.org/Vinegar/Installation.html)

Limitations:

- Some Studio plugins and UI panels are flaky under Wine.
- For serious Studio work, Windows or macOS is still the most predictable option.

Common Studio companion tools (any OS):

- [Rojo](https://rojo.space/) — sync filesystem projects into Studio
- [Wally](https://wally.run/) — Luau package manager
- Community template for AI-assisted workflows: [dnouri/roblox-pi-template](https://github.com/dnouri/roblox-pi-template) (mentions Vinegar on Linux)

## Raspberry Pi: realistic options

### What does not work on Pi OS

- **Sober on Flathub** lists architecture **x86_64 only** — it will not install on ARM Pi OS.
- **Wine/Grapejuice** — blocked for the player even on x86 PCs; irrelevant on ARM.
- Running Roblox inside normal **Raspberry Pi OS** (Debian-based) like a desktop PC is **not supported** today.

Forum confirmation: [Flatpak install sober not working (Pi 5)](https://forums.raspberrypi.com/viewtopic.php?t=394890)

### What can work: Android on the Pi (Pi 4 / Pi 5)

The workable approach is to treat the Pi as an **Android device**, not as Linux desktop:

1. Flash **LineageOS for Raspberry Pi** (e.g. [KonstaKANG builds](https://konstakang.com/devices/rpi5/)) to a **separate SD card** — do not overwrite a Pi OS card you still need unless you have backups.
2. Boot Pi 4 or Pi 5 (Pi 5 strongly recommended for performance).
3. Install **Google Play** via a GApps package (e.g. [NikGapps](https://nikgapps.com/downloads)) following the image maintainer’s instructions.
4. Sign into Google Play, install **Roblox** from the store, log in, pick experiences.

References:

- [How to install and play Roblox on Raspberry Pi (pihow)](https://pihow.co.uk/how-to-install-and-play-roblox-on-raspberry-pi/)
- [Roblox on Pi — Raspberry Pi Forums](https://forums.raspberrypi.com/viewtopic.php?t=385216)
- Video walkthrough (community): [Roblox on Raspberry Pi 5, Android 14](https://www.youtube.com/watch?v=QVEiWbubHUw)

Trade-offs:

- **Dual-boot mindset** — use a spare SD card for experiments; keep Pi OS on another card if you want both worlds.
- **Performance varies** — simple obby games may be fine; demanding experiences may stutter or fail.
- **Not a dev machine** — this path is for **playing**, not for comfortable Roblox Studio on Pi.
- **Account / parental controls** — same Roblox account rules as on any Android device.

### Pi as a thin client (lighter alternative)

If the goal is “Roblox in the living room on a Pi” without Android reflash:

- Run Roblox on a **PC, console, phone, or tablet** and stream or mirror to the TV.
- Or use **remote desktop** to a Windows/Mac machine from the Pi (latency and input lag apply).

## Practical recommendation for this repo


| Goal                                                        | Recommendation                                                                               |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Play Roblox on a Linux laptop/desktop (x86_64)**          | **Sober** via Flatpak; keep Flatpak and Sober updated                                        |
| **Make Roblox games on Linux**                              | **Vinegar** for Studio + Rojo/Wally; expect occasional Studio quirks                         |
| **Play on Raspberry Pi**                                    | **LineageOS + Play Store Roblox** on Pi 4/5, spare SD card; or use another device and stream |
| **Teach block coding / game making without Roblox lock-in** | [Luanti](../luanti/README.md) or [Terasology](../terasology/README.md); see [../README.md](../README.md) |
| **Follow old “install Grapejuice on Linux” blogs**          | **Outdated** — use Sober instead                                                             |


## Related sandbox / UGC options

Roblox is one of several UGC/sandbox paths documented in this repo. For side-by-side comparison and open-source options, see [../README.md](../README.md).

| In this repo | Why look at it |
| --- | --- |
| [Minecraft](../minecraft/README.md) | Paid voxel sandbox; Pi Python API in this repo |
| [Luanti](../luanti/README.md) | Open Lua mods; Linux and Pi without Roblox account |
| [Terasology](../terasology/README.md) | Open Java modules; desktop Linux |

Other commercial UGC/sandbox links (not separate folders): [Core Games](https://www.coregames.com/), [Creativerse on Steam](https://store.steampowered.com/app/280790/Creativerse/), [Scratch](https://scratch.mit.edu/), [Godot](https://godotengine.org/).

## Key links

### Official Roblox

- [Roblox](https://www.roblox.com/)
- [Create (Studio download)](https://create.roblox.com/)
- [Roblox system requirements](https://en.help.roblox.com/hc/en-us/articles/203312800-Computer-Hardware-Operating-System-Requirements)
- [Roblox mobile requirements](https://en.help.roblox.com/hc/en-us/articles/203625474)

### Linux community (unofficial)

- [Sober website](https://sober.vinegarhq.org/)
- [Sober on Flathub](https://flathub.org/apps/org.vinegarhq.Sober)
- [VinegarHQ documentation](https://vinegarhq.org/)
- [Sober FAQ](https://vinegarhq.org/Sober/FAQ/index.html)
- [Sober GitHub issues](https://github.com/vinegarhq/sober/issues)
- [Vinegar (Studio) on Flathub](https://flathub.org/apps/org.vinegarhq.Vinegar)

### Raspberry Pi

- [KonstaKANG — Raspberry Pi 5 LineageOS](https://konstakang.com/devices/rpi5/)
- [Raspberry Pi Forums — Roblox on Pi](https://forums.raspberrypi.com/viewtopic.php?t=385216)

## Safety and expectations

- Unofficial clients (**Sober**, **Vinegar**) are **not endorsed by Roblox**. Read each project’s notices before use.
- Roblox is an **online social platform** — use parental controls, privacy settings, and the same caution as on any network-heavy game service.
- On Pi, prefer a **dedicated SD card** for Android experiments so a failed flash does not destroy a school or coding Pi OS setup.
- When Sober’s automatic APK download fails (Cloudflare, region blocks, version mismatch), check [current GitHub issues](https://github.com/vinegarhq/sober/issues) — version strings in the UI sometimes lag the APK you actually need.

