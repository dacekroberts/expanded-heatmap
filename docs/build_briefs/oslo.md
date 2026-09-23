# Oslo — build brief

**Step 0 measured 2026-09-22/23.** Run `python scripts/brief_check.py oslo`
before writing code.

---

## The one-line summary

**A clean NACE register with a keyless two-stage geocoder — and a headline
number that was measuring the wrong address.** The recorded "152,060 sub-units"
is the API's answer to a filter that does **not** constrain the address the
build reads. The real figures: **138,896 sub-units physically in Oslo**, of
which **13,458** are in the three buckets.

---

## ⚠️ THE CORRECTION — the API cannot answer the scoping question

Brønnøysund's `?kommunenummer=0301` does **not** guarantee
`beliggenhetsadresse` is in Oslo. A first sample scored **57.3%** on the
geocoder and the misses were **Bergen, Copenhagen, Paris and Malmö** — plus
`c/o` lines, because `adresse` is a **list** whose first element is not always
a street.

**This is the registered-office trap in a third costume**, after ONRC, ACRA and
SIRENE's *sièges*. The rule worth carrying:

> **A filter parameter and the field you read are two different addresses until
> proven otherwise.**

Two API samples then disagreed — 24.5% and 4.3% not-in-Oslo — because
**brreg's API stops paging past ~10,000 and returns sub-units sorted by name**,
so both came from the alphabetical head. **The API cannot settle this.**

**Settled from the bulk file instead**, 2026-09-23:

| | |
|---|---|
| Endpoint | `https://data.brreg.no/enhetsregisteret/api/underenheter/lastned` |
| Size | **88.9 MB gzipped**, no key |
| Sub-units streamed | **864,903** |
| **`beliggenhetsadresse.kommunenummer == "0301"`** | **138,896** |
| **…of those in NACE 47/56/96** | **13,458 (9.7%)** |

**13,458 is the buildable figure.** For scale: Barcelona 58,908 at 1.6 M
residents, Madrid 53,355 at 3.2 M, Oslo 13,458 at ~700 k — about 19 per
thousand, between the two. Plausible, not a coverage failure.

---

## Business leg

`beliggenhetsadresse` is **the physical location address, kept deliberately
distinct from the registered one** — that distinction is Norway's answer to
this project's core question, and it is the reason Norway passed the screen.

⚠️ **Read `adresse` as a LIST.** Skip lines beginning `c/o`, `postboks`, `pb`.

---

## Taxonomy — NACE at UNIFORM depth, unlike Prague

| Code depth | Share |
|---|---|
| **5 chars** | **100.0%** |

**Every row reaches the national sub-class.** No raggedness — so a level *can*
be chosen here, which is exactly what Prague cannot do (57.9% at 5 chars,
31.4% stopping at 3).

Top codes: `56110` restaurants **18.4%** · `96210` laundry 8.5% · `47710`
clothing 7.9% · `96220` hairdressing 6.4% · `47110` groceries 6.2% · `96990`
other personal services **6.0%**.

### ✅ Catch-all share — measured 2026-09-23, and Oslo keys at the FINEST level

Against **SSB's own SN2007 labels** (`data.ssb.no/api/klass/v1/classifications/6`,
1,785 codes), counting Norwegian residual wording — *annen*, *andre*, *ikke
nærmere*, *ellers*, *diverse*:

| Level | Distinct | Catch-all | Unlabelled |
|---|---|---|---|
| division (2) | 3 | 0.0% | 0.0% |
| **group (3)** | 18 | **38.4%** | 0.0% |
| class (4) | 49 | 18.5% | 0.0% |
| **SN2007 (5)** | 54 | **15.5%** | 0.0% |

**Key at the 5-digit SN2007 level** — Barcelona's and Paris's shape. The
residual concentrates in `96990` *Andre personlige tjenester ikke nevnt annet
sted* (6.0%), `56220` *Kantinedrift og annen cateringvirksomhet* (4.1%),
`47120`, `47780` and `47270`.

⚠️ **Use SSB's labels, NOT a NACE Rev.2 list.** A first attempt used
INSEE's NAF labels on the theory that SN2007's 4-digit classes are NACE
classes. **They are not aligned by truncation**: Norway writes `56.110`
(2 digits + 3) where NACE's class is `56.10` (2 + 2), so slicing a 5-character
Norwegian code at 4 gives `5611`, not the class `5610`. That run reported
**57.8% unlabelled at class level and a meaningless 7.8% catch-all**.
**A high unlabelled share is the tell that the slice is wrong**, not that the
data is odd.

---

## Coordinates — Kartverket, keyless, 97.8% in two stages

`https://ws.geonorge.no/adresser/v1/sok` — no key. Returns
`representasjonspunkt` with `epsg` (EPSG:4258).

**Two stages, and the order matters:**

1. `?kommunenummer=0301&adressetekst=<street>` — exact
2. fall back to `?kommunenummer=0301&sok=<street>` — free text

**97.8%** on 139 real register addresses (130 exact + 6 recovered).

### ⚠️ `fuzzy=true` MUST NEVER BE USED

It "rescued" `Karenslyst allé 8B` as **`Karenslyst allé 1B`** — a different
building — and turned `7-Eleven` into `Ellen Gleditsch' vei 7`. **It returns
plausible coordinates for the wrong place, which a map renders without
complaint.**

The genuine residue is a **suffix-letter mismatch**: the register writes
`Thorvald Meyers gate 71`, the address file holds `71A`. Stage 2 fixes that;
fuzzy is not needed and is dangerous.

### ⚠️ The search is NATIONAL — always constrain

`sok=Karl Johans gate 1` with no `kommunenummer` returns **Sarpsborg**.

### ⚠️ The address API caps at 10,000

Offset 9,900 returns rows; 15,000 returns nothing. **It cannot enumerate the
city** — use it per-address, or take Geonorge's bulk address file.

True misses are register defects: `7-Eleven` and `Flyterminalen` are names in
an address field, ~1.4%.

---

## ✅ Rail — Entur answers, keyless

**`https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_rut-aggregated-gtfs.zip`**
— Ruter's aggregated GTFS via **Entur**, Norway's national access point. A
ranged GET returns **206 with `PK\x03\x04`**, a real zip. The whole-country
feed (`rb_norway-aggregated-gtfs.zip`) is there too if a wider scope is taken.

⚠️ **A HEAD request is not a probe here.** Both URLs answer `200` with
**size 0 and an empty content-type** to `curl -I` — Google Storage does not
serve HEAD usefully — which reads exactly like an empty file. **Use a ranged
GET and check the magic bytes.**

### ✅ MEASURED 2026-09-23 — and every route type is EXTENDED

**386 routes, and NOT ONE uses a basic route type.** The mix is `704` (203),
`712` (127), `702` (20), `705` (19), **`902` (6)**, `1008` (6), **`401` (5)**.

⚠️ **This is the documented trap, live.** `add-country` records that reading
only the basic 0–12 set reported *"Berlin, Hamburg, Stockholm and Oslo as
having no urban rail"*. **Oslo's feed confirms it** — a basic-only reader sees
zero rail here.

| Mode | Type | Lines |
|---|---|---|
| **Metro (T-bane)** | `401` | **5** — lines 1–5, all colour `EC700C` |
| **Tram** | `902` | **6** — lines 12, 13, 15, 17, 18, 19, all colour `0B91EF` |

**11 routes drawn · 356 stops served · 177 distinct parent stations.**

⚠️ **Every metro line shares ONE colour and every tram line shares
another.** `route_color` cannot distinguish line 1 from line 5, so the map
must assign its own per-line palette — the legend requirement is not
satisfiable from the feed alone, unlike Marseille where all five lines carry
distinct hexes.

⚠️ `1008` is water transport — **6 ferry routes**, not drawn, and the same
owner call Marseille raises.

---

## ✅ Licence — BOTH READ 2026-09-23, both permissive

| Source | Declared | Where |
|---|---|---|
| **Brønnøysund** (business) | **NLOD** — *Norsk lisens for offentlige data* | `data.brreg.no/enhetsregisteret/api/dokumentasjon`, stated in the API documentation header |
| **Kartverket / Matrikkelen – Adresse** | **CC BY 4.0** | Geonorge metadata, uuid `f7df7a18-b30f-4745-bd64-d0863812350c` |

Kartverket's record is unusually explicit: `AccessConstraints: Åpne data`,
**`OtherConstraints: "Ingen juridiske begrensninger."`** — no legal
restrictions — `UseLimitations: "Ingen begrensninger på bruk er oppgitt."`,
and INSPIRE `noLimitations` on public access.

**Verdict: PERMITTED WITH CONDITIONS** — attribution only, on both.

⚠️ **NLOD and CC BY 4.0 are different licences and both need their own
attribution line.** Do not collapse them into one credit.

---

## Region

`"region": "Europe"`.

---

## Still unknown — the honest list

- ~~Both licences~~ — ✅ **read 2026-09-23**, NLOD and CC BY 4.0.
- ~~Rail station COUNT~~ — ✅ **answered in this brief's own rail section**:
  **11 routes, 356 stops, 177 distinct parent stations.** This line said it
  was unread while the section above stated it; **a "still unknown" list goes
  stale the same way prose does.**
- ~~`navn` usable share~~ — ✅ **MEASURED 2026-09-23, and the framing was
  wrong.** See the section below; it is **100%**, and the real problem is a
  different one.
- **Scope** — Oslo kommune only, or the wider Osloområdet.

---

## 🚨 The name problem is NOT messiness — it is WHOSE name it is

**Measured 2026-09-23 on all 13,481 Oslo bucket sub-units** (NACE 47/56/96,
`beliggenhetsadresse.kommunenummer = 0301`).

### The cleanup question is settled, and it was never the issue

| | |
|---|---|
| Blank `navn` | **0** |
| End in a legal-form suffix (`AS`, `SA`, `ANS`…) | **41.3%** |
| Contain an `AVD` branch tail | **12.2%** — not the majority this brief implied |
| **Survive the cleanup rule** | ✅ **100.0%** — 0 empty |
| Changed by it | 53.4% |

⚠️ **The earlier reading — "usable share sits below 58.8%" — was wrong, and
wrong in a specific way worth keeping.** It treated a legal-form suffix as
*damage*. It is not: **`1 ØRE AS` → `1 ØRE` is a perfectly good trade name**,
and so are `7 DAYS MINI MARKED`, `377 SPORT`, `A DAY'S MARCH SHIRTS & STAPLES
NORWAY`. A two-character trim is not a data quality problem. **Oslo's names
are the best in this project** — 100% against Paris's 39.6% and Rennes' 53.5%.

### 🚨 But 28.6% of them may be A PERSON'S OWN NAME

| | |
|---|---|
| Sub-units carrying `overordnetEnhet` (the join key) | ✅ **100.0%** |
| Parent is **`ENK`** — *enkeltpersonforetak*, sole trader | ⚠️ **28.6%** (63 of 220 sampled parents) |
| …of those, sub-unit `navn` **identical to parent** `navn` | **54 of 63 — 86%** |
| Paris's comparable figure | **8.7%** |

**Oslo is more than three times more exposed than Paris**, and this project's
standing invariant is explicit: a trade name is fair game, a registrant's own
name at what looks like their premises is not.

### ⚠️ THE TRAP — and it is the registered-office trap in a FIFTH costume

**`organisasjonsform` on the sub-unit is populated on 100% of rows and is
useless for this.** It returns **`BEDR` 97.7% / `AAFY` 2.3% and ZERO `ENK`** —
because those are *sub-unit* forms. **The field exists, is complete, and
answers a different question than the one asked of it.**

The legal form lives on the **parent `enhet`**, reached by `overordnetEnhet`:

```
https://data.brreg.no/enhetsregisteret/api/enheter/{overordnetEnhet}
```

**This is exactly France's shape** — `categorieJuridiqueUniteLegale` lives on
the *unité légale*, never on the *établissement* — and Oslo's brief had no
equivalent rule until now. **Reading `organisasjonsform` off the sub-unit
would have returned a clean 0% natural persons and been believed.**

### So the build rule is

1. **Join every sub-unit to its parent** on `overordnetEnhet` (100% available).
2. **Suppress the name where the parent is `ENK`**; fall back to the address,
   as Paris does.
3. Expect usable names to land near **71%** — still the best in the project.
4. **`check_personal_exposure.py` is load-bearing here, not a formality**, and
   it needs a Norwegian-aware pass before Oslo ships.

```brief-checks
[
  {
    "id": "brreg-bulk-underenheter",
    "claim": "The bulk sub-unit download answers with no key, 88.9 MB gzipped, 864,903 rows. THIS is what settles the scoping question - the paged API stops past ~10,000 and sorts by name, so two API samples disagreed (24.5% vs 4.3%) because both came from the alphabetical head",
    "kind": "http_ok",
    "url": "https://data.brreg.no/enhetsregisteret/api/underenheter/lastned",
    "min_bytes": 50000000
  },
  {
    "id": "geonorge-address-keyless",
    "claim": "Kartverket's address API answers without a key and returns representasjonspunkt. Measured 97.8% via exact adressetekst then plain sok. NEVER pass fuzzy=true - it returned Karenslyst alle 8B as alle 1B, a different building",
    "kind": "http_ok",
    "url": "https://ws.geonorge.no/adresser/v1/sok?kommunenummer=0301&adressetekst=Middelthuns%20gate%2011B&treffPerSide=1",
    "min_bytes": 200
  },
  {
    "id": "brreg-kommune-filter-does-not-constrain-the-read-address",
    "claim": "The paged API answers ?kommunenummer=0301, but that does NOT guarantee beliggenhetsadresse is in Oslo - the misses included Bergen, Copenhagen, Paris and Malmo. Pinned so the trap is re-findable: filter on beliggenhetsadresse.kommunenummer locally, never on the query parameter",
    "kind": "http_ok",
    "url": "https://data.brreg.no/enhetsregisteret/api/underenheter?kommunenummer=0301&size=1",
    "min_bytes": 200
  },
  {
    "id": "brreg-legal-form-is-on-the-PARENT-not-the-subunit",
    "claim": "THE PRIVACY GUARD, and the trap that hides it. A sub-unit's own organisasjonsform is BEDR or AAFY on 100% of rows and NEVER ENK, because those are sub-unit forms - a complete, populated field that answers a different question. The sole-trader form lives on the parent enhet, reached by overordnetEnhet, which 100% of sub-units carry. Sampling 220 parents: 28.6% are ENK, and 86% of those share the sub-unit's name. Reading the sub-unit field instead would report 0% natural persons and be believed",
    "kind": "http_contains",
    "url": "https://data.brreg.no/enhetsregisteret/api/underenheter?kommunenummer=0301&naeringskode=47&size=1",
    "present": ["overordnetEnhet"]
  },
  {
    "id": "brreg-enheter-endpoint-serves-the-legal-form",
    "claim": "The parent endpoint is live and returns organisasjonsform, which is where ENK is actually visible. If this breaks, Oslo has no natural-person guard and must not ship - Norway is 3x more exposed than Paris at 28.6% against 8.7%",
    "kind": "http_contains",
    "url": "https://data.brreg.no/enhetsregisteret/api/enheter?kommunenummer=0301&organisasjonsform=ENK&size=1",
    "present": ["ENK"]
  }
]
```
