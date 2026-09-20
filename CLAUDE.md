# Project conventions

Multi-city map of commercial density around rail-transit stations. Read
`docs/project_context.md` first - it is the stable briefing (what's settled,
architecture, current state, lessons). `PLAN.md` is the open work,
`DECISIONS.md` the append-only reasoning trail, `docs/city_shortlist.md`
the city research.

**Adding a city? Use the `add-city` skill** (`.claude/skills/add-city/`) -
the process the built cities actually followed - and the `scaffold-city` skill
(`scripts/scaffold_city.py`) to generate its config, map script, page and
`cities.py` entry once Step 0 passes.

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
  `st.components.v1.html()`, not `streamlit-folium`.
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
- **Ridership and deep analysis are out of scope** until asked (see
  `docs/project_context.md`). Flag scope additions rather than building
  them.

## Working rules

- **Commit after each green step.** The commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md`** as it's made (the
  `decisions-entry` skill has the format). Never edit an old entry; add a
  new one. Keep `docs/project_context.md` to current state, no counts.
- **Run `python pipeline/drift_check.py` after any pipeline change.**
- **Verify app changes with the `deploy-verify` agent** - it runs against
  `.venv-lean` (what Streamlit Cloud installs), not the full environment.
- Draft interpretive prose in chat before writing it to a file.

## Commands

```bash
python pipeline/<city_slug>/step1_stations.py
python pipeline/<city_slug>/step2_clean_businesses.py
python pipeline/<city_slug>/step3_map.py
python pipeline/drift_check.py [city_slug]
python scripts/scaffold_city.py --slug <slug> --name <Name> --system-name <system> --taxonomy <key> --lat <lat> --lon <lon>   # add --dry-run first
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview_&_Introduction.py"
```

Environments: the full pipeline environment (`requirements-pipeline.txt`)
for `pipeline/`; `.venv-lean` (`requirements.txt` only, gitignored) for the
app. Build the lean one with `python -m venv .venv-lean` then
`.venv-lean/Scripts/python.exe -m pip install -r requirements.txt`.
