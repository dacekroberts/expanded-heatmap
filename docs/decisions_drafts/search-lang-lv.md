# Latvian (lv): settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code. Measured 2026-10-13
on the three Latvian cities, each built in memory with the lists patched for
the process (place caches `osm_places_2026-10-13.json` and
`osm_places_extra_2026-10-13.json`), on `pipeline/place_index.py` as it
stands after master's second rule batch (f68335fb): Riga, Daugavpils,
Liepaja. These are every city of the language on the map today; a fourth is
measured before it relies on them. Beside this file: `draft_lv.json` (the
lists), `by_id_riga.json` (the drops by id), `final_dump/<city>/` (every row).

## The owner's rulings (2026-10-13)

1. **Riga's numbered garden lanes drop by id: 19 street rows.** "11 Līnija"
   to "74 līnija" (18 names) and "Centra līnija", unpaved service ways beside
   the neighborhood Makšķernieku ciemats, with no neighborhood in the name.
   "līnija" stays a way word: 112 of Riga's larger roads end in it.
2. **The three Central Station tunnels drop by id: 3 street rows.** "A
   tunelis", "B tunelis", "C tunelis", lettered footway tunnels at Riga
   Central Station. "Hanzas tunelis" stays.
3. **The Daugavpils fortress's numbered works are KEPT: 10 rows.** "1.
   bastions" to "8. bastions" and "6. ravelīns" (9 landmarks, historic=fort,
   no wikidata) and the place "6. kurtīnlunete". A per-city keep, not a rule:
   no Latvian `CODED_TYPE` entry is to be written, and one written later
   would have to leave these ten in.
4. **"taka" (a trail) is a way word: 14 street rows** (Riga 13, Daugavpils 1).
5. **"dzelzceļš" is out and Latvian is not a suffix language: 2 rows left
   out** ("Rīgas bērnu dzelzceļš", five paths on a razed children's railway,
   which keeps a landmark row from its route relation; Liepaja's "Vecais
   dzelzceļš", railway=abandoned). With the suffix test on, the "-ceļš"
   ending admits exactly these two and nothing else.
6. **"grava" and "ierakums" are out: 1 row each left out** ("Līdaku grava",
   a ravine path in Riga; "Narkēvica ierakums", a path tagged barrier=ditch
   in Liepaja). Each names a landform, not a way.
7. **"dzīvojamā māja" (a dwelling house) is a home word: 2 rows dropped**,
   both exhibit houses of the Ethnographic Open-Air Museum in Riga, mapped
   building by building; the museum's barns, kiln and windmills stay.
8. **"stacija", "tirgus" and "brāļu kapi" are out of the bare type list:**
   each is a tram stop's real name (below).
9. **The house word that closes a name ("Mindeļa villa") is a shared-code
   finding, not a list entry** (below, "Shared-code findings").

## The lists

`LANGUAGE_NAMES` already holds `"lv": "Latvian"`.

`LEAK_WORDS["lv"]` (36): viesnīca, hotelis, hostelis, motelis, viesu nams,
viesu māja, stāvvieta, autostāvvieta, stāvlaukums, privāts, privāta,
privātais, privātā, privātīpašums, privātmāja, privātmājas, veikals,
lielveikals, restorāns, kafejnīca, aptieka, sia, a/s, dzīvokļi,
daudzdzīvokļu, dzīvojamā māja, tirdzniecības centrs, iebrauktuve,
piebraucamais, klīnika, autoserviss, garāžas, kooperatīvs, pansija,
pansionāts, degvielas uzpildes stacija.

`HOME_WORDS["lv"]` (11): privāts, privāta, privātais, privātā,
privātīpašums, privātmāja, privātmājas, dzīvokļi, daudzdzīvokļu, dzīvojamā
māja, pansionāts.

`WAY_WORDS["lv"]` (29), `"lv"` NOT in `SUFFIX_WAY_LANGUAGES`: iela,
šķērsiela, jauniela, augšiela, līnija, šķērslīnija, gatve, prospekts,
bulvāris, šoseja, ceļš, aleja, laukums, skvērs, aplis, gāte, sēta, tilts,
tunelis, dambis, aizsargdambis, krastmala, ostmala, mols, promenāde, pasāža,
taka, laipa, veloceliņš.

Latvian writes the way word last, as its own word, after a genitive
("Brīvības iela", "Raiņa bulvāris"). The compounds that occur (šķērsiela,
jauniela, augšiela, šķērslīnija, aizsargdambis, veloceliņš) are listed whole.
`_named_street` reads the last word for a language outside `WAY_WORD_LEADS`,
which is right for Latvian: "lv" stays out of `WAY_WORD_LEADS`.

No `WAY_LEAD`, no `WAY_ENDING`: no street name in the three cities leads with
a preposition ("pie" added no row anywhere).

`HOME_NAME_LEAD["lv"]` (4): villa, vila, savrupmāja, dzīvojamā. NOT "māja"
and NOT "nams": measured, they name museums, theaters and places of worship
(Stūra māja, Melngalvju nams, Kaķu nams, Rīgas Vāgnera nams, Virsnieku Saieta
nams, three "lūgšanu nams" prayer houses). NOT "muiža": it leads no name, and
glued it ends neighborhoods (Bišumuiža, Anniņmuiža).

`BARE_TYPE_NAMES["lv"]` (28): baznīca, kapela, kapliča, lūgšanu nams, parks,
skvērs, rotaļu laukums, bērnu rotaļu laukums, bērnu laukums, sporta laukums,
basketbola laukums, futbola laukums, suņu pastaigu laukums, skeitparks,
stadions, pludmale, peldvieta, piemineklis, piemiņas akmens, piemiņas
plāksne, piemiņas zīme, memoriāls, skulptūra, strūklaka, krusts, kapi,
kapsēta, estrāde.
**NOT "stacija", "tirgus" or "brāļu kapi": each is a tram stop's real name**
(Stacija in Daugavpils and Liepaja, 2 nodes each; Tirgus in Daugavpils, 3;
Brāļu kapi in Riga and Daugavpils, 2 each), and a bare type word drops a
station that has no wikidata. Add the words to `BARE_TYPE_NAMES` only;
`_BARE_FOLDED` is built from it at import.

## What was measured

Final builds: the lists above, Riga's 22 by-id drops applied.

| City | Rows | Streets | Landmarks | Places | Stations | Streets dropped by a leak word | Street ways dropped by id | Minor ways not read as a way (ways / names) |
|---|---|---|---|---|---|---|---|---|
| Riga | 2,632 | 1,970 | 363 | 143 | 156 | 0 | 22 | 33 / 22 |
| Daugavpils | 621 | 478 | 69 | 35 | 39 | 0 | 0 | 0 / 0 |
| Liepaja | 492 | 409 | 51 | 14 | 18 | 0 | 0 | 7 / 3 |

Latvian is on 100% of names in all three and English on 1.6%, 1.0% and 1.7%,
so each page names Latvian only. Not measured here: whether every map station
has an indexed place within 1 km.

**What moved against the first draft, and why.** The first draft's table
(Riga 2,662 rows, Daugavpils 622, Liepaja 492) was built before the second
rule batch. On today's file and before the by-id drops Riga is 2,654:
stations 163 to 156 (`station_dropped_outline` 7), landmarks 364 to 363
(`landmark_dropped_register_entry` 1). Daugavpils: stations 40 to 39
(`station_dropped_outline` 1). Liepaja's totals are unchanged (one landmark
moved from `not_notable` to the new `landmark_dropped_street_way`). None of
this is a list change. The by-id drops then take Riga's streets from 1,992
to 1,970.

- **Way words on larger roads.** Riga's 1,814 distinct larger-road names end
  in: iela 1,576, līnija 112, šķērslīnija 29, gatve 18, prospekts 12, bulvāris
  10, tilts 9, laukums 8, dambis 7, krastmala 7, aleja 5, aplis 3, and one or
  two each of šķērsiela, gāte, skvērs, jauniela, augšiela, šoseja, ceļš.
  Daugavpils: iela 441 of 452. Liepaja: iela 348 of 360, ostmala 2. Only
  intercity route names ("Rīga - Ērgļi") carry no way word, and a larger road
  is kept as named.
- **Minor-way names NOT read as a way, all read.** Riga's 22: twelve private
  service ways "1. vadi" to "12. vadi" (pipe or cable runs; private access
  drops them whatever the list), four footways named for a stop or a place
  (Aldaris, Depo, Imanta, Ziemeļblāzma), a cycle route's name ("Centrs -
  Teika - Jugla - Berģi"), "Wheelchair ramp", a private ditch track, a
  private arcade ("Krusteja"), and the two of rulings 5 and 6. Liepaja's 3:
  rulings 5 and 6 and "Zirgu sala", which has a row from its residential way.
  No real street is lost.
- **Minor-way-only names read as a way, all 121 read** (Riga 83, Liepaja 35,
  Daugavpils 3). Misfires per word: līnija 19 of 19 (ruling 1); tunelis 3 of
  4 (ruling 2); skvērs 1 of 1 (below); veloceliņš 2 of 2 are a cycle path
  named for its street ("Pulvera ielas veloceliņš"), a description more than
  a name, left in. Zero misfires: iela (59 names, tracks and service ways
  carrying a street's name), taka 15, mols 5, promenāde 3, aleja 3, laipa 2,
  gatve 2, bulvāris, tilts, pasāža, aizsargdambis, šķērslīnija. "E-D dambis"
  is private and dropped by the private-minor rule, as are three "iela"
  service ways.
- **skvērs moves one row.** "Baumaņa skvērs" is a service way and a square
  node with wikidata; with skvērs a way word the row is a street. Without it
  the row is a landmark.
- **Words that carry rows, by removal (before the by-id drops):** līnija 19,
  taka 14, mols 5, tunelis 4, promenāde 3, laipa 2, veloceliņš 2, skvērs,
  pasāža, aizsargdambis 1 each. laukums, dambis, sēta, gāte and aplis change
  no row: they sit on larger roads and matter only to `_named_street`.
- **Leak words.** The three caches hold almost no business names, so most of
  the 36 words are in on the dictionary and hit nothing. The hits: Riga's
  four dropped landmarks, three of which return with the words off (the two
  museum houses of ruling 7, a former hotel, "Bij. viesnīca Alba", and "Zasu
  muižas diētiskā pansija"), a tram platform "Pansionāts" in Daugavpils
  (platforms are skipped anyway) and Liepaja's "Hoijeres kundzes viesu nams"
  (tourism=museum, no wikidata, so already out; it needs a `PLACE_REVIEWED`
  line if it gains one).
- **Bare type words that hit as a whole name:** Kapela 1, Piemiņas plāksne 1
  (out as a memorial either way), Lūgšanu nams 1, all Riga: 2 landmark rows
  taken. None in Daugavpils or Liepaja.

## Left out, and why

- **Way words with no hit in the three cities:** kāpnes (steps), pārvads
  (overpass), tiltiņš (footbridge), celiņš (path), trase, stiga, estakāde,
  viadukts. A bare "Kāpnes" footway would be a type word, not a name.
- **Way words measured and out:** dzelzceļš 2 rows, grava 1, ierakums 1
  (rulings 5 and 6); vadi (12 private runs), krusteja (1, private), sala and
  kvartāls (no row).
- **Not leak words, measured:** tirgus (21 Riga hits, marketplaces and
  Tirgus iela), centrs (23, arts centers and a neighborhood), nams (15), māja
  (6), klubs, ciemats (neighborhoods), vasarnīcu and degvielas (Vasarnīcu
  iela, Degvielas iela: hence the whole phrase "degvielas uzpildes stacija").
  "as" for A/S is out unmeasured: a two-letter word that English names also
  hold. "a/s" is in.
- **Not bare type words:** stacija, tirgus, brāļu kapi (tram stops, ruling
  8); pils, muiža, tornis, osta, ezers and the like had no whole-name hit and
  are proper names in use elsewhere.

## Loose words and their future edit points

- **līnija.** Every minor-way-only hit today is a garden colony lane and is
  dropped by id. When Riga's cache is refreshed, list the minor-way street
  rows ending "līnija" that are new since this read; a numbered one with no
  neighborhood in its name goes by id.
- **tunelis.** 3 of 4 were station corridors. On a refresh, list new
  minor-way rows ending "tunelis"; a lettered or numbered one goes by id.
- **taka.** 14 rows, all trail names today. A trail name is a route more
  than a street; if the owner later rules trails out for any language, this
  word goes with German "pfad".
- **veloceliņš.** 2 rows in Liepaja, each a cycle path named for its street.
  If more appear as bare descriptions, the word comes out.
- **skvērs** as a way word turns a square mapped on a service way into a
  street row (1 today).
- **A new bare type word** is checked against the three cities' tram stop
  names before it is added.

## The id catches

`by_id_riga.json`, 22 ways, every id checked against its cached name by
`final_build.py`; after the drops none of the 22 names is left in the index.

- Garden lanes, 19: way/653417191, 653417192, 653417193, 653417195,
  653417196, 653417197, 653417199, 653417200, 653417201, 653417202,
  653417203, 653417207, 653417218, 653417228, 653417230, 653417232,
  653417233, 653417234 and way/116815796 ("Centra līnija"). Their sibling
  "4 Līnija" (way/653417214) is residential class and stays.
- Station tunnels, 3: way/155650361 ("A tunelis"), way/42206973 ("B
  tunelis"), way/155314061 ("C tunelis").

Daugavpils and Liepaja have no by-id drop. **Daugavpils keeps by the owner's
word** the fortress's nine numbered landmarks and one place (ruling 3); they
need no config entry today, since no rule takes them.

**For each city's eye read, not for a list:** the pedestrian areas
"Lāčplēša kara ordeņa kavalieru piemiņas stēlas" (Riga, a memorial drawn as
a street) and "Kungu ielas radošais kvartāls" (Liepaja); the places
"Mežaparka rezidences", "Imanta-1" to "Imanta-5", "1. terase", "2. terase",
"A-B dambis" (Riga) and "Sapnis D" (Daugavpils); English-only names ("Former
military training ground", "Speedway Stadium", "Jews in Latvia").

## Shared-code findings (not edits)

1. **A home word that closes the name.** Latvian puts the house word last
   ("Mindeļa villa", historic=building on building=yes, Riga), so
   `HOME_NAME_LEAD` catches only "Villa 'Wasa'" (1 row). `HOME_NAME_END`
   exists for Korean, Chinese and Georgian and reads the last word for a
   Latin-script language; an entry `"lv": ("villa",)` would take 1 row today.
   Not "nams" or "māja" (above). The draft JSON has no field for it, and
   `build_dump.py` patches none.
2. **Coded names.** `CODED_TYPE` has no Latvian entry. If one is written
   ("N. līnija" with no neighborhood, "A tunelis"), it must not take the
   Daugavpils fortress's numbered works (ruling 3), nor "Dārziņu 1. līnija"
   and its like, which are addressed streets.
3. **Russian needs no list.** No `name` in any of the three caches holds
   Cyrillic. A Russian form exists only as `name:ru`: Daugavpils 271 of
   1,752 named elements (15.5%; 43 of 455 distinct street names), Riga 3,374
   of 10,860 (31.1%; 412 of 1,947), Liepaja 77 of 1,518 (5.1%; 16 of 400).
   `name:ru` is read only if "ru" is in `PLACE_LANGUAGES`, and a declared
   language under 90% of rows stops the build (`LOCAL_MIN`), so Russian
   cannot be declared and brings no name into an index. The limit this
   leaves: a Russian form typed in Cyrillic finds nothing, in Riga as much
   as in Daugavpils.
4. **The scratch scripts.** `variant.py` adds the language to
   `SUFFIX_WAY_LANGUAGES` whatever the draft's "suffix" says;
   `measure_lang.py` tries every way word as an ending and counts
   `pedestrian` and `platform` as minor, which `MINOR_HIGHWAYS` does not;
   `build_dump.py`'s `streets.tsv` is distinct names, not street rows, and a
   newline in a tag value broke a row (fixed in `final_build.py`).

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map was rendered, so none of this has met the search box.

```
lv: {join: ["un"], stop: [],
     street: ["iela", "bulvaris", "prospekts", "gatve", "laukums", "aleja", "linija",
              "soseja", "cels", "dambis", "krastmala", "tilts", "skvers"],
     lead: [], station: ["stacija", "pietura"],
     abbr: {"bulv": "bulvaris", "prosp": "prospekts", "pr": "prospekts",
            "lauk": "laukums", "sk": "skersiela", "sv": "sveta"}}
```

Open for whoever folds it, each to test in the browser first:

1. Does `norm()` strip the Latvian marks (ā č ē ģ ī ķ ļ ņ š ū ž)? "Brivibas
   iela" must find "Brīvības iela".
2. The usual written short form is "Brīvības ie." or just "Brīvības": the
   street word must be optional at the end, as English "St" is.
3. Genitive against nominative: a reader types "Brīvība" or "Raiņis" for
   "Brīvības iela", "Raiņa bulvāris". Prefix matching covers the first, not
   the second.
4. Numbered lines: "1. līnija" typed "1 linija", and "Dārziņu 1. līnija".
5. "stacija" as a station word must not swallow the tram stops named
   "Stacija" in Daugavpils and Liepaja.
6. Regression queries: "Brīvības iela", "brivibas", "Krišjāņa Barona iela"
   typed "Kr. Barona", "Raiņa bulvāris un Brīvības bulvāris", "Vanšu tilts",
   "Dārziņu 1. līnija" (Riga); "Rīgas iela", "18. novembra iela", "Stacija"
   (Daugavpils); "Lielā iela", "Vecā ostmala", "Rožu laukums" (Liepaja).

`place_search_review.py`'s `PLACE_WORD` needs the Latvian place words too
(parks, dārzs, skvērs, laukums, baznīca, katedrāle, kapi, tilts, sala, ezers,
kalns, muzejs, piemineklis, pludmale, forts), so `odd` stays readable.
