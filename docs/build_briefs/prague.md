# Prague — build brief

**Step 0 measured 2026-09-22/23.** Run `python scripts/brief_check.py prague`
before writing code.

---

## The one-line summary

**The cheapest coordinate step in the project — and a taxonomy that cannot be
keyed at a level.** RÚIAN resolves 99.8% of rows to a coordinate by dict
lookup, but CZ-NACE is stored at **ragged depth**: only 57.9% of Prague's rows
reach the finest level and 31.4% stop at the 3-digit group.

---

## Business leg — the Statistical Office's RES

| | |
|---|---|
| File | `https://opendata.czso.cz/data/od_org03/res_data.csv` |
| Size | **543 MB**, 3,528,951 rows nationally |
| Prague filter | `OKRESLAU == "CZ0100"`, active = `DDATZAN` empty |
| Active Prague in NACE 47/56/96 | **≈85,000** (33,149 counted in the first 1.4 M rows) |
| `FIRMA` trade name | **100.0%** |
| Street + house number | **99.9%** |
| `KODADM` (RÚIAN code) | **99.9%** |

**`FIRMA` at 100% is the headline.** Milan's `insegna` is 17.6% and Paris's
premises name 42.9% — **Prague is the only one of the three with a name on
every row.**

⚠️ **CZ-NACE here is SINGLE-VALUED** (*převažující činnost*), unlike ARES's
fifteen-code array. Use RES, not ARES.

---

## Coordinates — a JOIN, 99.8%, the cheapest in the project

**RÚIAN's Praha export: `https://vdp.cuzk.gov.cz/vymenny_format/csv/
20260831_OB_554782_ADR.csv.zip` — 3.4 MB zipped, keyless.**

| | |
|---|---|
| Addresses | **134,627**, every one a unique `Kód ADM` |
| With coordinates | **99.99%** (134,621) |
| Measured join rate | **99.8%** on 6,000 active Prague bucket rows |

The old `vdp.cuzk.cz` host **redirects** rather than dying — unlike `rzp.cz`,
which moved to `rzp.gov.cz`.

### ⚠️ The CRS needs a sign flip AND an axis swap — verified, not reasoned

RÚIAN publishes `Souřadnice X` ≈ 1,042,569 and `Souřadnice Y` ≈ 744,384, both
**positive**. Transforming the first row — Hrad I. nádvoří, Prague Castle —
against its known position:

| Interpretation | Result |
|---|---|
| **`EPSG:5513` with (X, Y) as published** | **50.08948, 14.39861** ✅ |
| **`EPSG:5514` with (−Y, −X)** | **identical** ✅ |
| `EPSG:5514` with (−X, −Y) | 52.27849, 9.47158 — **Germany** |
| `EPSG:5514` with (Y, X) | 68.51016, 41.59194 — **the Arctic** |

**The wrong orderings produce plausible numbers and fail silently**, which is
why this was settled before any pipeline code existed to inherit it.

---

## ⚠️ Taxonomy — CZ-NACE is RAGGED, and no level can be chosen

`premises-taxonomy` assumes a level can be picked — Barcelona keys at its
finest, Madrid near the top. **Prague supports neither**, because the codes are
not all the same depth. Measured on 12,000 active Prague bucket rows:

| Code depth | Rows | Share |
|---|---|---|
| 2 chars — division | 532 | **4.4%** |
| **3 chars — group** | 3,773 | **31.4%** |
| 4 chars — class | 746 | 6.2% |
| **5 chars — national sub-class** | 6,949 | **57.9%** |

**Only 57.9% reach the finest level. Keying at class (4) covers 64.1%** — the
other 35.9% are too short even for that.

`4725` and `47250` both appear. So do `47`, `471` and `47190`. **RES stores
whatever depth the subject declared.**

### So the taxonomy must match on PREFIX, not on a level

Classify at the deepest level a row actually has, falling back up the
hierarchy. A fixed-level key would either discard a third of the city or
collapse it into one bucket.

**And the largest single code is `471` at 30.2%** — *retail sale in
non-specialised stores*, at group level. **Nearly a third of Prague's rows say
only that.** `56100` (restaurants) is another 29.4%, so two codes are 59.6% of
the city.

Catch-all share, for the record: division 25.7%, group 63.7%, class 39.7%.
**All three are worse than Paris's 19.3%**, and the raggedness is why.

---

## Rail — ✅ OSM, and the Golemio key is NOT needed

Measured 2026-09-23 over Prague's bounding box:

| | |
|---|---|
| Relations | **85** |
| Tram | 79 |
| Subway | 6 (Metro A, B, C — both directions) |
| **Named** | **85 / 85 = 100%** |
| Coloured | 61 (72%) |

**This settles gate item 4.** `api.golemio.cz` returns 401 and needs a key;
**it is not required** — OSM carries the whole network, fully named. Use
`osm-rail`.

⚠️ 24 relations carry no `colour`. Every drawn line needs a legend entry and an
on-map label regardless, so assign colours for those rather than dropping them.

---

## Licence — one read, one still open

**ČSÚ is settled. ČÚZK is not, and it is the only thing blocking this city.**

- ✅ **RES / ČSÚ — READ 2026-09-23. CC BY 4.0, PERMITTED WITH CONDITIONS.**
  The national catalogue's DCAT record resolves a `podmínky-užití`
  distribution per dataset, and ČSÚ's own terms page carries the operative
  text. ⚠️ **Read the DATA paragraph, not the website one** — the CC BY
  sentence is about `csu.gov.cz` *web pages*; the data conditions follow it
  under *"Další podmínky použití dat ČSÚ"*, and impose **two obligations
  this build triggers**:
  - **MUST DISPLAY** — *"v případě šíření dat ČSÚ vzniká povinnost uvést
    podmínky této licence, nejlépe přímým odkazem na tuto webovou stránku"* —
    state the licence conditions, preferably as a direct link to that page.
  - **MUST DISCLOSE, and MUST NOT SAY** — *"upravené nebo odvozené údaje musí
    být označeny jako upravené nebo odvozené a nesmí být prezentovány jako
    nezměněné oficiální statistiky Českého statistického úřadu"* — modified or
    derived data must be **marked as such** and must **not** be presented as
    unchanged official ČSÚ statistics. **This project's ring density, bucketing
    and storefront filtering are all transformations**, so this fires every
    time — the Montréal and INEGI family.
- **RÚIAN / ČÚZK** — `vdp.cuzk.gov.cz/vdp/ruian/vymennyformat` returns 200 but
  carries **no data licence**: the only terms link is *"Podmínky užívání
  aplikace a cookies"*, which is **application and cookie terms, not data
  terms** — the New York footer shape.

**Use the `licence-read` agent on each before any build.** A government open
portal is a reason to expect permissive terms, not evidence of them.

---

## Region

`"region": "Europe"` — per `docs/scaling_thresholds.md`.

---

## Still unknown — the honest list

- **ČÚZK / RÚIAN's licence** (above). **The single blocker.** ČSÚ is read.
- **The prefix-matching taxonomy has no precedent in this project** — four
  cities needed a local taxonomy and all four had uniform depth.
- **Scope** — Prague's `OKRESLAU CZ0100` is the whole city (all 22 městské
  části). Whether the tram network's reach justifies a wider scope is unasked.
- **The employee filter.** `KATPO` is an employee-count band and 46,447 of
  85,022 are `000`; the SIRENE-style filter would leave **38,575**. Whether to
  apply it is an owner call, unresolved — Paris's equivalent took 148,633 to
  50,156.
- **`EXPDATE`-style currency** — RES has no per-row validity window; the file
  is dated 2026-09-17 as a whole.

```brief-checks
[
  {
    "id": "czso-res-downloads",
    "claim": "The Statistical Office's RES file downloads with no key. 543 MB, 3,528,951 rows nationally. This is the business leg - use RES, not ARES, because CZ-NACE here is single-valued",
    "kind": "http_ok",
    "url": "https://opendata.czso.cz/data/od_org03/res_data.csv",
    "min_bytes": 1000000
  },
  {
    "id": "ruian-praha-addresses",
    "claim": "RUIAN's Praha address export is 3.4 MB zipped and keyless - 134,627 addresses, every one a unique Kod ADM, 99.99% with coordinates. This is what makes Prague's coordinate step a JOIN rather than a geocode, measured at 99.8%",
    "kind": "http_ok",
    "url": "https://vdp.cuzk.gov.cz/vymenny_format/csv/20260831_OB_554782_ADR.csv.zip",
    "min_bytes": 3000000
  },
  {
    "id": "cuzk-old-host-redirects",
    "claim": "The old vdp.cuzk.cz host REDIRECTS rather than dying, unlike rzp.cz which moved to rzp.gov.cz. Pinned so a future 404 is recognised as a move rather than a removal",
    "kind": "http_ok",
    "url": "https://vdp.cuzk.cz/vymenny_format/csv/20260831_OB_554782_ADR.csv.zip",
    "min_bytes": 3000000
  }
]
```
