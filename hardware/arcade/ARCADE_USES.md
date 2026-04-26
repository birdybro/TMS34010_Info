# Arcade uses of TMS34010 / TMS34020

Index of arcade machines whose graphics path is built around a TMS34010 or TMS34020. Driver paths are taken from MAME at the verified commit recorded in `emulation/mame/UPSTREAM.md` (`70725158b4e9d2e1230c0515faec754f9cee86a2`). Game/year strings come from each driver's top-of-file comments; trust them over generic web sources. The "verification" column says how each row was checked:

- `mame-driver` — title and year are listed in the indicated MAME `.cpp` file's header comment block.
- `mame-cpu` — additionally confirmed that the driver instantiates `TMS34010(...)` or `TMS34020(...)`.
- `unverified` — claim came from the original task list but has not been cross-checked yet.

Clock-speed citations point at the `.cpp` source file at the verified MAME commit; line numbers are anchored to that commit. Footnote markers `[^a]`, `[^b]`, ... appear in the "Clock" column and resolve at the bottom of this file.

| Title | Manufacturer | Year | Chip | Clock | MAME driver | Board | Verification | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NARC | Williams / Midway | 1989 | TMS34010 | 48 MHz [^a] | `src/mame/midway/midyunit.cpp` | Z-unit | mame-cpu | First Williams arcade title to use the GSP family. Z-unit `zunit()` machine config uses `FAST_MASTER_CLOCK`. |
| Trog | Midway | 1990 | TMS34010 | 40 MHz [^b] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | Driven via `yunit_cvsd_4bit_slow` (SLOW_MASTER_CLOCK). |
| Smash TV | Williams | 1990 | TMS34010 | 40 MHz [^b] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `yunit_cvsd_6bit_slow` (SLOW_MASTER_CLOCK). |
| Strike Force | Midway | 1991 | TMS34010 | 48 MHz [^c] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `yunit_cvsd_4bit_fast` overrides clock to FAST_MASTER_CLOCK at line 1357. |
| High Impact Football | Williams | 1991 | TMS34010 | 40 MHz [^b] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `yunit_cvsd_6bit_slow`. |
| Super High Impact | Midway | 1991 | TMS34010 | 40 MHz [^b] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `yunit_cvsd_6bit_slow`. |
| Terminator 2: Judgment Day | Midway | 1991 | TMS34010 | 50 MHz [^d] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `term2()` extends `yunit_adpcm_6bit_faster` (FASTER_MASTER_CLOCK at line 1393). Listed in midyunit.cpp top comment. |
| Mortal Kombat (original) | Midway | 1992 | TMS34010 | 48 MHz [^c] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `yunit_adpcm_6bit_fast` (FAST_MASTER_CLOCK override at line 1383). Original release was Y-unit. |
| Total Carnage | Midway | 1992 | TMS34010 | 48 MHz [^c] | `src/mame/midway/midyunit.cpp` | Y-unit | mame-cpu | `yunit_adpcm_6bit_fast`. |
| Mortal Kombat (T-unit) | Midway | 1992 | TMS34010 | 50 MHz [^e] | `src/mame/midway/midtunit.cpp` | T-unit | mame-cpu | T-unit reissue. `CPU_CLOCK = 50_MHz_XTAL`. |
| Mortal Kombat II | Midway | 1993 | TMS34010 | 50 MHz [^e] | `src/mame/midway/midtunit.cpp` | T-unit | mame-cpu | |
| NBA Jam | Midway | 1993 | TMS34010 | 50 MHz [^e] | `src/mame/midway/midtunit.cpp` | T-unit | mame-cpu | |
| NBA Jam Tournament Edition | Midway | 1994 | TMS34010 | 50 MHz [^e] | `src/mame/midway/midtunit.cpp` | T-unit | mame-cpu | Listed in midtunit.cpp top comment (not xunit). |
| Judge Dredd (prototype) | Midway | 1994 | TMS34010 | 50 MHz [^e] | `src/mame/midway/midtunit.cpp` | T-unit | mame-cpu | Prototype. |
| Revolution X | Midway | 1994 | TMS34020 | 40 MHz [^f] | `src/mame/midway/midxunit.cpp` | X-unit | mame-cpu | X-unit board uses TMS34020 (not '34010); board diagram in driver header confirms `TMS34020 - clock 40MHz`. |
| Mortal Kombat 3 | Midway | 1995 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | Wolf-unit `wunit()` instantiates `TMS34010 ... 50_MHz_XTAL`. |
| Ultimate Mortal Kombat 3 | Midway | 1995 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | |
| WWF WrestleMania | Midway | 1995 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | |
| 2 On 2 Open Ice Challenge | Midway | 1995 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | Sometimes referred to as "NHL 2-on-2 Open Ice Challenge"; MAME lists the title without "NHL". |
| NBA Hangtime | Midway | 1995 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | |
| NBA Maximum Hangtime | Midway | 1996 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | |
| Rampage World Tour | Midway | 1997 | TMS34010 | 50 MHz [^g] | `src/mame/midway/midwunit.cpp` | Wolf-unit | mame-cpu | |
| Hard Drivin' | Atari Games | 1989 | TMS34010 (GSP) + TMS34010 (MSP) | GSP 48 MHz [^h] / MSP 50 MHz [^i] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | First-gen polygon racer. Driver-board variant has GSP at HARDDRIV_GSP_CLOCK (48 MHz) and an optional MSP TMS34010 at XTAL(50'000'000). MSP also reused as "TMS34012" in the driver-header diagrams. |
| Hard Drivin' Compact | Atari Games | 1990 | TMS34010 (GSP) + TMS34010 (MSP) | GSP 48 MHz [^h] / MSP 50 MHz [^i] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | Multisync-MSP variant; both GSP and MSP present. |
| Race Drivin' | Atari Games | 1990 | TMS34010 (GSP) + TMS34010 (MSP) | GSP 48 MHz [^h] / MSP 50 MHz [^i] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | |
| Race Drivin' Compact | Atari Games | 1990 | TMS34010 (GSP only) | GSP 48 MHz [^h] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | Multisync-no-MSP variant per driver header (`multisync_nomsp`). |
| S.T.U.N. Runner | Atari Games | 1990 | TMS34010 (GSP only) | GSP 48 MHz [^h] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | Multisync-no-MSP variant per driver header (line ~123/128). |
| Steel Talons | Atari Games | 1991 | TMS34010 (GSP only) | GSP 48 MHz [^h] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | Multisync-no-MSP variant. |
| Hard Drivin's Airborne (prototype) | Atari Games | — | TMS34010 (GSP only) | GSP 48 MHz [^h] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | Multisync-II machine; year not given in driver header; prototype. |
| Street Drivin' (prototype) | Atari Games | — | TMS34010 (GSP only) | GSP 48 MHz [^h] | `src/mame/atari/harddriv.cpp` | Hard Drivin' | mame-cpu | Prototype mentioned in driver header. |
| BMX Heat (prototype) | Atari Games | — | TMS34010 | ? | `src/mame/atari/harddriv.cpp` (header only) | Hard Drivin' | mame-driver | **Mentioned in `harddriv.cpp:160` header text only** — there is no `GAME(...)` entry or machine config for BMX Heat at the verified MAME commit. Hardware is presumed to be a Hard Drivin' family board (so the GSP would track 48 MHz [^h]), but no concrete clock can be cited. |
| Police Trainer (Atari prototype) | Atari Games | — | TMS34010 | ? | `src/mame/atari/harddriv.cpp` (header only) | Hard Drivin' | mame-driver | **Mentioned in `harddriv.cpp:163` header text only** — no `GAME(...)` entry or machine config exists for it. Distinct from the production P&P Marketing / ICE "Police Trainer" arcade game. |
| Metal Maniax (prototype) | Atari Games | 1994 | TMS34020 | 40 MHz [^j] | `src/mame/atari/metalmx.cpp` | metalmx | mame-cpu | The `metalmx.cpp` driver still exists at the verified MAME commit (contradicting an earlier note). `TMS34020(config, m_gsp, 40'000'000); // Unverified` — MAME marks the clock as unverified upstream. |
| Cheese Chase | Art & Magic | 1993 | TMS34010 | 40 MHz [^k] | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-cpu | `MASTER_CLOCK_40MHz`. |
| Ultimate Tennis | Art & Magic | 1993 | TMS34010 | 40 MHz [^k] | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-cpu | |
| Stone Ball | Art & Magic | 1994 | TMS34010 | 40 MHz [^k] | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-cpu | |
| Shooting Star | Art & Magic | 1994 | TMS34010 | 40 MHz [^k] | `src/mame/misc/artmagic.cpp` | Art & Magic | mame-cpu | |
| Lethal Justice | ICE / Game Room | 1996 | TMS34010 | 40 MHz [^l] | `src/mame/ice/lethalj.cpp` | ICE | mame-cpu | Driver header notes the part is `TMS34010FNL-50` running on a 40 MHz crystal (clock input 20 MHz from the `40/2` divider on PLCC68); MAME instantiates the device at `40_MHz_XTAL`. |
| Egg Venture | ICE / Game Room | 1997 | TMS34010 | 40 MHz [^l] | `src/mame/ice/lethalj.cpp` | ICE | mame-cpu | |
| Ripper Ribit | ICE / Game Room | 1997 | TMS34010 | 40 MHz [^l] | `src/mame/ice/lethalj.cpp` | ICE | mame-cpu | |
| Chicken Farm | ICE / Game Room | 1999 | TMS34010 | 40 MHz [^l] | `src/mame/ice/lethalj.cpp` | ICE | mame-cpu | |
| Crazzy Clownz | ICE / Game Room | 1999 | TMS34010 | 40 MHz [^l] | `src/mame/ice/lethalj.cpp` | ICE | mame-cpu | |
| Little Robin | TCH | 1994 | TMS34010 | 40 MHz [^m] | `src/mame/tch/littlerb.cpp` | TCH | mame-cpu | TMS34010 lives on the `INDER_VIDEO` subdevice (`src/mame/shared/inder_vid.cpp`). MAME applies a 1.2x clock-scale workaround inside the driver (line 333) to compensate for an apparent timing-bug hack — the underlying part is still nominally 40 MHz. |
| AmeriDarts | Ameri Corporation | 1989 | TMS34010 | 40 MHz [^n] | `src/mame/misc/coolpool.cpp` | Ameri Corp / Ameri Darts | mame-cpu | `amerdart()` instantiates `TMS34010 ... XTAL(40'000'000)`. |
| Cool Pool | Catalina Games | 1992 | TMS34010 | 40 MHz [^o] | `src/mame/misc/coolpool.cpp` | Catalina | mame-cpu | `coolpool()` extends `_9ballsht()` which instantiates `TMS34010 ... XTAL(40'000'000)`. |
| 9-Ball Shootout | E-Scape | 1993 | TMS34010 | 40 MHz [^o] | `src/mame/misc/coolpool.cpp` | Catalina | mame-cpu | `_9ballsht()` instantiates `TMS34010 ... XTAL(40'000'000)`. Encrypted variant of the Cool Pool board. |
| F-15 Strike Eagle | MicroProse Games | 1991 | TMS34010 (VGB) | 40 MHz [^p] | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-cpu | TMS34010 here is the "VGB" (Video Generator Board) running at `40_MHz_XTAL`. The previously-recorded "5 MHz" was incorrect — that figure is the ADC0844 / sub-clock, not the GSP. |
| B.O.T.S.S.: Battle of the Solar System | MicroProse Games | 1992 | TMS34010 (VGB) | 40 MHz [^p] | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-cpu | |
| Tank Battle | MicroProse Games | 1992 | TMS34010 (VGB) | 40 MHz [^p] | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-cpu | |
| Super Tank Attack | MicroProse Games | 1992 | TMS34010 (VGB) | 40 MHz [^p] | `src/mame/misc/micro3d.cpp` | MicroProse arcade | mame-cpu | |
| Battletoads (Arcade) | Rare / Electronic Arts | 1994 | TMS34020 | 32 MHz [^q] | `src/mame/rare/btoads.cpp` | Rare arcade | mame-cpu | `CPU_CLOCK = XTAL(64'000'000)` divided by 2 → 32 MHz at the device. |

## Footnotes — clock-source citations

All paths are relative to the `mamedev/mame` repo at commit `70725158b4e9d2e1230c0515faec754f9cee86a2`.

[^a]: `src/mame/midway/midyunit.cpp:1239` defines `static constexpr XTAL FAST_MASTER_CLOCK = XTAL(48'000'000);` and line `1248` instantiates `TMS34010(config, m_maincpu, FAST_MASTER_CLOCK);` inside `midzunit_state::zunit(machine_config&)`. NARC is bound to `zunit` via `GAME(...)` macros at lines `3848`–`3853`.

[^b]: `src/mame/midway/midyunit.cpp:1238` defines `static constexpr XTAL SLOW_MASTER_CLOCK = XTAL(40'000'000);`. Line `1289` instantiates `TMS34010(config, m_maincpu, SLOW_MASTER_CLOCK);` inside `yunit_core(...)`. Trog/Smash TV/High Impact/Super High Impact bind via `yunit_cvsd_4bit_slow` and `yunit_cvsd_6bit_slow`, which invoke `yunit_core` without changing the clock.

[^c]: `src/mame/midway/midyunit.cpp` overrides the master clock for the "fast" Y-unit variants: `m_maincpu->set_clock(FAST_MASTER_CLOCK);` at line `1357` (`yunit_cvsd_4bit_fast` → Strike Force) and line `1383` (`yunit_adpcm_6bit_fast` → MK Y-unit, Total Carnage). `FAST_MASTER_CLOCK = XTAL(48'000'000)` (line 1239).

[^d]: `src/mame/midway/midyunit.cpp:1240` defines `static constexpr XTAL FASTER_MASTER_CLOCK = XTAL(50'000'000);`. Line `1393` calls `m_maincpu->set_clock(FASTER_MASTER_CLOCK);` inside `yunit_adpcm_6bit_faster`. T2 binds via `term2_state::term2(...)` which extends `yunit_adpcm_6bit_faster`.

[^e]: `src/mame/midway/midtunit.cpp:605` defines `constexpr XTAL CPU_CLOCK = 50_MHz_XTAL;` and line `612` instantiates `TMS34010(config, m_maincpu, CPU_CLOCK);` for all T-unit titles.

[^f]: `src/mame/midway/midxunit.cpp:657` instantiates `TMS34020(config, m_maincpu, 40_MHz_XTAL);`. Note the X-unit uses the second-generation TMS34020, not '34010 — confirmed by both the device class and the ASCII-art board diagram in the file header (line 33/59).

[^g]: `src/mame/midway/midwunit.cpp:630` instantiates `TMS34010(config, m_maincpu, 50_MHz_XTAL);` inside `wunit(...)`. The driver-header note at lines 82/87/88 also records "TMS34010 — input clock (pin5) 50.000MHz".

[^h]: `src/mame/atari/harddriv.h:39` defines `#define HARDDRIV_GSP_CLOCK XTAL(48'000'000)`. `harddriv.cpp:1483` instantiates `TMS34010(config, m_gsp, HARDDRIV_GSP_CLOCK);` inside `driver_nomsp(...)`. All Hard Drivin'-family games inherit from this base machine config.

[^i]: `src/mame/atari/harddriv.cpp:1525` (driver_msp) and line `1562` (multisync_msp) instantiate the optional MSP companion as `TMS34010(config, m_msp, XTAL(50'000'000));`. The MSP is sometimes labeled `TMS34012` in board photos and in the driver header (lines 118–156), but in MAME it is instantiated as a TMS34010-class device.

[^j]: `src/mame/atari/metalmx.cpp:738` instantiates `TMS34020(config, m_gsp, 40'000'000); // Unverified`. The clock is flagged as unverified by upstream MAME — keep the same caveat here.

[^k]: `src/mame/misc/artmagic.cpp:41` defines `#define MASTER_CLOCK_40MHz (XTAL(40'000'000))`. Line `813` instantiates `TMS34010(config, m_tms, MASTER_CLOCK_40MHz);`.

[^l]: `src/mame/ice/lethalj.cpp:1000` instantiates `TMS34010(config, m_maincpu, 40_MHz_XTAL);`. Driver-header notes (lines 48 and 60) record both '-40' and '-50' part variants on different PCBs; MAME standardizes on the 40 MHz crystal value.

[^m]: `src/mame/shared/inder_vid.cpp:100` instantiates `TMS34010(config, m_tms, XTAL(40'000'000));` for the INDER_VIDEO subdevice that Little Robin uses. `src/mame/tch/littlerb.cpp:333` then applies `m_indervid->subdevice<cpu_device>("tms")->set_clock_scale(1.2);` as a hack to compensate for what the driver author calls "a possible timing bug in the core" — the underlying device clock is 40 MHz before the scale factor.

[^n]: `src/mame/misc/coolpool.cpp:934` instantiates `TMS34010(config, m_maincpu, XTAL(40'000'000));` inside `amerdart_state::amerdart(machine_config&)`.

[^o]: `src/mame/misc/coolpool.cpp:975` instantiates `TMS34010(config, m_maincpu, XTAL(40'000'000));` inside `_9ballsht_state::_9ballsht(machine_config&)`. `coolpool_state::coolpool(machine_config&)` at line 1016 simply calls `_9ballsht(config);` and remaps memory; the clock is unchanged.

[^p]: `src/mame/misc/micro3d.cpp:317` instantiates `TMS34010(config, m_vgb, 40_MHz_XTAL);`. The "VGB" (Video Generator Board) is the TMS34010-driven graphics subsystem; the host CPU is a 68000 at 16 MHz and there is also an Am29000 ("Dr. Math") on a separate board.

[^q]: `src/mame/rare/btoads.cpp:921` defines `constexpr XTAL CPU_CLOCK = XTAL(64'000'000);` and line `925` instantiates `TMS34020(config, m_maincpu, CPU_CLOCK / 2);`, giving an effective device clock of `64 MHz / 2 = 32 MHz`.

## Title-list mismatches noted while verifying

- The user-supplied list put **Terminator 2** in T-unit; MAME's `midyunit.cpp` header lists it under Y-unit. T2 was originally a Y-unit board; verified.
- **NBA Jam Tournament Edition** is in `midtunit.cpp`, not `midxunit.cpp`. Revolution X is the only title currently in the X-unit driver header.
- **Mortal Kombat** (original release) sits in `midyunit.cpp`; the T-unit `midtunit.cpp` includes a Mortal Kombat T-unit conversion as well.
- **Metal Maniax** *does* still have a standalone `src/mame/atari/metalmx.cpp` driver in the master branch at the verified commit (contrary to an earlier note in this archive). The Hard Drivin' driver header mentions the title in its prose, but the working machine config lives in `metalmx.cpp` and uses TMS34020 at a clock MAME itself flags as `// Unverified`.
- **Revolution X** uses a TMS34020 (not '34010), per `midxunit.cpp:657`. The earlier "TMS34010" classification in this table has been corrected.
- **Hard Drivin' family**: the GSP runs at 48 MHz on every variant; some variants additionally instantiate an MSP TMS34010 at 50 MHz. The driver-board diagrams in `harddriv.cpp` lines 118–156 also reference a "TMS34012" alongside the MSP; in MAME both 'cause a TMS34010 to be instantiated (the '34012 is variant silicon documented externally — keep open as a research item).
- **MicroProse VGB clock corrected**: the previous table said 5 MHz; the actual TMS34010 ("VGB") clock is 40 MHz (`micro3d.cpp:317`). The 5 MHz figure most likely came from a different sub-device in the same machine config (e.g. `m_vgb->set_pixel_clock(40_MHz_XTAL / 8) = 5 MHz`).
- The user list showed AmeriDarts and B.O.T.S.S. but did not pre-classify their drivers; both are now mapped to `coolpool.cpp` and `micro3d.cpp` respectively.

## Items still to verify or add

- BMX Heat and "Police Trainer (Atari prototype)" sub-machine configs in `harddriv.cpp` were not isolated in this pass; both are tagged `?` clock pending a deeper read.
- "B.O.T.S.S." vs. "Battle of the Solar System" — micro3d.cpp lists both; confirmed they are the same game.
- Any '34020-only systems beyond Battletoads, Metal Maniax, and Revolution X — open question.
- Pinball boards (Williams DCS, Bally) using '34010 graphics — not yet enumerated here.
- Capcom CPS Changer / similar candidates — none expected; flag if found.
- MAME upstream marks the Metal Maniax TMS34020 clock as "Unverified". A real-hardware crystal photo or schematic would let us pin this down.
- The "TMS34012" parts shown in the Hard Drivin' header diagrams (alongside the GSP and MSP) deserve a separate datasheet hunt — '34012 is sometimes referred to as a customized '34010 variant.
