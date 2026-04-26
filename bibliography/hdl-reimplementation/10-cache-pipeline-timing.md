# 10 — Instruction cache, pipeline, and timing

## Why this matters

The '34010 has a **256-byte on-chip instruction cache**, a small fetch / decode / execute pipeline, and a documented per-instruction cycle model. The cache is essential for performance over the 16-bit external bus — without it, the chip would spend ~half its time fetching opcodes. The pipeline interactions are mostly straightforward (no branch prediction, no scoreboarding) but have a few quirks: self-modifying code, cache-flush semantics, mid-instruction interrupts, and the way long graphics ops gate the pipeline.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 12 ("Instruction Cache")** — cache organization, validity bits, fill/flush, self-modifying-code protocol.
- **SPVU001A, Chapter 13 ("Reset, Interrupts and Emulation")** — interrupt-acknowledge timing, NMI behavior, emulation breakpoints (the "EMU" instruction).
- **SPVU001A Appendix A** — per-instruction cycle counts (best-effort).
- **`docs/datasheets/84292.pdf` (SPVS002C), AC characteristics** — bus-cycle timing that the pipeline rides on.
- **MAME `tms34010.cpp` execute loop** at the pinned commit — the working software reference for "what instruction takes how many cycles". MAME is *not* strictly cycle-accurate vs. silicon, but it is the practical reference for "does this software-visible behavior happen within roughly the right window".

## Instruction cache organization

Approximate (verify in SPVU001A Ch. 12):

- **Total: 256 bytes.**
- Organized as **4 segments × 8 lines × 8 bytes** = 256 (one common decomposition; verify the segment/line counts).
- Each line has a **valid bit** (V) and a **subline-valid set** indicating which of the 8 bytes have been filled.
- A miss on any byte triggers a fill of that line (or sub-line) from the local bus.

### Segment selection

The cache is **segment-based**, not fully associative. A segment is selected based on a chunk of the PC's high bits; only one 8-line cache region in that segment can map a given block. The segment number is a small register; switching code regions resets / replaces the segment mapping.

The exact mapping (which PC bits select segment, which select line, which select byte) is in SPVU001A Ch. 12. **Get the bit-slicing right, or the cache silently aliases.**

### Fill behavior

- A fill reads from the local bus, populating one line (or sub-line set) at a time.
- Fill is interruptible — the chip won't deadlock if interrupts arrive during a fill.
- Multi-cycle fills are visible to bus arbitration (refresh, SRT, host) — they have to share.

### Self-modifying code

- The cache is **not** automatically coherent with data writes to instruction memory.
- Software that writes self-modifying code (or loads code into RAM) **must** explicitly flush the cache before executing the new code.
- Cache flush is done by writing a control bit in an I/O register (verify exact register; SPVU001A Ch. 12 names it). The flush invalidates all lines in one operation; there is no per-line invalidate from software.
- A subset of the cache control (segment-disable, etc.) lets software run with the cache fully off — useful for debugging.

## Pipeline

The '34010 pipeline is short (3 to 4 stages, depending on how you count). Approximate stages:

1. **Fetch.** PC drives cache lookup; hit returns a 16-bit half-word; miss issues a fill.
2. **Decode.** Half-word(s) interpreted into operation + operands. Long-immediate forms grab additional half-words from the cache.
3. **Execute.** ALU / shifter / field-engine / pixel-processing back-end runs. Memory-operand instructions issue local-bus cycles here.
4. **Writeback.** Register-file or memory write commits.

### Pipeline hazards

- **Read-after-write on registers** is not strictly hazardous — the writeback stage forwards to the next decode/execute cycle, or the pipeline is short enough that the writeback completes before the next dependent decode. SPVU001A is the source-of-truth on whether forwarding is required or whether a stall is inserted.
- **Memory accesses** stall the pipeline when the local bus is busy with refresh / SRT / host. The execute stage just waits.
- **Branches** (JR, JRcc) flush any prefetched-but-not-executed half-words and restart fetch at the new PC. Predicted-not-taken is the implicit policy; there is no branch prediction.

### Mid-instruction interruption

Long graphics ops (PIXBLT, FILL, LINE) and multi-register stack ops (MMTM, MMFM) **can be interrupted in the middle**. The pipeline state for resumption is stored in:

- **B-file scratch registers** for graphics ops (DADDR, DYDX, etc. are updated as the op progresses).
- **The stack pointer + status flags** for MMTM/MMFM (the multi-register state is reconstructable from PC and SP).

This is a critical RTL property: incremental commit of the operand registers, not bulk commit at instruction end. See `05-graphics-operations.md` and `11-interrupts-reset.md`.

### Atomic instructions

Some instructions cannot be interrupted (most short ALU ops, anything that would corrupt state if half-completed). SPVU001A Ch. 13 lists which instructions are interruptible vs. not.

## Instruction timing

SPVU001A Appendix A gives a cycle-count expression for each instruction. Forms:

- **Constant** for short ALU/move ops (typically a few cycles).
- **Linear in operand size** for field-mode moves (cycles depend on field size and bus alignment).
- **Linear in pixel count** for FILL / PIXBLT (cycles per pixel, plus startup, plus per-row overhead).
- **Linear in line length** for LINE (cycles per pixel of line).
- **Variable based on cache hit/miss** for fetch (most relevant for tight loops where the cache state matters).

### Wait-state contributions

- LRDY-deasserted cycles add to the bus-cycle count.
- Refresh and SRT cycles steal cycles from the CPU but at predictable intervals.
- Cache misses add fill-cycle latency.

For functional accuracy, you can ignore exact cycle counts. For performance modeling or for cycle-accurate behavior, you have to model all of the above.

## Reset behavior

On reset:

- PC is initialized to the reset vector (a fixed location, typically at the top of the address space — verify in SPVU001A Ch. 13).
- Status register flags are cleared; interrupts disabled.
- The cache is invalidated.
- I/O registers go to reset values (mostly zeros, but DPYCTL and a few others have specific defaults).
- Pin states are deterministic per the datasheet.

See `11-interrupts-reset.md` for the full reset sequence.

## Gotchas

- **Cache is not coherent with data writes.** Self-modifying code without an explicit flush will execute stale instructions. Software is expected to flush.
- **Cache flush is global.** No per-line invalidate from software. To invalidate one line you flush the whole cache.
- **Segment selection bit-slicing must match.** A wrong slice gives apparent random crashes — different code regions alias into the same cache line.
- **Long instructions (PIXBLT/FILL/LINE/MMTM) update operand state incrementally.** RTL must commit B-file or SP updates as the op progresses, not at the end.
- **Mid-instruction interrupt latency** is bounded by the chip's commit granularity — typically per-pixel or per-register. SPVU001A Ch. 13 specifies the bound; the worst-case interrupt-acknowledge time inside a long PIXBLT is on the order of "one pixel" plus the standard interrupt-entry latency.
- **EMU instruction** triggers a software-defined "emulator" trap. Used by debuggers (SPVU021A) for breakpoints. The trap mechanism is similar to TRAP but with a dedicated vector.
- **Cache-disable bit** lets software run uncached. Performance drops by a large factor; useful for measuring cache contribution and for debugging cache-coherence bugs.
- **Reset vector location** is fixed in hardware. Software cannot relocate it; the '34010 always boots from the same bit address.

## Implementation hints

- **Implement the cache as a simple direct-mapped cache first.** Get the segment-based structure right after functional cache works. The architectural-level behavior is "PC hit returns instruction, miss does a fill"; the segment structure is a performance and area optimization that you can layer in later.
- **Pipeline as in-order, no forwarding, with stall on memory operand busy.** This matches the spirit of the '34010 architecture and is easy to verify.
- **Track instruction-level resumability state in a "macro-op" finite state machine** for PIXBLT/FILL/LINE/MMTM. The macro-op FSM either commits a sub-step (one pixel, one register) and re-checks interrupt-pending, or holds in execute until done.
- **Cache-flush is a single signal that asserts all valid bits to zero.** Trivial.

## Cross-references

- Interrupt-pending check timing and entry sequence → `11-interrupts-reset.md`.
- Pixel-op incremental commit semantics → `05-graphics-operations.md`.
- Memory-bus interactions (refresh / SRT / host) that the pipeline arbitrates with → `07-memory-interface.md`, `09-host-interface.md`.
- MAME execute loop and per-op cycle accounting → `tms34010.cpp` via `emulation/mame/UPSTREAM.md`.
