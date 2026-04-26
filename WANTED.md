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

## Notes

If you find any of the above, attach: source URL, date acquired, SHA256, and a short note on copyright/redistribution status before committing the binary. For items where redistribution is unclear, prefer to record a working URL and metadata in `MANIFEST.csv` rather than commit the binary.
