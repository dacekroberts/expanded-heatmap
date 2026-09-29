# Bucharest — build brief

**Screening closed 2026-09-22; rail re-counted and addresses re-measured
2026-09-23.** Run `python scripts/brief_check.py bucharest` before writing any
code for this city.

> **Re-checked 2026-09-28 (staging), before the build.** These supersede the
> text below where they differ.
> - **Band B since 2026-09-27** (owner, the Band C memo), on the memo's two
>   conditions:
>   - **the owner fetches the files in their own browser**, the precedent
>     since followed for Ho Chi Minh City;
>   - **the licence stays SILENT, and the page discloses it.**
> - **The columns are known.** The screen of 2026-09-20 read them in the
>   browser (`docs/decisions/2026-09-20.md`, "Unitati de vanzare cu amanuntul
>   INREGISTRATE"):
>   - The fields are `Nr. crt.`, `Denumirea unitatii` (the unit's name,
>     trade names in the example), `Adresa`, `Sector`, `Categorie unitate`
>     and the registration number with its date.
>   - Example row: "Boutique Du Pain Bucharest, Academiei 28-30,S1, sector 1,
>     Restaurant, 6645/20.03.2023".
>   - There are **34 XLSX files, one per category**. 14 of them hold the
>     31,299 rows, and the file name is the taxonomy.
>   - The list of units of non-animal origin and 20 of the categories are
>     uncounted, so 31,299 is a floor.
>
>   So "the schema has not been read" and the one-file "56,009 bytes" below
>   are out of date. The 56,009 bytes are one of the 34 files.
> - **Rail: OSM now has 12 subway relations, M1-M5, every one with a ref and
>   a colour.** `Extensie M4` no longer appears (bbox query), so that trap is
>   gone. Colours: M1 `#FFFF00`, M2 `#003399`, M3 `#BC1725`, M4 `#347c11`,
>   M5 `#FF8040`.
> - **Both DSVSA hosts still answer 503 with the browser challenge.**
> - **The owner's browser fetch, 2026-09-28**: eight of the nine chosen
>   files (26 Hipermarket-supermarket still to come), 9,319,353 bytes, all
>   dated 25.08.2026, now in `data/bucharest/raw/` (sha256 prefixes:
>   01 `3b13434e4e3cd85a`, 02 `3d11a184654b049d`, 11 `419db7efb97c6c94`,
>   16 `7398d34557714273`, 19 `5c1fa63f00961899`, 20 `3a7655688cca630c`,
>   23 `7549ab134b5a5194`, 25 `639cbb07dc5f2899`).
>   - **Left out, as non-storefronts**: canteens (21), pastry labs (22),
>     catering (31), local producers (34), internet sales, mobile stalls,
>     vending machines, warehouses, fairs, and the farm and processing
>     categories. Canteens and pastry labs are marked for the owner's
>     confirmation.
>   - **Not yet opened**: the list of units of non-animal origin
>     (*Produse de origine non-animală*).
> - 🚨 **About a quarter of the rows are cancelled registrations.** The sheet
>   is "Active și desființate" (active and closed). Below a row reading
>   **ANULATE** ("cancelled") in each file, the rows are cancelled, printed
>   red on yellow, and carry the cancelling decision ("Decizia …"). There
>   is no status column: **the section is the status.**
>
>   | File | Active | Cancelled |
>   |---|---|---|
>   | 01 Carmangerie (pork butcher) | 116 | 145 |
>   | 02 Măcelărie (butcher) | 260 | 568 |
>   | 11 Pescărie (fishmonger) | 103 | 173 |
>   | 16 Honey shop | 5 | 3 |
>   | 19 Alimentație publică (restaurants, cafés, bars) | 9,915 | 3,363 |
>   | 20 Pizzerie | 544 | 260 |
>   | 23 Cofetărie-patiserie | 534 | 295 |
>   | 25 Magazin alimentar (food shop) | 7,540 | 2,939 |
>   | **Total** | **19,017** | **7,746** |
>
>   So the screen's 31,299 counted cancelled units as well. **Step 2 must cut
>   each file at its ANULATE row.** One row in file 19 (Nr. 379) has only two
>   filled cells, so parse by section, not by the shape of a row.
> - **Columns**: `Nr. crt.`, `Denumirea unității`, `Adresa`, `Sector`,
>   `Categorie unitate`, the registration number and date, and sometimes a
>   seventh cell ("Preschimbat <date>", renewed; or the cancelling decision).
>   - **The header sits on row 16 or 17**, below the authority's letterhead.
>   - **`Categorie unitate` is free text** with case and spelling variants
>     ("Fast food", "fast-food", "Fast-Food"). Some carry "(Unitate vânzare
>     prin internet)", meaning the unit also sells online. It is still a
>     registered premises.
>   - File 19's categories (Fast food, Bistro, Snack bar, Bar, Restaurant, …)
>     give a finer food-service split than any other one-bucket city.
> - **Names are legal entities**, not always the name on the sign ("Metro
>   Cash & Carry SRL", "Carrefour Romania SA"). **Sole traders appear under
>   their own names** ("… ÎNTREPRINDERE INDIVIDUALĂ", and PFA / II forms).
>   The project's rule applies: show the category, never a person's name.
>   `check_personal_exposure.py` should look for those suffixes first.
> - **The ninth animal-origin file** (26 Hipermarket-supermarket, 85,020 B,
>   sha256 `4bc41e29f86b8d67`): **499 active**, 201 cancelled. The
>   animal-origin set is therefore **19,516 active** before de-duplication.
>   One store can sit in several files (a hypermarket's butcher, fishmonger
>   and food counter), so **step 2 de-duplicates on name + address.**
> - **The non-animal-origin list** (45 files, mostly factories; the owner
>   fetched eight 2026-09-28 into `data/bucharest/raw/non-animal/`, same
>   layout, same ANULATE sections):
>
>   | File | Active | Cancelled | What the rows are | Call |
>   |---|---|---|---|---|
>   | 36 Baruri | **778** | 81 | Bar 557, Cafenea (café) 197, Ceainărie (tea house) 17 | ✅ food service |
>   | 33 Comerț cu amănuntul, supermarkets only | **1,083** | 149 | "Comerț cu amănuntul" (retail), a mixed bag: grocers, and shops selling some packaged food | ✅ food shops, with a sole-trader check (PFA names appear) |
>   | 42 Frozen and chilled non-animal food | **934** | 183 | Lidl and the like: bake-off counters in shops | ✅ food shops; most will be duplicates |
>   | 03 Bread and pastry making | **496** | 1,040 | Covrigării (pretzel shops), bakeries, pastry shops | ✅ food shops |
>   | 01 Bread making | **164** | 236 | In-store bakeries (Carrefour, Selgros) and market bakeries | ✅ food shops; many duplicates |
>   | 02 Pastry making | **76** | 650 | Pastry and doughnut shops | ✅ food shops |
>   | 24 Ice-cream making | **66** | 30 | Gelaterias, plus 3 kiosks and 2 vending machines | ✅ the 61 shops; kiosks and machines out |
>   | 34 Supermarket-hypermarket | 0 | 0 | Header only | - |
>
>   Sha256 prefixes: 01 `cc9c3ed541159ab9`, 02 `081dc27f739f0142`,
>   03 `5d25e9357ab110de`, 24 `206cfc828d10efc5`, 33 `30867121c2100d5c`,
>   34 `b1628ffd3c5870e0`, 36 `eab91027f4b99e2c`, 42 `da5c7e2a03d0cf9d`.
>   Together: **about 3,590 more active rows**, so **about 23,100 before
>   de-duplication.** "Sector" reads **U.M.** (unitate mobilă) on mobile
>   units, such as a wine truck with a number plate for an address. They are
>   out, as non-storefronts.
> - 🎯 **THE HIT RATE, measured 2026-09-28: about 80% placed on street and
>   house number.** The inputs:
>   - OSM: **145,892 address objects** inside relation 377733, pulled as a
>     CSV (owner-approved, 9,523,237 B, sha256 `49f1b99f5242b28d…`,
>     `data/bucharest/raw/osm_addresses_2026-09-28.csv`, via
>     overpass.kumi.systems). That gives 4,443 street keys and 132,287
>     street+number pairs.
>   - DSVSA: 23,032 active rows (mobile units, kiosks and vending machines
>     out), which merge on name and parsed address to **20,815
>     storefronts**.
>
>   | Pass | Placed | Share |
>   |---|---|---|
>   | 1: normalised street + number (types, diacritics, "nr." stripped) | 15,448 | 74.2% |
>   | 2: a tolerant key (words over 2 letters, ranks dropped, genitive stemmed); **a unique OSM street only** | +1,103 → **16,551** | **79.5%** |
>
>   - **Left unplaced: 4,264.** 1,051 are **ambiguous** (two or more OSM
>     streets fit) and are not guessed. The others either match a street
>     whose house number OSM lacks, or match no street. The split was not
>     measured.
>     - Long boulevards lead the missing numbers: Iuliu Maniu,
>       Alexandriei, Floreasca, Oltenitei.
>     - The no-match rows are market addresses such as Câmpul Moșilor, and
>       abbreviations still unresolved ("Dorobanți" against "Dorobanților",
>       "I.C. Brătianu").
>   - **By sector:** 1 76% · 2 83% · 3 79% · 4 78% · 5 75% · 6 86%.
>   - **By file:** 76-88%, except fishmongers at 57% (many sit inside
>     markets).
>   - **Where that leaves Bucharest:** below Prague's 99.8%, Oslo's 97.8% and
>     London's 94.9%, above Incheon's 71.3% (Band B, gap disclosed). A build
>     can raise it with more normalisation (the `address-join` skill's
>     patterns, an `i` stem, initials). **Street-level placement for the
>     street-only rows is not proposed**: a boulevard is kilometres long.
>   - **The measurement scripts** are session scratch
>     (`buc_match.py`, `buc_match2.py`). The build writes its own join in
>     step 2, and this table is its baseline.
> - **What the build still needs, in order:**
>   1. ~~The owner's browser fetch~~ done for eight files. Still to come:
>      26 Hipermarket-supermarket, and a look at the non-animal-origin list.
>   2. ~~Five rows of each, read for the names~~ done: legal entities, with
>      sole traders under their own names (above).
>   3. ~~The OSM address hit rate~~ measured: **79.5%** (above). **The owner
>      decides whether that is enough to build, with the gap disclosed.**
>   4. Owner calls for the build: canteens and pastry labs out (recommended);
>      the page's wording for the ~20% unplaced; whether to show legal-entity
>      names or the category only.

---

## The one-line summary

**The strongest rail in its band and the weakest access.** A real five-line
metro against three cities' trams — and a business register that can only be
fetched through a browser that has legitimately passed a JS challenge, from a
country whose national portal has been unreachable for days.

⚠️ **This is a ONE-BUCKET city.** It sits in the one-bucket band, not because
its coordinate route is unmeasured — that is done — but because **Romania's
national catalogue holds no second bucket.**

---

## Business leg — DSVSA, food only

| | |
|---|---|
| Source | **DSVSA Bucharest** — the sanitary-veterinary authority, `bucuresti.dsvsa.ro` |
| Rows | **31,299** |
| Bucket | **Food service ONLY** — DSVSA registers food-handling establishments |
| Format | **XLSX**, 56,009 bytes when fetched |

### ⚠️ Why there is no second bucket, and it is established rather than assumed

**Romania's entire national catalogue was enumerated** — 4,693 datasets read
from the Internet Archive, because `data.gov.ro` itself is unroutable. **The
only commercial register in it is ~40 dated snapshots of
`firme-inregistrate-la-registrul-comertului`** — ONRC's **company** register,
which is the registered-office shape this project exists not to map.

**So retail and personal services do not exist as Romanian open data**, and
that is a measured absence, not an unexplored one.

---

## 🚨 The fetch is browser-assisted by necessity

`ansvsa.ro` and `bucuresti.dsvsa.ro` sit behind a **"Verifying your browser"
JS challenge** — verified again 2026-09-23, both returning **HTTP 503** with a
challenge interstitial.

**The challenge covers the DATA FILES, not just the pages.** Plain `curl`
against the XLSX itself returns **503 with an 8,904-byte HTML body**. The
same URL **inside the browser that had legitimately passed the challenge**
returns **200, 56,009 bytes, magic `PK\x03\x04`** and the correct
`spreadsheetml.sheet` content type — a real file.

⚠️ **That is the route, and the distinction is the whole point: the file is
read INSIDE a browser that passed the challenge. A clearance cookie is NEVER
replayed to `curl`**, because that is working around bot detection rather than
passing it.

**Recorded as a build constraint on `fetch_sources.py`, not as a blocker.**

---

## ⚠️ The national portal has been down for days, and the framing softened

`data.gov.ro` resolves to **85.120.75.35** and **blackholes on both 443 and
80** — `time_connect` 0.000000s, no RST, no refusal.

It was recorded on 2026-09-22 as *"an outage, not a refusal"* because it had
answered earlier the same day. **Re-tested 2026-09-23: still black.** Two days
running weakens that reading. **It is not upgraded to a refusal — the evidence
does not support that either** — but the row now says how long, rather than
repeating a same-day judgment.

✅ **It is not on the critical path.** Its catalogue was read from the
Internet Archive, and DSVSA is a different host.

---

## Coordinates — OSM, measured

| | |
|---|---|
| Route | **OSM address objects** in relation **377733** |
| Supply | **146,228** — 132,478 nodes + 13,750 ways carrying **both** `addr:street` and `addr:housenumber` |
| Licence | **ODbL** — and Bucharest's rail is already OSM, so no new licence is added |

⚠️ **ANCPI, which owns the national address nomenclature, has no resolving
geospatial subdomain** — `ran.`, `geoportal.`, `ags.` and `inspire.` are all
NXDOMAIN. So the authoritative route does not exist for us and OSM is the
route, not a fallback.

🎁 **One useful find if a join is ever preferred to a match:** Romania
publishes a **complete national street nomenclature** as open data, including
`nomenclator-stradal-municipiul-bucuresti`. It was invisible until the
national catalogue was enumerated from the Archive.

### 🚨 The hit rate is NOT measured

**146,228 is the SUPPLY, not the match rate.** What share of DSVSA's 31,299
addresses actually resolve against it has never been tested, and it cannot be
tested without first fetching the register through the browser.

**This is the single largest unknown in this brief**, and it is the number
that decides whether Bucharest is buildable. Every other city in this band has
its rate: Prague 99.8%, Copenhagen 100%, Oslo 97.8%, Hong Kong 100%.

---

## ✅ Rail — the best in its band, RE-COUNTED 2026-09-23

Inside relation 377733:

| | |
|---|---|
| Subway route relations | **13** |
| Named | **13** |
| Coloured | **12** |
| Refs | **M1 · M2 · M3 · M4 · M5** |
| **Station nodes** | **64** |

**A real five-line metro** — against Stockholm's, Zurich's and Göteborg's
trams. This list previously carried *"~63 stations claimed, unverified"*; the
measured figure is **64**.

### ⚠️ The thirteenth relation is a trap

**`Extensie M4` carries NO `ref` and NO `colour`.**

- A build keying on **`ref`** drops it **silently**.
- A build keying on **relation count** draws a line it **cannot label** — and
  the project's invariant requires every drawn line to carry its real public
  name *and* a legend entry.

🚨 **This is now the third city in one day with an unref'd or uncoloured route
relation** — Singapore's `JRL` (5 relations, no colour) and Stockholm's
unref'd subway and tram are the others. **Treat it as the default expectation,
not as Bucharest's quirk.**

---

## Licence — SILENT, and the absence is established

**Read in the browser 2026-09-23** — the only way to reach the host.

- **`bucuresti.dsvsa.ro` has no terms-of-use page at all.** The entire site
  offers exactly two policy links: cookies and privacy.
- **The privacy policy is 8,465 characters about personal data with ZERO
  mentions** of reuse, reproduction, distribution, licence, commercial use,
  copyright or intellectual property.
- **DSVSA data is not on `data.gov.ro`** — the archived 4,693-dataset list was
  searched for `dsvsa`, `ansvsa`, `veterinar` and `sanitar-veterinar`: **zero
  matches**. So there is no national statement to inherit either.

⚠️ **The footer reads *"Ⓒ 2017 ANSVSA. Toate drepturile rezervate"* — all
rights reserved.** That is a **website** footer, which is the New York
situation `read-licence` records: it governs site content, not the data.

**Verdict: SILENT, with the pages named** — an established absence rather than
an unexamined gap.

---

## Region

`"region": "Europe"`.

---

## Still unknown

- 🚨 **The OSM hit rate against DSVSA's 31,299 addresses.** The single number
  that decides whether this city is buildable.
- ⚠️ **The register's actual columns.** 31,299 rows and a confirmed XLSX, but
  the schema has not been read — it needs the browser fetch first. **A row
  count is not a schema**, and this project has been caught by that before.
- ⚠️ **Whether a name column exists at all**, and whether it is a trade name
  or a licence holder — the Oslo and Singapore question, unasked here.
- **Scope** — Bucharest's sectors vs the municipality.

## ⚠️ Two facts that CANNOT be brief-checks, and why

**Three checks were attempted here and two were removed.** Both tried to
encode *"expect a non-200"*, and the checks framework has no such concept —
every kind asserts success. Recorded rather than quietly dropped, because the
temptation to re-add them is obvious:

**1. `bucuresti.dsvsa.ro` serves the challenge at HTTP 503.** An
`http_contains` on it fails, because `http_contains` requires a 200 — the
challenge body is real and the status is not. **The host being *challenged*
rather than *dead* is a genuine finding and simply cannot be expressed as a
passing check.**

**2. `data.gov.ro` must NOT be checked at all.** A check on it was written
with the claim *"this is expected to fail and its failure is the finding"* —
**which is not a check, it is a note that breaks the suite.** Every future
`brief_check bucharest` would show a failure, and **a suite that always shows
a failure teaches people to ignore failures.** It also burns a 300-second
connect timeout on every run. *This is the third time in one day I tried to
push a non-200 expectation into this framework — first as `http_status_in`,
then `http_status_expected`, now as a deliberately-failing `http_ok`.*

**3. Overpass cannot be a check either, and this one was tried and withdrawn.**
An `http_ok` against `overpass-api.de` for relation 377733 **passed, then
returned 504 ninety seconds later** — the public instance load-sheds. **A
check that fails intermittently is worse than no check**, for the same reason
as above. This project already has the precedent recorded: *"Bucharest's rail
count was attempted and failed on the mirrors, not on Bucharest."*

⚠️ **So Bucharest carries ONE brief-check, and that is itself the finding.**
Every other city here has three to thirteen. Bucharest's sources are a
challenged host, an unroutable portal and a rate-limited public API —
**there is almost nothing about it that can be verified automatically**, which
is a fair summary of what makes it hard.

```brief-checks
[
  {
    "id": "romania-catalogue-readable-via-archive",
    "claim": "THE ROUTE THAT ACTUALLY WORKS for Romania's national catalogue: data.gov.ro is unroutable for us, and its package_list is readable from the Internet Archive instead - which is how 4,693 datasets were enumerated and how the absence of a second bucket was established. If the Archive copy goes, that finding loses its source",
    "kind": "http_ok",
    "url": "https://archive.org/wayback/available?url=data.gov.ro%2Fapi%2F3%2Faction%2Fpackage_list",
    "min_bytes": 50
  },
  {
    "id": "bucharest-osm-metro-refs",
    "claim": "OSM carries Bucharest's metro as M1-M5, every relation referenced (added 2026-09-28: osm_route_refs now confirms a mismatch on a second mirror, which answers the 2026-09-23 objection to Overpass checks; Extensie M4 no longer appears)",
    "kind": "osm_route_refs",
    "bbox": [44.33, 25.95, 44.55, 26.25],
    "routes": ["subway"],
    "expect_refs": {"subway": 5},
    "require_refs": {"subway": ["M1", "M2", "M3", "M4", "M5"]}
  }
]
```
