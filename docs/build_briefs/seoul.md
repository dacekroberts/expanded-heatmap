# Seoul — build brief

**Step 0 completed 2026-09-24.** This supersedes the partial brief of
2026-09-23, whose list of "never done" items was partly stale on the day it
was written: the eight core datasets, their licence and the scope had been
measured on 2026-09-22 (`DECISIONS.md`). Run `python scripts/brief_check.py
seoul` before writing any code. **Four owner decisions are open (🚩 below).**
Nothing else blocks the build.

---

## The one-line summary

**Seventeen citywide permit registers, all 25 gu, coordinates on 91–99% and
filled to 97.7%+ from the register itself, KOGL Type 1 on every one, no
account and no operator columns. Three buckets: about 157,000 food premises,
53,000 retail and 40,000 personal services. The subway is the best-tagged in
the project.**

---

## 🚩 Owner decisions (recommendations, not decided)

1. **Buckets.** Measured below; each recommendation follows an existing
   precedent:

   | Dataset | Active | Recommendation | Precedent |
   |---|---|---|---|
   | 일반음식점 | 120,182 | **Food service**, less 출장조리 106, 이동조리 3, 푸드트럭 14 | not premises |
   | 휴게음식점 | 37,113 | **Food service**, less 푸드트럭 483; **편의점 6,037 and 과자점 186 → Retail** | Boston (convenience stores are retail); Japan (bakeries are retail) |
   | 미용업, 이용업, 세탁업 | 39,308 | **Personal services** | every city |
   | 목욕장업 (public baths, 찜질방) | 673 | **Personal services** | Prague kept saunas; Calgary's `BATH HOUSE` was adult services, which these are not |
   | 제과점영업, 즉석판매제조가공업, 식품판매업(기타) | 20,298 | **Retail** | Japan (bakeries and delis) |
   | 축산판매업 | 11,628 | **Retail: 식육판매업 (butchers) 6,317 only.** Distribution, import, milk and egg collection are wholesale | — |
   | 담배소매업 | 15,590 | **Retail**: convenience stores, corner shops, supermarkets | — |
   | 대규모점포 | 740 | **Retail**: department stores, marts, shopping centres, markets | — |
   | 건강기능식품일반판매업 | 29,315 | **Retail: 영업장판매 (in-store) 10,648 only.** 52% are e-commerce sellers, often at home | — |
   | 숙박업 | 2,788 | **Excluded** (lodging) | every city |
   | 동물병원 | 981 | **Excluded** (veterinary, NAICS 541940, professional) | the NAICS cities |
   | 유흥주점 | 1,682 | **Excluded**: 73% 룸살롱 (hostess bars), plus 카바레 and 요정 | Calgary and Edmonton adult-services rule (owner, 2026-09-21) |
   | 단란주점 (karaoke bars licensed for alcohol) | 1,865 | **Excluded**, on the same sensitivity grounds: the permit class sits beside 유흥주점 and is small. The alternative is Food service, as a drinking place | owner's call |

2. **Rail scope** (measured below). Draw the 9 numbered lines, 신분당선,
   우이신설선 and 신림선. The open question is the five Korail metro lines
   OSM tags `train`/commuter but Seoul signs as subway: 경의·중앙, 수인·분당,
   경춘, 서해 and 공항철도 (all-stop). GTX-A, AREX express and every intercity
   service stay out. The 김포 골드라인 enters Seoul only at its terminus, a
   stub, which goes to the owner as Japan's stubs did.
3. **Stations inside Seoul only**, matching the Seoul-only register (Japan's
   rule, owner 2026-09-24). Lines are still drawn to their ends.
4. **Map region.** No Asian region exists yet. Recommendation: **"East
   Asia"**, one region, as with South America (owner 2026-09-24: continent,
   not country). Japan, Taiwan and Hong Kong join it as they land. Scored by
   `check_macro_labels.py` like every region.

---

## Business leg — Seoul's 인허가 정보 (LOCALDATA, republished citywide)

| | |
|---|---|
| Source | `data.seoul.go.kr`, one dataset per permit type, **citywide: all 25 gu in every file** (25 `개방자치단체코드` each) |
| Access | ✅ **No account.** The dataset page's SHEET export: `POST datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do` with `infId=<OA-id>`, `srvType=S`, `serviceKind=1`, `gridTotalCnt=999999`, **`ssUserId=SAMPLE_VIEW`**. That is the anonymous identity the page sends when nobody is signed in, not a bypass. cp949 CSV |
| Schema | the LOCALDATA columns: `영업상태명`, `폐업일자`, `도로명주소`, `지번주소`, `사업장명`, `업태구분명`/`위생업태명`, **`좌표정보(X)`/`(Y)` in EPSG:5174** |
| Status | `영업/정상` vs `폐업`; a few types add `휴업` or `취소/말소…`. Keep `영업/정상` only |
| Updated | daily (`갱신주기 매일`) |
| Licence | **공공누리 제1유형 (KOGL Type 1) on all 17**, `제3저작권자 없음` on every one. The first eight were read 2026-09-22; the nine below were checked individually 2026-09-24 |

### 🚨 Find datasets by OA id, never by search

`data.seoul.go.kr`'s search ignores `GET ?srchDetailWord=` and `POST
searchKeyword=`: a real term and `zzzzqqq` returned byte-identical pages. The
citywide permit family lives in **OA-16040 to OA-16157**, one per type (per-gu
medical types follow). **A GET sweep of that range, reading `<meta
name="title">`, found 118 citywide permit types on 2026-09-24.** The
2026-09-21 sweep skipped 16050–16280, exactly where they are.

### The seventeen datasets (active = `영업/정상`)

| OA | Type | Rows | Active | Coords (active) |
|---|---|---|---|---|
| 16094 | 일반음식점 | 537,906 | 120,182 | **90.7%** → 97.7% with the join below |
| 16095 | 휴게음식점 | 147,582 | 37,113 | 97.6% |
| 16063 | 미용업 | 99,802 | 33,679 | 98.7% |
| 16064 | 이용업 | 15,635 | 2,366 | 99.0% |
| 16065 | 세탁업 | 15,360 | 3,263 | 99.3% |
| 16146 | 목욕장업 | 3,991 | 673 | 99.4% |
| 16044 | 숙박업 | 7,157 | 2,788 | 99.5% |
| 16007 | 동물병원 | 2,235 | 981 | 99.0% |
| 16084 | 제과점영업 | 16,714 | 4,228 | 98.2% |
| 16085 | 즉석판매제조가공업 | 156,268 | 15,410 | 95.9% |
| 16080 | 식품판매업(기타) | 1,962 | 660 | 98.6% |
| 16071 | 축산판매업 | 42,019 | 11,628 | 94.8% |
| 16144 | 담배소매업 | 95,506 | 15,590 | 97.3% |
| 16096 | 대규모점포 | 1,053 | 740 | 92.6% |
| 16070 | 건강기능식품일반판매업 | 116,123 | 29,315 | 95.1% |
| 16089 | 단란주점영업 | 11,616 | 1,865 | 98.9% |
| 16090 | 유흥주점영업 | 4,991 | 1,682 | 99.0% |

Not candidates (in the same range, recorded so nobody re-probes them):
wholesale, manufacturing and transport food types; 식품자동판매기업 (vending
machines); cinemas; travel agencies; sports facilities; environmental trades.
Pharmacies (약국) and opticians (안경업) have **no citywide file** in the
range. Pharmacies partly arrive through 건강기능식품 영업장판매.

### Taxonomy — the catch-all measurement (`premises-taxonomy`)

- **The bucket keys on the permit type, where there is no catch-all**: every
  file is one named type. So 일반음식점's `기타` (17.7%) and 휴게음식점's
  `기타 휴게음식점` (20.4%) stay in Food service whatever they are.
- **The sub-type is used only to take rows out or move them**: food trucks,
  catering, 편의점, 과자점, the 축산 channels and the 건기식 channels.
- **Recommendation: key at the permit type.** `pipeline/taxonomies/` gains a
  `korea_localdata.py` keyed on (dataset, 업태/위생업태).

### Retail after de-duplication (measured 2026-09-24)

A convenience store can hold a tobacco, a 휴게음식점 and a 건기식 permit at
once. Counted once per building, by brand for the five chains and by name
otherwise:
- 59,816 retail permits come to **53,215 premises**.
- **10,395 convenience stores.** 4,289 of the 6,037 휴게 편의점 were already
  counted.

Food and personal services overlap negligibly: 62 restaurant/café pairs and
21 salon/barber pairs share a name and building. Within-file repeats: 541
restaurants.

### Coordinates — the register fills its own gaps (the `address-join` shape)

- **11,121 active restaurants (9.3%) have an address but no point.** Not new
  premises lagging: about 10% of every licence year since 2013.
- **It is by district.** 종로구 1,861, 강남구 1,269, 영등포구 1,268, against
  양천구 8 and 노원구 28. Most were stamped by bulk updates in 2025-12 and
  2026-01.
- **Fix: borrow the point of any other row, open or closed, in any of the
  eight files, at the same building** (road address to the building number,
  else the lot address). The 1.2 million rows give 124,340 building points.
  - **Control**: 93,048 restaurants that have a point were placed this way
    from other rows. **Median 0 m, 90th percentile 0 m, 99th 11 m, and 0.2%
    over 100 m.** The register's points are building points.
  - **Result**: 8,409 of 11,121 placed (8,064 by road address, 345 by lot).
    Restaurants go **from 90.7% to 97.7%**. **2,712 remain unplaced**
    (2.3%), disclosed.
- No geocoder. If the owner wants the last 2.3%, the national road-address
  database (juso.go.kr) is the next source. It is unread and unprobed.

### Privacy

- **No operator column in any of the 17.** Only `전화번호` is personal-adjacent:
  **never read, never published.**
- **`scripts/check_personal_exposure.py` needs a Korean pass at build**
  (sized 2026-09-24):
  - The case is a trade name that is a bare person's name (a common surname
    plus two syllables, or that plus 헤어/네일/세탁소…) at an address that
    reads residential (아파트, 빌라, 동/호) and not commercial (상가, 빌딩, 시장…).
  - **113 premises** across the core eight: 51 restaurants, 49 salons, 7
    cafés, 5 laundries and 1 bathhouse.
  - Suppress the name on those, as the invariant requires.
  - E-commerce health-food sellers (home addresses) are already out by the
    bucket rule.

---

## Rail — MEASURED 2026-09-23 and 2026-09-24

Inside OSM relation **2297418** (서울특별시), resolved by name:

| | |
|---|---|
| `route=subway` | **149 relations**, all named and coloured, refs `1`–`9` and `신분당`. Line 1 is mostly Korail-operated and tagged subway |
| `route=light_rail` | **6 relations = 3 lines**, all coloured: 우이신설선 (`W`, #BACC50), 신림선 (#6789CA), 김포 골드라인 (#957326, a stub in Seoul) |
| `route=train` | 65 relations: the five Korail metro lines, GTX-A, AREX (express and all-stop), KTX/ITX/무궁화 intercity |
| **Stations** | **369 `railway=station`** (364 nodes, 5 ways). 313 `station=subway`, 41 `station=light_rail`. The 2026-09-23 "0" was a failed query, not a fact |

⚠️ **Korea's national station standard dataset has no line geometry**
(1,099 stations, no lines). **OSM is the rail source.**

### Per-line stations inside Seoul (for decision 2)

The longest relation of each line: its stops in order, those inside relation
2297418, and the mean gap between consecutive Seoul stops (straight line).
`scratchpad/seoul_s0/spacing.py`, Overpass, 2026-09-24:

| Line | OSM tag | Stops | In Seoul | Mean spacing | Max |
|---|---|---|---|---|---|
| 2 (circle) | subway | 44 | 44 | 1.10 km | 2.09 |
| 3 | subway | 44 | 33 | 1.10 | 1.94 |
| 4 | subway | 48 | 26 | 1.18 | 2.37 |
| 5 | subway | 49 | 45 | 1.00 | 1.91 |
| 6 | subway | 40 | 40 | 0.91 | 1.44 |
| 8 | subway | 24 | 12 | 1.02 | 1.62 |
| 9 | subway | 38 | 38 | 1.00 | 1.88 |
| 1 | subway (Korail-run) | 65 | 33 | 1.18 | 2.62 |
| 신분당 | subway | 16 | 7 | 1.36 | 2.81 |
| 우이신설 | light_rail | 13 | 13 | 0.89 | 1.17 |
| **경의·중앙** | train/commuter | 52 | **20** | **1.39** | 2.31 |
| **수인·분당** | train/commuter | 63 | **14** | **1.37** | 2.89 |
| **경춘** | train/commuter | 24 | **6** | **1.25** | 1.75 |
| 공항철도 (all-stop) | train/commuter | 14 | 6 | **3.37** | 6.35 |
| GTX-A | train/commuter | 5 | 2 | 8.42 | 8.42 |
| 서해 | train/commuter | 21 | **1** (stub) | — | — |
| 김포 골드라인 | light_rail | 10 | **1** (stub) | — | — |

- **Recommendation for decision 2.** Draw **경의·중앙, 수인·분당 and 경춘**:
  inside Seoul their spacing (1.25–1.39 km) sits within the subway's own
  (0.91–1.36 km). Seoul signs them as metropolitan subway lines, with
  integrated fares. Leave out 공항철도 (3.4 km, an airport commuter line),
  GTX-A and AREX express.
  - **Frequency** is the owner's third test and is **not measured** here (no
    GTFS). A cited timetable read goes with the decision.
  - 서해 and 김포 골드라인 are one-station stubs. Recommendation: leave both
    out, but they go to the owner under the stub rule.
- 🚨 **Two measurements FAILED and are not results.** Line 7 returned "0 in
  Seoul" (it runs through Seoul end to end; the area half of the query failed
  under Overpass 429/504s). 신림선 did not run before Overpass gave out. Both
  are re-measured at build, not recorded as zeros. AREX express returned 0,
  also unreliable (서울역 is in Seoul), but that line is excluded anyway.

---

## Still unknown

- The owner's four calls above.
- Whether juso.go.kr can place the last 2.3% keylessly (only if wanted).

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
    "id": "seoul-restaurant-dataset-page",
    "claim": "OA-16094 is the citywide 일반음식점 permit register (KOGL Type 1), found by OA id",
    "kind": "http_ok",
    "url": "https://data.seoul.go.kr/dataList/OA-16094/S/1/datasetView.do",
    "min_bytes": 20000
  },
  {
    "id": "seoul-tobacco-dataset-page",
    "claim": "OA-16144 is the citywide 담배소매업 register, the broadest retail proxy (15,590 active)",
    "kind": "http_ok",
    "url": "https://data.seoul.go.kr/dataList/OA-16144/S/1/datasetView.do",
    "min_bytes": 20000
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
