# 09 — Host interface

## Why this matters

The '34010 is normally used as a coprocessor: a host CPU (8086, 68000, 286, etc.) issues commands and reads results, and the '34010 does the graphics work. The host port is the dedicated channel for that — a memory-mapped window on the host's bus that exposes a 32-bit pointer + 16-bit data view into '34010 local memory, plus a small set of control / message bits in each direction. **Both sides of this interface have to be modeled** if you want to drop your reimplementation into a real or emulated TIGA-style system.

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 11 ("Host Interface").** This is the definitive chapter — it walks **both** the '34010-side view and the host-side view of the same registers, and the host-port-vs-local-bus arbitration. Read it before writing host-port RTL.
- **`docs/datasheets/84292.pdf` (SPVS002C), "Host Interface" section** for the pin-level signals and AC characteristics.
- **`tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf`** — the TIGA host-software API. Reading this alongside SPVU001A Ch. 11 makes it clear what message-passing patterns the host expects to be able to drive.

## What the host sees

From the host CPU's bus, the '34010's host port appears as a small window (typically four or so 16-bit registers) of memory-mapped I/O. The conventional layout (verify in SPVU001A Ch. 11):

| Host-side register | Function |
| --- | --- |
| HSTADRL | Host address low (low 16 bits of the pointer into '34010 memory) |
| HSTADRH | Host address high (high 16 bits) |
| HSTDATA | Data port — host reads/writes are routed by the chip to/from `[HSTADRH:HSTADRL]` in '34010 memory |
| HSTCTL | Host control: message-out, interrupt-in, ready/done flags, increment-on-access bit, byte-swap, etc. |

Behavior:

1. Host writes HSTADRH / HSTADRL with a target bit address.
2. Host reads or writes HSTDATA → the chip translates that into a local-bus cycle on the '34010 side, fetching or storing 16 bits at the addressed location.
3. If the auto-increment bit in HSTCTL is set, HSTADR advances by 16 bits per HSTDATA access. Lets the host stream a block of memory through HSTDATA without re-issuing the pointer per word.
4. HSTCTL provides bits for the host to assert "I have a message" (which raises an interrupt on the '34010 side) and to read "the chip has a message for me" (which the chip raises by setting that bit, optionally with an interrupt to the host).

## What the '34010 sees

From the '34010 side, the same physical resources appear in its own I/O register page (`HSTCTLL`, `HSTCTLH`, `HSTDATA`, `HSTADRL`, `HSTADRH`). But:

- The chip does not normally read HSTDATA from its own side — HSTDATA is the host's view of the chip's RAM, not a separate buffer.
- The chip can read HSTCTLL / HSTCTLH to see the host's message bits and interrupt-in bits.
- The chip can write HSTCTLL / HSTCTLH to set its own outbound message bits and to acknowledge inbound ones.
- The host's address (HSTADRL/H) is visible to the chip too, mostly for diagnostic / arbitration purposes.

**The two sides see different bit fields in HSTCTL.** A given physical bit might be readable-by-host / writable-by-chip, or vice versa. SPVU001A Ch. 11 tabulates which side sees which bit how. **You must read that table before designing the RTL, or you will create a chip that the host can't talk to.**

## Pin-level signals

Approximate inventory (verify pin names + count against SPVS002C):

- **HD0–HD15** — host data bus (16 bits).
- **HCS** — host chip select.
- **HRD, HWE** — host read / write strobes (or `HE` + `HRW` depending on bus mode).
- **HFS0, HFS1** — host function select. Two bits selecting which host-side register (HSTADRL, HSTADRH, HSTDATA, HSTCTL) the access is to.
- **HRDY** — host ready / wait. The chip asserts this to extend host bus cycles when the local bus is busy.
- **HINT** — host interrupt output (chip → host).
- **HBYTE** (or similar) — byte-mode select for hosts that want byte-wide rather than word-wide access.
- **HLDS, HUDS** — host lower/upper data strobes for byte-mode access on hosts that use them (68000-style).

The '34010 supports several host bus styles (Intel-style strobes, Motorola-style strobes) — selectable via pin strapping. SPVS002C lists the modes.

## Arbitration with the local bus

When the host accesses HSTDATA, the chip has to perform a local-bus cycle on the '34010 side to fulfill it. This means:

- The host's access has to wait, in general, for the next available local-bus cycle.
- HRDY is asserted to extend the host cycle until the local bus completes.
- If the '34010 CPU is mid-instruction, the host typically waits for the next cycle boundary; some atomic operations cannot be interrupted.

The chip implements an arbitration policy (configurable via a HSTCTL bit) that biases priority toward host or '34010 — useful for systems where the host is latency-sensitive vs. systems where the '34010 needs deterministic CPU cycles.

## Message-passing protocol

The standard TIGA-style usage:

1. Host writes a "command block" structure to '34010 memory via HSTADR + HSTDATA stream.
2. Host raises MSGIN bit in HSTCTL (host-side write).
3. The MSGIN bit causes an interrupt on the '34010 side (if enabled).
4. '34010 ISR reads the command block, executes it, writes results back to memory.
5. '34010 raises MSGOUT bit in HSTCTL (chip-side write).
6. MSGOUT causes an interrupt on the host side via HINT (if enabled).
7. Host ISR reads results, optionally clears MSGOUT.

Variations exist; the contract is: **a small set of bits in HSTCTL serves as a doorbell in each direction, and a 16-bit data-port can stream arbitrary command/result structures through '34010 memory**. The interrupt connection in each direction is configurable.

## NMI / reset over host port

Some bits in HSTCTL let the host force the '34010 into reset, NMI, or a halted state. This is used by host-side debuggers and by the C source debugger (SPVU021A). RTL must implement these as the host's path to in-system debugging.

## Gotchas

- **Bit roles differ per side.** The same physical bit might be read-only from one side and read/write from the other; some bits raise interrupts on the *other* side when set. Build the HSTCTL register as a per-bit struct with explicit "writable from host", "writable from chip", "reads as", "raises chip interrupt", "raises host interrupt" attributes. Do **not** treat it as a single 16-bit register.
- **Auto-increment is per-access, including reads.** A host reading HSTDATA twice with auto-increment on advances the pointer twice. This is conventional but easy to forget when modeling.
- **Address increment unit.** The auto-increment is "advance by one access width" — so 16 bits per HSTDATA word access if the host bus is wired 16-wide. Byte-mode access advances by 8 bits.
- **HRDY behavior must be exact.** If you don't assert HRDY long enough for the local bus to actually complete the cycle, the host gets stale data and silently corrupts the transfer.
- **Host bus mode (Intel vs. Motorola strobes) is pin-strapped.** Hardcoding the wrong style means the chip won't talk to the intended host CPU at all.
- **Byte-mode host access** has its own corner cases — endianness on byte transfers, byte-strobe ordering. SPVU001A Ch. 11 covers both endian modes.
- **Reset-via-host-port** is real and load-bearing. Debugger workflows depend on the host being able to forcibly reset the '34010 without yanking the system reset pin.

## Implementation hints

- **Treat the host port as its own clean module.** Inputs from host bus pins, an arbitration interface to the local bus, an interrupt output to the host, and an interrupt input to the chip's interrupt controller. The internal state is one set of latches for HSTADR / HSTCTL plus the auto-increment counter.
- **Implement HSTCTL as 16 individually-attributed flip-flops**, not a single register. Each flip-flop has its own read/write/raise-interrupt behavior.
- **Local-bus arbitration request goes through the same arbiter as refresh and SRT.** Priority configurable via the HSTCTL bit.
- **Test with the C source debugger ROM image** if you can — it exercises the host port deeply, including reset-via-host. See `tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf` and the original disk images in `tools/original-disks/`.

## Cross-references

- Local-bus arbitration that the host port competes with → `07-memory-interface.md`.
- Interrupt routing in both directions → `11-interrupts-reset.md`.
- Reset-via-host-port mechanics → `11-interrupts-reset.md`.
- Host-side software model (TIGA) → `tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf`.
