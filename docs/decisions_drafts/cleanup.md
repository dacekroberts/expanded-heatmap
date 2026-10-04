# DECISIONS drafts - cleanup

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-04 - Browser user-agent strings removed from five files; every host serves the project's agent

- **Why:** the owner's user-agent rule of the same day (staging drafts, "The
  reset wave's calls"): a refusal of curl's own agent is a refusal, a
  browser string is never sent to get past it, and the project's identified
  agent (`expanded-heatmap (github.com/dacekroberts/expanded-heatmap)`, the
  one `brief_check.py` and about sixty fetch scripts already send) is
  allowed. Five files still sent a browser string: `scripts/probe_geodata.py`,
  `scripts/screen_rail.py`, `scripts/rank_canada_storefront_density.py`,
  `pipeline/montreal/fetch_sources.py`, `pipeline/dublin/fetch_sources.py`.
- **Measured 2026-10-04,** each host once with curl's default agent and once
  with the project's (ranged GET of one byte, or a small API call):
  - `donnees.montreal.ca`, both Montréal downloads (business survey,
    agglomeration boundary): curl's agent **403 `RBAC: access denied`**;
    project agent **served** (206). Python `requests`' own default agent
    is also served, so the refusal is aimed at curl's agent. The CKAN API
    (`package_show`) serves both.
  - `www.stm.info`, `gtfs.gpmmom.ca` (Montréal's two feeds): both served.
  - `opendata.tailte.ie`, `services-eu1.arcgis.com`,
    `www.transportforireland.ie` (Dublin's register, boundary, feed): both
    served.
  - `bit.ly` to `storage.googleapis.com` (the Mobility Database catalogue),
    `files.mobilitydatabase.org` (feeds 2126, 712, 714),
    `data.calgary.ca`, `data.edmonton.ca`: both served.
  - `probe_geodata.py` and `screen_rail.py` take their hosts from input; the
    two docstring examples (`nlftp.mlit.go.jp`, `data.kric.go.kr`) serve
    both.
- **No host refuses both,** so nothing is flagged as a refusal under the
  rule, and neither published city (Montréal, Dublin) is affected. Montréal
  needed the browser string only because the build never tried the
  project's own agent.
- **Changed:** all five send the project's agent. Montréal's
  `BROWSER_HEADERS`, its `browser=` parameter and
  `config.BUSINESS_NEEDS_BROWSER_HEADERS` are gone; an RBAC refusal now
  stops the fetch and says to record it, not to retry. The same for
  `rank_canada_storefront_density.py`. The literal stays per file, as in
  every other fetch script; a shared constant would be a sweep of all of
  them, not of these five.
- **Internal docs corrected:** Montréal's build brief trap and the
  `add-country` skill's portal table no longer say browser headers are
  required.
- **Not changed, for the owner:** `docs/data_sources/canada.md` (rendered)
  says twice that the Montréal portal needs browser headers (the business
  row and the boundary row). Proposed wording is at review time. The licence
  capture note in `docs/licenses/montreal-licence-donnees-ouvertes.txt` is
  a dated record and stays.
- **Published outputs untouched:** fetch scripts are not run by
  `drift_check.py`, and nothing was re-fetched.
