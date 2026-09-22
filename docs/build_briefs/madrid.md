# Madrid — build brief

**Step 0's answers, banked 2026-09-22.** Read this before `add-city` Step 0,
then run `python scripts/brief_check.py madrid` before writing any code. A
brief caches Step 0's mistakes as confidently as its findings — Edmonton's
cached three — so every claim below that can be re-run is declared in the
`brief-checks` block at the end.

**Spain is a new country for this project.** `add-country` has profiled it;
this is the first Spanish city, so the country-level facts below are also the
ones Barcelona, Valencia, Bilbao, Málaga and Sevilla will inherit.

---

## The one-line summary

Business leg is **excellent and ready**. Rail leg is **resolved but the Metro
feed is four months expired**, and that is the only real decision in this
build.

---

## Business leg — `datos.madrid.es`, MEASURED 2026-09-22

**The portal is CKAN, at the bare host.** An earlier screen recorded it
"unreachable" on the path `/egob` — a fact about the guess, not the portal.

- Package: **`200085-0-censo-locales`** — *Censo de locales, sus actividades y
  terrazas de hostelería y restauración*
- Licence: **CC BY 4.0** (`cc-by`), confirmed in `package_show`
- `metadata_modified`: refreshed daily (2026-09-22T05:42 at time of writing)

### Which resource to use

The package carries 13+ resources. Three are in the datastore and matter:

| Resource | Rows | Cols | What it is |
|---|---|---|---|
| `200085-1-censo-locales` | **203,662** | 47 | Locales only |
| **`200085-5-censo-locales`** | **225,660** | **48** | **Locales × actividades join — USE THIS** |
| `200085-6-censo-locales` | 6,593 | 118 | Terrazas (pavement terraces) |

`200085-5` is the join, so a local with two activities appears twice. Dedupe on
`id_local` if a premises count is wanted; keep the duplication if the map is
activity-driven.

### ⚠️ TRAP — the download URL rots, the resource id does not

Resource URLs embed a build timestamp:

```
.../download/200085_20260922_053829.csv
              ^^^^^^^^^^^^^^^^^ changes on every refresh
```

**Do not hardcode a file URL in `config.py`.** Resolve it at fetch time from
`package_show` by resource id, which is stable. This is the first source in the
project where the URL is not durable, and a hardcoded one will 404 silently
within days.

### Schema — the fields that matter

- **Coordinates**: `coordenada_x_local`, `coordenada_y_local` — **EPSG:25830**
  (ETRS89 / UTM 30N). Already metres, so the project's
  never-measure-in-4326 invariant is satisfied by the source CRS itself; no
  reprojection is needed for the ring geometry, only for display.
- **Trade name**: `rotulo` — the shop sign. 100% populated on the usable rows.
- **Status**: `desc_situacion_local` — 100% populated.
  `Abierto` 159,835 · `Cerrado` 40,407 · `Baja` 12,557 ·
  `Uso vivienda` 8,486 · `Baja Reunificación` 4,382.
  **Filter to `Abierto`.** Note `Uso vivienda` means the unit reverted to
  residential use — a residence signal supplied by the source, which most
  cities make this project infer.
- **Classification**: three levels, `desc_seccion` → `desc_division` →
  `desc_epigrafe`. A documented local taxonomy, which the project's invariant
  explicitly permits; it is **not** NAICS and must not be forced into it.
- **Geography**: 22 districts (`desc_distrito_local`) — all of them — plus
  barrio and census section.

**Open + classified + with coordinates: 148,814**, i.e. 93.1% of `Abierto`.
That is the number the map will actually draw from, and it is larger than
Barcelona's 68,024.

### Encoding and delimiter

**UTF-8 with BOM, semicolon-delimited.** Record `SOURCE_ENCODING` in the city
config explicitly — declared, never inferred.

---

## Rail leg — CRTM, and the Metro feed is EXPIRED

Spain's National Access Point (`nap.transportes.gob.es`) is registration-gated
— it answered 401 for Sevilla's feed. **Madrid does not need it.** The
Mobility Database lists CRTM feeds with direct ArcGIS downloads.

| Feed | Modes | Calendar | State |
|---|---|---|---|
| **`mdb-794` Metro de Madrid** | **13 × `route_type=1`** | 20250527 → **20260527** | ⚠️ **EXPIRED ~4 months** |
| `mdb-792` CRTM | 4 × `route_type=0` (Metro Ligero) | 20260722 → 20270722 | ✅ current |
| `mdb-791` CRTM | 354 × `route_type=3` (bus) | 20260722 → 20270826 | ✅ current, 72 MB |
| `mdb-993` CRTM | 236 × `route_type=3` (bus) | 20260724 → 20261231 | ✅ current |

**CRTM keeps its bus and light-rail feeds current and lets the Metro feed go
stale.** That is the Edmonton failure shape exactly — a feed that downloads
cleanly, parses cleanly, and describes a service window that has already ended.

`mdb-794`'s contents, which are otherwise good:

- 1,503,773 bytes, 12 members, **`feed_info.txt` present** (`feed_version`
  `20250527`) — so staleness *is* checkable from the feed itself, unlike
  Toronto's
- **13 routes, all `route_type=1`** — lines 1–12 plus `R` (Ramal).
  Cross-validates against the OSM screen, which found 13 subway relations
- **1,050 stops**, and the station count needs care — it is the most
  error-prone number in this project:
  - **240** rows are `location_type=1` (declared stations)
  - **520** are `location_type=2` (street entrances) — never count these
  - but only **272 platforms are actually served by rail trips**, collapsing
    via `parent_station` to **230 stations**
  - **so 10 declared stations are served by no trip in this feed.** Use
    **230**, not 240. The gap is probably closures or stations the expired
    calendar no longer serves, and it has not been chased down.
  - `parent_station` is populated, so the collapse is reliable rather than
    name-matched
- **100% coordinates**, `shapes.txt` present — so
  every-line-drawn-and-labelled is satisfiable

### The decision this build has to make

1. **Find a newer CRTM item.** The Mobility Database entry may simply point at
   a superseded ArcGIS item id while CRTM publishes a current one elsewhere.
   Cheapest first move.
2. **Use OSM for the Metro leg.** The precedent exists and is documented —
   CDMX, approved as a per-city exception, validated at 195/195 stops. The
   `osm-rail` skill covers it. Madrid's 13 subway relations are already
   screened.
3. **Use the expired feed anyway.** Station *positions* do not expire even when
   the service calendar does, and this project draws geometry, not timetables.
   Defensible — but it must be a stated decision in `DECISIONS.md`, not a
   silent one, and the notice must not imply the data is current.

**Not yet decided. This is the build's first question.**

### ⚠️ Licence — UNREAD

`mdb-794` declares `http://www.crtm.es/licencia-de-uso`. **Nobody has opened
it.** Run the `read-licence` skill before publishing; LA Metro's GTFS forbids
modifying its data while the same city's business registry is CC0, so a
transit licence is never assumed from the business one.

---

## Notices this city will owe

Already recorded in `docs/data_sources.md` from the licence read on
2026-09-22 — three obligations, and they are conditions, not courtesies:

1. **Prescribed attribution wording** — *"Origen de los datos: Ayuntamiento de
   Madrid"*. CC BY wants attribution; Madrid dictates the sentence.
2. Modification/interpretation must be disclosed.
3. **No implied endorsement** — must not *"indicar, insinuar o sugerir que el
   Ayuntamiento de Madrid participa, patrocina o apoya"* the reuse.

Plus whatever CRTM's licence turns out to require.

---

## Still unknown — the honest list

- **Which rail route to take** (above). The only blocking question.
- **CRTM's licence terms.** Unread.
- Whether `200085-5`'s activity duplication needs deduping for this map, which
  depends on a taxonomy choice not yet made.
- Whether Madrid's system shape needs a sub-line filter
  (`docs/sub_transit_line_filters.md`) — 13 lines over 240 stations is dense
  and uniform, so probably not, but it has not been looked at.
- `check_personal_exposure.py` has never been run against a Spanish register.
  `rotulo` is a trade name, which is the safe field, but the epígrafe catch-all
  categories have not been reviewed the way LA's 812990 was.

```brief-checks
[
  {
    "id": "business-rows",
    "claim": "Resource 200085-5 (locales x actividades) holds 225,660 rows",
    "kind": "ckan_rows",
    "domain": "datos.madrid.es",
    "resource_id": "200085-5-censo-locales",
    "expect": 225660,
    "tolerance": 12000
  },
  {
    "id": "business-fields",
    "claim": "The join carries coordinates in EPSG:25830, a shop sign, a status field and the three-level taxonomy; and NO lat/lon",
    "kind": "ckan_fields",
    "domain": "datos.madrid.es",
    "resource_id": "200085-5-censo-locales",
    "present": ["id_local", "coordenada_x_local", "coordenada_y_local", "rotulo", "desc_situacion_local", "desc_seccion", "desc_division", "desc_epigrafe", "desc_distrito_local"],
    "absent": ["latitude", "longitude", "lat", "lon", "geo_point_2d"]
  },
  {
    "id": "business-locales-only",
    "claim": "Resource 200085-1 is locales WITHOUT the activity join, so it is smaller",
    "kind": "ckan_rows",
    "domain": "datos.madrid.es",
    "resource_id": "200085-1-censo-locales",
    "expect": 203662,
    "tolerance": 12000
  },
  {
    "id": "metro-feed-downloads",
    "claim": "Metro de Madrid's GTFS downloads direct from CRTM's ArcGIS, no NAP account",
    "kind": "http_ok",
    "url": "https://crtm.maps.arcgis.com/sharing/rest/content/items/5c7f2951962540d69ffe8f640d94c246/data",
    "min_bytes": 800000
  },
  {
    "id": "metro-feed-members",
    "claim": "The Metro feed carries feed_info.txt AND shapes.txt - staleness is checkable from the feed, and lines can be drawn",
    "kind": "gtfs_files",
    "url": "https://crtm.maps.arcgis.com/sharing/rest/content/items/5c7f2951962540d69ffe8f640d94c246/data",
    "present": ["routes.txt", "trips.txt", "stop_times.txt", "stops.txt", "shapes.txt", "feed_info.txt", "calendar.txt", "calendar_dates.txt"],
    "absent": []
  },
  {
    "id": "metro-feed-is-expired",
    "claim": "THE METRO FEED IS EXPIRED - calendar ended 2026-05-27. When this check FAILS, CRTM has refreshed it and the build's rail decision should be revisited",
    "kind": "gtfs_calendar_window",
    "url": "https://crtm.maps.arcgis.com/sharing/rest/content/items/5c7f2951962540d69ffe8f640d94c246/data",
    "expect": "expired"
  },
  {
    "id": "metro-is-all-rail",
    "claim": "13 routes, every one route_type=1, matching the OSM screen's 13 subway relations",
    "kind": "gtfs_route_type_counts",
    "url": "https://crtm.maps.arcgis.com/sharing/rest/content/items/5c7f2951962540d69ffe8f640d94c246/data",
    "expect": {"1": 13}
  },
  {
    "id": "metro-station-count",
    "claim": "230 BOARDABLE stations, not the 240 declared at location_type=1: 272 platforms are served by rail trips and collapse via parent_station to 230. Never count the 520 entrances",
    "kind": "gtfs_stations",
    "url": "https://crtm.maps.arcgis.com/sharing/rest/content/items/5c7f2951962540d69ffe8f640d94c246/data",
    "route_types": [1],
    "expect_parent_station_populated": true,
    "expect_platforms": 272,
    "expect_stations": 230
  },
  {
    "id": "madrid-utm-zone",
    "claim": "Madrid at about 3.7W falls in UTM 30N; the source CRS EPSG:25830 is the ETRS89 flavour of that same zone",
    "kind": "utm_zone_from_longitude",
    "lon": -3.7038,
    "expect": "EPSG:32630"
  }
]
```
