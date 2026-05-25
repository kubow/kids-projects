# Roblox

Průzkum **Robloxe** na Linuxu a Raspberry Pi. Bezplatná UGC platforma (hraní experiencí + **Roblox Studio** / Luau). **Žádný oficiální Linux desktop player** — níže komunitní nástroje.

## Platformy (vyber jeden stack)

| Stack | Platformy | Nejlepší pro | Limity |
| --- | --- | --- | --- |
| **Oficiální** | Windows, macOS | Player + Studio, aktualizace | Nativně ne na Linuxu |
| **Mobil** | Android, iOS | Telefony/tablety, velký katalog | Touch-first; něco-exkluzivní hry |
| **Sober** | Linux **x86_64** | Hraní na Linux PC | Neoficiální, closed source, experiment; [Hyperion](https://en.help.roblox.com/) zablokoval **Wine/Grapejuice** (~2023) pro player |
| **Vinegar** | Linux | **Jen Studio** (Wine) | Player zablokován; pluginy mohou být nestabilní |
| **Pi OS** | Raspberry Pi | — | Sober je x86_64-only; prakticky žádný nativní Roblox na Debian Pi OS |
| **Pi + LineageOS** | Pi 4/5 | Hraní přes Android APK | Samostatná SD karta; výkon se liší |

**Oficiální (Windows / macOS / mobil)**

- Plný player a [Roblox Studio](https://create.roblox.com/); nejlepší kompatibilita a podpora
- Online sociální platforma — účet, soukromí a rodičovská kontrola vědomě

## Linux: hraní (Sober)

Aktuálně funkční cesta: [Sober](https://sober.vinegarhq.org/) ([Flathub](https://flathub.org/apps/org.vinegarhq.Sober)) — spouští oficiální **Android x86_64** APK v dedikovaném runtime (ne Wine).

- **Kontext:** staré Linux návody používaly Wine/Grapejuice; **nepoužívat** pro player po Hyperion
- **Poznámky:** Roblox nepodporuje; může se rozbít po update; distribuce jen Flatpak; instalace APK může selhat (Cloudflare/region/verze — viz [issues](https://github.com/vinegarhq/sober/issues))
- **Požadavky:** kernel ≥ 5.11; **x86_64** + SSE4.1 (SSE4.2 doporučeno); OpenGL ES 3.0 (Vulkan 1.1 doporučeno); ARM/Pi **není** production-ready

```bash
grep -o sse4_1 /proc/cpuinfo | head -1   # jen PC; Pi ukáže aarch64
uname -m                                  # x86_64 vs aarch64
flatpak install flathub org.vinegarhq.Sober
```

- První spuštění: raději **automatická** instalace APK; **Quick Sign-in** často lepší než embedded web login
- Config / troubleshooting: [configuration](https://vinegarhq.org/Sober/Configuration/index.html) · [troubleshooting](https://vinegarhq.org/Sober/Troubleshooting.html)
- Odinstalace: `flatpak uninstall org.vinegarhq.Sober` (přidej `--delete-data` pro reset)

**Další možnosti hraní na Linuxu**

| Metoda | Stav |
| --- | --- |
| Waydroid | Možné; náročnější; Wayland/myš |
| Wine / Grapejuice / Lutris | **Zablokováno** (player) |
| VM + Windows | Funguje; licence + zdroje |
| Stream z jiného zařízení | Pi/PC jako thin client (Moonlight atd.) |

## Linux: Studio (Vinegar)

```bash
flatpak install flathub org.vinegarhq.Vinegar
flatpak run org.vinegarhq.Vinegar studio
```

- [Vinegar install docs](https://vinegarhq.org/Vinegar/Installation.html)
- Seriózní práce ve Studiu: Windows/macOS stále nejspolehlivější
- Nástroje (libovolné OS): [Rojo](https://rojo.space/) · [Wally](https://wally.run/) · [roblox-pi-template](https://github.com/dnouri/roblox-pi-template)

## Raspberry Pi

**Pi OS (Debian)** — Sober nejde nainstalovat (x86_64 Flathub); Wine cesta na ARM irelevantní ([forum](https://forums.raspberrypi.com/viewtopic.php?t=394890)).

**LineageOS + Play Store (jen hraní)**

- Flash [KonstaKANG LineageOS](https://konstakang.com/devices/rpi5/) na **náhradní SD kartu** (preferovaně Pi 5)
- Přidej GApps (např. [NikGapps](https://nikgapps.com/downloads)) dle docs image → Roblox z Play Store
- Náhradní SD chrání Pi OS; jednoduché hry OK, náročné experiencí mohou trhat; ne pro Studio
- Návody: [pihow](https://pihow.co.uk/how-to-install-and-play-roblox-on-raspberry-pi/) · [forums](https://forums.raspberrypi.com/viewtopic.php?t=385216) · [video](https://www.youtube.com/watch?v=QVEiWbubHUw)

**Bez přeflashování** — Roblox na telefonu/PC/konzoli a zrcadlení nebo remote desktop na TV (latence).

## Co použít v tomto repu

| Cíl | Použít |
| --- | --- |
| Hraní na Linux PC (x86_64) | Sober (Flatpak) |
| Studio na Linuxu | Vinegar + Rojo/Wally |
| Hraní na Pi | LineageOS + Roblox APK, nebo stream |
| Open voxel + Python (ne Roblox) | [../luanti/README.md](../luanti/README.md) |
| Staré Grapejuice blogy | Zastaralé → Sober |

## Související v tomto repu

- [../README.md](../README.md) — index
- [../minecraft/README.md](../minecraft/README.md) · [../luanti/README.md](../luanti/README.md) · [../terasology/README.md](../terasology/README.md) · [../retro/README.md](../retro/README.md)

## Odkazy

- [roblox.com](https://www.roblox.com/) · [Create / Studio](https://create.roblox.com/)
- [PC requirements](https://en.help.roblox.com/hc/en-us/articles/203312800-Computer-Hardware-Operating-System-Requirements) · [mobile requirements](https://en.help.roblox.com/hc/en-us/articles/203625474)
- [VinegarHQ](https://vinegarhq.org/) · [Sober FAQ](https://vinegarhq.org/Sober/FAQ/index.html) · [Vinegar on Flathub](https://flathub.org/apps/org.vinegarhq.Vinegar)
