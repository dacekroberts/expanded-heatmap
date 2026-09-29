# Buenos Aires — build brief

**Screened 2026-09-28 (staging, the large-transit gap's never-screened
list); Band A (owner).** Run `python scripts/brief_check.py buenos-aires`
before writing any code. The trail: `DECISIONS.md` 2026-09-28 "Buenos Aires
to Band A, Melbourne (City of Melbourne) to Band B...", and the Argentina row
in `docs/global_country_shortlist.md` Tier 4. Argentina's first city: run
`add-country` for the country profile first, briefly (one source, one city).

---

## The one-line summary

**A city-wide land-use survey of every ground-floor use, joined to the city's
own parcels at 99.8%, under a read CC BY licence. All three buckets, no
names. The work is the taxonomy (385 subtypes) and the rail scope.**

---

## Business leg — Relevamiento Usos del Suelo 2022-2024 (BA Data)

| | |
|---|---|
| **Rows** | **417,764**, one per observed use at an address (surveyed 2022: 78,191; 2023: 181,914; 2024: 157,659) |
| **Active storefronts** | **87,028** (`TIPO1 == "UNICOMERCIAL"` and `ESTADO == "ACTIVO"`) |
| Identified | **92.8%**: "SIN IDENTIFICAR" is 7.2% of active storefront rows (23.0% of all storefront rows, because 18,240 of the 19,323 inactive ones are unidentified vacant shopfronts) |
| Downtown catch-all | Monserrat 9.9%, San Nicolás 6.9%, Balvanera 11.5%, Palermo 4.9%, Recoleta 2.9%; worst Villa Riachuelo 31.9% |
| Subtypes | **385 distinct `TIPO2`** among active storefronts (471 across all rows): PELUQUERIA 2,692, BARBERIA 663, LAVADERO DE ROPA 947, RESTAURANTE 2,715, CAFÉ 1,728, KIOSCO 3,011, INDUMENTARIA 6,118, and so on |
| Against OSM | **3.5×** OSM's shops + food amenities inside CABA (18,285 + 6,493) |
| Names | **None**: the survey records uses, not businesses |
| Fields | `OBJECTID, SMP, BARRIO, TIPO1, TIPO2, ESTADO, PISOS, GP_Q, OBS, CALLE, PUERTA, UNIFICADO, SMP_IDEM, AÑO` |
| Published | October 2025 (BA Data, Subsecretaría de Planeamiento, DG Antropología Urbana) |
| Cached | `data/buenos-aires/raw/relevamiento-usos-del-suelo-2022-2024.csv`, 39,492,398 bytes, sha256 `5743336654ff9034a2f54129dd7c89011aa401c151828319b7fa1b06367fa2f1` (owner-approved download) |

### ⚠️ Taxonomy traps

- **Key on `TIPO2` inside `TIPO1 == "UNICOMERCIAL"`**, and write a
  `premises-taxonomy` module mapping the 385 strings to the three buckets.
  Measure the catch-all with `brief_check.py`'s `taxonomy_catchall` kind once
  the module exists. Out of scope inside UNICOMERCIAL: car workshops (TALLER
  MECANICO, 2,993), estate agents (INMOBILIARIA, 1,894), banks, car
  dealers and similar.
- **`TIPO2` accented vowels are mojibake IN THE PUBLISHED FILE** (corrected
  at the build, 2026-09-28): read as UTF-8, `CAFÉ` is `CAF├ë` (U+251C
  U+00EB), `LIBRERÍA` is `LIBRER├ìA`; the publisher decoded UTF-8 as code
  page 437 and saved the result. `Ñ` is intact. Repair with
  `value.encode("cp437").decode("utf-8")` (`ba_usos_suelo.repair`) and key
  on the repaired form. The same damage is in `TIPO1`/`BARRIO` values
  (`GALER├ìA BARRIAL`, `USOS M├ÜLTIPLES`).
- **MULTICOMERCIAL (615 rows) is one row per mall or arcade**: PASEO DE
  COMPRAS 361, GALERÍA BARRIAL 206, MERCADO 27, SHOPPING 21. The shops
  inside are not itemised. Leave them out, or show them as one pin each, and
  say which.
- **Homes with an economic activity are a RESIDENCIAL subtype**
  ("MULTIFAMILIAR / UNIFAMILIAR CON ACTIVIDAD ECONÓMICA", 1,758 rows). They
  are excluded by the `TIPO1` filter; keep them out, because they mark homes.
  `OBS` is empty on every active storefront row.
- **`UNIFICADO` / `SMP_IDEM` (5,051 rows)** mark parcels surveyed as merged;
  check them before de-duplicating.
- **"SIN IDENTIFICAR" active rows (6,243)**: a shopfront whose use the
  surveyor could not tell. Drop and disclose, or draw as an unclassified
  storefront; the owner's call at the build.

---

## Placement — a JOIN to Parcelas, not a geocoder (`address-join`)

| | |
|---|---|
| Source | BA Data **Parcelas** (`parcelas_catastrales.csv`), 318,046 parcels, one row per `smp`, `geometry` as **WKT POLYGON in WGS84 lon/lat** |
| Key | the survey's `SMP` against Parcelas' `smp`, after **removing spaces and upper-casing** (the survey writes `039-090-022a`; Parcelas has other spacings) |
| Exact match | **99.8%** of active storefront rows |
| Block match | 100% (section-block prefix), the fallback for the 0.2% |
| Point | the parcel centroid; project to the city's CRS before taking it |
| Cached | `data/buenos-aires/raw/parcelas_catastrales.csv`, 329,396,024 bytes, sha256 `f3debefdaccc02e59f0d417e60531ad95c9adefbe301c91ae9ca39099e5d7019` (owner pre-approved). **Read `smp` and `geometry` in chunks**; the file is 329 MB of polygons |

⚠️ **Several uses share one parcel** (towers, corner buildings). Pins stack
at the centroid; say so if the renderer jitters them.

---

## Licence — CC BY 2.5 AR, read (`licence-read` 2026-09-28)

- **Permitted with conditions**: worldwide, perpetual, royalty-free; the
  city's guide says commercial use is allowed. Nothing is owed up front.
- **The page must show**: credit to the Gobierno de la Ciudad de Buenos
  Aires / BA Data and the two author units (DG Antropología Urbana,
  Subsecretaría de Planeamiento; Subsecretaría de Registro, Interpretación y
  Catastro), the dataset titles and URIs
  (`https://data.buenosaires.gob.ar/dataset/relevamiento-usos-suelo`,
  `https://data.buenosaires.gob.ar/dataset/parcelas`), the licence URI
  (`http://creativecommons.org/licenses/by/2.5/ar/`), and **a sentence on how
  the data was changed** (filtered to storefronts, grouped into buckets,
  placed at parcel centroids).
- **Versions disagree**: the datasets say 2.5 AR, the 2022-2024 resources say
  unversioned `cc-by`, Parcelas' resources say 4.0. Write one credit that
  satisfies both 2.5 AR and 4.0; never describe the data as "CC BY 4.0"
  alone.
- **No GCBA or BA Data logos.** If the city asks for its credit to be
  removed, remove it (s.4(a)), and honour any removal request.
- The portal glossary speaks of sharing "under the same licence"; it is not a
  licence term, and the site does not redistribute the CSV.
- Needs `docs/data_sources.md` rows for both datasets, and the notice in the
  published-notices list.

---

## Rail — OpenStreetMap (the GTFS feed has no `routes.txt`)

| Mode | Relations | Refs | Colours |
|---|---|---|---|
| `subway` | 12 | **6**: A #1CA4CB, B #C20924, C #003EA1, D #217861, E #6B297E, H #F4CC21 | all |

⚠️ **The Premetro** (a light-rail feeder from line E) is not `route=subway`;
include it or not is a scope call. Commuter rail (Mitre, Sarmiento, Roca and
others) is out, by the project's usual rule.

⚠️ Scope is **CABA** (the Ciudad Autónoma), which is the survey's area and
contains the whole Subte. OSM area id 3603082668 resolved from
`["name"="Ciudad Autónoma de Buenos Aires"]["admin_level"="4"]`.

---

## Access traps

- **BA Data's CKAN API rejects non-browser clients**: `package_show` returns
  a 245-byte "Request Rejected" page to the project's user agent, and the
  full JSON to a browser user agent. **The CDN (`cdn.buenosaires.gob.ar`)
  serves the files to any client**; `fetch_sources.py` should download from
  the CDN, never through the API.
- The parcel download dropped once (curl exit 56 at 183 MB); resume with a
  range request rather than restarting.

---

## Scope, CRS, region

- **Scope:** CABA.
- **CRS:** UTM 21S (**EPSG:32721**), derived; POSGAR 2007 / Argentina 5
  (EPSG:5347) is the national alternative. Never buffer in 4326.
- **Region:** a new macro-map region may be needed (South America holds
  Brazil's nine; Buenos Aires can join it).

## Still unknown

- ⚠️ **The taxonomy**: 385 subtypes to map, and the catch-all measured on it.
- ⚠️ **MULTICOMERCIAL and SIN IDENTIFICAR**: owner calls at the build.
- ⚠️ **The Premetro**, and station counts per line (derive from the route
  stop members, `osm-rail`).
- ⚠️ **Personal exposure**: `check_personal_exposure.py` after step 2 (no
  names in the source, so the risk is a pin on a home; the RESIDENCIAL
  exclusion covers the known case).

```brief-checks
[
  {
    "id": "buenos-aires-survey-csv-on-cdn",
    "claim": "THE BUSINESS LEG: the 2022-2024 land-use survey CSV is served by the city's CDN to a non-browser client (the CKAN API is not; see Access traps). 39.5 MB when cached",
    "kind": "http_ok",
    "url": "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-de-desarrollo-urbano/relevamiento-usos-suelo/relevamiento-usos-del-suelo-2022-2024.csv",
    "min_bytes": 1000000,
    "content_type_contains": "csv"
  },
  {
    "id": "buenos-aires-parcels-csv-on-cdn",
    "claim": "THE PLACEMENT: the Parcelas CSV (318,046 parcels, WKT polygons in WGS84) is served by the CDN; the survey joins to it at 99.8% on the normalised SMP",
    "kind": "http_ok",
    "url": "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-de-desarrollo-urbano/parcelas/parcelas_catastrales.csv",
    "min_bytes": 1000000,
    "content_type_contains": "csv"
  },
  {
    "id": "buenos-aires-osm-subte-refs",
    "claim": "OSM carries Subte lines A, B, C, D, E and H inside CABA's bbox as route=subway, 6 distinct refs, all coloured",
    "kind": "osm_route_refs",
    "bbox": [-34.71, -58.54, -34.52, -58.33],
    "routes": ["subway"],
    "expect_refs": {"subway": 6},
    "require_refs": {"subway": ["A", "B", "C", "D", "E", "H"]}
  },
  {
    "id": "buenos-aires-projected-crs",
    "claim": "Buenos Aires projects to UTM 21S (EPSG:32721)",
    "kind": "utm_zone_from_longitude",
    "lon": -58.38,
    "north": false,
    "expect": "EPSG:32721"
  }
]
```
