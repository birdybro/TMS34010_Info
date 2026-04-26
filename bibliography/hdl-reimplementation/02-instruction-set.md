# 02 — Instruction set

## Why this matters

The ISA is the contract you have to satisfy. Every other block exists to make instructions go. The '34010 ISA mixes a fairly conventional 32-bit RISC-flavored core with a small set of *very* domain-specific graphics instructions (PIXBLT, FILL, LINE, etc.), and the hard part of the ISA is not the conventional instructions — it is the addressing modes, the implicit-register conventions of the graphics ops, and the field-size behavior.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Appendix A "Instruction Set" + Chapter 5 "Programmer's Model".** Each instruction has a one-page entry: mnemonic, operation, encoding, flags affected, exceptions, cycle count, addressing mode notes. **This is the authoritative semantics document.**
- **`tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf` (SPVU004), Appendix B "Opcode Charts".** The canonical encoding tables. SPVU001A and SPVU004 are largely consistent but the assembler manual is the one TI's own toolchain consumes — if you find a disagreement, SPVU004 is what working binaries match.
- **`tools/assembler/TMS34010_Assembly_Language_Tools_Reference_Card.pdf`.** Quick-lookup; useful to get a sense of the encoding shape before drilling into the full manual.
- **First-silicon vs. revised behavior:** if you are ever uncertain whether an instruction's documented behavior changed between 1986 and 1988, compare against `docs/ti-official/1986_SPVU001_TMS34010_Users_Guide_first_edition.pdf`.

## Instruction classes

Use these as the starting decomposition for a decode/dispatch table. Numbers and exact membership vary by reference — confirm against SPVU001A Appendix A.

1. **Move and load/store.** `MOVE`, `MOVB`, `MOVI`, `MOVK`, `MMTM`/`MMFM` (multi-register move to/from memory). Field size and sign-extension are governed by the FE0/FE1 bits in the status register and by the instruction encoding (e.g., MOVE Rs,Rd vs MOVE *Rs,Rd has different field semantics — see `04-memory-fields-pixels.md`).
2. **Arithmetic.** `ADD`, `ADDC`, `ADDI`, `ADDK`, `SUB`, `SUBB`, `SUBI`, `SUBK`, `NEG`, `NEGB`, `ABS`. Distinct K-form (short-immediate) vs I-form (long-immediate) encodings — important for instruction-length decode.
3. **Logical.** `AND`, `ANDI`, `ANDN`, `ANDNI`, `OR`, `ORI`, `XOR`, `XORI`, `NOT`, `BTST`, `CLR` / `CLRC`, `SETC`, `MOVI` (also lands here in some classifications).
4. **Shift / rotate.** `SLA`, `SLL`, `SRA`, `SRL`, `RL`. Both immediate-count and register-count forms.
5. **Compare / test.** `CMP`, `CMPI`, `CMPXY`, `CPW` (compare point with window — XY-clip relevant; see `06-xy-addressing.md`), `BTST`.
6. **Control flow.** `JR`, `JRcc`, `JA`, `JAcc`, `CALL`, `CALLR`, `CALLA`, `RETS`, `RETI`, `DSJ`, `DSJEQ`, `DSJNE`, `DSJS`. Note the **separate 8-bit short-jump and 16-bit long-jump encodings** (JRcc has both, distinguished by encoding form).
7. **Stack.** `MMTM`, `MMFM`, `PUSH`, `POPST`, `PUSHST`. The stack-multi forms are used for fast register-bank save in interrupt handlers — implementation must execute multiple register-memory transfers from a single instruction.
8. **System / mode.** `EINT`, `DINT`, `EMU` (emulator trap), `RETM`, `TRAP`, `RESET`, `SETF` (set field-size mode bits FE0/FE1), `EXGF`, `MMTM IOREG…` style I/O accesses.
9. **Pixel / graphics.** `PIXT` (single-pixel transfer) in three forms — register-indirect, *Rs,*Rd (linear-linear), *Rs.XY,*Rd.XY (XY-XY). `PIXBLT B`, `PIXBLT L`, `PIXBLT XY` and the matched `FILL L`, `FILL XY`, `LINE`, `DRAV` (draw-and-advance). These read the implicit B-file registers (DADDR / SADDR / DPTCH / SPTCH / OFFSET / DYDX / WSTART / WEND / etc.). See `05-graphics-operations.md` for the operand and side-effect map.
10. **Field move.** `MOVE` with field-size-1 / field-size-2 encoding lets you transfer arbitrarily-sized fields between registers and memory. The `34010fld.hxx` file in MAME is the cleanest implementation reference for the corner cases.

## Encoding shape

- Instructions are **16-bit-aligned half-words** in memory. (PC is a bit-address but increments by 16 per fetch.)
- Most instructions are 16 bits. **Long-immediate** forms (`MOVI`, `ADDI`, `JAcc`, etc.) are 32 or 48 bits, formed from a 16-bit opcode followed by 16 or 32 bits of immediate data.
- The decode space is dense — there is no easy "top-bits-give-class" partition. Use the SPVU004 opcode chart, or generate from the chart, rather than hand-rolling the decoder.
- MAME's `34010tbl.hxx` is a ~256 KB generated decode table; you can use it as a *cross-check* on the SPVU004 chart but **do not lift its structure verbatim** if you are doing a clean-room derivation. Read SPVU004, then verify your decoder produces the same dispatch.

## Addressing modes

The general-purpose modes:

- **Register direct** — `Rn` (A or B file).
- **Register indirect** — `*Rn`. The address in `Rn` is the **bit address** of the operand. Field size for the access is governed by the current FE0/FE1 setting selected by the instruction.
- **Register indirect with displacement** — `*Rn(disp)`. Displacement is in bits, sign-extended.
- **Register indirect with predecrement / postincrement** — `-*Rn`, `*Rn+`. The increment/decrement amount is the field size in bits — not 1, not 16. This is a frequent source of bugs in software, and a frequent source of confusion for HDL implementers expecting byte-step semantics.
- **Absolute** — `@addr`. The address is a 32-bit bit address.
- **PC relative** — used by JR (8-bit) and JRcc (8-bit short) for branches.
- **XY mode** — `*Rn.XY`. Two 16-bit halves of `Rn` are interpreted as Y (high) and X (low) coordinates and converted to a linear bit address using OFFSET, DPTCH or SPTCH, and CONVDP/CONVSP. See `06-xy-addressing.md`.

## Status flags

`N`, `C`, `Z`, `V` plus the field-size mode bits and the interrupt-mask bits all live in the ST register (see `03-registers.md`). Instructions document which flags they affect; some pixel ops set flags based on the **last** pixel transferred or the **comparison result against the window** rather than on a regular ALU outcome — read SPVU001A entries individually.

## Cycle counts

Each SPVU001A instruction page lists a cycle-count expression. These are **best-effort** for a real-silicon-compatible HDL but are not strictly required for a functional model. Many depend on memory wait states, cache hit/miss, and pixel size. If your goal is cycle-accuracy:

- The MAME core attempts cycle approximation but is **not** strictly cycle-accurate against silicon.
- For arcade-driven cycle accuracy, the most useful reference is the harness in `hardware/arcade/ARCADE_USES.md` — picking a Midway Y-unit ROM with known timing-sensitive frame-pacing and comparing your model's behavior against MAME's.

## Gotchas

- **Field size is dynamic.** Two instructions with the same mnemonic and operands can move different bit-widths depending on FE0 / FE1 in ST. Decode must include "which field-size selector this instruction uses" — most field-mode instructions encode a 1-bit "use FE0 vs FE1" selector.
- **PIXBLT operand sources are implicit.** A PIXBLT instruction encodes only "what shape" (B/L/XY) and possibly direction. **All** of source, destination, pitch, offset, color, transparency, plane mask, raster op, and clipping window come from B-file registers and I/O registers. Forgetting this and routing operands from the instruction word will produce a decoder that "works" on simple tests and silently corrupts on real graphics code.
- **`LINE` is interruptible.** Line draws can be long; the architecture allows interrupts mid-instruction with a defined save/resume mechanism. Don't model LINE as an atomic ALU op.
- **Self-modifying code interacts with the I-cache.** There are explicit cache-flush mechanisms (see `10-cache-pipeline-timing.md`); a strict implementation must honor them.
- **Two distinct JR / JRcc forms** (8-bit short and 16-bit long) — both encoded as the same mnemonic. Don't conflate them in the decoder.

## Cross-references

- Operand registers used by graphics ops → `03-registers.md`, `05-graphics-operations.md`.
- XY → linear conversion math → `06-xy-addressing.md`.
- Field size FE0/FE1 mechanics → `04-memory-fields-pixels.md`.
- Cache-flush behavior on self-modifying code → `10-cache-pipeline-timing.md`.
- MAME implementation entry points (`34010ops.hxx`, `34010gfx.hxx`, `34010fld.hxx`, `34010tbl.hxx`) → `emulation/mame/UPSTREAM.md`.
