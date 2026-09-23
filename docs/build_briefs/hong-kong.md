# Hong Kong — build brief

**Step 0 measured 2026-09-22. The indemnity is ACCEPTED, so nothing gates this
city.** Run `python scripts/brief_check.py hong-kong` before writing code.

---

## The one-line summary

**The cleanest register in the whole screen — and 40% of it is not
storefronts.** 35,808 rows at 100% fill on every column, with its own code
lookups and its own generation date inside the file. But **Food Factory is
11,566 rows and Swimming Pool is 1,440**, and neither is a shopfront, so the
buildable figure is roughly **21,545**, not 35,808.

---

## ✅ SETTLED — the owner's call

**The indemnity is accepted** (2026-09-22). Three conditions bind this build
and are restated under *Licence* below. `docs/data_sources.md` carries the
reasoning.

---

## Business leg — FEHD, three XML registers, MEASURED

All three at `https://www.fehd.gov.hk/english/licensing/license/text/`:

| Register | File | Rows | Types |
|---|---|---|---|
| Restaurants | `LP_Restaurants_EN.XML` | **17,260** | 3 |
| Other food | `LP_OtherFood_EN.XML` | **16,518** | 8 |
| Non-food | `LP_NonFood_EN.XML` | **2,030** | 9 |
| | | **35,808** | **20** |

**Every column is 100% populated** on all three — `SS` (shopsign), `ADR`
(address), `TYPE`, `DIST`, `EXPDATE`. That is unique in this project.

### Two properties this file has that most sources do not

- **It SELF-ATTESTS.** `<GENERATION_DATE>` sits in the file —
  **2026-09-23** when read — so staleness is checkable from the artifact.
  **Paris's IDFM feed cannot do this**, and the contrast is worth carrying:
  there, the date lives in a third party's metadata.
- **It is SELF-DOCUMENTING.** `<TYPE_CODE>`, `<DIST_CODE>` and `<INFO_CODE>`
  are code→label lookups **inside the same download**, so the taxonomy needs no
  external code list.

### Structure

```
<DATA>
  <DEPARTMENT> <GENERATION_DATE> <LINK>
  <TYPE_CODE>  <CODE ID="RL">General Restaurant Licence</CODE> …
  <DIST_CODE>  <CODE ID="11">Eastern</CODE> …
  <INFO_CODE>  …
  <LPS>  <LP> TYPE DIST LICNO SS ADR INFO EXPDATE </LP> … </LPS>
```

### ⚠️ How the register was found, and the lesson that was recorded WRONG

`organization_show?id=hk-fehd` returns **`package_count: 1`**, and this
project's notes drew a generalisable lesson from that — *"searching by PROVIDER
rather than by keyword is the generalisable move here, because a keyword search
cannot distinguish absent from named-differently."*

**That is wrong as stated.** `package_list` holds **19 `hk-fehd-*` datasets**,
including all three registers. The org endpoint's count is simply unreliable
on this portal, so the provider route failed for the same reason the keyword
route did.

**Enumerate the catalogue and match locally.** That is the move that worked
here, as it did for Stockholm, Zurich, Milan and Bulgaria.

---

## ⚠️ COMPOSITION — the finding that changes the city

`add-country` requires the composition measurement, not just presence. Taken
against the file's own labels:

**Other food — 16,518 rows, but only 3,853 are shops**

| Code | Rows | Label | Storefront? |
|---|---|---|---|
| `FF` | **11,566** | Food Factory Licence | ❌ manufacturing |
| `FP` | 3,086 | Fresh Provision Shop | ✅ |
| `FG` | 559 | Frozen Confection Factory | ❌ |
| `FE` | 443 | Factory Canteen | ❌ not public-facing |
| `FB` | 410 | Bakery | ✅ |
| `FS` | 357 | Siu Mei and Lo Mei Shop | ✅ |
| `FC` | 88 | Cold Store | ❌ |
| `FM` | 9 | Milk Factory | ❌ |

**Non-food — 2,030 rows, but only 432 are storefronts**

`TP` Swimming Pool **1,440** ❌ · `PE` Public Entertainment 262 ✅ · `TU`
Undertaker's 145 ❌ · `PC` Cinema/Theatre 73 ✅ · `KE` Karaoke 62 ✅ · `TC`
Commercial Bathhouse 35 ✅ · `TF` Funeral Parlour 7 ❌ · `TO` Offensive Trade
4 ❌ · `TS` Slaughterhouse 2 ❌

**Restaurants — all 17,260 count.** `RL` General 12,603 · `RR` Light
Refreshment 4,652 · `MR` Marine 5.

### So the buckets are

| Bucket | Rows |
|---|---|
| Food service | **17,260** |
| Food retail | **3,853** |
| Personal services / entertainment | **432** |
| **Buildable total** | **≈21,545** |
| *(filtered out)* | *14,263 factories, pools, cold stores, funeral trades* |

⚠️ **The master list's description of this register was wrong in two ways.** It
named *"Composite Food Shop"*, **which is not a licence type in the file at
all**, and it omitted **Food Factory, which is 70% of the register it was
describing**. Both corrected here.

⚠️ **There is no general retail.** Hong Kong licenses food and specified
trades; clothing, electronics and general shops have no register. Same gap as
most US cities — this is a `multi-source-city` candidate only if a second
source is ever found.

---

## Taxonomy — 20 types, and a catch-all share of ZERO

`premises-taxonomy`'s deciding measurement, run against the file's own
`TYPE_CODE` labels:

**Catch-all share: 0.0%.** Every one of the 20 types names a specific trade —
General Restaurant, Fresh Provision Shop, Bakery, Siu Mei and Lo Mei, Swimming
Pool, Karaoke, Commercial Bathhouse, Undertaker's. **There is no *Other*, no
*n.c.a.*, no residual bucket.**

**That is unique in this project.** Paris's NAF is 19.3% at its finest level,
Barcelona's 2.6%, Madrid keys near the top of its scheme, Milan's second
classification is binary. Hong Kong needs **no level choice at all**: the
scheme is flat, complete, and ships with its labels.

*(`TO` Offensive Trade Licence reads like a catch-all but is a defined
statutory category, and it holds 4 rows.)*

---

## Coordinates — ALS, keyless, MEASURED

**`https://www.als.gov.hk/lookup?q=<address>`** with
`Accept: application/json`. Free, no key, no account.

Measured on **120 real `ADR` strings** taken from the XML:

| | |
|---|---|
| **Hit rate** | **90.8%** (109/120) |
| Miss | 9.2% |
| Throttled / error | **0%** at 4 workers |
| Throughput | **3.9 req/s** |

Returns **lat/long AND HK1980 Grid easting/northing AND a confidence
`Score`**.

### ⚠️ Use the Score — 21% of hits are low-confidence

| Score | Share of hits |
|---|---|
| ≥ 90 | 37.6% |
| 75–90 | 41.3% |
| **50–75** | **21.1%** |

Median 87, min 50. **A geocoder that reports its own confidence is only worth
having if the confidence is actually read** — the same point as DAWA's
`kategori` and INSEE's `qualite_xy`. Set a threshold and decide what happens
below it; do not average over it.

### ⚠️ Addresses do NOT collapse — 1,799 distinct of 1,800

Unlike Singapore, where 35,064 postcodes became 7,767 buildings, Hong Kong's
addresses are almost all unique. **Budget the full ~35,000 lookups**, about
**2.5 hours** at the measured rate. Deduplicate anyway, but expect little.

---

## Rail leg — the best in the screen

**126 OSM relations, 125 named, 117 coloured.** No other city screened comes
close. Use `osm-rail`.

---

## Licence — PERMITTED WITH CONDITIONS, indemnity ACCEPTED

`data.gov.hk` Terms of Use v1.2. Download, distribution and reproduction are
permitted for **commercial and non-commercial purposes, free of charge**.

### MUST DISPLAY — all three elements of the same paragraph

1. **Identify the source** of the Data
2. **Acknowledge the Government's and the Relevant Organisations' ownership of
   the intellectual property** in it
3. **Proper attribution to the Government, the Relevant Organisations and
   DATA.GOV.HK**

These become numbered notices in `docs/data_sources.md` when the city is
committed, not before.

### MUST DO

- **`python scripts/check_personal_exposure.py hong-kong`**, excluding
  catch-all categories — the Los Angeles NAICS 812990 precedent. This is
  **condition 2 of the indemnity acceptance**, and it is a risk control rather
  than a formality: the realistic complainant is an individual whose name sits
  at what looks like a home.

### ⚠️ THE INDEMNITY — accepted, and what it actually says

> you shall **indemnify** the Government and the Relevant Organisations against
> any allegations or claims of infringement of the rights of any person and all
> costs, losses, damages and liabilities incurred … which in any case arise
> **directly or indirectly** in relation to your use, reproduction and/or
> distribution of the Data

**No cap. No notice-and-defend right.** The *Limitation of Liability* section
caps the **Government's** liability to the user, not the reverse, and it
separately disclaims any warranty of **non-infringement** — so the publisher
does not promise the Data is clean and the user indemnifies them if it is not.

**Accepted by the owner 2026-09-22** on the basis that the scope is
*rights-infringement only*, the data is a government public register
republished with required attribution, and the project's standing commitment to
honour removal requests without argument cuts off the likeliest escalation.
Full reasoning in `docs/data_sources.md`.

---

## Region

`"region": "Europe"` does **not** apply. Hong Kong needs a new region; the
macro map currently has United States (+halves), Canada West/East, Mexico and
Europe. **Adding one is an owner/app-role decision** — see
`docs/scaling_thresholds.md`, which sets the rule that a region is whatever
groups cities into one readable view.

---

## Still unknown — the honest list

- **Which region Hong Kong joins**, and whether it is alone in it.
- **What to do with ALS hits scoring 50–75** — 21% of them.
- ~~Whether `EXPDATE` should filter~~ — ✅ **MEASURED: it does not.** **0 of
  35,808 rows** carry an expiry before today. The file is a **live register**,
  not an archive, so the ~21,545 buildable figure stands without a currency
  filter. ⚠️ Re-check on a later pull: this makes the whole file a snapshot
  whose freshness rests entirely on `GENERATION_DATE`.
- ~~The `INFO` field and its 6-code lookup~~ — ✅ **READ, and it is
  MULTI-VALUED WITH NO DELIMITER.** Values concatenate: `#G#H`, `#F#G#H`,
  `#E#F#G#H`. **A naive `value_counts()` returns COMBINATIONS, not codes** —
  the Calgary / Edmonton / Surrey trap in a new costume, and worse here
  because there is no separator to split on except the `#` itself.
  The codes are **endorsements**, not categories: `#G` sashimi, `#H` sushi,
  `#F` raw oyster, `#E` raw meat, `#R`/`#S` shellfish, `#I`/`#Q` live and
  fresh poultry, `#J` lunch-box supply, `#C` karaoke exemption, and `#K`–`#P`
  the offensive-trade endorsements (lard boiling, shark-fin and fish-meal
  processing, leather dressing and tanning).
  **Most common: `#G#H` on 1,421 rows** — sashimi and sushi together.
- **Whether a general-retail source exists anywhere.** Without one Hong Kong
  is food-service-heavy by construction: 17,260 of 21,545 buildable rows.
- **District coverage** — 20 districts appear, but no check that the rail
  network's districts are all represented.

```brief-checks
[
  {
    "id": "fehd-restaurants-xml",
    "claim": "FEHD's restaurant register downloads with no key. 17,260 rows when measured, all three registers regenerated daily",
    "kind": "http_ok",
    "url": "https://www.fehd.gov.hk/english/licensing/license/text/LP_Restaurants_EN.XML",
    "min_bytes": 3000000
  },
  {
    "id": "fehd-otherfood-xml",
    "claim": "The other-food register downloads with no key. 16,518 rows - but only 3,853 are shops: Food Factory alone is 11,566 and is NOT a storefront",
    "kind": "http_ok",
    "url": "https://www.fehd.gov.hk/english/licensing/license/text/LP_OtherFood_EN.XML",
    "min_bytes": 3000000
  },
  {
    "id": "fehd-nonfood-xml",
    "claim": "The non-food register downloads with no key. 2,030 rows, of which Swimming Pool is 1,440 and is not a storefront either",
    "kind": "http_ok",
    "url": "https://www.fehd.gov.hk/english/licensing/license/text/LP_NonFood_EN.XML",
    "min_bytes": 300000
  },
  {
    "id": "fehd-xml-carries-its-own-generation-date",
    "claim": "The file SELF-ATTESTS - GENERATION_DATE is inside it, so staleness is checkable from the artifact rather than from a third party's metadata. This is what Paris's IDFM feed cannot do",
    "kind": "http_contains",
    "url": "https://www.fehd.gov.hk/english/licensing/license/text/LP_NonFood_EN.XML",
    "contains": "GENERATION_DATE"
  },
  {
    "id": "fehd-xml-is-self-documenting",
    "claim": "The taxonomy ships inside the download - TYPE_CODE maps every licence code to its label, so no external code list is needed. Catch-all share is ZERO, which no other city in this project can say",
    "kind": "http_contains",
    "url": "https://www.fehd.gov.hk/english/licensing/license/text/LP_NonFood_EN.XML",
    "contains": "TYPE_CODE"
  },
  {
    "id": "als-geocoder-keyless",
    "claim": "Hong Kong's Address Lookup Service answers without a key and returns lat/long, HK1980 Grid, and a confidence Score. Measured 90.8% on 120 real ADR strings at 3.9 req/s with zero throttling",
    "kind": "http_ok",
    "url": "https://www.als.gov.hk/lookup?q=1%20Harbour%20Road%2C%20Wan%20Chai",
    "min_bytes": 200
  },
  {
    "id": "datagovhk-org-count-is-unreliable",
    "claim": "organization_show for hk-fehd reports package_count 1 while package_list holds 19 hk-fehd-* datasets. This check pins the CATALOGUE, which is the route that works - the provider route was recorded as the generalisable move and it is not",
    "kind": "http_ok",
    "url": "https://data.gov.hk/en-data/api/3/action/package_list",
    "min_bytes": 50000
  }
]
```
