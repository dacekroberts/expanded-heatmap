# Iași — build brief

**Written 2026-10-07 by staging, on the owner's request ("write the briefs
for those three now").** Every figure below was measured that day on the
files the owner saved from DSVSA Iași's site into `data/iasi/raw/` and
`data/iasi/raw/non-animal/`, on OpenStreetMap through Overpass, and on CTP
Iași's own pages. Run `python scripts/brief_check.py iasi` before writing any
code for this city. Bucharest (`docs/build_briefs/bucharest.md`,
`pipeline/bucharest/`) is the template for the business leg; the tram-city
and osm-rail skills, through `pipeline/osm_tram.py`, for the rail.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **Band** | **C** (the master list has it in D) | The owner's fetch is done, so D's act is complete. **The first blocker is now the placement**: the OSM address join places **43.9%** of the storefronts, **61.0%** with Incheon's nearest same-side number, under the reduced-bucket bar's **70%** (Bucharest 74.9%, Palma 79.6%). One measurement stands between Iași and B: a placement source that reaches 70% (call 1). Without one, Santa Cruz–La Laguna's precedent (57.7%, to the discards, owner 2026-09-30) applies |
| **`mode`** | **`tram`** | Street trams, no metro |
| **`coverage`** | **`one_bucket`** | DSVSA registers food units only: Food service and Food shops, as Bucharest |
| **Scope** | **Municipiul Iași**, OSM relation **1207838** (admin_level 8, 91.9 km² in UTM 35N) | The register is county-wide and is filtered to the municipality |
| **Lines** | The operator's **9 tram lines** (1, 3, 5, 6, 7, 8, 9, 11, 13), drawn over OSM's track as the operator runs them now (call 4) | OSM's relations for 1, 8, 9 and 13 still run to Copou, which is closed for works |
| **Rings** | **0.05 / 0.1 / 0.2 / 0.3 mi** | Median stop gap **399 m** over OSM's 57 named stops in the city (the spacing rule: 550 m or less) |
| **CRS** | **EPSG:32635** (UTM 35N, 27.59° E) | Derived from the longitude, as Bucharest's |
| **Region** | `"Europe"` | |

---

## The one-line summary

**Bucharest's business route with a county list, a renumbered file set and a
thin address map.** The register is the same authority's, in the same
shape, and the owner has already saved it. What is Iași's own: the lists
cover the whole county (47% of active rows are in the city), the file
numbers mean different things than Bucharest's, the closed units are marked
differently, and OpenStreetMap holds only 4,551 addresses in the city, so
the join places fewer than half the storefronts.

| | Bucharest (built) | **Iași** |
|---|---|---|
| Register | DSVSA București, 17 files | **DSVSA Iași, 16 current files** (+2 old, call 2) |
| Rows in the city | the whole file (one municipality) | **3,464 of 7,421 active rows**; the rest are elsewhere in the county |
| Storefront premises | 20,821 | **3,063** (Food shops 1,634, Food service 1,429) |
| OSM address objects | 145,892 | **4,551** |
| Placed | 74.9% | **43.9%**; 61.0% with the nearest same-side number |
| Rail | Metrorex M1–M5, 64 stations | **CTP Iași trams, 9 lines, 57 OSM stop names in the city** |
| Rings | standard | **halved** (399 m median gap) |

---

## Business leg — DSVSA Iași, food only

### The files the owner saved (2026-10-07)

All 18 are old-format Excel (`.xls`, OLE2), one sheet with data (two carry
an empty `Sheet2`), letterhead above the header. **Each file prints its own
date** on row 10 ("Data ultimei actualizări"). The owner's page listing of
the animal-origin files was dated 05/10/2026; the files themselves print
30.09.2026.

| File | Bytes | SHA-256 prefix | Date printed | Active | Closed | Active in the city |
|---|---|---|---|---|---|---|
| `4-inregistrate-carmangerie.xls` (pork butchers) | 110,080 | `69ed241e31c6f74f` | 30.09.2026 | 32 | 1 (suspended) | 11 |
| `14-inregistrate-cofetarie-patiserie.xls` (confectioners) | 126,464 | `45feff90d76f155a` | 30.09.2026 | 105 | - | 82 |
| `18-inregistrate-hipermarket_supermarket.xls` | 138,240 | `f9131a4d7b36b77c` | 30.09.2026 | 166 | - | 94 |
| `20-inregistrate-macelarie.xls` (butchers) | 120,832 | `9d834d470b02267b` | 30.09.2026 | 86 | - | 56 |
| `21-inregistrate-magazin-alimentar.xls` (food shops) | 699,392 | `4a8504bac3320e06` | 30.09.2026 | 2,953 | - | 838 |
| `22-inregistrate-magazin-desfacere-miere.xls` (honey) | 106,496 | `48484f63448fc9fd` | 30.09.2026 | 6 | - | 4 |
| `23-inregistrate-magazin-desfacere-peste.xls` (fishmongers) | 111,616 | `a87d879125834445` | 30.09.2026 | 46 | - | 24 |
| `26-inregistrate-pizzerie.xls` | 123,392 | `04f0a4d8d73e9842` | 30.09.2026 | 97 | - | 55 |
| `28-inregistrate-restaurant-fast-food-bar.xls` | 434,688 | `a5a1995f92c780a9` | 30.09.2026 | 1,467 | - | 906 |
| `non-animal/Baruri.xls` (bars, cafés) | 449,536 | `0024017d00b6fb7c` | 25.06.2026 | 1,434 | 226 | 651 |
| `non-animal/Comercializ-prod-nonanimala-congelate.xls` (frozen) | 147,456 | `92714419a0d8fe4b` | 25.06.2026 | 191 | 51 | 134 |
| `non-animal/Comert-cu-amanuntul-exclusiv-supermarket-hipermarket.xls` (retail) | 299,520 | `449dfa2256042a37` | 25.06.2026 | 677 | 240 | 518 |
| `non-animal/Fabricare-inghetata.xls` (ice cream) | 95,744 | `23839dd198d32bfb` | 23.06.2026 | 10 | 3 | 5 |
| `non-animal/Fabricare-paine.xls` (bread) | 118,272 | `2ba33452eeb877fa` | **20.06.2025** | 22 | 56 | 7 |
| `non-animal/Paine-prajituri-proaspete-patiserie.xls` (bread and pastry) | 151,040 | `febd1fb437d1130d` | 23.06.2026 | 113 | 166 | 69 |
| `non-animal/Prajituri-proaspete-patiserie.xls` (pastry) | 101,376 | `95d40b5d31dc884c` | **04.04.2025** | 16 | 17 | 10 |
| `non-animal/Restaurante.xls` | 101,888 | `a081be0fef091b2c` | **03.09.2021** | 1 | 4 | 1 |
| `non-animal/Supermarket-hipermarket.xls` | 104,448 | `cf9741ee26c92ca8` | **19.10.2017** | 52 | (no section) | 34 |
| **Total** | **3,540,480** | | | **7,474** | **764** | **3,499** |

The 16 current files hold **7,421 active rows, 3,464 of them in the city.**
Canteens and catering ("Cantine-si-catering") were not taken, on Bucharest's
precedent (R1 in `docs/category_rules.md`).

### The shape, and three traps for a build that copies Bucharest's step 2

- **Columns** (header on row 18; row 19 in file 21): `Nr. Crt.`,
  `Denumirea unităţii` (the unit's name), `Adresa`, `Categorie unitate`,
  `Numărul de înregistrare şi data înregistrării`. Every active row fills all
  five, except 3 blank categories in file 21, 1 in file 26 and 6 in Baruri.
  **There is no Sector or locality column**: the locality is inside
  `Adresa`'s free text.
- 🚨 **Trap 1: the file numbers are not Bucharest's.** `romania_dsvsa.py`
  keys on Bucharest's codes, and Bucharest's step 2 derives the code from
  the file name's leading number. Run on Iași's files, that would read
  **Iași's 20 (butchers) as Bucharest's A20 (pizzerias, Food service)**,
  Iași's 26 (pizzerias) as A26 (supermarkets, a shop-first file) and Iași's
  23 (fishmongers) as A23 (confectioners). The non-animal files carry no
  number at all. **The config must map each file name to its role**
  (Iași 04 → A01, 20 → A02, 23 → A11, 22 → A16, 28 → A19, 26 → A20,
  14 → A23, 21 → A25, 18 → A26; Fabricare-paine → N01, Prajituri → N02,
  Paine-prajituri → N03, Fabricare-inghetata → N24, Comert-cu-amanuntul →
  N33, Baruri → N36, Congelate → N42), never derive it from the number.
- 🚨 **Trap 2: closed units are marked differently, and only in some
  files.** There is no ANULATE row. The non-animal files put their closed
  units below a row reading **"UNITĂȚI ÎNCHISE/DESFIINȚATE/INACTIVE"**
  (closed, dissolved, inactive; Fabricare-inghetata spells it "Unitati cu
  ativitatea inchisa"); file 4 has one unit below **"UNITATI CU ACTIVITATE
  SUSPENDATA"** (suspended). **The other eight animal-origin files have no
  section marker, no status column and no formatting difference** (one font,
  no strike-through, no fill, on every row): either DSVSA Iași leaves closed
  units off those lists or it does not mark them, and the files cannot say
  which. Step 2 cuts at any of the three markers and stops on an
  unrecognised one-cell row (file 21 has one five-character cell on row 261,
  file 26 a one-character cell on row 20: read them at the build).
- **Trap 3: the category column is sometimes a CAEN code.** Six non-animal
  files write CAEN Rev. 2 codes (4711, 4721, 4724, 4725, 4729, 1052, 1071,
  1082) instead of words. The file still decides the bucket; the codes only
  matter for the exclusions below.
- Registration years run from 2001 to 2026 (one 2027 and one 2039, typos).

### Inside the municipality: the locality is parsed from the address

Each list covers **the whole county**: Pașcani, Hârlău, Târgu Frumos, Podu
Iloaiei and the communes. Measured on the 7,421 active rows of the current
files, with a rule on markers only (no row printed):

| Class | Rule | Rows |
|---|---|---|
| **City** | "Iași" as a locality (not only inside "jud. Iași"), and none of the outside markers | **3,464** |
| Outside | "com.", "comuna", "sat", "oraș", one of the four towns, or one of the adjoining communes and villages by name (Miroslava, Valea Lupului, Tomești, Holboca, Ciurea, Bârnova, Rediu, Lețcani, Aroneanu, Popricani, Valea Adâncă, Lunca Cetățuii, Dancu and others) | 3,860 |
| County only | "jud. Iași" with no locality | 27 |
| No locality | none of the above | 70 |

- **Check against the OSM join**: of the 3,957 rows not in the city class,
  23 match an Iași street and house number exactly (17 marked outside, 5
  county only, 1 named only by an adjoining commune). A village street can
  share a city street's name, so the build keeps the text filter and also
  drops any placed point outside relation 1207838's polygon, as Bucharest's
  step 2 does.
- **The adjoining communes are left out with the rest of the county**: no
  tram reaches them except line 3's last stop (below), so the scope is the
  municipality.

### Duplicates

On the city's 3,464 current rows, **Bucharest's rule (name + parsed
address) merges them to 3,198 premises** before the storefront filter:
3,027 in one file, 144 in two, 21 in three, 6 in four. The commonest pairs
are a hypermarket's registrations (18 + 28: 26; 18 + 28 + Congelate: 7;
18 + 20 + 28: 6) and shops with a counter (21 + 28: 18), as Bucharest's.
**62 name-and-address pairs repeat inside one file** (one unit registered
twice); the merge takes them too. **498 street-and-number addresses carry
two or more different names**: a mall or a market holds many units, and
they stay separate premises.

### Address shape

Of the 3,317 kept rows: **89.5% carry a house number** (2,969), and **32.2%
name a block** ("bl."), the Iași housing estates' address form. 348 rows
have no number parsed: 54 give only a block, 80 a market or mall. Street
types parse as Bucharest's (strada, bulevardul, șoseaua, piața, calea,
aleea).

### Buckets, and what is left out (precedent first)

| Bucket (legend) | Files (Bucharest's role) | Premises in the city |
|---|---|---|
| **Food service** | 28 restaurants, fast food, bars (A19); 26 pizzerias (A20); Baruri (N36); Fabricare-inghetata (N24) | **1,429** |
| **Food shops** | 4, 20, 23, 22, 14, 21, 18 (A01, A02, A11, A16, A23, A25, A26); Fabricare-paine, Prajituri, Paine-prajituri, Comert-cu-amanuntul, Congelate (N01, N02, N03, N33, N42) | **1,634** |

Bucharest's shop-first rule (a premises in 21, 18 or Comert-cu-amanuntul is
a food shop even with a café registration) is applied. **3,317 kept rows,
3,063 premises.** Left out, each on its precedent:

- **Mobile units, kiosk carts, vending machines, street and market stalls:
  141 rows in the city** (Out, `docs/category_rules.md`: "Mobile units,
  kiosk carts, vending machines", romania_dsvsa.py, and R1's stalls).
  Iași's words are wider than Bucharest's regex, which catches 99 of the
  141: Baruri's "toneta cafenea" (48), "stand", "rulotă", "autoturism
  cafenea", "bicicletă mobilă"; Comert-cu-amanuntul's "toneta", "stand",
  "chioșc", "căruț"; Fabricare-inghetata's "aparat înghețată" (machines) and
  "chioșc". **Extending the shared regex for `stand`, `chiosc`, `aparat`,
  `triciclu`, `bicicleta`, `autoturism`, `autobuz`, `dubita` and `carut`
  must leave Bucharest's outputs unmoved** (`drift_check.py bucharest`);
  if Bucharest moves, that is an owner call, not a quiet change.
- **CAEN 4637 (wholesale, 1), 4776 (flowers, plants and pets, 3) and 4778
  (other goods, 2)** in Comert-cu-amanuntul: Out. Wholesale stays out (R4);
  a food-only register's non-food shops are out (Stockholm's pharmacies).
  One row reads 4733, not a CAEN Rev. 2 class: read it at the build.
- **Canteens and catering**: not taken (Bucharest's 21 and 31, R1).
- **No combined "canteen, catering, restaurant, vegan" file exists in Iași's
  set**, so there is nothing to split. The nearest, `Restaurante.xls`, is
  one of the two old files (call 2).

### The two old files (call 2)

| | Supermarket-hipermarket (2017) | Restaurante (2021) |
|---|---|---|
| Date printed | 19.10.2017 | 03.09.2021 |
| Active rows / in the city | 52 / 34 | 1 / 1 ("fast-food vegetarian") |
| Newest registration | 2017 | 2021 |
| In the city, same name + address in a current file | 17 | 0 |
| ... same street + number, any name | 28 | 0 |
| ... same company name, any address | 31 | 0 |
| **Matching nothing current** | **5** | **1** |

**Both fail the currency rule** (the master list's "Five rules": the newest
row under five years old; 2021-09-03 is five years and a month ago). And
the coverage they would add is **at most 6 premises**, each unconfirmed
since 2017 or 2021: the 2017 supermarkets are almost all in file 18's
current list already.

### Names and personal exposure

Measured on the 3,063 premises (counts only; no name read out):

- **91.2% of names carry a company legal form** (SRL, SA and the like):
  legal entities, as in Bucharest, not always the sign on the door.
- **230 (7.5%) carry a sole-trader form** (PFA, II, IF and the long forms,
  Bucharest's `SOLE_TRADER`). Bucharest's rule applies: the category only.
- **0 companies named only as a person** by Bucharest's test (Romanian given
  names plus a surname ending); the build's `check_personal_exposure.py`
  run is still required, sole-trader forms first.
- The page would show `Denumirea unităţii`, legal form stripped, or the
  category for a sole trader. No address reaches the map.

---

## Placement — the OSM address join, measured: 43.9%

**OSM address objects inside relation 1207838**, fetched 2026-10-07 with
Bucharest's query (`nwr["addr:street"]["addr:housenumber"](area.a); out
center;`, 291,969 bytes as CSV, overpass-api.de): **4,551 objects, 466
street keys, 4,367 street + number pairs.** Bucharest's was 145,892, so
Iași's is about 3% of it.

The join reuses Bucharest's normaliser and `place()` from
`pipeline/bucharest/step2_clean_businesses.py`, read-only, with no sector
(Iași has none) and the locality words stripped first:

| Tier | Premises | Share |
|---|---|---|
| Exact street + number | 1,107 | 36.1% |
| Whole number (14A → 14) | 60 | 2.0% |
| Tolerant street key, one OSM street | 179 | 5.8% |
| **Placed** | **1,346 of 3,063** | **43.9%** |
| Unplaced: the street, not the number | 851 | 27.8% |
| Unplaced: no number | 337 | 11.0% |
| Unplaced: no street | 268 | 8.7% |
| Unplaced: ambiguous (two streets, or points not one site) | 261 | 8.5% |

- **Control** (street type ignored, Bucharest's control shape): 1,275,
  41.6%.
- **With Incheon's nearest same-side number** (Palma's and Santa
  Cruz–La Laguna's second tier: the nearest number of the same parity,
  within 6, on the matched street): of the 851 street-only premises, 522
  more are placed (309 within 2, 145 within 4, 68 within 6), so **1,868 of
  3,063, 61.0%**. 294 have no same-side number within 6, and 35 match two
  tolerant streets.
- **Against the bar**: the reduced-bucket bar asks about 70% placed.
  Santa Cruz–La Laguna's join placed 57.7% with the same two tiers and went
  to the discards (owner, 2026-09-30); Palma passed at 66.2% on its screen
  (73.4% with the nearest-number tier) and placed 79.6% at the build.
- **By file** (each premises under its first file): from 18% (pork
  butchers, 2 of 11) and 30% (fishmongers, 6 of 20) to 63% (hypermarkets,
  58 of 92); restaurants 40%, food shops 43%, bars 42%.
- **What misses is OSM's supply, not the parser**: OSM knows the street of
  84.5% of premises, but holds the number for few of them. Better
  normalisation (the address-join skill's patterns) can recover part of
  the 261 ambiguous and 268 no-street rows; it cannot add numbers OSM lacks.
- **No second method was run** (Bucharest's Nominatim sample). Nominatim
  reads the same OSM, so it would test the join's accuracy, not raise its
  rate.

---

## Rail — CTP Iași's trams, from OpenStreetMap

**The operator's feed is not used.** CTP Iași's Open Data page names
tranzy.ai's portal as its GTFS route (`tranzy.ai/opendata`, real-time, said
to be open "subject at most to attribution and share-alike"); the feed needs
a tranzy.ai key, and **no key is requested** (the master list's row). So the
lines and stops come from OSM (osm-rail; ODbL, notice 1), and **CTP's own
route pages** (`sctpiasi.ro/trasee/...`) are read for headways and per-line
stop counts only, never republished.

### OSM, measured 2026-10-07 (bbox 47.05,27.45,47.25,27.75)

- **16 `route=tram` relations**, all `operator=CTP Iași`, each with a
  colour, under **9 route masters**: lines 3, 5, 6, 7, 8, 9 and 11 as
  direction pairs, lines 1 and 13 as one loop relation each.
- 🚨 **Tram 13's relation (4633529) has NO `ref`**; only its route master
  (5668463) carries `ref=13`. **A build keying on `ref` drops line 13
  silently** (the osm-rail trap). So 16 relations give 9 distinct refs
  counting the blank one: 1, 3, 5, 6, 7, 8, 9, 11 and none.
- **OSM's colours**: 1 `#ec008c`, 3 `#00a650`, 5 `#e77817`, 6 `#f9c0c1`,
  7 `#2e3092`, 8 `#d2e288`, 9 `#4ea391`, 11 `#f05b72`, 13 `#00adef`. Line 6's
  pale pink and line 8's pale green will need `line_colour_search.py`.
- **Stops**: 108 named stop members, **58 stop names, 57 inside the
  municipality.** **Dancu, line 3's terminus, lies 75 m outside** (Holboca
  commune), with 0.33 km of line 3's track: drawn to its end and listed as
  outside, on Florence's T1 precedent (owner call 17).
- **Median nearest-neighbour gap 399 m** (mean 411, minimum 214), so
  halved rings.
- ⚠️ **Four stop members are not stops**: a level crossing
  (12071260944, on 1, 8, 9 and 13 in the Copou section), a tram crossing
  (11725817468) and an untagged node (3842799350) on 7 near Gară, and an
  untagged node (9808499038) at line 9's southern end. `osm_tram.stop_rows()`
  stops on each; the two near Gară sit where CTP lists **Octav Băncilă**, a
  stop OSM does not name (call 5).
- ⚠️ **"C.E.T." spreads 213 m** across its stop positions, over
  `osm_tram.collapse`'s 200 m; and CTP now calls it **Silk District**.
  CTP also signs OSM's "Hotel Amadeo" as **Hotel Basarabia**, and spells
  "CFS 2", "CUG 1", "IPA" and "Podul de Piatră" as "C.F.S. II", "C.U.G. I",
  "I.P.A." and "Podu de Piatra" (call 5).

### 🚨 Copou is closed for works, and OSM still routes four lines there

CTP's notice of 30.09.2026: from 1 October tram 7 runs "Canta – Gara –
Bulevardul Nicolae Iorga – Baza 3 – Țuțora", **"for the whole period of the
rehabilitation works on the Copou tram line"**. CTP's route list (the page
itself says it is being updated) runs the lines as:

| Line | CTP's route (2026-10-07) | OSM's relations |
|---|---|---|
| 1 | Canta – Podu Roș – Tătărași – Canta | Copou loop |
| 3 | Gara – Târgu Cucu – Tătărași – Dancu | Gară – Dancu |
| 5 | Dacia – Gara Internațională – Țuțora | same |
| 6 | Dacia – Gara – Arcu – Târgu Cucu | same |
| 7 | Canta – Podu Roș – Țuțora (via Bd. Nicolae Iorga since 1 October) | Țuțora – Canta |
| 8 | Gara – Tudor Vladimirescu – Țuțora | Țuțora – Copou |
| 9 | Gara – Podu Roș – Spital Elytis | Tehnopolis – Copou |
| 11 | Dacia – Gara Internațională – Tătărași Nord | same |
| 13 | Canta – Tătărași – Podu Roș – Canta | Copou loop |

**Six OSM stops are served only by 1, 8, 9 and 13 on the Copou section**:
Piața Mihai Eminescu, Universitate, Triumf, George Coșbuc, Stadion and
Copou. Under the owner's rule for stations closed for works
(`docs/category_rules.md`, "Station scope", Berlin's U6), they are not
drawn or ringed, are listed as closed for works with the reopening date,
and PLAN.md carries the item to add them back. **No reopening date was
found** on CTP's news pages (call 4).

### Headways and the operator's stop counts (READ, CTP's route pages, 2026-10-07)

| Line | Weekdays | Weekends | CTP's distinct stop names (OSM's) |
|---|---|---|---|
| 1 | 10-11 min (every day) | 10-11 min | 24, one Canta loop (23, Copou loop) |
| 3 | 8-9 min | 11-12 min | 17 (17) |
| 5 | 11-12 min | 17-18 min | 17 (17) |
| 6 | 6-9 min 06:30-18:30, 10-11 off-peak | 10-11 min | 13 (13) |
| 7 | 11-12 min | 17-18 min | 19 (18) |
| 8 | 11-12 min | 17-18 min | 14, Gara – Țuțora (17, Copou – Țuțora) |
| 9 | 5-6 min at peaks, 7-8 off-peak | 7-8 min | 13, Gara – Spital Elytis (16, Copou – Tehnopolis) |
| 11 | 6-7 min at peaks, 10 off-peak | 10 min | 21 (21) |
| 13 | 10-11 min (every day) | 10-11 min | 23, one Canta loop (22, Copou loop) |

CTP's nine pages name **53 distinct stops**: OSM's 58 named stops, less
the six on the closed Copou section, plus Octav Băncilă, which OSM does
not name.

- **Every line runs at 12 minutes or better on weekdays by day**, so the
  20-minute floor (tram-city call 2) drops nothing; weekend waits of 17-18
  minutes on 5 and 7 are disclosed, Buffalo's precedent.
- **Gate 3**: CTP's lists are the operator's own, independent of OSM, but
  they follow the current diversions (line 7's page still shows the route
  before 1 October), so the counts are reconciled in config at the build
  with each reason written beside the figure.
- Each route page took about 61 seconds to answer; read them one at a time.

---

## Licences

- **DSVSA Iași: SILENT on Bucharest's precedent, the host itself unread.**
  The DSVSA county hosts answer 403 or 503 to scripts, and the rule here is
  not to touch them, so `iasi.dsvsa.ro`'s pages (a terms page, if any) were
  **not checkable** from here. **What was checkable**: the files' own
  letterhead rows name the authority, its address and contacts and the
  update date, and **carry no licence, terms or reuse text**. DSVSA's data
  is not on `data.gov.ro` (Bucharest's search of the archived national
  catalogue). Bucharest's position, "silent, the absence established", was
  read on `bucuresti.dsvsa.ro` in the browser; applying it to Iași rests on
  the same authority's same list format, not on Iași's own pages (call 3).
- **Notice 67** is written for DSVSA București; Iași needs its own sibling,
  or 67 widened to name DSVSA Iași (call 3).
- **OpenStreetMap: ODbL 1.0, notice 1**, for the tram lines and stops, the
  municipality boundary and the address points, each with its own row in
  `docs/data_sources/romania.md`.
- **CTP Iași's route pages**: read for counts and headways only, never
  republished or credited as a source of drawn data. **tranzy.ai's GTFS**:
  not used; its terms unread.

---

## Open calls for the owner

Each recommends the precedent first.

1. **Placement at 43.9%, 61.0% with the nearest-number tier**, under the
   reduced-bucket bar's 70%. Precedent: Santa Cruz–La Laguna, 57.7% on the
   same two tiers, to the discards (owner, 2026-09-30).
   - **Recommendation: C, with one measurement named**: a second placement
     source that lifts the join to 70%, looked for before any build: Iași's
     own GIS or street register with house numbers, ANCPI's INSPIRE address
     theme (Bucharest found no resolving host), each a download for the
     owner to approve. **If none reaches 70%, the discards, on Santa
     Cruz's precedent**, reopening when such a source appears.
   - **Tradeoff**: C keeps a city whose register is already saved, for one
     more search. The alternative, B on a disclosed gap, would break the
     bar: 39% of storefronts unplaced even with the second tier, and the
     placed share varies by file from 18% to 63%, so the map would show
     where OSM is mapped as much as where shops are.
   - Street-level placement for the 294 street-only rows left stays out on
     Bucharest's precedent ("a boulevard is kilometres long").
2. **The two old non-animal files.** **Recommendation: leave both out**, on
   the currency rule (newest row 2017 and 2021). **Tradeoff**: at most 6
   premises lost, none confirmed since.
3. **The licence and the notice.** **Recommendation: SILENT on Bucharest's
   precedent, disclosed, with notice 67 widened to "DSVSA București and
   DSVSA Iași"** (one notice per authority, the owner's 2026-09-29 wording).
   **Tradeoff**: Iași's own host was never read; a browser read of its
   footer and policy pages by the owner would close that, at one visit.
4. **The lines during the Copou works.** **Recommendation: draw the
   operator's current lines over OSM's track** (Manchester's routed lines,
   owner 2026-10-02, `pipeline/countries/uk.py`), leave the six Copou stops
   out as closed for works (Berlin's U6), and read the reopening date at
   the build. **Tradeoff**: routing adds work over drawing OSM's relations
   as they stand, which would draw four lines to a terminus no tram reaches
   and ring six stops nobody can board at.
5. **OSM's stop gaps and names.** **Recommendation: add Octav Băncilă by
   node** (`STATION_ADD`, Odense's precedent) once its node is found, name
   the non-stop members in config so the step can pass them, and alias
   C.E.T./Silk District and Hotel Amadeo/Hotel Basarabia in config, never
   in OSM (Manchester's rule). **Tradeoff**: each entry is a staleness check
   to keep; leaving them out drops a stop CTP serves.
6. **Line 3's Dancu terminus, 75 m outside.** **Recommendation: drawn to
   its end, listed as outside** (Florence's T1, call 17). **Tradeoff**: one
   stop's businesses uncounted.
7. **The non-storefront regex** (141 rows here, 99 by Bucharest's words).
   **Recommendation: widen `romania_dsvsa.NOT_STOREFRONT_CATEGORY`** on the
   mobile-unit and stall precedents, provided Bucharest's drift check shows
   no change. **Tradeoff**: if Bucharest moves, its page changes too, which
   is then the owner's call.

## Step 0 downloads for the owner to approve

- **OSM address objects inside relation 1207838** (Bucharest's query),
  about 292 KB, for `fetch_sources.py`.
- **The OSM tram relations, stops and boundary** (the osm_tram query),
  about 425 KB.
- **Any second placement source** call 1 finds (not yet identified).
- **Not** tranzy.ai's GTFS (needs a key) and **not** any DSVSA file by
  script (the owner's browser only).

## ⚠️ Claims that cannot be brief-checks, and why

**The saved files' sizes and row counts cannot be checked by
`brief_check.py`**: its `row_count` kind reads a CSV under the repository,
and no kind reads a local `.xls` or a file's size. They are recorded in
the table above (bytes and SHA-256 prefixes), and the build's
`fetch_sources.py` re-checks them, as Bucharest's prints each SHA-256.
**The DSVSA Iași host** cannot be a check either (Bucharest's reason: every
kind asserts success, and the host refuses scripts). The checks below cover
the OSM relation, the tram relations and refs, the operator's statements
and the CRS.

```brief-checks
[
  {
    "id": "iasi-osm-municipality",
    "claim": "OSM relation 1207838 is the municipality of Iasi, admin_level 8 (the scope polygon; the county relation 2256747 carries the same name)",
    "kind": "http_contains",
    "url": "https://www.openstreetmap.org/api/0.6/relation/1207838",
    "present": ["k=\"admin_level\" v=\"8\"", "v=\"Iași\""]
  },
  {
    "id": "iasi-osm-tram-relations",
    "claim": "OSM carries 16 tram relations in Iasi, 9 distinct refs counting tram 13's blank one (relation 4633529 has no ref; its route master does)",
    "kind": "osm_route_refs",
    "bbox": [47.05, 27.45, 47.25, 27.75],
    "routes": ["tram"],
    "expect_relations": {"tram": 16},
    "expect_refs": {"tram": 9},
    "require_refs": {"tram": ["1", "3", "5", "6", "7", "8", "9", "11"]}
  },
  {
    "id": "iasi-ctp-gtfs-via-tranzy",
    "claim": "CTP Iasi's Open Data page names tranzy.ai's portal as its GTFS route (a key is needed, so rail is OSM)",
    "kind": "http_contains",
    "url": "https://www.sctpiasi.ro/servicii/opendata",
    "present": ["tranzy.ai/opendata", "GTFS (General"]
  },
  {
    "id": "iasi-ctp-current-tram-routes",
    "claim": "CTP's route list runs lines 1 and 13 as Canta loops, 3 to Dancu and 9 to Spital Elytis (the Copou section closed for works)",
    "kind": "http_contains",
    "url": "https://www.sctpiasi.ro/trasee",
    "present": ["Trasee de tramvai", "Canta - Podu Roş - Tătăraşi - Canta", "Gara - Târgu Cucu - Tătărași - Dancu", "Gara - Podu Roş - Spital Elytis"]
  },
  {
    "id": "iasi-ctp-copou-works",
    "claim": "CTP's notice of 30.09.2026: tram 7 diverted for the whole period of the Copou tram line's rehabilitation",
    "kind": "http_contains",
    "url": "https://www.sctpiasi.ro/ro/stiri/traseul-tramvaiului-7-i-modific-itinerariul-ncep-nd-cu-1-octombrie-2026.html",
    "present": ["liniei de tramvai din Copou"]
  },
  {
    "id": "iasi-projected-crs",
    "claim": "Iasi's derived UTM zone is 35N (EPSG:32635), the municipality's centroid at 27.589 E",
    "kind": "utm_zone_from_longitude",
    "lon": 27.589,
    "expect": "EPSG:32635",
    "mode": "tram",
    "coverage": "one_bucket",
    "crs": "EPSG:32635",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
