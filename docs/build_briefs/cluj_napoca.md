# Cluj-Napoca — build brief

**Step 0 measured 2026-10-07 (staging), from the owner's saved DSVSA Cluj
files, OpenStreetMap and CTP Cluj's own timetable pages.** Run
`python scripts/brief_check.py cluj_napoca` before writing any code. The
owner asked for this brief ("write the briefs for those three now",
2026-10-07). **Bucharest is the template for the business leg**
(`docs/build_briefs/bucharest.md`, `pipeline/bucharest/`,
`pipeline/taxonomies/romania_dsvsa.py`); **the rail leg is a trams-only OSM
build** (`tram-city`, `osm-rail`, `pipeline/osm_tram.py`). Read
`add-city`, `scaffold-city`, `address-join` and `publish-city` with it.

⚠️ **Romania's second city, and the first DSVSA county other than
Bucharest's.** The county lists share Bucharest's columns but **not its file
numbers, its cancelled section or its column order** (the traps below).

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **Band** | **B** (call 1) | Bucharest's route and source, food only, placement gap disclosed. The D act (the owner's browser fetch) is done |
| **`mode`** | **`tram`** | CTP's three tram lines; the metro is under construction, not built, so not drawn |
| **`coverage`** | **`one_bucket`** (`categories` "Food premises only") | DSVSA registers food units only (Bucharest's shape; food shops count as food) |
| **Scope** | **Municipiul Cluj-Napoca**, OSM relation **3277038** (admin_level 8), **174.9 km²** in UTM 34N | The county lists cover every town in Cluj county; the address text names the locality, and the city is filtered on it. Every tram stop is inside |
| **Lines drawn** | **Trams 100, 101, 102**, CTP, OSM geometry; 102L (depot runs, no stops) in `NOT_DRAWN` | `osm-rail`, `tram-city` section 4 |
| **Stations** | **20 direction pairs** (call 11), every stop kept | The operator names each direction's stop separately |
| **Rings** | **Halved** (0.05 / 0.1 / 0.2 / 0.3 mi): median gap **475 m** on the 20 pairs (248 m on the 26 base names) | The spacing rule (about 550 m or less); recompute on the stations drawn |
| **Projected CRS** | **EPSG:32634** (WGS 84 / UTM 34N, from 23.59° E) | Not Bucharest's 35N |
| **Colors** | The project's palette | No OSM relation carries `colour` (kit call 3) |
| **Region** | `"Europe"`, country `"Romania"` | As Bucharest |

**The numbers in one place** (in-city premises after Bucharest's merge and
exclusions, before calls 6-10): **Food shops 2,799 · Food service 2,721**,
**3,321 placed (60.2%)**: Food shops 1,695, Food service 1,626. About **one
placed storefront in three (33.7%) sits within 0.3 mi of a tram stop**
(stop nodes, a stand-in for the build's rings).

---

## The one-line summary

**Bucharest's register and join on a county list, with a thinner address
map.** The register is the same DSVSA format and the same food-only shape;
OSM carries about a seventh as many address objects as Bucharest's for a
city about a fifth its size, and Bucharest's normaliser, unchanged, places **60.2%**, the
lowest of any built city (Incheon 71.3%, Bucharest 74.9%).

---

## Business leg — DSVSA Cluj, food only

**Source**: DSVSA Cluj (Direcția Sanitară Veterinară și pentru Siguranța
Alimentelor Cluj, under ANSVSA), its lists of registered retail food units
("Lista unităților de vânzare cu amănuntul de produse de origine animală /
non-animală înregistrate sanitar veterinar"), one file per unit category,
covering the **whole county**. Saved by the owner in their own browser on
2026-10-07 (staging's drafts, "Band D, the first three Romanian cities'
files complete"); **the DSVSA hosts refuse scripts and were not touched for
this brief.**

### The saved files, measured 2026-10-07

`data/cluj_napoca/raw/` (animal-origin list, `A`) and `raw/non-animal/`
(`N`). The code is the build's `source_files` value (Bucharest's `A<nn>` /
`N<nn>` scheme). "Date" is the date the file itself states; the site's list
pages were dated 18-29/09/2026 (animal) and 07/10/2026 (non-animal) when
the owner saved them. Header row is 1-based. "Unknown" names no locality
this brief could read (below).

| Code | File | Bytes | SHA-256 (first 16) | Date in file | Header | County rows | In city | Elsewhere | Unknown | Bucket |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | 01.inregistrate-carmangerie.xls | 105,472 | `137d5b6ed5914d01` | 15.09.2026 (an Excel serial, 46280, no label) | 7 | 22 | 7 | 15 | 0 | Food shops |
| A02 | 02.inregistrate-macelarie.xls | 101,376 | `07d5496e889e40fd` | 15.09.2026 (serial) | 21 | 4 | 1 | 3 | 0 | Food shops |
| A15 | 15.inregistrate-magazin-desfacere-miere.xls | 118,272 | `044d73fad049be25` | 25.09.2026 | 21 | 4 | 3 | 1 | 0 | Food shops |
| A17 | 17.inregistrate-restaurant-bistro.xls | 704,000 | `3e6a8eb2a8b19454` | **29.06.2026** | 21 | 3,113 | 1,970 | 1,073 | 70 | Food service |
| A18 | 18.inregistrate-pizzerie.xls | 202,240 | `eb44ad444be94629` | 25.09.2026 | 21 | 405 | 287 | 117 | 1 | Food service |
| A21 | 21.inregistrate-cofetarie_patiserie.xls | 181,760 | `cd08919fc1e38a05` | 25.09.2026 | 19 | 350 | 261 | 82 | 7 | Food shops |
| A23 | 23.inregistrate-magazin-alimentar.xls | 1,045,504 | `da52efeccf6512fb` | 25.09.2026 | 21 | 4,716 | 2,174 | 2,240 | 302 | Food shops (shop-first) |
| A24 | 24INREGISTRARE-SUPERMARKET.xls | 147,456 | `f3ac53f85b0fe751` | 28.09.2026 | 21 | 234 | 123 | 101 | 10 | Food shops (shop-first) |
| A36 | 36.inregistrate-Bar.xlsx | 168,430 | `b9940846f7ce2db2` | **30.04.2026** | 21 | 1,235 | 610 | 563 | 62 | Food service |
| N01 | 01.-FABRICARE-PAINE.xls | 103,936 | `6cc35b7890a2fbdf` | 06.10.2026 | 18 | 19 | 2 | 17 | 0 | Food shops |
| N02 | 02.inregistrate-prajituri_proaspete-patiserie.xlsx | 69,042 | `987eef23f4a4ba70` | 06.10.2026 | 16 | 156 | 87 | 56 | 13 | Food shops |
| N03 | 03.inregistrate-paine_prajituri_proaspete-patiserie-1-ok.xlsx | 61,350 | `9da1a32b5d02cf96` | 06.10.2026 | 18 | 95 | 32 | 62 | 1 | Food shops |
| N19 | 19.inregistrate-fabricare-inghetata_25047ro.xlsx | 67,339 | `efd5139501aee774` | 06.10.2026 | 18 | 7 | 4 | 3 | 0 | Food service |
| N26 | 26.inregistrate-comercializ-cu-amanuntul-prod-nonanimala.xlsx | 93,685 | `b203ce558a526971` | 06.10.2026 | 14 | 490 | 284 | 115 | 91 | Food shops (shop-first) |
| N27 | 27-.inregistrate-Bar_25092ro-1.xlsx | 118,931 | `58fc0c88abd40a3e` | 06.10.2026 | 21 | 650 | 325 | 280 | 45 | Food service |
| N29 | 29.inregistrate-cantine-catering_restaurant-vegan.xlsx | 64,572 | `fde2868c8fa7fde6` | 06.10.2026 (a bare date cell) | 15 | 63 | 43 | 12 | 8 | split (call 6) |
| N33 | 33.inregistrate-comercializ-prod-nonanimala-congelate.xlsx | 67,668 | `34568629f1a2ff14` | 06.10.2026 | 16 | 24 | 17 | 6 | 1 | Food shops |
| | **17 files** | **3,421,033** | | | | **11,587** | **6,230** | **4,746** | **611** | |

The animal-origin list has **no
fishmonger file and no file 10**, as the owner noted; Bucharest's file 11
(fishmongers) has no counterpart here.

### 🚨 Traps a Bucharest copy would walk into

1. **The file numbers are the county's own.** Cluj's A23 is the food shop
   file and A21 the confectioners; Bucharest's A23 is confectioners and A25
   food shops. Cluj's A17 is restaurants (Bucharest A19), A24 supermarkets
   (A26), N26 retail (N33), N27 bars (N36), N19 ice cream (N24), N33 frozen
   food (N42). `romania_dsvsa.py` keys its buckets on Bucharest's codes, so
   **the file-to-bucket map has to become per city**, with Bucharest's
   outputs unmoved (`drift_check.py bucharest` is the control). A Cluj code
   read through Bucharest's map silently re-buckets food shops as
   confectioners and raises on A17, A24, A36, N26, N27, N29.
2. **There is no ANULATE section.** Not one of the 17 files has a cancelled
   section, a status column or struck-through rows (fonts and fills read
   per cell: none meaningful). Five rows county-wide carry a closure note in
   an unheaded column: "închis" (closed) 2 in N02, "suspendată" 1 in N03, a
   suspension note 1 in N19, "anulat" 1 in A17. Step 2 drops those and
   reads the rest as registered units (call 4).
3. **N26's columns are swapped, row by row.** Its header says Adresa then
   Categorie unitate, but **most rows carry the category under Adresa and
   the address under Categorie** (84% of the Categorie cells carry a digit,
   2% of the Adresa cells), and a few rows are the right way round. Decide
   **per row by content**, never by the header.
4. **No Sector or locality column.** The locality leads the address text
   (99.1% of in-city rows begin with the city's name). The county's other
   towns and communes are named the same way, and street names such as
   Calea Florești, Calea Turzii and Piața Mihai Viteazu name other places:
   a locality word right after a street-type word is a street.
5. **Header rows differ** (row 7 to 21), A15's cells are merged (address in
   column E, category in J, registration in M), and every file ends in
   blank numbered rows (only `Nr. crt.` filled: up to 433 in N27). Parse by
   the header's names, then by content; skip rows with fewer than three
   filled cells. A01, A23, A36 and N27 have extra empty sheets (step 2
   checks they stay empty, as Bucharest's does).
6. **Five dates, not one.** A36 (bars) is dated 30.04.2026 and A17
   (restaurants) 29.06.2026; the others 15.09 to 06.10.2026. The page
   states the range (call 3).
7. **Two bars lists.** A36 sits in the animal-origin listing but its own
   title says non-animal origin; N27 is the non-animal list's bars file. They
   share **436 registration numbers** county-wide (A36 1,203, N27 632). In
   the city: A36 579 premises, N27 318, **187 in both** (call 2).

### Columns

`Nr. crt.`, `Denumirea unității` (the unit's legal name), `Adresa`,
`Categorie unitate` (free text, case and spelling variants: "fast food",
"fast-food", "fast- food"), `Numărul de înregistrare și data înregistrării`.
Unheaded, in some files: a date in column F (A17 275 rows, A23 211, A24 27;
all 2025-2026, unlabeled, perhaps a renewal or change date), and a two-letter
code in column F, G or K on 6-11% of rows (63% in N29) (`RM`, `RS`, `RR`; unlabeled,
**ASSERTED** to be a risk class: medium, low, high). Neither is used.

### Locality and duplicates

- **In the city: 6,230 rows** (the address names Cluj-Napoca: "Cluj-Napoca",
  "Cluj Napoca", "Mun. Cluj", "Cluj-N", with "jud. Cluj" removed first).
  Elsewhere in the county: 4,746. **Unknown: 611** (the address names no
  locality this brief's list of the county's towns, communes and common
  villages catches); only **26 of them** match a Cluj-Napoca street and
  number, so the build leaves the unknowns out and counts them.
- **One unit in several files**: the 6,230 rows merge on Bucharest's key
  (folded name + parsed street + number) to **5,626 premises**. 360
  premises sit in two or more files (A36 + N27 170, A17 + A23 60,
  A21 + A23 29, A17 + A36 24), and 221 rows repeat within one file.
  Bucharest's rule handles both: merge, keep every file in `source_files`,
  and let a shop file (A23, A24, N26 here) win the bucket.

### Address shape (the 6,230 in-city rows)

A number in **93.1%**; "nr." written in 13.2%; block parts (bl, sc, et, ap)
in 14.8%; "fn" (fără număr, no number) in 5.2%; a street-type word in only
30.9% (most rows write the bare street name after the city); market, mall or
stand words in 7.2%.

### Buckets and exclusions, on Bucharest's precedent

The FILE decides the bucket, the category text the exceptions
(`romania_dsvsa.py`'s contract). Food service: A17, A18, A36, N27, N19, and
N29's fast food. Food shops: A01, A02, A15, A21, A23, A24, N01, N02, N03,
N26, N33; a premises in A23, A24 or N26 is a food shop even with a
food-service registration (Bucharest's `SHOP_FIRST`).

**Left out by Bucharest's rule** (in-city premises): catering alone 41
(R1; N29's catering rows), pastry labs 26, in-house buffets ("bufet de
incintă") 19, mobile units 12, vending machines 5, trailers 3 — **106**.
"Restaurant-catering" (6) stays, as Bucharest's "restaurant/catering" did.

**For the owner** (calls 6-10): pharmacies 74, stalls 118, fixed kiosks 15,
canteens 4, production-named bakeries 49.

### Names — the owner's rule applies unchanged

`Denumirea unității` is the legal entity, not always the sign. Of the 5,626
in-city premises, **5,139 carry an SRL or SA form**; **90 (1.6%) read as
sole traders** on Bucharest's `SOLE_TRADER` test (PFA 33, II 25, the long
forms 24, IF 2), and **none** as a company named only as a person on its
`is_person_name` test. So the page shows the company name without its legal
form and the category for the 90 (owner, 2026-09-28 and 2026-09-29). No
address reaches the map. Run `check_personal_exposure.py cluj_napoca`
before publishing; sole-trader forms first.

---

## Placement — the OSM address join

**Inputs**: OSM address objects with `addr:street` and `addr:housenumber`
inside relation 3277038: **22,217** (10,370 nodes, 11,812 ways, 35
relations; 931 street keys), fetched 2026-10-07 via overpass-api.de with
Bucharest's query on this relation (1,644,797 bytes, sha256
`d4cd44963e7e7bc1`, a scratch copy, not cached in `data/`). OSM draws 1,219
named streets in the city. Bucharest: 145,892 objects for 1.7 million
people; Cluj: 22,217 for 324,576 (the relation's `population` tag).

**Method**: the 5,520 storefront premises (5,626 less the 106 above),
parsed by Bucharest's `parse_address` after the locality is stripped, and
placed by its `place()` (imported read-only) with no sector test (Cluj has
none), the street type kept, and the one-site test (150 m hops, 600 m wide).

| Tier | Premises | Share |
|---|---|---|
| exact (street + number) | 2,990 | 54.2% |
| whole number (14A → 14) | 77 | 1.4% |
| tolerant key (one OSM street only) | 254 | 4.6% |
| **placed** | **3,321** | **60.2%** |
| no street (about 340 leave no street name once parsed; the rest name a street OSM's addresses lack) | 830 | 15.0% |
| street only (592 of the 679 are streets OSM draws: **OSM lacks the number**) | 679 | 12.3% |
| no house number | 414 | 7.5% |
| ambiguous (two streets, or two sites) | 276 | 5.0% |

- **By bucket**: Food shops 1,695 of 2,799 (60.6%), Food service 1,626 of
  2,721 (59.8%).
- **Block addresses place better**: 71.0% (536 of 755) against 58.4%
  without block parts: the housing estates are better mapped than the
  older streets.
- **Control**: with the street-type test off, 3,328 (60.3%).
- **Headroom measured**: three Cluj repairs (date-named streets such as
  "21 Decembrie 1989" kept whole instead of read as number 21, one-letter
  initials dropped, "nr." spacing) give **3,510 of 5,537 (63.4%)**. The
  rest of the gap is OSM's: it lacks the number or the street's addresses.
  Street-level placement for street-only rows is not proposed (Bucharest's
  reasoning: a long street is kilometers).
- **Not yet done**: Bucharest's second method (house-level Nominatim
  answers against placed points) is a build-time control.

---

## Rail — CTP's trams, from OpenStreetMap

**OSM, fetched 2026-10-07** (bbox 46.70,23.45,46.83,23.72, `route` tram,
light_rail or subway): **8 `route=tram` relations**, all operator CTP
(Compania de Transport Public Cluj-Napoca), PTv2, **none with a `colour`**;
3 route masters ("Tramvai 100", "Tramvai 101", "Tramvai 102"). **No subway
or light_rail relation**: the metro is under construction, so nothing to
draw (a watch item).

| Ref | Relations | Stop members per direction (OSM) | Operator's stops per direction (CTP linear maps, READ 2026-10-07) | Length | Termini |
|---|---|---|---|---|---|
| 100 | 5671140, 5671141 | 10 / 10 | 10 / 10 | 5.5-5.6 km | B-dul Muncii (UNIMET) ↔ Piața Gării |
| 101 | 5673690, 5673691 | 10 / 11 | 9 (P-ța Gării → Clăbucet) / 11 | 6.8-6.9 km | Str. Bucium ↔ Piața Gării |
| 102 | 5673735, 5673736 | 19 / 20 | 19 / 20 | 12.1-12.3 km | Str. Bucium ↔ B-dul Muncii |
| 102L | 3793880, 13922576 | 0 / 0 | (depot runs) | 1.2-1.9 km | Disp. Bucium ↔ Depou: `NOT_DRAWN`, no stops |

- **102 runs the whole axis**; 100 is its eastern half (Piața Gării to the
  CUG industrial platform), 101 its western half (Piața Gării to
  Mănăștur). Every stop of 100 and 101 is a 102 stop.
- **38 distinct stop names, all 38 inside relation 3277038**; no stub, no
  stop outside the city.
- **The operator names each direction's stop separately.** Paired across
  the two directions, the network is **20 stations** (call 11): Disp.
  Bucium carries one name both ways; 9 pairs differ only by
  Nord/Sud/Est/Vest/Tram or Noi/Vechi; **6 western pairs carry two
  different names** (Horea / Facultatea de Litere, Opera Maghiară Est /
  Parcul Central, Splaiul Independenței / Cluj Arena, Gr. Alexandrescu /
  Calvaria, Răvașului / Parâng, Clăbucet / Baza Unirea; 20-248 m apart); 3
  pairs have one side unnamed in OSM (below); G. Barițiu has no
  opposite-direction stop.
- **Three stop members have no name** (nodes 11067242917, 11259441754,
  11254713222, tagged only `operator`). CTP's linear maps name them
  **Libertatea Est Tram, Primăria IRIS and Sala Sporturilor**. `osm_tram`
  stops on an unnamed member, so the build needs a config entry or an OSM
  fix (call 11).
- **Gate 3** (`tram-city` section 2): CTP's own linear stop maps
  (`ctpcj.ro/orare/png/img_<line>_lv_<inbound|outbound>.png`, read
  2026-10-07, for the count only) match OSM per direction, with one known
  reason to write beside the figure: CTP's 101 map towards Bucium ends at
  Clăbucet, where OSM's relation runs on to Disp. Bucium. Secondary: Romanian
  Wikipedia's line table (revision 17646299, edited 14 April 2026) gives 9,
  11 and 19 stations per line and 11.7 km.

### Frequency — READ from CTP's timetables

CTP's weekday timetables, valid from 07.09.2026 (`ctpcj.ro/orare/pdf/orar_<line>.pdf`,
read 2026-10-07), departures 10:00-16:00:

| Line | Midday, each terminus | Weekday span | Master list (earlier read) |
|---|---|---|---|
| 100 | every **17-18 min** | 09:03-20:44 only (no morning peak) | 16.7 |
| 101 | every **10.6 min** | 06:10-22:16 | 10.3 |
| 102 | every **13-14 min** | 04:45-22:39 | 13.6 |

Combined on the shared track at midday: about every 7.7 minutes on the
eastern half (100 + 102), every 6 on the western half (101 + 102), and
every 4.5 at Piața Gării (all three; the master list's "about every 4.3").
Saturday and Sunday timetables exist for all three.

**Kit call 2 applies, no new call**: 100 is slower than the light-rail
test's 15 minutes but within call 2's 20-minute floor, it is street track
(no frequency gate), and every one of its stops is also served by 102, so
no stop is infrequent. All three are drawn and the page states the waits.

---

## Licence and notices

- **DSVSA Cluj: SILENT, on Bucharest's precedent** ("silent, the absence
  established": `bucuresti.dsvsa.ro` has no terms page, its privacy policy
  says nothing of reuse, the ANSVSA footer is a website footer, and **no
  DSVSA data is on `data.gov.ro`**, a search of the national catalogue that
  covers every county). **What was not checkable here**: DSVSA Cluj's own
  site (its terms, privacy page and footer), because the county hosts
  answer scripts with 403 or 503 and were not touched. The owner can confirm
  in the browser that the Cluj site has no terms page either.
- **Notice**: 67 is Bucharest's ("displayed by choice, not required",
  wording approved 2026-09-29). A Cluj page needs the same credit for DSVSA
  Cluj (call 12).
- **OpenStreetMap**: ODbL 1.0, the address join and the rail and boundary;
  notice 1, already on every page.
- **CTP's timetable pages and linear maps**: read for frequency and gate 3
  only, never republished (`tram-city` section 2). CTP's "Termeni și
  condiții" page was not read. Tranzy, CTP's open-data partner, needs a key
  (Iași's shape) and is not used.
- **The city portal**: `data.e-primariaclujnapoca.ro` answers with a
  1.4 KB e-Primăria shell and its CKAN API with 404 (2026-10-07), as the
  master list records.

---

## Open calls for the owner (precedent first)

1. **Band B, the placement gap disclosed** (recommended). Precedent:
   Bucharest, "build, with the unplaced share disclosed" (owner,
   2026-09-28), and Incheon's disclosed gap. Tradeoff: 60.2% (63.4% with the
   measured repairs) is the lowest of any built city, so about two
   storefronts in five are missing from the map, and where OSM's addresses
   are thin the density reads thin. A placement floor above about 64%
   would make it Band C until OSM's Cluj addresses fill in.
2. **Both bars lists, merged** (recommended): A36 (30.04.2026) and N27
   (06.10.2026) merged on name and address as every other file is, the page
   stating both dates. Tradeoff: the 392 in-city premises only in A36 may
   have closed since April. N27 alone would lose them, though N27 is not a
   simple update: it holds fewer 2024-2026 registrations than A36.
3. **The page states the date range** (recommended): "dated 30 April to
   6 October 2026", the currency rule's data date. Tradeoff: two files
   (restaurants and bars, a third of the premises) are three to five months
   older than the rest.
4. **Read the lists as active; drop the five closure-noted rows; disclose**
   (recommended). Precedent: the currency rule (the source drops closed
   businesses). Tradeoff: the Cluj lists have no cancelled section, so
   whether DSVSA Cluj removes closed units is not stated; registrations run
   back to 2007. The page says the lists are registrations.
5. **Unknown-locality rows out, counted** (recommended): 611 county rows
   name no readable locality; 26 match a Cluj street and number. Tradeoff:
   up to 26 city premises lost (0.5%).
6. **N29 split by its category** (recommended): catering 42 in the city out
   (R1; Bucharest left catering, file 31, out), fast food 1 kept (Food
   service), the two mobile fast-food units out (mobile units row). The
   file's "restaurant vegan" names no row. Tradeoff: none measured.
7. **Pharmacies out** (recommended): 74 in-city premises (58 placed) whose
   category names a pharmacy ("farmacie", "magazin alimentar - farmacie").
   Precedent: a food-only register's pharmacies are out (Stockholm,
   `docs/category_rules.md`). Tradeoff: some may sell food as a real shop
   counter; keeping them is a departure.
8. **Stalls out, fixed kiosks kept** (recommended): "stand" 118 in-city
   premises (62 placed; 114 food shops, 4 food service, many inside markets)
   out on R1 (street and market stalls); "chioșc" 15 (6 placed) kept as
   fixed kiosks (Thessaloniki's call 2: a fixed kiosk is not a mobile unit).
   Tradeoff: some stands are counters inside a mall; Bucharest's regex has
   no "stand" (its register had one such row, not placed).
9. **Canteens out** (recommended): "restaurant-cantină" 4 (1 placed), R1;
   Bucharest left canteens (file 21) out. Tradeoff: none.
10. **Production-named bakeries kept** (recommended): 49 in-city premises
    (29 placed) whose category reads "fabricarea pâinii" or "unitate de
    producție". Precedent: Bucharest kept its bread-making files (164 placed
    rows named "fabric..."). Tradeoff: some are bakeries with no counter.
11. **Stations as direction pairs, labeled with the operator's names**
    (recommended): pair each direction's stop with the nearest opposite stop
    in line order (furthest pair 260 m), **20 stations**; a pair whose two
    names differ is labeled with both ("Opera Maghiară Est / Parcul
    Central"); the three unnamed OSM nodes are named in config by node id
    from CTP's linear maps, each with its expected position. Precedent:
    `tram-city` section 2 (a rename or a merge of differently named stops
    goes to the owner). Tradeoff: Aarhus's exact-name collapse needs no
    call but gives 41 points 67 m apart (median), rings stacked on rings;
    the base-name collapse gives 29 (26 + 3) and still splits the six
    western pairs.
12. **The DSVSA credit for Cluj** (recommended): one Romanian DSVSA notice
    naming each county directorate in notice 67's approved wording,
    "DSVSA București" and "DSVSA Cluj". Tradeoff: a new notice per county
    keeps 67 untouched but multiplies near-identical notices (Timișoara and
    Iași follow).
13. **Step 0 downloads for the owner to approve** (the build's
    `fetch_sources.py`, publisher's own hosts): the OSM address objects in
    relation 3277038 (about 1.6 MB, Bucharest's query), the relation's
    boundary, and the tram relations with their stop nodes. No GTFS (none
    used) and nothing from DSVSA (the owner's files are the cache).

---

## Watch items

- **The metro**: under construction; when it opens, `mode` and the page
  change, and the brief's `subway` count of 0 fails (by design).
- **OSM's three unnamed stops**: if a mapper names them, call 11's config
  entries must go (`osm_tram`'s staleness checks).
- **Timetables**: 101's and 102's weekend tables date from 14.06.2025; the
  weekday ones from 07.09.2026.

## ⚠️ What the checks cannot cover

**The saved files have no check.** `brief_check.py` has no kind for a local
file (`row_count` reads a CSV, and these are XLS and XLSX), and adding one is
outside a brief. The table above records each file's bytes and SHA-256
prefix; the build's `fetch_sources.py` prints the hashes, as Bucharest's
does, and a changed file is a new fetch to re-measure. **The DSVSA host is
not checked** for Bucharest's reason: it answers scripts with a refusal, and
the framework only asserts success.

```brief-checks
[
  {
    "id": "cluj-osm-tram-relations",
    "claim": "OSM carries CTP Cluj's trams as 8 route=tram relations in the city bbox (100, 101, 102 in both directions; 102L's two depot runs with no stops), and no subway or light_rail relation (the metro is under construction)",
    "kind": "osm_route_refs",
    "bbox": [46.70, 23.45, 46.83, 23.72],
    "routes": ["tram", "subway", "light_rail"],
    "expect_relations": {"tram": 8, "subway": 0, "light_rail": 0},
    "expect_refs": {"tram": 4},
    "require_refs": {"tram": ["100", "101", "102", "102L"]}
  },
  {
    "id": "cluj-boundary-relation",
    "claim": "The scope is OSM relation 3277038, Cluj-Napoca, an administrative boundary (admin_level 8; 174.9 km2 in UTM 34N measured 2026-10-07)",
    "kind": "http_contains",
    "url": "https://www.openstreetmap.org/relation/3277038",
    "present": ["Cluj-Napoca", "admin_level", "boundary"]
  },
  {
    "id": "cluj-utm-zone",
    "claim": "Cluj-Napoca (23.59 E) projects to UTM 34N, EPSG:32634, not Bucharest's 35N",
    "kind": "utm_zone_from_longitude",
    "lon": 23.59,
    "expect": "EPSG:32634"
  },
  {
    "id": "cluj-ctp-line-102-page",
    "claim": "CTP's own page for tram 102 runs Str. Bucium to B-dul Muncii and links the timetable PDF the frequencies were read from",
    "kind": "http_contains",
    "url": "https://ctpcj.ro/index.php/ro/orare-linii/linii-urbane/linia102",
    "present": ["orar_102.pdf", "Str. Bucium", "B-dul Muncii"]
  },
  {
    "id": "cluj-ctp-timetable-100",
    "claim": "CTP's timetable for tram 100 (weekdays 09:03-20:44, every 17-18 minutes at midday, valid from 07.09.2026) is published as a PDF",
    "kind": "http_ok",
    "url": "https://ctpcj.ro/orare/pdf/orar_100.pdf",
    "content_type_contains": "pdf"
  },
  {
    "id": "cluj-ctp-timetable-102",
    "claim": "CTP's timetable for tram 102 (every 13-14 minutes at midday, valid from 07.09.2026) is published as a PDF",
    "kind": "http_ok",
    "url": "https://ctpcj.ro/orare/pdf/orar_102.pdf",
    "content_type_contains": "pdf"
  },
  {
    "id": "cluj-wikipedia-line-table",
    "claim": "Gate 3's secondary source: Romanian Wikipedia's tram article carries a per-line station table (9, 11 and 19) and the 11.7 km network length",
    "kind": "http_contains",
    "url": "https://ro.wikipedia.org/wiki/Tramvaiul_din_Cluj-Napoca",
    "present": ["Număr stații", "11,7 km"]
  },
  {
    "id": "cluj-city-portal-api-gone",
    "claim": "The city's open-data portal has no CKAN API (404), so the city portal offers no second bucket",
    "kind": "endpoint_absent",
    "url": "https://data.e-primariaclujnapoca.ro/api/3/action/package_list",
    "expect_status": 404
  }
]
```
