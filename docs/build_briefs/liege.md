# Liège — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band B
with the gap disclosed, coverage measured inside the station rings first
(owner, 2026-10-03); kept at B after the KBO measurement, KBO not used
(owner, the same evening). Brief written 2026-10-03, with the in-ring
measurement the owner asked for (below).** Run
`python scripts/brief_check.py liege` before writing any code. The trail:
`docs/decisions_drafts/staging.md`, 2026-10-03 "The sweep's first group
banded", "Seven licence reads for the sweep's first group" and "KBO measured:
Belgian bands kept"; the master list's Band B row.

⚠️ **Charleroi's twin on the business side** (`docs/build_briefs/charleroi.md`):
the LoGIC reader, its traps, its license and notice, and TEC's feed are
Charleroi's; read those sections first. What differs: **one street tram**,
opened 2025-04-28, wholly inside the commune, so this is a trams-only page
(`tram-city`), narrowed like Zurich's and Den Haag's.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | One street tram, `route_type` 0 in TEC's feed; trams-only maps approved (2026-09-29) |
| **`coverage`** | **`narrowed`** ("Two") | Retail and food service from LoGIC; its "Services" class is a catch-all, left out (as Charleroi) |
| **Scope** | **Ville de Liège** (INS 62063) | LoGIC by INS; every tram stop is in the commune |
| **Lines drawn** | **T1** (TEC), Coronmeuse - Standard | The feed's only tram route |
| **Rings** | **halved**: **23 stops, median gap 351 m** | The owner's spacing rule |
| **Calls (new, recommend)** | **Hotels in HoReCa: disclose; names: the shop sign** | As Charleroi |
| **Call (new, recommend): the double-parent stop** | **One station** | One stop carries two parent ids in the feed (24 parents, 23 names); a merge of differently named parents is the owner's (`tram-city` section 2) |

---

## The one-line summary

**Wallonia's summer-2024 shop survey: 1,477 shops and 868 horeca premises,
complete inside 20 commercial perimeters that cover 16% of the tram's ring
area. One new tram line, 23 stops, every 6 minutes by day.**

---

## Scope

- **Ville de Liège, INS 62063**, every LoGIC point with that INS (checked
  against the commune polygon at build).
- **Postcodes** (for FAVV's comparison only): 4000, 4020, 4030, 4031, 4032.
- **CRS:** UTM 31N, **EPSG:32631** (5.57° E; still zone 31, west of 6° E).
  **Region** `"Europe"`; country `"Belgium"`.

---

## Rail — TEC's own GTFS (as Charleroi)

The feed, its two hosts, the license question (CC0 on the national access
point, CC BY 4.0 under the Belgian Mobility portal's terms: a `licence-read`
decides), the leading-space trap in `feed_info.txt` and the rolling fetch are
Charleroi's. OSM is the fallback.

### The tram (measured 2026-10-03 on the feed, Tuesday 2026-10-13)

| | |
|---|---|
| Route | **T1**, "Coronmeuse/Expo - St-Lambert - Guillemins-Standard", one route in the feed |
| Stops | **23 by name** (24 parent stations: one stop has two parents; 45 platforms over all dates) |
| Inside the commune | **23 of 23** (stop localities Liège and Sclessin, a district of the city) |
| Daytime headway (09-16) | **every 6 minutes** (longest gap 8-9) |
| Median nearest-neighbour gap | **351 m** by name (341 m over the 24 parents): halved rings |
| Feed color | `#FFCD00` (TEC yellow; check contrast on the light theme) |

- **Opened 2025-04-28**, 11.7 km (the screen; L'Avenir and TEC's press,
  2025-04). The Seraing and Herstal extensions were cancelled (2024).
- **The screen's "Bressoux branch"** is not a separate route in the feed;
  check at build whether any served stop lies on it, and name it on the page
  only if it runs.
- **Gate 3:** the City of Liège's open dataset "Tram - Stations"
  (opendata.liege.be, 23 rows, 2022, CC BY) is a public authority's list
  independent of OSM and of the feed: `OPERATOR_STATION_COUNTS = {"T1": 23}`
  with that source named, after confirming its rows match the line as
  opened. TEC's own pages answer scripts with 403 (as Charleroi).
- **Not drawn:** buses; NMBS-SNCB trains.

---

## Business leg — LoGIC 2024 (the downloaded GeoPackage only, as Charleroi)

### Liège (INS 62063)

| | Points |
|---|---|
| **Commerce de détail → Retail** | **1,477** |
| **HoReCa → Food service** | **868** |
| Services (out: a catch-all) | 623 |
| Cellule vide (out: vacant) | 793 |
| **All** | **3,761** |

- **Survey dates 2024-07-08 to 2024-08-26**; 20 perimeters.
- **Coverage:** every shop inside the perimeters, only shops over 200 m²
  outside them (the publisher). **Against FAVV** (food-service
  establishments by the postcodes above): **868 against 1,271, 68%**.
- **Traps:** Charleroi's (`INS` as float64; `NOD_CODE` set on every point,
  so the perimeter test is spatial; EPSG:3812).

### Inside the station rings — the owner's "measure first" (2026-10-03)

The 0.3-mile union around the 23 stops, in EPSG:32631:

| | |
|---|---|
| Ring union | **9.73 km²** |
| **Share of it inside a commercial perimeter** | **16%** (7 perimeters touch it) |
| Retail points inside the rings | 769 of 1,477 (52%), **756 inside a perimeter** |
| HoReCa points inside the rings | 567 of 868 (65%), **all 567 inside a perimeter** |

**Read:** as Charleroi. Inside the rings the survey's points sit almost
wholly in the perimeters (98% of retail, 100% of horeca), which cover 16% of
the ring area; the rest holds only shops over 200 m². The tram runs through
the city's commercial center, so the count gap is smaller than the area gap,
but no open source measures it. **For the owner, with the build:** the page
proceeds with the gap disclosed (Band B as approved), unless this figure
changes the call.

### Currency, privacy

As Charleroi: a summer-2024 snapshot with vacant units (re-check by 2029);
the dot shows the shop sign, never the street or number;
`check_personal_exposure.py liege`; each source keeps its own sole-trader
rule.

### The page (`tram-city` section 6)

- **Captions:** "Shops and horeca premises from the Service public de
  Wallonie's LoGIC 2024 survey (CC BY 4.0), surveyed **July and August
  2024**; the tram line and its stops from TEC's open data, fetched
  **{date}**."
- **The tram:** "1 TEC tram line is drawn, **T1**, labeled on the map and in
  the legend, in TEC's own color." "Trams run about every 6 minutes by day."
  "Liège has no metro, so its tram is its rapid transit, as in Riga. Every
  tram stop here gets rings." The halved-rings bullet with 351 m (recomputed).
  "The map covers the **City of Liège**." (The template's heading **The
  tram** for one line; the rail clause names the feed, as France's template
  does.)
- **The narrower scope:** "**This map has two categories, not three.**
  Wallonia's 2024 shop survey sorts each shop as retail, horeca, services or
  vacant. Its services class mixes hairdressers with banks and agencies, so
  it is left out, as are vacant units."
- **Proposals** (drafts file): the 200 m² sentence with "20 commercial
  districts"; the hotels sentence.
- `render_map_help('two business categories (Retail and Food service)')`.

---

## Licenses and notices

- **LoGIC 2024:** Charleroi's notice (the SPW citation verbatim, the
  catalogue link, the modification statement, CC BY 4.0; download only,
  never the MapServer), one notice for both cities where the sentence names
  no city.
- **TEC GTFS:** pending its `licence-read`; "Source: LETEC – Open Data –
  {date}" under the portal's form; no TEC logo.
- **City of Liège "Tram - Stations"** (gate 3 only, read for a count, never
  republished): CC BY per the screen; a row in
  `docs/data_sources/belgium.md` if the build reads it (`#support-sources`).

## Downstream

As Charleroi: Visuals and Analytics are told when the build pushes
(`docs/session_roles.md`, "Downstream sessions"), each notice marked card
face or caption only in the drafts file, the open terms question (TEC's
feed) named, the inputs listed: a new city, `outputs/liege/`, the city
registry, the notices.

## What remains for the build

- 🚨 **The in-ring figure to the owner** with the build (16% of ring area in
  perimeters), and the gap sentences as proposals.
- ⚠️ **Charleroi first** (the shared LoGIC module), or a joint build.
- ⚠️ **`licence-read` of TEC's feed**; the double-parent merge; the
  Bressoux question; gate 3 from the City's dataset.
- `check_personal_exposure.py liege`, `check_provenance.py` names Liège OK,
  `check_scope_disclosure.py` passes.

```brief-checks
[
  {
    "id": "liege-logic-coverage-statement",
    "claim": "LoGIC 2024's Metawal record still states the field survey of summer 2024 and the 200 m2 threshold outside the commercial perimeters, the gap the page discloses",
    "kind": "http_contains",
    "url": "https://metawal.wallonie.be/geonetwork/srv/api/records/5f56d784-2fd7-47eb-a62a-991d4741a67d",
    "present": ["relevé de terrain", "200 m"]
  },
  {
    "id": "liege-tec-feed-current",
    "claim": "TEC's feed on the Belgian Mobility portal is keyless and current (calendar_dates ran to 2026-12-25 when measured; feed_info's dates carry a leading space, so gtfs_feed_window cannot read them)",
    "kind": "gtfs_calendar_window",
    "url": "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static",
    "expect": "current"
  },
  {
    "id": "liege-tec-tram-stations",
    "claim": "Liège's T1 is TEC's only tram route and serves 24 parent stations over all dates, 23 stop names (one stop has two parents), parent_station populated",
    "kind": "gtfs_stations",
    "url": "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static",
    "route_types": ["0"],
    "expect_parent_station_populated": true,
    "expect_stations": 24,
    "crs": "EPSG:32631"
  },
  {
    "id": "liege-bmc-terms-cc-by",
    "claim": "The Belgian Mobility portal's terms make every dataset CC BY 4.0 unless stated otherwise, LETEC among the licensors, with the attribution form 'Source: [PTO Name] - Open Data - [date]'",
    "kind": "http_contains",
    "url": "https://data.belgianmobility.io/en/terms.html",
    "present": ["Creative Commons Attribution 4.0 International", "Source: [PTO Name]", "LETEC"]
  },
  {
    "id": "liege-projected-crs",
    "claim": "Liège's projected CRS is UTM 31N (EPSG:32631)",
    "kind": "utm_zone_from_longitude",
    "lon": 5.57,
    "expect": "EPSG:32631",
    "mode": "tram",
    "coverage": "narrowed",
    "scope": "city",
    "crs": "EPSG:32631",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
