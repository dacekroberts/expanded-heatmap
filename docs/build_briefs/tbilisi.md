# Tbilisi - build brief

**Step 0 measured 2026-10-02** (`add-country` for Georgia, same day:
[`../georgia_step0_endpoints.md`](../georgia_step0_endpoints.md), which holds
every endpoint, trap and the country answers). Run
`python scripts/brief_check.py tbilisi` before writing any code.

**✅ Decided by the owner, 2026-10-01** (`docs/decisions_drafts/staging.md`,
"Tbilisi moves from C to B"): (1) Geostat's register is accepted **with the
undercount disclosed**: it lists enterprises, not premises, so a chain appears
once; (2) **individual entrepreneurs are unnamed dots, category only**
(Taichung's precedent); (3) **personal ID columns are dropped at fetch**;
(4) Geostat is **permitted with attribution** (licence read, same day).
Open items below that ask these questions are answered.

---

## The one-line summary

**One keyless national API, filtered to the FACTUAL address in Tbilisi:
63,511 active entities, 14,806 storefronts after the standing exclusions,
12,036 (81.3%) at a real coordinate.** Three buckets, 64% of them individual
entrepreneurs. Rail from OSM: 2 lines, 23 stations, the operator's count.
About **316 storefronts per station within 0.6 mi** (placeholders removed),
which would rank near the top of the project.

---

## Business leg - Geostat's Statistical Business Register

| | |
|---|---|
| **API** | `https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&limit=10000&page=<1..7>&lang=en` |
| **Size** | `total` **63,511**, 7 pages of 10,000; ~16.7 MB of JSON per page, ~106 MB in all. Keyless, no CAPTCHA |
| **Filter** | `factualAddressRegion=11` (The city of Tbilisi, FACTUAL address; `legalAddressRegion` would map registered offices) and `isActive=true`. Both verified against a nonsense value (`total` 0) |
| **As of** | Live: `Reg_Date` max **2026-08-31**, `Init_Reg_date` max 2026-08-25. Record the pull date as the source date; `Change` is empty on every row |
| **Cadence** | Continuous (an API over the live register). "Active" is assessed from tax declarations, so new businesses lag (below) |
| **Rate limit** | 50 requests per window; HTTP 429 with `retryAfter`. Sleep between pages |
| **Encoding** | UTF-8 JSON. Names in Georgian script |

**Columns to KEEP** (non-personal): `Stat_ID` (Geostat's own statistical id,
not a personal number), `Legal_Form_ID`, `Legal_Form`, `Ownership_Type`,
`Region_Code2`, `City_Code2`, `City_name2` (district), `Activity_2_Code`,
`Activity_2_Name`, `ISActive`, `Zoma` (size class), **`X` = latitude**,
**`Y` = longitude**, `Init_Reg_date`, `Reg_Date`; and `Full_Name` **only for
rows whose `Legal_Form_ID` is not 30**.

**Columns that hold PERSONAL DATA and must be dropped in memory before
anything is written** (the API has no column selection, so the download
boundary cannot omit them; step 2 asserts their absence):
`Legal_Code` and `Personal_no` (for an individual entrepreneur, the 11-digit
personal number), `Full_Name` on legal-form-30 rows (the person's name),
`Head`, `Head_PN`, `Partner`, `Partner_PN` (people and their personal
numbers), `mob`, `Email`, `web`, `Address` (legal address: for an individual
entrepreneur usually a residence) and `Address2` (factual address string; the
coordinate is what places the pin).

**The column that identifies an individual entrepreneur**: `Legal_Form_ID`
**30** (`Legal_Form` = "Individual Entreprises", sic; `/api/legal-forms` gives
`Stat_ID_Type` 2, a natural person). Never call `/api/representatives`,
`/partners`, `/partners-vw`, `/full-name-web` or `/legal-unit-web`.

### Composition (2026-10-02)

Individual entrepreneurs 31,854 (50.2%) · LLCs 29,784 · non-commercial legal
persons 1,011 · joint-stock 446 · others under 200. Top divisions: 47 retail
14,493 · 46 wholesale 6,445 · 62 IT 3,332 · 68 real estate 3,298 · 45 motor
vehicles 2,762 · 41 construction 2,417 · 43 1,985 · 49 land transport 1,883 ·
53 couriers 1,873 · **56 food 1,628** · 85 education 1,392 · **96 personal
1,374**. The screen's three figures reproduce exactly.

## Taxonomy - NACE Rev. 2 (NCG 006-2016), keyed at the national leaf

`Activity_2_Code` is NACE Rev. 2 with a national fifth digit (`47.59.2`),
single-valued. **Never key on `Activity_Code`**: it is the old Rev. 1.1-shaped
code. Model the module on `pipeline/taxonomies/france_naf.py` (divisions 47 /
56 / 96, the same standing exclusions), with labels from `Activity_2_Name`
(British spelling in the source; American English in bucket labels).

| Bucket | Division rows | Standing exclusions (`docs/category_rules.md`) | **Kept** | Individual entrepreneurs | With coordinates | On a placeholder | **Real coordinate** |
|---|---|---|---|---|---|---|---|
| Retail | 14,493 | market stalls 47.81/47.82/47.89 **1,833**; nonstore 47.91 355, 47.99 111 | **12,194** | 8,144 (66.8%) | 10,998 | 1,105 | **9,893** |
| Food service | 1,628 | contract catering and canteens 56.29 195; event catering 56.21 83; group-only `56.2` 7 | **1,343** | 530 (39.5%) | 1,190 | 112 | **1,078** |
| Personal services | 1,374 | funeral 96.03 25; catch-all 96.09 80 (R2) | **1,269** | 855 (67.4%) | 1,143 | 78 | **1,065** |
| **Total** | 17,495 | 2,689 | **14,806** | 9,529 (64.4%) | 13,331 (90.0%) | 1,295 | **12,036 (81.3%)** |

- **Kept leaf codes**: 52 (47: 47, 56: 2, 96: 3). Largest: 47.11.0
  non-specialised with food 2,176 · 47.71.0 clothing 1,602 · 56.10.0
  restaurants 1,220 · 96.02.0 hairdressing 1,062 · 47.19.0 824 · 47.21.0
  fruit and vegetables 707 · 47.79.4 second-hand 627 · 47.52.0 hardware 577.
- **Personal services is three codes**: hairdressing and beauty 1,062,
  physical well-being 132, laundry and dry cleaning 75.
- **Catch-all share: 1,422 of 14,806 (9.6%)**: 47.19.0 824, 47.78.0 330,
  47.59.9 148, 47.29.0 104, group-only `47.2` 16. Under any ceiling the
  project has used; nothing to dispatch. (`brief_check.py`'s
  `taxonomy_catchall` kind speaks Socrata and CKAN only, so this share is
  guarded by the division-count checks below instead, and by step 2's own
  printout.)
- **Unclassified**: `Z` "ACTIVITY UNKNOWN" on 683 of 63,511 (1.1%); none in a
  bucket by construction.
- **Division 45 is OUTSIDE the three divisions** (decided below, 2026-10-02):
  45.32.0 parts retail 1,060 · 45.11.2 vehicle retail 435 · 45.11.1
  wholesale-and-retail 117 · 45.19.0 21; repair 45.20.0 661 stays out.

## Placement - 81% real, and the 19% is two different problems

1. **No coordinate: 1,475 kept rows (10.0%)**; 1,453 have an address string,
   892 sit in district "Unknown". **Recommend: drop and disclose** (no
   geocoder; a national address layer on NSDI is ASSERTED, behind a login,
   and only worth an `address-join` probe if the owner wants these placed).
2. **Placeholder coordinates: 1,295 kept rows (9.7% of those with
   coordinates) on ten points** that are district or settlement centroids,
   identified from the commonest company factual address on each point
   ("საბურთალო", "ისანი", "ვაკე", Digomi village, blank) or from rows in seven
   districts sharing one point:

   | Point (lat, lon) | Kept rows | What it is |
   |---|---|---|
   | 41.68655, 44.840891 | 255 | Isani district; **77 m from Isani station** |
   | 41.749448, 44.779977 | 221 | blank addresses; **1 m from Didube station** |
   | 41.725938, 44.750388 | 212 | Saburtalo district centroid |
   | 41.685844, 44.853535 | 165 | blank addresses; **87 m from Samgori station** |
   | 41.693803, 44.801517 | 164 | seven districts on one point; **113 m from Liberty Square** |
   | 41.789026, 44.810777 | 94 | Nadzaladevi, blank addresses |
   | 41.709599, 44.756885 | 77 | Vake district centroid |
   | 41.72151, 44.762499 | 45 | Digomi village centroid |
   | 41.695, 44.789167 | 33 | three-decimal point, city centre |
   | 41.613415, 44.908357 | 29 | Krtsanisi, blank addresses |

   **805 of them sit on four metro stations**, the worst place for a
   placeholder on this map. **Recommend: drop and disclose**, by an explicit
   list of points in config, re-derived at build from the rule "a point
   carrying 50+ rows whose commonest legal-entity factual address is a bare
   district or settlement name, or blank" (decided below, 2026-10-02).
3. **Not placeholders: the markets.** Lilo (Kakheti Highway 112, 484 kept
   rows) and Eliava (Tsabadze 8 and Khosharauli, 309), plus the Station
   Square market streets (several points of 20-90 rows each), carry real
   addresses. Their traders are individual entrepreneurs on fixed pitches,
   already coded 47.71 clothing and the like rather than 47.8x stalls.

## 🚇 Rail - OSM (no GTFS found)

- **Tbilisi Metro, Tbilisi Transport Company** (city-owned).
  - **Akhmeteli-Varketili Line** (`ref=1`, `#FF0000`): 16 stations, Akhmeteli
    Theatre to Varketili.
  - **Saburtalo Line** (`ref=2`, `colour=green`, a CSS keyword): 7 stations,
    State University to Station Square-2.
- **Operator's count for gate 3: "27.3 km with 23 stations on two lines"**
  (TTC's Stakeholder Engagement Plan, October 2024,
  `https://ttc.com.ge/sites/default/files/2024-10/Tbilisi%20Metro_New%20RS_SEP_09Oct2024_0.pdf`).
  OSM: **23 `station=subway` nodes, 16 + 7 stop members**. They agree.
- **Spacing**: nearest neighbour min 110 m (Station Square-1 and -2), median
  1,033 m, max 1,536 m. No platform duplication; keep every station (a
  uniformly sparse system, no sub-line filter).
- **One Overpass query** (cached: `data/tbilisi/raw/osm_metro.json`, 93
  elements, 2026-10-02; the query is in the cache's `_query`). The build's
  `fetch_sources.py` re-issues it once through `pipeline.osm.fetch()`.
- **All 23 stations are inside Tbilisi**; no excluded stations, no naming
  layer.
- **No `osm_route_refs` check below, deliberately**: each `brief_check` run
  would spend an Overpass query, and the owner's rule is one per city. The
  build's step 1 asserts 23 stations, 16 + 7, against the operator's count.
- **English names**: OSM `name:en` on all 23 (Georgian national
  romanisation). ⚠️ OSM writes **"Nadzaledevi"**; the operator's and the
  register's spelling is **Nadzaladevi**.

## Scope

**The city of Tbilisi** (region code 11; ten districts plus Didgori).
Stations: all 23. Business rows: factual address in region 11.

## Licence - Geostat: PERMITTED WITH CONDITIONS (read 2026-10-01, re-read 2026-10-02)

- **Terms of Use** (`https://www.geostat.ge/en/page/monacemta-gamoyenebis-pirobebi`,
  linked from the register app's footer as "Terms of Data Usage"): any use,
  "including commercial and non-commercial use, without restriction ...
  without prior permission". Third-party copyright and Geostat's logos are
  excluded from the grant.
- **MUST DISPLAY**: Geostat as the source ("Users should indicate Geostat as a
  source of information when using data of GEOSTAT"; also the statistics law,
  Art. 43(6)). Proposed wording: **"Business data: National Statistics Office
  of Georgia (Geostat), Statistical Business Register, retrieved
  <YYYY-MM-DD>; processed by this project."**
- **MUST NOT**: use Geostat's logo; imply Geostat's endorsement.
- **OpenStreetMap**: ODbL 1.0, the project's standing credit.
- **TTC**: only a published count is used; no TTC data is redistributed.

## Privacy

- **Unnamed dots for legal form 30** (owner): the pin shows the category only.
  9,529 of 14,806 kept rows (64.4%).
- **Companies keep their names**, in Georgian (96% Georgian script; `lang=en`
  does not translate names). ⚠️ An LLC can be named after a person, and
  `scripts/check_personal_exposure.py` reads Latin script only, so its zero
  would not be a finding: add a Georgian pass or record why the structural
  rule suffices.
- **No residence signal** in the register: legal address equal to factual on
  3.5% of kept individual-entrepreneur rows. The unnamed-dot rule is the
  control; record it in `docs/privacy_verdicts.md`.

## Region and projection

- **Projected CRS: UTM 38N, EPSG:32638** (longitude 44.79).
- **Region**: `add-city` says every European city tags `Europe`; Tbilisi at
  44.8 E is far east of every built European city, and `app/cities.py`'s
  `REGION_ORDER` comment says to re-measure Europe's frame "when a city appears
  far enough east". Decided below, 2026-10-02.
- **Country** string: `Georgia`; file `docs/data_sources/georgia.md`.
  ⚠️ "Georgia" is also a US state in this project's text (Atlanta's row):
  check that `app/country_sections.py` files Atlanta's sections under the
  United States and not under the new country.

## Open items

- ✅ **Placeholder coordinates: DROP AND DISCLOSE (owner, 2026-10-02,
  "approve all three").** 1,295 kept rows sit on ten centroid points, 805
  of them on four metro stations. Recommended: drop and disclose, like
  Madrid's zero coordinates. Alternative: keep and disclose, which inflates
  Isani, Didube, Samgori and Liberty Square by 164-255 dots each.
- ✅ **Division 45: THE PRECEDENT (owner, 2026-10-02).** Motor vehicles. The precedent (R4) keeps car dealers in
  Retail and leaves repair out; France is the disclosed exception that drops
  the whole division. **Recommend the precedent**: keep 45.11.2 vehicle retail
  (435), 45.19.0 (21) and 45.32.0 parts retail (1,060, the NAICS 441310
  analogue); leave out 45.11.1 "wholesale and retail" (117, the wholesale half
  decides it) and all repair. About +1,516 Retail rows, unmeasured for
  coordinates.
- ✅ **Region: a NEW leaf region, "West Asia" (owner, 2026-10-02).** The
  owner: "actually tbilisi is quite far away from other cities", "west asia
  could work too", "if georgia is officially in asia … we don't need to
  modify europe".
  - The UN M49 geoscheme puts Georgia in Western Asia, with Armenia,
    Azerbaijan, Turkey and Cyprus.
  - Dublin to Tbilisi is about 3,700 km, past the 3,300 km at which Canada
    was split.
  - Named for the area, as East Asia and Oceania were, so a later Baku,
    Yerevan or Ankara joins it.
  - **Europe is not modified.** `REGION_ORDER` gains "West Asia" with a
    comment saying why, and `scaffold_city.py` needs `--new-region`.
  - The label check is run as for any region. One city has nothing to
    collide with, and its pill shows in Global.
  Earlier the same day: `Europe`, measured, approved and then reopened. Tag `Europe` (the rule), then run `check_macro_labels.py`; if
  Europe's frame fails with Tbilisi in it, a new region is the owner's call.
  **Recommend `Europe`**, measured.
- ⚠️ **"Active" lags new businesses**: kept rows first registered in 2021
  1,193, 2023 484, 2024 189, 2025 99, 2026 33. Disclose on the page that a
  business appears once it has declared turnover or staff (the criterion is
  ASSERTED from a secondary source; find Geostat's own wording at build).
- ⚠️ **The undercount** (one row per enterprise) is disclosed per the owner's
  call; the page text comes from `docs/city_page_format.md`.
- ⚠️ **Station Square-1 / -2** are 110 m apart: two stations in the operator's
  count. Draw both (the count) with their real names; the rings overlap almost
  entirely.
- ⚠️ **"Nadzaledevi"** in OSM: label the station as the operator spells it,
  Nadzaladevi, with the fix recorded.
- ⚠️ **Rate limit**: `fetch_sources.py` sleeps between pages and honours
  `retryAfter`; a 429 mid-pull must not leave a partial file.
- ⚠️ **Font**: confirm `pipeline/theme.py`'s `FONT_STACK` renders Georgian
  (Segoe UI and Noto Sans Georgian do).
- ⚠️ **Boundary for the map frame**: OSM's administrative relation (fold it
  into the build's one Overpass query) or Geostat's GIS polygon (feature
  `"11"` in `gis.geostat.ge`'s bundle, not a stable URL). Recommend OSM.
- ⚠️ **No GTFS** is ASSERTED from one method (operator hosts plus web search;
  the Mobility Database was not read). A build may check the catalogue once.

```brief-checks
[
  {
    "id": "tbilisi-register-total",
    "claim": "Geostat's API returns 63,000-63,999 active units with a factual address in Tbilisi (region 11); measured 63,511 on 2026-10-02",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&limit=1&page=1&lang=en",
    "present": ["\"total\":63"]
  },
  {
    "id": "tbilisi-register-columns",
    "claim": "The API returns the personal columns the fetch must drop, the legal form, the NACE Rev. 2 code and X/Y (X is latitude)",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&limit=1&page=1&lang=en",
    "present": ["\"Personal_no\"", "\"Legal_Code\"", "\"Head_PN\"", "\"Partner_PN\"", "\"Full_Name\"", "\"Address2\"", "\"Legal_Form_ID\"", "\"Activity_2_Code\"", "\"X\"", "\"Y\""]
  },
  {
    "id": "tbilisi-register-nonsense-control",
    "claim": "The factual-region filter is real: a nonsense region returns zero rows",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=zzqq&isActive=true&limit=1&page=1&lang=en",
    "present": ["\"total\":0"]
  },
  {
    "id": "tbilisi-register-with-coordinates",
    "claim": "57,000-57,999 of the active Tbilisi units carry coordinates (91.1%); measured 57,869",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&x=true&y=true&limit=1&page=1&lang=en",
    "present": ["\"total\":57"]
  },
  {
    "id": "tbilisi-division-47",
    "claim": "Division 47 (retail) holds 14,000-14,999 active Tbilisi units; measured 14,493",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&activityCode=47&limit=1&page=1&lang=en",
    "present": ["\"total\":14"]
  },
  {
    "id": "tbilisi-division-56",
    "claim": "Division 56 (food service) holds 1,600-1,699 active Tbilisi units; measured 1,628",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&activityCode=56&limit=1&page=1&lang=en",
    "present": ["\"total\":16"]
  },
  {
    "id": "tbilisi-division-96",
    "claim": "Division 96 (personal services) holds 1,300-1,399 active Tbilisi units; measured 1,374",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/documents?factualAddressRegion=11&isActive=true&activityCode=96&limit=1&page=1&lang=en",
    "present": ["\"total\":13"]
  },
  {
    "id": "tbilisi-legal-form-30",
    "claim": "Legal form 30 is the individual entrepreneur, a natural-person identifier type",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/legal-forms?lang=en",
    "present": ["\"ID\":30,\"Abbreviation\":\"Individual Entreprises\"", "\"Stat_ID_Type\":2"]
  },
  {
    "id": "tbilisi-region-code",
    "claim": "Region code 11 is the city of Tbilisi",
    "kind": "http_contains",
    "url": "https://br-api.geostat.ge/api/locations/regions?lang=en",
    "present": ["\"Location_Code\":\"11\",\"Location_Name\":\"The city of Tbilisi\""]
  },
  {
    "id": "tbilisi-geostat-terms",
    "claim": "Geostat's Terms of Use still grant any use without prior permission and require naming Geostat as the source",
    "kind": "http_contains",
    "url": "https://www.geostat.ge/en/page/monacemta-gamoyenebis-pirobebi",
    "present": ["for any purpose, including commercial and non-commercial use", "without prior permission", "Users should indicate Geostat as a source of information", "does not include logos and trademarks"]
  },
  {
    "id": "tbilisi-ttc-station-count-doc",
    "claim": "TTC's 2024 Stakeholder Engagement Plan (the source of '23 stations on two lines', gate 3) is live",
    "kind": "http_ok",
    "url": "https://ttc.com.ge/sites/default/files/2024-10/Tbilisi%20Metro_New%20RS_SEP_09Oct2024_0.pdf",
    "min_bytes": 500000,
    "content_type_contains": "pdf"
  },
  {
    "id": "tbilisi-projected-crs",
    "claim": "Tbilisi projects to UTM 38N",
    "kind": "utm_zone_from_longitude",
    "lon": 44.79,
    "expect": "EPSG:32638"
  }
]
```
