# tms34010-sdk — upstream SDK mirror

Upstream catalog for the `tms34010guy/tms34010-sdk` GitHub repository, a
community-curated mirror that gathers TMS34010 / TMS340-family SDK
material previously hosted on bitsavers, plus a handful of additional
scans and disk images not in the bitsavers TMS340xx tree.

## Upstream

- Repo: <https://github.com/tms34010guy/tms34010-sdk>
- Pinned commit: `5692b4773328f49010896b7c47ada4f96bea73f8` (default branch `main`, fetched 2026-04-26)
- License: **none stated** — the repo has no `LICENSE` file. GitHub's
  API returns `"license": null`. Per this archive's `LEGAL_NOTES.md`,
  files derived from this upstream are recorded with
  `redistribution_status: do-not-redistribute` until the upstream
  publishes an explicit license. They have, however, been **mirrored
  locally** because this archive is private and for personal
  preservation/research use; the `do-not-redistribute` flag is a
  forward-looking signal for any future decision to share publicly.
- Upstream README excerpt (verbatim): *"Most of this was previously
  hosted on bitsavers, but it was extremely hard to find and sort
  through. Spent some time renaming things, making it more SEO
  friendly and easier to find what you need. ... I believe if TI had
  access to this SDK, they would make it freely available, but they
  unfortunately have lost the archives."*
- The full upstream README is mirrored as
  `emulation/tms34010-sdk-README.md`.

## Methodology for this catalog

1. `git clone` of the pinned commit into a temp directory
   (`/tmp/tms34010-sdk`).
2. `sha256sum` of every file (74 files, ~486 MB on disk).
3. Diff against `MANIFEST.csv` SHA256 column.
4. Files matching an existing manifest entry are recorded below as
   "exact duplicate of bitsavers mirror, already in archive" and are
   **not** re-mirrored.
5. Novel files are mirrored locally and have new `MANIFEST.csv` rows
   pointing to both the local path and the upstream URL.

Re-verification on 2026-04-26 against pinned commit reproduced the
split: **34 byte-identical duplicates of bitsavers content, 39 novel
files plus the upstream README**, totalling 74 files. (The earlier
catalog reported 35/39; one entry — `Docs/SPVU027 TMS340 Graphics
Library (1990-08).pdf` — is in fact a *different SHA256* from the
local `software/graphics-library/spvu027.pdf` and is therefore an
alternate scan, not a duplicate.)

## Exact duplicates of files already archived

These 34 SDK files are byte-identical (same SHA256) to files already
in `MANIFEST.csv`. No re-commit; the manifest is the canonical record.

| SDK upstream path | SHA256 (truncated) | Already at |
| --- | --- | --- |
| `Docs/SPVU021A TMS340 Family C Source Debugger Users Guide (1991-09).pdf` | `0c57d3a1...` | `tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf` |
| `Docs/SPVU006 TMS34010 Math Graphics Function Library Reference Card (1987).pdf` | `0fc9b044...` | `software/graphics-library/TMS34010_Math_Graphics_Library_Reference_Card.pdf` |
| `Docs/Video Interfaces/SLAS054 TLC34076 Video Interface Palette Data Manual (1992).pdf` | `10b6181e...` | `docs/datasheets/1992_SLAS054_TI_TLC34076_Video_Interface_Palette_Data_Manual.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family C Source Debugger Disk r5.00 rev2564060-1641.jpg` | `1abacf1b...` | `tools/original-disks/2564060-1641_C_SRC_DBGR_r5.00.jpg` |
| `Docs/SPVU005A TMS34010 C Compiler Reference Card (1988-08).pdf` | `21cc7257...` | `tools/compiler/TMS34010_C_Compiler_Reference_Card.pdf` |
| `Docs/SPVU004A TMS34010 Assembly Language Tools Reference Card (1987).pdf` | `2a413a60...` | `tools/assembler/TMS34010_Assembly_Language_Tools_Reference_Card.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (2 of 3) r2.01 rev2564059-1641.jpg` | `2c210007...` | `tools/original-disks/2564059-1642_GFX_LBR_r2.01_d2.jpg` |
| `Docs/SPVU002A TMS34010 Software Development Board Users Guide (1987-05).pdf` | `31f048a2...` | `docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` |
| `Patents/US5371517.pdf` | `39500634...` | `docs/patents/US5371517.pdf` |
| `Patents/US5696924.pdf` | `3b8a24e3...` | `docs/patents/US5696924.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (2 of 2) r5.01 rev2564062-1641.jpg` | `3f921e86...` | `tools/original-disks/2564062-1642_CODE_GEN_TOOLS_r5.01_d2.jpg` |
| `Patents/US5465058.pdf` | `4c987e6e...` | `docs/patents/US5465058.pdf` |
| `Docs/SPVU002A TMS34010 Software Development Board Users Guide Pocket Reference (1987-05).pdf` | `530f71d5...` | `docs/ti-official/TMS34010_SDB_Pocket_Reference.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family C Source Debugger r5.00 rev2564060-1641.zip` | `61e99023...` | `tools/original-disks/2564060-1641_C_SRC_DBGR_r5.00.zip` |
| `1990-11 TMS340 Family SDK/1990-11-19 TIGA SDK r2.01 rev2564053-1641.zip` | `69cbc13f...` | `tools/original-disks/2564053-1641_TIGA_SDK_r2.01.zip` |
| `Docs/SPVU005 TMS34010 C Compiler Users Guide (1986-12).pdf` | `6e68ca63...` | `tools/compiler/1986_TI_TMS34010_C_Compiler_Users_Guide.pdf` |
| `Docs/SPVU015A TIGA 340 Interface Users Guide (1989).pdf` | `6f6ae74c...` | `tools/tiga/1989_TI_TIGA-340_Interface_Users_Guide.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (1 of 2) r5.01 rev2564062-1641.zip` | `71528248...` | `tools/original-disks/2564062-1641_CODE_GEN_TOOLS_r5.01_d1.zip` |
| `Patents/US5636335.pdf` | `879ece19...` | `docs/patents/US5636335.pdf` |
| `Docs/SPVU006 TMS34010 Math Graphics Function Library Users Guide (1987).pdf` | `9136edee...` | `software/graphics-library/1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (1 of 2) r5.01 rev2564062-1641.jpg` | `9c50829d...` | `tools/original-disks/2564062-1641_CODE_GEN_TOOLS_r5.01_d1.jpg` |
| `Docs/SPVU015C TIGA Interface Users Guide (1990-09).pdf` | `a8b1aec3...` | `tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (1 of 3) r2.01 rev2564059-1641.jpg` | `b0876633...` | `tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.jpg` |
| `Docs/SPVU005A TMS34010 C Compiler Reference Guide (1988-08).pdf` | `bf9a9b91...` | `tools/compiler/TMS34010_C_Compiler_Reference_Guide_1988.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (3 of 3) r2.01 rev2564059-1641.jpg` | `c4e0fe27...` | `tools/original-disks/2564059-1643_GFX_LBR_r2.01_d3.jpg` |
| `Docs/SPVU004A TMS34010 Assembly Language Tools Users Guide (1987).pdf` | `c67005f7...` | `tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (1 of 3) r2.01 rev2564059-1641.zip` | `c91987ea...` | `tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.zip` |
| `Docs/SPVU001A TMS34010 Users Guide (1988-08).pdf` | `e5f9f50c...` | `docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` |
| `Patents/US5696923.pdf` | `e6093ed5...` | `docs/patents/US5696923.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (3 of 3) r2.01 rev2564059-1641.zip` | `f12541eb...` | `tools/original-disks/2564059-1643_GFX_LBR_r2.01_d3.zip` |
| `Docs/TMS34010 Software Development Board.jpg` | `f1dfe367...` | `hardware/pc-tiga/34010_devbd.jpg` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (2 of 3) r2.01 rev2564059-1641.zip` | `fb005548...` | `tools/original-disks/2564059-1642_GFX_LBR_r2.01_d2.zip` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (2 of 2) r5.01 rev2564062-1641.zip` | `fb199f80...` | `tools/original-disks/2564062-1642_CODE_GEN_TOOLS_r5.01_d2.zip` |
| `1990-11 TMS340 Family SDK/1990-11-19 TIGA SDK r2.01 rev2564053-1641.jpg` | `fee56b1a...` | `tools/original-disks/2564053-1641_TIGA_SDK_r2.01.jpg` |

## Files novel vs. this archive — **mirrored locally**

These 39 files (plus the upstream README) exist in the SDK upstream
with no SHA256 match in `MANIFEST.csv`. They have been **copied into
this archive** at the local paths shown, and full rows have been added
to `MANIFEST.csv`. Every row carries
`redistribution_status: do-not-redistribute` because the upstream has
no LICENSE.

### 1987-era TMS34010 SDK (8 disk images + label scan)

Bitsavers' TMS340xx tree contains the *1990* SDK (as
`TMS340_Tools_199011/`) and the *TIGA DDK* disks but does **not**
contain these earlier 1985–1987 floppies.

| Upstream path | Local path | SHA256 |
| --- | --- | --- |
| `1987-05 TMS34010 SDK/1985-05-20 TMS34010 Assembly Language Package (1 of 4) ASM-LNK-ARCH revD 1604811-1601.img` | `tools/original-disks/1985-05-20 TMS34010 Assembly Language Package (1 of 4) ASM-LNK-ARCH revD 1604811-1601.img` | `3dd3fe2d...` |
| `1987-05 TMS34010 SDK/1985-05-20 TMS34010 Assembly Language Package (2 of 4) GSPSIM-COMP revD 1604811-1602.img` | `tools/original-disks/1985-05-20 TMS34010 Assembly Language Package (2 of 4) GSPSIM-COMP revD 1604811-1602.img` | `9ba15c34...` |
| `1987-05 TMS34010 SDK/1985-05-20 TMS34010 Assembly Language Package (3 of 4) GSPSIM-TIPC revD 1604811-1603.img` | `tools/original-disks/1985-05-20 TMS34010 Assembly Language Package (3 of 4) GSPSIM-TIPC revD 1604811-1603.img` | `bb0454ab...` |
| `1987-05 TMS34010 SDK/1985-05-20 TMS34010 Assembly Language Package (4 of 4) ROM-DEMO revD 1604811-1604.img` | `tools/original-disks/1985-05-20 TMS34010 Assembly Language Package (4 of 4) ROM-DEMO revD 1604811-1604.img` | `5fe40c36...` |
| `1987-05 TMS34010 SDK/1987-05-19 TMS34010 Sample Function Library Package rev2547232-1601.img` | `tools/original-disks/1987-05-19 TMS34010 Sample Function Library Package rev2547232-1601.img` | `e929970e...` |
| `1987-05 TMS34010 SDK/1987-11-06 TMS34010 Simulator-C Tools-ASM Tools.img` | `tools/original-disks/1987-11-06 TMS34010 Simulator-C Tools-ASM Tools.img` | `3b4d2633...` |
| `1987-05 TMS34010 SDK/1987-12-03 TMS34010 Graphics Math Function Library r1.0.img` | `tools/original-disks/1987-12-03 TMS34010 Graphics Math Function Library r1.0.img` | `e1390cc7...` |
| `1987-05 TMS34010 SDK/1987-12-04 TMS34010 GSP Paint.img` | `tools/original-disks/1987-12-04 TMS34010 GSP Paint.img` | `15b06650...` |
| `1987-05 TMS34010 SDK/TMS34010_GDK_floppy_labels.png` | `tools/original-disks/TMS34010_GDK_floppy_labels.png` | `e8fcc753...` |

### 1991-07 TIGA Promo Kit and Art Software (8 disks/labels + 14 scans)

Bitsavers has `TIGA_Promo_Kit_Scans.zip` (the marketing scans, already
mirrored as `docs/ti-related/TIGA_Promo_Kit_Scans.zip`); this upstream
additionally exposes the individual demo disks as `.DSK` images and a
per-image set of higher-resolution promo scans not in the bitsavers
ZIP. A future cleanup may compare contents and decide which to keep
canonical.

| Upstream path | Local path | SHA256 |
| --- | --- | --- |
| `1991-07 TIGA Promo Kit and Art Software/Disks/1991-07-18 TIGA Interface Users Guide revB r2564001.DSK` | `tools/original-disks/1991-07-18 TIGA Interface Users Guide revB r2564001.DSK` | `87985d1d...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/1991-07-18 TIGA Interface Users Guide revB r2564001.jpg` | `tools/original-disks/1991-07-18 TIGA Interface Users Guide revB r2564001.jpg` | `195728d4...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Demo Disk (2 of 2) r1.1.DSK` | `tools/original-disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Demo Disk (2 of 2) r1.1.DSK` | `109c2811...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Demo Disk (2 of 2) r1.1.jpg` | `tools/original-disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Demo Disk (2 of 2) r1.1.jpg` | `82be2c14...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Program Disk (1 of 2) r1.1.DSK` | `tools/original-disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Program Disk (1 of 2) r1.1.DSK` | `3868d16c...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Program Disk (1 of 2) r1.1.jpg` | `tools/original-disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Program Disk (1 of 2) r1.1.jpg` | `58269d1c...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/TIGA Logo Bitmaps for Windows.DSK` | `tools/original-disks/TIGA Logo Bitmaps for Windows.DSK` | `83eafb9e...` |
| `1991-07 TIGA Promo Kit and Art Software/Disks/TIGA Logo Bitmaps for Windows.jpg` | `tools/original-disks/TIGA Logo Bitmaps for Windows.jpg` | `dff4aeb8...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Front Cover.jpg` | `tools/tiga/promo-kit-scans/Front Cover.jpg` | `bd60742f...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Back Cover.jpg` | `tools/tiga/promo-kit-scans/Back Cover.jpg` | `1ffb30ae...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Spine.jpg` | `tools/tiga/promo-kit-scans/Spine.jpg` | `f919654a...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Disk Sleeve (Front).jpg` | `tools/tiga/promo-kit-scans/Disk Sleeve (Front).jpg` | `18ff0943...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Disk Sleeve (Rear).jpg` | `tools/tiga/promo-kit-scans/Disk Sleeve (Rear).jpg` | `73452582...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Table Card.jpg` | `tools/tiga/promo-kit-scans/Table Card.jpg` | `cba50571...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/TIGA Logo (Large).jpg` | `tools/tiga/promo-kit-scans/TIGA Logo (Large).jpg` | `bddb9ee2...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/TIGA Demo Printout.jpg` | `tools/tiga/promo-kit-scans/TIGA Demo Printout.jpg` | `f0213cd8...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Chip Promo Picture.jpg` | `tools/tiga/promo-kit-scans/Chip Promo Picture.jpg` | `63b3d8f5...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/BYTE Award Stickers (Big).jpg` | `tools/tiga/promo-kit-scans/BYTE Award Stickers (Big).jpg` | `b2531fdd...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/BYTE Award Stickers (Small).jpg` | `tools/tiga/promo-kit-scans/BYTE Award Stickers (Small).jpg` | `046d3b5f...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/Promotional Kit Pages.pdf` | `tools/tiga/promo-kit-scans/Promotional Kit Pages.pdf` | `cd072d23...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/img354.jpg` | `tools/tiga/promo-kit-scans/img354.jpg` | `b039e85d...` |
| `1991-07 TIGA Promo Kit and Art Software/Scans/img355.jpg` | `tools/tiga/promo-kit-scans/img355.jpg` | `99d97561...` |

### Docs/ — additional manuals and datasheet revisions

| Upstream path | Local path | SHA256 |
| --- | --- | --- |
| `Docs/SPVU001 TMS34010 Users Guide (1986).pdf` | `docs/ti-official/1986_SPVU001_TMS34010_Users_Guide_first_edition.pdf` | `55e7f28a...` |
| `Docs/SPVS002A TMS34010 Graphics System Processor Production Data (1987-07).pdf` | `docs/datasheets/SPVS002A_TMS34010_Graphics_System_Processor_198707.pdf` | `d208783b...` |
| `Docs/SPVS002C TMS34010 Graphics System Processor Production Data (1991-06).pdf` | `docs/datasheets/SPVS002C_TMS34010_Graphics_System_Processor_199106_altscan.pdf` | `93dd8f0d...` |
| `Docs/SPVU018A Tiga Interface Art (1990-09).pdf` | `tools/tiga/SPVU018A_TIGA_Interface_Art_199009.pdf` | `788421e3...` |
| `Docs/SPVU027 TMS340 Graphics Library (1990-08).pdf` | `software/graphics-library/SPVU027_TMS340_Graphics_Library_199008_altscan.pdf` | `7e17b069...` |

`SPVU001` (1986 first edition) is genuinely novel — the archive
already had the 1988 SPVU001A revision but not the first edition.

`SPVS002A` (1987-07) is an earlier datasheet revision than the
SPVS002C (1991-06) already at `docs/datasheets/84292.pdf`; both are
now archived.

`SPVS002C` and `SPVU027` from the upstream are independent
rescans/recompressions of documents already archived. They are kept
under `_altscan` suffixes for future scan-quality comparison rather
than displacing the existing copies.

`SPVU018A TIGA Interface Art` (Sept 1990, pub no. 2564002-9721A)
covers TIGA logo/iconography conventions and was not previously in
the archive.

### Docs/Video Interfaces/ — TLC340xx datasheets (1995 production data)

These are RAMDAC / video palette companion chips intended to pair with
TMS34010/TMS34020 graphics processors.

| Upstream path | Local path | SHA256 |
| --- | --- | --- |
| `Docs/Video Interfaces/XLAS056 TLC34074 Video Interface DAC Production Data (1995-05).pdf` | `docs/datasheets/XLAS056_TLC34074_Video_Interface_DAC_199505.pdf` | `01721d77...` |
| `Docs/Video Interfaces/XLAS058 TLC34075A Video Interface Palette Production Data (1995-05).pdf` | `docs/datasheets/XLAS058_TLC34075A_Video_Interface_Palette_199505.pdf` | `f0814501...` |
| `Docs/Video Interfaces/XLAS076 TLC34076 Video Interface Palette Production Data (1995-05).pdf` | `docs/datasheets/XLAS076_TLC34076_Video_Interface_Palette_199505.pdf` | `386fbe38...` |

### Repository metadata

| Upstream path | Local path | SHA256 |
| --- | --- | --- |
| `README.md` | `emulation/tms34010-sdk-README.md` | `f5d35e05...` |

The upstream README is mirrored under a clarifying name to avoid
suggesting it is a top-level README of this archive.

## Recommended next actions

1. **Compare scan quality between the upstream rescans and the
   existing archive copies** for SPVS002C (`84292.pdf` vs.
   `SPVS002C_..._altscan.pdf`) and SPVU027 (`spvu027.pdf` vs.
   `SPVU027_..._altscan.pdf`); keep whichever scan is cleaner as the
   primary, demote the other.
2. **Cross-check `bitsavers.../TIGA/TIGA_Promo_Kit_Scans.zip` against
   `tools/tiga/promo-kit-scans/`.** Likely overlap; if the upstream
   set is a strict superset, the bitsavers ZIP can be retired in
   favour of the higher-resolution individual files.
3. **Compare SPVU001 (1986 first edition) to SPVU001A (1988 revision)**
   to see what changed between the first-silicon manual and the second
   public revision.
4. If the user wants to vendor the SDK as a submodule (analogous to
   the proposed MAME submodule scheme), pin to commit
   `5692b4773328f49010896b7c47ada4f96bea73f8`.
