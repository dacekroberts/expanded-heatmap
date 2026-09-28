# Plan


Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md).

Rules that make the rest work:

- **Commit after every green step.** A commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md` as it's made** (see the
  `decisions-entry` skill).
- **Live-verify a city's data before building it** (`add-city` Step 0).
- **Run `python pipeline/drift_check.py` after any pipeline change.**

Legend: `[ ]` open, `[x]` done (a done item stays only until its
`DECISIONS.md` entry exists), `[~]` in progress.

---

## Now

- [ ] Owner: `data/amsterdam/raw/gtfs-nl.zip` (243.8 MB, superseded by
  `gtfs-openov-nl.zip`) and `data/rome/raw/rome_static_gtfs.zip` (46.8 MB,
  downloaded, then not used) may be deleted from the main checkout.

- [ ] ⏰ **Prague: Flora reopens around December 2026**: when PID's feed serves
  it again, step 1 STOPS the build on purpose - remove the override then.

- [ ] Optional label follow-ups (DECISIONS, "Phone-width label placer verified
  and pushed"): a few re-placed labels sit ~54 px from their tip (Amsterdam's
  Metro 51), and labels may sit on cluster bubbles, which the placer does not avoid.

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375px — in the
Canada region as well as the US one.** Found during the run above. NOT a
regression: `fit_view` is byte-identical to the pre-switcher commit and frames
`IN_DEFAULT_VIEW` (US only), so Vancouver was never in the fitted box. But the
switcher makes it newly user-facing, because it now invites a viewer to look at
Canada and Canada still does not frame its own westernmost city. This is the
direct cost of RE-CENTRE-NEVER-RE-ZOOM: centring on Canada's midpoint leaves a
long label 25 degrees west of centre.
Options, in increasing cost: shorten the label to "Vancouver"; give that city a
right-side anchor; or set `REGIONS[i]["zoom"]` for Canada, which exists for
exactly this and costs a re-measure of that region's `label_offset` values.
Desktop is unaffected — the label is fully visible there.


- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20; see
  `DECISIONS.md` and `docs/navigation_sidebar_and_city_links.md`). The
  Overview's fallback link list is kept (decided 2026-09-21). The hop-between-cities
  gap is closed with a "Cities" dropdown on each city map (2026-09-21). Open: the
  final go/no-go. To revert, set `MAP_ONLY_NAV = False` in
  `app/cities.py`.
- [ ] **Overview page colours: the numeric contrast check was never verified.**
  The macro map's marker and label colours now come from `pipeline/theme.py`;
  measure them against the dark page (`#0B1220`) numerically, not by eye.

- [ ] **⏸ AFTER THE LAST VIABLE BUILD: put the cross-city inconsistency list
  on the site** (owner, 2026-09-24).
  - **The list**: `docs/map_inconsistencies.md` (draft, kept current by
    Cleanup) is one place that answers "why does this map differ from that
    one": what each map draws and what is missing, city by city. Readers should
    not have to read each city's prose to learn it.
  - **Placement is deliberately undecided.** The owner wants reminding only
    once every valid build is done: presentation cleanup (mostly prose and UI)
    comes after all the content is on the maps.
  - **Until then**: keep the draft current as cities land, and don't raise
    placement early.

- [ ] **🇲🇽 MONTERREY (REGIONAL) - BUILT 2026-09-27 on branch `worktree-monterrey`, HELD for a
  batch publish with a few smaller cities (owner): 58,565 storefronts, 38 stations, Metrorrey
  Líneas 1–3 across four municipios.** Page 47; text, blurb, notices and the whole-city layer
  approved (owner). Done up to `deploy-verify`: steps 1–3, provenance, scope disclosure,
  inconsistency rows, privacy verdict, label width (144.0) and placement - which moved
  Guadalajara's pill below its dot and Mexico City's 10 px lower. Still to do, at the batch:
  - [x] `deploy-verify` (city-added, plus the Mexico and landing views for the three moved labels) (2026-09-27, one run for the three-city batch: all PASS; DECISIONS)
  - [x] `check_deploy_imports.py` (0 problems) with `.venv-lean` linked, merge master, fetch, push, **reboot**
    (`cities.py` and `components.py` change), live check
  - [x] `city_master_list.md`'s band counts reconciled on the branch, in Staging's wording
    (A 6, Candidates 20, Built 47; 68f656c). **Merge notes from Staging**: if
    `docs/build_briefs/monterrey.md` line 111 conflicts, take master's (the same fix,
    dd3c75a); if Staging's wave-1 rewrite of the band counts lands first, take master's
    numbers and apply the Monterrey move to them - A -1, Candidates -1, Built +1.
  - [x] origin/master merged into the branch early (owner, 2026-09-27): both merge notes
    applied - the brief took master's line, and the band counts are master's with the
    Monterrey move (A 8, Candidates 63, Built 47). The two lines that called Monterrey the
    only Mexican city with a whole-city layer corrected. Merge again before the push.
  - [ ] Retire the `data/` junction and the `monterrey-static-tmp` launch entry

## Next cities, in ease order

- [ ] **Second-city screens, 2026-09-27 (Staging).** Wave 1 done and banded
  (France; Czechia, Norway, Denmark, the Netherlands, Latvia; Korea, Taiwan,
  Hong Kong): see `docs/city_master_list.md` and DECISIONS. Open:
  - [x] **Licence reads for Daegu and Busan** (2026-09-27).
  - [x] **Daegu's brief** (`docs/build_briefs/daegu.md`, 11/11, 2026-09-27,
    corrected the same evening), handed to Main Build. Three owner calls open
    in it (buckets as Seoul's; 대경선 out; stations inside Daegu).
  - [ ] **🇰🇷 DAEGU - BUILT 2026-09-27 on `worktree-daegu` (its own branch, owner), HELD
    for a batch publish: 67,212 storefronts, 86 stations, Lines 1–3.** Page 48. Owner
    calls taken as recommended; the rows end 2025-08-31 (owner: build, date disclosed).
    Done: steps 1–3, drift baseline, provenance rows, inconsistency rows, privacy
    verdict, label width (42.9) and placement (below the dot), DECISIONS. Still to do:
    - [x] Page prose, blurb, credit notice 48, the `excluded_categories.md` section and
      the line colours approved by the owner 2026-09-27, and written.
    - [x] `deploy-verify` (city-added, plus East Asia for the label) - **HELD until at
      least after Busan is built** (owner, 2026-09-27), then run once for both.
    - [x] Publish with the batch (`publish-city`): LIVE 2026-09-27 (pushed 9dc08de, rebooted by the owner, live-checked; DECISIONS). `check_deploy_imports.py` with
      `.venv-lean` linked, merge master, fetch, push, **reboot** (`cities.py`,
      `components.py`), live check. Retire the `data/` junction and the
      `daegu-static-tmp` entry in the monterrey worktree's `.claude/launch.json`.
  - [x] **Busan's brief** (`docs/build_briefs/busan.md`, 8/8, 2026-09-27),
    handed to Main Build. Three owner calls open in it (buckets as Seoul's;
    동해선, recommended out; stations inside Busan with the Busan–Gimhae LRT
    drawn).
  - [ ] **🇰🇷 BUSAN - BUILT 2026-09-27 on `worktree-busan` (its own branch, owner; stacked
    on `worktree-daegu` for the shared Korean module), HELD for the batch: 89,798
    storefronts, 110 stations, Lines 1–4 and the Busan–Gimhae LRT.** Page 49. Owner calls
    taken as recommended. Done: steps 1–3, drift baseline, provenance rows, inconsistency
    rows, privacy verdict, label width (41.9) and placement (below; Daegu's moved to the
    left), DECISIONS. Still to do:
    - [ ] At the owner's review: the page prose, blurb and credit notice 49, drafted in
      chat, and Line 4's darkened blue (#144B7A).
    - [x] Then `deploy-verify` ONCE for Daegu and Busan (city-added x2, plus East Asia). (2026-09-27, one run for the three-city batch: all PASS; DECISIONS)
    - [x] Publish with the batch: LIVE 2026-09-27 (pushed 9dc08de, rebooted by the owner, live-checked; DECISIONS). Pushing `worktree-busan` carried Daegu too. Retire the
      `data/` junction and the `busan-static-tmp` entry.
  - [ ] ⏸ **DEFERRED by the owner 2026-09-27: until the full tram list exists
    AND the second-wave screens are done** (the screens wait for the 10pm
    reset or later; wave 1 was very load-intensive). The tram list's open
    counts are Barcelona's TRAM, Hong Kong Tramways, Seoul's Wirye Line,
    D.C. Streetcar's status and Mexico City's Cablebús (below). **The
    tram-list count runs WITH wave 2** (owner). The rescopes' estimated load
    and a recommendation per category: `docs/tram_rescope_estimate.md`.
    **Band T's group decision**: build trams-only cities, and in what
    order (Nice, Montpellier, Brno and Bergen are the cheapest strong ones).
  - [ ] **Wave 2 held by the owner** (the US; Canada, Brazil and Ireland;
    Spain and Italy), possibly at a reset. Launch only on the owner's word,
    after checking usage and whether main is mid-build. **Its agents use
    `pipeline.osm.fetch`**, not the scratch `ovp.py`: since 2040dfc it refuses
    an all-zero `out count` answer, which the wave-1 scratch fetcher accepted
    (Amstelveen's density is still unmeasured for that reason).
    - **Both load tables, as republished, are saved in
      `docs/load_estimates.md`** (tram rescopes and wave 2).
    - **Estimated load (2026-09-27, judgement; wave 1's cost was never
      recorded)**: about **80–130% of one 5-hour window** (roughly 10–16% of
      the weekly limit), so probably more than one window. The 5-hour window
      is shared by every session, so the anchor may overstate.

      | Group | Estimate |
      |---|---|
      | Tram-list count (read-only, cached OSM) | 5–8% |
      | Canada, Brazil, Ireland (Brazil's national modules exist; Waterloo's ION the one real Canadian lead) | 15–25% |
      | Spain, Italy (registers found city by city; many tram cities) | 30–45% |
      | US (no national register, several sources per city, ~15–20 rail cities) | 30–50% |

    - **Run order, agreed by the owner 2026-09-27**, after the 10pm reset:
      1. The cheapest first: the tram-list count plus Canada, Brazil and
         Ireland.
      2. Read `get_usage` before and after, and rescale the other two
         groups' estimates.
      3. Spain and Italy next. The US waits for a later window if they land
         near the top of their range.
      4. Every screen agent fetches OSM through `pipeline.osm.fetch`.
  - [ ] **Tram rescopes of built cities held by the owner**, likely at the
    next reset; Cleanup's case-by-case list is in DECISIONS (2026-09-27).

- [ ] Idea (Washington D.C.): make `drift_check.py` say plainly when a key-gated
  city's raw input is missing (`WMATA_API_KEY`, a feed that expires), rather
  than report it like any other missing raw input.
- [ ] Idea (Miami, ring coverage 12.6%): consider scoping the all-businesses
  toggle to the station municipalities rather than the whole county.
- [ ] **New Orleans - DEFERRED POST-DEPLOY by the owner (2026-09-21),
  alongside Seattle.** The pre-deploy city scope is the nine that are
  built; this and Seattle's multi-municipality build come after. Findings
  kept so returning costs nothing. Screened 2026-09-21, needs a real
  Step 0.** `iqay-p646`
  "Active Occupational Licenses", 16,396 rows, and the **cleanest licence of
  any candidate: CC0 1.0, explicitly declared**. Has `businesstype`,
  `businessaddress`, `the_geom`. Two sibling datasets exist (`abc4-h3u3`, an
  application-workflow file of 20,956 rows that also carries `naics`,
  `category` and an `ishome` flag; `hjcd-grvu`, 37,902 rows) - pick one
  deliberately rather than merging them. Rail is streetcar-only (RTA's 5
  streetcar lines, dense in the core), which is a **scope** question for the
  owner, not a data one. Privacy flags: `ownername` and `businessphone`
  columns, and the name fields are inverted on some rows (blank `businessname`
  with the trade name sitting in `ownername`) - Boston's trap again.
- [ ] **Seattle - deferred by the owner 2026-09-21, and scoped as the project's
  first MULTI-MUNICIPALITY city.** Do not re-probe the Seattle registry itself;
  the findings are in `docs/build_briefs/seattle.md`, with checks
  (`python scripts/brief_check.py seattle`). On that evidence Seattle's own
  data is the best-equipped of any candidate - an official nightly export,
  **active-only by construction**, 54,604 rows with real NAICS (no new taxonomy
  module), a trade name, and point geometry (no geocoding step). It is on
  ArcGIS rather than Socrata, which is why earlier screens missed it.

  **The owner's intent (2026-09-21): full line coverage, not just the city.**
  This is deliberately the first test of merging several jurisdictions'
  business data into one map, and it **supersedes the standing rule that
  stations in another city are a new project rather than a config change** -
  for Seattle specifically, by the owner's decision. The named jurisdictions
  are Seattle, Shoreline, Lynnwood, Tukwila, Federal Way, Bellevue and
  Redmond. What to check before scoping the work:
  - **The station list is wider than seven jurisdictions.** Link also stops in
    **Mountlake Terrace** and **SeaTac** on the 1 Line and **Mercer Island** on
    the 2 Line; if Federal Way is in scope then the extension also runs through
    **Des Moines** and **Kent**. So plan for roughly ten to twelve, and settle
    the list from the real GTFS stop set against a Washington municipal
    boundary layer rather than from memory - the same discipline that caught
    16 Trolley stations in San Diego and 54 in Los Angeles.
  - **Each jurisdiction is an independent Step 0**, with its own registry,
    schema, classification, coordinate quality, licence and privacy profile.
    Seattle's own data says nothing about Lynnwood's. Expect some to have no
    usable registry at all, and decide up front what the map does where data is
    missing - a gap in coverage is the failure mode that made Boston's
    `Business Inventory` unusable, and it would appear here as whole
    suburbs reading as empty rather than as unsurveyed.
  - **The architecture already supports the taxonomy side.** Taxonomy plurality
    means each jurisdiction can carry its own module mapping into the shared
    three buckets, and `map_common.py` never names a taxonomy, so the map layer
    needs no fork. If several use NAICS (likely in Washington), they share
    `naics` and the merge is mostly plumbing.
  - **What genuinely does not exist yet** is multi-polygon scope: `CITY_KEEP`
    and the boundary filter assume one city. A multi-jurisdiction build needs a
    boundary *set*, per-jurisdiction row provenance on every business (so the
    map can say which registry a pin came from, and so a single city's data
    going stale is visible), and a cross-registry dedup rule for businesses
    licensed in more than one jurisdiction.
  - **Naming stays neutral**: this would be a region, and the project is never
    named after a city - so the page name needs deciding too ("Link light rail"
    rather than "Seattle" may be the honest label if it spans twelve cities).
- [ ] **Fifteen further rail cities were screened shallowly and nothing
  surfaced - that is NOT a disqualification.** Atlanta, Baltimore, Portland OR,
  Phoenix, Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City,
  Tucson, Sacramento, Salt Lake City, Honolulu, Buffalo. Twelve of those
  returned HTTP 404 from Socrata's discovery API, which means "not a Socrata
  domain", and the ArcGIS pass searched titles only. **Seattle proves the
  point**: it came back "no matching datasets" on Socrata and has a 54,604-row
  official layer on ArcGIS. Any of these needs a proper per-portal check before
  being written off. What the shallow screen DID find (from the retired
  `docs/city_shortlist.md`, 2026-09-27): **Baltimore** publishes liquor
  licences only, **Buffalo** contractor licences only (no locations), and
  **Phoenix** has two light-rail lines but no general city business licence.

### 🇯🇵 Japan — the plan (2026-09-24; evidence in `docs/global_country_shortlist.md`)

Ten cities; JR and private railways INCLUDED (owner, 2026-09-24). Measurement:
`scripts/screen_japan_join.py`. Deferred downloads are listed by domain in the
evidence section.

- [x] **Kobe built 2026-09-27** (`worktree-kobe`, held for review time):
  27,251 storefronts, 121 stations, on the shared Japanese steps. Publish
  through `publish-city` at review time (`app/` changes: a new page, notice
  50, Taoyuan's macro label).
- [x] **The `japan-city` skill**, written from Kobe 2026-09-27
  (`.claude/skills/japan-city/SKILL.md`): shared modules, standing calls,
  twelve traps, notices, and a sheet per remaining city. Next city
  recommended: Osaka.
- [ ] **Join control** - like-for-like against the Economic Census per-ward
  飲食店 count (the owner's chosen control) - at build. **Not yet run for
  Kobe**: it needs an e-Stat download (the owner's OK first). Kobe's join was
  checked instead against the Minato control and every screen, and a GSI
  sample in the brief.
- [ ] **Rail** - whether lines served only by limited-express trains count was
  never ruled on (the Shinkansen is out, owner 2026-09-24). **Owner, once for all five.**

### ▶ Handoff to main — the Band A candidates, 2026-09-24

**All 20 Band A cities are buildable**: each has a brief whose checks pass live
and its licences read. The items below are what should be settled BEFORE
main starts a city. Everything else is a decision inside the build, which the
brief names.

- [ ] Owner, minor: アイスクリーム類製造業 (692 rows; many are gelato
  counters) is OUT for now, since the owner's call named 菓子 and そうざい.
- [ ] **Kyoto, at build**: pin `as_of` to the fetch date. Before publishing,
  measure same-address successors and the factory share of 菓子 and そうざい
  (brief, "Still unknown").
- [x] **Japanese build order (owner, 2026-09-24): Osaka → Kobe → Sapporo →
  Fukuoka → Kyoto → Tokyo LAST.** (Kyoto was added later the same day, owner.) The stub test cleared the first four: every urban
  line keeps 80–100% of its stations inside the city line. Tokyo failed, with
  Chiyoda missing from the centre of its 8 wards. Tokyo goes last as the
  densest, and it benefits most from a Japan skill written off the first four.
  Kyoto sits after Fukuoka, before Tokyo (owner, 2026-09-24): Japan's first
  rebuilt register benefits from the join being settled on four cities first.
- [ ] **Tokyo — the missing wards as a planned project, before its build.**
  Chiyoda alone lifts urban station coverage from 45% to 56%; Chiyoda,
  Toshima and Bunkyō reach 67%; all 23 wards reach 98% (`tokyo.md`).
  Routes: request Chiyoda's ledger (owner, gated item 22); extract Ōta's,
  Kita's and Arakawa's PDF lists; Shinagawa's and Itabashi's partial files;
  requests to Toshima, Nerima and Edogawa.
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32). Not sent, and not the next step.
    The own-time probe round found nothing that fills the gaps openly (DECISIONS).
- [ ] **PARKED by the owner 2026-09-27 (conserving usage) - come back to it.** **Trams left
  off built maps - owner decides case by case (listed 2026-09-27, after "trams count").**
  **Estimated load and Staging's recommendations, saved for later (owner, 2026-09-27):
  `docs/tram_rescope_estimate.md`**:
  - the tram list first (it runs with wave 2);
  - the light batch yes, REM first, D.C. once its service is verified;
  - Paris T3 yes;
  - the heavy three (Toronto, Milan, Prague) not yet: a label and legend
    rule first, then a Toronto pilot;
  - Barcelona likely yes, Hong Kong Tramways stays out, Cablebús yes;
  - one batch overhead. About 55–85% of one 5-hour window in all.

  Read-only list; nothing rescoped. Stops = distinct stop names in scope,
  from cached GTFS/OSM. Rescoping is main's work, city by city, after the owner decides.
  - **Recorded reason was only "not rapid transit / overlay" (reversed by the rule):**
    Toronto streetcars (18 routes, 476 stops); Milan (17 routes, 323 of 341; ATM publishes
    no colours); Prague (37 routes, 285); Paris T3a/T3b + edges of T2/T9 (62); Barcelona
    TRAM T1-T6 (not counted - cache has no tram relations); Rome tram 8 (40; lines 2, 3, 5,
    14 have no trips in the GTFS); Hong Kong Tramways (not counted - OSM query skipped
    trams; excluded by the owner 2026-09-24).
  - **Mixed or close:** Madrid Metro Ligero ML1 (9, run by Metro de Madrid); SF F Market
    (46, heritage cars on a regular route); Fortaleza diesel VLT (11, every 40 min - failed
    the rail test); D.C. Streetcar and Montreal's REM (both silent omissions). **D.C.
    Streetcar: no longer operating** (DDOT ended it 2026-03-31; checked 2026-09-27).
  - ▶ **IN PROGRESS 2026-09-27 (owner cleared light and medium): specs for REM, Rome 8,
    Madrid ML1, Paris T3a/T3b and SF F Market in `docs/tram_rescope_specs.md`**, handed to
    Main Build to implement on a branch held for review time.
  - **Reason still stands:** SF cable cars, Rio Santa Teresa, Santos, Lille Amitram
    (heritage); Copenhagen Letbane, Marseille Aubagne, Philadelphia NHSL/D1/D2 (no stop in
    scope); Amsterdam tram 3 (no trips until 2026-12-12); Rotterdam 12/14/18 (event or
    works routes); Seoul Gimpo Goldline (1 stop, already drawn); Recife VLTs (fail the rail
    test); Porto Alegre Aeromovel (people mover).
  - **Blind spots:** Seoul's OSM query takes only subway/light_rail/train (Wirye Line
    unverified); Hong Kong's and Barcelona's caches hold no tram relations. Mexico City's
    Cablebús is also unstated (Toulouse's drawn Téléo is the precedent).
    `docs/map_inconsistencies.md` shows D.C. as "—", which is incomplete.
- [x] **An honest efficiency review of the whole PROCESS, the owner's habits included (owner,
  2026-09-24)** DONE 2026-09-27: findings in `docs/efficiency_review_2026-09-27.md`, the
  owner's order in DECISIONS (2026-09-27). Follow-ups, in that order:
  - [x] **Change 2 - batch approvals and deploys.** DONE 2026-09-27: queued for "review time",
    which only the owner calls; `app/` lands in one batch under one reboot. Rule and reminder
    threshold in memory (`batched-review-time`) and the `publish-city` skill.
  - [x] **Change 3 - trim what every session loads.** DONE 2026-09-27 (DECISIONS): CLAUDE.md
    4,345 -> 1,685 words, history verbatim in `docs/rule_history.md`; PLAN.md 20,675 -> 3,136
    words; `scripts/check_all.py` as `.githooks/pre-push`. The 7-day DECISIONS index was
    dropped (owner).
  - [x] **Change 1, half - archive DECISIONS.md.** DONE 2026-09-27, WEEKLY rather than
    monthly (owner; DECISIONS): `scripts/archive_decisions.py` at the start of each week,
    guarded in `merge_append_only.py`, proven by `archive_decisions_selftest.py`.
    DECISIONS.md 222,930 -> 8,490 words.
  - [ ] **Run `python scripts/archive_decisions.py` at the start of each week** (cleanup
    session, after the Sunday reset). Next: 2026-10-04. In the same sitting run
    `python scripts/efficiency_metrics.py --baseline` and show the owner the table: it is what
    the owner's session-count decision waits on (baseline in
    `docs/efficiency_review_2026-09-27.md`).
  - [ ] **The session count** - how many sessions run at once. A separate owner decision.
  - [ ] **The remaining findings, walked through with the owner** (asked 2026-09-27): 5
    (hand-kept documents that churn, e.g. a generated master list), what is left of 4
    (re-render batching beyond change 2), then 7.
  - Original item, kept for its method: only if the week's budget allows, at the start of a week, as ONE agent in
  its own context. Not a code review: how work gets done, verified, approved and shipped.
  - Evidence, not impressions: git history (`git log --since`, merge counts, files rewritten
    per day), the size of what every session loads, DECISIONS' index (never the whole file),
    `get_usage`, `check_*` run counts, approval round-trips per change.
  - Starting figures measured 2026-09-24 - verify, don't trust: DECISIONS.md ~210k words
    (~280k tokens), conflicting on every two-session push (archive older entries by month?);
    CLAUDE.md ~4,200 words loaded every session (how much belongs in skills/docs?);
    `docs/data_sources.md` ~52k words, PLAN.md ~16.7k; 2026-09-24 on master: 179 commits, 43
    merges, 286 `heatmap.html` rewrites (~seven full re-renders - batch renderer changes?);
    16 skills, 2 agents, 17 `check_*` scripts (which earn their keep?).
  - The owner's end, stated plainly: per-change wording approvals vs a batched review;
    batched `app/` pushes under one reboot; whether parallel sessions sharing one weekly
    limit spend more on coordination and merges than they save.
  - Deliverable, drafted for the owner: a ranked list (finding, evidence, estimated saving,
    whose habit - owner, session or structure), the top three changes, and a rough weekly
    saving for each. The owner decides.
- [ ] **Toronto's retail share** (`docs/map_inconsistencies.md` Q18): the baseline's buckets
  (870 of 19,575) and the cleaned rows the map draws (814 of 19,384) are both real. Settle by
  reading Toronto's step 2, not by editing a number.

**Not ready for main:**
- **Band C (7)** — one owner decision moves all seven: does a single-bucket
  page belong beside three-bucket cities? Yokohama (personal services only)
  has no page for now, whatever the answer (owner, 2026-09-24).
- **Band D (7)** — each waits on an owner act or on access:
  - Sendai's request (drafted) and Kaohsiung's request;
  - reads from inside Poland, India, Finland (Helsinki) and Estonia
    (Tallinn), by a person there, never a proxy;
  - Lisbon's DGAE account (item 28);
  - Tallinn's EHR order (item 23).
- ✅ **The open gap is empty** (2026-09-24): its last eight each got a verdict
  after a final re-probe.

**Owner's outside actions** are tracked in `docs/gated_access.md`, the list of
every key, account and letter:
- [ ] Item 21: send Sendai's request (`docs/notifications/sendai-permission-request.md`).
- [ ] Item 22: request Chiyoda's ledger.
- [ ] Item 23: place the Tallinn building-register orders (two reports).
- Items 25–27 (Hiroshima, MHLW, Osaka) are optional confirmations, not gates.

## Structure

- [ ] Idea: a smoke check that re-fetches every recorded endpoint and asserts a
  plausible content type - an endpoint recorded but never re-run is not verified
  (San Francisco's `data.sfgov.org` redirect wrote a 654-byte HTML stub, 2026-09-21).

## Before deploying

- [ ] **Philadelphia's permission request** (`docs/gated_access.md` item 12;
  DECISIONS, "Philadelphia: ask for permission, stay up on a reasoned position
  meanwhile"). The footer (`components._UNSETTLED_TERMS`) discloses it meanwhile.
    - [ ] **Follow up on 2026-09-28** (one week), at the owner's request. The
      owner SENT the request on 2026-09-21 to `maps@phila.gov`, copying
      `LIGISTEAM@phila.gov` (text in
      `docs/notifications/philadelphia-permission-request.md`). No
      reply as of 2026-09-21. If still silent: wait, chase once, or ring the Open
      Data Program. **Silence is not consent** - the interim position holds on
      the reasoned reading and the disclosure, not on the absence of an
      objection, and it does not strengthen with time. Sending it is the owner's to do. **Nothing in this project may
      claim a request is outstanding until it has actually been sent**, and
      silence must never harden into a claim that permission was given.
    - [ ] On a reply, follow the branch already written into that file: on
      permission the footer clause loses its only live subject and comes out
      entirely; on refusal Philadelphia comes off the site, and the remaining
      eastern cities' macro-map label offsets need re-checking at 854 and
      1200 px, because removing a marker moves `fit_view`'s bounds.
- **Reference, if the repo ever goes private** (it stays PUBLIC; DECISIONS, "Pre-deploy
  gate"): Streamlit Community Cloud supports private repos on the free tier, but
  needs the broader `repo` OAuth scope plus a deploy key, and its one-private-app
  limit needs checking; `outputs/` must stay committed either way.
- [ ] Optional: request a free Carto API key and set `CARTO_API_KEY` in the
  Streamlit Cloud secrets (the macro map uses Carto's keyless CDN; DECISIONS,
  "Pre-deploy gate").

## Data quality follow-ups

- [ ] Los Angeles: ~9% of registry rows have no NAICS code; consider whether
  the caveat needs to be visible on the city page.

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.

## Later / maybe

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
