# Danish (da): the settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code and no repository
file was changed. Measured 2026-10-13 on the three Danish cities, each built
in memory with the lists patched for the process (extract caches of
2026-10-12T20:21:35Z, the file `denmark-261012.osm.pbf`): Copenhagen (its
ten municipalities), Aarhus, Odense. These are every city of the language on
the map today; a fourth city is measured before it relies on them. The final
builds ran on `place_index.py` as of f68335fb (the second rule batch merged).

## The owner's rulings (2026-10-13)

1. **The English leak word "store" is set aside for Danish.** "Store" is
   Danish for "Great" and leads street and place names. With shared code as
   it was, 18 rows are lost: 13 streets (Copenhagen 8, among them Store
   Kongensgade, a primary street, Store Kannikestræde, Store Strandstræde,
   Store Kirkestræde, Store Regnegade; Odense 5, among them Store Glasvej and
   Store Gråbrødrestræde), 3 landmarks (Store Vejleå, a river; Store
   Kobberholm, a hill; Store Klaus, a park) and 2 places (Store Pederstrup,
   Store Ubberud). Aarhus loses none. It is a shared-code change that Cleanup
   makes (findings below); every figure here was built with "store" set
   aside in memory.
2. **Field-name endings in, the ten recommended:** -vænget, -skellet,
   -vangen, -krogen, -toften, -højen, -svinget, -kæret, -lodden, -dyssen.
   35 street rows over the three cities (Copenhagen 25, Aarhus 5, Odense 5),
   3 of them an allotment's own name (future edit point below).
3. **-gård and -gården out**, with the other endings measured out: -parken
   and -park, -haven and -have, -bakken, -lund and -lunden, -vang, -marken,
   -høj, -engen, -minde, -mosen, -løkken, -sporet, -rampen, -diget, -porten,
   -banen, -buen, -skrænten. -gård and -gården would add 23 names, 6 of them
   allotment names and 3 with restricted access.
4. **-gang and -gangen out.** They would add 65 street names (Copenhagen 53,
   Aarhus 10, Odense 2). 48 lie within 300 m of an allotment area's center
   (flower and tree series: Astersgangen, Bellisgangen, Dahliagangen,
   Ahorngang) and 9 are entrances ("Indgang C" to "Indgang N" at the Aarhus
   hospital, "Indgang 3"): "indgang" ends in "gang". The cost: about 8 real
   paths stay out (Filosofgangen in Aarhus, Søren Madsens Gang, Damegangen,
   Digtergangen, Kærgangen, Løvefodgangen, Rødhalsgangen, Sortspættegangen).

Settled by precedent, no ruling needed:

- **Allotment names are not leak words** (the German precedent). An
  association's own name on its roads ("Haveforeningen Aabrinken",
  "Hf. Bryggen", "Grønløkke Havekoloni") stays in the index: 29 street rows
  (Aarhus 17, Copenhagen 6, Odense 6).
- **A code beside a type word on minor ways drops by id** (Berlin's "Gang 1"
  to "Gang 5"). `street_description` keeps a way word beside a code in a
  language other than English, so the rows are in the index (id catches
  below).
- **Lead "ved" only.** It leads 66 larger-road names (Copenhagen 51, Aarhus
  9, Odense 6: Ved Stranden, Ved Vesterport) and adds 5 minor-way rows. Left
  out, one row each and each doubtful: "bag" (Bag skolen, a path in Aarhus),
  "under" (Under Byen, three service ways in Odense), "langs" (Langs diget
  (MTB), a mountain-bike trail), "nedenfor" (Nedenfor Grimhøj, a trail).

## The id catches

`by_id_<city>.json` beside this file, every way id checked against its cached
name by `build_final.py`; each name is a street row of the final build.

| City | Street rows | Ways | What |
|---|---|---|---|
| Copenhagen | 14 | 30 | "Vej 2", "Vej 3", "Vej 12", "Vej 14", "Vej A" to "Vej G", "Bro 7A", "Bro 7B" (13, a code beside a type word, minor ways only); "Kongelundsvej 200" (an address as a name, one service way) |
| Aarhus | 4 | 14 | Kyststien (MTB), Skrædderstien (MTB), Strandvejen (MTB), Vikingstien (MTB): mountain-bike trails |
| Odense | 8 | 32 | Blå, Grøn, Gul, Lilla and Rød Gade, Store Torv, Food Avenue, Forrest Walk: the aisles of one shopping center, footways and indoor corridors |

**A correction to the draft's count.** The draft gave 20 coded rows in
Copenhagen. 13 are on minor ways only and are in the file. The other 7, "Vej
4" to "Vej 10", each have one highway=unclassified way beside their service
ways, so the minor-way precedent does not cover them. They are NOT dropped
and are listed in `by_id_copenhagen_pending.json` (7 street rows, 40 ways)
for the owner.

Not in the files, to review by name at each city's read: "Hotel- og
Restaurantskolen" (Copenhagen, a college, dropped by the English word
"hotel"); "Riises Landsted" (historic=manor, kept); Odense's zoo and artwork
names that are a common noun (Løve, Elefant, Søløve).

## The lists

`LANGUAGE_NAMES` already holds `"da": "Danish"`.

`LEAK_WORDS["da"]` (26): hotel, hotellet, vandrerhjem, parkeringsplads,
p-plads, parkeringshus, p-hus, privat, privatvej, privat vej, butik,
restaurant, apotek, aps, a/s, supermarked, indkøbscenter, tankstation,
varelevering, indkørsel, udkørsel, boligforening, andelsboligforening,
ejerforening, plejehjem, drive-in.

`HOME_WORDS["da"]` (7): privat, privatvej, privat vej, boligforening,
andelsboligforening, ejerforening, plejehjem.

`WAY_WORDS["da"]` (53), with `"da"` in `SUFFIX_WAY_LANGUAGES` (Danish glues
the street word to the name and has a definite form: Nørregade, Teatergaden,
Brabrandstien): gade, gaden, vej, vejen, allé, alle, alléen, alleen, stræde,
strædet, plads, pladsen, torv, torvet, sti, stien, bro, broen, boulevard,
passage, passagen, kaj, kajen, gyde, gyden, trappe, trappen, tunnel,
tunnelen, promenade, promenaden, vold, volden, dæmning, dæmningen, viadukt,
viadukten, smøge, smøgen, strøg, strøget, brygge, bryggen, and the ten
field-name endings of ruling 2: vænget, skellet, vangen, krogen, toften, højen,
svinget, kæret, lodden, dyssen. "alle" beside "allé": OSM writes both
(Copenhagen's larger roads: 188 names end "Allé", 114 "Alle").

`WAY_LEAD["da"]` (1): ved. No `WAY_ENDING`.

`HOME_NAME_LEAD["da"]` (3): villa, landsted, landstedet. No name in the three
caches is led by any of them, so the list is by analogy with German and has
no measured effect. NOT "hus" or "huset" (an artwork title here; a "-hus"
ending is a town hall), NOT "gård" (a square: Boltens Gård, Paghs Gård) and
NOT "gammel" (Gammel Strand, a street and a station).

`BARE_TYPE_NAMES["da"]` (23): kirke, kapel, park, legeplads, mindesten,
mindesmærke, monument, springvand, kirkegård, skulptur, statue,
genforeningssten, genforeningsstenen, byfredssten, bautasten, mindelund,
vandkunst, græsplæne, stenkister, bænk, sten, abstrakt skulptur, steler.
Add to `BARE_TYPE_NAMES` only; `_BARE_FOLDED` is built from it at import.
NOT, since each is a place's real name here: parken (Copenhagen's national
stadium), mindelunden (Mindelunden i Ryvangen, with an article), haven (a
church of that name), grønningen and engen (parks), gadekæret (a
neighborhood in Ishøj), rundhøj (a neighborhood in Aarhus), anlægget. NOT
"untitled" (a title is not a type, as "ohne titel" was left out).

Not a list entry, and needed (ruling 1): the English leak word "store" set
aside for Danish. `draft_da.json` carries it as `leak_set_aside_en`.

## What was measured

Built with the final lists and "store" set aside, on `place_index.py` as of f68335fb, before any
by-id drop:

| City | Rows | Streets | Landmarks | Places | Stations | Streets dropped by a leak word | Minor ways not read as a way |
|---|---|---|---|---|---|---|---|
| Copenhagen | 6,609 | 5,481 | 830 | 177 | 121 | 0 | 932 ways (350 names) |
| Aarhus | 3,724 | 3,088 | 344 | 253 | 39 | 0 | 351 ways (163 names) |
| Odense | 2,388 | 2,024 | 194 | 138 | 32 | 0 | 274 ways (97 names) |

With "store" NOT set aside (shared code as it is) the leak column reads 30
ways (8 names) in Copenhagen and 27 ways (6 names) in Odense, every one a
"Store ..." street, and the indexes are 10 and 8 rows smaller (ruling 1).

**What moved on the rule batch merged since the draft,** with no list change: Copenhagen 6,611 to
6,609 rows (stations 123 to 121: Buddinge and Nørreport each lost a second row of the same name),
Aarhus 3,725 to 3,724 (the landmark Møllestien, which is also a street row). Odense is unchanged.
The Copenhagen landmark whose name split at semicolons ("SÖNDERJYLLANDS", "MODERLANDET") still has
its row; the dump's line breaks there were newlines inside tag values, now replaced by a space.

Danish is on 100% of names in all three and English on 0.6% (Copenhagen) and
0.2% (Aarhus, Odense), so each page names Danish only. No build stopped on an
uncovered station; the 1 km figure itself was not printed and is not claimed.

- **Way words, from the caches.** Named highway ways: Copenhagen 22,415,
  Aarhus 15,710, Odense 10,208. Distinct names on minor ways only:
  Copenhagen 926, Aarhus 318, Odense 181. On Copenhagen's larger roads the
  commonest endings are -vej 2,053, -gade 745, -allé and -alle 308, -vænget
  85, -plads 80, -parken 62, -bakken 59, -stien 57; on its minor-only names
  -stien 204, -vej 176, -plads 52, -gangen 43, -gade 33, -sti 25.
- **Minor-only names that ARE read as a way:** Copenhagen 606, Aarhus 128,
  Odense 75. All 809 were read, not a sample of 150.
- **Names NOT read as a way, read in full.** The largest classes are no
  streets: allotment associations under their own name (Copenhagen 62 names,
  Aarhus 26, Odense 31: "Haveforeningen Kalvebod", "Hf. Sundbo", "Dalum
  Havekoloni"), mountain-bike trails in Aarhus (25 names, "(MTB)" in the
  name), numbered and lettered service ways ("1" to "26", "B", "K"),
  entrances, and housing-estate service ways under a field name. Real
  streets among them are the classes of rulings 3 and 4; named paths with no
  ending of any kind also stay out (Cykelslangen, Svineryggen, Serpentinen,
  Kalvebod Bølge, Den grønne kile, Det Grønne Strøg is read). Pedestrian
  streets are not minor ways in the index and are kept as named (Nyhavn,
  Vimmelskaftet, Pusher Street, Immervad, Mageløs).
- **Allotment paths read by a core word.** A flower or vegetable series ends
  in the two commonest street words (Bonderosestien, 48 ways; Porrevej,
  Rødbedevej, Spinatvej). Of Copenhagen's 606 minor-only names, 45 lie within
  150 m of an allotment area's center and 69 within 300 m (Aarhus 6 and 12,
  Odense 2 and 3). A center is not an outline, so the figure is rough. They
  are named ways and no word can part them from streets; kept, as Berlin's
  colony paths ending -weg are.

### Misfires per word, on the minor-only names read as a way

No word misfires often enough to leave the list; the rows go by id.

| Word | Misfires | What they are |
|---|---|---|
| vej (whole word) | 19 in Copenhagen | "Vej 2" to "Vej 14" and "Vej A" to "Vej G" (18; 11 by id, 7 pending); "Kongelundsvej 200", an address as a name |
| bro | 3 in Copenhagen | "Bro 7A", "Bro 7B"; "Hf. Klausdalsbro", an allotment |
| bryggen | 1 in Copenhagen | "Hf. Bryggen", an allotment |
| gade | 5 in Odense | Blå, Grøn, Gul, Lilla and Rød Gade: the colored aisles of a shopping center (footways and corridors) |
| torv | 1 in Odense | "Store Torv", in the same shopping center |
| -stien | 3 in Aarhus | Kyststien (MTB), Skrædderstien (MTB), Vikingstien (MTB) |
| -vejen | 1 in Aarhus | Strandvejen (MTB) |
| -vænget, -toften, -højen | 1 each | Hf. Bispevænget, Havekolonien Lilletoften, Haveforeningen Oldhøjen |
| English "avenue", "walk" | 2 in Odense | Food Avenue, Forrest Walk, in the shopping center |

Zero misfires seen: plads, pladsen, torvet, allé, alle, alléen, passage,
passagen, stræde, strædet, strøg, kaj, kajen, smøgen, gyde, gyden,
promenade, promenaden, trappen, tunnelen, viadukten, dæmningen, boulevard,
broen, gaden, sti, -skellet, -vangen, -krogen, -svinget, -kæret, -lodden,
-dyssen, and the lead "ved". A bare way word as a whole name ("Trappen",
"Passagen", "Alleen") is already dropped by the shared way-word rule, and a
private or no-access minor way by the shared access rule ("A-Vej" to
"Z-Vej", "Kaj IV", "Kabelpladsen", the Aarhus busways).

### The loose words: names added, and how many are no street

Names that gain a street row when the word is added, over the three cities.
"Allotment" is the association's name in the street name, or a way within
300 m of an allotment center.

| Word | Added (Cph, Aar, Ode) | Allotment | Other no-street | Larger-road names it ends | Ruled |
|---|---|---|---|---|---|
| -vænget | 9 (5, 1, 3) | 1 | 1 private | 539 | in |
| -skellet | 11 (11, 0, 0) | 0 | 0 | 14 | in |
| -vangen | 2 (1, 0, 1) | 0 | 0 | 120 | in |
| -krogen | 2 (1, 1, 0) | 0 | 0 | 46 | in |
| -toften | 2 (0, 1, 1) | 1 | 0 | 99 | in |
| -højen | 2 (1, 1, 0) | 1 | 0 | 44 | in |
| -svinget | 1 (0, 1, 0) | 0 | 0 | 44 | in |
| -kæret | 1 (1, 0, 0) | 0 | 0 | 17 | in |
| -lodden | 2 (2, 0, 0) | 0 | 0 | 19 | in |
| -dyssen | 3 (3, 0, 0) | 2 near | 0 | 7 | in: Christiania's Norddyssen, Midtdyssen, Syddyssen |
| -gang | 23 (12, 9, 2) | 13 | 9 entrances | 3 | out |
| -gangen | 42 (41, 1, 0) | 35 | 0 | 10 | out |
| -gården | 14 (11, 2, 1) | 2 | 2 private; the rest housing courtyards, undecidable from tags | 23 | out |
| -gård | 9 (5, 1, 3) | 4 | 1 customers only | 19 | out |
| -parken | 5 (3, 1, 1) | 2 near | a park, a campus, a science park | 144 | out |
| -park | 2 (2, 0, 0) | 0 | both parks | 14 | out |
| -haven | 11 (7, 2, 2) | 5 | 1 MTB, 2 private, gardens | 135 | out |
| -have | 6 (2, 4, 0) | 3 | 3 gardens | 31 | out |
| -bakken | 12 (3, 8, 1) | 1 | Dyrehavsbakken (the amusement park, 15 footways), 1 MTB, sledding and park hills | 147 | out |
| -lund | 9 (4, 2, 3) | 8 | 0 | 15 | out |
| -lunden | 6 (1, 3, 2) | 3 | 0 | 48 | out |
| -vang | 6 (5, 0, 1) | 6 | 0 | 41 | out |
| -minde | 6 (2, 0, 4) | 5 | 0 | 7 | out |
| -mosen | 5 (3, 0, 2) | 3 | 0 | 13 | out |
| -løkken | 2 (0, 0, 2) | 2 | 0 | 44 | out |
| -engen | 5 (0, 0, 5) | 3 | 1 customers only | 18 | out |
| -marken | 4 (1, 0, 3) | 2 | 1 private | 68 | out |
| -høj | 9 (2, 7, 0) | 3 | 6 trail names in Aarhus (Grimhøj op, Gyvelhøj Hjem) | 78 | out |
| -sporet | 6 (0, 6, 0) | 0 | all 6 mountain-bike trails | 1 | out |
| -rampen | 3 (0, 3, 0) | 0 | 1 private, 1 steps | 1 | out |
| -diget | 2 (0, 2, 0) | 0 | 1 MTB (Langs diget) | 9 | out |
| -porten, -banen, -buen, -skrænten | 2 each | 1 each but -porten | Porten is access=no | 14, 5, 11, 12 | out |
| -linie, -molen | 1 each | 0 | Langelinie (11 service ways), Østmolen | 3, 1 | out, unmeasured beyond the one name |
| lead "ved" | 5 (5, 0, 0) | 0 | 0 | 66 | in |
| leads "bag", "under", "langs", "nedenfor" | 1 each | 0 | 2 trails, 2 doubtful | 3, 3, 3, 0 | out |

The per-word counts come from a replay of the street loop's two name tests
on the caches (`loose.py`); `variant.py`, run through the gate, confirmed
-gang, -gangen, -gård, -gården, -parken, -bakken, -diget and the leads on
full builds. Where the two differ by a name (-haven: 11 against 9), a later
rule of the build took the row.

- **Leak words.** No Danish leak word drops a street in any of the three
  cities: the caches hold almost no way named for a business. Left out on a
  measurement: "parkering" (its one hit is the tram stop "Parkering Odense
  Syd", which check E would then ask Odense to review), "værksted" (two
  museums: Arkæologisk Værksted, Dukkemagerens Værksted), "kro" (Gammel
  Vejlby Kro, historic), "kollegiet" (Rasmus Rask Kollegiet, tagged a
  college), "gård" (squares), "fabrik" (Raadvad Fabrik, a locality), "klub",
  "afdeling" and "indgang" (their names are not read as ways anyway), and the
  allotment words (precedent). Unmeasured because no name carries them, kept by
  analogy with the built languages: hotellet, vandrerhjem, the parking
  compounds, butik, apotek, aps, a/s, supermarked, indkøbscenter,
  tankstation, varelevering, indkørsel, udkørsel and the four housing words.
- **Bare type words that hit as a whole name:** græsplæne 1 (Odense, a park)
  and stenkister 1 (Aarhus). The others take no row today: the 25
  "Genforeningssten" (Aarhus 14, Copenhagen 6, Odense 5), "Skulptur",
  "Bautasten", "Bænk", "Sten", "Vandkunst", "Mindelund", "Byfredssten",
  "Steler" and "Abstrakt skulptur" are memorials and artworks the shared
  rules already leave out. They are listed so a later notable one cannot
  enter under its type.

## Future edit points

- **Allotment names by a field ending.** -vænget, -toften and -højen each
  read one allotment's own name today. When a Danish cache is refreshed, list
  the minor-way street rows that are new since the last read and carry
  "Haveforening", "Hf." or "Havekoloni".
- **A fourth Danish city** (Aalborg has field endings of its own) re-measures
  the ten endings and the lead before relying on them.
- **The English leak list.** A word added to `LEAK_WORDS["en"]` is read in
  every city: measure it on the Danish cities too ("store" was added for
  English and was never measured here).

## Shared-code changes Danish needs (findings, not edits)

1. Shared code, `leak_word`: the English "store" (ruling 1). No list entry can do it: the English
   words are read before any Danish `LEAK_ALLOW`. A per-language set-aside read in `leak_word`
   (`{"da": ("store",)}`) is what the builds here did in memory. Norwegian ("Store") would
   need the same; Swedish ("Stora") is not hit.
2. Shared code, `_named_street`: in a suffix language the "still reads as a
   street" test asks for the way word as the WHOLE last word, so a glued name
   never passes ("Store Kongensgade" ends in "kongensgade", not "gade").
   Reading the ending for a Latin-script suffix language would have kept 10
   of the 13 "Store" streets with no set-aside (Store Krog, Store Klaus and the footway Store Torv
   would not pass), but not the 5 landmarks and places. Dutch and German
   have the same gap for any leak word in a glued street name.
3. `measure_lang.py` counts pedestrian ways and platforms as minor; the index
   does not (`MINOR_HIGHWAYS`). Its "not read as a way" table overstates, so
   the tables here come from `ways_read.py`, a replay of the street loop.
4. `build_dump.py` and `variant.py` cannot set an English word aside; they
   were run through `run_da.py`, which patches the list in memory first.
5. The replay counts 920 ways not read as a way in Copenhagen where the
   build's report says 932; Aarhus and Odense agree exactly. Not traced.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map is rendered here, so none of this has met the search box.

```
da: {join: ["og"], stop: ["af", "den", "det", "de"],
     street: ["gade", "vej", "alle", "plads", "torv", "straede", "boulevard", "sti", "bro",
              "kaj", "vaenge", "passage"],
     lead: [], station: ["station", "st", "banegaard", "hovedbanegaard", "metro", "letbane"],
     abbr: {"skt": "sankt", "sct": "sankt", "gl": "gammel", "ndr": "nordre", "sdr": "sondre",
            "nr": "norre", "kgs": "kongens", "chr": "christian", "ll": "lille"}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. Does `norm()` fold æ, ø and å? They do not decompose as é does. "ae",
   "oe" and "aa" are typed for them, and "aa" is also official spelling
   (Aarhus, Aaboulevarden in older use). The words above are written in the
   folded form on that assumption.
2. "Allé" and "Alle" must meet: OSM writes both.
3. Danish glues the street word ("Nørrebrogade") and adds a definite ending
   ("Åboulevarden", "Strøget"): `street` matches whole words, so it needs a
   suffix form, as German does.
4. "St." is three things: "Store" (St. Kongensgade), "Sankt" (St. Pauls
   Gade) and "Station" (Lyngby St.). It is left out of `abbr` on purpose.
5. "Sdr." is "Søndre" and "Sønder", "Nr." is "Nørre", "Ndr." is "Nordre",
   "Gl." is "Gammel"; OSM carries some names abbreviated ("Sdr. Boulevard",
   "Gl. Lindved Å"), so the expansion may have to run both ways.
6. Regression queries to add: "Store Kongensgade" and "St. Kongensgade",
   "Strøget", "Nørrebrogade og Jagtvej", "Kongens Nytorv" typed "Kgs.
   Nytorv", "Gammel Kongevej" typed "Gl. Kongevej", "Østerbrogade" typed
   "Osterbrogade" and "Oesterbrogade", "Vigerslev Allé" typed "Vigerslev
   Alle" (Copenhagen); "Åboulevarden" typed "Aaboulevarden", "Sankt Pauls
   Kirkeplads" typed "Skt. Pauls Kirkeplads", "Aarhus H" (Aarhus); "Sdr.
   Boulevard" typed "Søndre Boulevard", "Store Gråbrødrestræde", "Odense
   Banegård" (Odense).

`place_search_review.py`'s `PLACE_WORD` needs the Danish place words too
(park, plads, torv, kirke, kirkegård, bro, sø, skov, have, anlæg, slot,
havn, strand, høj, museum), so `odd` stays readable.

## Files beside this one

`draft_da.json` (the final lists; `mk_draft.py` writes it), `final_dump/` (every row of the final
builds, `build_final.py`), `by_id_<city>.json` and `by_id_copenhagen_pending.json`,
`search-lang-da_draft.md` (this file before the rulings), `cand_da.json` and
`da_<city>_raw.txt` (the raw tables), `survey*.txt` (endings and first
words), `loose_<city>.txt` and `loose_table.py` (the loose words; measured
over the first draft, `draft_v1.json`, whose way words are the 43 core ones),
`wf/` (names not read, names read, per city), `final/` (the draft's builds,
before the rule batch), and the variant builds `keepstore/`,
`core/`, `nobare/`, `allot/` (built one draft earlier: three more leads,
-diget in, gadekæret in the bare list).
