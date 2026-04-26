# 01 — Architecture overview

## Why this matters

You need a top-level block diagram before you can partition the RTL. The '34010 is unusual: it is a CPU and a graphics accelerator and a programmable display controller and a memory controller, all sharing one external bus. The right partitioning of those subsystems is the first design decision.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 1 ("Architectural Overview").** Block diagram, datapath description, and the role of each major unit. This is your starting read.
- **`docs/datasheets/84292.pdf` (SPVS002C), front-matter "Functional Block Diagram"** — the same diagram in compact form, plus pin-level boundaries.
- **`docs/patents/US4718024.pdf`, Fig. 2.** The **canonical** TMS34010 block diagram as filed by the architects. CPU + register files + instruction cache + memory interface + special graphics hardware + host interface + I/O regs + video display controller. Use this when SPVU001A's diagram is ambiguous about block boundaries.
- The 13 sibling continuation applications referenced inside US 4,718,024 each cover one subsystem (color expand, transparent ops, X/Y coords, draw-and-advance, instruction set, variable field size memory access, etc.). For a deeper architectural rationale on a specific block, find the matching sibling.

## Top-level blocks

Approximate decomposition. Not authoritative — cross-check against SPVU001A Ch. 1 / US 4,718,024 Fig. 2 / SPVS002C functional diagram. The '34010 collapses what would normally be several chips into one die, and the architects called those out as discrete "logical" blocks even though they share datapaths.

1. **Instruction unit / sequencer.** Fetches, decodes, executes the instruction stream. Drives the datapath through micro-control.
2. **Register files (A and B).** Two banks of 15 general-purpose 32-bit registers, plus a stack pointer (SP) shared between banks. The B file is the "graphics-context" file — graphics instructions implicitly reference B-file registers (DADDR, SADDR, DPTCH, SPTCH, OFFSET, WSTART, WEND, etc.). See `03-registers.md`.
3. **ALU + barrel shifter.** 32-bit ALU and a 32-bit barrel shifter; the shifter is critical for field operations and pixel shifts.
4. **Field-extraction / field-insertion hardware.** Reads or writes a 1- to 32-bit field at any bit address. This is the substrate everything else (pixel ops, instruction fetch, register-mapped I/O) rides on.
5. **Pixel-processing hardware.** Implements the 16 boolean raster ops, transparency, plane masking, and pixel-size-aware compares. Hangs off the ALU/shifter datapath; selected by the PPOP / PSIZE fields in the CONTROL I/O register and PMASK.
6. **Instruction cache.** 256 bytes, on-chip. Reduces the cost of single-byte-aligned instruction fetch over the multiplexed 16-bit external bus. See `10-cache-pipeline-timing.md`.
7. **Local memory interface.** Drives the multiplexed local address/data bus (LAD0–LAD15) and control strobes (RAS / CAS / WE / OE / DDIN / TR-QE / etc.). Handles DRAM refresh and VRAM shift-register transfer cycles natively. See `07-memory-interface.md`.
8. **Host interface.** A second port that lets a host CPU on the **other side** of the chip see a 32-bit window into '34010 memory. Memory-mapped from the host's view as HSTADRL / HSTADRH / HSTDATA / HSTCTL. See `09-host-interface.md`.
9. **Video display controller.** A programmable CRTC: HESYNC / HEBLNK / HSBLNK / HTOTAL plus vertical equivalents, DPYSTRT / DPYTAP / DPYINT. Drives VCLK and the VRAM serial-port transfers that feed the RAMDAC. See `08-video-timing.md`.
10. **Interrupt logic.** External pins (LINT1, LINT2 — local) plus internal sources (display interrupt, host interrupt, NMI from reset/breakpoint). See `11-interrupts-reset.md`.
11. **Coprocessor / expansion bus interface.** Additional pins/cycles for attaching a '34082 FPU (or other coprocessor). Not essential for an MVP. See `12-system-coprocessor.md`.

## Datapath summary

- **Internal datapath:** 32-bit. Most operations on registers and ALU are full 32-bit.
- **External bus:** 16-bit, multiplexed address/data on LAD0–LAD15. Two bus cycles to fetch a 32-bit word; the cache amortizes this for instructions.
- **Address space:** 32-bit **bit address**. The chip exposes ~4 G**bits** = 512 Mbytes of byte-addressable space, addressed at bit granularity. Field operations work natively at the bit-address level — there is no separate alignment shifter you can leave out.
- **Internal register width:** 32 bits everywhere (register files, status, PC, SP). The PC is itself a bit address into instruction memory.
- **Pixel size is dynamic:** PSIZE selects 1, 2, 4, 8, or 16 bits per pixel. Pixel operations adapt at runtime; the hardware doesn't need separate datapaths per size, but it does need the field-size machinery from item 4 above.

## What is **not** a separate block

- There is **no** separate "graphics ALU" cleanly hung off to the side. Pixel ops reuse the main ALU + shifter, plus the pixel-processing combinational logic. Don't be fooled by the user's-guide block diagram into duplicating the datapath.
- There is **no** I/D-cache separation. Only **instructions** are cached. Data accesses go straight to the local memory interface. (This matters for your verification strategy — self-modifying code has cache-coherence implications, see `10-cache-pipeline-timing.md`.)
- There is **no** dedicated DMA engine. PIXBLT / FILL / LINE are instructions that hold the pipeline and drive the memory interface directly. See `05-graphics-operations.md`.

## Address-space map (high-level)

The full 32-bit (bit-)address space is mostly external memory. **High addresses** (`0xC0000000`–`0xC00001FF` byte equivalent, conventionally) are reserved for the **on-chip I/O register page** — display control, host port, interrupt control, pitch/offset registers, etc. See `03-registers.md` for the register layout and `08-video-timing.md` for the display-controller subset.

The bit-address representation of `0xC0000000` (byte-equivalent) → multiply by 8 to convert. SPVU001A uses bit addresses everywhere; SPVS002C sometimes uses byte addresses. Cross-check the multiplication factor before building any address decoder.

## Clean-room note

The block partitioning above is sufficient as a starting partition for HDL. The architects' own partitioning (US 4,718,024 Fig. 2 + sibling continuations) is in the public record and expired; using it as a structural reference for clean-room work is fine, but document the chain — you derived the partition from a publicly-issued patent that has now lapsed, not from leaked TI internals. See `14-patent-landscape.md`.

## Cross-references

- Datapath details and field-size machinery → `04-memory-fields-pixels.md`.
- Pixel-processing back-end (PPOP, PMASK, transparency) → `05-graphics-operations.md`.
- Multiplexed LAD bus and refresh / VRAM cycles → `07-memory-interface.md`.
- I/O register page memory map → `03-registers.md`.
- MAME's CPU-core file layout (which mirrors a partitioning very close to the above) → `emulation/mame/UPSTREAM.md`. Read `tms34010.cpp` for the execute loop, `34010ops.hxx` for generic instructions, `34010gfx.hxx` for graphics ops, `34010fld.hxx` for field-pixel moves, `34010tbl.hxx` for the dispatcher table.
