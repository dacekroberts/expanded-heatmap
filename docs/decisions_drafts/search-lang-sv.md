# Swedish (sv): settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code. Measured
2026-10-13 on the two Swedish-language cities, Stockholm and Göteborg, each
built in memory on `place_index.py` as it stands after master's second rule
batch, with the lists patched for the process (place caches of 2026-10-13,
OSM base 2026-10-12T20:21:35Z; `BARE_TYPE_NAMES` and `_BARE_FOLDED` both
patched; English "store" set aside). These are every city of the language
on the map today; a third city is measured before it relies on them.

## The owner's rulings (2026-10-13)

1. **English "store" is set aside for Swedish.** "Store" and "Stora" are
   Swedish for "great" and lead place names. In Göteborg the word dropped
   the headland Store udd (1 place row, now back: 370 to 371 places) and
   made the street Store Udds Väg an index leak hit (now none). A
   shared-code change for Cleanup; see the findings below.
2. **-gård and -gården, with -gårdar and -gårdarna, are IN, with an id
   catch as German -hof has.** 67 distinct street names: Göteborg 64,
   Stockholm 3. The 5 that are no street are dropped by id (8 ways), which
   leaves 62: Göteborg 61, Stockholm 1.
3. **-lycka and -lyckan, with -lyckor and -lyckorna, are IN.** 14 street
   names, all Göteborg. No misfire read.
4. **-gång and -gången are IN** (235 street names: Stockholm 89, Göteborg
   146; one underpass dropped by id), **and -faret is IN** (11, Stockholm
   only; 8 of them the named underground delivery streets of the center).
5. **-spår is OUT** (6 trail names in Stockholm, 8 rail-yard service ways in
   Göteborg). **-äng, -hage and -gärde are OUT** (12, 5 and 5 names, all
   Göteborg).
6. **The misfires read go by id**: descriptions under väg, stig and bro,
   the underpass, the indoor arcade, the Gallerian walkways and the
   "Serviceväg N" ways. 12 ids in Stockholm, 14 in Göteborg
   (`by_id_<city>.json`).

**The future edit point for -gård (owner):** the word also ends a churchyard
(kyrkogård), a garden (trädgård), a schoolyard (skolgård), an inner yard
(innergård) and a local-history farm (hembygdsgård). Five such names exist
today and are dropped by id. A later OSM edit can add another, and only a
read finds it: when a Swedish city's cache is refreshed, list its minor-way
street rows ending -gård, -gården, -gårdar or -gårdarna that are new since
the last read.

**The same for -gång:** list the new minor-way rows ending -gång or -gången
and look for "ingång" (an entrance), "uppgång" and "nedgång" (a station
exit), "undergång" and "övergång" (an underpass, a crossing). One exists
today and is dropped by id.

## The lists

`LANGUAGE_NAMES` already holds `"sv": "Swedish"`.

`LEAK_WORDS["sv"]` (46): hotell, vandrarhem, pensionat, värdshus, parkering,
parkeringsplats, parkeringshus, parkeringsgarage, kundparkering,
besöksparkering, personalparkering, p-hus, garage, privat, privatväg, butik,
affär, restaurang, apotek, ab, aktiebolag, handelsbolag, brf,
bostadsrättsförening, bostadsrättsföreningen, bostadshus, flerfamiljshus,
lägenheter, radhus, studentbostäder, äldreboende, vårdboende, seniorboende,
samfällighet, köpcentrum, galleria, gallerian, stormarknad, bensinstation,
infart, utfart, inlastning, varumottagning, godsmottagning, serviceväg,
drive-in.

`HOME_WORDS["sv"]` (14): privat, privatväg, brf, bostadsrättsförening,
bostadsrättsföreningen, bostadshus, flerfamiljshus, lägenheter, radhus,
studentbostäder, äldreboende, vårdboende, seniorboende, samfällighet.

`WAY_WORDS["sv"]` (70), with `"sv"` in `SUFFIX_WAY_LANGUAGES`: gata, gatan,
väg, vägen, gränd, gränden, stig, stigen, backe, backen, torg, torget, plan,
plats, platsen, allé, allén, gång, gången, bro, bron, spång, spången, trappa,
trappan, trappor, trapporna, trapp, brink, brinken, krok, kroken, krokarna,
slinga, slingan, kaj, kajen, led, leden, lid, liden, stråk, stråket, strand,
stranden, promenad, promenaden, esplanad, esplanaden, tunnel, tunneln,
viadukt, viadukten, passage, passagen, terrass, terrassen, svängen, ringen,
länken, rundan, faret, gård, gården, gårdar, gårdarna, lycka, lyckan, lyckor,
lyckorna.

Swedish glues the way word to the name and adds the definite ending
(Storgatan, Sveavägen), and writes it apart after a genitive ("... Gata",
"... Väg"). Each word is therefore listed in its indefinite and definite
form, and plural where streets use it (trappor, krokarna, gårdar, lyckor).

No `WAY_LEAD` and no `WAY_ENDING`: Swedish street names do not lead with a
preposition. The commonest first words are adjectives (Norra, Södra, Lilla,
Stora, Gamla), which decide nothing.

`HOME_NAME_LEAD["sv"]` (2): villa, bostadshus.

`BARE_TYPE_NAMES["sv"]` (34): kyrka, kyrkan, kapell, kapellet, park, parken,
lekplats, lekplatsen, lekpark, minnesmärke, minnessten, minneslund, fontän,
fontänen, kyrkogård, kyrkogården, begravningsplats, skulptur, staty, byst,
kors, fotbollsplan, bollplan, idrottsplats, badplats, utsikt, utsiktsplats,
utsiktspunkt, gravfält, runsten, domarring, kvarnruin, hamnkran, lekparken.
Whoever folds the list adds the words to `BARE_TYPE_NAMES` only;
`_BARE_FOLDED` is built from it at import.

## What was measured

The final build, by-id drops applied:

| City | Rows | Streets | Landmarks | Places | Stations | Streets dropped by a leak word | Minor-way names not read as a way |
|---|---|---|---|---|---|---|---|
| Stockholm | 6,500 | 5,000 | 1,119 | 241 | 138 | 0 (3 before the by-id drops) | 67 |
| Göteborg | 6,731 | 5,703 | 523 | 371 | 133 | 0 (3 before the by-id drops) | 307 |

Swedish is on 100% of names in both and English on 0.9% (Stockholm) and 0.2%
(Göteborg), so each page names Swedish only. No index leak hit in either
city. Distinct street names: 4,919 and 5,661. The step's own count of minor
ways dropped as no way name is 206 ways in Stockholm and 765 in Göteborg;
the table counts distinct names. Stations within 1 km of an indexed place
were not measured here.

**What moved against the first draft, and why.**

- Streets: Stockholm 5,003 to 5,006 with -gård in, then 5,000 after the
  by-id drops. Göteborg 5,634 to 5,712 with -gård and -lycka in (64 and 14
  names), then 5,703 after the by-id drops.
- Places: Göteborg 370 to 371, Store udd back with "store" set aside.
- **Stations: Göteborg 134 to 133, not from these lists.** The row
  "Virginsgatan" is gone on the rebuilt `place_index.py`; the lists do not
  touch stations, so this is master's second rule batch. Not traced further.
- Göteborg's street ways dropped by a leak word went from 5 to 3 before any
  list change of this round; the three left are the "Serviceväg N" ways.
  "Max Drive-In" (service=drive-through) is no longer counted there, which
  also points at the rule batch. Not traced further.

**Why Göteborg's cache holds fewer named non-highway elements (1,982
against Stockholm's 7,236).** It is not a short fetch: both caches carry the
same OSM base time and no remark. Stockholm's count is 4,933 named city
blocks (place=city_block, the kvarter names; Göteborg has 3). Without them
the two are 2,303 and 1,979. Stockholm also has more mapped parks (426
against 70) and artworks (453 against 161), which is where its landmark
count comes from.

- **Way words.** Stockholm has 651 distinct names that sit only on minor
  ways; 560 have a street row. Göteborg has 1,414; 969 have one. Of the
  rest, 24 (Stockholm) and 138 (Göteborg) read as a way and are dropped by
  id or by the rules for driveways, parking aisles and closed or private
  ways.
- **Names not read as a way.** Stockholm's 67 were all read: bus platform
  labels, numbered service ways, mountain-bike trail nicknames, station
  mezzanines, an indoor arcade, six exercise trails, and paths named after
  the park, harbor or jetty they cross. None is clearly a street; the
  nearest are Skosnöret and Alviksskälet, a cycleway and a footway under a
  single noun. Göteborg's 307: 94 are coded lanes of the port and the car
  plant ("TCV 1", "GM TUF"), about 45 are the meadow, terrain and facility
  names left out below, and most of the rest are single nouns in the
  definite form on a service way (Fjällblomman, Sockerbruket), which the
  city also uses for residential streets, where they are kept as named.
- **Leak words.** The only Swedish words that decide anything today are
  gallerian (3 walkways in Stockholm) and serviceväg (3 ways in Göteborg).
  The rest are the usual markers, listed ahead of need. Measured and left
  out: centrum (9 hits, district centers and a tram stop), krog (a city
  block's name), tomt (an archaeological site), hb and kb (a locality named
  "HB"), villa (a residential street leads with it in Göteborg).
- **Bare type words that hit as a whole name** (raw cache counts): gravfält
  2, kyrka, fontänen, kyrkogården, utsiktspunkt, runsten, domarring, byst,
  kors, kvarnruin, hamnkran, lekparken, one each in Stockholm; minnessten 1
  in Göteborg. The step's count of landmarks dropped as a bare type, English
  words included, is 11 in Stockholm and 1 in Göteborg.
- **Home words.** "villa" leads two Stockholm names: one is dropped as a
  home, one is a gallery and stays.

## What is left out, and why

- **Bare type words:** NOT "skansen" (four elements of the open-air museum
  carry it as their real name), NOT "torget", "torg", "saluhallen" or
  "obelisken" (real names in use), and no artwork title that is a common
  noun (Källan, Morgonbad).
- **Meadow and pasture endings (owner: out):** -äng, -ängen, -ängar 12
  names, -hage, -hagen 5, -gärde, -gärdet 5, all Göteborg. The same words
  name districts and parks.
- **Trails (owner: out):** -spår, -spåret.
- **Terrain, measured, not put to the owner as a call:** -ås, -åsen 9 names
  (a two-letter ending), -berg, -berget 8, -dal, -dalen 8, -kulle, -kullen
  and -höjd, -höjden 5. Hills, valleys and house names.
- **Facilities:** -park, -parken 11 names (paths inside a park), -hamn,
  -hamnen 5 (harbors), -port, -pir, -brygga with their forms 15 (gates,
  piers, jetties), -gläntan and -torp, -torpet 6.
- **A trailing "villan"** on one Göteborg landmark (historic=building): left
  for the place read, not listed as a home word.
- **To review by name once built:** Birger Jarlspassagen (Stockholm), a
  covered arcade with its own Wikipedia article, kept as a street row.

## Loose words, with their counts

Distinct street names each word holds, from in-memory builds.

| Word (with its forms) | Stockholm | Göteborg | Not streets | Future edit point |
|---|---|---|---|---|
| gård, gården, gårdar, gårdarna | 3 | 64 | 5, dropped by id | new -gård rows read at each cache refresh |
| gång, gången | 89 | 146 | 1 underpass, dropped by id | new -gång rows: ingång, uppgång, undergång |
| lycka, lyckan, lyckor, lyckorna | 0 | 14 | 0 read | none; re-measure on a third city |
| faret | 11 | 0 | 8 underground delivery streets, kept as named streets | none; Stockholm's own word |
| plats, platsen | 0 | 31 | 0; "Kontrollplats" already goes as closed | a new "...plats" that is a parking or play area |
| plan | 14 | 9 | 0 | a sports field ("...bollplan") on a path |
| passage, passagen | 2 | 8 | 1 indoor arcade in Stockholm, dropped by id | a new indoor=yes passage |
| stråk, stråket | 0 | 15 | 0; six are the color-named ways of a hospital site, its addresses | none |
| lid, liden | 0 | 13 | 0 | none |
| strand, stranden | 5 | 0 | 0; quay walks named as streets | a "badstrand" on a path |

**Misfires per word on minor-way-only rows**, all dropped by id. väg: 1 name
in Stockholm, 2 in Göteborg. stig: 1 and 2. bro and bron: 1 and 1. gång: 1
in Göteborg. gård and its forms: 2 and 3. passage: 1 in Stockholm. Zero
read: gata, gränd, backe, torg, plan, plats, allé, trappa and its forms,
brink, krok, slinga, kaj, lid, lycka, stråk, strand, promenad, terrass,
tunnel, spång, svängen, ringen, rundan, faret. Zero rows today, listed for
the next city: led, leden (larger roads only), viadukt, esplanad, länken,
gränden.

## The id catches

`by_id_stockholm.json` (12 ids, 7 names) and `by_id_goteborg.json` (14 ids,
12 names), each id checked against its cached name, in the shape
`{"ids": [[id, cached name, why]], "streets": [[name, why]]}`.

- **Stockholm.** -gård: Innergård (1 way), Stadshusträdgården (2 footpaths;
  the garden's own landmark row stays). Descriptions: "ridväg" (2 ways),
  "Liten stig" (1), "Gångbron" (2). Hötorgspassagen (1, indoor=yes). The
  three Gallerian walkways, which the leak word already takes: the ids are
  a backstop.
- **Göteborg.** -gård: Örgryte Nya Kyrkogård (1), Ellerödsträdgården (1),
  Gunnesby Hembygdsgård (2). Descriptions: "Clareberg ridväg" (1), "Stora
  Billingens Cykelväg" (2), "Naturstig" (1), "Reservstig" (1), "Amhults
  undergång" (1). A staff footbridge of one building (1). The three
  "Serviceväg N" ways, which the leak word already takes.
- **A correction to the first draft: Göteborg's four "arcades" are not
  dropped.** The draft said "up to 4 shopping arcades" under -passagen.
  Their tags say otherwise: Drottningpassagen, Kungspassagen, Torgpassagen
  and Victoriapassagen are open lanes through city blocks (surface=sett,
  some segments tunnel=building_passage, none indoor). They stay as street
  rows and are named here for the place read. Stockholm's Sturegallerian
  (indoor=yes) never had a row: nothing reads it as a way.

## Shared-code changes the language needs (findings, not edits)

1. **English "store" must not be read as a leak word in a Swedish city.**
   `leak_word()` reads the English list in every city. The builds here
   removed "store" from `LEAK_WORDS["en"]` for the process, which is not a
   fix to land: English cities need the word. What is needed is a
   per-language set-aside of English leak words (Danish asks for the same
   word). The draft records it as `"en_leak_set_aside": ["store"]`.
2. **`"sv"` joins `SUFFIX_WAY_LANGUAGES`.**
3. **A trailing home word.** `HOME_NAME_END` is read as a name's last word
   for Korean, Chinese and Georgian only. Swedish writes "... villan" last.
   One row today; no change asked for, noted for a third city.
4. **Descriptions on minor ways.** "ridväg", "Naturstig", "Gångbron" and
   "Liten stig" are a type word, or a type word with an adjective, standing
   in for a name. `bare_type()` is not applied to street rows, so they go by
   id. A bare-type test on minor-way street names would catch the class.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map is rendered here, so none of this has met the search box.

```
sv: {join: ["och", "hörnet"], stop: ["den", "det", "de", "i", "på", "av", "vid"],
     street: ["gatan", "gata", "vägen", "väg", "gränd", "stigen", "backen", "torget", "torg",
              "plan", "platsen", "plats", "allén", "allé", "gången"],
     lead: [], station: ["station", "stationen", "centralstation", "hållplats", "tunnelbana",
                         "t-bana", "pendeltåg"],
     abbr: {"g": "gatan", "v": "vägen", "gr": "gränd", "st": "sankt", "s:t": "sankt",
            "n": "norra", "s": "södra", "ö": "östra"}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. Swedish writes the street word inside the name ("Drottninggatan"), and
   the usual abbreviation is a suffix ("Drottningg.", "Sveav."). `abbr`
   matches whole words, so a suffix form or a prefix match on the last word
   is needed, as for German "Hauptstr.".
2. "v" is both "vägen" and "västra"; the draft gives it to "vägen". Test
   "V Hamngatan" before trusting either.
3. å, ä and ö typed as a, a and o ("Gotgatan", "Linnegatan"); é typed as e.
4. "S:t" and "Sankt" must meet ("S:t Eriksgatan"), and the genitive with and
   without its space ("Sergels torg", "Mariatorget").
5. Regression queries to add: "Drottninggatan", "Sveavägen", "Sergels
   torg", "Götgatan och Folkungagatan", "S:t Eriksplan" (Stockholm);
   "Kungsportsavenyen" typed "Avenyn", "Götaplatsen", "Linnégatan" typed
   "Linnegatan", "Västra Hamngatan och Kungsgatan", "Store Udds Väg"
   (Göteborg).

`place_search_review.py`'s `PLACE_WORD` needs the Swedish place words too
(park, parken, torg, kyrka, kyrkan, kyrkogård, bro, sjö, skog, berg,
trädgård, museum, minnesmärke, viken, holmen, badet), so `odd` stays
readable.

## Files beside this one

`draft_sv.json` (the final lists), `by_id_stockholm.json`,
`by_id_goteborg.json`, `final_dump/<city>/` (every row with ids and tags,
`rows_<kind>.tsv` and `streets.tsv`, by-id drops applied), `final_build.py`
(the wrapper that built them). From the first round: `variant_<city>.txt`,
`perword_<city>.txt`, `loose_<city>.txt`, `rep/`, `dump/` and `pre_dump/`
(the ruled lists before the by-id drops).
