# 16 — Open questions

## Why this matters

Some details in the documentation are ambiguous, contradictory between revisions, or simply not stated. Some of MAME's behavior is best-effort approximation rather than verified-against-silicon. This file enumerates known open questions that an HDL reimplementer will hit, with pointers to where to look or who to ask. **Resolve these against silicon (or against MAME for functional questions, or against an oscilloscope for timing questions) — don't guess.**

This list is not exhaustive. Add to it as the project progresses.

## Architecture / ISA

### Q1. Exact CONTROL register bit layout — first-silicon vs revision-A
- **Question:** SPVU001 (1986 first edition) and SPVU001A (1988) describe the CONTROL register slightly differently in places. Specifically, the position and presence of PSIZE, PPOP, transparency-enable, and window-mode bits may have moved between revisions.
- **How to resolve:** Compare the two user's guides side-by-side at the CONTROL register page in Ch. 6 of each. Identify which bits moved. Default to the SPVU001A layout for production-silicon compatibility; note SPVU001 differences for first-silicon ROM compatibility.
- **MAME behavior:** Models one representative layout. Read `34010ops.hxx` / `tms34010.h` to identify which.

### Q2. Field-extension behavior on partial-word writes
- **Question:** When writing a field whose size N exceeds the register-content significant bits, does the chip zero the high bits, sign-extend, or leave them undefined? SPVU001A is precise about reads but less explicit about writes.
- **How to resolve:** Test on MAME. If MAME diverges from the user's guide, check arcade-ROM behavior at a relevant code path.

### Q3. Predecrement / postincrement with field size 32
- **Question:** When FE0 = 32 and the predecrement/postincrement is "by field size", does the increment of 32 bits land cleanly on a 16-bit boundary? Edge case at the 32-bit boundary that the architecture documents but the implementation can get wrong.
- **How to resolve:** Hand-craft a test case: load a known pattern, do `MOVE *Rs+,Rd,F0` with FE0=32, verify Rs advanced by 32 bits.

### Q4. Stack alignment after MMTM/MMFM
- **Question:** Multi-register save/restore happens at the field size selected by the instruction. With 13 registers in flight, alignment of SP after an interrupt-aborted MMTM is non-obvious.
- **How to resolve:** SPVU001A Ch. 13 describes the partial-completion state. Verify against MAME.

### Q5. PIXBLT direction selection
- **Question:** Direction for overlapping PIXBLT is determined by software; the chip executes a forward or reverse PIXBLT based on encoding bits or implicit DYDX sign. Exact rule needs verification.
- **How to resolve:** Read SPVU001A Ch. 8 PIXBLT entry. Cross-check with MAME `34010gfx.hxx`.

## Timing and pipeline

### Q6. Cache-fill cycle count
- **Question:** A cache miss triggers a fill. How many local-bus cycles? How many subwords in the fill? Does the fill abort if a higher-priority bus need (refresh, SRT, host) arrives mid-fill?
- **How to resolve:** SPVU001A Ch. 12 + SPVS002C AC characteristics. MAME approximates but is not authoritative.

### Q7. Mid-PIXBLT interrupt latency
- **Question:** What is the worst-case cycles-from-interrupt-pending to first-handler-instruction during a long PIXBLT?
- **How to resolve:** SPVU001A Ch. 13 specifies a bound. Verify by hand-crafted test: long PIXBLT + LINT1 assertion partway through, measure cycles.

### Q8. Window-violation interrupt timing
- **Question:** When window-mode = "interrupt on violation" and a clipping violation occurs during a PIXBLT, does the interrupt fire on the first violating pixel (and abort the PIXBLT), on every violating pixel, or only at the end of the violating row?
- **How to resolve:** SPVU001A Ch. 7. MAME `34010gfx.hxx` for cross-check.

### Q9. NMI deferral during atomic operations
- **Question:** NMI is "non-maskable" but can be deferred during certain atomic ops. Which ops? For how long?
- **How to resolve:** SPVU001A Ch. 13. Test by injecting NMI mid-MMTM and observing.

## Memory interface

### Q10. Address row/column split for various VRAM organizations
- **Question:** The chip supports several row/col splits for the multiplexed LAD bus, selectable by pin strap or I/O register. Which exactly?
- **How to resolve:** SPVU001A Ch. 9 + SPVS002C signal description.

### Q11. SRT cycle scheduling under heavy CPU + host load
- **Question:** When CPU is busy, host port wants attention, refresh is due, and SRT is also due — what is the priority order, and does any of them get starved?
- **How to resolve:** SPVU001A Ch. 9. Verify the implemented arbitration matches.

### Q12. LRDY behavior during multi-cycle field accesses
- **Question:** A field that crosses bus boundaries does multiple cycles. If LRDY is deasserted during cycle 1, does cycle 2 still happen at the originally-scheduled slot, or is the entire multi-cycle access stretched?
- **How to resolve:** SPVS002C bus-cycle waveforms.

## Display controller

### Q13. DPYTAP semantics for sub-pixel scrolling
- **Question:** DPYTAP scrolls within a row, but the unit is unclear: bits, bytes, pixels (i.e., PSIZE-sized chunks)?
- **How to resolve:** SPVU001A Ch. 10. MAME `tms34010.cpp` display-update routine.

### Q14. DPYSTRT-update-at-VSYNC vs immediate
- **Question:** The DPYCTL bit that selects "update DPYSTRT at next VSYNC" vs "update immediately" — what are the exact semantics if software writes DPYSTRT with the VSYNC-update bit set, then changes the bit before the VSYNC arrives?
- **How to resolve:** Probably a "last-write-wins" semantic. Verify in SPVU001A Ch. 10 + MAME.

### Q15. Interlace mode behavior
- **Question:** Interlace mode in DPYCTL — exact field-output ordering, how the vertical counter advances, how DPYSTRT is reinterpreted.
- **How to resolve:** SPVU001A Ch. 10. Most boards ran progressive only; this corner is undertested in MAME.

### Q16. HSYNC / VSYNC polarity programmability
- **Question:** Are sync polarities individually programmable, or is there one global polarity bit?
- **How to resolve:** SPVU001A Ch. 6 (DPYCTL bit definitions). SPVS002C for output-pin behavior.

## Host interface

### Q17. Exact HSTCTL bit attributes per side
- **Question:** Each HSTCTL bit has independent attributes for "writable from host", "writable from chip", "raises interrupt on host", "raises interrupt on chip", "self-clearing on read", etc. Constructing the full table from SPVU001A Ch. 11 is tedious; transcription errors are likely.
- **How to resolve:** Table-construction exercise from SPVU001A Ch. 11. Cross-check with MAME's host-port register handling.

### Q18. Auto-increment behavior on host writes vs reads
- **Question:** Auto-increment advances the pointer per access. Writes only? Reads only? Both? With the same step size?
- **How to resolve:** SPVU001A Ch. 11. The standard answer is "both, by access width" but verify.

### Q19. Reset-via-host-port detail
- **Question:** When the host writes the reset bit in HSTCTL, what gets reset? Full chip reset (cache flushed, registers default)? Or just the CPU pipeline?
- **How to resolve:** SPVU001A Ch. 11 + Ch. 13. Test against the C source debugger's expected behavior.

### Q20. Byte-mode access endianness
- **Question:** In byte-mode (HBYTE asserted), the host's byte access maps to one of the two halves of the 16-bit chip-side word. Which half for which strobe?
- **How to resolve:** SPVU001A Ch. 11. Worth testing on both Intel-style and Motorola-style host configurations.

## Coprocessor / system

### Q21. Coprocessor-pipeline interaction during '34082-attached operation
- **Question:** When the '34082 is attached, do '34010 instructions stall whenever the coprocessor is busy, or only when a result is requested?
- **How to resolve:** SPVU001A Ch. 14 (or wherever coprocessor docs live; verify chapter number). The '34082 designer's handbook covers the other side of the protocol.
- **Scope:** Out of MVP scope for the reimplementation, but a flag.

## First-silicon vs revision-A divergences (general)

### Q22. Inventory of all first-silicon-vs-revision-A behavioral differences
- **Question:** Which behaviors changed between SPVU001 (1986) and SPVU001A (1988)? Beyond CONTROL register layout (Q1), there may be ALU flag differences, instruction-cycle differences, or even quietly-removed instructions.
- **How to resolve:** Page-by-page diff of the two user's guides. This is a tedious-but-tractable exercise.
- **Why it matters:** Most arcade ROMs target post-1988 production silicon. A few earlier designs (the SDB itself, early TIGA boards) target first-silicon. Knowing which lets you set a model "silicon revision" switch.

## MAME-specific divergences

### Q23. MAME's handling of the "TMS34012" Hard Drivin' parts
- **Question:** The Atari Hard Drivin' driver header references a "TMS34012" companion to the GSP. MAME instantiates it as a TMS34010-class device. The '34012 is sometimes described as a customized '34010 variant. What is the actual relationship?
- **How to resolve:** MAME source comments at `harddriv.cpp` lines 118–156. External documentation hunt — likely TI internal variant for MSP / Mathbox. Flagged in `hardware/arcade/ARCADE_USES.md`.

### Q24. Metal Maniax TMS34020 clock — "Unverified" upstream
- **Question:** MAME marks the Metal Maniax TMS34020 clock as `// Unverified`. The actual crystal value is ambiguous.
- **How to resolve:** Real-hardware crystal photo or schematic. Out of scope for '34010 reimplementation but flagged for completeness.

### Q25. Little Robin's `set_clock_scale(1.2)` workaround
- **Question:** MAME applies `m_indervid->subdevice<cpu_device>("tms")->set_clock_scale(1.2)` for the TCH Little Robin board. The driver author calls it a "possible timing bug in the core". Is this a model bug or a real-silicon quirk that the model is compensating for?
- **How to resolve:** Run on real hardware; observe whether the 1.2x factor is needed. Most likely a model bug; possibly a real silicon-clocking subtlety.

## Verification gaps

### Q26. No public verification suite
- **Question:** TI's internal verification suite for the '34010 is not in the public record. The closest substitutes are arcade ROMs (workload-specific) and the TI graphics library samples (smoke tests).
- **How to resolve:** Build your own. Phase 0 / Phase 1 tests in `15-verification.md` are the starting point. Treat MAME-vs-model differential testing as your most powerful tool.

## How to add to this list

Append entries with:

- A short title.
- The question.
- How to resolve (which PDF / chapter / line, or which experiment to run).
- Optional: the resolution once found, with date and source.

Resolved questions can be moved to a separate "resolved" section at the bottom, or deleted (with a note in `15-verification.md` if the resolution affects testing strategy).
