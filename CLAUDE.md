# Project conventions

Multi-city map of commercial density around rail-transit stations. Read
`docs/project_context.md` first - it is the stable briefing (what's settled,
architecture, current state, lessons). `PLAN.md` is the open work,
`DECISIONS.md` the append-only reasoning trail, `docs/city_shortlist.md`
the city research.

**Picking the next city? `docs/city_master_list.md`** is the current global
list - candidates banded by what is actually stopping each one, plus the built
cities and the discards with their evidence. It is current state, rewritten as
things change, so **read the counts off that file rather than from here** -
this pointer has gone stale twice by repeating them. `docs/global_country_shortlist.md` is the **evidence trail**
behind it (87 countries, every probe logged); when the two disagree the trail
wins and the list is stale.

**Adding a city in a country this project has never built in? Start with
`add-country`** (`.claude/skills/add-country/`) - the national facts that
disqualify every city at once, profiled once instead of per city. Canada is the
worked example; `docs/canada_retrospective.md` is what it cost.

**Adding a city? Use the `add-city` skill** (`.claude/skills/add-city/`) -
the process the built cities actually followed - and the `scaffold-city` skill
(`scripts/scaffold_city.py`) to generate its config, map script, page and
`cities.py` entry once Step 0 passes. **If one registry does not cover all
three buckets, use `multi-source-city`** - most large US cities do not license
general retail, so this is the common case rather than the exception (New York
needed four sources; Philadelphia's is 79% landlord registrations).

**Check `docs/build_briefs/<city>.md` first** - if one exists, Step 0's answers
are already banked there (endpoints, columns, CRS, traps, required notices, and
an explicit list of what is still unknown). It is a cache, not a prerequisite:
no brief means `add-city` Step 0 as usual, never waiting for one.

**Is the city's rail coming from OpenStreetMap rather than GTFS? Use
`osm-rail`** (`.claude/skills/osm-rail/`). Mexico City and Guadalajara both
needed it - one because every agency host is unreachable, one because the only
feed expired in 2023 and predates a line that now carries passengers - and most
of the remaining shortlist (Taipei, São Paulo, Israel) is not GTFS either. It
also carries the meta-rule that skill exists for: **a lesson written in the
previous city's config does not reach the next city.** Mexico City's config
warns in capitals never to match stations on a network label; Guadalajara's
first query did exactly that and lost a whole line. Put a lesson where the next
city must pass through it - a raising check in shared code, then a skill - not
in a sibling city's comments.

**Then run `python scripts/brief_check.py <city>` before writing any code for
it.** A brief caches Step 0's mistakes as confidently as its findings: Edmonton
inherited three wrong claims from its own, each an HTTP call from being caught,
and the MEASURED/ASSERTED labels did not prevent it - by the time a brief
*recommends* something, the label has been reasoned away. The checks live in a
fenced ```brief-checks block beside the prose, so writing a claim and writing
its test are one act. A failing check is a brief to correct, never a check to
relax. If a brief has no checks block, add one for the claims you rely on.

**More than one session working at once? Read `docs/session_roles.md`** - which
paths each role owns, and the worktree-per-session split that keeps them from
colliding. A single session does all of it and can ignore that file.

**Auditing rather than building? Use `consistency-sweep`**
(`.claude/skills/consistency-sweep/`) - the cleanup role. It sweeps for what
the forward-facing sessions leave behind: prose still written in the future
tense about a present that arrived, hand-kept counts that drifted, references
broken by renumbering, sources in use whose terms were never read, tables that
stopped rendering, branches and worktrees outliving their work. **Its preferred
output is a check rather than a correction**, which is why it owns
`scripts/check_*.py` - `check_provenance.py` was written to close one gap a
reader had already found and immediately found five more.

## Invariants

- **Live-verify a city's real data schema before writing any pipeline code
  for it.** Dataset titles and search summaries are not evidence (Denver and
  San Jose both looked viable and had no usable data). See `add-city` Step 0.
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
- **Map rendering is shared:** `pipeline/map_common.py`'s
  `render_heatmap()`. City `step3_map.py` files are thin and must not fork
  it. It never names a taxonomy - category grouping, tooltip label and
  legend text come from the taxonomy module.
- **Every drawn transit line gets a permanent on-map label (its real public
  name) AND a legend entry** - not one or the other.
- **A city's classification need not be NAICS.** A documented local taxonomy
  is fine: see `pipeline/taxonomies/`. Step 2 filters via
  `filter_to_storefront()`, never NAICS prefixes directly.
- **Check the rail system's shape before assuming "keep every station."**
  Central-corridor-plus-surface-offshoot systems (San Francisco's Muni
  Metro) need `docs/sub_transit_line_filters.md`; uniformly sparse ones (San
  Diego) don't.
- **The project is never named after a city.** A city name labels only that
  city's own page.
- **Publish public commercial information, not personal information.** A trade
  name is fair game; a registrant's own name at what looks like their home is
  not, even from a public registry. Run
  `python scripts/check_personal_exposure.py <city>` before publishing a city
  and after any change to its step 2 or taxonomy, and record the verdict in
  `DECISIONS.md`. Catch-all classification codes are the usual culprit (Los
  Angeles excludes NAICS 812990 for this reason).
- **Never remove the basemap attribution.** Every rendered map carries
  `© OpenStreetMap contributors` linked to the OSM copyright page; ODbL 1.0
  requires it to stay visible, not hidden behind UI or a toggle. Changing tile
  provider swaps that attribution for the new provider's - it never just
  disappears. Three other sources also require specific notices once the site
  is public (Chicago, SFMTA, LA Metro): the exact wording is in
  `docs/data_sources.md`, "Notices this project MUST display when published",
  and those are obligations rather than courtesies.
- **A pipeline step never fetches. Downloading lives in
  `pipeline/<city>/fetch_sources.py`**, deliberately not named `step*.py` so
  `drift_check.py` never runs it; the step reads the cache and exits non-zero
  naming that script when it is missing. A cache-guarded download inside a
  step is offline only on a machine that has already run it, so on a fresh
  checkout a drift check silently asks "does the CURRENT UPSTREAM still
  produce the committed output" instead of "does the COMMITTED CODE" - and
  Toronto proved that is not a pedantic difference, producing a map missing a
  storefront while the row-count baseline reported identical. `python
  scripts/check_no_fetch_in_steps.py` decides this, **including through a
  shared `pipeline/*.py` module**, which is how three `step3_geocode.py` files
  turned out to fetch via `census_geocoder.py` without importing an HTTP
  client themselves.
- **Run `python scripts/check_provenance.py` after adding a city, and make it
  name that city OK.** `docs/data_sources.md` is the only way a build can be
  reproduced, and the rule to record a city's sources there was followed for
  the US cities and silently skipped for every city that arrived through a
  country profile - Canada's for a day, Mexico's until a script looked.
  The gap is invisible by construction: **a city whose provenance is unrecorded
  looks exactly like a city that was checked**, which is why this is a script
  and not another paragraph. It also checks the notices list against
  `app/components.py`'s `_NOTICES`, which had two item 8s and two item 15s.
  A city under `KNOWN_GAPS` in that script is a dated defect, not a pass.
- **A source that is not a registry, a feed or a boundary still needs a row.**
  The naming layer that says which municipality an excluded station is in, the
  parcel or assessor layer a residence filter joins to, a geocoder. These are
  usually published by a county, a province or a state rather than by the city,
  so they carry their own licence and sometimes their own required notice - the
  Province of British Columbia's is notice 17, and it was missed for a day
  because no per-city checklist had a slot for it.
- **Record a new data source's licence when you add it**, in
  `docs/data_sources.md`, using the **`read-licence` skill**. A government
  open-data portal is a reason to expect permissive terms, not evidence of
  them: LA Metro's GTFS forbids modifying its data while LA's business registry
  is CC0, and New York City's datasets declare no licence at all. The skill
  exists because every licence correction in this project came from not opening
  a page an earlier review had merely cited - and the step most easily skipped
  is checking what a dataset page incorporates **by reference**, which is how
  Philadelphia's prohibition hid behind a licence that forbids nothing.
- **A removal request is honoured, not argued** - from a data publisher, a
  business owner, or anyone raising a privacy concern about a specific pin.
  Take it down first (the layer, or the whole city, as the request requires),
  then record what was removed and who asked in `DECISIONS.md`. Do not ask the
  requester to justify themselves, and do not weigh it against the fact that
  the licence review found nothing forbidding what is published: being
  permitted to display something is not a reason to insist on it. The standing
  commitment is published in `docs/data_sources.md` and
  `docs/excluded_categories.md` - keep those two consistent with each other.
- **Ridership and deep analysis are out of scope** until asked (see
  `docs/project_context.md`). Flag scope additions rather than building
  them.

## Working rules

- **Commit after each green step.** The commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md`** as it's made (the
  `decisions-entry` skill has the format). Never edit an old entry; add a
  new one, then run `python scripts/decisions_index.py` to refresh the
  generated index at the top. That file is 100 entries and ~57k words, and
  `drift_check.py` ends by telling you to find "the latest baseline entry" in
  it - the index is how. `--check` fails if it is stale. Keep
  `docs/project_context.md` to current state, no counts.
- **Run `python pipeline/drift_check.py` after any pipeline change** - then
  **`git checkout -- outputs/` if it leaves files modified but reported no
  drift.** On Windows the regenerated files come back CRLF while the committed
  ones are LF (`.gitattributes` sets `* text=auto eol=lf`), and Folium assigns
  fresh random element ids on every render, so `git status` shows changed
  `outputs/` files after a run that said "zero drift". Verified 2026-09-22:
  three CSVs differed **only** in line endings and three `heatmap.html` files
  showed exactly 6,062 insertions against 6,062 deletions. Committing that
  churn would rewrite files the deployed app reads for no change at all - and
  it is a second reason never to `git add -A`.
- **Run `python scripts/check_deploy_imports.py` before any push that touches
  `app/`**, and **reboot the deployed app after any push that changes a module
  it imports** - `app/cities.py` changes with every city. Streamlit Cloud's
  "Updated app!" re-runs the entry script and leaves imported modules cached,
  so the live site stayed down for over three hours on 2026-09-22 across five
  pulls. Gate item 9 in `docs/data_sources.md` has the detail. `deploy-verify`
  cannot catch either failure: it runs the working tree, and it always starts a
  fresh process.
- **Verify app changes with the `deploy-verify` agent**, and **always state a
  scope**: `city-added`, `map-chrome`, `app-deps` or `full`. It runs against
  `.venv-lean` (what Streamlit Cloud installs), not the full environment. A
  full sweep costs ~186k tokens and ~27 minutes, so it is reserved for
  before a real deploy, or for clearing a backlog of unverified changes in one
  batch. Skip it entirely for pipeline-only work (taxonomies, step 2 filters,
  exclusions) and doc edits - `drift_check.py`, a grep of `app/` for
  folium/geopandas/shapely/pyproj imports, and one browser render cover those.
- **Write probe and scratch output to the session scratchpad directory, never
  to the working directory or the home directory.** Step 0 research is mostly
  `curl`/`requests` dumps, and `-o la.json` with no path writes wherever the
  shell happens to be. The 2026-09-18 city screening left eight such files
  (`la.json`, `phila_sample.json`, a saved 404, a 283 KB saved HTML page, a
  file named `.json` that was HTML) sitting in the home directory until
  2026-09-21. Give every probe an explicit path under the scratchpad, or under
  a gitignored `data/<city>/raw/`. Nothing in this category is ever committed:
  the findings belong in `docs/data_sources.md` and `docs/city_shortlist.md`,
  which is where they can be trusted and the raw capture cannot.
- Draft interpretive prose in chat before writing it to a file.
- **Write multi-line text with the Write tool, never a shell heredoc or an
  inline quoted string.** Commit messages, `DECISIONS.md` entries, page prose,
  generated Python. Bash command-substitutes backticks and mangles escapes
  *inside* heredocs too: on 2026-09-22 it broke an f-string in generated code,
  silently emptied every backticked phrase from a commit message, and turned a
  `\n` into a literal newline mid-string - three times in one day, with the fix
  already recorded in `DECISIONS.md` after each one. **That repetition is the
  point of putting it here:** a lesson in the log describes what happened once,
  and a working rule is in hand at the moment of typing. Same reasoning as
  `osm-rail`'s opening section, which exists because a warning in one city's
  config did not reach the next city.
- **Resolve a conflicted append-only file with
  `python scripts/merge_append_only.py DECISIONS.md`, never by rebuilding it
  from one side.** Two sessions both append to the top of `DECISIONS.md`, so
  every master/staging merge conflicts there and the conflict is never a real
  disagreement. The tempting hand fix - take one side's file, re-append the
  other side's new entries - **silently deletes entries**, because *a conflict
  region shows where the two sides disagreed, not everything the other side
  added*. On 2026-09-22 staging's "Japan is a BUILD" entry sat lower in the
  file with no competing change beside it, so git auto-merged it outside the
  markers and rebuilding from master's stage would have dropped it; an hour
  later the France reversal arrived the same way, with the generated index as
  the *only* conflict. The script edits just the conflict regions of git's own
  merged file, dates each entry by the commit that introduced it so the two
  sides interleave by real time, and refuses to write unless the result equals
  the union of both sides' full stages. Run `scripts/decisions_index.py`
  afterwards.

## Commands

```bash
python pipeline/<city_slug>/step1_stations.py
python pipeline/<city_slug>/step2_clean_businesses.py
python pipeline/<city_slug>/step3_map.py
python pipeline/drift_check.py [city_slug] [--jobs N]   # --jobs 4 does all 13 in ~37s
python scripts/brief_check.py [city_slug]               # re-run a brief's claims against live sources
python scripts/check_provenance.py [--strict]           # every built city's sources actually recorded; run after adding a city
python scripts/check_no_fetch_in_steps.py [--list]      # no pipeline step may reach the network
python scripts/check_stale_claims.py                    # REPORTS only: prose that stopped being true (stale tense, drifted counts)
python scripts/check_deploy_imports.py [--ref REF]      # clean clone + lean venv: run before ANY push touching app/
python scripts/decisions_index.py [--check]             # refresh DECISIONS.md's index
python scripts/merge_append_only.py DECISIONS.md [--dry-run]   # resolve an append-only merge conflict
python scripts/scaffold_city.py --slug <slug> --name <Name> --system-name <system> --taxonomy <key> --lat <lat> --lon <lon>   # add --dry-run first
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview.py"
```

Environments: the full pipeline environment (`requirements-pipeline.txt`)
for `pipeline/`; `.venv-lean` (`requirements.txt` only, gitignored) for the
app. Build the lean one with `python -m venv .venv-lean` then
`.venv-lean/Scripts/python.exe -m pip install -r requirements.txt`.
