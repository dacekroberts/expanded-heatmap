### 2026-10-13 - Seven languages ruled; Monterrey's colonias kept; eleven cities rebuilt on master's second rule batch (branch search-final)

- **The owner, to the eleven language calls: "1. yes 2. yes. 3. yes. 4.
  yes. 5. yes. 6.yes. 7. 35 in like you said. 8. drop by id. 9.
  recommendation ok. 10. yes and test. 11. yes."** In the order asked:
  1. The English leak word "store" is set aside for Danish, Norwegian and
     Swedish, where it means "big" (Danish 18 rows lost, 13 of them streets
     such as Store Kongensgade; Norwegian 4 per city; Göteborg's Store udd).
     A shared-code change, so a finding for Cleanup.
  2. Farm and yard endings: Swedish -gård and -gården in with an id catch
     as German -hof has (67 rows, 5 not streets); Norwegian -gården in;
     Danish -gård out on its measured misfires.
  3. Home words that take heritage houses are in (Romanian "casa", 97
     landmark rows, 80 in Cluj-Napoca; Greek home leads, 2 rows), a house
     kept when it has an article of its own.
  4. Norwegian terrain endings in (-lia, -lien, -toppen, -grenda, -grenden,
     -tunet, -jordet, -kollen, -berget, -haugen, -gården): 49 rows, 1 not a
     street.
  5. Norwegian historic farms are held to the home rule: dropped until
     visiting is shown (Oslo: 64 landmarks ending in "gård", 54 with no
     Wikidata entry).
  6. Swedish -gång (235 rows, 1 misfire), -faret (11) and -lycka (14) in;
     -spår out.
  7. Danish field endings in, the ten measured (35 rows); -gang out.
  8. Riga's 19 numbered garden lanes and 3 station tunnels dropped by id;
     the Daugavpils fortress's ten numbered bastions kept.
  9. Italian: "villa" and "casa" stay out as home words (94 rows, 48 of
     them Roman ruins), "villino" in; "arco" and "belvedere" in; "galleria"
     out.
  10. Greek name endings as the street test: in, and tested (every row the
      endings admit read, the names they do not admit read, and the share
      they would match on non-streets measured).
  11. Romanian "pasajul" in, "pasaj" out.
- **The settled lists** go to `docs/decisions_drafts/search-lang-<code>.md`
  for `da`, `nb`, `sv`, `lv`, `ro`, `it`, `el`, each with its measurements,
  as German's did.
- **Monterrey's 19 colonias are kept by id (owner: "yes for monterrey").**
  Named neighborhood areas drawn on residential land, several from the
  municipal Plano de Colonias; the estate rule drops them. Written to
  `PLACE_KEPT`; the rows appear once that setting reaches the estate rule
  in Cleanup's third pass. Polanco and Del Maestro survive through another
  object and need no entry.
- **Master 4c89e15b merged (e96f8ab7) and eleven cities rebuilt** (the nine
  of the entry below, Anyang and Gwangju). `check_place_search.py` fails
  only on rule A (no map yet) and on two street names waiting for the
  owner: Taoyuan 停車場路, Monterrey "Calle Hotel Río".

Findings for Cleanup:

- **Candidate 6 was not taken by the station-outline rule:** Gwangju
  way/1442542051 is still a row after the rebuild.
- **Candidate 27 traced.** Sendero (node/1041636979, way/1286342563) is in
  `STATIONS_CSV` and is dropped by the station rule's bare-type branch:
  "sendero" is a Spanish bare type word and neither object carries a
  wikidata or wikipedia tag. The colonias are 21 ways in the extra cache
  under `place_dropped_estate`.
29. **A leak word of one language is a plain word of another** ("store").
30. **Florence's limited-traffic zone** (access=no, motor_vehicle=permit,
    foot=yes) loses 55 public streets to the private-street rule.
31. **Greek final sigma is not folded in `norm()`:** 726 names.
32. **`int_name` is not read:** Thessaloniki 44.1% of rows carry one.
33. **In a suffix language `_named_street` asks the way word as the whole
    last word,** so a glued name never passes (Danish, German, Dutch).
34. **A home-name ending is needed** where the house word comes last
    (Latvian "villa", Norwegian "gård").
35. **Romanian cedilla letters want folding to the comma forms:** 19 names.
36. **Second-language names below the declared floor are not searchable:**
    Cluj-Napoca's Hungarian (39.8% of rows), Daugavpils' Russian (15.5%).

### 2026-10-13 - Nine cities built on existing lists and read; Brussels (Regional) is 18 communes, not 19 (branch search-final)

- **Correction to the boundary entry below: Brussels (Regional) takes 18
  communes.** The session recommended all 19 and the owner agreed, and that
  was wrong. This map is cut to the communes outside the City of Brussels,
  which has its own page and index. The fetch's scope stop refused relation
  58274 (no station of this map inside it); the area was narrowed to the
  other 18 and refetched. The owner was told in chat.
- **Built and read on the lists already in `place_index.py`:** Taipei (with
  New Taipei), Taichung, Taoyuan (`zh`); Kitakyushu (`ja`); Brasília (`pt`);
  Monterrey, Guadalajara (`es`); Geneva (`fr`); Brussels (Regional) (`fr`,
  `nl`). Stations, places and landmarks were read by the place-read agent
  on the top model, streets screened on sonnet. Each reader wrote clear
  drops under a settled call to one file and everything else to a pending
  file; only the first was applied.
- **Dropped by id from the reads** (homes, businesses, descriptions,
  glitched names, duplicates, public art and plaques with no article, codes
  beside a path type on minor ways): Taipei 468, Taichung 143, Brasília 130,
  Guadalajara 123, Taoyuan 120, Brussels (Regional) 116, Monterrey 70,
  Geneva 28, Kitakyushu 16. Brussels' count includes 42 cemetery lanes
  named by an ordinal ("10ème Avenue - 10ème Laan"), dropped as a code
  beside a type on a minor way, and 25 slash-joined doubles of a street
  that has a clean row.
- **Held back by the session, not dropped, though a reader listed them:**
  - Monterrey "Basílica de": the Basílica del Roble under a cut name.
    Dropping it removes a major church.
  - Kitakyushu "遠賀川 (Onga River)", three ways: English glued on, but the
    river has no clean row.
  - Brasília "Primeiro Avenida" and Kitakyushu "新導寺曽根線": a typo on a
    real road is still that road.
  - Guadalajara: 273 street names the reader took for address numbers
    ("Abeto 1300") without checking a way, five park names with a typo and
    seven cut names.
- **Reviewed, kept under `PLACE_REVIEWED`:** Taoyuan's Airport Hotel metro
  station and an air-crash memorial; Brasília's Shopping station; six
  Taipei rows with their own articles; Geneva's Chemin de l'Auberge; in
  Brussels (Regional) four real streets (Brasserie twice, Clinique, Hôtel
  des Monnaies), that metro station and two town halls; Guadalajara's
  "Calle G.U.S.A.".
- **Classes no settled call covers wait for the owner** in each city's
  pending file: bridges as street rows, motorway ramps, planning-code
  parks, family compounds and farmhouse ruins with no article, estates
  tagged hamlets or parks, private streets inside gated estates, campus
  and cemetery numbered roads, shopping galleries, municipal road codes.

Findings for Cleanup (shared code; nothing edited here), rule candidates 19
onward:

19. **The Chinese bare-type list is short.** Earth-god shrine words as a
    whole name (土地公廟, 福德祠 and kin): Taoyuan about 203 rows, Taichung
    157, Taipei 263.
20. **A metro station's outline way enters as a second station row.**
    Brussels (Regional) 10 (dropped by id). Same shape as candidate 6;
    Hôtel des Monnaies' outline is that station's only row and stays.
21. **The way-word test is skipped for `highway=pedestrian`, busway, escape
    and dummy values.** Brasília.
22. **A bare word already in the lists gets through on a bilingual or
    article-led name** (Château, Donjon, Aqueduc, Totem, 本殿). Brussels
    (Regional), Geneva, Kitakyushu.
23. **A name of two street names joined by " / ".** Brussels (Regional) 41
    rows; 36 are one street in two spellings.
24. **An ordinal or number beside a type as the whole name** ("Avenue 1",
    "10ème Avenue"): Brussels (Regional) 60 rows.
25. **A name whose every way is `access=private`:** Brussels (Regional) 11
    names; Guadalajara 2,423 names inside gated cotos (13% of its streets).
26. **Estate amenities tagged `leisure=park` in Spanish:** Guadalajara
    "Terraza" 28 rows, "coto" 25, "Cluster N" 9, "Casa Club" 6, "Camellón"
    6; `amenity=letter_box` carrying a place tag 6.
27. **Monterrey: the Sendero station is missing from the index, and
    neighborhood ways carrying `landuse=residential` are dropped** though
    they are real colonias.
28. **River rows have no id in `place_ids.json`,** so a river cannot be
    dropped or kept by id.

### 2026-10-13 - Berlin: Gärten der Welt's small plots and courtyards dropped, the Kleistgrab kept (branch search-final)

- **The owner: "1. yes real name and drop small plots. 2. keep as
  attraction".** Inside Gärten der Welt the gardens with a name of their
  own stay (Chinesischer Garten, Orientalischer Garten, Christlicher Garten
  and the rest). Dropped by id: the five plots named only for a country
  (way/524037019, way/524037023, way/524037022, way/1042056230,
  way/501358054) and three courtyards drawn as localities (way/1042056279,
  way/497734026, way/497734021).
- **The Kleistgrab (node/639131685) stays** as a tourist attraction, though
  its article link is a section of another article and the grave rule alone
  would drop it. A grave that is tagged an attraction and is a known sight
  is kept on the owner's word, per city; no rule is asked for.

### 2026-10-13 - The boundaries for the last 24 cities; the smaller German items answered by precedent (branch search-final)

- **The owner, to the six boundary calls: "1. yes sounds good. 2. whole
  cities and new taipei for taipei. 3. yes. 4. yes. 5. yes. 6. yes".** Each
  of the straightforward cities takes its own municipality: Aarhus 1784663,
  Odense 2178124, Riga 13048688, Daugavpils 13048683, Liepāja 13048685,
  Bergen 404159, Stockholm 398021, Göteborg 935611, Bucharest 377733,
  Cluj-Napoca 3277038, Rome 41485, Florence 42602, Thessaloniki 1770680,
  Brasília the Federal District 421151, Kitakyushu 4008600. Taiwan takes
  whole cities: Taichung 2921154, Taoyuan 2770986, Taipei 1293250 with New
  Taipei 1527220. Brussels (Regional) takes the Region's 19 communes.
  Geneva takes the twelve communes a drawn station sits in. Copenhagen
  takes ten kommuner, Monterrey four municipios and Guadalajara four, each
  the ones holding a station. Oslo is 2775550 alone: the extract lookup
  puts every drawn station inside Oslo kommune, so Bærum is not added.
- **Scaffolded from one plan and fetched by the extract route.** Language
  codes: Norway `nb`, Taiwan `zh`, Brussels `fr` and `nl`. Kitakyushu's
  outline crosses two regions, so it is read from the Kyushu and Chugoku
  files of one dated run together.
- **The owner on the smaller items from the German reads: "if there is
  precedent to answer answer them, if not bring to me with
  recommendations".** Answered by a settled call:
  - Eleven more bare type words into the German list (26 rows; the list is
    in `search-lang-de.md`): a whole name that is only a type word.
  - Two graves with no article of their own, dropped by id: Berlin
    node/286472713 (on its subject's article) and node/925074789. The
    owner's rule for graves and plaques.
  - Two pools and a minigolf course tagged parks, dropped by id: Bremen
    way/205954387, Zurich way/37380208 and way/251217100. No pool or course
    is admitted by its own class; these came in on a wrong park tag, as the
    office and the club address already dropped in Bremen (candidate 15).
  - Two re-erected buildings in the Focke-Museum's grounds, on the museum's
    article, dropped by id as museum contents: Bremen way/162241218,
    way/207930409.
  - Bremen's 22 facade ornaments are artworks with no article: rule
    candidate 16 takes them, nothing by id.
  - Zurich's service roads closed to vehicles and open on foot stay: the
    private-street rule reads `access`, and these are in the street
    register.
- **Brought to the owner, no precedent:** the garden plots and courtyards
  inside Berlin's Gärten der Welt; the Kleistgrab, a grave that is a
  tourist attraction and sits on a section of another article.

### 2026-10-13 - German way words: -eck in, with an id catch (branch search-final)

- **The owner, to the one call left from the Berlin measurement: "add, note
  the id catch".** -eck joins the German way words (40 words). It adds 6
  street rows today, 3 in Berlin (Lilieneck, Poseidoneck, Siedlers Eck) and
  3 in Bremen, all lane names by their look.
- **The id catch:** -eck can also end a corner cafe's or a building's name
  on a footway. None is in an index today; one that a later edit brings in
  is dropped by id. When a German city's cache is refreshed, list the
  minor-way street rows ending -eck that are new since the last read, the
  same watch as -hof (`search-lang-de.md`).
- -gang and -moor stay out.

### 2026-10-13 - The owner's eight answers on the German reads; Berlin and Bremen drops; Low German endings measured on Berlin (branch search-final)

- **The owner, to the eight calls put after the reads:** "1. yes article
  needed. 2. keep these. 3. yes drop as code plus type 38 on minor ways
  okay. 4.keeping named public trails is GOOD yes. 5. drop those 50 besides
  the article ones. 6.drop until visiting. 7.leave as is. 8. agree with
  your recommendations and berlin measurement".
- **1, public art needs a Wikipedia article of its own.** Not applied here:
  it is a rule in `place_index.py` and changes the 19 live cities, so it is
  rule candidate 16 for Cleanup, with a changed-row report owed at the
  fold. Measured on this group: 1,048 of Berlin's 1,111 artworks and 171 of
  Zurich's landmarks are in on a Wikidata entry alone. The cost the owner
  accepted: a real sculpture with no article leaves too.
- **2, allotment lanes stay** (about 600 Bremen street rows, Berlin's
  flower-named paths): nothing in the data separates them from footpaths.
- **3, Berlin's coded path names dropped by id:** 79 names, 227 ways, 173
  street rows, every way a footway, path, service road or track: "Weg N"
  and "Weg X" (42 names), "Querweg N" and "3. Querweg" (16), "Stichweg X"
  (13), "Ring I" to "IV" (4), "Fußweg N" (3), "Nebenweg 1". Kept: the 144
  "Straße N" names on real roads and the 37 on minor ways (owner), "Weg A"
  and "Weg B" (each has a residential way), six "Weg N (Hasenweg)" names
  that carry a real name, the numbered Yorckbrücken, "Volksgartenweg 1" to
  "6" and "Pfuhlweg I" and "II" (a name plus a number, not a code plus a
  type). Rule candidate 17.
- **4, named public trails stay; a trail named by a description goes**, as
  already done by id. This settles the same open point for Anyang and
  Gwangju.
- **5, Berlin's dead railway alignments:** 28 ids dropped (railway or
  lifecycle-prefixed abandoned, disused or razed, no `wikipedia` tag on the
  way). Kept: the 18 ways that carry an article (Siemensbahn 9, Bötzowbahn
  5, Industriebahn Tegel-Friedrichsfelde 3, Neukölln-Mittenwalder Eisenbahn
  1). Also kept, as standing structures and no alignment, and so outside
  the ruling: three water towers, the AEG-Versuchstunnel and a tank loading
  ramp; told to the owner. The 50 put to the owner counted the article
  ways and these five. Rule candidate 18.
- **6, five homes tagged attractions dropped until a web check shows
  visiting:** Berlin way/8080757 (Corbusierhaus), way/112149783 (Kreuzberg
  Tower); Bremen way/162130229 (Aalto-Hochhaus), way/167729560 (Gut
  Landruhe), way/162235078 (Villa Borgward).
- **7, Bremen's Bremerhaven exclave stays** in the area, its 4 rows with it.
- **8, Low German endings:** -deich, -pad and -pforte into the German way
  words; -gang, -eck and -moor out. Berlin measured after the ruling:
  the three accepted endings add no name there, -gang adds 19 of which 13
  are no street name, -eck adds 3 that look like lane names, -moor none.
  Figures in `search-lang-de.md`.
- **After this round, built in memory:** Berlin 18,268 rows (12,985
  streets, 3,810 landmarks), Bremen 5,645 before the endings' 21 street
  rows. Still no German index on disk.

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
16. **Public art needs a Wikipedia article of its own (owner,
    2026-10-13).** tourism=artwork in on a `wikidata` tag alone: Berlin
    1,048 of 1,111 artwork rows, Zurich 171 landmark rows; Bremen and
    Gelsenkirchen not counted. Changes the live cities, so it needs a
    changed-row report. Nothing dropped by id for it.
17. **A code beside a path type on minor ways only** ("Weg 5", "Stichweg
    A", "Querweg 12", "Ring II"; owner, 2026-10-13). Berlin: 227 ways of 79
    names dropped by id, the entries whose reason reads "a code beside a
    type on minor ways". Not "Straße N", which is a real Berlin street name
    on any class of way.
18. **A dead railway alignment with no article of its own** (railway or
    abandoned:, disused:, razed:railway of rail on a way, no `wikipedia`
    tag; owner, 2026-10-13). Berlin: 28 ids dropped. A lifecycle tag on a
    standing structure (a water tower, a tunnel) is not this class.
7. **An exhibit admitted by its class's or kind's article.** Anyang
   way/829939487, 829939488, 829939493, 829939494, 829939495, 829939499,
   829939503, and way/829939489 (tourism=attraction, no historic tag).
   Dropped by id.
