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

`WAY_WORDS["de"]` (36), with `"de"` in `SUFFIX_WAY_LANGUAGES`: straße,
strasse, str, weg, gasse, allee, platz, ring, damm, ufer, brücke, steg, pfad,
stieg, steig, treppe, promenade, chaussee, markt, wall, graben, passage,
tunnel, unterführung, durchgang, trasse, kamp, winkel, acker, hof, höfe,
wegli, rain, halde, quai, viadukt.

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
