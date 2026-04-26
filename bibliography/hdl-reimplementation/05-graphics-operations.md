# 05 — Graphics operations

## Why this matters

The graphics ops are the differentiator. A '34010 without working PIXBLT / FILL / LINE is just a slow 16-bit-bus CPU. These instructions are also where the architecture concentrates its complexity: implicit register operands, raster-op selection, transparency, plane masking, window clipping, source-vs-destination pitch, draw-and-advance state, all interacting. **Get the data flow right before writing RTL** — block-diagramming the pixel-processing pipeline pays for itself many times.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 7 ("Pixel Processing") and Chapter 8 ("Graphics Instructions").** The two key chapters — Ch. 7 covers the pixel-processing back-end (PPOP, PMASK, transparency, PSIZE), Ch. 8 covers the per-instruction operand and side-effect tables.
- **`software/graphics-library/spvu027.pdf` (SPVU027), the TMS340 Graphics Library User's Guide.** Documents the *software* primitives that wrap the hardware ops. Reading the library source-of-truth alongside Ch. 7/8 of SPVU001A is the fastest way to understand the *intended* envelope of behavior — if SPVU027 calls a hardware op with a particular preamble, that preamble is the contract.
- **MAME `34010gfx.hxx`** at the pinned commit (`emulation/mame/UPSTREAM.md`) — ~94 KB of pixel ops. **Use as a cross-check, not as the canonical encoding source.**
- **Sibling patents to US 4,718,024**: the architects filed dedicated patents on color-expand, transparency, draw-and-advance, etc. Where SPVU001A is terse, the patents (now expired) give design rationale. See `14-patent-landscape.md`.

## Instruction families

### PIXT — single-pixel transfer

Three forms:

- `PIXT Rs,Rd` — register-to-register pixel copy (used for color manipulation).
- `PIXT *Rs,*Rd` — linear → linear single pixel.
- `PIXT *Rs.XY,*Rd.XY` — XY → XY single pixel, with clipping if window mode enabled.

The single-pixel cases are useful as the **HDL bring-up path**: get PIXT working end-to-end (with all six PPOPs, transparency, plane mask, clipping), and PIXBLT is the same logic in a loop.

### PIXBLT — block transfer

Three forms, all implicit:

- `PIXBLT B` — **binary** source, full-color dest. Source is a 1-bit-per-pixel bitmap; the chip color-expands it on the fly to PSIZE-wide pixels using COLOR0 and COLOR1 (B-file regs).
- `PIXBLT L` — **linear** source, linear dest. Source is the same PSIZE as dest. Dimensions in DYDX (B7).
- `PIXBLT XY` — XY source, XY dest. Source/dest are XY-coord pairs with clipping.

All three respect the same back-end: PPOP, PMASK, transparency, window clipping. **Operands are entirely B-file:** SADDR, SPTCH, DADDR, DPTCH, DYDX, OFFSET, COLOR0, COLOR1, WSTART, WEND.

### FILL — block fill

Two forms:

- `FILL L` — linear fill of dimensions DYDX with COLOR1.
- `FILL XY` — XY fill, clipped.

No source; just dest + color + raster op + plane mask + clipping. Useful as a **second bring-up step** after PIXT, since it exercises the dest-side path without the source-side complexity of PIXBLT.

### LINE — line draw

Bresenham-style line draw with sub-pixel precision. The instruction is **interruptible** mid-line — the partial state lives in B-file scratch registers, and on RTI the CPU resumes mid-line. RTL must serialize the state cleanly and check the interrupt-pending input between pixels (or at a defined granularity), not just at instruction boundaries.

### DRAV — draw-and-advance

A single-pixel "plot then advance" instruction. The advance amount is a packed delta in a B-file register. Used inside line/curve/glyph software loops where the inner loop is in software but the per-pixel op is one instruction.

### Other graphics-adjacent instructions

- `CPW` — **compare point with window**. Tests an XY coord against (WSTART, WEND); sets V/N/Z flags. The XY-form pixel ops use this internally for clipping.
- `CMPXY` — pairwise XY compare (for sorting / clipping logic in software).
- `FILL`-like degenerate forms exist via PIXT in a loop, but the explicit instruction is faster.

## Pixel-processing back-end

This is the combinational block that turns a "raw" source pixel + dest pixel + control state into a final write. Conceptually:

```
                ┌────────────────────┐
                │ source pixel       │
                │ (PSIZE bits, after │
                │  XY/linear fetch + │
                │  color-expand if B)│
                └────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ raster op (16 boolean) │
            │   selected by PPOP     │  ◄── fed dest pixel
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │ pixel-processing op    │
            │   (replace, transparent│
            │   AND/OR/XOR + ADD/SUB │
            │   /MIN/MAX, etc.)      │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │ plane-mask merge       │
            │   PMASK gates which    │
            │   bits update          │
            └────────┬───────────────┘
                     │
                     ▼
            write to dest at bit address
```

The exact set of pixel-processing ops (PPOP) is documented in SPVU001A Ch. 7. **There are more than 16 PPOPs** — the 16-boolean raster ops *plus* arithmetic ops (ADD, SUB, MIN, MAX) *plus* transparency variants. Don't conflate "16 raster ops" (the boolean Boolean-2 truth-table set inherited from common 2D conventions) with "PPOP encoding values" (a wider set).

### Transparency

Transparency suppresses writes when the **source** pixel matches a sentinel (typically 0, but the precise rule is set by a CONTROL bit). Implemented by gating the write-enable on a per-pixel "is transparent" comparison upstream of the plane-mask merge.

### Plane mask

`PMASK` is `~write_enable_per_bit`. A 1 in PMASK means "preserve the existing dest bit"; a 0 means "let the new value through". Replicated across the pixel for sub-16-bit pixels. See `04-memory-fields-pixels.md`.

### Color expand (PIXBLT B)

Each source bit selects between COLOR0 and COLOR1 per dest pixel. The hardware reads the source as 1-bit-per-pixel, then writes COLOR0 or COLOR1 (PSIZE-wide) into dest. Functionally equivalent to a font/glyph blit. Transparency typically applies to one of the two colors (commonly COLOR0).

## Window clipping

When window-mode is enabled (a CONTROL bit), XY-form pixel ops clip against (WSTART, WEND). There are several clipping behaviors selectable in CONTROL:

- **No clip** — writes outside window are still drawn (window mode off).
- **Pre-clip** — out-of-window pixels are silently dropped.
- **Window hit interrupt** — on a clip violation, the chip raises a window-violation interrupt.
- **Force inside** — coordinates are clamped (less common).

The exact menu is in SPVU001A Ch. 7. Make sure your RTL handles each consistently — software relies on the interrupt-on-violation mode to detect overflow.

## Direction (forward / reverse)

PIXBLT has to handle source/dest overlap. The instruction encoding includes a direction bit (or implies direction via DYDX sign / address ordering). Reverse-direction PIXBLT walks dest from the bottom-right toward top-left so an overlapping copy doesn't corrupt itself. Software computes which direction is needed; hardware obeys.

## Cycle behavior

- Pixel ops can be **long**. A large PIXBLT can take thousands of cycles.
- Most are interruptible at well-defined boundaries. SPVU001A documents which ops are atomic and which can resume mid-instruction; LINE is the explicit example, but PIXBLT is similarly resumable in the standard implementation.
- The B-file registers used as state get **modified** during execution — at the end of an interrupted PIXBLT, DADDR / DYDX / etc. hold "where we got to" rather than the original values. RTL must commit those updates incrementally so a mid-instruction interrupt can resume cleanly.

## Gotchas

- **Implicit operands.** Routing source/dest through the instruction word will appear to work on simple tests and will fail on every real graphics workload. All operands come from B-file regs and the I/O page; the instruction encoding only selects the *shape* of the op (B/L/XY, direction, etc.).
- **B-file state is destroyed.** PIXBLT is destructive on B0–B14. Software conventionally saves whatever B-file context it needs across calls; there is no automatic save.
- **Mid-instruction interrupt resume.** PIXBLT/LINE/FILL must commit B-file state incrementally. A common mistake is to update B-file only at instruction completion, which breaks any interrupt that fires while a long PIXBLT is in flight.
- **Color-expand source bit-order.** PIXBLT B reads source bits in a specific order within each source word (often LSB-first). If you reverse it, fonts come out mirrored and unhelpful.
- **CONTROL register bit positions changed between SPVU001 (1986) and SPVU001A (1988).** The 1986 first-edition layout is not bit-for-bit compatible with the 1988 production layout — see `16-open-questions.md`.
- **Plane mask zero-value convention.** PMASK = `0` means "all planes write-enabled". This is the opposite of what many RTL designers reflexively code (mask=1=enable). Match the spec.
- **Raster op encoding ordering.** The 16 boolean PPOPs are encoded by truth-table column ordering — the conventional 0..15 mapping in the literature is (~Source ~Dest, ~Source Dest, Source ~Dest, Source Dest) bits → row 0..3 of the 4-row truth table. The SPVU001A table is canonical. Don't guess.

## Implementation hints

- **Build PIXT first.** Single-pixel ops exercise the entire back-end without the address-stepping complexity of PIXBLT. When PIXT works for all PSIZEs and all PPOPs with PMASK, transparency, and clipping, PIXBLT is a controlled loop wrapping it.
- **Then build FILL.** No source-side fetch; pure dest-side stress test.
- **Then PIXBLT L.** Adds source fetch but no XY math.
- **Then PIXBLT XY.** Adds the conversion (which you have separately verified in `06-xy-addressing.md`).
- **PIXBLT B last.** Adds color-expand, which is just a 1-bit-source-driven mux into an already-tested PIXBLT L back-end.
- **LINE separately.** It's its own state machine — Bresenham accumulator, error term, sub-pixel step. Can be brought up against software-emulated line draws as a reference.

## Verification angles

- The TI graphics library (`software/graphics-library/spvu027.pdf` and the earlier `1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf`) provides reference functions whose hardware setup is documented; running them against your implementation and a MAME instance is a good smoke test.
- Arcade ROMs (`hardware/arcade/ARCADE_USES.md`) hammer PIXBLT with very particular operand patterns; Mortal Kombat, NBA Jam, and Smash TV in particular drive transparency, color-expand, and plane-mask paths hard. Pick one ROM as a "known-good" stress test.

## Cross-references

- Pixel-size machinery and PMASK basics → `04-memory-fields-pixels.md`.
- XY → linear conversion math (used by PIXBLT XY, FILL XY, PIXT XY) → `06-xy-addressing.md`.
- B-file register inventory → `03-registers.md`.
- Mid-instruction interrupt mechanics → `11-interrupts-reset.md`.
- MAME `34010gfx.hxx` for cross-checking encodings → `emulation/mame/UPSTREAM.md`.
- Patent rationale (color-expand, transparent ops, draw-and-advance) → `14-patent-landscape.md`.
