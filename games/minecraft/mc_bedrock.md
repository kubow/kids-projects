### Bedrock Edition

- Cross-play mezi Bedrock zařízeními; Marketplace; silné na konzolích, mobilech, split-screen
- Méně komunitního moddingu než Java; vázané na Microsoft účet/služby; oddělené od Java světů a serverů

### Co u nás funguje (licence × platforma)

*Ověřeno: 10/2026*

Licence Bedrocku **není přenositelná mezi obchody** (žádný cross-buy): hra koupená na Google Play platí jen pro Android build, hra koupená přes Microsoft Store / Xbox jen pro Windows build. Microsoft (Xbox) účet v Android verzi slouží jen k přihlášení (Realms, přátelé, cross-play), licenci pro Windows nedává.

| Platforma | Jak se spouští | Build hry | Potřebná licence | Stav u nás |
| --- | --- | --- | --- | --- |
| **Android** (mobil/tablet) | nativně z Google Play | Android | Google Play | ✅ funguje, hlavní platforma |
| **Linux – mcpelauncher** | [mcpelauncher](https://minecraft-linux.github.io/) (AUR `mcpelauncher-ui` + `mcpelauncher-linux`, příp. flatpak `io.mrarm.mcpelauncher`) | Android | Google Play (login v launcheru) | ✅ funguje, **tohle používáme**, viz poznámky níže; ⚠️ **ne s Family Link účtem** |
| **Linux – nadstavby nad mcpelauncherem** | [Trinity Launcher](https://github.com/Trinity-LA/Trinity-Launcher), Cianova, Iosel Edition (AppImage) | Android | Google Play | ⚠️ nezkoušeno, stejné jádro i omezení jako mcpelauncher |
| **Linux – Waydroid** | Android v kontejneru | Android | Google Play | ❌ nové verze zamrznou na loading screenu |
| **Linux – BedrockOnLinux 2.0** (07/2026) | [BedrockOnLinux](https://github.com/CryptoFewka/BedrockOnLinux): WineGDK, Xbox přihlášení, Realms, servery | Windows (GDK) | Microsoft Store / Xbox | ❌ s Google Play licencí nejde (ověřeno 17. 10. 2026: store download hlásí *„not entitled to this content“*) |
| **Linux – WineGDK / GDK-Proton ručně** | [mcbe-on-linux](https://github.com/inbob1/mcbe-on-linux), [Lutris + GDK-Proton](https://github.com/jphein/minecraft-bedrock-linux) | Windows (GDK) | Microsoft Store / Xbox | ❌ s Google Play licencí nejde; GDK-Proton u 1.26.x nefunguje (chybí D3D zařízení), funguje jen čistý WineGDK |
| **Linux – Windows VM** | VirtualBox / QEMU s Windows | Windows | Microsoft Store / Xbox | ❌ stejný problém s licencí, navíc náročné |
| **Windows** | Minecraft Launcher / Microsoft Store / PC Game Pass | Windows (GDK) | Microsoft Store / Xbox / Game Pass | ❌ s Google Play licencí nespustitelné |
| **Windows – Android emulátor** | BlueStacks / LDPlayer (WSA zrušeno 03/2025, Google Play Games na PC Minecraft nenabízí) | Android | Google Play | ⚠️ Microsoft to uvádí jako cestu, nám se to rozjet nepodařilo |

**Shrnutí:** s **Google Play licencí** hrajeme jen na **Androidu** a na **Linuxu přes mcpelauncher** (nebo jeho nadstavby). Všechny Windows-based cesty (BedrockOnLinux, WineGDK, VM, samotný Windows) potřebují **Xbox / Microsoft Store** licenci, tu nemáme.

### mcpelauncher – na co si dát pozor (stav 10/2026)

- Od roku 2026 je ve hře **DRM**. Novější verze potřebují externí mod **`mcpelauncher-updates`** (aktuálně 0.0.2). Když launcher nabídne DRM update, **neodmítat ho**, jinak nepůjde spustit žádná verze. Starý mod (např. pro 1.26.45.1) smazat, jinak se znovu zapne.
- Poslední launcher: **v1.8.4-qt6** (17. 9. 2026), opravuje chybu Google loginu.
- **Hru neaktualizovat naslepo.** Od 20. 9. 2026 hlásí launcher verzi **1.26.51.1** jako „unsupported“ ([#2044](https://github.com/minecraft-linux/mcpelauncher-manifest/issues/2044), zatím bez opravy). Zůstat na poslední verzi, která funguje, a před updatem projít [issues](https://github.com/minecraft-linux/mcpelauncher-manifest/issues).
- Autoři negarantují další podporu: kvůli DRM se aktualizace můžou kdykoli zpozdit nebo skončit. Záložní plán: Android tablet/mobil.

### Add-ony (mody) na tabletu přes USB

Mody v Bedrocku = **add-ony**: dvojice *behavior pack* (BP, chování) + *resource pack* (RP, textury). Na Androidu leží v `Android > data > com.mojang.minecraftpe > files > games > com.mojang > behavior_packs` / `resource_packs`, zapnutí ve světě je v `minecraftWorlds/<id>/world_behavior_packs.json` a `world_resource_packs.json`.

Seznam našich add-onů (verze, zdroje, ve kterých světech jsou): **[mc_bedrock_addons.md](./mc_bedrock_addons.md)**.

Správa z Linuxu: [addons.py](./addons.py). Stejné příkazy s `--pc` spravují add-ony v mcpelauncheru na tomto PC (`python addons.py --pc list`). Tablet připojit kabelem, odemknout, v notifikaci zvolit **Přenos souborů**. Skript jde přes KDE (`kioclient`, MTP), protože `kiod` drží USB spojení a `mtp-*` nástroje pak hlásí „device is busy“.

```bash
python addons.py list                       # nainstalované packy + v kolika světech jsou
python addons.py worlds [--all]             # světy a jejich zapnuté packy
python addons.py backup [CÍL]               # záloha packů (default ~/minecraft-backups/addons/<datum>)
python addons.py install soubor.mcaddon     # .mcaddon / .mcpack / .zip / složka (--replace = přepsat)
python addons.py enable <id světa> <pack>   # zapne pack i jeho BP/RP dvojče ve světě
python addons.py disable <id světa> <pack>
python addons.py remove <pack>              # smaže pack + dvojče a odpojí ho ze světů (ptá se)
```

`<pack>` = část názvu/složky nebo začátek UUID; svět zadávat **id složky** (spousta světů se jmenuje „Můj svět“).

Pozor:
- **Minecraft na tabletu zavřít** při zápisu, po instalaci hru restartovat.
- MTP nezvládne paralelní čtení (data se pomíchají) ani přepsání souboru (zapisuje se smazáním + nahráním) → skript je sekvenční, `list`/`worlds` trvá ~25 s, záloha ~3 min.
- Některé add-ony potřebují ještě zapnout **Experimenty** v nastavení světa.
- Zbraně/mobi z odebraného add-onu ve světě zmizí; před `remove` udělat `backup` (a zálohu světa).
- Diagnostika: chyby add-onů jsou v `com.mojang/logs/ContentLog*.txt` (stáhnout přes `kioclient copy`). Add-ony, které přepisují hráče (`minecraft:player`, `player.entity.json`), si navzájem kolidují a rozbíjí skiny – max. jeden takový na svět.
- Svět importovaný/uložený s add-onem má **vlastní kopii packů** v `minecraftWorlds/<id>/behavior_packs` a `resource_packs` – při opravě packu vyměnit i tu.
- **Mr. Nido's Guns** (v1.0.0) je rozbitý pro 1.26 (miliony chyb, skiny/animace hráče) → opravená verze 1.0.1 přes [fixes/fix_nido_guns.py](./fixes/fix_nido_guns.py) (11/2026). **ACT Weapons** na tabletu nefunguje (potřebuje `@minecraft/server-admin`, to je jen na dedicated serveru).

### mcpelauncher a dětský účet (Google Family Link)

*Zjištěno: 17. 10. 2026*

**Problém:** přihlášení Google účtem pod Family Link v mcpelauncheru se zasekne na login obrazovce (prázdná stránka, smyčka zpět na formulář nebo „tento účet zde nelze použít“).

**Proč:** launcher se při stahování hry tváří jako Android telefon, který se přihlašuje do Google Play. Google dohlížené (Family Link) účty na nespravovaných zařízeních a v klientech třetích stran blokuje. Rodič to nemůže schválit ani v aplikaci Family Link, protože launcher není skutečné Android zařízení, které by Family Link uměl spravovat. Nejde o chybu launcheru.

**Co nefunguje:**

- Schválení nového zařízení přes Family Link (funguje jen pro skutečné Android / ChromeOS zařízení).
- Zkopírovat hru z BedrockOnLinux (`~/.local/share/bedrock-on-linux/games/…`). To je **Windows (GDK) build** (`Microsoft.MinecraftUWP_…`), mcpelauncher potřebuje **Android build** (APK z Google Play). Formáty nejsou zaměnitelné.

**Co funguje / řešení:**

1. **Stáhnout hru jiným, nedohlíženým Google účtem, který Minecraft vlastní** (typicky rodičovský). Google účet launcher potřebuje jen ke stažení APK. Ve hře se pak dítě přihlásí svým **Microsoft/Xbox** účtem (Realms, přátelé, cross-play).
   - Pokud hru koupil jen dětský účet: zkusit **Rodinnou knihovnu Google Play** (Family Library). Když ji hra podporuje (ověřit na stránce hry v Google Play), sdílí se nákup s rodičovským účtem ve stejné rodině a ten ji pak může stáhnout v launcheru.
2. **Přenést už stažené verze** z jiného počítače s funkčním mcpelauncherem: složka `~/.local/share/mcpelauncher/versions/` (flatpak: `~/.var/app/io.mrarm.mcpelauncher/data/mcpelauncher/versions/`). Stažená verze se pak spouští bez Google loginu.
3. **Ukončit dohled** v Family Link, až dítě dosáhne věku digitálního souhlasu (v ČR 15 let, jinde 13–16). Pak se účet přihlásí normálně.

**Přihlášení do Xbox/Microsoft účtu ve hře** (nezaměňovat s Google loginem v launcheru) řídí **Microsoft Family Safety**, ne Google Family Link: na [family.microsoft.com](https://family.microsoft.com) → dětský účet → nastavení Xbox povolit přihlášení a hraní multiplayeru. Účet dítěte do 13 let musí mít souhlas rodiče.

### Umístění světů

| Platforma | Cesta k `minecraftWorlds` |
| --- | --- |
| Android | `Android > data > com.mojang.minecraftpe > files > games > com.mojang > minecraftWorlds` |
| Linux – mcpelauncher | `~/.local/share/mcpelauncher/games/com.mojang/minecraftWorlds` (flatpak: `~/.var/app/io.mrarm.mcpelauncher/data/mcpelauncher/games/com.mojang/minecraftWorlds`) |
| Linux – BedrockOnLinux / GDK-Proton | `~/.local/share/bedrock-on-linux/compatdata/pfx/drive_c/users/steamuser/AppData/Roaming/Minecraft Bedrock/Users/Shared/games/com.mojang/minecraftWorlds` |

Zálohy světů jsou v [./minecraftWorlds](./minecraftWorlds).

Složky světů (na tabletu i v záloze) jsou od 11/2026 přejmenované podle názvu světu (ASCII, `Můj svět` zůstávají s původním id) (název je vidět i v `levelname.txt` každé složky). Hra svět najde podle složky, přejmenování nevadí. Pozor: úložiště Androidu **nerozlišuje velká/malá písmena** (`Viki` = `VIKI`).

### Bedrock on Linux – odkazy

- [MeantPlace279/mcbeonlinux](https://github.com/MeantPlace279/mcbeonlinux): přehled všech známých metod (průběžně aktualizovaný)
- [minecraft-linux / mcpelauncher](https://minecraft-linux.github.io/) · [releases](https://github.com/minecraft-linux/mcpelauncher-manifest/releases) · [FAQ #797](https://github.com/minecraft-linux/mcpelauncher-manifest/issues/797): Android verze, Google Play
- [Trinity Launcher](https://github.com/Trinity-LA/Trinity-Launcher): Qt6 nadstavba nad mcpelauncherem (správa verzí, mody, texture packy)
- [CryptoFewka/BedrockOnLinux](https://github.com/CryptoFewka/BedrockOnLinux) · [Wyze3306/BedrockOnLinux](https://github.com/Wyze3306/BedrockOnLinux): Windows verze, Xbox licence
- [inbob1/mcbe-on-linux](https://github.com/inbob1/mcbe-on-linux) · [jphein/minecraft-bedrock-linux](https://github.com/jphein/minecraft-bedrock-linux): Windows verze přes WineGDK / GDK-Proton
- [XDA: BedrockOnLinux 2.0](https://www.xda-developers.com/after-nine-years-linux-gamers-can-finally-join-their-console-friends-in-minecraft-bedrock/) (07/2026)
