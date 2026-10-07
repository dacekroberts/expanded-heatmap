# Timișoara — build brief

**Step 0 measured 2026-10-07 (staging), on the owner's saved DSVSA Timiș
files, one OSM address query, one OSM tram query and SMTT's own line pages.**
Run `python scripts/brief_check.py timisoara` before writing any code. A
trams-only city on Bucharest's business route (`docs/build_briefs/bucharest.md`)
and the `tram-city` skill. Written at the owner's request ("write the briefs
for those three now", 2026-10-07). Builds wait for the owner's go.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **Band** | **C** (from D) | The D blocker is gone: the files are saved. The next blocker is **placement**. The OSM address join places **51.6%** of the kept premises, against the "about 70%" a page has needed (Ino, Macau) and Bucharest's 74.9%. Rail and data both pass, so placement is the first blocker. See call 1 |
| **`mode`** | **`tram`** | Street trams, no metro (the light-rail test: never left the tram list) |
| **`coverage`** | **`one_bucket`** | DSVSA registers food units only: Food service plus Food shops. Food shops count as food (`tram-city` section 5), as on Bucharest's and Göteborg's pages |
| **Scope** | **Municipiul Timișoara**, OSM relation **6927733** (admin_level 8) | Every OSM tram stop lies inside it. The register is county-wide, so it is cut to the municipality (see "Which rows are in the city") |
| **Lines drawn** | Trams **1, 2, 4, 7, 8, 9** (SMTT's six running lines) | Lines 5, 6a and 6b have OSM relations but no stops and no timetable on SMTT's programme page. They go in `NOT_DRAWN` (call 5) |
| **Rings** | **0.05 / 0.1 / 0.2 / 0.3 mi** | Median nearest-stop gap **336 m** over the six refs' 68 OSM stop names (328 m over all 74). The spacing rule gives halved rings. Recompute on the stations actually drawn |
| **Projected CRS** | **EPSG:32634** (UTM 34N, 21.23° E) | Not Bucharest's 35N |
| **Region** | `"Europe"` | |
| **Template** | **Bucharest** (`pipeline/bucharest/`, `taxonomies/romania_dsvsa.py`) for the register, names and join. **Aarhus** / `pipeline/osm_tram.py` for the tram step 1, or **Manchester's routing** (`pipeline/countries/uk.py`) if call 4 goes that way | |

**Calls** are numbered under "Open calls" at the end. Each has a
recommendation and its tradeoff.

---

## The one-line summary

**Bucharest's register in a county shape, with a thinner address layer and
a tram network that has moved on from its OSM relations.** The DSVSA files
read cleanly and are mostly current. But OSM holds **11,268** address objects
in Timișoara (Bucharest: 145,892), so the join places about half the city's
food premises. OSM's line relations for 1, 2, 4 and 8 also follow routes SMTT
no longer runs.

---

## Business leg — DSVSA Timiș, food only

### The saved files

**Saved by the owner** from DSVSA Timiș's "Unități înregistrate" page in
their own browser (`docs/decisions_drafts/staging.md`, "Band D, the first
three Romanian cities' files complete"). The files are old-format **XLS**
(OLE2), not Bucharest's XLSX, so the build reads them with `xlrd`, not
`openpyxl`.

**The two lists:**

- **Animal-origin**: 9 files in `data/timisoara/raw/`. Each says
  "actualizare **20.07.2026**" on row 10, except 16, which states no date. The
  page lists them under 21/07/2026.
- **Non-animal**: 9 files in `raw/non-animal/`. Each says "data ultimei
  actualizări: **07.08.2026**".

**The layout:**

- Every sheet has 17 letterhead rows, then the **header on row 18**.
- The columns are `Nr. crt.`, `Denumirea unității`, `Adresa`,
  `Numărul de înregistrare și data înregistrării` and, in most files,
  `Categorie unitate`. The order differs: in N01, N34, N35 and N36 the
  category comes before the registration number.
- **No locality column** and no coordinates. The locality is written inside
  `Adresa`.

"Rows" below means rows with a name or an address. Several files pad their
numbering with empty numbered rows, which are not counted.

| File | Bytes | sha256 (prefix) | Rows | Closed | Active | Active in the city |
|---|---|---|---|---|---|---|
| A01 Carmangerii (pork butchers) | 117,248 | `a14aa6447b33b877` | 61 | – | 61 | 24 |
| A02 Măcelării (butchers) | 131,584 | `58fdb6e351e71612` | 150 | – | 150 | 63 |
| A11 Pescării (fishmongers) | 107,008 | `251fe4fb1540c9b0` | 37 | – | 37 | 27 |
| A16 Miere (honey shops) | 104,448 | `4841052d68df15aa` | 5 | – | 5 | 4 |
| A19 Restaurante, **six sheets** | 1,572,352 | `cf471c98ffa8f95e` | 5,399 | – | 5,399 | 3,154 |
| · BAR | | | 1,126 | | | 589 |
| · BUFET | | | 339 | | | 163 |
| · FAST FOOD | | | 2,341 | | | 1,471 |
| · RESTAURANTE | | | 963 | | | 612 |
| · RULOTE (trailers) | | | 445 | | | 177 |
| · SNACK BAR | | | 185 | | | 142 |
| A20 Pizzerii | 99,840 | `2e7c4f73d26e4ec8` | 173 | – | 173 | 85 |
| A23 Cofetării-patiserii | 137,216 | `508f9e50d641f368` | 123 | – | 123 | 63 |
| A25 Magazine alimentare (food shops) | 985,600 | `43f0f00f21815be0` | 3,897 | – | 3,897 | 1,749 |
| A26 Hipermarket-supermarket | 156,672 | `9c8c789f498d3f18` | 278 | – | 278 | 158 |
| N01 Fabricarea pâinii (bakeries) | 111,616 | `fa807aa9e96fad29` | 124 | 21 | 103 | 7 |
| N02 Prăjituri, patiserie (pastry) | 124,416 | `fbf4dd1e142d6107` | 199 | 26 | 173 | 26 |
| N03 Pâine, prăjituri, patiserie | 182,784 | `13dbf9e2047c8afa` | 441 | 53 | 388 | 58 |
| N24 Fabricare înghețată (ice cream) | 94,208 | `f90b6c8d2dd70ff1` | 48 | 3 | 45 | 5 |
| N33 Comerț cu amănuntul (retail) | 314,368 | `0af3d11501f33eb7` | 1,259 | 35 | 1,224 | 102 |
| N34 Hypermarket-supermarketuri | 87,040 | `6372fed464d982ab` | **0** | | | |
| N35 Bar | 180,224 | `3ee8412936adb681` | 326 | – | 326 | 38 |
| N36 Cantine, catering, restaurant vegan | 87,040 | `1bd9699318ee1e04` | **0** | | | |
| N40 Comerț cu amănuntul, congelate (frozen) | 99,328 | `a039f1e8de910497` | 92 | 3 | 89 | 7 |
| **Total** | 4,893,568 | | **12,612** | **141** | **12,471** | **5,570** |

**Animal-origin 10,123 rows, non-animal 2,489.**

⚠️ **File 19 is six sheets, one per category.** A seventh, `Sheet1`, is
empty. Bucharest's `read_file()` exits when a second sheet holds data, so
Timișoara's step 2 must **read every sheet and take the sheet name as the
category**. These sheets carry no category text of their own. In FAST FOOD
the registration number sits in the column headed `Categorie unitate` (1,930
rows), so the build reads columns by content there, not by header.

⚠️ **N34 and N36 are empty**: a header and 100 numbered rows with no name or
address. **N36 "Cantine catering restaurant vegan" holds nothing to split**,
so the planned split of canteens and catering from vegan restaurants is moot
for this edition. The build should still check the next edition.

### Active and closed: not Bucharest's shape

- **No ANULATE section anywhere.** No file has Bucharest's cancelled block,
  and no row is struck through or filled red in the animal-origin files.
  **The animal-origin list marks no closures at all.** The sheets read as a
  list of registered units, and nothing says whether a closed unit is dropped
  or kept. Registration years run to 2026 in most files (A26: 173 rows
  registered or renewed in 2026). **The currency rule** (the source drops
  closed businesses) is therefore **not established** for this list (call 3).
- **The non-animal list marks closures in its category column**: **ÎNCHIS**
  ("closed") on 141 rows (N01 21, N02 26, N03 53, N24 3, N33 35, N40 3). Step
  2 drops them.
- **N33 also has cell fills**: 45 rows filled red and 52 white that are not
  marked ÎNCHIS. Their meaning is not stated. The brief does not drop them,
  and the build reads a few in the owner's presence (call 3).

### Which rows are in the city

The lists cover all of Timiș County. The locality is the first part of
`Adresa`.

- **5,570 active rows name Timișoara.** In 5,542 of them the name falls in the
  first 15 characters, and only 2 of them are a street named after the city.
  These are the in-city rows. 5,327 come from the animal-origin list and only
  243 from the non-animal one.
- **The out-of-city rows name their locality.** Lugoj 691, Dumbrăvița 305,
  Moșnița 194, Giroc 179, Sânnicolau Mare 177, Jimbolia 177 and so on. Only
  about 24 begin with a street and name no place.
- 🚨 **The non-animal list writes "TM" where the animal list writes the
  city.** 1,301 active rows (N33 776, N35 194, N03 152, N02 87, N40 57, N24
  20, N01 13, A25 2) begin "TM" and name no city.
  - 468 of them go straight on to a street word.
  - Only 11 name one of the 44 nearby places the script listed.
  - **Read strictly, the non-animal list is almost absent from the city**: 38
    of N35's 326 bars, 102 of N33's 1,224 shops. Read as Timișoara, it adds
    about **1,160 premises**.
- **The join cannot settle it.** Stripped of "TM" and joined to Timișoara's
  addresses, the TM rows place at 45.1% (552 of 1,225 premises). But a
  control does almost as well: TM rows that do name a village place at
  **23.4%** (15 of 64), because Romanian street names repeat from town to
  town (call 2).

### De-duplication

One unit can be registered in several files or sheets: a hypermarket's fast
food, butcher and food counter, or a bar also registered for fast food.
**Bucharest's rule applies: merge on the name without its legal form, plus the
parsed street and number.**

- **5,570 in-city rows merge to 5,089 premises.**
- 323 keys appear in two or more files or sheets. The commonest pairs:
  - FAST FOOD with A26: 115;
  - FAST FOOD with A25: 56;
  - A02 with A26: 37;
  - A02 with FAST FOOD: 33;
  - BAR with FAST FOOD: 31.
- 96 rows repeat a key within one file.

### Buckets, on Bucharest's file rule

The file decides the bucket. **SHOP_FIRST** applies: a premises in A25, A26 or
N33 is a food shop, even if it also has a food-service registration. The
taxonomy needs Timiș's own file codes (A19's sheets as sub-codes; N35 for
Bucharest's N36 bars; N40 for Bucharest's N42 frozen counters), so
`romania_dsvsa.py` gains a city-keyed file table or a second module. That is
a shared-module change and goes to the app/chrome role.

| | In-city premises | Placed | Share placed |
|---|---|---|---|
| **Food service**: A19 BAR, FAST FOOD, RESTAURANTE, SNACK BAR; A20; N24; N35 | **2,620** | 1,442 | 55.0% |
| **Food shops**: A01, A02, A11, A16, A23, A25, A26, N01-N03, N33, N40 | **2,160** | 1,047 | 48.5% |
| **BUFET only** (call 6) | **145** | 53 | 36.6% |
| *Out: RULOTE only (trailers)* | *164* | | |
| **Kept, BUFET included** | **4,925** | **2,542** | **51.6%** |

These figures read the city strictly: only rows that name Timișoara, with
none of the TM rows.

### Left out, each on its precedent (`docs/category_rules.md`)

- **RULOTE (trailers)**: 445 rows, 164 in-city premises in no other sheet.
  **Out**: "Mobile units, kiosk carts, vending machines". This is Bucharest's
  `rulota` rule (owner, 2026-09-29). A trailer that also holds a fixed
  registration elsewhere stays, under its fixed one.
- **Canteens and catering**: **out** on Bucharest's precedent (files 21 and
  31, owner 2026-09-28; R1). Timiș's N36 is empty, so nothing is lost now.
  The category-text rule ("bufet de incintă", "catering" alone) cannot fire
  here, because Timiș's category column is nearly empty: 4 non-blank values
  in A23, none in A19.
- **Pastry labs**: Bucharest drops a row whose category text says
  "laborator". Timiș's N01-N03 carry no category text, so that rule has
  nothing to read. N01-N03 are **kept** as bakeries and pastry shops, as
  Bucharest kept its N01-N03.
- **Closed (ÎNCHIS) rows**: out, 141.
- **N34 and N36**: empty.

### Address shape (5,570 in-city active rows)

- **House number found: 5,315 (95.4%)**, using Bucharest's `parse_address`
  after the locality is stripped. 5,087 write "nr".
- **Street type:**
  - Strada 3,502;
  - Calea 648;
  - Bulevardul 525;
  - Piața 389;
  - Aleea 129;
  - none 335.
- Blocks are written on 133 rows and apartments on 232. 299 rows carry a
  market or mall word, the kind of address Bucharest's fishmongers missed on.

### Names and personal exposure

Counts only. No name was printed or stored.

- **The name column is `Denumirea unității`**: legal entities, as in
  Bucharest. 4,854 of the 5,570 in-city rows carry SRL and 112 SA.
- **Sole-trader forms (PFA, II, IF, ÎI and their long forms)**: 157 rows
  (2.8%), by Bucharest's `SOLE_TRADER` pattern. **2** more are companies
  named only as a person (`is_person_name`). Bucharest's figures were 308
  and 6.
- **The owner's rule applies unchanged** (2026-09-28/29): the company name
  without its legal form, and the category alone for a sole trader or a
  person-named company. `Adresa` never reaches the map.
- `check_personal_exposure.py timisoara` runs at the build, sole-trader
  suffixes first, with the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

---

## Placement — the OSM address join, measured

| | |
|---|---|
| Route | **OSM address objects** (`addr:street` + `addr:housenumber`) in relation **6927733** |
| Supply | **11,268** objects: 779 street keys, 10,543 street+number pairs. 709,060 bytes as CSV, overpass-api.de, 2026-10-07 (scratch only; the build fetches its own dated copy in `fetch_sources.py`) |
| Matcher | **Bucharest's**, imported read-only from `pipeline/bucharest/step2_clean_businesses.py`: `parse_address`, the type-kept key, the tolerant key and `one_site` (150 m hops, 600 m wide). There is no sector test: one city, no sectors. The locality ("Timișoara", "Mun.", "jud. Timiș", postcodes) is stripped first |
| Licence | **ODbL 1.0**, notice 1. The rail is OSM too, so no new licence is added |

**In-city premises (5,089), strict reading:**

| Tier | Premises |
|---|---|
| exact street and number | 1,991 |
| whole number (14A → 14) | 88 |
| tolerant street key, one street only | 519 |
| **Placed** | **2,598 = 51.1%** (kept set: **2,542 of 4,925 = 51.6%**) |
| street found, number not in OSM | 1,232 |
| no street match | 713 |
| two places (not one site) | 304 |
| no house number | 242 |

- **Control**: with the street-type test off, the join places 2,553 (50.2%),
  with ambiguous rising to 392. The type test costs nothing here and holds
  back wrong matches.
- **By file**, placed of in-city premises:
  - A19 1,616 of 3,028;
  - A25 788 of 1,716;
  - A26 102 of 155;
  - N33 54 of 100;
  - A11 11 of 27.
- **What misses is OSM, not the register.** "Street found, number missing" is
  the largest class: OSM has the street but not that house. The register's
  addresses carry a number 95% of the time. **Street-level placement is not
  proposed** (Bucharest's precedent: a boulevard is kilometres long).
- **Stand-in ring share**: 69.7% of placed premises lie within 0.3 mi of a
  stop on the six running refs, and 91.1% within 0.6 mi. **This reads high**:
  OSM's addresses cluster in the centre, along the tram lines, so the placed
  half is not a fair sample.
- **ANCPI** has no reachable geospatial address service (Bucharest's brief).
  The city's catalogue (36 datasets, enumerated 2026-10-07) holds no address
  layer.

---

## Rail — trams, OSM against SMTT

### What OSM holds (one query, 2026-10-07, overpass.kumi.systems after a 504 on overpass-api.de)

- **18 `route=tram` relations, 9 refs: 1, 2, 4, 5, 6a, 6b, 7, 8, 9**, two
  per ref. All carry `network=S.T.P.T.`; a few carry the operator's full
  name. **None carries a `colour`**, so the project's own palette is needed
  (`tram-city` call 3).
- 7 `route=train` relations (CFR) fall in the same box. They are not drawn.
- **74 stop names network-wide, all 74 inside relation 6927733**, so there is
  no stub and no out-of-city section. No name spreads over 200 m. No stop
  member lacks a name.
- On the six running refs: **68 stop names, median gap 336 m.** 6 names are
  served only by 5, 6a or 6b.

| Ref | OSM relation names (termini) | Stop names |
|---|---|---|
| 1 | Gara de Nord ⇄ Stația Meteo | 22 |
| 2 | Shopping City ⇄ Stația Meteo | 29 |
| 4 | Piața Gheorghe Domășnean ⇄ Calea Torontalului | 19 |
| 5 | Ronaț ⇄ Meteo | 25 |
| 6a / 6b | Piața Maria ⇄ Banatim (loop pair) | 18 / 17 |
| 7 | Dâmbovița ⇄ Calea Torontalului | 26 |
| 8 | Gara de Nord ⇄ Piața Gheorghe Domășnean | 16 |
| 9 | Gara de Nord ⇄ Piața Gheorghe Domășnean | 18 |

### What SMTT runs (READ, smtt.ro, plain GET, 2026-10-07)

SMTT is the metropolitan transport authority: Asociația de Dezvoltare
Intercomunitară, operator STPT.

**Its home page lists six tram lines:**

- **1** Gara de Nord – Piața Gh. Domășneanu (AEM);
- **2** Shopping City – Calea Torontalului (Ciocanul);
- **4** Calea Torontalului – Piața Gh. Domășneanu (AEM);
- **7** Bulevardul Dâmbovița – Calea Torontalului;
- **8** and **9** Gara de Nord – Ciarda Roșie, as the home page names them.
  The line pages name the far end differently: 8 ends at AEM (Dräxlmaier),
  9 at Piața Gh. Domășneanu.

The "Program Tramvaie" page carries the same six. **Lines 5, 6a and 6b
appear only in the site menu**, and their pages list no stops.

**Per line, distinct stop names on the programme page** ("Stații utilizate",
both directions), with each direction's page count:

| Line | Distinct names | Each direction |
|---|---|---|
| 1 | 16 | 13 |
| 2 | 23 | 21 |
| 4 | 24 | 23 |
| 7 | 29 | 26 |
| 8 | 18 | 16 |
| 9 | 21 | 17 |

**Network-wide: 60 names**, the master list's figure. SMTT qualifies names by
direction ("Piața Sfânta Maria (16 Decembrie 1989)" and "(Gheorghe Doja)"),
so **60 names is not 60 stops**. Gate 3 needs a collapse rule (call 4).

🚨 **OSM's relations lag SMTT's lines** (`osm-rail`, the Manchester section).

- **Line 1**: SMTT runs it Gara de Nord – Liviu Rebreanu – Piața Gh.
  Domășneanu. OSM's relation runs through the centre to Meteo (Hotel
  Continental, Prefectura, Traian, UMT).
- **Line 2**: SMTT's ends at Calea Torontalului. OSM's ends at Meteo.
- **Line 4**: SMTT's runs Calea Torontalului – Piața Crucii – Banatim – AEM.
  OSM's runs from Piața Gh. Domășnean through the centre (3 August 1919,
  Hotel Continental, Prefectura, Traian).
- **Line 8**: SMTT's runs to AEM via Banatim. OSM's ends at Piața Gh.
  Domășnean.
- **Lines 7 and 9** agree, apart from name forms:
  - SMTT abbreviates ("N. Bălcescu", "A. Mocioni", "C. Brâncoveanu");
  - OSM writes names in full ("Nicolae Bălcescu");
  - SMTT appends the cross street ("Gheorghe Lazăr (Cetății)"), where OSM
    has "Cetății".

  Every stop SMTT lists has an OSM node somewhere. The ones not found by base
  name are abbreviations or cross-street forms that an alias table resolves.

### Frequency

**Not read.** SMTT's line pages load their departure times through a
scripted call (`admin-ajax.php`, behind a reCAPTCHA key), which is not a
plain GET, so it was not made. **ASSERTED**: none recorded on the master list
or here.

READ on SMTT's home page: news items of 2025-09-08 add trams on lines 7 and 2
"in the school period".

The build reads headways from the city's trips file (call 4) or from SMTT's
timetables in a browser. Street trams have no frequency gate. The page
states the waits (`tram-city` section 1).

### The city's own feed (named, not fetched)

The master list's "city's own CC BY feed" is the city catalogue's
**`mobility`** dataset, "Transportul Public" (Primăria Timișoara). The
catalogue reads `license_id: cc-by`, "Creative Commons Attribution", with
**no version stated**. **It is JSON-LD, not GTFS**:

- `mobility-stops.jsonld`: 421,996 B;
- `mobility-routes.jsonld`: 38,257 B;
- `mobility-trips.jsonld`: 8,878,950 B.

All three were updated 2026-08-25. A separate `lista-statii` dataset (STPT,
`stops.txt`, 85,614 B, 2026-06-29) **states no licence**. Neither was
fetched.

---

## Licences

- **DSVSA Timiș: SILENT, on Bucharest's precedent.** Bucharest's position was
  "silent, the absence established": no terms page, a privacy policy silent
  on reuse, a website "toate drepturile rezervate" footer, not on
  `data.gov.ro`. It takes notice **67**, displayed by choice.
  - **Not checkable from here**: every county DSVSA host answers scripts with
    503 or 403 (master list, 2026-10-06). As instructed, this session did not
    touch it.
  - **The owner's browser can confirm** that `timis.dsvsa.ro` carries the
    same two policy links and no terms page. Until then the position is
    Bucharest's, by the same publisher's template.
- **OpenStreetMap**: ODbL 1.0, notice 1. It covers the address join, the
  boundary and (unless call 4 picks the feed) the tram geometry and stops.
- **The city's `mobility` dataset**: CC BY as the catalogue declares it. The
  version, attribution wording and any terms by reference are **unread**: one
  `licence-read` before use.
- **SMTT's pages**: footer "(©) 2025 - Informațiile aparțin SMTT". Read for
  line lists and counts only, never republished.

---

## Open calls

Precedent first; each has a recommendation and its tradeoff.

1. **Band C, on placement.** **Recommend C**, with two routes to B for the
   owner:
   - **(a)** a second placement layer. The city's GIS or the Timiș County
     geoportal may hold address points; neither has been looked for. Read
     each as `reprobe-city` would.
   - **(b)** the owner accepts about 52% with the gap disclosed, Bucharest's
     wording extended.

   *Tradeoff*: no published city sits this low. Bucharest is 74.9% and
   Incheon 71.3%. Macau's 70% went to C, then R, on a thin ring map. Read
   this way, half of Timișoara's food premises would be missing, unevenly,
   mostly away from the centre.
2. **The "TM" rows (1,301 active, about 1,160 premises).** **Recommend the
   strict reading** (only rows naming Timișoara) **until the build reads the
   TM rows' address shape with the owner**. That means a count of how many
   name a locality after "TM", read in the files, never printed here.
   *Tradeoff*: strict is safe, but leaves the non-animal list (bars, shops,
   bakeries) at 243 rows in the city. If "TM" means Timișoara, the city's
   bars are under-counted about fivefold. The join cannot decide: village
   rows place at 23.4%.
3. **Currency of the animal-origin list.** It marks no closures, unlike
   Bucharest's ANULATE section and the non-animal list's ÎNCHIS. **Recommend
   asking**: the owner's browser can check DSVSA Timiș's page for a separate
   "desființate" (closed) list.
   - If the list holds active units only, it passes the currency rule as it
     stands.
   - If it holds both, with no marker, it fails, and the city waits.
   - N33's 45 red-filled rows go the same way.

   *Tradeoff*: another browser visit, against building on a list whose
   closures cannot be seen.
4. **The tram source.** **Recommend the city's CC BY `mobility` dataset** as
   the rail source: lines, stops and trips. It is the city's own, current
   (2026-08-25) and declares a licence. **A Step 0 download for the owner to
   approve**: three files, 9,339,205 B in all, from `data.primariatm.ro`, plus
   one `licence-read`. OSM stays the cross-check.
   - **Fallback**: SMTT's six lines **routed over OSM's kept track** through
     SMTT's stop sequences. That is the owner's Manchester rule of
     2026-10-02, with an alias table for SMTT's abbreviations.

   *Tradeoff*: OSM alone would draw four of six lines on routes they no longer
   run, so it is not offered. The feed is JSON-LD, not GTFS, so step 1 writes
   a reader. Its stop collapse and gate-3 counts come from it, against SMTT's
   per-line pages as the independent source (16, 23, 24, 29, 18, 21 names,
   collapsed the same way).
5. **Lines 5, 6a and 6b: `NOT_DRAWN`**, with the reason "no stops or
   timetable on SMTT's programme page, 2026-10-07". They are re-checked at
   the build. **Recommend** this, on the `tram-city` rule (relations without
   service are listed, never dropped silently). *Tradeoff*: none, if they are
   suspended. If they return, the 6 stop names they alone serve gain rings.
6. **BUFET (145 in-city premises in no other sheet).** **Recommend keep,
   Food service**, on Bucharest's taxonomy, which keeps "bufet" and drops
   only "bufet de incintă" (in-house). Timiș's sheet carries no category
   text, so in-house buffets cannot be told apart. 14 of the 163 in-city
   BUFET rows name a school or university word. Those 14 are dropped by name
   as R1 canteens. *Tradeoff*: a few staff canteens under other names may
   stay; dropping the sheet whole loses about 130 public buffets.
7. **A `romania-city` skill** before the second Romanian build
   (`docs/handoff_staging_2026-09-30.md`; the owner's per-country rule). It
   should carry:
   - the county cut by the address's first segment;
   - multi-sheet files;
   - per-county file codes;
   - XLS through `xlrd`;
   - the closure markers (ANULATE, ÎNCHIS, none).

   **Recommend** writing it from this brief and Bucharest's build. Iași's and
   Cluj-Napoca's files will show which of these are county quirks.

---

## Checks

**What the checks cannot hold.** The claims a build relies on most are the
saved files' sizes and row counts. **No check kind reads a local binary
file**: `row_count` reads CSV under the repository, and `data/` is not
committed. They stay in the table above, with SHA-256 prefixes, as
Bucharest's are, and step 2 re-prints them.

**What the block holds:**

- the OSM boundary relation;
- the tram relation and ref counts (two mirrors confirm a mismatch);
- SMTT's six running lines;
- the city catalogue's CC BY declaration and the three JSON-LD files;
- the CRS, with `vs_config` for the build.

DSVSA Timiș is not checked: its host answers scripts with 503 or 403, and
`http_contains` asserts a 200 (Bucharest's note).

```brief-checks
[
  {
    "id": "timisoara-osm-boundary",
    "claim": "OSM relation 6927733 is the Municipiul Timisoara boundary (name Timișoara, admin_level 8): the scope, and the area of the address join (area 3606927733)",
    "kind": "http_contains",
    "url": "https://api.openstreetmap.org/api/0.6/relation/6927733",
    "present": ["k=\"name\" v=\"Timișoara\"", "k=\"admin_level\" v=\"8\"", "k=\"boundary\" v=\"administrative\""]
  },
  {
    "id": "timisoara-osm-tram-refs",
    "claim": "OSM carries 18 tram relations, 9 refs (1, 2, 4, 5, 6a, 6b, 7, 8, 9), two per ref, none coloured (2026-10-07); 5, 6a and 6b are not on SMTT's programme",
    "kind": "osm_route_refs",
    "bbox": [45.68, 21.10, 45.82, 21.35],
    "routes": ["tram"],
    "expect_relations": {"tram": 18},
    "expect_refs": {"tram": 9},
    "require_refs": {"tram": ["1", "2", "4", "5", "6a", "6b", "7", "8", "9"]}
  },
  {
    "id": "timisoara-smtt-six-lines",
    "claim": "SMTT's Program Tramvaie page carries the six running lines 1, 2, 4, 7, 8, 9 (both directions each), and no return page for 5, 6a or 6b (2026-10-07)",
    "kind": "http_contains",
    "url": "https://smtt.ro/program-tramvaie/",
    "present": ["linie-transport-public-1-r", "linie-transport-public-2-r", "linie-transport-public-4-r", "linie-transport-public-7-r", "linie-transport-public-8-r", "linie-transport-public-9-r"],
    "absent": ["linie-transport-public-5-r", "linie-transport-public-6a-r", "linie-transport-public-6b-r"]
  },
  {
    "id": "timisoara-mobility-cc-by",
    "claim": "The city catalogue's 'mobility' dataset (Transportul Public) declares cc-by and carries the stops, routes and trips JSON-LD files the build would ask to download (updated 2026-08-25)",
    "kind": "http_contains",
    "url": "https://data.primariatm.ro/api/3/action/package_show?id=mobility",
    "present": ["\"license_id\": \"cc-by\"", "mobility-stops.jsonld", "mobility-routes.jsonld", "mobility-trips.jsonld"]
  },
  {
    "id": "timisoara-projected-crs",
    "claim": "Timișoara's derived UTM zone is 34N (EPSG:32634), not Bucharest's 35N",
    "kind": "utm_zone_from_longitude",
    "lon": 21.227,
    "expect": "EPSG:32634",
    "mode": "tram",
    "coverage": "one_bucket",
    "crs": "EPSG:32634",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
