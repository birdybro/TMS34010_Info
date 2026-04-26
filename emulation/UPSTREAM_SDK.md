# tms34010-sdk — upstream SDK mirror

Upstream catalog for the `tms34010guy/tms34010-sdk` GitHub repository, a
community-curated mirror that gathers TMS34010 / TMS340-family SDK
material previously hosted on bitsavers, plus a handful of additional
scans and disk images not in the bitsavers TMS340xx tree.

## Upstream

- Repo: <https://github.com/tms34010guy/tms34010-sdk>
- Pinned commit: `5692b4773328f49010896b7c47ada4f96bea73f8` (default branch `main`, fetched 2026-04-26)
- License: **none stated** — the repo has no `LICENSE` file. GitHub's
  API returns `"license": null`. Per this archive's `LEGAL_NOTES.md`,
  that means the material is treated as `copyright_status: unclear`
  and metadata-only — files are **not** copied into this archive
  unless redistribution is independently established.
- Upstream README excerpt (verbatim): *"Most of this was previously
  hosted on bitsavers, but it was extremely hard to find and sort
  through. Spent some time renaming things, making it more SEO
  friendly and easier to find what you need. ... I believe if TI had
  access to this SDK, they would make it freely available, but they
  unfortunately have lost the archives."*

## Methodology for this catalog

1. Shallow `git clone --depth 1` of the pinned commit into a temp
   directory.
2. `sha256sum` of every file (74 files, ~486 MB on disk).
3. Diff against `MANIFEST.csv` SHA256 column.
4. Anything matching an existing manifest entry is recorded below as
   "exact duplicate of bitsavers mirror, already in archive".
5. Anything novel is listed below as "new vs. archive" with the SHA256
   so a future pass can rehydrate from upstream if a license clarifies.

## Exact duplicates of files already archived

These 35 SDK files are byte-identical (same SHA256) to files already
in `MANIFEST.csv`. No re-commit; the manifest is the canonical record.

| SDK upstream path | SHA256 (truncated) | Already at |
| --- | --- | --- |
| `Docs/SPVU021A TMS340 Family C Source Debugger Users Guide (1991-09).pdf` | `0c57d3a1...` | `tools/debugger/1991_SPVU021A_TMS340_Family_C_Source_Debugger_Users_Guide.pdf` |
| `Docs/SPVU006 TMS34010 Math Graphics Function Library Reference Card (1987).pdf` | `0fc9b044...` | `software/graphics-library/TMS34010_Math_Graphics_Library_Reference_Card.pdf` |
| `Docs/Video Interfaces/SLAS054 TLC34076 Video Interface Palette Data Manual (1992).pdf` | `10b6181e...` | `docs/datasheets/1992_SLAS054_TI_TLC34076_Video_Interface_Palette_Data_Manual.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family C Source Debugger Disk r5.00 rev2564060-1641.jpg` | `1abacf1b...` | `tools/original-disks/2564060-1641_C_SRC_DBGR_r5.00.jpg` |
| `Docs/SPVU005A TMS34010 C Compiler Reference Card (1988-08).pdf` | `21cc7257...` | `tools/compiler/TMS34010_C_Compiler_Reference_Card.pdf` |
| `Docs/SPVU004A TMS34010 Assembly Language Tools Reference Card (1987).pdf` | `2a413a60...` | `tools/assembler/TMS34010_Assembly_Language_Tools_Reference_Card.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (2 of 3) r2.01 rev2564059-1641.jpg` | `2c210007...` | `tools/original-disks/2564059-1642_GFX_LBR_r2.01_d2.jpg` |
| `Docs/SPVU002A TMS34010 Software Development Board Users Guide (1987-05).pdf` | `31f048a2...` | `docs/ti-official/1987_TI_TMS34010_Software_Development_Board_Users_Guide.pdf` |
| `Patents/US5371517.pdf` | `39500634...` | `docs/patents/US5371517.pdf` |
| `Patents/US5696924.pdf` | `3b8a24e3...` | `docs/patents/US5696924.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (2 of 2) r5.01 rev2564062-1641.jpg` | `3f921e86...` | `tools/original-disks/2564062-1642_CODE_GEN_TOOLS_r5.01_d2.jpg` |
| `Patents/US5465058.pdf` | `4c987e6e...` | `docs/patents/US5465058.pdf` |
| `Docs/SPVU002A TMS34010 Software Development Board Users Guide Pocket Reference (1987-05).pdf` | `530f71d5...` | `docs/ti-official/TMS34010_SDB_Pocket_Reference.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family C Source Debugger r5.00 rev2564060-1641.zip` | `61e99023...` | `tools/original-disks/2564060-1641_C_SRC_DBGR_r5.00.zip` |
| `1990-11 TMS340 Family SDK/1990-11-19 TIGA SDK r2.01 rev2564053-1641.zip` | `69cbc13f...` | `tools/original-disks/2564053-1641_TIGA_SDK_r2.01.zip` |
| `Docs/SPVU005 TMS34010 C Compiler Users Guide (1986-12).pdf` | `6e68ca63...` | `tools/compiler/1986_TI_TMS34010_C_Compiler_Users_Guide.pdf` |
| `Docs/SPVU015A TIGA 340 Interface Users Guide (1989).pdf` | `6f6ae74c...` | `tools/tiga/1989_TI_TIGA-340_Interface_Users_Guide.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (1 of 2) r5.01 rev2564062-1641.zip` | `71528248...` | `tools/original-disks/2564062-1641_CODE_GEN_TOOLS_r5.01_d1.zip` |
| `Patents/US5636335.pdf` | `879ece19...` | `docs/patents/US5636335.pdf` |
| `Docs/SPVU006 TMS34010 Math Graphics Function Library Users Guide (1987).pdf` | `9136edee...` | `software/graphics-library/1987_TI_TMS34010_Math_Graphics_Function_Library_Users_Guide.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (1 of 2) r5.01 rev2564062-1641.jpg` | `9c50829d...` | `tools/original-disks/2564062-1641_CODE_GEN_TOOLS_r5.01_d1.jpg` |
| `Docs/SPVU015C TIGA Interface Users Guide (1990-09).pdf` | `a8b1aec3...` | `tools/tiga/SPVU015C_TIGA_Interface_Users_Guide_199009.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (1 of 3) r2.01 rev2564059-1641.jpg` | `b0876633...` | `tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.jpg` |
| `Docs/SPVU005A TMS34010 C Compiler Reference Guide (1988-08).pdf` | `bf9a9b91...` | `tools/compiler/TMS34010_C_Compiler_Reference_Guide_1988.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (3 of 3) r2.01 rev2564059-1641.jpg` | `c4e0fe27...` | `tools/original-disks/2564059-1643_GFX_LBR_r2.01_d3.jpg` |
| `Docs/SPVU004A TMS34010 Assembly Language Tools Users Guide (1987).pdf` | `c67005f7...` | `tools/assembler/TMS34010_Assembly_Language_Tools_Users_Guide_SPVU004.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (1 of 3) r2.01 rev2564059-1641.zip` | `c91987ea...` | `tools/original-disks/2564059-1641_GFX_LBR_r2.01_d1.zip` |
| `Docs/SPVU001A TMS34010 Users Guide (1988-08).pdf` | `e5f9f50c...` | `docs/ti-official/1988_TI_TMS34010_Users_Guide.pdf` |
| `Patents/US5696923.pdf` | `e6093ed5...` | `docs/patents/US5696923.pdf` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (3 of 3) r2.01 rev2564059-1641.zip` | `f12541eb...` | `tools/original-disks/2564059-1643_GFX_LBR_r2.01_d3.zip` |
| `Docs/TMS34010 Software Development Board.jpg` | `f1dfe367...` | `hardware/pc-tiga/34010_devbd.jpg` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Graphics Library (2 of 3) r2.01 rev2564059-1641.zip` | `fb005548...` | `tools/original-disks/2564059-1642_GFX_LBR_r2.01_d2.zip` |
| `1990-11 TMS340 Family SDK/1990-11-19 TMS340 Family Code Generation Tools (2 of 2) r5.01 rev2564062-1641.zip` | `fb199f80...` | `tools/original-disks/2564062-1642_CODE_GEN_TOOLS_r5.01_d2.zip` |
| `1990-11 TMS340 Family SDK/1990-11-19 TIGA SDK r2.01 rev2564053-1641.jpg` | `fee56b1a...` | `tools/original-disks/2564053-1641_TIGA_SDK_r2.01.jpg` |

## Files genuinely new vs. this archive (metadata-only, NOT mirrored locally)

These 39 files exist in the SDK upstream but have no SHA256 match in
`MANIFEST.csv`. **They have NOT been copied into the archive** because
the upstream repo has no LICENSE file and the redistribution status is
`unclear`. To rehydrate any of them later, fetch from the pinned
commit using the path below; SHA256 should match.

### 1987-05 TMS34010 SDK (8 disk images + label scan)

These are the original 1985–1987 TMS34010 SDK floppy disk images. The
bitsavers TMS340xx tree contains the *1990* SDK (as `TMS340_Tools_199011/`)
and the *TIGA DDK* disks, but does **not** contain these earlier 1987-era
floppies. Genuinely novel.

| File | SHA256 | Notes |
| --- | --- | --- |
| `1985-05-20 TMS34010 Assembly Language Package (1 of 4) ASM-LNK-ARCH revD 1604811-1601.img` | `3dd3fe2dd751f3b48ac53409d4c67d72a7564c3c102d3a48acd85de5942d92a9` | Floppy image (368 640 bytes = 360 KB MS-DOS); rev D, 1985-05-20 |
| `1985-05-20 TMS34010 Assembly Language Package (2 of 4) GSPSIM-COMP revD 1604811-1602.img` | `9ba15c34b1add956a002ba1e0f22fc35be41b6e95c67a62baa1fda6a98c52244` | |
| `1985-05-20 TMS34010 Assembly Language Package (3 of 4) GSPSIM-TIPC revD 1604811-1603.img` | `bb0454ab6e73f65b26ca69c18c8c5bfec154202ef6137662036b1d1a02650b92` | |
| `1985-05-20 TMS34010 Assembly Language Package (4 of 4) ROM-DEMO revD 1604811-1604.img` | `5fe40c36e33073b9ce332ff23c6499405ea1f6bef24865f01561476686672115` | |
| `1987-05-19 TMS34010 Sample Function Library Package rev2547232-1601.img` | `e929970e757abf4cbccb49b29d22c8821e86ae4925ba4a13f4610a70791cfa2d` | 360 KB; pub no. 2547232-1601 |
| `1987-11-06 TMS34010 Simulator-C Tools-ASM Tools.img` | `3b4d2633e7722295d550b5673cd309b6997a37a84d6d75de3ba5118d60b18411` | 1.2 MB image |
| `1987-12-03 TMS34010 Graphics Math Function Library r1.0.img` | `e1390cc7efb008785f962269286a71e791978fcecf2258e1130516562996068e` | 1.2 MB image; r1.0 |
| `1987-12-04 TMS34010 GSP Paint.img` | `15b066507b8e9970523706782946ade8121b4f64e5c6958812cd7ae9bd1a6392` | TI's "GSP Paint" demo program |
| `TMS34010_GDK_floppy_labels.png` | `e8fcc75358dc97f682bba74886a2bd66bc0886ea9b5bd5fe61f1c5d55d7576d1` | Composite scan of the disk labels above |

### 1991-07 TIGA Promo Kit and Art Software (12 disk images/labels + 12 scans)

Bitsavers has `TIGA_Promo_Kit_Scans.zip` (the marketing scans, already
mirrored as `docs/ti-related/TIGA_Promo_Kit_Scans.zip`), but this
upstream additionally exposes the individual demo disks as `.DSK`
images and a per-image set of higher-resolution promo scans that are
**not** present in the bitsavers ZIP. Need to verify whether the
contents of bitsavers' ZIP overlap with this set before deciding which
to keep canonical.

| File | SHA256 | Notes |
| --- | --- | --- |
| `Disks/1991-07-18 TIGA Interface Users Guide revB r2564001.DSK` | `87985d1d3a129f195f8aa42fca536019ef7817f796a7500db4264ddcd558f9ac` | TIGA Interface User's Guide rev B disk; pub no. 2564001 |
| `Disks/1991-07-18 TIGA Interface Users Guide revB r2564001.jpg` | `195728d4ba4a0297320d579a78e9014ffbfd0be81bad55454850aa6adce3757a` | Disk label scan |
| `Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Demo Disk (2 of 2) r1.1.DSK` | `109c2811fea1b607758405ef738123901c20a3e30034117062f5bd3ab8d910b2` | "Desktop Artist Demopak" |
| `Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Demo Disk (2 of 2) r1.1.jpg` | `82be2c148d54c6a0c677d82ea919dba184f69e2788a78b763d8aef5d39785c02` | Disk label scan |
| `Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Program Disk (1 of 2) r1.1.DSK` | `3868d16c88d9fbbae67bc6384538f178f6eba092c3c3e7af6df0377b5879fd54` | |
| `Disks/1991 TIGA Promo Kit - Desktop Artist Demopak - Program Disk (1 of 2) r1.1.jpg` | `58269d1ca932a4b01179736d8ad9a76bad8f51aba1a2dc9cf20e6da32709b6fe` | Disk label scan |
| `Disks/TIGA Logo Bitmaps for Windows.DSK` | `83eafb9e480f1f0c47e5b8eda02cff82c097385c6d3cb060c9f5984128a84de3` | TIGA logo bitmap art (Windows-format) |
| `Disks/TIGA Logo Bitmaps for Windows.jpg` | `dff4aeb885304a64d522cbeeccc6244b5a612d976f25d97fedab4785f20de9d1` | Disk label scan |
| `Scans/Front Cover.jpg` | `bd60742f4c27d5efb995020a724785215d24fb7ba3a04dc701c819bb94412400` | TIGA promo kit front cover |
| `Scans/Back Cover.jpg` | `1ffb30aea86a7631e9c7e595c24cafda665ca72a9c75ba2b4eafc3400e086050` | |
| `Scans/Spine.jpg` | `f919654ac44a361683ccb6a2f972719560e7b47888734e9e5776de66cf693b9a` | |
| `Scans/Disk Sleeve (Front).jpg` | `18ff094317e78397728154e8c3ee879d3fa5592360ba48cfd2383c02788d14f7` | |
| `Scans/Disk Sleeve (Rear).jpg` | `73452582bc79a5b44b9ee06215adb350cf3a11dbbbcd5b4dc8b0098b5653587d` | |
| `Scans/Table Card.jpg` | `cba50571426258691613d892f7287d2b3f613ac172940eed31d664947ec2bd70` | |
| `Scans/TIGA Logo (Large).jpg` | `bddb9ee2c8478e1c1bd10e5bfb4903746c1bb98cc8debb96f5f61efd95c9b5ec` | |
| `Scans/TIGA Demo Printout.jpg` | `f0213cd8a68d00f17b4b941da94d6a7f65c55640b11e1a36fc2157a6e18cbf2d` | |
| `Scans/Chip Promo Picture.jpg` | `63b3d8f56675922eb609375f7d0704e5913d898e0e5b14edd76cd8a44683666d` | TI marketing photo of the chip |
| `Scans/BYTE Award Stickers (Big).jpg` | `b2531fdd7a75ad3519c419bdbc6161ad7e67027e4696f25dce2e71f9df78254e` | "BYTE Award" stickers as found in the kit |
| `Scans/BYTE Award Stickers (Small).jpg` | `046d3b5fae5c2dbbfa8510bdcca3b6ef7286b21706aec3cce4f291b7a2dc84af` | |
| `Scans/Promotional Kit Pages.pdf` | `cd072d236c2131d788eca8a1305b0b7471ca785d8e48d3e291f712eede57cf9f` | Combined promo-kit pages |
| `Scans/img354.jpg` | `b039e85dba67890576cff388ed60d208803c21ff543da226acc69cc94e1639af` | Numbered promo scan |
| `Scans/img355.jpg` | `99d9756192114c280241781e01b430ab49e8af60103034767c19ff6a83e82942` | Numbered promo scan |

### Docs/ — additional manuals not in bitsavers' TMS340xx tree

| File | SHA256 | Notes |
| --- | --- | --- |
| `SPVU001 TMS34010 Users Guide (1986).pdf` | `55e7f28a38bce1c050585abe682e464d8d612bc65bbe95440c92ce4ffdd6bef2` | **Earlier** edition of the '34010 User's Guide (1986). Bitsavers has the 1988 SPVU001A revision; this is the 1986 first edition. Worth a follow-up to compare pagination and which features were added between revisions. |
| `SPVS002A TMS34010 Graphics System Processor Production Data (1987-07).pdf` | `d208783b672fce799820eaace03e0811c41db19b96842b6b8b7e55c00750ceb1` | **Earlier** 1987-07 datasheet revision. The archive currently has SPVS002C (1991-06) at `docs/datasheets/84292.pdf`. SPVS002A pre-dates that. |
| `SPVS002C TMS34010 Graphics System Processor Production Data (1991-06).pdf` | `93dd8f0dd6c2bda2f9111a9c1324321ee35f43d176edf0ddab322bbeb48e7639` | The same SPVS002C as our local `docs/datasheets/84292.pdf`, but a *different SHA256*. Means the upstream repo's PDF was rescanned / recompressed independently of the alldatasheet mirror we used. Worth comparing later to see which scan is cleaner. |
| `SPVU018A Tiga Interface Art (1990-09).pdf` | `788421e3a7c4ee7925b3c88f529b5f8a4054074b89c0deaf083876f5da8aeef4` | **TIGA Interface Art** — a TIGA companion document not currently in the archive. Likely covers the TIGA logo / iconography conventions. Needs scope review before mirroring. |
| `SPVU027 TMS340 Graphics Library (1990-08).pdf` | `7e17b06920b6584fcd943af8678cc10a58e3a430c203663e2636d76583796f1e` | Same SPVU027 the archive already has (`software/graphics-library/spvu027.pdf`), but again a *different SHA256* — different scan/recompression. |

### Docs/Video Interfaces/ — TLC34074/075/076 datasheets (1995 production data)

| File | SHA256 | Notes |
| --- | --- | --- |
| `XLAS056 TLC34074 Video Interface DAC Production Data (1995-05).pdf` | `01721d77fba3f828cda781ca6a8001521a80ee4bcc829d2f50b665a6a5671e27` | Newer (1995) datasheet for the TLC34074. Not in the bitsavers TMS340xx mirror. |
| `XLAS058 TLC34075A Video Interface Palette Production Data (1995-05).pdf` | `f0814501991ef6b5c6eb9f00520f55d6b53aded03a4966bd33a737cef667e5ba` | TLC34075**A** revision (1995); we have the older `TLC34075-110FN.pdf` already. |
| `XLAS076 TLC34076 Video Interface Palette Production Data (1995-05).pdf` | `386fbe3884311d4279ecd2bf3223460ea3888f479315d06dad1a7dac32fc2b1b` | TLC34076 (1995); supersedes the undated `TLC34076.pdf` we already have. |

### Repository metadata

| File | SHA256 | Notes |
| --- | --- | --- |
| `README.md` | `f5d35e05e3eeb4ab7c910a0602d3cfd5456656657b2bd7db4fda8eeaa3fd8b87` | Upstream README (excerpted above). |

## Recommended next actions

1. **Open an issue or PR upstream asking for a LICENSE file.** The
   author's README implies they want this preserved and freely shared
   ("if TI had access to this SDK, they would make it freely
   available"). A `CC0` or `Unlicense` declaration would let this
   archive mirror the genuinely-novel files (the 1987-era SDK floppies
   and the 1991 TIGA Promo Kit individual scans, which are the most
   historically valuable).
2. **Cross-check `bitsavers.../TIGA/TIGA_Promo_Kit_Scans.zip` against
   the `1991-07 .../Scans/` set.** Likely overlap; if the upstream
   set is a strict superset and a license is granted, the bitsavers
   ZIP can be replaced with the higher-resolution individual files.
3. **Add the 1987-era TMS34010 SDK floppy images to `WANTED.md`** as
   a citation. They are not on bitsavers and are the canonical source
   for the original 1985–1987 TMS34010 toolchain (revisions of
   ASM/LNK/ARCH, GSPSIM, the 1987 Sample Function Library Package,
   and the 1987 GSP Paint demo).
4. **Compare SPVU001 (1986 first edition) to SPVU001A (1988 revision)**
   to see what changed between the first-silicon manual and the second
   public revision.
5. If the user wants to vendor the SDK as a submodule (analogous to
   the proposed MAME submodule scheme), pin to commit
   `5692b4773328f49010896b7c47ada4f96bea73f8`.
