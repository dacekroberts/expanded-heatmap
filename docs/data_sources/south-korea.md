# Data sources — South Korea

Part of [`data_sources.md`](../data_sources.md), the project's provenance
record, which was split by country on 2026-09-27. This file holds the
South Korea rows of the tables there and the source sections about its cities,
moved verbatim under the same headings. The numbered notices this project must
display, the removal-request commitment and the deploy gate are in the entry
point, not here.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Seoul | **Seventeen citywide permit registers** (인허가 정보, Seoul Metropolitan Government, via Seoul Open Data Plaza, daily; the national LOCALDATA records): 일반음식점, 휴게음식점, 단란주점영업, 미용업, 이용업, 세탁업, 목욕장업, 제과점영업, 즉석판매제조가공업, 식품판매업(기타), 축산판매업, 담배소매업, 대규모점포, 건강기능식품일반판매업; 숙박업 and 동물병원 lend building points only; 유흥주점영업 read and excluded (owner) | Food service **148,256**, Retail **51,663** (11,401 convenience stores), Personal services **39,491**: **239,410** storefronts, one per premises; 4,875 open permits with no point at their building left off; 138 names withheld (a personal name at a home-looking address) | `https://datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do` (POST `infId=<OA id>`, `srvType=S`, `serviceKind=1`, `gridTotalCnt=999999`, `ssUserId=SAMPLE_VIEW`, the page's anonymous identity); dataset pages `https://data.seoul.go.kr/dataList/{oa}/S/1/datasetView.do` (OA ids in `pipeline/seoul/config.py`) | none server-side; `영업/정상` and the taxonomy's sub-type rules in step 2; columns read by exact name - never `전화번호` (asserted) | 2026-09-25 |
| Daegu | **Fourteen permit registers** (인허가데이터, Daegu Metropolitan City's D-데이터허브, origin 한국지역정보개발원; the national LOCALDATA records, monthly edition **2026-08, whose rows end 2025-08-31** - the newest 인허가일자, 폐업일자, 최종수정시점 and 데이터갱신일자 in every file): 일반음식점, 휴게음식점, 단란주점영업, 미용업, 이용업, 세탁업, 목욕장업, 제과점영업, 즉석판매제조가공업, 식품판매업(기타), 축산판매업, 담배소매업, 대규모점포, 건강기능식품일반판매업 | Food service **38,468**, Retail **16,269** (2,194 convenience stores), Personal services **12,475**: **67,212** storefronts, one per premises; 612 open permits with no point at their building left off; 113 names withheld (a personal name at a home-looking address) | `https://data.daegu.go.kr/cmm/fms/FileDown.do?atchFileId={file_id}&fileSn=0` (the page's own download button, keyless; XLSX); dataset pages `https://data.daegu.go.kr/open/data/dataView.do?dataSetId={dataset}&provdMethod=FILE` (ids in `pipeline/daegu/config.py`; each month is a new set) | none server-side; `영업/정상` and the taxonomy's sub-type rules in step 2 through `pipeline/countries/korea.py`; columns resolved by name - never `소재지전화` (asserted). The health-food file's addresses are masked with * by the publisher (every row); its points are used as published | 2026-09-27 |
| Busan | **Fourteen permit types** (the national LOCALDATA records through Busan Metropolitan City's keyless `LocalDataService` Open API on Big-데이터웨이브; **frozen at 2026-04-15**, and the rows agree - permits every month to 2026-04): 일반음식점, 휴게음식점, 단란주점영업, 미용업, 이용업, 세탁업, 목욕장업, 제과점영업, 즉석판매제조가공업, 식품판매업(기타), 축산판매업, 담배소매업, 대규모점포, 건강기능식품일반판매업 | Food service **53,152**, Retail **20,140** (2,910 convenience stores), Personal services **16,506**: **89,798** storefronts, one per premises; 810 open permits with no point at their building left off; 114 names withheld (a personal name at a home-looking address) | `https://data.busan.go.kr/open/services/LocalDataService/{op}` (GET `pageSize=1000`, `resultType=json`, `opnSvcId=<id>`; operations and ids in `pipeline/busan/config.py`) | **`state` never sent** (it drops every permit since 2025-02) and **`opnSvcId` always sent** (대규모점포 only by id); every type pulled in full; `영업/정상` and the taxonomy's sub-type rules in step 2 through `pipeline/countries/korea.py`; fields resolved by name - never `sitetel` (asserted). The health-food register's addresses are masked by the publisher | 2026-09-27 |
| Incheon | **SEMAS's 상가(상권)정보** (소상공인시장진흥공단, the Small Enterprise and Market Service's commercial-district register): a national quarterly file of trading storefronts, each with a WGS84 point, classified by SEMAS's own 대/중/소분류 | All three buckets via `pipeline/taxonomies/korea_sbiz.py` (keyed at 소분류, the owner's calls 2026-09-29), read through `pipeline/countries/korea_sbiz.py`. Incheon's 136,995 rows -> **82,671 storefronts** (Food service 39,298, Retail 31,424, Personal services 11,949), 100% placed on the register's own point; 107 personal names at a residential address withheld | `https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003695831&fileDetailSn=1&insertDataPrcus=N` (the dataset page `https://www.data.go.kr/data/15083033/fileData.do`), **keyless**; a 352,699,739-byte ZIP of per-province UTF-8 CSVs, cached NATIONALLY at `data/korea/raw/sbiz_15083033.zip` by `pipeline/countries/korea_sbiz_fetch.py`. ⚠️ **The ZIP's member names are undecodable** (neither UTF-8 nor CP949): a province's CSV is found by its first row's 시도명. ⚠️ The file id changes each quarter | none at download; step 2 reads 12 columns by name (no phone or owner column exists) and keeps 시도명 인천광역시. **Why not the brief's route** (2026-09-29): the national LOCALDATA API (data.go.kr 15154916) needs a key, and data.go.kr accounts need a Korean identity check (본인인증); Incheon's own permit lists (15048906 and four more, keyless, still in `data/incheon/raw/`) placed only 73.4% through KESA's lift-building join (15156424), and their salons list carries lot-number addresses no keyless file places. Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Goyang | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 고양시 | All three buckets via `korea_sbiz`: 50,587 rows -> **27,808 storefronts** (12,413 / 11,327 / 4,068), 100% on the register's own point; 9 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 고양시. **Why not the brief's sources** (2026-09-29): the Ministry's LOCALDATA API needs a Korean identity check; Goyang's own data.go.kr files hold only a meat-retail list (15118551), and 경기데이터드림's terms are ambiguous. Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Seongnam | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 성남시 | All three buckets via `korea_sbiz`: 46,326 rows -> **25,529 storefronts** (11,770 / 9,951 / 3,808), 100% on the register's own point; 30 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 성남시. **Why not the brief's sources** (2026-09-29): the Ministry's LOCALDATA API needs a Korean identity check; Seongnam's own data.go.kr files (restaurants 15076265 and six more) carry no coordinates, and 경기데이터드림's terms are ambiguous. Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Yongin | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 용인시 | All three buckets via `korea_sbiz`: 46,309 rows -> **23,481 storefronts** (10,999 / 9,353 / 3,129), 100% on the register's own point; 16 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 용인시. **Why not the brief's sources** (2026-09-29): the Ministry's LOCALDATA API needs a Korean identity check; Yongin's own data.go.kr files hold no food or retail register, and 경기데이터드림's terms are ambiguous. Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Suwon | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 수원시 (its four 구: 영통, 팔달, 권선, 장안) | All three buckets via `korea_sbiz`: 57,488 rows -> **33,433 storefronts** (16,022 / 12,214 / 5,197), 100% on the register's own point; 37 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 수원시. The brief's sources are closed or ambiguous for Suwon as for the first three satellites (Goyang's row). Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Bucheon | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 부천시 (its three 구, restored in 2024: 원미, 소사, 오정) | All three buckets via `korea_sbiz`: 37,720 rows -> **22,512 storefronts** (10,119 / 8,755 / 3,638), 100% on the register's own point; 28 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 부천시. The brief's sources are closed or ambiguous for Bucheon as for the first three satellites (Goyang's row). Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Namyangju | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 남양주시 (no 구) | All three buckets via `korea_sbiz`: 33,692 rows -> **18,344 storefronts** (8,069 / 7,699 / 2,576), 100% on the register's own point; 37 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 남양주시. The brief's sources are closed or ambiguous for Namyangju as for the first satellites (Goyang's row). Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Ansan | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 안산시 (its two 구: 상록, 단원) | All three buckets via `korea_sbiz`: 34,489 rows -> **19,711 storefronts** (9,263 / 7,494 / 2,954), 100% on the register's own point; 17 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 안산시. The brief's sources are closed or ambiguous for Ansan as for the first satellites (Goyang's row). Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |
| Uijeongbu | **SEMAS's 상가(상권)정보**, the same national file as Incheon's (row above), 경기도's member, 시군구명 의정부시 (no 구) | All three buckets via `korea_sbiz`: 20,888 rows -> **13,103 storefronts** (5,875 / 5,090 / 2,138), 100% on the register's own point; 11 personal names at a residential address withheld | The country cache `data/korea/raw/sbiz_15083033.zip` (Incheon's row) | 시도명 경기도, 시군구명 starting 의정부시. The brief's sources are closed or ambiguous for Uijeongbu as for the first satellites (Goyang's row). Licence **제한 없음** - Small Enterprise and Market Service, notice 68 | 2026-09-29 (edition 2026-06-30) |

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Seoul | **OpenStreetMap** - Lines 1–9, 신분당 (Shinbundang), 우이신설 (Ui LRT, ref `W`), 신림 (Sillim), and Korail's 경의·중앙, 수인·분당 and 경춘, matched on the relation's `ref` within network `수도권 전철`; English station names from the `railway=station` objects where the stop nodes lack `name:en` | the network's route relations and the station objects in Seoul's bbox, via `https://overpass-api.de/api/interpreter`, `https://overpass.kumi.systems/api/interpreter` or `https://maps.mail.ru/osm/tools/overpass/api/interpreter` (tried in that order) | 2026-09-25 | **Why not the agency:** Korea's national urban-railway station standard dataset has 1,099 stations and no line geometry, and no agency GTFS is published. No gate 3 (no operator counts read). One stop node renamed by id (9459739637 is 삼양사거리, not 삼양) and one interchange under two names merged (이수 / 총신대입구). Line 8's #D11D70 darkened to #92144E for contrast with Food service. AREX, GTX-A, the Seohae Line and the Gimpo Goldline not drawn (owner). OpenStreetMap, ODbL 1.0 - notice 1 |
| Daegu | **OpenStreetMap** - Daegu Metro Lines 1, 2 and 3 (Line 3 is `route=monorail`), matched on the relation's route type and `ref`, never on network (the labels disagree); English station names from the `railway=station` objects | every subway, light-rail, monorail and tram route relation in Daegu's bbox plus 대경선 (`ref=대경`), and the station objects, via `pipeline/osm.py`'s hosts (`https://overpass-api.de/api/interpreter`, then `https://overpass.kumi.systems/api/interpreter`) | 2026-09-27 | **Why not the agency:** Korea's national station dataset lacks Daegu Metro, and no GTFS is published. Gate 3 exact (35 / 29 / 30 whole-line stations) against **Korean Wikipedia**, a secondary source: dtro.or.kr rendered blank and data.go.kr refused the connection on 2026-09-27. Line 2's #00AA80 darkened to #00664D for contrast with Personal services. 대경선 not drawn (owner, on spacing). OpenStreetMap, ODbL 1.0 - notice 1 |
| Busan | **OpenStreetMap** - Busan Metro Lines 1-4 (Line 4 is `route=monorail`) and the Busan-Gimhae LRT (`ref=BGL`), matched on the relation's route type and `ref`, never on network (동해선 is tagged `부산 도시철도` like the city's lines); English station names from the `railway=station` objects | every subway, light-rail, monorail and tram route relation in Busan's bbox plus 동해선 (`ref=동해`), and the station objects, via `pipeline/osm.py`'s hosts (`https://overpass-api.de/api/interpreter`, then `https://overpass.kumi.systems/api/interpreter`) | 2026-09-27 | **Why not the agency:** no GTFS is published. Gate 3 exact (40 / 43 / 17 / 14 / 21 whole-line stations) against **Korean Wikipedia**, a secondary source, as Daegu's. Line 4's #217DCB darkened to #144B7A for contrast with Retail. 동해선 not drawn (owner, on spacing). OpenStreetMap, ODbL 1.0 - notice 1 |
| Incheon | **OpenStreetMap** - Incheon Lines 1 (`인천1`) and 2 (`I2`, light_rail), Line 1, Line 7 and the Suin-Bundang Line (`수인·분당`, route=train), matched on the relation's route type and ref; every relation in the box must be placed, drawn or named as not drawn (Line 4, Line 9, Gimpo Goldline, and the Wolmi Sea Train by name). AREX is not queried (Seoul's precedent) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.35,126.55,37.62,126.80 | 2026-09-29 | 79 stations inside Incheon, 151 of the drawn lines outside it (`outputs/incheon/excluded_stations.csv`). **Gate 3 exact** on Incheon Line 1 (33), Line 2 (27), Line 7 (53) and the Suin-Bundang Line (63), English Wikipedia's infoboxes read 2026-09-29 (secondary); Line 1 (102) left out of the whole-line gate, its southern branches never touching Incheon's box. ODbL, notice 1 |
| Goyang | **OpenStreetMap** - Line 3 and the Gyeongui-Jungang Line (`경의·중앙`, route=train), matched on route type and ref; every relation in the box placed, drawn or named as not drawn (Lines 1, 2, 4, 5, 6, 9, the Seohae Line - on the Gyeongui-Jungang track through the same stations in Goyang - GTX-A, the Ui LRT, the Gimpo Goldline, Incheon Lines 1 and 2) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.55,126.65,37.77,127.01 | 2026-09-29 | 20 stations inside Goyang (Line 3 11, Gyeongui-Jungang 10), 76 outside; GTX-A's Kintex has no ring. Gate 3 exact on Line 3 (44, English Wikipedia, secondary); the Gyeongui-Jungang Line not gated whole (OSM 55 names against 57). ODbL, notice 1 |
| Seongnam | **OpenStreetMap** - Line 8, the Suin-Bundang, Shinbundang and Gyeonggang Lines, matched on route type and ref (Line 3 and GTX-A named as not drawn) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.31,127.01,37.49,127.22 | 2026-09-29 | 18 stations inside Seongnam, 91 outside. Gate 3 exact on the Suin-Bundang (63) and Shinbundang (16) Lines; Line 8 (OSM's 24 stations against the infobox's 25) and the Gyeonggang Line (11 on its metropolitan section against 18) not gated whole. ODbL, notice 1 |
| Yongin | **OpenStreetMap** - the EverLine (`용인`, light_rail), the Suin-Bundang and Shinbundang Lines, matched on route type and ref (Line 1, the Gyeonggang Line and GTX-A named as not drawn) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.06,127.0,37.39,127.45 | 2026-09-29 | 24 stations inside Yongin, 67 outside; GTX-A's Guseong has no ring. Gate 3 exact on all three (15, 63, 16; English Wikipedia, secondary). ODbL, notice 1 |
| Suwon | **OpenStreetMap** - Line 1 (`1`), the Suin-Bundang (`수인·분당`, route=train) and Shinbundang Lines, matched on route type and ref (Line 4 and GTX-A, which only cross the box, named as not drawn) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.20,126.90,37.37,127.11 | 2026-09-29 | 14 stations inside Suwon (Line 1 4, Suin-Bundang 9, Shinbundang 2; Suwon shared), 129 outside. Gate 3 exact on the Suin-Bundang (63) and Shinbundang (16) Lines; Line 1 left out of the whole-line gate, as in Incheon. OSM's English name for 매탄권선 ("MaetanGwonseon") overridden to the signed Maetan-Gwonseon. ODbL, notice 1 |
| Bucheon | **OpenStreetMap** - Line 1 (`1`), Line 7 (`7`) and the Seohae Line (`서해`, route=train; drawn, owner 2026-09-29), matched on route type and ref (Lines 2, 5 and 9, Incheon Lines 1 and 2, the Gimpo Goldline and GTX-A, none with a station in Bucheon, named as not drawn) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.44,126.72,37.57,126.86 | 2026-09-29 | 14 stations inside Bucheon (Line 1 5, Line 7 7, Seohae 4; Sosa and Bucheon Stadium shared), 121 outside. Gate 3 exact on Line 7 (53); Line 1 left out of the whole-line gate, as in Incheon; the Seohae Line not gated whole. Samsan Gymnasium, on the Incheon border (operated by Incheon Transit), falls about 50 m inside OSM's Bucheon boundary and is kept (owner); Incheon's build left it out on the same boundary. Seohae's colour is OSM's tag (#5EAC41). ODbL, notice 1 |
| Namyangju | **OpenStreetMap** - Line 4 (`4`), Line 8 (`8`), the Gyeongui–Jungang Line (`경의·중앙`) and the Gyeongchun Line (`경춘`), the last two route=train, matched on route type and ref (Lines 2, 5, 6 and 9 and GTX-A, none with a station in Namyangju, named as not drawn) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.52,127.10,37.81,127.45 (the rail answer's OSM base 2026-07-28) | 2026-09-30 | 17 stations inside Namyangju (Gyeongchun 7, Gyeongui–Jungang 6, Line 4 3, Line 8 2; Byeollae shared), 105 outside. No line takes the whole-line gate (each for a recorded reason, `config.LINE_STATION_COUNTS`); each line's in-city stations read against its line table instead, all four agreeing. Two English names spaced or hyphenated as signed. ODbL, notice 1 |
| Ansan | **OpenStreetMap** - Line 4 (`4`), the Suin–Bundang Line (`수인·분당`) and the Seohae Line (`서해`; drawn on Bucheon's precedent, owner 2026-09-29), the last two route=train, matched on route type and ref (Line 1, Incheon Line 1 and GTX-A, none with a station in Ansan, named as not drawn) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.16,126.50,37.40,126.95 | 2026-09-30 | 13 stations inside Ansan (Line 4 8, Suin–Bundang 7, Seohae 5; six shared by Line 4 and Suin–Bundang, Choji by all three), 110 outside. Gate 3 exact on the Suin–Bundang Line (63); Line 4 left out of the whole-line gate (only its service relations reach the box), the Seohae Line not gated whole, as in Bucheon. One English name spaced as signed. ODbL, notice 1 |
| Uijeongbu | **OpenStreetMap** - the U Line (`U`, Uijeongbu LRT, light_rail), Line 1 (`1`) and Line 7 (`7`), matched on route type and ref (Line 4 and GTX-A, none with a station in Uijeongbu, named as not drawn; the U Line's two depot-shuttle relations, with no ref, placed by name as not drawn, Incheon's pattern) | The Overpass mirrors in `pipeline/osm.py`, bbox 37.67,126.99,37.79,127.15 | 2026-09-30 | 20 stations inside Uijeongbu (U Line 15, Line 1 5, Line 7 1; Hoeryong shared), 126 outside. Gate 3 exact on the U Line (15) and Line 7 (53); Line 1 left out of the whole-line gate, as in Incheon. The U Line's 경전철의정부 (LRT Uijeongbu) and Korail's 의정부 are separate stations 257 m apart. ODbL, notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Seoul | **OpenStreetMap relation 2297418** (서울특별시, admin_level 4), fetched by id and checked by name, polygonised from outer ways and area-gated at its measured 606 km2 | The Overpass mirrors in `pipeline/seoul/config.py` | Seoul; the 223 stations of drawn lines outside it are recorded in `outputs/seoul/excluded_stations.csv`. OpenStreetMap, ODbL 1.0 - notice 1 |
| Daegu | **OpenStreetMap relation 2395674** (대구광역시, admin_level 4, with 군위군), fetched by id and checked by name, polygonised from outer ways and area-gated at its measured 1,495 km2 | `pipeline/osm.py`'s Overpass hosts | Daegu; the 5 Gyeongsan stations of Lines 1 and 2 are recorded in `outputs/daegu/excluded_stations.csv`. OpenStreetMap, ODbL 1.0 - notice 1 |
| Busan | **OpenStreetMap relation 2396450** (부산광역시, admin_level 4), fetched by id and checked by name, polygonised from outer ways and area-gated at its measured 2,019 km2 (it includes territorial water) | `pipeline/osm.py`'s Overpass hosts | Busan; the 17 stations of drawn lines outside it (Line 2's 5 in Yangsan, the LRT's 12 in Gimhae) are recorded in `outputs/busan/excluded_stations.csv`. OpenStreetMap, ODbL 1.0 - notice 1 |
| Incheon | **OpenStreetMap relation 2297419** (인천광역시, admin_level 4, KR-28), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **9,906 km²** with territorial sea around the Ongjin islands (about 1,067 of land), gated at 9,800-10,000. Scopes the stations; the businesses are the register's own 인천광역시 rows. ODbL, notice 1 |
| Goyang | **OpenStreetMap relation 2409166** (고양시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **266 km²**, gated at 260-272. Scopes the stations; the businesses are the register's own 고양시 rows. ODbL, notice 1 |
| Seongnam | **OpenStreetMap relation 2409180** (성남시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **142 km²**, gated at 138-146. Scopes the stations; the businesses are the register's own 성남시 rows. ODbL, notice 1 |
| Yongin | **OpenStreetMap relation 2409189** (용인시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **592 km²**, gated at 580-604. Scopes the stations; the businesses are the register's own 용인시 rows. ODbL, notice 1 |
| Suwon | **OpenStreetMap relation 2409182** (수원시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **121 km²** (the city publishes 121.1), gated at 116-126. Scopes the stations; the businesses are the register's own 수원시 rows. ODbL, notice 1 |
| Bucheon | **OpenStreetMap relation 2409162** (부천시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **54 km²** (the city publishes 53.4), gated at 51-57. Scopes the stations; the businesses are the register's own 부천시 rows. ODbL, notice 1 |
| Namyangju | **OpenStreetMap relation 2409175** (남양주시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **457 km²**, gated at 440-475. Scopes the stations; the businesses are the register's own 남양주시 rows. ODbL, notice 1 |
| Ansan | **OpenStreetMap relation 2409159** (안산시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **486 km²** (Daebudo and its sea included), gated at 470-500. Scopes the stations; the businesses are the register's own 안산시 rows. ODbL, notice 1 |
| Uijeongbu | **OpenStreetMap relation 2409183** (의정부시, admin_level 6), fetched by id and checked by name, polygonised | The Overpass mirrors in `pipeline/osm.py` | **82 km²**, gated at 78-86. Scopes the stations; the businesses are the register's own 의정부시 rows. ODbL, notice 1 |

## Licences and terms of use

### Explicit and permissive — confirmed

| Source | Licence | Attribution declared |
|---|---|---|
| **Seoul** — the seventeen `인허가 정보` datasets below (**built 2026-09-25**, notice 18, Seoul Metropolitan Government; 8 read 2026-09-22, 9 checked 2026-09-24) | **공공누리 제1유형 / KOGL Type 1** — attribution required, commercial use and derivative works permitted | 저작권자 **서울특별시**; 제3저작권자 **없음** (none) |

#### Seoul — eight `인허가 정보` datasets, read 2026-09-22 (BUILT 2026-09-25)

Recorded when the licence was read; **Seoul was built 2026-09-25, so these are
active obligations - notice 18, Seoul Metropolitan Government.** Source: `data.seoul.go.kr`,
downloaded via the SHEET CSV export (`ssUserId=SAMPLE_VIEW`, no account — see
`docs/global_country_shortlist.md`).

| `infId` | Dataset | Bucket | Active premises |
|---|---|---|---|
| `OA-16094` | 서울시 일반음식점 인허가 정보 | Food | 120,182 |
| `OA-16095` | 서울시 휴게음식점 인허가 정보 | Food | 37,113 |
| `OA-16063` | 서울시 미용업 인허가 정보 | Personal services | 33,679 |
| `OA-16064` | 서울시 이용업 인허가 정보 | Personal services | 2,366 |
| `OA-16065` | 서울시 세탁업 인허가 정보 | Personal services | 3,263 |
| `OA-16146` | 서울시 목욕장업 인허가 정보 | Personal services | 673 |
| `OA-16044` | 서울시 숙박업 인허가 정보 | Personal services | 2,788 |
| `OA-16007` | 서울시 동물병원 인허가 정보 | Personal services | 981 |

**Nine more, checked 2026-09-24** (the same fields on each page, read
individually): all **공공누리 1유형**, `제3저작권자` 없음, 매일, 원본시스템
지방행정 인허가정보. The pages also carry an empty `AI유형 -` tag. Buckets are
as the owner decided on 2026-09-24 (`seoul.md`). The
bucket column above was the 2026-09-22 guess; the brief recommends
**excluding** 숙박업 and 동물병원.

| `infId` | Dataset | Recommended bucket | Active premises |
|---|---|---|---|
| `OA-16084` | 서울시 제과점영업 인허가 정보 | Retail | 4,228 |
| `OA-16085` | 서울시 즉석판매제조가공업 인허가 정보 | Retail | 15,410 |
| `OA-16080` | 서울시 식품판매업(기타) 인허가 정보 | Retail | 660 |
| `OA-16071` | 서울시 축산판매업 인허가 정보 | Retail (식육판매업 only) | 6,317 of 11,628 |
| `OA-16144` | 서울시 담배소매업 인허가 정보 | Retail | 15,590 |
| `OA-16096` | 서울시 대규모점포 인허가 정보 | Retail | 740 |
| `OA-16070` | 서울시 건강기능식품일반판매업 인허가 정보 | Retail (영업장판매 only) | 10,648 of 29,315 |
| `OA-16089` | 서울시 단란주점영업 인허가 정보 | Food service (owner, 2026-09-24) | 1,865 |
| `OA-16090` | 서울시 유흥주점영업 인허가 정보 | Excluded (adult services) | 1,682 |

**The first eight carry identical metadata** (as do the nine), checked individually rather than
inferred from one: `이용허락범위` = **공공누리 1유형 : 출처표시 (상업적 이용 및
변경 가능)**, `저작권자` = 서울특별시, **`제3저작권자` = 없음**, `갱신주기` =
매일 (daily). `원본시스템` is 공공데이터포털(지방행정 인허가정보) — i.e. these
are Seoul's republication of the national LOCALDATA register.

**`제3저작권자: 없음` is the check that matters most here.** It is the field
that would disclose rights incorporated *by reference* — the trap that hid
Philadelphia's prohibition behind a licence forbidding nothing. Seoul declares
none, on all eight.

**KOGL Type 1, from `kogl.or.kr` itself rather than from the label.** Three
obligations, and one of them is easy to miss:

1. **출처표시 — attribution.** The prescribed form names the institution, the
   year, the KOGL type and the dataset title. And: *"온라인에서 출처
   웹사이트에 대한 하이퍼링크를 제공하는 것이 가능한 경우에는 링크를
   제공하여야 합니다"* — **where a hyperlink is possible, one must be
   provided.** That is an obligation of the same shape as ODbL's, not a
   courtesy, and it is the part a plain "Source: Seoul Metropolitan Government"
   string would fail.
2. **No implied endorsement.** *"이용자는 공공기관이 이용자를 후원한다거나
   공공기관과 이용자가 특수한 관계에 있는 것처럼 제3자가 오인하게 하는 표시를
   해서는 안됩니다"* — nothing may suggest Seoul sponsors this project or has
   any special relationship with it.
3. **저작인격권 — moral rights, which bear on transformation.** Modified use
   must not mislead; the licence's own second example is *"연구보고서의
   연구성과나 통계수치 등을 수정하여 제3자로 하여금 착오를 불러일으킬 수 있는
   경우"* — altering figures so as to mislead a third party. This project
   aggregates premises into per-station counts, which is exactly a statistical
   transformation, so it falls under the same disclosure duty already met for
   **INEGI** and **Montréal**: say plainly that the counts are this project's
   derivation and not Seoul's published figures.

**The publisher already did the privacy work — verified, not assumed.** All
eight files were checked for a proprietor-name column (`대표자`, `성명`, `이름`,
`주민`, `생년`): **none exists** in any of them, across 37–39 columns. The only
name field is `사업장명`, the registered trade name, which this project's
invariant explicitly permits. Same posture as France's *non-diffusible*,
Edmonton's `<REDACTED FOR PRIVACY>` and Austria's GISA.

**One privacy item left for build time, not resolved here.** Korean salon and
restaurant trade names very often *contain* a personal name — `김은미장`
("Kim Eun-mi salon") among 미용업, and ~30% of 사업장명 values are a bare 2–4
hangul token. These are registered trade names, so the invariant allows them,
but `scripts/check_personal_exposure.py` will need a Korean-aware pass rather
than its current one, and Personal services is the bucket where a salon
operating from a residential address is most plausible. **Flagged for
`add-city` Step 0, not pre-judged.**

### 🇰🇷 Daegu and Busan (both built 2026-09-27; notices 48 and 49) — read 2026-09-27 by the `licence-read` agent

**The same national register (LOCALDATA, 행정안전부 / 한국지역정보개발원) carries
different declared terms depending on who republishes it.** Seoul attaches KOGL
Type 1; Daegu and Busan attach no KOGL type at all; data.go.kr now declares
**이용허락범위 제한 없음** for the national listings (15096283, 15045016,
15006730, and the successor API 15154916). `global_country_shortlist.md`
records 15096283 as KOGL Type 1, which is no longer what data.go.kr shows.
So **Seoul's three KOGL duties do not carry over by licence**, but the standing
non-affiliation line is kept on both pages anyway.

**Busan — the keyless `LocalDataService` Open API** (`data.busan.go.kr`,
"구군 인허가포털", OA_TT00001–39; frozen at 2026-04-15). **PERMITTED WITH
CONDITIONS; nothing to do beyond a credit.**
- **The grant** is the portal's own 공공데이터 이용정책
  (`https://data.busan.go.kr/bdip/publicDataPolicy.do`): *"데이터웨이브에서
  제공하는 공공데이터는 공공데이터법에 따라 누구나 이용가능하고, 영리 목적의
  이용을 포함한 자유로운 활용이 보장됩니다"*, and *"별도의 신청절차 없이
  이용 가능"*. The catalogue's managing department is 행정안전부, whose
  national listings say 제한 없음. 공공데이터법 제3조④ bars a public body from
  restricting use.
- **Machine metadata is NOT evidence here**: `usePrmisnEnnc` reads "없음" on
  all 11 operations a build would use, but on a control dataset (15143208)
  Busan's DCAT says 제한 없음 where data.go.kr says CC BY, and the list popup
  writes the two fields into swapped cells. The permission rests on the policy
  sentence and the Ministry's declaration, not on this field.
- **Conditions**: a reasonable source credit (저작권법 제37조, no wording
  prescribed), and good-faith use (공공데이터법 제3조⑤). **Credit**: Busan's
  Big-데이터웨이브 (linked) as the channel, the Ministry's local-government
  licence data as the source, and the snapshot date.
- **Reasoned position, owner-accepted 2026-09-27: the portal terms' 제14조.**
  *"플랫폼이 작성한 저작물에 대한 저작권 … 은 플랫폼에 귀속합니다"* and ②
  bars republishing information whose IP belongs to the platform without
  consent. Read as covering only works the platform itself authored: this
  register is entered by the 16 districts through the Ministry's system. The
  restrictive reading (API output as the platform's IP) is recorded, not
  adopted. Any objection from Busan is honoured, not argued.
- **Privacy**: no 대표자 or 성명 field; the API returns **`sitetel` (phone)**,
  which is never published. The terms are silent on caching API output and on
  the frozen feed; no retirement notice among 345 portal notices.

**Daegu — D-데이터허브 monthly files** (`data.daegu.go.kr`,
"26년08월_인허가데이터", DMI_0000119600–09 and 119690–95, origin 한국지역정보개발원).
**AMBIGUOUS in a way that matters; proceeding on a disclosed reasoned
position (owner, 2026-09-27).**
- **The dataset pages declare nothing**: every licence field in the embedded
  JSON is null, and no page text mentions 공공누리, 이용허락 or 약관. The only
  reuse text is "[출처 : 한국지역정보개발원]".
- **The permissive side**: D-데이터허브's 공공데이터 이용정책
  (`https://data.daegu.go.kr/open/introduce/openData.do`) repeats the national
  *"영리 목적의 이용을 포함한 자유로운 활용이 보장됩니다"*; its data page says
  the permit data is *"공공데이터포털(data.go.kr)에서 제공하는 데이터"*; the
  national listings say 제한 없음; and 공공데이터법 제3조④ forbids restricting
  use.
- **The restrictive side**: the City's own copyright guide
  (`https://www.daegu.go.kr/index.do?menu_id=00050251`, the footer's
  저작권정책) says *"공공누리가 부착되지 않은 자료들을 이용하고자 할 경우에는
  공공저작물 관리책임관 및 실무담당자와 사전에 협의한 이후에 이용해 주시기
  바랍니다."* The files carry no KOGL mark. On that reading, publishing waits on
  a consultation (phone only: 053-803-3770 / 3785).
- **Why the permissive reading was taken**: the guide is written under
  저작권법 제24조의2 about 저작물 (its examples are photos and report
  statistics), D-데이터허브 does not link to it, its wording is a request, and
  the Public Data Act governs public data unless another law specially
  provides (제4조).
- **The route that would have avoided the question failed**: the national
  file host the data.go.kr listings link to (`file.localdata.go.kr`) answered
  403 to a plain fetch and to the browser on 2026-09-27. The listing's file was
  last modified 2025-11-27, older than Daegu's 2026-08 edition.
- **If Daegu objects, the page comes down** (the removal commitment below).
  The consultation stays available as an owner act, not a prerequisite.
- **Credit** (suggested, not prescribed): Daegu Metropolitan City,
  D-데이터허브 (`data.daegu.go.kr`), originally 한국지역정보개발원.
- **The XLSX columns, measured 2026-09-27** (`docs/build_briefs/daegu.md`):
  the phone column is **`소재지전화`**, never read. No 대표자 or 성명 column in
  any of the eleven files a build reads. `권리주체일련번호` (the rights holder's
  serial, in 축산판매업) and the tenure and rent columns are never read either.
  Select columns by exact name.
