# Sources

Catalog of all known upstream locations for TMS340-family material. Files actually fetched into this repo are tracked in `MANIFEST.csv` with their SHA256s. Anything listed here without a manifest entry is a pointer for future work.

## Bitsavers — primary mirror

Base: <https://bitsavers.trailing-edge.com/components/ti/TMS340xx/>

Bitsavers is the most complete public mirror of TI '340-family documentation, including original disk images. Each file below has been seen in the directory listing as of 2026-04-26; sizes are bitsavers' reported sizes, not yet verified by SHA256 against our local copies.

### Manuals and datasheets (root)

- `1986_TI_TMS34010_C_Compiler_Users_Guide.pdf` (4.4 MB)
- `1987_TI_TMS34010_Assembly_Language_Tools_Users_Guide.pdf` (23 MB) — SPVU004
- `1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf` (9.9 MB)
- `1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` (11 MB) — already archived
- `1988_TI_TMS34010_Users_Guide.pdf` (32 MB) — primary '34010 architecture reference, NOT yet archived locally
- `1989_TI_TIGA-340_Interface_Users_Guide.pdf` (16 MB) — already archived
- `1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf` (1.3 MB) — SPVU021A
- `1992_SLAS054_TI_TLC34076_Video_Interface_Palette_Data_Manual.pdf` (3.8 MB) — SLAS054
- `2558670-9761B_TMS34020_Software_Development_Board_Users_Guide_1991.pdf` (10 MB)
- `2564006-9721_TMS34020_Users_Guide_Aug90.pdf` (60 MB) — already archived
- `SPPS010A_TMS34061_Video_System_Controller_198602.pdf` (1.7 MB) — SPPS010A
- `SPUV027_TMS340_Graphics_Library_199008.pdf` (2.2 MB) — SPVU027 (filename has typo "SPUV"); already archived as `spvu027.pdf`
- `SPVU015C_TIGA_Interface_Users_Guide_199009.pdf` (2.3 MB) — SPVU015C; already archived
- `TI_Color_Graphics_Controller_Board_Users_Guide_1986.pdf` (2.9 MB) — pre-TIGA TI color board
- `TLC34075-110FN.pdf` (285 KB) — RAMDAC datasheet
- `TLC34076.pdf` (394 KB)
- `TMS340_Compiler.zip` (4.7 MB)
- `TMS340_Compiler_unpacked.zip` (13 MB)
- `TMS34010_Assembly_Language_Tools_Reference_Card.pdf` (1.9 MB)
- `TMS34010_C_Compiler_Reference_Card.pdf` (298 KB)
- `TMS34010_C_Compiler_Reference_Guide_1988.pdf` (4.6 MB) — already archived
- `TMS34010_Math_Graphics_Library_Reference_Card.pdf` (1.1 MB)
- `TMS34010_SDB_Pocket_Reference.pdf` (1.1 MB)
- `TMS34061_Users_Guide.pdf` (19 MB)
- `TMS34082_Designers_Handbook_1991.pdf` (26 MB) — '34082 FPU companion
- `tms34010_asm_pkg_1987.zip` (2.6 MB)
- `34010_devbd.jpg` (640 KB) — TI '34010 dev board photo
- `34020_devbd.jpg` (1.2 MB)

### TIGA subdirectory

Base: <https://bitsavers.trailing-edge.com/components/ti/TMS340xx/TIGA/>

- `TIGA_DDK_Rel_2_20.imd` — original disk image of the TIGA Driver Development Kit
- `TIGA_DDK_Rel_2_20.jpg` — disk label scan
- `TIGA_Disk_Images.zip`
- `TIGA_Promo_Kit_Scans.zip`

### TMS340_Tools_199011 subdirectory

Base: <https://bitsavers.trailing-edge.com/components/ti/TMS340xx/TMS340_Tools_199011/>

Original TI floppy distribution from Nov 1990, both disk-image archives and label scans:

- `2564053-1641_TIGA_SDK_r2.01.zip` / `.jpg`
- `2564059-1641_GFX_LBR_r2.01_d1.zip` / `.jpg` (Graphics Library disk 1 of 3)
- `2564059-1642_GFX_LBR_r2.01_d2.zip` / `.jpg`
- `2564059-1643_GFX_LBR_r2.01_d3.zip` / `.jpg`
- `2564060-1641_C_SRC_DBGR_r5.00.zip` / `.jpg` (C Source Debugger v5.00)
- `2564062-1641_CODE_GEN_TOOLS_r5.01_d1.zip` / `.jpg` (Code Generation Tools disk 1 of 2)
- `2564062-1642_CODE_GEN_TOOLS_r5.01_d2.zip` / `.jpg`

### patents subdirectory

Base: <https://bitsavers.trailing-edge.com/components/ti/TMS340xx/patents/>

- `US5371517.pdf`
- `US5465058.pdf`
- `US5636335.pdf`
- `US5696923.pdf`
- `US5696924.pdf`

These are TI-assigned patents collected by bitsavers under the TMS340xx tree; titles/inventors not yet recorded — verify against `patents.google.com` after download.

### Foundational TMS340 / VRAM patents (NOT in bitsavers' patents subdirectory)

Pulled from Google Patents directly; bitsavers' patent folder happens to skip these older filings. All have been mirrored locally and are in `MANIFEST.csv`:

- `US4718024` (1985-11 / 1988-01) — Asal/Guttag/Novak — "Graphics Data Processing Apparatus for Graphic Image Operations Upon Data of Independently Selectable Pitch". The canonical foundational TMS340 architecture patent (Fig. 2 = '34010 block diagram).
- `US5333261` (1993 / 1994) — Guttag/Asal/Tebbutt/Novak — X/Y coordinate instruction (continuation in the original family).
- `US5437011` (1994 / 1995) — Guttag/Asal/Van Aken/Tebbutt/Novak — graphics computer system (continuation in the original family).
- `US4747081` (1983-12 / 1988-05) — Heilveil/Van Aken/Guttag/Redwine/Pinkham/Novak — Video DRAM with parallel + serial access.
- `US4663735` (1983-12 / 1987-05) — Novak/Guttag — Random/serial access mode selection for the same VRAM.

PDF source for each is `https://patentimages.storage.googleapis.com/...` (URLs recorded in `MANIFEST.csv`). US patents are public-domain works of the federal government, so `redistribution_status: public`.

## GitHub — community SDK mirror

- `https://github.com/tms34010guy/tms34010-sdk` — community-maintained mirror of TI '340 SDK material. **Cataloged in `emulation/UPSTREAM_SDK.md`** at pinned commit `5692b4773328f49010896b7c47ada4f96bea73f8` (fetched 2026-04-26). Of 74 files, 35 are byte-identical to existing manifest entries; 39 are genuinely novel (1987-era TMS34010 SDK floppy images, 1991 TIGA Promo Kit individual scans, an SPVU001 1986 first-edition User's Guide, an SPVS002A 1987 datasheet revision, the SPVU018A "TIGA Interface Art" doc, and three later TLC340xx datasheets). The upstream repo has **no LICENSE file**, so the novel files are recorded as metadata only and not mirrored locally.

## TI live product/lit URLs

- <https://www.ti.com/lit/gpn/sm34020a-s> — SM34020A military-spec '34020 product page
- <https://www.ti.com/lit/an/spra402/spra402.pdf> — SPRA402 application report (TMS340 family)
- TMS34010 / TMS34020 / TMS34061 / TMS34070 / TMS34082: TI's live product pages have been intermittently scrubbed; primary archive remains bitsavers. Check `ti.com/product/<part>` and `ti.com/lit/gpn/<part>-s` before falling back.

## Datasheet mirrors (reference-only)

- <https://www.alldatasheet.com/datasheet-pdf/pdf/82998/TI/TMS34010.html>
- <https://www.alldatasheet.com/datasheet-pdf/pdf/126656/TI/TMS34020.html>

These are reformatted scrapes; prefer bitsavers or TI direct.

## Emulator and decompilation projects

- MAME — <https://github.com/mamedev/mame>. License BSD-3 (mostly) and GPL where noted in individual files. The TMS34010 CPU core, drivers for arcade hardware that uses '34010 / '34020, and supporting infrastructure all live here. **Do not** clone as a submodule without explicit user confirmation; record upstream URL + commit hash + file paths in `emulation/mame/UPSTREAM.md`. Verified HEAD as of 2026-04-26: `70725158b4e9d2e1230c0515faec754f9cee86a2`.
- Drivers actually using TMS34010/TMS34020 in current MAME (cross-checked at the verified commit; see `hardware/arcade/ARCADE_USES.md`):
  - `src/mame/midway/midyunit.cpp` — Williams/Midway Y-unit (NARC, Smash TV, Trog, Terminator 2, Mortal Kombat orig., Total Carnage, etc.)
  - `src/mame/midway/midtunit.cpp` — T-unit (MK, MK II, NBA Jam, NBA Jam TE, Judge Dredd proto)
  - `src/mame/midway/midxunit.cpp` — X-unit (Revolution X)
  - `src/mame/midway/midwunit.cpp` — Wolf-unit (MK3, UMK3, NBA Hangtime, WrestleMania, Open Ice, Rampage WT)
  - `src/mame/atari/harddriv.cpp` (+ `harddriv.h`, `harddriv_a.cpp`, `harddriv_m.cpp`) — Hard Drivin' family
  - `src/mame/atari/metalmx.cpp` — Metal Maniax (proto, '34020), separate driver at the verified commit
  - `src/mame/misc/artmagic.cpp` — Cheese Chase, Ultimate Tennis, Stone Ball, Shooting Star
  - `src/mame/ice/lethalj.cpp` — Lethal Justice, Egg Venture, Ripper Ribit, Chicken Farm, Crazzy Clownz
  - `src/mame/tch/littlerb.cpp` — Little Robin
  - `src/mame/misc/coolpool.cpp` — AmeriDarts, Cool Pool, 9-Ball Shootout (TMS34010 main CPU)
  - `src/mame/misc/micro3d.cpp` — F-15 Strike Eagle, B.O.T.S.S., Tank Battle, Super Tank Attack (MicroProse arcade)
  - `src/mame/rare/btoads.cpp` — Battletoads Arcade (TMS34020)
- Ghidra TMS34010 processor support — <https://github.com/NationalSecurityAgency/ghidra/issues/3990> tracks community/Sleigh work for '34010 disassembly. Capture any referenced forks or attached `.sla` files.

## Articles / historical writeups

- <https://www.computer.org/publications/tech-news/chasing-pixels/Famous-Graphics-Chips-IBMs-professional-graphics-the-PGC-and-8514A/Famous-Graphics-Chips-TI-TMS34010-and-VRAM> — IEEE/Computer Society "Famous Graphics Chips" column on TMS34010 + VRAM.
- <https://kguttag.com/wp-content/uploads/2024/04/1992-Interview-about-the-9918.pdf> — Karl Guttag interview (1992); Guttag was a key TI graphics architect.
- <https://www.geekdot.com/tiga-programming/> — community writeup on TIGA programming model.
- <https://34010.endlessskye.com/> — community '34010 technical notes site.
- <https://siliconpr0n.org/archive/doku.php?id=bercovici:ti:tms34020> — die-shot archive for '34020. **Mirrored** to `hardware/silicon-die/tms34020/bercovici/` (rendered HTML page, detail page, and the 1600px JPEG; original stitch resolution 15523x14912 not exposed by the wiki).
- <https://siliconpr0n.org/archive/doku.php?id=bercovici:ti:tms34010> — die-shot archive for '34010. **Mirrored** to `hardware/silicon-die/tms34010/bercovici/` (rendered HTML, detail page, 1600px JPEG; original 13385x11159).
- <https://siliconpr0n.org/archive/doku.php?id=bercovici:ti:tms34082bopt> — die-shot archive for the TMS34082B FPU companion. **Mirrored** to `hardware/silicon-die/tms34082/bercovici/`. Discovered via the `tag:vendor_ti` listing (the only three TI-tagged TMS340-family die shots on Silicon Prawn). All three scans by Antoine Bercovici / SiliconInsider, license CC BY-NC 3.0.
- <https://siliconpr0n.org/archive/doku.php?id=mcmaster:ti:tms34010> and `mcmaster:ti:tms34020` do **not** exist on Silicon Prawn (HTML "This topic does not exist yet").
- <https://tms34020.uav.nl/> — Eric Theunissen, "Avionics and the TMS34020". **Mirrored** to `docs/articles/tms34020_uav_nl_avionics.html` plus 18 article images under `docs/articles/tms34020_uav_nl_avionics_files/`. Site was 502 on first attempt (logged in `wanted/download_failures.md`); reachable on retry 2026-04-26.

Other historically relevant articles to chase (not yet sourced):

- "The TMS34010: An Embedded Microprocessor" — IEEE Micro (Guttag et al.)
- "The Texas Instruments 34010 Graphics System Processor"
- "Taking the Wraps off the 34020"
- BYTE magazine coverage of the TMS34010 GSP
- "TMS34010 VRAM Karl Guttag"
- TIGA-board specific coverage of the '34020

## Adding MAME later as a submodule (optional)

If the user later approves a full MAME mirror as a submodule:

```
git submodule add https://github.com/mamedev/mame emulation/mame/mame
git -C emulation/mame/mame checkout <known-good-tag>
git submodule update --init --recursive
```

Until then, only `emulation/mame/UPSTREAM.md` (URL + commit hash + relevant paths) should live in the tree.
