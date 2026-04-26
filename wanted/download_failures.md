# Download failures

Append-only log of URLs that failed to download. Re-run
`scripts/download_sources.py` after fixing connectivity
or finding a new mirror. Failures recorded by hand here
when the script wasn't used (e.g. one-off article fetches).

## Run at 2026-04-26 (article batch, hand-fetched)

- `https://siliconpr0n.org/archive/doku.php?id=bercovici%3Ati%3Atms34020` -> `docs/articles/siliconpr0n_bercovici_tms34020.html`: HTTP 403 from Cloudflare-managed challenge ("Just a moment..." with `cf_chl_opt`); requires JS+cookies. A real headless-browser fetch (Playwright/Puppeteer) would be needed. URL itself appears valid based on the redirect target.
- `https://tms34020.uav.nl/` -> `docs/articles/tms34020_uav_nl_avionics.html`: HTTP 502 Bad Gateway (nginx) at fetch time; site may be temporarily down. Linked from the `34010.endlessskye.com` index page as "Avionics and the TMS34020". Retry later.
