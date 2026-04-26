#!/usr/bin/env python3
"""Download TMS340-family source material listed in SOURCES / MANIFEST.

Idempotent: skips files that already exist (path + SHA256). Failures
are logged to wanted/download_failures.md so a future run can pick up
where this one left off.

Use Python stdlib only (urllib, hashlib, csv, argparse). Requires
Python 3.8+.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import socket
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
INCOMING = REPO_ROOT / "incoming"
MANIFEST_CSV = REPO_ROOT / "MANIFEST.csv"
FAILURES_MD = REPO_ROOT / "wanted" / "download_failures.md"

USER_AGENT = (
    "TMS34010_Info-archiver/0.1 "
    "(+https://github.com/Kevin-Coleman/TMS34010_Info; preservation/research)"
)
TIMEOUT = 60  # seconds per request

# Minimum set of bitsavers items to fetch when run with no --csv argument.
# Edit this list as needed; for the full set use --csv MANIFEST.csv.
BITSAVERS_BASE = "https://bitsavers.trailing-edge.com/components/ti/TMS340xx/"
BITSAVERS_TIGA = BITSAVERS_BASE + "TIGA/"
BITSAVERS_TOOLS = BITSAVERS_BASE + "TMS340_Tools_199011/"
BITSAVERS_PATENTS = BITSAVERS_BASE + "patents/"

DEFAULT_SOURCES: list[tuple[str, str]] = [
    # (url, dest_relpath_under_repo_root)
    (BITSAVERS_BASE + "1988_TI_TMS34010_Users_Guide.pdf",
     "docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf"),
    (BITSAVERS_BASE + "1986_TI_TMS34010_C_Compiler_Users_Guide.pdf",
     "tools/compiler/1986_TI_TMS34010_C_Compiler_Users_Guide.pdf"),
    (BITSAVERS_BASE + "1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf",
     "software/graphics-library/1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf"),
    (BITSAVERS_BASE + "1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf",
     "tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf"),
    (BITSAVERS_BASE + "2558670-9761B_TMS34020_Software_Development_Board_Users_Guide_1991.pdf",
     "docs/ti-official/2558670-9761B_TMS34020_Software_Development_Board_Users_Guide_1991.pdf"),
    (BITSAVERS_BASE + "SPPS010A_TMS34061_Video_System_Controller_198602.pdf",
     "docs/datasheets/SPPS010A_TMS34061_Video_System_Controller_198602.pdf"),
    (BITSAVERS_BASE + "TMS34061_Users_Guide.pdf",
     "docs/ti-official/TMS34061_Users_Guide.pdf"),
    (BITSAVERS_BASE + "TMS34082_Designers_Handbook_1991.pdf",
     "docs/ti-official/TMS34082_Designers_Handbook_1991.pdf"),
    (BITSAVERS_BASE + "TLC34075-110FN.pdf",
     "docs/datasheets/TLC34075-110FN.pdf"),
    (BITSAVERS_BASE + "TLC34076.pdf",
     "docs/datasheets/TLC34076.pdf"),
    (BITSAVERS_BASE + "1992_SLAS054_TI_TLC34076_Video_Interface_Palette_Data_Manual.pdf",
     "docs/datasheets/1992_SLAS054_TI_TLC34076_Video_Interface_Palette_Data_Manual.pdf"),
    (BITSAVERS_BASE + "TI_Color_Graphics_Controller_Board_Users_Guide_1986.pdf",
     "hardware/pc-tiga/TI_Color_Graphics_Controller_Board_Users_Guide_1986.pdf"),
    (BITSAVERS_BASE + "TMS34010_Assembly_Language_Tools_Reference_Card.pdf",
     "tools/assembler/TMS34010_Assembly_Language_Tools_Reference_Card.pdf"),
    (BITSAVERS_BASE + "TMS34010_C_Compiler_Reference_Card.pdf",
     "tools/compiler/TMS34010_C_Compiler_Reference_Card.pdf"),
    (BITSAVERS_BASE + "TMS34010_Math_Graphics_Library_Reference_Card.pdf",
     "software/graphics-library/TMS34010_Math_Graphics_Library_Reference_Card.pdf"),
    (BITSAVERS_BASE + "TMS34010_SDB_Pocket_Reference.pdf",
     "docs/ti-official/TMS34010_SDB_Pocket_Reference.pdf"),
    (BITSAVERS_BASE + "34010_devbd.jpg",
     "hardware/pc-tiga/34010_devbd.jpg"),
    (BITSAVERS_BASE + "34020_devbd.jpg",
     "hardware/pc-tiga/34020_devbd.jpg"),
    (BITSAVERS_BASE + "TMS340_Compiler.zip",
     "tools/extracted/TMS340_Compiler.zip"),
    (BITSAVERS_BASE + "TMS340_Compiler_unpacked.zip",
     "tools/extracted/TMS340_Compiler_unpacked.zip"),
    (BITSAVERS_BASE + "tms34010_asm_pkg_1987.zip",
     "tools/extracted/tms34010_asm_pkg_1987.zip"),
    # TIGA originals
    (BITSAVERS_TIGA + "TIGA_DDK_Rel_2_20.imd",
     "tools/original-disks/TIGA_DDK_Rel_2_20.imd"),
    (BITSAVERS_TIGA + "TIGA_DDK_Rel_2_20.jpg",
     "tools/original-disks/TIGA_DDK_Rel_2_20.jpg"),
    (BITSAVERS_TIGA + "TIGA_Disk_Images.zip",
     "tools/original-disks/TIGA_Disk_Images.zip"),
    (BITSAVERS_TIGA + "TIGA_Promo_Kit_Scans.zip",
     "docs/ti-related/TIGA_Promo_Kit_Scans.zip"),
    # Tools 199011 - SDK + libraries + debugger + codegen
    (BITSAVERS_TOOLS + "2564053-1641_TIGA_SDK_r2.01.zip",
     "tools/original-disks/2564053-1641_TIGA_SDK_r2.01.zip"),
    (BITSAVERS_TOOLS + "2564053-1641_TIGA_SDK_r2.01.jpg",
     "tools/original-disks/2564053-1641_TIGA_SDK_r2.01.jpg"),
    (BITSAVERS_TOOLS + "2564059-1641_GFX_LBR_r2.01_d1.zip",
     "tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.zip"),
    (BITSAVERS_TOOLS + "2564059-1641_GFX_LBR_r2.01_d1.jpg",
     "tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.jpg"),
    (BITSAVERS_TOOLS + "2564059-1642_GFX_LBR_r2.01_d2.zip",
     "tools/original-disks/2564059-1642_GFX_LBR_r2.01_d2.zip"),
    (BITSAVERS_TOOLS + "2564059-1642_GFX_LBR_r2.01_d2.jpg",
     "tools/original-disks/2564059-1642_GFX_LBR_r2.01_d2.jpg"),
    (BITSAVERS_TOOLS + "2564059-1643_GFX_LBR_r2.01_d3.zip",
     "tools/original-disks/2564059-1643_GFX_LBR_r2.01_d3.zip"),
    (BITSAVERS_TOOLS + "2564059-1643_GFX_LBR_r2.01_d3.jpg",
     "tools/original-disks/2564059-1643_GFX_LBR_r2.01_d3.jpg"),
    (BITSAVERS_TOOLS + "2564060-1641_C_SRC_DBGR_r5.00.zip",
     "tools/original-disks/2564060-1641_C_SRC_DBGR_r5.00.zip"),
    (BITSAVERS_TOOLS + "2564060-1641_C_SRC_DBGR_r5.00.jpg",
     "tools/original-disks/2564060-1641_C_SRC_DBGR_r5.00.jpg"),
    (BITSAVERS_TOOLS + "2564062-1641_CODE_GEN_TOOLS_r5.01_d1.zip",
     "tools/original-disks/2564062-1641_CODE_GEN_TOOLS_r5.01_d1.zip"),
    (BITSAVERS_TOOLS + "2564062-1641_CODE_GEN_TOOLS_r5.01_d1.jpg",
     "tools/original-disks/2564062-1641_CODE_GEN_TOOLS_r5.01_d1.jpg"),
    (BITSAVERS_TOOLS + "2564062-1642_CODE_GEN_TOOLS_r5.01_d2.zip",
     "tools/original-disks/2564062-1642_CODE_GEN_TOOLS_r5.01_d2.zip"),
    (BITSAVERS_TOOLS + "2564062-1642_CODE_GEN_TOOLS_r5.01_d2.jpg",
     "tools/original-disks/2564062-1642_CODE_GEN_TOOLS_r5.01_d2.jpg"),
    # Patents
    (BITSAVERS_PATENTS + "US5371517.pdf", "docs/patents/US5371517.pdf"),
    (BITSAVERS_PATENTS + "US5465058.pdf", "docs/patents/US5465058.pdf"),
    (BITSAVERS_PATENTS + "US5636335.pdf", "docs/patents/US5636335.pdf"),
    (BITSAVERS_PATENTS + "US5696923.pdf", "docs/patents/US5696923.pdf"),
    (BITSAVERS_PATENTS + "US5696924.pdf", "docs/patents/US5696924.pdf"),
    # TI live URL
    ("https://www.ti.com/lit/an/spra402/spra402.pdf",
     "docs/articles/spra402.pdf"),
]

# URLs that need human review before being committed (legality unclear,
# vendor-proprietary, etc.). Run with --review-only to fetch into
# incoming/needs-review/ instead of the main tree.
REVIEW_ONLY: list[tuple[str, str]] = [
    # Add entries here as questionable sources are discovered.
]


@dataclass
class Result:
    url: str
    dest: Path
    status: str  # "downloaded" | "skipped-exists" | "failed" | "dry-run"
    sha256: str | None = None
    bytes_written: int = 0
    error: str | None = None


def sha256_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            buf = f.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def fetch(url: str, dest: Path, dry_run: bool) -> Result:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return Result(url, dest, "skipped-exists", sha256=sha256_of(dest),
                      bytes_written=dest.stat().st_size)
    if dry_run:
        return Result(url, dest, "dry-run")

    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp, tmp.open("wb") as out:
            shutil.copyfileobj(resp, out)
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout, TimeoutError, OSError) as e:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        return Result(url, dest, "failed", error=str(e))

    tmp.rename(dest)
    return Result(url, dest, "downloaded", sha256=sha256_of(dest),
                  bytes_written=dest.stat().st_size)


def load_csv_sources(csv_path: Path) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    with csv_path.open(newline="") as f:
        for row in csv.DictReader(f):
            url = (row.get("source_url") or "").strip()
            local = (row.get("local_path") or "").strip()
            status = (row.get("redistribution_status") or "").strip()
            if not url or not local:
                continue
            if status == "reference-only":
                continue
            out.append((url, local))
    return out


def append_failure(results: Iterable[Result]) -> None:
    fails = [r for r in results if r.status == "failed"]
    if not fails:
        return
    FAILURES_MD.parent.mkdir(parents=True, exist_ok=True)
    new_file = not FAILURES_MD.exists()
    with FAILURES_MD.open("a") as f:
        if new_file:
            f.write("# Download failures\n\n"
                    "Append-only log of URLs that failed to download. Re-run "
                    "`scripts/download_sources.py` after fixing connectivity "
                    "or finding a new mirror.\n\n")
        f.write(f"## Run at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n\n")
        for r in fails:
            f.write(f"- `{r.url}` -> `{r.dest.relative_to(REPO_ROOT)}`: {r.error}\n")
        f.write("\n")


def report(results: list[Result]) -> None:
    counts: dict[str, int] = {}
    total_bytes = 0
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
        total_bytes += r.bytes_written
    print()
    print("=== summary ===")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]}")
    print(f"  bytes on disk for downloaded/existing: {total_bytes:,}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", type=Path, default=None,
                   help="Source the URL/dest list from MANIFEST.csv "
                        "(uses source_url + local_path; skips reference-only).")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be fetched without downloading.")
    p.add_argument("--review-only", action="store_true",
                   help="Only fetch URLs in the REVIEW_ONLY list, "
                        "into incoming/needs-review/.")
    args = p.parse_args()

    if args.review_only:
        sources = [(u, str(INCOMING / "needs-review" / Path(d).name))
                   for u, d in REVIEW_ONLY]
    elif args.csv is not None:
        sources = load_csv_sources(args.csv)
    else:
        sources = list(DEFAULT_SOURCES)

    if not sources:
        print("no sources to process", file=sys.stderr)
        return 1

    results: list[Result] = []
    for url, dest_rel in sources:
        dest = (REPO_ROOT / dest_rel).resolve()
        # Safety: refuse to write outside the repo.
        if REPO_ROOT.resolve() not in dest.parents and dest != REPO_ROOT.resolve():
            results.append(Result(url, dest, "failed",
                                  error="dest outside repo"))
            continue
        r = fetch(url, dest, args.dry_run)
        flag = {"downloaded": "[+]", "skipped-exists": "[=]",
                "failed": "[!]", "dry-run": "[?]"}[r.status]
        sha_short = (r.sha256[:12] + "...") if r.sha256 else ""
        size = f"{r.bytes_written:>11,}" if r.bytes_written else " " * 11
        err = f"  {r.error}" if r.error else ""
        print(f"{flag} {size}  {sha_short}  {dest_rel}{err}")
        results.append(r)

    append_failure(results)
    report(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
