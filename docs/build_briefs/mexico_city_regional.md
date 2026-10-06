# Mexico City (Regional) - extension brief: Ecatepec, Nezahualcóyotl, La Paz, Naucalpan

**Drafted 2026-10-06 (staging; the owner released the next items that day to
get briefs ready for build time; builds stay paused).** Mexico City is built
and live (`app/pages/15_Mexico_City_Heatmap.py`, 169 stations). This adds the
**11 stations** of the page's own lines that lie in the State of México, all
11 now in `outputs/mexico_city/excluded_stations.csv`. Run
`python scripts/brief_check.py mexico_city_regional` before writing any code.

Read `regional-extension` (this is its first queue row), `add-city`,
`publish-city`, `docs/mexico_retrospective.md` and Mexico City's own
pipeline. Monterrey's `MUNICIPIOS` / `MUNIDS`
(`pipeline/monterrey/config.py`) is the scope pattern. The pipeline slug
stays `mexico_city`; this brief's file name only marks the extension.

## Settled before this brief

- **Marked by the owner 2026-10-04, all four municipios** ("34. yes 35. yes
  all four 36. defer until brief 37. keep out"; `docs/decisions_drafts/staging.md`,
  "Mexico City (Regional) marked"). Naucalpan's single station followed
  Anyang + Uiwang at the time; the stub rule of 2026-10-06 reopens it (owner
  call 2 below).
- **Out, the owner's call:** the Tren Suburbano and El Insurgente (commuter
  spacing) and Mexicable (a cable car). Rail stays the page's own lines.
- **The station repair has landed on master** (`DECISIONS.md`, 2026-10-04,
  "Mexico City's station repair landed"; commits 097fb3af and 39699586): the
  nine stop-only Metro stations are taken from route membership
  (`pipeline/stations.py`'s `route_stop_members`), Consulado and Candelaria
  collapse to one station each, and `check_route_stops_covered` raises if any
  stop of a drawn line is left without a station. Cuatro Caminos is now in
  `excluded_stations.csv` (200 m outside the city). Read-only confirmation
  2026-10-06: 169 kept, 11 excluded, every one of the 11 listed below.
- **The stub rule (owner, 2026-10-06):** an urban line cut to ONE station in
  its city is left out, its station kept through other lines; two or more
  stations are drawn cut.

## Stations (11)

Line membership measured 2026-10-06 from the cached route relations
(`data/mexico_city/raw/osm_routes.json`). The municipio split is staging's
probe (2026-10-04); the cache holds only the CDMX polygon, so **the build
asserts each station's municipio by point in polygon on `INEGI:MUNID`**.

| Municipio (INEGI code) | Line | Stations | Outside CDMX | Ring (0.6 mi) in CDMX |
|---|---|---|---|---|
| Ecatepec de Morelos (15033) | Línea B | Múzquiz, Ecatepec, Olímpica, Plaza Aragón, Ciudad Azteca (5) | 2.3-5.5 km | 0% each |
| Nezahualcóyotl (15058) | Línea B | Nezahualcóyotl, Impulsora, Río de Remedios (3) | 0.6-2.0 km | 13%, 0%, 0% |
| La Paz (15070) | Línea A | Los Reyes, La Paz (2) | 1.4 and 2.0 km | 0% each |
| Naucalpan de Juárez (15057) | Línea 2 | Cuatro Caminos, its terminus (1) | 0.2 km | 40% |

- **Línea B gains 8 stations, Línea A 2 (both drawn cut at two or more, as
  the stub rule allows), Línea 2 its terminus.** The cached route relations
  name 21 stops on Línea B, 10 on Línea A and 24 on Línea 2, so the extended
  map shows each of the three whole. Nearest-neighbour spacing of
  the 11: 588 m (Impulsora to Río de Remedios) to 1,920 m (Los Reyes to La
  Paz).
- **No rail refetch.** The cached station and route files already hold all 11
  (the fetch box runs to Ciudad Azteca and La Paz); step 1's route-coverage
  check already covers their stops.
- **Gate 3 stays unavailable** (`STATION_COUNT_GATE_3 = None`, the operator's
  host unreachable); the page already says so.

### What moves for storefronts already on the map (measured, CDMX only)

Over the 280,185 CDMX storefronts in `data/mexico_city/processed/businesses_clean.csv`
(135,284 in a ring today), nearest station by distance:
- **317 enter a ring for the first time and 28 change station**: Cuatro
  Caminos takes 271, Nezahualcóyotl 74. So the page's in-ring count moves even
  on the CDMX side.
- **Seven kept CDMX stations' rings already cross the city line**: Santa Marta
  31% outside, Tepalcates 23%, Canal de San Juan 19%, Villa de Aragón 17%,
  Guelatao 16%, Peñón Viejo 3%, Politécnico under 1%. The parts that fall in
  the four municipios gain storefronts; parts in any other municipio stay
  blank. **Measure at build with the municipio polygons** and say which.
- **Ecatepec's share in a ring will be low** (the owner's note, 2026-10-04):
  its five stations run along its western edge, and the municipio is 1.65
  million people (INEGI's catalogue).

## Business leg: DENUE over entidades 09 and 15

| | |
|---|---|
| **Entidad 09** | The cached `data/mexico_city/raw/denue_09_csv.zip`, 45,439,249 B, **the same size and Last-Modified (2026-05-20) as the live file on 2026-10-06**, so the cache is the current edition, 05_2026. 462,732 rows, every one `cve_ent` 09; 42 columns, `cve_mun` and `municipio` among them. Unchanged by the extension |
| **Entidad 15: TWO ZIPs (the build's downloads)** | `https://www.inegi.org.mx/contenidos/masiva/denue/denue_15_1_csv.zip`: **50,572,588 B** (listed as 48.2 MB), Last-Modified 2026-05-20, `application/x-zip-compressed` · `https://www.inegi.org.mx/contenidos/masiva/denue/denue_15_2_csv.zip`: **30,236,017 B** (listed as 28.8 MB), Last-Modified 2026-05-20. Found 2026-10-06 in INEGI's own download page (`https://www.inegi.org.mx/app/descarga/?ti=6&ag=15`), whose DENUE tab lists them as "2026/05 (1 de 2)" and "(2 de 2)", logical paths `/masiva/denue/denue_15_1` and `/masiva/denue/denue_15_2`, `_csv.zip` appended under `/contenidos`. Sizes from response headers only; **nothing downloaded** |
| **The single-ZIP URL is a soft 404** | `denue_url("15")` gives `.../denue_15_csv.zip`, which answers **HTTP 200, `text/html`, 2,263 B, "Página no encontrada"**. The fetch's magic-byte check would stop it, but the module should never build that URL for 15 |
| **Members (unmeasured)** | Expected `conjunto_de_datos/denue_inegi_15_1_.csv` and `..._15_2_.csv` on INEGI's naming, plus the dictionary near-miss in each. **Read `namelist()` at build and name the member exactly**; never take the first `.csv` |
| **Scope** | Four codes, Monterrey's shape: `MUNICIPIOS = {"033": "Ecatepec de Morelos", "058": "Nezahualcóyotl", "070": "La Paz", "057": "Naucalpan de Juárez"}`, `MUNIDS` = 15 + code. Codes checked 2026-10-06 against INEGI's municipio catalogue (`https://gaia.inegi.org.mx/wscatgeo/mgem/15`, 125 municipios; a check reference only, not a pipeline source). Step 2 asserts each code's DENUE `municipio` spelling, so a wrong code fails loudly |
| **Which part holds which municipio** | Unknown until download. Read both parts, filter on `cve_mun`, and **assert no `id` appears in both parts** (they should be disjoint) |
| **Filters and taxonomy** | Unchanged: `scian.py`, `Fijo` only, the four forbidden columns never loaded, the same carve-outs. Give any SCIAN code that appears in 15 and not in 09 a verdict from `docs/category_rules.md` |
| **Still to measure at build** | Rows, `Fijo` share and storefronts per municipio and bucket; coordinates filled; points outside their own municipio polygon (Monterrey dropped 22); blank `nom_estab`; `numero_int` rate; storefronts per station against CDMX's 818 and Monterrey's 389 |

### The module change for two ZIPs

`pipeline/countries/mexico.py` assumes one ZIP per entidad (`denue_url`,
`denue_member`). Proposed, and every built Mexican city must stay at zero
drift through it:
- A `DENUE_PARTS = {"15": ("15_1", "15_2")}` table, a `denue_urls(state_code)`
  that returns one URL per part (one for every other entidad), and a
  `denue_members(state_code)` to match. `denue_url("15")` raises, naming the
  parts.
- `pipeline/mexico_city/fetch_sources.py` downloads both parts to
  `data/mexico_city/raw/denue_15_1_csv.zip` and `denue_15_2_csv.zip` (new
  names in the shared `data/`, nothing overwritten), each checked by magic
  bytes. Step 2 reads them only when `REGIONAL` is on and never fetches.
- INEGI split entidad 15 in every edition since 2018/03, so this is a
  standing layout, not a one-off.

### Boundaries

The extension needs the four municipios' polygons. Recommended: **one
Overpass query** in `fetch_sources.py` for the `admin_level=6` relations
carrying `INEGI:MUNID` 15033, 15057, 15058 and 15070 (Monterrey's join key),
written to a new raw file, area-gated like CDMX's 1,300-1,700 km². OSM is
already credited (notice 1, OpenStreetMap). One query in flight per session;
after a 504 or 429, wait at least 60 s. The scope polygon is CDMX plus the
four; check `MEXICO_CITY_BBOX` still holds them (widen the sanity box, not
the fetch box).

## Licence, notices and personal data

- **No new licence row and no new notice.** DENUE's terms are read and
  recorded (`docs/data_sources/mexico.md`, the Mexico City, Guadalajara and
  Monterrey rows; INEGI's "Términos de Libre Uso", stored at
  `docs/licenses/inegi-terminos-libre-uso-informacion.pdf`). Notice 8 (INEGI)
  already carries the prescribed attribution, the transformation disclosure
  and non-endorsement; its city sentence gains the four municipios. Add the
  entidad 15 URLs to Mexico City's row there (provenance checks URL constants
  verbatim).
- **Privacy:** the same structural position (no registrant-name column
  loaded; INEGI withholds `raz_social` for sole traders). Re-run
  `python scripts/check_personal_exposure.py mexico_city` on the extended
  city; its entry already exists. Inspect sign names with phone-length digit
  runs or e-mail shapes by hand (Monterrey found four), and print none.
  Record the verdict in the drafts file, then `docs/privacy_verdicts.md`.

## Build order (regional-extension's steps)

1. **The city alone, at zero drift:** add `REGIONAL = False` to
   `pipeline/mexico_city/config.py`, commit it off, run
   `pipeline/drift_check.py mexico_city` through `heavy_job.py`. False must
   reproduce the repaired 169-station build byte for byte. Regional processed
   files go to `data/mexico_city/processed/regional/` from the first run.
2. The module change, then Guadalajara and Monterrey at zero drift too.
3. The downloads (owner call 1), then steps 1-3 with `REGIONAL = True`.
4. Account for every change the drift check reports: stations kept and
   excluded, storefronts per municipio and bucket, in-ring count and share.
   `excluded_stations.csv` keeps only what is left out (none, or Cuatro
   Caminos under call 2); check how `check_scope_disclosure.py` property E
   reads an empty file before relying on it.
5. The page: same file and slug, display name **"Mexico City (Regional)"**
   (`app/cities.py` `name`, `blurb`; `NAME` in config; the page's
   `render_city_nav` / `render_city_title`); macro label re-scored at 375,
   768 and 1200; page text in `docs/city_page_format.md`'s format, the
   approved Cuatro Caminos sentence revised for the new scope; the What Is
   Excluded section renamed, with a **Stations.** line and the State of
   México municipios with no station named as not covered.
6. Gates: personal exposure, `check_provenance.py` names the city OK, scope
   disclosure, `check_ring_shares.py --write`, the drafts entry. Reboot: yes.
   deploy-verify `city-added` at review time. Downstream note owed.

## Open owner calls

1. **The download (first).** `denue_15_1_csv.zip` (50,572,588 B) and
   `denue_15_2_csv.zip` (30,236,017 B), edition 05/2026, from INEGI's own
   host, plus one Overpass query for the four municipio boundaries.
   **Recommend yes**: the brief now names them, as the 2026-10-04 call asked.
   If INEGI publishes the November edition first, fetch 15 from the 05/2026
   edition's dated archive path (INEGI keeps past editions under dated
   folders) so 09 and 15 share one edition and the city alone stays at zero
   drift; re-pulling both is the alternative, and moves the live page's
   numbers.
2. **Naucalpan under the stub rule.** Two readings:
   - **(a) Keep it, recommended.** The rule is about a LINE cut to one
     station; Línea 2 has 24 stations on the regional map, and
     Cuatro Caminos is its real terminus 200 m past the city line, so no
     one-station fragment is drawn. It also matches the owner's 2026-10-04
     "all four". Cuatro Caminos' ring is 40% in CDMX and takes 271 CDMX
     storefronts. Tradeoff: all of Naucalpan (834,000 people) enters the
     page's storefront total with one ring, so it lowers the in-ring share.
     The page says so.
   - **(b) Leave Naucalpan out entirely.** If the rule is read per
     municipio, Línea 2 is cut to one station there. Cuatro Caminos has no
     other line (Mexicable and the Suburbano stay out), so nothing keeps
     its station: it stays in `excluded_stations.csv` as today, and the
     extension is three municipios and 10 stations. Tradeoff: simpler and
     cheaper, but Línea 2 stops one station short of its terminus, a large
     transfer hub.
3. **Boundaries from OSM** (recommended, keyed on `INEGI:MUNID` as
   Monterrey) rather than INEGI's geostatistical framework, which would be a
   new source needing its own licence read.

```brief-checks
[
  {
    "id": "mexico-regional-denue-15-listing",
    "claim": "INEGI's mass-download listing for entidad 15 counts 41 DENUE entries (2026-10-06), the newest the two-part 05/2026 edition (denue_15_1 48.2 MB, denue_15_2 28.8 MB). A change means a new edition or a new layout: re-read the listing before downloading",
    "kind": "http_contains",
    "url": "https://www.inegi.org.mx/app/api/descarga/descarga/descargamasiva/lista/totales?tinfo=6&ag=15&prog=0&cc=0&subtema=0&anio=0&formato=0&datosAbiertos=3&textoBuscar=&ingles=0",
    "present": ["\"clasificacion\":\"DENUE\",\"total\":\"41\""]
  },
  {
    "id": "mexico-regional-denue-15-single-zip-soft-404",
    "claim": "Entidad 15 has no single DENUE ZIP: denue_15_csv.zip answers HTTP 200 with INEGI's not-found page, so the country module must build two part URLs for 15, never denue_url('15')",
    "kind": "http_contains",
    "url": "https://www.inegi.org.mx/contenidos/masiva/denue/denue_15_csv.zip",
    "present": ["no encontrada"]
  },
  {
    "id": "mexico-regional-download-page-denue-tab",
    "claim": "INEGI's download page still carries the DENUE tab whose listing names denue_15_1_csv.zip and denue_15_2_csv.zip (the names arrive by the page's own listing call, not in the HTML)",
    "kind": "http_contains",
    "url": "https://www.inegi.org.mx/app/descarga/?ti=6&ag=15",
    "present": ["data-tinfo=\"6\"", "CargarTablaDescarga('denue')", "Descarga masiva"]
  },
  {
    "id": "mexico-regional-municipio-codes",
    "claim": "INEGI's catalogue gives the four municipios the codes the scope keys on: 033 Ecatepec de Morelos, 058 Nezahualcóyotl, 070 La Paz, 057 Naucalpan de Juárez",
    "kind": "http_contains",
    "url": "https://gaia.inegi.org.mx/wscatgeo/mgem/15",
    "present": [
      "\"cvegeo\":\"15033\",\"cve_agee\":\"15\",\"cve_agem\":\"033\",\"nom_agem\":\"Ecatepec de Morelos\"",
      "\"cvegeo\":\"15058\",\"cve_agee\":\"15\",\"cve_agem\":\"058\",\"nom_agem\":\"Nezahualcóyotl\"",
      "\"cvegeo\":\"15070\",\"cve_agee\":\"15\",\"cve_agem\":\"070\",\"nom_agem\":\"La Paz\"",
      "\"cvegeo\":\"15057\",\"cve_agee\":\"15\",\"cve_agem\":\"057\",\"nom_agem\":\"Naucalpan de Juárez\""
    ]
  },
  {
    "id": "mexico-regional-projected-crs",
    "claim": "The city and the four municipios project to UTM 14N (EPSG:32614), the city's existing CRS; metro mode, regional scope",
    "kind": "utm_zone_from_longitude",
    "lon": -99.13,
    "expect": "EPSG:32614",
    "mode": "metro",
    "scope": "regional",
    "crs": "EPSG:32614"
  }
]
```
