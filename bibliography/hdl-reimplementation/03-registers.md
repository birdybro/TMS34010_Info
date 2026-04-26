# 03 — Registers

## Why this matters

The register file is the most touched piece of HDL state. The '34010 has two banks (A, B), a status register with mode bits that change instruction semantics, a PC that is itself a bit address, and a memory-mapped I/O register page that controls every other block on the chip. **The B file is special** — graphics instructions read it implicitly, so its register-name discipline is part of the ISA contract, not a software convention.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 2 ("Programming Model")** for A/B/SP/PC/ST.
- **SPVU001A, Chapter 6 ("I/O Registers")** for the on-chip register page (display controller, host port, interrupts, pitch/offset, etc.).
- **`docs/datasheets/84292.pdf` (SPVS002C), "Register Summary".** Compact reference; useful when you want all bit-fields on one page.
- **For first-silicon variants** (some I/O registers added or relocated between SPVU001 and SPVU001A), cross-check `docs/ti-official/1986_SPVU001_TMS34010_Users_Guide_first_edition.pdf`.

## CPU registers

### General-purpose register files A and B

Two banks, each 15 registers wide, plus the shared SP.

```
A0 A1 A2 ... A14   (file A)
B0 B1 B2 ... B14   (file B)
SP                 (one stack pointer, accessible from both files as A15/B15)
```

- All 32 bits.
- Most arithmetic / logical / move instructions specify which bank in the encoding.
- **Graphics instructions implicitly use the B file.** B0–B14 carry the standing graphics context (source/dest addresses, pitches, offset, plane mask, etc. — see below). Software has to keep B-file content valid before issuing PIXBLT / FILL / LINE.

### B-file conventional usage

The B file's register names are *conventional* in software but *load-bearing in hardware* — graphics instructions hard-wire which B-file register supplies which datum. The standard mapping (verify in SPVU001A Chapter 7 "Graphics Operations"):

| B-file reg | Conventional name | Used by |
| --- | --- | --- |
| B0 | SADDR (source address, bits) | PIXBLT B/L/XY src |
| B1 | SPTCH (source pitch) | PIXBLT, LINE, FILL |
| B2 | DADDR (dest address, bits) | PIXBLT, FILL, LINE, DRAV |
| B3 | DPTCH (dest pitch) | PIXBLT, FILL, LINE, DRAV |
| B4 | OFFSET | XY → linear conversion |
| B5 | WSTART (window start XY) | clipping (CPW, PIXBLT XY) |
| B6 | WEND (window end XY) | clipping |
| B7 | DYDX (height/width, packed) | PIXBLT, FILL |
| B8 | COLOR0 | FILL transparent / mono fill |
| B9 | COLOR1 | FILL solid / pattern |
| B10–B14 | scratch / line params (DI, etc.) | LINE intermediate state |

The exact assignment matters at the bit level — check SPVU001A before wiring it. The list above is a navigation index.

### Status register (ST)

ST holds:

- **Condition flags** N, C, Z, V (from the ALU).
- **Field-size mode bits** FE0 (selects the size for "field-1" mode) and FE1 (size for "field-2" mode), and their associated **field-extension** bits (sign-extend vs. zero-extend on field reads). Several instructions encode a 1-bit selector that picks FE0 or FE1; the hardware then uses the corresponding ST entry.
- **Pixel-processing controls** (in some references these live in ST; in others in the I/O `CONTROL` register — see Gotchas).
- **Interrupt enable / mask** bits (E, IE).
- **Privilege / mode** bits (in some forms).

Read SPVU001A Chapter 2 for the exact bit layout. SPVS002C has the compact summary.

### Program counter (PC) and stack pointer (SP)

- **PC is a 32-bit bit address.** Increments by 16 (decimal) per 16-bit instruction half-word fetched. Branches do bit-address arithmetic.
- **SP is a 32-bit bit address** as well — it can point at any field-aligned position in memory; conventional stack semantics (push decrements, pop increments by the field size of the operand) are the rule.

## I/O register page

Memory-mapped at the high end of the address space. Conventionally referred to as `0xC0000000` upward (byte equivalent) or the corresponding bit address. Each register is 16 bits in the byte-equivalent map, but accessed as 16-bit fields.

Register **classes** (full per-bit layouts: SPVU001A Ch. 6 + SPVS002C register summary):

### Display / video controller

| Register | Function |
| --- | --- |
| HESYNC | Horizontal end of sync |
| HEBLNK | Horizontal end of blanking |
| HSBLNK | Horizontal start of blanking |
| HTOTAL | Horizontal total |
| VESYNC | Vertical end of sync |
| VEBLNK | Vertical end of blanking |
| VSBLNK | Vertical start of blanking |
| VTOTAL | Vertical total |
| DPYCTL | Display control (enable, screen origin, etc.) |
| DPYSTRT | Display start address (top-of-screen bit address in VRAM) |
| DPYINT | Display interrupt scanline |
| DPYTAP | Tap-point register (for offscreen → onscreen scrolling) |
| DPYSTL | Display status line (counter readback) |

See `08-video-timing.md` for how these compose.

### Memory / pixel control

| Register | Function |
| --- | --- |
| CONTROL | Master control: PSIZE, PPOP, transparency enable, window mode, etc. |
| CONVDP | Convert dest pitch (precomputed log2 lookup helper for XY conversion) |
| CONVSP | Convert source pitch (analogous) |
| PSIZE | Pixel size (1, 2, 4, 8, 16) — in some refs this is a CONTROL field, in others its own reg |
| PMASK | Plane mask (which bit-planes are write-enabled) |

See `04-memory-fields-pixels.md` and `05-graphics-operations.md`.

### Host interface

| Register | Function |
| --- | --- |
| HSTADRL | Host address low |
| HSTADRH | Host address high |
| HSTDATA | Host data (the read/write window) |
| HSTCTLL | Host control low (host-to-'34010 message bits, `INTIN`, `MSGIN`, etc.) |
| HSTCTLH | Host control high ('34010-to-host message bits, `INTOUT`, `MSGOUT`, etc.) |

These are the **'34010-side** view. The host CPU sees a different mapping — SPVU001A Chapter 11 describes both. See `09-host-interface.md`.

### Interrupt control

| Register | Function |
| --- | --- |
| INTPND | Interrupt pending |
| INTENB | Interrupt enable |

See `11-interrupts-reset.md`.

### Refresh / DRAM control

| Register | Function |
| --- | --- |
| REFCNT | Refresh count (controls DRAM refresh interval) |

See `07-memory-interface.md`.

## Gotchas

- **PSIZE / PPOP location varies by reference.** Some appendix tables show them as fields inside `CONTROL`; others list them as standalone I/O registers. SPVU001A Ch. 6 is the source-of-truth. Do not implement from the datasheet's terse register summary alone — read the full chapter.
- **`OFFSET` is a B-file register, not an I/O register.** Easy to misfile. It participates in every XY → linear conversion (see `06-xy-addressing.md`).
- **CONVDP / CONVSP are precomputed log-pitch helpers.** Software writes a value derived from `log2(pitch)` and the hardware uses it during XY → linear conversion to avoid per-instruction divides. Get the encoding wrong and pitches above 64 silently misalign.
- **The host-side and '34010-side I/O register maps are different.** Same physical resources, different addresses, sometimes different bit layouts. The host port's `HSTCTL` exposes some bits the '34010 cannot directly see and vice versa. SPVU001A Ch. 11 ("Host Interface") is the only place that walks both views.
- **First-silicon (1986) and revision-A (1988) I/O register sets are not identical.** A few registers were renamed or had bit fields reshuffled. If you are matching a specific test ROM, identify which silicon revision it was authored against; SPVU001 (1986) is the first-silicon reference, SPVU001A (1988) is the production reference.
- **PC bit-address sloppiness.** Some debuggers and tools display PC as a byte address even though the architecture is bit-address. The internal RTL state is a bit address; converting only at debug-display time is the cleanest invariant to enforce.

## Cross-references

- Field-size machinery (FE0/FE1 mode bits, sign extension) → `04-memory-fields-pixels.md`.
- Implicit B-file usage by graphics ops → `05-graphics-operations.md`.
- Display-controller register layout in detail → `08-video-timing.md`.
- Host-port register-layout differences → `09-host-interface.md`.
- Interrupt-control bits → `11-interrupts-reset.md`.
- DRAM refresh control via REFCNT → `07-memory-interface.md`.
