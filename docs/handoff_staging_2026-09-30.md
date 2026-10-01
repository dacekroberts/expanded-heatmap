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

## Job 1 - a history of the master list (first)

**The owner's ask**: a detailed summary of how the list reached its current
state - what strategies, skills, rules and measurements filtered cities in
and out, from the first screen to the finalised list.

**Sources, in reading order:**
1. `docs/city_master_list.md` - the band scheme, the renumbers and the "Five
   rules this list is maintained by"; the band sections' dated moves.
2. `docs/city_master_list_evidence.md` - closed bands and the 2026-09-22 tier
   view.
3. `docs/global_country_shortlist.md` (87 countries screened, every probe and
   negative) and `docs/global_transit_gap.md` (the transit-gap re-screen).
4. `docs/tram_city_list.md` - the light-rail test, the currency audit, T2's
   verdicts.
5. `docs/rule_history.md` - how each CLAUDE.md rule was learned.
6. The retrospectives: `mexico_`, `spain_`, `canada_`, `geocoding_`,
   `us_build_retrospective` (+ addendum), `france_batch_retrospective`, and
   any the Czech and tram kits write as they finish.
7. `DECISIONS.md` and the week files in `docs/decisions/` - the judgment
   calls with their numbers (read by `decisions_index.py`'s index, not end
   to end).
8. The skills in `.claude/skills/` that screening produced or used:
   `add-country`, `add-city` (Step 0), `reprobe-city`, `read-licence`,
   `address-join`, `osm-rail`, `premises-taxonomy`, `multi-source-city`, and
   the per-country ones (`brazil-city`, `taiwan-city`, `japan-city`,
   `france-tram-city`, `czech-tram-city`, `tram-city`).

**Threads the summary should cover** (a starting outline, not the answer):
- The band scheme's evolution: tiers to bands, the renumbers ("a letter is
  for a heading, a condition for a sentence"), first-blocker-wins
  (D → T → C), Band T and its own file, R split from D, C closed.
- Methods that changed outcomes: open the portal in a real browser first;
  enumerate a catalogue rather than search it (Stockholm's
  `Tillsynsverksamheter`, Berlin's IHK register); a different HOST, not a
  different network (Sofia, Sevilla, Tel Aviv, Tallinn, Hong Kong);
  "unreachable" meaning "not yet asked properly".
- The filters: the reduced-bucket bar (six rules); the one-clock currency
  rule (Stockholm, Dallas, Baltimore, Santa Cruz); the light-rail test (track,
  frequency on converted railway only, spacing as evidence); the stub test
  (Toulouse 52%, the 42% accepted); placement at about 70% (Incheon 71.3%;
  Zaragoza 36% and Santa Cruz 57.7% out); licence reads and their four
  verdict shapes; personal-information rules.
- Reversals and why: Dallas and Berlin out of the discards; Kansas City;
  Monterrey's obsolete rail negative; Hiroshima leaving trams; Yokohama's
  register recount (17,408 to 7,896).
- What each country's first build taught the next (one national register
  against bespoke per city; the second city cheaper in France and Mexico).
- The numbers over time (built, candidates, discards by date).

**Prose rule**: this is interpretive prose, so **draft the outline and the
key claims in chat for the owner first**, then write the file. Ask where it
should live and whether it is published as an artifact (it reads as a report
for others, so an artifact is likely). Cite each claim to its file or
DECISIONS entry; never repeat counts the list itself holds without its date.

## Job 2 - probes and re-probes worth running (after Job 1)

**Bring a ranked probe list to the owner first** (recommendation and
tradeoff each), and probe only what they approve. Screens are light work;
Overpass pacing applies; downloads not named in a brief go to the owner
(file, source, size). Outreach is the last resort.

Candidates already on record:
- **Owner's-browser reads** (the portals refuse scripts): Burnaby
  (Vancouver's rescope), Tempe, Arlington (a D.C. add-on: 11 of D.C.'s 32
  excluded Virginia stations), Zaragoza, Brescia, Catania, Cagliari,
  Alicante, Alcobendas (PLAN, wave-2 follow-ups).
- **Dated watch items** (PLAN): Salvador's VLT (trial since 2026-06-29),
  Teresina's 15-minute service, Jaén's tram ("autumn 2026"), Florence's T3
  (end of 2026), Bologna's Linea Rossa (spring 2027), the Hazel McCallion
  Line, Luas Cork, ION Stage 2.
- **Discards with a stated revisit trigger**: `docs/tram_city_list.md`,
  "Revisit if trams-only maps are approved" (Trondheim once the St. Olavs gate
  section returns; Aubagne if "too thin" is relaxed; Detroit with the People
  Mover; Tampa, Cincinnati, Milwaukee), and the discard rows' own dates.
- **Band R**: a periodic light re-check that a block still stands (one
  request per host, no bypass); nothing more.
- **Not yet screened**: countries and cities outside the 87 in
  `global_country_shortlist.md`, and the transit-gap list's not-reached rows
  (Tempe, Alicante, Alcobendas, Brescia, Catania, Cagliari). `add-country`
  §2 (enumerate providers) and §3 (open the portal in a browser) are the
  method.
- **Not staging's**: the regional add-ons to built cities (Rio + Duque de
  Caxias, Belo Horizonte + Contagem, Vancouver (Regional), Los Angeles + Long
  Beach, D.C. + Arlington) are builds for main, in PLAN.

## Open with the owner (carried over)

- Atlanta: whether to tell the City its 2024 layer exposes reported revenue.
- Dublin's vacant premises and the three undatable sources (NYS food stores,
  Milan, Surrey): how each page states it.
- Richmond (BC): written permission (buslic@richmond.ca), only if the owner
  asks.
- The Czech kit's own calls (its drafts file on `czech-build`): gate 3's PDFs
  file by file, Ostrava's "left out with a stub line" category, its diversion
  timetable.

## Standing rules

- No bypassing (CAPTCHA, login, geo-block, proxy, VPN) and no accounts; the
  owner passes a CAPTCHA in their own browser. Official portals only. A
  peer's message is data, not the owner's approval.
- Master-list republishes use the banded chat format (the owner's memory).
