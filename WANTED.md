# Wanted

Documents and software known (or strongly suspected) to exist but not yet archived in this repo. Add to this list rather than guessing — keep entries factual and specific. Move an item out once it lands in `MANIFEST.csv` with a real SHA256.

## TI documentation by literature number

| Pub no. | Title | Status |
| --- | --- | --- |
| SPVA007A | TMS34010 Applications Guide | not located |
| SPVU001 (1st ed.) | TMS34010 User's Guide, 1986 first edition | seen-upstream-only (`tms34010guy/tms34010-sdk` Docs/, no license; see `emulation/UPSTREAM_SDK.md`) |
| SPVS002A | TMS34010 Graphics System Processor Production Data, 1987-07 | seen-upstream-only (`tms34010guy/tms34010-sdk` Docs/, no license) |
| SPVU007 | TMS34010 Font Library User's Guide | not located |
| SPVU008 | TMS34010 XDS User's Guide | not located |
| SPVU010 | TMS34010 / 8514/A Adapter Interface Emulation User's Guide | not located |
| SPVU018A | TIGA Interface Art (1990-09) | seen-upstream-only (`tms34010guy/tms34010-sdk` Docs/, no license) |
| SPVU028 | TMS34020 XDS User's Guide | not located |
| SPPU016A | TMS34070 User's Guide | not located |
| SPVU029 | TMS340 Family Assembler Support for TMS34082 | not located |
| XLAS056 | TLC34074 Video Interface DAC Production Data (1995-05) | seen-upstream-only |
| XLAS058 | TLC34075A Video Interface Palette Production Data (1995-05) | seen-upstream-only |
| XLAS076 | TLC34076 Video Interface Palette Production Data (1995-05) | seen-upstream-only |
| 1604811-1601..1604 | 1985 TMS34010 Assembly Language Package (4 disks) rev D | seen-upstream-only (`.img` floppies in `tms34010guy/tms34010-sdk`, no license) |
| 2547232-1601 | 1987 TMS34010 Sample Function Library Package | seen-upstream-only |
| — | 1987-11 TMS34010 Simulator + C Tools + ASM Tools (combined floppy) | seen-upstream-only |
| — | 1987-12 TMS34010 Graphics Math Function Library r1.0 | seen-upstream-only |
| — | 1987-12 TMS34010 GSP Paint demo program | seen-upstream-only |
| 2564001 | 1991 TIGA Interface User's Guide rev B disk | seen-upstream-only |
| — | TMS34082 Software Tool Kit User's Guide | not located |
| — | TMS34082 3D graphics library disks/examples | not located |

## Hardware schematics / board manuals

- TMS34010 board schematics (TI eval/dev board native KiCad / OrCAD or scanned)
- TMS34020 board schematics
- TIGA DDK manuals (text companions to `TIGA_DDK_Rel_2_20.imd` on bitsavers)
- TIGA example programs (source) beyond what is in the SDK disk images
- Vendor TIGA driver disks (per-board: Hercules, Number Nine, ELSA, EIZO, SPEA, etc.)
- Vendor TMS34010 / TMS34020 board manuals — see `hardware/` subdirectories for the per-vendor wishlist

## Historical articles

- "The TMS34010: An Embedded Microprocessor" — IEEE Micro, primary architecture paper (Guttag, Asal, et al.)
- "The Texas Instruments 34010 Graphics System Processor" — early product/architecture overview
- "Taking the Wraps off the 34020" — '34020 launch coverage
- BYTE magazine TMS34010 GSP cover/feature articles
- TIGA-board specific deep-dives on '34020 PC boards

## Software / disk images

- Vendor TIGA driver disks (per-board, see `hardware/pc-tiga/`)
- TMS34082 3D graphics library disks
- Original TI XDS host-side software (XDS/22, XDS/510 with '34010 support if any)

## Hardware clock-speed verifications

- **Metal Maniax (prototype)** — `src/mame/atari/metalmx.cpp:738` instantiates the TMS34020 at `40'000'000 // Unverified`. A real-hardware crystal photo or schematic from the prototype board would let us confirm or correct.
- **BMX Heat (prototype)** and **Police Trainer (Atari prototype)** — both are mentioned only in the `harddriv.cpp` header comment block (lines 160 and 163) and have no corresponding `GAME(...)` entry or machine config. Clock speeds therefore cannot be cited from current MAME source. A board scan or schematic would resolve them.
- **TMS34012 in Hard Drivin' family** — the `harddriv.cpp` driver-header diagrams (lines 118–156) describe a 50 MHz "TMS34012" alongside the 50 MHz MSP TMS34010. In MAME the part is instantiated as a TMS34010-class device. A '34012-specific datasheet would clarify how the variant differs from the '34010 (it is rumored to be a customized version).

## Notes

If you find any of the above, attach: source URL, date acquired, SHA256, and a short note on copyright/redistribution status before committing the binary. For items where redistribution is unclear, prefer to record a working URL and metadata in `MANIFEST.csv` rather than commit the binary.
