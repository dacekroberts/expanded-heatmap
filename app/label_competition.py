"""The Global view's label competition (owner, 2026-10-01).

Global labels the whole world at one zoom, so its pills cannot all fit: Europe
piled up as a block of overlapping names. Hand-placing each city's offset
against every neighbour stopped scaling long ago. Instead the cities compete:

  1. A STATIC FILTER takes some out of the running: a tram city (orange on the
     legend) and a minor-tier city (`label_tier` in cities.py) never carry a
     Global label. Their dots and tooltips stay; each is labelled in its own
     region's view.
  2. The rest are RANKED, highest first, by RANK_ORDER: mode (metro > light
     rail > tram) first, then storefronts and coverage (full > narrowed > one
     category) in the order RANK_ORDER gives, then name. Mode outranks
     coverage on purpose: coverage measures this project's data, not the
     city, and a sum of the two put Rouen above Stockholm.
  3. In that order each city tries its own `label_offset`, then right, left,
     above and below its dot. The first position that overlaps no pill
     already placed, covers neither its own dot nor the dot of any city that
     has already won a label, and sits under none of the map's controls wins;
     a city with no such position goes unlabelled - and so does a city whose
     own dot already lies under a higher-ranked city's pill (Copenhagen's
     under Berlin's, 2026-10-01: its dot would have drawn over Berlin's name).

A LOWER-RANKED CITY'S DOT MAY SIT UNDER A PILL, because in Global the dots are
drawn ABOVE the pills (Overview.py): no dot is ever erased or unclickable, at
worst it sits on a pill's edge. At world zoom Europe is a few dozen pixels
across - a pill beside Paris reaches Prague - so a rule that kept every pill
off every dot left Paris, Berlin and Marseille unlabelled (measured
2026-10-01).

The competition covers the whole world, not the opening frame: the map pans,
and São Paulo or Sydney below the first screen must win their labels too.

Global's zoom is fixed, so two pills overlap by the same pixels at every
screen width: one competition serves phones and desktops alike, and a wider
screen simply shows more of the world. Deck.gl's own CollisionFilterExtension
was tried first (2026-10-01) and, in Streamlit's bundle, hides every text or
icon label while working only for plain shapes - so the competition runs here,
in Python, and scripts/check_macro_labels.py and check_deploy_imports.py score
exactly what it chose.

Pure Python, no dependencies: the app's lean venv and a clean clone import it.
"""
import math

# Measured in the browser at `600 14px "Space Grotesk", sans-serif`, the font
# app/components.set_base_font() loads and the TextLayer renders with. Re-measure
# when a city is added; a wrong width here makes every number downstream wrong.
TEXT_WIDTH = {
    "Boston": 48.4, "Calgary": 51.8, "Chicago": 55.0, "Edmonton": 69.0,
    "Barcelona": 67.9, "Dublin": 42.8, "Milan": 36.3, "Paris": 32.9,
    "Marseille": 60.3,
    # Toulouse measured 2026-09-23 the same way, and the run was validated by
    # re-measuring six cities already in this table - Barcelona 67.9, Boston
    # 48.4, Dublin 42.8, Marseille 60.3, Milan 36.3, Paris 32.9 - all six
    # reproduced exactly. So this is the same basis rather than a new one.
    "Toulouse": 60.4,
    # Lille (Regional) measured 2026-09-23, validated the same way: five
    # entries already here - Guadalajara (Regional) 152.7, Miami (Regional)
    # 112.6, Vancouver (Regional) 144.4, Toulouse 60.4, Marseille 60.3 -
    # reproduced exactly in the same run.
    "Lille (Regional)": 99.7,
    # Rennes measured 2026-09-23 in the deployed app's own frame (/~/+/),
    # validated the same way: six entries here - Toulouse 60.4, Paris 32.9,
    # Marseille 60.3, Milan 36.3, Lille (Regional) 99.7, Boston 48.4 -
    # reproduced exactly. ⚠ The OUTER page measured every one of them
    # differently (Toulouse 61.2, Paris 34.2) with the font reported loaded,
    # so measure in the app frame, never the top document.
    "Rennes": 49.7,
    # Oslo measured 2026-09-24 in the app frame the same way; six entries -
    # Rennes 49.7, Toulouse 60.4, Paris 32.9, Marseille 60.3, Milan 36.3,
    # Boston 48.4 - reproduced exactly in the same run.
    "Oslo": 29.0,
    # Copenhagen measured 2026-09-24 in the local app's own document (the
    # deployed app's /~/+/ frame; locally the app IS the top document), with
    # seven entries reproduced exactly in the same run - Oslo 29.0, Rennes
    # 49.7, Toulouse 60.4, Paris 32.9, Milan 36.3, Boston 48.4, Marseille
    # 60.3. The map's own st.iframe measured the outer-page values (Oslo 31.1,
    # Toulouse 61.2), so the frame warning above holds locally too.
    "Copenhagen": 85.5,
    # Prague measured 2026-09-24 in the local app's own document, the same
    # way, with eight entries reproduced exactly in the same run - Copenhagen
    # 85.5, Oslo 29.0, Rennes 49.7, Toulouse 60.4, Paris 32.9, Milan 36.3,
    # Boston 48.4, Marseille 60.3.
    "Prague": 47.3,
    # Amsterdam measured 2026-09-24 in the local app's own document, the same
    # way, with nine entries reproduced exactly in the same run - Prague 47.3,
    # Copenhagen 85.5, Oslo 29.0, Rennes 49.7, Toulouse 60.4, Paris 32.9,
    # Milan 36.3, Boston 48.4, Marseille 60.3.
    "Amsterdam": 76.5,
    # Rome measured 2026-09-24 in the local app's own document, the same way,
    # with nine entries reproduced exactly in the same run - Prague 47.3,
    # Copenhagen 85.5, Oslo 29.0, Rennes 49.7, Toulouse 60.4, Paris 32.9,
    # Milan 36.3, Boston 48.4, Marseille 60.3.
    "Rome": 37.5,
    # The nine Brazilian cities measured 2026-09-24 in the local app's own
    # document, the same way, with eleven entries reproduced exactly in the
    # same run - Rome 37.5, Amsterdam 76.5, Prague 47.3, Copenhagen 85.5, Oslo
    # 29.0, Rennes 49.7, Toulouse 60.4, Paris 32.9, Milan 36.3, Boston 48.4,
    # Marseille 60.3.
    "São Paulo": 65.6, "Rio de Janeiro": 95.6, "Belo Horizonte": 98.5,
    "Brasília": 49.0, "Salvador": 58.6, "Fortaleza (Regional)": 135.9,
    "Porto Alegre (Regional)": 156.6, "Recife (Regional)": 115.9,
    "Santos (Regional)": 120.1,
    # Rotterdam measured 2026-09-24 in the local app's own document, the same
    # way, with thirteen entries reproduced exactly in the same run - Amsterdam
    # 76.5, Rome 37.5, Prague 47.3, Copenhagen 85.5, Oslo 29.0, Rennes 49.7,
    # Toulouse 60.4, Paris 32.9, Milan 36.3, Boston 48.4, Marseille 60.3, São
    # Paulo 65.6, Santos (Regional) 120.1.
    "Rotterdam": 70.7,
    # Hong Kong measured 2026-09-24 in the deployed app's own frame (/~/+/),
    # as Rennes was, with five entries reproduced exactly in the same run -
    # Amsterdam 76.5, Copenhagen 85.5, Prague 47.3, Rome 37.5, Rotterdam 70.7.
    "Hong Kong": 73.5,
    # Riga measured 2026-09-24 in the deployed app's own frame, five entries
    # reproduced exactly in the same run - Amsterdam 76.5, Hong Kong 73.5,
    # Prague 47.3, Rome 37.5, Rotterdam 70.7.
    "Riga": 29.5,
    # Seoul measured 2026-09-25 in a local lean-venv app's own document (the app
    # frame when run locally), seven entries reproduced exactly in the same run
    # - Amsterdam 76.5, Copenhagen 85.5, Hong Kong 73.5, Prague 47.3, Riga 29.5,
    # Rome 37.5, Rotterdam 70.7.
    "Seoul": 37.5,
    # Taichung measured 2026-09-25 the same way, with ten entries reproduced
    # exactly in the same run (Seoul 37.5, Hong Kong 73.5, Riga 29.5, Amsterdam
    # 76.5, Rotterdam 70.7, Rome 37.5, Prague 47.3, Copenhagen 85.5).
    "Taichung": 61.7,
    # Taoyuan measured in the same run as Taichung (2026-09-25).
    "Taoyuan": 57.4,
    # Taipei (Regional) measured in the same run as Taichung (2026-09-25).
    "Taipei (Regional)": 112.5,
    # Daegu measured 2026-09-27 in the deployed app's own frame (/~/+/), seven
    # entries reproduced exactly in the same run - Seoul 37.5, Hong Kong 73.5,
    # Riga 29.5, Amsterdam 76.5, Rome 37.5, Prague 47.3, Taichung 61.7.
    "Daegu": 42.9,
    # Busan measured 2026-09-27 the same way, eight entries reproduced exactly
    # (Daegu 42.9 among them).
    "Busan": 41.9,
    # Monterrey (Regional) measured 2026-09-27 in the deployed app's own frame
    # (/~/+/), font reported loaded, with three entries reproduced exactly in
    # the same run (Guadalajara (Regional) 152.7, Los Angeles 80.8, Madrid 47.2).
    "Monterrey (Regional)": 144.0,
    # Kobe measured 2026-09-27 in the local app's own document (lean venv), font
    # reported loaded, with Busan 41.9 and Taichung 61.7 reproduced exactly.
    "Kobe": 34.2,
    # Osaka measured 2026-09-27 in the local app's own document (lean venv), font
    # reported loaded, with Kobe 34.2, Busan 41.9 and Taichung 61.7 reproduced
    # exactly in the same run.
    "Osaka": 40.6,
    # Sapporo measured 2026-09-28 in the local app's own document (lean venv),
    # font reported loaded, with Osaka 40.6 and Kobe 34.2 reproduced exactly in
    # the same run.
    "Sapporo": 56.9,
    # Fukuoka measured 2026-09-28 in the local app's own document (lean venv),
    # font reported loaded, with Sapporo 56.9, Osaka 40.6, Kobe 34.2 and Busan
    # 41.9 reproduced exactly in the same run.
    "Fukuoka": 56.8,
    # Kyoto measured 2026-09-28 the same way, with Fukuoka 56.8, Osaka 40.6 and
    # Kobe 34.2 reproduced exactly in the same run.
    "Kyoto": 40.2,
    # Tokyo measured 2026-09-28 the same way, with Kobe 34.2, Osaka 40.6 and
    # Kyoto 40.2 reproduced exactly in the same run.
    "Tokyo": 40.5,
    # Berlin measured 2026-09-28 in the local lean app's own document with
    # Space Grotesk loaded (document.fonts.check true); five entries reproduced
    # exactly in the same run - Prague 47.3, Tokyo 40.5, Marseille 60.3, Oslo
    # 29.0, Copenhagen 85.5.
    "Berlin": 38.8,
    # London measured 2026-09-28 in the local lean app's own document with
    # Space Grotesk loaded (document.fonts.check true); five entries reproduced
    # exactly in the same run - Prague 47.3, Tokyo 40.5, Marseille 60.3, Oslo
    # 29.0, Copenhagen 85.5.
    "London": 50.9,
    # Buenos Aires measured 2026-09-28 in the deployed app's own frame (/~/+/)
    # with Space Grotesk loaded (document.fonts.check true); seven entries
    # reproduced exactly in the same run - Prague 47.3, Tokyo 40.5, Marseille
    # 60.3, Oslo 29.0, Copenhagen 85.5, Berlin 38.8, London 50.9.
    "Buenos Aires": 87.4,
    # Glasgow: measured 2026-09-28 in the deployed app's own frame, canvas
    # measureText after document.fonts.load, Space Grotesk loaded; Prague 47.3,
    # Tokyo 40.5 and London 50.9 reproduced exactly in the same run.
    "Glasgow": 56.8,
    # Newcastle (Regional): measured 2026-09-28 in the deployed app's own frame,
    # canvas measureText after document.fonts.load, Space Grotesk loaded; Prague
    # 47.3, Tokyo 40.5, London 50.9 and Guadalajara (Regional) 152.7 reproduced.
    "Newcastle (Regional)": 143.1,
    # Sydney: measured 2026-09-28 in the deployed app's own frame, canvas
    # measureText after document.fonts.load, Space Grotesk loaded; Prague 47.3,
    # Tokyo 40.5 and London 50.9 reproduced exactly in the same run.
    "Sydney": 51.4,
    # Melbourne: measured in the same run as Sydney (2026-09-28, the deployed
    # app's own frame; Prague, Tokyo and London reproduced).
    "Melbourne": 72.4,
    # Bucharest: measured 2026-09-29 in the deployed app's own frame, canvas
    # measureText after document.fonts.load, Space Grotesk loaded; Prague 47.3,
    # Tokyo 40.5, London 50.9 and Glasgow 56.8 reproduced exactly in the same run.
    "Bucharest": 69.8,
    # Stockholm: measured 2026-09-29 in the deployed app's own frame, canvas
    # measureText after document.fonts.load, Space Grotesk loaded; Prague 47.3,
    # Tokyo 40.5, London 50.9 and Glasgow 56.8 reproduced exactly in the same run.
    "Stockholm": 72.1,
    # Incheon: measured 2026-09-29 in the deployed app's own frame, canvas
    # measureText after document.fonts.load, Space Grotesk loaded; Prague 47.3,
    # Tokyo 40.5, London 50.9 and Glasgow 56.8 reproduced exactly in the same run.
    "Incheon": 54.4,
    # Goyang, Seongnam, Yongin: measured in the same run as Incheon (2026-09-29,
    # the deployed app's own frame; Prague, Tokyo, London and Glasgow reproduced).
    "Goyang": 52.1, "Seongnam": 71.4, "Yongin": 45.9,
    # Suwon: measured 2026-09-29 in the local app's own document (lean venv),
    # canvas measureText after document.fonts.load, Space Grotesk loaded;
    # Prague, Tokyo, London, Glasgow, Incheon, Goyang and Yongin reproduced.
    "Suwon": 45.3,
    # Bucheon: measured 2026-09-29 in the local app's own document (lean venv),
    # canvas measureText after document.fonts.load, Space Grotesk loaded;
    # Prague, Tokyo, London, Glasgow, Incheon, Goyang and Yongin reproduced.
    "Bucheon": 60.1,
    # Namyangju: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load, with Prague 47.3, Tokyo
    # 40.5, Houston 56.9 and Toronto 52.4 reproduced exactly in the same run.
    "Namyangju": 75.8,
    # Ansan: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load, with Prague 47.3, Tokyo
    # 40.5, Houston 56.9 and Toronto 52.4 reproduced exactly in the same run.
    "Ansan": 41.5,
    # Uijeongbu: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load, with Prague 47.3, Tokyo
    # 40.5, Houston 56.9 and Toronto 52.4 reproduced exactly in the same run.
    "Uijeongbu": 68.6,
    # Anyang: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load, with Prague 47.3, Tokyo
    # 40.5, Houston 56.9 and Toronto 52.4 reproduced exactly in the same run.
    "Anyang": 51.6,
    # Bergen: measured 2026-09-29 in the local app's own document (lean venv),
    # canvas measureText after document.fonts.load, Space Grotesk loaded;
    # Prague, Tokyo, London, Glasgow and Oslo reproduced.
    "Bergen": 48.3,
    # Aarhus: measured 2026-09-29 in the local app's own document (lean venv),
    # canvas measureText at 600 14px "Space Grotesk" after document.fonts.load;
    # Prague 47.3, Tokyo 40.5, London 50.9, Glasgow 56.8 and Oslo 29.0
    # reproduced (the Suwon/Bucheon/Bergen session's run).
    "Aarhus": 46.9,
    # Odense: measured 2026-09-30 in a browser tab with Google Fonts' Space
    # Grotesk stylesheet loaded, canvas measureText at 600 14px "Space
    # Grotesk" after document.fonts.load; Aarhus 46.9, Prague 47.3, Oslo 29.0,
    # Riga 29.5, Bergen 48.3, Boston 48.4 and Chicago 55.0 reproduced (tram kit).
    "Odense": 50.6,
    # Liepāja: measured 2026-09-30 the same way as Odense, in the same tab
    # (Aarhus 46.9, Riga 29.5 and Odense 50.6 reproduced again; tram kit).
    "Liepāja": 48.2,
    # Daugavpils: measured 2026-09-30 in the same tab, the same way.
    "Daugavpils": 73.7,
    # Kansas City: measured 2026-09-30 the same way as Odense, in a fresh tab
    # (Houston 56.9, Odense 50.6, Daugavpils 73.7 and Riga 29.5 reproduced).
    "Kansas City": 79.3,
    # Tucson: measured in the same tab as Kansas City, the same way.
    "Tucson": 48.6,
    # New Orleans: measured in the same tab as Kansas City, the same way.
    "New Orleans": 82.8,
    # Florence: measured 2026-09-30 in a fresh tab, the same way (Houston 56.9,
    # Odense 50.6, Kansas City 79.3 and Daugavpils 73.7 reproduced).
    "Florence": 58.1,
    # Göteborg, Den Haag and Zurich: measured in the same tab as Florence, the
    # same way (2026-09-30, tram kit).
    "Göteborg": 63.6,
    "Den Haag": 63.8,
    "Zurich": 42.6,
    # Buffalo: measured 2026-09-29 in the local app's own document (lean venv),
    # canvas measureText at 600 14px "Space Grotesk" after document.fonts.load;
    # Prague 47.3, Tokyo 40.5, London 50.9, Glasgow 56.8 and Oslo 29.0
    # reproduced (the Suwon/Bucheon/Bergen session's run).
    "Buffalo": 48.8,
    # Sacramento: measured 2026-09-29 in the local app's own document (lean
    # venv), canvas measureText at 600 14px "Space Grotesk" after
    # document.fonts.load; Prague 47.3, Tokyo 40.5, London 50.9, Glasgow 56.8
    # and Oslo 29.0 reproduced (the Suwon/Bucheon/Bergen session's run).
    "Sacramento": 81.3,
    # Houston: measured 2026-09-29 in the local app's own document (lean venv),
    # canvas measureText at 600 14px "Space Grotesk" after document.fonts.load,
    # in the Suwon/Bucheon/Bergen session's run that measured Sacramento.
    "Houston": 56.9,
    # Ottawa: measured 2026-09-29 by canvas measureText at 600 14px "Space
    # Grotesk" after document.fonts.load, the font from Google Fonts as the app
    # loads it; Prague 47.3, Tokyo 40.5, Houston 56.9 and Toronto 52.4 reproduced
    # in the same run (the Band B build session).
    "Ottawa": 47.5,
    # Minneapolis: measured 2026-09-30 the same way (Space Grotesk from Google
    # Fonts, document.fonts.load, canvas measureText at 600 14px); Prague 47.3,
    # Tokyo 40.5, Houston 56.9 and Toronto 52.4 reproduced in the same run.
    "Minneapolis": 81.6,
    # Pittsburgh: measured 2026-09-30 by canvas measureText at 600 14px "Space
    # Grotesk" after document.fonts.load (Google Fonts, as the app loads it);
    # Prague 47.3, Tokyo 40.5, Houston 56.9 and Toronto 52.4 reproduced.
    "Pittsburgh": 70.7,
    # Kitchener–Waterloo (Regional): measured 2026-09-30 in a browser with Space
    # Grotesk 600 14px loaded, Prague 47.3, Tokyo 40.5, Houston 56.9 and Toronto
    # 52.4 reproduced.
    "Kitchener–Waterloo (Regional)": 207.2,
    # Palma: measured 2026-09-30 in a browser with Space Grotesk 600 14px
    # loaded, Prague 47.3, Tokyo 40.5, Houston 56.9 and Toronto 52.4 reproduced.
    "Palma": 40.1,
    # Yokohama: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load, with Prague 47.3, Tokyo
    # 40.5, Houston 56.9 and Toronto 52.4 reproduced exactly in the same run.
    "Yokohama": 68.8,
    # Hiroshima: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load, with Prague 47.3, Tokyo
    # 40.5, Houston 56.9 and Toronto 52.4 reproduced exactly in the same run.
    "Hiroshima": 66.3,
    # Dallas: measured 2026-09-30 (Band B session), canvas measureText at 600
    # 14px "Space Grotesk" after document.fonts.load (document.fonts.check
    # true), with Prague 47.3, Tokyo 40.5, Houston 56.9, Toronto 52.4 and
    # Yokohama 68.8 reproduced exactly in the same run.
    "Dallas": 40.1,
    "Guadalajara (Regional)": 152.7, "Los Angeles": 80.8, "Madrid": 47.2,
    "Mexico City": 80.0,
    "Miami (Regional)": 112.6, "Montréal": 60.8, "New York": 61.4,
    "Philadelphia": 82.3, "San Diego": 67.4, "San Francisco": 94.3,
    "Toronto": 52.4, "Vancouver (Regional)": 144.4, "Washington D.C.": 110.3,
    # The French tram batch: measured 2026-09-30 by the cleanup session in
    # the app's own document with the font loaded (controls Paris 32.9,
    # Marseille 60.3 and Lille 99.7 reproduced exactly).
    "Le Mans": 55.6,
    "Besançon": 66.8,
    "Tours": 36.7,
    "Dijon": 33.8,
    "Reims": 40.0,
    "Orléans": 50.7,
    "Mulhouse": 65.8,
    "Brest": 36.2,
    "Avignon": 54.7,
    "Saint-Étienne": 92.2,
    "Nice": 29.4,
    "Strasbourg": 75.9,
    "Le Havre": 57.2,
    "Caen": 33.7,
    "Rouen (Regional)": 115.8,
    "Nantes (Regional)": 120.5,
    "Valenciennes (Regional)": 162.4,
    "Montpellier": 77.3,
    "Bordeaux (Regional)": 137.9,
    "Grenoble (Regional)": 133.5,
    # Angers: measured 2026-09-30 by the France build session, canvas
    # measureText at 600 14px "Space Grotesk" after the Google Fonts faces
    # loaded; Paris 32.9, Marseille 60.3, Lille (Regional) 99.7, Le Havre 57.2
    # and Saint-Étienne 92.2 reproduced exactly.
    "Angers": 47.2,
    # The six Czech tram cities: measured 2026-09-30 in the local app's own
    # document (lean venv, czech-build), canvas measureText at 600 14px "Space
    # Grotesk" after document.fonts.load, with eight entries reproduced exactly
    # in the same run - Prague 47.3, Copenhagen 85.5, Oslo 29.0, Rennes 49.7,
    # Toulouse 60.4, Paris 32.9, Lille (Regional) 99.7, Milan 36.3.
    "Brno": 31.9, "Plzeň": 36.0, "Olomouc": 59.1, "Ostrava": 51.6,
    "Liberec (Regional)": 122.9, "Most (Regional)": 107.5,
}

PILL_H = 18.0             # measured from rendered pixels, 14 px text
PILL_PAD_X = 5            # background_padding=[5, 2]
MARKER_R = 6.0            # Overview.DOT_PX / 2
TOUCH = 1.0               # abutting pills are not a collision
CANVAS = {375: 343, 768: 726, 1200: 1030}   # viewport -> deck canvas width
CANVAS_H = 460
FALLBACK_CHAR_W = 8.0     # the app's guess for a name not yet measured

MODE_RANK = {"metro": 3, "light_rail": 2, "tram": 1}
COVERAGE_RANK = {"full": 3, "narrowed": 2, "one_bucket": 1}
STATIC_OUT_MODES = ("tram",)
# Right, left, above, below - tried after the city's own offset.
CANDIDATES = (("start", 11, 0), ("end", -11, 0), ("middle", 0, -22), ("middle", 0, 22))


def project(lat, lon, centre_lat, centre_lon, zoom, w, h):
    """Web-Mercator pixel position on a w x h canvas centred on the view."""
    scale = 512 * 2 ** zoom
    x = w / 2 + ((lon + 180) / 360 - (centre_lon + 180) / 360) * scale

    def merc(d):
        s = math.sin(math.radians(d))
        return 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)
    return x, h / 2 + (merc(lat) - merc(centre_lat)) * scale


def text_width(name, strict=False):
    if name in TEXT_WIDTH:
        return TEXT_WIDTH[name]
    if strict:
        raise KeyError(name)
    return FALLBACK_CHAR_W * len(name)


def pill_box(name, x, y, offset, strict=False):
    """(x0, y0, x1, y1) of a name's pill at offset (anchor, dx, dy)."""
    anchor, dx, dy = offset
    w = text_width(name, strict)
    a = x + dx
    left = a if anchor == "start" else a - w if anchor == "end" else a - w / 2
    return (left - PILL_PAD_X, y + dy - PILL_H / 2, left + w + PILL_PAD_X, y + dy + PILL_H / 2)


def controls(cw):
    """The map's own controls on a cw-wide canvas, which hide what is under them."""
    credit = ((cw - 10 - 244.1, CANVAS_H - 30, cw - 10, CANVAS_H - 10) if cw < 640
              else (cw - 244.1, CANVAS_H - 20, cw, CANVAS_H))
    return [("theme button", (cw - 163.0, 10.0, cw - 52.0, 42.0)),
            ("zoom buttons", (cw - 42.0, 12.0, cw - 13.2, 69.6)),
            ("map credit", credit)]


def _overlaps(a, b, tol=TOUCH):
    return min(a[2], b[2]) - max(a[0], b[0]) > tol and min(a[3], b[3]) - max(a[1], b[1]) > tol


def eligible(city):
    return city.get("mode") not in STATIC_OUT_MODES and city.get("label_tier") != "minor"


# The tie-breaks after mode, in order. ("coverage", "storefronts") is the
# owner's first proposal; ("storefronts", "coverage") labels London, Berlin and
# Osaka in Global where it loses Lille (measured 2026-10-01).
RANK_ORDER = ("storefronts", "coverage")


def rank_key(city, storefronts):
    keys = {"coverage": -COVERAGE_RANK.get(city.get("coverage"), 0),
            "storefronts": -(storefronts.get(city["name"]) or 0)}
    return (-MODE_RANK.get(city.get("mode"), 0), *(keys[k] for k in RANK_ORDER), city["name"])


def compete(cities, centre_lat, centre_lon, zoom, storefronts, strict=False):
    """{name: (anchor, dx, dy)} for the cities that win a Global label.

    `cities` is every city drawn (all dots count as obstacles); `storefronts`
    is macro_facts.json's map. Positions are scored on the widest canvas and
    checked against the controls at every width where the dot is on screen."""
    pos = {}
    for c in cities:
        pos[c["name"]] = {w: project(c["lat"], c["lon"], centre_lat, centre_lon, zoom, w, CANVAS_H)
                          for w in CANVAS.values()}
    ref = max(CANVAS.values())
    placed, won, won_dots = [], {}, []
    for c in sorted((c for c in cities if eligible(c)), key=lambda c: rank_key(c, storefronts)):
        cx0, cy0 = pos[c["name"]][ref]
        if any(p[0] < cx0 < p[2] and p[1] < cy0 < p[3] for p in placed):
            continue
        own = ((c.get("label_offset_by_region") or {}).get("Global") or c.get("label_offset"))
        tries = ([tuple(own)] if own else []) + [o for o in CANDIDATES if o != (tuple(own) if own else None)]
        for off in tries:
            x, y = pos[c["name"]][ref]
            box = pill_box(c["name"], x, y, off, strict)
            if any(_overlaps(box, p) for p in placed):
                continue
            if any(box[0] < dx < box[2] and box[1] < dy < box[3] for dx, dy in won_dots + [(x, y)]):
                continue
            under = False
            for w in CANVAS.values():
                cx, cy = pos[c["name"]][w]
                b = pill_box(c["name"], cx, cy, off, strict)
                # Any part of the pill on screen counts, not just the dot: a
                # pill can reach the canvas from a dot below it (Santos under
                # the map credit, 2026-10-01).
                if b[2] < 0 or b[0] > w or b[3] < 0 or b[1] > CANVAS_H:
                    continue
                if any(_overlaps(b, cb) for _, cb in controls(w)):
                    under = True
                    break
            if under:
                continue
            placed.append(box)
            won_dots.append((x, y))
            won[c["name"]] = off
            break
    return won
