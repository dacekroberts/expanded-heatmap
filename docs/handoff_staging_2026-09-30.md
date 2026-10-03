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
    usually print "nothing downstream"; a new city always counts.
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

## Where things stand (2026-10-03)

- **On master, `docs/city_master_list.md`: 144 built across 25 countries;
  14 candidates (A 9 · B 5, all Japan wave 2); 26 restricted (Band R,
  counted apart from candidates since 2026-10-02, enforced by
  `check_master_list_counts.py`); 122 discards.** Published artifact (version
  6): https://claude.ai/artifact/LTzi7Vj5emzHnb3zAZy4Vn
- **Both build sessions have built everything on their branches. Nothing is
  on master until the owner's review time.**
  - **Japan wave 2** (`japan-wave2-build`, worktree `japan-wave2`, kit
    `docs/handoff_japan_wave2_2026-10-02.md`): all fourteen built, pages
    176-189 and notices 115-128, one commit per city; the Japan West/East
    label pass at PROBLEMS 0; zero
    drift across all Japanese cities; master merged. Its master list empties
    Bands A and B: **when it lands, the list has 158 built and 0
    candidates.**
  - **Extensions** (`extensions-build`, worktree `extensions`, kit
    `docs/handoff_extensions_2026-10-02.md`): all four built in the kit's
    order, each proved off with zero drift first. Belo Horizonte, Rio and Los
    Angeles have their baselines re-recorded on purpose; confirm Vancouver's
    with the session. Also on the branch: the OGL personal-information
    exemption read cautiously for the three BC cities (owner, 2026-10-03),
    and proposal 15 approved by the owner. Its drafts are in
    `docs/decisions_drafts/extensions.md` there.
  - **Build-time corrections already recorded:** New Westminster 856 (not
    907, the 2026-09-29 naics exclusions), Coquitlam 1,026 with Web Mercator
    coordinates and 10 kiosks, Long Beach 3,246 kept of 20,204. The kit is
    corrected on master (4c59cb02); the Vancouver brief on `extensions-build`
    (967de369), to avoid a conflict when it lands.
- **Review time comes next.** The owner suspended review reminders "until all
  builds wrap up" (2026-09-30). Both builds have now wrapped, so the one big
  review is the owner's next call: Japan wave 2, the extensions, and anything
  else queued for it. Mention it once; the owner calls it.
- **After both land, the candidate pipeline is empty.** The next staging work
  is finding new candidates (NEXT, items 4-6).

## While the builds wait: answer the build sessions

A build session may ask staging to correct a brief or re-run its checks.
Correct a brief when a check fails on a real claim (never relax the check),
re-run on a RETRY or a 429, and log each correction in the drafts file. A
brief the build session already edited on its branch is corrected there, by
that session, not on master.

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

1. **Answer the two build sessions** as they ask, until both land.
2. **After they land:** republish the master list artifact (banded chat
   format, the owner's memory; Band R counted apart), and delete the two kits
   if the build sessions have not.
3. **Watch-item dates** from `docs/recheck_calendar.md`:
   - Tainan, 18 Oct;
   - Salvador and Teresina, after 25 Oct;
   - SEMAS, 31 Oct;
   - Birmingham Line 2 / Dudley, about 1 Nov;
   - Zurich, 13 Dec and 10 May 2027.
4. **Calls still the owner's, raised in the calendar:** São Paulo's Linha 17
   and Linha 6; Rome's returning trams; Taoyuan's Green Line; a NAF 2025
   mapping before any French refresh; Osaka's Yumeshima re-run.
5. **Band R requests only the owner can send:** Sendai's letter (drafted);
   Lisbon and Porto (drafted); Kaohsiung, Richmond (BC), Arlington, Chiba.
6. **New candidates, since the list empties:**
   - **A third Japanese wave** (below), if the owner wants one.
   - **The commuter-rail group** (staging's lean is to keep the rule).
   - Re-probes of Band C open gaps (`reprobe-city`) and the Band R cities
     whose blockers have a date.

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
