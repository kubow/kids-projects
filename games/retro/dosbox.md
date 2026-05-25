# DOSBox

- Emulátor **x86 PC s DOSem** — zvuk a grafika; shell vypadá jako starý textový DOS.
- Spouštíš **`.exe` / `.com` / `.bat`** ze složky na disku (shareware, vlastní zálohy legálně).
- Na **Pi OS / Linux**: `apt install dosbox`; hry typicky v `~/dos-games`.
- Při chybě DOSBox **ukončí běh bez varování** — zkontroluj `mount` a cesty.

## Instalace

```bash
sudo apt update && sudo apt install dosbox
mkdir -p ~/dos-games
dosbox
```

- Konfigurace po prvním běhu: `~/.dosbox/dosbox-0.74.conf` (úprava: `nano ~/.dosbox/dosbox-0.74.conf`)
- Spuštění s vlastním configem: `dosbox -conf ~/dos-games/moje-hra.conf`

## Základní příkazy (uvnitř DOSBox)

Na úvodní obrazovce DOSBox nabízí vestavěné nápovědy — zadej v promptu `Z:\>`:

| Příkaz | Co udělá |
| --- | --- |
| `intro` | Přehled intro příkazů |
| `intro mount` | Jak připojit složku jako disk (C:, D:, …) |
| `intro cdrom` | CD-ROM / image (`.iso`, `.cue`) |
| `intro special` | Speciální klávesy (fullscreen, mapper, …) |
| `help` | Seznam příkazů shellu |
| `mount` | Bez argumentů: seznam připojených disků |
| `mount c ~/dos-games` | Složka z Linuxu jako disk **C:** |
| `mount d ~/dos-games/cd -t cdrom` | Příklad CD-ROM disku |
| `c:` | Přepnout na disk C |
| `dir` | Výpis souborů (jako v DOS) |
| `GAME.EXE` | Spustit hru (název podle souboru) |
| `exit` | Ukončit DOSBox |

**Typický postup po startu:**

```
mount c ~/dos-games
c:
dir
GAME.EXE
```

## Klávesy a ovladač

- **Fullscreen:** `Alt+Enter`
- **Mapper (přemapování kláves):** `Ctrl+F1` nebo spuštění `dosbox -startmapper`
- **Rychlost za běhu:** `Ctrl+F12` zrychlit (víc cycles), `Ctrl+F11` zpomalit — v titulku okna uvidíš aktuální cycles
- Více: příkaz `intro special` uvnitř DOSBox

## Pomalý DOSBox (výkon)

Nejdřív rozliš, **co** je pomalé:

| Symptom | Typicky pomůže |
| --- | --- |
| Hra „jde“, ale jako na slabém PC (pomalá animace, hudba trhaná) | **Zvýšit cycles** (viz níže) |
| Celé okno trhá, Pi se hřeje, pozdní 90. / 3D hry | **Hardware limit** — zkus lehčí hru, Staging, nebo hru na silnějším PC |
| Jen zvuk zpomaluje obraz | Dočasně `sbtype=none` v configu (test) |

**1. Cycles (nejčastější u starých her)**

V `~/.dosbox/dosbox-0.74.conf` v sekci `[cpu]`:

```ini
[cpu]
core=auto
cycles=auto
# nebo pevně, pokud auto nestačí:
# cycles=max
# cycles=10000
```

- Za běhu: **`Ctrl+F12`** (rychleji) / **`Ctrl+F11`** (pomaleji), dokud hra nepůsobí přirozeně
- Příliš vysoké cycles = hra běží *příliš* rychle; příliš nízké = „slideshow“

**2. Jednodušší „virtuální PC“**

V `[sdl]` / `[render]` / `[dosbox]` (podle verze configu):

- Menší okno nebo nižší `output=surface` místo těžkého scaleru (zkus výchozí, pak uprav)
- V `[machine]`: pro staré hry stačí `machine=vga` nebo `svga_s3` — ne nastavovat zbytečně vysoký SVGA, pokud hra nepotřebuje

**3. Raspberry Pi**

- Starší Pi (0–3) zvládne hlavně **2D DOS a lehké 3D**; Duke3D, Doom v DOSBox často **pomalé nebo na hraně**
- **Pi 4/5:** často pomůže `cycles=max` + aktualizovaný systém; u problémů s grafikou zkus [DOSBox-Staging](./dosbox.md#forky-a-retropie)
- Zavři jiné náročné programy; hraj spíš v okně než v 4K fullscreen na TV

**4. Config jen pro jednu hru**

```bash
dosbox -conf ~/dos-games/moje-hra.conf
```

V souboru jen úpravy pro tu hru (cycles, `machine`, vypnutý zvuk pro test).

**5. Když to pořád nestačí**

- Zkus **DOSBox-Staging** (lepší výkon na některých platformách)
- Nebo stejnou hru přes **RetroPie** (`roms/pc/`) — někdy jiné výchozí nastavení
- Pozdní DOS / Win9x tituly raději na **běžném PC** nebo DOSBox-X na desktopu


- **DOSBox-Staging** — vylepšený fork; volitelný balíček v RetroPie ([staging](https://www.dosbox-staging.com/))
- **DOSBox-X** — širší emulace PC; těžší na Pi
- **RetroPie:** hry do `~/RetroPie/roms/pc/` — viz [README retro](./README.md#retropie)

## Odkazy

- [DOSBox](https://www.dosbox.com/) · [Wiki](https://www.dosbox.com/wiki) · [dosbox.conf](https://www.dosbox.com/wiki/dosbox.conf) · [Cycles](https://www.dosbox.com/wiki/Configuration:CPU)
- [Pi My Life Up — DOSBox na Pi](https://pimylifeup.com/raspberry-pi-dosbox/)
- [Retro — index](./README.md)
