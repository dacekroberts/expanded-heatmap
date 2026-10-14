### 2026-10-13 - Search rollout: the final shared rules merged, every city rebuilt once, twin rounds, reach reasons (branch search-rollout)

- **Merged the integration branch at 73f025df (77371e8a, `--no-ff`, no conflict in any file), then rebuilt 168 of the branch's 170 searched cities,** each by its own index step, four runner processes through the cleanup worktree's gate, every child with `HEATMAP_NO_NETWORK=1`. Selftest 311 of 311. No request of any kind, nothing rendered, nothing pushed, no shared code edited. The merge's regeneration rewrote `app/macro_facts.json` for Mexico City again (the tram rescope's data on the shared disk) and that rewrite was put back. The record is `data/_search_rollout/extract_rules56/final_rebuild.md` (on disk only), with `final_lists/<city>.tsv` and the rounds' twin lists.
- **Not rebuilt, both another lane's:** Mexico City's step stops on San Isidro (the dated known gap of check H). Prague was rebuilt and put back to the merge's index: its committed index is older than the article rule, and a rebuild takes 375 rows by rule (292 works of public art and 11 libraries with no article among them) and adds 16; the list is `prague_if_rebuilt.tsv`.
- **Rows across the 170, before to after:** stations 10,360 to 10,297; junctions 24,410 to 24,409; landmarks 123,151 to 120,715; places 82,110 to 81,945; streets 524,599 to 524,585; intersections 1,078,725 to 1,078,710. Removed by id 2,755; removed by rules 47 (29 platforms merged into their stop, 10 stop names that were streets in Ostrava and Liberec, the sea roads by way id); added by rules 99 (51 stations of different names no longer folded on a shared Wikidata entry, about 30 squares returned where the street row beside them bears another name, Brno's 8 boroughs); added by keeps 24.
- **Twin rounds: 222 same-named neighbours dropped by id in 47 cities over 13 rounds; round 14 found none.** A twin is a row new against the pre-rebuild index with the kind and name of a row a `PLACE_DROPPED` id removed; each went under the class of the row it replaced, in its config under a "Twin round N" comment. Lille 60 (Immeuble, Immeubles, Maison, Maisons on a register's nodes), Belo Horizonte 29 (the cableway's pylons, ruling 21), Salvador 24. Kept, 11: the survivor where the dropped row was a second row of one object. Antwerp's Groenplaats came back as two rows for one dropped.
- **Owner rulings applied with the rebuild (2026-10-13):** Sapporo's 山麓 (node/1781191908, the Mount Moiwa ropeway's base station) kept by id, now a station row. Two sea labels dropped by id: Kochi's 土佐湾 (node/13339743364) and Fukuoka's 玄界灘 (node/6355776632).
- **`PLACE_SCOPE_REACH_REASON` written in 17 configs,** one dated sentence each, for rule D of `check_place_scope.py` (branch search-scope-check; not on this branch yet), each city's reach measured on its rebuilt index with that rule's own code: Incheon 179.6 km, Shizuoka 67.6, Palma 56.4, Sasebo 51.4, Rio de Janeiro 46.1, Ansan 41.6, Daegu 40.7, Toyota 39.7, Fukuoka 37.7, Hakodate 33.0, Morioka 28.6, Porto Alegre 28.3, Sapporo 28.2, Matsumoto 27.0, Toyama 27.0, Nagasaki 26.5, Salvador 26.2. None for Kochi (12.6 km) or Naha (3.2 km).
- **Four `PLACE_REVIEWED` entries removed** (Grenoble, Iwaki, Kurashiki, Orléans): each named a row a reader's id has since dropped, and check E called each stale.
- **Confirmed:** no id in any `PLACE_DROPPED` is still a row. Of the 48 `PLACE_KEPT` ids on the branch 46 have a row; Kochi's はりまや橋 (node/5099545223) is findable under the tram stop's row of the same name and has no landmark row of its own, and Seattle's second "Large Lock" way is folded into the first. The four sea roads are gone (Naha, Nagasaki, Kagoshima two); Oita's 国道197号（海上区間） is still a street row, named by no ruling. Nagasaki's node/4448589490 and node/1423804998, Ichikawa's 里見公園 and Belo Horizonte's node/7051900020 are rows. Returned stations: Toyama's 電鉄富山, Nagasaki's 浦上, Kobe's 三宮, Kagoshima's 鹿児島. Still missing: Montpellier's Saint-Denis (node/3127521470, `public_transport=station` alone).
- **Checks:** `check_place_scope.py` OK. `check_place_search.py`: rule A on the 151 unrendered cities, and "the map's index URL is stale" on 17 live cities whose indexes this rebuild changed (they want the one render); E clear; Mexico City the known gap.
- **Not done:** no render, no browser test, no eye read of the twins' replacements beyond the lists.

### 2026-10-13 - Search rollout: Mendoza's searched area corrected from the province to its department (branch search-rollout)

- **Mendoza's index covered Mendoza Province, not the city.** The scaffold had set `PLACE_AREA` to relation 153540 (admin_level 4, the province of the same name), found by Mendoza's reader: 653 peaks and 155 rivers out to Malargüe and Aconcagua. Set to relation 2204157, Departamento Capital (admin_level 5), which holds all seven stations and is the boundary the map's businesses are cut to. Read from the lookup cache already on disk (`data/mendoza/raw/osm_place_area_lookup_2026-10-13.json`, the extract route), so no lookup was run again.
- **New caches under new names, from the held Argentina extract (`argentina-261012.osm.pbf`), no download, no Overpass:** `osm_places_v2_2026-10-13.json` (9,654 elements) and `osm_places_extra_v2_2026-10-13.json` (65). The province's caches stay on disk under the old names. The outline cache has one fixed name: the province's was copied to `osm_place_outline_v1_province_2026-10-13.json` and then replaced (approved for this one city).
- **Wikidata: nothing asked.** The old cache was copied to `wikidata_articles_v2_2026-10-13.json`; it holds both ids the new area asks about.
- **Rows before to after:** stations 81 to 7; landmarks 1,688 to 119; places 926 to 20; streets 9,775 to 623; intersections 26,922 to 1,884. The seven stations are the map's seven.
- **`PLACE_REVIEWED` emptied:** its three hotel ruins lay in the province and are no longer rows; check E named each as stale.
- **Why `check_place_scope.py` passed it:** rule B only refuses a named area with no station inside, and the province holds all seven; nothing asks whether a smaller boundary would hold them. A cheap test, not built (shared check): the index's reach beyond the stations' bounding box, or the area's admin_level against the business boundary's.
- **The same screen run on every searched city, nothing changed** (`data/_search_rollout/extract_rules56/scope_screen.tsv`, 170 cities): 18 indexes reach more than 25 km beyond their stations on some side. Each names the city's own municipality: a wide municipal territory or its islands (Incheon 176 km, Shizuoka 58, Sasebo 51, Palma 50 with Cabrera), not a wrong boundary. Naha (239 km), Nagasaki (79) and Kagoshima (64) owe their reach to one street row each, the sea section of a national highway (国道390号, 国道499号, 国道58号 "海上区間"), a row for a reader or a rule.
- **The reader's verdicts on the province-wide index** (`data/_search_rollout/reads_rules56/mendoza.tsv`, 40 drop, 52 unsure): 3 drops and 1 unsure are still rows (Iglesia Adventista Séptimo Día node/2443028624, Templo Evangelico Metodista way/255485266, Hermanas de Nuestra Señora de la Caridad del Buen Pastor node/3639401230; unsure Jardines Dalvian relation/21131495).
- **Checks:** `check_place_search.py` fails Mendoza on rule A alone; `check_place_scope.py` OK. Not rendered, nothing pushed.

### 2026-10-13 - Search rollout: the extract run's 151 cities rebuilt on rule passes 5 and 6 (branch search-rollout)

- **Merged master at e0138000 (3ca0fa0f, no conflict), then rebuilt all 151 indexes, each by its own index step, from the place caches on disk.** Two runner processes through the job gate, disjoint halves, one city at a time each, every child with `HEATMAP_NO_NETWORK=1`. No extract, Overpass or Wikidata request; nothing rendered, nothing pushed, no shared rule code edited, no by-id drop or keep added. The record is `data/_search_rollout/extract_rules56/` (on disk only): `summary.md`, `summary.json`, one `<city>.tsv` per changed city, the build logs and the check logs.
- **Wikidata: no city had an id to ask.** Each city's ids were counted against its cache before anything ran, by the fetch script's own `collect_ids`. The 118 caches hold every id the rules ask about; the 33 cities with nothing to ask got an empty cache from `pipeline/place_wikidata_fetch.py` (no request), which also recorded it in each city's `provenance.json`.
- **151 of 151 built, exit 0; 126 indexes changed, 25 are byte-identical.** Rows across the 151, before to after: stations 6,479 to 6,461; junctions 22,425 to 22,425; landmarks 81,305 to 79,278; places 64,004 to 63,997; streets 284,122 to 284,120; intersections 573,849 to 573,847.
- **2,103 rows left, each attributed from build()'s own log in a second, in-memory build that writes nothing:** worship named by a denomination or chain 980; a park named as a square merged into its street row 827; bare type words 191; religious offices 39; estate and mall facilities 32; stations under a bare type 13; segment merges 7; closed or private stations 4; station entrances 4; and 2 each for a described street, a station with no railway tag and a suburb boundary beside its own node.
- **49 rows returned:** 44 French landmarks named "Hôtel de/du/des ..." that the old leak-word test had taken (Montpellier 15, Avignon 14, Dijon 5), and 5 stations kept apart from a namesake that shares their Wikidata entry (Amsterdam 4, Madrid 1). Rio de Janeiro's "Convento de Santa Teresa" and Madrid's five (below) never left a committed index, so they show in no list.
- **Largest changes:** Rio de Janeiro 490 rows left, Porto Alegre 200, Salvador 188, Belo Horizonte 177, Recife 146, Santos 106, Fortaleza 88, Madrid 82, Osaka 68, Daegu 33. The Brazilian cities and Madrid are the square rule and the worship rule; Osaka and Daegu the bare types, estate facilities and offices.
- **For the owner or the readers, nothing changed here:**
  - 41 merged squares whose own name is no longer the name or another name of any row (`squares_name_not_findable.tsv`). Most sit beside a street row spelled another way ("Praça do Japão" beside "Praça Japão"); 8 were merged into a street row of a different name altogether (Belo Horizonte's Praça Alberto Mazoni and Praça Nova República, Porto Alegre's Praça Osvaldo Schwerdt, Recife's Praça do Parnamirim, Rio's Largo do Bicão, Praça Poeta Duque Costa and Praça da Harmonia, Santos's Praça Azevedo Junior). Three of the 41 carry an entry: Porto Alegre's Praça do Japão, Rio's Largo de São Francisco de Paula and Praça da Harmonia.
  - Rows with an entry of their own taken under a generic name: Kumamoto's 仏舎利塔 (way/489068359, the Hanaokayama Peace Pagoda), Strasbourg's two "Église Protestante" (way/46986392, way/48558298), Valenciennes's "Temple protestant" (way/110103951), four "Temple antoiniste" (Nantes, Nice, Orléans, Rouen; the owner left Paris's as built), Amsterdam's "Zonder Titel" (node/2937809212).
  - No named convent or monastery left any index.
- **The five pilot cities:** 149 reader drops are still rows and are not by-id drops (`pilot_still_rows.tsv`: Rio de Janeiro 54, Madrid 39, Osaka 24, Amsterdam 17, Daegu 15). Madrid's four named convents and its bare "Polvorín" (node/5129628112) are listed apart in `madrid_five_owner_word.tsv`: they stay rows by the owner's rulings on the rule and need an owner word before any by-id drop.
- **Checks:** `check_place_search.py` fails on rule A alone, the 151 (no render); check E is clear. `check_all.py` 70 of 73: that, `check_place_unopened.py` on Anyang, Gwangju, Most and Yamagata as recorded, and `check_macro_facts.py` on Mexico City (407,628 recorded, 427,121 in the shared processed data: the tram rescope's work on disk before its landing; the merge's regeneration rewrote `app/macro_facts.json` to match and that rewrite was put back, since Mexico City is another lane's). `check_barred_marks.py` passes now.
- **Owner rulings on this report (2026-10-13, "all approved"), applied by id, each id read with its cached name first:**
  - Madrid: the bare "Polvorín" (node/5129628112) is dropped in `PLACE_DROPPED`, the type word standing alone. The four named convents stay rows and need no entry.
  - Kumamoto: 仏舎利塔 (way/489068359, the Hanaokayama Peace Pagoda) is kept in `PLACE_KEPT`. The by-id keep beats the bare-type rule (`landmark_drop` tests the id first) and the row is back.
  - Left dropped: Strasbourg's two "Église Protestante", Valenciennes's "Temple protestant", the four "Temple antoiniste", Amsterdam's "Zonder Titel".
  - Only Madrid and Kumamoto were rebuilt, through the gate: Madrid 32,710 to 32,709 places, Kumamoto 2,022 to 2,023. Each city's index, intersections file, street lines file, `place_ids.json` and `place_search.json` changed; no other city's file did.
- **Not done:** no eye read, no render, no browser test. `check_place_index_drift.py` was not run to its end.

### 2026-10-13 - Search rollout: check E settled by the existing rules on the extract run's 73 cities; 52 unopened stations added to the watch file (branch search-rollout)

- **The 334 names failing check E are not all streets.** Counted from the index rows: 156 landmarks, 130 junctions, 36 streets, 12 stations. Each was settled by the precedent for its own kind, read from its cached tags, one city at a time through the job gate. The full list, with ids, verdict and reason, is `data/_search_rollout/extract_rules34/leak_streets.tsv` (on disk only: `data/_*/` is not committed). No shared rule code edited, nothing rendered, nothing pushed, no network request.
- **Kept and reviewed in `PLACE_REVIEWED`: 325 names in 73 cities** (Toulouse 38, Dijon 25, Yongin 22, Lille 18, Uijeongbu 14, Bucheon 12, Bordeaux 11, Montpellier 10, Ansan 9, Gimhae 8).
  - Junctions, 128: every one is a node tagged `junction=yes` or `highway=traffic_signals` named for the building beside it. Kept on the Seoul and Busan precedent (batch 2b): a road feature, not the building. 97 Korean, 31 Japanese.
  - Landmarks, 149: 108 French and Belgian listed mansions and public buildings named "Hôtel ..." (`ref:mhs` or a heritage tag, or tagged an attraction with a Wikidata entry), kept on the Paris precedent as the building's historic name. The other 41 each carry a reason of their own: museums, universities and colleges whose field is the word (the Tokyo precedent), hotel ruins (the Kyoto and Seattle precedents), and two notable buildings that still house what their name carries (the Panama Hotel precedent: Strasbourg's Gallia, Yokohama's Mitsui Sumitomo branch).
  - Streets, 36: every one has a way of residential class or above (or pedestrian, living street) and none is tagged private. Kept on the batch 2b precedent (`_named_street`) and São Paulo's Rua do Shopping.
  - Stations, 12: tram stops and stations named for the place beside them (the Prague precedent, Hotel Golf).
- **Dropped in `PLACE_DROPPED`: 9 names, 12 ids, in 4 cities.**
  - Lille: "Hôtel particulier" (four listed buildings under the bare type, nodes 2063752623, 2063752640, 2063752650, 2063752654) and "Ancien hôtel" (node 2063752408). A type or a description standing in for a name; none has an article. The fourth node surfaced only after the first three were dropped, so the rebuild was run twice.
  - Porto Alegre: four closed businesses tagged `historic=ruins` whose names end "(FECHADO)" (the "(geschlossen)" precedent), and "2 - Ruínas Restaurante" (a number and a description).
  - Daegu: 큰장네거리 (node 436833410), a junction node also tagged `shop=variety_store` whose English name is a shop's description joined to the junction's. A glitched name, never repaired; the junction leaves the search with it.
  - Gimpo: node 414915406, a junction whose name is wrapped in stray brackets. A glitched name.
- **Tags do not decide, kept and listed (2):** Iwaki's 常磐畜産株式会社 (a `historic=ruins` node whose whole name is a company's, no article) and Recife's "Rua do Hotel Pousada do Vale" (one residential way, no access tag, named whole for a hotel).
- **Rule candidates, not built (shared code):**
  - Leak words on junction rows, Korean 99 and Japanese 31: a junction row is a road feature whatever building its name carries. 128 of the 130 were kept; the 2 dropped were glitched names.
  - "hôtel", French, 125 landmark rows: a listed building (`ref:mhs` or `heritage`) named "Hôtel ..." is a mansion or a public building, not a hotel.
  - "hôtel dieu" without the hyphen, French, 5 rows (Nantes 3, Rennes, Rouen): `LEAK_ALLOW` holds only the hyphenated form. Likewise "hôtel de police", "hôtel de région", "hôtel du département", "hôtel des postes", "hôtel communal", 6 rows.
  - "brasserie", French, 10 streets, every one "Rue de la ... Brasserie" on a residential-class way.
  - "hôtel particulier" and "ancien hôtel" as French bare type names, 5 objects in Lille.
  - A name ending "(FECHADO)", Portuguese, 4 rows: the Portuguese form of the "(geschlossen)" rule.
  - "cafe", English, 3 Brazilian streets: a surname (Café) in an alternate name.
- **Unopened stations: 52 rows added to `docs/place_search_unopened_stations.json`**, every field from cached OpenStreetMap files: Montpellier 35, Salvador 7, Belo Horizonte 5, Gimhae 2, Incheon, Rio de Janeiro and Uijeongbu 1 each.
  - The place caches hold no relation members, so memberships were read from each city's cached rail file. Montpellier's 35 stops are members of route relations 19846275 and 19846276 (tram, ref 5) in `data/montpellier/raw/osm_routes.json`: line "Tram 5", source "relation". No other city's rail cache holds a relation with one of its stations.
  - By tag, the `network` value where it names a line: Belo Horizonte 4 ("Linha 2"), Salvador 5.
  - Null with a reason, 8, nothing looked up: Belo Horizonte's Barreiro, Gimhae's 장유 and 신월, Incheon's 학익 (a network, no line), Rio de Janeiro's Gávea, Salvador's Almeida Brandão and Calçada (a network, no line), Uijeongbu's 탑석.
  - `open_namesake_in_index` is true for Salvador's Calçada and Uijeongbu's 탑석.
  - The brief counted 54; the check lists 52 skipped stations in this branch's cities. Anyang and Gwangju fail for another reason (no `stations_not_open`: scaffolded in wave 2, not built) and are not among the 151. Most and Yamagata likewise, on stale summaries. All four left alone.
- **All 73 cities rebuilt through the gate, three at a time, every one exit 0.** `PLACE_REVIEWED` is read by the check, not by the build, so 69 indexes came back byte-identical; Daegu, Gimpo, Lille and Porto Alegre lost 1, 1, 4 and 5 rows.
- **Checks after:** `check_place_search.py` fails on rule A alone, 151 cities (an index no map uses, expected with no render); check E is clear. `check_place_unopened.py` fails on the four cities named above. `check_place_index_drift.py`: the 151 OK.
- **`check_barred_marks.py`, confirmed and not edited:** it matches Angers's mark as a substring in six names of `app/static/places/mendoza.json`: "Hipólito Irigoyen", "Plaza Hipólito Irigoyen", "Bernardo de Irigoyen", "Martín de Irigoyen", "Irigoyen" and "Barrio Irigo Giorgiani". The first five are a surname; the last holds the mark as a whole word.
- **Not done:** no eye read of the 151, no render, no browser test. The reads here cover only rows carrying a leak word.

### 2026-10-13 - Search rollout: the extract run's 151 cities rebuilt on the third and fourth rule passes (branch search-rollout)

- **Committed the extract run as it stood (cfa030e7), merged master at 50d551f4 (6c82294a, no conflict), then rebuilt all 151 cities in three stages, each committed whole.** Nothing rendered, nothing pushed, no shared rule code edited. The record is `data/_search_rollout/extract_rules34/summary.md` and `.json`, with the check logs beside them.
- **Re-filtered all 151 with `place_extract_fetch.py <city> --force`, from the extracts on disk.** Each run named its file with `--pbf` (two files for Gimpo and Incheon) and ran with `HEATMAP_NO_NETWORK=1`, so no request was possible; `--force` wrote over this run's own three caches only. Reason for `--pbf`: without it the script chooses a region and can ask the server for sizes. 151 of 151 exit 0, none skipped. The shared-border rule admits 243 street ways in 10 cities: Recife 48, Fortaleza 34, Porto Alegre 30, Belo Horizonte 29, Valenciennes 28, Grenoble 23, Rouen 18, Bordeaux 16, Lille 11, Nantes 6; the other 11 cities with several municipalities gain none.
- **Wikidata lookup: one job, one city after another, 1,942 entries in 118 cities, every batch answered at its first try.** 33 cities carry no entry on a work of public art or a library; nothing was asked for them and no cache file exists, so their step reads the tag alone, which gives the same result. Bordeaux has one entry Wikidata does not hold.
- **All 151 indexes rebuilt, no step stopped.** Rows across the 151, before to after: stations 6,807 to 6,479; junctions 22,426 to 22,426; landmarks 82,664 to 81,314; places 64,091 to 64,004; streets 283,931 to 284,122; intersections 573,077 to 573,849. Public art kept: 456 with a wikipedia tag, 97 without (on Wikidata); libraries 198 and 53. The split is counted from the id side file and the caches, not printed by the step. The largest first-open index is Rio de Janeiro, 640 KB gzipped.
- **Not decided here, for the owner or the eye read:**
  - Check E, 334 names carrying a leak word in 73 cities (Toulouse 38, Dijon 25, Yongin 22, Lille 20, Uijeongbu 14, Bucheon 12, Bordeaux 11, Montpellier 10): a rule, a drop or a `PLACE_REVIEWED` entry each. The list is `check_place_search.log` in the summary folder.
  - `check_place_unopened.py` B, 54 stations the builds skipped as not open and the watch file lacks: Montpellier 35, Salvador 7, Belo Horizonte 5, Gimhae 2, Anyang, Gwangju, Incheon, Rio de Janeiro and Uijeongbu 1 each. Each row needs its line and where the line came from, so none was written.
  - Most and Yamagata still carry the summaries of their failed builds (no `stations_not_open`). Neither is among the 151; both wait for `PLACE_QUIET_STATIONS`.
- **Found, not fixed: `check_barred_marks.py` reads Angers's barred mark inside Mendoza's street names.** `app/static/places/mendoza.json` holds "Hipólito Irigoyen", "Bernardo de Irigoyen", "Barrio Irigo Giorgiani" and three more, and the check matches the mark as a substring. The names were in the index before this rebuild. Whether the check should match whole words, or skip another city's index, is a call on shared code.
- **`check_all.py`: 70 of 73 pass.** Failing: `check_place_search.py` (rule A on all 151, expected with no render, and E above), `check_place_unopened.py` (above) and `check_barred_marks.py` (above).
- **Not done:** no eye read, no render, no browser test, no row written to the unopened-stations watch file.

### 2026-10-13 - Night runner: the extract source (branch search-rollout)

- **Gave the night runner a second source, `--source extract`, and left
  Overpass the default.** `scripts/place_search_night.py` now runs the
  lookup as one `place_search_area_lookup.py --source extract` child and
  each city's fetch as its own `pipeline/place_extract_fetch.py <city>`
  child, both through the job gate, with no mirror queue, no `--hosts`
  (refused with this source) and no 60 s Overpass wait. The scaffold, the
  gated index build, the checks and the report are the same code for both
  sources. Reason: Overpass was down or slow all of 2026-10-13 and the first
  night left wave 2 scaffolded and unfetched. Rejected: making the extract
  route the default, which is the owner's call and was not given.
- **Capped extract fetches at three at once, and counted a build as one of
  them.** `--workers` takes 1 to 3 and defaults to 3: the gate admits four
  heavy jobs on this machine and one place stays free for other sessions
  (owner's brief). An index build is started beside the fetches only while
  fewer than `--workers` of them run, so the runner never holds more than
  three places. Rejected: four workers with builds deferred, which would
  have left no place for another session's job.
- **Declared 3.5 GB a fetch to the gate, as an estimate.** Measured peaks
  were 0.9 GB for a 102 MB file and 2.5 GB for 696 MB (osm-extract skill),
  close to linear in the file's size; 3.5 GB is that line at the fetch
  script's own cap of 1,000 MB. Left unstated, the gate takes its default of
  8 GB for a label it has never measured and would refuse the second of
  three children. The lookup child declares the same figure, an upper
  bound: its peak was not measured. To re-measure if `MAX_MB` rises.
- **Ordered fetches by regional file: the first city of a region runs alone
  for that region.** The runner works out each city's region offline, the
  way `choose_extract` does (the outline cache when there is one, else the
  stations), from the region index on disk and with no request. One city of
  a region is started; the others of that region wait until a child has
  printed the file's data date, then run side by side. Cities of other
  regions fill the remaining places meanwhile. A region that cannot be
  worked out offline is treated as one shared unknown, one city at a time.
  A wrong grouping costs a wait on the download lock, never a wrong cache:
  the child chooses its file for itself. Rejected: starting three cities of
  one region at once, two of which would sit on the download lock for the
  length of the download.
- **A first city stopped by its regional file fails the rest of that region
  with no child started.** Three kinds are the file's own: over the size
  cap, refused by the download ledger, a download the server did not
  complete. The next city would be stopped the same way, and each try
  costs the server a request. No failure is tried twice in one run;
  `--retry-failed` is the second try, and it clears these with the rest.
- **Kept each failure with the script's own last line.** Classes, read from
  the wording in `pipeline/osm_extract.py` and
  `pipeline/place_extract_fetch.py`: region (none covers the city, or the
  area reaches past its region), size cap, ledger, download, stale (an
  extract older than 7 days), scope stop, lock, timeout, other. A refusal by
  the job gate is not a failure: the city is left waiting and a plain rerun
  fetches it, as a refused build already was. The selftest fails if one of
  the phrases the classifier reads leaves those two files.
- **Added `--skip-cities` for either source.** The named cities are taken
  out of the waves before any step and listed in the report as held out; a
  name in no wave is said, not refused. Built for the owner's ruling that
  Madrid, Rome, Milan and Toronto go last as one batch (2026-10-13). The
  state file keeps what it already held for a skipped city.
- **The report names the source.** With the extract source it carries one
  line saying no Overpass request was made, a table of each regional file
  read (region, data date, bytes, downloaded or held, the cities that read
  it) and a table of each city's seconds and peak memory as the script
  printed them, with the gate's measured peak beside. The seconds are the
  script's whole run, so the city that fetched a file carries its download.
  An Overpass run's report is unchanged.
- **Did not pass `--max-mb` through.** The size caps stay the scripts' own
  (1,000 MB for a fetch, 800 MB for a lookup): a larger file is a person's
  call by the extract route's own rule, and a city stopped by the cap lands
  in the report under its own heading.
- **Selftest 41 to 66 cases; no network and no extract in any.** The 25 new
  cases drive stand-in children through every class above, the three-place
  limit, the first-city rule, `--skip-cities` on both sources, the argument
  refusals, a rerun, `--retry-failed`, a state file switched from Overpass
  to extract, and the dry run.
- **Dry run on the real waves file, wave 2 (25 cities, all scaffolded, none
  fetched):** ten regional files, none held: six Czech regions with one city
  each (ustecky, olomoucky, liberecky, plzensky, moravskoslezky,
  jihomoravsky), south-korea for 16 cities, islas-baleares, argentina and
  noord-holland. Written to
  `data/_search_rollout/extract_2026-10-13_dryrun.txt`. No real run was
  started and no file was downloaded by this work.
- **Merged origin/master (86aadced) and place-extract into the branch
  first, after committing wave 2's scaffold as it stood.** Both merges were
  clean. `scripts/regen_generated.py` rewrote `app/ring_shares.json` after
  the master merge: 19 `map_blob` hashes, the 19 maps re-rendered by
  86aadced, whose own copy of that file still carries the old hashes. For
  Cleanup: master's `ring_shares.json` is one regeneration behind.
- **`scripts/check_all.py`: 72 of 73, the one failure not this change's.**
  `check_place_unopened.py` fails for the 25 wave 2 cities, each for an
  `outputs/<city>/place_search.json` that does not exist yet: they are
  scaffolded and not built. It clears when their index steps have run.
