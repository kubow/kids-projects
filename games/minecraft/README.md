# Minecraft

Poznámky a nástroje pro **Minecraft** na Linuxu a Raspberry Pi v tomto repu. Komerční hra (Microsoft); tři hlavní edice se liší platformou a tím, co lze skriptovat.

## Edice (vyber jeden stack)

| Edice | Platformy | Nejlepší pro | Toto repo |
| --- | --- | --- | --- |
| **Pi Edition** | Raspberry Pi (legacy) | Python block API, Pi ve třídě | [Streamlit app](./app.py) + `mcpi` |
| **Java** | Windows, macOS, Linux | Plná hra, mody, servery, redstone | Jen poznámky k hraní/instalaci — ne Pi API app |
| **Bedrock** | Windows, konzole, mobily, tablety | Cross-play, Marketplace, ovladače | Zde nepokrýváno |

### Pi Edition (+ cíle API pro app)

- Malý starý sandbox na Pi; umístění/odstranění bloků, pohyb hráče, kamera, chat přes **Python** ([`mcpi`](https://pypi.org/project/mcpi/))
- Lehký na slabém hardware; vhodný pro malou automatizaci a úpravy světa
- **Není** moderní Minecraft: málo bloků/mechanik, bez Realms/Marketplace/cross-play s Java nebo Bedrock
- **Komunitní revival:** [Minecraft Pi: Reborn](https://gitea.thebrokenrail.com/minecraft-pi-reborn/minecraft-pi-reborn)
- **Java server shim:** [RaspberryJuice](https://www.raspberrypi-juice.com/) — plugin pro Paper/Spigot s Pi-like API, stejné `mcpi` skripty míří na Java svět (experiment; ne moderní mod stack)
- **Tutoriál:** [Getting Started with Minecraft Pi](https://projects.raspberrypi.org/en/projects/getting-started-with-minecraft-pi/0)

### Java Edition

- Plná desktop hra; mody, modpacky, shadery, data packy, snapshoty, velký ekosystém serverů
- **Linux hraní (bez `mcpi`):** oficiální launcher nebo [Prism Launcher](https://prismlauncher.org/) s minimální instancí (např. Fabric + Sodium pro výkon)
- Bez cross-play s Bedrock; modding/instalace techničtější; výkon závisí na hardware a modpacku

### Bedrock Edition

- Cross-play mezi Bedrock zařízeními; Marketplace; silné na konzolích, mobilech, split-screen
- Méně komunitního moddingu než Java; vázané na Microsoft účet/služby; oddělené od Java světů a serverů

## Streamlit app (jen Pi API)

[app.py](./app.py) — webové UI pro **Minecraft Pi Edition API** (`mcpi`, volitelně [`minecraftstuff`](https://pypi.org/project/minecraftstuff/)).

- **Připojení k:** Pi Edition **nebo** RaspberryJuice na Java serveru (host + port, výchozí **4711**)
- **Funkce:** umístění bloků (vč. spread), předpřipravené stavby, entity, teleport hráče, import `.schematic` s fallbackem pro nepodporované bloky
- **Není** launcher pro Java/Bedrock; nástroj pro výuku/skriptování na starém API

```bash
source venv/bin/activate
pip install -r requirements.txt
streamlit run games/minecraft/app.py
```

## Co použít v tomto repu

- **Programovat bloky z Pythonu** → Pi Edition nebo RaspberryJuice + tato app
- **Hrát moderní Minecraft na Linuxu** → Java Edition přímo (bez `mcpi`, Paper nebo RaspberryJuice)

## Související v tomto repu

- [../README.md](../README.md) — index
- [../luanti/README.md](../luanti/README.md) — open voxel + [Miney](../luanti/README.md) (Python, jako `mcpi`)
- [../roblox/README.md](../roblox/README.md) · [../terasology/README.md](../terasology/README.md)

## Odkazy

- [minecraft.net](https://www.minecraft.net/)
- [mcpi](https://pypi.org/project/mcpi/) · [minecraftstuff](https://pypi.org/project/minecraftstuff/)
- [StanislavPetrovV/Minecraft](https://github.com/StanislavPetrovV/Minecraft) · [fogleman/Craft](https://github.com/fogleman/Craft) — malé vzdělávací klony
