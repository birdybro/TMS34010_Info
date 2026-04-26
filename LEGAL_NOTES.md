# Legal notes

This repository is a **preservation and research archive** focused on the Texas Instruments TMS340 graphics processor family (TMS34010, TMS34020, and related companion parts). It is not a distribution channel for current commercial software.

## Goals

- Preserve historical technical documentation (datasheets, user's guides, application notes, reference cards) that is otherwise scattered across volunteer mirrors.
- Catalog and provide pointers to original development tools (compilers, assemblers, debuggers, TIGA SDK, graphics libraries) released by TI between roughly 1986 and 1992.
- Record where '34010 / '34020 silicon was actually used (arcade boards, PC graphics accelerators, workstations, embedded systems) so the documentation can be tied back to real hardware.
- Provide enough metadata (source URL, SHA256, date) that anyone can reproduce the archive and verify provenance.

## What is NOT redistributed here

The following are **out of scope** for this archive and must not be committed:

- Commercial arcade ROMs (program ROMs, sound ROMs, graphics ROMs from Midway, Atari Games, Williams, etc.).
- BIOS ROMs from PC graphics boards or workstations.
- Commercial game binaries or game assets.
- Proprietary drivers, SDKs, or support libraries from third-party vendors where a redistribution license is not clearly granted.
- Anything explicitly marked confidential, NDA, or "internal use only" by the original publisher.

If a contributor uncovers such material, the appropriate action is to record a citation (source URL, date, contact) — not to commit the binary.

## Classification used in `MANIFEST.csv`

The `redistribution_status` column uses one of:

- `public` — explicitly public-domain or freely redistributable (e.g. US patent grants).
- `archival` — long-running volunteer mirrors (bitsavers and similar) have hosted the material publicly for many years without takedown; redistribution is widely understood to be tolerated for preservation but is not formally licensed. Treat as best-effort preservation.
- `unclear` — copyright holder identifiable, no explicit license known. Treat conservatively. Default for original TI manuals.
- `restricted` — known to be under active redistribution restriction; metadata only, no binary in this repo.
- `do-not-redistribute` — explicitly off-limits (NDA material, leaked sources, ROMs, etc.).
- `pending-download` — listed as a target but not yet archived locally; may move to one of the above once fetched and reviewed.
- `reference-only` — pointer to an external mirror (alldatasheet, TI live URL, etc.); not mirrored locally.

## TI material specifically

Most '340-family manuals were copyright Texas Instruments, late 1980s / early 1990s. TI has not, to our knowledge, issued a blanket public-domain or free-redistribution grant for them. They have been mirrored on bitsavers and similar archives for two decades without known takedown action — that is the basis for `archival` status. If TI requests removal, comply.

## Patents

US patents (e.g. `US5025407`, `US5371517`, `US5465058`, `US5636335`, `US5696923`, `US5696924`) are public records and are safe to redistribute as-issued.

## Emulator source code

Where the upstream license permits (e.g. MAME's BSD-3 / GPL components), files can be vendored, mirrored, or pulled in as a git submodule. The default policy is to **record upstream URL + commit hash + relevant paths** rather than full-clone, because:

- MAME alone is multi-GB and rarely needs to live inside this archive.
- Submodule pinning is more useful than mirroring for tracking which version of a CPU core matches a given finding.

If a full MAME mirror is later approved by the user, add it as a git submodule and pin a tag.

## Receiving takedown / clarification requests

If you are a rightsholder and want material removed, file an issue or contact the repo owner. Provide identification and the specific path(s) in question. Removals will be honored without prejudice; an entry will be added to `WANTED.md` so the missing item is at least discoverable as a citation.
