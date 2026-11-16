### Bedrock add-ony (tablet)

*Stav: 16. 11. 2026 · tablet Galaxy Tab S6 Lite · Minecraft 1.26.62 (Android)*

Seznam add-onů, které používáme. **Samotné soubory v repu nejsou** (repo je veřejné, add-ony jsou cizí práce) – lokálně leží v `~/Downloads/Minecraft`, jinak stáhnout ze zdroje. Instalace a správa: [addons.py](./addons.py), postup v [mc_bedrock.md](./mc_bedrock.md#add-ony-mody-na-tabletu-přes-usb).

#### Nainstalované

| Add-on | Verze | Packy | Soubor | Zapnuto ve světech | Stav | Zdroj |
| --- | --- | --- | --- | --- | --- | --- |
| Better Basic Structures 1.3 (Al3xandre) | 6.5.0 | BP (subpack `hard_rates`) | `Better Basic Structures 1.3 By Al3xandre.mcpack` | `l4qVavJfjZ8=` (Můj svět), `Muj_svetViki`, `VVV` | ✅ OK | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/better-basic-structures) · [MCPEDL](https://mcpedl.com/better-basic-structures-add-on/) |
| Furniture Craft (FleetMC Studio) | 1.0.0 | BP + RP | `Furniture_Craft.mcaddon` | `TUi39f38ZLY=` (Můj svět) | ✅ OK | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/furniture-craft) · [MCPEDL](https://mcpedl.com/furniture-craft/) |
| Laser Minigun | 10.0.0 | BP + RP | `Minigun-v10 (1).mcaddon` | `TUi39f38ZLY=` (Můj svět) | ✅ OK | pravděpodobně [CurseForge – Minigun!](https://www.curseforge.com/minecraft-bedrock/addons/minigun) |
| Mr. Nido's Guns (**opravený**) | 1.0.1 | BP + RP | `Mr. Nido's Guns Add-on (fixed).mcaddon` | – (připraveno pro jiný svět) | 🔧 originál 1.0.0 rozbitý pro 1.26 → [fixes/fix_nido_guns.py](./fixes/fix_nido_guns.py) | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/mr-nidos-guns-add-on) |
| Explorer's World Map & Minimap (Minecart7) | 1.3.1 | BP + RP | `Explorer's World Map STABLE V1.3.1 ACHIEVEMENTS.mcaddon` | – | ✅ stabilní verze bez Beta API, autor projekt „pozastavil“ | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/explorers-world-map) |
| Ore Boost V2 (INTOR) | 2.0.0 | BP (subpack `50` / `75` %) | `Ore_Boost_V2.mcaddon` | – | ✅ jen nově generované chunky → nejlépe nový svět | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/ore-boost) |
| ThatMob's Verity (PnTMC) | 4.0.0 | BP + RP | `ThatMob's Verity 4.0.0 (V26.60).mcaddon` | – | ⚠️ horor; svět musí mít **Experimenty → Beta APIs**; beta API vázané na verzi hry (26.60); AI/hlas jen přes Python bridge na PC (`/connect`) | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/verity-bedrock-edition) |
| Alex's Mobs (animals for 1.26.1) | 1.0.2 | BP + RP | `Alex_Mobs_animals_for_1.26.1.mcaddon` | – | ⚪ nepoužitý | neověřeno – existuje víc portů, např. [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/alex-mobs), [MCPEDL](https://mcpedl.com/alex-s-mobs/) |
| Modern Furniture WE 14.3 | 1.0.1 | BP + RP | `Modern Furniture WE 14.3 BP.mcpack` + `… 14.3s RP.mcpack` | – | ⚪ nepoužitý, existuje novější verze | pravděpodobně [CurseForge – Modern Furniture +750 BLOCKS](https://www.curseforge.com/minecraft-bedrock/addons/modern-furniture-minecraft-bedrock) |
| Crafting Table Blueprint | 1.0.0 | RP (textury) | `Crafting Table Blueprint (Bedrock).mcpack` | – | ⚪ nepoužitý | neznámý |

`Svět` = název složky v `minecraftWorlds`.

#### Odebrané / nevhodné

| Add-on | Důvod |
| --- | --- |
| Mr. Nido's Guns 1.0.0 (originál) | Na 1.26 miliony chyb, rozbité skiny/animace hráče (zbytky ze superhero add-onu, překlep `maindhand`, padající skripty). Nahrazeno opravenou 1.0.1. |
| ACT Weapons (`actwThompsonandJammingaddedversion.mcaddon`) | Potřebuje `@minecraft/server-admin` (jen dedicated server) a `server-gametest` beta → na tabletu nefunguje. Navíc přepisuje hráče. Smazáno. |
| CRAFTING TABLE BLUE PRINT.zip | Java resource pack (`pack.mcmeta`), ne Bedrock. Smazáno. |
| Toykai, MOA Decor Toys | Java mody (Forge/NeoForge `.jar`), na Bedrock nejdou. Nestaženo. |

#### Pravidla

- **Odkud stahovat:** Bedrock add-ony jsou na CurseForge pod `/minecraft-bedrock/…`; odkazy `/minecraft/mc-mods/…` jsou **Java** a na tabletu nefungují. Další zdroj: [MCPEDL](https://mcpedl.com/category/addons/).
- **Max. jeden add-on, který mění hráče, na svět** (zbraně, Pickup & Carry, More Body Actions, Morphing Bracelet, Spider-Man…). Přepisují `player.entity.json` a navzájem rozbíjí skiny.
- Před instalací ověřit verzi: `min_engine_version` a hlavně **beta** závislosti (`…-beta`) musí sedět na verzi hry.
- Po instalaci restart hry; zapnutí ve světě v nastavení světa nebo `python addons.py enable <svět> <pack>`.
