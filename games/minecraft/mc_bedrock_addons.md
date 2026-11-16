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

### Bedrock add-ony (PC – mcpelauncher)

*Stav: 16. 11. 2026 · Linux, mcpelauncher · Minecraft 1.26.60.4*

Správa stejným skriptem s přepínačem `--pc`: `python addons.py --pc list|worlds|install|enable …` (cesta `~/.local/share/mcpelauncher/games/com.mojang`). Soubory v `~/Downloads/Minecraft/Addons`, stažené z MCPEDL (CurseForge blokuje stahování skriptem; MCPEDL stránky obsahují přímé odkazy `edge.mcpedl.com/files/…`).

| Add-on | Verze | Packy | Soubor | Stav | Zdroj |
| --- | --- | --- | --- | --- | --- |
| ThatMob's Verity (PnTMC) | 4.0.0 – V26.60 | BP + RP | `ThatMob-s-Verity-4.0.0-by-PnTMC-Add-on-V26.60.mcaddon` | ⚠️ beta (`server@2.12.0-beta`), nahradil build V26.50 (stejné UUID), ve 22 světech; kopie vložené v 17 světech vyměněny taky (záloha `~/minecraft-backups/verity-26.50-embedded-2026-11-16.tar.gz`); světy potřebují **Experimenty → Beta APIs** | [MCPEDL](https://mcpedl.com/verity-bedrock-edition/) |
| Me Poppy Playtime | 1.0.15 | BP + RP | `Me Poppy Playtime v1.0.15.mcaddon` | ✅ 17 světů | neznámý |
| Chikawa Mob | 1.3.1 | BP + RP | `ChikawaMob_Beh-Res_v1_3.mcaddon` | ✅ 12 světů | neznámý |
| World Animals (+ Structures Generator) | 1.0.0 | 2× BP + RP | `World Animals Add-on.mcaddon` | ✅ | neznámý |
| Border Expansion | 1.1.0 | BP | – (přišel s importovaným světem) | ⚠️ chybí jeho RP (`61130485…`) | neznámý |
| Paws & Claws: Rodent Companions | 1.3.9 | jen RP | `PawsClaws_RodentCompanions_1.3.9_RP.mcpack` | ⚠️ chybí BP, nepoužitý | neznámý |
| The Sift WE 0.9 | 1.0.1 | RP | `The-Sift-WE-0.9-RP.mcpack` | ⚪ nepoužitý | neznámý |
| Kittens (MCTools) | 1.0.0 | skin pack | `../Packs/Kittens.mcpack` | ✅ | neznámý |
| Furniture Craft | 1.0.0 | BP + RP | `Furniture_Craft.mcaddon` | ✅ nainstalováno 16. 11. | [MCPEDL](https://mcpedl.com/furniture-craft/) |
| Explorer's World Map | 1.3.1 STABLE | BP + RP | `EWM STABLE V1.3.1 ACHIEVEMENTS.mcaddon` | ✅ nainstalováno 16. 11. | [MCPEDL](https://mcpedl.com/explorers-world-map/) |
| Ore Boost V2 | 2.0.0 | BP | `Ore_Boost_V2.mcaddon` | ✅ nainstalováno 16. 11. | [MCPEDL](https://mcpedl.com/ore-boost/) |
| Mr. Nido's Guns (**opravený**) | 1.0.1 | BP + RP | `Mr. Nido's Guns Add-on (fixed).mcaddon` | ✅ nainstalováno 16. 11., mění hráče | [MCPEDL](https://mcpedl.com/mr-nidos-guns-add-on/) + [fixes/fix_nido_guns.py](./fixes/fix_nido_guns.py) |
| 🆕 Alylica's Dragons | 2.2.0 | BP + RP | `AlylicasDragons 2.2.0.mcaddon` | ✅ nainstalováno 16. 11., bez experimentů; 16 draků k vylíhnutí a ježdění | [MCPEDL](https://mcpedl.com/alylicas-dragons-addon/) · [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/alylicas-dragons-addon) |
| 🆕 Core Craft | 1.2.9 | BP + RP | `core-craft_v1.2.9.mcaddon` | ✅ nainstalováno 16. 11.; mobi, struktury, nábytek, End update; velký → nejlépe nový svět | [MCPEDL](https://mcpedl.com/core-craft/) · [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/core-craft) |
| 🆕 Structures Plus | 1.0 | BP | `Structure-1.0-BP.mcpack` | ✅ nainstalováno 16. 11.; jen nové chunky | [MCPEDL](https://mcpedl.com/structures-plus/) · [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/structures-plus) |
| 🆕 Legendary Mobs | 1.1.0 | BP + RP | `Legendary Mobs - 1.1.0.mcaddon` | ✅ nainstalováno 16. 11., bez experimentů; jezdecká zvířata z MC Legends | [MCPEDL](https://mcpedl.com/legendary-mobs/) · [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/legendary-mobs) |

Z tabletového seznamu na PC zatím **chybí** (na MCPEDL není přímý soubor, jen CurseForge → stáhnout ručně v prohlížeči do `~/Downloads/Minecraft/Addons` a `addons.py --pc install …`): Better Basic Structures, Laser Minigun, Alex's Mobs, Modern Furniture WE, Crafting Table Blueprint.

#### Tipy na další (nevyzkoušené)

| Add-on | Proč | Pozor | Zdroj |
| --- | --- | --- | --- |
| Immortal Dogs (INTOR) | ochočení psi neumřou | – | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/immortal-dogs) |
| SERP Pokédrock | Pokémoni, souboje, evoluce | velký, „Beta“ release → vlastní svět | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/serp-pokemon-addon) |
| Poppy Pluhtime | Poppy Playtime továrna, GrabPack | pravděpodobně mění hráče | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/poppy-pluhtime) |
| Absolute Guns 3 (3D) | 26 zbraní | rozpracovaná beta (14 %) | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/absolute-guns-3-3d) |
| Twixxel's Stalkers BE (PnTMC) | horor-lite, od autora Verity | – | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/twixxels-stalkers-bedrock-edition) |
| Always Watching | postava jen kouká, neútočí | – | [CurseForge](https://www.curseforge.com/minecraft-bedrock/addons/always-watching) |

Nevhodné: More Body Actions / Pickup & Carry a Multiplayer Waypoint System (Beta API, mění hráče), Dragon Mounts 3 (všechny experimenty, rozbité, 2024), Simple Vehicles (experimenty).

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
