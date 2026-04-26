# Wanted

Documents and software known (or strongly suspected) to exist but not yet archived in this repo. Add to this list rather than guessing — keep entries factual and specific. Move an item out once it lands in `MANIFEST.csv` with a real SHA256.

## TI documentation by literature number

| Pub no. | Title | Status |
| --- | --- | --- |
| SPVA007A | TMS34010 Applications Guide | not located |
| SPVU007 | TMS34010 Font Library User's Guide | not located |
| SPVU008 | TMS34010 XDS User's Guide | not located |
| SPVU010 | TMS34010 / 8514/A Adapter Interface Emulation User's Guide | not located |
| SPVU028 | TMS34020 XDS User's Guide | not located |
| SPPU016A | TMS34070 User's Guide | not located |
| SPVU029 | TMS340 Family Assembler Support for TMS34082 | not located |
| — | TMS34082 Software Tool Kit User's Guide | not located |
| — | TMS34082 3D graphics library disks/examples | not located |
| — | TIGA Promo Kit Desktop Artist Demopak — Demo Disk **(1 of 2)** r1.1 | gap — only disk 2/2 was in `tms34010guy/tms34010-sdk`; disk 1/2 of the Demo set is missing. |
| — | TIGA Promo Kit Desktop Artist Demopak — Program Disk **(2 of 2)** r1.1 | gap — only Program Disk 1/2 was in `tms34010guy/tms34010-sdk`; Program Disk 2/2 is missing. |

## Die shots (high-resolution originals)

- **TMS34010 / TMS34020 / TMS34082B** — Antoine Bercovici's Silicon Prawn pages expose only 1600px-wide rendered JPEGs (mirrored under `hardware/silicon-die/`). The detail-page metadata indicates original Kolor-stitched scans at 13385x11159 (TMS34010), 15523x14912 (TMS34020), and (TBD) for the TMS34082B that are not served by the wiki. The high-res originals would have to be sourced directly from Antoine Bercovici / SiliconInsider (https://siliconinsider.com/).
- **TMS34010 / TMS34020 die shots from any other decapper** (mcmaster:ti:tms34010 and mcmaster:ti:tms34020 do **not** exist on Silicon Prawn as of 2026-04-26). No die shots for TMS34061, TMS34070, TMS34012, or TMS34082 (non-B) are known.

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
