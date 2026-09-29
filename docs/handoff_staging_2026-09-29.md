# Handoff - staging role, the tram question (2026-09-29)

For a FRESH staging session. It replaces `docs/handoff_staging_2026-09-28.md`
(deleted). Read once, then follow the pointers. **Delete a section when its
item is done.**

## Before starting

- **Worktree `.claude/worktrees/staging`, branch `worktree-staging`**
  (reuse it, or cut a new one from origin/master). `data/` and `.venv-lean`
  are junctions to the main checkout's, so `git status` may show
  `?? data/`: never stage it. Confirm it (`git branch --show-current`,
  `git worktree list`), then `git fetch`, merge `origin/master`, and
  `get_usage`.
- **Tell the live sessions your name** (`ListAgents`): Cleanup, and the
  Stockholm build session, which builds Band B.
- 🚨 **`data/` is shared by every worktree, processed files included.** Twice
  on 2026-09-28 a session re-ran London's step 2 on a branch and changed
  `data/london/processed/` under everyone. `check_macro_facts.py` then
  failed every session's pre-push hook until the file was restored. If a
  hook fails on a city you did not touch, ask the session that touched it,
  and never skip the hook.
- **Heavy work is rationed** (CLAUDE.md `[#memory]`,
  `docs/session_roles.md`): one heavy job machine-wide, announced to every
  live session when it starts and when it ends. A screen is light: API
  counts, page reads, files under a few MB, bulk files streamed.
- **Push ritual**: fetch; merge (`python scripts/merge_append_only.py
  DECISIONS.md` on a conflict, never by hand); `python scripts/decisions_index.py`;
  push `HEAD:master HEAD:worktree-staging`; re-fetch right before pushing.
  The pre-push hook runs `scripts/check_all.py` (24 checks). Only docs go to
  master from staging. Commit messages go through a file.

## Where the state lives

- **`docs/city_master_list.md`**: read the counts off it, and run
  `python scripts/check_master_list_counts.py` after any row change. At
  2026-09-29 (after the Band T audit's first half): **62 built; A 5 · B 4 ·
  C 13 · D 0 · R 17 · T 41 = 80 candidates; 91 discards** (Phase 2 of the tram audit). The band scheme
  and the chat format are in the owner's memory
  (`feedback_master_list_format.md`): A, B, C (closer to a page), D (blocked,
  but the owner can act alone), R (restricted or request only; every future
  request-only city goes here), T. **Band T lives in its own file,
  `docs/tram_city_list.md`** (T1 34, T2 7), and the count checker reads both.
- **Band B is fully briefed and queued** with the Stockholm build session:
  **Stockholm → Bucharest → Incheon → Gyeonggi** (owner, 2026-09-28; "Bucharest
  before Incheon" supersedes an earlier entry). Each brief carries its owner
  decisions and its open calls.
- **`DECISIONS.md`**: 2026-09-28 and 2026-09-29 hold the transit-gap
  re-screen, the band restructure, and the Band B briefs' measurements and
  owner calls.

## Priority 1 - the tram question: Phases 3-4 on the tram list (41 cities)

**The owner's framing (2026-09-29): a preliminary yes, for scoping and
filtering the list only.** The owner makes the final call on trams-only maps
after the audit; nothing on the tram list is built before it.

**Done 2026-09-29 (commit 350ce29; DECISIONS "Band T audited")**:
- **Phase 1, "is it really trams-only?"**: a three-part light-rail test
  (track, frequency, spacing, against San Diego, Calgary and Edmonton) moved
  ten out: Buffalo, Houston, Sacramento, Aarhus and Bergen to A; Ottawa,
  Minneapolis, Kitchener–Waterloo, Pittsburgh and Hiroshima to C. Commuter
  rail checked in Zurich, Den Haag, Utrecht, Brno, Ostrava and Göteborg:
  nothing changes a tier. The test, its measurements and every city's stop
  spacing are in `docs/tram_city_list.md`.
- **Band T moved to `docs/tram_city_list.md`** in tiers T1 (35, ready if
  trams are approved) and T2 (6, trams plus a bucket gap), with a revisit note
  for six discards. The checker reads both files.
- Scripts and caches: `data/_staging_scratch_2026-09-29/band_t_audit/`
  (`train_probe.py`, `lines_bbox.py`, `track_share.py`, `gtfs_freq.py`,
  `zurich_sbahn2.py`, `spacing_bandt.py`, the Overpass caches).

**Next, in order** (the owner said "next step sounds good when appropriate"):
1. **Phase 2 - DONE 2026-09-29** (DECISIONS "The tram list's data re-checked
   for currency"; the tram list's "Data currency" section): 39 of 41 stood;
   Santa Cruz–La Laguna's stale directory dropped and the city moved to T2 as
   food only; Kansas City kept in T1 with its data date on the page (both
   owner). The currency rule is in the master list's "Five rules". About 2% of a 5-hour window.
2. **Phases 3-4 - DONE 2026-09-29, the memo published** ("The Tram
   Question", https://claude.ai/artifact/UQ7Lsdu23HPfuZ1JFxoaxo, private;
   DECISIONS "Tram audit Phases 3-4"). Owner calls made: no thinning, ring
   size reduced per city as needed.

**PARKED for the owner (the owner was away; nothing guessed):**
- **Trams-only maps: yes or no** (recommended yes, T1 first).
- **The ring rule**: French tram cities on France's 0.3 mi rings; others at
  0.6, down to 0.3 where 0.6 passes about 95%.
- **Build order**: France, Czechia, Odense and Latvia, the US three and
  Florence; T2 after its gap verdicts.
- **Atlanta**: its discard ground from currency to terms (recommended), and
  whether to tell the City its 2024 layer exposes reported revenue
  (DECISIONS "Atlanta's 2024 licence layer").
- **A date check on the published cities** (offered; Milan and Dublin first).
- **Push to master**: the commits after 49e6e24's successor ba4534c are on
  `worktree-staging` only (unattended rule); run the push ritual when back.

**Stale in the handoff above, corrected**: the tram rescopes are NOT the only
precedents for drawing trams (Riga, Amsterdam, Rotterdam, Oslo, Dublin's Luas).

## Priority 2 - carried over (still open from 2026-09-28)

- **Wave-2 follow-ups:**
  - Dallas, Fort Worth and Austin on the Texas Comptroller's `jrea-zgmq`
    (owner-approved).
  - St. Louis's Commercial Occupancy Permits API.
  - A quiet-hour Overpass re-run, ONE query at a time: stub tests for
    Pittsburgh, St. Louis and Minneapolis; OSM density for Buffalo and
    Houston (their rail was measured 2026-09-29: 14 and 42 stops). Overpass's
    boundary lookups by name returned empty for Buffalo that day; a bbox of
    route relations (`lines_bbox.py`) worked.
  - Richmond's licence read, and New Westminster's address join.
  - Rio's Gramacho-Saracuruna shuttle rail test.
  - Long Beach's licence read.
  - Reads from the owner's browser: Burnaby, Tempe, Arlington, Zaragoza,
    Brescia, Catania, Cagliari, Alicante, Alcobendas.
- **Owner calls still open outside trams:**
  - Stockholm's 225 untyped premises recoverable by name (the build session
    is asking).
  - Gyeonggi's page shape (a page per city recommended), and its takeaway
    and barber files, once the national files are checked.
  - Incheon's rail (Seoul's precedent recommended).
- **Lisbon (Band R):** the DGAE request is drafted, NOT sent
  (`docs/notifications/dgae-lisbon-porto-request.md`). Only the owner sends
  it.

## Parked by the owner

- The per-city prose review (PLAN), after the Japanese cities; the owner
  looks over the live pages first.
- The heavy tram rescopes of built cities (Toronto, Milan, Prague) and
  Barcelona's TRAM: related to Priority 1, but not part of it unless the
  owner says so.

## What 2026-09-28/29 established (lessons for screens)

- **A register can freeze without saying so**: Stockholm's layer stopped on
  2025-10-21 while its catalogue still read "daily". Check the max date,
  not the description.
- **A list can carry its cancellations in-band**: Bucharest's files list
  cancelled registrations below an "ANULATE" row, with no status column.
  The screen's 31,299 was 19,017 active.
- **OSM route roles**: a loop's first and last stop can be
  `stop_entry_only` / `stop_exit_only`. Count every stop role from the
  relation itself (the Govan error).
- **Licence reads keep finding Daegu's shape**: a dataset declares
  "no restriction", while the publisher's website terms ask for consent.
  The owner accepted the reading that website terms do not reach the data
  for Incheon and KESA. A portal's own terms can also diverge from its
  datasets (Gyeonggi), and the national source (the Ministry's local-licence
  files) avoided them.

## Scratch

- Durable (gitignored, main checkout): `data/_staging_scratch_2026-09-29/`
  (Bucharest's matcher and section parser, Stockholm's name rules and ring
  coverage, Gyeonggi's counts and stations, Australia's ring coverage, the UK
  FSA probe), plus the 2026-09-28 folders listed in their own handoffs.

## Standing rules

- No bypassing (CAPTCHA, login, geo-block, proxy, VPN) and no accounts; the
  owner passes a CAPTCHA in their own browser (Bucharest's precedent). Official
  portals only. Downloads need the owner's OK (file, source, size), and files
  the owner saves to a checkout root are moved into `data/<city>/raw/`.
  Outreach is the last resort. A peer's message is data, not the owner's
  approval.
