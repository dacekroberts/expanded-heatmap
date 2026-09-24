---
name: scaffold-city
description: Generate the shared skeleton of a new city for expanded-heatmap (pipeline config, map script, app page, cities.py entry, and a skeleton taxonomy module if the city needs its own) with scripts/scaffold_city.py, and say which built city to copy for the steps it does not generate. Use right after add-city's Step 0 passes, when starting to build a city - not for edits to a built one.
---

# Scaffolding a new city

`scripts/scaffold_city.py` writes the parts that are identical in every built
city, so per-city work starts where cities actually differ. Run it after
`add-city` Step 0 (the data, GTFS and boundary are confirmed live), in place of
creating the folders, config, map script and page by hand (Steps 2, 3, 6 and 8's
files).

## Run it

```bash
python scripts/scaffold_city.py --slug dallas --name Dallas --system-name DART \
    --taxonomy naics --lat 32.7767 --lon -96.7970 \
    --region "United States East" --country "United States"
```

- `--slug` lower snake_case; `--name` the display name (also the switcher name);
  `--system-name` the rail system as riders name it ("CTA 'L'", "Metro Rail").
- `--region` the macro-map view it belongs to (a value in `REGION_ORDER`);
  `--country` groups it in the city switcher, spelled as `app/cities.py`
  already spells that country. Both are required: `cities.py` raises at import
  without them.
- `--lat/--lon` the macro-map marker; the projected CRS (UTM zone) is derived
  from the longitude and its derivation written into the config.
- `--map-step 4` if you will insert a geocoding step (Los Angeles); default 3.
- `--dry-run` shows what would be written; existing files are skipped, never
  overwritten (`--force` to override). Re-running for a listed city is safe.

**What it writes:** `pipeline/<slug>/__init__.py`, `config.py`,
`step<N>_map.py`; `data/<slug>/{raw,processed}` and `outputs/<slug>/`;
`app/pages/<n>_<Slug>_Heatmap.py` (next free number); and the `app/cities.py`
entry. Every value only the city's data can supply is a `TODO`.

**The page is named from `--slug`, not `--name`**, so "Lille (Regional)" gets
`24_Lille_Heatmap.py`. The live station table finds each city's `outputs/`
directory by reading it back out of the page filename, so a display name's
brackets, accents or dots in the filename leave that city's row empty.
Guadalajara and Lille both hit this and renamed their pages by hand before the
scaffold was fixed; it now refuses to write a page that does not resolve.

## Custom taxonomies

- **NAICS city:** `--taxonomy naics`. `RAW_CLASSIFICATION_COLUMN` is a `TODO`
  (the raw export's NAICS column; step 2 renames it).
- **A taxonomy already built** (`chicago_license`, ...): pass its name. The
  config takes its `VALUE_COLUMN` as the raw column and, if the module defines
  `EXTRA_COLUMNS`, says to keep those columns through step 2.
- **A new local taxonomy:** `--taxonomy <name> --new-taxonomy --value-column
  <raw column> [--field-label "..."]` writes an empty skeleton module and
  registers it in `TAXONOMY_MODULES`. It maps nothing until you do the real
  work: pull the full distinct values with counts (restricted to the rows step
  2 keeps), map each to a bucket, and hand-sample catch-alls. Chicago is the
  worked example, including what a local taxonomy tends to need:
  - values that say nothing about the business (Limited / Regulated Business
    License) classified by a second field: list it in `EXTRA_COLUMNS`;
  - one storefront holding several licenses: one row per site with a
    priority list (`LICENSE_PRIORITY`), primary license first;
  - a source that is a term history: filter to active licenses and record the
    snapshot date (`AS_OF_DATE`).

## What it does NOT write - copy the nearest built city

`step1_stations.py` and `step2_clean_businesses.py` differ per city and hold
most of the effort. Copy the one closest in shape, then adapt:

| The new city looks like... | Copy |
|---|---|
| Uniformly sparse system, one boundary polygon, pre-geocoded data | San Diego (`step1`, `step2`) |
| A boundary layer of many cities, so excluded stations can be named | Los Angeles `step1` |
| Compact central corridor plus dense surface offshoots | San Francisco `step1` (sub-transit-line filters) |
| Coordinates missing or corrupt | Los Angeles `step2` and `step3_geocode.py` (then `--map-step 4`) |
| Local taxonomy, multi-field classification, several licenses per site | Chicago `step2`; GTFS parent stations: Chicago `step1` |

## Afterwards

1. Fill every `TODO`; `grep -rn TODO pipeline/<slug> app` must come back empty.
   `LINE_SHAPES` is empty on purpose: the map script refuses to run until each
   drawn line has a shape, colour and real public name (label and legend).
2. Continue `add-city` at Step 4 (stations), Step 5 (businesses), then run,
   look at the map, `deploy-verify`, drift check, `DECISIONS.md` entry.
3. Not generated, still yours: the page prose (avoid restating counts), the
   `cities.py` blurb and optional `label` side (only where markers are close),
   docs and the drift baseline.

## Keeping the script honest

The templates in `scripts/scaffold_city.py` mirror a built city's config, map
script and page. If those conventions change (a new config constant every city
needs, a `render_heatmap()` argument), change the templates in the same commit.
Smoke test without touching the repo: copy `app/cities.py`, `app/pages/` and
`pipeline/taxonomies/` to a scratch directory, run the script with `--root`,
then compile the output and import each generated `config.py`.
