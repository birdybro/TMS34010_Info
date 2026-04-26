# 08 — Video timing controller

## Why this matters

The '34010 has an on-chip programmable display controller — it is not just a CPU with graphics ops. The display controller drives HSYNC, VSYNC, BLANK, and pixel-clock-domain signals, schedules VRAM SRT cycles to keep the serial port refilled, and raises the display interrupt at programmed scanlines. **Software programs CRT timing directly via I/O registers.** No external CRTC is needed for basic systems (though the '34061 VSC provides a heavier alternative).

## Source-of-truth

- **`docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` (SPVU001A), Chapter 10 ("Display Operations").** The full programmer's view of HESYNC/HEBLNK/HSBLNK/HTOTAL, the vertical analogues, DPYSTRT, DPYTAP, DPYINT, DPYCTL.
- **`docs/datasheets/84292.pdf` (SPVS002C), "Display Timing" / "Video Output" sections** for the AC characteristics on VCLK, the SRT-cycle timing, and the display-related pin definitions.
- **`docs/ti-official/TMS34061_Users_Guide.pdf`** — only relevant if you are studying the **alternative** companion-chip path (system uses '34061 instead of '34010 native display controller). For an MVP, ignore.

## Programming model

The display controller has a small set of I/O registers programmed by software at boot or mode-change. They divide into horizontal-timing, vertical-timing, frame-buffer-pointer, and control:

### Horizontal timing

Counted in **VCLK periods** (the pixel-clock-domain count), measured from a reference edge:

| Register | Meaning |
| --- | --- |
| HESYNC | End of horizontal sync (sync ends at this count) |
| HEBLNK | End of horizontal blanking (active video begins) |
| HSBLNK | Start of horizontal blanking (active video ends) |
| HTOTAL | Total horizontal period (loop point) |

Order of events per scanline: counter resets at 0 (start of HSYNC) → HSYNC pulse runs until HESYNC → blanking continues until HEBLNK → active video runs until HSBLNK → blanking until HTOTAL → reset.

So `HESYNC < HEBLNK < HSBLNK < HTOTAL` and they are all measured from the same zero point.

### Vertical timing

Counted in **scanlines**, with the same monotonic relationship:

| Register | Meaning |
| --- | --- |
| VESYNC | End of vertical sync |
| VEBLNK | End of vertical blanking (active frame begins) |
| VSBLNK | Start of vertical blanking (active frame ends) |
| VTOTAL | Total vertical period |

### Frame buffer pointers

| Register | Meaning |
| --- | --- |
| DPYSTRT | Bit address of the first pixel of the frame buffer (top-left) |
| DPYTAP | Bit-tap into DPYSTRT for sub-row scrolling — controls where within a row the SRT cycle starts |
| DPYCTL | Master display-control bits: enable, interlace, mode, vertical/horizontal scroll bits |

DPYSTRT can be changed at any time; the new value takes effect at the next VSYNC (or immediately, depending on a DPYCTL bit). This is how page-flipping works.

### Display interrupt

| Register | Meaning |
| --- | --- |
| DPYINT | Scanline number at which to raise the display interrupt |

DPYINT lets software synchronize to a particular scanline. Used for split-screen effects, mid-frame palette changes, vertical-blank handlers that need precise timing, etc. See `11-interrupts-reset.md`.

### Status readback

A "current scanline" / "current display position" register exists (the exact name varies by reference — sometimes `DPYSTL`, sometimes a field of `DPYCTL`). Software can poll the current scanline to busy-wait for VSYNC. SPVU001A Ch. 10 names it precisely.

## SRT scheduling

For VRAM-based systems, the display controller issues a shift-register transfer cycle once per scanline (or once per *N* scanlines if the SAM is wide enough), at a defined point in the horizontal blanking interval. This:

1. Loads the VRAM serial-output register with the next row of pixels.
2. Then VRAM clocks pixels out the serial port at VCLK rate during active video.
3. Frees the local bus for CPU work during the rest of the scanline.

Programmer-visible: software just writes DPYSTRT and lets the hardware do it. The scheduler is internal to the chip.

For non-VRAM (FPGA / BRAM) implementations, replace SRT with a line-buffer fill that pulls from the model's internal memory at the same scanline boundary. See `07-memory-interface.md`.

## Output signals

Pin-level (verify against SPVS002C pin list):

- **VCLK** — pixel clock (input or output depending on configuration).
- **HSYNC** — horizontal sync output.
- **VSYNC** — vertical sync output.
- **BLANK** (or `BLANKB`) — blanking signal output. Active during both HSYNC and HBLANK.

The chip drives these from the programmed timing. The pixel data itself comes from the VRAM serial port — the '34010 does not output pixels on its own pins. (This surprises some readers: the '34010 is a CRTC for sync timing but a RAMDAC-pairing companion for actual color output.)

## Pixel-clock domain

VCLK is independent of the CPU clock. The display controller has its own counter in the VCLK domain, and the local bus (LCLK domain) is synchronized to it through the SRT scheduler. Two clock domains in your HDL — keep the boundary clean:

- **CPU / bus domain (LCLK):** instruction execution, local memory cycles, host port.
- **Pixel / video domain (VCLK):** display counter, HSYNC/VSYNC generation, SRT trigger to bus domain, BLANK output.

The crossing in the typical implementation: the display controller is in VCLK domain and asserts an SRT-request to the bus arbiter (LCLK domain). The bus arbiter responds with a single SRT cycle on the local bus. CDC machinery (a request flag and an ack flag, registered into both clocks) is the canonical clean-room fix.

## Interlace and mode bits

DPYCTL contains bits for:

- Display enable / disable
- Interlace mode
- Display address-mode (linear vs XY — affects what DPYSTRT means)
- Possibly the auto-load behavior for DPYSTRT at VSYNC

Read SPVU001A Ch. 10 for the per-bit list. Interlace mode is the most likely-to-be-buggy in a reimplementation; many board designs ran progressive only.

## Companion chip path: '34061 VSC

If your target system uses the '34061 instead of (or in addition to) the '34010's built-in controller, the display I/O register set on the '34010 side becomes mostly idle and the '34061 handles its own timing. The '34010 generates pixel reads on the local bus and the '34061 handles VRAM SRT scheduling. Reference: `docs/ti-official/TMS34061_Users_Guide.pdf`.

For a clean-room '34010 HDL implementation, you don't need to model the '34061. It is a separate chip on the system board.

## Gotchas

- **All horizontal counts are in VCLK periods, not in pixels.** PSIZE doesn't enter into HSYNC/HBLANK timing — it only enters into how many VCLK periods of active video produce one pixel from VRAM. In practice software computes the values such that `HSBLNK - HEBLNK = active_horizontal_pixels * pixel_clocks_per_pixel`.
- **HTOTAL must equal the actual total period.** Off by one and you get rolling pictures. Off by hundreds and the monitor refuses sync.
- **DPYSTRT updates are sometimes delayed.** A DPYCTL bit selects "update DPYSTRT immediately" vs "update at next VSYNC". Page-flipping code relies on the latter; flicker-free updates depend on it.
- **DPYTAP scrolls within a row.** The combination of DPYSTRT (which row) + DPYTAP (which bit-offset within the row) gives byte- or sub-pixel scrolling without changing the frame-buffer layout. Software uses this for hardware-accelerated panning.
- **Display interrupt fires once per frame.** Setting DPYINT to a specific scanline gives that one interrupt. For multiple per-frame interrupts, software reprograms DPYINT inside the handler.
- **The two clock domains.** Forgetting to register-cross the SRT request gives a chip that "almost works" but glitches at frame boundaries. CDC discipline is mandatory.
- **HSYNC / VSYNC polarity.** Often programmable (active-high or active-low) via a DPYCTL bit. Get it wrong and a real CRT flips colors or refuses to lock; an LCD usually just shows a black screen with no error.
- **VCLK can be input or output** depending on system mode. SPVS002C specifies both. The choice is set by external pin strapping, not by software.

## Implementation hints

- **Build the horizontal counter in VCLK domain first.** Stand-alone module: counts 0..HTOTAL-1, generates HSYNC/HEBLNK/HSBLNK/BLANK signals from comparator outputs. Verifiable in isolation.
- **Then the vertical counter, ticked by HSYNC end.** Same pattern with VESYNC/VEBLNK/VSBLNK/VTOTAL.
- **Then the SRT scheduler and CDC.** Trigger SRT request at a defined HBLANK position; cross to LCLK domain; ack back.
- **Then DPYINT and the display-interrupt path.** Comparator on the vertical counter, edge-detected, flagged into the interrupt controller.
- **DPYSTRT update logic** — registered double-buffer if "update at VSYNC" mode; pass-through otherwise.

## Cross-references

- SRT cycle on the local bus → `07-memory-interface.md`.
- Display interrupt as one of the interrupt sources → `11-interrupts-reset.md`.
- I/O register page address layout for the display registers → `03-registers.md`.
- Companion '34061 VSC for alternative system pairings → `12-system-coprocessor.md`.
