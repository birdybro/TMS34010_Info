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
  tiga/             TIGA host API guides
emulation/
  mame/             upstream pointers to MAME (no full clone by default)
  mame-historical/
  mame4all-lineage/
  ghidra/           Ghidra/Sleigh '34010 work
  simulators/       other simulators / cycle-accurate models
hardware/
  arcade/           arcade-board notes (atari/midway/art-magic/ice-game-room/tch)
  pc-tiga/          TIGA PC graphics boards
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
- `emulation/UPSTREAM_SDK.md` — catalog and dedupe of the `tms34010guy/tms34010-sdk` GitHub repo (pinned commit, file-by-file SHA256 dedupe; novel files are recorded as metadata only because the upstream has no LICENSE).

## Documents currently archived

### Silicon

| File | TI doc # | Description |
| --- | --- | --- |
| `docs/datasheets/84292.pdf` | SPVS002C | **TMS34010 Graphics System Processor** datasheet (June 1986, revised June 1991). Pinout, electrical characteristics, register summary, instruction-set overview. |
| `docs/ti-official/2564006-9721_TMS34020_Users_Guide_Aug90.pdf` | 2564006-9721 | **TMS34020 User's Guide** (August 1990). Full reference for the second-generation '34020 part — architecture, instruction set, I/O registers, host/local bus, video timing. The big one (~63 MB). |

### Tools (assembler / compiler / development board)

| File | TI doc # | Description |
| --- | --- | --- |
| `tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf` | SPVU004 | **Assembly Language Tools User's Guide** — assembler, linker, archiver, COFF object format. |
| `tools/compiler/TMS34010_C_Compiler_Reference_Guide_1988.pdf` | — | **TMS34010 C Compiler Reference Guide** (1988) — language extensions, runtime conventions, optimizer notes. |
| `docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` | — | **Software Development Board User's Guide** (1987) — TI's PC-hosted '34010 dev/eval board. |

### Graphics libraries / host APIs

| File | TI doc # | Description |
| --- | --- | --- |
| `software/graphics-library/spvu027.pdf` | SPVU027 | **TMS340 Graphics Library User's Guide** (August 1990) — graphics primitives library shipped with the TI toolchain. |
| `software/graphics-library/TI_TMS340_Family_Graphics_Library.pdf` | SPVU027 | **Duplicate of `spvu027.pdf`** (byte-identical, SHA256 `b7cba156…`). Kept for now; flagged in `MANIFEST.csv` for removal. |
| `tools/tiga/1989_TI_TIGA-340_Interface_Users_Guide.pdf` | — | **TIGA-340 Interface User's Guide** (1989) — earlier edition of the TIGA host-side API for PC graphics boards. |
| `tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf` | SPVU015C | **TIGA Interface User's Guide** (Sept 1990) — later, more complete revision of the same TIGA API. |

### Ecosystem

| File | TI doc # | Description |
| --- | --- | --- |
| `docs/ti-related/1990-340-Family-THIRD-PARTY-GUIDE-4th-edition.pdf` | — | **TMS340 Family Third-Party Guide, 4th edition** (1990) — catalog of third-party hardware boards, software, and libraries available for the '340 family. Useful for historical context on the ecosystem. |

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
