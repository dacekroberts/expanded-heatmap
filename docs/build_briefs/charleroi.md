# Charleroi — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band B
with the gap disclosed, coverage measured inside the station rings first
(owner, 2026-10-03); kept at B after the KBO measurement, KBO not used
(owner, the same evening). Brief written 2026-10-03, with the in-ring
measurement the owner asked for (below).** Run
`python scripts/brief_check.py charleroi` before writing any code. The trail:
`docs/decisions_drafts/staging.md`, 2026-10-03 "The sweep's first group
banded", "Seven licence reads for the sweep's first group" and "KBO measured:
Belgian bands kept"; the master list's Band B row.

⚠️ **Liège's twin on the business side** (`docs/build_briefs/liege.md`):
both read Wallonia's LoGIC 2024 survey, so write its reader once as a
country module. **Zurich and Den Haag are the narrowed-page precedents**
("Two"). Read with `add-city`, `osm-rail` (the fallback), `tram-city`
(spacing, gate 3, page template) and `publish-city`.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`light_rail`** | A tunnel and viaduct core with street-running branches (Gosselies, Anderlues): Edmonton's and Pittsburgh's shape, both `light_rail`. TEC's feed types M2-M4 as `route_type` 1 (metro), but mode flags lie (Reims's tram typed metro); the alternative, `metro`, is Liverpool's call for an underground loop. The owner's |
| **`coverage`** | **`narrowed`** ("Two") | Retail and food service (LoGIC's HoReCa); its "Services" class mixes personal services with banks and agencies, so it is left out (R2's logic) |
| **Scope** | **Ville de Charleroi** (INS 52011) | LoGIC is selected by INS; M2's Anderlues branch leaves the commune |
| **Lines drawn** | **M2, M3, M4** (TEC) | The feed's three metro routes; **M1 is not a metro route in the current feed** (below) |
| **Rings** | **halved**: 48 stations by name (38 inside), **median gap 385 m inside** | The owner's spacing rule (under about 550 m) |
| **Call (new, recommend): M2 to Anderlues** | **Drawn to its end**: 13 of 23 stops inside (57%); the 10 in Fontaine-l'Évêque and Anderlues listed as outside | Over half inside, as Den Haag's tram 1 (51%, call 26) |
| **Call (new, recommend): colors** | **The project's own palette** | M2, M3 and M4 all carry `#FFCD00` in the feed; two lines with one color are refused (Dijon). Or TEC's own network-map colors, read at build |
| **Call (new, recommend): hotels in HoReCa** | **Disclose, do not split** | LoGIC's HoReCa does not separate lodging (out by the category rules); only a keyword pass on the shop sign could, which is not register quality |
| **Call (new, recommend): names** | **The shop sign (`ENSEIGNE`) as the dot's name** | A surveyed street sign is a trade name (hub.brussels's precedent for the City of Brussels); LoGIC carries no legal form, so `check_personal_exposure.py` reads the signs, and a sign that reads as a person's own name is withheld |

---

## The one-line summary

**Wallonia's summer-2024 shop survey gives 980 shops and 450 horeca premises
with points, CC BY 4.0, downloaded once. It is complete only inside the
city's commercial perimeters, which cover 11% of the station-ring area. Three
light-metro lines from TEC's own feed, every 10 or 15 minutes.**

---

## Scope

- **Ville de Charleroi, INS 52011**, every LoGIC point with that INS
  (checked against the commune polygon at build). The commune covers its
  former communes (Gosselies, Jumet, Gilly, Lodelinsart, Dampremy,
  Marchienne-au-Pont, Monceau-sur-Sambre, Goutroux and others), so M3 and M4
  are wholly inside.
- **Postcodes** (for FAVV's comparison count only): 6000, 6001, 6010, 6020,
  6030, 6031, 6032, 6040, 6041, 6042, 6043, 6044, 6060, 6061.
- **CRS:** UTM 31N, **EPSG:32631** (4.44° E). LoGIC is EPSG:3812 (Lambert
  2008): reproject. **Region** `"Europe"`; country `"Belgium"`.

---

## Rail — TEC's own GTFS

### The source

- **TEC's static GTFS through the Belgian Mobility Open Data Portal**,
  keyless: `https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static`
  (84,926,285 bytes, Last-Modified 2026-10-04); the same feed sits on TEC's
  own host, `https://opendata.tec-wl.be/Current%20GTFS/TEC-GTFS.zip`
  (78,649,593 bytes, 2026-10-02), a bare directory listing with no terms.
  **Feed window 2026-10-02 to 2026-12-25.**
- **License:** the national access point (`transportdata.be`, `tec-gtfs`)
  states **CC0** at dataset and resource level; the Belgian Mobility
  portal's terms say CC BY 4.0 unless otherwise stated. **A `licence-read`
  decides**; credit TEC either way ("Source: LETEC – Open Data – {date}",
  the portal's form; the feed's agency name is LETEC). OSM (`osm-rail`) is
  the fallback.
- **Trap: `feed_info.txt`'s dates carry a leading space** (" 20261225"),
  which crashes `brief_check.py`'s `gtfs_feed_window` (so this brief checks
  `calendar_dates` instead). Strip before parsing.
- Rolling: fetched at every build. `stop_times.txt` is 502 MB: chunked
  (peak 0.55 GB measured).

### Lines, stations and headways (measured 2026-10-03 on the feed, Tuesday 2026-10-13)

| Line | Route | Stops | Inside | Daytime headway (09-16) |
|---|---|---|---|---|
| M2 | Gare Centrale - Anderlues Monument | 23 | 13 (57%) | 15 (max 16) |
| M3 | Gare Centrale - Gosselies Faubourg de Bruxelles | 26 | 26 | 10 |
| M4 | Gare Centrale - Gilly Soleilmont | 9 | 9 | 10 |
| **Network** | | **48 stations by name** (49 parent stations, all dates) | **38** | |

- **M1 is not a metro route in this feed.** The screen (from secondary
  sources) had M1 and M2 each every 30 minutes on the Anderlues branch; the
  feed has **M2 alone, every 15**, so the branch still meets the converted-
  railway frequency gate (the old vicinal line). `M1ab`, `M3ab` and `M4ab`
  are buses (`route_type` 3, 6 to 14 trips that day): not drawn. **Read
  TEC's notice for M1** at build.
- **Outside the commune (10):** Fontaine-l'Évêque 6 (Leernes included),
  Anderlues 4, all on M2.
- **Stations are collapsed by `parent_station`** (populated). Two names
  carry two parents each (Gare Centrale's two quays; Tirou): a merge of
  differently named parents is the owner's (`tram-city` section 2). The
  screen named Villette among the loop's stations; no served stop carries
  that name: check whether it is closed for works or renamed.
- **Median nearest-neighbour gap 385 m inside** (395 m over all 49
  parents): halved rings.
- **M5** (to Châtelet) is under construction, planned for 2027: not drawn.
- **Light-rail test:** grade-separated core, street-running branches, 15
  minutes on the converted branch. It passes on precedent.
- **Gate 3:** TEC's site answers scripts with 403 (not attempted further);
  read its line pages in a browser at build, else a dated secondary source
  named as secondary (the screen's 48 stations, 24 metro and 24 tram stops,
  is Wikipedia's network-wide figure, which counts M1).

---

## Business leg — LoGIC 2024 (the downloaded GeoPackage only)

### The source

- **"Offre commerciale en Wallonie (LoGIC 2024)"**, Service public de
  Wallonie (SPW), produced with SEGEFA (ULiège): **cached** at
  `data/belgium/raw/LOGIC_2024_GEOPACKAGE_3812.zip` (3,172,940 bytes, sha256
  `1b42f6ff...`, the files dated 2025-04-09), unzipped to
  `data/belgium/raw/logic/` with its descriptive sheet and conditions page.
  ATOM: `.../5f56d784-2fd7-47eb-a62a-991d4741a67d/atom_dataset.xml`.
  **Never the MapServer** (its service terms bring in a no-alteration
  clause).
- **Layer `LOGIC_2024__POINTS_VENTE`**, EPSG:3812, 37,701 points: OBJECTID,
  ID_TERRAIN, RUE, POLICE, ENSEIGNE (shop sign), NOD_NOM and NOD_CODE
  (perimeter), NATURE, DATE_RELEV, INS, CODE_POST. **NATURE has four values
  only**: Commerce de détail, HoReCa, Services, Cellule vide. **Never carry
  RUE or POLICE** to the page.
- **`LOGIC_2024__PERIM_COMMERCE`**: 493 commercial perimeters.
- **Traps (measured 2026-10-03):** `INS` is float64 (52011.0): compare as an
  integer. **Every point carries a `NOD_CODE`, even outside every perimeter
  polygon**, so "inside a perimeter" is a spatial test, never the field.

### Charleroi (INS 52011)

| | Points |
|---|---|
| **Commerce de détail → Retail** | **980** |
| **HoReCa → Food service** | **450** |
| Services (out: a catch-all) | 454 |
| Cellule vide (out: vacant) | 769 |
| **All** | **2,653** |

- **Survey dates 2024-08-08 to 2024-08-22**; 18 perimeters.
- **The publisher's own coverage statement:** every shop inside the
  perimeters, **only shops over 200 m² of sales area outside them**.
- **Against FAVV** (registered food-service establishments by the postcodes
  above): **450 HoReCa against 857, 53%**. FAVV has no point in Wallonia,
  so this cannot be repeated inside the rings.

### Inside the station rings — the owner's "measure first" (2026-10-03)

The 0.3-mile union around the 38 stations inside the commune (the rings'
outer edge), in EPSG:32631:

| | |
|---|---|
| Ring union | **16.86 km²** |
| **Share of it inside a commercial perimeter** | **11%** (9 perimeters touch it) |
| Retail points inside the rings | 659 of 980 (67%), **638 of them inside a perimeter** |
| HoReCa points inside the rings | 330 of 450 (73%), **328 inside a perimeter** |

**Read:** inside the rings the survey's points sit almost wholly in the
perimeters (97% of retail, 99% of horeca), and the perimeters are 11% of the
ring area. The other 89% holds only shops over 200 m². The commercial cores
the perimeters draw are where storefronts cluster, so the gap in counts is
smaller than the gap in area, but no open source measures it inside the
rings. **For the owner, with the build:** the page proceeds with the gap
disclosed (Band B as approved), unless this figure changes the call.

### Currency, privacy

- **Currency:** a summer-2024 field survey, a snapshot that records vacant
  units: it drops closures; the newest row is under five years old
  (re-check by 2029). The page gives the survey month.
- **Privacy:** the dot shows the shop sign (the call above), never the
  street or number; `check_personal_exposure.py charleroi` reads the signs.
  **Each source keeps its own sole-trader rule** (owner, 2026-10-03); KBO's
  does not reach LoGIC.

### The page (`docs/city_page_format.md`; `tram-city` section 6)

- **Captions:** "Shops and horeca premises from the Service public de
  Wallonie's LoGIC 2024 survey (CC BY 4.0), surveyed **August 2024**; the
  metro lines and their stations from TEC's open data, fetched **{date}**."
- **First heading** "The lines" (`docs/city_page_format.md`), not "The
  trams".
- **The narrower scope:** "**This map has two categories, not three.**
  Wallonia's 2024 shop survey sorts each shop as retail, horeca, services or
  vacant. Its services class mixes hairdressers with banks and agencies, so
  it is left out, as are vacant units."
- **Proposals, not template** (flag in the drafts file): "The survey
  recorded every shop inside the city's 18 commercial districts, but only
  shops over 200 m² outside them, so small shops away from those districts
  are missing."; "Horeca includes hotels, which the survey does not
  separate."; M2's outside stops; the M1 sentence if TEC names a reason.
- `render_map_help('two business categories (Retail and Food service)')`.

---

## Licenses and notices

- **LoGIC 2024: permitted with conditions** for the downloaded GeoPackage,
  CC BY 4.0 (in the zip and on Metawal). **The SPW citation verbatim:**
  "Source : Service public de Wallonie (SPW) - Offre commerciale en Wallonie
  (LoGIC 2024) (2025-04-09)", **plus the catalogue link** (the Metawal
  record, `metawal.wallonie.be/geonetwork/srv/api/records/5f56d784-2fd7-47eb-a62a-991d4741a67d`;
  the citation's own geodata.wallonie.be URI answers 404) **and a statement
  of modifications** (proposed: "Modified by this project: the services
  class and vacant units left out; points reprojected and cut to the city.").
  No SPW or Wallonia logo; nothing implying endorsement.
- **TEC GTFS:** pending its `licence-read` (CC0 or CC BY 4.0, above). No TEC
  logo.
- **Notice numbers:** claimed by the Belgium kit; one LoGIC notice shared
  with Liège where the sentence names no city.

## Downstream

When the build pushes, Visuals and Analytics are told
(`docs/session_roles.md`, "Downstream sessions"). **For each notice**
(LoGIC's, TEC's) **the build records in its drafts file card face or caption
only**, from the license's own words, and **any open terms question** (TEC's
feed until its read lands). Inputs moved: a new city, `outputs/charleroi/`,
the city registry, the notices, two license rows, a new country module.

## What remains for the build

- 🚨 **The in-ring figure to the owner** with the build (11% of ring area in
  perimeters), and the gap sentences as proposals.
- ⚠️ **M1:** TEC's reason; Villette; the two double-parent names.
- ⚠️ **`licence-read` of TEC's feed**; license rows for LoGIC and the feed
  in `docs/data_sources/belgium.md`.
- ⚠️ **The owner's calls:** mode, colors, hotels, the shop-sign names.
- ⚠️ **Gate 3** from TEC's pages in a browser, or a named secondary source.
- `check_personal_exposure.py charleroi`, `check_provenance.py` names
  Charleroi OK, `check_scope_disclosure.py` passes (the two-category gap,
  the 200 m² gap and M2's outside stops in Charleroi's own sections).

```brief-checks
[
  {
    "id": "charleroi-logic-licence-citation",
    "claim": "LoGIC 2024's Metawal record names CC-BY 4.0 and carries the SPW citation the page must show verbatim",
    "kind": "http_contains",
    "url": "https://metawal.wallonie.be/geonetwork/srv/api/records/5f56d784-2fd7-47eb-a62a-991d4741a67d",
    "present": ["CC-BY 4.0", "Offre commerciale en Wallonie (LoGIC 2024) (2025-04-09)"]
  },
  {
    "id": "charleroi-logic-atom-geopackage",
    "claim": "SPW's ATOM download feed still lists the EPSG:3812 GeoPackage the build reads (cached at data/belgium/raw/, 3,172,940 bytes, files dated 2025-04-09)",
    "kind": "http_contains",
    "url": "https://geoservices.wallonie.be/geotraitement/spwdatadownload/results/5f56d784-2fd7-47eb-a62a-991d4741a67d/atom_dataset.xml",
    "present": ["LOGIC_2024_GEOPACKAGE_3812.zip", "2025-04-09"]
  },
  {
    "id": "charleroi-tec-route-types",
    "claim": "TEC's feed carries three metro routes (M2, M3, M4; no M1) and one tram route (Liège's T1). A change means TEC's network moved: re-read the lines before step 1",
    "kind": "gtfs_route_type_counts",
    "url": "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static",
    "expect": {"0": 1, "1": 3}
  },
  {
    "id": "charleroi-tec-metro-stations",
    "claim": "The three metro routes serve 49 parent stations network-wide (all dates; 48 names on 2026-10-13 once the double-parent names, Gare Centrale's two quays and Tirou, merge), parent_station populated; 38 lie in the commune, 10 in Fontaine-l'Evêque and Anderlues",
    "kind": "gtfs_stations",
    "url": "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static",
    "route_types": ["1"],
    "expect_parent_station_populated": true,
    "expect_stations": 49,
    "crs": "EPSG:32631"
  },
  {
    "id": "charleroi-projected-crs",
    "claim": "Charleroi's projected CRS is UTM 31N (EPSG:32631)",
    "kind": "utm_zone_from_longitude",
    "lon": 4.44,
    "expect": "EPSG:32631",
    "mode": "light_rail",
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
