# Luanti

Open-source voxel **platforma pro tvorbu her** (dříve Minetest): komunitní **hry** a **mody** přes [ContentDB](https://content.luanti.org/), modding v **Lua**, silné na **Linuxu** a **Raspberry Pi**. Bez komerčního účtu. Web: [luanti.org](https://www.luanti.org/).

## Miney (Python API)

Externí ovládání jako [Minecraft Pi + `mcpi`](../minecraft/README.md) — ne vestavěné Lua-only API ([api.luanti.org](https://api.luanti.org/)).

- **Co:** [Miney](https://miney.readthedocs.io/) — Python klient + [mod z ContentDB](https://content.luanti.org/packages/Miney/miney/) na serveru světa
- **Vyžaduje:** Luanti **5.7+**, Python **3.6+**, zapnutý mod **`miney`**, svět **hostovaný** (i solo hra na vlastním PC)
- **Lokální svět:** otevři svět na tomto stroji → zapni mod → **Host game** → app se připojí na `127.0.0.1`, port **30000** (ne samostatný vzdálený server)
- **Limity:** API **beta**; názvy uzlů jsou řetězce (`default:stone`), ne Pi numerická ID; stavby v repu předpokládají uzly `default:*`
- **Nastavení:**
  - ContentDB → nainstaluj **Miney** → zapni ve světě
  - `pip install miney` (nebo `pip install -r requirements.txt` z kořene repa)
  - Hostuj svět; ověř: `python examples/check_setup.py` z [miney-py/miney](https://github.com/miney-py/miney)
- **Streamlit app:** [app.py](./app.py) — bloky, předpřipravené stavby, teleport, chat

```bash
source venv/bin/activate
pip install -r requirements.txt
streamlit run games/luanti/app.py
```

Výchozí přihlášení v sidebaru: hráč `miney`, heslo `ChangeThePassword!` (srovnej se serverem).

- **vs Minecraft Pi v tomto repu:**

| | Minecraft Pi | Luanti + Miney |
| --- | --- | --- |
| Python | `mcpi`, `minecraftstuff` | `miney` |
| Most | Pi Edition / RaspberryJuice | mod `miney` |
| UI | [../minecraft/app.py](../minecraft/app.py) | [./app.py](./app.py) |

- **Jiná Python cesta:** [Raspberry Jam Mod](https://github.com/arpruss/raspberryjammod-minetest) (legacy **mcpi** shim; neudržovaný)
- **Odkazy:** [docs](https://miney.readthedocs.io/) · [GitHub](https://github.com/miney-py/miney) · [ContentDB mod](https://content.luanti.org/packages/Miney/miney/)

## Instalace a platformy

| Platforma | Nejlepší pro | Omezení |
| --- | --- | --- |
| **Linux apt** | Rychlý desktop / Pi OS | Balíček může zaostávat (`luanti` nebo `minetest`) |
| **Linux Flatpak** | Sandboxed instalace | Zkontroluj arch na Flathub |
| **Linux kompilace** | Nejnovější engine / jen server | [Compile guide](https://github.com/luanti-org/luanti/blob/master/doc/compiling/linux.md) |
| **Raspberry Pi OS** | Klient + LAN server | Nižší FPS; lehké game packy |
| **Dedikovaný server** | Headless / Docker | UDP **30000**; shodná verze klienta |
| **Android** | Mobilní hraní | Pro Miney workflow zde nepoužíváno |

**Linux apt**

```bash
sudo apt update && sudo apt install luanti
```

**Linux kompilace (shrnutí)**

```bash
sudo apt install g++ make libc6-dev cmake libpng-dev libjpeg-dev libgl1-mesa-dev \
  libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-gnutls-dev \
  libfreetype6-dev zlib1g-dev libgmp-dev libjsoncpp-dev libzstd-dev \
  libluajit-5.1-dev gettext libsdl2-dev git
git clone --depth 1 https://github.com/luanti-org/luanti.git && cd luanti
cmake . -DRUN_IN_PLACE=TRUE && make -j$(nproc)
```

- CMake: `-DRUN_IN_PLACE=FALSE` (system install); `-DBUILD_CLIENT=FALSE -DBUILD_SERVER=TRUE` (jen server)
- Datové cesty: `~/.minetest` nebo `$MINETEST_USER_PATH`; system share často `/usr/share/minetest`

**Raspberry Pi**

- Klient: **64-bit Pi OS**, `apt install luanti`, sniž view distance, vyber malé ContentDB packy
- Server: stejný port **30000**; Docker arm64: [linuxserver/docker-luanti](https://github.com/linuxserver/docker-luanti) — image může potřebovat hru zkopírovanou do `/config/.minetest/games/`

## Obsah a modding

- **ContentDB:** instalace her, modů, textur v klientovi; kvalita se liší — packy vybírat vědomě; potřeba sítě
- **Lua:** oficiální mod API; hrát → upravovat → publikovat mody; docs na [wiki](https://wiki.luanti.org/Getting_Started) a příklady modů
- **MineClone-style hry:** pocit jako Minecraft bez nákupu; náročnější na starém Pi

## Multiplayer

| Režim | Poznámky |
| --- | --- |
| Veřejné servery | Pravidla s dětmi projít |
| LAN / doma | Host na PC nebo Pi; stejná verze Luanti |
| Internet | Port-forward UDP 30000 jen pokud chápeš riziko |

## Související v tomto repu

- [../README.md](../README.md) — index všech her
- [../minecraft/README.md](../minecraft/README.md) · [../roblox/README.md](../roblox/README.md) · [../terasology/README.md](../terasology/README.md)

## Odkazy

- [Luanti](https://www.luanti.org/) · [Downloads](https://www.luanti.org/downloads/) · [GitHub](https://github.com/luanti-org/luanti) · [ContentDB](https://content.luanti.org/)
- [Freeminer](https://freeminer.org/) · [Minetest Game](https://github.com/minetest/minetest_game) · [Veloren](https://veloren.net/)
