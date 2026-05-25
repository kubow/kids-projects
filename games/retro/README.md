# Retro hry

**Klasické hry** na Linuxu a Raspberry Pi přes **emulaci** — zaměření **RetroPie** (konzole/handheldy) a **[DOSBox](./dosbox.md)** (MS-DOS). ROMy, diskové image nebo soubory her dodáváš legálně; repo nehostuje hry.

## Stacky (vyber jeden)

| Stack | Nejlepší pro | Limity |
| --- | --- | --- |
| **RetroPie image** | Dedikovaná Pi „retro konzole“ u TV | Vlastní SD; ROM složky + scrapery se naučit |
| **RetroPie na Pi OS** | Pi OS + emulátory | Ruční; sladit verze Pi OS / RetroPie |
| **[DOSBox](./dosbox.md) (apt)** | Pár DOS her na desktop Pi/PC | Slabé na starém Pi pro pozdní 90. 3D; ruční `mount` |
| **DOSBox-Staging / X** | Lepší DOS nebo Win 3.x/9x | Pi 5 + Mesa ([staging #4240](https://github.com/dosbox-staging/dosbox-staging/issues/4240)) |
| **DOS přes RetroPie** | DOS + SNES/atd. v jednom UI | Stejná pravidla; layout `roms/pc/` |

## RetroPie

EmulationStation front-end + RetroArch / emulátory po systémech.

**Plný image (běžné na Pi)**

- Stáhni [retropie.org.uk](https://retropie.org.uk/) → flash [Pi Imager](https://www.raspberrypi.com/software/) (náhradní SD pokud zůstává Pi OS)
- Boot, spáruj gamepad, síť; ROMy v `~/RetroPie/roms/<system>/` ([docs](https://retropie.org.uk/docs/))
- Volitelný scraper obalů (potřeba sítě)
- Pi 5: [raspberrypi5-retropie-setup](https://github.com/danielfreer/raspberrypi5-retropie-setup)

**Na existujícím Pi OS**

```bash
git clone --depth=1 https://github.com/RetroPie/RetroPie-Setup.git
cd RetroPie-Setup && sudo ./retropie_setup.sh
```

- Nejdřív **core** balíčky, pak volitelné (vč. variant DOSBox)
- Ovladač-first obývák; mnoho systémů (NES → PlayStation atd.)
- ROMy/BIOS dodáváš ty; Pi 4/5 pro těžší systémy (některé PSX/N64); core update může dočasně rozbít
- DOS hry: `~/RetroPie/roms/pc/` — detail [DOSBox](./dosbox.md)

## DOSBox

→ **[dosbox.md](./dosbox.md)** — instalace, `intro mount` / `intro special`, `mount c`, spuštění `.exe`, klávesy.

## Linux desktop (ne jen Pi)

- **DOSBox** / Staging: distro balíčky, stejný layout `~/.dosbox` — viz [dosbox.md](./dosbox.md)
- **RetroArch**: frontend bez plného RetroPie image
- **RetroPie-Setup**: orientované na Pi; na PC raději Lutris, Steam retro balíčky nebo distro emulátory

## Právo a soubory

- ROMy/BIOS jen pokud je **smíš** používat (vlastní zálohy, freeware, public domain)
- RetroPie neobsahuje autorská díla
- Udržuj layout `roms/<system>/`; zálohuj `~/.dosbox` / RetroArch configy

## Co použít v tomto repu

| Cíl | Použít |
| --- | --- |
| Pi obývák konzole | Plný RetroPie image, dedikovaná SD |
| Pi OS + emulátory | RetroPie-Setup |
| Rychlý DOS na Pi/PC | [DOSBox](./dosbox.md) — `apt install dosbox` + `~/dos-games` |
| DOS + konzole jedno UI | RetroPie + `roms/pc/` |
| Těžký DOS / Windows 9x | DOSBox-X nebo PC hardware |
| Sandbox / UGC (ne retro) | [../minecraft/README.md](../minecraft/README.md) · [../luanti/README.md](../luanti/README.md) |

## Související v tomto repu

- [../README.md](../README.md) — index (vč. dalších srovnatelných her)
- [../minecraft/README.md](../minecraft/README.md) · [../roblox/README.md](../roblox/README.md) · [../luanti/README.md](../luanti/README.md)

## Odkazy

- [RetroPie](https://retropie.org.uk/) · [docs](https://retropie.org.uk/docs/) · [manual install](https://retropie.org.uk/docs/Manual-Installation/) · [RetroPie-Setup](https://github.com/RetroPie/RetroPie-Setup)
- [DOSBox](./dosbox.md) — základní příkazy a návod v repu
- [Nativní hry na Pi (bez emulátoru)](https://raspberrytips.com/raspberry-pi-os-best-games/)
