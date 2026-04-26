# TMS34010_Info

An archive of original Texas Instruments documentation for the **TMS340 graphics processor family** (TMS34010 and TMS34020), intended as a corpus for AI-driven analysis. The TMS340 family is a line of 32-bit graphics-oriented CPUs from the late 1980s / early 1990s, used in arcade hardware (Mortal Kombat, NBA Jam, Smash TV, etc.), early PC graphics accelerators, and graphics workstations.

This repository started as **PDF source documents only**. It is now expanding into a broader preservation archive: documentation, original development tools, references to emulator source, hardware usage indexes, and related historical material. See `LEGAL_NOTES.md` before adding anything new.

## Archive structure

```
docs/
  ti-official/      original TI manuals (user's guides, board guides)
  ti-related/       TI-adjacent material (third-party guide, promo kits)
  third-party/      non-TI vendor docs
  articles/         historical articles, app notes
  patents/          US patents (full text)
  manuals/          manuals not yet classified
  datasheets/       chip-level datasheets ('34010, '34061, TLC34075/76, etc.)
tools/
  original-disks/   floppy/disk-image originals (e.g. TIGA SDK, GFX LBR)
  extracted/        unpacked tool archives
  compiler/         C compiler manuals + reference cards
  assembler/        assembler/linker manuals + reference cards
  debugger/         C source debugger
  tiga/             TIGA host API guides (+ promo-kit-scans/)
emulation/
  mame/             upstream pointer to MAME (UPSTREAM.md, pinned commit)
  mame-historical/
  mame4all-lineage/
  ghidra/           Ghidra/Sleigh '34010 work
  simulators/       other simulators / cycle-accurate models
  UPSTREAM_SDK.md   pin + dedupe of tms34010guy/tms34010-sdk
hardware/
  arcade/           arcade-board notes + ARCADE_USES.md (atari/midway/art-magic/ice/tch)
  pc-tiga/          TIGA PC graphics boards
  silicon-die/      community die-shots (tms34010, tms34020, tms34082) — CC BY-NC 3.0
  amiga/ mac/ workstation/ embedded-avionics/
software/
  examples/
  tiga-demos/
  graphics-library/
bibliography/
wanted/              missing-document tracker (also `WANTED.md` at root)
scripts/             download_sources.py, hash_manifest.py
incoming/            staging area; contents not for direct commit
```

Key indexes:

- `MANIFEST.csv` — every archived file with title, device, doc number, source URL, local path, SHA256, size, and redistribution status.
- `SOURCES.md` — known upstream URLs (bitsavers, TI live pages, GitHub mirrors, articles), whether or not the file is yet local.
- `WANTED.md` — documents and disks known to exist but not yet found.
- `LEGAL_NOTES.md` — preservation/research scope, classifications, what is **not** redistributed here.
- `hardware/arcade/ARCADE_USES.md` — arcade titles using the '34010 / '34020, with verified MAME driver paths and clock-source citations at a pinned MAME commit.
- `emulation/mame/UPSTREAM.md` — pinned MAME upstream commit, CPU-core file paths under `src/devices/cpu/tms34010/`, and the per-driver path index for every '34010/'34020-using driver. No upstream code is mirrored; this is a navigation index.
- `emulation/UPSTREAM_SDK.md` — catalog and dedupe of the `tms34010guy/tms34010-sdk` GitHub repo (pinned commit, file-by-file SHA256 dedupe; 34 of 74 files are byte-identical duplicates of bitsavers content already archived, 39 are novel — those are mirrored locally but flagged `do-not-redistribute` because the upstream has no LICENSE). The upstream README is mirrored at `emulation/tms34010-sdk-README.md`.

## Documents currently archived

### Silicon

#### TMS34010 / TMS34020 GPU

| File | TI doc # | Description |
| --- | --- | --- |
| `docs/datasheets/84292.pdf` | SPVS002C | **TMS34010 Graphics System Processor** datasheet (June 1986, revised June 1991). Pinout, electrical characteristics, register summary, instruction-set overview. **Primary** copy. |
| `docs/datasheets/SPVS002A_TMS34010_Graphics_System_Processor_198707.pdf` | SPVS002A | **TMS34010 Graphics System Processor** datasheet, **earlier revision** (Jan 1986 / Rev. July 1987). Sibling of SPVS002C; useful for tracking which characteristics were finalized later. |
| `docs/datasheets/SPVS002C_TMS34010_Graphics_System_Processor_199106_altscan.pdf` | SPVS002C | Same SPVS002C document as `84292.pdf` but a different scan/recompression. Kept for scan-quality comparison. |
| `docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` | SPVU001A | **TMS34010 User's Guide** (1988-08, revision A). The canonical architecture/instruction reference for the '34010. **Primary** copy. |
| `docs/ti-official/1986_SPVU001_TMS34010_Users_Guide_first_edition.pdf` | SPVU001 | **TMS34010 User's Guide first edition** (1986). Predates SPVU001A; the original first-silicon user manual. Use when comparing first-silicon vs. revised behavior. |
| `docs/ti-official/2564006-9721_TMS34020_Users_Guide_Aug90.pdf` | 2564006-9721 | **TMS34020 User's Guide** (August 1990). Full reference for the second-generation '34020 part — architecture, instruction set, I/O registers, host/local bus, video timing. The big one (~63 MB). |

#### Companion silicon (video controller, FPU)

| File | TI doc # | Description |
| --- | --- | --- |
| `docs/datasheets/SPPS010A_TMS34061_Video_System_Controller_198602.pdf` | SPPS010A | **TMS34061 Video System Controller** datasheet (February 1986). Pinout, electrical characteristics, register layout. The '34061 is the VRAM/CRTC controller often paired with a '34010 in the frame-buffer path. |
| `docs/ti-official/TMS34061_Users_Guide.pdf` | — | **TMS34061 User's Guide**. Full architecture/programming reference for the '34061; the deep counterpart to `SPPS010A`. |
| `docs/ti-official/TMS34082_Designers_Handbook_1991.pdf` | — | **TMS34082 Designer's Handbook** (1991). Programmer-level reference for the '34082 floating-point matrix-math coprocessor (the FPU sold alongside the '34020). Use this for engineering questions; reach for the '34082 patent (`docs/patents/US5025407.pdf`) only for IP-scope / claim-language context. |

### Tools (assembler / compiler / debugger / development boards)

| File | TI doc # | Description |
| --- | --- | --- |
| `tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf` | SPVU004 | **Assembly Language Tools User's Guide** — assembler, linker, archiver, COFF object format. |
| `tools/assembler/TMS34010_Assembly_Language_Tools_Reference_Card.pdf` | — | Quick-lookup reference card companion to SPVU004. |
| `tools/compiler/TMS34010_C_Compiler_Reference_Guide_1988.pdf` | SPVU002A | **TMS34010 C Compiler Reference Guide** (1988) — language extensions, runtime conventions, optimizer notes. **Primary** C-toolchain reference. |
| `tools/compiler/1986_TI_TMS34010_C_Compiler_Users_Guide.pdf` | — | **TMS34010 C Compiler User's Guide, 1986 edition** — earlier (pre-revision-A) compiler manual. Use when first-silicon / pre-1988 compiler behavior matters. |
| `tools/compiler/TMS34010_C_Compiler_Reference_Card.pdf` | SPVU005A | Quick-lookup reference card companion to the C compiler guide. |
| `tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf` | SPVU021A | **TMS340 Family C Source Debugger User's Guide** (Sept 1991) — TI's source-level debugger for the C toolchain. |
| `docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` | — | **TMS34010 Software Development Board User's Guide** (1987) — TI's PC-hosted '34010 dev/eval board. Long-form. |
| `docs/ti-official/TMS34010_SDB_Pocket_Reference.pdf` | — | Pocket reference card for the '34010 SDB. |
| `docs/ti-official/2558670-9761B_TMS34020_Software_Development_Board_Users_Guide_1991.pdf` | 2558670-9761B | **TMS34020 Software Development Board User's Guide** (1991) — companion dev board for the '34020 (a physically different board from the '34010 SDB). |

### Original tool disks

`tools/original-disks/` holds preservation copies of the original TI distribution media that shipped the toolchain — the '34010 Assembly Language Package (4 floppies, May 1985), the '34010 Sample Function Library (1987), the Simulator/C/ASM Tools master disk (1987), the Math/Graphics Function Library (1987), the GSP Paint demo (1987), the **1990-11 TMS340 Family SDK** set (TIGA SDK r2.01, GFX LBR r2.01 disks 1–3, C Source Debugger r5.00, Code Generation Tools r5.01 disks 1–2), the TIGA Interface User's Guide companion disk (1991-07-18, revB), the TIGA DDK rel 2.20, the TIGA Promo Kit demo + program disks (1991), and the TIGA Logo Bitmaps for Windows disk. Each disk has a sidecar JPEG of the floppy label where available. Disk-image formats are mixed (`.img`, `.DSK`, `.imd`, `.zip`); see `MANIFEST.csv` for sizes and provenance. Unpacked archives, where present, are under `tools/extracted/`.

### Graphics libraries / host APIs

| File | TI doc # | Description |
| --- | --- | --- |
| `software/graphics-library/spvu027.pdf` | SPVU027 | **TMS340 Graphics Library User's Guide** (August 1990) — the family-wide ('34010 + '34020) graphics primitives library shipped with the TI toolchain. **Primary** copy. |
| `software/graphics-library/TI_TMS340_Family_Graphics_Library.pdf` | SPVU027 | **Duplicate of `spvu027.pdf`** (byte-identical, SHA256 `b7cba156…`). Kept for now; flagged in `MANIFEST.csv` for removal. |
| `software/graphics-library/SPVU027_TMS340_Graphics_Library_199008_altscan.pdf` | SPVU027 | **Alternate scan** of SPVU027 (different SHA256 — *not* a byte-identical duplicate). Mirrored from the `tms34010-sdk` upstream; kept for scan-quality comparison. |
| `software/graphics-library/1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf` | — | **TMS34010 Math/Graphics Function Library User's Guide** (1987) — '34010-only predecessor of the family-wide SPVU027 library. |
| `software/graphics-library/TMS34010_Math_Graphics_Library_Reference_Card.pdf` | SPVU006 | Quick-lookup reference card for the math/graphics function library. |
| `tools/tiga/1989_TI_TIGA-340_Interface_Users_Guide.pdf` | — | **TIGA-340 Interface User's Guide** (1989) — earlier edition of the TIGA host-side API for PC graphics boards. |
| `tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf` | SPVU015C | **TIGA Interface User's Guide** (Sept 1990) — later, more complete revision of the same TIGA API. **Primary** TIGA reference. |
| `tools/tiga/SPVU018A_TIGA_Interface_Art_199009.pdf` | SPVU018A | **TIGA Interface Art** (Sept 1990) — TIGA's logo / iconography / branding-conventions companion document. **Not** another TIGA API edition. |
| `tools/tiga/promo-kit-scans/` | — | Unpacked imagery from the 1991 TIGA Promotional Kit (covers, table card, demo printout, logo art). |

### Ecosystem

| File | TI doc # | Description |
| --- | --- | --- |
| `docs/ti-related/1990-340-Family-THIRD-PARTY-GUIDE-4th-edition.pdf` | — | **TMS340 Family Third-Party Guide, 4th edition** (1990) — catalog of third-party hardware boards, software, and libraries available for the '340 family. Useful for historical context on the ecosystem. |
| `docs/ti-related/TIGA_Promo_Kit_Scans.zip` | — | Original TIGA Promotional Kit scans (zipped). The unpacked imagery is also available under `tools/tiga/promo-kit-scans/`. |

### Hardware (boards, photos, silicon)

| File | Description |
| --- | --- |
| `hardware/pc-tiga/TI_Color_Graphics_Controller_Board_Users_Guide_1986.pdf` | **TI Color Graphics Controller Board User's Guide** (1986) — TI's own '34010-based PC graphics card, the reference board behind the TIGA ecosystem. |
| `hardware/pc-tiga/34010_devbd.jpg`, `34020_devbd.jpg` | Photographs of TI's '34010 and '34020 development boards. |
| `hardware/silicon-die/tms34010/bercovici/` | TMS34010 die-shot (stitched MZ JPEG, ~3.7 MB at 1600px, original ~13k×11k from 42 sub-images) plus the rendered DokuWiki source pages from siliconpr0n.org. Photographer: Antoine Bercovici / SiliconInsider. **License: CC BY-NC 3.0** — attribution required, non-commercial. Captured 2007-06-08. |
| `hardware/silicon-die/tms34020/bercovici/` | TMS34020 die-shot (stitched MZ JPEG, ~2.0 MB at 1600px, original ~15k×14k from 75 sub-images) plus rendered DokuWiki source pages. Same author and license. Captured 2022-02-14. |
| `hardware/silicon-die/tms34082/bercovici/` | TMS34082B floating-point coprocessor die-shot (stitched MZ JPEG, ~3.7 MB) plus rendered DokuWiki source pages. Same author and license. |
| `hardware/silicon-die/_index/tag_vendor_ti/` | Snapshot of the siliconpr0n `vendor:ti` tag listing. Confirms only `bercovici:ti:tms34010`, `bercovici:ti:tms34020`, and `bercovici:ti:tms34082bopt` exist for the TMS340 family on that site. |
| `hardware/arcade/ARCADE_USES.md` | Index of arcade titles using the '34010 / '34020 — game / manufacturer / year / chip / clock / MAME driver / verification status. Each clock cites a line number in the upstream MAME `.cpp` at the pinned commit recorded in `emulation/mame/UPSTREAM.md`. |

### Articles, app notes, and historical material

| File | Description |
| --- | --- |
| `docs/articles/IEEE_Chasing_Pixels_TMS34010_and_VRAM.html` | Jon Peddie's **"Famous Graphics Chips: TI TMS34010 and VRAM"** column (IEEE / Computer Society). HTML mirror — **do-not-redistribute**, copyright held by IEEE/Computer Society; local file is for offline reference only. |
| `docs/articles/geekdot_tiga-programming.html` | Community writeup of TIGA's host-side programming model (geekdot.com). HTML mirror; author copyright. |
| `docs/articles/spra402.pdf` | TI Application Report SPRA402 (~6.6 MB). |
| `docs/articles/1992_Guttag_Interview_about_the_9918.pdf` | 1992 interview with Karl Guttag about the **TMS9918** (Guttag's earlier video display controller and a direct design lineage ancestor of the TMS34010 architecture work). Mirrored from kguttag.com; do-not-redistribute. |
| `docs/articles/34010_endlessskye_index.html` + `34010_endlessskye_mk3-*.jpg` | Capture of the **34010 Endless Skye** fan site (Karl Butz, content 2011–2015) including TMS34010-on-Mortal-Kombat-3 board photos (credit: Nicholas Caetano, Sept 2011). |
| `docs/articles/tms34020_uav_nl_avionics.html` + `tms34020_uav_nl_avionics_files/` | Eric Theunissen's article on **TMS34020 in avionics primary flight displays** (F-16 ADP, ISD second-generation displays). Word-exported HTML with image refs rewritten to a self-contained sidecar directory. Author copyright. |

### Emulation pointers (no upstream code mirrored)

| File | Description |
| --- | --- |
| `emulation/mame/UPSTREAM.md` | Pinned MAME upstream commit (`70725158…`), CPU-core file paths under `src/devices/cpu/tms34010/`, and the per-driver path index (Midway Y/T/X/Wolf-unit, Atari Hard Drivin' family + Metal Maniax, Art & Magic, ICE/Game Room, TCH, Coolpool/AmeriDarts, MicroProse Micro3D, Rare Battletoads). |
| `emulation/UPSTREAM_SDK.md` | Pinned `tms34010guy/tms34010-sdk` commit (`5692b477…`) with file-by-file SHA256 dedupe — 34 of 74 files are byte-identical to bitsavers material already archived; 39 are novel (mirrored locally with `do-not-redistribute` because the upstream has no LICENSE). |
| `emulation/tms34010-sdk-README.md` | Verbatim mirror of the `tms34010-sdk` upstream README (pinned). |

### Patents

| File | Patent # | Description |
| --- | --- | --- |
| `docs/patents/US4718024.pdf` | US 4,718,024 | **"Graphics Data Processing Apparatus for Graphic Image Operations Upon Data of Independently Selectable Pitch"** — Asal, Guttag, Novak / Texas Instruments. Filed Nov 5 1985, issued Jan 5 1988. **The foundational TMS340 architecture patent.** Fig. 2 shows the canonical TMS34010 block diagram (CPU + register files + instruction cache + memory interface + special graphics hardware + host interface + I/O regs + video display controller). Cross-references 13 sibling applications filed in late 1985 / early 1986 covering the rest of the '34010 architecture (color expand, transparent ops, X/Y coords, draw-and-advance, instruction set, variable field size memory access, etc.). |
| `docs/patents/US5333261.pdf` | US 5,333,261 | **"Graphics Processing Apparatus Having Instruction Which Operates Separately on X and Y Coordinates of Pixel Location Registers"** — Guttag, Asal, Tebbutt, Novak / TI. Filed May 7 1993, issued Jul 26 1994. Continuation of the original 1985 TMS340 family. Covers the '34010's XY-addressing mode at the instruction level. |
| `docs/patents/US5437011.pdf` | US 5,437,011 | **"Graphics Computer System, a Graphics System Arrangement, a Display System, a Graphics Processor and a Method of Processing Graphic Data"** — Guttag, Asal, Van Aken, Tebbutt, Novak / TI. Filed Feb 4 1994, issued Jul 25 1995. Continuation in the original 1985 TMS340 family at the system level. |
| `docs/patents/US4747081.pdf` | US 4,747,081 | **"Video Display System Using Memory with Parallel and Serial Access Employing Serial Shift Registers Selected by Column Address"** — Heilveil, Van Aken, Guttag, Redwine, Pinkham, Novak / TI. Filed Dec 30 1983, issued May 24 1988. **Foundational VRAM patent** — the dual-port memory architecture that the TMS340 family was designed to drive. |
| `docs/patents/US4663735.pdf` | US 4,663,735 | **"Random/Serial Access Mode Selection Circuit for a Video Memory System"** — Novak, Guttag / TI. Filed Dec 30 1983, issued May 5 1987. Companion to US 4,747,081; covers the access-mode selection circuitry. |
| `docs/patents/US5025407.pdf` | US 5,025,407 | **"Graphics Floating Point Coprocessor Having Matrix Capabilities"** — Gulley & Van Aken / TI. Filed Jul 28 1989, issued Jun 18 1991. Covers the **floating-point coprocessor companion** to the '340 graphics processor (the TMS34082-class FPU sold alongside the '34020), with matrix-math acceleration. **Note:** this is *not* the '34010 GPU itself — the graphics processor is shown as a separate block in Fig. 1. |
| `docs/patents/US5371517.pdf`, `US5465058.pdf`, `US5636335.pdf`, `US5696923.pdf`, `US5696924.pdf` | various | TMS340-family patents collected by bitsavers under the `patents/` subdirectory: video palette, output buffer Miller-effect circuit, and three later '340-family filings. Mirrored from bitsavers; redistribution status: public-domain (US patents). See `MANIFEST.csv` for individual notes. |

## Scripts

- `scripts/download_sources.py [--csv MANIFEST.csv] [--dry-run] [--review-only]` — idempotent fetcher. Default list pulls remaining bitsavers items into the appropriate archive folders; `--csv MANIFEST.csv` walks every row whose `redistribution_status` is not `reference-only`.
- `scripts/hash_manifest.py [--write]` — recompute SHA256 + size for every locally-present `local_path` row.

Both are stdlib-only Python 3.8+; no external deps.
