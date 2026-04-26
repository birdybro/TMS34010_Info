# 13 — Pinout and electrical characteristics

## Why this matters

For a reimplementation that targets new silicon or an FPGA evaluation board with the same physical pinout, the package and pin-function assignment is the contract. For an FPGA-only or simulation-only reimplementation, the pinout still matters because it tells you which signals are conceptually grouped (host port vs local bus vs video vs coprocessor) and what the AC characteristics constrain at the pin boundary.

## Source-of-truth

- **`docs/datasheets/84292.pdf` (SPVS002C, June 1991).** The authoritative production-silicon datasheet. Pin function table, AC/DC characteristics, package drawings, ordering information.
- **`docs/datasheets/SPVS002A_TMS34010_Graphics_System_Processor_198707.pdf`** for the earlier (1987) revision. Some AC parameters and pin behaviors differ.
- **`docs/datasheets/SPVS002C_TMS34010_Graphics_System_Processor_199106_altscan.pdf`** is the same SPVS002C document but a different scan; useful only when the primary copy has unreadable diagrams.
- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Appendix B / signal-description appendix** for an architectural-level signal description (less complete than the datasheet's electrical view).

## Package

The '34010 was offered in:

- **PGA (Pin Grid Array)** — typical 132-pin or so for the larger configuration.
- **PLCC (Plastic Leaded Chip Carrier)** — 68-pin and 84-pin variants, though the '34010 is typically larger; verify in SPVS002C ordering section.
- **PQFP** — flat-pack equivalents in some ordering options.

Verify package counts in SPVS002C "Mechanical Data" / "Ordering Information". Different speed grades (e.g., '34010-50 vs '34010-40) exist; speed grade is the primary AC-characteristic differentiator.

## Pin groups (functional)

Approximate inventory. **Verify pin counts per group against SPVS002C — these numbers are illustrative.**

### Power and ground
- VCC, VSS — usually multiple of each, distributed for current return paths.

### Clock
- LCLK1, LCLK2 (or CLKIN, CLKOUT) — local clock input plus chip-generated derived clocks.
- VCLK — pixel clock; can be input or output depending on configuration.

### Local memory bus
- LAD0–LAD15 — multiplexed Local Address/Data, 16 bits.
- RAS, CAS — DRAM strobes.
- W (or WE) — write strobe.
- DDIN — data direction.
- TR-QE — transfer / output enable for VRAM serial port.
- LRDY — wait-state input.
- LCLK1 / LCLK2 — local clocks (if separately routed).

### Display / video
- HSYNC — horizontal sync output.
- VSYNC — vertical sync output.
- BLANK — blanking output.
- VCLK — pixel clock.
- (Pixel data does not come out the chip; it comes from VRAM serial port to RAMDAC directly.)

### Host interface
- HD0–HD15 — host data bus, 16 bits.
- HCS — host chip select.
- HRD, HWE (or HE + HRW) — host read/write strobes.
- HFS0, HFS1 — host function select (which host-side register).
- HRDY — host ready.
- HINT — host interrupt output (chip → host).
- HBYTE — byte-mode select.
- HLDS, HUDS — byte strobes for byte-mode.

### Interrupt and reset
- LINT1, LINT2 — local interrupt inputs.
- RESET — reset input.
- NMI — non-maskable interrupt input (in some pin maps; in others NMI is internal-only).
- HOLD, HLDA — bus arbitration.

### Coprocessor / expansion
- Coprocessor strobes (if present on '34010 — verify; some signals are shared with the local bus and only differentiated by phase / qualifier).
- The '34020 has a more elaborate coprocessor bus; the '34010's is lighter.

### Test
- Test mode strobes for production test (typically one or two pins). Document for completeness; not used in normal operation.

## AC characteristics (what to model)

Read SPVS002C "Timing Requirements" / "Switching Characteristics" sections. Parameters that load-bear:

### Clock
- Maximum LCLK frequency (40, 48, 50 MHz are common speed grades).
- LCLK duty cycle, rise/fall, jitter.
- VCLK maximum frequency.

### Local bus cycle
- RAS-to-CAS delay (tRCD).
- CAS access time (tCAC).
- Address setup/hold to RAS, CAS.
- Data setup/hold for writes.
- LRDY setup time relative to clock.

### Host bus cycle
- HCS to HRD/HWE setup.
- HRDY assertion time.
- HD0–HD15 valid window for reads.
- HD setup/hold for writes.
- HINT pulse width (or level-active behavior — verify).

### Display outputs
- HSYNC / VSYNC / BLANK delay relative to VCLK.
- Polarity (programmable).

### Reset
- Minimum RESET pulse width.
- Power-up reset hold time after VCC stable.

### Interrupt inputs
- LINT1 / LINT2 setup/hold relative to LCLK.
- Minimum pulse width.

For an FPGA reimplementation, most of these parameters become "best-effort" — you target a clock rate that your fabric supports, and AC parameters scale accordingly. For an ASIC reimplementation, match the datasheet exactly if drop-in compatibility is the goal.

## DC characteristics

Standard CMOS DC: VIH/VIL, VOH/VOL, IIH/IIL, IOZ. Read the SPVS002C DC section.

The '34010 was originally a 5V part. A reimplementation running at 3.3V or lower needs level-shifters or a redesigned I/O buffer; the chip's I/O behavior is documented at 5V only.

## Pinout differences across silicon revisions

- **First-silicon (early 1986)** had some test/diagnostic pins that revision-A removed or repurposed.
- **Speed grade variants** ('34010-32, -40, -50) share the same pinout but have different AC timings.
- **Package variants** are not pin-compatible across PGA / PLCC / PQFP — pin ordering changes.

If your reimplementation targets a specific package, lock the pinout to that package's drawing in SPVS002C.

## Gotchas

- **VCLK direction is configurable.** If your reimplementation hardcodes "VCLK is output", a system designed to drive VCLK from an external clock generator won't work.
- **Multi-pin VCC/VSS distribution matters at speed.** A reimplementation that consolidates power pins will have current-return issues — match the original distribution if at all possible.
- **TR-QE (or whatever it's named in SPVS002C)** is the VRAM serial-port transfer pin. Not a typo; it's TI's pin name.
- **Some pins multiplex functions based on a mode bit.** SPVS002C marks these. Don't assume a 1:1 pin-to-function mapping.
- **Reset behavior varies between the RESET pin and the RESET instruction.** Subtle — the pin is harder; the instruction is closer to a soft reset that preserves some state. SPVU001A Ch. 13 enumerates.
- **HOLD / HLDA arbitration is rarely used** in practice. Most '34010 systems route arbitration through the host port instead. RTL must still implement HOLD/HLDA correctly per the datasheet for compliance.
- **LINT1 and LINT2 polarity** and edge/level-trigger choice — verify in SPVS002C.

## Implementation hints

- **Group pins as in this document's "Pin groups" subsection** when partitioning the top-level RTL. Each group becomes a clean module boundary.
- **For FPGA targets:** typical TMS34010 boards used 5V TTL; modern FPGAs are 3.3V or 1.8V. Plan level-shifters or use bidirectional voltage-translating buffers on every pin if you want drop-in compatibility with original boards.
- **Document AC parameters as constraints in your synthesis flow** so failing them is a synthesis-time error rather than a board-bring-up surprise.
- **The MAME core does not model AC timing.** Use it as a functional reference only; the datasheet is the only AC reference.

## Cross-references

- Local-bus signal semantics (what each strobe does in each cycle) → `07-memory-interface.md`.
- Host port pin-level behavior → `09-host-interface.md`.
- Display pin functions and pixel-clock domain → `08-video-timing.md`.
- Reset pin behavior in detail → `11-interrupts-reset.md`.
- Clock generation strategy in HDL → `01-architecture.md`.
