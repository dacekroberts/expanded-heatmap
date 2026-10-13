# Norwegian (nb): settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code. Measured 2026-10-13
on the two Norwegian cities, Oslo and Bergen, each built in memory with the
lists patched for the process (place caches `osm_places_2026-10-13.json` and
`osm_places_extra_2026-10-13.json`), on `place_index.py` as it stands after
master's second rule batch was merged. These are every city of the language
on the map today; a third city is measured before it relies on them. Bokmål
and Nynorsk forms sit under the one code `nb`: Bergen's names carry both
("-vegen" on 222 larger street names, "-veien" on 197) and its own town forms
("-gaten", "-broen", "-kaien", "-smauet", "-allmenningen").

The machine-readable lists are `draft_nb.json` beside this file. The final
rows are in `final_dump/<city>/`, the by-id drops in `by_id_oslo.json` and
`by_id_bergen.json`.

## The owner's rulings (2026-10-13)

1. **English "store" is set aside for Norwegian** ("store" is Norwegian for
   big). A shared-code change Cleanup makes; built here with the word set
   aside in memory. It returns 4 rows in each city: Bergen's Store
   Lungegårdsvannet, Store Stuthaugen, Store Langhaugen and the street Store
   Starefossen; Oslo's Store Borgen, Store Frøen and two landmarks.
2. **Terrain endings are way words.** In: -lia, -lien, -toppen, -grenda,
   -grenden, -tunet, -jordet, -kollen, -berget, -haugen, -gården. They add 22
   street rows in Oslo and 27 in Bergen (49). Out: -åsen, -dalen, -hagen,
   -dammen, -porten, -parken, -gang, -ring.
3. **Historic farms are held to the home rule:** dropped until visiting is
   shown, kept on an article of their own. 58 Oslo landmarks go by id
   (55 `historic=farm`, 3 `historic=croft`); 5 stay on an article, 1 on its
   name (below). Bergen has none.
4. **By precedent, in:** "as" (the company form; 1 row, a Bergen park named
   for a company) and "borettslag" (a housing co-operative mapped as a
   neighborhood; 2 Bergen places, one of which the estate rule now takes
   first).
5. **Dropped by id:** the way-word misfires of the read (9 Oslo streets, 6
   Bergen streets) and Bergen's 24 monuments named by a two-letter code.

## The lists

`LANGUAGE_NAMES` already holds `"nb": "Norwegian"`.

`LEAK_WORDS["nb"]` (53): hotell, hotel, pensjonat, vandrerhjem, parkering,
parkeringsplass, parkeringshus, parkeringsanlegg, parkeringskjeller, p-hus,
p-plass, beboerparkering, gjesteparkering, garasje, garasjer, garasjeanlegg,
garasjeport, privat, privat vei, privat veg, privatvei, innkjørsel,
innkjøring, utkjørsel, utkjøring, avkjørsel, oppkjørsel, adkomst, atkomst,
varelevering, varemottak, butikk, restaurant, kafé, kafe, apotek, as, a/s,
asa, borettslag, brl, sameie, sameiet, boligsameie, kjøpesenter, legesenter,
tannlege, leiligheter, boliger, studentboliger, omsorgsboliger, snuplass,
busslomme.

`HOME_WORDS["nb"]` (14): privat, privat vei, privat veg, privatvei,
borettslag, brl, sameie, sameiet, boligsameie, leiligheter, boliger,
studentboliger, omsorgsboliger, beboerparkering.

`WAY_WORDS["nb"]` (90), with `"nb"` in `SUFFIX_WAY_LANGUAGES`. Norwegian
glues the way word to the name and adds a definite ending ("Bogstadveien",
"Strandgaten", "Bjølsengata"), so each form is listed on its own:

- roads and streets: vei, veien, veg, vegen, gate, gata, gaten, allé,
  alléen, strede, stredet, veita, veiten, ringen, faret, stubben
- squares and quays: plass, plassen, torg, torget, torv, torvet,
  allmenning, allmenningen, almenning, almenningen, kai, kaia, kaien,
  brygge, brygga, bryggen, terrasse, terrassen
- lanes, paths and trails: sti, stien, stigen, smau, smauet, smug, smuget,
  gangen, tråkk, tråkket, løype, løypa, løypen, passasje, passasjen,
  promenade, promenaden
- slopes and bends: bakke, bakken, bakkene, bakkane, kleiv, kleiva,
  kleiven, kleivene, sving, svingen, svingene, svingane, krok, kroken
- structures: bru, brua, bro, broen, trapp, trappa, trappen, trappene,
  tunnel, tunnelen, tunellen, viadukt, undergang, undergangen
- terrain endings (ruling 2): lia, lien, toppen, grenda, grenden, tunet,
  jordet, kollen, berget, haugen, gården

No `WAY_LEAD` and no `WAY_ENDING`: no preposition lead added a row in either
city ("Gamle Hadelandsvei" already ends in a way word).

`HOME_NAME_LEAD["nb"]` (1): villa. NOT "hus" or "gård" as a lead: neither
leads a name in either city.

`BARE_TYPE_NAMES["nb"]` (21): kirke, kapell, park, lekeplass, leikeplass,
lekeplassen, minnesmerke, monument, statue, skulptur, fontene, kirkegård,
gravlund, krigsminnesmerke, minnelund, kanoner, kanon, relieff, telefon,
gurdwara, bosetning. NOT "torget" and NOT "bryggen": Bergen's Torget and
Bryggen are those places' real names. NOT "utsikten", "tempelet", "stranden",
"dammen", "hagen": each names a peak or a locality here.

## What was measured (final build)

With the lists, "store" set aside and the by-id drops applied:

| City | Rows | Streets | Landmarks | Places | Stations | Street ways dropped by a leak word | Minor ways not read as a way | Minor-only names not read |
|---|---|---|---|---|---|---|---|---|
| Oslo | 5,017 | 2,871 | 1,147 | 791 | 194 | 1 | 540 | 113 of 468 |
| Bergen | 3,284 | 2,126 | 526 | 586 | 46 | 1 | 1,848 | 81 of 325 |

Oslo also holds 14 junction rows. Norwegian is on 100% of names in both
cities and English on 0.8% (Oslo) and 0.5% (Bergen), so each page names
Norwegian only. `name:nn` is on 4 objects in Bergen and `name:no` on 59 in
Oslo; neither is read. Whether every map station has an indexed place within
1 km was not measured.

**What moved since the draft, and why.** Before any by-id drop the builds
give Oslo 5,083 rows and Bergen 3,314. The draft gave 5,107 and 3,311, and
"store" returns 4 rows in each, so Oslo is 28 rows lower and Bergen 1 lower
for a reason that is not these lists: master's second rule batch (its new
drops show in the build report as gardens 32 and 13, register entries 3,
estates 3 and 1). The by-id drops then take 66 rows net in Oslo (58 farms
and 9 street names; one row fewer than their sum, not traced) and 30 in
Bergen (24 monuments, 6 streets).

- **Minor ways not read as a way.** The count is of ways, not names. Most
  are service roads that share a terrain name with a residential street,
  which keeps its row. A "minor-only name" has no way of residential class
  or above.
- **Way words.** 355 of Oslo's 468 minor-only names and 244 of Bergen's 325
  read as a way. The busiest words on minor-only names: -veien 93, -stien
  80, vei 57, -smauet 40 (Bergen only), -bakken 37. Listed and matching no
  minor-only name in either city, kept for larger streets or the next city:
  alléen, bakkane, torv, torvet, strede, smau, smug, allmenning, almenning,
  kai, brygga, sving, svingane, krok, kleiv, passasje, promenade, ringen,
  veita, viadukt, tråkk, undergang, undergangen.
- **"tunellen"** is a misspelling on two ways (Ammerudtunellen,
  Kronstadtunellen), listed so the two tunnels keep their rows.
- **Leak words, what each met.** Oslo: garasje 2 service ways (bus garages),
  boligsameie 2 parks (a co-operative's shared gardens), beboerparkering 1
  and parkering 1 service way, snuplass 1 (a bus turning place), restaurant
  1 viewpoint, hotell 1 bus stop. Bergen: borettslag 2 neighborhoods, sameie
  1 footway, garasjeport 1, busslomme 1, snuplass 1, as 1 park. The other
  words met no name in either city and are listed as strong markers,
  unmeasured.
- **Bare type words, rows each takes:** telefon 8 (Oslo 6, Bergen 2: listed
  telephone kiosks), lekeplassen 1, minnelund 1, gurdwara 1, bosetning 1.
  "kanoner" is the whole name of 7 Bergen objects and "relieff" and
  "krigsminnesmerke" of 1 each, none of which reaches the index anyway; the
  words stay as a guard.
- **Home words.** "villa" leads 5 Oslo names; one reaches the index (Villa
  Stenersen, a museum with a wikidata item) and stays under the public-home
  rule.

## What is left out and why

- **Not leak words, measured.** senter: 27 Oslo and 16 Bergen names, among
  them tram stops, a museum and places of worship. verksted: 8 Oslo names,
  memorials to a shipyard. terminal: 21 Bergen names, stations. skole and
  barnehage: stops and a chapel named after a school. bensinstasjon: one
  Bergen museum. bolig: a memorial and a park. inngang: a mine entrance.
  lekeplass: one named playground (a bare type word instead).
- **Way endings out (ruling 2), distinct minor-only names over both
  cities:** -åsen 8, 4 no street ("Tåsen senter" and three trail
  descriptions); -dalen 6, 3 no street; -hagen 5, 3 gardens; -dammen 5, all
  paths around ponds; -porten 4, 2 station hallways; -parken 3, none a
  street; -gang 1 (it would also end "inngang" and "utgang"; "-gangen" is in
  and reads Bergen's three); -ring 0 (it ends "parkering" and "rundkjøring";
  "-ringen" is in).
- **Not measured enough to list, one or two names each:** -løkka, -skogen,
  -kurven, -kneika, -viken, -banen, -hellinga, -brekka, -brekken, -høgda,
  -leitet, -brotet, -neset, -træet, -engen, -heia, -lunden, -myra, -stranda,
  -bølgen. The leads gamle, langs, til, ved, mot, den, på, under, over, bak
  add no row; "via" adds one that is kept anyway by its wikidata.
- **Real streets still lost,** about 10 in each city, by their tags: Oslo's
  Asperudåsen, Hauketoåsen, Langteigåsen and Meklenborgåsen (-åsen),
  Giskehagen, Dalsløkka, Sørhellinga, Smalåkeren, Gamlelinja, Koll aveny;
  Bergen's Paradisleitet, Sandeidbrotet, Skjenbrekken, Skredderdalen,
  Ulvhøyen, Karensfryd, Bahustræet.

## Loose words and their future edit points

Rows are distinct minor-only street names; "no street" is by the tags (class,
access) and the name's look. No address register was read: the caches hold 2
`addr:street` tags.

| Ending (in) | Rows added | No street |
|---|---|---|
| -gården | 17 (Bergen) | 1, a war cemetery kept anyway by its wikidata; 16 are the named yards and passages of Bryggen and the old town |
| -lia, -lien | 8 | 0 |
| -grenda, -grenden | 8 | 0 |
| -tunet | 5 | 0 |
| -toppen | 4 | 0 |
| -jordet | 3 | 0 |
| -berget | 3 | 0 |
| -haugen | 3 | 0 |
| -kollen | 2 | 0 |

**The future edit point (terrain endings):** every one also ends a hill, a
farm or a housing cluster, and "-gården" ends "kirkegården" (a cemetery) and
"skolegården" (a schoolyard). No such row exists today beyond the cemetery
above. When a Norwegian city's cache is refreshed, list its minor-way street
rows with these endings that are new since the last read; a misfire goes by
id.

**The future edit point (farms):** the 58 farm drops are by id, so a farm
mapped later comes in until the home-ending rule below exists. When Oslo's
cache is refreshed, list the landmark rows whose last word ends in "gård"
that are new since this read.

**Suffix matching reads any word of the name, not only the last:** "Tåsen
senter" would read as a way under "-åsen", and "Gangsti,
Firdagaten-Blekenberg" does under "-gaten". Shared behavior, noted for the
reader.

**Misfires per word on the minor-only names read as a way** (all 355 and 244
read, not a sample): vei 6 of 57, sti 2 of 6, vegen 1 of 15, torget 1 of 3,
plass 1 of 15, veg 1 of 5, bakken 1 of 37, English "tunnel" 1. Zero: veien,
stien, gate, gata, gaten, smauet, brua, bru, bro, broen, trapp and its forms,
kroken, svingen, faret, stubben, kleiva, passasjen, promenaden, kaien,
gangen, løypa and its forms, terrasse. Each misfire is in the by-id files.

## The id catches

`by_id_oslo.json` and `by_id_bergen.json`, in the shape
`{"ids": [[id, cached name, why]], "streets": [[name, why]]}`. Every id was
checked against its cached name by the script that wrote the file.

**Oslo, 58 ids:** historic farms with no wikidata, no wikipedia and no tag
that shows visiting (55 `historic=farm`, 3 `historic=croft`). One of them,
Årvoll gård, only surfaced after a same-named object was dropped; the build
was repeated until a pass found nothing new.

**Oslo farms kept** (also listed in the file under `kept_farms`):

- On an article of their own (wikidata): Bakkehaug gård, Geitmyra gård,
  Madserud gård, Nordseter gård, Ulsrud gård.
- On its name: Sørli besøksgård ("besøksgård" is a visiting farm). No tag
  shows visiting, so this one is a judgment for the owner to confirm.
- No Oslo farm carries a tag that shows visiting (no museum, opening hours
  or `tourism=attraction`). Linderud gård is a museum and is not
  `historic=farm`; it was never in the class.
- For the owner's eye: Tøyen hovedgård (way/10501503) is in the drops. Its
  tags show no visiting and it has no article in OSM, though it stands in
  the university's botanical garden.

**Oslo, 9 streets:** "Snarvei til bussen" and "pedestrian tunnel under
railway" (descriptions), "Driftsvei" (a type word), "Exit towards
Jernbanetorget" and "Valkyrie plass stasjon (entrance)" (station exits read
as a way), and four road numbers standing in for names ("Vei 20337", "Vei
20338", "Vei 9151", "Vei 9754"; the numbered-street rule keeps a local way
word with a number, as it keeps "Rua 1").

**Bergen, 24 ids:** `historic=monument` nodes named by a two-letter code
("CQ" to "CZ", "CÆ", "DA" to "DF", "EA" to "EF", "cÅ", "cØ"). The draft said
21; the three with Norwegian letters were missed in that count.

**Bergen, 6 streets:** "Tursti" and "Ridevei" (type words), "Gangsti,
Firdagaten-Blekenberg", "Sti venåsen - Nybøvegen" and "Hamrebakken - Øvre
Titlestad" (route descriptions), "hristiania postveg" (a typing slip for
Christiania postveg, which keeps its row).

**The five bare definite forms are not in the files.** Oslo's "Kroken",
"Passasjen", "Stien" and "Stubben" and Bergen's "Broen" are whole names equal
to a listed way word on minor ways only, and the description rule already
takes them once the lists are in (5 and 1 in the build report, the fifth in
Oslo being "Driftsvei" until it goes by id).

**Still to review by name:** Oslo's "De Norske Gjærspritfabrikker a/s"
(`historic=archaeological_site`) stays in the index and carries the leak word
"a/s": check E fails on it until `config.PLACE_REVIEWED` names it or it is
dropped. Also "Farmhouse ruins" (Bergen), "Midlertidig Minnesmerke" (Oslo),
and Vigeland's 36 numbered groups ("Nr. 1: Geniemylder").

## Shared-code changes the language needs (findings, not edits)

1. **An English leak word set aside per language.** `leak_word()` reads the
   English list for every city, and `LEAK_ALLOW` removes only a listed
   compound, so no Norwegian list can excuse "store". Danish found the same.
   Measured here: 8 names in each city carry it, 4 rows in each return.
2. **A home ending for farms.** `HOME_NAME_END` exists for Korean, Chinese
   and Georgian; an `nb` entry of "gård", "hovedgård" and "prestegård" (as a
   word's ending, since "hovedgård" is one word) would hold the class to
   `_public_home` by rule and retire the 58 ids. Measured in memory on the
   earlier build: it takes 60 Oslo rows and none in Bergen. It differs from
   the ruling in one way: `_public_home` does not keep a farm on an article,
   so the five kept above would go too. Alternatively `historic=farm` and
   `historic=croft` could join `HOME_HISTORIC`.
3. **Norwegian description phrases.** `STREET_DESCRIPTIONS` is English only.
   "driftsvei", "tursti" and "ridevei" are each the whole name of one
   minor-only street (3 rows, dropped by id here).
4. **Two-letter codes as names.** `CODED_TYPE` has no pattern for a bare
   code; Bergen's 24 go by id.
5. **`build_dump.py`** writes a tag value holding a newline as it is, which
   breaks the row; `build_final.py` here replaces any run of white space
   with one space.

## What this does not show

Two cities. Trondheim's "-veita", Stavanger's and Tromsø's forms are listed
from general knowledge or not at all, and none was measured. "Street" and
"visiting" were judged from tags, never from an address register or a
farm's own site. The matcher words below have not met the search box.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map is rendered here, so none of this has met the search box.

```
nb: {join: ["og"], stop: ["i", "på", "ved", "av"],
     street: ["vei", "veien", "veg", "vegen", "gate", "gata", "gaten", "gt", "plass",
              "plassen", "pl", "alle", "sti", "stien", "torg", "terrasse", "bakken"],
     lead: [], station: ["stasjon", "stasjonen", "holdeplass", "stoppested", "t-bane", "tbane"],
     abbr: {"gt": "gate", "v": "vei", "vn": "veien", "pl": "plass", "dr": "doktor",
            "prof": "professor"}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. Does `norm()` fold ø, æ and å? NFKD splits å into a plus a ring; it does
   not touch ø or æ. Readers without the keys type "o" or "oe", "ae", and
   "aa" (which is also a real spelling: "Haakon").
2. Norwegian writes the street word inside the name ("Bogstadveien") and
   abbreviates it as a suffix ("Bogstadvn.", "Kirkegt."). `abbr` matches
   whole words, so this needs a suffix form, as German's "Hauptstr." does.
3. Definite forms differ by town and by reader: Bergen signs "Strandgaten",
   a reader types "Strandgata"; "veien" against "vegen". A typed "-gata"
   should find "-gaten", and "-vegen" find "-veien".
4. "St." is how OSM writes Sankt here ("St. Olavs gate", "St. Hanshaugen"),
   so "st": "sankt" in `abbr` is left out until it is known which side
   `norm()` expands. A typed "Sankt Olavs gate" must find "St. Olavs gate".
5. Regression queries to add: "Karl Johans gate", "Bogstadveien",
   "Kirkeveien og Bogstadveien", "Dronning Eufemias gate", "St. Olavs gate"
   typed "Sankt Olavs gate", "Doktor Smiths vei" typed "Dr. Smiths vei",
   "Majorstuen stasjon" (Oslo); "Strandgaten" typed "Strandgata",
   "Torgallmenningen", "Øvregaten" typed "Ovregaten", "Kong Oscars gate",
   "Nygårdsgaten" typed "Nygaardsgaten", "Bryggen", "Bredsgården", "Store
   Lungegårdsvannet" (Bergen). The street names were checked against the
   draft build; "Store Lungegårdsvannet" is a row of the final build.

`place_search_review.py`'s `PLACE_WORD` needs the Norwegian place words too
(park, parken, plass, kirke, kapell, gravlund, bru, vann, vannet, skog,
hage, minnesmerke, museum, gård), so `odd` stays readable.

## Scripts and files in this folder

- `draft_nb.json`: the lists (its `noterrain` variant is the draft's
  measurement aid, not a setting).
- `build_final.py`: the final in-memory build. It sets "store" aside, works
  out and writes the by-id files, applies them and dumps `final_dump/`.
- `by_id_oslo.json`, `by_id_bergen.json`: the drops.
- `explore.py`, `analyze.py`, `perword.py`, `described.py`, `checks.py`,
  `farms.py`, `review.py`, `build_nostore.py`, `build_homeend.py`: the
  draft's measurements; `dump*/`, `an1/`, `an2/`: their output, on the
  earlier `place_index.py`.
