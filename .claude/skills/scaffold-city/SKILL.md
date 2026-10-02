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
    --region "United States East" --country "United States" --mode light_rail
```

- `--slug` lower snake_case; `--name` the display name (also the switcher name);
  `--system-name` the rail system as riders name it ("CTA 'L'", "Metro Rail").
- `--region` the macro-map view it belongs to (a value in `REGION_ORDER`);
  `--country` groups it in the city switcher, spelled as `app/cities.py`
  already spells that country. Both are required: `cities.py` raises at import
  without them.
- `--mode` (`metro`, `light_rail` or `tram`): the HIGHEST-ORDER mode the
  city's map will draw. It colours the macro dot; trams drawn beside a metro
  leave it `metro`. Required, with no default, and the owner approves it with
  the build (owner, 2026-09-30).
- `--lat/--lon` the macro-map marker; the projected CRS (UTM zone) is derived
  from the longitude and its derivation written into the config.
- `--map-step 4` if you will insert a geocoding step (Los Angeles); default 3.
- `--page-number N` when another session is building at the same time: the
  number from the block `docs/session_roles.md` reserves for this session.
  Without it the page takes one past the highest on this branch, and two
  parallel branches take the same one. A taken number is refused.
- `--dry-run` shows what would be written; existing files are skipped, never
  overwritten (`--force` to override). Re-running for a listed city is safe.

**What it writes:** `pipeline/<slug>/__init__.py`, `config.py`,
`step<N>_map.py`; `data/<slug>/{raw,processed}` and `outputs/<slug>/`;
`app/pages/<n>_<Slug>_Heatmap.py` (`--page-number`, or the next free number); and the `app/cities.py`
entry. Every value only the city's data can supply is a `TODO`.

**The page is born in the city-page format** (`docs/city_page_format.md`,
section 1; owner, 2026-10-01), so never replace it with a copy of an older
page. In order, with nothing between the parts: `render_city_nav` and
`render_city_title("<Name>")` (the name alone over the shared subtitle); the
map, `st.iframe(HEATMAP_HTML, width=1000, height=650)`; the date caption,
`render_data_age("<Name>")`, which a city with a provenance file replaces with
its own caption of the sources' dates and credits (Seoul's); the bullets, in
one `st.markdown` block, as TODO bullets under **The lines** (the lines drawn
by name, what is not drawn and why, the area covered with stations left out
"listed below") and **The businesses** (the source and any category it is
missing); `render_map_help("three business categories (Retail, Food service
and Personal services)")`, whose argument a one- or two-category city changes
to its own name for its layers; `render_excluded_stations`;
`render_country_links`; and `render_site_notices()` last.

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
   look at the map, drift check, and a decisions entry in the session's
   drafts file; `deploy-verify` waits for review time.
3. **Add `data_age` and `placement` to the `cities.py` entry** (add-city Step
   8). The scaffold writes neither, and the page's `render_data_age` raises
   `KeyError` until `data_age` is there.
4. Not generated, still yours (add-city Step 8, `docs/city_page_format.md`):
   - **the page's bullets**: replace each TODO bullet with one plain claim
     true for this city, `app/pages/43_Seoul_Heatmap.py` the model; a third
     bold heading only when the city needs one. Avoid restating counts. No
     repository path, script, check or skill name, and no controls paragraph
     (`render_map_help` covers it). The scaffold's bullets filled in for the
     city need no read-back; a sentence no template covers is a proposal for
     your drafts file;
   - the caption: keep `render_data_age`, or swap in the city's own caption
     of its sources' dates, plus any credit a source prescribes word for word
     (directly under the map, outside any `if`/`try`);
   - the `cities.py` blurb and optional `label` side (only where markers are
     close);
   - the city's sections of `docs/excluded_categories.md` and
     `docs/data_sources/<country>.md` (headings that name the city, its gaps
     in its own section), and the drift baseline.

## Keeping the script honest

The templates in `scripts/scaffold_city.py` mirror a built city's config, map
script and page. If those conventions change (a new config constant every city
needs, a `render_heatmap()` argument, a change to `docs/city_page_format.md`),
change the templates in the same commit. The `PAGE` template IS the page
format for every city outside France (`scripts/france_page.py` writes those),
so the spec and the template change together.
Smoke test without touching the repo: copy `app/cities.py`, `app/pages/` and
`pipeline/taxonomies/` to a scratch directory, run the script with `--root`,
then compile the output and import each generated `config.py`.
