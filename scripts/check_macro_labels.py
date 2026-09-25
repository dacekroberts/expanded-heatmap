"""Check the macro map's city labels for collisions, covered markers and clipping.

WHY THIS EXISTS. The macro map is the app's only navigation, and its label
layout is hand-tuned pixel offsets in `app/cities.py`. Three defects have
shipped from it, each found by eye or by an agent rather than by a check:

  - a pill covering its OWN marker (Guadalajara, spotted by the owner on the
    rendered map: the opaque pill erased the teal dot entirely);
  - a pill covering ANOTHER city's marker (New York's pill erases Boston's dot
    in the composite view - 0 rendered teal pixels against 32-65 for every
    other city);
  - a pill overlapping another pill (Toronto x Boston, 30x12 px).

An ad-hoc check written for the region split found none of the last two,
because it scored only each REGION'S OWN MEMBER CITIES. Every city is drawn in
every region - the view is centred, not filtered - so a non-member still
renders at the frame edge and still collides. `docs/` calls that the blind
spot it was: "Los Angeles" x "San Diego" overlap 20.5 x 11.2 px in United
States East, where neither is a member.

So this scores EVERY city in EVERY region at EVERY width, and it is a script
rather than a note because the offsets are re-tuned whenever a city is added.

The model is Web-Mercator arithmetic against `fit_view`'s own maths, with text
widths measured once in a real browser with the real font loaded (see
TEXT_WIDTH). It reproduced deploy-verify's rendered-pixel measurements of five
clipped labels to 0.1 px on 2026-09-22, which is what licenses using it in
place of a browser for routine checks.

    python scripts/check_macro_labels.py [--width 375] [--verbose]

Exit status is non-zero if any collision or covered marker is found. CLIPPING
AT PHONE WIDTH IS REPORTED, NOT FAILED: cities.py documents it as a structural
trade-off (Washington D.C. is 39% clipped at 375 px), every clipped pill stays
clickable, and the full text-link list beneath the map is the navigation
guarantee.
"""
import argparse
import math
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):   # "Montréal" is unprintable under cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "app"))
from cities import (  # noqa: E402
    CITIES,
    DEFAULT_FRAME,
    DEFAULT_REGION,
    REGION_MEMBERS,
    REGION_ZOOM_WITHOUT,
    REGIONS,
    cities_in,
    elsewhere_counts,
)

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
    "Guadalajara (Regional)": 152.7, "Los Angeles": 80.8, "Madrid": 47.2,
    "Mexico City": 80.0,
    "Miami (Regional)": 112.6, "Montréal": 60.8, "New York": 61.4,
    "Philadelphia": 82.3, "San Diego": 67.4, "San Francisco": 94.3,
    "Toronto": 52.4, "Vancouver (Regional)": 144.4, "Washington D.C.": 110.3,
}

PILL_PAD_X = 5            # background_padding=[5, 2]
PILL_H = 18.0             # measured from rendered pixels, 14 px text
MARKER_R = 5.0            # get_radius=4 plus the 1 px ring
DEFAULT_OFFSET = ("middle", 0, -22)
CANVAS = {375: 343, 768: 726, 1200: 1030}   # viewport -> deck canvas width
CANVAS_H = 460
REF_W, FILL = 320, 0.7

# Abutting pills are not a defect: a shared edge reads as two pills, not one
# smear. Only an overlap on BOTH axes greater than this counts.
TOUCH = 1.0

# KNOWN-ACCEPTED OVERLAPS, each with the numbers it was accepted at.
#
# This is deliberately NOT a raised TOUCH threshold. Loosening the rule to 2 px
# to silence one hairline case would also silence every future one, which is
# tuning a check to hide a finding. An entry here says: this exact pair, in
# this region, at these measured dimensions, has been looked at and judged
# harmless - and nothing else has.
#
# It still fails if the geometry MOVES. The recorded overlap is a ceiling plus
# ACCEPTED_TOL, so a change that grows the overlap past what was actually
# examined comes back as a problem rather than inheriting the exemption.
#
# Keyed (region, then the two names sorted).
# EMPTIED 2026-09-23, and by removing the CAUSE rather than the symptom.
#
# This held one entry - Guadalajara x Los Angeles in the United States view,
# an owner's call agreeing with deploy-verify that a 1.1 px abutment of two
# pill BACKGROUNDS, with the glyphs clear, was legible rather than a defect.
# Marseille's arrival was about to add two more, and that is what made the
# shape visible: all three were a NON-MEMBER's label colliding inside a view it
# does not belong to, and the list would have grown by roughly one entry per
# international city forever.
#
# `Overview.py` now labels only a region's own cities, composites included, so
# none of the three collisions can occur at all. An accepted-overlap entry is a
# judgement that a real collision is harmless; these are no longer real.
#
# The mechanism stays, because the reasoning above it is still right: an entry
# here says THIS pair, in THIS region, at THESE measured dimensions has been
# looked at - and nothing else has. It is not a loosened threshold.
ACCEPTED_OVERLAPS = {}
ACCEPTED_TOL = 0.5

# THE MAP'S OWN CONTROLS, which sit above the label canvas and hide whatever is
# under them. Not modelled until 2026-09-23, so the check scored PROBLEMS 0
# while Oslo's pill - the Europe frame's northernmost city, label above its dot
# - was entirely under the theme button at 375px (label x 242-281 y 18-36,
# button x 180-291 y 10-42; found by Oslo's deploy-verify, not by this).
#
# Measured in the deployed app's own frame (/~/+/) at 375px (canvas 343) and
# 1200px (canvas 1030), each after a screenshot forced a real frame - a hidden
# pane reported the Mapbox controls at a 300px-wide layout. Offsets are from
# the canvas's RIGHT edge because that is how the CSS places them:
#   theme button  `#macro-theme-toggle { top: 10px; right: 52px }` - 111 px wide
#                 with "☀ Light mode", 103.5 with "☾ Dark mode"; the wider is
#                 used, since either can be showing. 32 px tall.
#   zoom group    Mapbox's top-right navigation control, 28.8 x 57.6.
#   credit        Mapbox's attribution, 244.1 x 20: inset 10 px in its compact
#                 form on a narrow map (375) and flush in the corner on a wide one
#                 (1200). Mapbox goes compact below 640 px of map width.
# The button's width depends on the system sans-serif, so re-measure if the
# label text or font changes.
def controls(cw):
    credit = ((cw - 10 - 244.1, CANVAS_H - 30, cw - 10, CANVAS_H - 10) if cw < 640
              else (cw - 244.1, CANVAS_H - 20, cw, CANVAS_H))
    return [("theme button", (cw - 163.0, 10.0, cw - 52.0, 42.0)),
            ("zoom buttons", (cw - 42.0, 12.0, cw - 13.2, 69.6)),
            ("map credit", credit)]


def fit_view(lats, lons, west_pad=0.12):
    lon_min = min(lons) - west_pad * max(max(lons) - min(lons), 0.5)
    lat_span = max(max(lats) - min(lats), 0.5)
    lon_span = max(max(lons) - lon_min, 0.5)
    centre_lat = (max(lats) + min(lats)) / 2
    z_lon = math.log2(REF_W * 360 * FILL / (512 * lon_span))
    z_lat = math.log2(CANVAS_H * 360 * FILL * math.cos(math.radians(centre_lat))
                      / (512 * lat_span))
    return centre_lat, (max(lons) + lon_min) / 2, max(1.0, min(z_lon, z_lat, 9.0))


def region_view(region):
    """Centre and zoom exactly as app/Overview.py computes them: the landing
    region borrows DEFAULT_FRAME's frame, and every frame but that one is
    re-centred."""
    frame = DEFAULT_FRAME if region["name"] == DEFAULT_REGION else region["name"]
    here = cities_in(frame)
    lats, lons = [c["lat"] for c in here], [c["lon"] for c in here]
    # The zoom may leave out a region's outlier (cities.REGION_ZOOM_WITHOUT,
    # Riga in Europe); the centre below still takes every city, as Overview does.
    skip = REGION_ZOOM_WITHOUT.get(frame, ())
    zs = [c for c in here if c["name"] not in skip] or here
    centre_lat, centre_lon, zoom = fit_view([c["lat"] for c in zs], [c["lon"] for c in zs])
    if frame != DEFAULT_FRAME:                  # Overview.py's re-centring block
        centre_lat = (max(lats) + min(lats)) / 2
        centre_lon = (max(lons) + min(lons)) / 2
    return centre_lat, centre_lon, zoom


def scored_labels(region, clat, clon, zoom):
    """Which cities' pills this region is held to.

    A region labels its own cities and is scored on all of them. THE LANDING
    VIEW IS THE EXCEPTION (owner's decision 2026-09-24, see DEFAULT_REGION in
    cities.py): it labels every city on the planet at the United States zoom,
    so on a wide screen Europe and South America pile up at the right-hand
    side. The owner accepted that; each has its own region, scored in full.

    So the landing view is held to the cities whose MARKERS fall on the
    phone-width canvas, the frame fit_view is sized for. That is North
    America today, decided by the arithmetic and not by a list, so a city
    built inside that frame is scored here without anyone remembering to add
    it.
    """
    if region["name"] != DEFAULT_REGION:
        return {c["name"] for c in region["cities"]}
    cw = CANVAS[375]
    out = set()
    for c in CITIES:
        x, y = project(c["lat"], c["lon"], clat, clon, zoom, cw, CANVAS_H)
        if 0 <= x <= cw and 0 <= y <= CANVAS_H:
            out.add(c["name"])
    return out


def project(lat, lon, centre_lat, centre_lon, zoom, w, h):
    scale = 512 * 2 ** zoom
    x = w / 2 + ((lon + 180) / 360 - (centre_lon + 180) / 360) * scale

    def merc(d):
        s = math.sin(math.radians(d))
        return 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)
    y = h / 2 + (merc(lat) - merc(centre_lat)) * scale
    return x, y


def pill(city, x, y):
    anchor, dx, dy = tuple(city.get("label_offset") or DEFAULT_OFFSET)
    try:
        w = TEXT_WIDTH[city["name"]]
    except KeyError:
        # Raising beats guessing: a width estimated from character count would
        # make every number downstream wrong while still printing confidently.
        raise SystemExit(
            f"no measured text width for {city['name']!r}. Measure it in a real "
            f"browser with the real font loaded and add it to TEXT_WIDTH:\n"
            f"    await document.fonts.ready;\n"
            f"    const c = document.createElement('canvas').getContext('2d');\n"
            f"    c.font = '600 14px \"Space Grotesk\", sans-serif';\n"
            f"    c.measureText({city['name']!r}).width\n"
            f"Check a city already in the table at the same time - if its width "
            f"has moved, the font changed and every entry needs re-measuring.")
    a = x + dx
    left = a if anchor == "start" else a - w if anchor == "end" else a - w / 2
    return (left - PILL_PAD_X, y + dy - PILL_H / 2,
            left + w + PILL_PAD_X, y + dy + PILL_H / 2)


def overlap(a, b):
    return (min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1]))


def caption_arithmetic():
    """The front page's caption must account for every city exactly once.

    ASSERTS A PROPERTY, IT DOES NOT RE-IMPLEMENT THE SUM. A check that
    recomputed the caption the way Overview.py does would agree with it while
    both were wrong, which is precisely what happened: the caption said
    "every region except this one", `REGIONS` holds composites AND their
    halves, and selecting "United States" reported its own nine cities as
    elsewhere - 3 in United States West, 6 in United States East - on the
    DEFAULT view of the front page. Europe read "4 shown, 25 elsewhere" out of
    20 cities. Found on the live site 2026-09-22, not by a check.

    shown + elsewhere == total is true of any correct partition and false of
    that bug, whatever code computes it.
    """
    total = len(CITIES)
    bad = []
    for region in REGIONS:
        name = region["name"]
        shown = len(cities_in(name))
        counts = elsewhere_counts(name)
        got = shown + sum(c for _, c in counts)
        if got != total:
            listed = ", ".join(f"{c} in {m}" for m, c in counts) or "(none)"
            bad.append(
                f"{name}: caption accounts for {got} of {total} cities "
                f"({shown} shown + {got - shown} elsewhere: {listed})"
            )
        for member, _ in counts:
            if member in REGION_MEMBERS:
                bad.append(
                    f"{name}: names the composite {member!r} as elsewhere; "
                    f"composites overlap their halves, so only leaves may be "
                    f"counted"
                )
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, action="append",
                    help="viewport width to check (repeatable; default all three)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    widths = args.width or sorted(CANVAS)

    problems, clips, near, accepted = [], [], [], []
    problems.extend(caption_arithmetic())
    for region in REGIONS:
        clat, clon, zoom = region_view(region)
        for vw in widths:
            cw = CANVAS.get(vw, vw)
            # MARKERS ARE EVERY CITY; LABELS ARE NOT. Overview.py draws the whole
            # CITIES frame in the markers layer at every region - the view is
            # centred, never filtered - but a LEAF region labels only its own
            # members, so a non-member contributes a dot and no pill. Getting
            # this wrong in either direction hides a defect: scoring LABELS for
            # members only was the blind spot that let "Los Angeles" x "San
            # Diego" overlap 20.5 x 11.2 px in United States East while a check
            # called that region clean, and scoring every city's label now would
            # report pills the app no longer draws.
            # EVERY REGION LABELS ITS OWN CITIES, composites included since
            # 2026-09-23 - see Overview.py for the measurement that ended the
            # composite's exemption. `region["cities"]` already resolves a
            # composite to its members, so this needs no special case.
            # The landing view is the one exception - see scored_labels().
            labelled = scored_labels(region, clat, clon, zoom)
            markers, placed = [], []
            for city in CITIES:
                x, y = project(city["lat"], city["lon"], clat, clon, zoom, cw, CANVAS_H)
                on = 0 <= x <= cw and 0 <= y <= CANVAS_H
                markers.append((city, x, y, on))   # a coverage target either way
                if city["name"] not in labelled:
                    continue
                box = pill(city, x, y)
                # A pill entirely off the canvas is not drawn and cannot collide
                # with anything. A pill PARTLY on it can, so the test is
                # intersection with the canvas rather than the marker being
                # inside it.
                if (box[2] < 0 or box[0] > cw or box[3] < 0 or box[1] > CANVAS_H):
                    continue
                placed.append((city, x, y, box, on))

            for city, x, y, box, marker_on in placed:
                # A marker is ERASED when its CENTRE falls inside the pill: the
                # pill is opaque (alpha 235) and drawn above the markers, so the
                # dot stops reading as a position at all - which is how
                # Guadalajara's disappeared. A pill merely touching a dot's edge
                # is not that, and scoring it as such flags Philadelphia against
                # New York, a pair deploy-verify measured as BOTH rendering
                # normally. Grazing contact is listed under `near` instead.
                for other, ox, oy, _ in markers:
                    who = ("its OWN marker" if other is city
                           else f"{other['name']}'s marker")
                    if box[0] < ox < box[2] and box[1] < oy < box[3]:
                        problems.append(
                            f"{region['name']:<20} {vw:>4}px  "
                            f"{city['name']}'s pill covers {who}")
                    elif (box[0] - MARKER_R < ox < box[2] + MARKER_R
                            and box[1] - MARKER_R < oy < box[3] + MARKER_R):
                        near.append(
                            f"{region['name']:<20} {vw:>4}px  "
                            f"{city['name']}'s pill grazes {who}")
                # Only for a city the reader can actually see: a non-member
                # drifting past the frame edge is not "clipped", it is simply
                # elsewhere, and reporting it would bury the real cases.
                if marker_on and (box[0] < 0 or box[2] > cw):
                    cut = max(0.0, -box[0]) + max(0.0, box[2] - cw)
                    clips.append(f"{region['name']:<20} {vw:>4}px  "
                                 f"{city['name']:<24} clipped {cut:5.1f} px "
                                 f"({100 * cut / (box[2] - box[0]):.0f}%)")
                if marker_on and (box[1] < 0 or box[3] > CANVAS_H):
                    problems.append(f"{region['name']:<20} {vw:>4}px  "
                                    f"{city['name']} falls off vertically")
                # Under one of the map's own controls: the pill, or the dot of
                # a city this region labels.
                for what, cb in controls(cw):
                    ox, oy = overlap(box, cb)
                    if ox > TOUCH and oy > TOUCH:
                        problems.append(
                            f"{region['name']:<20} {vw:>4}px  "
                            f"{city['name']}'s pill is under the {what} "
                            f"({ox:.1f} x {oy:.1f} px)")
                    if cb[0] < x < cb[2] and cb[1] < y < cb[3]:
                        problems.append(
                            f"{region['name']:<20} {vw:>4}px  "
                            f"{city['name']}'s marker is under the {what}")

            for i, (a, _, _, ab, _) in enumerate(placed):
                for b, _, _, bb, _ in placed[i + 1:]:
                    ox, oy = overlap(ab, bb)
                    if ox <= TOUCH or oy <= TOUCH:
                        continue
                    key = (region["name"], *sorted((a["name"], b["name"])))
                    ok = ACCEPTED_OVERLAPS.get(key)
                    if ok and ox <= ok[0] + ACCEPTED_TOL and oy <= ok[1] + ACCEPTED_TOL:
                        accepted.append(
                            f"{region['name']:<20} {vw:>4}px  "
                            f"{a['name']} x {b['name']} overlap "
                            f"{ox:.1f} x {oy:.1f} px (accepted at "
                            f"{ok[0]:.1f} x {ok[1]:.1f})")
                        continue
                    problems.append(
                        f"{region['name']:<20} {vw:>4}px  "
                        f"{a['name']} x {b['name']} overlap "
                        f"{ox:.1f} x {oy:.1f} px"
                        + (f" - GREW past the accepted {ok[0]:.1f} x {ok[1]:.1f}"
                           if ok else ""))

    if accepted and args.verbose:
        print(f"Known-accepted overlaps ({len(accepted)}) - see ACCEPTED_OVERLAPS:")
        for line in accepted:
            print(f"  {line}")
        print()

    if near and args.verbose:
        print(f"Pills grazing a marker's edge ({len(near)}) - reported, not failed:")
        for line in near:
            print(f"  {line}")
        print()

    if clips and args.verbose:
        print(f"Clipping at the canvas edge ({len(clips)}) - reported, not failed:")
        for line in clips:
            print(f"  {line}")
        print()
    elif clips:
        print(f"{len(clips)} label(s) clipped at a canvas edge; --verbose to list.\n")

    if problems:
        print(f"PROBLEMS {len(problems)}")
        for line in problems:
            print(f"  {line}")
        return 1
    print(f"PROBLEMS 0 - {len(REGIONS)} regions x {len(widths)} widths, "
          f"every city scored in every region; and every region's caption "
          f"accounts for all {len(CITIES)} cities exactly once")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
