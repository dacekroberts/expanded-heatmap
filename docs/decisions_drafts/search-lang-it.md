# Italian (it): settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code, and no repository
file was changed. Measured 2026-10-13 on the two Italian-language cities
with a place cache (caches of 2026-10-13), each built in memory with the
lists patched for the process, on `place_index.py` as it stands after
master's second rule batch: Rome and Florence. Milan has a pipeline folder
and no place config; it is measured before it relies on these lists.

## The owner's rulings (2026-10-13)

The owner ruled "recommendation ok" on the draft's calls.

- **"arco" and "belvedere" are way words.** arco adds 3 street rows in Rome
  (Arco degli Acetari, Arco della Pace, Arco di Santa Margherita), none in
  Florence, no misfire. belvedere adds 5 in Rome and 1 in Florence, each a
  named terrace on a footway.
- **"galleria" and "scalo" are not; the phrase "galleria pedonale" is.**
  galleria added 6 minor-way rows (Rome 5, Florence 1), 4 of them no street:
  a tram stop's platforms, a station concourse, an arcade, a station's
  shopping passage. "galleria pedonale" keeps Rome's two pedestrian tunnels.
  scalo added 11 rows, 10 of them the lanes of Florence's wholesale produce
  market at Novoli; Rome's Scalo De Pinedo, the one real name, goes with
  them.
- **Home-name leads: "villino" and "villini" only** (5 Florence rows, town
  houses under historic=building). "villa", "casa" and "palazzo" are out.
  The reason, recorded: the home-name test reads any `historic` value, and
  in Rome villa would take 55 rows of which 48 are Roman archaeological
  sites and ruins (Villa di Livia, Villa dei Quintili, Villa di Massenzio),
  and casa 7, all excavated houses (Casa delle Vestali, Casa di Livia). In
  Florence villa would take 39 historic buildings and casa 4. palazzo would
  take 79 in Florence and 8 in Rome, town palaces, the German "Haus" case.
  villa and casa can come back to the owner once the test sets aside
  historic=archaeological_site and ruins: villa would then take 39 + 7 and
  casa 4.
- **Leak phrases "proprietà privata" and "strada privata", not bare
  "privata" or "privato".** The phrases drop the same 3 Rome ways. The bare
  words also hit an archaeological site whose Latin name holds "Privata" and
  a law library, and in Milan "Via Privata ..." is a street type.
- **Florence's 11 indoor market aisles and the other misfires read go by
  id** (`by_id_florence.json`, 14 ways, 12 street rows; `by_id_rome.json`,
  17 ways, 7 street rows). See "The id catches".
- **Two findings go to shared code** (below): Florence's limited-traffic
  zone losing 55 public streets to the private-street rule, and the
  indoor=yes aisles.

## The lists

`LANGUAGE_NAMES` already holds `"it": "Italian"`.

`LEAK_WORDS["it"]` (32): albergo, ostello, agriturismo, affittacamere, b&b,
parcheggio, parcheggi, garage, autorimessa, proprietà privata, strada
privata, negozio, ristorante, trattoria, pizzeria, farmacia, supermercato,
ipermercato, centro commerciale, condominio, residence, appartamenti, srl,
s.r.l., s.p.a., snc, s.n.c., s.a.s., ingresso, accesso, autolavaggio,
distributore. ("hotel" is an English leak word, read in every city.)

`HOME_WORDS["it"]` (5): proprietà privata, strada privata, condominio,
residence, appartamenti.

`WAY_WORDS["it"]` (63), NOT in `SUFFIX_WAY_LANGUAGES`: via, viale, vialetto,
vicolo, vico, viuzzo, viuccia, largo, piazza, piazzale, piazzetta,
piazzaletto, corso, strada, stradone, lungotevere, lungarno, lungomare,
lungolago, lungomura, ponte, ponticello, passerella, salita, discesa, rampa,
rampe, scalea, scalinata, scala, gradinata, cordonata, clivo, clivio, erta,
borgo, borghetto, chiasso, sdrucciolo, sentiero, ciclabile, ciclovia,
ciclopedonale, superciclabile, passeggiata, passaggio, passetto, sottopasso,
sottopassaggio, sottovia, galleria pedonale, traforo, viadotto, cavalcavia,
circonvallazione, rotatoria, svincolo, raccordo, complanare, traversa,
argine, arco, belvedere.

`WAY_WORD_LEADS` gains `"it"`. No `WAY_LEAD`, no `WAY_ENDING`: Italian
writes the street's type word out (14,897 of Rome's 14,938 larger-road
names and 2,101 of Florence's 2,103 carry a listed word).

`HOME_NAME_LEAD["it"]` (2): villino, villini.

`BARE_TYPE_NAMES["it"]` (68): chiesa, cappella, parco, giardino, giardini,
parco giochi, area giochi, fontana, fontanella, monumento, monumento ai
caduti, statua, madonnina, edicola, obelisco, rudere, ruderi, anfiteatro,
mausoleo, colombario, ninfeo, cisterna, cisterne, sacrario, area fitness,
area relax, parco condominiale, parco comunale, giardino comunale, giardino
parrocchiale, parco per bambini, parco della chiesa, chiesa evangelica,
chiesa cristiana evangelica, chiesa apostolica, evangelica, sala del regno,
sala del regno dei testimoni di geova, tomba romana, tombe romane, cisterna
romana, villa romana, villa rustica, domus rustica, mausoleo romano,
sepolcro romano, terme romane, terme romana, ninfeo romano, colonna romana,
cippo romano, vasca romana, resti di una villa romana, zona archeologica,
necropoli arcaica, basilica paleocristiana, latrine pubbliche, cortili
porticati, strada lastricata, piazzale lastricato, calidarium, frigidarium,
colonnata, edicola di culto, sepolcro a camera, roman tomb, pista ciclabile,
percorso ciclopedonale.
NOT "giardinetti" (a Rome neighborhood and its station), NOT "castello" (a
Florence district; two Rome castles carry it with a Wikidata item), NOT
"colonna" (Rome's Rione III).

## What was measured

The final builds, with the lists above and the by-id drops applied
(`final_dump/<city>/`):

| City | Rows | Streets | Landmarks | Places | Stations | Ways dropped at the leak test | Minor ways not read as a way |
|---|---|---|---|---|---|---|---|
| Rome | 19,461 | 16,467 | 2,409 | 331 | 254 | 12 | 236 ways, 119 distinct names |
| Florence | 3,474 | 2,333 | 1,004 | 87 | 50 | 0 | 88 ways, 58 distinct names |

Italian is on 100% of names in both and English on 0.5% (Rome) and 0.4%
(Florence), so each page names Italian only. Every map station has an
indexed place within reach in both cities.

**What moved since the draft, and why.** The draft's builds ran before
master's second rule batch. Against them, with the same lists: Rome's
landmarks went from 2,426 to 2,409 because the batch drops a landmark that
is a street's own way (`landmark_dropped_street_way`, 42 elements: Via Appia
Antica, Via Sacra, Via Flaminia as historic roads; their street rows stay),
and its places from 339 to 331 (`place_dropped_boundary_duplicate`, 19
elements). Florence lost one landmark the same way. The street rows moved
only by the by-id drops: Rome 16,474 to 16,467, Florence 2,345 to 2,333.

**Rome's size.** 19,461 rows and 28,591 intersections. The index would
weigh 1,467,696 bytes (433,372 gzipped), its intersections file 829,745 and
its street lines file 925,500. Beside the largest built: Mexico City
4,968,532 bytes, Sao Paulo 4,578,987, London 4,353,785, Taipei 2,909,405.
Rome is about 30% of Mexico City's index. The build peaked at 0.71 GB and
ran under a minute.

- **Way words.** Of Rome's 2,258 distinct name sets on minor ways the list
  reads 2,139; of Florence's 603 it reads 545. Before the by-id drops Rome
  had 1,036 street rows on minor ways only and Florence 78. Rome's by
  leading word: via 410, viale 199, vicolo 94, largo 77, piazza 42, rampa
  33, piazzale 30, sentiero 23, ciclabile 15, percorso 14 (read by
  ciclopedonale), passeggiata 12, scalea 9, salita 8, clivo 7, ponte 7,
  scala 6, passaggio 5, scalinata 5.
- **Names not read as a way.** Florence's 58: about 38 footways named for a
  tram stop ("Careggi - Ospedale"), the 10 wholesale-market lanes under
  "scalo", garden and cloister paths, and "Corte di Zannine" (one real
  court). Rome's 119: 18 bus-terminal lanes ("Corsia 1"), 7 numbered gates
  and 5 cemetery entrances, 29 names on paths, most of them mountain-bike
  trail nicknames, the cemetery's numbered terraces ("Gradone I"), park
  names on paths. Real names not read on their footways, each with a row
  from another way: Clivus Capitolinus, Clivus Palatino, Decumano Massimo,
  Riva Ostiense, Foro Traiano. "Vie Enrico Glori" is a typo for Via.
- **Misfires per word on minor-way-only rows.** Florence, all 78 read: via
  11 of 34 (the market hall's aisles), viuccia 1. Rome, a seeded sample of
  150 of 1,036: via 1, passeggiata 1, piazzale 2 (customers-only lanes,
  below); the other 146 read as real names. Over all of Rome's rows: ponte
  2 of 12, passaggio 1 of 5, sentiero 1 of 23. Zero seen: viale, vicolo,
  largo, rampa, scalea, scalinata, scala, salita, clivo, clivio, ciclabile,
  ciclopedonale, sottopasso, passetto. No word misfires often enough to
  leave the list; the rows go by id.
- **Leak words.** The index step counts 12 Rome ways dropped at the leak
  test. Over the whole cache the words hit 18 way names, most already out
  as no way name: 7 entrances, 5 "accesso ..." descriptions, 2 car parks, 2
  "Proprietà Privata ..." tracks, "Strada Privata" and "Centro Commerciale
  Maximo". Two place nodes go as well, a gated estate's north and south
  entrances tagged as neighborhoods. Florence: one footway, out already as
  no way name. No index row carries a listed word. `WAY_WORD_LEADS` changes
  no row in either city with this list.
- **Bare type words that hit as a whole name.** Rome 67 rows: cisterna
  romana 6, chiesa cristiana evangelica 5, tomba romana 4, roman tomb 3,
  chiesa apostolica 2, mausoleo romano 2, sepolcro romano 2, villa romana 2,
  and one each for 39 more words. Florence 3: cappella, chiesa evangelica,
  giardino comunale. Three Rome streets go as descriptions, among them
  "Pista Ciclabile" and "Percorso ciclopedonale". Florence's "Obelisco"
  keeps its row on an article of its own.

## What is left out, and why

- **Leak words measured and left out:** osteria (Via dell'Osteria, three
  Rome villages named Osteria ...), villaggio (5 neighborhoods), residenza,
  condominiale (a museum; the parks so named go by the bare list), consorzio
  and comprensorio (2 indexed places each), palazzina (6 Florence
  buildings), cancello (its numbered gates are not read as a way anyway, and
  it would take Via del Cancello), sede, scuola, ospedale, uffici (Via degli
  Uffici del Vicario), caffè (a largo named for an economist), campeggio
  (Via del Campeggio), scala, lotto, gruppo, edificio, and the bare privata
  and privato.
- **Home leads left out:** villa, casa, palazzo (ruled above); casale (5
  Rome rows: a mill, a castle, a farmhouse, a site), casino (4, garden
  pavilions and a monastery), palazzina (5 Florence pavilions), palazzetto
  (2), podere (0 rows).
- **Way words left out with no measured effect, as generic words:** canto,
  volta, costa, passo, scale, percorso, rotonda. Florence's Volta and Costa
  streets sit on pedestrian or residential ways and keep their rows without
  the word; its two Canto squares are pedestrian areas, skipped as areas.

## Loose words and their future edit points

| Word | Rows added (Rome + Florence) | Not streets | Ruling |
|---|---|---|---|
| arco | 3 + 0 | 0 | in |
| belvedere | 5 + 1 | 6 named terraces, no street | in |
| galleria | 5 + 1 | 4 | out; "galleria pedonale" in (2 rows) |
| scalo | 1 + 10 | 10 (a wholesale market's lanes) | out |
| pista | 2 + 0 | 1 (a skating rink) | out; "Pista ciclabile X" is read by ciclabile |
| scalone | 1 + 0 | 1 | out |
| scalette | 0 + 1 | 1 (a tram stop's platform) | out |
| prato | 0 + 1 | 1 (a tram stop's platform) | out |
| corsia | 18 + 0 | 18 (bus-terminal lanes) | out |
| gradone | 4 + 0 | 4 (cemetery terraces) | out |
| parco | 7 + 1 | 8 (parks on paths) | out |
| corte | 0 + 1 | 0 | out (also a courtyard) |
| clivus, decumano, foro, riva | 0 | 0 | out (each name has a row already) |

**Future edit points.**

- **belvedere and arco:** each also names a hotel, a bar or a monument. None
  is in an index today. When an Italian city's cache is refreshed, list the
  minor-way street rows led by Belvedere or Arco that are new since the last
  read.
- **ponte, passaggio, sentiero:** a park, a gorge or a description can carry
  the word (the Rome drops by id below). The same listing after a refresh.
- **Milan and any northern city:** measure "strada privata" before relying
  on it ("Via Privata ..." and "Strada Privata ..." are addressed streets
  there), and look for way words these two cities do not use (alzaia, ripa,
  bastioni, calle, fondamenta, salizada, crosa, rua).
- **Tram and bus platforms drawn as footways** carry the stop's name. None
  is a street row today. A stop named with a listed word ("Piazza ...")
  would read as a way: after a refresh, list the minor-way street rows whose
  every way is a platform.

## The id catches

Every id was checked against its cached name by the script that wrote the
files (`mk_by_id.py`), and both final builds ran with them applied.

- **`by_id_florence.json`: 14 ways, 12 street rows.** The central market
  hall's 11 indoor aisles (13 ways, highway=footway, indoor=yes, level=0,
  named after towns: Via di Fiesole, Via di Campi, Via di Calenzano, Via di
  Sesto, Via di Signa, Via di Firenze, Via di Settignano, Via di Rovezzano,
  Via di Bagno a Ripoli, Via di Casellina e Torri, Via del Galluzzo) and
  "Viuccia var." (way/912178164, a path's variant).
- **`by_id_rome.json`: 17 ways, 7 street rows.** "Via della Storta 435"
  (way/190124659, an address as a name), a gated estate's two perimeter
  tracks (10 ways) and its country club's track (3 ways), "passaggio per
  evitare cancello" (way/1050717989, a description), "Forra di Ponte Terra"
  (way/1298768213, a gorge) and "Parco Archeologico Ponte Di Nona" (2 ways,
  a park's name on its paths).
- **Left for the eye read, not dropped:** six customers-only service roads
  at one site in west Rome named for European capitals (Piazzale Kiev,
  Piazzale Roma, Piazza Lisbona, Via Londra, Via Vilnius, Viale Bruxelles),
  undecidable from tags; 15 Rome street names that start lowercase; the
  Verano cemetery's named avenues ("Viale Arciconfraternita ...", 11 rows),
  real names inside a cemetery.

## Shared-code findings (not edits)

1. **A limited-traffic zone is read as private: Florence loses 55 public
   streets.** The old center's streets are tagged exactly
   `access=no` + `motor_vehicle=permit` + `foot=yes` on highway=residential
   or unclassified: closed to cars without a permit, open to anyone on foot.
   The rule that drops a residential street with access=private or no
   (`street_dropped_private_residential`, 95 ways in Florence) takes 55 such
   names on 82 ways; 100 more names so tagged keep a row only because
   another of their ways is tagged otherwise (whether their drawn lines are cut
   short was not measured). Five examples: Costa San Giorgio (way/24976069), Via Santa Reparata
   (way/24695297), Piazza dei Peruzzi (way/25020485), Via Cesare Battisti
   (way/23158528), Via Torta (way/25020357). `ztl_florence.tsv` lists all 55
   with their way ids. Rome has no way with this combination. A change to
   measure on the built cities: a way with foot=yes, or with
   motor_vehicle=permit, is not private. Until then Florence's index is
   missing these streets, and its reader should know.
2. **Indoor aisles named as streets.** A footway with indoor=yes named like
   a street reads as one: Florence's 11 market aisles (dropped by id above),
   and in Rome one row, Scala Sancta. A rule to measure: a minor-way street
   row whose every way is indoor=yes is no street.
3. **`WAY_WORD_LEADS` needs "it"**, or a larger road named with a leak word
   behind its street word ("Via dell'Albergo") would be dropped. No such
   name exists in the two cities with this leak list.
4. **The home-name test reads any `historic` value**, so a lead word such as
   villa or casa takes excavated Roman houses (55 Rome rows between them).
   Setting aside historic=archaeological_site and ruins would let the owner
   reconsider both words.
5. Whoever folds the lists adds the bare words to `BARE_TYPE_NAMES` only;
   `_BARE_FOLDED` is built from it at import.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map was rendered, so none of this has met the search box.

```
it: {join: ["e", "angolo"], stop: ["di", "del", "della", "dello", "dei", "degli", "delle", "da",
                                    "il", "lo", "la", "i", "gli", "le", "l", "d"],
     street: ["via", "v", "viale", "vle", "vicolo", "vic", "piazza", "pza", "pzza", "piazzale",
              "ple", "largo", "lgo", "corso", "cso", "lungotevere", "lgt", "lungarno", "ponte",
              "borgo", "circonvallazione", "strada"],
     lead: ["via", "v", "viale", "vle", "vicolo", "vic", "corso", "cso", "lungotevere", "lgt",
            "lungarno", "borgo", "circonvallazione", "strada"],
     station: ["stazione", "staz", "fermata", "metro"],
     abbr: {"vle": "viale", "pza": "piazza", "pzza": "piazza", "ple": "piazzale", "lgo": "largo",
            "cso": "corso", "lgt": "lungotevere", "vic": "vicolo", "s": "san", "sta": "santa",
            "ss": "santi", "staz": "stazione"}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. The elided articles: "dell'Osteria", "d'Italia", "Sant'Angelo". Does
   `norm()` split at the apostrophe, so that "l" and "d" work as stop words,
   and is "dell" needed too? Both the straight and the curly apostrophe
   occur in the caches.
2. "V.le", "P.za", "P.le", "L.go", "C.so": check what `norm()` leaves of
   each dotted form before trusting the `abbr` keys.
3. "s" for San is a guess at a one-letter abbreviation ("S. Giovanni") and
   may be too loose as a whole-word rule.
4. Numerals written out: OSM has "Corso Vittorio Emanuele Secondo" and
   "Galleria Giovanni Ventitreesimo"; readers type "II" and "XXIII". An
   alias, not a matcher word, may be the answer.
5. Regression queries to add: "Via del Corso", "Corso Vittorio Emanuele II",
   "Lungotevere dei Mellini", "Piazza di Spagna", "Via Appia Antica e Via
   Ardeatina", "V.le Trastevere", "Termini" (Rome); "Ponte Vecchio", "Via
   de' Tornabuoni" typed "Via dei Tornabuoni" and "Via Tornabuoni",
   "Lungarno Corsini", "Piazza della Signoria", "Borgo San Frediano",
   "Santa Maria Novella", and "Costa San Giorgio" once finding 1 is fixed
   (Florence).

`place_search_review.py`'s `PLACE_WORD` needs the Italian place words too
(parco, giardino, piazza, chiesa, basilica, cappella, cimitero, ponte,
porta, villa, palazzo, museo, teatro, fontana, torre, mura, acquedotto,
tempio, terme, forte, monte, colle), so `odd` stays readable.

## Files and scripts

- `draft_it.json`, `by_id_rome.json`, `by_id_florence.json`,
  `ztl_florence.tsv`, `final_dump/<city>/` (rows_<kind>.tsv, streets.tsv,
  report.json). The dump was written by `build_it.py`, not `build_dump.py`:
  it patches `WAY_WORD_LEADS`, applies the by-id file, and flattens
  newlines in tag values. One difference in format: the sixth column of
  streets.tsv counts the row's platform ways where `build_dump.py` writes
  the service values.
- `variant.py` forces the code into `SUFFIX_WAY_LANGUAGES`, wrong for
  Italian; `loose.py` measured each word on the caches instead, and the
  decisive ones were confirmed by full builds.
- `measure_lang.py` counts pedestrian and platform ways as minor and tries
  each way word as an ending; its tables were used for candidates only.
- Earlier dumps kept for the record: `b1`, `b2`, `b2home` (every home lead
  at once), `b3`.
