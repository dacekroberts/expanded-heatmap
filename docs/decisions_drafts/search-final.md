### 2026-10-13 - Gwangju: the owner's four answers on its read (branch search-final)

- **The owner, to four questions with a recommendation each: "1 keep, 2
  drop, 3 drop, 4 drop and keep like you said".**
- **1. Kept:** the signed junction 전철우사거리 (node/436870846), named for a
  restaurant brand that is also a living person's name. A road feature
  under a trade name; no config entry is needed, since no leak word fires.
- **2. Dropped by id:** 정율성생가 (way/629024038), a birthplace admitted by
  the composer's own article. The home rule needs a checked sign of
  visiting and none was checked; it can come back through
  `PLACE_VISITABLE` with a source.
- **3. Dropped by id:** 제1전투비행단 (way/444717696), the air force unit as
  a second row for the airfield 광주공항 (way/105569841), which stays.
- **4. Dropped by id:** 광주하남3도시개발지역 (node/6411444468), a development
  zone's planning label. **Kept:** 목교 (node/6367714556) and 월봉
  (way/572641161), as localities.
- Index 4,242 rows to 4,239.

### 2026-10-13 - Search final group: the four search areas ruled; Anyang and Gwangju built and read; German measured on Gelsenkirchen, not yet ruled (branch search-final)

- **Branch `search-final`, cut from `search-rollout` 57bdff22, holds the 32
  cities the extract run left for hand work.** Milan and Toronto are not in
  it. Every fetch below is the extract route; no Overpass request was made.
  Nothing is pushed and no map is rendered, so rule A of
  `check_place_search.py` fails for every city here until the landing's one
  render.
- **The owner, to the four search-area recommendations: "1-3 yes sounds
  good".** (1) Anyang widened, (2) Gwangju keeps Buk-gu, (3) Most and
  Yamagata get a recorded exception.
- **Anyang: `PLACE_AREA` widened to the three relations the regional map is
  cut to** (안양시 2409161, 군포시 2409167, 의왕시 2409184; the config's
  `REGIONAL_RELATIONS`). The plan had taken the city alone; measured
  2026-10-13, 7 of 14 stations lay 1.1 to 3.9 km outside it. Refetched from
  south-korea-261012 (`--force`, over this city's own extract caches):
  stations 7, 6 and 1, none outside. Index 2,010 rows as built, 1,988 after
  the read.
- **Gwangju: Buk-gu kept through `PLACE_AREA_KEPT`.** No 광주광역시 relation
  exists in south-korea-261012; the only level 4 relation is 전남광주통합특별시
  (21039457), the merged province. Buk-gu (relation/7348583) holds none of
  the 20 stations and 12,657 of the map's 47,214 businesses, the most of the
  five districts. Precedent: Daejeon, Daegu and Busan index the whole city as
  one relation, districts without a station included. Rejected: dropping
  Buk-gu, which leaves 27% of the map's pins on streets the search cannot
  find. Index 4,297 rows as built (391 KB raw), 4,242 after the read.
- **Most and Yamagata are PARKED on shared code: four stations are quiet,
  not cut off.** Measured 2026-10-13 with `place_index.build_city` and
  `uncovered_stations` in memory, and for Most a read of ustecky-261012 for
  every named object within 1 km in any municipality:
  - Most: Záluží, areál Hlubina; Záluží, doprava; Záluží, čerpací stanice.
    All three inside Litvínov (relation/436574). No named highway way
    within 1 km of any in the whole extract; nearest index row 1,065, 1,388
    and 1,308 m; nearest indexed street line 1,112, 1,688 and 2,707 m. The
    stops serve a chemical works. Widening the area adds a municipality with
    no station and covers nothing.
  - Yamagata: Omoshiroyama-Kogen, inside Yamagata (relation/4137051), 1,071 m
    from its edge. Within 1 km: the station, the river 紅葉川 (74 m; its row
    point 2,961 m away) and a viewpoint with no Wikidata entry. Nearest
    index row 2,146 m, nearest street line 1,439 m.
  - Sent to Cleanup as a finding: `config.PLACE_QUIET_STATIONS`, station name
    to reason, read by `place_index.run()` and rule H, a listed station that
    is covered or not on the map stopping the step. Cleanup builds it after
    `search-rules-2` lands. Rejected: counting a river's drawn line toward
    reach, which covers Yamagata and one of Most's three only.
- **Anyang's read (place-read on the top model; streets on Sonnet), acted on
  where a settled call covers it.** `PLACE_REVIEWED`: 12 signed junctions
  named for the building beside them (Seoul's precedent). `PLACE_DROPPED`,
  each id checked against its cached name: 5 parks and playgrounds whose
  operator tag is an apartment estate's management office; a vicariate
  office and a building name tagged places of worship; 3 descriptions; a
  monument whose name is cut short; 8 Railroad Museum exhibits whose article
  is their class's or kind's; the corridors of an underground shopping mall
  (19 ways), a station-to-store footbridge and a street named
  "보행자전용도로" (3 ways). The street screen read 87 of 1,310 distinct
  names line by line and filtered the rest by pattern.
- **Gwangju's read, the same way.** `PLACE_REVIEWED`: 7 junctions.
  `PLACE_DROPPED`, 77 ids: 6 estate gardens and playgrounds, 18
  descriptions (benches and flowerbeds tagged parks among them), a cafe's
  name on a historic building, a shopping street's name tagged a monument, a
  school tagged a place of worship, two religious houses and two church
  offices, a former church, an artwork and a community office each admitted
  by someone else's article, a shrine drawn a second time as a place, a
  market car park's entrance tagged a junction, a bus platform, and 16
  street names (41 ways: a street named "no", school and estate roads,
  access ramps, a planning code, an address). The street screen read about
  770 of 3,015 rows line by line.
- **Left as they are, for the owner:** Anyang's 오봉 (a rail yard in the
  index as a station), one locomotive with a class article and a registered
  property number, two Buddhist sites that may be residences; Gwangju's
  junction named for a restaurant brand that is also a living person's
  name, a composer's birthplace on the composer's article, four named
  plazas that may be an estate's, three place rows that are not
  neighborhoods, the air base as a second row for the airport. In both
  cities: cycle routes, hiking trails and footbridges as street rows
  (Korean way words keep them, Seoul's and Busan's precedent).
- **Rule candidates sent to Cleanup, not built here:** Korean bare type
  words (Anyang 족구장 3, 고인돌, 왕국회관; Gwangju 19 words on 20 rows); "N호"
  park codes (Anyang 3); an operator tag naming an apartment management
  office (Anyang 5, Gwangju 1); `access=customers` on a described service
  road (Gwangju 3 names, 12 ways); a grave kept on its subject's article
  (Anyang 1); a second station row from a station building's outline
  (Gwangju 상무역). Gwangju's 35 stations skipped as not yet open (Line 2,
  34 stations) are listed for the watch file in the read's scratch folder.
- **German, measured on Gelsenkirchen and NOT yet ruled.** Scaffolded on
  relation 62522 (Stadt Gelsenkirchen, admin_level 6, the municipality key
  the map is cut to), which the owner has not yet confirmed as Germany's
  level. Its boundary is not whole in muenster-regbez-261012, so
  duesseldorf-regbez-261012 (216,496,220 bytes) and arnsberg-regbez-261012
  (194,825,164 bytes) were downloaded once each through the module and the
  three read as one: the first three-file set, 689 objects held by more
  than one file and taken once, 64.8 s, 1,533 MB. Built in memory only
  (scratch `build_draft.py`, lists patched for the process): 1,852 rows,
  German on 100% of names and English on 0%, all 60 stations covered. Of
  458 distinct minor-way names 366 read as a way under 26 way words (as a
  word or a compound's ending) and 12 leading prepositions; the 92 others
  are tram platforms, coded private roads on an industrial site and field
  names. Field-name endings (-kamp, -delle, -winkel, -garten) add 3 street
  rows and -hof 9 more; neither is proposed before Berlin, Bremen and Zurich
  are measured, since -hof also ends Bahnhof and Friedhof. The 30 leak words
  hit two names here and are unmeasured until Berlin. The lists go to
  Cleanup as `docs/decisions_drafts/search-lang-de.md` once the owner rules.
- **Downstream:** no map, notice or licence row changes on this branch; the
  two new regional files are the source already recorded for place search.

## Rule candidates from the final group's reads (one numbered list, kept current)

For Cleanup's third list to the owner after `search-rules-2` lands (Cleanup,
2026-10-13). A config comment "candidate N" marks a by-id drop the rule would
make redundant. Gwangju's unopened stations are in
`search-final_unopened_gwangju.md`, beside this file.

1. **Korean bare type words.** Anyang: 족구장 (way/468970401, way/543834661,
   way/1461490384), 고인돌 (node/6408221707), 왕국회관 (node/10709274202).
   Gwangju: 가든 way/473240192, 공터 way/636604061, 구령대 way/638451660, 물놀이장
   way/555643161, 산책로 way/1022327187, 생태 공원 way/504443138, 조각공원
   way/1226960956, 호수공원 way/1132460208, 기념탑 node/7178968717, 설립기념탑
   node/4664813406, 일주문 way/1236241022, 비좌 node/10310832459, 연자방아
   node/10310832461, 훈련센터 node/4699518289, 자연마을 node/9573137349 (a
   place row); 놀이공원, 물놀이공원 and 썬큰광장 are dropped by id in Gwangju.
2. **Korean code plus type, "N호" beside a park type.** Anyang:
   way/683033814, way/381700280, way/580706448. None dropped by id.
3. **leisure=park whose operator names an apartment estate or its
   management office.** Anyang way/777263833, 777264096, 777262929,
   777263610, 746342781; Gwangju way/835704878. Dropped by id.
4. **access=customers on a service road named by a description.** Gwangju,
   3 names and 12 ways (후문 진입로, 단지 내 도로, 숭의중 도로). Dropped by id.
5. **A grave kept on its subject's article.** Anyang way/1418223062. Left as
   it is; Cleanup checks the own-article test on it.
6. **A second station row from a station building's outline.** Gwangju
   way/1442542051. Left for batch 2's one-row-per-station rule.
7. **An exhibit admitted by its class's or kind's article.** Anyang
   way/829939487, 829939488, 829939493, 829939494, 829939495, 829939499,
   829939503, and way/829939489 (tourism=attraction, no historic tag).
   Dropped by id.
