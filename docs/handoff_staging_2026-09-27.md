# Handoff - staging role (2026-09-27)

For the new Staging session taking over from the one that ran 2026-09-21 to
2026-09-27. Read once; follow the pointers. Keep it short: delete a section
when its priority is done rather than adding an addendum.

## Before starting

- **Work in `.claude/worktrees/staging` on `worktree-staging`.** Run
  `git branch --show-current`; if you are anywhere else, stop and say so. The
  previous Staging session must be closed first (two sessions in one tree
  overwrite each other's uncommitted edits).
- `git fetch` and `git merge origin/master`, then `get_usage` before big
  work. **The owner stops at 98% of the 5-hour window.**
- **Push ritual**: fetch, merge (a `DECISIONS.md` conflict is resolved with
  `python scripts/merge_append_only.py DECISIONS.md`), then
  `python scripts/decisions_index.py`, then push `HEAD:master` and
  `HEAD:worktree-staging`. Re-fetch immediately before pushing.
- **Nothing is in flight.** No agents running, nothing uncommitted, and every
  download is already in the main checkout's `data/`
  (`check_worktree_data.py` passes).

## Where the state lives

- `docs/city_master_list.md`: **64 candidates**, A 9 · C 13 · T 32 · D 10,
  33 discards. The owner's chat format for it is in memory
  (`feedback_master_list_format.md`): read the counts off the file, never
  from here.
- `DECISIONS.md`, the 2026-09-27 entries: first blocker wins / Band T; the
  East Asia screen; wave 1 banded (with Cleanup's tram list); Daegu's and
  Busan's licences.
- `PLAN.md`, "Second-city screens, 2026-09-27": the open items.
- `docs/data_sources.md`, "Daegu and Busan (candidates, not built)": both
  licence positions.
- `docs/global_country_shortlist.md`, first section: the method used for each
  country in wave 1.

## The old session's scratch (read-only; do not write there)

- **Scratchpad**:
  `C:\Users\dacek\AppData\Local\Temp\claude\C--Users-dacek-Documents-Portfolio-expanded-heatmap\0b2764e2-fcfd-416a-accf-2da6f76c8d2f\scratchpad\`
- **Durable copy** of the part that matters, in case Windows clears Temp:
  `data\_staging_scratch_2026-09-27\` in the MAIN checkout (gitignored). It
  holds `second_cities\` and `licence_busan\`.
- **Inside `second_cities\`:**
  - `COMMON_BRIEF.md`: the shared brief wave-1 screen agents worked from.
    Reuse it for wave 2, but **fetch OSM through `pipeline.osm.fetch`**, not
    `ovp.py` (the all-zero-count guard; see PLAN).
  - `korea\`: `dg_*` (Daegu's file ids: `dg_ids.json`, the `dg_views_*.json`
    groups), `bs_*` (Busan's API: `bs_ops.json` and `bs_pull.py`), `gg_*`
    (Gyeonggi), `ic_*` (Incheon), `xl_profile.py`, `lic_daegu\` (licence
    captures) and `klid_probe\`.
  - `france\screen_results.csv`, `france\stations\<slug>.csv` and
    `france\gtfs_rail.txt`: the numbers behind Band T's French rows.
  - `czechia\business_results.json` and the `gtfs_tram_stops_*.csv` files;
    `denmark\` (the OSM-to-DAR join controls); `netherlands\`, `norway\`,
    `latvia\`.
  - `ovp_routes_{KR,TW,HK,MO}.json`: OSM rail enumerations by country.

## Priorities, in order

1. **Daegu's brief** (`docs/build_briefs/daegu.md`, with a `brief-checks`
   block), then hand it to main. It is the recommended next Korean city.
   - Seoul's modules carry over (`korea_localdata`).
   - The licence is a disclosed reasoned position; its credit and the removal
     line are in `data_sources.md`.
   - Still unmeasured: the XLSX columns (a phone column is implied, so select
     by exact name), and the sibling files for bakeries, butchers,
     health-food, barbers, laundries and baths.
   - Rail is OSM, 86 stops.
2. **Busan's brief.**
   - The keyless API is frozen at 2026-04-15, and the owner accepted that
     snapshot, with the date on the page.
   - Never publish `sitetel`.
   - Credit: Busan's Big-데이터웨이브 plus the Ministry's licence data.
   - Scope question: the Busan–Gimhae LRT's 12 Gimhae stations.
3. **Held by the owner. Do not start without the owner's word:**
   - **Tram rescopes of built cities**, likely at a reset. Cleanup's
     case-by-case list is in the DECISIONS "Wave-1 ... banded" entry.
     Missing counts: Seoul's Wirye line, and Hong Kong's and Barcelona's
     trams (no tram relations in their caches).
   - **Wave 2 of the screens** (the US; Canada, Brazil and Ireland; Spain
     and Italy). Launch only after checking usage and whether main is
     mid-build.
   - **Band T's group decision**: build trams-only cities, and in what order.
     Nice and Bergen need no calls; Brno is the biggest.
   - **Band C memo** (it lived only in chat): does a one-bucket page belong
     beside three-bucket cities? The recommendation was option C, case by
     case:
     - yes to Zurich, Göteborg, Hiroshima and Stockholm, and to Bucharest if
       its manual fetch is accepted;
     - no to Singapore (food ten years stale) and Yokohama (no food at all).
   - **Lisbon**: the owner is checking a DGAE account
     (https://mapadocomercio.dgae.gov.pt/ and https://cadastro.dgae.gov.pt/;
     the data endpoint returns 401). If the account is region-locked, probe
     national alternatives.
4. **Main's Monterrey** is built on `worktree-monterrey`, unpushed, for the
   owner's batch publish. If its master-list lines conflict, take master's
   numbers and apply A −1, Candidates −1, Built +1 (also in PLAN's Monterrey
   item).

## Standing rules this role keeps tripping on

- **No bypassing.** Never bypass a CAPTCHA, login, geo-block, proxy or VPN,
  and never create accounts.
- **No lookup back ends.** Never harvest a lookup page's back end to stand in
  for a blocked bulk file.
- **Columns.** Select by EXACT name and never print whole rows. Two privacy
  slips happened on 2026-09-27, both on file in DECISIONS.
- **Downloads.** Official portals only: at most 1.5 GB per file and 20 GB in
  total.
- **Outreach and moves.** Outreach is the last resort. Band moves are the
  owner's call. Recommend, then wait for a yes.
- **No restores.** Never restore files deleted for privacy (the Helsinki 2019
  CSV, Vienna's takeaways, the jvis and Oiva harvests).
- **Scratch output.** It goes in YOUR session's scratchpad. The hook refuses a
  backslash or backtick in a Bash heredoc, so write a script file instead.
- **Stray file.** `opd.pdf` (2026-09-25) at the main checkout's root is not
  Staging's, and the owner has not ruled on it. Leave it.
