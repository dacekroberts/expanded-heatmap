# Gyeonggi satellites — build brief

**Screened 2026-09-27; passed to Band B 2026-09-28 (owner), the café file's
gap disclosed. Brief written 2026-09-28.** Run
`python scripts/brief_check.py gyeonggi` before writing any code. The trail:
`DECISIONS.md` 2026-09-28 "Band C's last five get verdicts" (Gyeonggi
satellites: PASS, to B; "which satellites is the brief's question").

⚠️ **Korean cities: read `cjk-text`, and Seoul's, Daegu's and Busan's briefs
first.** The satellites sit around Seoul (built) and share its lines, so
Seoul's rail precedent applies (below).

---

## The one-line summary

**One province portal covers all 31 cities and counties with 14 permit
types, most with coordinates and a trading status. Two food files have no
status (cafés, takeaway), and the café file has no location either. The
brief's question is which satellites to build: the recommendation is
Goyang, Seongnam and Yongin first.**

---

## Business leg — 경기데이터드림 (data.gg.go.kr), 14 province-wide files

Downloaded 2026-09-27 into `data/gyeonggi/raw/` (CP949 unless noted).
Counted 2026-09-28 by streaming each file, never whole:

| File | Bucket | Rows | Active | Coordinates (active) | Status column |
|---|---|---|---|---|---|
| `ilban`, 일반음식점 restaurants | food | 487,690 | **145,909** | 96.3% | 영업/정상 · 폐업 |
| `hyuge`, 휴게음식점 cafés | food | 144,047 | ⚠️ unknown | **0%** | **none** |
| `jeuksuk`, 즉석판매제조가공 takeaway food | food | 198,994 | ⚠️ unknown | **0%** | **none** |
| `jegwa`, 제과점 bakeries | food | 15,470 | 4,469 | 99.4% | yes |
| `miyong`, 미용업 beauty | personal | 102,456 | **46,577** | 96.1% | yes |
| `iyong`, 이용업 barbers | personal | 12,087 | ⚠️ unknown | 89.9% | **none** |
| `setak`, 세탁업 laundry | personal | 13,769 | 4,066 | 99.1% | yes |
| `mogyok`, 목욕장업 baths | personal | 2,672 | 777 | 96.4% | yes |
| `dambae`, 담배소매업 tobacco retail (convenience stores) | retail | 139,336 | **26,830** | 92.2% | yes |
| `geongang`, 건강기능식품 health-food | retail | 113,198 | **35,963** | 94.6% | yes |
| `chuksan`, 축산물판매업 meat retail | retail | 49,347 | 17,779 | 98.5% | yes |
| `daegyumo`, 대규모점포 large stores | retail | 839 | 514 | 89.1% | yes |
| `sikpum_gita`, other food retail | retail | 3,512 | 1,494 | 95.3% | yes |
| `danran`, 단란주점 karaoke bars | out | 5,762 | 1,871 | 98.0% | yes |

### ⚠️ The three files without a status

- **Cafés (`hyuge`)**: no name, location or status (the screen's finding,
  disclosed at the pass). Unplaceable as it stands: **cafés are the page's
  gap.**
- **Takeaway food (`jeuksuk`)**: no status and no coordinates, so open and
  closed cannot be told apart. The recommendation is to leave it out and
  disclose it. Including 199k rows of unknown status would swamp the food
  layer.
- **Barbers (`iyong`)**: no status, but 89.9% have coordinates. The
  recommendation is to leave them out with the others (unknown closures),
  or to include only those with a recent permit date: a build call,
  measured then.

### Other traps

- **Coordinates come in two forms**: `위도`/`경도` (WGS84) on some files,
  `X좌표값`/`Y좌표값` (a Korean TM, likely EPSG:5174 or 2097, to verify) or
  `정제WGS84위도`/`경도` on others. Read each file's header; never assume.
- **Tobacco retail (`dambae`)** is the convenience-store proxy (Seoul's
  precedent, to confirm in `pipeline/taxonomies/`). Health-food sellers carry
  home addresses, so apply Incheon's apartment-unit filter.
- **Karaoke bars (`danran`)** are out, as adult entertainment, unless
  Seoul's taxonomy says otherwise.
- **The download page asks a "purpose of use" question.** Answer it honestly
  at the build (owner).

---

## Which satellites — measured 2026-09-28

Active storefronts with a status and an address, from the files above (cafés,
takeaway and barbers excluded), and OSM station nodes per 시군 (inside
KR-41, admin_level 6; **nodes only, a floor**: stations mapped as areas are
missed):

| 시군 | Storefronts | Food | Retail | Personal | Stations (OSM nodes) | Networks |
|---|---|---|---|---|---|---|
| **고양 Goyang** | **34,211** | 22,226 | 7,106 | 4,879 | **22** | Line 3, 경의·중앙, GTX-A |
| **수원 Suwon** | 30,399 | 18,541 | 5,451 | 6,407 | 14 | Line 1, 수인·분당 |
| **성남 Seongnam** | **27,528** | 17,697 | 5,301 | 4,530 | **18** | Line 8, 수인·분당, 신분당 |
| **용인 Yongin** | **26,738** | 16,995 | 6,135 | 3,608 | **24** | EverLine, 수인·분당, 신분당 |
| 부천 Bucheon | 21,424 | 12,886 | 3,703 | 4,835 | 13 | Line 1, Line 7, 서해 |
| 화성 Hwaseong | 19,499 | 11,693 | 5,633 | 2,173 | 7 | |
| 남양주 Namyangju | 17,756 | 9,138 | 5,541 | 3,077 | 17 | 경의·중앙, 경춘, Line 4 |
| 안산 Ansan | 15,743 | 8,749 | 3,278 | 3,716 | 12 | Line 4, 수인·분당, 서해 |
| 안양 Anyang | 14,815 | 8,767 | 3,048 | 3,000 | 7 | Line 1, Line 4 |
| 의정부 Uijeongbu | 12,438 | 7,317 | 2,584 | 2,537 | 20 | Line 1, U Line |
| 김포 Gimpo | 11,453 | 6,161 | 3,344 | 1,948 | 9 | Gimpo Goldline |

Network names are general knowledge beside the OSM operator counts, to be
confirmed per city at the build. Smaller 시군 (Hanam, Gwangmyeong, Guri,
Gwacheon, Uiwang…) are under 8,000 storefronts and five stations each.

**Decided (owner, 2026-09-28), as recommended: Goyang, Seongnam and Yongin
first, then Suwon and Bucheon.** Each is in the top
four on both measures. **Suwon and Bucheon next**: Suwon's 14 stations
look low for its network and need a recount including station areas.
Uijeongbu has many stations but half the storefronts, and Gimpo's single
light line was screened as EDGE.

**Page shape: an owner call.** Either one page per city, or one page
covering several satellites, as Tokyo's page covers its wards. The
recommendation is a page per city, since each has its own centre and
network.

---

## Licence

_(The read of 경기데이터드림's terms is running 2026-09-28; filled in when it
reports.)_

---

## Rail — Seoul's precedent

`docs/build_briefs/seoul.md`: lines 1-9, 신분당, 우이신설 and 신림, plus
the Korail metro lines 경의·중앙, 수인·분당 and 경춘, are drawn. GTX-A,
AREX and intercity services are left out. The same rule applies here, with
each satellite's local line added (EverLine, U Line, Goldline) and cut at
the city boundary.

## Scope, CRS, region

- **Scope:** each chosen 시 by its OSM boundary (admin_level 6 in KR-41).
- **CRS:** UTM 52N (EPSG:32652).
- **Region:** `"region": "East Asia"`.

## Still unknown

- ⚠️ **The licence read** of the portal.
- ⚠️ **The satellites and the page shape** (owner).
- ⚠️ **Takeaway and barbers**: out, or partly in by permit date.
- ⚠️ **The TM projection** of the X/Y files.
- ⚠️ **Station areas**: recount with ways, Suwon first.

```brief-checks
[
  {
    "id": "gyeonggi-portal-up",
    "claim": "Gyeonggi's open-data portal, the source of all 14 permit files, still answers",
    "kind": "http_ok",
    "url": "https://data.gg.go.kr/",
    "min_bytes": 1000
  },
  {
    "id": "gyeonggi-osm-local-lines",
    "claim": "OSM carries the satellites' light metros as light_rail route relations in the province's bbox (7 refs on 2026-09-28), including Gimpo's Goldline; EverLine's and U Line's refs are to be pinned at the build",
    "kind": "osm_route_refs",
    "bbox": [37.10, 126.60, 37.80, 127.30],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["김포 골드라인"]}
  },
  {
    "id": "gyeonggi-projected-crs",
    "claim": "Gyeonggi's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 127.0286,
    "expect": "EPSG:32652"
  }
]
```
