# Arcade uses of TMS34010 / TMS34020

Index of arcade machines whose graphics path is built around a TMS34010 or TMS34020. Driver paths are taken from MAME at the verified commit recorded in `emulation/mame/UPSTREAM.md` (`70725158b4e9d2e1230c0515faec754f9cee86a2`). Game/year strings come from each driver's top-of-file comments; trust them over generic web sources. The "verification" column says how each row was checked:

- `mame-driver` — title and year are listed in the indicated MAME `.cpp` file's header comment block.
- `mame-cpu` — additionally confirmed that the driver instantiates `TMS34010(...)` or `TMS34020(...)`.
- `unverified` — claim came from the original task list but has not been cross-checked yet.

| Title | Manufacturer | Year | Chip | Clock (MHz) | MAME driver | Board | Verification | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NARC | Williams / Midway | 1989 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y/Z-unit | mame-driver | First Williams arcade title to use the GSP family. |
| Trog | Midway | 1990 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | |
| Smash TV | Williams | 1990 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | |
| Strike Force | Midway | 1991 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | |
| High Impact Football | Williams | 1991 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | |
| Super High Impact | Midway | 1991 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | |
| Terminator 2: Judgment Day | Midway | 1991 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | Listed in midyunit.cpp top comment, not midtunit. |
| Mortal Kombat (original) | Midway | 1992 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | Original release was Y-unit. |
| Total Carnage | Midway | 1992 | TMS34010 | — | `src/mame/midway/midyunit.cpp` | Y-unit | mame-driver | |
| Mortal Kombat (T-unit) | Midway | 1992 | TMS34010 | — | `src/mame/midway/midtunit.cpp` | T-unit | mame-driver | T-unit reissue. |
| Mortal Kombat II | Midway | 1993 | TMS34010 | — | `src/mame/midway/midtunit.cpp` | T-unit | mame-driver | |
| NBA Jam | Midway | 1993 | TMS34010 | — | `src/mame/midway/midtunit.cpp` | T-unit | mame-driver | |
| NBA Jam Tournament Edition | Midway | 1994 | TMS34010 | — | `src/mame/midway/midtunit.cpp` | T-unit | mame-driver | Listed in midtunit.cpp top comment (not xunit). |
| Judge Dredd (prototype) | Midway | 1994 | TMS34010 | — | `src/mame/midway/midtunit.cpp` | T-unit | mame-driver | Prototype. |
| Revolution X | Midway | 1994 | TMS34010 | — | `src/mame/midway/midxunit.cpp` | X-unit | mame-driver | |
| Mortal Kombat 3 | Midway | 1995 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | |
| Ultimate Mortal Kombat 3 | Midway | 1995 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | |
| WWF WrestleMania | Midway | 1995 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | |
| 2 On 2 Open Ice Challenge | Midway | 1995 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | Sometimes referred to as "NHL 2-on-2 Open Ice Challenge"; MAME lists the title without "NHL". |
| NBA Hangtime | Midway | 1995 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | |
| NBA Maximum Hangtime | Midway | 1996 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | |
| Rampage World Tour | Midway | 1997 | TMS34010 | — | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-driver | |
| Hard Drivin' | Atari Games | 1989 | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | First-gen polygon racer. |
| Hard Drivin' Compact | Atari Games | 1990 | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | |
| Race Drivin' | Atari Games | 1990 | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | |
| Race Drivin' Compact | Atari Games | 1990 | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | |
| S.T.U.N. Runner | Atari Games | 1990 | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | |
| Steel Talons | Atari Games | 1991 | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | |
| Hard Drivin's Airborne (prototype) | Atari Games | — | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | Year not given in driver header; prototype. |
| Street Drivin' (prototype) | Atari Games | — | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | Prototype mentioned in driver header. |
| BMX Heat (prototype) | Atari Games | — | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | Prototype mentioned in driver header. |
| Police Trainer (Atari prototype) | Atari Games | — | TMS34010 | — | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-driver | Prototype on Hard Drivin' hardware (not the production P&P/ICE Police Trainer). |
| Metal Maniax (prototype) | Atari Games | — | TMS34020 | — | `src/mame/atari/harddriv.cpp` | reworked Hard Drivin' | mame-driver | Listed in `harddriv.cpp` header. The earlier standalone `metalmx.cpp` no longer exists in current MAME. |
| Cheese Chase | Art & Magic | 1993 | TMS34010 | — | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-driver | |
| Ultimate Tennis | Art & Magic | 1993 | TMS34010 | — | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-driver | |
| Stone Ball | Art & Magic | 1994 | TMS34010 | — | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-driver | |
| Shooting Star | Art & Magic | 1994 | TMS34010 | — | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-driver | |
| Lethal Justice | ICE / Game Room | 1996 | TMS34010 | — | `src/mame/ice/lethalj.cpp` | ICE | mame-driver | |
| Egg Venture | ICE / Game Room | 1997 | TMS34010 | — | `src/mame/ice/lethalj.cpp` | ICE | mame-driver | |
| Ripper Ribit | ICE / Game Room | 1997 | TMS34010 | — | `src/mame/ice/lethalj.cpp` | ICE | mame-driver | |
| Chicken Farm | ICE / Game Room | 1999 | TMS34010 | — | `src/mame/ice/lethalj.cpp` | ICE | mame-driver | |
| Crazzy Clownz | ICE / Game Room | 1999 | TMS34010 | — | `src/mame/ice/lethalj.cpp` | ICE | mame-driver | |
| Little Robin | TCH | 1994 | TMS34010 | — | `src/mame/tch/littlerb.cpp` | TCH | mame-driver | |
| AmeriDarts | Ameri Corporation | 1989 | TMS34010 | 40 (XTAL) | `src/mame/misc/coolpool.cpp` | Ameri Corp / Ameri Darts | mame-cpu | XTAL is 40 MHz; effective core clock per device divisor not yet noted here. |
| Cool Pool | Catalina Games | 1992 | TMS34010 | 40 (XTAL) | `src/mame/misc/coolpool.cpp` | Catalina | mame-cpu | |
| 9-Ball Shootout | E-Scape | 1993 | TMS34010 | 40 (XTAL) | `src/mame/misc/coolpool.cpp` | Catalina | mame-cpu | |
| F-15 Strike Eagle | MicroProse Games | 1991 | TMS34010 | 5 | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-driver | Listed in driver header; MicroProse arcade hardware (68000 + TMS34010 + i8051). |
| B.O.T.S.S.: Battle of the Solar System | MicroProse Games | 1992 | TMS34010 | 5 | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-driver | |
| Tank Battle | MicroProse Games | 1992 | TMS34010 | 5 | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-driver | |
| Super Tank Attack | MicroProse Games | 1992 | TMS34010 | 5 | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-driver | |
| Battletoads (Arcade) | Rare / Electronic Arts | 1994 | TMS34020 | — | `src/mame/rare/btoads.cpp` | Rare arcade | mame-cpu | Confirmed `TMS34020(config, m_maincpu, CPU_CLOCK / 2)` in driver. |

## Title-list mismatches noted while verifying

- The user-supplied list put **Terminator 2** in T-unit; MAME's `midyunit.cpp` header lists it under Y-unit. T2 was originally a Y-unit board; verified.
- **NBA Jam Tournament Edition** is in `midtunit.cpp`, not `midxunit.cpp`. Revolution X is the only title currently in the X-unit driver header.
- **Mortal Kombat** (original release) sits in `midyunit.cpp`; the T-unit `midtunit.cpp` includes a Mortal Kombat T-unit conversion as well.
- **Metal Maniax** is *not* in a separate `metalmx.cpp` anymore — that file no longer exists at the verified MAME commit. It is documented inside `harddriv.cpp`.
- The user list showed AmeriDarts and B.O.T.S.S. but did not pre-classify their drivers; both are now mapped to `coolpool.cpp` and `micro3d.cpp` respectively.

## Items still to verify or add

- Clock speeds — only the MicroProse arcade hardware (5 MHz) and the AmeriDarts/Cool Pool/9-Ball XTAL (40 MHz oscillator) are filled in. Remaining cells are blank pending a source-of-truth pass through each driver's `XTAL(...)` / `MAIN_OSC` / `set_clock(...)` lines.
- "B.O.T.S.S." vs. "Battle of the Solar System" — micro3d.cpp lists both; confirmed they are the same game.
- Any '34020-only systems beyond Battletoads and Metal Maniax — open question.
- Pinball boards (Williams DCS, Bally) using '34010 graphics — not yet enumerated here.
- Capcom CPS Changer / similar candidates — none expected; flag if found.
