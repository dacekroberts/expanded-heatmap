# Ghent — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band B,
food service with food shops as a Retail partial (owner, 2026-10-03); kept at
B on FAVV after the KBO measurement, KBO not used (owner, the same evening).
Brief written 2026-10-03.** Run `python scripts/brief_check.py ghent` before
writing any code. The trail: `docs/decisions_drafts/staging.md`, 2026-10-03
"The sweep's first group banded", "Seven licence reads for the sweep's first
group" and "KBO measured: Belgian bands kept"; the master list's Band B row.

⚠️ **Antwerp's twin.** The business leg, the licenses, the notices and the
feed are Antwerp's (`docs/build_briefs/antwerp.md`): build the FAVV-to-VKBO
join once as a country module, and read Antwerp's sections on the two
sources, the classification, the `(0,0)` placeholder, the WFS-only rule and
the notices before this one. **Göteborg is the page template.** What differs
is below: a smaller, simpler tram network and no merger.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | Street trams; every drawn route is `route_type` 0 in De Lijn's feed; trams-only maps approved (2026-09-29) |
| **`coverage`** | **`one_bucket`** ("Food premises only") | Food service plus food shops (Göteborg) |
| **Scope** | **Stad Gent** (NIS 44021) | The FAVV join is placed by VKBO's points; no merger touched Ghent in 2025 |
| **Lines drawn** | De Lijn trams **T1, T2, T4** in the feed's colors | **Three lines, not four**: the screen's "T1-T4" was a range, and there is no T3 tram in the feed |
| **Rings** | **halved**: 51 stations by name (50 inside), **median gap 272 m** | The owner's spacing rule |
| **Call (approved): caterers** | **Out**: PL83, 184 placed | As Antwerp (R1) |
| **Call (approved): sole traders** | **Every food premises placed**; no name shown | As Antwerp (owner, 2026-10-03, call 5) |
| **Call (new, recommend): stop names** | **Merge platform names** ("perron N") | As Antwerp: no `parent_station` in the feed, so the merge is the owner's |
| **Call (new, recommend): complementary retail** | **Out**: PL29 with AC95, 95 placed | As Antwerp |

---

## The one-line summary

**FAVV's food register on VKBO's points: 1,810 of 1,905 food-service premises
placed (95.0%) and 932 food shops, no names in the chain. Three De Lijn tram
lines, every 5 to 10 minutes by day, one stop outside the city.**

---

## Scope

- **Postcodes (10):** 9000, 9030 (Mariakerke), 9031 (Drongen), 9032
  (Wondelgem), 9040 (Sint-Amandsberg), 9041 (Oostakker), 9042 (Desteldonk,
  Mendonk, Sint-Kruis-Winkel), 9050 (Gentbrugge, Ledeberg), 9051 (Afsnee,
  Sint-Denijs-Westrem), 9052 (Zwijnaarde). Every postcode's `GEM Nom` in
  FAVV reads Ghent or one of its sections.
- **VKBO:** NIS 44021, 75,117 rows (45,466 establishment units, 29,651
  legal-person enterprises), **2,911 on the `(0,0)` placeholder**; real
  points X 94,726-115,970, Y 186,462-208,371 (Lambert 72).
- **CRS:** UTM 31N, **EPSG:32631** (3.72° E). **Region** `"Europe"`.

---

## Rail — De Lijn's own GTFS

The source, its license position, the rolling fetch and the chunked read are
Antwerp's (the Belgian Mobility portal's keyless De Lijn feed, CC BY 4.0
under the portal's terms, a `licence-read` before use, OSM the fallback).

### Lines, stops and headways (measured 2026-10-03 on the feed, Tuesday 2026-10-13)

| Line | Feed route variants | Feed color | Stops | Inside | Daytime headway (09-16) |
|---|---|---|---|---|---|
| T1 | 3 | `#FFCC00` | 21 | 21 | 5 (max 6) |
| T2 | 2 | `#15882E` | 22 | 21 (95%) | 8 (max 10) |
| T4 | 2 | `#E40521` | 28 | 28 | 10 (max 12) |
| **Network** | | | **51 stations** | **50** | |

- **One stop outside: T2's terminus in Melle.** T2 keeps 95% inside, so it is
  drawn to its end and the Melle stop is listed as outside.
- **Tuesday 2026-11-24:** 51 stations again (T1 22, T4 29 stops). Recount
  on the feed current at build.
- **Inside** is read from the locality the feed prefixes to each stop name
  (Gent, Gentbrugge, Ledeberg, Sint-Denijs-Westrem); the build cuts by the
  city polygon.
- **The screen's 71 stop names are not the network's.** They came from
  data.stad.gent's stop table (`bushaltes-gent`: 134 platform rows that De
  Lijn tags as tram-served). **The feed serves 51 stations on both dates
  read.** Before step 1, compare the two lists and read De Lijn's notices:
  a section not served this timetable period is the category rules'
  "station closed for works" (not drawn, listed with the reopening date, a
  `PLAN.md` item), not a silent drop. T1's and T4's route names in the feed
  mention termini (Moscou, Muidebrug, Lange Steenstraat) worth checking
  against the stops served.
- **Median nearest-neighbour gap 272 m**: halved rings.
- **Gate 3:** De Lijn's line pages, script-rendered, read in a browser at
  build, else `OPERATOR_COUNTS_GAP` (as Antwerp).
- **Colors:** three distinct feed colors. **T1's yellow `#FFCC00`**: check
  contrast on the light theme (Lille's darkening if it fails).
- **Not drawn:** buses; NMBS-SNCB trains.

---

## Business leg — FAVV joined to VKBO (as Antwerp)

| Bucket | FAVV establishments | Joined | **Placed** | Rate |
|---|---|---|---|---|
| Food service | 1,905 (restaurants 1,255, bars and cafés 494, friteries 85, pita 71) | 1,855 | **1,810** | **95.0%** |
| Food shops | 954 (retailers 738, bakeries about 107, butchers about 95, fishmongers 13) | 949 | **932** | **97.7%** |
| Caterers (out) | 191 | 191 | 184 | 96.3% |
| Complementary retail (out) | 99 | 96 | 95 | 96.0% |

- **The misses:** food service 50 (33 FAVV-internal numbers, 17 KBO numbers;
  none of a sample of 17 found anywhere in VKBO). Bars and cafés place
  lowest (90%), mostly on `(0,0)` points.
- **No names; tooltip shows the FAVV category** (Berlin's precedent);
  `check_personal_exposure.py ghent` still runs.
- **Currency, KBO not used, the classification, the WFS-only rule:** as
  Antwerp.

### The page

- **Captions:** Antwerp's, with Ghent's dates.
- **The narrower scope, one-bucket form:** "**This map shows food only, not
  three categories.** Its dots are the food businesses registered with
  FAVV-AFSCA, Belgium's food safety agency: restaurants, bars and cafés,
  friteries and pita shops, and food shops (bakers, butchers, fishmongers and
  other food retailers), shown as Food service and Food shops." Then "So
  **clothes shops, hairdressers and the like are not on this map**."
- **The trams bullet:** "3 De Lijn tram lines are drawn, **T1, T2 and T4**
  ..., in De Lijn's own colors" and "Trams run about every 5 to 10 minutes by
  day". The scope bullet: "T2 runs on into Melle, so its 1 stop there is left
  out."
- **Proposals:** as Antwerp (the type-not-name sentence; the placement
  sentence); any closed-for-works sentence.

---

## Licenses and notices

**FAVV, VKBO and De Lijn: Antwerp's three, unchanged**, with "Ghent's food
businesses" in the FAVV sentence: FAVV-AFSCA credited through its home page
with the extract date (CC BY 4.0); VKBO's prescribed line "publieke KBO
gegevens, verrijkt met adressen uit het Vlaamse Adressenregister" plus the
extract date (Modellicentie gratis hergebruik v1.0); "Source: De Lijn – Open
Data – {feed date}" pending the feed's read. One notice per source shared
with Antwerp where the sentence names no city.

## Downstream

As Antwerp: Visuals and Analytics are told when the build pushes
(`docs/session_roles.md`, "Downstream sessions"), each notice marked card
face or caption only in the drafts file, the open terms question (De Lijn's
feed) named, and the inputs listed: a new city, `outputs/ghent/`, the city
registry, the notices.

## What remains for the build

- 🚨 **The 71 against 51 stations:** compare data.stad.gent's stop table
  with the feed's served stops; closed-for-works handling if a section is
  out this period.
- ⚠️ **Antwerp first** (the shared FAVV and VKBO module), or a joint build.
- ⚠️ **The owner's calls:** platform-name merge, complementary retail, notice
  wording.
- ⚠️ **Gate 3**, T1's yellow, `(0,0)` dropped.
- `check_personal_exposure.py ghent`, `check_provenance.py` names Ghent OK,
  `check_scope_disclosure.py` passes.

```brief-checks
[
  {
    "id": "ghent-favv-dataset-page",
    "claim": "FAVV's open-data page still names CC BY 4.0 (in Dutch), weekly updates, and the language files (the EN one is cached at data/belgium/raw/)",
    "kind": "http_contains",
    "url": "https://favv-afsca.be/nl/open-data/favv-operatoren",
    "present": ["Naamsvermelding 4.0 Internationaal", "Wekelijks", "inter_actieve_actoren_NL.csv"]
  },
  {
    "id": "ghent-vkbo-wfs-feature-type",
    "claim": "VKBO's WFS still serves the VKBO:Vkbo feature type and advertises propertyName and resultType, which the build's name-free paging depends on (never the OGC API, which ignores both)",
    "kind": "http_contains",
    "url": "https://geo.api.vlaanderen.be/VKBO/wfs?service=WFS&request=GetCapabilities",
    "present": ["VKBO:Vkbo", "propertyName", "resultType"]
  },
  {
    "id": "ghent-delijn-route-types",
    "claim": "De Lijn's feed carries 42 tram route variants (route_type 0) across Flanders, Ghent's T1 (3), T2 (2) and T4 (2) among them, and no metro type. A change means the network moved: re-read the lines before step 1",
    "kind": "gtfs_route_type_counts",
    "url": "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/delijn/static",
    "expect": {"0": 42, "1": 0}
  },
  {
    "id": "ghent-bmc-terms-cc-by",
    "claim": "The Belgian Mobility portal's terms make every dataset CC BY 4.0 unless stated otherwise, each operator the licensor, with the attribution form 'Source: [PTO Name] - Open Data - [date]'",
    "kind": "http_contains",
    "url": "https://data.belgianmobility.io/en/terms.html",
    "present": ["Creative Commons Attribution 4.0 International", "Source: [PTO Name]", "De Lijn"]
  },
  {
    "id": "ghent-projected-crs",
    "claim": "Ghent's projected CRS is UTM 31N (EPSG:32631)",
    "kind": "utm_zone_from_longitude",
    "lon": 3.72,
    "expect": "EPSG:32631",
    "mode": "tram",
    "coverage": "one_bucket",
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
