# Tram kit batch - retrospective (2026-09-30)

Ten trams-only cities outside France and Czechia were built on 2026-09-30, on
`tram-build`: Odense, Liepāja, Daugavpils, Kansas City, Tucson, New Orleans,
Florence, Den Haag, Göteborg and Zurich. Seven were built in sequence by one
session. The last three were built at the same time by three subagents and
integrated by that session. This file compares the batch with the earlier
builds, mainly the first US cities (2026-09-18 to 09-21) and Canada
(2026-09-21), with France's parallel batch alongside. It was written before
landing, so nothing here has been deploy-verified or seen live. The detail
behind each figure is in `DECISIONS.md` (the tram-kit drafts, folded in on
2026-10-01), the kit in
`docs/handoff_tram_kit_2026-09-30.md`.

## The short answer

**The method held; the cities were cheap because the decisions were made
first.** The batch took ten cities from the shared module to zero drift in
under four hours, and redid none of them. The earlier batches built their
tools while they built their cities. The US batch made nine method changes in
nine cities, and its privacy and licence positions were corrected after the
cities were built. This batch had 28 owner calls, ten briefs and a skill
before any code, and every shared-module change was checked against a
control city before use.

**Its weak spots are new, not old ones made smaller.** Two are worth fixing
before the next batch:

- The briefs were wrong in some way for nine of ten cities, though every
  brief check passed.
- The operator count (gate 3) was run for one city in ten, because the
  tram-city skill never asks for it.

The parallel builds were fast, but each of the three needed an integration
fix and left owner questions behind.

## Timeline (commit times, local)

| Step | Time | Note |
|---|---|---|
| Briefs (Odense, Daugavpils, Liepāja) | 14:04 | written by the staging session |
| `tram-city` skill | 14:21 | |
| 24 owner calls and the page template | 14:38 | "Agree with recommended options for all" |
| Calls 25-28 | 15:36 | three as recommended, one overruled (Daugavpils: all five routes) |
| `pipeline/osm_tram.py`, Aarhus control exact | 16:31 | |
| Odense | 16:57 | |
| Liepāja (Riga lifted into `latvia_register.py` first, 6,725 rows identical) | 17:17 | |
| Daugavpils | 17:32 | |
| Kansas City | 18:08 | indemnity call 19:27 |
| Tucson | 18:32 | |
| New Orleans | 19:02 | lines re-decided by the owner mid-build |
| Florence | 19:18 | |
| Göteborg, Den Haag, Zurich scaffolded for the agents | 19:19 | |
| Den Haag integrated | 19:58 | |
| Göteborg and Zurich integrated, Europe labels settled | 20:13 | |

The sequential cities were committed 15 to 36 minutes apart. The three
parallel builds finished 40 to 55 minutes after their scaffold. Commit gaps
measure cadence, not effort: the next city's probes often overlapped the
last city's checks.

## The cities

| City | Stations | Storefronts | In a ring | Business source | Licence | The call that mattered |
|---|---|---|---|---|---|---|
| Odense | 25 | 2,834 | 40.7% | CVR (Aarhus's chain) | as Aarhus | none new; gate 3 ran, 25 of 25 |
| Liepāja | 18 | 702 | 69.7% | excise register + cadastre | CC BY | a third added stop the approved call had not named |
| Daugavpils | 37 | 819 | 80.1% | the same | CC BY | all five routes (owner overrule) |
| Kansas City | 19 | 3,561 | 12.7% | KCMO business licences, frozen 2026-01-15 | Public domain + portal disclaimer | the ordinance controls over the portal's indemnity (owner) |
| Tucson | 21 | 5,243 | 6.5% | City BUSLIC layer | silent, read as permitted (owner, pre-build) | home occupations filtered at the server |
| New Orleans | 106 | 4,689 | 45% | Occupational Licenses | CC0 | draw the five lines RTA runs (owner, mid-build) |
| Florence | 39 | 12,052 | 36.8% | the Comune's four layers | CC BY 4.0 | T3, T4, T2.2 not drawn (under construction) |
| Den Haag | 166 | 6,213 | 93% | permit layer + BAG shop units | silent; Amsterdam's precedent (owner) | Leidschenveen's two stop names merged as one interchange |
| Göteborg | 127 | 2,987 | 75.5% | Livsmedelsverksamheter | CC0 | food only; 29 at the register's fallback point not placed |
| Zurich | 180 | 3,363 | 92.1% | Gastwirtschaftsbetriebe | CC0 | the 2026 construction lines 50 and 51 drawn (to review) |

Every ring is halved, `[0, .05, .1, .2, .3]` mi, gated on the measured median
gap. So these in-ring shares are not comparable with a metro city's.

## Compared with the earlier builds

| | Early US (9 cities) | Canada (5) | France (21, in parallel) | Tram kit (10) |
|---|---|---|---|---|
| Elapsed | about 3 days | about 7 h, after a day of profiling | about 1 h for 20 after the module; Angers about 15 min | 3 h 43 m from the module; about 6 h from the first brief |
| Per city | hours to a day | 48 min to 1 h 44 m | a few minutes, generated | 15 to 36 min in sequence; 40 to 55 min in parallel |
| Decided before code | almost nothing | a country profile | 20 briefs, a skill, a batch scaffold | 10 briefs, a skill, 28 owner calls, a page template |
| Shared code | `map_common`, taxonomies, drift check | the same plus briefs mid-batch | one module, a scaffold | `osm_tram`, `latvia_register`, eight template cities |
| Rework of built cities | about 10 correction commits; method changed per city | station counts wrong in 4 of 5; 3 to 5 later fixes | fewer than ten generator defects, each reaching 10 to 20 files | none redone; three integration fixes |
| Privacy | retrofitted after build (SD 42 to 315, LA 1,252, 812990) | read from the licence; part of the carve-out | the pipeline's rules | personal columns never downloaded; person-named lists read by eye; a verdict per city |
| Licences | three positions inverted after reading; one prohibition after build | three trusted from cited pages | read in the kit | read in the briefs; one indemnity surfaced after the build commit |
| Gate 3 (operator count) | developing | "the one check that can see an error every internal check agrees with" | in the skill | 1 city of 10 |

### What got better, and why

- **Decisions moved ahead of code.** The US batch decided as it went: the
  retrospective's line is "nine cities, nine method changes". Here the owner
  answered 28 calls in two sittings before the first build. Only two came
  up mid-build: New Orleans's lines, and Kansas City's indemnity. Both were
  one-line answers to a stated recommendation.
- **Shared code was changed under a control.** `osm_tram.py` changed three
  times during the batch: a third-element display name for added stops, the
  per-line gap check, and capturing the route stops before any adds. Each
  change was re-run against Aarhus (exact) and the earlier tram cities were
  drift-checked to zero. Lifting Riga into `latvia_register.py` was proven
  the same way: 6,725 rows identical. France's costliest defects were in
  generators that ran unpiloted over many cities. This batch had none of
  that kind.
- **Privacy moved from repair to design.** In the US, home businesses were
  found after build: San Diego went from 42 to 315 pins removed, Los Angeles
  1,252, and Philadelphia's 0.00% was a false negative. Here the personal
  columns were never downloaded where a server filter allowed it (Tucson's
  home occupations, New Orleans, Den Haag). Each person-shaped name list was
  read by eye: Kansas City 26, Tucson 45, New Orleans 25, Göteborg 13, Zurich
  12. Such a business shows its street address instead of the name, Houston's
  rule. Each city has a recorded privacy verdict; Göteborg's and Zurich's
  exposure checks, run at integration, find no person-like name at a
  residential unit.
- **The checks caught the cross-city damage.** Each new label could move
  another city's: Chicago, San Diego, Houston, Rome, Milan, Oslo and Prague
  all moved. Liepāja alone produced 57 label problems until it came out of
  Europe's zoom fit. In the US batch the label check could not fail. Here
  `check_macro_labels.py` scored every region at three widths, and an
  in-process grid search found clean layouts in about a minute.
- **Licence reading happened in the brief.** The US batch inverted three
  positions after reading what the cited pages said. Here the licences were
  read before the build. The exception was Kansas City's portal terms, read
  just after the build commit: they carried an indemnity that needed an
  owner call.

### What got worse, or is not yet known

- **The briefs were cached guesses with passing checks.** Nine of ten had a
  discrepancy found at build. `brief_check.py` checks the claims a brief
  makes, not the claims it should have made. Canada named this same flaw.
  - Kansas City's brief swapped the name columns. `dba_name` is the holder,
    so following the brief would have published people's names
    ("SURNAME GIVEN-NAME INITIAL") as pins.
  - New Orleans's brief drew a routing RTA no longer runs.
  - Zurich's brief put dance halls out, against category rule R5. Its CRS
    claim was the UTM zone where the build uses LV95, and it said tram 12
    had two city stops where it has one.
  - Den Haag's brief missed a colour pair 2.9 apart.
  - Liepāja's approved call named two added stops where three were needed.
  - Daugavpils's brief counted 38 stations, against 37 built.
  - Several median gaps were off by 11 to 32 m.

  Each was caught by the build's own gates, but only because the build
  re-derived the number rather than trusting the brief.
- **Gate 3 regressed.** Canada and Mexico relied on the operator's own
  station count as the one independent check. In this batch it ran only in
  Odense (25 of 25). Four drafts say "No gate 3", five are silent, and
  Kansas City's station check compared OSM against the brief's count, which
  came from OSM itself. The cause is a skill gap: `osm-rail`'s checklist
  asks for per-line counts wherever the operator publishes them, but
  `tram-city` never mentioned it. Since fixed: `tram-city` now requires gate
  3 for new builds, and a 25-city back-fill is in `PLAN.md` (lesson 1).
- **Parallel agents produced builds that each needed integrating.**
  - Den Haag left an interchange split under two names.
  - Göteborg wrote a coverage tier that only existed on an unmerged branch
    (`one_bucket`, from macro-legend). It was set to `narrowed` until that
    landed, and is now one category (`one_bucket`, with Stockholm) under the
    owner's tier rule.
  - Zurich needed a new national grid in `check_provenance.py` and a
    corrected brief.

  Each fix was small, but each was a judgment the coordinator made after
  the fact, and the agents left owner questions open: Zurich four, Den Haag
  four, Göteborg several.
- **The review backlog is large.**
  - About 30 items are queued for review time: four new numbered notices,
    page sentences outside the template, seven published cities' label
    moves and two zoom-fit changes.
  - France's batch used the same numbers, so at landing every notice from 69
    up was numbered in landing order: France 69-71, Ottawa to Plzeň 72-79,
    the kit's four 80-83.
  - None of the ten maps has been deploy-verified.

  The earlier batches found their worst defects after landing: San Diego's
  home businesses, Calgary's Blue Line 3.3 from the Retail pins, Toronto's
  collapse check. This batch's equivalent count is unmeasured until review
  time.
- **The machine became a shared resource.** Overpass mirrors returned 504s
  under several sessions' load, and memory dropped to 0.5 GB free during
  this batch's last drift check, held by other sessions' rehearsals. An
  orphaned 4.7 GB grep had to be stopped earlier in the day. The US and
  Canada batches ran one or two sessions; this one ran beside at least
  five.

### Not like-for-like

Most of the speed is the cities themselves. Most have 1 to 14 lines and 18
to 180 stations. There were eight template cities to copy (Aarhus, Riga,
Houston, Milan and Rome, Stockholm, Rotterdam and Amsterdam). The briefs
existed before the build. The US and Canada built the infrastructure this
batch used: the scaffold, the exposure check, `stations.py`, `linecolour`,
the briefs, `brief_check`, `heavy_job` and the drafts rule. Their cost per
city includes that.

## Lessons

1. **Put gate 3 in `tram-city`.** Done the same evening (section 2, "Gate
   3"). The operator's per-line counts go in config before step 1 is
   written. A tram step 1 stops on a mismatch. The source must be
   independent of OSM, and where none is published the gap is recorded in
   config. The nine cities built without it land without it (owner): a
   survey found 16 earlier cities in the same state, so all 25 are one
   post-review item for the next deploy (`PLAN.md`).
2. **A brief check passes only the claims written down.** For a tram brief,
   the claims that failed were the name columns, the current routing and the
   CRS. Make those three mandatory checks in every brief (a sample row shown
   with its column names; the operator's current line list, dated; the
   projected CRS from the skill, not the longitude).
3. **Give a parallel agent the branch's own checks, not the latest
   decision.** Göteborg's agent wrote for a branch that had not landed. An
   agent should run every pass/fail check on its own branch before it hands
   off, and name any it expects to fail.
4. **Keep the control-city rule for shared code.** It is why three
   mid-batch changes to `osm_tram.py` cost no rework.
5. **Notice and page numbers need a ledger before a parallel day,** not a
   renumbering after it.

## For review time

All items carry a recommendation in the drafts file:

- The four new notices, as written on the branch:
  Kansas City, Missouri (KCMO's disclaimer verbatim), City of Tucson, Comune
  di Firenze and Gemeente Den Haag (proposed text), written as 69-72 on the
  branch and renumbered 80-83 in landing order.
- Göteborg's coverage flip to `one_bucket` with Stockholm once macro-legend
  lands (done: one category, under the owner's tier rule).
- The two optional `sweden_livsmedel` changes. Each moves Stockholm.
- Zurich's four flags: Dancing / Disco kept, trams 50 and 51 drawn,
  institutional kitchens disclosed, seven colours moved. Drawing 50 and 51
  needs a dated plan item to rebuild Zurich after 12 December 2026.
- Den Haag's four flags: coffeeshops kept, the dwelling rule, tram 10
  peak-only, the notice text.
- Kansas City's thin food service, kept as `full` on Houston's precedent
  (since narrowed, with Houston, under the owner's thin-layer rule, call A2).
- The label moves for seven published cities and the two zoom-fit changes.
- Page sentences outside the template, per city.
