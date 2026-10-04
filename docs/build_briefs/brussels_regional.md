# Brussels (Regional) — build brief

**Screened and measured 2026-10-03/04 (staging); Band B, owner-approved
2026-10-03 (call 12 of Belgium's twelve build calls, "i say yes to all").**
Run `python scripts/brief_check.py brussels_regional` before writing any
code. The trail, in `docs/decisions_drafts/staging.md`, 2026-10-03:
"Seven licence reads for the sweep's first group" (the KBO read), "KBO
measured: Belgian bands kept; Brussels (Regional) D to C", "BeST-Address
Brussels read", "Brussels: STIB's GTFS with the owner's acceptance" and
"Belgium's build calls, and Brussels (Regional) from C to B". Master list:
`docs/city_master_list.md`, Band B, "Brussels (Regional)". Kit: the
Belgium handoff, deleted when the build landed (2026-10-04; its calls are in
`DECISIONS.md`) (page **201**; notices **151** KBO,
**152** BeST-Address, **148** STIB shared with Brussels).

**Build it last, after Brussels** (`docs/build_briefs/brussels.md`): the
rail leg reuses the City's STIB feed, thinning rule and premetro trap, and
the Brussels page gets a bullet pointing here. Skills: `add-city`,
`scaffold-city`, `address-join`, `premises-taxonomy`, `publish-city`;
`osm-rail` only on the City's fallback. Not `tram-city`: the backbone is the
metro.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot color) | **`metro`** | STIB's metro runs on through the 18 communes to most of its termini (Erasme, Stockel, Herrmann-Debroux; ASSERTED, the feed confirms) |
| **`coverage`** | **`narrowed`** ("Two") | Retail and Food service full; **Personal services off** (owner, call 12): companies only drops most salons (0.47 times the survey's count, 51% recall). Charleroi's and Liège's shape |
| **Scope** | **The 18 communes of the Brussels-Capital Region outside the City of Brussels**, `SCOPE = "regional"` with the 18 NIS codes as `SCOPE_CODES` | The City is its own page, "Brussels" (hub.brussels's survey); the two are never merged without a key |
| **Method** | **Different from the City's, said on the page** (owner, call 12) | The City maps a ground-floor field survey of every shop, sole traders' included; this page maps companies' registered establishment units, filtered by four rules |
| **Trams** | **Drawn and thinned, the City's rule** | As the Brussels brief; the 18 communes carry most of the tram network |
| **Page name** | **"Brussels (Regional)"**, slug `brussels_regional`; the scope bullet names the 18 communes and says the City of Brussels is on the Brussels page | The City brief's pairing (owner, 2026-10-03) |
| **Rings** | by the spacing rule (`docs/ring_rules.md`) | Measure the median gap among the stations kept |
| **Region** | `"Europe"`, country `"Belgium"` | Belgium's country work is the Brussels build's |

---

## The one-line summary

**KBO/BCE Open Data's companies' establishment units in the 18 communes,
joined to BeST-Address Brussels (96.8% placed at a house number, 88.5%
exact), filtered by four storefront rules: Retail 9,124 (8,754 placed) and
Food service 5,209 (5,007 placed). Measured against hub.brussels's survey in
the City: Retail 78.2% precision / 76.1% recall, Food 84.4% / 84.0%. Rail:
STIB metro and premetro beyond the City, plus thinned trams.**

| | **Brussels (Regional)** |
|---|---|
| Rail | STIB-MIVB: metro M1, M2, M5, M6, the premetro, trams |
| Stations in scope | **Counted by the build** from STIB's feed. ASSERTED, not looked up: English Wikipedia's 69 metro and premetro stations network-wide, less the City's 25, leaves about 44 in the 18 communes (the metro lies wholly inside the Region) |
| Projected CRS | **EPSG:32631** (UTM 31N, about 4.37° E) |
| Business source | KBO/BCE Open Data (FPS Economy), full file, extract 501, snapshot 2026-10-02; placed on BeST-Address Brussels (FPS BOSA), CSV of 2026-09-30 |

---

## Scope — the 18 communes

| Commune (FR / NL) | Postcode | NIS |
|---|---|---|
| Anderlecht | 1070 | 21001 |
| Auderghem / Oudergem | 1160 | 21002 |
| Berchem-Sainte-Agathe / Sint-Agatha-Berchem | 1082 | 21003 |
| Etterbeek | 1040 | 21005 |
| Evere | 1140 | 21006 |
| Forest / Vorst | 1190 | 21007 |
| Ganshoren | 1083 | 21008 |
| Ixelles / Elsene | 1050 | 21009 |
| Jette | 1090 | 21010 |
| Koekelberg | 1081 | 21011 |
| Molenbeek-Saint-Jean / Sint-Jans-Molenbeek | 1080 | 21012 |
| Saint-Gilles / Sint-Gillis | 1060 | 21013 |
| Saint-Josse-ten-Noode / Sint-Joost-ten-Node | 1210 | 21014 |
| Schaerbeek / Schaarbeek | 1030 | 21015 |
| Uccle / Ukkel | 1180 | 21016 |
| Watermael-Boitsfort / Watermaal-Bosvoorde | 1170 | 21017 |
| Woluwe-Saint-Lambert / Sint-Lambrechts-Woluwe | 1200 | 21018 |
| Woluwe-Saint-Pierre / Sint-Pieters-Woluwe | 1150 | 21019 |

The City of Brussels (NIS 21004; postcodes 1000, 1020, 1120, 1130) is out.

- ⚠️ **Scope by commune, never by postcode.** The City's Avenue Louise strip
  and European quarter carry **1050 and 1040**, Ixelles's and Etterbeek's
  postcodes: KBO's municipality field puts 3,377 legal establishments of the
  City in those two postcodes (1040 1,208; 1050 2,169). A postcode scope
  would put City units on this page.
- **The key:** the matched BeST point's `municipality_id` (the NIS code; the
  CSV carries it on every address), checked against the Region's
  commune-limits polygons (the City brief's PARADIGM dataset, CC0 1.0) and
  KBO's own municipality field. Step 2 reports the units where the three
  disagree; the screen keyed the 18 communes on KBO's municipality field
  (the City = that field or its four postcodes).
- **The Region's special postcodes** (1099, 1105, 1110 and the like) belong
  to whichever commune the point falls in.
- Stations inside the City get no ring here (they are the Brussels page's).
  Units in the 18 communes near a City station (the Louise and EU-quarter
  edges) fall outside every ring on this page: **the build counts the placed
  units within a ring of a City station and no regional one**, and brings
  the figure to the owner if it is large.

---

## Business leg — KBO/BCE Open Data on BeST-Address Brussels

### The cached files (no fetch needed for the build's first run)

| File | Bytes | sha256 | Meta |
|---|---|---|---|
| `data/belgium/raw/KboOpenData_0501_2026_10_03_Full.zip` | 313,432,247 | `3a5719a9...2f705b97` | `.zip.json`: fetched by the owner under their own free account, 2026-10-03 |
| `data/belgium/raw/openaddress-bebru.zip` | 17,941,521 | `f558a29d...a76df24d76` | `.zip.json`: `https://opendata.bosa.be/download/best/openaddress-bebru.zip`, fetched 2026-10-03 on the owner's approval |

- **KBO cannot be fetched by a script**: the portal needs the owner's login.
  `pipeline/brussels_regional/fetch_sources.py` (or a shared Belgian one)
  verifies the owner-placed zip against its meta JSON and refuses otherwise,
  naming the owner's act. A step never fetches.
- **BeST** is named here, so a re-fetch is pre-permitted; a re-fetch means
  re-running the control below. ⚠️ **From 2026-10-11 BOSA's CSVs replace
  `EPSG:31370_x/_y` (Lambert 72) with `EPSG:3812_x/_y` (Lambert 2008)**. The
  cached CSV's columns: `EPSG:31370_x, EPSG:31370_y, EPSG:4326_lat,
  EPSG:4326_lon, address_id, box_number, house_number, municipality_id,
  municipality_name_de/fr/nl, postcode, postname_fr/nl, street_id,
  streetname_de/fr/nl, region_code, status`. **Read the `EPSG:4326_*`
  columns only** (BOSA keeps WGS84 after the switch) and assert them by name.
- KBO's members: `meta.csv` (SnapshotDate 02-10-2026, ExtractNumber 501),
  `enterprise.csv`, `establishment.csv`, `address.csv`, `activity.csv`
  (1.53 GB uncompressed), `code.csv`; and `denomination.csv`, `contact.csv`,
  `branch.csv`, below.
- **Memory:** the screen's extract pass measured **1.32 GB** (heavy-job gate,
  session staging; the BeST index alone 0.50 GB). Step 2 runs through
  `scripts/heavy_job.py` declaring an estimate scaled from that.

### Personal information — companies only

- **Companies' establishment units only**: `TypeOfEnterprise` 2 (legal
  person). KBO's license makes every natural-person entity's data personal
  data; the read's condition is companies' establishments only.
- **`contact.csv` is never read.** **`denomination.csv` only through a step
  that first restricts to legal-person entity numbers**, so no natural
  person's row is ever parsed or held; the screen opened neither file. The
  dot's name, if the page shows one, is the commercial name the
  establishment unit carries, else the company's name (the build's
  recommendation to the owner if it departs from the City's shop signs);
  `check_personal_exposure.py brussels_regional` decides the rest (a company
  name that is a person's own name).
- Never print an establishment or enterprise number, a name or an address:
  counts only, in the drafts file, the commit messages and any log.
- No direct marketing use (license 2.2); the project is the GDPR controller
  (2.1): a removal or objection request is honored first (the removal rule).

### The base, then the four rules

**Base** (the license plus currency): legal person; `JuridicalSituation`
**000** (normal: bankruptcy 050 and liquidation 012 out); the establishment
address (`TypeOfAddress` BAET) **not struck off** (`DateStrikingOff` empty);
in a bucket (below); **placed at a number tier** of the join. The file holds
active entities only (`Status` AC), so closures drop out at each snapshot.

**Then drop a unit when** (the screen's definitions, exactly):

| Rule | Definition | Why | Region units it names, filtered base (R / F / P) |
|---|---|---|---|
| **A** | **every in-bucket MAIN code is a catch-all**: NACE-BEL 2025 47.120, 47.279, 47.690, 47.789, 96.999 (2008's own list where 2008 decides) | a placeholder activity, not a shop type | 1,724 / 0 / 816 |
| **B** | **the address hosts 5 or more companies' establishment units of any activity (any juridical situation), and fewer than half of them are in a bucket**; the address key is postcode + street + house number, box ignored | a business or domiciliation center; the half test keeps shopping centers | 3,155 / 595 / 406 |
| **C** | **the box is a plain number** once its prefix (`bte`, `boîte`, `bus`, `box`, `b`) is removed; ground-floor marks (`RDC`, `RC`, `GV`, `gelijkvloers`, `0`) and floor marks are not numeric | an apartment or office unit, not a ground-floor shop | 2,542 / 444 / 350 |
| **D** | **10 or more distinct MAIN codes (in the NACE version used), at least one outside the three buckets** | a registered seat's laundry list of activities | 5,380 / 939 / 534 |

Rules overlap. Rejected and why (`screens/kbo/sf_filter_rules.md`): "any MAIN
code outside the buckets" (Retail recall to 59.9%), "single establishment
with an outside code", any start-date window (no signal), juridical form,
seat = establishment.

### The bucket rule — `czech_nace2025` plus `france_naf`'s exclusions

- **NACE-BEL 2025** (NACE Rev. 2.1 with Belgian 5- and 7-digit sub-codes):
  `pipeline/taxonomies/czech_nace2025.py`'s division buckets (47 Retail, 56
  Food service, 96 Personal services) and its structural exclusions by prefix
  (47.9 intermediation, 56.12 mobile, 56.2 catering and canteens, 56.4,
  96.3 funeral, 96.4, 96.91), **plus two on `france_naf.py`'s precedent**:
  **96.101 industrial laundries** and **47.781 heating-fuel dealers** (the
  category rules' nonstore row). Car retail 47.81 is Retail (R4). The Belgian
  catch-all list above is the city's, not Czechia's (`CATCH_ALL_CODES` there
  differs). A thin Belgian module or config over the Czech one; never fork a
  taxonomy silently, and `check_category_continuity.py` must answer it.
- **NACE 2008** only where a unit has no 2025 MAIN code (0.1% decide on it):
  `france_naf.py`'s structural set at class level (47.8, 47.9, 56.2, 96.03,
  96.011, 47.781).
- **Establishment-level codes first** (99.6% of legal establishments carry
  their own; activity group 003); the enterprise's MAIN codes only when the
  unit has none (0.4%).
- ⚠️ **"MAIN" is not one code.** 36% of legal establishments list five or
  more distinct MAIN codes, unordered. The rule measured and approved: **any
  MAIN code in a bucket; priority Food service over Retail over Personal
  services.** The priority runs before Personal services is dropped, so a
  unit with a food or retail code keeps that bucket and a personal-only unit
  leaves the map. A first-listed rule lost a third of real restaurants
  (Antwerp, against FAVV).
- **The catch-all share** (`premises-taxonomy` step 2): catch-all codes sit
  on 30% of Retail and 39% of Personal services units region-wide; rule A
  is the response. `brief_check.py`'s `taxonomy_catchall` kind reads a
  remote column and cannot reach this local file: step 2 prints the share
  per bucket instead.
- Web shops: Rev. 2.1 files them under the product, so no code removes them
  (disclosed, as Oslo and Prague); 2008's 47.91 shows 574 in the Region.

### The join — tiers (`address-join`)

Both sides normalized: accents folded; street-type words and abbreviations
folded to one token; Dutch compound suffixes split (`-straat`, `-steenweg`,
`-laan`, `-plein`...); FR and NL street names both tried; house number
parsed to number + letter; box prefix dropped, leading zeros removed. BeST
rows kept: 847,377 (current 663,350, proposed 180,679, retired 3,348;
rejected 1,402 dropped). First hit wins:

| Legal in-bucket units, filtered base (Region, 19 communes) | Units | exact | number, box dropped | number relaxed (letter/range) | number, other postcode or loose street name | street only | none | **placed (number tiers)** |
|---|---|---|---|---|---|---|---|---|
| Retail | 20,992 | 87.5% | 7.1% | 1.1% | 0.9% | 2.1% | 1.2% | **96.7%** |
| Food service | 9,252 | 90.7% | 4.3% | 1.1% | 0.6% | 2.3% | 0.9% | **96.7%** |
| Personal services | 2,489 | 88.5% | 7.7% | 1.1% | 0.6% | 0.9% | 1.2% | **97.9%** |
| **All** | 32,733 | **88.5%** | 6.4% | 1.1% | 0.8% | 2.1% | 1.1% | **96.8%** |

- **Street-only and unplaced units (3.2%) stay off the map**, disclosed in
  the city's section of What Is Excluded.
- ⚠️ **The "other postcode or loose street name" tier (0.8%) is the
  district-free key `address-join` warns about**: it joins wrongly at a
  higher rate. Count the street keys that recur in more than one postcode,
  read that tier's misses by class, and keep it only if it holds; dropping
  it costs under one point.
- **The control that must reproduce** before anything else counts: on the
  City's four postcodes, **88.5% exact, 97.2% placed**, and the agreement
  figures below. The screen's scripts sit in staging's scratchpad
  (`screens/kbo_sf_defs.py`, `kbo_storefront_extract.py`,
  `kbo_storefront_analyse.py`), which another session may not reach: this
  brief carries the rules in full.

### Counts, measured (filtered, four rules)

| Scope | Retail kept / placed | Food service kept / placed | Personal services kept / placed (off) |
|---|---|---|---|
| Brussels-Capital Region (19 communes) | 11,851 / 11,382 | 7,566 / 7,294 | 1,250 / 1,216 |
| **The 18 communes** (KBO municipality field) | **9,124 / 8,754** | **5,209 / 5,007** | 1,010 / 981 |
| The City (municipality field or its four postcodes) | 2,727 / 2,628 | 2,357 / 2,287 | 240 / 235 |

Before the four rules (the base alone), the Region held 20,992 / 9,252 /
2,489. Per commune by postcode, placed (Etterbeek and Ixelles include the
City's 1040/1050 parts; step 2 re-counts by commune):

| Commune | Retail | Food service |
|---|---|---|
| Anderlecht | 1,254 | 555 |
| Auderghem | 205 | 95 |
| Berchem-Sainte-Agathe | 166 | 61 |
| Etterbeek (1040) | 429 | 305 |
| Evere | 157 | 85 |
| Forest | 320 | 185 |
| Ganshoren | 94 | 61 |
| Ixelles (1050) | 1,248 | 897 |
| Jette | 348 | 148 |
| Koekelberg | 134 | 65 |
| Molenbeek-Saint-Jean | 842 | 351 |
| Saint-Gilles | 651 | 561 |
| Saint-Josse-ten-Noode | 239 | 230 |
| Schaerbeek | 1,122 | 710 |
| Uccle | 867 | 378 |
| Watermael-Boitsfort | 134 | 67 |
| Woluwe-Saint-Lambert | 346 | 190 |
| Woluwe-Saint-Pierre | 273 | 129 |

### Agreement with the survey — measured in the City, the only ground truth

**Method:** KBO legal, filtered, placed units on the City's four postcodes,
started on or before hub.brussels's survey date (2025-10-17), against
hub's 6,531 rows there (types mapped as the City's screen did). **Precision**
= share of KBO units with a compatible hub shop within 15 m; **recall** =
share of hub's shops in a bucket with a compatible KBO unit within 15 m. All
distances in EPSG:32631.

| Bucket | Before the rules: precision / recall | **After A-D: precision / recall** | After: 1:1 precision | After: KBO placed / hub's count | After, at 5 m: precision / recall |
|---|---|---|---|---|---|
| Retail | 61.6% / 82.6% | **78.2% / 76.1%** | 63.4% | **1.09** | 65.1% / 55.3% |
| Food service | 79.5% / 87.1% | **84.4% / 84.0%** | 68.7% | **1.22** | 71.6% / 70.5% |
| Personal services (off) | 46.7% / 58.1% | 75.9% / 51.1% | 68.4% | 0.47 | 68.9% / 44.5% |

- **Caveats, for the page's limits section:** the rules were calibrated in
  the City, the Region's densest and most office-heavy commune, so B and D
  may remove fewer true shops in the outer communes (not measurable without
  a second survey; none is published); the two snapshots are a year apart;
  a 15 m match accepts the adjacent building.

### The page's method sentence (a proposal: no template covers it)

Drafted for the build's drafts file and review time, not yet approved:

> Unlike the Brussels page, which maps a 2025 street survey of every shop,
> this page maps companies' registered business locations from Belgium's
> national business register, filtered to leave out offices, apartments and
> business centers. Sole traders are not included, and personal services
> such as hair salons are not mapped. Checked against the street survey
> inside the City of Brussels, about four in five of these locations matched
> a shop, and the filter found three in four shops and five in six
> restaurants and cafés.

The Brussels page gets one bullet pointing back (a proposal for that page,
written by the Belgium build).

---

## Rail — STIB-MIVB beyond the City

- **Source: STIB's static GTFS**, the same fetch as Brussels (the owner
  accepted the Belgian Mobility Company portal's terms for the build's first
  fetch; a re-fetch after the terms change goes back to the owner). This
  brief carries **no check that fetches the feed or touches that portal**;
  the Brussels brief carries the portal check. Fallback: `osm-rail`, one
  Overpass query, as the City's.
- **Stations:** every underground metro and premetro station in the 18
  communes is the central corridor, never thinned. ⚠️ **The premetro trap
  is bigger here:** the 18 communes hold more underground stations served by
  trams alone (on the North-South axis south of the Pentagon and on the
  Greater Ring, ASSERTED, not counted); mark them by name or by the feed's
  station structure, never by route type. Gate 3: STIB's per-line station
  lists, English Wikipedia's 69 as the named fallback, less the City's 25.
- **Trams: drawn and thinned, the City's rule** (`docs/sub_transit_line_filters.md`,
  `pipeline/stations.py`'s `thin()`): underground stations kept; each line's
  two terminals inside the scope kept; a stop on two or more lines kept; the
  rest to one per half mile along the line's own stop sequence. Each cut goes
  to the excluded-stations file with "spacing" in its reason; the page names
  the thinned lines.
- **Lines that cross the Region's edge** (some trams run on into Flemish
  Brabant, ASSERTED): drawn to their ends with the stops outside listed as
  out of scope (Mendoza's and Charleroi's M2 precedent), or cut at the edge;
  the build brings the call with the count. Every drawn line gets its
  permanent on-map label and a legend entry. Buses and SNCB trains are not
  drawn; the page says so.

---

## Licenses and notices

| Notice | Source | Verdict | Display |
|---|---|---|---|
| **151** | **KBO/BCE Open Data**, FPS Economy | **Permitted with conditions** (`licence-read` 2026-10-03): companies' establishments only; reuse within the purpose the owner declared at registration (2.3); no direct marketing (2.2); the project is the GDPR controller (2.1); do not alter or distort (2.7); **cite the source and the update date (2.8)**; term changes by e-mail on notice (9.1, 15 days); **a download at least yearly (10.5)** | The source and the update date (snapshot 2026-10-02, extract 501), presented as the register's data, **not as a guarantee** of any business's status; companies only; a statement of the modifications (filtered, joined, grouped) |
| **152** | **BeST-Address Brussels**, FPS BOSA (`openaddress-bebru.zip`) | **Permitted with conditions** (`licence-read` 2026-10-03): CC BY 4.0 (BOSA's DCAT, landing pages, license PDF, data.gov.be); BeST-in-a-Box section 8 defers to the region's license, CC0 for Brussels; data.gov.be's research-results request read as not applying (owner) | FPS BOSA and the Brussels address register (the Region's, via datastore.brussels) as the source, **CC BY 4.0** with its link, and **a statement that business addresses were matched to its points**; no endorsement, no accuracy claim, no Paradigm or datastore.brussels marks |
| **148** | **STIB-MIVB GTFS**, Belgian Mobility Company portal | As Brussels | "Source: STIB-MIVB – Open Data – [feed date]", the modified-data line, the portal |

Plus the site's OSM basemap notice 1. Each source gets its row in
`docs/data_sources/belgium.md`; KBO and BeST rows are this page's only.

## Currency

KBO is a daily snapshot of active entities (the full file stays on the
portal 31 days); BeST is weekly. The page's data-age caption states the KBO
snapshot date and the BeST date. Re-pull within the license's yearly
download duty, which also keeps the contract alive.

## Scope, CRS, region

- **Scope:** `SCOPE = "regional"`, `SCOPE_CODES` the 18 NIS codes above.
  The scope bullet: the Brussels-Capital Region's 18 communes outside the
  City of Brussels, which has its own page.
- **CRS:** UTM 31N, **EPSG:32631**. Points from BeST's `EPSG:4326_*`
  columns, projected; never buffer in 4326.
- **Scaffold:** `scaffold_city.py --slug brussels_regional --name "Brussels
  (Regional)" --system-name "STIB-MIVB" --taxonomy <the Belgian key>
  --lat 50.838 --lon 4.37 --region Europe --country Belgium --mode metro
  --page-number 201` (`--dry-run` first). Two Belgian dots sit together on
  the macro map: `check_macro_labels.py` at 375, 768 and 1200.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, per notice, **card face or caption
only**, and any open terms question:
- **KBO (151): caption.** Article 2.8 asks for the source and the update
  date, with nothing on placement.
- **BeST-Address (152): caption.** CC BY 4.0 section 3(a), any reasonable
  manner for the medium.
- **STIB (148): caption**, as Brussels.
- **Open terms question: none known.** The declared purpose (2.3) is the
  owner's registration; if it named a narrower purpose than a public map and
  its derived visuals, that becomes one.

## Still open for the build

- ⚠️ **KBO's declared purpose**: if KBO asks (2.3), the question goes to the
  owner, who registered; nothing is sent by a session.
- ⚠️ **The yearly download** (10.5): the owner's act (a login); the build
  records the due date (by 2027-10-02) in the drafts file and the source row.
- ⚠️ **The station count**, gate 3, the tram lines and the thinned count;
  lines crossing the Region's edge.
- ⚠️ **The ring size** from the median gap.
- ⚠️ **Units near City stations only** (scope section), counted.
- ⚠️ **The join's loose tier**, read or dropped; the control reproduced.
- ⚠️ **The method sentence** (a proposal) and the Brussels page's pointer.
- ⚠️ **The privacy verdict** (`check_personal_exposure.py`), with
  `docs/privacy_verdicts.md`.

```brief-checks
[
  {
    "id": "brussels-regional-kbo-open-data-portal",
    "claim": "THE BUSINESS LEG: KBO/BCE Open Data is still free behind an account on FPS Economy's portal, a file of all active entities registered in the CBE. A changed page means re-reading the terms (companies only, the update-date credit, the yearly download)",
    "kind": "http_contains",
    "url": "https://kbopub.economie.fgov.be/kbo-open-data/login?lang=en",
    "present": ["files contain information about all the active entities registered in the CBE", "Access to this files is free", "/kbo-open-data/signup?form", "cbe-open-data"]
  },
  {
    "id": "brussels-regional-best-dcat",
    "claim": "THE ADDRESS FILE: BOSA's DCAT still lists the Brussels BeST CSV (openaddress-bebru.zip) as a distribution, and the record still carries CC BY 4.0",
    "kind": "http_contains",
    "url": "https://opendata.bosa.be/download/best/dcat.rdf",
    "present": ["https://opendata.bosa.be/download/best/openaddress-bebru.zip", "fpsbosa-dis-best-deriv-bru-csv", "CSV Brussels Gewest", "licence/CC_BY_4_0"]
  },
  {
    "id": "brussels-regional-best-landing-lambert",
    "claim": "BOSA's BeST page still offers the Brussels CSV under Creative Commons 4.0 Attribution with its conditions of use, and still announces the switch of the CSV's EPSG:31370 columns to EPSG:3812 (from 2026-10-11). When the notice goes, the switch has happened: confirm the build reads only the EPSG:4326 columns",
    "kind": "http_contains",
    "url": "https://opendata.bosa.be/index.fr.html",
    "present": ["/download/best/openaddress-bebru.zip", "creativecommons.org/licenses/by/4.0", "Creative Commons 4.0 Attribution", "bestinabox_conditionsdutilisation.pdf", "EPSG:31370_x", "EPSG:3812_x"]
  },
  {
    "id": "brussels-regional-projected-crs",
    "claim": "The 18 communes project to UTM 31N (EPSG:32631); metro mode, narrowed coverage (Retail and Food service), regional scope",
    "kind": "utm_zone_from_longitude",
    "lon": 4.37,
    "expect": "EPSG:32631",
    "mode": "metro",
    "coverage": "narrowed",
    "scope": "regional",
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
