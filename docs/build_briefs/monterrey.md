# Monterrey (Regional) — build brief

**Step 0 measured 2026-09-27** (the second-city screen; scratch in
`second_cities/monterrey/`). Run `python scripts/brief_check.py monterrey`
before writing any code. **Mexico's third city**, on the national modules
Mexico City and Guadalajara built: DENUE, `scian.py`, and INEGI's licence and
notice. Copy **Guadalajara**, the regional precedent and the closest shape.

**Why it was never built:** Monterrey was recorded as "a real negative" on
2026-09-22 for one reason. Nuevo León publishes no Metrorrey data: no feed, and
no reachable operator or state GIS host. That negative stopped mattering when
OpenStreetMap was approved as a rail source (`osm-rail`), and Mexico City and
Guadalajara were built on it.

**✅ Decided by the owner, 2026-09-27:**
1. **OSM is the rail ground** ("OSM ok").
2. **Scope: "Monterrey (Regional)"** over the four municipios, with 38
   stations ("regional scope yes").
3. **Línea 3 is drawn in the operator's RED** ("use operator's red"), not
   OSM's orange.
   - Take the hex from the operator's 2026-05-08 vector map at build (the
     screen had no PDF library to read it).
   - Keep Línea 1's and Línea 2's colours checked against the same map. The
     map's orange belongs to Línea 6, which is not drawn.
   - `check_map_markup.py`'s contrast parts still apply.

## Owner calls, as put (✅ decided above)
1. **OSM as the rail ground.** The grounds are the same as for Mexico City's
   per-city exception: there is no agency feed, `metrorrey.gob.mx` does not
   resolve, the state GIS (`mapas.nl.gob.mx`) times out, and `datos.nl.gob.mx`
   is a brochure site. Two Overpass mirrors agree, and the operator's own map
   matches the station counts exactly (19 / 13 / 9).
2. **Scope: "Monterrey (Regional)"** = Monterrey, San Nicolás de los Garza,
   Guadalupe and General Escobedo, **38 stations**.
   - A Monterrey-only build cuts **Línea 2 to 8 of 13 stations (62%)**, below
     Rennes' 11 of 15 (73%), the lowest kept commune-only. It would also lose
     the northern leg, Universidad included.
   - These four are exactly the municipios any 0.6-mile ring reaches: Los
     Ángeles is 39% in San Nicolás, Niños Héroes 33%, Sendero 41%.
   - Dropping Escobedo loses one terminal station (Sendero).
3. **Línea 3's colour.** OSM says `#FF8000` (orange); the operator's 2026-05
   map draws Línea 3 **red** and uses orange for Línea 6. Take the operator's
   (the hex needs extracting from the PDF), or decide.

---

## The one-line summary

**58,587 storefronts in all three buckets from DENUE 05_2026, coordinates on
100% of rows, around 38 Metrorrey stations on three lines. It is the same
register, edition, licence and privacy position as the two built Mexican
cities. Only the owner's three calls stand before the build.**

## Business leg: DENUE, Nuevo León (state 19)

| | |
|---|---|
| **File** | `https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip`: **21,475,515 B**, Last-Modified 2026-05-20, edition **"DENUE 05_2026"** (the same edition as CDMX's and Guadalajara's cached files). Member `conjunto_de_datos/denue_inegi_19_.csv`, **latin-1** |
| **Columns** | the same 42 as CDMX's, so `USECOLS` and the four forbidden columns carry over |
| **Scope rows** | 211,349 units statewide. The four municipios hold 117,276 (Monterrey 62,758 · Guadalupe 22,780 · San Nicolás 17,165 · Escobedo 14,573); 114,007 fixed (`Fijo`, 97.2%) |
| **Storefronts** | **58,587 = Retail 37,869 · Food 12,639 · Personal 8,079** (Monterrey 29,237 · Guadalupe 11,852 · San Nicolás 8,961 · Escobedo 8,537) |
| **Non-storefront share of fixed premises** | **48.6%** (Guadalajara 39.1%, CDMX 35.9%). Repair (SCIAN 811, 9,593) is most of the difference, which fits an industrial city. Not a defect |
| **Carve-outs** | Guadalajara's all apply: 469 (16), 812410 parking (482), 721 hotels (264), 811 repair (9,593), 813 associations (2,452), plus the `Fijo` filter. No codes fall in NAICS 44/45 |
| **Coordinates** | **100.000% filled, no zeros.** 99.92% of points fall inside their own municipio's OSM polygon |
| **Join key** | OSM's `INEGI:MUNID` (e.g. 19039) equals DENUE's `cve_ent` + `cve_mun`: join on the code, not the name |
| **Against OSM** | food **13.5×** (Guadalajara 13.8×); total 18.4× (Guadalajara 14.9×). Thin OSM coverage, not an inflated register |
| **Density** | **14,780 storefronts within 0.6 mi of the 38 stations, 389 per station.** The same method reproduces Guadalajara's 659; CDMX is 818 |
| **Trade name** | `nom_estab` blank on 42 rows (0.07%) |

## Rail: Metrorrey, from OSM (`network=Metrorrey`, all `route=subway`)

| Line | ref | Relations | Stations | Monterrey | San Nicolás | Guadalupe | Escobedo |
|---|---|---|---|---|---|---|---|
| Línea 1 | 1 | 7890221 / 7890222 | 19 | 16 | – | 3 | – |
| Línea 2 | 2 | 3403903 / 7890220 | 13 | 8 | 4 | – | 1 (Sendero) |
| Línea 3 | 3 | 12380644 / 12380647 | 9 | 8 | 1 | – | – |
| **Collapsed by name** | | | **38** | 29 | 5 | 3 | 1 |

- **Gate 3 passes**: the operator's map
  (`https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/Sistema%20de%20Transporte%20Colectivo%20%28Metrorrey%29/Repositorios/20260508_mapa_red_metrorrey.pdf`,
  2026-05-08) names exactly 19 / 13 / 9. It is read for the check only, never
  republished. Spacing: minimum 519 m, median 788 m.
- **Líneas 4 and 6 are NOT carrying passengers.** The operator's map says "en
  construcción", the state homepage (to 2026-09-26) still says Línea 6 is
  coming "próximamente", and OSM has no route relations for either. Do not
  draw them. The monorail check below fails loudly the day one appears.
- **Not rail**: Ecovía (BRT), TransMetro and MetroEnlace (buses).
- **Boundaries** (`admin_level=6`): Monterrey 5606060, San Nicolás 5606272,
  Guadalupe 5605824, Escobedo 5605805. Union 650.7 km² in EPSG:32614.

### OSM traps the build must handle
- 🚨 **11 unbuilt Línea 4/6 monorail stations are tagged `railway=station` +
  `construction=yes`.** A tag whitelist in the CDMX style would admit them.
  Build stations from **route membership**, and add a raising check on
  `construction=yes`.
- **Members come in mixed types**: 36 are `railway=station` nodes, but
  Cuauhtémoc and General Anaya are members only as `railway=stop` stop
  positions.
- **Accent-fold before collapsing names**: "Félix U. Gomez" (L1) and "Félix
  U. Gómez" (L3) are one station. Without folding, the count is 39.
- **Correct public names**: "Ruiz Cortinez" → **Ruiz Cortines**; "Niños
  Heroes" → **Niños Héroes**.
- **"Parque Fundidora" now names a Línea 6 station.** The Línea 1 station is
  **Arena Monterrey**.

## Licence and notices
- DENUE: the metadata declares INEGI's "Términos de Libre Uso", **already
  read** (`docs/data_sources.md`). **No new notice**: INEGI notice 8 covers it
  and already requires disclosing transformations. The page states the
  four-municipio scope and the `Fijo` and bucket filters.
- OpenStreetMap rail and boundaries: ODbL, the OpenStreetMap notice 1.
- Add a `data_sources.md` row for Monterrey (provenance) at build. The nl.gob.mx
  site terms are unread; the PDF is not republished.

## Privacy (same position as CDMX and Guadalajara)
- No registrant-name column is loaded, and INEGI withholds `raz_social` for
  sole traders. The four forbidden columns are never read.
- `check_personal_exposure.py` needs a `monterrey` entry (raw, trade, owner
  and address all `None`), with the residence gap recorded as for the other
  two.
- The person-name heuristic flags 33.8%, the known Spanish misfire (CDMX 32.2%).
- **Inspect by hand at build**: 1 e-mail-shaped and 3 phone-length digit runs
  inside sign names. None printed.
- Separate, for the Guadalajara page: **11 published names there carry
  phone-length digit runs**, unchecked. A cleanup item.

## CRS
**EPSG:32614** (UTM 14N): the centre is at −100.31, and the extent (−100.47
to −100.12) lies inside zone 14.

## Still unknown
- Línea 3's exact red, from the operator's PDF at build.
- Líneas 4 and 6 opening dates.
- A Mobility Database re-check (its negative is from 2026-09-22).

```brief-checks
[
  {
    "id": "monterrey-denue-19",
    "claim": "DENUE's Nuevo León bulk file is live at INEGI's masiva path (edition 05_2026, ~21.5 MB) - the business leg",
    "kind": "http_ok",
    "url": "https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip",
    "min_bytes": 20000000
  },
  {
    "id": "monterrey-metrorrey-refs",
    "claim": "Metrorrey is 6 subway relations carrying refs 1, 2 and 3 in the Monterrey bbox, and NO monorail relation - a monorail relation appearing means Linea 4 or 6 may have opened: re-check before drawing",
    "kind": "osm_route_refs",
    "bbox": [25.55, -100.55, 25.90, -100.05],
    "routes": ["subway", "light_rail", "monorail"],
    "expect_relations": {"subway": 6, "monorail": 0},
    "expect_refs": {"subway": 3},
    "require_refs": {"subway": ["1", "2", "3"]}
  },
  {
    "id": "monterrey-operator-map",
    "claim": "The operator's 2026-05-08 network map (gate 3: 19 / 13 / 9 stations) is still published",
    "kind": "http_ok",
    "url": "https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/Sistema%20de%20Transporte%20Colectivo%20%28Metrorrey%29/Repositorios/20260508_mapa_red_metrorrey.pdf",
    "min_bytes": 500000
  },
  {
    "id": "monterrey-inegi-terms",
    "claim": "INEGI's free-use terms page still says 'Libre Uso' - the licence read for DENUE",
    "kind": "http_contains",
    "url": "https://www.inegi.org.mx/inegi/terminos.html",
    "present": ["Libre Uso"]
  },
  {
    "id": "monterrey-utm",
    "claim": "Monterrey projects in EPSG:32614 (UTM 14N)",
    "kind": "utm_zone_from_longitude",
    "lon": -100.31,
    "expect": "EPSG:32614"
  }
]
```
