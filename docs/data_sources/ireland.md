# Data sources — Ireland

The Ireland part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country on 2026-09-27.
The numbered notices this project must display, the removal-request
commitment and the deploy gate apply to every country and are kept in
that record.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Dublin | Tailte Éireann **rateable valuation register** (the Irish non-domestic valuation list), queried per local authority across the four Dublin councils | All three buckets, via the register's own `Uses` field — a **rateable-property register**, a fourth shape after the licence registers, the national establishment registers and the premises field surveys. **`Category` (13 values) cannot be used**: it puts 1,483 of 2,335 food-service rows and 677 of 744 personal-service rows inside `RETAIL (SHOPS)`, so all three buckets collapse. `Uses` (963 values, 318 distinct segments) is the only level that separates them, and it is keyed by SEGMENT because the field is comma-separated with `-` as a null placeholder | `https://opendata.tailte.ie/api/Property/GetProperties?Fields=*&LocalAuthority=<AUTHORITY>&Format=json&Download=false` — no key, no account. **Two predecessor hosts are dead and neither redirects**: `api.valoff.ie` is NXDOMAIN and `www.valoff.ie` answers 000, which is why an earlier screen recorded the whole country as negative | none server-side. ⚠️ **`LocalAuthority` is matched EXACTLY and a wrong string returns HTTP 200 with an EMPTY LIST**, not an error — the register spells one council `DUN LAOGHAIRE RATHDOWN CO CO` where the boundary layer spells it `DUN LAOGHAIRE-RATHDOWN COUNTY COUNCIL`, so the join is an explicit mapping table and `fetch_sources.py` asserts a non-trivial row count per authority. **This register carries NO name column of any kind** — no trade name, no occupier, no ratepayer, no owner; step 2 asserts that and EXITS if one ever appears, so the pin label is the street address and Los Angeles' blank-trade-name failure cannot occur here. **`Eircode` is dropped at load** (third-party database right). Licence CC BY 4.0 — notice **22** | 2026-09-22 |

### Dublin — endpoints and findings, verified 2026-09-22

Recorded before the build, while the endpoints were being verified; Dublin
has since been built (the tables below). The full evidence and its six checks,
all passing, are in Dublin's build brief (`docs/build_briefs/dublin.md`).

**The first Irish city, and Ireland yields only this one**, so the national
questions are answered inside the city brief rather than in a separate country
profile.

**Businesses** — Tailte Éireann, the Irish rateable valuation register, through
a keyless JSON API:

```
https://opendata.tailte.ie/api/Property/GetProperties
    ?Fields=*&LocalAuthority=<AUTHORITY>&Format=json&Download=false
```

No key, no account, no registration. **38,265 rows across the four Dublin local
authorities**, of which **13,945 are storefront**. Coordinates are `Xitm`/`Yitm`
in **EPSG:2157 (Irish Transverse Mercator), already in metres, on 99.87% of
rows** — so there is no geocoding step and no reprojection step.

> **TWO PREDECESSOR HOSTS ARE DEAD AND NEITHER REDIRECTS.** `api.valoff.ie` is
> **NXDOMAIN** and `www.valoff.ie` answers **000**. An earlier screen recorded
> Ireland as *negative* on the strength of those two corpses. The API moved
> twice and left no forwarding, and `opendata.tailte.ie/` is itself a 404 with
> no documentation page, no `robots.txt` and no Swagger — the contract is
> stated only in the error body: `Use either Property Number or Local
> Authority`.

> **`LocalAuthority` IS MATCHED EXACTLY, AND A WRONG STRING RETURNS HTTP 200
> WITH ZERO ROWS.** The register spells one authority
> `DUN LAOGHAIRE RATHDOWN CO CO`; the spelled-out
> `DUN LAOGHAIRE RATHDOWN COUNTY COUNCIL` silently returns nothing. The
> **boundary layer spells the same place `DUN LAOGHAIRE-RATHDOWN COUNTY
> COUNCIL`** — hyphenated and unabbreviated. Two strings for one authority, in
> the two sources that must be joined, so the join is an explicit mapping table
> and never string equality.

The four values, with row counts measured 2026-09-22: `DUBLIN CITY COUNCIL`
19,810 · `FINGAL COUNTY COUNCIL` 6,528 · `SOUTH DUBLIN COUNTY COUNCIL` 6,926 ·
`DUN LAOGHAIRE RATHDOWN CO CO` 5,001.

**The register carries no business name.** No trade name, no occupier, no
ratepayer, no owner — 19 fields, all address, classification, valuation and
geometry, checked against
`name|occupier|tenant|owner|ratepayer|proprietor|person|contact` with zero
matches. It records premises, and the Irish valuation list is non-domestic by
statute. This is the strongest privacy position of any source in this project
and it is structural rather than measured.

**Classification is `Uses` (963 distinct values), not `Category` (13).**
`Category` cannot separate this project's three buckets: 1,483 of 2,335
food-service rows and 677 of 744 personal-service rows both sit inside
`RETAIL (SHOPS)`. See the brief for the catch-all measurement, which inverts
Barcelona's rule.

> **TAILTE WITHHOLDS FLOOR-LEVEL DETAIL FOR NAMED PROPERTY TYPES, AND IT DOES
> NOT AFFECT THIS BUILD — MEASURED.** `tailte.ie/home/api/` warns of missing
> detail for "Hotels, Pubs, Cinemas, Service Stations, Guesthouses…" on
> confidentiality grounds. Measured with a control: all 767 `PUB`, 210 `HOTEL`,
> 184 `SERVICE STATION` and 116 guesthouse/hostel/cinema rows arrive **present
> and fully classified**, with `ValuationReport` empty on **100%** of them and
> on **0%** of hairdressers, pharmacies and clothes shops. What is withheld is
> the per-floor valuation, which this project never reads. **It would bite
> totally, and precisely on food service, if the build ever weighted by floor
> area.**

**Boundary** — Tailte Éireann, *Local Authorities — National Statutory
Boundaries — Ungeneralised — 2026*, layer 3:

```
https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/
  National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/
  FeatureServer/3
```

Authority name is `ENG_NAME_VALUE` (Irish `GLE_NAME_VALUE`), spatial reference
**wkid 2157**, 937.3 km² over the four authorities. Unwrapped, for the
provenance check and for copying:

`https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/FeatureServer/3`

> **USE THE FEATURESERVER, NOT THE HUB DOWNLOAD.** `data.gov.ie`'s resource
> list points at `data-osi.opendata.arcgis.com/api/download/v1/items/...`,
> which is the **async job endpoint that answers HTTP 202** — the Surrey trap
> in `add-country`. The FeatureServer above is synchronous and takes a
> where-clause.

> **THE LAYER IS MULTIPART.** Fingal returns **46** polygons and Dún
> Laoghaire–Rathdown **42** — islands and coastal outcrops, most under
> 0.1 km². Dissolve by `ENG_NAME_VALUE` before any point-in-polygon test, or a
> station gets tested against Lambay Island.

**Rail** — the **National Transport Authority's national GTFS**, not
OpenStreetMap. ⚠️ **This corrects what this section said when Dublin's brief
was written.**

`https://www.transportforireland.ie/transitData/Data/GTFS_All.zip`

**The feed is current, measured rather than assumed:** `feed_info.txt` declares
`feed_end_date` **20270922**, a year out, and it carries **Woodbrook
(`8220WBROK`), a station that opened in 2025** — so it is maintained, not a
re-uploaded archive. Three routes are drawn: `10000 GREEN g a` (Luas Green,
`route_type 0`), `10000 RED g a` (Luas Red, `0`) and `BRAY-HOWTH-I` (DART,
`2`). Commuter and InterCity are other `route_id`s under the same
`route_type 2` and are excluded.

> **THE BRIEF ASSERTED "OPENSTREETMAP, NOT A FEED" WITHOUT CHECKING FOR ONE,
> AND THAT WAS MADRID'S FAILURE REPEATED.** The `osm-rail` order is agency GIS
> layers → agency GTFS → OSM **on a recorded ground**; neither of the first two
> had been run. Both pass. The NTA also publishes a **Feature Service already
> in EPSG:2157** — 14,079 stops, 6,507 route polylines, at
> `services-eu1.arcgis.com/p0UmGrpumWZYhF0p/` — whose `GTFS - Stops` layer even
> carries `local_authority` pre-populated in the boundary layer's spelling.

> **THE FEED IS 158 MB AND ITS `shapes.txt` IS 372 MB OVER 8.0M ROWS.**
> `fetch_sources.py` trims it once to the three routes (→ 1.9 MB) so no step
> and no drift check ever parses the national file.

> **`route_color` IS EMPTY FOR ALL THREE ROUTES**, in both the feed and the
> feature service, so the palette is chosen rather than inherited — and it is
> chosen against `map_common`'s CIE76 separation check, not by eye. OSM's
> community colours scored 21.7–27.5 against the category pins the lines are
> drawn under. See `pipeline/dublin/config.py` for the measurements: Luas Red
> `#8B0000`, Luas Green `#006400`, DART `#F57C00`.

> **DART'S `route_long_name` IS "Bray - Howth", WHICH UNDERSTATES IT** — its
> own stops run Malahide to Greystones. The drawn label is `route_short_name`,
> `DART`.

**OpenStreetMap is retained as a cross-check**, not as the source — 42 route
relations in the Dublin bbox, cached and compared against the feed every run
(GTFS 98 station names, OSM 100, 88 shared; the differences are spelling).
Madrid's three sources agreeing on 13 lines while landing at 243 / 236 / 230
stations is why a second opinion is kept.

> **OSM TAGS ALL FOUR DART RELATIONS `network=Commuter`** — the same value the
> Northern, Western and South Western services carry. A `network` filter drops
> Dublin's principal line, which a run proved before the source changed. The
> `osm-rail` rule that a `network` tag is a label and not evidence, measured.

> **`overpass.osm.ch` RETURNED AN EMPTY 200 FOR THIS QUERY ON 2026-09-22.**
> `pipeline/osm.py` rejects that; a hand-rolled fetch does not, and the first
> attempt here would have recorded "0 relations" against a real 42.

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Dublin | **National Transport Authority national GTFS** — 3 drawn routes: `10000 GREEN g a` (Luas Green, `route_type 0`), `10000 RED g a` (Luas Red, `0`) and `BRAY-HOWTH-I` (DART, `2`) | `https://www.transportforireland.ie/transitData/Data/GTFS_All.zip` | 2026-09-22 | **The brief said "OpenStreetMap, not a feed" and was WRONG — corrected during the build** (Madrid's failure in its general form). Why the feed is trusted, its size and trim, its empty `route_color` and the OSM cross-check are in "Dublin — endpoints and findings" above; OSM tags all four DART relations `network=Commuter`, so the whitelist is on `ref`. ODbL 1.0 for the cross-check — notice **1** |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Dublin | Tailte Éireann **Local Authorities — National Statutory Boundaries — Ungeneralised — 2026**, layer 3 | `https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/FeatureServer/3` | The four Dublin councils, **937.3 km²** dissolved (Dublin City 130.1, Fingal 457.2, South Dublin 223.4, Dún Laoghaire-Rathdown 126.5), name field `ENG_NAME_VALUE`, native **wkid 2157**. ⚠️ **Use the FeatureServer, NOT the resource data.gov.ie lists** — that is the ArcGIS Hub async download endpoint which answers HTTP 202 with a job id, the Surrey trap. ⚠️ **THE LAYER IS MULTIPART**: Fingal returns **46** polygons and Dún Laoghaire-Rathdown **42**, nearly all islands and coastal outcrops under 0.1 km², so it must be dissolved by name before any point-in-polygon test or a station is tested against Lambay Island. Only 2 stations fall outside (Bray Daly and Greystones, both County Wicklow), recorded in `outputs/dublin/excluded_stations.csv` |
