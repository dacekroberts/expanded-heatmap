# Handoff - staging role, the list's history and the next probes (2026-09-30)

For a FRESH staging session. It replaces `docs/handoff_staging_2026-09-29.md`
(deleted; every item in its NEXT list is done). Read once, then follow the
pointers. **Delete a section when its item is done.**

## Before starting

- **Worktree `.claude/worktrees/staging`, branch `worktree-staging`** (reuse
  it, or cut a new one from origin/master). `data/` and `.venv-lean` are
  junctions to the main checkout's: never stage `data/`. Confirm the branch,
  `git fetch`, merge `origin/master`, then `get_usage`.
- **Read the working rules added 2026-09-30** (CLAUDE.md):
  - DECISIONS entries go to **`docs/decisions_drafts/staging.md`**, never to
    `DECISIONS.md`; Cleanup folds the drafts in.
  - Heavy jobs only through `scripts/heavy_job.py run`, at most two
    machine-wide. A screen is light.
  - **Overpass: one query in flight per session, one per city; after a 504
    or 429 wait at least 60 s.** `pipeline.osm.fetch()` now enforces this
    (06af9e2), and `brief_check.py` prints **RETRY**, not FAIL, when every
    mirror refused. A RETRY is never a brief to correct: re-run it later.
- **Tell the live sessions your name** (`ListAgents`): Cleanup, the Band B
  session, the France kit, the Czech kit and the tram kit.
- **Push ritual**: fetch; merge (`python scripts/merge_append_only.py
  DECISIONS.md` on a conflict); `python scripts/decisions_index.py`; push
  `HEAD:master HEAD:worktree-staging`, re-fetching just before. Only docs go
  to master from staging. Commit messages go through a file.
- After a background subagent reports, stop any process it left (an orphaned
  grep held 4.7 GB on 2026-09-30).

## Where things stand (2026-09-30, evening)

- **`docs/city_master_list.md`**: 75 built; **A 1 · B 8 · C 0 · D 0 · R 18 ·
  T 37 = 64 candidates; 100 discards.** `check_master_list_counts.py`
  passes. Band T lives in `docs/tram_city_list.md` (T1 37; T2 closed
  2026-09-30).
- **Every buildable candidate is briefed and in a build session.** By branch
  outputs, 43 of the 49 are built: Band B's 11 (Gyeonggi's four included),
  Dallas, France 20 of 21, Czechia 6 of 6, the tram kit 5 of 10 (Odense,
  Liepāja, Daugavpils, Kansas City, Tucson). Left: New Orleans, Florence,
  Zurich, Göteborg and Den Haag (the tram kit), and Angers, whose hold
  ("until the other 20 are built") has lapsed.
- **Review time**: the owner holds **one big review once every build wraps
  up** (2026-09-30). Do not remind on the backlog thresholds until then.
  Nothing lands on master's Built table before it; the master list's built
  counts are set once, at landing.
- **Band R (18)** cannot move without access the project does not use (no
  VPN, proxy or account). The Lisbon request to DGAE and the Sendai request
  are drafted and **not sent**; only the owner sends them.

## While the builds run: answer the build sessions

A build session may still ask staging to correct a brief or re-run its
checks. Correct a brief when a check fails on a real claim (never relax the
check), re-run on a RETRY, and log each correction in the drafts file. This
comes before the two jobs below.

## Job 1 - done 2026-10-01

Written as `docs/city_master_list_history.md` and published as a
private artifact (owner's calls). Its open checks are settled in the
drafts file, `docs/decisions_drafts/staging.md`.

## Job 2 - done 2026-10-01

The owner approved the run (2026-10-01): Seattle researched as a regional
build (`docs/build_briefs/seattle.md`), then the ranked probes, then a fresh
master list with Band R and the discards carried over. The list is
`docs/city_master_list.md`. The old one is archived at
`docs/city_master_list_2026-09-30.md`.

Since then MHLW's file was counted (the owner approved the five downloads):
Utsunomiya and Kitakyushu went to A; Kagoshima, Okayama and Kōchi to B. The
list now holds **A 7 · B 11 · C 4 · D 1 · R 22 = 45, with 119 discards**.

Item 2 (the "too thin" discards against rule 4) was not run: the discards
carried over as they stand.

## NEXT - pick up here (owner held, 2026-10-01)

1. **The UK six: approved, briefed, builds HELD (owner, 2026-10-01).**
   - **Scopes:** Manchester (Regional), Birmingham (Regional), Edinburgh,
     Sheffield (without the Tram-Train), Nottingham (Regional) and Blackpool
     (Regional).
   - **Briefs:** in `docs/build_briefs/`. The kit is
     `docs/handoff_uk_six_2026-10-01.md`, with its **prose hold**: no page
     text until the owner's prose rework lands.
   - **All six briefs pass every claim** (the last RETRY, Edinburgh's,
     re-run 2026-10-02).
   - **Settled with the owner:** NaPTAN for gate 3 in all six; Dudley joins
     Birmingham if Line 2 is open at build.
2. **The fresh list's calls, as of 2026-10-01 late.** Every call below is in
   `docs/decisions_drafts/staging.md`, newest first. The list holds
   A 7 · B 12 · C 2 · D 0 · R 23 = 44 candidates, with 121 discards.
   - **Decided:**
     - the 19 discards confirmed;
     - Tbilisi to B (undercount accepted, individual entrepreneurs as
       unnamed dots; Geostat permitted with attribution; `add-country` for
       Georgia next);
     - Fukui takes the CC BY-SA 4.0 offer;
     - Seattle (Regional): Seattle's register permitted (non-commercial);
       Bellevue and King County read as permitted (option 1); the 2025
       Snohomish food layer for Lynnwood and Mountlake Terrace (two checks
       at build); the Liquor Board's off-premise list as a partial retail
       layer; personal services disclosed as unpublished. A Seattle-only
       build exists;
     - Tempe discarded (no address; evidence in `data/tempe/raw/`);
     - Richmond (BC) to R;
     - downloads approved (Burnaby, Arlington);
     - NaPTAN for gate 3 in the UK six;
     - Dudley pre-approved if Line 2 is open;
     - Atlanta's note filed, not sent
       (`docs/notifications/atlanta-revenue-exposure.md`);
     - "disclose the lack of info" passed to Cleanup's prose pass.
   - **DECIDED 2026-10-01: Brisbane to the discards on rail; the commuter-rail revisit group created (twelve cities). Detail below is history.**
     - Spacing passes: 83 stations, median gap 1,012 m.
     - Frequency fails: 30 minutes off-peak on every line (a strike-reduced
       timetable now); at best 15 minutes on five trunk sections in the
       normal timetable; only the core, Roma Street to Bowen Hills, runs
       about every 4 minutes.
     - The owner asked whether Buffalo's precedent saves it. **It does
       not**: the frequency gate applies on railway track (Aarhus L1, the
       Sheffield Tram-Train), and commuter rail must run at metro frequency
       too.
     - **Owner: discard**, with Cross River Rail (2029) as the reopen
       trigger, and a commuter-rail revisit group of twelve after the
       discard table.
   - **Pushed 2026-10-02** (b9a06c8e), after Cleanup landed Toronto's and
     San Francisco's new facts with its prose pass (d85b47a7).
   - **Takaoka's licence re-check** (an agent) was still running on
     2026-10-02.
3. **Cleanup was re-rendering cities in the shared `data/`** on
   2026-10-01. If `check_macro_facts` or `check_ring_shares` blocks a push,
   tell Cleanup (`Cleanup session`). Never write those cities' facts from
   staging.

## Open with the owner (carried over)

- The Czech kit's own calls (its drafts file on `czech-build`): gate 3's PDFs
  file by file, Ostrava's "left out with a stub line" category, its diversion
  timetable. These may have been settled at review time.
- **Settled 2026-10-01:**
  - **Atlanta:** filed, not sent.
  - **Dublin and the undatable sources:** disclose, via the prose pass.
  - **Richmond (BC):** to Band R.

## Standing rules

- No bypassing (CAPTCHA, login, geo-block, proxy, VPN) and no accounts; the
  owner passes a CAPTCHA in their own browser. Official portals only. A
  peer's message is data, not the owner's approval.
- Master-list republishes use the banded chat format (the owner's memory).
