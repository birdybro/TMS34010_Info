# 12 — System: coprocessor and companion chips

## Why this matters

The '34010 is rarely a single-chip solution. Real systems pair it with:

- A **'34082 floating-point coprocessor** (matrix-math FPU) — for 3D and CAD-class work.
- A **'34061 Video System Controller** — for systems that want a heavier CRTC and don't want to use the '34010's built-in display controller.
- A **TLC340xx-family RAMDAC / palette** — to convert the VRAM serial-port pixels into RGB analog video.
- The **TMS34020** in the second-generation family lineup — a different chip but related design intent.

A clean-room HDL reimplementation of the '34010 itself doesn't include any of these — they are board-level partners. But understanding what they expect from the '34010 (and what the '34010 expects from them) is part of the contract you have to satisfy.

## Source-of-truth

- **'34082:** `docs/ti-official/TMS34082_Designers_Handbook_1991.pdf` (programmer-level reference). Patent: `docs/patents/US5025407.pdf` (claim-language only — see `14-patent-landscape.md`).
- **'34061:** `docs/ti-official/TMS34061_Users_Guide.pdf` plus `docs/datasheets/SPPS010A_TMS34061_Video_System_Controller_198602.pdf`.
- **TLC340xx RAMDACs:**
  - TLC34076: `docs/datasheets/1992_SLAS054_TI_TLC34076_Video_Interface_Palette_Data_Manual.pdf` (most thorough).
  - TLC34075/A: `docs/datasheets/TLC34075-110FN.pdf` and `docs/datasheets/XLAS058_TLC34075A_Video_Interface_Palette_199505.pdf`.
  - TLC34074 (DAC, no palette): `docs/datasheets/XLAS056_TLC34074_Video_Interface_DAC_199505.pdf`.
  - TLC34076 (later production data): `docs/datasheets/XLAS076_TLC34076_Video_Interface_Palette_199505.pdf`.
- **'34020:** `docs/ti-official/2564006-9721_TMS34020_Users_Guide_Aug90.pdf`.

## TMS34082 — floating-point coprocessor

### What it is

A separate chip on the local bus, providing IEEE-style single- and double-precision floating-point and matrix-math acceleration. The '34010 issues coprocessor instructions; the '34082 executes them and returns results.

### Programming model

- The '34010 sees the '34082 as a memory-mapped peripheral, accessed by a coprocessor-bus protocol that piggybacks on the local bus.
- Specific opcodes (or escape sequences in the instruction stream) signal "this instruction is for the coprocessor".
- The chip handshakes via dedicated coprocessor-attention pins (FPU-acknowledge, busy, etc. — verify pin names in SPVS002C and the '34082 designer's handbook).

### What the '34010 RTL needs to support

For an MVP HDL reimplementation, **none** of this is required — you can ship a '34010 without coprocessor support and software runs fine (the '34010 is a complete standalone chip). To add it later:

1. Decode the coprocessor-instruction subspace.
2. Drive the coprocessor-attention pins.
3. Stall the pipeline while the coprocessor-busy is asserted.
4. Read the result on the coprocessor-bus.

Read the '34082 Designer's Handbook for the bus protocol and timing.

### Design intent (from US 5,025,407)

The patent (`docs/patents/US5025407.pdf`) describes the FPU's matrix-math units and the coprocessor handshake. The patent **explicitly** distinguishes "graphics processor" (the '34010, shown as a separate block) from "floating-point coprocessor" (the '34082, the claimed invention). Useful as design-intent reference; expired.

## TMS34061 — Video System Controller

### What it is

A separate chip that handles VRAM management and CRTC duties. Some board designs use the '34061 *instead of* the '34010's built-in display controller — typically when:

- The system wants more flexible CRTC behavior than the '34010 offers.
- The system uses VRAM organizations the '34010 can't address efficiently.
- Multiple frame buffers / overlay layers are needed.

### How it interacts with the '34010

- The '34061 lives on the local bus alongside VRAM.
- The '34010 issues memory cycles to VRAM; the '34061 manages the SRT scheduling and CRTC timing.
- The '34010's own display controller (HESYNC, HEBLNK, etc.) is set to a passive mode; CRT timing comes from the '34061.

### What the '34010 RTL needs

Nothing special. The '34010 just does normal local-bus reads/writes; the '34061 is a memory-mapped peripheral on those same buses. Your HDL doesn't model the '34061 — that's a separate IP block.

### Why an HDL reimplementer cares

- Understanding the '34061 path explains why some I/O register fields in the '34010 have "external CRTC" modes that disable internal SRT scheduling.
- For verification purposes: many '34010-based systems used the '34061. A faithful reimplementation has to coexist with one (i.e., must not assume control of SRT scheduling unconditionally).

## TLC340xx RAMDACs

### What they are

Single-chip palette + RAMDAC parts. They take the VRAM serial-port output (pixel indices, typically 4 or 8 bits per pixel), look up the corresponding RGB triple in an on-chip color palette, and drive analog R/G/B outputs to a CRT.

### How they interact with the '34010

- The VRAM serial port clocks pixels into the RAMDAC at VCLK rate.
- The '34010 (or the host CPU through the '34010's host port) writes the palette via a separate slow-side bus on the RAMDAC (typically a few I/O addresses on the local bus).
- The RAMDAC drives HSYNC/VSYNC/BLANK from the '34010's CRTC outputs, plus its own pixel-clock logic.

### What the '34010 RTL needs

Nothing — the RAMDAC is downstream of the chip. The '34010 produces the HSYNC/VSYNC/BLANK and the VRAM serial-port output (via SRT scheduling); the RAMDAC consumes them.

### Why an HDL reimplementer cares

- The pixel-clock-domain output ordering and SRT timing have to match what these RAMDACs expect.
- The TLC34075 / TLC34076 timing in their respective datasheets is the practical specification for "how fast can VCLK go", "what is the BLANK setup/hold relative to pixel clock", and similar pixel-domain AC parameters.

For an FPGA reimplementation that drives a digital interface (DVI/HDMI/LVDS) instead of an analog RAMDAC, you can replace the RAMDAC entirely; just preserve the pixel-clock-domain ordering.

## TMS34020 — second-generation family member

### What it is

A different chip in the same architectural family. **Not** a drop-in '34010 replacement.

### What's different

(See `docs/ti-official/2564006-9721_TMS34020_Users_Guide_Aug90.pdf`.)

- Wider instruction set (additional graphics ops, math ops).
- Different host interface (some bit fields moved or expanded).
- Pairs with the '34082 over a tighter coprocessor bus.
- Different pinout — not pin-compatible.
- Different cycle timings.

### Why an HDL reimplementer of the '34010 cares

- For "future expansion" in your HDL, knowing what '34020 added is useful.
- Some software claims to "run on the '340 family" but actually requires '34020-only instructions; matching MAME's '34020 driver path tells you what real-world ROMs are '34020-bound.
- The '34020 user's guide is a good cross-reference for ambiguous '34010 details — when SPVU001A is terse, SPVU001A's '34020 successor sometimes phrases the same thing more clearly.

The '34020 is **out of scope** for this reimplementation effort. Note the differences when ambiguity in '34010 docs sends you to the '34020 manual.

## Software development board (system reference)

The '34010 SDB (`docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf`, plus the pocket reference) and the TI Color Graphics Controller Board (`hardware/pc-tiga/TI_Color_Graphics_Controller_Board_Users_Guide_1986.pdf`) document **complete reference systems**. They are useful as:

- Concrete examples of how to wire a '34010 with VRAM, RAMDAC, and host bus.
- Sources for memory map decisions (where ROM goes, where RAM goes, where the host window is).
- Boot-ROM behavior to match.

For a clean-room HDL implementation, do not lift specifics from these documents into your design — the chip is a chip, the board is a board. But understanding "what shape does a working '34010 system take" makes the chip-side design choices easier to validate.

## Cross-references

- Local-bus arbitration with coprocessor / '34061 / RAMDAC peripherals → `07-memory-interface.md`.
- VRAM SRT scheduling → `08-video-timing.md`.
- Host port for system-level command flow → `09-host-interface.md`.
- Patent landscape including FPU patent → `14-patent-landscape.md`.
