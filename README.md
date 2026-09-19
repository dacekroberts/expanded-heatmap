# Expanded Heatmap

A multi-city map of how commercial activity clusters around rail-transit
stations. For each city it shows retail, food-service and personal-service
businesses by distance from the nearest station (0-0.1, 0.1-0.2, 0.2-0.3 and
0.3-0.6 miles), as heat layers, distance rings and clustered category pins.
Every transit line is drawn from real GTFS geometry, labelled with its public
name, and listed in a collapsible legend.

Mapped so far: San Diego, San Francisco, Los Angeles.

## How it works

The project is split in two so the deployed app stays light.

- **Pipeline (offline):** per-city scripts in `pipeline/<city>/` turn raw
  transit and business-license data into `outputs/<city>/` (a station list,
  an excluded-stations audit file, and a self-contained `heatmap.html`).
  Heavy dependencies (geopandas, folium) live only here.
- **App (deployed):** a Streamlit app in `app/` that reads `outputs/` and
  embeds the pre-rendered maps. It opens on a clickable map of every mapped
  city; each city has its own page. It needs only `streamlit` and `pandas`.

Business categories come from a per-city taxonomy in
`pipeline/taxonomies/`, so a city can use NAICS or its own license
classification. Shared map rendering is in `pipeline/map_common.py`.

## Run it

Pipeline (full environment):

```bash
pip install -r requirements-pipeline.txt
python pipeline/<city_slug>/step1_stations.py
python pipeline/<city_slug>/step2_clean_businesses.py
python pipeline/<city_slug>/step3_map.py
```

Los Angeles has an extra geocoding step (`step3_geocode.py`) and its map
script is `step4_map.py`. Raw data is not committed; each `step1`/`step2`
script says what to download and from where.

App (lean environment; on macOS/Linux use `.venv-lean/bin/python`):

```bash
python -m venv .venv-lean
.venv-lean/Scripts/python.exe -m pip install -r requirements.txt
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview_&_Introduction.py"
```

## Repository guide

| Path | What it holds |
|---|---|
| `docs/project_context.md` | Stable briefing: scope, architecture, lessons |
| `DECISIONS.md` | Append-only log of every judgment call |
| `PLAN.md` | Open work |
| `docs/city_shortlist.md` | Which cities are viable, and why others were ruled out |
| `CLAUDE.md` | Working conventions and invariants |
| `.claude/skills/add-city/` | Step-by-step process for adding a city |

`python pipeline/drift_check.py` re-runs the pipelines and compares the
results to what is committed.

## Scope

Ridership and deeper analysis are out of scope.
