# Incheon — build brief

**Screened 2026-09-27; passed to Band B 2026-09-28 (owner), all three
buckets with a measured placement gap, disclosed. Brief written 2026-09-28.**
Run `python scripts/brief_check.py incheon` before writing any code. The
trail: `DECISIONS.md` 2026-09-28 "Band C's last five get verdicts"
(Incheon: PASS, to B) and "Four small probes… Incheon's coordinates need an
application" (2026-09-27). **Order (owner, 2026-09-28): built after
Bucharest**, whose page drafts the wording for a disclosed placement gap
that Incheon then reuses.

⚠️ **Korean city: read `cjk-text`, and Seoul's, Daegu's and Busan's briefs
first** (`pipeline/korean_names.py`, the rail precedent below).

> **Measured at the build, 2026-09-29 (build session, branch `incheon`)** -
> these supersede the business leg below:
> - 🚨 **Built on SEMAS's 상가(상권)정보 instead (owner, 2026-09-29).** The
>   brief's route was built through step 2 first: 48,736 active permit rows,
>   **33,092 placed (73.4%)** through KESA (exact 20,152, interpolated 11,453,
>   same main number 1,487). But the salons-and-baths list (15061611, 9,493)
>   carries **lot-number addresses only** - KESA and OSM are road-name only,
>   and juso.go.kr needs a Korean identity check - so Personal services could
>   not be placed at all. The national LOCALDATA API needs a data.go.kr key,
>   and **data.go.kr accounts are for Korean nationals or Korean-registered
>   companies, with 본인인증** (sign-up page read 2026-09-29).
> - **SEMAS** (data.go.kr 15083033, keyless ZIP, 352.7 MB, edition
>   2026-06-30): Incheon's 136,995 rows -> **82,671 storefronts** (Food
>   service 39,298, Retail 31,424, Personal services 11,949), **100% on the
>   register's own point**, already on the 2026-07-01 districts (서해구, 검단구,
>   제물포구, 영종구). 107 names withheld. Licence: permitted with conditions,
>   SEMAS's website copyright policy read as the homepage's (owner).
> - **Rail**, as recommended: 79 stations inside Incheon, 151 outside; gate 3
>   exact on Incheon Line 1 (33), Line 2 (27), Line 7 (53) and the
>   Suin-Bundang Line (63); Line 1 not gated whole (its southern branches never
>   touch the box). The Wolmi Sea Train is placed by name as not drawn.
> - **68.3% of storefronts within a ring.**

---

## The one-line summary

**Citywide active-only permit lists, keyless, with addresses but no
coordinates, placed by joining to a national lift-building file and
interpolating along the road: 71.3% of restaurants placed, the rest
disclosed. The work is the join, two privacy filters, and Seoul's rail
precedent.**

---

## Business leg — Incheon's permit files on data.go.kr

Downloaded 2026-09-27 (keyless) into `data/incheon/raw/`. All CP949:

| data.go.kr id | Contents | Rows (screen) | Columns |
|---|---|---|---|
| **15048906** | 일반음식점, restaurants | **33,256** | `인허가관할기관`, `업소명`, `업종`, `업태`, `업소주소`, `영업상태` |
| **15048905** | 휴게음식점, cafés and rest-food | **10,156** | as above |
| **15061611** | 목욕탕 etc., baths, salons and other public-hygiene premises | **9,493** | `구분`, `상호명`, `주소` |
| **15120709** | 건강기능식품 판매업, health-food sellers (the only retail) | **7,467** | `업소명`, `업종`, `업태`, **`업자명`**, `지번주소`, `도로명주소` |
| 15045294 | 대규모점포, large stores (Homeplus etc.) | small | `법인명`, `상호`, `업태`, `소재지`, areas |
| 15064869, 15065162 | per-district counts only | - | not premises |

- **Active only**: the lists carry `영업상태` = 정상 (trading), a 2026-01
  snapshot.
- **Retail is thin**: health-food sellers plus large stores. Treat the page
  as "Retail thin" (the summary-table value Berlin introduced).
- 🚨 **Two privacy filters, both before step 2 writes anything:**
  1. **Drop `업자명`** (the operator's personal name) from 15120709 on
     read. It must never reach `processed/`.
  2. **Health-food sellers at apartment-unit addresses** (a `동` and `호`
     in the address, e.g. "…아파트 102동 1203호") are home businesses.
     Leave them out. Measure the share at the build and record it.

---

## Placement — the lift-building join (measured 2026-09-28)

**No keyless coordinate route exists.** juso.go.kr's coordinate file
(위치정보요약DB) needs a Korean identity check; V-World is geo-blocked; the
parcel two-hop has no keyless file. The route found:

| | |
|---|---|
| **Source** | Korea Elevator Safety Agency (KESA) lift-building coordinates, data.go.kr **15156424**, keyless CSV |
| **File** | `data/incheon/raw/kesa_15156424_elevator_buildings.csv` (36.4 MB, downloaded on the owner's OK; UTF-8 with BOM, unlike the permit files) |
| **Incheon buildings** | **17,235**, each a road-name address + WGS84 |
| **Key** | district + road name + building number |

| Tier | Restaurants placed |
|---|---|
| Exact match | **41.0%** |
| Interpolated along the road between the two nearest listed buildings (the owner's ground-floor workaround) | **+30.3%** |
| **Placed** | **71.3%** |
| Extrapolated (beyond the last listed building) | 11.4%, median error 74 m, p90 526 m: **dropped** |
| Unplaced, disclosed | about 16% |

Leave-one-out on 2,000 listed buildings: median error **15 m** between
same-side neighbours, 52 m either side. Step 2 writes each row's tier.
The join and interpolation scripts are kept in
`data/_staging_scratch_2026-09-28b/`: a start, not a module.

⚠️ **On any refresh**: Incheon's districts were reorganised on 2026-07-01
(중구/동구 → 제물포구/영종구; 서구 split, 검단구: general knowledge, check it). The permit files are a
2026-01 snapshot; a newer one needs a 법정동 mapping before the district
key works.

---

## Licence

### Incheon's permit lists — read 2026-09-28 (`licence-read`): PERMITTED WITH CONDITIONS

- **All five datasets declare `이용허락범위 제한 없음`** ("no restriction on
  use") on the page and in DCAT (`dct:rights`). None carries a KOGL type,
  and none says 변경금지 (no derivatives) or 상업적 이용금지 (no commercial
  use).
- **What makes it a grant:**
  - Incheon's own data-portal policy: 제한 없음 means "자유로운 이용이
    가능" (free use is possible), including for profit.
  - Public Data Act 제3조④: public bodies may not forbid or restrict reuse
    outside the Article 28 cases.
  - data.go.kr's guide: "제약없이 활용" (use without constraint).
- **Must display:** a credit to 인천광역시 (Incheon Metropolitan City) with
  the source. No wording is prescribed. Incheon's portal terms (제10조③)
  ask for the phrase "인천데이터포털 공공데이터", so including it is the
  conservative course. The read's draft: "Source: Incheon Metropolitan City
  (인천광역시), business permit data via 공공데이터포털 (data.go.kr; 인천데이터포털
  공공데이터), 이용허락범위 제한 없음", with the snapshot dates, linked.
- **Must not:** imply acting for the City (portal terms 제9조②); publish
  personal information (개인정보보호법 제19조, through data.go.kr's terms).
  Dropping `업자명` on read satisfies this. **Discrepancy:** 15120709's page
  says owner names are not disclosed, yet the file carries `업자명`. Record
  that in the source row.
- **Must do:** nothing.
- 🟡 **An owner call, Daegu's shape:** the City **website's** terms (제15조,
  제18조: no copying or redistribution of information obtained through "the
  service") and its copyright policy (consult before using material without
  a KOGL mark) were read as covering www.incheon.go.kr, not these datasets.
  - That reading is stronger than Daegu's, because all five pages declare
    제한 없음 and the City's data portal says that means free use.
  - Consultation stays available: 콘텐츠산업과 (the content-industry
    division), 032-440-5692.
  - **The owner decides whether to accept the read's reading.**
- ⚠️ **Freshness:** 15061611 (salons and baths) is a one-off from
  **2021-11-08**, and 15045294 (large stores) one from 2022-08-06. Neither
  is maintained. Restaurants, cafés (2026-01-15) and health-food (2026-08-18)
  are yearly. **Personal services would be five years old: an owner call**,
  either disclosed on the page or the bucket shown thin.

### KESA lift-building file — read 2026-09-28 (`licence-read`): PERMITTED WITH CONDITIONS

- **The dataset declares `이용허락범위 제한 없음`** (no restriction) on the
  page and in DCAT, with no KOGL type. It was registered and last modified
  2025-12-12, as a **one-off (1회성)**: it may never be refreshed. It has
  357,392 rows, with columns 건물명, 건물주소, 경도, 위도.
- **Conditions** (Public Data Act 제3조⑤; data.go.kr FAQ 186): good faith,
  and no falsifying or distorting the factual content. For this project,
  **a pin placed by the join is the project's derivation and must not be
  presented as KESA's record.** The page's placement sentence says so.
- **Must display:** nothing is prescribed. The read's suggested credit:
  "건물 좌표: 한국승강기안전공단, 「승강기 설치 건물 좌표 목록」 (2025-12-12),
  공공데이터포털 [link], 이용허락범위 제한 없음" (Building coordinates: Korea
  Elevator Safety Agency, lift-installed building coordinates, via
  data.go.kr). A support-source row goes in `docs/data_sources/south-korea.md`.
- **Must do:** nothing.
- **`건물명` is never published.** The layer supplies coordinates only, and
  a single-owner building's name can be a person's name.
- 🟡 **An owner call, Daegu's shape again:** KESA's website copyright policy
  bars unauthorised copying of "the homepage's contents" and asks for prior
  consultation on material without a KOGL mark. The read judged it covers
  the website, not this file:
  - it is written about web pages;
  - its wording is a request;
  - the dataset page never links to it;
  - KOGL is attached only to data containing copyright works, and a file of
    building names, addresses and coordinates contains none.

  Consultation is by phone only (문화홍보실, the culture and PR office,
  055-751-0862). **The same owner decision as the City website's terms
  above**, and one answer can cover both.

---

## Rail — OpenStreetMap, measured 2026-09-28

**97 stations in Incheon** (railway=station inside KR-28, by operator):
Incheon Transit 64, Korail 21, AREX 8, airport facility (maglev) 8.

Route relations in bbox 37.35,126.55,37.62,126.80:

| Ref | Mode | Network | Colour |
|---|---|---|---|
| **인천1** (Incheon Line 1) | subway | 수도권 전철 | `#B4C7E7` |
| **I2** (Incheon Line 2) | light_rail | 수도권 전철;인천도시철도 | `#F4A462` |
| **1** (Line 1, Korail) | subway | 수도권 전철 | `#004A85` |
| **7** (Line 7, Bupyeong extension) | subway | 수도권 전철 | `#6E7E31` |
| 4, 9, 김포 골드라인 | | | touch the bbox edge, outside Incheon |
| monorail, no ref | | | probably the Wolmi Sea Train, a tourist ride: out |

**The recommendation, Seoul's precedent** (`docs/build_briefs/seoul.md`):
Incheon Lines 1 and 2, Line 1 and Line 7, and **수인·분당** (Suin–Bundang, a
Korail metro line tagged `train`, drawn in Seoul). **AREX is left out**, as
in Seoul (all-stop spacing 3.37 km), and the airport maglev is suspended (general knowledge; its 8 station nodes remain in OSM).
Cut at the city boundary; Yeongjong Island without AREX has no drawn rail.

---

## Scope, CRS, region

- **Scope:** Incheon Metropolitan City (KR-28). Ganghwa and Ongjin counties
  are in the files; with no rail, they add nothing to the rings but can be
  kept (the page counts within rings).
- **CRS:** UTM 52N (EPSG:32652), as Seoul.
- **Region:** `"region": "East Asia"`.

## Still unknown

- ~~The licence reads~~ done: both permitted with conditions. **Decided
  (owner, 2026-09-28): the City's and KESA's website copyright terms do not
  reach the data.go.kr files.** No consultation is needed before
  publishing, and the removal rule applies if either body objects.
- **Decided (owner, 2026-09-28): personal services are shown from the
  2021-11-08 list, with its date on the page**, not marked thin.
- ⚠️ **The rail call**: the recommendation above (owner).
- ⚠️ **Cafés' and salons' placement rates**: 71.3% was measured on
  restaurants; the other lists use the same join and need their own figure.
- ⚠️ **The apartment-unit share** of health-food sellers.
- ⚠️ **Personal exposure**: `check_personal_exposure.py incheon` after
  step 2.

```brief-checks
[
  {
    "id": "incheon-osm-metro-refs",
    "claim": "OSM carries Incheon Line 1 (ref 인천1), Line 2 (I2, light_rail), and Seoul Metropolitan Subway lines 1 and 7 in Incheon's bbox",
    "kind": "osm_route_refs",
    "bbox": [37.35, 126.55, 37.62, 126.80],
    "routes": ["subway", "light_rail"],
    "require_refs": {"subway": ["인천1", "1", "7"], "light_rail": ["I2"]}
  },
  {
    "id": "incheon-kesa-dataset-page",
    "claim": "The KESA lift-building file that places Incheon's businesses is still published on data.go.kr (15156424)",
    "kind": "http_ok",
    "url": "https://www.data.go.kr/data/15156424/fileData.do",
    "min_bytes": 1000
  },
  {
    "id": "incheon-restaurants-dataset-page",
    "claim": "Incheon's restaurant permit list is still published on data.go.kr (15048906)",
    "kind": "http_ok",
    "url": "https://www.data.go.kr/data/15048906/fileData.do",
    "min_bytes": 1000
  },
  {
    "id": "incheon-projected-crs",
    "claim": "Incheon's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 126.7052,
    "expect": "EPSG:32652"
  }
]
```
