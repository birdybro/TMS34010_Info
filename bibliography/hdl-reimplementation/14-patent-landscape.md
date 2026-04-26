# 14 — Patent landscape

## Why this matters

The '34010 architecture is described — formally — in a set of US patents filed by Texas Instruments between 1983 and 1995. The foundational set was filed in late 1985 as the chip was being designed. **All of the relevant patents have expired** (as of 2026), so they no longer constrain what an HDL reimplementation can do. They remain useful for two reasons:

1. **Design intent.** The patents describe *why* the architecture is shaped the way it is, often more clearly than the user's guides.
2. **Clean-room derivation.** Because the patents are published, they are a legitimate reference for understanding the architecture without ever touching TI internal documentation. Citing them in your design notes is a clean provenance chain.

## Source-of-truth

The relevant patents are mirrored under `docs/patents/` in this archive. Original filings are at `patents.google.com` or `uspto.gov` for cross-checking.

## Foundational architecture patents (priority chain from late 1985)

### US 4,718,024 — "Graphics Data Processing Apparatus for Graphic Image Operations Upon Data of Independently Selectable Pitch"

- **File:** `docs/patents/US4718024.pdf`
- **Inventors:** Asal, Guttag, Novak / Texas Instruments
- **Filed:** Nov 5, 1985. **Issued:** Jan 5, 1988. **Expired** (20 years from filing pre-1995-rule, though this filed pre-GATT — likely the 17-years-from-issue rule, expiring Jan 2005).
- **What it covers:** The TMS340-family architecture as a whole, with claims around independently-selectable row pitch and arbitrary-bit-address graphics data processing. **Fig. 2 is the canonical TMS34010 block diagram.**
- **What's interesting for HDL:**
  - Block decomposition (CPU + reg files + I-cache + memory IF + special graphics HW + host IF + I/O regs + video display controller).
  - Selectable pitch (CONVDP / CONVSP) is a central claim.
  - The patent narrates 13 sibling applications filed in the same window covering specific subsystems.
- **Sibling continuations** — the patent mentions 13 applications filed in late 1985 / early 1986 by the same group, each on one subsystem. Two issued in their original form: US 5,333,261 (XY instruction) and US 5,437,011 (graphics computer system, system-level). The other 11 may have been abandoned, consolidated, or reissued under different numbers; bitsavers does not have them all in its TMS340 patents folder.

### US 5,333,261 — "Graphics Processing Apparatus Having Instruction Which Operates Separately on X and Y Coordinates of Pixel Location Registers"

- **File:** `docs/patents/US5333261.pdf`
- **Inventors:** Guttag, Asal, Tebbutt, Novak / TI
- **Filed:** May 7, 1993 (continuation of 1985 priority chain). **Issued:** Jul 26, 1994.
- **What it covers:** The XY-pair instructions (`PIXT *Rs.XY,*Rd.XY`, `CMPXY`, etc.) and the underlying coordinate format.
- **What's interesting for HDL:** Direct reference for `06-xy-addressing.md`. The patent walks the XY-instruction design rationale and the coordinate-register layout.

### US 5,437,011 — "Graphics Computer System, a Graphics System Arrangement, a Display System, a Graphics Processor and a Method of Processing Graphic Data"

- **File:** `docs/patents/US5437011.pdf`
- **Inventors:** Guttag, Asal, Van Aken, Tebbutt, Novak / TI
- **Filed:** Feb 4, 1994 (continuation of 1985 priority chain). **Issued:** Jul 25, 1995.
- **What it covers:** System-level claims — host + '34010 + VRAM + RAMDAC as a graphics system.
- **What's interesting for HDL:** Less directly useful than US 4,718,024 for chip-internal design. Useful for `12-system-coprocessor.md` context.

## VRAM patents (the memory the '34010 was built to drive)

### US 4,747,081 — "Video Display System Using Memory with Parallel and Serial Access Employing Serial Shift Registers Selected by Column Address"

- **File:** `docs/patents/US4747081.pdf`
- **Inventors:** Heilveil, Van Aken, Guttag, Redwine, Pinkham, Novak / TI
- **Filed:** Dec 30, 1983. **Issued:** May 24, 1988. **Expired** (issued more than 17 years ago).
- **What it covers:** TI's foundational dual-port VRAM patent. Describes the parallel random-access port plus serial-access port architecture that the '34010 SRT cycle drives.
- **What's interesting for HDL:** Only relevant to the **memory partner**, not the '34010 itself. Useful for understanding why the SRT cycle exists and what VRAM is doing on the other end of it (see `07-memory-interface.md`).

### US 4,663,735 — "Random/Serial Access Mode Selection Circuit for a Video Memory System"

- **File:** `docs/patents/US4663735.pdf`
- **Inventors:** Novak, Guttag / TI
- **Filed:** Dec 30, 1983. **Issued:** May 5, 1987. **Expired.**
- **What it covers:** The mode-selection circuitry inside VRAM that decides between random and serial port access.
- **What's interesting for HDL:** Same as above — VRAM-internal, not '34010-internal. Cite when explaining the SRT cycle's other end.

## Floating-point coprocessor patent

### US 5,025,407 — "Graphics Floating Point Coprocessor Having Matrix Capabilities"

- **File:** `docs/patents/US5025407.pdf`
- **Inventors:** Gulley, Van Aken / TI
- **Filed:** Jul 28, 1989. **Issued:** Jun 18, 1991. **Expired.**
- **What it covers:** The TMS34082 FPU. Matrix-math units, the coprocessor handshake, the bus protocol.
- **What's interesting for HDL:** Useful for `12-system-coprocessor.md`. **Not** the '34010 GPU itself — the patent explicitly distinguishes "graphics processor" (separate block) from "floating-point coprocessor" (the claimed invention). If a user search tags this as "the TMS34010 patent", correct them: this is the '34082-class FPU patent.

## Other TMS340-family patents

Bitsavers' TMS340 patents folder also holds:

- **US 5,371,517** — video palette palette related
- **US 5,465,058** — output buffer Miller-effect circuit
- **US 5,636,335, US 5,696,923, US 5,696,924** — three later '340-family filings (verify topic in each PDF cover page)

Local mirrors at `docs/patents/US5371517.pdf`, `US5465058.pdf`, `US5636335.pdf`, `US5696923.pdf`, `US5696924.pdf`. These are tangential to a clean-room reimplementation of the '34010 itself; cite as needed.

## Clean-room considerations

- **All cited patents are expired.** No active patent claims block an HDL reimplementation of the '34010 in 2026.
- **Using expired patents as design references is legal and standard.** The patent grant has lapsed; the disclosure is in the public record forever.
- **Document your derivation chain** in your project notes:
  - "Block decomposition derived from US 4,718,024 Fig. 2 (expired)."
  - "XY-instruction semantics derived from US 5,333,261 (expired) and SPVU001A Ch. 7."
  - "VRAM SRT scheduling reference: US 4,747,081 (expired)."
- **Trademarks are separate from patents.** "TMS34010" is a Texas Instruments trademark. A clean-room reimplementation can be functionally compatible without using TI's trademarks; call your part something else (e.g., "GSP-compatible core" or a project-specific name).
- **Microcode listings, chip layouts, and TI internal documents are not in the public record** — and to the extent they leaked, they remain TI's trade secrets. Do not consume any leaked-internal TI document in a clean-room flow. The PDFs in this archive are public TI documentation (user's guides, datasheets, designer's handbooks) and public patent filings; both are clean-room safe.
- **MAME is BSD-licensed.** Reading MAME's '34010 implementation is fine for understanding behavior; copying its source verbatim is OK only if you carry the BSD license forward, and clean-room work generally avoids reading reference implementations to keep provenance clean. **If your project goal is patentable / proprietary, prefer the SPVU001A + datasheet + patents path** and treat MAME only as a black-box verification target. **If your project goal is open-source compatible**, reading MAME freely is fine.

## Patent claim summaries (quick reference)

For a reimplementer drafting design notes, the load-bearing claims (paraphrased — read the patents for the actual claim language):

- **US 4,718,024:** A graphics data processor with (a) a register file, (b) an arithmetic unit, (c) a memory interface configured to read/write fields at any bit address with a runtime-selectable field size, (d) special graphics hardware operating on those fields with a runtime-selectable pitch, (e) an instruction cache. *That's the chip.*
- **US 5,333,261:** An instruction that operates on X and Y halves of a register independently — applied to coordinate ops.
- **US 5,437,011:** A system architecture combining (a) a graphics processor, (b) host CPU, (c) shared frame buffer, (d) display output stage. *That's the board.*
- **US 4,747,081 / US 4,663,735:** A memory device with parallel random-access and serial-out ports, with a mode-selection circuit. *That's VRAM.*
- **US 5,025,407:** A floating-point coprocessor with matrix-math units that attaches to a graphics processor over a coprocessor bus. *That's the '34082.*

## Cross-references

- Block decomposition derived from US 4,718,024 → `01-architecture.md`.
- Field-engine and selectable-pitch from US 4,718,024 + sibling continuations → `04-memory-fields-pixels.md`, `06-xy-addressing.md`.
- VRAM SRT cycle → `07-memory-interface.md`.
- '34082 attach → `12-system-coprocessor.md`.
- Original PDF set under `docs/patents/` and listed in the README's Patents section.
