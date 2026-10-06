# Project conventions

Multi-city map of commercial density around rapid-transit stations. Read
`docs/project_context.md` first - it is the stable briefing (what's settled,
architecture, current state, lessons). `PLAN.md` is the open work,
`DECISIONS.md` the append-only reasoning trail, `docs/city_master_list.md`
the city list. **How each rule below was learned is in
`docs/rule_history.md`, at the anchor in brackets** - read it before relaxing
a rule, not before obeying one.

## Where to start

- Picking the next city -> `docs/city_master_list.md` (read counts there,
  never repeat them); `docs/global_country_shortlist.md` wins when they
  disagree. [#master-list]
- First city in a new country -> `add-country`, then the Mexico (one
  national register) or Spain (bespoke per city) retrospective in `docs/`.
  [#add-country]
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
- Writing a city's page, or its sections of What Is Excluded and About the
  Data -> `docs/city_page_format.md`: the page order, bullets, sections that
  name the city, process notes kept off rendered docs, American spelling.
- Keeping or dropping any category, in any city -> `docs/category_rules.md`
  first; recommend the precedent, and bring a departure to the owner with the
  precedent it breaks.
- Addresses but no coordinates -> `address-join`, **before writing any
  geocoder.** [#address-join]
- Chinese, Japanese or Korean text -> `cjk-text`. [#cjk-text]
- Re-probing a thin city (open-gap row, one-bucket Band C) -> `reprobe-city`. [#reprobe-city]
- Screening cities -> `screen-wave`, probes by the `city-probe` agent; extending
  a built map -> `regional-extension`.
- Brazilian city -> `brazil-city`; Taiwanese city -> `taiwan-city`; Japanese
  city -> `japan-city`; Korean city -> `korea-city`; French city -> `france-tram-city`; a trams-only
  city outside France and Czechia -> `tram-city`. [#country-skills]
- **Overpass: one query in flight per session, one per city**, never
  parallel; after a 504 or 429 wait at least 60 s before a retry (owner,
  2026-09-30).
- Rail from OpenStreetMap, not GTFS -> `osm-rail`. Put a lesson where the next
  city must pass through it - a raising check in shared code, then a skill - not
  in a sibling city's comments. [#osm-rail]
- Map opens at the wrong zoom -> `map-view`; verify with
  `scripts/check_map_view.js`, never a screenshot, live as well as locally. [#map-view]
- More than one session at once -> `docs/session_roles.md`. [#session-roles]
- Auditing rather than building -> `consistency-sweep`; prefer a check to a
  correction. [#consistency-sweep]
- A review in lanes (several sessions, one pinned commit) ->
  `docs/review_lane_kit.md`. Process or efficiency review ->
  `efficiency-review`.

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
- **Publish public commercial information, not personal information**: a
  trade name, never a registrant's own name at what looks like a home, even
  from a public registry. Run `scripts/check_personal_exposure.py <city>`
  before publishing and after any step-2 or taxonomy change; record the
  verdict in `DECISIONS.md` and `docs/privacy_verdicts.md`. Suspect catch-all
  codes first. Withheld-name lists hold KEYS, never names
  (`pipeline/name_keys.py`), and nothing quotes a registrant's own name.
  [#personal-info]
- **Never remove the basemap attribution** `© OpenStreetMap contributors`,
  linked and visible on the render (ODbL 1.0); a new tile provider swaps in
  its own. Check K of `check_provenance.py` refuses an unclamped legend; run
  `scripts/check_map_attribution.js` at more than one viewport height, and
  again if a page's embed height changes. Other required notices:
  `docs/data_sources.md`, "Notices this project MUST display when
  published". [#attribution]
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
- **A removal request is honoured, not argued**, from a publisher, a
  business owner or anyone with a privacy concern: take it down first (the
  layer or the city), then record it in `DECISIONS.md`, keeping
  `docs/data_sources.md` and `docs/excluded_categories.md` consistent. Never
  ask for justification. [#removal]
- **Ridership is out of scope, a hard line**: no ridership figures,
  correlations or foot-traffic stand-ins, since the data cannot be had for
  every city; it changes only for a publishable subset with the owner's
  approval (2026-10-02). Flag scope additions rather than building them.
- **AI-driven deep analysis is permitted; every analysis carries an
  AI-driven acknowledgement (hard line).** Analyses are private to the owner:
  never on the site (`app/`, `outputs/`) or in public material unless the
  owner says so for a piece (2026-10-02).

## Working rules

- **Commit after each green step.** The commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call** as it's made (`decisions-entry` skill): **a
  build session in `docs/decisions_drafts/<branch>.md`, never in
  `DECISIONS.md`**; Cleanup folds the drafts when the owner hands them off.
  Never edit an old entry; add one and run `scripts/decisions_index.py`.
  Older weeks move to `docs/decisions/<Sunday>.md` by
  `scripts/archive_decisions.py` each Sunday. `docs/project_context.md` holds
  current state, no counts. [#decisions]
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
- **Verify app changes with the `deploy-verify` agent once per batch, at
  review time** (`docs/review_time.md`), always with a scope (`city-added`,
  `map-chrome`, `app-deps`, `full`); during the day, at most one quick browser
  render of a session's own change. Approvals, `app/` landings and full
  re-renders wait for review time, which only the owner calls. Pipeline-only
  and doc work needs no deploy-verify. [#deploy-verify]
- **Write probe and scratch output to the session scratchpad directory, never
  to the working directory or the home directory** - an explicit path, or a
  gitignored `data/<city>/raw/`. Never commit it; findings go in
  `docs/data_sources.md` and `docs/city_master_list.md`. [#scratch]
- **What a build's brief and skill cover is pre-permitted** (owner,
  2026-09-30): fetching the sources they name from the publisher's own host,
  with their licence rows and notices, and page text from an approved
  template. A source not in the brief goes to the owner first; a sentence no
  template covers is a proposal in the drafts file, flagged at review time;
  other interpretive prose is drafted in chat first.
- **A backslash or a backtick never goes into a Bash command. Write the
  content to a file with the Write tool and run the file.** Escapes, not
  length, are the test; quoting the heredoc delimiter does not help.
  `.claude/hooks/block_heredoc.py` enforces it. [#no-escapes]
- **Once per review time, Cleanup tells Visuals and Analytics what moved**
  (`scripts/downstream_changes.py`; `docs/session_roles.md`). At most three
  build sessions at once; a branch takes master in only before its own push
  (owner, 2026-10-04).
- **Re-check `origin/master` in the same breath as the push**: `git fetch`,
  merge if behind, push, nothing slow in between; re-fetch if a gate re-runs
  after that merge. [#fetch-before-push]
- **Python is capped at 8 GB a process, 12 GB with its children**
  (`scripts/python_memcap.py`). **At most four heavy jobs, each admitted by
  the gate: `python scripts/heavy_job.py run --label <job> --session <you> --
  <command>`**; a refused job waits (`--wait <min>`), and `heavy_job.py status`
  names what holds the memory. Declare the label's measured peak (the
  default), else an estimate scaled from measured ones (`--peak-gb N
  --estimate "..."`); the rest is in `docs/session_roles.md`. Drift checks
  `--jobs 2` at most, one per machine. A `MemoryError` is a script to fix,
  never a cap to raise. PDFs: `pdftotext` or `pypdf`, never a hand-written
  decoder. [#memory]
- **Resolve a conflicted append-only file with
  `python scripts/merge_append_only.py DECISIONS.md`, never by rebuilding it
  from one side** - a conflict region is not everything the other side added.
  Run `scripts/decisions_index.py` afterwards. [#merge-append-only]

## Code comments

Neutral voice: no "I", "we" or "you"; short statements of what and why,
readable by an outsider but useful to whoever changes the code next. Keep
every measured value, every "re-measure if X changes" warning and every
pointer to `DECISIONS.md`, `docs/rule_history.md` or a skill. How something
was found or verified gets one line at most; the full story belongs in the
decisions log. Never touch dated log text, verbatim licence quotes or any
string that renders. `scripts/check_provenance.py` is the reference example.

**No em dashes in any comment or docstring**, including CSS/JS comments
inside strings (`pipeline/map_common.py`'s ship in every committed map, so
rewording one means re-rendering). Enforced by
`python scripts/check_no_em_dashes.py`. Visible text is exempt.

## Commands

Every script's usage line is in `docs/commands.md`; the ones every session
needs: `python scripts/check_all.py` (the pre-push hook; enable once per clone
with `git config core.hooksPath .githooks`), `python pipeline/drift_check.py
[city] [--jobs N]`, `python scripts/regen_generated.py` after any merge, and
`.venv-lean/Scripts/python.exe -m streamlit run "app/Overview.py"`.

Environments: the full pipeline environment (`requirements-pipeline.txt`)
for `pipeline/`; `.venv-lean` (`requirements.txt` only, gitignored) for the
app. Build the lean one with `python -m venv .venv-lean` then
`.venv-lean/Scripts/python.exe -m pip install -r requirements.txt`.
