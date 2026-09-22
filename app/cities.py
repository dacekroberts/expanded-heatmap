"""The app's list of mapped cities - the single source for the Overview's
macro map, its fallback link list, and every city page's city switcher.

Adding a city means adding its entry here (plus its page under app/pages/).
`page` is relative to the entry script (app/Overview.py), which is what
st.page_link and st.switch_page expect.

PAGE NUMBERING: cities are numbered 1..N in the order they were IMPLEMENTED,
and the two information pages sit at 90 and 91 so they never compete for a
city's slot and always sort last in the sidebar. Vancouver is 10 as the tenth
city; **11 is the next free city slot**, which
`scripts/scaffold_city.py`'s `next_page_number()` already returns on its own
because it globs `*_Heatmap.py` and so does not see 90 or 91. Nothing needs
reserving by hand - just do not renumber a city page without updating its
`page` value here, since these two are the only link between them. `lat`/`lon` place the
city's marker on the macro map; they only need to be a sensible centre of its
mapped area, not the exact centre of the city's own map.

Deliberately app-side and tiny: a fuller per-city registry (map centre,
CRS, taxonomy, data sources) is still open in PLAN.md and would live with
the pipeline, not here - the deployed app must stay free of pipeline
dependencies.

Optional `label_offset` places the city's name on the macro map, as
`(text_anchor, dx, dy)` in PIXELS from its marker - anchor is "middle", "start"
(text runs right from the point) or "end" (text ends at the point). Omitted, a
city's name sits just above its marker.

This replaced a three-sided "top"/"left"/"right" enum on 2026-09-21, because
three sides at a ~20 px offset could not separate the east-coast cluster:
Washington D.C., Philadelphia, New York and Boston sit 6-15 px apart at the
continental zoom this map is fitted to, and their name pills are 56-126 px
wide, so with D.C. added there were 11 label collisions - "Philadelphia" and
"Washington D.C." overlapping by 102x13 px, one unreadable smear.

THE OFFSETS ARE IN PIXELS, AND THE MAP IS ZOOMABLE. That combination is what
constrains this layout, and it is the one thing to understand before changing
any number here. A pixel offset does not follow its dot: zoom in and the four
eastern dots spread apart while their names stay put, so a name placed far
from its dot ends up pointing at nothing. An earlier version of this stacked
those four names VERTICALLY at dy -130/-102/-74/-46, in latitude order, which
was collision-free at every width and looked wrong the moment a reader zoomed
in - the owner's screenshot showed "Boston" adrift 130 px from a dot that had
moved elsewhere.

So the four eastern names sit EAST of their dots and near-parallel to them,
at dy -24/-8/+8/+24: close enough to track their own dot (24 px of drift at
worst, against 130 px before) and spread just enough to clear each other,
since the dots' own 6-15 px of vertical spread adds to the offsets. +-24 is
the measured MINIMUM that stays collision-free; tighter and the pills touch.

The map stays zoomable by the owner's decision (2026-09-21): non-US cities are
a possibility, and a fixed view would force continent-specific maps and a
layer of extra pages, which costs more than this layout does. Locking the view
would have allowed the vertical stack instead.

THE ACCEPTED TRADE-OFF: at phone width these four names are clipped by the
right edge - Washington D.C. is 54% visible, Philadelphia 59%, New York 77%,
Boston 79%. That is structural, not tuning. "Washington D.C." is a 126 px pill
whose dot sits at x~271 in a 340 px canvas, leaving 69 px to its east, so no
`dx` fits it; the only anchor that would is "middle", which spends width on
both sides of the dot, and that is what the vertical stack was doing. West
placement collides with Chicago. The clipped pills stay clickable, and the
Overview carries a full text-link list of every city directly beneath the map.

Do NOT solve a label overflow by padding `fit_view`'s bounding box. Padding
widens the longitude span, which lowers the zoom, which pulls the cluster
TIGHTER - an east pad of 0.30 would take the New York/Philadelphia dots from
6.0 px apart to 4.7 px. Move the label, not the box.

Every offset here is verified collision-free at 854 and 1200 px wide, with the
phone-width clipping above as the known exception (the canvas height is always
460 and `fit_view`'s zoom never varies with width, so width is the only
variable). Re-check all three widths after changing any of them, or after
adding a city whose name is long.

`MAP_ONLY_NAV` (below) switches the app between two ways of moving around: True
(the current pilot) hides the sidebar page list and the city switcher on every
city page, so the map is the only navigation (a city's page opens from its
marker, and each city map has an "All cities" button back); False restores the
sidebar and the switcher. Both are documented in
docs/navigation_sidebar_and_city_links.md.
"""

MAP_ONLY_NAV = True

CITIES = [
    {
        "name": "San Diego",
        "lat": 32.7157,
        "lon": -117.1611,
        "page": "pages/1_San_Diego_Heatmap.py",
        "blurb": "MTS Trolley (Blue, Orange, Green, Copper, Silver lines)",
        # East of its dot: it sits south-east of Los Angeles, so the two
        # names split left/below rather than colliding.
        "label_offset": ("start", 16, 0),
    },
    {
        "name": "San Francisco",
        "lat": 37.7509,
        "lon": -122.4414,
        "page": "pages/2_San_Francisco_Heatmap.py",
        "blurb": "Muni Metro (J Church, K Ingleside, L Taraval, M Ocean View, N Judah, T Third Street)",
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Los Angeles",
        "lat": 34.05,
        "lon": -118.31,
        "page": "pages/3_Los_Angeles_Heatmap.py",
        "blurb": "Metro Rail (A, B, C, D, E, K Lines)",
        # BELOW its dot, not west of it. Westward, "Los Angeles" ran off the
        # left edge at phone width - the "flush at 375 px" problem - and
        # widening the view to make room would have lowered the zoom.
        "label_offset": ("middle", 0, 26),
    },
    {
        "name": "Chicago",
        "lat": 41.8781,
        "lon": -87.6298,
        "page": "pages/4_Chicago_Heatmap.py",
        "blurb": "CTA 'L' (Red, Blue, Brown, Green, Orange, Pink, Purple Lines)",
        # SOUTH of its dot, moved 2026-09-21 for the same pre-emptive reason
        # as Vancouver's. Above its dot this label occupied x 439-510,
        # y 158.9-179.9, and **Toronto's dot lands at x 506.6, y 182.0** -
        # touching that box's corner. Toronto's own label will need the band
        # above and east of its dot, which is precisely what this frees.
        #
        # dy is +16 and NOT larger, which is counter-intuitive: a bigger
        # southward offset is WORSE here, because "San Diego" runs east from
        # its own dot to about x 464 at y 224-245, and Chicago's box spans
        # x 439-510. Pushing Chicago further south walks it into that pill.
        # +16 is the measured maximum clearance (7.9 px); +26 collided.
        #
        # A pill 21 px tall at dy +16 starts 5.5 px below the dot's centre,
        # which clears the 4 px marker and its 1 px ring - so it reads as
        # below the dot rather than on it.
        "label_offset": ("middle", 0, 16),
    },
    {
        "name": "New York",
        "lat": 40.7128,
        "lon": -74.006,
        "page": "pages/5_New_York_Heatmap.py",
        "blurb": "Subway trunk lines (8 Av, 6 Av, 7 Av, Lexington Av, Broadway, "
                 "Nassau St, Flushing, Crosstown, 14 St-Canarsie) and the Staten "
                 "Island Railway",
        # East of its dot, second from the top of the eastern column.
        "label_offset": ("start", 14, -8),
    },
    {
        "name": "Philadelphia",
        "lat": 39.9526,
        "lon": -75.1652,
        "page": "pages/6_Philadelphia_Heatmap.py",
        "blurb": "SEPTA Metro — the Market–Frankford and Broad Street Lines, "
                 "plus the subway-surface and Girard Avenue trolleys",
        # East of its dot, third from the top of the eastern column.
        "label_offset": ("start", 14, 8),
    },
    {
        # The only entry whose name is not just a city: this map covers the
        # whole Metrorail/Metromover network, which runs through six
        # municipalities, so "Miami" alone would overstate its scope. The name
        # must match render_city_nav()'s argument on the page.
        "name": "Miami (Regional)",
        "lat": 25.7743,
        "lon": -80.1937,
        "page": "pages/7_Miami_Heatmap.py",
        "blurb": "Metrorail and Metromover (42 stations across six municipalities)",
        # Below its dot: the widest name here (133 px) and the southernmost
        # city, so the empty canvas beneath it is the only place it fits
        # without hitting San Diego's name.
        "label_offset": ("middle", 0, 24),
    },
    {
        "name": "Boston",
        "lat": 42.3601,
        "lon": -71.0589,
        "page": "pages/8_Boston_Heatmap.py",
        "blurb": "MBTA rapid transit (Red, Orange, Blue, Green Lines and the Mattapan Trolley)",
        # East of its dot, top of the eastern column - the northernmost of
        # the four, so it takes the largest upward offset.
        "label_offset": ("start", 14, -24),
    },
    {
        "name": "Washington D.C.",
        "lat": 38.9072,
        "lon": -77.0369,
        "page": "pages/9_Washington_DC_Heatmap.py",
        "blurb": "WMATA Metrorail (Red, Blue, Green, Yellow, Orange, Silver "
                 "Lines; the 40 stations inside the District)",
        # East of its dot, bottom of the eastern column - the southernmost
        # of the four, and the widest name, so it clips first on a phone.
        "label_offset": ("start", 14, 24),
    },
    {
        # "(Regional)" for Miami's reason: this map spans Vancouver AND
        # Surrey, and a map covering two municipalities cannot honestly be
        # called Vancouver. The name must match render_city_nav()'s argument
        # on the page.
        "name": "Vancouver (Regional)",
        "lat": 49.2827,
        "lon": -123.1207,
        "page": "pages/10_Vancouver_Heatmap.py",
        "blurb": "SkyTrain (24 stations across Vancouver and Surrey)",
        # OUTSIDE THE DEFAULT VIEW - the first city to be, and the reason the
        # flag exists. See IN_DEFAULT_VIEW below.
        "in_default_view": False,
        # WEST of its dot, moved 2026-09-21 to pre-empt a collision that was
        # measured rather than anticipated. Running EAST, this 184 px pill
        # occupied x 348-532 at y 129.6-150.6 - and **Calgary's dot lands at
        # x 371.6, y 139.4, inside that box**, with Edmonton's at x 373.8 just
        # above it. So the longest label on the map sat directly across the
        # next two Canadian cities' dots.
        #
        # West is empty: it is the westernmost entry, with ocean beyond, and
        # San Francisco's label sits 30 px lower in y.
        #
        # THE COST, measured and accepted: at 400 px the canvas puts this dot
        # at x 109, so a west-running pill needs 196 px where 109 exist and
        # about 44% of it is clipped by the left edge - worse than Washington
        # D.C.'s 54%-visible. Same trade-off the eastern four already carry,
        # and the same mitigation: the pill stays clickable and the Overview
        # carries a full text-link list of every city beneath the map.
        "label_offset": ("end", -12, -10),
    },
    {
        # Accented display name, ASCII page filename - the one thing this
        # city's build brief flagged as untested. The name here and
        # render_city_nav()'s argument on the page must match each other;
        # neither has to match the filename.
        "name": "Montréal",
        "lat": 45.5019,
        "lon": -73.5674,
        "page": "pages/11_Montreal_Heatmap.py",
        "blurb": "STM Métro (4 lines, 64 stations on the island)",
        # OUTSIDE THE DEFAULT VIEW, for the same reason as Vancouver: it keeps
        # fit_view's zoom pinned at 1.4525 so no existing label moves. Its dot
        # is still on canvas at every width - it sits only ~18 px from
        # Boston's - so this is about the FIT, not about visibility.
        "in_default_view": False,
        # WELL ABOVE its dot, and the direction is measured rather than
        # chosen. Montréal's dot is the NORTHERNMOST on the map, so north is
        # the only empty side: Boston sits 10 px east and 17 px SOUTH, New
        # York 26 px south, Chicago 55 px WEST and 20 px south.
        #
        # It took three tries, and each rejection was a measurement:
        #   west, ("end", -12, -6)     - drove an ~80 px pill across CHICAGO's.
        #   centred, ("middle", 0,-30) - cleared Chicago but collided with
        #                                VANCOUVER's, because "Vancouver
        #                                (Regional)" is a ~184 px pill running
        #                                east from its dot and reaching x~532.
        #   east and high, this one    - clears Vancouver's pill by ~9 px
        #                                horizontally and Boston's by ~6 px
        #                                vertically, at 400, 854 and 1200 px.
        # Montréal is wedged between the two longest names on the map, so if
        # either of those labels is ever moved or renamed, re-check this one.
        "label_offset": ("start", 12, -34),
    },
    {
        "name": "Calgary",
        "lat": 51.0447,
        "lon": -114.0719,
        "page": "pages/12_Calgary_Heatmap.py",
        # 45, not 83. The feed publishes 83 PLATFORMS and this blurb said so
        # until the collapse was written - the same error the Canada ranking
        # made. See pipeline/calgary/config.py.
        "blurb": "CTrain (Red and Blue Lines, 45 stations)",
        # Outside the default view, as every non-US city is - it keeps
        # fit_view's zoom pinned at 1.4525 so no existing label moves.
        "in_default_view": False,
        # EAST and slightly SOUTH of its dot, and the reason is Edmonton.
        # Their dots are 16 px apart vertically - Calgary at x 372, y 139;
        # Edmonton at x 374, y 124 - which is the east-coast cluster's problem
        # in miniature. So these two split the way those four did: Calgary
        # takes the SOUTH offset and Edmonton will take the NORTH one, both
        # running east into the space Vancouver's label vacated when it moved
        # west on 2026-09-21. That move was made for exactly this.
        "label_offset": ("start", 12, 9),
    },
]

# THE INITIAL VIEW FRAMES ONLY THE CITIES FLAGGED FOR IT, NOT ALL OF THEM.
#
# The owner's decision (2026-09-21), and it retires a problem rather than
# tuning it. `fit_view` used to frame every entry, which meant each new city
# outside the existing box re-fitted the whole map: adding Vancouver alone took
# the longitude span from 57.55 to 58.31 degrees, dropped the zoom from 1.4525
# to 1.4336, and pulled the east-coast cluster tighter - New York to
# Philadelphia from 5.95 px to 5.87 px. Every label offset in this file was
# measured at the old zoom, so every non-US city would have meant re-measuring
# all of them, and a European city would have forced continent-specific maps
# and a layer of extra pages.
#
# Framing the default view on the well-distributed US set fixes the zoom at
# 1.4525 for good. Cities outside it are still fully on the map, found by
# zooming out and panning, and every one of them is in the text-link list
# beneath it - which is the real navigation guarantee, not the view.
#
# A city is in the default view unless it says otherwise, so US cities need no
# flag and nothing here changed for them.
#
# NOTE FOR scripts/scaffold_city.py: its insertion anchor is the closing "]"
# of CITIES, and adding this block below the list once caused it to splice a
# new city INTO this comprehension and break the module. If a scaffold run
# produces a SyntaxError here, that is why - move the entry up into CITIES by
# hand rather than reverting.
IN_DEFAULT_VIEW = [c for c in CITIES if c.get("in_default_view", True)]
