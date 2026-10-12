# Plan


Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md). Done items moved out at a
weekly archive are kept verbatim in [`docs/plan_done/`](docs/plan_done/).
A long open item keeps one or two lines here and its detail in
[`docs/plan_detail/`](docs/plan_detail/), under the heading its line names
(since 2026-10-08).

Rules that make the rest work:

- **Commit after every green step.** A commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md` as it's made** (see the
  `decisions-entry` skill).
- **Live-verify a city's data before building it** (`add-city` Step 0).
- **Run `python pipeline/drift_check.py` after any pipeline change.**

Legend: `[ ]` open, `[x]` done (a done item stays only until its
`DECISIONS.md` entry exists), `[~]` in progress.

Detail files: [japan](docs/plan_detail/japan.md),
[labels and macro map](docs/plan_detail/labels_and_macro_map.md),
[city watch](docs/plan_detail/city_watch.md),
[data and disclosure](docs/plan_detail/data_and_disclosure.md),
[process and tooling](docs/plan_detail/process_and_tooling.md).

---

## Now

- [ ] **From the portfolio review (owner, 2026-10-11; DECISIONS, that day),
  in order:**
  - [~] Phase 2 runs with no weekly usage stop; one usage check-in with the
    owner when it finishes (`docs/build_plan_2026-10-07.md`).
  - [ ] When the batch lands: give the owner the city count, read from
    `app/cities.py`, for every "about N cities" line in his other projects.
  - [ ] After the phase 2 landing: draft a handoff file for transit-globe to implement ITS OWN search feature
    (owner, 2026-10-12, in Cleanup's chat; Cleanup drafts it, which
    replaces the earlier "his to write"). It names the index files that
    feature needs (the per-city place index and the intersections file
    under `app/static/places/`, their format, and the ODbL credit they
    carry) and lets the app filter out search terms outside its scope.
    The app stays independent: it reads our export read-only, borrows no
    code, and the handoff is a full build-and-decisions account for it to
    critique, with every pilot-only choice named (owner, 2026-10-07 and
    2026-10-08). A draft for the owner to read before it goes over.
  - [ ] **The commercial-use audit, after the batch lands:**
    `docs/commercial_use_positions.md`, for transit-globe's decisions only
    (this site stays non-commercial). One row per city, layer and source;
    the weakest source in use decides the city's column (allowed,
    blacklisted, held), with "allowed if layer X is left out" where true; a
    source whose read never addressed commercial use is held. From the
    record first, then one `licence-read` per source transit-globe wants.
    A script confirms every `app/cities.py` city appears once. The review
    session's first draft is the starting point, not a source. **The same
    pass answers public sharing** (owner, 2026-10-11): which analytics and
    visuals pieces could go public, with what notices and which cities
    removed; Analytics supplies its pieces and the cities each uses.
  - [ ] **Per-category city totals in every city's
    `outputs/<slug>/baseline.json`, after phase 2 lands** (owner,
    2026-10-11, for Analytics; an exception to the freeze), in the same
    pass as the held Japanese re-render: `storefronts`,
    `storefronts_retail`, `storefronts_food_service`,
    `storefronts_personal_services`, as the Japanese cities carry them.
    Counted AFTER the renderer's contact-detail screen, so they match
    the map (Rouen and Seattle differ by one row today). 61 cities carry
    the keys; 33 have no `baseline.json`. Size it first: no one shared
    writer was found.
  - [ ] ⏸ Waiting on the owner: whether the cross-city chart goes public
    (a PRIVATE draft is approved, Analytics', on the measure "share of
    Food service storefronts within 0.3 mi of a station"; owner,
    2026-10-11), home-page utility copy (suggestions only), and the
    prose pass against the tone guide (about 2026-11-07; the guide loads
    from the owner's global CLAUDE.md; changes are reported per page, never
    applied).

- [ ] **At the phase 2 landing (owner, 2026-10-11; DECISIONS, that day):**
  - **Bucharest's name repair, a privacy repair on a published map:**
    apply Kansai-2's `name_kind_extended()`
    (`pipeline/taxonomies/romania_dsvsa.py`, arriving with Cluj-Napoca)
    in Bucharest's step 2, so a company named as a given name beside one
    other word shows its category: 127 pins, 93 names, measured. Then
    re-render, `check_personal_exposure.py bucharest`, and the verdict in
    `docs/privacy_verdicts.md`. The "on two or more premises, so a
    brand" exception is NOT applied: every such name stays withheld
    (owner, 2026-10-12).
  - Osaka's three lines renamed "Osaka Metro ..." at its held re-render,
    as the line registry has them; drift checks for Suita, Osaka and
    Bucharest.
  - After it, at a review time: move Bucharest's address and name
    functions, which Cluj-Napoca's step 2 imports, to a shared module.
  - **Branches, nothing pushed:** `worktree-japan-east-2` (11 cities),
    `worktree-japan-kansai-2` (7 and Cluj-Napoca),
    `worktree-japan-regional-2` (11); each has its drafts file and a
    handoff note. The owner's calls below were given in the build
    sessions' and Staging's chats and are recorded in those drafts
    (S numbers are Staging's).
  - **First: Regional-1's eleven cities are missing from
    `app/osm_notice.py` and `_OSM_STATION_NAMES`** (verified on master,
    2026-10-11), so their live pages show no OpenStreetMap station-names
    line; the map's corner credit is in place. Reported and not
    verified: notice 1's sentence stops at "Tachikawa and Hino". At the
    landing, first, not alone (owner, 2026-10-12).
  - **Shared-code changes, Cleanup's (S14):** S1, `glitched_name` treats
    U+E000 to U+F8FF as glitched (measure the built maps first;
    Kawaguchi is held on it); S2, a late start whose first-permit date
    is on or before the list's date stays (Kawaguchi gains about 100
    pins); S17, 自動販売形態 into `japan_eigyo.FORM_RULES` (83 vending
    pins; Kurashiki re-runs steps 2-3); S19,
    `japan_register.permits_from_rows` tests the area-wide rule after
    the city cut, Tottori's hook deleted (reproduce 237 area-wide, 2,240
    storefronts); call 182, Yamagata's permit-match name rule moved from
    its config into `japan_step2` (it flags 3 rows, the brief counted 4).
    Each with the Minato control and a Japan drift run. S18: read
    Kurashiki's 8 特殊形態 pins, then a rule only if needed.
  - **Lines:** JR Keiyo to `#C81000` in the registry (S3), Tokyo's own
    literal switched to the registry, the dark-mode label check run (it
    was not; 10.2 from the Keikyu Main Line), then Tokyo, Funabashi,
    Ichikawa and Urayasu re-rendered; a `NEIGHBOUR_EXCEPTIONS` entry with
    a note for Okazaki's Meitetsu Nagoya Main Line and Toyota's Mikawa
    Line (S16).
  - **Macro map (Cleanup's, call 198):** Minoh, Fuji and Kurashiki are
    labelled in no view; `TEXT_WIDTH` lacks "Ibaraki (Osaka)", "Yao" and
    "Takatsuki".
  - Cluj-Napoca publishes under notice 215, treated as Bucharest (S8).
    It takes Bucharest's hold off public pieces (owner, 2026-10-12), in
    the downstream note.
  - Staging moves the master list's cities to Built after the landing
    (`check_provenance.py` fails on the branches until then).
  - **Deferred from the phone legend (owner, 2026-10-12: "defer both"),
    for a tested change that rides a later re-render** (the search
    rollout's waves re-render every city). The 40% cap with its own
    scroll LANDED with phase 2 (measured 224 px of a 560 px frame on
    Tokyo). Not built:
    - folding the lines by operator past a measured threshold. Place
      search reads the legend's line rows (`aria-pressed`), so the fold
      changes what search sees: test the two together.
    - the map frame's height on phones. One CSS rule in the app is NOT
      enough: the map is a fixed 650 px inside its frame (only its width
      follows the frame), so a 560 px frame puts the OpenStreetMap credit
      at 636 to 650 px, out of view (measured 2026-10-12). The map's
      height has to follow the frame inside the phone-fit script
      (`pipeline/map_common.py`, the one with the load-race history),
      then `check_map_view.js`, `check_map_labels.js` and
      `check_map_attribution.js` at phone heights, and the owner's iPhone.
  - **A repair pass for names holding a private-use character** (owner,
    2026-10-12, with S1): 1,797 names in 29 cities show their category
    since S1. Where one publisher uses one code point for one known
    character (two code points cover 228 of Osaka's 787), restore the
    character, as "Caf?" is restored; verify each mapping against the
    publisher's file first.
  - OPEN: the Global View button on Seattle (Regional)'s map does
    nothing on the owner's iPhone (reached from its Overview dot; the
    button works on Tokyo's map); not reproduced at 375 px by a
    scripted click.
  - **The order, and what is not here:**
    `docs/handoff_cleanup_2026-10-12.md`.
  - Place search (branch `place-search`, 28b1ecb8 and later): the
    owner's phone test of São Paulo, then London, before any rollout;
    the stations OSM draws as not yet open are an internal watch file
    on the branch with its check, no per-city page text; one general
    sentence for About the Data is approved (the handoff has it).
  - **FIRST after the phase 2 landing, before the rollout or the audit
    starts: the skills that make both cheap** (owner, 2026-10-12). **The
    order after the landing (owner): 1. these skills; 2. the DeepSeek
    integration (the owner's own handoff, read and started in a new
    session); 3. everything else** (the search rollout, the
    commercial-use audit, the label batch).
    - **`search-city` skill**, with what it rests on: one script that
      scaffolds every remaining city's search config and thin index step
      (area from the boundary already in the repo, languages from
      `travel_packs.LOCAL_LANG`); an unattended fetch queue over
      `place_index_fetch.py` with a LOCK in the fetch script for the
      one-query rule (a lock guards a queue and any outside model, a hook
      only a Claude session); the flagged-name review as one request per
      city (names and a fixed rubric in, a verdict per name out as JSON),
      the step a cheaper model can take overnight, sampled afterwards;
      visitable former homes left out of the rollout; one re-render and
      one sampled deploy-verify per wave. The lane lessons of this
      landing go in it: a lane server needs `--server.enableStaticServing
      true` or the index never loads, Travel draws only on ports 8501 and
      8000, the hidden pane needs the frame and timer method
      (`docs/review_lane_kit.md` 7b).
    - **The size projection, measured 2026-10-12: about 190 MB at 237
      cities (models range 180 to 280 MB), about 50 MB gzipped, not the
      475 MB of the flat extrapolation.** The 19 built indexes are 39.2
      MB (10.0 MB gzipped) and are the large cities: their median station
      box is 638 km2 against 138 km2 for the 218 left. Fitted log-log on
      stations drawn, the stations' bounding box and storefronts
      (leave-one-out: median miss a factor of 1.26, total 8% low); the
      median city left projects at 0.43 MB, 117 under 0.5 MB, four over 3
      MB (Los Angeles, Taipei, Guadalajara, Rio de Janeiro). Limits: 30
      cities are smaller than any built index, the index covers a boundary
      and the predictors only stations, and Mexico City's rebuild adds to
      its 6.1 MB. Re-measure after the first wave. The wave order is the
      owner's, now that the figure is in.
    - **`commercial-use-audit` skill**: the question and the verdict
      shapes (permitted, permitted with a condition, forbidden, silent)
      under the owner's rules of 2026-10-11; each DISTINCT source audited
      once and fanned out to its cities, counted first; a table that
      settles the standard licences (CC BY 4.0, ODbL, the government open
      licences) with no read; a first pass by a cheaper model over the
      STORED licence texts that returns a verdict and the sentence it
      rests on, with a script confirming the sentence is in the stored
      text; Claude reads the silent and conditional ones and a sample of
      the permitted; the owner decides the forbidden and unclear. A wrong
      "permitted" is the costly error: the cheaper model finds and
      quotes, it does not give the final verdict, and its reading of
      Japanese and Korean terms is tried on known sources first.
    - Nothing from a business register goes to an outside model; an API
      key never enters the repo.
  - **Search rollout, first wave: Mexico City's index is rebuilt for the
    regional map** (owner, 2026-10-12: "fix in search rollout"). The
    index landed cut to Mexico City proper: the 11 stations in the four
    State of México municipios are not in it, and it holds 0 or 1 places
    within 1 km of each (median 145 for the other stations; measured on
    `app/static/places/mexico_city.json` against
    `processed/regional/stations.csv`). Widen `PLACE_AREA` to the four
    municipios, re-fetch (`place_index_fetch.py`), rebuild, re-render the
    map. Check whether Mixcoac is indexed as the one junction row.
  - **Idea for the next landing (owner, 2026-10-12): a button that
    returns a map to its starting view.** After a search the map stays
    at the found place and nothing restores the city-wide view (the
    marker and the fade end after 12 s on their own; clearing the box
    does not end them early). The button is an ICON, no words, in the
    family of the layer control and the search button. If the button row
    gets crowded, this may be the reason to move the Cities menu out of
    it. Not decided: whether clearing a search should also end the fade
    at once. Shared map code, so it rides a re-render (the search
    rollout's waves); measure the button row at 343 px first.

- [ ] **Next landing:**
  - Phase 2 Japanese cities (East-2, Kansai-2, Regional-2) and Cluj-Napoca,
    on the owner's go (Cluj-Napoca waits on call 215, the placement bar).
  - Place search, if the Kyoto pilot reports well.
  - **After the reset, one label batch:** Ostrava's Tram 14 (2.1 px under
    the button row at 854; fix in `_layout_labels`, measuring first how many
    of the 206 maps reframe), Osaka's three labels at 375, the Overview's
    343-vs-333 scorer canvas, then Los Angeles (Regional) and Rio de Janeiro
    (Regional) re-placed. `docs/plan_detail/labels_and_macro_map.md`, "After the reset, one label batch".
  - Follow-ups: UK line colours, day-first notices, "45 from every pin"
    configs, caterers' counter forms. `docs/plan_detail/process_and_tooling.md`, "Next landing follow-ups".
  - **Branch `legend-dot-georgia` (16a68efe, Cleanup's, local; worktree
    `.claude/worktrees/review-prep`), lands at review time:** legend dots
    10 px that never shrink (the owner's iPhone check), Tbilisi in Europe
    East, the phone's region dropdowns take no typing (`filter_mode=None`),
    Analytics' four map issues with Ōita's masked-name clause as a proposal
    (`docs/plan_detail/japan.md`, "From Analytics (2026-10-08)"; DECISIONS,
    2026-10-08, all), the neutral wording of the maps'
    embedded comments, and the sign rule on all 64 Japanese pages. All 206 maps re-render once at the
    landing, with place search's five; app reboot (`app/cities.py`).
  - `scripts/stress_overview.py` stops on master: 23 Japanese cities of the
    last batch missing from `BUILT_PREF`.
  - ⏸ **HELD until every Japanese city is built (owner, 2026-10-11):
    the re-render of the built Japanese cities on `WAVE5_RULES`**, once,
    after phase 2 lands, over the list drawn up then (it read "the 34
    built" and named no list; 64 are built). Toyota first, call 158 with
    it. Not held: Japanese
    shared-code fixes, five credits (notices 157, 161, 178, 184, 186) and
    three Kansai-1 briefs. `docs/plan_detail/japan.md`, "Kept from the drafts' notes at the
    2026-10-08 fold".

- [~] **This week (from the 2026-10-11 reset), the final scoped adds (owner,
  2026-10-11):** phase 2, the last build wave; place search batch 3
  alongside it; the site's partial Travel view, which waits on the owner's
  go-live call and hosting (the basemap branch's resume note, five
  blockers). Nothing else new (the freeze of 2026-10-08).

- [ ] **A site-wide junk-name pass once the final batch lands** (owner,
  2026-10-08, via the place-search pilot): no dot shows an error value or
  placeholder ("#N/A", "nan", "None", "Untitled", U+FFFD, a name with no
  letter). Reuse `pipeline/place_index.junk_name` (place-search branch) and
  keep it as a standing check in `check_all`; `map_common.glitched_name`
  already hides "?"-only names (legend-dot-georgia). Gaps found 2026-10-08:
  U+FFFD is not caught (only the Korean readers strip it, silently); CJK
  Extension A is in `_CJK_RE` but not `_LETTER`; `_has_contact_details`
  misses non-NANP phone formats (place search's `place_index._CONTACT`
  already has trunk-prefixed Japanese and Korean numbers: merge it).

- [ ] **A site-wide code audit after the reset and the final city builds**
  (owner, 2026-10-08); scope and lanes set with the owner first. `docs/plan_detail/process_and_tooling.md`, "A
  site-wide code audit".

- [ ] **Review time, two process slips (Staging, 2026-10-08):** Kurashiki's
  PDF text printed four operators' names to Staging's console (nothing
  published or committed); a licence-read agent ran `taskkill` on grep.exe
  by image name, which stops every session's grep: stop a process by PID.

- [~] **The Japanese pages' name-rule bullet gains the sign rule: APPROVED
  2026-10-08, on `legend-dot-georgia`, all 64 pages** (the eight whose
  lists name no operator by the owner's wording of the same day); lands at
  review time.
  `docs/plan_detail/japan.md`, "The name-rule bullet's sign rule".

- [ ] São Paulo's Linha 6-Laranja stays out until full service (sentence
  OK'd); re-check when it leaves trial operation.

- [ ] **Overview at phone width:** correct the scorer's 375 px canvas (343
  vs 333 measured), then re-place Los Angeles (Regional) and Rio de Janeiro
  (Regional). `docs/plan_detail/labels_and_macro_map.md`, "Overview at phone width".

- [ ] **Heavy-job gate follow-ups (2026-10-03):** Japanese drift memory, and
  orphaned children in the ledger. `docs/plan_detail/process_and_tooling.md`, "Heavy-job gate follow-ups".

- [ ] **Left by the 2026-10-03 lanes batch:** Rome's tram 3 and Oslo's tram
  13 need fresh pulls; owner: SFMTA's clause 4. `docs/plan_detail/city_watch.md`, "Left by the
  2026-10-03 lanes batch".

- [ ] **The UK six's watch items:** Birmingham's Metro Line 2 (due about 1
  November 2026) and Eastside stops; Sheffield's Shalesmoor and second
  bucket. `docs/plan_detail/city_watch.md`, "The UK six's watch items".

- [ ] ⏸ **Per-city restriction disclosures on every city's page (owner,
  2026-09-28): ask the owner for general advice first, then wait.** `docs/plan_detail/data_and_disclosure.md`,
  "Per-city restriction disclosures".
  - [ ] ⏸ **Per-city wait times as data: TABLED (owner, 2026-09-30)** until
    the owner is back at a desktop. `docs/plan_detail/data_and_disclosure.md`, "Per-city wait times as data".
  - [ ] **Japanese cities onto N02-25**, one drift check per city: six
    left on N02-24 (Tokyo, Kobe, Sapporo, Fukuoka, Kyoto, Yokohama; the
    pass of 2026-10-11 read `pipeline/countries/japan.py`). `docs/plan_detail/japan.md`,
    "Japanese cities onto N02-25".
  - [ ] **City-map legend model (2026-09-30):** the obstacle becomes
    max(model, a content-based estimate). `docs/plan_detail/labels_and_macro_map.md`, "City-map legend model".
  - [ ] **Published-city date fixes (2026-09-29):** (a) and (b) done; (c) Milan
    done, New York State and Surrey open; (d) to (f) open, three owner
    calls (the pass of 2026-10-11); Philadelphia re-read around 2026-10-13. Review time. `docs/plan_detail/data_and_disclosure.md`,
    "Published-city date fixes".
  - [ ] **Toulouse and Rennes: did step 1's name-level fallback fire?** NOT
    confirmed by the 2026-10-11 pass: one read-only step 1 run per city
    settles it. `docs/plan_detail/city_watch.md`, "Toulouse and Rennes".

- [ ] ⏰ **Prague: Flora reopens** (about the end of February 2027): remove
  the override then. `docs/plan_detail/city_watch.md`, "Prague: Flora reopens".

- [ ] Optional label follow-ups (DECISIONS, "Phone-width label placer
  verified and pushed"). `docs/plan_detail/labels_and_macro_map.md`, "Optional label follow-ups".

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375 px.**
  `docs/plan_detail/labels_and_macro_map.md`, "Vancouver (Regional) clipped".

- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20): the
  final go/no-go. `docs/plan_detail/labels_and_macro_map.md`, "Map-only navigation pilot".
- [ ] **Overview page colours: the numeric contrast check was never run.**
  The macro map's marker and label colours come from `pipeline/theme.py`;
  measure them against the dark page (`#0B1220`) numerically.

- [ ] **The category fix batch:** landed with review-batch-2; left and
  READY (stockholm-catering has landed; the continuity check queues one
  approved fix), Stockholm's torghandel stall (still `pending` in
  `scripts/category_continuity_table.py`). `docs/plan_detail/data_and_disclosure.md`, "The category fix batch".
- [ ] **Next cross-city discrepancy audits (owner, 2026-09-29):** six,
  read-only, one at a time. `docs/plan_detail/data_and_disclosure.md`, "Next cross-city discrepancy audits".

## Next cities, in ease order

- [ ] **Second-city screens (Staging, 2026-09-27).** Waves 1 and 2 are done
  and banded (`docs/city_master_list.md`, DECISIONS). Open:
  - [ ] **Wave-2 follow-ups** (run 2026-09-30): owner calls on Richmond and
    on reads from the owner's own browser; group 2's watch list. `docs/plan_detail/city_watch.md`, "Wave-2 follow-ups".
  - **Watch items from group 1:** `docs/plan_detail/city_watch.md`, "Watch items from group 1".
  - [ ] **Tram rescopes of built cities held by the owner**; Cleanup's
    case-by-case list is in DECISIONS (2026-09-27).

- [ ] Idea (Washington D.C.): make `drift_check.py` say plainly when a
  key-gated city's raw input is missing (`WMATA_API_KEY`, an expiring feed).
- [ ] Idea (Miami, ring coverage 12.6%): scope the all-businesses toggle to
  the station municipalities rather than the whole county.

### 🇯🇵 Japan — the plan (2026-09-24; evidence in `docs/global_country_shortlist.md`)

JR and private railways INCLUDED (owner, 2026-09-24). Measurement:
`scripts/screen_japan_join.py`. Re-run the census join control
(`scripts/japan_census_control.py`) with each new Japanese city.

- [ ] **Madrid's 343 px touch:** widen `DENSE_LABEL_SCRIPT`'s trigger and
  re-render Madrid. `docs/plan_detail/labels_and_macro_map.md`, "Madrid's 343 px touch".
- [ ] **Berlin:** U6 to Alt-Tegel about August 2027; refetch before VBB's
  calendar ends 2026-12-12. `docs/plan_detail/city_watch.md`, "Berlin".
- [ ] **London:** refetch before the FSA extracts age. `docs/plan_detail/city_watch.md`, "London".
- [ ] **Buenos Aires:** SBASE refetch (the inconsistency list's rows are in). `docs/plan_detail/city_watch.md`, "Buenos Aires".
- [ ] **Kyoto:** add the August 2026 list when published. `docs/plan_detail/japan.md`, "Kyoto's
  August 2026 list".
- [ ] **Osaka's Umekita → 福島 stretch:** a re-render for review time. `docs/plan_detail/japan.md`,
  "Osaka's Umekita stretch".

### ▶ Handoff to main — the Band A candidates, 2026-09-24

Each Band A city has a brief whose checks pass live and its licences read;
decisions inside a build are named in its brief.

- [ ] Owner, minor: アイスクリーム類製造業 (692 rows; many gelato counters) is
  OUT for now; the owner's call named 菓子 and そうざい.
- [ ] **Tokyo: the missing wards** (built 2026-09-28 with 8 of 23). `docs/plan_detail/japan.md`,
  "Tokyo: the missing wards".
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32), not sent and not the next step.
- [ ] ⏸ **Trams left off built maps: PARKED (owner, 2026-09-27); the owner
  decides case by case.** `docs/plan_detail/city_watch.md`, "Trams left off built maps".
- [ ] **Efficiency review follow-ups:** the weekly `archive_decisions.py`
  run, due 2026-10-11 and HELD until phase 2 finishes (owner, that day:
  the build prompts cite entries in `DECISIONS.md`); owner: the session count and the remaining findings. `docs/plan_detail/process_and_tooling.md`,
  "Efficiency review follow-ups".

**Not ready for main:** Band C, waiting on the owner; Band D is empty
(counts in `docs/city_master_list.md`, never here).
`docs/plan_detail/city_watch.md`, "Not ready for main".

**Owner's outside actions**, tracked in `docs/gated_access.md`:
- [ ] Item 21: send Sendai's request (`docs/communications/sendai-permission-request.md`).
- [ ] Item 22: request Chiyoda's ledger.
- [ ] Item 23: place the Tallinn building-register orders (two reports).
- Items 25–27 (Hiroshima, MHLW, Osaka) are optional confirmations, not gates.

## Structure

- [ ] Idea: a smoke check that re-fetches every recorded endpoint and asserts a
  plausible content type - an endpoint recorded but never re-run is not verified
  (San Francisco's `data.sfgov.org` redirect wrote a 654-byte HTML stub, 2026-09-21).

## Before deploying

- [ ] **Philadelphia's permission request** (`docs/gated_access.md` item 12),
  waiting on a reply. **Silence is not consent**, and must never harden into
  a claim that permission was given. `docs/plan_detail/data_and_disclosure.md`, "Philadelphia's permission
  request".
- **If the repo ever goes private:** `docs/plan_detail/process_and_tooling.md`, "If the repo ever goes
  private".

## Data quality follow-ups

- [ ] **Three code problems from the comment pass (owner, 2026-10-01: do
  later).** `docs/plan_detail/process_and_tooling.md`, "Three code problems from the comment pass".
- [ ] **From the prose pass's deploy check (2026-10-02), not blocking.**
  `docs/plan_detail/data_and_disclosure.md`, "From the prose pass's deploy check".
- [ ] **License gaps from staging's ranking.** `docs/plan_detail/data_and_disclosure.md`, "License gaps".
- [ ] **`scaffold_city.py` has only the GTFS map template.** `docs/plan_detail/process_and_tooling.md`,
  "scaffold_city.py's map template".
- [ ] ⏸ **After the prose and UI pass lands (owner, 2026-10-01).** `docs/plan_detail/process_and_tooling.md`,
  "After the prose and UI pass lands".
- [ ] ⏰ **Zurich: rebuild after 2026-12-12** (owner, 2026-09-30, call C1).
  `docs/plan_detail/city_watch.md`, "Zurich".
- [ ] **For the site-wide prose and UI pass (owner, 2026-09-30, calls A3,
  A6, A7, B6).** `docs/plan_detail/labels_and_macro_map.md`, "For the site-wide prose and UI pass".
- [ ] **What Is Excluded's opening claims no longer hold** (review lane 4,
  2026-09-30). `docs/plan_detail/data_and_disclosure.md`, "What Is Excluded's opening claims".
- [ ] ⏰ **Philadelphia: 11th St back on 2027-08-30** (SEPTA). `docs/plan_detail/city_watch.md`,
  "Philadelphia: 11th St".
- [ ] ⏰ **Yamagata: rebuild on the September 2026 food list** (owner, 2026-10-11; the city
  replaces its file monthly). `docs/plan_detail/city_watch.md`, "Yamagata: the September food list".
- [ ] **Sacramento's Green Line: check from 2026-10-15** (due back by
  mid-October 2026). `docs/plan_detail/city_watch.md`, "Sacramento's Green Line".


## Later / maybe

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] **An English-language switch for station names**, for cities whose
  operator publishes English names (owner, 2026-10-12, in the Naha build's
  chat, relayed: "potential future implementation ... let cleanup know").
  Recorded, NOT built: the feature freeze of 2026-10-08 stands. A map
  control would swap the site's romanised style (Naha-kuko, Itami's
  Osaka-kuko) for the operator's own English (Naha Airport). Half the data
  exists: each config's `OSM_NAME_EN_OVERRIDES` cites the OSM spelling it
  replaces. The romanised precedent stands site-wide with no exception:
  Naha's airport station is Naha-kuko (owner, in that chat, relayed:
  "naha-kuko okay"). He places the idea with the Travel view or the
  transit-globe app, not the site's maps ("i will worry about the
  english wording more for the transit-globe or maybe the partial
  travel version"): name it in transit-globe's search handoff.
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
