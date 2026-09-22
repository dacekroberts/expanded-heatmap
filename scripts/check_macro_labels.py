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
from cities import CITIES, REGIONS  # noqa: E402

# Measured in the browser at `600 14px "Space Grotesk", sans-serif`, the font
# app/components.set_base_font() loads and the TextLayer renders with. Re-measure
# when a city is added; a wrong width here makes every number downstream wrong.
TEXT_WIDTH = {
    "Boston": 48.4, "Calgary": 51.8, "Chicago": 55.0, "Edmonton": 69.0,
    "Guadalajara (Regional)": 152.7, "Los Angeles": 80.8, "Mexico City": 80.0,
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
    """Centre and zoom exactly as app/Overview.py computes them."""
    here = region["cities"]
    lats, lons = [c["lat"] for c in here], [c["lon"] for c in here]
    centre_lat, centre_lon, zoom = fit_view(lats, lons)
    if region["name"] != "United States":       # Overview.py's re-centring block
        centre_lat = (max(lats) + min(lats)) / 2
        centre_lon = (max(lons) + min(lons)) / 2
    return centre_lat, centre_lon, zoom


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
    w = TEXT_WIDTH[city["name"]]
    a = x + dx
    left = a if anchor == "start" else a - w if anchor == "end" else a - w / 2
    return (left - PILL_PAD_X, y + dy - PILL_H / 2,
            left + w + PILL_PAD_X, y + dy + PILL_H / 2)


def overlap(a, b):
    return (min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, action="append",
                    help="viewport width to check (repeatable; default all three)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    widths = args.width or sorted(CANVAS)

    problems, clips, near = [], [], []
    for region in REGIONS:
        clat, clon, zoom = region_view(region)
        for vw in widths:
            cw = CANVAS.get(vw, vw)
            # EVERY CITY, NOT THE REGION'S MEMBERS. The view is centred, never
            # filtered - Overview.py hands both layers the whole CITIES frame -
            # so a non-member is still drawn, still labelled, and still
            # collides. Scoring members only is the exact blind spot that let
            # "Los Angeles" x "San Diego" overlap 20.5 x 11.2 px in United
            # States East, where neither is a member, while a check reported
            # that region clean.
            placed = []
            for city in CITIES:
                x, y = project(city["lat"], city["lon"], clat, clon, zoom, cw, CANVAS_H)
                box = pill(city, x, y)
                # A pill entirely off the canvas is not drawn and cannot collide
                # with anything. A pill PARTLY on it can, so the test is
                # intersection with the canvas rather than the marker being
                # inside it - that is how a non-member at the frame edge stays
                # in scope without dragging in a city the reader cannot see.
                if (box[2] < 0 or box[0] > cw or box[3] < 0 or box[1] > CANVAS_H):
                    continue
                placed.append((city, x, y, box,
                               0 <= x <= cw and 0 <= y <= CANVAS_H))

            for city, x, y, box, marker_on in placed:
                # A marker is ERASED when its CENTRE falls inside the pill: the
                # pill is opaque (alpha 235) and drawn above the markers, so the
                # dot stops reading as a position at all - which is how
                # Guadalajara's disappeared. A pill merely touching a dot's edge
                # is not that, and scoring it as such flags Philadelphia against
                # New York, a pair deploy-verify measured as BOTH rendering
                # normally. Grazing contact is listed under `near` instead.
                for other, ox, oy, _, _ in placed:
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

            for i, (a, _, _, ab, _) in enumerate(placed):
                for b, _, _, bb, _ in placed[i + 1:]:
                    ox, oy = overlap(ab, bb)
                    if ox > TOUCH and oy > TOUCH:
                        problems.append(
                            f"{region['name']:<20} {vw:>4}px  "
                            f"{a['name']} x {b['name']} overlap "
                            f"{ox:.1f} x {oy:.1f} px")

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
          f"every city scored in every region")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
