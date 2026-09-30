# DECISIONS drafts - the France builds (branch `france-build`)

Entries for `DECISIONS.md`, newest first, each exactly as it should land
(owner's rule of 2026-09-30: build sessions keep drafts; cleanup folds them
in when handed off). Anything that must cite a DECISIONS verdict cites this
file until then.

### 2026-09-30 - France landing group 2 built: Montpellier, Strasbourg, Le Havre, Caen, Rouen, Bordeaux, Nantes, Grenoble, Valenciennes

- **All twenty French cities are now built through step 3**: group 1 on
  `france-build`, group 2 on `france-build-2`. Group 2's storefronts:
  Montpellier 6,276, Strasbourg 5,614, Le Havre 2,433, Caen 2,214, Rouen
  (Regional) 4,168, Bordeaux (Regional) 12,807, Nantes (Regional) 6,570,
  Grenoble (Regional) 5,781, Valenciennes (Regional) 2,330. Within a ring:
  87%, 85%, 60%, 71%, 62%, 65%, 63%, 78%, 69%.
- **Masked at source**: 15.8% to 19.1%. **`96.09Z`**: 9.2% to 15.6%.
  **Nantes's 15.6% is just above the five cities' 14.0% top**. It is near
  enough that the precedent stands (both catch-alls excluded); a share far
  outside would have gone to the owner.
- **The personal-exposure check passes** for all nine: 0 contact details,
  and 0 person-like names at a residential unit.
- **The Licence Ouverte same-name rule acted where the kit said it would.**
  Bordeaux's five pairs and Caen's Presqu'île pair each keep their first row,
  so Bordeaux's lines count one or two fewer than the kit's table and Caen's
  T2 17, not 18. The configs record why.
- **OpenStreetMap geometry for five cities, and a template departure for
  the owner.** Montpellier, Strasbourg, Le Havre, Caen and Rouen draw their
  track from OSM. The approved sentence "from the operator's own published
  timetable feed" would be untrue on those pages, so they read "their stops
  from the operator's own published timetable feed and their track from
  OpenStreetMap". Caen and Rouen say "the Normandie region's published
  timetable feed", since their stops come from the aggregate. **A proposed
  sentence for the owner at review time.** The rest of the template is
  unchanged. Montpellier's OSM line 4 is the loop's 4A relation.
- **Gate 3 again reads low on branched lines** (the single-relation count):
  - Rouen's métro, 20 against 31: two branches, Georges Braque and
    Technopôle;
  - Montpellier's line 3, 26 against 29: Lattes and Pérols;
  - Bordeaux's A, B and E;
  - Nantes's 2, 25 against 34;
  - Grenoble's C, D and E: OSM's relations are incomplete, E reading 17
    against 31;
  - Strasbourg's A, C and E, and Valenciennes's T2, by one or two.
  Recorded as OSM has them.
- **Notices 69-71** (TaM, M réso, LiA) are numbered in
  `docs/data_sources.md`. **Renumber at landing**: `check_provenance.py`
  wants the list contiguous from master's last number, and the Band B
  branches also carry a 69. The Band B session and cleanup agree to
  renumber in landing order.

### 2026-09-30 - France's pages take 100-119; three ODbL notices; group 2 on a stacked branch

- **The twenty French pages are numbered 100-119** (Le Mans 100 to
  Valenciennes 119), not 76-95. The Band B builds hold 76-86 (Ottawa to
  Dallas, six already pushed) and the Czech builds took 150-155, so a reserved
  block avoids interleaving at landing. Agreed with the Band B session. Only
  file names and `app/cities.py`'s `page` fields moved; each page's slug and
  `outputs/` directory are unchanged.
- **Landing group 1 lives on `france-build`** (the eleven cities, 24 of 26
  checks passing). **Group 2 is on `france-build-2`**, stacked on it:
  Montpellier, Strasbourg, Le Havre, Caen, Rouen, Bordeaux, Nantes,
  Grenoble, and Valenciennes last. Group 2's scaffolds first sat on
  `france-build` and were moved off it, so group 1 can land without nine
  half-built cities.
- **Three §4.3 notices added to `app/components.py` `_NOTICES`**, one per
  ODbL feed, on Tisséo's and STAR's model: TaM (Montpellier), Réseau
  urbain TAG (Grenoble, naming the SMMAG) and LiA (Le Havre). Montpellier's
  and Le Havre's name only the stations, since their line geometry is
  OpenStreetMap's.
- **Bordeaux's transit caption credits Bordeaux Métropole alone** (the
  LO 1.0 read). Caen's and Rouen's credit Syndicat mixte Atoumod.
- **Le Havre's colours are the project's own**: A `#EF6C00` and B
  `#6D4C41`, which clear the preferred 45 against every pin (67.0 and 53.8)
  and sit 71.1 from each other. Neither is LiA's scheme.

### 2026-09-30 - Ten more French tram cities built through step 3: Besançon, Avignon, Tours, Dijon, Reims, Orléans, Mulhouse, Brest, Saint-Étienne, Nice

- **The first landing group's pipelines**: all eleven commune-scope cities
  whose feeds carry real shapes, with Le Mans. Each ran the shared module:
  fetch (feed always fresh; one Overpass query per city, one in flight, a 60 s
  pause before any retry), step 1, step 2 and step 3. Storefronts:
  Besançon 2,042, Avignon 2,416, Tours 2,652, Dijon 2,668, Reims 2,662,
  Orléans 1,852, Mulhouse 2,155, Brest 1,980, Saint-Étienne 2,998, Nice
  10,063.
- **Masked at source and catch-alls** were in range everywhere, so the
  precedent's two exclusions stand. Masked: Besançon 15.9%, Avignon 14.5%,
  Tours 19.0%, Dijon 18.7%, Orléans 19.8%, Mulhouse 12.7%, Brest 18.2%,
  Saint-Étienne 16.8%, Nice 15.9%, Reims 17.7%. 96.09Z ran 8.6% to 13.4%
  (Saint-Étienne 8.6% and Mulhouse 8.9% just under the five cities' 9.6%
  low), and 56.29B 0.6% to 2.5%.
- **Within-ring shares**: Le Mans 73%, Besançon 64%, Avignon 26% (one line,
  ten stops), Tours 66%, Dijon 67%, Reims 55%, Orléans 85%, Mulhouse 79%,
  Brest 77%, Saint-Étienne 76%.
- **Reims draws TWO lines, T1 and T2, not the brief's one.** Since
  2025-11-24 Grand Reims Mobilités runs T1 (Neufchâtel - Hôpital Debré, 21
  stops) and T2 (to Gare Champagne TGV, 22), the former A and B
  (fr.wikipedia; OpenStreetMap's relations agree). The feed still carries
  one route, "TRAM". The invariant that every drawn line carries its real
  public name decides it, so this is a correction of the brief's facts, not
  a new call. `ROUTE_BRANCHES` in the shared module splits the route's
  trips:
  - by the terminus each trip serves;
  - short workings go by the branch's own stops (the 12 trips ending at
    Léon Blum are T2's);
  - a trip on shared stops only counts for both lines.
  The split gives exactly 21 and 22, and gate 3 matches the published
  counts. T1 keeps the feed's red; T2 takes OpenStreetMap's #00AEF0, since
  the feed cannot tell the lines apart. **For the owner at review time**,
  since the brief said one line.
- **Nice's route B is Line B**: CADAM - Airport Terminal 2, opened
  2025-01-06 on L2's former branch (Lignes d'Azur; fr.wikipedia). It is
  drawn as "Tram B", as approved.
- **Colours below the hard floor, darkened on Lille's rule** (the
  operator's hue kept, darkened 16% of HSL lightness):
  - Tours: `#BD074E` was ΔE 5.5 from the Food service pins, so it becomes
    `#6E042E` (29.5);
  - Dijon: Divia gives T1 and T2 one colour, `#AB0672`. T1 keeps it and T2
    becomes `#5C033D` (30.6 from T1).
- **Gate 3 against OpenStreetMap is exact** for Le Mans, Besançon, Avignon,
  Dijon, Orléans, Mulhouse, Brest B, Tours and Reims (both by hand). Tours
  read 31 until the count took distinct positions: its relation lists one
  stop twice and adds entry- and exit-only roles. **Where it disagrees, the
  difference is OpenStreetMap's shape, traced by name:**
  - **Brest A**, 25 against 30: each relation covers one of A's two
    northern branches, and some A trips reach Gares.
  - **Saint-Étienne**, 25, 11 and 27 against 27, 12 and 29: around the
    Peuple and Bourse stops, OSM's stop positions sit 114-152 m from the
    feed's.
  - **Nice L1 and L3**, 20 and 23 against 22 and 24: OSM positions are
    111-566 m off the feed's named stops.
  A union-of-relations count was tried and rejected: it over-counted
  exactly where the single-relation count was right (Le Mans, Tours,
  Orléans).
- **Brest**: the cable car is drawn (owner). Its gate 3 is its two stations,
  since OSM tags it an aerialway, not a tram route. The two `FIC_` switch
  stops are excluded, as the brief said.
- **Legacy INSEE codes, all 20 scopes**, from geo.api.gouv.fr's communes
  associées and déléguées, with Lille's 59298 and 59355 as the control: only
  Le Havre (76539 Rouelles) and Saint-Étienne (42190 Rochetaillée) have one,
  and the scaffold adds them to `COMMUNE_PREFIXES`.
- **Kit additions, all on this branch:**
  - `scripts/france_fill_build_day.py` fills the self-attest flag,
    route_ids and colours from the fresh feed, and gate 3 from OSM. It
    reproduced Le Mans's hand-filled values as its control.
  - `scripts/france_page.py` writes each page from the approved template,
    with braces from the build's own measurements.
  - The step 2 wrapper writes `outputs/<slug>/sirene_facts.json`, the
    funnel counts the page quotes (`france_register.LAST_RUN`, read-only;
    nothing changes for Paris to Rennes).
  - The shared steps emit baseline figures.

### 2026-09-30 - Le Mans built on the shared French tram module: 35 stops, 1,991 storefronts; a French step 2 peaks at 0.37 GB

- **The first of the France batch, and the shared module's control.**
  `pipeline/countries/france_tram.py` (steps 1 and 3) and
  `france_tram_fetch.py` (downloads) now carry the owner's station rule, the
  commune and regional scopes, gate 3 from OpenStreetMap, and both geometry
  sources. A city's fetch, step 1 and step 3 are three-line wrappers, which
  `scripts/scaffold_france_batch.py --go` writes. Le Mans took SETRAM's
  `gtfs_setram_lmm_auto` resource. It self-attests: Mecatran, 2026-09-25 to
  2026-11-11, fetched 2026-09-30.
- **Rail:** route_ids `T1` and `T2`, colours `#E4151E` and `#0D65AE` (the
  feed's own). 70 platforms become 35 stations (every platform has a parent);
  all 35 are inside commune 72181, T1 24 and T2 18. **Gate 3 is exact**
  against OpenStreetMap's route relations (24 and 18). Median gap 437 m (min
  238), so the half-size rings. Geometry is the feed's `shapes.txt`, two
  shapes per line.
- **Business:** SIRENE, September 2026 edition. The funnel: 85,363 rows
  under 72181, 29,395 active, 24,765 diffusible (**15.8% masked**), 3,624 in
  divisions 47, 56 and 96, 1,283 structurally excluded, 2,341 storefronts,
  and 1,992 after the precedent's catch-alls. **96.09Z at 13.0%** is inside
  the five cities' 9.6-14.0% range, and 56.29B is at 1.9%. Coordinates joined
  for 100.00%, one centroid-grade row dropped: **1,991 storefronts** (900
  retail, 632 food, 459 personal). Premises name on 59.7%. Food is 1.79
  times the screen's OpenStreetMap count. 1,462 (73%) sit within a ring.
  Legacy codes: none under 72181 (geo.api.gouv.fr's communes associées and
  déléguées, with Lille's 59298 and 59355 as the control).
- **`check_personal_exposure.py le_mans`: PASS on the structural guarantee.**
  No registrant-name column is loaded. 0 contact details; 0 of 1,462 pins
  are a person-like name at a residential unit. The heuristic flags 18.5% as
  person-like, against Rennes's 17.9% on the same code. The twenty batch
  cities are registered in the script in one entry.
- **A French SIRENE step 2 is not a heavy job**: a measured peak of
  **0.37 GB** (psutil, the process and its children), because it streams
  row groups of at most 7 MB uncompressed for the columns it reads. It was
  announced to every live session with the measured figure.
- **The page** is the approved template with Le Mans's braces. No line leaves
  the commune, so the template's bracketed "where a line runs past it"
  sentence is left out as the template intends. The density paragraph ends
  at this city's ratio; Rennes's comparison with its siblings was Rennes's
  own fact. The page also adds a business caption carrying INSEE's
  prescribed « Source : Insee » with the SIRENE edition. None of the five
  built French pages carries that string; a separate task was raised for
  them, since it is an `app/` change to published pages.
- **Still to do before Le Mans lands** (at review time, with its landing
  group):
  - `map_inconsistencies.md` rows and `macro_facts.json`;
  - its macro label width, measured in a browser, in one pass for the group;
  - `ring_shares.json` and the README list;
  - its `excluded_categories.md` section;
  - its `docs/data_sources/france.md` rows (feed, contour, OSM);
  - the cities.py `mode` once macro-legend lands.
