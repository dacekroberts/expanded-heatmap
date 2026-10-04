# Antwerp — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band B,
food service with food shops as a Retail partial (owner, 2026-10-03); KBO
measured the same evening and Antwerp kept at B on FAVV, KBO not used (owner,
"i accept all calls including the download"). Brief written 2026-10-03.** Run
`python scripts/brief_check.py antwerp` before writing any code. The trail:
`docs/decisions_drafts/staging.md`, 2026-10-03 "The sweep's first group
banded", "Seven licence reads for the sweep's first group" and "KBO measured:
Belgian bands kept"; the master list's Band B row
(`docs/city_master_list.md`).

⚠️ **The first Belgian build and the first city on two new sources.** Ghent
(`docs/build_briefs/ghent.md`) shares every business-side step: write the
FAVV-to-VKBO join once, as a country module both call. **Göteborg is the page
template** (food service plus food shops, one bucket); **Den Haag is the
precedent for a tram network with tram tunnels** drawn as `tram`. Read with
`tram-city`, `add-city`, `address-join` and `publish-city`.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | Every route De Lijn's feed draws here is `route_type` 0, the premetro included: trams in tunnels, not a metro. Den Haag's precedent (its tram tunnel, `tram`). `metro` would put a metro dot on a city that draws no metro |
| **`coverage`** | **`one_bucket`** ("Food premises only") | Food service plus food shops, and food shops count as food (`tram-city` section 5, Göteborg) |
| **Scope** | **Stad Antwerpen**, its nine districts **plus Borsbeek** (merged into Antwerp on 2025-01-01; measured below) | The FAVV join is placed by VKBO's points; Antwerp's own polygon cuts them |
| **Lines drawn** | De Lijn trams **1, 2, 4, 6, 7, 8, 10, 11, 12, 24, A3, A9** in the feed's own colors | Every route `route_type` 0 in the Antwerp group; lines 3, 5, 9 and 15 are not in the current feed (below) |
| **Rings** | **halved**: 163 stations by name (148 inside), **median gap 279 m inside** | The owner's spacing rule (under about 550 m) |
| **Call (approved): caterers** | **Out**: PL83 Traiteur, 332 placed | The category rules (R1, Coquitlam's precedent): FAVV cannot separate a caterer with a counter from one without |
| **Call (approved): sole traders** | **Every food premises placed**; no name shown | FAVV carries no names and VKBO's points come under Flanders' license (owner, 2026-10-03, call 5) |
| **Call (new, recommend): thinning** | **No thinning**, every stop ringed | The tram list's standing call (no stop thinning on trams-only maps). The screen had named `docs/sub_transit_line_filters.md` for the surface stops; Antwerp's network is dense across the whole city, not Muni Metro's sparse corridor with far branches. A departure from the screen's line, so the owner's |
| **Call (new, recommend): stop names** | **Merge platform names into one station** ("perron N", "Metro Perron X", "Metro", case) | De Lijn's feed has no `parent_station`; `tram-city` section 2 sends a merge of differently named stops to the owner |
| **Call (new, recommend): complementary retail** | **Out**: PL29 with AC95, 238 placed | "Retail as a complementary activity": food sold beside a non-food main trade, not a food shop |

---

## The one-line summary

**FAVV's food register, joined on the establishment number to Flanders'
geocoded KBO copy, places 3,100 of 3,231 food-service premises (95.9%) and
1,764 food shops, with no name anywhere in the chain. Twelve De Lijn tram
lines from De Lijn's own feed, every 10 minutes by day. The work is the join,
Borsbeek, and a network the current timetable runs in a works shape.**

---

## Scope — the city with Borsbeek

- **Postcodes (15):** 2000, 2018, 2020, 2030, 2040, 2050, 2060, 2100
  (Deurne), 2140 (Borgerhout), **2150 (Borsbeek)**, 2170 (Merksem), 2180
  (Ekeren), 2600 (Berchem), 2610 (Wilrijk), 2660 (Hoboken). The screen used
  the first fourteen; **Borsbeek joined Antwerp on 2025-01-01** and the
  build adds it.
- **Measured 2026-10-03 (VKBO WFS, count-only `resultType=hits`):** 1,876
  VKBO rows carry postcode 2150; **1,701 already file under Antwerp's NIS
  11002**, 175 still under Borsbeek's old 11007. FAVV labels 2150's rows
  "Borsbeek (Antw.)" (46) or "Antwerpen" (91). **FAVV in 2150: 110
  establishments, 27 food service, 24 food shops, 2 caterers** (85 with a KBO
  number, 25 FAVV-internal), not yet joined.
- **So:** FAVV is selected by the 15 postcodes; VKBO is paged for NIS 11002
  **and** 11007; the points are kept inside the merged city's polygon (the
  boundary from the build's one Overpass query, or the source the build's
  `osm-rail` step already reads). Assert the 2150 rows arrive.
- **CRS:** UTM 31N, **EPSG:32631** (4.40° E). VKBO's points are Lambert 72
  (EPSG:31370): reproject, never measure in either geographic system.
- **Region** `"Europe"`; country `"Belgium"` (new in `app/cities.py`).

---

## Rail — De Lijn's own GTFS

### The source, and why not OSM

- **De Lijn's static GTFS through the Belgian Mobility Open Data Portal**
  (`data.belgianmobility.io`, the four operators' common portal):
  `https://api-management-discovery-production.azure-api.net/api/gtfs/feed/delijn/static`,
  **keyless** (the anonymous tier, 100 requests a day), 222,204,417 bytes,
  **feed window 2026-10-03 to 2026-11-30** (`feed_info.txt`), calendar
  dates to 2026-11-30. De Lijn's own portal (`data.delijn.be`) wants an API
  key; this route does not.
- **License stated: CC BY 4.0**, the portal's Terms of Use (effective
  2026-01-01, art. 3), each operator the sole licensor; attribution (art. 4)
  "Source: [PTO Name] – Open Data – [Date of dataset update]", and when
  modified "Contains data originally published by [PTO Name], modified by
  [User Name]". The national access point (`transportdata.be`, CKAN
  `de-lijn-gtfs-static`) lists the dataset with no license and its resource
  as ODC-BY. **A `licence-read` runs before the feed is used** (one source
  per call); a row in `docs/data_sources/belgium.md` either way.
- **Why the feed:** it is current, open and the operator's own, and it shows
  what OSM cannot: which lines run this timetable period. OSM stays the
  fallback (`osm-rail`) if the license read fails, as for Olomouc.
- **Rolling:** `fetch_sources.py` downloads it at every build (`tram-city`
  section 4). Its `stop_times.txt` is **1.79 GB**: read it in chunks,
  filtered to the tram trips, through `heavy_job.py` (the measurement below
  peaked at 0.88 GB in 2M-row chunks).

### Lines, stops and headways (measured 2026-10-03 on the feed, Tuesday 2026-10-13)

Stops are collapsed by name with platform suffixes stripped (the call above),
per line over the whole line. "Inside" is by the locality the feed prefixes
to each stop name (Antwerpen, Berchem, Borgerhout, Deurne, Hoboken, Merksem,
Wilrijk, Ekeren, Borsbeek): the build cuts by polygon.

| Line | Feed color | Stops | Inside | Daytime headway (09-16) |
|---|---|---|---|---|
| 1 | `#8C2B87` | 20 | 20 | 10 |
| 2 | `#15882E` | 29 | 29 | 10 |
| 4 | `#00A6E2` | 26 | 26 | 10 |
| 6 | `#E6007E` | 26 | 26 | 10 |
| 7 | `#0056A4` | 47 | 42 (89%) | 10 |
| 8 | `#FC95C5` | 23 | 22 (96%) | 10 |
| 10 | `#C8D300` | 33 | 30 (91%) | 10 |
| 11 | `#FFFFFF` (text `#822A3A`) | 22 | 22 | 7.5-8 |
| 12 | `#E40521` | 21 | 21 | 10 |
| 24 | `#69C0AC` | 24 | 23 (96%) | 10 |
| A3 | `#FFCC00` | 37 | 28 (76%) | 10 |
| A9 | `#A85E24` | 26 | 23 (88%) | 10 |
| **Network** | | **163 stations** | **148** | |

- **15 stops outside**: Mortsel 9, Wijnegem 3, Wommelgem 2, Boechout 1.
  Every line keeps 76% or more inside, so **every line is drawn to its end**
  and those stops are listed as outside (Göteborg's 4 and 12, Den Haag's
  tram 1).
- **The same read for Tuesday 2026-11-24** gives 165 stations (150 inside):
  24 and A3 gain a stop each. Recount at build on the feed then current.
- **Median nearest-neighbour gap: 279 m inside (287 m network)**, so halved
  rings; recompute on the stations drawn.
- **Frequency:** every line every 10 minutes by day (11 every 7.5-8). No
  route needs the 20-minute floor.

### The works shape — read before step 1

- **Lines 3, 5, 9 and 15 are not in the feed**, and no tram stop on the
  left bank (Linkeroever, postcode 2050) is served on either date read.
  **A3 (P+R Merksem - P+R Boechout) and A9 (Wijnegem - Berchem Station)** run
  on the right bank, along the routes of 3 and 9. The screen's list (2, 3, 5,
  6, 8, 9, 10 and 15 in the premetro) predates this.
- **The rule is the category rules' "station closed for works"**: drawn as
  the timetable runs; left-bank stations not drawn, not ringed, listed in
  `excluded_stations.csv` as closed for works with De Lijn's reopening date,
  named on the page, a dated `PLAN.md` item, and step 1 stops once the feed
  serves them again. **Read De Lijn's own notice for the reason and the date**
  (not read here), and what De Lijn calls A3 and A9 on its line pages: the
  label is the public name.
- **One stop on lines 2, 4, 7 and 8 carries "(tijdelijk afgeschaft)",
  temporarily discontinued, in its feed name.** Check `pickup_type` and
  `drop_off_type`: if no trip boards there, it is the same rule.

### Gate 3 and colors

- **Gate 3:** the operator's own per-line counts. `delijn.be`'s line pages
  are script-rendered (the static HTML carries no stop list); read them in a
  browser at build (one browser-using agent at a time), else
  `OPERATOR_COUNTS_GAP`. The feed is De Lijn's data but is the build's own
  input, so it is not an independent count.
- **Colors:** twelve distinct feed colors. **Line 11 is white**: check its
  contrast on both map themes (Göteborg's line 1; Lille's darkening if it
  fails). `pipeline/linecolour.py`'s checks and `check_map_markup.py`.
- **Not drawn:** buses; NMBS-SNCB trains (national rail, not tested here);
  the Kusttram (another region).

---

## Business leg — FAVV joined to VKBO

### The two sources

1. **FAVV's operator list** (Federal Agency for the Safety of the Food
   Chain): `https://www.static.favv.be/bo-documents/inter_actieve_actoren_EN.csv`,
   **cached** at `data/belgium/raw/` with its meta JSON (87,947,437 bytes,
   Last-Modified 2026-09-28, latin-1, 310,806 rows; the code descriptions
   are French even in the EN file). Weekly. **Do not download it again for
   the build's first pass**: `fetch_sources.py` re-fetches only when the
   build is ready to refresh, and records the date. One row per operator x
   place x activity x product; **no name, no street, no point**.
   `OP N° Unique Id` is the KBO establishment number (2xxxxxxxxx) or a FAVV
   number (9xxxxxxxxx, mostly farms; they cannot join).
2. **VKBO** (Digitaal Vlaanderen's enriched KBO, "VKBO ondernemingen en
   vestigingseenheden V3"): every active establishment unit with a Flemish
   address, geocoded to an Adressenregister position. **Use the WFS
   `https://geo.api.vlaanderen.be/VKBO/wfs`, `VKBO:Vkbo`, with
   `propertyName` limited to `Ondernemingsnr`, `Type_onderneming`,
   `KBO_NISCODE`, `AR_postcode` and `SHAPE`.** Never request a name,
   `Telefoonnummer` or `Email`. **Never use the OGC API Features endpoint**:
   it ignores `properties=` and filters and returns every column, names
   included. Page politely (5,000 a page, 1.5 s apart; about 25 minutes for
   both cities), cached per city by `fetch_sources.py`; `numberMatched`
   caps at 10,000, so count by paging.

### Classification (FAVV place `PAP PLA` x activity `PAP ACT`, per establishment, first match wins)

- **Food service:** PL92 Restaurant, PL12 Débit de boisson (bar or café),
  PL46 Friterie, PL70 Pita-house.
- **Food shops (the "Food shops" layer, as on Göteborg's page):** PL9 butcher,
  PL10 bakery, PL72 fishmonger (each not AC94 ambulant), and PL29 retailer
  with AC96, AC68 or AC93.
- **Out:** PL83 caterers (approved); PL29/AC95 complementary retail (call
  above); PL88 vehicles and AC94 ambulant sales; schools, crèches, other
  collective kitchens, rest homes, hospitals, central kitchens (R1);
  wholesalers, manufacturers, transport, warehouses, traders, farms,
  apiarists; PL23 B&B (lodging); PL93 pharmacies (a food register's
  pharmacies are out); vending (PL57, PL39); food banks; service providers.

### Measured (the screen, 2026-10-03; 14 postcodes, before Borsbeek)

| Bucket | FAVV establishments | Joined | **Placed** | Rate |
|---|---|---|---|---|
| Food service | 3,231 (restaurants 2,406, bars and cafés 546, friteries 154, pita 125) | 3,184 | **3,100** | **95.9%** |
| Food shops | 1,833 (retailers 1,392, bakeries about 226, butchers about 173, fishmongers 42) | 1,812 | **1,764** | **96.2%** |
| Caterers (out) | 354 | 349 | 332 | 93.8% |
| Complementary retail (out) | 253 | 251 | 238 | 94.1% |

- **Plus Borsbeek** (27 food service, 24 food shops before the join).
- **The misses:** food service 47 (28 FAVV-internal numbers, 19 KBO numbers;
  1 of a sample of 19 found anywhere in VKBO, in Kontich): units VKBO does
  not hold, not units placed elsewhere. Bars and cafés place lowest (92%),
  mostly on `(0,0)` points.
- **`(0,0)` is VKBO's placeholder** for an address the Adressenregister did
  not match: **7,001 of 142,008 NIS 11002 rows**. Not null: drop it by a
  bounding box. Real points span X 142,832-159,587, Y 189,996-229,745
  (Lambert 72); inspect the handful south of the city.
- **Bakery and butcher splits move by 1-3 between runs** (an establishment
  with several retail places takes the first in set order): fix the order in
  code so the build is deterministic.
- **Personal names: none by construction.** FAVV has no name column and the
  VKBO request omits every name, so a tooltip shows the FAVV category only
  (Berlin's "no names" precedent). `check_personal_exposure.py antwerp`
  still runs, a row in `docs/privacy_verdicts.md`.
- **Currency:** FAVV lists only current registrations, weekly; VKBO lags
  KBO by 1-3 days and holds active units only. Both drop closures: the
  one-clock rule passes. The page gives FAVV's extract date.
- **KBO's own file is not used here** (owner, 2026-10-03): its retail and
  personal-service layers are not added.

### The page (`docs/city_page_format.md`; `tram-city` section 6)

- **Captions:** "Food premises from FAVV-AFSCA, extract of **{date}**,
  placed on VKBO's address points, extracted **{date}**; the tram lines and
  their stops from De Lijn's open data, fetched **{date}**." (Den Haag's
  two-source shape; the feed clause replaces "OpenStreetMap", as France's
  template does.)
- **The narrower scope, one-bucket form:** "**This map shows food only, not
  three categories.** Its dots are the food businesses registered with
  FAVV-AFSCA, Belgium's food safety agency: restaurants, bars and cafés,
  friteries and pita shops, and food shops (bakers, butchers, fishmongers and
  other food retailers), shown as Food service and Food shops." Then
  Göteborg's "So **clothes shops, hairdressers and the like are not on this
  map**." (the template's braces filled; no read-back needed)
- **Proposals, not template** (flag in the drafts file): the left-bank
  closure sentence with its date; "A dot shows the type of business, never
  its name"; a sentence that the dots are registered premises placed at
  their registered address (about 4 in 100 food-service premises could not
  be placed).
- `render_map_help('business categories (Food service and Food shops)')`,
  Göteborg's string as built (`app/pages/137_Goteborg_Heatmap.py`).

---

## Licenses and notices

- **FAVV operator list: permitted with conditions**, CC BY 4.0 ("Creative
  Commons Naamsvermelding 4.0 Internationaal" on the dataset page). Credit
  with the extract date, no implied endorsement, nothing misleading. **Link
  FAVV-AFSCA's home page only** (a deep link asks for the webmaster's say
  first). The site terms' prior approval for downloadable documents is read
  as the Dutch text limits it, to brochures and the like (owner). Proposed
  notice (a proposal for the owner): "Antwerp's food businesses are from
  FAVV-AFSCA's list of operators, extracted on {date}, licensed under CC BY
  4.0. Modified by this project: food-service and food-shop activities
  selected and placed on VKBO's address points. FAVV-AFSCA does not endorse
  this map."
- **VKBO: permitted with conditions**, Modellicentie voor gratis hergebruik
  v1.0. **Its prescribed credit, verbatim:** "publieke KBO gegevens, verrijkt
  met adressen uit het Vlaamse Adressenregister", **plus the extract date**
  (which also meets KBO's art. 2.8 should the federal terms ever reach the
  KBO-derived fields). KBO's purpose limit binds registrants, not VKBO's
  reusers.
- **De Lijn GTFS:** CC BY 4.0 under the portal's terms, pending its
  `licence-read`: "Source: De Lijn – Open Data – {feed date}" and the
  modification line. **No De Lijn logo.**
- **OpenStreetMap:** the basemap notice only, unless the boundary comes from
  OSM (then ODbL, notice 1).
- **Notice numbers:** claimed by the Belgium kit from the next free ones
  (`docs/session_roles.md`'s claims sentence), shared with Ghent where the
  wording is one sentence for both (FAVV, VKBO, De Lijn).

## Downstream

When the build pushes, Visuals and Analytics are told
(`docs/session_roles.md`, "Downstream sessions"). **For each notice it adds**
(FAVV's, VKBO's, De Lijn's), **the build records in its drafts file whether
the notice belongs on a card's face or in a caption only**, from the
license's own words on where it must appear, and **any open terms question**
(De Lijn's feed until its read lands). It names the downstream inputs the
branch changes: a new city and a new country, `outputs/antwerp/`, the city
registry, the notices, three license rows, a new taxonomy or country module,
and a new category answer (FAVV's codes) for `check_category_continuity.py`.

## What remains for the build

- 🚨 **Borsbeek:** postcode 2150 in the FAVV set, NIS 11007 in the VKBO
  paging, the merged polygon; re-measure the join with it.
- 🚨 **The works shape:** the left-bank closure under the closed-for-works
  rule, De Lijn's reason and date, A3 and A9's public names, the
  discontinued stop's boardability.
- ⚠️ **The owner's calls:** thinning, the platform-name merge, complementary
  retail; the notice wording.
- ⚠️ **`licence-read` of De Lijn's feed** (and OSM as the fallback if it
  fails); license rows for FAVV, VKBO and the feed in
  `docs/data_sources/belgium.md`.
- ⚠️ **Gate 3** from De Lijn's line pages in a browser, or the gap recorded.
- ⚠️ **Line 11's white**; `(0,0)` dropped; deterministic bakery and butcher
  order; the OGC API never touched.
- ⚠️ **The FAVV taxonomy module** answers every row in
  `docs/category_rules.md` (`check_category_continuity.py`).
- `check_personal_exposure.py antwerp`, `check_provenance.py` names Antwerp
  OK, `check_scope_disclosure.py` passes (the one-bucket gap and the
  left-bank stations in Antwerp's own sections).

```brief-checks
[
  {
    "id": "antwerp-favv-dataset-page",
    "claim": "FAVV's open-data page still names CC BY 4.0 (in Dutch), weekly updates, and the four language files the build reads (the EN one is cached)",
    "kind": "http_contains",
    "url": "https://favv-afsca.be/nl/open-data/favv-operatoren",
    "present": ["Naamsvermelding 4.0 Internationaal", "Wekelijks", "inter_actieve_actoren_EN.csv"]
  },
  {
    "id": "antwerp-vkbo-licence-and-credit",
    "claim": "VKBO's metadata record names the Modellicentie gratis hergebruik v1.0 and carries the prescribed Dutch credit line the page must show verbatim",
    "kind": "http_contains",
    "url": "https://metadata.vlaanderen.be/srv/api/records/5c874565-a669-4744-93ef-0bc00df722a6",
    "present": ["modellicentie-gratis-hergebruik/v1.0", "publieke KBO gegevens, verrijkt met adressen uit het Vlaamse Adressenregister"]
  },
  {
    "id": "antwerp-vkbo-borsbeek-under-11002",
    "claim": "Borsbeek (postcode 2150) merged into Antwerp on 2025-01-01, and VKBO already files most of its units under Antwerp's NIS 11002 (1,701 of 1,876 on 2026-10-03; 175 still under 11007). A count-only WFS query; it fails if no 2150 row files under 11002",
    "kind": "http_contains",
    "url": "https://geo.api.vlaanderen.be/VKBO/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=VKBO%3AVkbo&resultType=hits&filter=%3Cfes%3AFilter+xmlns%3Afes%3D%22http%3A%2F%2Fwww.opengis.net%2Ffes%2F2.0%22%3E%3Cfes%3AAnd%3E%3Cfes%3APropertyIsEqualTo%3E%3Cfes%3AValueReference%3EKBO_NISCODE%3C%2Ffes%3AValueReference%3E%3Cfes%3ALiteral%3E11002%3C%2Ffes%3ALiteral%3E%3C%2Ffes%3APropertyIsEqualTo%3E%3Cfes%3APropertyIsEqualTo%3E%3Cfes%3AValueReference%3EKBO_Postcode%3C%2Ffes%3AValueReference%3E%3Cfes%3ALiteral%3E2150%3C%2Ffes%3ALiteral%3E%3C%2Ffes%3APropertyIsEqualTo%3E%3C%2Ffes%3AAnd%3E%3C%2Ffes%3AFilter%3E",
    "present": ["numberMatched="],
    "absent": ["numberMatched=\"0\""]
  },
  {
    "id": "antwerp-delijn-feed-current",
    "claim": "De Lijn's static GTFS on the Belgian Mobility portal is keyless and current (calendar_dates ran to 2026-11-30 when measured); a rolling feed, fetched at every build",
    "kind": "gtfs_calendar_window",
    "url": "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/delijn/static",
    "expect": "current"
  },
  {
    "id": "antwerp-projected-crs",
    "claim": "Antwerp's projected CRS is UTM 31N (EPSG:32631)",
    "kind": "utm_zone_from_longitude",
    "lon": 4.40,
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
