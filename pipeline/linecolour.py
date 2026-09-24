"""Transit-line colour separation, measured rather than eyeballed.

Calgary's Blue Line shipped as Calgary Transit's own `#0072CE`, which is
**CIE76 Delta-E 3.3 from Retail's `#2a78d6`** - the same blue as the pins drawn
on top of it. Nobody measured it. It surfaced only when Edmonton's build ran
this check for the first time, weeks later, while choosing a different city's
palette.

TWO THRESHOLDS, AND THE GAP BETWEEN THEM IS A RECORDED DECISION
---------------------------------------------------------------
The obvious implementation - refuse to render any line within ~45 Delta-E of a
category colour - is **wrong for this project**, and measuring before building
it is what showed that. Surveyed 2026-09-21 across all fourteen cities:

    13.6  New York    #009952   (MTA green)
    14.0  New York    #0062CF   (MTA blue)
    16.9  Montreal    #0095E6   (STM blue)
    20.1  Boston      #00843D   (MBTA green)
    26.0  Washington  #009CDE
    26.2  Philadelphia #0097D6
    27.3  Boston      #003DA5
    ...   fourteen values below 45 across six cities

Every one is an **agency's official colour**, kept under the owner's branding
decision of 2026-09-21: real line names and real route colours, with a
non-affiliation notice. A hard gate at 45 would recolour six cities and
overturn that decision by implication, which a lint rule has no business doing.

So:

  **HARD_FLOOR (10)** - below this two colours are not "close", they are the
  same colour at a glance, and a line drawn under its own pins disappears.
  This RAISES. Calgary's 3.3 would have failed here at render time.

  **PREFERRED (45)** - this project's working figure, behind `#C2185B`'s
  selection (49.6) and `#FBB878`'s (44.8). Below it, a line is REPORTED, every
  render, with its measurement. A new city should clear it: Toronto kept four
  of five TTC colours and darkened one; Edmonton kept its hue and darkened two.
  An existing city below it is a known trade, not a bug to fix silently.

Separation is an **INTRA-CITY** constraint. Each city renders its own map with
its own legend and on-map labels, so two cities sharing a red can never be
confused - Edmonton's Metro red is deliberately Calgary's Red Line red. Nothing
here compares across cities, and it should not: the usable palette runs out
long before the city list does, and the cost of pretending otherwise lands on
later cities as colours that read badly against their own pins.

CIE76 rather than CIEDE2000: it is what this project's existing figures were
computed with, and swapping the metric would silently move every recorded
number. Consistency is worth more here than the last few points of perceptual
accuracy.
"""

import colorsys
import math

HARD_FLOOR = 10.0
PREFERRED = 45.0


def _srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_lab(hex_colour):
    """sRGB hex -> CIE L*a*b* (D65)."""
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"expected a 6-digit hex colour, got {hex_colour!r}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    R, G, B = (_srgb_to_linear(v) for v in (r, g, b))
    X = R * 0.4124564 + G * 0.3575761 + B * 0.1804375
    Y = R * 0.2126729 + G * 0.7151522 + B * 0.0721750
    Z = R * 0.0193339 + G * 0.1191920 + B * 0.9503041

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(X / 0.95047), f(Y / 1.0), f(Z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b):
    """CIE76 colour difference between two hex colours."""
    la, aa, ba = to_lab(a)
    lb, ab, bb = to_lab(b)
    return math.sqrt((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2)


# LINE LABELS, in both themes, and readers who could not read them. A line label
# is drawn in its line's colour on a halo, and until 2026-09-24 both themes got
# it wrong in different ways:
#
#   - DARK (the default) lifted every label with `filter: brightness(1.8)`,
#     which scales each sRGB channel and so does nothing for a colour whose
#     light is all in blue (Porto Alegre's navy Trensurb read at 1.91:1). The
#     filter sat on the label element, so it brightened the HALO too: the dark
#     page colour rendered #132039, and a model measuring against #0B1220 was
#     measuring a halo nobody saw (the map-chrome deploy check, 2026-09-24).
#   - LIGHT drew every label on a white halo, where 145 of 235 - the agencies'
#     yellows and oranges - read under 4.5:1 (Milan's M3 at 1.08:1).
#
# The owner's calls (2026-09-24), both at WCAG's 4.5:1 for text of this size:
#
#   - Dark: lighten a label that fails (the owner's option), and - since the
#     deploy check - with no filter. Each label carries an explicit dark-theme
#     colour: what the old filter produced (so a label that already read is
#     unchanged), with its HSL lightness raised by the smallest step that
#     reaches 4.5:1 against the halo actually drawn, the page colour.
#   - Light: NOT the dark treatment mirrored. Darkening to 4.5:1 moved the
#     median failing label by CIE76 19.9 and turned every yellow olive, so a
#     label no longer matched its line. Instead a label keeps its colour and
#     takes the halo it reads better on - the dark page colour for most, white
#     for navy - and a mid-tone that misses on both gets the smallest
#     lightness step away from its halo (at most Delta-E 3.7 in the survey).
#
# The lines themselves are untouched in both themes.
# scripts/check_map_markup.py measures every committed label the same way.
LABEL_MIN_CONTRAST = 4.5
DARK_LABEL_BRIGHTNESS = 1.8     # the retired dark filter, kept as the starting shade


def _rgb(hex_colour):
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"expected a 6-digit hex colour, got {hex_colour!r}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in rgb)


def _lum(hex_colour):
    r, g, b = (_srgb_to_linear(v) for v in _rgb(hex_colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    """WCAG 2 contrast ratio between two hex colours."""
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def brightened(hex_colour, factor=DARK_LABEL_BRIGHTNESS):
    """The shade CSS `brightness(factor)` gave: each sRGB channel scaled and
    clipped, truncated as the browser does (rounding once put a label 0.04 on
    the wrong side of 4.5:1)."""
    return "#" + "".join(f"{min(255, math.floor(v * factor)):02x}" for v in _rgb(hex_colour))


def _away_from(colour, halo, minimum):
    """`colour` with its HSL lightness moved away from `halo` by the smallest
    0.01 step that reads at `minimum` against it."""
    r, g, b = (v / 255 for v in _rgb(colour))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    sign = -1 if _lum(halo) > _lum(colour) else 1
    for step in range(1, 101):
        c = _hex(v * 255 for v in colorsys.hls_to_rgb(h, min(1.0, max(0.0, l + sign * step / 100)), s))
        if contrast_ratio(c, halo) >= minimum:
            return c
    raise ValueError(f"{colour}: no lightness reaches {minimum}:1 against {halo}")


def label_colours(colour, *, light_halo, dark_halo, minimum=LABEL_MIN_CONTRAST):
    """(light-theme colour, light-theme halo, dark-theme colour) for a line
    label drawn in `colour`. Every result reads at `minimum` against its halo."""
    on_light, on_dark = contrast_ratio(colour, light_halo), contrast_ratio(colour, dark_halo)
    if on_light >= minimum:
        light, halo = colour, light_halo
    else:
        halo = dark_halo if on_dark >= on_light else light_halo
        light = colour if max(on_light, on_dark) >= minimum else _away_from(colour, halo, minimum)
    base = brightened(colour)
    dark = base if contrast_ratio(base, dark_halo) >= minimum else _away_from(base, dark_halo, minimum)
    return light, halo, dark


def check_line_colours(line_colours, category_colours, *, city=""):
    """Measure every transit-line colour against the category pin palette.

    `line_colours`: {label: hex}. `category_colours`: {bucket: hex}.

    Prints one line per transit line, RAISES below HARD_FLOOR, and returns the
    list of (label, hex, worst_bucket, delta_e) below PREFERRED so a caller can
    record them. Also checks the lines against EACH OTHER, since two lines a
    reader cannot tell apart is the same failure one step over.
    """
    if not line_colours or not category_colours:
        return []

    rows, flagged, fatal = [], [], []
    for label, hexv in line_colours.items():
        worst_bucket, worst = None, float("inf")
        for bucket, cat in category_colours.items():
            d = delta_e(hexv, cat)
            if d < worst:
                worst_bucket, worst = bucket, d
        rows.append((label, hexv, worst_bucket, worst))
        if worst < HARD_FLOOR:
            fatal.append((label, hexv, worst_bucket, worst))
        elif worst < PREFERRED:
            flagged.append((label, hexv, worst_bucket, worst))

    where = f" ({city})" if city else ""
    print(f"  line colour separation{where}, CIE76 against the category pins:")
    for label, hexv, bucket, d in sorted(rows, key=lambda r: r[3]):
        mark = ("  *** TOO CLOSE ***" if d < HARD_FLOOR
                else "  (below the preferred 45, recorded)" if d < PREFERRED
                else "")
        print(f"    {hexv}  {label:<28} {d:6.1f} vs {bucket}{mark}")

    labels = list(line_colours)
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            d = delta_e(line_colours[labels[i]], line_colours[labels[j]])
            if d < HARD_FLOOR:
                fatal.append((f"{labels[i]} vs {labels[j]}", "", "each other", d))

    if fatal:
        detail = "; ".join(f"{lab} {hx} is Delta-E {d:.1f} from {b}"
                           for lab, hx, b, d in fatal)
        raise ValueError(
            f"{city or 'this city'}: transit-line colour(s) indistinguishable "
            f"from what is drawn on top of them - {detail}. Below "
            f"{HARD_FLOOR:.0f} two colours are the same colour at a glance, and "
            f"the line vanishes under its own pins. Calgary shipped a Blue Line "
            f"at 3.3 from Retail blue and it went unnoticed for weeks, which is "
            f"why this raises rather than warns. Keep the agency's hue and "
            f"darken it until it clears - see pipeline/linecolour.py."
        )
    return flagged
