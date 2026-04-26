# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **document archive**, not a code project. It contains scanned/original PDFs of Texas Instruments documentation for the TMS340 graphics processor family (TMS34010 and TMS34020) and its surrounding toolchain. The stated purpose (`README.md`) is AI-driven analysis of these sources, and over time the scope has been broadened to: original tool disks, emulator/decompiler upstream pointers, hardware-usage indexes, and historical articles.

There is no build system, no tests, no linter, no application code. Do not invent commands. If asked to "run" or "build", clarify — there is nothing to run. The two scripts in `scripts/` (`download_sources.py`, `hash_manifest.py`) are stdlib-only Python and exist to maintain the archive, not to ship runnable software.

## Repo layout (high level)

- `docs/` — TI manuals, datasheets, articles, patents (`ti-official`, `ti-related`, `articles`, `patents`, `datasheets`, `manuals`, `third-party`).
- `tools/` — toolchain manuals + original disk images (`compiler`, `assembler`, `debugger`, `tiga`, `original-disks`, `extracted`).
- `software/` — graphics library, TIGA demos, examples.
- `hardware/` — usage of the '34010/'34020 silicon (`arcade/{atari,midway,art-magic,ice-game-room,tch}`, `pc-tiga`, `amiga`, `mac`, `workstation`, `embedded-avionics`).
- `emulation/` — upstream pointers to MAME and similar (no full clones by default).
- `bibliography/`, `wanted/`, `scripts/`, `incoming/`.

Indexes live at the repo root: `MANIFEST.csv`, `SOURCES.md`, `WANTED.md`, `LEGAL_NOTES.md`.

## Choosing the right document

When the user asks a question, the answer almost always lives in one of these PDFs. Pick by topic:

- **What a pin does, electrical timing, register bit layouts on the '34010** → `docs/datasheets/84292.pdf` (SPVS002C, the '34010 datasheet).
- **Anything '34020-specific** (the second-generation part has a wider instruction set, different host interface, etc.) → `docs/ti-official/2564006-9721_TMS34020_Users_Guide_Aug90.pdf`. Do **not** assume '34010 behavior carries over.
- **Instruction encodings, assembler directives, COFF, linker behavior** → `tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf`.
- **C language extensions, calling convention, runtime** → `tools/compiler/TMS34010_C_Compiler_Reference_Guide_1988.pdf`.
- **Graphics primitives shipped by TI (line draw, fill, blit wrappers, etc.)** → `software/graphics-library/spvu027.pdf` (SPVU027).
- **Host-side PC API for TIGA boards** → prefer `tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf` (newer/more complete) over `tools/tiga/1989_TI_TIGA-340_Interface_Users_Guide.pdf`. Consult the 1989 one only when comparing revisions.
- **Which third-party board / library existed for the '340 family** → `docs/ti-related/1990-340-Family-THIRD-PARTY-GUIDE-4th-edition.pdf`.
- **The TI-branded eval/dev board hardware** → `docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf`.
- **TMS34082 floating-point coprocessor / matrix-math claims and architecture** → `docs/patents/US5025407.pdf` (US Patent 5,025,407, Gulley & Van Aken, TI, 1991). This is a *patent*, not a datasheet — language is legal/claim-style, not engineering reference. Use for prior-art questions, IP scope, or to understand the FPU's design intent; don't quote it as if it were a programmer's reference.
- **Foundational '34010 GPU architecture (block diagram, raster ops, selectable pitch)** → `docs/patents/US4718024.pdf` (US 4,718,024, Asal/Guttag/Novak / TI, filed Nov 1985, issued Jan 1988). Fig. 2 shows the canonical TMS34010 block diagram. The same group filed 13 sibling applications in late 1985 / early 1986 covering the rest of the architecture; two of those issued as **US 5,333,261** (X/Y coordinate instruction; `docs/patents/US5333261.pdf`) and **US 5,437,011** (graphics computer system; `docs/patents/US5437011.pdf`). For prior-art / claim-scope questions about the '34010 itself, start here, not at US 5,025,407.
- **VRAM (the storage technology underneath the '34010)** → `docs/patents/US4747081.pdf` (US 4,747,081, Heilveil/Van Aken/Guttag/Redwine/Pinkham/Novak, filed 1983, issued 1988) and its companion `docs/patents/US4663735.pdf` (US 4,663,735, Novak/Guttag, same filing date, issued 1987). These are TI's foundational dual-port video DRAM patents; the TMS340 was designed to drive this memory.

## Known gotchas

- **`software/graphics-library/spvu027.pdf` and `software/graphics-library/TI_TMS340_Family_Graphics_Library.pdf` are byte-identical duplicates** (same SHA256 `b7cba156…`, MD5 `141d99f4…`). Read either, but cite `spvu027.pdf` since that filename matches the TI literature number. The duplicate is flagged in `MANIFEST.csv`; do not delete without explicit user approval.
- **'34010 vs '34020**: they share a family but the '34020 adds instructions and changes parts of the host interface. Always check which chip the user means before quoting register or opcode details.
- **Two TIGA editions exist** (1989 and SPVU015C/Sept 1990). When citing TIGA APIs, default to SPVU015C.
- **`docs/patents/US5025407.pdf` covers the FPU coprocessor, not the '34010 GPU.** The patent explicitly distinguishes "graphics processor" (separate block) from "floating-point coprocessor" (the claimed invention). If a user asks for "the TMS34010 patent" and points at this file, gently correct — this is the '34082-class FPU patent. The foundational '34010 architecture patent is **`docs/patents/US4718024.pdf`** (Asal/Guttag/Novak, filed Nov 1985, issued Jan 1988). See the Patents section in `README.md` for the full set.
- The PDFs are **large** (the '34020 guide is ~63 MB, third-party guide ~37 MB, assembly tools ~24 MB). Always pass a `pages` range to the Read tool — opening one without paging will fail or waste context. The TI literature numbers and dates above are confirmed from the title pages; trust them when planning which page range to fetch.

## Working in this repo

- Edits will most often be to `README.md`, this file, `MANIFEST.csv`, or markdown indexes (`SOURCES.md`, `WANTED.md`, hardware/arcade lists).
- New material lands under the directory layout above. Do not put new files in the repo root unless they are repo-wide indexes.
- If the user wants OCR'd text, indexes, or extracted notes from these PDFs, those are new artifacts — put them under a sibling like `bibliography/` or alongside the source PDF, and update `MANIFEST.csv` accordingly.
- Git history early on used one-PDF-per-commit messages like `Create <filename>.pdf`. Newer commits group changes by intent (structure, manifest, hardware index). Match the style of recent commits.
- When adding new files, run `python3 scripts/hash_manifest.py --write` to refresh SHA256/size, and add a row to `MANIFEST.csv` with at minimum: title, device, source_url, local_path, copyright_status, redistribution_status.
