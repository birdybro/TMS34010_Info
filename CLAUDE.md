# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **document archive**, not a code project. It contains scanned/original PDFs of Texas Instruments documentation for the TMS340 graphics processor family (TMS34010 and TMS34020) and its surrounding toolchain. The stated purpose (`README.md`) is AI-driven analysis of these sources.

There is no build system, no tests, no linter, no application code. Do not invent commands. If asked to "run" or "build", clarify — there is nothing to run.

## Choosing the right document

When the user asks a question, the answer almost always lives in one of these PDFs. Pick by topic:

- **What a pin does, electrical timing, register bit layouts on the '34010** → `84292.pdf` (SPVS002C, the '34010 datasheet).
- **Anything '34020-specific** (the second-generation part has a wider instruction set, different host interface, etc.) → `2564006-9721_TMS34020_Users_Guide_Aug90.pdf`. Do **not** assume '34010 behavior carries over.
- **Instruction encodings, assembler directives, COFF, linker behavior** → `TMS34010_Assembly_Language_Tools_Users_Guide (SPVU004).pdf`.
- **C language extensions, calling convention, runtime** → `TMS34010_C_Compiler_Reference_Guide_1988.pdf`.
- **Graphics primitives shipped by TI (line draw, fill, blit wrappers, etc.)** → `spvu027.pdf` (SPVU027).
- **Host-side PC API for TIGA boards** → prefer `TIGA Interface Users Guide (SPVU015C) sept1990.pdf` (newer/more complete) over the 1989 edition. Consult the 1989 one only when comparing revisions.
- **Which third-party board / library existed for the '340 family** → `1990-340-Family-THIRD-PARTY-GUIDE-4th-edition.pdf`.
- **The TI-branded eval/dev board hardware** → `1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf`.

## Known gotchas

- **`spvu027.pdf` and `TI_TMS340_Family_Graphics_Library.pdf` are byte-identical duplicates** (same MD5). Read either, but cite `spvu027.pdf` since that filename matches the TI literature number.
- **'34010 vs '34020**: they share a family but the '34020 adds instructions and changes parts of the host interface. Always check which chip the user means before quoting register or opcode details.
- **Two TIGA editions exist** (1989 and SPVU015C/Sept 1990). When citing TIGA APIs, default to SPVU015C.
- The PDFs are **large** (the '34020 guide is ~63 MB, third-party guide ~37 MB, assembly tools ~24 MB). Always pass a `pages` range to the Read tool — opening one without paging will fail or waste context. The TI literature numbers and dates above are confirmed from the title pages; trust them when planning which page range to fetch.

## Working in this repo

- Edits will almost always be to `README.md` or this file, or to add new PDFs / extracted notes. There is no source tree to navigate.
- If the user wants OCR'd text, indexes, or extracted notes from these PDFs, those are new artifacts — ask where they should live (e.g., `notes/`, `extracted/`) before scattering files into the repo root.
- Git history so far is one PDF per commit with messages like `Create <filename>.pdf`. Match that style when adding more source documents.
