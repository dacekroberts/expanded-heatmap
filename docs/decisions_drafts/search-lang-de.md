# German (de): draft lists for place search

For Cleanup to fold into `pipeline/place_index.py` and
`pipeline/map_common.py` after `search-rules-2` lands (Cleanup, 2026-10-13).
Nothing here is in shared code on `search-final`. Measured 2026-10-13 on the
four German-language cities, each built in memory with the lists patched for
the process (extract caches of 2026-10-12T20:21:35Z): Gelsenkirchen, Bremen,
Berlin, Zurich. These are every city of the language on the map today; a
fifth city is measured before it relies on them.

## What the owner ruled (2026-10-13)

- German is the first new language, Gelsenkirchen its first city.
- Field-name endings: "1 yes, note the future edit point". In: -kamp,
  -winkel, -acker, -hof (and -höfe). Out: -garten, -wiese, -heide.
- "AG" and "KG" are not leak words ("2 yes").
- Swiss German way words for Zurich ("3 sounds good"): -wegli, -rain,
  -halde, -quai, -viadukt.
- Low German endings ("agree with your recommendations and berlin
  measurement", later the same day). In: -deich, -pad, -pforte. Out: -gang,
  -moor (measured on Berlin after the ruling, below).
- -eck in after the Berlin measurement ("add, note the id catch").
  **The id catch (owner):** -eck also ends a corner cafe or a building
  by its name. None is in an index today. One that appears on a
  footway after a cache refresh is dropped by id, found the same way as
  -hof below: list the minor-way street rows ending -eck that are new
  since the last read.

**The future edit point (owner):** -hof also ends a shopping passage, a
schoolyard and a works yard. Three such rows exist today and are dropped by
id (below). A later OSM edit can add another, and only a read finds it: when
a German city's cache is refreshed, list its minor-way street rows ending
-hof that are new since the last read.

## The lists

`LANGUAGE_NAMES` already holds `"de": "German"`.

`LEAK_WORDS["de"]` (28): hotel, gasthof, gasthaus, pension, parkplatz,
parkhaus, tiefgarage, privat, privatweg, privatstraße, privatgrundstück,
laden, geschäft, restaurant, gaststätte, wohnanlage, wohnpark, wohnhaus,
mehrfamilienhaus, apotheke, gmbh, ohg, supermarkt, einkaufszentrum, zufahrt,
seniorenresidenz, autohaus, tankstelle.

`HOME_WORDS["de"]` (9): wohnanlage, wohnpark, wohnhaus, mehrfamilienhaus,
privat, privatweg, privatstraße, privatgrundstück, seniorenresidenz.

`WAY_WORDS["de"]` (40), with `"de"` in `SUFFIX_WAY_LANGUAGES`: straße,
strasse, str, weg, gasse, allee, platz, ring, damm, ufer, brücke, steg, pfad,
stieg, steig, treppe, promenade, chaussee, markt, wall, graben, passage,
tunnel, unterführung, durchgang, trasse, kamp, winkel, acker, hof, höfe,
wegli, rain, halde, quai, viadukt, deich, pad, pforte, eck.

`WAY_LEAD["de"]` (12, the name's first word): am, an, auf, im, in, zum, zur,
hinter, unter, vor, bei, beim. No `WAY_ENDING`.

`HOME_NAME_LEAD["de"]` (3): wohnhaus, villa, landhaus. NOT "haus": in
Westphalia it names a manor (Haus Darl, Haus Leithe), and a "-haus" ending
is a town hall or a hospital.

`BARE_TYPE_NAMES["de"]` (22): kirche, kapelle, park, spielplatz, denkmal,
brunnen, friedhof, mahnmal, wegekreuz, wegkreuz, bolzplatz, sportplatz,
grünanlage, ehrenmal, gedenkstein, kriegerdenkmal, gedenktafel, skulptur,
pfarrhaus, gedenkkreuz, trauerhalle, evangelisches gemeindehaus.
NOT "marktplatz" (a square's real name) and NOT "ohne titel" (a title is
not a type; the three rows so named carry a Wikidata entry).

## What was measured

| City | Rows | Streets | Landmarks | Places | Stations | Streets dropped by a leak word | Minor-way names not read as a way |
|---|---|---|---|---|---|---|---|
| Berlin | 18,561 | 13,185 | 3,890 | 740 | 744 | 57 | 617 |
| Bremen | 5,686 | 4,807 | 527 | 168 | 184 | 13 | 423 |
| Zurich | 3,365 | 2,470 | 563 | 106 | 218 | 3 | 109 |
| Gelsenkirchen | 1,848 | 1,564 | 165 | 50 | 69 | 0 | 104 |

German is on 100% of names in all four and English on 0.5% or less, so each
page names German only. Every map station has an indexed place within 1 km.

- **Way words.** On Gelsenkirchen's 458 distinct minor-way names, the first
  26 words and the 12 leads read 366 as a way. Most names not read as a way
  in every city are tram and bus platforms, which are no streets.
- **Field-name endings, street rows added over the four cities:** -kamp 18
  (Bremen 17, Gelsenkirchen 1), -winkel 9 (Berlin 6, Bremen 2, Gelsenkirchen
  1), -acker 1, -hof and -höfe 26 (Bremen 11, Gelsenkirchen 9, Berlin 5,
  Zurich 1). Left out: -garten 6 rows, 2 of them an allotment colony's path
  and a maze; -wiese 3; -heide 2, one a waterworks. No station or cemetery
  came in under -hof: those names sit on platforms. -delle, -bruch and
  -busch added no row and are not in the list.
- **The three -hof misfires, dropped by id in their cities' configs:**
  Bremen "Lloydhof" (8 footways of a shopping passage, way/28262455 and its
  group), Bremen "Alter Schulhof" (way/23422198, way/23422199), Berlin
  "Zuwegung Wirtschaftshof" (way/698687608, access=delivery).
- **Swiss words:** they add one street row in Zurich (Blockhauswegli); the
  other names they read already had a row from a larger way, so the words
  lengthen drawn lines. A dozen rows was the estimate given to the owner
  before the build; one is the measurement.
- **Leak words.** Berlin's 57 dropped streets: 42 ways named "Privatstraße"
  or "Privatstraße N", 7 "Privatweg" names, 10 "Zufahrt" ways, the rest
  "Am Parkplatz" and a platform. Bremen's 13: motorway approach ramps named
  "Zufahrt" and one service road. "ag" as a whole word dropped
  AG-Weser-Straße (Bremen, tertiary), which is why it is out; "kg" went with
  it, unmeasured. Not leak words, measured: siedlung (145 Berlin names,
  neighborhoods), betriebshof (tram stops), residenz, werkstatt, "e.V." (41
  places of worship and arts centres).
- **To review by name once built:** "Theodor-Fontane-Apotheke im Bethanien"
  (Berlin, tourism=museum).
- **Bare type words that hit as a whole name:** Kapelle 9, Kriegerdenkmal 6,
  Skulptur 3, Gedenkstein 2, Denkmal 2, Mahnmal 2, Ehrenmal 1, Pfarrhaus 1,
  and Gelsenkirchen's Gedenkkreuz, Trauerhalle and Evangelisches
  Gemeindehaus, one each.

## After the reads (2026-10-13, later the same day)

**A correction to the table above.** The first in-memory builds patched
`BARE_TYPE_NAMES` and not `_BARE_FOLDED`, the table `bare_type()` reads for a
Latin-script language, so the German bare type words were not applied: the
readers found "Kapelle" still in. With both patched, and every by-id drop in
the four configs applied, the indexes are: Berlin 18,461 rows (13,158
streets, 3,830 landmarks, 733 places, 738 stations), Bremen 5,648 (4,789,
510, 165, 184), Zurich 3,331 (2,465, 534, 106, 218), Gelsenkirchen 1,843
(1,562, 162, 50, 69). The bare list took 12 rows in Berlin, 2 in Bremen, 2
in Zurich and 3 in Gelsenkirchen. Whoever folds the lists adds the words to
`BARE_TYPE_NAMES` only; `_BARE_FOLDED` is built from it at import.

**Way words, misfires per word on minor-way-only rows** (the Sonnet street
screens; Berlin 1,870 such rows, Bremen 1,025, Zurich 747, Gelsenkirchen
125). No word misfires often enough to leave the list; the rows go by id.
Zero misfires: damm, winkel, wall, stieg, steg (one under construction),
acker, gasse, kamp (Bremen's four "Turmkamp I" to "IV" are a numbered
series, not a misfire of the word), ufer, allee (two glued names), markt,
chaussee, trasse. tunnel: 8 of 11 in Berlin (station corridors), 2 in
Zurich, 1 in Bremen. passage: Berlin 5 of 11, Bremen 2 to 5 (arcades).
treppe: Berlin 5. pfad: Zurich 4, Bremen 5 (trail names; the owner has not
ruled on trails). hof: Berlin 7, Bremen 8, Zurich 1 clear, Gelsenkirchen 10
undecidable from tags. The leading prepositions are the loosest group:
about 14 misfires in Bremen's 69 and 15 in Berlin ("Am Reitstall", "Zum
Spielplatz"), against about 80 real names in Berlin alone.

**Low German endings, ruled by the owner (in: -deich, -pad, -pforte; out:
-gang, -moor; -eck in after Berlin).** Street rows each adds in Bremen, none in
Gelsenkirchen or Zurich: -deich 12, -pad 7 (one of them private), -pforte
2, -eck 3; left out: -gang 10 (three are not streets: Bahnhofsgang, Laubengang,
Wasserwerksgang), -moor 2, -diek 1 (and 1 in Gelsenkirchen), the
leads "achter" 2 and "hinterm" 1. Berlin, measured after the ruling as
distinct street names: -deich, -pad, -pforte, -moor, -diek and both leads
add none; -gang adds 19, of which 13 are no street name (Eingang zur ANB,
four "Zugang ..." descriptions, Hochbahnübergang, Übergang S1/S2 zur U6,
Wandelgang and the coded "Gang 1" to "Gang 5")
and 6 are (Eosgang, Judengang, Liebstadter Gang, Lunagang, Rosengang,
Tulpengang), so -gang stays out; -eck adds 3 (Lilieneck, Poseidoneck,
Siedlers Eck), all lane names by their look, and the owner
added -eck on that (6 street rows over Berlin and Bremen).
With the three endings in and the drops of the second round applied, the
indexes are Berlin 18,268 rows (12,985 streets, 3,810 landmarks, 733
places, 738 stations) and Bremen 5,645 before the endings' 21 street rows.

**Bare type words the reads found, NOT yet ruled** (whole names still in an
index): friedhofskapelle (Berlin 9, Bremen 2), dachgarten (Zurich 2),
rodelberg (Berlin 3, Bremen 1), badestrand (Berlin 2), fkk-strand (Berlin 1,
Bremen 1), hundestrand, tennisstadion, sporthalle, vereinsplatz, hügelgrab,
kirchgemeindehaus, atrium, hartplatz, one each. Kept out on purpose: rathaus,
bürgerpark, stadtwald, rosengarten, dorfkirche (proper names in use), and
every artwork title that is a common noun.

**Home words:** "villa" and "landhaus" lead four Berlin names the rule
missed because three are tagged a park or garden, where the home-name lead
is not read. "mietshaus" and "reihenhäuser" hit one row each. "haus" (67
Berlin hits, nearly all museums and theatres) and "heim" stay out.

## Matcher words (`map_common.LANG_WORDS`), drafted and NOT tested

No map is rendered on this branch, so none of this has met the search box.

```
de: {join: ["und", "ecke"], stop: ["der", "die", "das", "den", "dem"],
     street: ["strasse", "str", "weg", "allee", "platz", "gasse", "ring", "damm", "ufer",
              "chaussee"],
     lead: [], station: ["bahnhof", "bf", "bhf", "hbf", "haltestelle"],
     abbr: {"str": "strasse", "pl": "platz", "bf": "bahnhof", "bhf": "bahnhof",
            "hbf": "hauptbahnhof", "st": "sankt"}}
```

Open for whoever folds it, each to test in the browser before it lands:

1. Does `norm()` fold ß to "ss"? "Straße" and "Strasse" must meet, and
   Zurich writes only "strasse".
2. German writes the street word inside the name ("Hauptstraße"), and the
   usual abbreviation is a suffix ("Hauptstr."). `abbr` matches whole words,
   so "Hauptstr" needs a suffix form or a prefix match on the last word.
3. "ae", "oe", "ue" typed for ä, ö, ü.
4. Regression queries to add: "Kurfürstendamm", "Unter den Linden", "Karl-Marx-Allee
   und Straße der Pariser Kommune" (Berlin); "Bahnhofstrasse" (Zurich);
   "Am Wall" (Bremen); "Kurt-Schumacher-Straße" typed "Kurt-Schumacher-Str."
   (Gelsenkirchen).

`place_search_review.py`'s `PLACE_WORD` needs the German place words too
(park, platz, kirche, friedhof, brücke, see, wald, garten, denkmal, museum),
so `odd` stays readable.
