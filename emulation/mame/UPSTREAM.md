# MAME — upstream reference

This repository **does not** vendor or submodule MAME. We record the upstream URL, the commit hash we last verified, the relevant file paths, and a short note on what each driver covers. To pull the source locally, see "Adding MAME later as a submodule" in `SOURCES.md`.

## Upstream

- Repo: <https://github.com/mamedev/mame>
- License: BSD-3-Clause / MAME License (see `COPYING` and per-file headers in upstream); some components are GPL.
- Verified HEAD commit: `70725158b4e9d2e1230c0515faec754f9cee86a2` (master, fetched 2026-04-26)
- Default branch: `master`

## TMS34010 / TMS34020 CPU core

Path: `src/devices/cpu/tms34010/`

| File | Bytes (approx) | Role |
| --- | --- | --- |
| `tms34010.cpp` | ~53.8 KB | Core: device init, execute loop, interrupt handling |
| `tms34010.h` | ~41.6 KB | Public interface, register definitions, device class |
| `34010ops.h` / `34010ops.hxx` | ~7.2 / ~104.7 KB | Generic instruction implementations |
| `34010fld.hxx` | ~14.6 KB | Field move and other field-pixel ops |
| `34010gfx.hxx` | ~93.8 KB | Graphics opcodes (PIXBLT, FILL, LINE, etc.) |
| `34010tbl.hxx` | ~256.2 KB | Decode table (the giant generated dispatcher) |
| `34010dsm.cpp` / `34010dsm.h` | ~31.2 / ~2.0 KB | Disassembler |

The same core handles `TMS34010` and `TMS34020` variants via a feature flag — confirm in `tms34010.h` before assuming behavior parity.

## Drivers that use the '34010 / '34020

| Driver | Path | Bytes (approx) | What it covers |
| --- | --- | --- | --- |
| Midway Y-unit | `src/mame/midway/midyunit.cpp` | ~283.9 KB | NARC, Smash TV, Trog, Strike Force, High Impact Football, Super High Impact, Total Carnage, Mortal Kombat (Y-unit). Williams/Midway boards built around the TMS34010. |
| Midway T-unit | `src/mame/midway/midtunit.cpp` | ~137.7 KB | Mortal Kombat, MK II, NBA Jam (original), Judge Dredd prototype, Terminator 2: Judgment Day. |
| Midway X-unit | `src/mame/midway/midxunit.cpp` | ~47.3 KB | Revolution X, NBA Jam Tournament Edition. |
| Midway W-unit / Wolf-unit | `src/mame/midway/midwunit.cpp` | ~140.5 KB | Mortal Kombat 3, Ultimate Mortal Kombat 3, WWF WrestleMania, Open Ice, NBA Hangtime, NBA Maximum Hangtime, Rampage World Tour. |
| Atari Hard Drivin' family | `src/mame/atari/harddriv.cpp` | ~345.9 KB | Hard Drivin', Race Drivin', S.T.U.N. Runner, Steel Talons, Hard Drivin' Compact, Race Drivin' Compact, Hard Drivin's Airborne (prototype), **Metal Maniax (prototype)**. Note: in current MAME, `metalmx.cpp` no longer exists as a separate file — the Metal Maniax prototype is documented inside `harddriv.cpp`. |
| Atari Hard Drivin' helpers | `src/mame/atari/harddriv.h`, `harddriv_a.cpp`, `harddriv_m.cpp` | ~25.8 / ~12.9 / ~42.3 KB | Header + audio + machine support split. |
| Art & Magic | `src/mame/misc/artmagic.cpp` (+ `artmagic.h`, `artmagic_v.cpp`) | ~43.2 / ~3.2 / ~8.6 KB | Cheese Chase, Ultimate Tennis, Stone Ball, Shooting Star. |
| ICE / Game Room | `src/mame/ice/lethalj.cpp` | ~71.7 KB | Lethal Justice, Egg Venture, Ripper Ribit, Chicken Farm, Crazzy Clownz. |
| TCH / Little Robin | `src/mame/tch/littlerb.cpp` | (small) | Little Robin (TCH). |

Sizes were captured via the GitHub Contents API at the verified commit; numbers will drift as upstream changes.

## Notes

- "Metal Maniax" was previously in a standalone driver `src/mame/atari/metalmx.cpp`; that file no longer exists in the master branch as of `70725158b…`. It is now covered by comments and code paths inside `harddriv.cpp`. If pinning to a much older MAME commit, expect to find the standalone file.
- Battletoads Arcade (Rare) is not in any of the above; it lives in `src/mame/rare/btoads.cpp` and also drives a TMS34010. **Verify** before adding to the arcade index.
- AmeriDarts (Ameri Corp) — verify driver path before listing.
- F-15 Strike Eagle (MicroProse arcade) and B.O.T.S.S. — verify driver path; both candidates for the `embedded-avionics`-adjacent or `misc` MAME tree.
- For exact game/clone lists per driver, read the upstream file directly. The list above is a navigation index, not a manifest of every ROM set.

## How to vendor MAME locally (if/when approved)

```sh
git submodule add https://github.com/mamedev/mame emulation/mame/mame
git -C emulation/mame/mame checkout 70725158b4e9d2e1230c0515faec754f9cee86a2
git submodule update --init --recursive
```

Pinning to a specific commit (rather than tracking master) is recommended so research notes stay reproducible.
