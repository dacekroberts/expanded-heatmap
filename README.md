# Storefronts Near Transit

*(The repository is `expanded-heatmap`; the site is called Storefronts Near
Transit. A standing rule is that this project is never named after a city.)*

**Live site: TODO — paste the Streamlit Cloud URL here once the app is
created.** The subdomain is chosen at app creation and cannot be derived
in advance; this line and the `PLAN.md` entry beside it are the only two
places that need it.

A multi-city map of how commercial activity clusters around rail-transit
stations. For each city it shows retail, food-service and personal-service
businesses by distance from the nearest station (0-0.1, 0.1-0.2, 0.2-0.3 and
0.3-0.6 miles), as heat layers, distance rings and clustered category pins.
Every transit line is drawn from real GTFS geometry, labelled with its public
name, and listed in a collapsible legend.

Mapped so far: San Diego, San Francisco, Los Angeles, Chicago, New York,
Philadelphia, Miami (regional), Boston and Washington D.C. — nine cities.

**Read every map as a snapshot of a public register on its retrieval date**,
redrawn and filtered, not as a census of what is open. Registers lag the
street. Two of the transit licences behind this project specifically forbid
claiming that the data is accurate, complete or timely, and the maps are
described accordingly.

**It is an independent project**, not affiliated with, sponsored by or
endorsed by any transit agency or city government. Line names and route
colours identify each line as its riders know it; no agency logo, wordmark or
route symbol is reproduced.

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

Los Angeles and Washington D.C. each have an extra geocoding step
(`step3_geocode.py`), so their map script is `step4_map.py`. Washington D.C.
also needs a free WMATA API key in `WMATA_API_KEY` before
`pipeline/washington_dc/fetch_sources.py` will run, and its transit feed is
only valid for ten days at a time. Raw data is not committed; each `step1`/`step2`
script says what to download and from where.

App (lean environment; on macOS/Linux use `.venv-lean/bin/python`):

```bash
python -m venv .venv-lean
.venv-lean/Scripts/python.exe -m pip install -r requirements.txt
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview.py"
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

## Licence

**The code is MIT.** See `LICENSE`.

**The data is not, and could not be.** `outputs/<city>/` is committed so the
deployed app can read it without running the pipeline, and each `heatmap.html`
embeds material derived from sources this project does not own: transit line
geometry redrawn from agency GTFS feeds, and business names and coordinates
from municipal and state licence registers. Their terms range from
public-domain dedications to a feed that forbids modifying its data and one
that prohibits redistributing it to third parties; two say nothing about reuse
at all, and at least two are revocable without notice.

So the MIT grant covers this project's own work only. Every source, its
endpoint, its retrieval date and its terms are in `docs/data_sources.md`, and
what was filtered out of each city is in `docs/excluded_categories.md`. Take
the code freely; for the data, go to the source.

**Removal requests are honoured, not argued** — from a data publisher, a
business owner, or anyone raising a privacy concern about a specific listing.
No reason is required and no case will be argued first. The full commitment is
in `docs/data_sources.md`.

**Not affiliated** with any transit agency or city government. Line names and
route colours identify each line as its riders know it; no agency logo,
wordmark or route symbol is reproduced.
