---
name: romania-city
description: Build a Romanian city on what Bucharest and Cluj-Napoca built - the county DSVSA food-unit lists the owner saves by browser, each file read by its ROLE from its name (every county numbers its files differently), the county cut to the city by address, what the owner leaves out (canteens, catering, trailers, stands), the OpenStreetMap address join with the nearest same-side number tier, the 70% placed bar, the name rule and its two extensions, notice wording, and trams from OSM as direction pairs. Use for any Romanian city after Cluj-Napoca; read with add-city, address-join, osm-rail, tram-city and publish-city, which it does not replace.
---

# Building a Romanian city

Written 2026-10-11 from **Cluj-Napoca**, Romania's second city
(`DECISIONS.md`, 2026-10-11, "Cluj-Napoca built", folded from Kansai-2's
drafts file), on what **Bucharest** built first (2026-09-29).
Romania is **Spain's shape in its business leg**: one national authority
(ANSVSA) but one directorate (DSVSA) per county, each publishing its own
files its own way. The classification, the join and the name rule are
shared; the file list, the dates and the address quirks are the county's.

Read the city's brief first (`docs/build_briefs/<city>.md`, and run
`python scripts/brief_check.py <city>`), then this. Cluj-Napoca's files are
the worked example for a county list: `pipeline/cluj_napoca/`.

## What already exists - reuse it, do not rewrite it

| Where | What it does |
|---|---|
| `pipeline/taxonomies/romania_dsvsa.py` | The classification. Bucharest's bare file codes keep their own sets. **Every later county writes `source_files` as `<A|N><nn>:<role>`** and is bucketed by `ROLE_BUCKET`; `role_for_file(name)` reads the role from the file's NAME and raises on a name it cannot read. `NOT_STOREFRONT_CATEGORY` (Bucharest's) and `NOT_STOREFRONT_CATEGORY_ROLES` (the county exclusions) decide what is left out; `name_kind_extended()` is the name rule's two extensions |
| `pipeline/bucharest/step2_clean_businesses.py` | The name rule (`display_name`, `SOLE_TRADER`, `is_person_name`), the street normaliser (`street_parts`, `key2`, `parse_address`), the one-site test and `place()`. **Imported unchanged** by Cluj-Napoca's step 2: a change there changes every Romanian city (parked call "Cluj D" asks for a shared module) |
| `pipeline/cluj_napoca/step2_clean_businesses.py` | The county reader: XLS through `xlrd` and XLSX through `openpyxl`, header found by name on any row, rows read by content where a file's columns are swapped, closure notes, the cut to the city by address, the three address repairs, and `nearest_number()`, the tier |
| `pipeline/cluj_napoca/fetch_sources.py` | Checks each owner-saved file's SHA-256 against `config.py` (a changed file stops the fetch), then the boundary, the tram relations and the address objects from OpenStreetMap, one Overpass query at a time |
| `pipeline/osm_tram.py` | Tram stops from OSM relations; `name_members` names a stop member OSM leaves unnamed, from the operator's own stop list |
| `pipeline/cluj_napoca/step1_stations.py` | Stations as DIRECTION PAIRS, for an operator that names each direction's stop separately |

## The register - what every county shares, and what none does

- **The DSVSA hosts refuse scripts.** The owner saves each county's files in
  their own browser into `data/<city>/raw/` (animal-origin list) and
  `raw/non-animal/`. No script fetches them and no cookie is replayed. The
  build records each file's bytes and SHA-256 and stops on a changed file.
- **Map files to roles by NAME, never by number.** Cluj's file 23 is food
  shops and its 21 confectioners; Bucharest's 23 is confectioners and its 25
  food shops. A county's numbers read through another county's map re-bucket
  food shops silently. A file name no pattern reads raises: add its pattern
  to `ROLE_BY_NAME` (longer names first), then run the Bucharest control
  below.
- **A county list covers the whole county and has no locality column.** The
  locality leads the address text. Keep a row where the address names the
  city; leave out, and count, every row that names another place or none. A
  row that opens with a village or commune word (`sat`, `com.`) is that
  place's whatever it mentions later, and a bare county name names neither.
  Street names carry place names too (Calea Florești, Calea Turzii): test for
  the city's own name, never for the absence of others.
- **Expect none of Bucharest's structure.** Cluj's files have no `ANULATE`
  section, no status column and no Sector column; headers sit on rows 7 to
  21; one file's cells are merged; every file ends in numbered blank rows;
  one file has its address and category columns swapped on most rows (read
  each row by content); a closure can be a note in an unheaded column. Probe
  structure first with a script that prints headers and counts only, never
  names or addresses.
- **The files carry different dates.** The page states the range (Cluj:
  April 30 to October 6, 2026), never one date.
- **Two lists can hold the same premises** (Cluj's bars sit in both the
  animal-origin and the non-animal listing): read both and merge on
  Bucharest's key, folded name + parsed street + number.

## What is left out - the owner's calls, do not re-ask

- **Canteens, catering, pastry labs, local producers, internet-only sales,
  warehouses, fairs** (owner, 2026-09-28): whole files never read where the
  county files them apart, and by category text where it does not.
- **Mobile units, trailers (rulotă), kiosk carts (tonetă), vending machines,
  in-house buffets (bufet de incintă)** (2026-09-28 and 2026-09-29), in every
  spelling: Cluj writes "bar mobil", "cafenea mobilă", "bufet ambulant".
- **Stands** (market and street stalls, "stand") are out; **a fixed kiosk
  ("chioșc") stays** (Thessaloniki's call).
- **Pharmacies** are out (a food-only register's pharmacies, Stockholm's
  rule). **Bakeries registered as production units stay** (Bucharest kept its
  bread-making files).
- **A shop file wins the bucket** (`ROLE_SHOP_FIRST`): a supermarket's café
  is a food shop.
- Print every category per file in step 2 and read the list: a new kind of
  unit is looked at, never waved through.

## The name rule (owner, 2026-09-28 and 2026-09-29)

The pin shows the company name without its legal form; **a sole trader, or a
company named only for a person, is shown by its category**. Bucharest's
`display_name()` does the first pass. Then `romania_dsvsa.name_kind_extended()`:

- **Abbreviated sole-trader forms** ("Intrepr.Ind.", "Intr.Fam.",
  "Intreprind."): Cluj had 15 that Bucharest's test let through.
- **Names Bucharest's person test cannot read**: it looks for Romanian given
  names and surname endings, so Transylvanian and Hungarian names passed. The
  extension withholds a shown name that is a given name (Romanian or
  Hungarian) beside exactly one other word that is no business word. It errs
  toward showing a category.

Measure with counts only. Never print a name to check the rule; print form
fragments and word frequencies. Run `scripts/check_personal_exposure.py
<city>` after step 3; its Latin heuristic reads capitalised company names as
people (about 40% of pins), which is not a finding here.

## Placement - the OSM address join, the tier, and the 70% bar

- **No national address file is reachable** (ANCPI's RENNS does not resolve),
  so the join target is OpenStreetMap's address objects inside the
  municipality's relation, Bucharest's query. Cache them under the fetch date.
- **Bucharest's `place()`**, with `use_sector=False` outside Bucharest: exact
  street and number, the whole number (14A to 14), then the tolerant street
  key where one OSM street has the number; always the one-site test (150 m
  hops, 600 m wide).
- **The city's own repairs** come before the parse: the locality cut,
  date-named streets kept whole ("21 Decembrie 1989" is not number 21),
  one-letter initials dropped from the key on both sides, "nr." spacing.
- **The nearest-number tier** (owner, call 215a; Palma's rule): where OSM has
  the street but not the number, the nearest number it lists on the same side
  (odd or even), at most 6 numbers away, a tie to the lower number, and only
  where that number's points are one site. Cluj: 447 premises, a median 2
  house numbers from their own address.
- **The bar is 70% placed** (the reduced-bucket bar; Santa Cruz-La Laguna was
  discarded at 57.7%). Step 2 stops under `config.PLACED_SHARE_MIN`. Cluj
  reached 71.3% only with the tier; Timișoara, Iași and Arad measured 50 to
  64% with it and are in Band R. A city under the bar is not built on a
  disclosure.
- **The page states the unplaced share** in bold, and what the tier does.

## Controls

- **Bucharest must not move.** After any change to `romania_dsvsa.py`,
  classify every row of `data/bucharest/processed/businesses_clean.csv` and
  `premises_all.csv` with the committed module and the changed one: 0
  differences (15,589 and 20,814 rows on 2026-10-11). This is read-only;
  Bucharest's steps are not run from a build branch.
- **`python scripts/osm_tram_control.py`** after any change to `osm_tram.py`.
- **Each file's row count** against the brief's (`config.EXPECTED_ROWS`).

## Rail

Bucharest's metro and Cluj-Napoca's trams are both OpenStreetMap's (no feed
is usable). For trams read `tram-city` and `osm-rail`. Two things Cluj added:

- **An operator that names each direction's stop separately** (CTP: UNIMET
  Nord and UNIMET Sud; Opera Maghiară Est one way, Parcul Central the other)
  makes a name collapse draw each station twice. Pair each stop with the
  nearest stop of the other direction (the line that runs the whole axis
  gives the directions), state the furthest pair, show the shared part of
  the two names or both names, and gate the station count.
- **Gate 3 per direction** against the operator's own stop maps, with any
  known difference written beside the figure.

Project to the city's own UTM zone: Bucharest is 35N, Cluj-Napoca 34N.

## Notices, licence and the page

- **DSVSA publishes with no stated licence**: SILENT for DSVSA București and
  for DSVSA Cluj, each county's own site read in a browser by the
  `licence-read` agent. One notice per county directorate (Bucharest's and
  Cluj-Napoca's are in `docs/data_sources.md`), in the wording the owner
  approved for Bucharest's, with the city's own changes named. `data.gov.ro`
  and ANSVSA's own site are part of the read.
- OpenStreetMap supplies the rail, the boundary and the address points:
  notice 1, with an entry in `app/osm_notice.py` and the same words in notice
  1's list in `app/components.py`.
- The page follows Bucharest's (`app/pages/64_Bucharest_Heatmap.py`): food
  only in bold, no open register of other shops, what is left out, one pin
  per premises, the name rule, the unplaced share in bold. A sentence it does
  not cover is a proposal in the drafts file.
- `coverage: "one_bucket"`, `categories: "Food premises only"`,
  `record_kind: "Food hygiene register"`, region "Europe East".

## Which city next

None is ready. Timișoara, Iași, Arad, Galați, Ploiești, Craiova, Reșița and
Oradea were measured in October 2026 and sit in Band R on placement
(`docs/city_master_list.md` wins). A city leaves R when a second address
layer, or OSM's own growth, takes its join over 70%: re-measure with Cluj's
step 2 before any other work.
