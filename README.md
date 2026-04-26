# TMS34010_Info

An archive of original Texas Instruments documentation for the **TMS340 graphics processor family** (TMS34010 and TMS34020), intended as a corpus for AI-driven analysis. The TMS340 family is a line of 32-bit graphics-oriented CPUs from the late 1980s / early 1990s, used in arcade hardware (Mortel Kombat, NBA Jam, Smash TV, etc.), early PC graphics accelerators, and graphics workstations.

This repository contains **PDF source documents only** — no code.

## Documents

### Silicon

| File | TI doc # | Description |
| --- | --- | --- |
| `84292.pdf` | SPVS002C | **TMS34010 Graphics System Processor** datasheet (June 1986, revised June 1991). Pinout, electrical characteristics, register summary, instruction-set overview. |
| `2564006-9721_TMS34020_Users_Guide_Aug90.pdf` | 2564006-9721 | **TMS34020 User's Guide** (August 1990). Full reference for the second-generation '34020 part — architecture, instruction set, I/O registers, host/local bus, video timing. The big one (~63 MB). |

### Tools (assembler / compiler / development board)

| File | TI doc # | Description |
| --- | --- | --- |
| `TMS34010_Assembly_Language_Tools_Users_Guide (SPVU004).pdf` | SPVU004 | **Assembly Language Tools User's Guide** — assembler, linker, archiver, COFF object format. |
| `TMS34010_C_Compiler_Reference_Guide_1988.pdf` | — | **TMS34010 C Compiler Reference Guide** (1988) — language extensions, runtime conventions, optimizer notes. |
| `1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` | — | **Software Development Board User's Guide** (1987) — TI's PC-hosted '34010 dev/eval board. |

### Graphics libraries / host APIs

| File | TI doc # | Description |
| --- | --- | --- |
| `spvu027.pdf` | SPVU027 | **TMS340 Graphics Library User's Guide** (August 1990) — graphics primitives library shipped with the TI toolchain. |
| `TI_TMS340_Family_Graphics_Library.pdf` | SPVU027 | **Duplicate of `spvu027.pdf`** (byte-identical). Kept for now; safe to remove. |
| `1989_TI_TIGA-340_Interface_Users_Guide.pdf` | — | **TIGA-340 Interface User's Guide** (1989) — earlier edition of the TIGA host-side API for PC graphics boards. |
| `TIGA Interface Users Guide (SPVU015C) sept1990.pdf` | SPVU015C | **TIGA Interface User's Guide** (Sept 1990) — later, more complete revision of the same TIGA API. |

### Ecosystem

| File | TI doc # | Description |
| --- | --- | --- |
| `1990-340-Family-THIRD-PARTY-GUIDE-4th-edition.pdf` | — | **TMS340 Family Third-Party Guide, 4th edition** (1990) — catalog of third-party hardware boards, software, and libraries available for the '340 family. Useful for historical context on the ecosystem. |
