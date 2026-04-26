# HDL Reimplementation Notes — TMS34010

A roadmap for designing a clean-room HDL implementation of the Texas Instruments TMS34010 Graphics System Processor, indexed against the documentation in this archive. **This is not a copy of the user's guide.** It is a reimplementer's working notebook: where to look, what to verify, what is load-bearing, and what is easy to get wrong.

## Scope

- **Target part: TMS34010.** First-generation device, 32-bit internal datapath, 16-bit external bus, bit-addressable memory, programmable display controller. The TMS34020 is a distinct second-generation device with a wider instruction set and a different host interface; '34020 differences are out of scope here except where noted in `12-system-coprocessor.md` and `16-open-questions.md`.
- **Compatibility goal: functional / programmer-visible.** Cycle-accurate timing parity with original silicon is **not** assumed; cycle behavior is documented where the source PDFs cover it but the MAME core (not silicon) is the practical golden reference for cycle effects (see `15-verification.md`).
- **Out of scope:** the '34082 floating-point coprocessor (companion chip, not internal); the '34061 video system controller (companion VRAM/CRTC chip — covered only as a system-context partner); the TIGA host-side software stack.

## How to use these notes

Each file in this folder targets one design block or design topic. The structure is roughly:

1. **Why this matters** — what HDL designers care about for this block.
2. **Source-of-truth in the archive** — which PDF (and where in it) is authoritative.
3. **Summary of the load-bearing facts** — schematic, not transcribed. Read the source for bit-level detail.
4. **Gotchas** — silent foot-guns, revision differences, things that look like one chip but aren't, things MAME models that the docs don't and vice versa.
5. **Cross-references** to other files here and to MAME (`emulation/mame/UPSTREAM.md`).

When a fact is critical, the file cites a specific PDF + chapter or section. **If you are about to write RTL based on a claim in these notes, open the cited PDF and verify.** Notes drift; user's guides do not.

## File index

| File | Topic |
| --- | --- |
| `00-README.md` | This file. Index, scope, methodology. |
| `01-architecture.md` | Top-level block diagram, datapath, internal vs. external buses. |
| `02-instruction-set.md` | Opcode classes, encoding shapes, addressing modes; pointer to authoritative encoding tables. |
| `03-registers.md` | A-file, B-file, status register, PC, SP, and the I/O register page. |
| `04-memory-fields-pixels.md` | Bit-addressable memory, variable field size (FE0/FE1), pixel sizes 1/2/4/8/16. |
| `05-graphics-operations.md` | PIXBLT (B / L / XY), FILL, LINE, raster ops, pixel processing, plane mask, transparency. |
| `06-xy-addressing.md` | Coord-to-linear, pitch, draw-and-advance, window-clipping registers (WSTART/WEND). |
| `07-memory-interface.md` | DRAM/VRAM bus, refresh, shift-register transfer cycles, multiplexed LAD. |
| `08-video-timing.md` | Programmable display controller — HESYNC/HEBLNK/HSBLNK/HTOTAL, vertical analogues, DPYCTL/DPYSTRT/DPYTAP/DPYINT. |
| `09-host-interface.md` | Host port — HSTCTL bits, HSTADRL/H, HSTDATA, message-passing semantics, host-CPU view. |
| `10-cache-pipeline-timing.md` | 256-byte instruction cache (segment / line organization), prefetch behavior, instruction-timing model. |
| `11-interrupts-reset.md` | Interrupt sources, vector layout, priority and masking; reset sequence and post-reset state. |
| `12-system-coprocessor.md` | Coprocessor / expansion bus to the '34082; pairing with the '34061 VSC and TLC340xx RAMDACs. |
| `13-pinout-electrical.md` | Package, pin function map, AC/DC characteristics, clocking. |
| `14-patent-landscape.md` | Foundational TI patents, claim summaries, clean-room implications (all expired by 2026). |
| `15-verification.md` | Verification strategy: MAME as golden reference, original tool disks for assembled test programs, '34061 datasheet for system-context tests. |
| `16-open-questions.md` | Items where the documentation is ambiguous or mute and verification against silicon (or MAME, or both) is required. |

## Source-document map (jump table)

For each topic, the **primary** source first, then secondary/cross-checks. Paths are relative to the repo root.

| Topic | Primary | Secondary / cross-check |
| --- | --- | --- |
| Architecture / instruction reference | `docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A) | `docs/ti-official/1986_SPVU001_TMS34010_Users_Guide_first_edition.pdf` for first-silicon diffs |
| Pinout / AC-DC / register summary | `docs/datasheets/84292.pdf` (SPVS002C, June 1991) | `docs/datasheets/SPVS002A_TMS34010_Graphics_System_Processor_198707.pdf` (earlier rev) |
| Instruction encodings (canonical) | `tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf` (SPVU004) | `docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A) appendices |
| Quick-lookup encoding | `tools/assembler/TMS34010_Assembly_Language_Tools_Reference_Card.pdf` | — |
| Graphics-library calls (semantics of HW ops in software form) | `software/graphics-library/spvu027.pdf` (SPVU027) | `software/graphics-library/1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf` (earlier '34010-only) |
| Software development board (system-level usage examples) | `docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` | `docs/ti-official/TMS34010_SDB_Pocket_Reference.pdf` |
| TI's own '34010 PC graphics card (reference system) | `hardware/pc-tiga/TI_Color_Graphics_Controller_Board_Users_Guide_1986.pdf` | Board photos in `hardware/pc-tiga/` |
| Companion VSC chip | `docs/ti-official/TMS34061_Users_Guide.pdf` + `docs/datasheets/SPPS010A_TMS34061_Video_System_Controller_198602.pdf` | — |
| Companion FPU | `docs/ti-official/TMS34082_Designers_Handbook_1991.pdf` | `docs/patents/US5025407.pdf` (claim-language only) |
| Patents (foundational / clean-room reference) | `docs/patents/US4718024.pdf` | `docs/patents/US5333261.pdf`, `US5437011.pdf`, `US4747081.pdf`, `US4663735.pdf` |
| Verification — golden-reference CPU core | `emulation/mame/UPSTREAM.md` → `src/devices/cpu/tms34010/` at the pinned commit | `hardware/arcade/ARCADE_USES.md` for real-world ROMs to drive against the model |

## Methodology notes

- The PDFs are the ground truth. MAME is a faithful but secondary model; trust silicon-relevant PDFs over MAME, but trust MAME's source over plain-text web claims when the PDFs are silent.
- Keep an eye on **revision drift**: SPVS002A (1987) → SPVS002C (1991), and SPVU001 (1986) → SPVU001A (1988). For first-silicon-correct behavior, cross-check the older revision; for production-silicon behavior, default to the newer.
- The '34010 was filed in late 1985 and shipped in 1986, with refinements through 1988. The user's guide and datasheet went through revisions tracking real silicon changes — register layouts in the early 1986 user's guide are not always the same as the 1988 revision-A. Document discrepancies in `16-open-questions.md`.
- All foundational patents on this architecture have **expired** as of 2026. They are useful as design-intent references and clean-room derivation aids, not as blocking IP.
