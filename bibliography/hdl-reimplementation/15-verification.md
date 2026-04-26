# 15 — Verification strategy

## Why this matters

You will not find every bug by reading SPVU001A and writing tests against your interpretation of it. The chip has 35 years of working software behind it; that software is the practical correctness contract. **The verification strategy is built around running real software against your model and comparing against MAME** — and, where possible, the original tool disks and arcade ROMs.

## Source-of-truth (for verification, as opposed to design)

- **MAME `tms34010` core** — the practical golden reference. Functionally close to silicon, well-tested against thousands of arcade games. Path index: `emulation/mame/UPSTREAM.md`. Files: `tms34010.cpp`, `34010ops.hxx`, `34010gfx.hxx`, `34010fld.hxx`, `34010tbl.hxx`, `34010dsm.cpp`.
- **Arcade ROMs that exercise the chip in different ways** — `hardware/arcade/ARCADE_USES.md`. Each row maps a real-world ROM to the MAME driver that runs it.
- **Original tool disks** under `tools/original-disks/` — TI-shipped assembler test programs, simulator inputs, GFX library samples. These are the closest thing to TI's own validation suite that survives publicly.
- **TI graphics library** (`software/graphics-library/spvu027.pdf` + the 1987 predecessor) — documents the function-level behavior that the hardware should support.
- **C source debugger** (`tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf`) — exercises the host-port debug protocol deeply.

## Verification phases

A pragmatic ordering:

### Phase 0: Unit tests on the field engine

The field engine (`04-memory-fields-pixels.md`) is the foundation. Build a stand-alone testbench with a known memory image and exhaustively test:

- Read field of size N at bit address A, for N ∈ {1, 8, 16, 24, 32}, A ∈ {0, 1, 7, 15, 16, 17, 31, 32, ...}.
- Sign-extend and zero-extend variants.
- Write field of size N at bit address A, RMW-correct.
- Pre-decrement / post-increment by N bits.

When this passes for every (N, A) combination, you have a foundation that everything else can ride on.

### Phase 1: Single-instruction tests

Hand-craft very short test programs (1–10 instructions each) that target:

- Each ALU op with immediate, register, and memory operands.
- Each move/load/store form.
- Each shift / rotate.
- Each control-flow form (JR, JRcc, CALL, RET).
- Each addressing mode (direct, indirect, indirect+disp, predec, postinc, absolute, PC-rel).
- Each field-mode access (FE0 vs FE1).

Run each test on:

- Your model.
- MAME (using its `34010` instance in a minimal harness).

Diff the post-instruction register/memory state. They should match exactly for almost everything; document any divergence as a candidate bug in either model.

### Phase 2: Pixel ops in isolation

Build minimal test cases for:

- `PIXT` in all three forms × all PSIZEs × all PPOPs × {transparency on/off} × {plane mask all/some/none}.
- `FILL L` with a known DYDX, COLOR1, raster op.
- `FILL XY` with the same plus a clip window.
- `PIXBLT L` with a known source/dest layout.
- `PIXBLT XY` with the same plus clip.
- `PIXBLT B` with a small font glyph as source.
- `LINE` with horizontal, vertical, and diagonal endpoints.

Run on model + MAME. Compare framebuffer output bit-for-bit. **The framebuffer comparison is your most powerful regression tool.**

### Phase 3: Real software — TI-shipped

Pick a small TI-shipped sample from the original disks (`tools/original-disks/` and `tools/extracted/`). Examples:

- 1987-12-04 GSP Paint — exercises full TIGA-style display + pixel ops.
- 1987-12-03 TMS34010 Graphics Math Function Library r1.0 — math + drawing primitives.
- 1985-05-20 TMS34010 Assembly Language Package, disk 4 (ROM-DEMO) — small canned demos.

These need a way to load disk images into memory and to run the resulting binary. The simulator-on-PC programs ship with their own loader; you can sidestep that by extracting the binary from the disk image and loading it at the documented entry point.

Run on model + MAME side-by-side. Compare:

- Framebuffer at end of frame.
- Final register state.
- Memory contents in any documented region.

Differences point at either a model bug or a MAME bug. MAME is well-tested but not perfect; if you suspect MAME, check upstream issues / commits since the pinned commit.

### Phase 4: Arcade ROMs

This is the most realistic stress test. Pick a ROM from `hardware/arcade/ARCADE_USES.md` based on what corners of the chip you want to stress:

- **Mortal Kombat (T-unit, midtunit.cpp)** — heavy PIXBLT B for sprite blitting, heavy plane masking, transparency.
- **Smash TV (Y-unit, midyunit.cpp)** — many simultaneous moving sprites, exercises pipeline + interrupt latency.
- **NBA Jam (T-unit)** — large sprites with palette tricks, exercises PIXBLT + RAMDAC interaction.
- **Lethal Justice (ICE)** — TMS34010-50 part, '40 MHz crystal with `40/2` divider — different clocking; exercises CRTC at a different rate.
- **Hard Drivin' (Atari, harddriv.cpp)** — dual-CPU with both GSP and MSP TMS34010s; exercises host-port arbitration.

Replace MAME's '34010 core with your model (this requires implementing the MAME device interface for your model, which is its own effort — the BSD license makes this legal and a smaller initial integration path than full standalone validation).

### Phase 5: Hardware bring-up (if applicable)

If the goal is real silicon or an FPGA on a real board:

- Bring up against the C source debugger over the host port (`tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf`). The debugger's host-port protocol is well-defined and a good early test.
- Run TI-shipped tools that came on the original SDK disks (assembler, linker, simulator) — these are not the targets of your reimplementation but the *outputs* they generate (binaries) are what you want to run against.
- Run the GFX library sample programs as the next step.
- Then move to arcade ROMs.

## What MAME models well

- Functional instruction execution.
- PIXBLT / FILL / LINE semantics (excellent coverage; many years of arcade-ROM regression).
- Display-controller register effects on visible output.
- Host-port message passing (where games use it).
- Interrupt sources and priority.

## What MAME does not model accurately

- **Cycle-level timing.** MAME approximates per-instruction cycle counts but is not strictly cycle-accurate against silicon.
- **AC characteristics at the pin level.** MAME is functional, not electrical.
- **First-silicon vs. revision-A differences.** MAME models a single representative behavior.
- **'34010 vs. silicon variants ('34012, '-50 vs '-40 speed grades).** MAME treats these as one device.
- **Cache fill/miss timing detail.** Functionally a hit/miss is modeled, but the exact cycle penalty is approximated.

For these, fall back to the datasheet (SPVS002C / SPVS002A) and to first-principles modeling.

## What to do when model and MAME disagree

1. **Read the relevant SPVU001A chapter.** The user's guide is the design contract; if the spec is unambiguous and you match it and MAME doesn't, file a MAME bug (and note the divergence in `16-open-questions.md`).
2. **If SPVU001A is silent or ambiguous,** look at the patents. Sometimes the design intent is clearer there.
3. **If both are silent,** trust MAME — it represents 25+ years of testing against real silicon.
4. **Document every divergence.** A divergence list is its own deliverable.

## Useful test inputs from the archive

- **`tools/original-disks/1987-12-03 TMS34010 Graphics Math Function Library r1.0.img`** — math + graphics primitives.
- **`tools/original-disks/1987-12-04 TMS34010 GSP Paint.img`** — interactive paint demo, exercises many ops.
- **`tools/original-disks/1985-05-20 TMS34010 Assembly Language Package (4 of 4) ROM-DEMO`** — TI's own demo programs.
- **`tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.zip`** through `_d3.zip` — the 1990 graphics library that wraps PIXBLT/FILL/LINE.
- **Arcade ROMs** — not in this archive (legal status varies); driven via MAME against real ROM dumps.

## Cross-references

- Field-engine corner cases → `04-memory-fields-pixels.md`.
- Pixel-op verification angles → `05-graphics-operations.md`.
- XY conversion verification → `06-xy-addressing.md`.
- Cache-flush verification → `10-cache-pipeline-timing.md`.
- Interrupt-latency verification → `11-interrupts-reset.md`.
- Host-port debug protocol → `09-host-interface.md`.
- MAME files at the pinned commit → `emulation/mame/UPSTREAM.md`.
- Arcade ROM-to-driver map → `hardware/arcade/ARCADE_USES.md`.
- Open divergences → `16-open-questions.md`.
