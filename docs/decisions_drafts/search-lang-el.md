# Greek (el): settled lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py`. Nothing here is in shared code. Measured
2026-10-13 on Thessaloniki, the only city whose `PLACE_LANGUAGES` holds
`"el"`, built in memory with the lists patched for the process (place caches
of 2026-10-13, no network request), on `place_index.py` as it stands after
master's second rule batch was merged (commit 34d0fedd). One city, and a
small one: 185 minor ways, 589 named objects that are not ways. A second
Greek city is measured before it relies on any figure below.

## The owner's rulings (2026-10-13)

- **The genitive endings are in as `WAY_ENDING`** ("yes and test"): -ου,
  -ού, -ας, -άς, -ης, -ής, -ος, -ων, -ών, -ους, -ως. 30 street rows.
- **The single-letter endings are in** ("yes and test"): -η, -ή, -α, -ά. 8
  street rows.
- **The test the owner asked for** is in this folder and summarized below:
  38 of 38 admitted rows read as streets, no street among the names the
  endings do not admit, and the looseness measured at 78.1% of non-street
  names.
- **Home leads are in, and a house is kept on an article of its own:**
  οικία, κατοικία, βίλα, βίλλα, έπαυλη, αρχοντικό, σπίτι. 2 landmark rows
  go. Neither of the two mansions survives the current rule: both carry a
  Wikidata item and no `wikipedia` tag, and the article test reads the
  `wikipedia` tag only.
- **The other recommendations stand:** the four plain way words with no hit
  here are in (0 rows); δρόμος and άξονας are out; the bare type words take
  4 rows and σιντριβάνι is out; the leak list of 25 takes 1 street row;
  reading `int_name` and folding the final sigma are shared-code findings,
  not edits.

## The shape of Greek street names

Greek is not a way-word language and not a suffix language. A street is
named by a bare genitive with the word for street left unwritten: "Αγίας
Σοφίας", "Ερμού", "Ιωάννη Τσιμισκή". Of the 1,362 distinct names on larger
roads, 29 carry a way word, and none in the cache carries "Λεωφόρος". This
is Czech's case (`WAY_LEAD`, `WAY_ENDING`, batch 2a), not German's.

## The lists

`LANGUAGE_NAMES`, `SCRIPTS` and `_OWN_SCRIPTS` already hold Greek. `"el"`
does NOT go in `SUFFIX_WAY_LANGUAGES`.

`LEAK_WORDS["el"]` (25): ξενοδοχείο, ξενώνας, πάρκινγκ, στάθμευση,
στάθμευσης, γκαράζ, ιδιωτικός, ιδιωτική, ιδιωτικό, φαρμακείο, εστιατόριο,
ταβέρνα, κατάστημα, σούπερ μάρκετ, εμπορικό κέντρο, πρατήριο, βενζινάδικο,
πολυκατοικία, διαμερίσματα, α.ε., ε.π.ε., ο.ε., ι.κ.ε., επε, ικε.

`HOME_WORDS["el"]` (5): πολυκατοικία, διαμερίσματα, ιδιωτικός, ιδιωτική,
ιδιωτικό.

`WAY_WORDS["el"]` (9): οδός, λεωφόρος, πλατεία, πάροδος, στοά, μονοπάτι,
γέφυρα, σκάλες, πεζόδρομος.

`WAY_ENDING["el"]` (15, the ending of the name's last word): ου, ού, ας, άς,
ης, ής, ος, ων, ών, ους, ως, η, ή, α, ά. Accented and plain forms are both
listed because the test does not fold accents. No `WAY_LEAD`.

`HOME_NAME_LEAD["el"]` (7): οικία, κατοικία, βίλα, βίλλα, έπαυλη, αρχοντικό,
σπίτι.

`BARE_TYPE_NAMES["el"]` (20): εκκλησία, εκκλησάκι, παρεκκλήσι, ναός, ιερός
ναός, πάρκο, πάρκο τσέπης, παιδική χαρά, πλατεία, μνημείο, ηρώο, άγαλμα,
προτομή, γλυπτό, κρήνη, βρύση, νεκροταφείο, κοιμητήριο, εικονοστάσι,
βοηθητικό γήπεδο. Whoever folds the list adds the words to
`BARE_TYPE_NAMES` only; `_BARE_FOLDED` is built from it at import.

## What was measured

| City | Rows | Streets | Landmarks | Places | Stations | Streets dropped by a leak word | Minor ways not read as a way |
|---|---|---|---|---|---|---|---|
| Thessaloniki | 1,996 | 1,558 | 377 | 47 | 14 | 1 | 25 ways (10 names) |

Rebuilt on the merged `place_index.py`: no count moved. The only change in
the build report is a new line, `street_roundabout_kept` 1, which adds no
row. Greek is on 100% of names. The build reports English on 4.4%; its
denominator was not traced here.

- **Way words, street rows each adds on minor-only names:** πάροδος 2,
  πλατεία 1 (the 14 footways of Πλατεία Αριστοτέλους), στοά 1, μονοπάτι 1;
  οδός 0 (its names are on larger roads); λεωφόρος, γέφυρα, σκάλες,
  πεζόδρομος 0 (no name in the cache). One more row comes from an English
  alias ("Lisia street").
- **Endings, street rows each adds:** -ου 14, -ού 3, -ας 5, -ης 2, -ής 1,
  -ος 3, -ων 1, -ως 1; -η 4, -α 4. The forms -άς, -ών, -ους, -ή, -ά add none
  here and complete the set. With no endings the index would have 36 fewer
  street rows.
- **Leak words:** 1 street row dropped, "Πάρκινγκ δημαρχείου Θεσσαλονίκης"
  (way/200513672). Every other word hits no name in the cache. No index row
  carries a leak word, so check E asks for no review.
- **Home leads:** 2 landmark rows dropped, "Βίλα Χιρς" (way/223437584,
  wikidata Q29553154) and "Κατοικία Χιφζί Μπέη" (way/976182858, wikidata
  Q56194203), both `historic=building` on `building=yes`, neither with a
  `wikipedia` tag or a `tourism` tag. The other leads change no row: their
  houses are kept as attractions (Οικία Σάλεμ, Έπαυλη Μοδιάνο, Βίλλα
  Μορντώχ) or already dropped as `building=house`.
- **Bare type words that hit as a whole name:** εκκλησάκι (way/142042548),
  πλατεία (way/881577214), πάρκο τσέπης (way/693629509), βοηθητικό γήπεδο
  (relation/3290222): 4 landmark rows.

## The test of the endings

Files: `ending_rows.tsv`, `ending_negative.tsv`, `ending_misapplied.txt`,
written by `test_endings.py` with the verdicts in `verdicts.json`.

**(a) Every minor-way-only name the endings admit: 39 names, all read.** 38
have a street row and 38 are streets: genitives of ancient, mythical and
family names on the alleys, steps and footways of the upper town. One of
the 38 is marked for a second look and is no fault of the ending:
"Σελίτσης", seven service ways with no larger way. The 39th is "Πάρκινγκ
δημαρχείου Θεσσαλονίκης", admitted by -ης and then dropped by the leak word,
so it has no row. Misfires that reach the index: 0.

**(b) Every minor-way name the endings do NOT admit: 13 names.** 10 have
minor ways only and are dropped; none is a street (seven coded tracks, "Μ2",
"Δρόμος 01", and a park's footways under the park's name). 3 also sit on a
larger way, which keeps their row: "Αλβέρτου Ναρ" and "Άξονας Περιπάτου
Ερνέστου Εμπράρ" (foreign surnames with no Greek ending; one footway of
each is not drawn) and "Καπετάν" (a cut-off name on one path). No street
row is lost.

**(c) The endings misapplied.** The rule is only asked of a minor way's
names. Run against everything else in the cache:

| Names | Count | An ending matches | Two letters or more | Single letters |
|---|---|---|---|---|
| Named objects that are not ways | 589 | 460 (78.1%) | 311 (52.8%) | 149 (25.3%) |
| of them `place=*` | 80 | 63 (78.8%) | 27 | 36 |
| of them `leisure=*` | 75 | 65 (86.7%) | 54 | 11 |
| of them `historic=*` | 172 | 135 (78.5%) | 79 | 56 |
| of them `amenity=*` | 139 | 117 (84.2%) | 99 | 18 |
| Larger-road street names | 1,447 | 1,390 (96.1%) | 1,023 | 367 |
| Minor-way names | 112 | 99 (88.4%) | 85 | 14 |
| Names in Latin script only | 26 | 0 | 0 | 0 |
| Latin-script aliases (`name:en`, `int_name` and the like) | 2,248 | 0 | 0 | 0 |

So the endings are no test of a street at all: they match about four in five
Greek names of any kind. What they tell apart is a Greek name from a code, an
acronym or a foreign word. Tried alone, the type words "Είσοδος", "Έξοδος",
"Αυλή", "Παιδική Χαρά", "Στάθμευση", "Ράμπα" and "Αυλή Σχολείου" all pass;
"Πάρκινγκ", "Πάρκο", "Γήπεδο", "Σχολείο", "Γκαράζ" do not. The rule holds in
Thessaloniki because its named minor ways are streets (38) or codes (9), with
one description. The 3.9% of larger-road names that no ending matches (57,
foreign surnames mostly) is the share of real streets the rule would miss
on a minor way.

## The loose words and their future edit points

- **Every ending, the single letters most.** The edit point: when a Greek
  city's cache is refreshed, or a second Greek city is built, list the
  minor-way-only street rows read by an ending that are new since the last
  read (38 today, in `ending_rows.tsv`) and drop a description by id. A
  description is the expected misfire: a type word in the nominative
  ("Είσοδος") or an "X of Y" phrase ("Αυλή Σχολείου").
- **στοά.** 1 minor-only row, "Στοά Χρυσικοπούλου", a shopping arcade's
  passage. A new στοά row on a footway is read the same way.
- **Home leads.** A house that gains a `wikipedia` tag of its own comes back
  under the article rule; a `tourism` tag brings it back as an attraction.

## Left out, and why

- Way words: δρόμος (its one hit is the coded "Δρόμος 01"); άξονας (adds
  only a second row for a footway of a promenade that has a row); ανάχωμα,
  περιφερειακή, είσοδος, έξοδος (no row).
- Leak words, each for a measured hit: καφέ ("Κουλέ Καφέ" is a
  neighborhood); εταιρεία and εταιρείας (the street "Φιλικής Εταιρείας");
  αγορά ("Ρωμαϊκή Αγορά"); σχολή (university schools); μέγαρο (the concert
  hall); πρώην; "αε" without stops (a sports club's prefix, unmeasured);
  είσοδος (its one name is skipped as an area already).
- Home leads: μέγαρο and πύργος (the concert hall; towers of the city
  walls).
- Bare type words: σιντριβάνι and συντριβάνι (Sintrivani is a metro station
  and a square here); ωδείο (the Roman Odeon); μύλος, ροτόντα, πορτάρα,
  κέντρο (proper names in use).

## The id catches

`by_id_thessaloniki.json` holds no id: the rulings drop no row by id, and
the endings' one misfire is taken by the leak word. It lists three rows as
`pending`, for the eye read and the owner, with ids checked against their
cached names:

- "Σελίτσης" (seven service ways, way/19860786 and its group): a street or
  a yard's roads?
- "27ου Δημοτικού Σχολείου" (way/561834174, pedestrian): "of the 27th
  primary school", kept by its class whatever the lists say.
- "Κατάληψη Libertatia" (way/307657067, `historic=ruins`): a squat.

Also for the read, not for the lists: "Πλατεία Βασ. Ρομφέη (Κουλέ Καφέ)"
carries a second name in brackets; "Ζαΐμη" (alias "Ζαϊμη") and "Ζαίμη" are
separate rows, and eight more street pairs differ only by where the accent
sits; the Atatürk house museum ("Σπίτι του Κεμάλ Ατατούρκ") is out of the
index with or without the home leads.

## Shared-code findings (not edits)

1. **`norm()` does not fold the final sigma.** It leaves ς on 726 of the
   2,110 Greek names and aliases in the index. Three failures: a query in
   capitals that stops inside a word ("ΑΡΙΣ" lower-cases to "αρις", no prefix
   of "αριστοτελους"; 749 names hold a medial σ); the joined form the
   matcher adds ("αγιαςσοφιας") never meets a query typed without the space
   (282 names); an abbreviation ends in σ where a word would end in ς ("Βασ.
   Αδαμίδου", 3 names). One replacement of ς by σ in `norm()`, on both
   sides, answers all three and merges no two different names here.
2. **The index does not read `int_name`.** `_name_tags` reads `name`,
   `name:en`, `name:el`, `name:el-Latn` and the `alt_`, `official_`,
   `short_` and `old_name:en` tags. A Latin-script name or alias is on 262
   of 1,996 rows (13.1%): stations 14 of 14, landmarks 196 of 377, places 11
   of 47, streets 41 of 1,558 (2.6%). With `int_name` read: 880 rows
   (44.1%), streets 630 (40.4%). In the caches `name:en` is on 7.4% of named
   objects, `int_name` on 42.5%, either on 48.8%. `int_name` is a
   transliteration in more than one spelling ("Kharilaou" beside
   "Charilaou"), and 227 of its 1,900 values add a word the Greek name lacks
   ("Kosti Palama Street", "Odos Tenedou"). Reading it would also feed
   English way words to `_reads_as_way` on minor ways: measure that first.
3. **`_has_word` is accent-sensitive.** A leak or way word written in
   capitals without accents ("ΠΑΡΚΙΝΓΚ", "ΠΑΡΟΔΟΣ") would slip past the
   lists. No such name is in this cache. `bare_type` folds accents already.
4. **`build_dump.py` and `variant.py` cannot patch `WAY_ENDING`**, and
   `build_dump.py` breaks a TSV row on a multi-line tag value. The builds
   here used `lang_el/el_final.py`; the draft carries the endings under a
   new key, `way_ending`.
5. Accents and the diaeresis need nothing: `norm()` removes U+0300 to U+036F
   after decomposing, which covers the tonos (2,103 names) and the diaeresis
   (26). No polytonic letters are in the data.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map is rendered here. Words are as `norm()` leaves them today: no
accents, final ς kept. If the sigma fold lands, every ς below becomes σ.

```
el: {join: ["και"], stop: ["του", "της", "των", "το", "την", "τον"],
     street: ["οδος", "οδ", "λεωφορος", "λεωφ", "πλατεια", "πλ", "παροδος", "παρ", "στοα"],
     lead: ["οδος", "οδ", "λεωφορος", "λεωφ", "παροδος", "παρ"],
     station: ["σταθμος", "μετρο"],
     abbr: {}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. Greek names carry no street word, and a reader will still type "Οδός
   Τσιμισκή": the word has to be set aside as a lead word.
2. "και" as the join word splits a street named with it ("Καραολή και
   Δημητρίου"). Czech's "a" is the precedent to check against.
3. `abbr` is empty because the usual abbreviations are prefixes. The harder
   case runs the other way: the INDEX name is abbreviated ("Αγ. Πάντων",
   "Βασ. Αδαμίδου", 63 names) and the reader types the word in full.
4. If `int_name` is read, add "odos", "leoforos", "plateia" and "street" to
   `street`.

**Regression queries, with the first result expected** (from the index's
rows; none has met the search box): `regression_queries.tsv`, 17 queries.

`place_search_review.py`'s `PLACE_WORD` needs the Greek place words too
(πλατεία, πάρκο, ναός, ιερός ναός, μονή, παρεκκλήσιο, μουσείο, μνημείο,
άγαλμα, προτομή, ανδριάντας, κρήνη, θέατρο, πύργος, κήπος, στάδιο).

## Files (all under `lang_el/`)

`draft_el.json`; `final_dump/thessaloniki/` (rows and streets, line breaks
in tag values replaced); `by_id_thessaloniki.json`; `ending_rows.tsv`,
`ending_negative.tsv`, `ending_misapplied.txt`, `verdicts.json`;
`regression_queries.tsv`; the raw tables of the draft round
(`step1_thessaloniki.txt`, `minor_final.txt`, `diffs.txt`, `fold_check.txt`,
`intname.txt`). Eight in-memory builds went through the gate, one at a
time, each with a measured peak of 0.01 GB.
