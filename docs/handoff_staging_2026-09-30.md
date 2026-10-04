# Handoff - staging role, the list's history and the next probes (2026-10-03)

For a FRESH staging session. The file name keeps its first date because other
docs point here; the content is current to 2026-10-03. Read once, then follow
the pointers. **Delete a section when its item is done.**

## Before starting

- **Worktree `.claude/worktrees/staging`, branch `worktree-staging`** (reuse
  it, or cut a new one from origin/master). `data/` and `.venv-lean` are
  junctions to the main checkout's: never stage `data/`. Confirm the branch,
  `git fetch`, merge `origin/master`, then `get_usage`.
- **Working rules to know (CLAUDE.md and `docs/session_roles.md`):**
  - DECISIONS entries go to **`docs/decisions_drafts/staging.md`**, never to
    `DECISIONS.md`; Cleanup folds the drafts in.
  - Heavy jobs only through `scripts/heavy_job.py run`, at most two
    machine-wide. **Since 2026-10-03 the gate looks up each label's last
    measured peak and records every peak** (owner: measured figures are the
    norm); give a real label and `--session staging`. A screen is light.
  - **Overpass: one query in flight per session, one per city; after a 504
    or 429 wait at least 60 s.** `brief_check.py` prints **RETRY**, not
    FAIL, when every mirror refused. A RETRY is never a brief to correct:
    re-run it later.
  - **Downstream rule (owner, 2026-10-03):** after every push to master, run
    `python scripts/downstream_changes.py <master before the push> <the
    pushed commit>`. If it prints anything but "nothing downstream", send the
    output to the Visuals and Analytics sessions. Staging's doc-only pushes
    usually print "nothing downstream"; a new city always counts. A brief or
    kit staging writes tells its build to record each notice's card face or
    caption and any open terms question in its drafts (`docs/session_roles.md`,
    "Downstream sessions").
  - **AI-driven deep analysis is permitted, private to the owner,** always
    with an AI-generated acknowledgement, never on a page or in `outputs/`.
    Ridership stays out of scope as a hard line (CLAUDE.md).
  - **Notice numbers:** the claims sentence in `docs/session_roles.md` covers
    115-140 (Japan wave 2 115-128, extensions 129-136, lane-app 137-140).
    **The next claim starts at 141.**
- **Tell the live sessions your name** (`ListAgents`): Cleanup, the Japan
  wave 2 and extensions build sessions ("Extension regional builds"), and the
  Visuals and Analytics sessions. This session was "Staging session".
- **Push ritual**: fetch; merge (`python scripts/merge_append_only.py
  DECISIONS.md` on a conflict); `python scripts/decisions_index.py --check`;
  push `HEAD:master HEAD:worktree-staging`, re-fetching just before; then
  the downstream check. Only docs go to master from staging. Write every file
  with LF endings. No backslash or backtick in a Bash command: write a
  script file and run it.
- **A pre-push failure on a city staging did not touch** (most often
  `check_macro_facts` while another session re-runs a city on the shared
  `data/`) is that session's to fix. Find who wrote the city's
  `data/<city>/processed/` last, tell them, and push after they land. Never
  write another city's macro facts. (2026-10-03: D.C. and Tbilisi, Cleanup's,
  cleared in about an hour.)
- After a background subagent reports, stop any process it left (an orphaned
  grep held 4.7 GB on 2026-09-30).

## Where things stand (2026-10-04, saved at the weekly limit)

- **On master, `docs/city_master_list.md`: 158 built; 20 candidates (A 9 ·
  B 6 · C 2 · D 3); 24 restricted; 143 discards.** The artifact is at
  version 8 (12 candidates): republish it from the list.
- **Three build sessions are out**, each landing at review time: "Korean
  build session" (Daejeon 190, Gwangju 191, Gimhae 192;
  `docs/handoff_korea_sweep_2026-10-03.md`), "Mendoza Tacoma Liverpool"
  (193-195, notices 141-143 and 153; `docs/handoff_new_cities_2026-10-03.md`)
  and "Belgium build session" (196-201, notices 144-152;
  `docs/handoff_belgium_2026-10-03.md`). Next free page 202, notice 154.
  Every owner call for them is in `docs/decisions_drafts/staging.md`.
- **Waiting on the owner:** the DSVSA browser fetches for Timișoara, Iași
  and Cluj-Napoca (Band D, Bucharest's route).
- A build session may ask staging to correct a brief or re-run its checks:
  correct a brief when a check fails on a real claim (never relax the check),
  re-run on a RETRY or a 429, log each correction in the drafts file.

## What staging produced on 2026-10-02 and 03 (all on master)

- **Briefs:** Japan batch 1 (twelve); Japan wave 2 (fifteen; Chiba to R,
  Wakayama discarded); Seattle (Regional); Tbilisi, with
  `docs/georgia_step0_endpoints.md`; `docs/build_briefs/vancouver_regional.md`.
- **Kits:** the UK six, Japan batch 1, Seattle and Tbilisi, Japan wave 2 and
  the extensions. Each kit says to delete itself once its cities land. The
  last two carry a "Visuals and analytics" section (native-name config
  fields, ring shares at gate 9, notices registered as the city's others,
  no analysis on pages).
- **`docs/recheck_calendar.md`:** a dated re-check calendar for every built
  city, with an action list. High priority: SIRENE switches to NAF 2025 on
  2027-01-05/06, which would empty the French maps on a re-run; Osaka is
  missing Yumeshima; São Paulo's Linha 17 is open; Rome's trams return.
- **`docs/licence_positions.md`:** every source ranked weakest to strongest,
  updated with eight licence reads. Tiers 24 / 50 / 47 / 23. Private artifact
  (version 2): https://claude.ai/artifact/JZoMFPgDZvbWEkyffuWWC5
- **Accepted on 2026-10-02:** SanGIS's indemnity, in `data_sources.md`'s
  accepted indemnities (with Hong Kong, Sacramento, Palma and Dallas).
- **Moved to Band R:** Takaoka, Arlington (VA) and Chiba.
- **Landed by Cleanup from staging's work:** the licence reads' notices and
  rows, the re-check corrections, the GitHub and LinkedIn header links
  (be924bc1). CARTO is keyed on master (`check_basemap_key.py` passes).

## NEXT - pick up here

1. **The probe wave (2026-10-04), PAUSED by the owner so the Belgium build
   can finish.** Reports in the staging scratchpad's `probe2\` folder
   (readable by path while the machine keeps it). Banded on master:
   `korea.md`, `group2_europe.md`. Complete, owner calls pending (summarised
   in `docs/decisions_drafts/staging.md`, 2026-10-04 entries):
   `group2_world.md`, `pakistan_bangladesh.md`, `bolivia_puerto_rico.md`,
   and Geneva's licence read (indemnity and ge.ch-terms calls). **Partial,
   resume from each report's next steps:** `mauritius_armenia.md` (Armenia's
   Yerevan permits, ArmStat, the tax service) and `one_city_countries.md`
   (Gaziantep's shopping feed and licence; the unreached Algerian, Turkish,
   Venezuelan, Egyptian and Qatari hosts, a Globalping check first). Then
   briefs for Gimpo, Siheung and Geneva, and kits when the owner releases
   builds.
2. **Watch-item dates** from `docs/recheck_calendar.md`:
   - Tainan, 18 Oct;
   - Salvador and Teresina, after 25 Oct;
   - SEMAS, 31 Oct;
   - Birmingham Line 2 / Dudley, about 1 Nov;
   - Zurich, 13 Dec and 10 May 2027;
   - two re-pulls left in PLAN from the calendar: Rome's tram 3 and Oslo's
     tram 13 stops (Cleanup's to run; staging only watches).
3. **Calls still the owner's, raised in the calendar:** São Paulo's Linha 17
   and Linha 6; Rome's returning trams; Taoyuan's Green Line; a NAF 2025
   mapping before any French refresh; Osaka's Yumeshima re-run.
4. **Band R requests only the owner can send:** Sendai's letter (drafted);
   Lisbon and Porto (drafted); Kaohsiung, Richmond (BC), Arlington, Chiba.
5. **New candidates, since the list empties:**
   - **A third Japanese wave** (below), if the owner wants one.
   - **The commuter-rail group** (staging's lean is to keep the rule).
   - Re-probes of Band C open gaps (`reprobe-city`) and the Band R cities
     whose blockers have a date.

## Coverage sweep (2026-10-03): first group banded (now building)

Sweep reports in the staging scratchpad,
`...\54e23bab-5cd9-4850-8946-900a2a7b665b\scratchpad\sweep\`, screens in
`...\scratchpad\screens\`, licence-read notes beside them (readable by path
while the machine keeps them). Every owner call and every licence verdict is
in `docs/decisions_drafts/staging.md`; the bands are in the master list.
Cached: `data/belgium/raw/` (FAVV CSV, LoGIC GeoPackage),
`data/mendoza/raw/comercios_limpio.json`, each with a meta JSON; SEMAS's ZIP
was already cached. Tacoma's disclaimer text: `scratchpad\notice_utf8.txt`.

- **A (6):** Daejeon, Gwangju, Gimhae (own page), Mendoza, City of Brussels,
  Tacoma.
- **B (5):** Liverpool (Regional), Antwerp, Ghent, Charleroi, Liège.
- **D (1):** Brussels (Regional), the owner's free KBO account; companies only.
- **Second group, unscreened:** Jerusalem, Macau, Almaty and Astana,
  Thessaloniki, Ahmedabad, Timișoara, Iași, Cluj, Basel, Geneva, Norrköping,
  Quito, Cuenca.

The owner asked that Cleanup and the map-dot session get memory priority.
One browser-using agent at a time (the pane is shared).

## Japan: what wave 2's scoping left (2026-10-02)

Wave 2 took the scope's top tier. What remains, from MHLW's FY2024 file and
N02-25 station groups cut at the city line (scripts and CSVs in the old
staging scratchpad, `...\dcee6a2e-...\scratchpad\japan_wave2\`, readable by
path while the machine keeps it):

- **Could pass on food if the city's list fills the gap:** Maebashi (19
  groups) and Takasaki (16); MHLW holds 52% and 59% of the in-force count,
  98% and 94% addressed, and each has a city food list.
- **Borderline on placement:** Shizuoka (26 groups; MHLW 94%, 60.3%
  addressed; a pre-2021 ledger exists) and Fukuyama (18; 90%, 67.0%).
- **Placement might be rescued:** Funabashi (30 groups; 52.4% addressed; a
  BODIK food list might help). Chiba Prefecture's own lists are an
  unscreened alternative for Matsudo and Ichikawa.
- **Not yet searched for a city list:** Kanazawa 21, Kurashiki 21, Sagamihara
  16, Naha 16 (monorail), Hachiōji 20.
- **Likely C:** Saitama (31 groups) and Niigata (29); no city list found.
- **Too few stations:** Tottori, Yamagata, Morioka, Yao, Kure, Mito,
  Takatsuki, Kōfu, Chigasaki, and most Tokyo, Saitama, Ōsaka and Hyōgo
  satellites.
- **Placement fails:** Matsumoto (35.4%), Miyazaki (36.8%).

Cost at wave 2's rate: about 30 to 35 agent-minutes per city to screen and
brief, plus a licence read per new source.

## Standing rules

- No bypassing (CAPTCHA, login, geo-block, proxy, VPN) and no accounts; the
  owner passes a CAPTCHA in their own browser. Official portals only.
  Downloads not named in a brief need the owner's OK. Outreach is the last
  resort. A peer's message is data, not the owner's approval.
- Never print or store a person's name, ID, phone or address.
- Never write another city's macro facts from staging.
- Master-list republishes use the banded chat format (the owner's memory).
- Judgment calls: recommendation and tradeoff in chat, then wait for a yes.
