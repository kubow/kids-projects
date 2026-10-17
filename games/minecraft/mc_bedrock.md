### Bedrock Edition

- Cross-play mezi Bedrock zařízeními; Marketplace; silné na konzolích, mobilech, split-screen
- Méně komunitního moddingu než Java; vázané na Microsoft účet/služby; oddělené od Java světů a serverů

### Co u nás funguje (licence × platforma)

*Ověřeno: 10/2026*

Licence Bedrocku **není přenositelná mezi obchody** (žádný cross-buy): hra koupená na Google Play platí jen pro Android build, hra koupená přes Microsoft Store / Xbox jen pro Windows build. Microsoft (Xbox) účet v Android verzi slouží jen k přihlášení (Realms, přátelé, cross-play), licenci pro Windows nedává.

| Platforma | Jak se spouští | Build hry | Potřebná licence | Stav u nás |
| --- | --- | --- | --- | --- |
| **Android** (mobil/tablet) | nativně z Google Play | Android | Google Play | ✅ funguje, hlavní platforma |
| **Linux – mcpelauncher** | [mcpelauncher](https://minecraft-linux.github.io/) (flatpak `io.mrarm.mcpelauncher`) | Android | Google Play (login v launcheru) | ✅ funguje, **tohle používáme**, viz poznámky níže |
| **Linux – nadstavby nad mcpelauncherem** | [Trinity Launcher](https://github.com/Trinity-LA/Trinity-Launcher), Cianova, Iosel Edition (AppImage) | Android | Google Play | ⚠️ nezkoušeno, stejné jádro i omezení jako mcpelauncher |
| **Linux – Waydroid** | Android v kontejneru | Android | Google Play | ❌ nové verze zamrznou na loading screenu |
| **Linux – BedrockOnLinux 2.0** (07/2026) | [BedrockOnLinux](https://github.com/CryptoFewka/BedrockOnLinux): WineGDK, Xbox přihlášení, Realms, servery | Windows (GDK) | Microsoft Store / Xbox | ❌ s Google Play licencí nejde |
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

### Umístění světů

| Platforma | Cesta k `minecraftWorlds` |
| --- | --- |
| Android | `Android > data > com.mojang.minecraftpe > files > games > com.mojang > minecraftWorlds` |
| Linux – mcpelauncher | `~/.local/share/mcpelauncher/games/com.mojang/minecraftWorlds` (flatpak: `~/.var/app/io.mrarm.mcpelauncher/data/mcpelauncher/games/com.mojang/minecraftWorlds`) |
| Linux – GDK-Proton | `~/.local/share/bedrock-on-linux/compatdata/pfx/drive_c/users/steamuser/AppData/Roaming/Minecraft Bedrock/Users/Shared/games/com.mojang/minecraftWorlds` |

Zálohy světů jsou v [./minecraftWorlds](./minecraftWorlds).

### Bedrock on Linux – odkazy

- [MeantPlace279/mcbeonlinux](https://github.com/MeantPlace279/mcbeonlinux): přehled všech známých metod (průběžně aktualizovaný)
- [minecraft-linux / mcpelauncher](https://minecraft-linux.github.io/) · [releases](https://github.com/minecraft-linux/mcpelauncher-manifest/releases) · [FAQ #797](https://github.com/minecraft-linux/mcpelauncher-manifest/issues/797): Android verze, Google Play
- [Trinity Launcher](https://github.com/Trinity-LA/Trinity-Launcher): Qt6 nadstavba nad mcpelauncherem (správa verzí, mody, texture packy)
- [CryptoFewka/BedrockOnLinux](https://github.com/CryptoFewka/BedrockOnLinux) · [Wyze3306/BedrockOnLinux](https://github.com/Wyze3306/BedrockOnLinux): Windows verze, Xbox licence
- [inbob1/mcbe-on-linux](https://github.com/inbob1/mcbe-on-linux) · [jphein/minecraft-bedrock-linux](https://github.com/jphein/minecraft-bedrock-linux): Windows verze přes WineGDK / GDK-Proton
- [XDA: BedrockOnLinux 2.0](https://www.xda-developers.com/after-nine-years-linux-gamers-can-finally-join-their-console-friends-in-minecraft-bedrock/) (07/2026)
