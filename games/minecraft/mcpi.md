### Pi Edition (+ cíle API pro app)

- Malý starý sandbox na Pi; umístění/odstranění bloků, pohyb hráče, kamera, chat přes **Python** ([`mcpi`](https://pypi.org/project/mcpi/))
- Lehký na slabém hardware; vhodný pro malou automatizaci a úpravy světa
- **Není** moderní Minecraft: málo bloků/mechanik, bez Realms/Marketplace/cross-play s Java nebo Bedrock
- **Komunitní revival:** [Minecraft Pi: Reborn](https://gitea.thebrokenrail.com/minecraft-pi-reborn/minecraft-pi-reborn)
- **Java server shim:** [RaspberryJuice](https://www.raspberrypi-juice.com/) — plugin pro Paper/Spigot s Pi-like API, stejné `mcpi` skripty míří na Java svět (experiment; ne moderní mod stack)
- **Tutoriál:** [Getting Started with Minecraft Pi](https://projects.raspberrypi.org/en/projects/getting-started-with-minecraft-pi/0)

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
