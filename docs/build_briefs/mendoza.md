# Mendoza — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band A,
owner-approved 2026-10-03** ("mendoza can be built": the capital alone, seven
stations). Run `python scripts/brief_check.py mendoza` before writing any
code. The trail: `docs/decisions_drafts/staging.md`, 2026-10-03 "Mendoza
approved for a build: the capital alone, seven stations (owner)", "Mendoza's
placement measured: every business has a point; Band A", and the licence
read in "Seven licence reads for the sweep's first group". Argentina's second
city: Buenos Aires (`docs/build_briefs/buenos-aires.md`) is the country
precedent, but its business source and placement are nothing alike, so
read `docs/spain_retrospective.md`'s warning about familiar-looking countries
before reusing any of its code. Skills: `add-city`, `scaffold-city`,
`osm-rail`, `premises-taxonomy`, `publish-city`. **Not** `tram-city`: the
Metrotranvía passes the light-rail test.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot color) | **`light_rail`** | Converted railway (ex-San Martín mainline), 7 minutes at peak and 11-12 off-peak, stops about 700 m apart on average: passes the light-rail test (`docs/tram_city_list.md`) |
| **`coverage`** (macro dot fill) | **`full`** | All three buckets. If personal services comes out thin after the taxonomy (331 at the screen), `narrowed` "Personal services thin" is the owner's call (Kansas City's and New Orleans's precedent) |
| **Scope** | **Ciudad de Mendoza, the capital department alone** (owner, 2026-10-03) | No neighboring department publishes a business register |
| **Stations in scope** | **7 of the line's 25** | Pedro Molina, Belgrano, Mendoza, Suipacha, Moldes, Lugones, Rubilar (the city's own stop list) |
| **Line drawn** | the whole Metrotranvía, Gutiérrez (Maipú) to Avellaneda (Las Heras), with the 18 stations outside listed (**owner, 2026-10-03: "yes draw mendoza line to end"**) | Florence's T1 and Göteborg's 4 and 12 precedent (tram-city calls 17 and 21): the line is drawn to its end, the stations outside get no ring and are listed below the map. **The owner's call at build** |
| **Rings** | by the spacing rule on the 7 stations in scope | Mean gap about 700 m over the whole line; measure the median on the capital's 7 (`docs/ring_rules.md`) |
| **Region** | `"South America"` | Buenos Aires's region |

---

## The one-line summary

**The capital's own list of 8,309 open commercial accounts, every one with a
point, under CC BY 4.0; seven Metrotranvía stations. The work is the
taxonomy (one business, many activity rows) and the name rule.**

| | **Mendoza** |
|---|---|
| Rail | **Metrotranvía de Mendoza** (Sociedad de Transporte de Mendoza), one line, lines 100/101, about 17 km, 25 stations |
| Stations in scope | **7** in the Ciudad de Mendoza; Godoy Cruz 7 plus Parque TIC, Las Heras 5, Maipú 5 |
| Projected CRS | **EPSG:32719** (UTM 19S, 68.84° W) |
| Register | "Listado Comercios por Actividad 2025" (Municipalidad de la Ciudad de Mendoza), 8,309 businesses, 41,179 activity rows, CC BY 4.0 |

---

## Business leg — "Listado Comercios por Actividad 2025"

| | |
|---|---|
| Publisher | Municipalidad de la Ciudad de Mendoza, CKAN `listado-comercios-por-actividad-2025` on `datos.ciudaddemendoza.gob.ar` (organization: Coordinación de Estacionamiento Medido), "Listado Comercios por Actividad a Junio 2025" |
| Resources | CSV 7,905,521 B, KMZ 1,776,091 B, **JSON `comercios_limpio.json` 12,239,392 B**; none is datastore-backed |
| **The build's source** | **the JSON**, cached at `data/mendoza/raw/comercios_limpio.json` (owner-approved download 2026-10-03, sha256 `ca6af57c5625eb9868a77d6d5bd7e112b9408a33c74de7da00cb9986b707fd17`, beside it `comercios_limpio.meta.json`). It carries the points and the activity rows together |
| Rows | **41,179 activity rows for 8,309 businesses** (`comercio_id`; at most 30 rows per business) |
| JSON fields | `comercio_id, nombre_fantasia, calle, numero, tipo_actividad, desc_full, fecha_inicio, x, y` |
| CSV-only fields | `estado_cuenta`, `baja_fecha`, `desc_breve`, `desc_ampliada`, `piso`, `depto`, `local` and the rest; **the JSON has no `desc_breve`** |
| Currency | **Passes.** In the CSV, `estado_cuenta` = ALTA on all 41,179 rows and `baja_fecha` empty on all: a snapshot of open accounts at June 2025 (newest `fecha_inicio` 2025-07-08; 652 openings in 2025). The JSON carries no status field, so the currency claim rests on the CSV read at the screen. **The page states the data date, June 2025** |
| Points | **8,309 of 8,309 (100%)** carry a nonzero `x`/`y`, one point per business (no business has two). 6,161 distinct points, so galleries and shopping centers stack |
| Fetch | `fetch_sources.py` downloads the JSON from the resource URL `https://datos.ciudaddemendoza.gob.ar/dataset/df39f71e-0d7e-40e5-a475-c31f098fab93/resource/94e44b27-951e-4f38-a5c4-17eec535a3fe/download/comercios_limpio.json` and checks it against the cached sha256; a step never fetches |

### Placement — x/y in Gauss-Krüger zone 2

- **`x`, `y` are POSGAR / Argentina zone 2 Gauss-Krüger.** EPSG:5344 (POSGAR
  2007) and EPSG:22182 (POSGAR 94) agree within 0.0001 degrees; the median
  point falls at the city center and all 8,309 sit inside a rough box around
  the capital (`mza_placement.py`, the staging scratchpad). Read with
  EPSG:5344, the current frame, and say so in config.
- **Check every point against the department's own boundary** at build, not
  the rough box. Candidate: the portal's `seccionales-ciudaddemendoza`
  dataset (the city's seccionales, whose union is the department). Its
  format and licence are unverified: confirm both, and give it its own row
  in `docs/data_sources/argentina.md`. A different boundary source goes to
  the owner first.
- No address join is needed.

### Classification — RAM, one business with many activity rows

- **`tipo_actividad` has three levels**: RAM (rama, the business type),
  RUB (fee items, mostly signage and motor counts: not a classifier) and
  SUB. In the JSON: RUB 20,464, SUB 12,311, **RAM 8,274**, blank 130.
  **8,158 businesses carry a RAM row**; 151 carry none. Key on RAM.
- **The JSON names a rama by `desc_full` only** (418 distinct RAM values).
  The screen's counts keyed on the CSV's `desc_breve` (about 450 values), so
  the taxonomy is written against `desc_full` and the counts re-measured.
- **The screen's rule for a business's bucket** (`mza_buckets.py`, a rough
  map for counts, not a taxonomy): map each of the business's RAM rows to a
  bucket, then take the first in the order Food service, Retail, Personal
  services, catch-all, out. So one in-scope rama puts the business on the
  map. At that level: **Retail 3,350 · Food service 721 · Personal services
  331** · catch-all 601 · out 3,155 · no RAM row 151.
- **The rule itself is the build's, from the `premises-taxonomy` skill's
  measurement**: measure the catch-all share with `brief_check.py`'s
  `taxonomy_catchall` kind first, decide whether "any in-scope rama" or "the
  first RAM row" fits, and decide what a business with no RAM row gets (its
  SUB rows, or out). Record the rule and its counts in the drafts file.
- Catch-alls (mostly offices, likely out): ESCRITORIO 192, ADMINISTRAC 170,
  EMPRESA 54, ACT.ADMIN. 39, ESCAPARATE 38, DEPOSITO 28, REPRESENTAC. 21.
- Largest out: CONSULTORIO 509 (doctors' offices), CASA DPTOS 279 (rental
  flats), ESTACIONAM. 210, AG.VIAJES 134, HOTEL 89, GIMNASIO 74. Check each
  against `docs/category_rules.md`.
- Personal services is thin but real: PELUQUERIA 137, PELUQ.DAMAS 44,
  INST.BELLEZA 57, S.BELLEZA 20, TATUPIERCI 14, laundries 36.

### ⚠️ Privacy — sole traders' own names in `nombre_fantasia`

- **`nombre_fantasia` is filled on every business, and on some rows it is a
  sole trader's own name, surname first** ("SURNAME, GIVEN-NAME" form). The
  screen measured no share.
- **Vancouver's rule of 2026-09-21 applies**: a name that reads as a person's
  own, printed surname first, shows the business type instead; a name with
  "&" or a digit never counts. A list of names withheld holds keys
  (`pipeline/name_keys.py`), never the names.
- Run `python scripts/check_personal_exposure.py mendoza` after step 2,
  record the verdict in the drafts file and `docs/privacy_verdicts.md`.
  CONSULTORIO is out anyway.
- Ley 25.326 (Argentina's data-protection law) is outside the licence: the
  name rule and the privacy check carry it.
- **Never print a row** from this file. The screen printed one by accident,
  and its trade name was a person's name (drafts, 2026-10-03). Field names
  and counts only.

---

## Rail — the Metrotranvía

| | |
|---|---|
| Line | One line, Gutiérrez (Maipú) to Avellaneda (Las Heras), about 17 km, **25 stations** (15 in 2012, 9 more to Las Heras on 2019-05-06, Parque TIC on 2021-05-29: es.wikipedia's line diagram, secondary) |
| In scope | **Ciudad de Mendoza 7**: Pedro Molina, Belgrano, Mendoza, Suipacha, Moldes, Lugones, Rubilar |
| Outside | Godoy Cruz 7 (25 de Mayo, Pellegrini, San Martín, Mitre/Godoy Cruz, Progreso, Independencia, 9 de Julio) plus Parque TIC; Las Heras 5 (José María Godoy, Patricias Mendocinas, Roca/Tamarindos, Burgos, Avellaneda); Maipú 5 (Luzuriaga, Piedra Buena, Alta Italia, Maza, Gutiérrez) |
| Border stops | **Pedro Molina, 25 de Mayo, José María Godoy**: decide each by the polygon, not by the city's list |
| Frequency | **every 7 minutes at peak** (Cadena 3, 2026-03-06, 16 two-car sets); **11-12 off-peak** (the operator's 2024 timetable). Weekdays about 05:15-00:35, Saturdays to about 22:15, Sundays about 06:00-21:40 |
| Not open | the south branch, Pellegrini to Luján (14 stops; the Benegas section "expected October" in the press) and the north extension to the airport (4 stops, end-2026). Neither reaches the capital; re-count the whole line at build |

- **Rail source: OpenStreetMap through `osm-rail`** (not queried for this
  brief). No GTFS was found at the screen. One Overpass query for the city,
  never parallel; after a 504 or 429 wait at least 60 s. Read whether OSM
  tags the line `route=light_rail` or `route=tram`; `mode` stays
  `light_rail` either way, on the test.
- **The city's stop list** (`paradas-metrotranvia`, Dirección de Tránsito,
  CC BY 4.0, 46 platforms, fields `OID_, nombre, departamen` only, 2021
  vintage re-uploaded 2024, no Parque TIC) names each stop's department:
  14 platforms in the Ciudad de Mendoza, so 7 stations. Use it as the scope
  cross-check; it carries no coordinates (the KMZ, 5,953 B, does). If the
  build draws any point from it, it needs its own source row and credit.
- **Gate 3**: the operator's own count of the whole line (Sociedad de
  Transporte de Mendoza or the province's Metrotranvía page), read for the
  count only, in `OPERATOR_STATION_COUNTS` and `OPERATOR_COUNTS_SOURCE`.
  es.wikipedia's diagram is the secondary fallback, named as secondary.
  Not looked up for this brief.
- Buses and the other departments' stations are not drawn; the page says so.
- Every drawn line gets its permanent label ("Metrotranvía") and a legend
  entry. No operator logo.

---

## Licence — CC BY 4.0, read (`licence-read` 2026-10-03)

- **Permitted with conditions**: CC BY 4.0 at every level (the dataset's
  `license_id` CC-BY-4.0, the portal and the resources agree).
- **The page must show** (CC BY 4.0 section 3(a)):
  - credit to the **Municipalidad de la Ciudad de Mendoza**, with the
    dataset title "Listado Comercios por Actividad 2025" and its page,
    `https://datos.ciudaddemendoza.gob.ar/dataset/listado-comercios-por-actividad-2025`;
  - the licence link, `https://creativecommons.org/licenses/by/4.0/`;
  - **a statement of the modifications**: filtered to storefront
    businesses, grouped into three categories, reprojected from the
    Gauss-Krüger grid, and names that read as a person's own replaced by the
    business type;
  - **no suggestion of endorsement** by the Municipalidad, and no city logo.
- No wording is prescribed. The build drafts the credit as one numbered
  notice; a sentence the template does not cover is a proposal, flagged in
  the drafts file and at review time.
- Needs a row in `docs/data_sources/argentina.md` (the boundary source and,
  if used, the stop list too) and the notice in the published-notices list.
  Honor any removal request (the removal rule).

---

## Scope, CRS, region

- **Scope:** the Ciudad de Mendoza (capital department), `SCOPE = "city"`.
  The page title is "Mendoza"; the scope bullet names the capital department
  and says the line runs on into Godoy Cruz, Las Heras and Maipú.
- **CRS:** UTM 19S, **EPSG:32719**, derived from 68.84° W. The register is
  read in EPSG:5344 and projected; never buffer in 4326.
- **Region:** `"South America"`, country `"Argentina"`.

## Downstream

Per `docs/session_roles.md`, "Downstream sessions": the build records in its
drafts file, for each notice (the CC BY credit, and the stop list's if used),
**card face or caption only**, read from the licence's own words on where
attribution must appear, and **any open terms question**, so the pushing
session can pass both to Visuals and Analytics with the new city.

## Still unknown

- ⚠️ **The taxonomy** on `desc_full`, its catch-all share, and the bucket
  rule for a business with several ramas.
- ⚠️ **The share of trade names that are a person's own**, and the privacy
  verdict.
- ⚠️ **The department boundary source** and its licence; the three border
  stops.
- ⚠️ **The operator's whole-line station count** for gate 3, and how OSM
  tags and collapses the line.
- ⚠️ **The ring size**: the median gap among the 7 capital stations.

```brief-checks
[
  {
    "id": "mendoza-register-package",
    "claim": "THE BUSINESS LEG: the capital's 'Listado Comercios por Actividad 2025' package is CC-BY-4.0 and still lists the JSON resource the build reads (comercios_limpio.json, resource 94e44b27-...), which is not datastore-backed",
    "kind": "http_contains",
    "url": "https://datos.ciudaddemendoza.gob.ar/api/3/action/package_show?id=listado-comercios-por-actividad-2025",
    "present": ["CC-BY-4.0", "comercios_limpio.json", "94e44b27-951e-4f38-a5c4-17eec535a3fe", "\"datastore_active\": false"]
  },
  {
    "id": "mendoza-stop-list-rows",
    "claim": "The city's Metrotranvía stop list (paradas-metrotranvia, datastore resource b6fd7ea0-...) holds 46 platforms",
    "kind": "ckan_rows",
    "domain": "datos.ciudaddemendoza.gob.ar",
    "resource_id": "b6fd7ea0-b6c7-430e-a329-91701565d5f6",
    "expect": 46
  },
  {
    "id": "mendoza-stop-list-fields",
    "claim": "The stop list names each stop and its department (nombre, departamen) and carries no coordinate columns",
    "kind": "ckan_fields",
    "domain": "datos.ciudaddemendoza.gob.ar",
    "resource_id": "b6fd7ea0-b6c7-430e-a329-91701565d5f6",
    "present": ["nombre", "departamen"],
    "absent": ["lat", "lon", "x", "y", "latitud", "longitud"]
  },
  {
    "id": "mendoza-capital-platforms",
    "claim": "14 of the stop list's platforms are in the Ciudad de Mendoza, so 7 stations in scope",
    "kind": "http_contains",
    "url": "https://datos.ciudaddemendoza.gob.ar/api/3/action/datastore_search?resource_id=b6fd7ea0-b6c7-430e-a329-91701565d5f6&limit=1&filters=%7B%22departamen%22%3A%22Ciudad%20de%20Mendoza%22%7D",
    "present": ["\"total\": 14"]
  },
  {
    "id": "mendoza-projected-crs",
    "claim": "Mendoza projects to UTM 19S (EPSG:32719); light rail, full coverage, the capital alone",
    "kind": "utm_zone_from_longitude",
    "lon": -68.84,
    "north": false,
    "expect": "EPSG:32719",
    "mode": "light_rail",
    "coverage": "full",
    "scope": "city",
    "crs": "EPSG:32719",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
