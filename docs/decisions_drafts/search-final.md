### 2026-10-13 - The four German cities read; drops by id in each config; the classes left for the owner (branch search-final)

- **The owner, to the three list calls: "1 yes, note the future edit point,
  2 yes, 3 sounds good"**: -kamp, -winkel, -acker and -hof in with the -hof
  misfires dropped by id; "AG" and "KG" out of the leak words; the Swiss
  way words in. The lists and every measurement are in
  `search-lang-de.md`.
- **Read from in-memory dumps, since no German index can be written before
  the lists are folded in.** The `place-read` agent cannot use
  `place_search_review.py` without an index file, so each reader got a dump
  of every row with its OSM id and cached tags (scratch `build_dump.py`).
  Places, stations and landmarks on the top model: Berlin (all 740 places,
  744 stations and 3,873 landmarks read by name and deciding tags, full tags
  for about 200), Bremen (all 879 rows), Zurich (all 895 rows);
  Gelsenkirchen by hand. Streets on Sonnet, minor-way-only rows read line
  by line and the rest screened by pattern (Berlin 1,870 of 10,840 rows
  read, Bremen 1,268 of 4,620, Zurich 747 of 2,430, Gelsenkirchen 125 of
  1,544).
- **A fault in this session's own measure, found by the readers and
  fixed:** the in-memory patch missed `_BARE_FOLDED`, so no German bare type
  word was applied in the first builds or in the dumps the readers read.
  The corrected counts are in `search-lang-de.md`.
- **Dropped by id, each checked against its cached name, each under a
  settled call:** Berlin 110 ids (66 landmark, place and station objects, 44
  ways of 27 street names); Bremen 55 (19 objects, 36 ways of 18 names,
  Lloydhof and Alter Schulhof among them); Zurich 35 (27 objects, 8 ways of
  5 names); Gelsenkirchen 34 in all (15 objects, 19 ways of 2 names). The
  classes: homes and residents' facilities, dealers' galleries with no
  article, offices and residences tagged places of worship, descriptions
  and codes standing in for names, names that say the thing is gone, names
  cut short or with a mapper's note in them, site relations placed
  kilometres from their object, zoo and museum contents, one Stolperschwelle,
  station corridors and exits, facility roads.
- **NOT acted on, for the owner (no precedent, or a precedent that points
  two ways):**
  1. Public art admitted by a Wikidata entry alone: 1,048 of Berlin's 1,111
     artworks and 171 of Zurich's 563 landmarks, from bulk imports, many
     under generic titles ("Figur", "Ohne Titel", "Mutter mit Kind" eleven
     times).
  2. Allotment lanes: about 600 single-word "-weg" street rows in Bremen
     and the flower-named paths in Berlin ("Rosenweg" merges 76 footpaths),
     inferred from themed names, no allotment tag in the cache.
  3. Coded path names on minor ways in Berlin, about 116 rows ("Weg 5",
     "Stichweg A", "Querweg 12"), and 38 "Straße N" rows on minor ways only
     (138 on residential ways are real street names and stay).
  4. Trail and route names as streets (Zurich 8, Bremen 6, Berlin's Berliner
     Mauerweg, Gelsenkirchen's Radschnellweg), the question already open
     for Anyang and Gwangju.
  5. Abandoned railway alignments as landmarks: 66 rows in Berlin, 50
     abandoned, disused or razed.
  6. Homes that are visited monuments (Corbusierhaus, Aalto-Hochhaus, Villa
     Borgward, Gut Landruhe, Kreuzberg Tower): tourism=attraction opens the
     home rule and no opening was checked.
  7. Bremen's exclave: the city relation includes the Überseehafengebiet
     inside Bremerhaven, 55 km north, with 4 rows and no tram stop.
  8. Garden plots inside Berlin's Gärten der Welt (10 rows, each with its
     own Wikidata entry, named for countries) and six courtyards of the
     same garden drawn as localities.
  9. Smaller ones, by id once ruled: Zurich's private-for-vehicles service
     roads that carry a street-register Wikidata entry (about 8), two
     graves of public figures tagged memorials, pools and a minigolf course
     tagged parks, Bremen's facade ornaments (22 rows of one ensemble) and
     the Focke-Museum's re-erected buildings, the Low German endings and
     the bare type words in `search-lang-de.md`.
- **Station rows are left to batch 2's one-row-per-station rule**: Berlin's
  names collide across S-Bahn, U-Bahn, tram and mainline rows (54 names on 2
  to 4 rows once "S ", "U ", "S+U " and "Berlin " are set aside), Bremen
  splits stops by platform letters, Zurich has two true duplicates.

### 2026-10-13 - German: the owner's answers; Anyang's three; Gelsenkirchen's drops by id (branch search-final)

- **The owner, to the four German calls: "1. measure on other cities like
  you said first. 2. confirm you are allowed to do so. 3. address the two
  classes like your recommendation", and then "yes 2 is my confirmation".**
- **1. Field-name street endings are not in the draft lists** (-kamp,
  -delle, -winkel, -garten, -hof). They are measured on Berlin, Bremen and
  Zurich before any is proposed.
- **2. Germany's search area is the relation whose municipality key
  (de:amtlicher_gemeindeschluessel) is the one the map is cut to:**
  Gelsenkirchen 62522 (level 6), Berlin 62422 (level 4, the city-state),
  Bremen 62559 (level 6, the city and not the state with Bremerhaven).
  Zurich is 1682248, its config's `ZURICH_RELATION`. Berlin, Bremen and
  Zurich were scaffolded and fetched on that word.
- **3. Prayer stones:** the seven "Schmerz Mariens" stones are dropped by
  id and their group row (node/4553571141) stays. Each is tagged a place of
  worship and carries no register key, unlike Prague's Stations of the
  Cross. **Untitled artworks:** the three rows named "Ohne Titel" in some
  form carry a Wikidata entry and stay; the fourth, with no entry
  (node/5272526752), was never a row, since the notable rule already leaves
  it out. Nothing was dropped for this class.
- **Gelsenkirchen's other drops by id, each covered by a settled call:** a
  kindergarten and a church youth office tagged places of worship, four
  sections of the zoo drawn as parks, a park named for the cattle in it and
  a building named by a description. 15 ids in all; in memory the index is
  1,837 rows (165 landmarks).
- **The owner, to Anyang's three: "1. drop, 2. keep, 3. keep".** 오봉
  (node/7817073349), a rail yard in the index as a station, is dropped by
  id. The Pasi-class locomotive 5-23 (way/829939510) stays on its
  registered property number. 오봉정사 (node/12133504731) and 복전원
  (way/1219935236 and four buildings) stay: the tags cannot tell a
  residence from a temple.

### 2026-10-13 - Most and Yamagata: the quiet stations recorded in their configs; a page note proposed (branch search-final)

- **`PLACE_QUIET_STATIONS` is written in both configs**, station name as in
  `STATIONS_CSV` to the measured distances, on the owner's approval as
  Cleanup relayed it (in `DECISIONS.md` on master, 2026-10-13). Nothing
  reads the list yet: both cities stay parked until Cleanup lands the
  shared code after `search-rules-2`.
- **PROPOSAL for review time, a DRAFT, the owner's wording to settle: one
  sentence on each city's page, after the search bullet.**

  > Most: Three tram stops at the Záluží chemical works have no named
  > street or place within 1 km in OpenStreetMap, so a search near them
  > finds only the stops.

  > Yamagata: Omoshiroyama-Kogen is a mountain station with no named street
  > or place within 1 km in OpenStreetMap, so a search near it finds only
  > the station.

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
8. **The private-street rule does not read living_street.** Berlin, 7 rows
   tagged access=private: way/38574171, 114189253, 114189255, 24839839,
   148434465, 888746629, 244839885. Not dropped by id.
9. **A site relation or a boundary relation indexed at a centroid far from
   its object, a duplicate of a row with the same Wikidata entry.** Bremen
   relation/2979110 and relation/31489 (dropped by id), relation/62559 (the
   city boundary, left for batch 2's rule 10); Zurich relation/9379205
   (dropped by id).
10. **A `wikipedia` value that is a list article with an anchor ("de:Liste
    der ...#ref") counted as an article of the object's own.** Bremen, 63
    landmark rows, example node/5843658961; it keeps bare type names in
    (way/27012701, way/240493406, way/163219377, node/5858985786).
11. **A name that says the thing is gone, with no lifecycle tag:**
    "(geschlossen)", "(abgebrannt)", "(stillgelegt)", "(außer Betrieb)",
    one each in Berlin, dropped by id; "ehem." or "ehemalig" leads 39 Berlin
    landmark names, several of them standing buildings, so the word alone
    is no drop. A razed prefix on a railway key (way/405302873) is not read.
12. **A Stolperschwelle** (artwork_type=stolperstein, memorial=
    stolperschwelle): Berlin node/11338877281, dropped by id; the rule reads
    memorial=stolperstein only.
13. **A public_transport=station object with no railway tag in the index as
    a station:** Berlin node/12469014918 and node/11897068961 (a service
    point and a shared-vehicle hub, dropped by id), way/465683464 (a
    mezzanine, dropped), way/378955812; Bremen node/2562313294,
    node/21316810, way/26493594.
14. **The home-name lead is not read on a park or a garden:** Berlin
    way/666599487 and way/667618844 (dropped by id), relation/18772488.
15. **leisure=park on something that is no park** (a pool, a club, an
    office): Bremen way/237339879 and node/13460725211 (dropped by id),
    way/205954387; Zurich way/251217100, way/37380208.
7. **An exhibit admitted by its class's or kind's article.** Anyang
   way/829939487, 829939488, 829939493, 829939494, 829939495, 829939499,
   829939503, and way/829939489 (tourism=attraction, no historic tag).
   Dropped by id.
