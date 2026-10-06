# Copenhagen (Regional) - build brief

**A regional extension of a built page, accepted by the owner on 2026-10-06**
(call 66, a-d, all as recommended): Copenhagen's page extended along the
Greater Copenhagen Light Rail, Hovedstadens Letbane (`docs/city_master_list.md`,
"Unscreened, ranked", item 1; `DECISIONS.md`, "The Greater Copenhagen Light
Rail extends Copenhagen's own page": no dot of its own, page 202 released).
Brief written 2026-10-06 by staging from cached files only: nothing
downloaded, no Overpass query, no Datafordeler call. Run
`python scripts/brief_check.py copenhagen_regional` before writing any code.

Read `regional-extension` (the steps this brief follows), then Copenhagen's
and Aarhus's briefs (`docs/build_briefs/copenhagen.md`, `aarhus.md`) and
`pipeline/copenhagen/`. Not `multi-source-city`: one register, cut by
kommune code (`regional-extension` Step 2, the first shape).

---

## The owner's calls (2026-10-06, call 66)

| | Call | What the build does |
|---|---|---|
| **a** | Extend Copenhagen's page with the Letbane, a line the page does not draw today | Draw it as a new line; the eight kommuner its 29 stops stand in join the business filter |
| **b** | The 8 suburban S-tog stations (Brøndby Strand, Brøndbyøster, Bagsværd, Kildebakke, Skovbrynet, Stengården, Sorgenfri, Virum) are IN only if measured passing the same spacing-and-frequency test Copenhagen's S-tog passed, otherwise OUT | Run the test below; spacing and coverage are measured here, frequency is the build's read |
| **c** | Albertslund (0165) stays out of the business filter; Glostrup Nord's ring may cross the line, as edge stations do elsewhere | `KOMMUNER` gets the eight, never 165 |
| **d** | Placement in the added kommuner on the owner's existing Datafordeler key, one DAR `Adressepunkt` file per kommune: one placement source on the page | The build fetches eight files through `fetch_sources.py`; the key stays in the owner's environment |

---

## The one-line summary

**Copenhagen's own CVR chain on eight more kommune codes, its own DAR join on
eight more `Adressepunkt` files, and one new OSM line already in Copenhagen's
rail cache: 29 Letbane stops (all eight kommuner), 3,907 storefronts before
placement, and the eight suburban S-tog stations decided by one frequency
read.** The rail leg needs no fetch at all: the Letbane's two relations and
every kommune polygon are in `data/copenhagen/raw/` since 2026-09-24.

| | Copenhagen (built) | **Copenhagen (Regional)** |
|---|---|---|
| Kommuner | 101 + 147 | **+ 173, 159, 163, 161, 187, 183, 153, 175** (ten) |
| Lines | Metro M1-M4, S-tog A, B, Bx, C, E, F, H | **+ Hovedstadens Letbane (L)** |
| Stations | 64 kept, 59 listed outside | **93** kept (the eight OUT) or **101** (IN); **53** or **45** listed outside |
| Storefronts | 14,922 placed (`baseline.json`) | **+ 3,907** before placement; 3,790 (97.0%) resolve to a DAR Husnummer |
| Placement | DAR via Datafordeler (98.3%) | the same, eight more `Adressepunkt` files |
| Register | CVR generation 505 | the same file, the same generation |

---

## Step 0 - is it an extension? (`regional-extension` Step 0)

1. **Lines already drawn: partly, and the owner chose it.** The Letbane is a
   line Copenhagen does not draw (`docs/commuter_rail_list.md`, Copenhagen's
   row); call (a) adds it. The S-tog stations in the eight kommuner are on
   lines the page draws.
2. **No bucket at a few stations only: yes.** The same CVR register gives the
   eight all three buckets.
3. **Station counts:** 29 stops in eight kommuner, 1 to 7 each; Rødovre's one
   is an add-on count, as Uiwang's.
4. **Terms: accepted.** CVR and DAR are the page's own (notices 30 and 31);
   OSM is the page's own.
5. **Extension, not a page: the owner's call** (2026-10-06, call 66 a).

---

## Rail - the Letbane, from Copenhagen's own cache

### The line

- **Open in full since 22 August 2026** (in part from 26 October 2025,
  Ishøj to Rødovre), 29 stations on 28 km: the operator's own pages, read by
  the probe 2026-10-06 (`dinletbane.dk/da/om-os/historik/`,
  `/da/driftsinformation/linjefoering-og-stationer/`).
- **Frequency, weekdays, read from the operator** (`dinletbane.dk/da/koereplan/`):
  service 05-24; about every 10 minutes 06-08, **every 5-8 minutes 08-17**,
  about every 10 minutes 17-24. It passes the light-rail test (15 minutes or
  better by day) at every stop: all trains serve all stations.
- **OSM carries it in Copenhagen's cached `osm_rail.json`** (OSM base
  2026-09-24T04:27:55Z): relations **19757374** (Lundtofte to Ishøj) and
  **19757375** (Ishøj to Lundtofte), `route=light_rail`, `ref=L`, 29 stop
  members each, the same 29 names both ways, `colour=#32ac5c`,
  `network=Movia`, `wikidata=Q10655459`, and **no `operator` tag** (it has
  `operator:wikidata` only).

### The whitelist key

**Whitelist on `route=light_rail` + `ref=L` + `wikidata=Q10655459`**, the
tag both relations carry. Copenhagen's S-tog rule keys on `operator=DSB`,
which the Letbane lacks; `ref=L` alone is unique in the bbox today
(Gribskovbanen is `L41`, Lokaltog `910`), but `wikidata` pins the system.
Never `network`: ⚠ **Copenhagen's config comment says every relation in the
bbox carries network "Takst Sjaelland"; the Letbane carries "Movia".**
Correct that comment when the switch goes in.

### Stops per kommune - MEASURED on OSM's kommune polygons

Placed by Copenhagen's own `kommuner.kommune_polygons()` on the cached
`osm_kommuner.json`, ETRS89 / UTM 33N. Matches the probe's counts; the
operator's pages name the kommune for three stops only (Brøndbyvester and
Kirkebjerg: Brøndby; Glostrup Nord - Hersted: Glostrup), so the polygon
test is the evidence for the rest.

| Kommune | Code | Stops (OSM names, route order north to south) | n |
|---|---|---|---|
| Lyngby-Taarbæk | 0173 | Lundtofte, Rævehøjvej, Anker Engelunds Vej - DTU, Akademivej - DTU, Fortunbyen, Lyngby Centrum, Lyngby | **7** |
| Gladsaxe | 0159 | Gammelmosevej, Buddinge, Gladsaxe Rådhus, Gladsaxevej, Gladsaxe Trafikplads, Dynamovej | **6** |
| Herlev | 0163 | Herlev Hospital, Herlev Bymidte, Herlev, Herlev Syd | **4** |
| Rødovre | 0175 | Rødovre Nord | **1** |
| Glostrup | 0161 | Glostrup Ejby, Glostrup Nord, Glostrup Hospital - Rigshospitalet, Glostrup | **4** |
| Brøndby | 0153 | Kirkebjerg, Brøndbyvester | **2** |
| Vallensbæk | 0187 | Delta Park, Vallensbæk, Strandhaven | **3** |
| Ishøj | 0183 | Ishøj Strand - Arken, Ishøj | **2** |

- **0 stops in Copenhagen or Frederiksberg** (as Copenhagen's build found),
  0 outside the eight. Kommune areas on OSM's polygons (gate them in
  `kommuner.AREA_KM2`): Lyngby-Taarbæk 38.8, Ishøj 26.5, Gladsaxe 24.9,
  Brøndby 21.0, Glostrup 13.3, Rødovre 12.2, Herlev 12.1, Vallensbæk 9.5 km².
- **Names:** OSM's names carry the operator's suffixes (" - DTU", " - Arken",
  " - Rigshospitalet"); OSM's "Glostrup Nord" is the operator's **"Glostrup
  Nord - Hersted"** (line map and stop page). A build-time detail: keep OSM's
  names, or override that one to the signed form.
- **Spacing:** consecutive gaps min 312, **median 834**, max 2,265 m (25.3 km
  straight-line); nearest-neighbor **median 670 m**. Copenhagen kept the
  standard rings (0.1 / 0.2 / 0.3 / 0.6 mi) on a 708 m median, and the halved
  ones were taken at 341-541 m: **standard rings stay.** Re-measure across
  the regional station set at step 1.
- **Line name and color:** one line, so the system's name, Odense's precedent
  (`"L": "Odense Letbane"`): **`LINE_NAMES["L"] = "Hovedstadens Letbane"`**,
  a permanent label and a legend entry. OSM's `#32ac5c` scores **11.4** from
  Metro M1's `#008d41` (CIE76; the floor is 10, Copenhagen moved pairs to a
  margin of about 13): it passes `linecolour.py`; lightening it is the
  build's call on Copenhagen's rule (the newer line moves, never the Metro).
- **Gate 3:** `OPERATOR_STATION_COUNTS["Letbane (network)"] = 29`, first-party
  ("29 stationer", the operator's line page); `EXPECTED_INSIDE_PER_LINE["L"] = 29`.

### Interchanges

Seven Letbane stops lie within 400 m of an S-tog station. Six share the
S-tog station's name and collapse by name (Copenhagen's rule, no alias):
**Lyngby** 165 m (A/E), **Buddinge** 64 m (B/Bx), **Herlev** 247 m (C/H),
**Glostrup** 181 m (B/Bx), **Vallensbæk** 137 m (A), **Ishøj** 80 m (A/E)
(point to point; step 1 prints the spread over every stop position and
exits above `COLLAPSE_MAX_SPREAD_M` = 400, so Herlev is the one to watch).
**Lyngby Centrum** is 357 m from Lyngby S-tog under its own name and stays a
station of its own.

### S-tog stations in the eight kommuner - 14, and call (b)

All 14 are in Copenhagen's committed `excluded_stations.csv` today. The six
interchanges above are kept with their Letbane stops. The other eight are
call (b): Brøndby Strand (A), Brøndbyøster (B) in Brøndby; Bagsværd (B),
Kildebakke (B/Bx), Skovbrynet (B), Stengården (B) in Gladsaxe; Sorgenfri and
Virum (A/E) in Lyngby-Taarbæk. Rødovre Kommune has no S-tog station (Rødovre
station is in Hvidovre and stays out).

### The S-tog test for call (b) - two parts measured, frequency to read

**The test is Copenhagen's own** (`pipeline/copenhagen/config.py`, "WHAT
COUNTS"; `scripts/measure_rail_backbone.py`'s precedents): inside the scope,
(1) station spacing near metro spacing, (2) frequency near metro frequency,
(3) coverage, districts no drawn station reaches. Copenhagen's S-tog passed
on a 1,227 m median, every line every 10 minutes through the day, and most
stations far from the Metro. **It has always been applied per line inside
the scope, never per station.**

Measured from the cached OSM (straight-line gaps between consecutive stops
of one relation per ref, both ends in scope; the "two kommuner" column
reproduces Copenhagen's 1,227 m within rounding, at 1,203 m):

| Line | Median gap, two kommuner | **Median gap, the ten** | Inside, ten (eight OUT) | Inside, ten (eight IN) |
|---|---|---|---|---|
| A | 1,132 m | **1,463 m** | 14 | 17 |
| B | 1,299 m | **1,313 m** | 14 | 19 |
| Bx | 1,310 m | 1,310 m | 14 | 15 |
| E | 1,129 m | **1,400 m** | 13 | 15 |
| C, F, H | 1,139 / 892 / 1,129 m | 1,185 / 892 / 1,306 m | 18 / 12 / 10 | 18 / 12 / 10 |

(The two-kommune "inside" counts, 11 / 12 / 12 / 17 / 11 / 12 / 9 for A, B,
Bx, C, E, F, H, reproduce `EXPECTED_INSIDE_PER_LINE` exactly; the Metro's
are unchanged by the extension.)

| Station | Line | Gaps to its neighbors | Nearest other drawn station |
|---|---|---|---|
| Brøndby Strand | A | Vallensbæk 2,225 m; Avedøre 2,190 m | Delta Park (L) 2,147 m |
| Brøndbyøster | B | Rødovre 1,160 m; Glostrup 2,670 m | Glostrup 2,670 m |
| Bagsværd | B | Skovbrynet 1,364 m; Stengården 1,279 m | Stengården 1,279 m |
| Kildebakke | B | Buddinge 907 m; Vangede 1,183 m | Buddinge 867 m |
| Skovbrynet | B | Hareskov 1,621 m; Bagsværd 1,364 m | Bagsværd 1,364 m |
| Stengården | B | Bagsværd 1,279 m; Buddinge 1,703 m | Bagsværd 1,279 m |
| Sorgenfri | A | Lyngby 1,907 m; Virum 1,788 m | Lyngby 1,746 m |
| Virum | A | Sorgenfri 1,788 m; Holte 1,311 m | Sorgenfri 1,795 m |

- **(1) Spacing:** the eight's own gaps have a median of 1,492 m; lines A, B
  and E run at 1,313-1,463 m inside the ten, between Copenhagen's S-tog
  (1,227 m) and São Paulo's Linha 9 (1,778 m, drawn on frequency).
  **Within the precedents.**
- **(3) Coverage:** **none of the eight has another drawn station within
  800 m** (Kildebakke's 867 m is the nearest). **Passes.**
- **(2) Frequency: the build's read**, from DSB's own published S-tog
  timetables (dsb.dk), weekday daytime, for lines A, B and E at the eight.
  That lines A, B and E run every 10 minutes through the day to these
  stations is ASSERTED (general knowledge, and Copenhagen's "every line every
  10 minutes" inside the city); Bx is a peak line and Kildebakke is on B as
  well. Quote the timetable where the decision is recorded.
- **The rule for the result:** a line passes if its weekday daytime service
  at the eight is every 10 minutes (Copenhagen's figure), since spacing and
  coverage already pass. A passing line's stations among the eight are IN; a
  failing line's stay OUT and are listed in `excluded_stations.csv` with the
  reason (the test, not the kommune). Route membership would keep them
  otherwise, so OUT needs an explicit list in the config. **A per-station
  reading** (Brøndby Strand's 2.2 km gaps on both sides would fail it on
  Rio's Santa Cruz precedent) **departs from the test's precedent and goes
  to the owner with that precedent named.**

### Rings that cross out of scope - call (c), and three more kommuner

The 0.6 mi (966 m) outer ring reaches kommuner outside the ten at 12 stops.
Businesses there are never counted: the filter is CVR's own kommune code,
never a polygon (Copenhagen's Hellerup precedent).

| Stop | Kommune outside | Share of the outer ring |
|---|---|---|
| **Glostrup Nord** | **Albertslund (0165)** | **38%** (the stop is 11 m from the boundary) |
| Glostrup Hospital - Rigshospitalet | Albertslund | 13% |
| Gammelmosevej | Gentofte (0157) | 24% |
| Buddinge | Gentofte | 17% |
| Gladsaxe Rådhus | Gentofte | 4% |
| Rødovre Nord | Ballerup (0151) | 12% |
| Herlev Syd | Ballerup | 11% |
| Lundtofte, Fortunbyen, Lyngby, Lyngby Centrum, Herlev | Rudersdal, Gentofte, Ballerup | 1% or less |

**Call (c) names Albertslund.** Gentofte, Ballerup and Rudersdal hold no
Letbane stop and are in exactly Albertslund's position, so the brief applies
(c) to them: out of the filter, disclosed in What Is Excluded as halved
rings. *Flagged for review time, not asked.* Gentofte's and Ballerup's S-tog
stations (Vangede, Dyssegård, Ballerup, Malmparken and the rest) stay listed
outside.

---

## Business leg - CVR generation 505, eight more codes

### Measured 2026-10-06 (staging, counts only)

Run through `pipeline/countries/denmark_register.py`'s own `_premises()`
and `_parent_forms()` with `KOMMUNER` set to the eight, the taxonomy
`denmark_db25`, Copenhagen's `CATCH_ALL_EXCLUDE`; `heavy_job.py` label
`copenhagen-regional-cvr-measure`, **measured peak 0.70 GB**. No name,
person, address or identifier was printed.

| Stage | The eight |
|---|---|
| Active production units with a current `beliggenhedsadresse` | **43,270**: Lyngby-Taarbæk 11,022 · Gladsaxe 9,462 · Rødovre 5,455 · Brøndby 4,677 · Herlev 4,623 · Glostrup 3,486 · Ishøj 2,561 · Vallensbæk 1,984 |
| hovedbranche / name / parent / legal form found | 100.0% each; no parent ceased |
| DB25 divisions 47 / 56 / 96 | 4,480 |
| structurally excluded | 424 |
| after `filter_to_storefront()` | 4,056 |
| **`969900` dropped** (Copenhagen's verdict) | 149 (3.7%), personally owned **83%** against 44% overall |
| **Storefronts** | **3,907** |

**The catch-all verdict carries over on the eight's own numbers**:
Copenhagen's 82% against 39%, Aarhus's 78% against 45%. The other catch-alls
stay kept, as in Copenhagen: 477800 219, 561190 183, 472700 82, 475590 39,
476990 12, 471200 11.

| Kommune | Code | Retail (47) | Food service (56) | Personal services (96) | **Total** | Personally owned | Shown by address | Address id | To a Husnummer |
|---|---|---|---|---|---|---|---|---|---|
| Lyngby-Taarbæk | 173 | 533 | 214 | 132 | **879** | 34.0% | 34.2% | 96.8% | 96.8% |
| Gladsaxe | 159 | 488 | 130 | 161 | **779** | 49.9% | 50.4% | 98.1% | 98.1% |
| Rødovre | 175 | 400 | 110 | 124 | **634** | 40.7% | 41.2% | 94.0% | 94.0% |
| Herlev | 163 | 249 | 70 | 91 | **410** | 43.4% | 43.7% | 99.3% | 99.3% |
| Glostrup | 161 | 228 | 66 | 91 | **385** | 38.2% | 39.0% | 97.1% | 97.1% |
| Brøndby | 153 | 246 | 61 | 70 | **377** | 52.3% | 53.3% | 97.3% | 97.3% |
| Ishøj | 183 | 140 | 62 | 57 | **259** | 38.2% | 38.6% | 96.5% | 96.5% |
| Vallensbæk | 187 | 111 | 29 | 44 | **184** | 50.0% | 50.5% | 98.4% | 98.4% |
| **Eight** | | **2,395** | **742** | **770** | **3,907** | **42.5%** | **42.9%** | **97.0%** | **97.0%** |

(Buckets by DB25 division; the taxonomy's own labels decide at build.)

### Placement - call (d): DAR, one `Adressepunkt` file per kommune

- **The chain is Copenhagen's:** CVR `Adressering.Adresse` -> DAR `Adresse`
  -> `Husnummer` -> `Adressepunkt` (EPSG:25832, converted on read).
  `Adresse` and `Husnummer` are national and cached (DAR generation 761,
  2026-09-18); `Adressepunkt` is cached for 0101 and 0147 only.
- **Measured to the Husnummer:** 3,790 of 3,907 storefronts (97.0%) carry an
  address id, and **every one of them** resolves to a current Husnummer with
  an `adgangspunkt`: **2,815 distinct address-point ids** the eight new files
  must hold. Placement is at most 97.0% (Copenhagen's own: 98.3%); the build
  prints the real rate.
- **The eight files:** `Adressepunkt_0153`, `_0159`, `_0161`, `_0163`,
  `_0173`, `_0175`, `_0183`, `_0187` (`DAR_KOMMUNER` padded; `KOMMUNER`
  unpadded, CVR's form). **Never `_0165`** (call c).

### The fetch, and its four traps

`python pipeline/copenhagen/fetch_sources.py` with `REGIONAL = True`, run
with `DATAFORDELER_API_KEY` set in the environment by the owner. The script
reads the key from the environment, never writes it and scrubs it from
every message (`_scrub`); the build session never sees it.

1. **It plans only the eight `Adressepunkt` files** if the manifest is
   intact: the six CVR files, the national `Adresse` and `Husnummer` and
   Copenhagen's two `Adressepunkt` files are cached and recorded, so `want()`
   skips them. Read the printed plan before answering yes: **eight files,
   each a few MB zipped** (0101 was 10.3 MB, 0147 1.2 MB).
2. **The national fallback.** The DAR loop asks per kommune only if
   **all** ten codes are listed (`all(per)`); one unlisted code makes it plan
   the NATIONAL `Adressepunkt` instead, a download this brief does not name.
   Stop and ask the owner if the plan shows it.
3. **Mixed DAR generations, with no guard.** The CVR generation guard covers
   CVR only. The new files will be a later DAR generation than 761; the join
   keys are DAR `id_lokalId`s, stable across generations, so the loss is the
   points re-created since 2026-09-18. Record each file's generation from
   the manifest in the drafts entry and on the page's data age.
4. **OSM and provenance.** `fetch_osm()` runs first and reads Copenhagen's
   two OSM caches (`pipeline/osm.py` returns a cached file; **no Overpass
   query**, which is right: the Letbane and every polygon are in them). It
   then rewrites the committed `outputs/copenhagen/provenance.json`; its diff
   must be the eight new files only. **Never `--refresh-cvr`**: the CVR and
   DAR caches are national and shared with Aarhus and Odense.

**Currency:** CVR generation 505 expired on Datafordeler on 2026-09-25
(`manifest.json`). Build on 505 with its date on the page, as Aarhus and
Odense did; the currency rule's clock is five years.

---

## Licenses and notices - all already recorded, no new verdict

- **CVR** (Datafordeler, CC BY 4.0, credit Det Centrale Virksomhedsregister):
  notice **30**. **DAR** (Datafordeler, CC BY 4.0, credit Klimadatastyrelsen):
  notice **31**. Neither is per kommune; no new read
  (`docs/data_sources/denmark.md`, Copenhagen's rows).
- **OpenStreetMap**: notice 1 and the rail-geometry notice, whose text names
  "Copenhagen's Metro and S-tog lines and stations and the municipal
  boundaries used to select them" (`app/components.py`): it gains the
  Letbane. A rendered string; the wording is a drafts proposal.
- **Notices 30 and 31 name their cities** in the title, the text and
  `_DENMARK` ("spelled as app/cities.py spells them"): they follow the
  rename. A title such as "(Copenhagen (Regional), Aarhus, Odense)" nests
  parentheses; the form is a drafts proposal.
- **The operator's pages** (dinletbane.dk) are cited for the stop count and
  the frequency, not reused as data: no row and no notice, Aarhus's
  Midttrafik precedent. Movia's or Rejseplanen's GTFS is **not** used
  (Copenhagen's 2026-09-24 call stands).
- **Rows in `docs/data_sources/denmark.md`:** Copenhagen's CVR row gains the
  eight codes and counts; its DAR row gains the eight `Adressepunkt` files
  and their generation; its OSM rail row gains relations 19757374 and
  19757375; the boundary row gains the eight kommuner.

## Privacy

- **Copenhagen's name rule, unchanged** (`denmark_register.build_storefronts`):
  a personally owned business (legal forms 10, 15, 30), any name with the
  `v/` marker, a franchisee's store-number name or a blank trade name is
  shown by its street address. Measured on the eight: **trade name on 2,229,
  address on 1,678 (42.9%)**: personally owned 1,659, `v/` on a company
  form 2, a store-number name 17, blank 0.
- **`coNavn` never arrives** (`FORBIDDEN_COLUMNS`, asserted in step 2).
- ⚠ **`build_storefronts` prints up to five store-number names** ("e.g.")
  in its log. They are company names by the rule's own definition, but keep
  that log out of anything published.
- **Run `python scripts/check_personal_exposure.py copenhagen`** on the
  regional file (`processed/regional/` while the switch is on) and record
  the verdict in the drafts file and `docs/privacy_verdicts.md`.

---

## Steps, in order

1. **The city alone at zero drift.** Add `REGIONAL = False` to
   `pipeline/copenhagen/config.py`, with `KOMMUNER`, `DAR_KOMMUNER`,
   `DATA_PROCESSED` (`data/copenhagen/processed/regional/`), the sanity box,
   `LINE_NAMES`, `LINE_COLOURS`, `EXPECTED_INSIDE_PER_LINE`,
   `OPERATOR_STATION_COUNTS` and `kommuner.AREA_KM2` following it (Belo
   Horizonte's and Los Angeles' configs). Commit it off, then
   `python scripts/heavy_job.py run --label "copenhagen drift" --session <you>
   -- python pipeline/drift_check.py copenhagen`: no drift, then
   `git checkout -- outputs/` if files show modified. Copenhagen has a
   `baseline.json`; no first baseline is needed.
2. **Fetch** the eight `Adressepunkt` files (above, with its traps).
3. **The S-tog frequency read** for call (b), from DSB's timetables; record
   the eight's verdict (by line) in the drafts file before step 1 runs on.
4. **Switch on:** steps 1-3 with `REGIONAL = True`. Step 1 whitelists the
   Letbane on `ref` + `route` + `wikidata`; step 2 filters on the ten codes;
   the sanity box widens to the ten kommuner (their polygons span about
   55.59-55.81 N, 12.21-12.69 E; Copenhagen's box stops at 12.43 E and
   55.76 N), never the rail bbox. The drift check reports only the
   extension's changes: stations 64 -> 93 or 101, excluded 59 -> 53 or 45,
   the storefronts, the ring counts. Re-record the baseline deliberately.
5. **Page:** the same file and slug (`app/pages/27_Copenhagen_Heatmap.py`,
   `copenhagen`); the name becomes **"Copenhagen (Regional)"** in
   `app/cities.py`; `blurb` gains the Letbane, `placement` and `data_age`
   (CVR 505; DAR 761 and the new files' generation) re-stated, `mode` stays
   `metro`. Macro label re-scored at 375, 768 and 1200 (the pill widens;
   the staged Letbane pill was already dropped from the overview branch).
   Text in `docs/city_page_format.md`'s format.
6. **What Is Excluded:** rename Copenhagen's section; name the eight
   kommuner with their counts, the `969900` drop, the address-shown count,
   the out-of-scope rings (Albertslund, Gentofte, Ballerup, Rudersdal), and a
   **Stations.** line: the Letbane's 29 stops drawn and ringed, and the eight
   S-tog stations IN or OUT with the test's reason.
   `docs/map_inconsistencies.md`: the rename **settles theme 5's row**
   ("Copenhagen covers Frederiksberg unlabeled"); Copenhagen joins the
   "(Regional)" list.
7. **Gates:** `check_personal_exposure.py copenhagen`, `check_provenance.py`
   (names Copenhagen OK; notices 30, 31 in bijection with `_NOTICES`),
   `check_scope_disclosure.py`, `check_ring_shares.py --write` (Copenhagen's
   row only), `check_macro_labels.py`, `check_deploy_imports.py`. Land at
   review time only; **reboot: yes** (`app/cities.py` changes); deploy-verify
   `city-added`. Downstream: an extension always counts (outputs, notices 1,
   30, 31, macro facts, ring shares, the Visuals card's name).

## Owner calls

**None open.** Call 66 (a-d) settles the extension. Two items go to review
time as flags: (c) applied to Gentofte, Ballerup and Rudersdal as to
Albertslund, and the notice wordings above (drafts proposals). A per-station
S-tog reading, if the build finds it needed, is a new call.

## What the build must still measure

- DSB's weekday daytime frequency on A, B and E at the eight (call b).
- The placement rate on the eight new files (at most 97.0% here), and the
  storefronts dropped by the widened sanity box (expected none).
- The regional station spacing and ring choice (standard expected), the
  collapse spreads at the six interchanges (Herlev's 247 m first).
- Ring shares per kommune, and the privacy verdict on the regional file.

```brief-checks
[
  {"id": "cphreg-excluded-total", "claim": "Copenhagen's committed map lists 59 stations of drawn lines outside Copenhagen and Frederiksberg, the list the fourteen S-tog stations in the eight kommuner come from", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "expect": 59},
  {"id": "cphreg-eight-broendby-strand", "claim": "Brondby Strand (S-tog A, Brondby) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Brøndby Strand", "expect": 1},
  {"id": "cphreg-eight-broendbyoester", "claim": "Brondbyoster (S-tog B, Brondby) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Brøndbyøster", "expect": 1},
  {"id": "cphreg-eight-bagsvaerd", "claim": "Bagsvaerd (S-tog B, Gladsaxe) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Bagsværd", "expect": 1},
  {"id": "cphreg-eight-kildebakke", "claim": "Kildebakke (S-tog B/Bx, Gladsaxe) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Kildebakke", "expect": 1},
  {"id": "cphreg-eight-skovbrynet", "claim": "Skovbrynet (S-tog B, Gladsaxe) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Skovbrynet", "expect": 1},
  {"id": "cphreg-eight-stengaarden", "claim": "Stengarden (S-tog B, Gladsaxe) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Stengården", "expect": 1},
  {"id": "cphreg-eight-sorgenfri", "claim": "Sorgenfri (S-tog A/E, Lyngby-Taarbaek) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Sorgenfri", "expect": 1},
  {"id": "cphreg-eight-virum", "claim": "Virum (S-tog A/E, Lyngby-Taarbaek) is outside Copenhagen's map today: call (b)", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Virum", "expect": 1},
  {"id": "cphreg-interchange-lyngby", "claim": "Lyngby S-tog, collapsed with the Letbane's Lyngby stop (165 m), is outside the map today", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Lyngby", "expect": 1},
  {"id": "cphreg-interchange-buddinge", "claim": "Buddinge S-tog, collapsed with the Letbane's Buddinge stop (64 m), is outside the map today", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Buddinge", "expect": 1},
  {"id": "cphreg-interchange-herlev", "claim": "Herlev S-tog, collapsed with the Letbane's Herlev stop (247 m), is outside the map today", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Herlev", "expect": 1},
  {"id": "cphreg-interchange-glostrup", "claim": "Glostrup S-tog, collapsed with the Letbane's Glostrup stop (181 m), is outside the map today", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Glostrup", "expect": 1},
  {"id": "cphreg-interchange-vallensbaek", "claim": "Vallensbaek S-tog, collapsed with the Letbane's Vallensbaek stop (137 m), is outside the map today", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Vallensbæk", "expect": 1},
  {"id": "cphreg-interchange-ishoej", "claim": "Ishoj S-tog, collapsed with the Letbane's Ishoj stop (80 m), is outside the map today", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Ishøj", "expect": 1},
  {"id": "cphreg-albertslund-stays-out", "claim": "Albertslund station stays listed outside: call (c) keeps Albertslund out of the filter", "kind": "row_count", "path": "outputs/copenhagen/excluded_stations.csv", "column": "station", "equals": "Albertslund", "expect": 1},
  {"id": "cphreg-utm-33", "claim": "The ten kommuner stay in UTM zone 33 (EPSG:25833, Copenhagen's own): Ishoj Kommune's western edge, 12.209 E, is east of 12 E. The check derives the WGS84 twin", "kind": "utm_zone_from_longitude", "lon": 12.209, "expect": "EPSG:32633"},
  {"id": "cphreg-letbane-29-stations", "claim": "The operator's line page lists 29 stations, Lundtofte to Ishoj, with Glostrup Nord - Hersted: gate 3's first-party count", "kind": "http_contains", "url": "https://dinletbane.dk/da/driftsinformation/linjefoering-og-stationer/", "present": ["29 stationer", "Glostrup Nord - Hersted", "Lundtofte", "Ishøj Strand"]},
  {"id": "cphreg-letbane-frequency", "claim": "The operator's timetable page: every 5-8 minutes on weekdays 08-17, about every 10 minutes either side - the light-rail test passes at every stop", "kind": "http_contains", "url": "https://dinletbane.dk/da/koereplan/", "present": ["hvert 5.-8. minut"]},
  {"id": "cphreg-letbane-open-in-full", "claim": "The Letbane opened along its full length on 22 August 2026 (the operator's history page)", "kind": "http_contains", "url": "https://dinletbane.dk/da/om-os/historik/", "present": ["22. august 2026"]}
]
```
