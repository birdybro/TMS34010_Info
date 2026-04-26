# 04 — Memory, fields, and pixels

## Why this matters

This is the load-bearing block. Everything else — instruction fetch, register-mapped I/O, pixel ops, even the stack — is a consumer of one underlying primitive: **a read or write of an N-bit field at any bit address in a 32-bit address space, where N is selected dynamically.** Get this block right and the ISA falls out cheaply. Get it wrong and the entire architecture limps.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 4 ("Memory Organization") and Chapter 5 ("Programmer's Model").** The bit-addressable memory model and the field-extension semantics.
- **SPVU001A, Chapter 7 ("Pixel Processing")** for the pixel-size scaling.
- **`docs/patents/US4718024.pdf`** is the first-issued of the 13-sibling architecture-patent set; the **independently-selectable-pitch** and **variable-field-size memory access** are central claims. The corresponding sibling patents (some unissued, two issued as US 5,333,261 and US 5,437,011) cover the field-size machinery in more depth and are clean-room useful for understanding **why** the design is shaped the way it is.

## Memory model

- **32-bit address space, but the address is a bit address.** Equivalent to ~512 Mbyte addressable.
- **No alignment requirement** at the architectural level: any field of 1 ≤ N ≤ 32 bits can start at any bit position. The hardware does the read-modify-write across a bus boundary if the field straddles one.
- **External bus is 16 bits wide.** A field that crosses a 16-bit boundary takes two bus cycles. Field sizes ≤ 16 bits that happen to be 16-bit-aligned hit one cycle.
- **Endian / bit-order convention:** documented in SPVU001A Ch. 4 — confirm before writing the bit-extraction logic. (The '34010 numbers bits within a 16-bit half-word in a specific order; reversing it gives a chip that "works" on byte-aligned data and corrupts everything else.)

## Field operations

### Field size selectors

Two field-size registers live in the status register: **FE0** and **FE1**. Each holds:

- A field-size value (1 to 32).
- A field-extension bit (0 = zero-extend on read, 1 = sign-extend on read).

Field-mode instructions (`MOVE *Rs,Rd,F`, etc.) include a 1-bit selector that picks FE0 or FE1. There is no third option — software must reload FE0/FE1 if it needs a different size.

### Read semantics

For a field-mode read of N bits from bit address A:

1. Form the 32-bit-aligned (or 16-bit-aligned, depending on the implementation choice) read window covering A through A+N−1.
2. Right-shift the read data so the field's LSB lands at register bit 0.
3. If the field crosses the bus-cycle boundary, do a second read and concatenate.
4. Mask off bits above bit N−1.
5. If FEn's extension bit = 1, sign-extend bit N−1 through bit 31. Otherwise zero-extend.

### Write semantics

For a field-mode write of N bits from register R to bit address A:

1. Read the existing memory under the field (RMW).
2. Mask off the N-bit window.
3. OR in the lower N bits of R, shifted to the field's bit position.
4. Write back.
5. If the field crosses a bus boundary, do this twice.

### Predecrement / postincrement

The increment quantum is **N bits** — the current field size. So `MOVE *Rs+,Rd,F` advances `Rs` by FEn bits, not by 16, not by the bus width. This is a frequent gotcha both for software and for HDL implementers who reflexively model post-increment as "+= bus width".

## Pixel addressing

The "pixel" view sits on top of the field view: a pixel is a field of size **PSIZE**, where PSIZE ∈ {1, 2, 4, 8, 16}. The PIXBLT / FILL / LINE / PIXT / DRAV instructions all use PSIZE for their per-pixel operations.

- PSIZE lives in the I/O `CONTROL` register (or in its own register depending on revision — see `03-registers.md`).
- Pixel addresses are still bit addresses; PSIZE is just the multiplier on each step.
- A 1-bit pixel scheme (mono) drops to a degenerate field-of-1 operation; it shares the same datapath.

### XY-to-linear conversion

When the address mode is `*Rn.XY` or when an XY-form pixel op fires:

```
linear_bit_addr = OFFSET + (Y << CONVxx) + (X * PSIZE)
```

Where `CONVxx` is `CONVDP` for dest or `CONVSP` for source. CONVxx encodes `log2(pitch)` so the multiply by row pitch becomes a left shift. See `06-xy-addressing.md` for the full math (the formula above is approximately correct; verify the bit positions and the role of OFFSET against SPVU001A Ch. 7).

## Bus-cycle minutiae

- The local memory interface multiplexes address and data on LAD0–LAD15. A field read drives RAS / CAS to assemble a bus word, then the field-extraction logic shifts and masks.
- Writes that don't span a bus boundary can be done as straight CAS-write with the appropriate data byte/halfword strobes.
- Writes that span a bus boundary must be RMW.
- VRAM shift-register transfer cycles are **separate** memory cycles initiated by the display controller; they do not interfere with field read/write semantics from the CPU side. See `07-memory-interface.md` and `08-video-timing.md`.

## Plane mask

Field write × plane mask interaction: for **pixel** writes (not arbitrary field writes), `PMASK` selectively gates which bits of the pixel are actually modified. Implemented as `(new_pixel & ~PMASK) | (existing_pixel & PMASK)` after the raster op runs.

- PMASK is per-pixel-bit, replicated across the field if the pixel is < 16 bits.
- PMASK is **not** applied to non-pixel field writes (e.g., MOVE field-mode); only to PIXBLT / FILL / LINE / PIXT.

## Gotchas

- **Field-extension bit is per-FE-slot.** FE0 and FE1 each carry their own sign/zero-extend choice. A `MOVE Rs,Rd,F0` with a different FE0 setting than expected silently flips sign-extension behavior.
- **The increment is the field size, not the field-aligned size.** `MOVE *Rs+,Rd,F` with FE0=24 increments Rs by 24 bits per move.
- **PSIZE is shared global state.** Changing PSIZE between PIXBLTs is legal but easy to forget; the hardware does no checking.
- **PMASK only covers the pixel-write path.** Misapplying it to a regular MOVE field write is a common simulator bug — and a common bug in third-party '34010 software too.
- **A 32-bit field can land at any bit address.** That means up to **three** 16-bit bus accesses if the field straddles a 16-bit boundary and the read/write is over a bus that cannot fetch 32 bits in one cycle. Some references say "two cycles for 32-bit field" — true only when 16-bit-aligned.
- **CONVDP / CONVSP must match the actual pitch.** They are software-loaded log2 helpers; the hardware **doesn't** sanity-check them. A pitch of 320 with a wrong CONVDP gives image-shaped garbage, not a clear failure.
- **First-silicon vs revision-A field-extension behavior on partial-word writes** — flagged in `16-open-questions.md`. Worth verifying against silicon if you care about pre-1988 ROMs.

## Implementation hints

- **Implement the field engine as a stand-alone block** with a clean read/write interface, parameterized by (bit_address, field_size, sign_extend). Then express MOVE-field, instruction fetch, MMTM/MMFM, register-mapped I/O, and pixel ops as clients of that block. Trying to fold field semantics into each instruction's microcode duplicates a lot of logic.
- **Cache the "current bus word" between consecutive field accesses to the same 16-bit cell.** Many code patterns (instruction fetch, scanline fills) will re-touch the same word.
- **Generate the field shifter as a barrel shifter parameterized 0..15.** The byte-boundary case (no shift) drops out; the 1..15 cases all use the same combinational path.

## Cross-references

- ALU + barrel-shifter datapath that the field engine consumes → `01-architecture.md`.
- Pixel-op back-end (raster ops, transparency) that the field engine feeds → `05-graphics-operations.md`.
- XY conversion math → `06-xy-addressing.md`.
- Bus-side semantics (RAS/CAS, VRAM shift cycles) → `07-memory-interface.md`.
- MAME's field engine: `34010fld.hxx` (`emulation/mame/UPSTREAM.md`).
