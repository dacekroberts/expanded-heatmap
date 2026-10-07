"""Check the macro map's city labels for collisions, covered markers and clipping.

WHY THIS EXISTS. The macro map is the app's only navigation, and its label
layout is hand-tuned pixel offsets in `app/cities.py`. Three defects have
shipped from it, none caught by a check:

  - a pill covering its OWN marker (Guadalajara: the opaque pill erased the
    teal dot entirely);
  - a pill covering ANOTHER city's marker (New York's pill erases Boston's dot
    in the composite view: 0 rendered teal pixels against 32-65 for every
    other city);
  - a pill overlapping another pill (Toronto x Boston, 30x12 px).

Scoring only each REGION'S OWN MEMBER CITIES misses the last two. Every city
is drawn in every region (the view is centred, not filtered), so a
non-member still renders at the frame edge and still collides: "Los Angeles"
x "San Diego" overlap 20.5 x 11.2 px in United States East, where neither is
a member.

So this scores, at EVERY width, every city each region labels: its own
members (a minor-tier city only in its own region) plus REGION_LABELS_ALSO,
and in the Global landing view the winners of app/label_competition.py. Every
city's marker counts as something a pill may not cover, except that in Global
only winners' dots do. It is a script rather than a note because the offsets
are re-tuned whenever a city is added.

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
import re
import sys

if hasattr(sys.stdout, "reconfigure"):   # "Montréal" is unprintable under cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "app"))
from cities import (  # noqa: E402
    CITIES,
    COMPETING_REGIONS,
    COUNTRY_TOP,
    DEFAULT_FRAME,
    DEFAULT_REGION,
    LANDING_NO_ROOM,
    REGION_MEMBERS,
    REGION_LABELS_ALSO,
    REGION_ZOOM,
    REGION_ZOOM_WITHOUT,
    REGIONS,
    cities_in,
    elsewhere_counts,
    region_caption,
)

# TEXT_WIDTH, the measured pill widths, lives in app/label_competition.py
# since 2026-10-01, where the app's Global label competition reads it too.
from label_competition import TEXT_WIDTH, compete  # noqa: E402

# GLOBAL'S LABELS ARE WON, NOT LISTED (owner, 2026-10-01): the landing view
# labels the winners of app/label_competition.py's competition at their
# winning offsets, so this check scores exactly those. Filled in by main().
GLOBAL_WON = {}
# The same for each region in cities.COMPETING_REGIONS (2026-10-04), keyed by
# region: its labelled cities compete at its own view.
REGION_WON = {}

PILL_PAD_X = 5            # background_padding=[5, 2]
PILL_H = 18.0             # measured from rendered pixels, 14 px text
MARKER_R = 6.0            # Overview.DOT_PX / 2: 12 px icons since 2026-09-30 (was 4 + 1 px ring)
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
# EMPTIED 2026-09-23 by removing the CAUSE rather than the symptom. Its one
# entry (Guadalajara x Los Angeles in the United States view, a 1.1 px
# abutment of two pill BACKGROUNDS with the glyphs clear, accepted by the
# owner) and the two Marseille would have added were all a NON-MEMBER's label
# colliding inside a view it does not belong to; the list would have grown by
# about one entry per international city. `Overview.py` now labels only a
# region's own cities, composites included, so none of them can occur.
#
# The mechanism stays: an entry here says THIS pair, in THIS region, at THESE
# measured dimensions has been looked at, and nothing else has. It is not a
# loosened threshold.
ACCEPTED_OVERLAPS = {}
ACCEPTED_TOL = 0.5

# DOTS ON TOP OF DOTS (review lessons, 2026-09-30): two markers whose centres
# sit within one marker radius in a member's OWN region - the closest view the
# macro map gives it - so neither can be told apart or clicked anywhere. Global
# and the composites are not judged: a continental view stacks neighbours by
# design, and the reader drills down. These seven were measured on 2026-10-01
# and wait for the site-wide prose and UI pass (PLAN, calls A3, A6, A7, B6:
# draw the older city on top, or give the pair a closer regional view); a NEW
# pair, or one of these drawn closer, fails.
# (city, city) sorted -> the centre distance in px when listed (zoom is fixed
# per region, so it is the same at every width).
KNOWN_STACKED = {
    ("Taipei (Regional)", "Taoyuan"): 1.8,
    ("Kobe", "Osaka"): 2.3,
    ("Tokyo", "Yokohama"): 2.3,
    ("Den Haag", "Rotterdam"): 3.0,
    ("Kyoto", "Osaka"): 3.5,
    ("Santos (Regional)", "São Paulo"): 4.6,
    ("Kobe", "Kyoto"): 5.1,
}
STACKED_TOL = 0.2

# THE MAP'S OWN CONTROLS, which sit above the label canvas and hide whatever is
# under them. Modelled since 2026-09-23; before that the check scored PROBLEMS
# 0 while Oslo's pill (the Europe frame's northernmost city, label above its
# dot) was entirely under the theme button at 375px (label x 242-281 y 18-36,
# button x 180-291 y 10-42).
#
# Measured in the deployed app's own frame (/~/+/) at 375px (canvas 343) and
# 1200px (canvas 1030), each in a rendered frame: a hidden pane reports the
# Mapbox controls at a 300px-wide layout. Offsets are from the canvas's RIGHT
# edge because that is how the CSS places them:
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
    # The frame takes the REGION_LABELS_ALSO anchors too, as Overview.py does
    # (owner, 2026-10-04: East Asia had fitted Hong Kong and Taiwan alone).
    here = cities_in(frame) + [c for c in CITIES if c.get("region") in REGION_LABELS_ALSO.get(frame, ())
                               and c.get("label_tier") != "minor"]
    lats, lons = [c["lat"] for c in here], [c["lon"] for c in here]
    # The zoom may leave out a region's outlier (cities.REGION_ZOOM_WITHOUT,
    # Riga in Europe); the centre below still takes every city, as Overview does.
    skip = REGION_ZOOM_WITHOUT.get(frame, ())
    zs = [c for c in here if c["name"] not in skip] or here
    centre_lat, centre_lon, zoom = fit_view([c["lat"] for c in zs], [c["lon"] for c in zs])
    # A zoom set outright (cities.REGION_ZOOM, France North and South at 5.0),
    # applied after the fit exactly as Overview.py applies it.
    zoom = REGION_ZOOM.get(frame, zoom)
    if frame != DEFAULT_FRAME:                  # Overview.py's re-centring block
        centre_lat = (max(lats) + min(lats)) / 2
        centre_lon = (max(lons) + min(lons)) / 2
    return centre_lat, centre_lon, zoom


def scored_labels(region, clat, clon, zoom):
    """Which cities' pills this region is held to.

    A region labels its own cities (a minor-tier city only in its own
    region) and any REGION_LABELS_ALSO anchors, and is scored on all of them.
    THE LANDING VIEW IS THE EXCEPTION: since 2026-10-01 it labels only the
    winners of app/label_competition.py's competition (GLOBAL_WON), across the
    whole world, and is scored on exactly those.
    """
    # A minor city is labelled only in its own region - Overview.py's rule
    # (owner's label tiers, 2026-09-29; first applied 2026-09-30).
    def labelled(c):
        return c.get("label_tier") != "minor" or c.get("region") == region["name"]

    if region["name"] in REGION_WON:
        return set(REGION_WON[region["name"]])
    if region["name"] != DEFAULT_REGION:
        # Plus another region's anchors where this view labels them (East Asia
        # names Seoul) - REGION_LABELS_ALSO in cities.py, as Overview.py reads it.
        also = REGION_LABELS_ALSO.get(region["name"], ())
        return ({c["name"] for c in region["cities"] if labelled(c)}
                | {c["name"] for c in CITIES if c.get("region") in also
                   and c.get("label_tier") != "minor"})
    # The landing view: the competition's winners (GLOBAL_WON), the whole
    # world rather than the cities on the phone-width frame as before
    # 2026-10-01.
    return set(GLOBAL_WON)


def project(lat, lon, centre_lat, centre_lon, zoom, w, h):
    scale = 512 * 2 ** zoom
    x = w / 2 + ((lon + 180) / 360 - (centre_lon + 180) / 360) * scale

    def merc(d):
        s = math.sin(math.radians(d))
        return 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)
    y = h / 2 + (merc(lat) - merc(centre_lat)) * scale
    return x, y


def pill(city, x, y, region_name=None):
    # A region's own override first (label_offset_by_region, Overview.py's rule).
    off = (city.get("label_offset_by_region") or {}).get(region_name)
    if region_name == DEFAULT_REGION and city["name"] in GLOBAL_WON:
        off = GLOBAL_WON[city["name"]]
    if city["name"] in REGION_WON.get(region_name, {}):
        off = REGION_WON[region_name][city["name"]]
    anchor, dx, dy = tuple(off or city.get("label_offset") or DEFAULT_OFFSET)
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
    both were wrong, as on the live site on 2026-09-22: the caption said
    "every region except this one", `REGIONS` holds composites AND their
    halves, and selecting "United States" reported its own nine cities as
    elsewhere (3 in United States West, 6 in United States East) on the
    DEFAULT view of the front page. Europe read "4 shown, 25 elsewhere" out of
    20 cities.

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


def caption_against_labels(region, vw, placed):
    """A region view's caption must account for every label the view draws.

    The owner's finding of 2026-10-03: East Asia's caption said "Showing 6
    cities" while the view labelled 15, nine of them REGION_LABELS_ALSO
    anchors from Japan and the Seoul Capital Area. Reads the sentence the app
    renders (cities.region_caption) and asserts two properties at each width:
    the number it states is the region's own member count, and every pill at
    least partly on the canvas belongs to a member, or to a city or region the
    caption names. A member left unlabelled (a minor-tier city in a composite)
    is not a failure: its dot is still drawn. Global states the whole site's
    count and is not judged here.
    """
    name = region["name"]
    if name == DEFAULT_REGION:
        return []
    caption = region_caption(name)
    members = {c["name"] for c in region["cities"]}
    bad = []
    stated = re.search(r"Showing (\d+) cit", caption)
    if not stated or int(stated.group(1)) != len(members):
        bad.append(f"{name:<20} {vw:>4}px  caption {caption!r} does not state "
                   f"the region's {len(members)} cities")
    # Or its country: a caption names a country split into views once
    # (cities._CAPTION_NAME, "Japan" for the nine Japanese views).
    unnamed = sorted(c["name"] for c, *_ in placed
                     if c["name"] not in members and c["name"] not in caption
                     and c.get("region") not in caption and c.get("country") not in caption)
    if unnamed:
        bad.append(f"{name:<20} {vw:>4}px  caption {caption!r} neither counts "
                   f"nor names {len(unnamed)} labelled cit"
                   f"{'y' if len(unnamed) == 1 else 'ies'}: {', '.join(unnamed)}")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, action="append",
                    help="viewport width to check (repeatable; default all three)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    widths = args.width or sorted(CANVAS)

    problems, clips, near, accepted = [], [], [], []
    # A MEMBER WHOSE OWN DOT IS OFF THE CANVAS: the clipping test below runs
    # only for a visible marker, so this is listed separately (2026-09-30:
    # Bordeaux and Nice in France South at 375 px, each leaving a fragment of
    # its pill; Tucson's re-centring pushing San Francisco and Sacramento off
    # United States West). Reported, not failed, like clipping: the pinned
    # France zooms accept it by the owner's call.
    offframe = []
    stacked = []
    problems.extend(caption_arithmetic())
    g = next(r for r in REGIONS if r["name"] == DEFAULT_REGION)
    facts = __import__("json").loads((pathlib.Path(__file__).resolve().parents[1] / "app"
                                       / "macro_facts.json").read_text(encoding="utf-8"))
    GLOBAL_WON.clear()
    REGION_WON.clear()
    GLOBAL_WON.update(compete(CITIES, *region_view(g), facts.get("storefronts", {}), strict=True))
    for region in REGIONS:
        clat, clon, zoom = region_view(region)
        if region["name"] in COMPETING_REGIONS:
            # Entrants first (the hand rule's labelled set), then the winners
            # replace them, exactly as Overview.py runs it.
            REGION_WON[region["name"]] = compete(
                CITIES, clat, clon, zoom, facts.get("storefronts", {}), strict=True,
                entrants=scored_labels(region, clat, clon, zoom), region=region["name"])
        for vw in widths:
            cw = CANVAS.get(vw, vw)
            # MARKERS ARE EVERY CITY; LABELS ARE NOT. Overview.py draws the whole
            # CITIES frame in the markers layer at every region - the view is
            # centred, never filtered - but a LEAF region labels only its own
            # members, so a non-member contributes a dot and no pill. Getting
            # this wrong in either direction hides a defect: scoring LABELS for
            # members only was the blind spot that let "Los Angeles" x "San
            # Diego" overlap 20.5 x 11.2 px in United States East unreported,
            # and scoring every city's label now would report pills the app no
            # longer draws.
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
                box = pill(city, x, y, region["name"])
                if not on:
                    shows = not (box[2] < 0 or box[0] > cw or box[3] < 0 or box[1] > CANVAS_H)
                    offframe.append(f"{region['name']:<20} {vw:>4}px  {city['name']:<24} "
                                    f"dot off the canvas"
                                    + (", a fragment of its pill shows" if shows else ""))
                # A pill entirely off the canvas is not drawn and cannot collide
                # with anything. A pill PARTLY on it can, so the test is
                # intersection with the canvas rather than the marker being
                # inside it.
                if (box[2] < 0 or box[0] > cw or box[3] < 0 or box[1] > CANVAS_H):
                    continue
                placed.append((city, x, y, box, on))

            problems.extend(caption_against_labels(region, vw, placed))

            for city, x, y, box, marker_on in placed:
                # A marker is ERASED when its CENTRE falls inside the pill: the
                # pill is opaque (alpha 235) and drawn above the markers, so the
                # dot stops reading as a position at all (Guadalajara's). A pill
                # merely touching a dot's edge is not that: scored as such it
                # flags Philadelphia against New York, a pair deploy-verify
                # measured as BOTH rendering normally. Grazing contact is listed
                # under `near` instead.
                for other, ox, oy, _ in markers:
                    # In Global and a competing region a non-winner's dot is
                    # drawn faded UNDER the pills by design (Overview.py);
                    # only a winner's counts.
                    won = (GLOBAL_WON if region["name"] == DEFAULT_REGION
                           else REGION_WON.get(region["name"]))
                    if won is not None and other["name"] not in won:
                        continue
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

            # Dots on top of dots, judged in a member's own region only.
            onc = [(c, x, y) for c, x, y, on in markers if on]
            for i, (a, ax, ay) in enumerate(onc):
                for b, bx, by in onc[i + 1:]:
                    if region["name"] not in (a.get("region"), b.get("region")):
                        continue
                    d = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
                    if d >= MARKER_R:
                        continue
                    key = tuple(sorted((a["name"], b["name"])))
                    was = KNOWN_STACKED.get(key)
                    line = (f"{region['name']:<20} {vw:>4}px  {key[0]} x {key[1]} "
                            f"dots {d:.1f} px apart")
                    if was is not None and d >= was - STACKED_TOL:
                        stacked.append(line + " (known; the UI pass)")
                    else:
                        problems.append(line + (f" - CLOSER than the known {was}"
                                                if was is not None else
                                                " - one dot on top of the other"))

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

    # THE OWNER'S LABEL GOAL (2026-10-07, Staging's call 197): "all dots
    # visible in at least one regional view" and "every nation's top 1 ... in
    # global view". Every city is labelled in at least one view, and each
    # country's top city (cities.COUNTRY_TOP) is labelled on the landing view
    # unless cities.LANDING_NO_ROOM names it; one named there that now fits is
    # reported, so the list does not outlive its reason.
    named = set(GLOBAL_WON)
    for region in REGIONS:
        if region["name"] != DEFAULT_REGION:
            named |= set(scored_labels(region, *region_view(region)))
    unnamed = [c["name"] for c in CITIES if c["name"] not in named]
    if unnamed:
        problems.append(f"{'(every view)':<20}        {unnamed} labelled in no view - give each "
                        f"a view that places it (a country view, as Benelux placed Den Haag)")
    roomy = []
    for country, (top, _) in COUNTRY_TOP.items():
        if top not in GLOBAL_WON and top not in LANDING_NO_ROOM:
            problems.append(f"{DEFAULT_REGION:<20}        {country}'s top city {top} has no label "
                            f"on the landing view (cities.COUNTRY_TOP)")
        elif top in GLOBAL_WON and top in LANDING_NO_ROOM:
            roomy.append(top)
    if roomy:
        print(f"Now labelled on the landing view, so drop from cities.LANDING_NO_ROOM: {roomy}\n")

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

    if stacked and args.verbose:
        print(f"Known dots on top of dots ({len(stacked)}) - see KNOWN_STACKED:")
        for line in stacked:
            print(f"  {line}")
        print()
    elif stacked:
        print(f"{len({l.split('px  ')[1].split(' dots')[0] for l in stacked})} known pair(s) "
              f"of dots on top of each other (KNOWN_STACKED); --verbose to list.\n")

    if offframe and args.verbose:
        print(f"Members whose dot is off the canvas ({len(offframe)}) - reported, not failed:")
        for line in offframe:
            print(f"  {line}")
        print()
    elif offframe:
        print(f"{len(offframe)} member dot(s) off the canvas; --verbose to list.\n")

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
          f"every city scored in every region; every region's caption "
          f"accounts for all {len(CITIES)} cities exactly once, and for every "
          f"label its own view draws")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
