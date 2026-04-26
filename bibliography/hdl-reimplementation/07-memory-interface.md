# 07 — Memory interface (local bus, DRAM, VRAM)

## Why this matters

The '34010 was designed to drive **dual-port video DRAM (VRAM)** directly. The local bus speaks DRAM (RAS / CAS / WE / OE) natively, can issue **shift-register transfer cycles** to load VRAM's serial output port from the random-access port, and arbitrates between CPU accesses, refresh, and display fetches without an external memory controller. Reimplementing this faithfully — even if you target a different external memory technology — means understanding the cycle taxonomy first.

## Source-of-truth

- **`docs/datasheets/84292.pdf` (SPVS002C), AC characteristics + bus-timing waveforms.** The authoritative reference for cycle shapes. Look for the labeled timing diagrams: read cycle, write cycle, refresh cycle, shift-register transfer (SRT) cycle, host cycle.
- **SPVS002C, "Local Memory Interface" section.** Pin-level signal definitions (LAD0–LAD15, RAS, CAS, W, DDIN, TR-QE, etc.).
- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 9 ("Memory Interface")** — architectural / programmer's view of the bus, including REFCNT, the bus-arbitration scheme, and how display fetches interleave with CPU cycles.
- **`docs/patents/US4747081.pdf` and `US4663735.pdf`** — TI's foundational VRAM patents. The '34010 was co-designed with these parts; the SRT cycle exists because dual-port VRAM exists. Use the patents for design-intent context (both expired by 2026).
- **`docs/datasheets/SPPS010A_TMS34061_Video_System_Controller_198602.pdf` and `docs/ti-official/TMS34061_Users_Guide.pdf`** — the '34061 is a *companion* video system controller used in some boards instead of the '34010's built-in display fetch path. Read these only if you want to understand alternative pairings; the '34010's own memory interface does the same job.

## Pin-level signals

Approximate inventory (verify pin names + count against SPVS002C front-matter pin description):

- **LAD0–LAD15** — multiplexed Local Address/Data. 16-bit external bus.
- **LCLK1, LCLK2** — local clock outputs (the '34010 generates the bus clock).
- **RAS, CAS** — DRAM row/column address strobes.
- **W** — write strobe.
- **DDIN** — data direction (high = read, low = write, or similar).
- **TR-QE** — transfer / output enable for VRAM serial port. (The pin name is unusual — read the datasheet pin description.)
- **LRDY** — local ready, for slow memory wait states.
- **HOLD, HLDA** — bus arbitration with another master (less common in '34010 systems but defined).
- **HLDA / BRQ / BACK** — variations exist; SPVS002C has the canonical names.

## Cycle taxonomy

The local bus runs a fixed-shape cycle that the '34010 specializes by what it does in each phase. Cycle types (verify against SPVS002C waveforms):

1. **Memory read cycle** — RAS, multiplexed row → col on LAD, CAS, data returned on LAD second half.
2. **Memory write cycle** — RAS, row → col, W asserted with data on LAD.
3. **Refresh cycle** — RAS-only-refresh (no CAS), governed by REFCNT.
4. **Shift-register transfer (SRT) cycle** — special VRAM cycle that loads the VRAM's serial port from the random-access port at a given row. Used by the display controller to refill the SAM output buffer once per scanline (or per few scanlines, depending on geometry).
5. **Host cycle** — when the host port is granted, the local bus cycle is on behalf of the host CPU rather than the '34010. The CPU pipeline stalls during these.
6. **Coprocessor cycle** — when an attached coprocessor (the '34082) takes the bus. See `12-system-coprocessor.md`.

Each cycle takes a fixed number of LCLK phases. Wait-state insertion uses LRDY to extend.

## Refresh

- **REFCNT** — I/O register that controls refresh rate. Software writes the period; hardware ticks down and issues a refresh cycle when it expires.
- The refresh cycle takes priority over CPU cycles but is **deferred** during SRT cycles or atomic indivisible CPU operations.
- Field operations that span a bus boundary cannot be split by a refresh — the RMW for the second half completes first.

## Shift-register transfer (VRAM-specific)

- VRAM has a parallel-load serial-output port. An SRT cycle copies one **row** of the random-access array into the serial-output shift register.
- The display controller schedules SRTs based on the programmed display geometry (HTOTAL etc., see `08-video-timing.md`) and DPYSTRT (which row).
- After the SRT, the VRAM clocks pixels out the serial port at the **video clock** rate, independent of the local bus, freeing the local bus for CPU work.
- SRT cycles and CPU cycles share the same bus; the chip arbitrates so SRT happens at the right scanline boundaries.

If you target an external memory technology that is **not** dual-port VRAM (e.g., synchronous DRAM, SRAM, embedded BRAM in an FPGA), you have a choice:

- **Faithfully model the SRT cycle** as a no-op or a translated bulk-copy from your memory into a separate "video line buffer" that feeds the pixel output. Most clean-room reimplementations on FPGA take this path; the line-buffer approach is the modern equivalent of VRAM's serial port.
- **Drop SRT and replace with a different display-fetch scheme.** Programmer-visible behavior is unaffected as long as DPYSTRT / DPYTAP / HSBLNK / HTOTAL produce the same pixel output.

## Address multiplexing

DRAM expects the row address on RAS edge and the column address on CAS edge, so the '34010 multiplexes its 32-bit bit-address (after byte/word alignment) onto LAD0–LAD15 in two phases. The bit-address-to-row/col mapping is parameterized by external pin strapping or by an I/O-register choice — the '34010 supports a few row/column splits to accommodate different VRAM organizations. Verify in SPVU001A Ch. 9 / SPVS002C.

## Wait states

- **LRDY** lets memory pull the chip's bus cycle out by an integer number of LCLK phases.
- Slow ROM / mapped I/O outside the on-chip register page can use LRDY to insert as many waits as needed.
- The on-chip register page does **not** stall the bus — it is on-chip and answers in zero waits.

## Bus arbitration

A second bus master (typically the host CPU when it goes through HOLD rather than through the host port) can request the bus. The '34010 grants HLDA when it is between cycles; it does not split atomic operations. Most '34010 systems use the host **port** rather than HOLD-style arbitration; HOLD is there for unusual configurations.

## Local bus vs. host port

These are **two distinct chip ports**:

- **Local memory interface** (LAD, RAS, CAS, …) connects to the '34010's own DRAM/VRAM and is what executes its instructions.
- **Host port** (a separate set of pins, see `09-host-interface.md`) lets a foreign CPU peek into the same memory through a memory-mapped window on the host's side.

Both view the same address space, but one drives the local bus to do so and the other arbitrates with the local bus through the host-port logic.

## Gotchas

- **VRAM is not assumed.** The chip works with plain DRAM if you don't use the SRT cycle. The display controller can still drive video by CPU-side pixel reads at HSYNC rate, though that is unusual and slow.
- **Refresh and SRT both compete with CPU access.** Cycle-accurate behavior requires modeling both arbitration paths. Functional models can ignore both.
- **Address mux choice changes the row/col split.** Wrong choice → the DRAM works but with apparent random address scrambling. Verify pin strapping or I/O-register encoding.
- **LCLK is a chip output, not an input.** The '34010 generates its bus clock from its own clock input. Your HDL needs an internal clock-divider; don't expect to route a system clock straight onto LCLK.
- **The bus is 16 bits wide regardless of VRAM organization.** A x16 VRAM (one chip's worth) is the simplest pairing; x4 VRAMs require four-wide assemblies and parallel CAS strobes; x8 require pairing. The '34010 doesn't care — its bus is 16 bits — but the board does.
- **Field accesses can issue 1, 2, or 3 bus cycles depending on alignment.** A 32-bit field at an unaligned bit address needs three 16-bit cycles: low-half, middle, high-half. Don't assume two.
- **DRAM-style refresh is required even for SRAM-backed implementations** if you want to honor REFCNT timing (refresh interrupts visible to software). For an FPGA reimplementation backed by BRAM, REFCNT becomes a stub that still ticks but nothing happens; that's fine for functional accuracy.

## Implementation hints

- **Model the local bus as a state machine with fixed-cycle templates.** Each cycle type is a 4–6-state walk through (idle → row → col-or-data → optional-wait → done).
- **Make the cycle scheduler explicit.** A small priority arbiter chooses next cycle: SRT > refresh > CPU_access > idle, deferred only if a multi-cycle field op is mid-flight.
- **Keep VRAM-vs-DRAM as a runtime configuration**, not a synthesis choice — software can write SRT-issuing display setups even on systems where SRT is a no-op. Letting it run as no-op is simpler than special-casing.
- **For FPGA targets, replace SRT with a line-buffer fill** clocked from internal BRAM. The display controller's view (DPYSTRT, DPYTAP, HSBLNK, HTOTAL) doesn't change.

## Cross-references

- Display-fetch scheduling and the display controller's view of SRT → `08-video-timing.md`.
- Host port arbitration with the local bus → `09-host-interface.md`.
- VRAM patents (US 4,747,081 and US 4,663,735) for design-intent → `14-patent-landscape.md`.
- '34061 companion VSC — alternative system pairing → `12-system-coprocessor.md`.
- Bit-address vs. byte-address conventions (the address that gets multiplexed onto LAD is derived from the bit address, with alignment) → `04-memory-fields-pixels.md`.
