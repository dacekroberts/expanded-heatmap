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

- [ ] **HARD LINE (owner, 2026-10-08): the PLAN cleanup pass, first after
  the 2026-10-11 reset.** It confirms each item written before the large
  review (35d43c4a) live or moves it to `docs/plan_done/`; nobody acts on
  such an item before the pass confirms it. The 2026-10-08 trim moved text
  and marked "probably done" items, but confirmed none.

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
  - **Owner, review time: re-render the 34 built Japanese cities on
    `WAVE5_RULES`**, Toyota first, call 158 with it; plus Japanese
    shared-code fixes, five credits (notices 157, 161, 178, 184, 186) and
    three Kansai-1 briefs. `docs/plan_detail/japan.md`, "Kept from the drafts' notes at the
    2026-10-08 fold".

- [ ] **This week (to the 2026-10-11 reset): refinements, not builds** (owner,
  2026-10-08, weekly near its ceiling; the 10% check-ins ended). Place search,
  possibly the basemap, and the site infrastructure they need. The wave 2
  builds above wait for the reset.

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

- [ ] **Macro-map regions:** the Europe split and Japan's views landed with
  the review (2026-10-07). Still to come: Brăila and Galați, Nagakute and
  Nisshin, Itami and Toyonaka into `KNOWN_STACKED`.

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
  - [ ] **Japanese cities onto N02-25**, one drift check per city. `docs/plan_detail/japan.md`,
    "Japanese cities onto N02-25".
  - [ ] **City-map legend model (2026-09-30):** the obstacle becomes
    max(model, a content-based estimate). `docs/plan_detail/labels_and_macro_map.md`, "City-map legend model".
  - [ ] **Published-city date fixes (2026-09-29):** (a) to (f), three owner
    calls; Philadelphia re-read around 2026-10-13. Review time. `docs/plan_detail/data_and_disclosure.md`,
    "Published-city date fixes".
  - [ ] **Toulouse and Rennes: did step 1's name-level fallback fire?** `docs/plan_detail/city_watch.md`, "Toulouse and Rennes".
  - [ ] **Groundwork before the tram batch:** probably done (the batch is
    on master); confirm and close. `docs/plan_detail/city_watch.md`, "Groundwork before the tram
    batch".
  - [ ] **Macro-map label tiers (owner 2026-09-29):** a Seoul Capital Area
    pilot, review time. `docs/plan_detail/labels_and_macro_map.md`, "Macro-map label tiers".

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

- [ ] **The category fix batch:** landed with review-batch-2; left,
  Stockholm's torghandel stall (still `pending` in
  `scripts/category_continuity_table.py`). `docs/plan_detail/data_and_disclosure.md`, "The category fix batch".
- [ ] **Next cross-city discrepancy audits (owner, 2026-09-29):** six,
  read-only, one at a time. `docs/plan_detail/data_and_disclosure.md`, "Next cross-city discrepancy audits".

## Next cities, in ease order

- [ ] **Second-city screens (Staging, 2026-09-27).** Waves 1 and 2 are done
  and banded (`docs/city_master_list.md`, DECISIONS). Open:
  - [ ] ⏸ **Band T's group decision, DEFERRED by the owner 2026-09-27.** `docs/plan_detail/city_watch.md`, "Band T's group decision".
  - [ ] **Wave-2 follow-ups** (run 2026-09-30): owner calls on Richmond and
    on reads from the owner's own browser; group 2's watch list. `docs/plan_detail/city_watch.md`, "Wave-2 follow-ups".
  - **Watch items from group 1:** `docs/plan_detail/city_watch.md`, "Watch items from group 1".
  - [ ] **Tram rescopes of built cities held by the owner**; Cleanup's
    case-by-case list is in DECISIONS (2026-09-27).

- [ ] Idea (Washington D.C.): make `drift_check.py` say plainly when a
  key-gated city's raw input is missing (`WMATA_API_KEY`, an expiring feed).
- [ ] Idea (Miami, ring coverage 12.6%): scope the all-businesses toggle to
  the station municipalities rather than the whole county.
- [ ] **Fifteen rail cities were screened shallowly; nothing surfacing is NOT
  a disqualification.** `docs/plan_detail/city_watch.md`, "Fifteen rail cities".

### 🇯🇵 Japan — the plan (2026-09-24; evidence in `docs/global_country_shortlist.md`)

JR and private railways INCLUDED (owner, 2026-09-24). Measurement:
`scripts/screen_japan_join.py`. Re-run the census join control
(`scripts/japan_census_control.py`) with each new Japanese city.

- [ ] **Unticked publish steps** (Osaka, Buenos Aires, Sapporo, Fukuoka,
  Kyoto): probably done; confirm and tick. `docs/plan_detail/japan.md`, "Unticked publish steps".
- [ ] **Madrid's 343 px touch:** widen `DENSE_LABEL_SCRIPT`'s trigger and
  re-render Madrid. `docs/plan_detail/labels_and_macro_map.md`, "Madrid's 343 px touch".
- [ ] **Berlin:** U6 to Alt-Tegel about August 2027; refetch before VBB's
  calendar ends 2026-12-12. `docs/plan_detail/city_watch.md`, "Berlin".
- [ ] **London:** refetch before the FSA extracts age. `docs/plan_detail/city_watch.md`, "London".
- [ ] **Buenos Aires:** the inconsistency list's prose; SBASE refetch. `docs/plan_detail/city_watch.md`, "Buenos Aires".
- [ ] **Kyoto:** add the August 2026 list when published. `docs/plan_detail/japan.md`, "Kyoto's
  August 2026 list".
- [ ] **Osaka's Umekita → 福島 stretch:** a re-render for review time. `docs/plan_detail/japan.md`,
  "Osaka's Umekita stretch".

### ▶ Handoff to main — the Band A candidates, 2026-09-24

Each Band A city has a brief whose checks pass live and its licences read;
decisions inside a build are named in its brief.

- [ ] Owner, minor: アイスクリーム類製造業 (692 rows; many gelato counters) is
  OUT for now; the owner's call named 菓子 and そうざい.
- [ ] **Kyoto before publishing:** probably done (`AS_OF` pinned, the city
  published); confirm. `docs/plan_detail/japan.md`, "Kyoto before publishing".
- [ ] **Tokyo: the missing wards** (built 2026-09-28 with 8 of 23). `docs/plan_detail/japan.md`,
  "Tokyo: the missing wards".
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32), not sent and not the next step.
- [ ] ⏸ **Trams left off built maps: PARKED (owner, 2026-09-27); the owner
  decides case by case.** `docs/plan_detail/city_watch.md`, "Trams left off built maps".
- [ ] **Efficiency review follow-ups:** the weekly `archive_decisions.py`
  run; owner: the session count and the remaining findings. `docs/plan_detail/process_and_tooling.md`,
  "Efficiency review follow-ups".

**Not ready for main:** Band C (7) and Band D (7), each waiting on the owner.
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
- [ ] **Deferred from the mega-review (owner, 2026-09-30, call C2).** `docs/plan_detail/data_and_disclosure.md`,
  "Deferred from the mega-review".
- [ ] **For the site-wide prose and UI pass (owner, 2026-09-30, calls A3,
  A6, A7, B6).** `docs/plan_detail/labels_and_macro_map.md`, "For the site-wide prose and UI pass".
- [ ] **What Is Excluded's opening claims no longer hold** (review lane 4,
  2026-09-30). `docs/plan_detail/data_and_disclosure.md`, "What Is Excluded's opening claims".
- [ ] ⏰ **Philadelphia: 11th St back on 2027-08-30** (SEPTA). `docs/plan_detail/city_watch.md`,
  "Philadelphia: 11th St".
- [ ] **Sacramento's Green Line: check from 2026-10-15** (due back by
  mid-October 2026). `docs/plan_detail/city_watch.md`, "Sacramento's Green Line".
- [ ] **Gambling is bucketed inconsistently** (owner, 2026-09-28): one rule
  for every taxonomy. `docs/plan_detail/data_and_disclosure.md`, "Gambling".


## Later / maybe

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
