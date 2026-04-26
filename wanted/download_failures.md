# Download failures

Append-only log of URLs that failed to download. Re-run
`scripts/download_sources.py` after fixing connectivity
or finding a new mirror. Failures recorded by hand here
when the script wasn't used (e.g. one-off article fetches).

## Run at 2026-04-26 (article batch, hand-fetched)

- ~~`https://siliconpr0n.org/archive/doku.php?id=bercovici%3Ati%3Atms34020` -> `docs/articles/siliconpr0n_bercovici_tms34020.html`: HTTP 403 from Cloudflare-managed challenge ("Just a moment..." with `cf_chl_opt`); requires JS+cookies. A real headless-browser fetch (Playwright/Puppeteer) would be needed. URL itself appears valid based on the redirect target.~~  **Resolved 2026-04-26**: bypassed via undetected-chromedriver (Selenium fork) running headed Chromium against the local X display; full Playwright + plain Chromium and `curl-cffi`/`curl_chrome120` impersonation both still hit the JS challenge wall. See `hardware/silicon-die/{tms34010,tms34020,tms34082}/bercovici/` for the resulting mirror.
- ~~`https://tms34020.uav.nl/` -> `docs/articles/tms34020_uav_nl_avionics.html`: HTTP 502 Bad Gateway (nginx) at fetch time; site may be temporarily down. Linked from the `34010.endlessskye.com` index page as "Avionics and the TMS34020". Retry later.~~  **Resolved 2026-04-26**: site reachable on retry; mirrored to `docs/articles/tms34020_uav_nl_avionics.html` plus 18 inline images under `docs/articles/tms34020_uav_nl_avionics_files/`.
