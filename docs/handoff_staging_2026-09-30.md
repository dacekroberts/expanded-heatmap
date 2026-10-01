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

### Parked until after review time (owner, 2026-09-30)

The outline below was drafted in chat on 2026-09-30. The owner deferred
the file until review time ends, so the history describes the list after
the review batch lands (Cleanup's `review-rehearsal` moves it to 114 built,
28 candidates). Still open with the owner: whether the outline needs
changes; where the file lives (recommended:
`docs/city_master_list_history.md`, with a pointer from
`docs/project_context.md`); whether to publish it as an artifact
(recommended: yes, with the numbers chart).

**Outline, as drafted (sources in brackets):**
1. Before the list, 09-18 to 09-21. The US screen went from 25 to 10 to 9.
   Denver and San Jose taught live-verify. Dropping NAICS turned three of
   the four largest cities from fail to pass ("the single
   highest-leverage decision", US addendum). Canada went 13 to 6, with
   rail removing 6, and built five in about seven hours.
2. The global screen, 09-21: 87 countries, 2,476 static feeds. The filter
   order was flipped to premises data first and rail last. Four qualifying
   shapes; a company register is a category error
   (`global_country_shortlist.md`).
3. Tiers to bands, 09-22 and 09-23. The list's first state was 14 built,
   48 candidates, 14 discards. Rules from that churn: "a letter is for a
   heading", and a band closes when its condition stops being true. The
   coordinates band closed by succeeding. Summary drift (20/33/30 against
   22/29/32) led to `check_master_list_counts.py`.
4. Evidence rules, 09-22 to 09-24: "not reached" is not a discard (11
   rows); a country ruling needs two cities; the discard audit (12, then 5,
   to the open gap); evidence columns and `check_discard_evidence.py`; the
   gap emptied 09-24.
5. Methods: the browser first (the 09-22 sweep); enumerate, don't search
   (Stockholm, Zurich 938 of 1,128, Hong Kong 3,821, Berlin 2,626
   packages, India 288,011 titles); a different host (seven cities);
   nonsense-term controls; an address file before a geocoder (four for
   four); IP-level refusals are the limit, which became Band R.
6. Widening, 09-27 and 09-28: wave 1 (+43, 32 of them trams-only); wave 2;
   the transit-gap re-screen (seven cities built 09-28). Candidates peaked
   at 87.
7. The scheme settles, 09-27 to 09-30: Band T and first-blocker-wins
   (D→C→T, then D→T→C the same evening); N retooled as C; R split from D;
   T moved to its own file; the light-rail test (ten cities left T);
   trams approved 09-29; C closed 09-29; T2 closed 09-30.
8. The filters, each with its triggering case: the reduced-bucket bar
   (rule 1 amended for Yokohama); one currency rule (three clocks lasted
   about 15 minutes); the light-rail test; the stub test (52% Toulouse,
   42% accepted); about 70% placement; licence verdicts; personal
   information.
9. Reversals: Dallas, Berlin, Kansas City, Monterrey, Hiroshima, Yokohama
   (17,408 to 7,896), Singapore, Paris, Amsterdam, the UK and Australia.
10. What each first build taught the next: Mexico, Spain, France,
    Brazil/Taiwan/Japan (joins), Czechia (a different agency), Band B
    (template plus config; mistakes moved to framing).
11. Numbers over time, end of day on master's first-parent history, as
    built / candidates / discards:

    | Date | Built | Candidates | Discards |
    |---|---|---|---|
    | 09-22 | 20 | 31 | 30 |
    | 09-23 | 27 | 33 | 16 |
    | 09-24 | 42 | 24 | 27 |
    | 09-25 | 46 | 20 | 27 |
    | 09-27 | 50 | 63 | 51 |
    | 09-28 | 62 | 80 | 91 |
    | 09-29 | 75 | 66 | 97 |
    | 09-30 | 75 | 64 | 100 |

    09-22 opened at 14 / 48 / 14. Add the post-review state.

**Checks found while drafting:**
- **Settled:** Zaragoza's 36% is the share of addresses with a house
  number (61% are a bare street; `city_master_list.md`, its discard row).
  It is not a measured placement rate.
- **Open:** the discard audit's commits fall on the night of 09-23, but
  the log dates it 09-24.
- **Open:** when Berlin went back into the discards between 09-22 and
  09-28 is not pinned down.
- **Miscitations:**
  - This handoff's Job 2 calls Tempe, Alicante and the rest "the
    transit-gap list's not-reached rows". They are wave 2's.
  - The master list credits "enumerate providers" to `add-country` §2. The
    method is written up in the shortlist's "Tier 5 closed by browser
    navigation".
- **Stale, for Cleanup:**
  - The master list still gives Yokohama 17,408 premises.
  - `add-country`'s station-density table still has Canada's
    pre-correction figures.

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
