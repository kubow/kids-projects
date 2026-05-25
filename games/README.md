# Digitální hry

Hry sledované v tomto repu — sandbox / UGC a **retro emulace** — hlavně pro **Linux** a **Raspberry Pi**. Každá volba má vlastní složku s poznámkami k instalaci a odkazy.

- → [Minecraft/](./minecraft/)
    - Placený voxel sandbox: survival, creative, multiplayer a mody.
    - Bezplatné alternativy jako [Minecraft Pi: Reborn](https://gitea.thebrokenrail.com/minecraft-pi-reborn/minecraft-pi-reborn) (komunitní revival)
    - Bonus: **Pi Edition API** pro programování bloků v Pythonu ([Streamlit app](./minecraft/app.py)).
- → [Roblox/](./roblox/)
    - Bezplatná platforma pro hraní a publikování **experiencí** od hráčů;
    - **Roblox Studio** pro stavbu v Luau.
- → [Luanti/](./luanti/)
    - Open-source voxel **engine** (dříve Minetest); hry a mody z ContentDB, skriptování v **Lua**.
    - Silné na **Linuxu** a **Raspberry Pi**; volitelný domácí server (bez komerčního účtu).
    - **Programování bloků v Pythonu:** mod [Miney](https://miney.readthedocs.io/) + [Streamlit app](./luanti/app.py) (obdoba Minecraft Pi / `mcpi`).
- → [Terasology/](./terasology/)
    - Open-source voxel hra s **moduly** (Java); **Terasology Launcher** na desktop **Linux x86_64**.
    - Klient na Pi nepodporován; na Pi raději Luanti nebo Minecraft.
- → [Retro/](./retro/)
    - Klasické hry přes **emulaci** na Linuxu a Raspberry Pi.
    - Hlavní zaměření: **RetroPie** (konzole/handheldy) a **DOSBox** (MS-DOS).

## Další srovnatelné hry

Bez vlastní složky v repu — pro srovnání a alternativy.

### UGC platformy a online sandboxy

- [Core Games](https://www.coregames.com/) — bezplatná UGC platforma (Unreal); tvorba a hraní multiplayer světů na PC
- [Creativerse](https://store.steampowered.com/app/280790/Creativerse/) — voxel sandbox na Steamu; blueprinty, dobrodružství, online světy
- [Fortnite Creative / UEFN](https://www.fortnite.com/creative) — kreativní režim od Epic; jiné publikum než Roblox

### Open-source voxel

- [Veloren](https://veloren.net/) — open multiplayer voxel RPG (Rust)
- [Freeminer](https://freeminer.org/) — fork ve větvi Minetest / Luanti

### Sandboxy spíš na hraní (ne plné UGC platformy)

- [Trove](https://www.trionworlds.com/trove) — MMO voxel dobrodružství
- [Terraria](https://terraria.org/) — 2D sandbox, crafting a bossové

### Učení a tvorba her (ne katalogy ve stylu Roblox)

- [Scratch](https://scratch.mit.edu/) — blokové programování pro začátečníky
- [GDevelop](https://gdevelop.io/) — vizuální editor her; export na web a mobil
- [Godot](https://godotengine.org/) — open game engine; vlastní hry (náročnější než Studio)

### Malé / vzdělávací projekty ve stylu Minecraft

- [Getting Started with Minecraft Pi](https://projects.raspberrypi.org/en/projects/getting-started-with-minecraft-pi/0) — tutoriál Raspberry Pi Foundation
- [StanislavPetrovV/Minecraft](https://github.com/StanislavPetrovV/Minecraft) — voxel engine v Pythonu a OpenGL
- [fogleman/Craft](https://github.com/fogleman/Craft) — jednoduchý Minecraft-like klon v C a OpenGL
