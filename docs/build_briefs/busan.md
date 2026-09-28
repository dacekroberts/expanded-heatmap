# Busan — build brief

**Step 0 completed 2026-09-27** (Staging). Run `python scripts/brief_check.py
busan` before writing any code. The licence is read (PERMITTED WITH
CONDITIONS, a credit; the terms' 제14조 read narrowly, owner 2026-09-27) and
the frozen snapshot is accepted ("Busan snapshot ok"). **Three owner calls
are open** (below), each with a recommendation.

---

## The one-line summary

**Seoul's register through a keyless API, with two parameter traps that each
silently drop rows.** Fourteen permit types, all 16 구·군, points on
94.4–99.5%, no operator field. **About 53,600 food premises, 23,000 retail and
16,700 personal-services permits** before de-duplication, the same types as
Seoul's. The snapshot is frozen at 2026-04-15 and, unlike Daegu's label, the
rows agree with it. Rail is four city lines (one a monorail Seoul's query
would drop) and the Busan–Gimhae LRT: **110 stations** in Busan.

---

## Owner calls — open, with recommendations

1. **Buckets as Seoul's** (owner 2026-09-24): 단란주점 → Food service (1,481);
   유흥주점 (2,271), lodging and veterinary clinics out; convenience stores and
   confectioners holding a café permit → Retail; butchers only from 축산판매업;
   in-store sellers only from 건강기능식품. Nothing new to decide unless the
   owner wants to revisit.
2. **동해선 광역전철 (Korail, 부전–태화강): recommended OUT, but this one is
   closer than Daegu's.**
   - Inside Busan it has **16 stops at a mean 2.29 km** (max 5.44). The
     city's lines run 0.86–1.09 km. Seoul drew Korail lines at 1.25–1.39 km
     and left out 공항철도 at 3.37 km, so 2.29 sits between the precedents.
   - **For drawing it: coverage.** It is the only rail along the 해운대–송정–
     기장 coast beyond Line 2's end, and 기장군 has no other line.
   - **Frequency is not measured** (no GTFS). A cited timetable read goes with
     the decision; a 30-minute off-peak headway would fail the test as
     Mulhouse's tram-train did.
3. **Stations inside Busan only** (Seoul's, Daegu's and Japan's rule), with
   **the Busan–Gimhae LRT drawn** and its 9 Busan stations kept.
   - Its 12 Gimhae stations and Line 2's 5 Yangsan stations are excluded,
     with the lines drawn to their ends. Neither city is in Busan's register.
     Gimhae itself is in Band D (no reachable register), so a "(Regional)"
     scope would add stations with no businesses around them.
   - The LRT keeps 9 of 21 (43%), under Toulouse's 54% precedent. But its
     Busan stretch is not a stub: it is the 사상–대저 corridor, with two
     transfer stations.

---

## Business leg — Busan's `LocalDataService` Open API (the national LOCALDATA register)

| | |
|---|---|
| Source | `data.busan.go.kr` (Big-데이터웨이브), "구군 인허가포털", catalogued OA_TT00001–36 (37–39 are other Ministry lists). One REST operation per GROUP of permit types, e.g. `LocalRstrn` (음식점), `LocalStore` (식품 제조·가공·판매) |
| Access | ✅ **No key, no account.** `GET https://data.busan.go.kr/open/services/LocalDataService/<Operation>?pageIndex=N&pageSize=1000&resultType=json&opnSvcId=<id>`. `totalCount` comes back as a string. The host is slow and intermittently answers non-JSON under load: retry with backoff, and pull one operation at a time |
| Parameters | Documented by the portal (`selectOpenData.do`): `localCode`, `bgnYmd`/`endYmd` (permit date), `lastModTsBgn`/`lastModTsEnd`, `state` (01 영업/정상, 02 휴업, 03 폐업, 04 취소…), `pageIndex`, `pageSize`, `resultFileYn`, `resultType`, **`opnSvcId`** |
| Coverage | all **16 구·군** in every operation read, each under its own `opnsfteamcode` |
| Snapshot | **Frozen.** Every operation's newest `updatedt` is 2026-04-15 and newest `lastmodts` 2026-04-13, the day before LOCALDATA moved to data.go.kr. **Unlike Daegu's, the rows agree with the label**: restaurant permits run every month to 2026-04 (147 in April's first two weeks). Owner's call: build from it and state the date on the page |
| CRS | **EPSG:5174** (`x`, `y`), as Seoul and Daegu: of the open premises with a point, **97,260 land inside OSM's 부산광역시 boundary and 2 outside** |
| Licence | PERMITTED WITH CONDITIONS; credit and position in `docs/data_sources.md`, "Daegu and Busan" |

### 🚨 Two parameter traps — each silently drops rows

1. **Never filter on `state`.** Rows permitted after 2025-01-31 carry **no
   status code** (`trdstategbn` null), so `state=01` excludes every one of
   them while still returning older rows that have since closed.
   - Measured on 일반음식점: `state` 01 + 03 = 125,708 of 129,512 rows. The
     ~3,800 left over are the 3,746 permitted 2025-02-01 to 2026-04-30, of
     which **2,879 are open**. A `state=01` pull shows openings stopping dead
     at 2025-01 while closures continue: it looks like a dying register and
     is a filter artefact.
   - **Pull without `state`, and keep `trdstatenm == "영업/정상"` yourself.**
     The full pull also brings the closed rows that Seoul's coordinate-donor
     join borrows points from.
2. **Always pass `opnSvcId`.** An operation's unfiltered answer does not
   carry every type it documents. `LocalDstrb`'s default output is five
   door-to-door and mail-order types, and **대규모점포 (`08_25_01_P`) appears
   only when asked for by id.** Pull each needed type by its id.

### The permit types a build reads

Open = `trdstatenm` 영업/정상, from full pulls (no `state`) on 2026-09-27.
The two restaurant types come from the earlier `state=01` pull plus a pull of
everything permitted since 2025-02-01 (see "Still unknown").

| Operation | `opnSvcId` | Type | Rows | Open | Opened since 2025-02 | Points (open) |
|---|---|---|---|---|---|---|
| LocalRstrn | 07_24_04_P | 일반음식점 | 129,512 | **42,420** | 2,879 | 99.4% |
| LocalRstrn | 07_24_05_P | 휴게음식점 | 37,300 | **11,273** | 1,291 | 98.8% |
| LocalBar | 07_23_01_P | 단란주점영업 | 4,887 | 1,481 | 30 | 99.1% |
| LocalBtyIndst | 05_18_01_P | 미용업 | 31,756 | **13,712** | 1,306 | 99.4% |
| LocalSrvcIndst | 05_19_01_P | 이용업 | 5,248 | 1,130 | 59 | 98.6% |
| LocalLndry | 06_20_01_P | 세탁업 | 4,826 | 1,204 | 22 | 99.2% |
| LocalBths | 11_44_01_P | 목욕장업 | 1,818 | 651 | 7 | 99.5% |
| LocalTobaco | 11_43_02_P | 담배소매업 | 39,552 | **8,916** | 671 | **94.4%** |
| LocalStore | 07_22_03_P | 건강기능식품일반판매업 | 28,545 | 6,263 | 1,408 | 98.8% |
| LocalStore | 07_22_04_P | 축산판매업 | 11,324 | 3,851 | 265 | 97.0% |
| LocalStore | 07_22_18_P | 제과점영업 | 4,069 | 1,186 | 139 | 99.4% |
| LocalStore | 07_22_19_P | 즉석판매제조가공업 | 46,502 | **6,045** | 719 | 99.2% |
| LocalStore | 07_22_13_P | 식품판매업(기타) | 758 | 338 | 6 | 99.4% |
| LocalDstrb | 08_25_01_P | 대규모점포 | 91 | 78 | 2 | 98.7% |

**8,804 of the open premises (9%) were permitted after 2025-01-31**, and a
`state=01` pull would have lost every one of them.

Not read: 유흥주점영업 (`07_23_02_P`, excluded, 2,271 open), 숙박업 and
동물병원 (excluded), and the rest of `LocalDstrb` (통신판매업 etc., mail
order and door-to-door, with **99% of addresses masked**).

### Schema — the API's lowercase codes, not Seoul's column names

| Seoul (CSV) | Busan (API field) |
|---|---|
| `사업장명` | `bplcnm` |
| `영업상태명` | **`trdstatenm`** (keep `영업/정상`) |
| `도로명주소` / `지번주소` | `rdnwhladdr` / `sitewhladdr` |
| `좌표정보(X)`, `(Y)` | `x`, `y` |
| `업태구분명` / `위생업태명` | **`uptaenm`** / **`sntuptaenm`** |
| `관리번호` | `mgtno` (de-duplicate the two pulls on it) |
| `전화번호` (NEVER_READ) | **`sitetel`**: never read, never published |

- 🚨 **The health-food channel is in `sntuptaenm`** (영업장판매, 전자상거래…),
  as Daegu's is in `위생업태명`. `uptaenm` is blank for that type. Seoul's
  rule keyed on the first column would drop every health-food row.
- **Other columns never to read**: `rgtmbdsno` (the rights holder's serial,
  in `LocalStore`), `bdngownsenm` (building tenure), `monam` (rent). **There
  is no 대표자 or 성명 field in any operation.**
- **`uptaenm` for 담배소매업 is blank**, as in Seoul and Daegu.
- 🚨 **Address masking** (Main Build's `korea.py` check raises on it):
  **건강기능식품일반판매업 masks every open row's house number** (6,263 of
  6,263), exactly as Daegu's file does, so declare it in config. Elsewhere
  masking is rare among open rows: 6 restaurants, 4 cafés, 1 bath and 1
  on-site food maker. The unused mail-order types in `LocalDstrb` are 99%
  masked.
- The address regexes need **`부산광역시 (\S+[구군])`**: 기장군 is a 군.

### Sub-types (open) — Seoul's `KINDS` carries over

- **일반음식점**: 한식 17,532 · 기타 6,552 (15.4%; Seoul 17.7%, Daegu 17.0%) ·
  호프/통닭 3,372 · 경양식 2,762 · 식육(숯불구이) 2,710 · 분식 2,420 · 중국식
  1,614 · 횟집 1,376 · 일식 1,164. DROP: 이동조리 18, 출장조리 17.
- **휴게음식점**: 커피숍 4,703 · 기타 휴게음식점 2,326 · 일반조리판매 1,699 ·
  **편의점 1,330 → Retail** · 패스트푸드 423 · 다방 247 · **푸드트럭 167 (DROP)**
  · 아이스크림 116 · 백화점 74 · **과자점 46 → Retail**.
- **미용업**: key on `uptaenm` (일반미용업 8,328 · 피부미용업 2,312 · 네일아트업
  2,175 · 메이크업업 798). **`sntuptaenm` holds combined values** here
  ("피부미용업, 네일미용업", 종합미용업…), so it is the wrong field for a kind.
- **축산판매업**: 식육판매업 (butchers) **2,282** of 3,851; the rest is milk,
  distribution, import, eggs and by-products, which is wholesale.
- **건강기능식품**: 영업장판매 **2,818** kept; 전자상거래 2,613, 방문판매 520 and
  the rest out.
- **대규모점포**: 구분없음 24, 그 밖의 대규모점포 21, 복합쇼핑몰 14, 대형마트 7,
  쇼핑센터 4, 백화점 4, 시장 3, 전문점 1.

### Counts, before de-duplication (Seoul's rules applied)

| Bucket | Permit rows (open) |
|---|---|
| Food service | 일반음식점 42,385 + 휴게음식점 9,730 + 단란주점 1,481 = **53,596** |
| Personal services | 13,712 + 1,130 + 1,204 + 651 = **16,697** |
| Retail | tobacco 8,916 + on-site food makers 6,045 + in-store health-food 2,818 + butchers 2,282 + moved convenience stores and confectioners 1,376 + bakeries 1,186 + other food shops 338 + large stores 78 = **23,039** |

- **Within 966 m of a drawn stop: 71,736 of the 97,260 placed open premises**
  (all fourteen types, before bucket rules), 74%.
- **De-duplication is unmeasured.** Seoul's rule carries over. Expect retail
  to fall the most: a convenience store holds a tobacco and a café permit.

### Coordinates

Points on 94.4% (tobacco) to 99.5%. The full pulls include every closed row,
so Seoul's donor join (another row's point at the same building) has its
donors. It needs the `[구군]` regex, and it cannot key health-food rows,
whose addresses are masked. Its yield is unmeasured.

### Privacy

- No operator field in any operation. `sitetel` is never read; the licence
  read already requires that.
- **`pipeline/korean_names.py` flags 152 open rows**: 미용업 51, 일반음식점 43,
  건강기능식품 32 (mostly e-commerce, already out by the channel rule),
  즉석판매 9, 담배 6, 휴게음식점 3, 이용업 3, 목욕장업 2, 세탁업 1, 단란주점 1,
  제과점 1. Withhold the flagged names, as Seoul does.
- Run `scripts/check_personal_exposure.py busan` at build.

---

## Rail — MEASURED 2026-09-27 (OSM, via `pipeline.osm.fetch`)

The boundary is **relation 2396450** (부산광역시, admin_level 4), resolved by
name. Its polygon is 2,020 km², including territorial water; the land area
is about 770 km².

| Line | OSM `route` | Relations | Stops | In Busan | Mean / max spacing | Colour |
|---|---|---|---|---|---|---|
| 1 (노포–다대포해수욕장) | subway | 2 | 40 | **40** | 0.97 / 1.40 km | #F06A00 |
| 2 (장산–양산) | subway | 2 | 43 | **38** | 0.94 / 1.44 | #81BF48 |
| 3 (수영–대저) | subway | 2 | 17 | **17** | 1.09 / 3.03 | #BB8C00 |
| 4 (미남–안평) | **monorail** | 2 | 14 | **14** | 0.86 / 1.19 | #217DCB |
| 부산김해경전철 (사상–가야대) | light_rail | 2 | 21 | **9** | 1.34 / 2.10 | #8652A1 |
| 동해선 광역전철 (부전–태화강) | train | 2 | 22 | 16 | **2.29** / 5.44 | #0054A6 |

- **Stations drawn (recommended)**: Lines 1–4 give 40 + 38 + 17 + 14 = 109
  stops, less 6 transfer stations (서면 1/2, 연산 1/3, 동래 1/4, 덕천 2/3,
  수영 2/3, 미남 3/4) = **103**. The Busan–Gimhae LRT adds 9 in Busan, 2 of
  them transfers (사상 with Line 2, 대저 with Line 3): **110** in all.
  Confirm the transfer list at build.
- 🚨 **Line 4 is `route=monorail`** (it is a rubber-tyred automated line),
  exactly as Daegu's Line 3. A `subway|light_rail|train` query loses it.
- 🚨 **Never match on `network`**: the Korail-run 동해선 is tagged
  `부산 도시철도` like the city's own lines, and the station nodes mostly carry
  no network. Select by route type and `ref` (`1`–`4`, `BGL`; 동해선's is
  `동해`).
- Line 2 runs 5 stops into Yangsan (양산시), and the LRT 12 stops into Gimhae
  (김해시). Neither city is in Busan's register.
- The rest in the bbox is intercity (경부선 KTX, 경전선, 코레일 services), not
  drawn.
- The projected CRS is **UTM 52N (EPSG:32652)**, as Seoul and Daegu.

---

## Still unknown

- **The restaurant and café counts are within a few dozen.** For 일반음식점,
  states 01 and 03 plus the post-2025 rows account for 129,454 of 129,512.
  The other 58 are rows with no state code permitted before 2025-02; for
  휴게음식점 it is 17. A build's full pull settles them.
- 🚨 **`LocalBtyIndst` fails a permit-date filter** (`bgnYmd`/`endYmd` →
  XML `UNKNOWN_ERROR`, code 999) while answering unfiltered and
  `lastModTs`-filtered queries. **Pull every operation in full.**
- De-duplication counts, and the donor join's yield (both at build).
- 동해선's frequency (only if the owner wants it tested).
- Downloads, in the MAIN checkout's `data/busan/raw/`:
  - the earlier `<Operation>_active.json` pulls (`state=01`, **incomplete by
    construction**: keep only as history);
  - `<Operation>_<opnSvcId>_all.json` (full, for 11 types);
  - `LocalRstrn_07_24_0{4,5}_P_since2025.json` and
    `LocalBar_07_23_01_P_since2025.json`.

  A build's `fetch_sources.py` re-pulls all fourteen in full, one operation
  at a time with backoff, and records row counts and hashes.

```brief-checks
[
  {
    "id": "busan-api-post-2025-restaurants",
    "claim": "The keyless API returns 3,746 일반음식점 rows permitted 2025-02-01..2026-04-30 when NO state filter is given - rows a state=01 pull loses. A changed count means the frozen feed moved: re-measure before building",
    "kind": "http_contains",
    "url": "https://data.busan.go.kr/open/services/LocalDataService/LocalRstrn?pageIndex=1&pageSize=1&resultType=json&opnSvcId=07_24_04_P&bgnYmd=20250201&endYmd=20260430",
    "present": ["\"totalCount\":\"3746\"", "NORMAL_CODE"]
  },
  {
    "id": "busan-api-restaurants-total",
    "claim": "일반음식점 holds 129,512 rows in all states (frozen at 2026-04-15)",
    "kind": "http_contains",
    "url": "https://data.busan.go.kr/open/services/LocalDataService/LocalRstrn?pageIndex=1&pageSize=1&resultType=json&opnSvcId=07_24_04_P",
    "present": ["\"totalCount\":\"129512\""]
  },
  {
    "id": "busan-api-large-stores-by-id",
    "claim": "대규모점포 comes only by asking LocalDstrb for opnSvcId=08_25_01_P (91 rows); the operation's default output is mail-order and door-to-door types",
    "kind": "http_contains",
    "url": "https://data.busan.go.kr/open/services/LocalDataService/LocalDstrb?pageIndex=1&pageSize=1&resultType=json&opnSvcId=08_25_01_P",
    "present": ["\"totalCount\":\"91\"", "대규모점포"]
  },
  {
    "id": "busan-api-salon-date-filter-broken",
    "claim": "LocalBtyIndst answers a permit-date filter with UNKNOWN_ERROR 999, so every operation is pulled in full rather than by date",
    "kind": "http_contains",
    "url": "https://data.busan.go.kr/open/services/LocalDataService/LocalBtyIndst?pageIndex=1&pageSize=1&resultType=json&opnSvcId=05_18_01_P&bgnYmd=20250201&endYmd=20260430",
    "present": ["UNKNOWN_ERROR"]
  },
  {
    "id": "busan-free-use-policy",
    "claim": "Big-데이터웨이브's data-use policy still carries the free-use grant the licence position rests on",
    "kind": "http_contains",
    "url": "https://data.busan.go.kr/bdip/publicDataPolicy.do",
    "present": ["영리 목적의 이용을 포함한 자유로운 활용"]
  },
  {
    "id": "busan-osm-lines",
    "claim": "OSM carries Busan Lines 1-3 as subway (2 relations each), Line 4 as MONORAIL and the Busan-Gimhae LRT as light_rail (ref BGL) - a subway|light_rail|train query loses Line 4",
    "kind": "osm_route_refs",
    "bbox": [34.95, 128.75, 35.45, 129.35],
    "routes": ["subway", "monorail", "light_rail"],
    "expect_relations": {"subway": 6, "monorail": 2, "light_rail": 2},
    "require_refs": {"subway": ["1", "2", "3"], "monorail": ["4"], "light_rail": ["BGL"]}
  },
  {
    "id": "busan-osm-boundary",
    "claim": "OSM relation 2396450 is 부산광역시, resolved by name",
    "kind": "http_contains",
    "url": "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A60%5D%3Brel(2396450)%3Bout%20tags%3B",
    "present": ["부산광역시", "\"admin_level\": \"4\""]
  },
  {
    "id": "busan-projected-crs",
    "claim": "Busan projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 129.07,
    "expect": "EPSG:32652"
  }
]
```
