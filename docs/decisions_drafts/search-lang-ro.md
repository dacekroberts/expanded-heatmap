# Romanian (ro): settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code. Measured
2026-10-13 on the two Romanian cities, each built in memory with the lists
patched for the process (place caches `osm_places_2026-10-13.json` and
`osm_places_extra_2026-10-13.json`), on `place_index.py` as it stands after
master's second rule batch (branch head 34d0fedd): Bucharest and
Cluj-Napoca. These are every city of the language on the map today; a third
city is measured before it relies on them. `draft_ro.json` holds the lists,
`final_dump/<city>/` the built rows, `by_id_<city>.json` the drops by id.

## The owner's rulings (2026-10-13)

1. **"casa" and "vila" are home-name leads, "with a house kept when it has
   an article of its own".** "casa" (and "casă") takes 98 landmark rows, 97
   distinct names: Cluj 81, Bucharest 17. "vila" takes 5: Cluj 4,
   Bucharest 1.
   **The home rule as it stands keeps none of them on an article.** Since
   the second rule batch a home with its own article stays out (the
   owner's rule of the same day, 294 rows on the 19 cities), unless private
   access is its only home sign; a name lead is a different sign. Rows that
   carry a `wikipedia` tag, each read as the object's own article by
   `own_article()`: Cluj 1 of 81 (way/275140983), Bucharest 1 of 17
   (way/80025736), no "vila" row. A `wikidata` tag alone keeps none either,
   under this rule or any other: Cluj 1 row, Bucharest 7 "casa" rows and 1
   "vila" row carry one with no `wikipedia` tag. No row of the 103 is a
   museum or an attraction by its tags, the one exemption the rule has.
   So the ruling needs one of two things, and that choice is the owner's:
   the two article rows named in `config.PLACE_KEPT` (the lists are in
   `article_casa_<city>.json`), or a change to the home rule, which would
   reopen the 294. Neither is done here.
2. **"residence" and "rezidențial" are home words** (leak words too): 13
   place rows in Bucharest, developers' estates mapped as neighborhoods, on
   top of the 10 the estate rule takes; 1 park in Cluj.
3. **"pasajul" in, "pasaj" out.** "pasajul" holds 6 minor-way rows in
   Bucharest, 2 of them descriptions, dropped by id. "pasaj" would add 7,
   5 of them no street name; the 2 real arcades it loses are Pasaj Comedia
   and Pasaj Majestic. "Pasaj Victoriei" is a row without the word.
4. **"Biserica Reformată" is a bare type:** 1 row in Cluj, three objects.
5. **By id:** the 8 minor-way misfires, the 2 "Pasajul" descriptions among
   them: 4 street rows on 9 ways in Bucharest, 4 on 4 in Cluj.
6. **Recorded as shared-code findings**, below: the cedilla-to-comma fold,
   and Cluj's Hungarian names (39.8% of rows, not searchable).

## What Romanian does

- **The street word LEADS the name, as its own word, in the definite form:**
  "Strada Avram Iancu", "Aleea Rozelor", "Intrarea Albinari", "Drumul
  Taberei". Romanian is NOT a suffix language: `"ro"` stays out of
  `SUFFIX_WAY_LANGUAGES`, and belongs in `WAY_WORD_LEADS` (with fr, ca, es,
  cs, pt). Today that second set changes no row in either city (measured:
  identical builds with and without it); it is the right setting for the
  first Romanian street that carries a business word.
- **The definite form is the name; the indefinite form is a description.**
  "Intrarea Albinari" is a street, "Intrare cimitir" is a cemetery's
  entrance. "Aleea Rozelor" is a street, "Alee pietonală" is "a footpath".
  So the list holds the definite forms only, and the indefinite ones were
  measured one by one (below). This is the language's main rule, and what
  the next Romanian city should be read against.
- **Two spellings of ș and ț.** OSM in these cities writes the comma form
  (ș, ț); 17 Bucharest names and 2 Cluj names carry the older cedilla form
  (ş, ţ), among them one "Piaţa". `_has_word` matches exact letters, so the
  way and leak lists carry both spellings where a word has the letter
  (piața / piaţa, șoseaua / şoseaua, rezidențial / rezidenţial). A fold of
  cedilla to comma in the index step would replace the doubles; it is recorded
  under the shared-code findings below.
- No street name without a street word was found: of 4,858 distinct larger
  road names in Bucharest 16 have no way word, and of 1,084 in Cluj 10; all
  are typos ("Prelugirea", "StradaPetre"), road numbers, proposed roads or
  English descriptions. So no `WAY_LEAD`, no `WAY_ENDING`.

## The lists

`LANGUAGE_NAMES` needs `"ro": "Romanian"` if it is not there.

`LEAK_WORDS["ro"]` (28): hotel, hotelul, hostel, motel, pensiune, pensiunea,
parcare, parcarea, privat, privată, magazin, restaurant, restaurantul,
farmacia, srl, s.r.l., s.a., supermarket, hipermarket, benzinărie,
benzinăria, rezidențial, rezidenţial, residence, apartamente, blocuri,
acces, intrare.

`HOME_WORDS["ro"]` (7): privat, privată, rezidențial, rezidenţial,
residence, apartamente, blocuri.

`WAY_WORDS["ro"]` (22), `"ro"` NOT in `SUFFIX_WAY_LANGUAGES`, `"ro"` in
`WAY_WORD_LEADS`: strada, aleea, intrarea, drumul, bulevardul, șoseaua,
şoseaua, calea, piața, piaţa, piațeta, piaţeta, splaiul, prelungirea,
fundătura, cheiul, rondul, podul, pasajul, pasarela, promenada, scările.

No `WAY_LEAD["ro"]`, no `WAY_ENDING["ro"]`.

`HOME_NAME_LEAD["ro"]` (4): casa, casă, vila, vilă. NOT "palatul" (46 names
over the two cities: banks, ministries, the parliament), NOT "hanul" (8 inns
in Bucharest's old town, visitor sites), NOT "blocul" (2 listed interwar
apartment blocks tagged attractions), NOT "căminul" (an arts center and a
gallery in two hits of three).

`BARE_TYPE_NAMES["ro"]` (24): biserică, biserica, capelă, capela, parc,
parcul, loc de joacă, troiță, troița, cruce, monument, statuie, bust,
fântână, fântână arteziană, cimitir, foișor, clopotniță, casa parohială,
casă parohială, biserica ortodoxă, biserică ortodoxă, biserica reformată,
teren de sport. `bare_type()` sets accents aside, so "Biserica Ortodoxa"
and "Loc de joaca" are caught by the accented entries.

## What was measured

| City | Rows | Streets | Landmarks | Places | Stations | Streets dropped by a leak word | Minor-way names not read as a way |
|---|---|---|---|---|---|---|---|
| Bucharest | 6,552 | 5,243 | 735 | 182 | 392 | 6 | 83 |
| Cluj-Napoca | 1,515 | 1,162 | 256 | 50 | 46 (and 1 junction) | 2 | 18 |

Built before the by-id drops, which take 4 street rows in each city. The
last two columns count ways, as the index step reports them. Romanian is on
100% of names in both; English on 0.8% (Bucharest) and 2.3% (Cluj), so each
page names Romanian only. No row of either index carries a leak word, so
check E has nothing to review. The build ran in 0.2 GB at most.

**What moved against the first draft, none of it from a list** (the lists
did not change; the second rule batch did): Bucharest lost 1 station
(`station_merged_complex`, new) and went from 6,553 to 6,552; Cluj lost 1
street (`street_dropped_private_residential` 20 to 21) and 1 place
(`place_dropped_boundary_duplicate`, new) and went from 1,517 to 1,515.
The "casa" count in Cluj reads 81 rows here and 80 in the draft: 80 was
distinct names.

- **Hungarian in Cluj-Napoca.** 594 of 1,492 index rows, a street counted
  once per name, carry a `name:hu` (39.8%): 473 of 1,139 streets (41.5%)
  and 121 of 353 other rows (34.3%). Only one row's main name IS its
  Hungarian name; the rest are a second form. In the raw cache 45.1% of
  named elements carry one, and 17.5% an `old_name:hu` as well. With
  `PLACE_LANGUAGES = ("ro",)` none of these is read, so a Hungarian street
  name finds nothing today. Bucharest: 9 rows (0.1%). No Hungarian list is
  drafted.
- **Way words, larger roads.** Every definite street type on Bucharest's
  4,858 distinct larger-road names: strada 3,548, intrarea 562, aleea 295,
  drumul 153, bulevardul 102, piața 60, șoseaua 47, calea 22, pasajul 17,
  podul 16, prelungirea 5, splaiul 2, rondul 1, cheiul 1. Cluj's 1,084:
  strada 921, aleea 90, piața 13, calea 8, podul 7, bulevardul 5, splaiul 1,
  drumul 1, fundătura 1.
- **Way words, minor ways.** The list admits 280 street rows carried only by
  minor ways in Bucharest and 91 in Cluj. All 371 were read, not a sample of
  150. Bucharest: intrarea 102, aleea 80, strada 61, drumul 21, pasajul 6,
  piața 3, podul 2, and pasarela, promenada, rondul, scările one each. Cluj:
  strada 68, aleea 18, podul 3, drumul 1, piața 1.
- **Minor-way names NOT read as a way: no real street is lost.** Bucharest's
  are car-park lanes ("Parcare Unirii G"), English descriptions ("Private
  parking", "Underground Parking Exit"), a works' gates ("Faur Poarta 3"), a
  park's parterre ("Parterul Central", 24 ways), three "Sectorului N"
  footways, supermarket lanes and the words left out below. Cluj's are a
  drive-through, a supermarket exit, a pump track, two trail names and the
  words left out below.
- **Leak words.** Streets dropped, Bucharest: "Alee Parcare IDM", "Rampa
  Acces persoane dizabilitati" and the English-worded ways ("Private access
  road", "Residential private parking access", "Hospital private parking").
  Cluj: "Drum privat" (privat) and "Aleea Blocuri Trifoiului" (blocuri).
  Places dropped: 13 in Bucharest (below). Landmarks: "Intrare Biserica"
  (a church's entrance, mapped as a church) and Cluj's "Parc Junior
  Residence".
- **Bare type words that hit as a whole name:** Bucharest 9 distinct names
  (Biserică, Capela, Parc, Loc de joacă, troiță, Foișor twice, Biserica
  Ortodoxă in two spellings); Cluj 2 (Biserica Ortodoxă; Biserica Reformată,
  three objects). The other words are in by the settled class and hit
  nothing today.

## Misfires per way word (minor-way-only rows, all read)

| Word | Rows | Not a street name |
|---|---|---|
| strada | 129 | 2 named by an address ("Strada Mihail Sebastian 31", "Strada Postalionului 53-55"); 2 to look at: "Strada Palatul Cotroceni" (access=no on 3 of 4 ways), Cluj's "Strada Căminele Hașdeu" (private on 4 of 6) |
| aleea | 98 | 2 named by an address (Cluj's "Aleea Becaș 11", "Aleea Becaș 19-21"); 2 coded (Cluj's "Aleea 1", "Aleea a 2-a", footways) |
| intrarea | 102 | 0 |
| drumul | 22 | 0 |
| pasajul | 6 | 2 ("Pasajul Pietonal Metrou Unirii", "Pasajul de la halta Grivița") |
| podul | 5 | 0 |
| piața | 4 | 0 |
| pasarela | 1 | 1 arguable ("Pasarela pietonală Popești-Leordeni", a footbridge by its description) |
| promenada, rondul, scările | 1 each | 0 |

The address-numbered and coded rows are a class a by-id drop answers; none
is frequent enough to move a word.

## Loose words

**In the list, and what each adds:**

- pasajul: 6 minor-way rows in Bucharest (5 leave with the word), 2 of
  them descriptions (above).
  The 17 larger-road "Pasajul" names (road underpasses) are kept whatever
  the list says.
- pasarela, promenada, rondul, scările: 4 rows in Bucharest, 0 in Cluj.
- podul: 3 rows (Bucharest 1, Cluj 2), all named footbridges.
- piața and its forms: 4 rows (Bucharest 3, Cluj 1).
- Leak "acces": 1 street row dropped (the disabled-access ramp); the other
  five "acces" names were never read as a way. Leak "intrare": 1 landmark.
  Neither word is in a real street name in either cache.
- Leak and home "blocuri": 1 street row (Cluj's service alley among blocks).

**Left out, with what each would add:**

- pasaj (indefinite): 7 rows in Bucharest, 5 of them no street name ("Pasaj
  pietonal", "Pasaj pietonal sub Pasaj Aviatiei", "Pasaj Pietonal Grant" and
  two metro underpasses); 2 are real arcades (Pasaj Comedia, Pasaj
  Majestic). "Pasaj Victoriei" is kept without the word. Out, as German
  -gang was at 13 of 19.
- alee (indefinite): 2 rows in Cluj, both descriptions ("Alee pietonală",
  "Alee Parc Colina").
- drum (indefinite): 1 row in Cluj ("Drum enduro", a trail).
- pista, pistă: 4 rows, all cycle-track descriptions.
- pietonal, pietonală: 4 rows, an adjective on descriptions.
- poteca: 2 rows in Bucharest, one a real path name, one "Poteca
  principală" (7 ways of a park). A trail word; the owner has not ruled on
  trails.
- trecere 1 ("Trecere neamenajată", an unbuilt crossing); traseul 1
  ("Traseul nr. 7").
- Lead "la": 3 rows in Bucharest ("La Bălți", "La Potcoavă", "La
  Stâncărie"), spots inside parks drawn as footways, not streets. The other
  prepositions (spre, pe, sub, lângă, între, prin) add nothing.
- rampa, scuar, platou, intrare, pod, centura, autostrada, fundătură,
  stradă: no row in either city.

**Leak words measured and left out,** each for a real name it would hit:
farmacie (the Faculty and the University of Medicine and Pharmacy, in both
cities), fabrica (Strada Fabrica de Chibrituri, Șoseaua Fabrica de Glucoză,
a park: 40 elements), bloc and blocul (listed buildings), vila as a leak
word (it is a home-name lead instead), cămin and căminul (student halls
tagged a university; an arts center), complex and complexul (tram stops,
student campuses), cartier and cartierul (tram stops, the Armenian
quarter), mall (a tram stop), magazinul (the national contemporary art
museum's name), sediul (a library, a palace), autogara (bus stations,
already set aside as not rail), incinta, curtea (Curtea Veche), cafeneaua,
terasa. "sa" alone is a Romanian word and is not the company form.

## The id catches

`by_id_bucharest.json` (9 ids, 4 street rows) and `by_id_cluj_napoca.json`
(4 ids, 4 street rows); every id was checked against its cached name, and
all 8 rows are in the built index.

| City | Street row | Ways | Why |
|---|---|---|---|
| Bucharest | Strada Mihail Sebastian 31 | way/150539862, way/1547016258 | a service way named by an address |
| Bucharest | Strada Postalionului 53-55 | way/1122545151 | a service way named by an address |
| Bucharest | Pasajul Pietonal Metrou Unirii | way/740314410, way/1520124749 | a description |
| Bucharest | Pasajul de la halta Grivița | way/23679712, way/357222296, way/1211546964, way/1211546965 | a description |
| Cluj-Napoca | Aleea Becaș 11 | way/585206582 | a service way named by an address |
| Cluj-Napoca | Aleea Becaș 19-21 | way/585204635 | a service way named by an address |
| Cluj-Napoca | Aleea 1 | way/694262074 | a coded footway |
| Cluj-Napoca | Aleea a 2-a | way/223357863 | a coded footway |

Not dropped, for the eye read to settle: "Strada Palatul Cotroceni"
(access=no on 3 of 4 ways), "Strada Căminele Hașdeu" (private on 4 of 6),
"Pasarela pietonală Popești-Leordeni", and "Biserica Unitariană" (Cluj, one
church on two ways, with an English name), left as a name.

## Shared-code findings (not edits)

1. **Fold cedilla to comma.** 17 Bucharest names and 2 Cluj names write ş
   and ţ with a cedilla, where the rest of both cities writes ș and ț with
   a comma. `_has_word` matches exact letters, so the lists carry both
   spellings of piața, piațeta, șoseaua and rezidențial, and every future
   Romanian word with either letter would need the same. One fold in the
   index step (U+015F to U+0219, U+0163 to U+021B, and the capitals) would
   replace the doubles; the browser's `norm()` needs the same pair to meet.
2. **Cluj's Hungarian names are not searchable:** 39.8% of rows have a
   Hungarian form nobody can type. Declaring `"hu"` fails the index step
   as it stands: `LOCAL_MIN` is 0.9 and Hungarian covers 0.40. It needs a
   second-language setting that reads `name:hu` as an alias without the
   coverage floor and without naming the language on the page unless
   `LIST_SHARE` (0.5) is met. No Hungarian word list is drafted; the way
   words would be utca, út, tér, köz, sétány, híd.
3. **`"ro"` belongs in `WAY_WORD_LEADS`.** It changes no row today.
4. **The home rule and ruling 1** (above): an article keeps no home-name
   row as the rule stands.

## Notes for whoever folds this

- `build_dump.py` patches `_BARE_FOLDED` (the German correction holds) but
  not `WAY_WORD_LEADS`; `lang_ro/finalize.py` builds with it and writes the
  final dump, with newlines in tag values replaced by a space.
- `variant.py` adds every language to `SUFFIX_WAY_LANGUAGES`, whatever the
  draft's `"suffix"` says. For Romanian that would read any word ENDING in
  "strada" or "podul" as a way, so it was not used; `lang_ro/diff_ro.py`
  does the same job, respects `"suffix"`, and also handles leak, home, lead
  and bare edits.
- `measure_lang.py` counts platform, corridor, proposed and construction
  ways, which the index skips; its "not read as a way" lists are longer
  than the build's for that reason.
- **The future edit point:** the indefinite forms. A mapper's "Alee",
  "Pasaj", "Drum", "Intrare" or "Pistă" on a footway is a description. When
  a Romanian city's cache is refreshed, list the minor-way names not read as
  a way and check none is a real arcade; and list new "Pasajul" rows on
  footways, where the two misfires are.
- Landmark names for the eye read to look at: "parc copii", "Statuie poloist", "Monumentul eroilor",
  "Turnul de apă" (Bucharest), "Capela reformată", "Bisericuța de lemn"
  (Cluj). The place-read agent's eye read is still owed for both cities.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map is rendered here, so none of this has met the search box.

```
ro: {join: ["și", "si", "cu", "colț"], stop: ["de", "din", "la", "cel", "lui", "al", "a"],
     street: ["strada", "str", "aleea", "al", "intrarea", "intr", "drumul", "dr", "bulevardul",
              "bd", "bdul", "bld", "blvd", "soseaua", "sos", "calea", "cal", "piata", "pta",
              "splaiul", "spl", "prelungirea", "prel", "fundatura", "fdt", "pasajul", "podul"],
     lead: ["strada", "str", "aleea", "al", "intrarea", "intr", "drumul", "dr", "bulevardul",
            "bd", "bdul", "bld", "blvd", "soseaua", "sos", "calea", "cal", "splaiul", "spl",
            "prelungirea", "prel", "fundatura", "fdt"],
     station: ["gara", "statia", "metrou", "halta"],
     abbr: {"str": "strada", "bd": "bulevardul", "bdul": "bulevardul", "bld": "bulevardul",
            "blvd": "bulevardul", "sos": "soseaua", "pta": "piata", "spl": "splaiul",
            "prel": "prelungirea", "intr": "intrarea", "fdt": "fundatura", "sf": "sfantul",
            "dr": "doctor", "gen": "general", "ing": "inginer", "prof": "profesor"}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. Does `norm()` fold ș and ț to "s" and "t", in BOTH spellings? The comma
   forms decompose under NFKD (s + combining comma) and so do the cedilla
   forms; ă, â, î decompose too. "Piata Victoriei" typed with no diacritics
   must find "Piața Victoriei".
2. "dr" is "Drumul" as a street word and "Doctor" as a title ("Strada
   Doctor ..."); "al" is "Aleea" and the article in "Ioan al II-lea". One
   of each pair has to go: test which reading the box needs more.
3. "cu" as a join word ("Victoriei cu Dacia", how an intersection is said)
   is also inside street names ("Aleea cu Platani", "Hanul cu Tei"). Test
   before keeping it; "și" is the safe join.
4. "Piața" is left out of `lead` on purpose, as Catalan "plaça" and French
   "place" are: a square is searched by its full name.
5. The tram stops abbreviate ("Bd. Ferdinand", "Bd. Timișoara"): the `bd`
   abbreviation has to meet "Bulevardul Ferdinand" the street.
6. Regression queries to add: "Calea Victoriei", "Bulevardul Unirii" typed
   "bd unirii", "Soseaua Kiseleff" typed without ș, "Piata Romana",
   "Calea Victoriei și Bulevardul Dacia", "Gara de Nord", "Pasajul
   Vilacrosse" (Bucharest); "Strada Memorandumului" typed "str
   memorandumului", "Piata Unirii", "Calea Turzii", "Bulevardul 21
   Decembrie 1989" (Cluj-Napoca). And, as a query expected to find NOTHING
   until Hungarian is read: a Cluj street's `name:hu`.

`place_search_review.py`'s `PLACE_WORD` needs the Romanian place words too
(parc, parcul, biserica, piața, cimitirul, podul, lacul, pădurea, grădina,
muzeul, monumentul, statuia, catedrala, mănăstirea, teatrul), so `odd`
stays readable.
