# Search final group: the held rows settled and applied (2026-10-13)

The 1,699 rows the three read-only lanes settled by the existing rules
(`data/_search_rollout/final_held_settle/lane_1.tsv` to `lane_3.tsv` in the
Cleanup worktree; the Cleanup entry counts 1,698), with the owner's ten
rulings of 2026-10-13 on the new classes and the conflicts ("all approved"),
written into the configs of branch `search-final`. The entry in
`search-final.md` has the summary; this file has the counts and the lists.
A home, family or person row is cited by OSM id alone.

## Totals

- Lane rows: 657 drop, 884 keep, 117 new class, 41 unsure.
- **730 ids added to `PLACE_DROPPED`** in 27 cities, for 598 lane rows (479 places by their own id, 119 street names by every way that bears the name) and 6 same-named twins a drop promoted to a row.
- **931 records added to `PLACE_RULED_KEPT`** in 29 cities: every keep verdict (all 884 were rows a reader held), the 39 new-class rows the owner kept, and the 8 lane drops the rulings reverse.
- **61 rows left for the shared rule pass**, not dropped by id (`left_for_rules.tsv` beside the lane files).
- **41 rows unsure**, left in the index.
- 66 drop rows needed nothing: no row of their own in the built index already.
- Rows in the 29 rebuilt indexes: 256,955 to 256,360 (-595). No name gained a row, no kept row was lost, and every dropped id and street name is gone, checked against the committed index of a48922bb by `place_ids.json` and by name.

## By city

| City | Ids dropped | Lane rows dropped | Twins | Ruled keeps recorded | Left for rules | Unsure | Already no row | Rows before | Rows after |
|---|---|---|---|---|---|---|---|---|---|
| aarhus | 12 | 12 | 0 | 17 | 0 | 0 | 0 | 3,700 | 3,688 |
| bergen | 37 | 13 | 0 | 61 | 0 | 2 | 0 | 3,235 | 3,222 |
| berlin | 11 | 6 | 0 | 31 | 0 | 0 | 0 | 17,053 | 17,045 |
| brasilia | 76 | 66 | 0 | 27 | 11 | 3 | 0 | 14,762 | 14,699 |
| bremen | 17 | 1 | 0 | 31 | 0 | 0 | 0 | 5,588 | 5,587 |
| brussels_regional | 21 | 16 | 0 | 100 | 12 | 1 | 0 | 5,538 | 5,522 |
| bucharest | 51 | 26 | 3 | 17 | 1 | 2 | 2 | 6,509 | 6,483 |
| cluj_napoca | 5 | 5 | 0 | 19 | 0 | 1 | 0 | 1,481 | 1,476 |
| copenhagen | 9 | 9 | 0 | 54 | 0 | 0 | 0 | 6,522 | 6,514 |
| daugavpils | 1 | 1 | 0 | 2 | 0 | 0 | 0 | 613 | 612 |
| florence | 11 | 11 | 0 | 26 | 1 | 1 | 0 | 3,296 | 3,285 |
| geneva | 8 | 8 | 0 | 20 | 6 | 0 | 0 | 2,499 | 2,491 |
| goteborg | 8 | 7 | 0 | 16 | 0 | 2 | 0 | 6,639 | 6,632 |
| guadalajara | 66 | 54 | 1 | 89 | 9 | 10 | 0 | 27,488 | 27,434 |
| kitakyushu | 22 | 21 | 1 | 47 | 0 | 0 | 0 | 3,149 | 3,128 |
| liepaja | 4 | 4 | 0 | 1 | 0 | 0 | 0 | 489 | 485 |
| monterrey | 36 | 36 | 0 | 43 | 1 | 1 | 0 | 23,487 | 23,451 |
| most | 1 | 1 | 0 | 2 | 0 | 0 | 0 | 510 | 509 |
| odense | 0 | 0 | 0 | 17 | 0 | 0 | 0 | 2,371 | 2,371 |
| oslo | 33 | 33 | 0 | 32 | 0 | 1 | 0 | 4,785 | 4,752 |
| riga | 21 | 21 | 0 | 19 | 9 | 6 | 0 | 2,600 | 2,579 |
| rome | 36 | 27 | 0 | 48 | 0 | 3 | 4 | 19,287 | 19,260 |
| stockholm | 23 | 22 | 0 | 84 | 0 | 2 | 0 | 6,267 | 6,246 |
| taichung | 115 | 105 | 1 | 42 | 0 | 2 | 53 | 23,613 | 23,508 |
| taipei | 36 | 35 | 0 | 34 | 10 | 2 | 5 | 35,959 | 35,924 |
| taoyuan | 57 | 45 | 0 | 29 | 1 | 1 | 1 | 23,447 | 23,402 |
| thessaloniki | 9 | 9 | 0 | 10 | 0 | 1 | 0 | 1,917 | 1,908 |
| yamagata | 4 | 4 | 0 | 8 | 0 | 0 | 0 | 969 | 965 |
| zurich | 0 | 0 | 0 | 5 | 0 | 0 | 1 | 3,182 | 3,182 |
| **Total** | 730 | 598 | 6 | 931 | 61 | 41 | 66 | 256,955 | 256,360 |

A street name is one lane row and as many ids as it has ways, so ids exceed rows where streets were dropped (Guadalajara, Taoyuan, Bergen, Bremen). A duplicate that was a second row of one name leaves the name in the index, so rows fall by less than names would suggest.

## Drops by rule

| Class (the lane's rule, grouped) | Place rows | Street names |
|---|---|---|
| NEW: planning width codes on public streets (ruling 2) | 0 | 33 |
| NEW: a city programme's name on pocket parks (ruling 3) | 16 | 0 |
| NEW: religious offices, halls and residences tagged a place of worship (ruling 1) | 10 | 0 |
| NEW: historic route relations, wrecks, venue halls, prison chapels (ruling 4) | 17 | 0 |
| NEW: numbered microdistricts the lane singled out (ruling 5) | 2 | 0 |
| Bare type word or type phrase as the whole name | 210 | 7 |
| Duplicates, parts of one object, boundary and station doubles | 65 | 1 |
| Address strings and street names ending in a house number | 0 | 44 |
| Codes beside a type word, path codes, planning-code parks | 19 | 8 |
| Descriptions and inscriptions standing in for a name | 20 | 8 |
| Museum, zoo and building contents with no article | 9 | 0 |
| Housing and commercial developments mapped as places (ruling 6) | 24 | 0 |
| Homes and family compounds with no visiting and no article | 15 | 0 |
| Offices, societies and religious houses tagged a place of worship | 18 | 0 |
| Non-parks tagged a park, campus lawns, a non-notable garden | 24 | 0 |
| Businesses and private clubs | 7 | 0 |
| Rides and non-passenger stations | 8 | 0 |
| Public art, graves and objects admitted by another's entry | 8 | 0 |
| Street rules: ramps, mode lanes, corridors, site names, private, minor-way descriptions | 1 | 17 |
| Glitches, a thing that is not there, a city block as a neighborhood | 5 | 1 |
| Other: A library with no article of its own is dropped (owner 2026- | 1 | 0 |

Each config entry carries the lane's own `rule_or_ruling` text as its reason; a new-class entry carries the owner's ruling.

## Keeps by the rulings on new classes

- riga: 7, a numbered microdistrict of a large housing district is kept (owner, 2026-10-13)
- stockholm: 9, a park named for a city block is kept (owner, 2026-10-13)
- taichung: 10, a peak carrying a village's name is kept (owner, 2026-10-13)
- taoyuan: 13, a peak carrying a village's name is kept (owner, 2026-10-13)

## Where the lanes were not followed

- **Ruling 7** (a home tagged an attraction with a Wikipedia article of its own is kept): Bergen way/431495717 and Brussels way/241553744, dropped by lane 1 on the German precedent, are recorded as ruled keeps.
- **Ruling 8** (same-named parks more than 300 m apart are two rows): six parks the lanes dropped as a second drawing just past the 300 m merge are kept and recorded:
  - geneva: Parc des Molliers (way/118190141): 300 m from the other way of the name
  - guadalajara: Zona turistica Parian de San Pedro Tlaquepaque (way/597015961): third drawing of the same zone, 311 m from the nearest, so a second row
  - kitakyushu: 勝山公園 (way/1124048009): second drawing of one park, just past ROW_MERGE_M (300 m)
  - kitakyushu: 東田大通公園 (way/1055572497): second drawing of one park, just past ROW_MERGE_M (300 m)
  - kitakyushu: 皇后崎公園 (way/675806191): second drawing of one park, just past ROW_MERGE_M (300 m)
  - taoyuan: 五酒桶山風景區 (node/5823960472): a node 325 m from the area of the same name
- **Twins added.** Six ids the lanes did not list were dropped with the row they share a name with, because the first drop made the twin a row (found by comparing `place_ids.json` before and after):
  - bucharest: node/11259913599 (Tun), twin of node/11259913598
  - bucharest: node/1725768053 (Tunuri), twin of node/1725768052
  - bucharest: node/1725768054 (Tunuri), twin of node/1725768052
  - guadalajara: way/1492272252 (Astas), twin of way/1492272251
  - kitakyushu: way/858485720 (間島), twin of way/858485719
  - taichung: node/2571584094 (赤嵌頭), twin of node/2571583892
- **Guadalajara, two ways the lane named whose street name is an alt_name:** way/148901928 (own name a bare number, the corollary of the house-number ruling) and way/151679080 (own name a code beside a type word, its twin already dropped). Both dropped by id as the lane has it.

## Not applied, and why

- **Carried only by an alt_name, cannot be dropped by way id** (the way's own name is another street):
  - brasilia: "Edf Marginal Df480": way/159385483 (own name 'Residencial Pomares'); way/1144590362 (own name 'Residencial Pomares')
  - brasilia: "Edf Nucleo Rural Capão Comprido Chácara Flengo Nurmero 7": way/133863040 (own name 'Capão Comprido Chácara 4 Quadra 2 Rua 11'); way/1004114198 (own name 'Capão Comprido'); way/1004114199 (own name 'Residencial Capão Comprido Quadra 2 Rua 18'); way/1004116501 (own name 'Rua 8 Chácara 61')
- **Already no row** (a rule or a merge took it since the read):
  - bucharest: 2, already no row of its own (a rule or a merge took it)
  - rome: 4, already no row of its own (a rule or a merge took it)
  - taichung: 53, already no row of its own (a rule or a merge took it)
  - taipei: 5, already no row of its own (a rule or a merge took it)
  - taoyuan: 1, already no row of its own (a rule or a merge took it)
  - zurich: 1, street name is no row already
  Taichung's 53 are the bare shrine words the third pass's list already takes.

## Left for the shared rules

Not dropped by id; written with every lane column and a reason to `data/_search_rollout/final_held_settle/left_for_rules.tsv` (Cleanup worktree), as evidence for the rule pass.

| City | Class | Rows |
|---|---|---|
| brasilia | a facility of an apartment estate or mall tagged a park or square | 1 |
| brasilia | a place of worship named only by a denomination, a hall type or a church chain | 10 |
| brussels_regional | a place of worship named only by a denomination, a hall type or a church chain | 12 |
| bucharest | a place of worship named only by a denomination, a hall type or a church chain | 1 |
| florence | a place of worship named only by a denomination, a hall type or a church chain | 1 |
| geneva | a place of worship named only by a denomination, a hall type or a church chain | 6 |
| guadalajara | a facility of an apartment estate or mall tagged a park or square | 8 |
| guadalajara | a place of worship named only by a denomination, a hall type or a church chain | 1 |
| monterrey | a place of worship named only by a denomination, a hall type or a church chain | 1 |
| riga | a place of worship named only by a denomination, a hall type or a church chain | 9 |
| taipei | a place of worship named only by a denomination, a hall type or a church chain | 10 |
| taoyuan | a facility of an apartment estate or mall tagged a park or square | 1 |

**Bare type words: none left, 217 applied by id.** The instruction was to leave a bare-type row for the rules where the lane's note says the shared rule should have caught the word. No lane note says so (most are empty), so each went by id, as the fallback said. They are listed in `bare_type_applied_by_id.tsv` beside the lane files: a word the rule pass adds to a list makes its ids here redundant, and they can be removed then.

## Unsure rows, left in the index

- bergen: Åsane kirke (way/381377378): a church building named Åsane kirke 900 m south of the 1993 church that stands beside Åsane gamle kirke's row; the label of its Wikidata entry Q15964130 would say which church it is
- bergen: way/469522633: a park whose name reads as a given name; leisure=park and the name are its only tags; whether it is an official place name would decide
- brasilia: node/6556105487: a place of worship whose name carries a person's name and nothing else is tagged; whether it stands at a home would decide
- brasilia: Brasília (node/303847107): railway=station with an article of its own and no passenger tag; a source on whether any passenger train calls there would decide
- brasilia: Infraero (node/4949885122): a company's name on a historic=monument node; what stands there is not tagged
- brussels_regional: Le Thé au Harem d’Archi Ahmed (way/239903636): a heritage building under what reads as a film's title; the regional inventory entry (ref:UrbIS 6087664) would say what it is
- bucharest: Cotroceni (way/23557177): palace grounds tagged a park with access=no, under the suburb's bare name; the home test reads access=private only; whether the grounds are open would decide
- bucharest: Parcul Sala Palatului (way/125447897): a park with access=no and no note; whether the closure is for good would decide
- cluj_napoca: Disp. Tram CUG (node/1870509058): a tram stop node named as a dispatcher point, not a station of the map; the operator's stop list would say whether passengers board there
- florence: Giardino vittime di via Fani (way/763779020): a second park of the name 520 m from relation/19357489; the commune's place-name list would say which area bears it
- goteborg: Sidovägen (way/113805280): two service ways; 'the side road' may be generic or a real name; the municipal street register (NVDB name) would decide
- goteborg: Stigvägen (way/26747514): one footway; reads as a Swedish street name but may be generic; the municipal street register would decide
- guadalajara: node/2810167115: place=locality with a hacienda name and no other tag; a visiting tag, an article, or a census locality of that name would decide
- guadalajara: Antiguo Pueblo de Arcediano (node/14005560287): place=town, population=0, name says former village; the lifecycle rule reads only abandoned or demolished flags, which are absent
- guadalajara: 20 de Noviembre (way/1373216727): six ways are one river row; nothing in the tags says whose name it is; the channel's official name, or a street of that name running along it, would decide
- guadalajara: 20 de Noviembre (way/1373216728): six ways are one river row; nothing in the tags says whose name it is; the channel's official name, or a street of that name running along it, would decide
- guadalajara: 20 de Noviembre (way/1373216730): six ways are one river row; nothing in the tags says whose name it is; the channel's official name, or a street of that name running along it, would decide
- guadalajara: 20 de Noviembre (way/1373216731): six ways are one river row; nothing in the tags says whose name it is; the channel's official name, or a street of that name running along it, would decide
- guadalajara: 20 de Noviembre (way/1373216732): six ways are one river row; nothing in the tags says whose name it is; the channel's official name, or a street of that name running along it, would decide
- guadalajara: 20 de Noviembre (way/1373216733): six ways are one river row; nothing in the tags says whose name it is; the channel's official name, or a street of that name running along it, would decide
- guadalajara: José Cuervo Express (way/149816275): railway=station named for a tourist train brand, no usage or network tag; usage=tourism (a ride) or a regular passenger service would decide
- guadalajara: way/291224426: a park named with two people's names; cited by id; an official park register would decide
- monterrey: Pablo G. Garza (way/1319957016): monorail station with no construction or opening tag, not on the map; its line's other stations carry construction=yes; the operator's list of open stations would decide
- oslo: way/756392960: historic=building with a nickname and no other tag; whether it is a dwelling or open to visit would decide
- riga: Bērnu (node/4511175479): a bare genitive on a locality node; nothing says what it names; a look at the place would decide
- riga: Ezerkrastu (node/4511175480): a bare genitive on a locality node 240 m from the one above; same
- riga: Vecā grunts (node/4511175481): a locality of the same cluster; nothing says what it names
- riga: A-B dambis (node/3106207722): a letter pair beside 'dam' reads as a code, but it may be the dam's signed name; a check of local use would decide
- riga: way/904308294: a park named as a villa's garden, the villa named for a person: cited by id; an access tag or the city's park list would decide
- riga: Volvo sporta centrs (relation/12857963): a brand-named sports center tagged a stadium; an operator or commercial tag would decide
- rome: Happy Family (way/589782512): a park with nothing but a name that reads as a business; an operator or commercial tag would decide
- rome: Laghi del Salice (node/1250242025): a park node with nothing but a name that reads as fishing lakes; same
- rome: set Ben Hur (way/889382373): a film set tagged a fort; whether it stands is not in the tags
- stockholm: Crawl Space (way/733417529): reads as an artwork's title on a park; an artwork tag or the city's art register would decide
- stockholm: Pelarsalen (node/5026949256): a hall name on a locality node; no tag says what it is
- taichung: 楓之谷-1956祕密花園 (way/510333828): a paid garden by its name, with attraction nodes inside it; a fee or operator tag would decide
- taichung: 星夢谷 (way/909825777): tagged a place of worship with no religion; the name does not read as a temple
- taipei: 百事可問 (node/6090305171): tagged a place of worship with no religion; may be a fortune-telling business; a religion tag or a look would decide
- taipei: 財神會館 (node/9748205713): tagged a place of worship with no religion, 2 m from a temple node; same
- taoyuan: 平鎮 (node/14244739700): railway=station on the national network, no lifecycle tag, no article; the operator's station list would say whether it is open
- thessaloniki: 27ου Δημοτικού Σχολείου: one pedestrian way, no addr:street use in the cache; a street sign or an address would decide

## Flags for Cleanup

- **Cluj-Napoca's "Micro 1" to "Micro 4"** went by the lane's verdict (a code beside a type word). The lane's own note says such names can be everyday district names in Romania; ruling 5 kept Riga's numbered microdistricts. Applied as the lane has it; one line to reverse if the owner reads them as Riga's.
- **Bucharest node/672149975** (the monastery's node, dropped as a duplicate 10 m from the church way that shares its article): the church way keeps its row under the church's name, so the monastery's own spelling is no longer a row. Applied as the lane has it.
- **Rome node/1619249491** (Roma Casilina, railway=service_station, an article): dropped as a station not for passengers on the tags alone; the lane notes a timetable check would confirm.
- **Copenhagen's København Syd** keeps two rows after the S-train node went: the mainline node and the Metro node (its own Wikidata entry), which the S-train node had been standing for. Østerport reads the same way. An interchange stays two rows.
- **Taipei way/547156822** is a live row named only by the library type word and is in no lane file (the three the lane listed were no rows already). Not touched.
- **`docs/place_search_exclusions.md` owes rows** for the classes dropped by id here for the first time (religious offices, planning width codes, a programme's name, historic route relations, underwater wrecks, venue halls, prison chapels). Not written on this branch: the rule pass is editing that file.
- **`PLACE_RULED_KEPT` grew from 85 to 1016 records** that no code reads. A row recorded there is not shielded from a later rule (finding 51 stands).

## Checks

- `python scripts/check_place_search.py`: 32 problems, rule A on each of the 32 cities (an index no map uses yet), nothing else.
- `python scripts/check_no_em_dashes.py`: OK.
- 29 indexes rebuilt through `scripts/heavy_job.py` (three at once, `HEATMAP_NO_NETWORK=1`), four of them twice for the twins. No cache written, no network request by a step.
- Every id acted on was checked in the city's two caches first: all present. Odense and Zurich changed in config only (records); their indexes are byte for byte the same.
