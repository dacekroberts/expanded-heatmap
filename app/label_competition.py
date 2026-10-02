"""The Global view's label competition (owner, 2026-10-01).

Global labels the whole world at one zoom, so its pills cannot all fit (Europe
became a block of overlapping names), and hand-placing each city's offset
against every neighbor does not scale. Instead the cities compete:

  1. A STATIC FILTER takes some out of the running: a tram city (orange on the
     legend) and a minor-tier city (`label_tier` in cities.py) never carry a
     Global label. Their dots and tooltips stay; each is labeled in its own
     region's view.
  2. The rest are RANKED, highest first, by RANK_ORDER: mode (metro > light
     rail > tram) first, then storefronts and coverage (full > narrowed > one
     category) in the order RANK_ORDER gives, then name. Mode outranks
     coverage on purpose: coverage measures this project's data, not the
     city, and a sum of the two put Rouen above Stockholm.
  3. In that order each city tries its own `label_offset`, then right, left,
     above and below its dot. The first position that overlaps no pill
     already placed, covers neither its own dot nor the dot of any city that
     has already won a label, and sits under none of the map's controls wins.
     A city with no such position goes unlabeled, and so does a city whose
     own dot already lies under a higher-ranked city's pill (Copenhagen's
     under Berlin's, 2026-10-01: its dot would have drawn over Berlin's name).

A LOWER-RANKED CITY'S DOT MAY SIT UNDER A PILL, because in Global the dots are
drawn ABOVE the pills (Overview.py): no dot is ever erased or unclickable; at
worst it sits on a pill's edge. At world zoom Europe is a few dozen pixels
across (a pill beside Paris reaches Prague), so keeping every pill off every
dot left Paris, Berlin and Marseille unlabeled (measured 2026-10-01).

The competition covers the whole world, not the opening frame: the map pans,
and São Paulo or Sydney below the first screen must win their labels too.

Global's zoom is fixed, so two pills overlap by the same pixels at every
screen width: one competition serves phones and desktops alike, and a wider
screen shows more of the world. Deck.gl's own CollisionFilterExtension does
not serve: in Streamlit's bundle it hides every text or icon label and works
only for plain shapes (2026-10-01). So the competition runs here, in Python,
and scripts/check_macro_labels.py and check_deploy_imports.py score exactly
what it chose.

Pure Python, no dependencies: the app's lean venv and a clean clone import it.
"""
import math

# Measured in the browser at `600 14px "Space Grotesk", sans-serif`, the font
# app/components.set_base_font() loads and the TextLayer renders with. Re-measure
# when a city is added; a wrong width here makes every number downstream wrong.
#
# A dated entry records how it was checked: where it was measured ("deployed
# frame" is the deployed app's /~/+/ frame, "local app" the top document of a
# locally run app) and the entries already here that the same run re-measured
# as controls, which reproduced their values. Later runs used canvas
# measureText after document.fonts.load. ⚠ The deployed app's OUTER page and
# the map's own st.iframe measured differently with the font reported loaded
# (Toulouse 61.2, Paris 34.2, Oslo 31.1): measure in the app frame, never the
# top document of the deployed page.
TEXT_WIDTH = {
    "Boston": 48.4, "Calgary": 51.8, "Chicago": 55.0, "Edmonton": 69.0,
    "Barcelona": 67.9, "Dublin": 42.8, "Milan": 36.3, "Paris": 32.9,
    "Marseille": 60.3,
    # Toulouse, 2026-09-23; controls Barcelona, Boston, Dublin, Marseille,
    # Milan, Paris (the same basis as the entries above).
    "Toulouse": 60.4,
    # Lille (Regional), 2026-09-23; controls Guadalajara (Regional), Miami
    # (Regional), Vancouver (Regional), Toulouse, Marseille.
    "Lille (Regional)": 99.7,
    # Rennes, 2026-09-23, deployed frame; controls Toulouse, Paris, Marseille,
    # Milan, Lille (Regional), Boston.
    "Rennes": 49.7,
    # Oslo, 2026-09-24, app frame; controls Rennes, Toulouse, Paris, Marseille,
    # Milan, Boston.
    "Oslo": 29.0,
    # Copenhagen, 2026-09-24, local app; controls Oslo, Rennes, Toulouse,
    # Paris, Milan, Boston, Marseille.
    "Copenhagen": 85.5,
    # Prague, 2026-09-24, local app; controls Copenhagen, Oslo, Rennes,
    # Toulouse, Paris, Milan, Boston, Marseille.
    "Prague": 47.3,
    # Amsterdam, 2026-09-24, local app; controls Prague and the eight Prague's
    # run used.
    "Amsterdam": 76.5,
    # Rome, 2026-09-24, local app; the same nine controls as Amsterdam.
    "Rome": 37.5,
    # The nine Brazilian cities, 2026-09-24, local app; controls Rome,
    # Amsterdam and Rome's nine.
    "São Paulo": 65.6, "Rio de Janeiro": 95.6, "Belo Horizonte": 98.5,
    "Brasília": 49.0, "Salvador": 58.6, "Fortaleza (Regional)": 135.9,
    "Porto Alegre (Regional)": 156.6, "Recife (Regional)": 115.9,
    "Santos (Regional)": 120.1,
    # Rotterdam, 2026-09-24, local app; thirteen controls: the Brazilian run's
    # eleven plus São Paulo and Santos (Regional).
    "Rotterdam": 70.7,
    # Hong Kong, 2026-09-24, deployed frame; controls Amsterdam, Copenhagen,
    # Prague, Rome, Rotterdam.
    "Hong Kong": 73.5,
    # Riga, 2026-09-24, deployed frame; controls Amsterdam, Hong Kong, Prague,
    # Rome, Rotterdam.
    "Riga": 29.5,
    # Seoul, 2026-09-25, local app (lean venv); controls Amsterdam, Copenhagen,
    # Hong Kong, Prague, Riga, Rome, Rotterdam.
    "Seoul": 37.5,
    # Taichung, 2026-09-25, the same way; ten controls, among them Seoul, Hong
    # Kong, Riga, Amsterdam, Rotterdam, Rome, Prague, Copenhagen.
    "Taichung": 61.7,
    # Taoyuan and Taipei (Regional): the same run as Taichung.
    "Taoyuan": 57.4,
    "Taipei (Regional)": 112.5,
    # Daegu, 2026-09-27, deployed frame; controls Seoul, Hong Kong, Riga,
    # Amsterdam, Rome, Prague, Taichung.
    "Daegu": 42.9,
    # Busan, 2026-09-27, the same way; eight controls, Daegu among them.
    "Busan": 41.9,
    # Monterrey (Regional), 2026-09-27, deployed frame; controls Guadalajara
    # (Regional), Los Angeles, Madrid.
    "Monterrey (Regional)": 144.0,
    # Kobe, 2026-09-27, local app (lean venv); controls Busan, Taichung.
    "Kobe": 34.2,
    # Osaka, 2026-09-27, local app; controls Kobe, Busan, Taichung.
    "Osaka": 40.6,
    # Sapporo, 2026-09-28, local app; controls Osaka, Kobe.
    "Sapporo": 56.9,
    # Fukuoka, 2026-09-28, local app; controls Sapporo, Osaka, Kobe, Busan.
    "Fukuoka": 56.8,
    # Kyoto, 2026-09-28, local app; controls Fukuoka, Osaka, Kobe.
    "Kyoto": 40.2,
    # Tokyo, 2026-09-28, local app; controls Kobe, Osaka, Kyoto.
    "Tokyo": 40.5,
    # Berlin, 2026-09-28, local app (document.fonts.check true); controls
    # Prague, Tokyo, Marseille, Oslo, Copenhagen.
    "Berlin": 38.8,
    # London, 2026-09-28, the same run and controls as Berlin.
    "London": 50.9,
    # Buenos Aires, 2026-09-28, deployed frame; controls Prague, Tokyo,
    # Marseille, Oslo, Copenhagen, Berlin, London.
    "Buenos Aires": 87.4,
    # Glasgow, 2026-09-28, deployed frame; controls Prague, Tokyo, London.
    "Glasgow": 56.8,
    # Newcastle (Regional), 2026-09-28, deployed frame; controls Prague, Tokyo,
    # London, Guadalajara (Regional).
    "Newcastle (Regional)": 143.1,
    # Sydney, 2026-09-28, deployed frame; controls Prague, Tokyo, London.
    "Sydney": 51.4,
    # Melbourne: the same run as Sydney.
    "Melbourne": 72.4,
    # Bucharest, 2026-09-29, deployed frame; controls Prague, Tokyo, London,
    # Glasgow.
    "Bucharest": 69.8,
    # Stockholm, 2026-09-29, deployed frame; the same controls as Bucharest.
    "Stockholm": 72.1,
    # Incheon, 2026-09-29, deployed frame; the same controls as Bucharest.
    "Incheon": 54.4,
    # Goyang, Seongnam, Yongin: the same run as Incheon.
    "Goyang": 52.1, "Seongnam": 71.4, "Yongin": 45.9,
    # Suwon, 2026-09-29, local app (lean venv); controls Prague, Tokyo, London,
    # Glasgow, Incheon, Goyang, Yongin.
    "Suwon": 45.3,
    # Bucheon, 2026-09-29, local app; the same controls as Suwon.
    "Bucheon": 60.1,
    # Namyangju, 2026-09-30; controls Prague, Tokyo, Houston, Toronto.
    "Namyangju": 75.8,
    # Ansan, 2026-09-30; the same controls as Namyangju.
    "Ansan": 41.5,
    # Uijeongbu, 2026-09-30; the same controls as Namyangju.
    "Uijeongbu": 68.6,
    # Anyang, 2026-09-30; the same controls as Namyangju.
    "Anyang": 51.6,
    # Bergen, 2026-09-29, local app (lean venv); controls Prague, Tokyo,
    # London, Glasgow, Oslo.
    "Bergen": 48.3,
    # Aarhus, 2026-09-29, local app; the same run and controls as Bergen.
    "Aarhus": 46.9,
    # Odense, 2026-09-30, in a browser tab with Google Fonts' Space Grotesk
    # stylesheet loaded (not the app); controls Aarhus, Prague, Oslo, Riga,
    # Bergen, Boston, Chicago.
    "Odense": 50.6,
    # Liepāja, 2026-09-30, the same tab as Odense; controls Aarhus, Riga,
    # Odense.
    "Liepāja": 48.2,
    # Daugavpils, 2026-09-30, the same tab.
    "Daugavpils": 73.7,
    # Kansas City, 2026-09-30, as Odense in a fresh tab; controls Houston,
    # Odense, Daugavpils, Riga.
    "Kansas City": 79.3,
    # Tucson and New Orleans: the same tab as Kansas City.
    "Tucson": 48.6,
    "New Orleans": 82.8,
    # Florence, 2026-09-30, as Odense in a fresh tab; controls Houston, Odense,
    # Kansas City, Daugavpils.
    "Florence": 58.1,
    # Göteborg, Den Haag and Zurich: the same tab as Florence (2026-09-30).
    "Göteborg": 63.6,
    "Den Haag": 63.8,
    "Zurich": 42.6,
    # Buffalo, 2026-09-29, local app (lean venv); the same run and controls as
    # Bergen.
    "Buffalo": 48.8,
    # Sacramento, 2026-09-29, the same run and controls as Bergen.
    "Sacramento": 81.3,
    # Houston, 2026-09-29, the same run as Sacramento.
    "Houston": 56.9,
    # Ottawa, 2026-09-29, the font from Google Fonts as the app loads it;
    # controls Prague, Tokyo, Houston, Toronto.
    "Ottawa": 47.5,
    # Minneapolis, 2026-09-30, the same way and controls as Ottawa.
    "Minneapolis": 81.6,
    # Pittsburgh, 2026-09-30, the same way and controls as Ottawa.
    "Pittsburgh": 70.7,
    # Kitchener–Waterloo (Regional), 2026-09-30, in a browser; the same
    # controls as Ottawa.
    "Kitchener–Waterloo (Regional)": 207.2,
    # Palma, 2026-09-30, in a browser; the same controls as Ottawa.
    "Palma": 40.1,
    # Yokohama, 2026-09-30; the same controls as Ottawa.
    "Yokohama": 68.8,
    # Hiroshima, 2026-09-30; the same controls as Ottawa.
    "Hiroshima": 66.3,
    # Dallas, 2026-09-30; controls Prague, Tokyo, Houston, Toronto, Yokohama.
    "Dallas": 40.1,
    "Guadalajara (Regional)": 152.7, "Los Angeles": 80.8, "Madrid": 47.2,
    "Mexico City": 80.0,
    "Miami (Regional)": 112.6, "Montréal": 60.8, "New York": 61.4,
    "Philadelphia": 82.3, "San Diego": 67.4, "San Francisco": 94.3,
    "Toronto": 52.4, "Vancouver (Regional)": 144.4, "Washington D.C.": 110.3,
    # The French tram batch, 2026-09-30, the app's own document; controls
    # Paris, Marseille, Lille (Regional).
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
    # Angers, 2026-09-30, after the Google Fonts faces loaded; controls Paris,
    # Marseille, Lille (Regional), Le Havre, Saint-Étienne.
    "Angers": 47.2,
    # The six Czech tram cities, 2026-09-30, local app (lean venv); controls
    # Prague, Copenhagen, Oslo, Rennes, Toulouse, Paris, Lille (Regional),
    # Milan.
    "Brno": 31.9, "Plzeň": 36.0, "Olomouc": 59.1, "Ostrava": 51.6,
    "Liberec (Regional)": 122.9, "Most (Regional)": 107.5,
    # The UK six, 2026-10-02, after the Google Fonts face loaded in the
    # browser pane; controls Newcastle (Regional) 143.1, London, Glasgow.
    "Manchester (Regional)": 153.9, "Birmingham (Regional)": 153.2, "Edinburgh": 69.3,
    "Sheffield": 59.7, "Nottingham (Regional)": 151.7, "Blackpool (Regional)": 139.7,
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
    """Web-Mercator pixel position on a w x h canvas centered on the view."""
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
