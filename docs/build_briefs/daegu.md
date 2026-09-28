# Daegu — build brief

**Step 0 completed 2026-09-27** (Staging). Run `python scripts/brief_check.py
daegu` before writing any code. The licence position is already decided (a
disclosed reasoned position, owner 2026-09-27; `docs/data_sources.md`, "Daegu
and Busan"). **Three owner calls are open** (below). None needs a probe; each
is a recommendation waiting for a yes.

⚠️ **Corrected the same evening.** The first version of this brief said
Daegu's publication has no bakeries, delis or other food shops, and
recommended building with a narrower retail bucket. **That was wrong.** The
dataset page shows its files **six per page**, and the three types were on
pages 2–4 of the food-manufacturing group. The check that "confirmed" it read
page 1 only. The full edition is 195 files, and all three are measured below.
See DECISIONS, 2026-09-27, "Daegu's brief corrected".

---

## The one-line summary

**Seoul's register and schema, one month behind.** Fourteen 2026-08 permit
files, all 7 gu and 2 counties, points on 95.9–100% (one file 72%), no
operator column. About **38,900 food premises, 12,500 personal services and
18,700 retail permits** before de-duplication, the same types as Seoul's. Rail
is three OSM lines, **86 stations**, one of them a monorail that Seoul's
query would drop.

---

## Owner calls — open, with recommendations

1. **Buckets as Seoul's** (owner 2026-09-24): 단란주점 → Food service (457);
   유흥주점, lodging and veterinary clinics out; bakeries, on-site food makers
   and other food shops → Retail. Nothing new to decide unless the owner wants
   to revisit.
2. **Rail: draw Lines 1, 2 and 3 only.** 대경선 (Korail's Gumi–Daegu–Gyeongsan
   metropolitan line, opened 2024-12) has 3 stops inside Daegu, a mean
   **4.08 km** apart. The subway's spacing is 0.77–1.07 km. It fails the
   spacing test as Seoul's 공항철도 (3.37 km) did. Its frequency is **not
   measured** (no GTFS); a cited timetable read goes with the decision.
3. **Stations inside Daegu only** (Seoul's and Japan's rule). Line 1's Hayang
   extension leaves 2 stops in Gyeongsan, and Line 2 leaves 3. The lines are
   drawn to their ends and the 5 stops are listed as excluded. Line 2 keeps
   26 of 29, so the stub test does not call for a regional scope.
   - Region: **East Asia** (exists).

---

## Business leg — D-데이터허브's monthly LOCALDATA files

| | |
|---|---|
| Source | `data.daegu.go.kr` (D-데이터허브), "26년08월_인허가데이터", one dataset per GROUP of permit types, each a set of XLSX files. Origin: 한국지역정보개발원 |
| Access | ✅ **No account.** The page's own download button: `GET https://data.daegu.go.kr/cmm/fms/FileDown.do?atchFileId=<FILE_id>&fileSn=0` (`Content-Type: application/x-msdownload`, a zip body). A re-download of the restaurant file was **byte-identical** to the copy cached earlier the same day |
| Edition | **Monthly.** Each month is a NEW set of dataset ids and file ids (July's barbers are DMI_0000119244, August's 119503). Pin the edition in `config.py` |
| 🚨 **Real date** | **The "26년08월" edition holds data only through 2025-08-29** (found by Main Build, 2026-09-27). In 일반음식점, 담배소매업 and 미용업 the newest 인허가일자, 폐업일자, 최종수정시점 and 데이터갱신일자 all end in late August 2025, after steady monthly activity: an extract taken about 2025-09-02, not a register tapering off. **The edition label is the portal's month, not the data's.** Owner's call: build it, and state **"as of 2025-08-31"** on the page. Read the rows' own newest dates for any later edition rather than trusting its label |
| Coverage | all **9 authorities**: the 7 gu, 달성군 and **군위군** (code 5141000, part of Daegu since 2023-07). 중구 is present (2,981 open restaurants), which the 2026-09-22 data.go.kr route lacked |
| CRS | **EPSG:5174**, as Seoul. 66,697 open points land inside OSM's 대구광역시 boundary and **11 outside** |
| Licence | Decided: a disclosed reasoned position; credit and removal line in `docs/data_sources.md` |

### 🚨 Enumerate by id, and the edition is scattered

The 2026-08 edition is **36 group datasets in four id blocks**:
DMI_0000119500–09, 119560–69, 119600–09 and 119690–95. Every id between the
blocks returns a 979-byte "페이지를 찾을 수 없습니다" page under every
`provdMethod`, so they are not hidden datasets. **The record before this brief
named only 119600–09 and 119690–95**, and "barbers, laundries and baths are in
sibling files not yet pulled" was a statement about those two blocks. The
personal-services and bar files are in the other two.

- 🚨 **A dataset page embeds its files SIX AT A TIME.** The page's own
  `search` object says so (`"recordCountPerPage":6,"totalRecordCount":23`
  for the food-manufacturing group). The rest come from the page's own call,
  `POST /data/rest/getDataSetDetailListInfo.do` with that `search` object and
  `currentPageNo` = 2, 3, 4. It answers JSON only with the page's `Origin`
  and `Accept: application/json` headers, and an HTML error page otherwise.
  **Always compare the files listed against `totalRecordCount`.** Reading
  page 1 alone is how this brief first recorded bakeries and delis as absent.
- **The whole edition is 195 files**, the national scheme's full set of permit
  types, across the 36 group datasets.
- The listing page's search **works**: `GET /open/data/dataList.do?searchWrd=`
  gives zzzzqqq → 0 and 인허가 → hits. This is unlike Seoul's inert search. It
  embeds only the first page of results.
- The files are named by the national scheme's group codes,
  `6270000_대구광역시_<aa>_<bb>_<cc>_P_<type>.xlsx`.

### The files a build reads (2026-08; active = `영업/정상`)

| Group dataset | File id | Type | Rows | Active | Points (active) |
|---|---|---|---|---|---|
| 119607 식품_음식점 | 33041 | 일반음식점 | 94,345 | **30,530** | 99.3% |
| 119607 | 33040 | 휴게음식점 | 29,379 | **9,385** | 98.6% |
| 119565 식품_유흥주점,단란주점 | 32961 | 단란주점영업 | 906 | 457 | 99.3% |
| 119690 생활_미용 | 33054 | 미용업 | 23,773 | **10,475** | 99.2% |
| 119503 생활_이용 | 32908 | 이용업 | 3,351 | 848 | 99.4% |
| 119502 생활_세탁소,빨래방 | 32906 | 세탁업 | 3,577 | 993 | 99.8% |
| 119561 생활_목욕탕,찜질방,사우나 | 32951 | 목욕장업 | 835 | 232 | 100% |
| 119695 기타_담배 | 33094 | 담배소매업 | 33,423 | **6,492** | 95.9% |
| 119604 식품_식품 제조,가공,판매 | 33004 | 축산판매업 | 9,910 | 3,471 | 97.0% |
| 119604 | 33013 | 건강기능식품일반판매업 | 19,709 | 4,616 | 98.2% |
| 119604 (page 4) | 33020 | 제과점영업 | 3,781 | 1,020 | 99.1% |
| 119604 (page 4) | 33002 | 즉석판매제조가공업 | 32,455 | 4,631 | 99.5% |
| 119604 (page 3) | 32999 | 식품판매업(기타) | 685 | 308 | 99.4% |
| 119605 생활_유통 | 33024 | 대규모점포 | 232 | 161 | **72.0%** |

File ids are `FILE_0000000000` + the five digits. Also in the edition, **not
read**: 유흥주점영업 (32962, excluded), 숙박업 (32992, excluded), 동물병원
(32943, excluded). They are candidates only as coordinate donors.

### Schema — Seoul's columns under different names (🚨 traps)

The same LOCALDATA fields, but **XLSX rather than cp949 CSV**, and renamed.
Seoul's step 2 selects by exact name, so **every one of these would fail or,
worse, silently read nothing**:

| Seoul | Daegu |
|---|---|
| `좌표정보(X)`, `좌표정보(Y)` | **`좌표정보X(EPSG5174)`, `좌표정보Y(EPSG5174)`** |
| `도로명주소` | **`도로명전체주소`** |
| `지번주소` | **`소재지전체주소`** |
| `전화번호` (NEVER_READ) | **`소재지전화`**: NEVER_READ must name THIS, or the assertion guards a column that is not there |

- 🚨 **The health-food channel is in `위생업태명`, and `업태구분명` is present but
  BLANK** (4,616 of 4,616). Seoul's `read_register` takes `업태구분명` whenever
  the column exists, so the `ONLY` rule (영업장판매) would drop **every**
  health-food row. Fall back per ROW, not per column.
  - Daegu's channels: 영업장판매 **2,366** (kept), 전자상거래(통신판매업) 1,811,
    방문판매 313, others under 40.
  - 🚨 **The health-food file masks every house and unit number with `*`**
    (4,616 of 4,616 open rows; found by Main Build). 98% still carry a point,
    but the address cannot key the donor join or a building de-duplication.
    `pipeline/countries/korea.py` now raises on masking in any file its
    config does not declare.
- **Tobacco**: `업태구분명` is blank, as in Seoul. Its status adds
  `취소/말소/만료/정지/중지` (3,613) and `휴업` (11); keep `영업/정상` only.
- **축산판매업**: 식육판매업 (butchers) **2,416** of 3,471. The rest is milk, egg
  collection, distribution and import, which is wholesale, as in Seoul.
- **대규모점포** adds `점포구분명` (대규모점포 64, **준대규모점포 28**: supermarket
  chains' SSMs, kept as retail). Its `업태구분명` includes `그 밖의 대규모점포` 89
  and `구분없음` 13. Only 72% have a point. 45 have an address and no point, and
  the donor join below is their only route.
- 🚨 **Seoul's address regexes anchor on `서울특별시 (\S+구)`.** Daegu needs
  `대구광역시 (\S+[구군])`, because 달성군 and 군위군 are 군. A `구`-only pattern
  silently gives 3,076 open restaurants in 달성군 no building key.
- **Columns never to read**: `소재지전화` (phone); `권리주체일련번호` (the
  rights holder's serial, in 축산판매업); `건물소유구분명`, `보증액` and `월세액`
  (tenure and rent, not needed). None is an operator name. **There is no
  대표자 or 성명 column in any of the fourteen.**

### Sub-types (active) — Seoul's `KINDS` mostly carries over

- **일반음식점**: 한식 12,491 · 기타 5,182 (17.0%, Seoul 17.7%) · 식육(숯불구이)
  2,863 · 호프/통닭 2,083 · 경양식 1,522 · 분식 1,118 · 중국식 1,118 · 일식 902.
  DROP: 출장조리 39 (no 이동조리 or 푸드트럭 rows).
- **휴게음식점**: 커피숍 3,857 · 기타 휴게음식점 1,980 · **편의점 1,322 → Retail** ·
  일반조리판매 1,140 · 다방 379 · 패스트푸드 359 · **푸드트럭 96 (DROP)** ·
  **과자점 22 → Retail**. New values Seoul's `KINDS` lacks: 고속도로 18 (motorway
  services), 유원지 3, 관광호텔 2.
- **미용업**: 일반미용업 6,928 · 피부미용업 1,581 · 네일아트업 1,278 · 메이크업업 506
  · 기타 182.
- **이용업** 848 · **세탁업** 993 (일반세탁업 956, 운동화전문세탁업 19, 빨래방업 3) ·
  **목욕장업** 232 (공동탕업 195, with 찜질 27).
- **제과점영업**: 1,019, plus **1 푸드트럭 (DROP**: Seoul's `DROP` has no bakery
  entry, so add one). **즉석판매제조가공업** 4,631 and **식품판매업(기타)** 308 each
  carry a single sub-type value.

### Counts, before de-duplication

| Bucket | Permit rows (active) |
|---|---|
| Food service | 일반음식점 30,491 (less catering) + 휴게음식점 7,945 (less food trucks and the moved rows) + 단란주점 457 = **38,893** |
| Personal services | 10,475 + 848 + 993 + 232 = **12,548** |
| Retail | tobacco 6,492 + on-site food makers 4,631 + butchers 2,416 + in-store health-food 2,366 + bakeries 1,019 + other food shops 308 + large stores 161 + moved convenience stores and confectioners 1,344 = **18,737** |

- **Within 966 m of a drawn stop: 51,510 of the 72,623 placed rows** (all
  fourteen files, before bucket rules), 71%.
- **De-duplication is unmeasured.** Seoul's rule carries over (one pin per
  premises; the five convenience-store brands matched by name). Expect retail
  to fall the most, as in Seoul, where 59,816 permits became 53,215 premises.

### Coordinates

Points on 95.9–100% of active rows in ten files, and 72.0% in 대규모점포.
About 950 active rows have an address and no point. **Seoul's donor join
(another row's point at the same building) carries over but is unmeasured
here.** It needs the `[구군]` regex above. At Seoul's rate it would place most
of them.

### Privacy

- No operator column (above). `소재지전화` is never read.
- **`pipeline/korean_names.py` flags 123 open rows** across the fourteen files:
  미용업 63, 일반음식점 23, 건강기능식품 12, 즉석판매제조가공업 7, 세탁업 6, 담배 6,
  휴게음식점 5, 축산 1. The
  health-food rows are mostly e-commerce, already out by the channel rule.
  Withhold the flagged names, as Seoul does.
- Run `scripts/check_personal_exposure.py daegu` at build, as for every city.

---

## Rail — MEASURED 2026-09-27 (OSM, via `pipeline.osm.fetch`)

The boundary is **relation 2395674** (대구광역시, admin_level 4), resolved by
name, at **1,495 km²** (with 군위군).

| Line | OSM `route` | Relations | Stops | In Daegu | Mean / max spacing | Colour |
|---|---|---|---|---|---|---|
| 1 (설화명곡–하양) | subway | 2 | 35 | **33** | 0.92 / 1.57 km | #D93F5C |
| 2 (문양–영남대) | subway | 2 | 29 | **26** | 1.07 / 1.88 | #00AA80 |
| 3 (칠곡경대병원–용지) | **monorail** | 2 | 30 | **30** | 0.77 / 1.04 | #FFB100 |
| 대경선 (구미–경산) | train | 2 | 8 | 3 | **4.08** / 4.92 | #0054A6 |

**86 stations drawn**: 33 + 26 + 30, less the three transfer stations
(반월당 1/2, 명덕 1/3, 신남 2/3). This matches the screen's count.

- 🚨 **Line 3 is `route=monorail`.** Seoul's step 1 query asks for
  `subway|light_rail|train`, which would **lose the whole line** without
  error. `osm-rail`'s meta-rule is that a query that can lose a line must say
  so, so Daegu's must name `monorail`.
- 🚨 **Never match on `network`.** The labels disagree: Lines 1–2 read
  `대구 도시철도`, Line 3 `대구도시철도`, the station nodes `대구권 전철`, and
  대경선 (Korail-run) is tagged `대구 도시철도` too. Select by route type and
  `ref` (`1`, `2`, `3`). 대경선's ref is `대경`.
- The rest in the bbox is intercity: 경부선 KTX and 코레일 services, not drawn.
- The operator's colours match OSM's (red, green, yellow).
- The projected CRS is **UTM 52N (EPSG:32652)**, as Seoul.

---

## Still unknown

- De-duplication counts, and the donor join's yield (both measured at build).
- 대경선's frequency (only if the owner wants it tested rather than excluded on
  spacing).
- Downloads: the fourteen 2026-08 files are cached in the MAIN checkout's
  `data/daegu/raw/` as `dg_<type>_202608.xlsx` (ilban, hyuge, danran, miyong,
  iyong, setak, mogyok, dambae, chuksan, geongi, daegyumo, jegwa, jeuksuk,
  sikpum). A build's
  `fetch_sources.py` downloads them itself by file id and records sizes and
  hashes.

```brief-checks
[
  {
    "id": "daegu-portal-live",
    "claim": "D-데이터허브 answers without an account",
    "kind": "http_ok",
    "url": "https://data.daegu.go.kr/main.do",
    "min_bytes": 10000
  },
  {
    "id": "daegu-food-dataset",
    "claim": "DMI_0000119607 is the 2026-08 restaurant group and carries 일반음식점 as FILE_000000000033041 and 휴게음식점 as FILE_000000000033040 - and no 제과점영업",
    "kind": "http_contains",
    "url": "https://data.daegu.go.kr/open/data/dataView.do?dataSetId=DMI_0000119607&provdMethod=FILE",
    "present": ["26년08월_6270000_대구광역시_07_24_04_P_일반음식점", "FILE_000000000033041", "FILE_000000000033040"],
    "absent": ["제과점영업"]
  },
  {
    "id": "daegu-food-manufacturing-pages",
    "claim": "The 2026-08 food manufacturing/sales group holds 23 files but its page embeds only 6 (butchers and health-food among them); bakeries, on-site food makers and other food shops are on later pages of the detail list. An earlier version of this check asserted them ABSENT from page 1 and passed - a check that could not see past page 1",
    "kind": "http_contains",
    "url": "https://data.daegu.go.kr/open/data/dataView.do?dataSetId=DMI_0000119604&provdMethod=FILE",
    "present": ["\"recordCountPerPage\":6,\"totalRecordCount\":23", "FILE_000000000033004", "FILE_000000000033013"]
  },
  {
    "id": "daegu-bakery-file",
    "claim": "제과점영업 is FILE_000000000033020 (page 4 of DMI_0000119604), served keylessly (1,022,615 bytes on 2026-09-27)",
    "kind": "http_ok",
    "url": "https://data.daegu.go.kr/cmm/fms/FileDown.do?atchFileId=FILE_000000000033020&fileSn=0",
    "min_bytes": 900000,
    "content_type_contains": "msdownload"
  },
  {
    "id": "daegu-barbers-in-the-119500-block",
    "claim": "The 2026-08 edition is scattered: barbers are DMI_0000119503 (FILE_000000000032908), outside the 119600-09/119690-95 blocks first recorded",
    "kind": "http_contains",
    "url": "https://data.daegu.go.kr/open/data/dataView.do?dataSetId=DMI_0000119503&provdMethod=FILE",
    "present": ["26년08월", "05_19_01_P_이용업", "FILE_000000000032908"]
  },
  {
    "id": "daegu-baths",
    "claim": "Public baths are DMI_0000119561, FILE_000000000032951",
    "kind": "http_contains",
    "url": "https://data.daegu.go.kr/open/data/dataView.do?dataSetId=DMI_0000119561&provdMethod=FILE",
    "present": ["26년08월", "11_44_01_P_목욕장업", "FILE_000000000032951"]
  },
  {
    "id": "daegu-download-route",
    "claim": "The page's own download route serves a file keylessly by atchFileId (대규모점포, 50,041 bytes on 2026-09-27)",
    "kind": "http_ok",
    "url": "https://data.daegu.go.kr/cmm/fms/FileDown.do?atchFileId=FILE_000000000033024&fileSn=0",
    "min_bytes": 40000,
    "content_type_contains": "msdownload"
  },
  {
    "id": "daegu-free-use-policy",
    "claim": "D-데이터허브's data-use policy still repeats the national free-use guarantee the licence position rests on",
    "kind": "http_contains",
    "url": "https://data.daegu.go.kr/open/introduce/openData.do",
    "present": ["영리 목적의 이용을 포함한 자유로운 활용"]
  },
  {
    "id": "daegu-osm-lines",
    "claim": "OSM carries Daegu Lines 1 and 2 as subway (2 relations each) and Line 3 as MONORAIL (2 relations) - a subway|light_rail|train query loses Line 3",
    "kind": "osm_route_refs",
    "bbox": [35.55, 128.35, 36.35, 128.85],
    "routes": ["subway", "monorail"],
    "expect_relations": {"subway": 4, "monorail": 2},
    "require_refs": {"subway": ["1", "2"], "monorail": ["3"]}
  },
  {
    "id": "daegu-osm-boundary",
    "claim": "OSM relation 2395674 is 대구광역시, resolved by name (1,495 km2 with 군위군)",
    "kind": "http_contains",
    "url": "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A60%5D%3Brel(2395674)%3Bout%20tags%3B",
    "present": ["대구광역시", "\"admin_level\": \"4\""]
  },
  {
    "id": "daegu-projected-crs",
    "claim": "Daegu projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 128.60,
    "expect": "EPSG:32652"
  }
]
```
