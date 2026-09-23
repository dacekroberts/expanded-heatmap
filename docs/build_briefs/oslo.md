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

⚠️ **Run `brief_check.py`'s `taxonomy_catchall` before writing the module.**
`96990` is the visible residual at 6.0%, but the catch-all share at each level
has **not** been computed here, and `premises-taxonomy` is explicit that it is
the deciding measurement and the one always skipped.

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

## Rail — NOT YET MEASURED

Norway publishes GTFS through **Entur**, the national point, and OSM is the
fallback. **Neither has been probed**, and the station-density estimate that
would rank Oslo failed: three Overpass endpoints returned `runtime error:
open64`. **Oslo's station count is UNMEASURED, not zero.**

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
- **Rail** — Entur vs OSM unprobed; station count unmeasured.
- **The NACE catch-all share at each level.**
- **Trade-name fill.** `navn` exists on every sub-unit, but whether it is a
  trade name or a legal name is unmeasured — the question that caught Milan and
  Paris.
- **Scope** — Oslo kommune only, or the wider Osloområdet.

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
  }
]
```
