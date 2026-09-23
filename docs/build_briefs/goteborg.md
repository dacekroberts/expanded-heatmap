# Göteborg — build brief

**Step 0 measured 2026-09-23**, after the blocker that had kept this city
unmeasured turned out to be a wrong walk rather than a missing node. Run
`python scripts/brief_check.py goteborg` before writing any code.

⚠️ **One-bucket city — but see the bucket question below, which is live.**
It shares a single owner decision with **Zurich** and **Stockholm**.

---

## The one-line summary

**No geocoding leg, CC0, the cleanest taxonomy in the project — and a second
distribution of the same dataset that is quietly wrong in three ways.**

---

## Business leg — `Livsmedelsverksamheter`, MEASURED

| | |
|---|---|
| **Rows** | **5,063** |
| Source | **CSV distribution**, `catalog.goteborg.se/store/6/resource/57478` |
| Encoding / delimiter | **utf-8-sig**, **`;`** — verified, not assumed |
| Licence | ✅ **CC0 1.0** |
| Refresh | `accrualPeriodicity: DAILY` |

### 🚨 TAKE THE CSV. The rowstore JSON is wrong in three ways.

The dataset publishes **three** distributions — CSV, an EntryStore rowstore
JSON, and a WMS. **The JSON is lossy and mis-shaped:**

| | CSV | rowstore JSON |
|---|---|---|
| Rows | **5,063** | **4,786** |
| `namn` | clean | **`﻿namn`** — BOM-mangled, so a consumer keying on `namn` reads nothing |
| `y_sweref991200` | 6,397,893 *(northing)* ✅ | 149,193 *(easting)* ❌ |
| `x_sweref991200` | 149,193 *(easting)* ✅ | 6,397,896 *(northing)* ❌ |

🚨 **The 277-row gap is explained, and the explanation is the worst part:**
**5,063 − the 279 rows whose `typ` is blank = 4,784**, against the rowstore's
4,786. **The JSON silently drops rows with no classification.** A build taking
it would lose 5.5% of the register and never see an error.

⚠️ **The axis swap is Prague's EPSG:5513 flip in a new costume** — except here
both copies come from one publisher and only one is right.

### ⚠️ Finding the CSV at all was the original blocker

The recorded obstacle was *"its DCAT distribution node exposes no
`accessURL` — `resource/18` returns RDF rather than data."* **The node was
real and the walk was wrong.** Two things to know:

1. **The dataset is in CONTEXT 6**, not 1. `store/1` returns *"The requested
   context ID does not exist"*, which reads like a dead catalogue.
2. **EntryStore's search response is `{offset, resource, limit, results,
   facetFields}` where `results` is an INTEGER COUNT and `resource` is a dict
   with one key, `children`.** A reader treating `results` as the array gets
   nothing from a 21 KB response full of data. **Zero results from a populated
   response is a statement about the parser.**

✅ **In DCAT, walk `dataset → dcat:distribution → accessURL`.** The property
you want is on the **child**.

---

## ✅ Coordinates — there is NO geocoding leg

| | |
|---|---|
| `lat` / `lon` | **100.0% populated** |
| Outside Göteborg's bounding box | **0** (lat 57.5631–57.8583, lon 11.7044–12.2050) |

**That is Paris's shape**, and it was unknown while the row count was.
`y_sweref991200`/`x_sweref991200` (SWEREF99 12 00) are also present, but
**`lat`/`lon` sidestep the axis question entirely — use them.**

---

## Taxonomy — `typ`, 47 values, and the catch-all is 0.9%

| | |
|---|---|
| Distinct values | **47** |
| Populated | **94.5%** — ⚠️ **5.5% blank** |
| **Catch-all share** | ✅ **0.9%** — the cleanest in this project |

| Value | Rows | Share |
|---|---|---|
| RESTAURANG | 1,591 | 31.4% |
| LIVSMEDELSBUTIK | 685 | 13.5% |
| KAFÉ | 485 | 9.6% |
| *(blank)* | 279 | 5.5% |
| FÖRSKOLA — tillagning | 265 | 5.2% |
| FÖRSKOLA — mottagning | 232 | 4.6% |
| GROSSIST | 133 | 2.6% |

---

## 🚨 The bucket question — Göteborg may NOT be one bucket

`typ` does not describe one bucket:

| Bucket | Types | Rows |
|---|---|---|
| **Food service** | RESTAURANG 1,591 · KAFÉ 485 | **~2,076** |
| **Food retail** | LIVSMEDELSBUTIK 685 · BAGERI 65 · APOTEK 61 | **~811** |

**Hong Kong's build already counts food service and food retail as two
separate buckets** (17,260 / 3,853 / 432). **Applying the same reading moves
Göteborg out of the one-bucket band** — and the owner's bar is that two is
acceptable and one is not.

⚠️ **Raised, not decided.** It changes a band, and it turns on exactly the
distinction Hong Kong's split already embodies.

### ⛔ And a quarter of the register is not a storefront

FÖRSKOLA 497 · SKOLA 216 · GRUPP/SERVICEBOENDE 150 · GROSSIST 133 ·
AMBULERANDE 114 · HUVUDKONTOR 72 · LAGER 64 · MATMÄKLARE 54 · TRANSPORTÖR 42
— **~1,342 rows, 26.5%.**

**With the blanks dropped too, buildable is roughly 3,442.**

---

## ⚠️ Rail — UNVERIFIED, and do not inherit it

This project's records say *"Trams, no metro."* 🚨 **That is INHERITED, not
measured**, and it comes from the same screen that gave **Copenhagen a tram it
does not have** and **Stockholm 21 trams against a measured 6**.

**Count it before writing pipeline code.** And note that **tram-only is not a
blocker** — `route_type 0` is drawn in seven built cities, and every tram
exclusion is a city that *also* has a metro. See `zurich.md`, which carries
the full reasoning.

⚠️ **The Muni Metro spacing test is also unrun** — an attempt on 2026-09-23
failed its own control.

---

## Region

`"region": "Europe"`.

## Still unknown

- 🚨 **Rail — uncounted.** See above.
- 🚨 **The bucket question** — one or two.
- ⚠️ **Stop spacing** — needs a method whose control passes.
- ⚠️ **What the 279 blank-`typ` rows are.** They are dropped by the JSON and
  kept by the CSV; nobody has looked at them.

```brief-checks
[
  {
    "id": "goteborg-csv-distribution-live",
    "claim": "The CSV distribution is the route that works - 5,063 rows, utf-8-sig, semicolon-delimited. TAKE THIS, never the rowstore JSON, which silently drops the 279 rows whose typ is blank, swaps x/y against this file, and returns namn BOM-mangled",
    "kind": "http_ok",
    "url": "https://catalog.goteborg.se/store/6/resource/57478",
    "min_bytes": 500000
  },
  {
    "id": "goteborg-licence-cc0-on-the-distribution",
    "claim": "The licence is CC0 and it is on the DISTRIBUTION node, not the dataset. Foodbusinesses (store/6/resource/35) carries fourteen properties and no license, rights or accessRights of any kind - a reader checking the dataset node would record Goteborg as SILENT and be wrong in the permissive direction",
    "kind": "http_contains",
    "url": "https://catalog.goteborg.se/store/6/metadata/57479",
    "contains": "publicdomain/zero"
  }
]
```
