# Bremen - build brief

**Band B, owner-approved 2026-10-04** (`docs/decisions_drafts/staging.md`,
"Bremen to B, retail only; Gelsenkirchen's licence settled; Kurashiki
measured (owner)": "75 approved", one full bucket, a retail-only page, the
survey's date disclosed). **Licence read 2026-10-05** (same file, "Band B's
Japanese sources read" entry, its Bremen bullet): permitted with conditions,
display only. Brief written 2026-10-05 from the cached survey file, GovData's
CKAN record and BSAG's own timetable page. Run
`python scripts/brief_check.py bremen` before writing any code.

Germany's second city (Berlin is the first; the country is profiled in
`docs/build_briefs/berlin.md` and `docs/data_sources/germany.md`, so no
`add-country`). Read `tram-city` (a trams-only city outside France and
Czechia; Bremen is not one of its ten sheets, so this brief is its sheet),
`add-city`, `scaffold-city`, `premises-taxonomy` (a new module keyed on the
survey's goods-group code), `osm-rail`, `publish-city`.

**Templates:** **Göteborg** (`app/pages/137_Goteborg_Heatmap.py`) for the
one-bucket tram page; **Odense** (`pipeline/odense/`) for an OSM tram leg on
`pipeline/osm_tram.py` and for `CRS_PROJECTED = "EPSG:25832"`; **Florence**
(`pipeline/taxonomies/florence_attivita.py`) for a no-name layer whose pin
shows an English type label; **Kansas City**'s page for the data-date
sentence. No built city takes its businesses from a retail survey, so the
business leg is new (record kind on Madrid's and Barcelona's precedent).

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | BSAG's 8 tram lines; Bremen has no metro. The S-Bahn (Regio-S-Bahn Bremen/Niedersachsen) is commuter rail, out as everywhere, and named on the page |
| **`coverage`** | **`one_bucket`** | Retail only: the survey holds shops and nothing else (no food service, no personal services). The legend's single layer is Retail |
| **`categories`** | **"Retail only"**, a NEW value (call 3) | The allowed values (`FIELDS` in `scripts/check_inconsistency_list.py`) have "Food premises only" and "Personal services only" but no retail one |
| **`record_kind`** | **"Street survey or census"** | A survey of every retail site in the region, Madrid's and Barcelona's kind (premises censuses) |
| **Scope** | **The City of Bremen** (Stadtgemeinde Bremen), `SCOPE = "city"` (call 2) | The row's 3,153 points; businesses by the survey's `Gemeinde` field, stations by the city polygon |
| **Lines drawn** | **1, 2, 3, 4, 5, 6, 8, 10**, each to its end | BSAG's base timetable (below); line 4 runs on into Lilienthal (Lower Saxony) |
| **Line 4 into Lilienthal** | **Drawn to its end; its stops in Lilienthal listed as outside, no rings** | Florence's T1 and Göteborg's 4 and 12 (the kit's calls 17 and 21): about 39 of 49 stops inside, not a stub |
| **Stations** | **164 on the network by BSAG's own names; about 154 in the city** (by polygon at build) | BSAG's timetable page, read 2026-10-05 (below). The row's "about 165" is this list |
| **Rings** | **Halved expected** (the spacing rule, `tram-city` section 3) | Urban tram spacing; the median gap is not measured here (no Overpass); compute it on the stations drawn |
| **Projected CRS** | **EPSG:25832** (ETRS89 / UTM 32N) | Bremen is at 8.80° E, so its UTM zone is 32N (EPSG:32632). The survey ships in EPSG:25832, the same zone on the ETRS89 datum (sub-metre apart), so the build projects in it and never transforms the survey's points: Odense's precedent. `check_provenance.py` accepts the 258xx family |
| **Region** | `"Europe"`, country `"Germany"` | The European rule (`add-city`); no `label_tier`, as the kit's European cities (Odense, Florence, Göteborg) carry none; `check_macro_labels.py` decides, and a failure there goes to the owner with the minor tier as the option |
| **Currency** | **The survey's date on the page**; the five-year rule holds until **2027-09-30** at the latest | Fieldwork 2022-03-01 to 2022-09-30 (the record's temporal fields). The survey repeats every five years, per the record, so a 2027 survey is the expected refresh |

**Owner calls already made (do not re-ask):**
- Band B, retail only, one full bucket, the survey's date disclosed; no food
  service or personal services source exists (owner, 2026-10-04).
- The single-file download of the survey, cached in `data/bremen/raw/`
  (owner, 2026-10-04).
- The licence: permitted with conditions, display only (read 2026-10-05,
  staging's drafts; below).
- The five-year rule: the survey passes until 2027; a new survey or a refresh
  is the condition after that (owner, 2026-10-04).
- Every tram stop gets rings, no thinning, rings by the spacing rule, gate 3
  against the operator, OSM rail where no feed is in the brief (the kit's
  standing calls, `tram-city`).

**Open, carried (not this build's to settle):**
- ⚠️ **The CC BY version.** The record names "Creative Commons Namensnennung
  (CC-BY)" with no version. Whether 4.0 (the EU database right expressly
  licensed) or 3.0 (not) applies is an open owner question, held by staging.
  The notice below satisfies the strictest reading (4.0 §3(a)); the build
  does not resolve it.

**New calls for the owner at build** (each with a recommendation and its
tradeoff):
1. **"Sonstige EH-Einrichtungen" (other retail facilities), 94 rows in the
   city (3.0%): keep as Retail** (recommended). The survey files them as retail
   establishments in a survey of retail only, and the public file gives
   nothing finer. Tradeoff: the group cannot be read, so it may hold a petrol
   station shop or car dealer (both kept under R4 anyway), a market hall or a
   stall (R1: out). Out, the city reads 3,059. This is the one catch-all;
   measure it with `brief_check.py`'s `taxonomy_catchall` kind once the module
   exists.
2. **Scope: the City of Bremen alone** (recommended), line 4 drawn to
   Lilienthal with its stops there listed as outside. The survey also covers
   Lilienthal (119 rows), so a "Bremen (Regional)" page could take Lilienthal
   in; that is a `regional-extension` add-on (the city proved first, then the
   switch), not a first build. Tradeoff: about 10 stops and 119 shops wait
   for the add-on.
3. **`categories` "Retail only", added to `FIELDS` and to `TIER_OF` as
   `one_bucket`** in `scripts/check_inconsistency_list.py`, with a comment
   naming Bremen and the owner's date (recommended), the way "Personal services
   only" came in for Yokohama. `check_macro_facts.py` needs no change: a table
   B row of "— / {n} / —" is a single figure. Tradeoff: none found; the value
   is new on purpose, never misspelled into place.
4. **Gate 3 from BSAG's own timetable page** (recommended): the per-line stop
   lists embedded in `bsag.de/fahrplan/linien-und-fahrplaene`, independent of
   OSM, read for the counts only and never republished. Tradeoff: it is a
   timetable index, not a stop register, so the counts depend on the fold
   stated below.
5. **The city boundary: the Stadtgemeinde Bremen's OSM boundary from the
   build's one Overpass query** (recommended; Antwerp's and Thessaloniki's
   route, ODbL, the site's own notice). Take the city, never the Land (the
   Land adds Bremerhaven, 50 km north). The official boundary from GeoBasis-DE
   / Landesamt GeoInformation Bremen has an unread licence, so it goes to the
   owner first. Tradeoff: OSM is a volunteer map; the cross-check below
   catches a wrong polygon.
6. **The page's new sentences**: the one-bucket sentence, the survey-date
   sentence and the survey's caveat (under "The page"). Each is a proposal in
   the build's drafts file (`docs/city_page_format.md`, section 6).

---

## The one-line summary

**The 2022 regional retail survey (Kommunalverbund Niedersachsen/Bremen),
cached: 3,153 shops in the City of Bremen, every one placed in EPSG:25832, a
goods group and a floor-area class per row and no name, address or person
field. All 19 goods groups are retail; one catch-all (94) is a call. BSAG's 8
tram lines, 164 stops by the operator's own list, about 10 of them in
Lilienthal. CC BY (no version), credit the Kommunalverbund. The work is a
19-code taxonomy, the OSM tram leg, the boundary and the date sentences.**

---

## Business leg - Einzelhandelsbestand in der Region Bremen 2022

| | |
|---|---|
| **Source** | "Einzelhandelsbestand in der Region Bremen 2022", publisher **Kommunalverbund Niedersachsen/Bremen e.V.** (the rights holder); hosted by the Landesamt GeoInformation Bremen on `geoportal.bremen.de`. Metadata `f6323bd1-bd38-4f72-a7ec-cb08209564ff`, harvested to GovData as `einzelhandelsbestand-in-der-region-bremen-2022` (GDI-DE) |
| **What it is** | The record's own words: retail businesses "im engeren Sinn" at the survey date, location and main goods group. It is the data behind the Regional Centres and Retail Concept (RZEHK), from a survey of every retail site in the region **repeated every five years**; the public variant names only the trade, while a secured variant holds the range, address and sales area (not used, not asked for) |
| **File** | `data/bremen/raw/Einzelhandelsbestand_reduziert.zip` (cached 2026-10-04, 172,889 bytes, sha256 `654aec18...6646469e`, Last-Modified 2026-08-04, meta JSON beside it): one `Einzelhandelsbestand_reduziert.geojson`, 1,482,711 bytes, member dated 2026-07-24. **"Reduziert" is fewer fields, not fewer rows** |
| **Data date** | **Fieldwork 2022-03-01 to 2022-09-30** (the record's `temporal_start`/`temporal_end`; `issued` 2022-09-30). No per-row date. The record's `modified` (2026-08-13) and its frequency "CONT" describe the catalogue entry, not the survey |
| **Encoding** | UTF-8, no BOM (`SOURCE_ENCODING = "utf-8"`). The labels carry umlauts and "m²"; set `PYTHONIOENCODING=utf-8` before printing on Windows, where the console shows them as "?" |
| **Fetch** | `pipeline/bremen/fetch_sources.py` takes the same zip from `geoportal.bremen.de/resources/data/` (the brief's source, pre-permitted) and refuses a file whose sha256 differs from the meta JSON without saying so. `data/` is shared across worktrees, and the cached copy is already there |

### Fields (6, all filled on all 5,573 rows)

`id` (integer, distinct per row), `Gemeinde` (municipality, 25 values),
`HWG_C` / `HWG` (main goods group code and label, 19 values), `Gr_Kl_C` /
`Gr_Kl` (floor-area class code and label). Every geometry is a Point; no null
or zero coordinates.

- **No name, address, person, phone or business-ID field** (`id` is a row
  number). A brief check cannot watch the file's fields without downloading
  it, so step 2 asserts the six names and stops on any other.
- **Key on the codes, never the labels**: `Gr_Kl_C` 1 carries two labels
  ("0 bis 100 m²" and, on one regional row outside the city, "-").

### Measured 2026-10-05 (cached file)

- **5,573 rows in the region; 3,153 with `Gemeinde` = "Bremen"**, the next
  largest Delmenhorst 390, Verden 217, Osterholz-Scharmbeck 159 and Lilienthal
  119. Bremerhaven is not in the file (not a member of the Kommunalverbund).
- **The city cut is the `Gemeinde` field**, one exact label. Step 2 also
  checks it against the city polygon: every "Bremen" row inside, every other
  row outside, and any disagreement named and counted rather than resolved
  silently.
- **City extent** (EPSG:25832): E 467,398 to 497,864, N 5,874,877 to
  5,896,019, consistent with the city, Bremen-Nord included.
- **3,142 distinct points**; 10 points carry 2 or 3 rows (shops in one
  building), each kept as its own dot.

### Classification (the build's taxonomy decides; `docs/category_rules.md`)

Every goods group is retail, matched by what the premises is. One bucket,
**Retail**; the pin label is an English name for the group (Florence's
precedent), the German name kept in the module.

| `HWG_C` | Goods group | City | Region | Bucket and rule |
|---|---|---|---|---|
| 1 | Nahrungs-/Genussmittel (food and drink shops: grocers, bakeries, butchers, drinks, kiosks) | **1,141** | 1,978 | Retail (NAICS 445). A fixed kiosk is a shop, not the mobile-units row |
| 7 | Bekleidung und Zubehör (clothing) | **417** | 681 | Retail |
| 2 | Apotheken/ Drogerie/ Parfümerie (pharmacies, drugstores) | **209** | 351 | Retail (the pharmacies row: kept where the source covers general retail) |
| 17 | Baumarkt-/ Gartencenterspezifische Sortimente (DIY and garden) | **201** | 511 | Retail (NAICS 444) |
| 13 | Medien (electronics, phones, music and film) | **157** | 242 | Retail |
| 10 | Optik, Hörgeräte, Sanitätswaren, orthopädische Waren (opticians, hearing aids, medical supply) | **152** | 271 | Retail (the opticians row; Melbourne's exception is ANZSIC's, not this survey's) |
| 14 | GPK/ Geschenke/ Hausrat (glass, china, gifts, housewares) | **133** | 226 | Retail |
| 11 | Uhren/ Schmuck (watches and jewelry) | **105** | 156 | Retail |
| 19 | **Sonstige EH-Einrichtungen** (other retail facilities) | **94** | 188 | **Call 1** (recommended: Retail) |
| 9 | Sport/ Freizeit (sporting goods) | **93** | 166 | Retail |
| 18 | Möbel/ Antiquitäten (furniture, antiques) | **92** | 162 | Retail |
| 8 | Schuhe/ Lederwaren (shoes, leather goods) | **70** | 117 | Retail |
| 4 | Büroartikel, Schreibwaren, Zeitungen Zeitschriften (stationery, newsagents) | **56** | 100 | Retail |
| 6 | Spielwaren, Hobby (toys, hobby) | **53** | 83 | Retail |
| 15 | Haus-/ Heimtextilien (home textiles) | **51** | 99 | Retail |
| 5 | Bücher (books) | **43** | 72 | Retail |
| 12 | Elektro/ Leuchten (electrical, lighting) | **32** | 53 | Retail |
| 16 | Teppiche/ Bodenbeläge (carpets, flooring) | **27** | 47 | Retail |
| 3 | Blumen/ Zoo (florists, pet shops) | **27** | 70 | Retail |
| | **Total** | **3,153** | **5,573** | 3,153 kept on call 1 as recommended; 3,059 without group 19 |

- **What is absent, not excluded:** food service, personal services, and
  (from the goods-group list) car dealers and petrol stations. The page says
  what is missing; `docs/excluded_categories.md` carries it in Bremen's own
  section.
- **Floor-area classes (city):** 1 (0-100 m²) 2,127; 2 (101-400) 550; 3
  (401-800) 240; 4 (801-2,000) 167; 5 (2,001-4,000) 41; 6 (4,001-10,000) 22; 7
  (over 10,000) 5; 8 ("k.A.", not given) 1. **Every class is kept**: no city
  filters shops by size, and a hypermarket or DIY store is a storefront
  everywhere. "k.A." keeps its row (an unknown size is not a reason to drop a
  shop).
- The build writes the 19-code table as `pipeline/taxonomies/bremen_hwg.py`
  (a name for the build to settle) and runs `check_category_continuity.py`,
  which fails a new taxonomy until it answers every rule.

---

## Rail - BSAG trams

- **The operator's own lines and stops** (gate 3): BSAG's page "Linien und
  Fahrpläne" (`https://www.bsag.de/fahrplan/linien-und-fahrplaene`, read by
  curl 2026-10-05 with the project's user agent, HTTP 200) embeds its
  timetable index as JSON. The base timetable **`BSAG_S26C`, "Grundfahrplan",
  valid 17.8.2026 to 21.03.2027**, lists **8 tram lines**. The two other
  schedules in force (`BSAG_ACH-1`, Achterstraße works; `BSAG_A270`, the A270
  closure) carry buses only.
- **The fold:** both directions' stop names, the platform letter dropped
  (`Hauptbahnhof_A` to `_F` are one station), and "HBF-Nord/Messe" read as
  "Hauptbahnhof-Nord/Messe". The raw index holds 188 names over 350 stop
  keys; folded:

  | Line | Ends (BSAG) | Stops |
  |---|---|---|
  | 1 | Huchting - Bf Mahndorf | 44 |
  | 2 | Gröpelingen - Sebaldsbrück | 33 |
  | 3 | Gröpelingen - Weserwehr | 29 |
  | 4 | Arsten - Lilienthal | 49 |
  | 5 | Gröpelingen - Bürgerpark | 14 |
  | 6 | Flughafen - Universität | 25 |
  | 8 | Huchting - Kulenkampffallee | 27 (5 served one way only: a city-centre loop, Am Brill and Obernstr. one way, Falkenstr., Daniel-v.-Büren-Str. and Radio Bremen the other) |
  | 10 | Gröpelingen - Sebaldsbrück | 32 |

  **164 distinct stations on the network** (65 on more than one line; 253
  line-stops). These go in `OPERATOR_STATION_COUNTS` (whole lines, line 4
  with its Lilienthal stops), with `OPERATOR_COUNTS_SOURCE` naming the page,
  the timetable code, its validity and the date read. A difference from
  OSM's collapse (Aarhus's, by name within 200 m) is reconciled in config
  with its reason, never by loosening.
- **Outside the city, by name:** line 4 past Borgfeld, probably the 10 from
  Truperdeich to Lilienthal (Trupe and Falkenberg are Lilienthal localities).
  **The polygon decides**, and step 1 asserts the count. Every other line's
  ends (Huchting, Mahndorf, Sebaldsbrück, Weserwehr, Flughafen, Universität,
  Gröpelingen, Arsten) are Bremen districts.
- **Geometry and stops: OpenStreetMap through `osm-rail`**, on the shared
  `pipeline/osm_tram.py` (Odense's and Florence's wrappers), **one Overpass
  query for the city** (relations, stop nodes and the boundary), never
  parallel; after a 504 or 429 wait at least 60 s. No GTFS was probed: VBN's
  feed and Germany's national feed are not in this brief and go to the owner
  first.
- **Compare OSM's relations with BSAG's current lines before drawing**
  (`osm-rail`, Manchester's lesson): the timetable changed on 2026-08-17, so
  check line 5's end at Bürgerpark and line 8's loop against OSM's route
  relations; a relation that lags is a station question for config, not a
  page edit.
- **Frequency: not measured here.** The page holds no headways. Read each
  line's daytime headway at build from BSAG's own timetables (the PDFs this
  page links, on BSAG's host), else record the gap. **Call 2's 20-minute floor
  is for an outlier route** (`tram-city` section 1): line 5 is the short line
  to check, and only Bürgerpark is served by line 5 alone.
- **Colors:** OSM's `colour`, else the project's own palette (the kit's call
  3); `pipeline/linecolour.py`'s checks and `check_map_markup.py`; two lines
  with one color are refused. Lines 2 and 10 share both ends, so each still
  needs its own color, label and legend entry.

---

## Licence - CC BY, no version (read 2026-10-05; cite, do not re-read)

The verdict is staging's drafts entry "Band B's Japanese sources read",
its Bremen bullet (`docs/decisions_drafts/staging.md`), read through
GovData's CKAN and GDI-DE's CSW copy. **MetaVer answered HTTP 429 to both
readers and is not called.**

- **PERMITTED WITH CONDITIONS, display only.** "Creative Commons
  Namensnennung (CC-BY)", **no version** (DCAT-AP.de's unversioned
  `http://dcat-ap.de/def/licenses/cc-by`, linking
  `https://opendefinition.org/licenses/cc-by/`).
- **Rights holder: the Kommunalverbund Niedersachsen/Bremen e.V.** The
  Landesamt GeoInformation Bremen only hosts the file.
- **MUST DISPLAY:** "Quellenvermerk: Kommunalverbund Niedersachsen/Bremen
  e.V."; the licence title exactly as written; a link to that licence page;
  and that the data was changed.
- **MUST NOT** imply endorsement.
- **Not governing:** geo.bremen.de's CC BY-NC-ND page footer ("Sofern nicht
  anders angegeben", the site's own content) and the Kommunalverbund
  imprint's private-use clause (its own pages, incorporated nowhere).
- **Not this source's credit:** "© GeoBasis-DE / Landesamt GeoInformation
  Bremen" (the surveying offices' base data). Never put it on the survey.
- **Open:** the CC BY version (above), held by staging.
- The row goes in `docs/data_sources/germany.md` (the survey, and OSM's
  boundary and rail as support sources), with the verdict and the notice.
  Honour any removal request (the removal rule), from the Kommunalverbund or
  a business.

## Notices (the build claims the number in `docs/session_roles.md`)

- **PROPOSAL, for the drafts file** (a sentence no template covers; the
  required parts kept as written, the rest in American English):
  "Quellenvermerk: Kommunalverbund Niedersachsen/Bremen e.V. Retail survey
  "Einzelhandelsbestand in der Region Bremen 2022", licensed under Creative
  Commons Namensnennung (CC-BY) (https://opendefinition.org/licenses/cc-by/).
  This map has been changed from the source: its points are filtered to the
  City of Bremen, grouped into one category and aggregated into a heatmap.
  The Kommunalverbund Niedersachsen/Bremen e.V. has not reviewed or endorsed
  it." With the file's fetch date beside it.
- OSM's ODbL notice for the rail and the boundary (the site's own).

## The page (`docs/city_page_format.md`; the kit's template, Göteborg's shape)

- **Caption** (the kit's template): "Retail survey data from the
  Kommunalverbund Niedersachsen/Bremen e.V. (CC BY), surveyed **March to
  September 2022**; the tram lines and their stops from OpenStreetMap, fetched
  **{date}**."
- **The trams:** the kit's bullets, filled from step 1: eight BSAG lines,
  labeled; buses and the S-Bahn not drawn; "Bremen has no metro, so its trams
  are its rapid transit, as in Riga"; the halved-ring bullet if the median gap
  allows; the scope bullet ("Line 4 runs on into Lilienthal, so its {k} stops
  there are left out") and the "listed below" bullet.
- **The businesses** (proposals, flagged in the drafts file):
  - **"This map shows shops only, not three categories."** The template's
    one-bucket sentence, Göteborg's "food only" with the bucket changed: a
    departure, so a proposal. Then what the source holds: every shop the 2022
    regional retail survey counted, from grocers and bakeries to furniture and
    DIY stores. Then "So **restaurants, cafés, hairdressers and the like are
    not on this map**."
  - A dot shows the shop's goods group, never a name (the survey has none).
  - The in-ring share in words, last.
- **Reading the density:**
  - **"The survey dates from 2022."** It counted the shops open between March
    and September 2022, so shops that opened since then are missing, and some
    that have closed are still shown (Kansas City's sentence, filled: a
    proposal).
  - The template's "Read the density as a register, not a street survey" does
    not fit a survey. Proposal: "**Read the density as a 2022 survey.** It
    counts each shop once by its main goods group, whatever its size."
- `render_map_help("business layer")`, Yokohama's one-layer string.

## Privacy

- **No name, address or person field**, by construction of the public
  variant; the tooltip shows the goods group only (Florence's and Berlin's
  no-name precedent). Floor-area class is read to measure, and shown only if
  the owner asks.
- `python scripts/check_personal_exposure.py bremen` after step 2; the verdict
  in the drafts file and `docs/privacy_verdicts.md`.
- **Never print a row.** Field names, goods groups and counts only, in this
  brief, the drafts file and the commit messages.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for the Kommunalverbund's notice, **card
face or caption only** (CC BY asks for credit reasonable to the medium; a card
that travels without its caption carries "Quellenvermerk: Kommunalverbund
Niedersachsen/Bremen e.V." and the licence title on its face), the survey's
date on any card (the currency rule), and the open terms question: **the CC BY
version**. New inputs: a new city, a new taxonomy, a new `categories` value,
the notice, the licence row.

## What the build must still measure

- ⚠️ **The owner's calls 1-6 above**, and the open CC BY version.
- ⚠️ **The stations by polygon**: the Lilienthal stops (about 10), the count
  in the city (about 154), the median gap and the ring size; gate 3 against
  the table above.
- ⚠️ **The boundary cross-check**: the 3,153 "Bremen" rows inside the polygon,
  the other 2,420 outside.
- ⚠️ **Each line's daytime headway**, from BSAG's timetables, or the gap
  recorded.
- ⚠️ **OSM's relations against BSAG's 2026-08-17 lines**, line 5 and line 8
  first; colors.
- ⚠️ **The catch-all share** (`taxonomy_catchall`), the privacy verdict, the
  in-ring share, and `check_macro_labels.py` for the label.
- ⚠️ **A dated item in `docs/recheck_calendar.md`**: look for the 2027 survey
  from 2027-03-01; the five-year rule lapses on 2027-09-30.

```brief-checks
[
  {
    "id": "bremen-govdata-record",
    "claim": "THE BUSINESS LEG AND ITS LICENCE: GovData's CKAN record for the 2022 regional retail survey still names the Kommunalverbund as publisher, the 2022-03-01 to 2022-09-30 fieldwork, the geoportal zip, and 'Creative Commons Namensnennung (CC-BY)' with DCAT-AP.de's unversioned cc-by licence. A versioned licence appearing fails the check: the owner's open CC BY version question then has new evidence; re-read",
    "kind": "http_contains",
    "url": "https://www.govdata.de/ckan/api/3/action/package_show?id=einzelhandelsbestand-in-der-region-bremen-2022",
    "present": ["f6323bd1-bd38-4f72-a7ec-cb08209564ff", "Kommunalverbund Niedersachsen/Bremen e.V.", "Creative Commons Namensnennung (CC-BY)", "dcat-ap.de/def/licenses/cc-by\"", "geoportal.bremen.de/resources/data/Einzelhandelsbestand_reduziert.zip", "2022-03-01", "2022-09-30"],
    "absent": ["licenses/cc-by-4.0", "licenses/cc-by/4.0", "licenses/cc-by-3.0", "licenses/cc-by/3.0"]
  },
  {
    "id": "bremen-govdata-public-variant",
    "claim": "The record still says the public variant names only the trade, with range, address and sales area held in a secured variant (the privacy reading rests on the public file having no name or address), and that the survey repeats every five years (the refresh condition)",
    "kind": "http_contains",
    "url": "https://www.govdata.de/ckan/api/3/action/package_show?id=einzelhandelsbestand-in-der-region-bremen-2022",
    "present": ["Einzelhandelsbetriebe im engeren Sinn", "alle 5 Jahre", "nur mit Nennung der jeweiligen Branche"]
  },
  {
    "id": "bremen-bsag-timetable",
    "claim": "BSAG's lines-and-timetables page still embeds the base timetable BSAG_S26C (Grundfahrplan, valid 17.8.2026 to 21.03.2027), gate 3's source, with line 4's Lilienthal end and the other lines' ends named in the brief. If the code changes, re-read the per-line stop lists",
    "kind": "http_contains",
    "url": "https://www.bsag.de/fahrplan/linien-und-fahrplaene",
    "present": ["BSAG_S26C", "Grundfahrplan", "17.8.2026 bis 21.03.2027", "Truperdeich", "Lilienthal-Mitte", "Kutscher Behrens", "Weserwehr", "Kulenkampffallee", "Bf Mahndorf", "Arsten"]
  },
  {
    "id": "bremen-projected-crs",
    "claim": "Bremen's derived UTM zone is 32N (EPSG:32632); the build projects in EPSG:25832, the same zone on ETRS89 and the survey's own CRS (Odense's precedent); tram mode, one-bucket coverage, city scope",
    "kind": "utm_zone_from_longitude",
    "lon": 8.80,
    "expect": "EPSG:32632",
    "mode": "tram",
    "coverage": "one_bucket",
    "scope": "city",
    "crs": "EPSG:25832",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
