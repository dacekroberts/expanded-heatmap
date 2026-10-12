# The Travel basemap: packs, the table, and what a new city owes

Internal working notes. Each city map can carry a second base layer,
"Travel", drawn from one PMTiles pack per city that this project builds from
OpenStreetMap. How it was designed and measured is in the decisions log
(entries of 2026-10-07 to 2026-10-11, "basemap"); the licenses are in
`docs/data_sources.md`, "The Travel basemap". This file is the procedure.

## The three parts

| Part | Where | In git |
|---|---|---|
| The style | `pipeline/travel_style.js`, inlined by `pipeline/map_common.py` | yes |
| The table: host, label language, legend routes | `pipeline/travel_packs.py` | yes |
| The packs and the folder a host serves | `data/_basemap_build/host_upload_2026-10/` | no (built files) |

`PACK_HOST` in the table is None until the owner's go-live call, and every
map then renders exactly as it does without the feature. Setting it is one
line plus one re-render of the maps.

## A new city: three things, in this order

A city that lands after the table was written fails
`python scripts/check_travel_packs.py` (part of `check_all.py`) until step 1
is done. The check cannot see a host, so steps 2 and 3 are on this list, not
on a check.

1. **Place the city in `pipeline/travel_packs.py`**, by its `outputs/`
   folder name: under its label language in `LOCAL_LANG` (the code
   `@protomaps/basemaps` uses; the check knows the list), or in
   `ENGLISH_ONLY`. Where a country has more than one language, use the
   city's own. Add a `ROUTES` line only for a named ferry or cable car a
   rider would look for in the legend.
2. **Build its pack.** Tools are in `data/_basemap_build/` (the shared data
   folder, main checkout), under `download_plan_2026-10-08/` and
   `session_tools_2026-10-08/`; each has its usage line at the top.
   - Box: `pack_bounds.py <data dir> <city>` (the stations' extent plus
     10 km, measured in the city's own UTM zone).
   - Extract: the smallest Geofabrik region containing the box
     (`extract_list.py`). 93 regions are held in
     `geofabrik_extracts_2026-10/`; a region not held is a new download,
     which the owner runs (`download.ps1`: one file at a time, MD5-checked,
     its dated address logged for the ODbL 4.6 offer). A box that crosses
     two regions needs `merge_extracts.py` first.
   - Add the city's row to `plan_cities.csv` (city, `False`, extract or
     extracts, box, share covered), then
     `python build_packs.py <city>`: one java run through the memory gate,
     declared at 4 GB, typically 3.5 minutes and up to 10 for the largest
     extracts (measured 2026-10-11), never `--download`.
3. **Refresh the upload folder:** `python make_upload.py`, then copy the new
   `packs/<city>.pmtiles` and `MANIFEST.csv` to the host once one exists.
   While `PACK_HOST` is None nothing reads the folder, so this step can wait
   for go-live; the pack must be on the host before a map rendered with the
   switch on is published.

## After a change

- The style or the builder's trim lists:
  `node scripts/check_travel_style.mjs <basemaps.js> [<TravelTrim.java>]`.
- The table: `python scripts/check_travel_packs.py`.
- The layer code in `pipeline/map_common.py`: the headless check
  `dark_check.mjs` in the session tools (Travel and Business, light and
  dark, the language pill), against a locally served upload folder.

## Open at landing time

The pack tools sit in the gitignored build folder, beside the builder, its
JDK and the extracts. Whether they move into `scripts/` is decided when the
Travel view lands.
