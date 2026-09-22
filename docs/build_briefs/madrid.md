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

Business leg is **excellent and ready**. Rail leg is **settled: Metro comes
from OpenStreetMap**, because CRTM's Metro feed expired four months ago, no
newer item exists, and CRTM's licence forbids displaying stale data.

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

### ⚠️ TRAP — the coordinate column is 100% populated and partly invalid

**Do not quote 148,814 as the mappable count.** Open + classified + with a
non-empty coordinate is 148,814, but a share of those coordinates are a
literal zero, which in EPSG:25830 projects to a point in the Atlantic off West
Africa — it vanishes silently on a station-radius map rather than erroring.

**The zeros are stored as the string `'0.0'`, not as empty.** So a
"is this column populated?" test passes them, and so does the `ckan_fields`
check in this very brief. Only a numeric or bounding-box test catches them.

| | |
|---|---|
| Evidence trail, full file, 2026-09-22 | **29,744 of 148,814 = 19.99%** zero → **119,070 genuinely mappable** |
| Re-measured 2026-09-22, first 4,000 `Abierto` rows via datastore | **234 = 5.85%** |

**These disagree and the rate is NOT settled.** The datastore sample is the
first 4,000 rows in `_id` order, not a random draw, so it is not
representative and the trail's 19.99% is the safer planning figure. **Measure
it on the full download before quoting any density number** — at 20% this
moves Madrid's headline by a fifth, so the check has to run before the number
is published, not after.

> ### ✅ SETTLED 2026-09-22 on the full 124,987,034-byte download — and neither figure was the one that matters
>
> | Scope | Rows | Zero | Rate |
> |---|---|---|---|
> | All `Abierto` | 159,787 | 34,316 | **21.48%** |
> | The three storefront sections | 88,718 | 13,120 | **14.79%** |
> | **…minus `SERVICIOS DE ALOJAMIENTO`** | **81,142** | **7,471** | **9.21%** |
>
> → **73,671 usable rows, 61,466 usable DISTINCT premises.**
>
> **THE RATE WAS NEVER THE DELIVERABLE; THE DISTRIBUTION WAS**, and the
> distribution turned out to explain the disagreement. The zeros are not spread
> across the register — they concentrate in activities this project does not
> map:
>
> | Activity | Zero rate |
> |---|---|
> | VIVIENDAS TURÍSTICAS | **85.9%** |
> | HOSTALES | 74.7% |
> | ALBERGUES JUVENILES… | 68.5% |
> | ACTIVIDADES ADMINISTRATIVAS Y AUXILIARES DE OFICINA | 55.0% |
> | ACTIVIDADES JURIDICAS | 45.0% |
> | *vs* FARMACIA | **1.2%** |
> | *vs* TALLER DE REPARACIÓN (chapa y pintura) | **0.7%** |
>
> **`HOSTELERÍA` is the `72`-versus-`722` trap in Spanish.** It splits into
> `SERVICIOS DE COMIDAS Y BEBIDAS` (20,345 rows, **10.6%** zero) and
> `SERVICIOS DE ALOJAMIENTO` (7,576 rows, **74.6%** zero). Accommodation is not
> food service and must be excluded from the bucket on scope grounds alone —
> the same correction the Mexico build made when counting `72` instead of `722`
> swept in hotels. Excluding it removes 5,649 of the 7,471 remaining zeros.
>
> The district bias collapses with it. Raw, CENTRO is **46.1%** against
> Villaverde's **4.6%** — a 10× spread that would have gutted precisely the
> downtown a transit-density map is about. Once accommodation is out, the
> spread is Barajas **19.4%** to Villaverde **2.9%**, because the raw figure
> was largely tourist flats and hostels clustered in the centre.
>
> **So the loss is real but tolerable, and it is NOT the Los Angeles case.**
> LA's bad coordinates were biased *toward* the rows the map wanted (22% of
> post-2020 registrations against ~1% of older ones). Madrid's are biased
> *away* from them. No geocoding leg is needed, and CartoCiudad stays unprobed.
>
> **⚠ CORRECTION TO THIS BRIEF'S OWN COMPARISON.** "Madrid is 2.2× Barcelona's
> 68,024" divides 148,814 — all open sections, joined rows, zeros included — by
> Barcelona's ground-floor premises census. Those are not comparable
> quantities. On storefront-filtered mappable premises Madrid is **61,466**,
> which is *comparable to* Barcelona rather than double it. Before either
> number is published, establish whether Barcelona's 68,024 is itself
> storefront-filtered; until then the two cities' counts should not be compared
> at all.

Madrid is the **second** city in this project with literal `(0,0)` rows — Los
Angeles had ~9%. Two of the three pre-geocoded registries examined at this
depth had the defect, which is why `add-city` Step 0 asks for a bounding-box
count on every city rather than only on suspicion.

**Even at 119,070, Madrid is 1.75× Barcelona's 68,024 and needs no
geocoding.**

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

### The decision this build has to make — RESOLVED 2026-09-22

1. ~~**Find a newer CRTM item.**~~ **MEASURED OUT.** CRTM's ArcGIS org
   (`orgId UxADft6QPcvFyDU1`, owner `ConsorcioRegional`) holds **exactly six
   GTFS items**, and the Metro one is the stale one:

   | Item | Last modified |
   |---|---|
   | GTFS Red de EMT | 2026-07-29 |
   | GTFS Red de Autobuses Urbanos | 2026-07-29 |
   | GTFS Red de Autobuses Interurbanos | 2026-07-29 |
   | **GTFS Red de Metro Ligero** (`aaed26cc…`) | **2026-07-29** |
   | **GTFS Red de Metro** (`5c7f2951…`) | **2025-05-30** |
   | GTFS Red de Cercanías (`1a25440b…`) | 2024-08-27 |

   **`5c7f2951…` is the current item.** The Mobility Database is not pointing
   at something superseded; CRTM refreshes four of its six feeds and has
   stopped refreshing Metro. There is nothing newer to find.
2. **Use OSM for the Metro leg.** The precedent exists and is documented —
   CDMX, approved as a per-city exception, validated at 195/195 stops. The
   `osm-rail` skill covers it. Madrid's 13 subway relations are already
   screened.
3. ~~**Use the expired feed anyway.**~~ **RULED OUT 2026-09-22 by CRTM's own
   licence**, which was unread when this option was written. It obliges the
   reuser to *"garantizar que la información mostrada en su sistema esté
   siempre actualizada"* — keep what is shown up to date. Station positions
   not going stale is beside the point; the condition is about what the
   reuser displays, and a feed CRTM has stopped refreshing cannot satisfy it.

> ### ⚠️ SUPERSEDED 2026-09-22 — the rail leg comes from CRTM after all
>
> **Option 1 was measured out against CRTM's six GTFS ITEMS, and CRTM
> publishes the same network twice.** Its ArcGIS **feature services** are a
> different product on a different refresh cycle, and they are maintained:
>
> | Product | Last edited | Age |
> |---|---|---|
> | GTFS Red de Metro | 2025-05-30 | ~16 months |
> | **`M4_Red`** (stations + segments) | **2026-06-05** | **~3.5 months** |
> | `M4_Lineas` (per-line breakdown) | 2026-04-21 | ~5 months |
>
> `M4_Red` carries the whole leg — `M4_Estaciones` **293 points** with
> `DENOMINACION`, `CODIGOMUNICIPIO`, `DISTRITO` and `FECHAACTUAL`;
> `M4_Tramos` **560 polylines** with **`NUMEROLINEAUSUARIO`** (the line as
> riders name it, e.g. `10b`), `SENTIDO` and `MUNICIPIO`; `M4_Accesos` 802
> entrances **already separate** from stations. Natively **EPSG:25830, the
> same CRS as the premises data**.
>
> **Owner's decision 2026-09-22: use CRTM's feature layers, keep OSM as the
> cross-check.** That removes the CDMX-style per-city exception and its page
> notice, gives the operator's own line names instead of a hand-assigned
> palette, and reads far better against the "siempre actualizada" condition at
> 3.5 months than at 16 — stated beside `FECHAACTUAL` 20260529, which Madrid's
> own licence already obliges this project to display.
>
> **Why the tripwire missed it.** `metro-feed-is-expired` says *"when this
> check FAILS, CRTM has refreshed it"* — and it still passes, correctly,
> because the GTFS really is still expired. It watched the feed while the
> build wanted the network. The two `arcgis_layer` checks added to the block
> below watch the product actually consumed; that is the generalisable lesson
> and it is why the check kind exists.
>
> **Two traps carry over regardless of source.** `SENTIDO` 1/2 duplicates
> every stretch, so **560 tramos is not 560 segments** — CRTM's form of the
> 28-relations trap recorded for OSM below. And **293 is not the station
> count** against OSM's 236 and GTFS's 230; reconcile in Step 4 before quoting
> a figure, rather than taking the largest number because it is largest.
>
> **The OSM work below is not wasted** — it becomes an independent second
> source agreeing on line count and station positions, which is gate-3-grade
> corroboration, and gate 3 is otherwise UNAVAILABLE for Madrid as it was for
> Mexico City.

~~**So the answer is 2: take Madrid's Metro from OpenStreetMap**, the CDMX
precedent, which the owner approved as a documented per-city exception and
which validated at 195/195 stops exact. Use the `osm-rail` skill.~~

**One nuance worth keeping:** `GTFS Red de Metro Ligero` *is* current
(2026-07-29, `mdb-792`, 4 × `route_type=0`, 96 stops). So Madrid could take
Metro from OSM and Metro Ligero from the agency feed. That is a mixed-source
rail leg for one city, which this project has not done before — simpler to
take both from OSM, and the reason to choose otherwise would be that agency
data is the standing default. **Left to the build; both inputs are known
good.**

Cercanías (commuter rail) is stale too (2024-08-27) and is probably out of
scope for a metro-density map, but that has not been decided either.

### OSM validated for Madrid Metro — MEASURED 2026-09-22

Run before committing the build to it, the way CDMX was. Metropolitan bbox
`40.20,-3.95,40.65,-3.45`, wider than the municipality because lines 9, 10 and
12 leave it.

| | OSM | GTFS `mdb-794` | |
|---|---|---|---|
| Lines | **13 distinct `ref`** — L1–L12 + R | **13** `route_type=1` | **exact match** |
| Stations | **236** `station=subway` nodes | **230** boardable | **2.6% apart** |

Two independent sources agreeing exactly on line count and to within six
stations is the strongest cross-validation available here, and it is what
makes OSM safe for this city rather than merely available.

- **All 28 relations are named. All 28 carry a `colour`.** So the
  every-line-labelled-and-in-the-legend invariant is satisfiable directly from
  OSM tags, with no hand-assigned palette — unlike Medellín, where only 2 of 6
  were coloured.

⚠️ **28 relations is NOT 28 lines.** They are **directional pairs** plus
depot/variant branches — *"Línea 4: Pinar de Chamartín-Argüelles"* and
*"Línea 4: Argüelles-Pinar de Chamartín"* are the same line, and *"Línea 6:
Andén 2"* and *"Línea 12. Metrosur (Dirección Loranca - Andén 2)"* are
platform-direction variants. **Deduplicate on `ref`, which gives 13.** Counting
relations would draw and label Madrid as a 28-line system. This is the
Guadalajara lesson in its other form: the first query there matched on a
network label and lost a whole line; here a naive count invents fifteen.

⚠️ **The construction filter returned 0, which is not the same as "none".**
Per the Tel Aviv finding, a zero can mean *"nothing to flag"* or *"this
convention is not used here"*. Madrid has no Metro line under construction
today, so 0 is plausible — but it was not independently confirmed, and the
filter's silence is not evidence.

**The 6-station gap is unexplained** and worth a minute during the build: it is
probably Metro Ligero stops tagged `station=subway`, or stations the expired
feed dropped. 326 `railway=station` nodes exist in the same bbox, so the
`station=subway` qualifier is doing real work — do not drop it.

### ✅ Licence — READ 2026-09-22

`mdb-794` declares `http://www.crtm.es/licencia-de-uso`. **Now read in full;
see `docs/data_sources.md`.** Verdict **PERMITTED WITH CONDITIONS** —
commercial reuse and modification are expressly granted, and the share-alike
clause binds redistribution of the *data*, not a value-added derivative work
like this map.

Three consequences for the build:

- **A new prescribed notice: "Powered by CRTM"** with a link to crtm.es. It is
  this project's **sixth** prescribed notice and its first Spanish one.
- **Raw-vs-processed must be stated** — *"especificando si son datos en bruto
  o explotados"*. A bare source credit does not satisfy it.
- **The "keep it up to date" condition rules out the expired feed**, above.

**Madrid therefore owes two separate attributions from two separate
licences** — Ayuntamiento de Madrid for the premises, CRTM for the rail.

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

- **Metro Ligero: agency feed or OSM?** The Metro question is settled
  (OSM); this sub-question is not, and neither is whether Cercanías is in
  scope at all.
- Whether `200085-5`'s activity duplication needs deduping for this map, which
  depends on a taxonomy choice not yet made.
- Whether Madrid's system shape needs a sub-line filter
  (`docs/sub_transit_line_filters.md`) — 13 lines over 240 stations is dense
  and uniform, so probably not, but it has not been looked at.
- **The real zero-coordinate rate** (above): 19.99% on the full file per
  the trail, 5.85% on an unrepresentative datastore sample. Settle it on
  the full download.
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
    "id": "crtm-metro-network-layer",
    "claim": "CRTM's M4_Red feature service is the rail leg's ACTUAL source and is still maintained - 293 stations with the name and municipality fields the build needs. If this goes stale the rail decision must be revisited, which the GTFS tripwire below cannot tell you",
    "kind": "arcgis_layer",
    "url": "https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M4_Red/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 293,
    "tolerance": 25,
    "present": ["DENOMINACION", "CODIGOESTACION", "CODIGOMUNICIPIO", "FECHAACTUAL"],
    "max_age_days": 550
  },
  {
    "id": "crtm-metro-line-geometry",
    "claim": "M4_Tramos carries the drawable line geometry with NUMEROLINEAUSUARIO, the line as riders name it, so the label-and-legend invariant is satisfiable from operator data",
    "kind": "arcgis_layer",
    "url": "https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M4_Red/FeatureServer/4",
    "expect_geometry": "esriGeometryPolyline",
    "expect_rows": 560,
    "tolerance": 60,
    "present": ["NUMEROLINEAUSUARIO", "SENTIDO", "MUNICIPIO"],
    "max_age_days": 550
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
