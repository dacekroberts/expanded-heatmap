# Gyeonggi satellites — build brief

**Screened 2026-09-27; passed to Band B 2026-09-28 (owner), the café file's
gap disclosed. Brief written 2026-09-28.** Run
`python scripts/brief_check.py gyeonggi` before writing any code. The trail:
`DECISIONS.md` 2026-09-28 "Band C's last five get verdicts" (Gyeonggi
satellites: PASS, to B; "which satellites is the brief's question").

> **Measured at the build, 2026-09-29 (build session, branch `gyeonggi`,
> stacked on `incheon`)** - these supersede the business leg and the page
> shape below:
> - 🚨 **The national LOCALDATA source is closed**: its data.go.kr API needs a
>   key, and data.go.kr accounts need a Korean identity check (본인인증). A probe
>   of each city's own files found them unusable: Goyang publishes only a
>   meat-retail list, Yongin no food or retail register, and Seongnam files
>   without coordinates. **Built on SEMAS's 상가(상권)정보 (owner)**, Incheon's
>   source and module, every storefront on its own point.
> - **One page per city (owner)**, and a new **Seoul Capital Area** macro-map
>   region (owner): Seoul, Incheon and the three, whose labels cannot share
>   East Asia's zoom.
> - Goyang **27,808** storefronts, 20 stations (Line 3, Gyeongui-Jungang),
>   66.6% in a ring; Seongnam **25,529**, 18 stations (Line 8, Suin-Bundang,
>   Shinbundang, Gyeonggang), 76.1%; Yongin **23,481**, 24 stations (EverLine,
>   Suin-Bundang, Shinbundang), 55.4%.
> - Takeaway and barbers, the brief's open calls, do not arise: SEMAS files
>   takeaway food under 음식 and barbers under 이용·미용, with the rest.
> - Suwon **33,433** storefronts, 14 stations (Line 1, Suin-Bundang,
>   Shinbundang; the brief's 14 nodes were the whole count), 47.6% in a ring
>   (build session, branch `suwon`, 2026-09-29).
> - Bucheon **22,512** storefronts, 14 stations (Line 1, Line 7 and the
>   Seohae Line, drawn here on its own track, owner), 80.4% in a ring (build
>   session, branch `bucheon`, 2026-09-29).
> - **The next satellites, briefed 2026-09-29 (owner's scope)**: Namyangju,
>   Ansan and Uijeongbu; Hwaseong, Anyang, Gimpo and the smaller 시군 left
>   out with the reason. See "The next satellites" below.

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

## The next satellites — measured 2026-09-29 (staging session)

**Scope (owner, 2026-09-29):** brief Namyangju, Ansan and Uijeongbu;
recount Hwaseong and Anyang and brief them only if the recount lifts them
above seven stations; leave Gimpo and the smaller 시군 out, with the reason.

Measured the built five's way:
- **Stations** from route-relation membership (`osm-rail`), on Seoul's
  precedent (GTX-A never drawn).
- **The areas recount:** every `railway=station` node, way and relation
  inside each OSM boundary, set against the stations route membership found.
- **Storefronts** from SEMAS (edition 2026-06-30), through
  `korea_sbiz.storefronts`.
- **The ring share** at each city's outer ring, to the nearest drawn station.

Scratch data is in `data/_staging_scratch_2026-09-29/briefs/gyeonggi/`.

| City | OSM boundary | Area | Stations | Lines drawn (stations in the city) | Median gap → rings | SEMAS storefronts (food / retail / personal) | In ring | Verdict |
|---|---|---|---|---|---|---|---|---|
| **남양주 Namyangju** | 2409175 | 457 km² | **17** | Gyeongchun 7, Gyeongui–Jungang 6, Line 4 3, Line 8 2 | 2,294 m → standard | **18,344** (8,069 / 7,699 / 2,576) | **54.9%** | **Brief** |
| **안산 Ansan** | 2409159 | 486 km² | **13** | Line 4 8, Suin–Bundang 7, Seohae 5 | 1,417 m → standard | **19,711** (9,263 / 7,494 / 2,954) | **64.3%** | **Brief** |
| **의정부 Uijeongbu** | 2409183 | 82 km² | **20** | U Line 15, Line 1 5, Line 7 1 | 622 m → standard | **13,103** (5,875 / 5,090 / 2,138) | **85.3%** | **Brief** |
| 화성 Hwaseong | 2409173 | 1,073 km² | 3 | Line 1 1, Suin–Bundang 2 | 2,532 m | 25,272 | 5.2% | Out |
| 안양 Anyang | 2409161 | 59 km² | 7 | Line 1 4, Line 4 3 | 1,487 m → standard | 15,177 | 64.2% | Out on the agreed test; ⚠️ owner call below |

- A station on two lines counts on each line in the lines column.
- **The areas recount changed nothing in the four cities with metro
  stations.** Every station object inside Namyangju, Ansan, Uijeongbu and
  Anyang is on a queried route relation, and every station in these cities
  is an OSM node.
- Ansan's 13 by route membership stand against 12 station-object names, and
  the 2026-09-28 floor of 12.
- Names withheld by Seoul's personal-name rule are few: 37, 17, 11, 19 and
  28 in the table's order.

### Namyangju (남양주시)

- **Four lines:**
  - Gyeongchun, 7 stations;
  - Gyeongui–Jungang, 6;
  - Line 4's Jinjeop extension, 3: Byeollae Byeolgaram, Onam and Jinjeop;
  - Line 8's Byeollae extension, 2: Dasan and Byeollae. Byeollae is shared
    with the Gyeongchun Line.
- Seoul draws Gyeongui–Jungang, Line 4 and Line 8. Gyeongchun is a Korail
  metro line in Seoul's precedent.
- **Colours:** Seoul's drawn ones, with Line 8 as Seongnam draws it
  (`#92144E`). Gyeongchun's is OSM's `#007A62`.
- **A sprawling city:** 457 km² and a 2,294 m median gap, so standard rings
  and 54.9% in a ring, level with Yongin's 55.4%.
- **English names:** 11 stop nodes have no `name:en`, but every station
  object inside the city has one, and step 1 takes the station object's name
  first.
- **SEMAS:** 시군구명 prefix `남양주시` (no 구).

### Ansan (안산시)

- **Three lines:**
  - Line 4, 8 stations;
  - Suin–Bundang, 7;
  - Seohae, 5: Wonsi, Siu, Seonbu, Dalmi and Choji.
- Line 4 and Suin–Bundang share six stations: Gojan, Singil Oncheon, Ansan,
  Jungang, Choji and Handae-ap.
- **The Seohae Line is drawn, on Bucheon's precedent** (the owner's call
  there, 2026-09-29).
  It runs on its own track through Wonsi, Siu, Seonbu and Dalmi, and meets
  the other lines only at Choji. That is Bucheon's shape, not Goyang's.
- **Area:** 486 km² takes in Daebudo and the sea around it, which is why the
  median gap is wide. 64.3% of storefronts are in a ring.
- **SEMAS:** prefix `안산시` (상록구, 단원구).

### Uijeongbu (의정부시)

- **Three lines:**
  - the U Line (Uijeongbu LRT, OSM `#F0831E`), 15 stations;
  - Line 1, 5, with Hoeryong shared with the U Line;
  - Line 7, 1: Jangam.
- Line 7's single station is drawn by the satellites' rule (every line with
  a station in the city, to its ends).
- ⚠️ **OSM carries the U Line as three relations.**
  - The main one has ref `U`.
  - The two depot-shuttle relations, `의정부경전철: 발곡 → 차량기지임시승강장`
    and `의정부경전철: 차량기지임시승강장 → 탑석`, have no ref.
  - Place the two in `NOT_DRAWN_BY_NAME`: step 1 never matches a drawn line
    on text, and the relation with the ref already carries the whole line.
- **Rings:** a 622 m median gap, just above the 550 m threshold, so standard
  rings. 85.3% in a ring, the highest of any satellite.
- **SEMAS:** prefix `의정부시`.

### Left out, with the reason

- **Hwaseong:**
  - three drawn stations in 1,073 km², and 5.2% of storefronts in a ring;
  - Dongtan, its centre, is served by GTX-A only, which is not drawn;
  - the other three station objects inside it (서화성, 향남, 화성시청) are
    Korail `station=train` nodes on no metro route relation. By name they
    are the Seohae Line's southern intercity section.
  - The recount lowers it from 7 to 3, so it is out.
- **Anyang:**
  - the recount holds at 7 (Line 1 4, Line 4 3), so it is out on the agreed
    test.
  - ⚠️ **But 64.2% of its 15,177 storefronts are in a ring**, on 59 km².
    That is above Suwon's 47.6% and Yongin's 55.4%, and level with Ansan's.
    The seven-station bar stood in for coverage, and the measured ring share
    says it covers well.
  - **Owner call:** brief it with the three, or leave it out.
- **Gimpo:** the Goldline only, screened as an edge network (2026-09-28).
  Not re-measured.
- **The smaller 시군** (Hanam, Gwangmyeong, Guri, Gwacheon, Uiwang…): under
  8,000 storefronts and five stations each (2026-09-28).

Once the three are built and Anyang is decided, the Band B row closes.

---

## Licence — read 2026-09-29 (`licence-read`): AMBIGUOUS on the portal; clean on the national source

**The datasets are permissive everywhere they are declared:**
- data.gg.go.kr's 14 dataset pages: "상업적이용허용 및 콘텐츠변경허용"
  (commercial use and modification allowed), the portal's own scheme, not
  KOGL.
- data.go.kr's 17 Gyeonggi listings and the Ministry's national listings
  (행정안전부, 15154916, 15096283): "이용허락범위 제한 없음".
- The provincial ordinance (경기도 공공데이터 조례 제4조③) forbids
  restricting even commercial use.

**The portal's own terms of use diverge:**
- 이용약관 제12조⑥: no commercial use of material, "such as processing and
  selling", without Gyeonggi's express approval.
- 제14조②9: no profit-making activity without prior consent.
- On the permissive reading (only commercial use is barred), a
  non-commercial map is outside both clauses. On the restrictive reading
  (가공, processing, is barred by itself), publishing waits on approval.
- The terms' effective date is a blank placeholder ("2026년 00월 00일"),
  apparently from the portal's 2026-05-29 relaunch.

**On the portal, the duties would be:**
- a credit to the author and source (제12조③);
- a statement that the page uses Gyeonggi public data (제12조⑤; no form
  set);
- nothing implying acting for Gyeonggi (제14조②7);
- nothing presented as Gyeonggi's own figures (FAQ #7).

The purpose-of-use question on download is a mandatory survey, not a
condition; answer it honestly.

🟢 **Recommended route: take the build's data from the national source, not
the portal.**
- Most portal files name the Ministry (행정안전부) as provider, sourced from
  공공데이터포털.
- Busan's build already uses the Ministry's national local-licence files
  (`data/busan/raw/Local*_P_all.json`).
- Those declare "제한 없음", so the portal's terms never apply, and one
  source serves Busan and Gyeonggi alike.
- **The national files may also close the café and takeaway gaps.** The
  read found the portal's café metadata listing an address and lat/lon, so
  "no location" may be the portal's export and not the data. To be checked
  on the national file, before the page's gap is written.
- The downloaded portal files stay as a scratch cross-check.
- ~~An owner call~~ **Decided (owner, 2026-09-29): the national files.**

**Never publish** phone numbers (소재지시설전화번호), deposit or rent
(보증액, 월세액), or the rights-holder and livestock identifiers
(권리주체고유번호, 축산고유번호). None of the checked files has an owner-name
column.

**Portal access for checks**: a bare user agent is blocked, and dataset
pages render only with `Accept-Language: ko-KR`.

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

- ~~The source~~ **Decided (owner, 2026-09-29): the Ministry's national
  local-licence files** ("제한 없음", Busan's source). The portal's files
  are a scratch cross-check only, and the portal's terms do not apply.
  **The download needs the owner's OK** (size to state at the build).
- ⚠️ **The café and takeaway gaps on the national files**: they may carry
  a name, location and status that the portal's exports lack.
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
    "id": "gyeonggi-next-north-lines",
    "claim": "Namyangju's and Uijeongbu's drawn lines are in OSM by ref: the U Line (with its two no-ref depot-shuttle relations), Lines 1, 4, 7 and 8, the Gyeongchun and Gyeongui-Jungang Lines (2026-09-29)",
    "kind": "osm_route_refs",
    "bbox": [37.51, 127.00, 37.78, 127.38],
    "routes": ["light_rail", "subway", "train"],
    "require_refs": {"light_rail": ["U", "<no ref>"], "subway": ["1", "4", "7", "8"], "train": ["경춘", "경의·중앙"]}
  },
  {
    "id": "gyeonggi-next-ansan-lines",
    "claim": "Ansan's drawn lines are in OSM by ref: Line 4, the Suin-Bundang and Seohae Lines (2026-09-29)",
    "kind": "osm_route_refs",
    "bbox": [37.25, 126.75, 37.38, 126.94],
    "routes": ["subway", "train"],
    "require_refs": {"subway": ["4"], "train": ["수인·분당", "서해"]}
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
