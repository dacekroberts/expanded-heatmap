# Data sources — Germany

<!-- internal -->The Germany part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country. The numbered
notices this project must display, the removal-request commitment and the
deploy gate apply to every country and are kept in that record. Germany's
country profile is a section of Berlin's build brief, in the project's
repository (`docs/build_briefs/berlin.md`): Berlin is the country's only viable
city (Munich, Frankfurt, Cologne and Hamburg were discarded on 2026-09-24 and
2026-09-28).<!-- /internal -->

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Berlin | **IHK Berlin's *Gewerbedaten*** (Industrie- und Handelskammer zu Berlin) — its MEMBERS' business premises as points (WGS84 in the CSV, EPSG:25833 on the WFS), each with WZ 2025 (NACE Rev. 2.1) class `nace_id`, IHK's own finer `ihk_branch_id`, employee band, business age and type. **No name and no street column of any kind.** Crafts (Handwerkskammer members: hairdressers, laundries, many bakers) and liberal professions are not members, so they are all but absent | All three buckets via `pipeline/taxonomies/ihk_wz2025.py` (prefix-matched on `nace_id`); Personal services partial. **60,313 storefronts** built 2026-09-28 from 368,841 rows | `https://media.githubusercontent.com/media/IHKBerlin/IHKBerlin_Gewerbedaten/master/data/IHKBerlin_Gewerbedaten.csv` (126,348,283 bytes, Git LFS, keyless), updated monthly - the register's date is IHK's last commit of the file, read from `https://api.github.com/repos/IHKBerlin/IHKBerlin_Gewerbedaten/commits?path=data/IHKBerlin_Gewerbedaten.csv&per_page=1` (**2026-09-01** at fetch). The same data as a WFS: `https://gdi.berlin.de/services/wfs/gewerbedaten` (typename `gewerbedaten:gewerbedaten`; 367,575 features the same day, an older cut), not used | None server-side (a CSV); `fetch_sources.py` refuses a header carrying a name-like column. Step 2: structural exclusions 3,554 (479, 5612, 562, 564, 964, 9691); catch-alls `nace_id` 969* (10,210) and `ihk_branch_id` 47122 EXACT (12,194) - owner's calls; 1 point outside the Land. `employees_range`, `business_age`, `business_type` read to measure, never written out. License: CSV/CKAN **CC0 1.0**, WFS **dl-de/zero-2.0** - **PERMITTED, nothing to display**; courtesy credit on the page (see notice 57) | 2026-09-28 |

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Berlin | **VBB (Verkehrsverbund Berlin-Brandenburg)** — U-Bahn (`route_type 400`, agency 796 BVG, U1-U9) and S-Bahn (`109`, agency 1 S-Bahn Berlin GmbH, 16 lines), matched on route type, agency and short name, never `route_id` | `https://www.vbb.de/gtfs` (307 from `https://www.vbb.de/vbbgtfs`; 78,379,003 bytes), keyless | 2026-09-28 | **No `feed_info.txt`**; `calendar.txt` runs 2026-09-24 to 2026-12-12, recorded in `outputs/berlin/provenance.json` for the page. Each line's shape is chosen by rule in step 1 (VBB reissues `shape_id`s). Construction diversions in the window are set aside by a 10% served-share rule. Gate 3: U-Bahn 170 = BVG's 175 less the U6's five Tegel stations, closed for works until about August 2027 (owner: drawn as the timetable runs); S-Bahn 168 = S-Bahn Berlin's 168. Trams (`900`) are in the feed and not drawn (owner). Colors: `route_color`, moved by `scripts/line_colour_search.py`. OSM's route relations (VBB network) are the cross-check (brief check `berlin-osm-rail-refs`). License **CC BY 4.0** per VBB's dataset page, credit "VBB Verkehrsverbund Berlin-Brandenburg GmbH", state the changes, VBB's disclaimer, no logos — notice **57** |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Berlin | **ALKIS Berlin, *Landesgrenze*** (SenStadt, Geoportal Berlin) | `https://gdi.berlin.de/services/wfs/alkis_land?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=alkis_land:landesgrenze&OUTPUTFORMAT=application/json&SRSNAME=EPSG:4326` (one MultiPolygon, keyless) | **The Land of Berlin - 890.7 km²** in UTM 33N (OSM relation 62422 is the cross-check). It scopes both businesses (1 point outside) and stations (36 S-Bahn stations in Brandenburg excluded to `outputs/berlin/excluded_stations.csv`). License **dl-de/zero-2.0**, no notice |
