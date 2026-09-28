# Project conventions

Multi-city map of commercial density around rapid-transit stations. Read
`docs/project_context.md` first - it is the stable briefing (what's settled,
architecture, current state, lessons). `PLAN.md` is the open work,
`DECISIONS.md` the append-only reasoning trail, `docs/city_master_list.md`
the city list. **How each rule below was learned is in
`docs/rule_history.md`, at the anchor in brackets** - read it before relaxing
a rule, not before obeying one.

## Where to start

- Picking the next city -> `docs/city_master_list.md` (read counts there, never
  repeat them here; `check_master_list_counts.py` enforces them, and closed
  bands live in `city_master_list_evidence.md`); its evidence trail,
  `docs/global_country_shortlist.md`, wins when they disagree. [#master-list]
- First city in a new country -> `add-country`, then
  `docs/mexico_retrospective.md` (one national register) or
  `docs/spain_retrospective.md` (bespoke per city; also read it before trusting
  a country that looks familiar). Worked example:
  `docs/canada_retrospective.md`. [#add-country]
- Adding a city -> `add-city`, then `scaffold-city` once Step 0 passes. Check
  `docs/build_briefs/<city>.md` first: a cache, never a prerequisite. [#add-city]
- A brief exists -> **run `python scripts/brief_check.py <city>` before writing
  any code.** A failing check is a brief to correct, never a check to relax. If
  a brief has no checks block, add one for the claims you rely on. [#brief-check]
- One registry does not cover all three buckets -> `multi-source-city` (the
  usual case in large US cities). [#multi-source]
- Classification is not NAICS -> `premises-taxonomy`. Measure the catch-all
  share at each level with `brief_check.py`'s `taxonomy_catchall` kind first;
  there is no default level. [#premises-taxonomy]
- Addresses but no coordinates -> `address-join`, **before writing any
  geocoder.** [#address-join]
- Chinese, Japanese or Korean text -> `cjk-text`. [#cjk-text]
- Re-probing a thin city (open-gap row, one-bucket Band C) -> `reprobe-city`. [#reprobe-city]
- Brazilian city -> `brazil-city`; Taiwanese city -> `taiwan-city`; Japanese
  city -> `japan-city`. [#country-skills]
- Rail from OpenStreetMap, not GTFS -> `osm-rail`. Put a lesson where the next
  city must pass through it - a raising check in shared code, then a skill - not
  in a sibling city's comments. [#osm-rail]
- Map opens at the wrong zoom -> `map-view`; verify with
  `scripts/check_map_view.js`, never a screenshot, live as well as locally. [#map-view]
- More than one session at once -> `docs/session_roles.md`. [#session-roles]
- Auditing rather than building -> `consistency-sweep`; prefer a check to a
  correction. [#consistency-sweep]

## Invariants

- **Live-verify a city's real data schema before writing any pipeline code
  for it.** Titles and search summaries are not evidence. See `add-city` Step 0. [#live-verify]
- **Never buffer or measure distance in EPSG:4326.** Project to the city's
  own UTM zone (metres), do the geometry, project back for display. The
  projected CRS is per-city, never copied.
- **Keep `requirements.txt` lean** (streamlit, pandas). Streamlit Cloud
  installs from it - geopandas/folium there breaks the deploy. Pipeline
  dependencies live in `requirements-pipeline.txt`.
- **`outputs/<city>/` is committed; `data/<city>/raw/` and `processed/` are
  not.** The deployed app only reads `outputs/`, never runs the pipeline.
- **Maps are pre-rendered static HTML** embedded with
  `st.iframe()`, not `streamlit-folium`.
- **Map rendering is shared:** city `step3_map.py` files stay thin and never
  fork `pipeline/map_common.py`'s `render_heatmap()`, which never names a
  taxonomy - grouping, tooltip label and legend text come from the taxonomy
  module. [#wording]
- **Every drawn transit line gets a permanent on-map label (its real public
  name) AND a legend entry** - not one or the other.
- **A city's classification need not be NAICS** (`pipeline/taxonomies/`).
  Step 2 filters via `filter_to_storefront()`, never NAICS prefixes. [#wording]
- **Check the rail system's shape before assuming "keep every station."**
  Central-corridor-plus-surface-offshoot systems need
  `docs/sub_transit_line_filters.md`. [#rail-shape]
- **The project is never named after a city.** A city name labels only that
  city's own page.
- **Publish public commercial information, not personal information** - a
  trade name, never a registrant's own name at what looks like their home,
  even from a public registry. Run `python scripts/check_personal_exposure.py
  <city>` before publishing a city and after any change to its step 2 or
  taxonomy; record the verdict in `DECISIONS.md`. Suspect catch-all codes
  first. [#personal-info]
- **Never remove the basemap attribution:** `© OpenStreetMap contributors`,
  linked to the OSM copyright page, visible on the render (ODbL 1.0); a new
  tile provider swaps in its own. Check K of `check_provenance.py` refuses an
  unclamped legend; run `scripts/check_map_attribution.js` at more than one
  viewport height. The credit also stays clear only because `app/pages/*.py`
  embeds each map at the map's own height - change that height and re-run the
  check. Other required notices: `docs/data_sources.md`, "Notices
  this project MUST display when published" - obligations, not courtesies. [#attribution]
- **A pipeline step never fetches.** Downloads live in
  `pipeline/<city>/fetch_sources.py` - deliberately not named `step*.py`, so
  `drift_check.py` never runs it; a step
  reads the cache and exits non-zero naming that script.
  `scripts/check_no_fetch_in_steps.py` decides it, **including through shared
  `pipeline/*.py` modules.** [#no-fetch]
- **A step may fetch when a person runs it; a drift check may never fetch.**
  A step that cannot stop fetching guards it with `pipeline/offline.py`'s
  `refuse_if_offline()`, not a wider exception list. `HEATMAP_NO_NETWORK=1`
  tests a fresh checkout. [#offline-guard]
- **Run `python scripts/check_provenance.py` after adding a city, and make it
  name that city OK** - an unrecorded city looks exactly like a checked one.
  A city under `KNOWN_GAPS` is a dated defect, not a pass. [#provenance]
- **A city is scoped TWICE, and both halves have to reach the reader** - its
  rail network and its excluded businesses, in `docs/excluded_categories.md`.
  `python scripts/check_scope_disclosure.py` decides this. [#scope-twice]
- **A source that is not a registry, a feed or a boundary still needs a row**
  in `docs/data_sources.md` (a naming layer, a parcel layer, a geocoder), with
  its own licence and any notice it requires. [#support-sources]
- **Record a new data source's licence when you add it**, in
  `docs/data_sources.md` (per-country sections live in
  `docs/data_sources/<country>.md`), using the **`read-licence` skill**. A government
  portal is a reason to expect permissive terms, not evidence; check what a
  dataset page incorporates by reference. [#licence]
- **A removal request is honoured, not argued** - from a publisher, a business
  owner, or anyone with a privacy concern about a pin. Take it down first (the
  layer or the whole city), then record what and who asked in `DECISIONS.md`.
  Never ask for justification or weigh it against what the licence permits.
  Keep `docs/data_sources.md` and `docs/excluded_categories.md` consistent on
  it. [#removal]
- **Ridership and deep analysis are out of scope** until asked (see
  `docs/project_context.md`). Flag scope additions rather than building
  them.

## Working rules

- **Commit after each green step.** The commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md`** as it's made (`decisions-entry`
  skill). Never edit an old entry; add a new one, then run
  `python scripts/decisions_index.py` (`--check` fails if stale). Entries older
  than the current week (Sunday to Saturday) live in `docs/decisions/<Sunday>.md`,
  moved verbatim by `scripts/archive_decisions.py` at the start of each week.
  Keep `docs/project_context.md` to current state, no counts. [#decisions]
- **Run `python pipeline/drift_check.py` after any pipeline change** - then
  **`git checkout -- outputs/` if it leaves files modified but reported no
  drift** (CRLF and Folium's random ids). Never `git add -A`. [#drift-churn]
- **Run `python scripts/check_deploy_imports.py` before any push that touches
  `app/`**, and **reboot the deployed app after any push that changes a module
  it imports** (`app/cities.py` changes with every city): "Updated app!" keeps
  imported modules cached (gate item 9, `docs/data_sources.md`).
  `deploy-verify` catches neither. [#deploy-reboot]
- **Publishing a city? Use `publish-city`.** Landing `app/` on master IS
  deploying; compute the reboot question from the WHOLE push's `app/` diff. [#publish-city]
- **Reading a source's terms? The `licence-read` agent** - one source per call,
  out of the main conversation. [#licence-read]
- **Verify app changes with the `deploy-verify` agent - once per batch, at
  review time** (`docs/review_time.md`); during the day a session checks its
  own `app/` change with at most one quick browser render. **Always state a
  scope**: `city-added`, `map-chrome`, `app-deps` or `full` (`full` for a large
  batch). Approvals, `app/` landings and full re-renders also wait for review
  time, which only the owner calls. Skip it for pipeline-only work and doc
  edits: `drift_check.py`, a grep of `app/` for folium/geopandas/shapely/pyproj
  imports, and one browser render cover those. [#deploy-verify]
- **Write probe and scratch output to the session scratchpad directory, never
  to the working directory or the home directory** - an explicit path, or a
  gitignored `data/<city>/raw/`. Never commit it; findings go in
  `docs/data_sources.md` and `docs/city_master_list.md`. [#scratch]
- Draft interpretive prose in chat before writing it to a file.
- **A backslash or a backtick never goes into a Bash command. Write the
  content to a file with the Write tool and run the file.** Escapes, not
  length, are the test; quoting the heredoc delimiter does not help.
  `.claude/hooks/block_heredoc.py` enforces it. [#no-escapes]
- **Re-check `origin/master` in the same breath as the push**: `git fetch`,
  merge if behind, push, nothing slow in between; re-fetch if a gate re-runs
  after that merge. [#fetch-before-push]
- **Resolve a conflicted append-only file with
  `python scripts/merge_append_only.py DECISIONS.md`, never by rebuilding it
  from one side** - a conflict region is not everything the other side added.
  Run `scripts/decisions_index.py` afterwards. [#merge-append-only]

## Commands

```bash
python pipeline/<city_slug>/step1_stations.py
python pipeline/<city_slug>/step2_clean_businesses.py
python pipeline/<city_slug>/step3_map.py
python pipeline/drift_check.py [city_slug] [--jobs N]   # --jobs 4 does every city
python scripts/brief_check.py [city_slug]               # re-run a brief's claims live
python scripts/check_all.py [--list]                    # every pass/fail check, ~30s; the pre-push hook runs it
git config core.hooksPath .githooks                     # once per clone: turns that hook on
python scripts/check_provenance.py [--strict]           # after adding a city
python scripts/check_no_fetch_in_steps.py [--list]
python scripts/check_no_fetch_in_steps_selftest.py      # touches nothing
python scripts/check_scope_disclosure.py
python scripts/check_scope_disclosure_selftest.py       # touches nothing
python scripts/check_inconsistency_list.py              # when a city lands
python scripts/check_stray_downloads.py                 # untracked files at any checkout's root
python scripts/check_overpass_hosts.py [--live|--selftest]   # every Overpass mirror is global
python scripts/check_worktree_data.py <worktree> [--list]   # before removing a worktree
python scripts/check_render_current.py                  # after merging
python scripts/check_map_markup.py [--verbose]          # dark-mode label contrast, legend styles
python scripts/check_inline_arrays.py [--report|--selftest]   # no JS array an iPhone cannot compile; after any re-render
python scripts/check_city_registry.py                   # after merging
python scripts/check_plan_done.py [--verbose]           # REPORTS only
python scripts/check_stale_claims.py                    # REPORTS only
python scripts/check_stale_claims.py --only E           # "only city" claims; when a city lands
python scripts/check_discard_evidence.py [--selftest]   # when the discard table changes
python scripts/measure_rail_backbone.py --osm <json> --relation <id> --municipios <json> --codes <ibge> --stations <csv> --crs <epsg>   # commuter-line rail test
python scripts/check_deploy_imports.py [--ref REF]      # before ANY push touching app/
node scripts/profile_zoom.mjs <baseUrl> <city,city> [reps]   # zoom lag
node scripts/check_macro_attribution.mjs [baseUrl] [375,768,1200]   # front page OSM credit; live: <app>/~/+
python scripts/decisions_index.py [--check]
python scripts/archive_decisions.py [--dry-run]          # start of each week: older entries -> docs/decisions/
python scripts/merge_append_only.py DECISIONS.md [--dry-run]   # archived entries count as present
python scripts/scaffold_city.py --slug <slug> --name <Name> --system-name <system> --taxonomy <key> --lat <lat> --lon <lon> --region <region> --country <country>   # add --dry-run first
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview.py"
```

Environments: the full pipeline environment (`requirements-pipeline.txt`)
for `pipeline/`; `.venv-lean` (`requirements.txt` only, gitignored) for the
app. Build the lean one with `python -m venv .venv-lean` then
`.venv-lean/Scripts/python.exe -m pip install -r requirements.txt`.
