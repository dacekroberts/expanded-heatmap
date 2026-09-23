# Seoul — build brief

**Partial. Written 2026-09-23 from Korea's country screening plus a rail
probe.** ⚠️ **This is the least complete brief in the project and says so at
the top** — Seoul had none at all until now, despite sitting in the
ready-to-build band. Run `python scripts/brief_check.py seoul` before writing
any code.

---

## The one-line summary

**The largest business register of any unbuilt city, with coordinates on both
legs and no account anywhere — and the best rail in the project.** What it
does not have is a Step 0: the eight datasets have never been enumerated
individually, and its taxonomy has never been measured.

---

## Business leg — 인허가 정보, from Korea's country screen

| | |
|---|---|
| Source | **Seoul's 인허가 정보** (licensing information), `data.seoul.go.kr` |
| Rows | **197,276 active premises** across **8 datasets** |
| Account | ✅ **None.** The SHEET export is the logged-out path — `ssUserId=SAMPLE_VIEW` |
| Coordinates | ✅ **`좌표정보(X/Y)` on 99.5% of active premises**, **EPSG:5174** |
| Licence | **KOGL Type 1** |
| Portal | Live 2026-09-23 — `data.seoul.go.kr` answers 200 |

✅ **Korea needs neither a geocoding leg nor a new geocoder** — coordinates
come with the register. That is Paris's shape and it is why Korea was ordered
first among the three keyless candidates.

⚠️ **EPSG:5174 is Korea Central Belt 2010.** Project rule: never buffer or
measure in 4326 — but here the *source* is already projected, so the flow is
5174 → WGS84 for display, and the ring geometry can stay in a metric CRS
throughout.

### 🚨 The portal's search is INERT — enumerate, never search

`data.seoul.go.kr` **ignores both `GET ?srchDetailWord=` and
`POST searchKeyword=`**. A real hygiene term and the nonsense term `zzzzqqq`
returned **byte-identical pages**, and the ten datasets on them looked like
hygiene results only because the catalogue's default ordering surfaces them.
**A conclusion was already drawn from that and was wrong.**

**Use the portal's own facet counts instead of sampling**: its
`제공유형 SHEET (182) OPENAPI (180) LINK (71) CHART (27)` — with **no FILE
row** — settled in one read what paging through 251 results did not.

---

## Rail — the best in the project, MEASURED 2026-09-23

Inside OSM relation **2297418** (서울특별시 / Seoul, admin_level 4):

| | |
|---|---|
| **Subway route relations** | **149** |
| **Named** | ✅ **149 — all of them** |
| **Coloured** | ✅ **149 — all of them** |
| Refs | **10** — `1` `2` `3` `4` `5` `6` `7` `8` `9` `신분당` |
| **Relations with NO `ref`** | ✅ **0** |
| `train` (commuter — excluded) | 65 relations, 38 coloured, **27 with no `ref`** |

✅ **Zero unref'd subway relations is the opposite of what three other cities
showed on the same day** — Bucharest's `Extensie M4`, Singapore's uncoloured
`JRL`, Stockholm's unref'd subway and tram. **Seoul's metro needs no
hand-assigned colours and no ref recovery.**

⛔ **`train` is commuter rail** — AREX, GTX-A, 경의·중앙, 경춘, 공항철도,
서해, 수인·분당 — excluded by the standing rule in every built city.

### 🚨 Two rail measurements FAILED and are NOT recorded as results

- **`light_rail` returned a transport error**, not a count. **Unmeasured.**
  Seoul has light-rail lines (Ui-Sinseol, Sillim), so this is a real gap.
- **The station-node query returned `0`.** Seoul has several hundred stations.
  **That zero is a statement about the query, not about Seoul** — Korean
  stations are evidently tagged in a way `node["railway"="station"]` misses.
  **It is recorded as UNKNOWN rather than as zero**, because an uncontrolled
  zero is exactly what this project keeps being caught by.

⚠️ **Korea's national station standard dataset is a false friend here.** It
carries **1,099 stations with WGS84 coordinates and NO LINE GEOMETRY at all**
— `add-country` names this exact case: it passes *"are there station points"*
and fails *"is there line geometry"*, and **a screen that asks only the first
records a false pass.** This project draws and labels every line, so **OSM is
the rail source, not the standard dataset.**

---

## ⚠️ What this brief does NOT have — the honest list

**This is Step 0 work that has never been done, not detail that was omitted.**

1. 🚨 **The eight datasets have never been enumerated individually.** 197,276
   is a country-screen total. **Which eight, how many rows each, what columns,
   and whether they overlap** are all unknown. **A row count is not a schema**,
   and this project has been caught by that repeatedly.
2. 🚨 **The taxonomy has never been measured.** Korean licensing categories
   (업태구분명 and similar) need `premises-taxonomy`'s deciding measurement —
   **the catch-all share at each level** — before any module is written. Four
   cities have needed this and it has been skipped every time.
3. 🚨 **The non-storefront share is unknown.** Every register measured this
   week carried one: Philadelphia 79%, D.C. 61%, Göteborg 26.5%, Hong Kong
   14,263 of 35,808. **Seoul's is not a question of whether, only how large.**
4. 🚨 **`check_personal_exposure.py` needs a Korean-aware pass** before any
   publish — a standing item, and the same shape Copenhagen needs for Danish.
5. ⚠️ **The KOGL Type 1 terms have not been read** with `read-licence`. Type 1
   is permissive by reputation, **and a government portal is a reason to
   expect permissive terms, not evidence of them.**
6. ⚠️ **Partial geocoding for 일반음식점 at 90.7%** is recorded from screening
   — what the other 9.3% are, and whether the gap is systematic, is unasked.
7. ⚠️ **Scope** — Seoul Special City is 25 자치구; whether the register is
   published per-gu or citywide is unconfirmed.

---

## Region

Seoul needs its **own map region** — it is not Europe. Same open question as
Hong Kong.

```brief-checks
[
  {
    "id": "seoul-portal-live",
    "claim": "data.seoul.go.kr answers without an account. NOTE the standing trap on this host: its search parameter is INERT - a real term and the nonsense term zzzzqqq return byte-identical pages - so enumerate or use the portal's own facet counts, never trust a search result",
    "kind": "http_ok",
    "url": "https://data.seoul.go.kr/",
    "min_bytes": 50000
  },
  {
    "id": "seoul-osm-boundary-resolves",
    "claim": "OSM relation 2297418 is Seoul (서울특별시), admin_level 4, and is the area the 149 subway relations were counted in. Resolved BY NAME rather than guessed - a guessed relation id returned 0 for Bucharest once and that zero was a statement about the guess",
    "kind": "http_ok",
    "url": "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A60%5D%3Brel(2297418)%3Bout%20ids%3B",
    "min_bytes": 100
  }
]
```
