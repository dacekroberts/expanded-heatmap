# Bucharest — build brief

**Screening closed 2026-09-22; rail re-counted and addresses re-measured
2026-09-23.** Run `python scripts/brief_check.py bucharest` before writing any
code for this city.

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
  }
]
```
