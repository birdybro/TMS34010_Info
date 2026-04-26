# 06 — XY addressing

## Why this matters

XY addressing is the '34010's signature trick: most graphics software wants to think in (x, y) screen coordinates, not in linear bit addresses. The chip lets the CPU write `*Rn.XY` and the hardware does the conversion to a linear bit address using OFFSET, the pitch, and PSIZE — in one cycle, no software multiply. Get the conversion wrong by one bit and every graphics op silently scribbles the wrong place.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 7 ("Pixel Processing")** for the conversion formula.
- **SPVU001A, Chapter 8** for which instructions accept the XY mode and how clipping interacts.
- **`docs/patents/US5333261.pdf`** — "Graphics Processing Apparatus Having Instruction Which Operates Separately on X and Y Coordinates of Pixel Location Registers" (Guttag, Asal, Tebbutt, Novak / TI, issued Jul 1994 from a 1985-priority chain). The patent narrates the XY-instruction design intent and is useful cross-reference for clean-room derivation. **Expired.**
- **MAME `34010gfx.hxx`**: the conversion routine inside the XY pixel ops.

## Coordinate format

A 32-bit register in XY mode is split:

```
bit 31 .................... bit 16 | bit 15 .................... bit 0
            Y coordinate           |          X coordinate
```

(Verify the high/low assignment against SPVU001A Ch. 7 — TI used Y in the high half. Some references abbreviate.)

Both halves are signed 16-bit. Negative coordinates are legal and meaningful for clipping and offscreen scratch buffers.

## Conversion formula

For a pixel at (X, Y) on a surface whose row-pitch and per-pixel-size are encoded by `CONVxx` (CONVDP for dest, CONVSP for source) and PSIZE, the linear bit address is approximately:

```
linear_bit_addr = OFFSET + (Y << CONVxx) + (X * PSIZE)
```

Read this carefully:

- `OFFSET` is a B-file register (B4 by convention). It is the **bit address** of the (0, 0) corner of the surface in linear memory.
- `CONVxx` encodes `log2(row_pitch_in_bits)`. The hardware **does not multiply Y by pitch**; it shifts Y left by CONVxx. This requires row pitch to be a power of two in bits — which is why software typically pads non-power-of-two screen widths up to the next power-of-two row stride.
- `X * PSIZE` is the per-pixel offset within the row. With PSIZE in {1, 2, 4, 8, 16}, this is also a shift (left by log2(PSIZE)), so the entire conversion is two shifts and an add.
- The Y term and the X term are both in **bits**.

The actual hardware encoding of CONVxx is a small bitfield (likely 4 or 5 bits) holding the shift count. The exact field width and any reserved bits are in SPVU001A Ch. 6 / Ch. 7.

## Pitch and CONVxx loading

Software computes CONVxx from the row pitch and writes it before issuing XY ops. There are two of them:

- **CONVDP** — for destination XY conversion (used by FILL XY, PIXBLT XY dest).
- **CONVSP** — for source XY conversion (used by PIXBLT XY source).

If source and dest live on different surfaces with different pitches, both are loaded. They are independent.

## OFFSET semantics

OFFSET is the **base bit address** of the surface origin. It is *not* "screen origin"; it is "where (0, 0) lives in linear memory for whatever surface the next graphics op targets." Software changes OFFSET when switching surfaces (e.g., between an offscreen buffer and the visible frame buffer).

A common convention is to set OFFSET = 0 and put the surface origin at the bit-address-zero point in memory. This is fine but loses the abstraction; most TI library code keeps OFFSET surface-relative.

## Window clipping

XY-form pixel operations apply clipping using two B-file registers:

- **WSTART** — XY of window upper-left.
- **WEND** — XY of window lower-right.

The CONTROL register selects the clipping mode (none, pre-clip, interrupt-on-hit, etc.) — see `05-graphics-operations.md`.

The clip check is performed coordinate-wise on (X, Y) before the conversion to linear bit address. Don't reorder this — clipping after conversion will fail for surfaces where the linear address wraps or where two coordinates map to the same linear bit address (degenerate cases, but they exist in offscreen scratch use).

`CPW Rs,Rd` — "compare point with window" — is the explicit instruction for window tests; it sets V/N/Z flags based on whether (X, Y) is inside (WSTART, WEND). The XY pixel ops use the same machinery internally.

## Negative coordinates and edge cases

- (X, Y) can be negative (signed 16-bit). Software uses negative coords for "the source of this PIXBLT starts off the top of the surface" patterns.
- The shift-left by CONVxx is a logical shift on Y treated as 32-bit; sign-extension of Y matters here, and it is the *implementation's responsibility* to correctly extend the 16-bit Y to 32 bits before the shift.
- The X*PSIZE multiply is also signed (X is signed); same extension responsibility.
- The final add with OFFSET is 32-bit modular.

These edge cases are where a misimplementation typically diverges from silicon. SPVU001A is precise; cross-check the sign-extension before, not after, the shift.

## Multiple addressing modes interact

When an instruction takes `*Rn.XY` and also uses postincrement (`*Rn.XY+`?), the increment behavior depends on the instruction. Some forms increment by PSIZE in X and 0 in Y (advance one pixel rightward). Others advance by DYDX-encoded amounts. SPVU001A Ch. 8 lists each instruction's exact increment behavior; **don't generalize**.

## Gotchas

- **Pitch must be a power of two in bits.** CONVxx is a shift count, not a multiply. Software using non-power-of-two pitches has to round up and waste row padding.
- **OFFSET is signed in usage but treated as unsigned bit address by the hardware.** A "negative" OFFSET is just a wrap-around in the 32-bit address space.
- **CONVDP and CONVSP are independent.** Source-pitch ≠ dest-pitch is the normal case (offscreen buffer with one stride being blitted to a frame buffer with a different stride). A PIXBLT XY with a stale CONVSP / CONVDP silently misalignment.
- **X high half vs Y low half.** Verify the high/low assignment against SPVU001A. Switching them gives a 90°-rotated memory layout that "almost works".
- **Clipping happens before conversion.** The window check is in (X, Y) space, not in linear-address space. Don't reorder.
- **OFFSET is added once.** The conversion is `OFFSET + (Y<<CONVxx) + X*PSIZE`, *not* `OFFSET + (Y<<CONVxx) + OFFSET_of_X + X*PSIZE`. Easy mistake when factoring the formula.
- **CONVDP / CONVSP encoding details (whether it's `log2(pitch)` directly, or `log2(pitch) - 1`, or includes a reserved high bit) need to be read out of SPVU001A Ch. 6.** Don't infer.

## Implementation hints

- **Express the converter as a combinational block** with inputs (Rn[31:0], OFFSET, PSIZE_log2, CONVxx) and output linear_bit_addr[31:0]. Two shifts, two adders, one sign-extender. Fits comfortably in one cycle on any modern process; on an FPGA implementation you can pipeline if needed.
- **Share the converter** between source-side (CONVSP) and dest-side (CONVDP). Multiplex inputs, not outputs.
- **Decouple the converter from clipping.** Clipping is a separate combinational compare against (WSTART, WEND); its output is (in_window flag) and an updated (X, Y) for the clamp mode if implemented. Keep them as independent blocks so verification can target each.

## Cross-references

- Pixel-processing back-end consuming the converter's output → `05-graphics-operations.md`.
- B-file register layout for OFFSET / WSTART / WEND → `03-registers.md`.
- Field-size / pixel-size primitives → `04-memory-fields-pixels.md`.
- US 5,333,261 patent for design-intent reference → `14-patent-landscape.md`.
- MAME's XY conversion routine → `34010gfx.hxx` via `emulation/mame/UPSTREAM.md`.
