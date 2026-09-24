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
        "region": "United States West",
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
        "region": "United States West",
        "lat": 37.7509,
        "lon": -122.4414,
        "page": "pages/2_San_Francisco_Heatmap.py",
        "blurb": "Muni Metro (J Church, K Ingleside, L Taraval, M Ocean View, N Judah, T Third Street)",
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Los Angeles",
        "region": "United States West",
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
        "region": "United States East",
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
        "region": "United States East",
        "lat": 40.7128,
        "lon": -74.006,
        "page": "pages/5_New_York_Heatmap.py",
        "blurb": "Subway trunk lines (8 Av, 6 Av, 7 Av, Lexington Av, Broadway, "
                 "Nassau St, Flushing, Crosstown, 14 St-Canarsie) and the Staten "
                 "Island Railway",
        # East of its dot, second from the top of the eastern column.
        #
        # dx IS 24 AND NOT 14, because at 14 this pill ERASED BOSTON'S MARKER -
        # deploy-verify measured 0 teal pixels for Boston in the landing view at
        # 1200 and 768 px, against 32-65 for every other city. Boston's dot
        # lands at x 627.0 while this pill spanned x 624.5-695.9 at y
        # 180.4-198.4, so the dot sat inside an opaque pill drawn above it. Same
        # defect as Guadalajara's, one view over, and it went unseen because the
        # check of the day scored pills against pills and not against markers.
        #
        # East rather than down: the eastern column's vertical slots are 16 px
        # apart and +8 is Philadelphia's, so any dy that clears Boston's dot
        # walks into another name. dx 22 is the arithmetic minimum (Boston's dot
        # centre plus its 5 px radius); 24 leaves 2.5 px. It costs 10 px more
        # clipping at 375 px - 27% of the pill against 13% - which is the same
        # accepted trade-off as Washington D.C.'s 39% two rows below.
        "label_offset": ("start", 24, -8),
    },
    {
        "name": "Philadelphia",
        "region": "United States East",
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
        "region": "United States East",
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
        "region": "United States East",
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
        "region": "United States East",
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
        "region": "Canada West",
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
        "region": "Canada East",
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
        "region": "Canada West",
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
    {
        "name": "Edmonton",
        "region": "Canada West",
        "lat": 53.5444,
        "lon": -113.4909,
        "page": "pages/13_Edmonton_Heatmap.py",
        "blurb": "ETS LRT (Capital, Metro and Valley Lines)",
        # OUTSIDE THE DEFAULT VIEW, like the other three Canadian cities. See
        # IN_DEFAULT_VIEW below.
        "in_default_view": False,
        # EAST of its dot, like Calgary's. Edmonton sits almost directly NORTH
        # of Calgary - 2.5 degrees of latitude, 0.6 of longitude - so the pair
        # is separated vertically rather than horizontally and both labels can
        # run east without meeting. Nudged slightly ABOVE the dot (negative y)
        # so the gap to Calgary's label, which sits below its own dot, is the
        # sum of the two offsets rather than the difference.
        "label_offset": ("start", 12, -6),
    },
    {
        "name": "Toronto",
        "region": "Canada East",
        "lat": 43.6532,
        "lon": -79.3832,
        "page": "pages/14_Toronto_Heatmap.py",
        "blurb": "TTC (Lines 1, 2 and 4 subway; Lines 5 and 6 LRT)",
        # OUTSIDE THE DEFAULT VIEW, like the other Canadian cities. Toronto is
        # the closest of the four to the framed region - its longitude sits
        # inside the US span and its latitude only just north of Boston's - so
        # its dot lands near the frame's top edge rather than off the map.
        "in_default_view": False,
        # EAST of its dot and slightly ABOVE, which is the band Chicago's label
        # was moved south to free on 2026-09-21 - see the Chicago entry, which
        # recorded Toronto's dot at x 506.6, y 182.0 before this city existed.
        # Running east keeps it clear of Boston and New York, which sit east of
        # their own dots further south.
        # ABOVE and WEST of its dot. Its pill overlapped "Boston" by 30x12 px
        # (measured from rendered pixels) and covered Montréal's marker; both
        # went unnoticed because nothing checked either. ("end", 0, -16) clears
        # Boston, clears Montréal's dot, and keeps Toronto's own dot visible.
        "label_offset": ("end", 0, -16),
    },
    {
        "name": "Mexico City",
        "lat": 19.4326,
        "lon": -99.1332,
        "page": "pages/15_Mexico_City_Heatmap.py",
        "blurb": "Metro CDMX (Líneas 1–9, A, B and 12) and the STE Tren Ligero",
        "region": "Mexico",
        # Outside the United States frame, like every Canadian city - see
        # IN_DEFAULT_VIEW below. Mexico's centre sits 14.02 degrees SOUTH of the
        # US centre and 1.41 degrees west, almost an exact mirror of Canada's
        # 14.53 north and 1.49 east, so the switcher moves the view vertically
        # and the pinned zoom is untouched.
        "in_default_view": False,
        # SOUTH of its dot, AND THIS KEY MUST EXIST AT ALL. Omitting it took the
        # whole Overview page down from 2026-09-22 until deploy-verify caught it:
        # pd.DataFrame fills a key some entries omit with float('nan'), the
        # offset resolver tested `v is None`, and `tuple(nan)` raised
        # TypeError on every load - map, city list, caption and site notices all
        # replaced by a traceback. Overview.py is scalar-safe now, but every
        # city still declares one, because fifteen cities happening to have one
        # is what hid the bug.
        #
        # Above its dot (the old default) this pill measured x338-426 y264-281
        # and collided with BOTH "Los Angeles" (13x1 px) and
        # "Guadalajara (Regional)" (19x0 px). At dy +22 it sits y308-325 and
        # clears both - including the Los Angeles overlap, which predated this
        # city and was reported as out of scope.
        "label_offset": ("middle", 0, 22),
    },
    {
        # REGIONAL, like Miami and Vancouver: SITEUR's own description has
        # Línea 3 connecting Zapopan, Guadalajara and Tlaquepaque, and Línea 4
        # connecting Tlajomulco de Zúñiga, Tlaquepaque and Guadalajara. The
        # display name carries "(Regional)"; the page file keeps the plain city
        # name, as Miami's does.
        "name": "Guadalajara (Regional)",
        "lat": 20.6597,
        "lon": -103.3496,
        "page": "pages/16_Guadalajara_Heatmap.py",
        "blurb": "Tren Ligero (Líneas 1–4, across four municipios)",
        "region": "Mexico",
        # Outside the United States frame, like Mexico City and every Canadian
        # city - see IN_DEFAULT_VIEW below.
        "in_default_view": False,
        # West of its dot, ending AT the point rather than short of it. The
        # first attempt, ("end", -14, 0), was measured by deploy-verify from
        # real pixels as overlapping "Mexico City" by 19x0 px and, at 375 px,
        # clipped 15 px by the west canvas edge - rendering as
        # "uadalajara (Regional)". Dropping dx to 0 moves the pill 14 px east:
        # it clears Mexico City outright and its west edge lands on-canvas at
        # every width. Chosen against a projection model that reproduces four
        # pixel-measured pills to within 2 px, not by eye.
        #
        # ABOVE its dot, and the dy is the whole point. ("end", 12, 0) put the
        # pill's right edge 17 px right of the marker with dy 0 centring it
        # vertically on that marker - so the opaque pill (alpha 235) ERASED
        # Guadalajara's teal dot entirely. The owner spotted it on the rendered
        # map; no check here was looking for a label covering a marker, only
        # for labels covering each other.
        #
        # The three constraints conflict on dx alone: clearing the dot with an
        # "end" anchor needs dx <= -10, and clearing the west canvas edge at
        # 360 px needs dx >= +10. So dy has to do the work - a pill is 17 px
        # tall and a marker 5 px in radius, which needs |dy| >= 14. At
        # ("middle", 0, -16) the label sits above its dot, clears it, and also
        # clears Mexico City and Miami at every width.
        "label_offset": ("middle", 0, -16),
    },
    {
        "name": "Madrid",
        "lat": 40.4168,
        "lon": -3.7038,
        "page": "pages/17_Madrid_Heatmap.py",
        "blurb": "Metro de Madrid (Líneas 1–12 and the Ramal, 193 stations "
                 "inside the city)",
        "region": "Europe",
        # Outside the United States frame, like every non-US city - see
        # IN_DEFAULT_VIEW below. The first city here in EUROPE, which is what
        # the region model was always going to have to absorb.
        "in_default_view": False,
        # ABOVE its dot, and this key MUST EXIST AT ALL - Mexico City omitting
        # it took the whole Overview page down on 2026-09-22, because
        # pd.DataFrame fills a missing key with float('nan') and `nan is None`
        # is False. Overview.py is scalar-safe now; every city still declares
        # one, because fifteen cities happening to have one is what hid that.
        #
        # Madrid is alone in its region and far from every other city on the
        # map, so nothing constrains this but the canvas edge. Measured by
        # scripts/check_macro_labels.py across six regions and three widths.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Barcelona",
        "lat": 41.3874,
        "lon": 2.1686,
        "page": "pages/18_Barcelona_Heatmap.py",
        "blurb": "Metro de Barcelona (L1–L12 across TMB and FGC, plus the "
                 "Montjuïc and Vallvidrera funiculars, 112 stations inside "
                 "the city)",
        # Outside the United States frame, like every non-US city. OMITTING
        # THIS IS NOT NEUTRAL: IN_DEFAULT_VIEW defaults a missing key to TRUE,
        # so Barcelona silently joined the landing frame and stretched it from
        # California to Catalonia. The symptom named innocent cities -
        # check_deploy_imports reported Calgary/Toronto and Guadalajara/Los
        # Angeles colliding and three labels clipped off the west edge, because
        # everything had been compressed to fit an Atlantic-wide view.
        "in_default_view": False,
        # Spain's two cities sit 500 km apart but frame close together, and
        # Madrid's label goes ABOVE its marker - so Barcelona's goes to the
        # RIGHT rather than stacking into it. Omitting this key is not a
        # neutral default: pd.DataFrame fills a missing key with float('nan'),
        # and nan is truthy, which is what took the Overview down on
        # 2026-09-22.
        "label_offset": ("start", 14, 6),
        "region": "Europe",
    },
    {
        "name": "Dublin",
        "lat": 53.3498,
        "lon": -6.2603,
        "page": "pages/19_Dublin_Heatmap.py",
        "blurb": "Luas Red and Green Lines, and the DART",
        "region": "Europe",
        "in_default_view": False,
        # STARTING VALUE, NOT A MEASURED ONE. Offsets are PIXELS at a
        # pinned zoom. Run `python scripts/check_macro_labels.py`,
        # which scores every city in every region at three widths -
        # and which will first demand this city's label width be
        # MEASURED in a real browser with Space Grotesk loaded, since
        # it refuses a guessed one.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Milan",
        "lat": 45.4642,
        "lon": 9.19,
        "page": "pages/20_Milan_Heatmap.py",
        "blurb": "Metro M1-M5 (rossa, verde, gialla, blu, lilla)",
        "region": "Europe",
        "in_default_view": False,
        # STARTING VALUE, NOT A MEASURED ONE. Offsets are PIXELS at a
        # pinned zoom. Run `python scripts/check_macro_labels.py`,
        # which scores every city in every region at three widths -
        # and which will first demand this city's label width be
        # MEASURED in a real browser with Space Grotesk loaded, since
        # it refuses a guessed one.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Paris",
        "lat": 48.8566,
        "lon": 2.3522,
        "page": "pages/21_Paris_Heatmap.py",
        "blurb": "Métro (Lignes 1–14, plus 3bis and 7bis)",
        "region": "Europe",
        "in_default_view": False,
        # TURNED BELOW THE DOT 2026-09-24, when Oslo joined Europe, and the
        # check chose it. Oslo is far enough north that the Europe frame
        # zoomed out, which pressed the French cities together: at the old
        # ("middle", 0, -22) Paris's pill covered Lille (Regional)'s marker
        # and overlapped Rennes' label at all three widths (6 problems).
        # Scored alternatives: below, right ("start", 12, 4) and upper-right
        # ("start", 10, -14) all 0; left ("end", -12, 4) covered Rennes.
        # Below keeps it clear of both neighbours that crowd it - Lille to
        # the north, Rennes to the west.
        "label_offset": ("middle", 0, 22),
    },
    {
        "name": "Marseille",
        "lat": 43.2965,
        "lon": 5.3698,
        "page": "pages/22_Marseille_Heatmap.py",
        "blurb": "RTM Métro 1–2 and Tramway 1–3",
        "region": "Europe",
        "in_default_view": False,
        # BELOW THE MARKER, not above, and the check chose it rather than
        # taste. Marseille's width was measured at 60.3 px in a real browser
        # with Space Grotesk loaded (five known cities reproduced the table
        # exactly, which is what proves the font loaded). At the scaffold's
        # default ("middle", 0, -22) it collided TWICE in the United States
        # view at 1200 px - Madrid x Marseille 28.4 x 2.9 px and
        # Milan x Marseille 43.4 x 6.2 px - because every European city here
        # points its label straight up and Marseille sits between them.
        #
        # The same offset every other European city uses, and deliberately so
        # after two attempts to tune it away. Marseille is boxed in - Paris
        # north, Milan north-east, Madrid west, Barcelona south-west, and
        # Barcelona's own label points up into Marseille's space - so moving
        # it above collided with Madrid and Milan, and moving it below then
        # collided with Barcelona at 38.6 x 12.1 px.
        #
        # OWNER'S CALL 2026-09-23: the two remaining overlaps happen only in
        # the UNITED STATES view, where Europe is a corner cluster, and chasing
        # them is not worth it as coverage goes global - a parent region labels
        # every city on earth, so this class of collision grows with the map
        # rather than with any defect. Recorded in check_macro_labels.py's
        # ACCEPTED_OVERLAPS with the measured numbers, which is the mechanism
        # built for exactly this and which still fails if the geometry moves.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Toulouse",
        "lat": 43.6047,
        "lon": 1.4442,
        "page": "pages/23_Toulouse_Heatmap.py",
        "blurb": "Tisséo Métro A–B, Tramway T1 and the Téléo cable car",
        "region": "Europe",
        "in_default_view": False,
        # ANCHORED "end" SO THE LABEL RUNS WEST, and the check chose it.
        # Toulouse's width was measured at 60.4 px in a real browser with
        # Space Grotesk loaded (six cities already in the table reproduced
        # exactly, which is what proves the font loaded rather than a
        # fallback).
        #
        # At the scaffold's default ("middle", 0, -22) it collided with
        # MARSEILLE at 19.5 x 12.5 px in the Europe view at all three widths.
        # The cause is geometric rather than cosmetic: Toulouse is 43.60 N and
        # Marseille 43.30 N, so at this scale their labels sit at the same
        # HEIGHT, and both pointed straight up with the same offset.
        #
        # Toulouse is WEST of Marseille (1.44 E against 5.37 E), so running
        # its label leftward separates them along the axis they actually
        # differ on instead of fighting for vertical space. Moving it DOWN was
        # the other option and was rejected: Barcelona sits south at 41.39 N
        # with its own label pointing up, which is the collision Marseille's
        # comment records hitting at 38.6 x 12.1 px.
        "label_offset": ("end", -8, -22),
    },
    {
        "name": "Lille (Regional)",
        "lat": 50.6292,
        "lon": 3.0573,
        "page": "pages/24_Lille_Heatmap.py",
        "blurb": "ilévia Métro 1–2 and Tram R–T, across eleven communes",
        "region": "Europe",
        "in_default_view": False,
        # THE SCAFFOLD'S DEFAULT, KEPT BECAUSE IT SCORED CLEAN - not left
        # unexamined. Width measured at 99.7 px in a real browser with Space
        # Grotesk loaded (five cities already in the table reproduced
        # exactly), then check_macro_labels.py scored every region at three
        # widths: PROBLEMS 0. Lille sat north of every other European city
        # here, so a label pointing up had nothing to meet - unlike
        # Toulouse, whose default collided with Marseille at the same
        # latitude and had to be turned west.
        #
        # TURNED UP AND WEST 2026-09-24, when Amsterdam arrived north of it:
        # the pill above the dot covered Amsterdam's marker at 375, 768 and
        # 1200. Scored alternatives: due west met Rennes (59.7 x 2.6 px),
        # below covered Paris's marker; up-and-west scores PROBLEMS 0 across
        # 7 regions x 3 widths.
        "label_offset": ("end", -10, -14),
    },
    {
        "name": "Rennes",
        "lat": 48.1113,
        "lon": -1.68,
        "page": "pages/25_Rennes_Heatmap.py",
        "blurb": "STAR Métro a and b",
        "region": "Europe",
        "in_default_view": False,
        # THE SCAFFOLD'S DEFAULT, KEPT BECAUSE IT SCORED CLEAN. Width
        # measured at 49.7 px in the deployed app's own frame with Space
        # Grotesk loaded (six cities already in the table reproduced
        # exactly), then check_macro_labels.py scored every region at three
        # widths: PROBLEMS 0, and Rennes is not among the labels clipped at
        # 375 px. It sits alone in the west of France, 3.4 degrees of
        # longitude from Paris, so a label pointing up has nothing to meet.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Oslo",
        "lat": 59.9139,
        "lon": 10.7522,
        "page": "pages/26_Oslo_Heatmap.py",
        "blurb": "Ruter T-bane 1–5 and Trikk 12, 13, 15, 17, 18, 19",
        "region": "Europe",
        "in_default_view": False,
        # TURNED BELOW THE DOT, and not by check_macro_labels.py. Width 29.0
        # px, measured in the deployed app's own frame with six table entries
        # reproducing exactly. The scaffold's ("middle", 0, -22) scored clean
        # against every label and dot - but Oslo is the northernmost city in
        # the Europe frame, and deploy-verify (2026-09-24) found its name
        # ENTIRELY under the macro map's "Light mode" button at 375 px (label
        # x 242-281, y 18-36; button x 180-291, y 10-42). The checker does not
        # model that button, so its PROBLEMS 0 could not see this. Below the
        # dot the label clears the button's bottom edge. Oslo also changed
        # the frame itself - see Paris's entry.
        "label_offset": ("middle", 0, 22),
    },
    {
        "name": "Copenhagen",
        "lat": 55.6761,
        "lon": 12.5683,
        "page": "pages/27_Copenhagen_Heatmap.py",
        "blurb": "Metro M1–M4 and S-tog A, B, Bx, C, E, F, H",
        "region": "Europe",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured at 85.5 px in the app's own document (2026-09-24), and
        # check_macro_labels.py passes every region at 375, 768 and 1200 with
        # PROBLEMS 0 - Copenhagen sits mid-frame in Europe, clear of Oslo to
        # the north and of the map's controls.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Prague",
        "lat": 50.0755,
        "lon": 14.4378,
        "page": "pages/28_Prague_Heatmap.py",
        "blurb": "Metro A, B and C",
        "region": "Europe",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured at 47.3 px in the app's own document (2026-09-24), and
        # check_macro_labels.py passes every region at 375, 768 and 1200 with
        # PROBLEMS 0.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Amsterdam",
        "lat": 52.3728,
        "lon": 4.8936,
        "page": "pages/29_Amsterdam_Heatmap.py",
        "blurb": "Metro 50–54 and 16 tram lines",
        "region": "Europe",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured at 76.5 px in the app's own document with nine entries
        # reproduced, and check_macro_labels.py passes every region at 375,
        # 768 and 1200 with PROBLEMS 0 - after Lille's label was turned up
        # and west, since Lille's pill had covered this marker.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "Rome",
        "lat": 41.8933,
        "lon": 12.4829,
        "page": "pages/30_Rome_Heatmap.py",
        "blurb": "Metro A, B, B1, C and Roma–Viterbo",
        "region": "Europe",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured at 37.5 px in the app's own document with nine entries
        # reproduced, and check_macro_labels.py passes every region at 375,
        # 768 and 1200 with PROBLEMS 0 - re-scored after merging with
        # Amsterdam, built on a separate branch the same night.
        "label_offset": ("middle", 0, -22),
    },
    {
        "name": "São Paulo",
        "lat": -23.5505,
        "lon": -46.6333,
        "page": "pages/31_Sao_Paulo_Heatmap.py",
        "blurb": "Metrô Linhas 1–5 and 15, CPTM Linha 9",
        "region": "South America",
        "in_default_view": False,
        # LEFT of the dot, not above: Santos's dot is 6 px away at South
        # America's zoom (3.04) and Rio's 40 px east, so the three names
        # go three ways - São Paulo west, Rio east, Santos below. Scored: the
        # label width was measured in the app's own document with eleven
        # entries reproduced, and check_macro_labels.py passes every region at
        # 375, 768 and 1200 with PROBLEMS 0.
        "label_offset": ("end", -11, 0),
    },
    {
        "name": "Rio de Janeiro",
        "lat": -22.9068,
        "lon": -43.1729,
        "page": "pages/32_Rio_de_Janeiro_Heatmap.py",
        "blurb": "MetrôRio 1, 2 and 4, VLT Carioca, SuperVia Deodoro and Saracuruna",
        "region": "South America",
        "in_default_view": False,
        # RIGHT of the dot, clear of São Paulo's name 40 px west. Scored: the
        # label width was measured in the app's own document with eleven
        # entries reproduced, and check_macro_labels.py passes every region at
        # 375, 768 and 1200 with PROBLEMS 0.
        "label_offset": ("start", 11, 0),
    },
    {
        "name": "Belo Horizonte",
        "lat": -19.9167,
        "lon": -43.9345,
        "page": "pages/33_Belo_Horizonte_Heatmap.py",
        "blurb": "Metrô BH Linhas 1 and 2",
        "region": "South America",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        "label_offset": ('middle', 0, -22),
    },
    {
        "name": "Brasília",
        "lat": -15.7939,
        "lon": -47.8828,
        "page": "pages/34_Brasilia_Heatmap.py",
        "blurb": "Metrô-DF Linha Verde and Linha Laranja",
        "region": "South America",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        "label_offset": ('middle', 0, -22),
    },
    {
        "name": "Salvador",
        "lat": -12.9714,
        "lon": -38.5014,
        "page": "pages/35_Salvador_Heatmap.py",
        "blurb": "Metrô Linhas 1 and 2",
        "region": "South America",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        "label_offset": ('middle', 0, -22),
    },
    {
        "name": "Fortaleza (Regional)",
        "lat": -3.7319,
        "lon": -38.5267,
        "page": "pages/36_Fortaleza_Heatmap.py",
        "blurb": "Metrofor Linha Sul",
        "region": "South America",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        "label_offset": ('middle', 0, -22),
    },
    {
        "name": "Porto Alegre (Regional)",
        "lat": -30.0346,
        "lon": -51.2177,
        "page": "pages/37_Porto_Alegre_Heatmap.py",
        "blurb": "Trensurb Linha 1",
        "region": "South America",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        # 7.5 px (5%) clipped at the west edge at phone width -
        # reported, not failed, the class Guadalajara's 6% is in.
        "label_offset": ('middle', 0, -22),
    },
    {
        "name": "Recife (Regional)",
        "lat": -8.0476,
        "lon": -34.877,
        "page": "pages/38_Recife_Heatmap.py",
        "blurb": "Metrô do Recife Linhas Centro and Sul",
        "region": "South America",
        "in_default_view": False,
        # Above the dot, and SCORED rather than assumed: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        "label_offset": ('middle', 0, -22),
    },
    {
        "name": "Santos (Regional)",
        "lat": -23.9608,
        "lon": -46.3336,
        "page": "pages/39_Santos_Heatmap.py",
        "blurb": "VLT Linhas 1 and 2",
        "region": "South America",
        "in_default_view": False,
        # BELOW the dot: São Paulo's dot sits 6 px away, so its name runs
        # west and this one drops under both. Scored: the label width was
        # measured in the app's own document with eleven entries reproduced,
        # and check_macro_labels.py passes every region at 375, 768 and 1200
        # with PROBLEMS 0.
        "label_offset": ('middle', 0, 22),
    },
    {
        "name": "Rotterdam",
        "lat": 51.9225,
        "lon": 4.4792,
        "page": "pages/40_Rotterdam_Heatmap.py",
        "blurb": "RET metro A–E and 9 tram lines",
        "region": "Europe",
        "in_default_view": False,
        # UP AND LEFT of the dot, the only placement that scores: Amsterdam's
        # name sits above, Lille's to the south-west and Prague's pill to the
        # east. Width 70.7 px measured in the app's own document, thirteen
        # entries reproduced; check_macro_labels.py passes every region at
        # 375, 768 and 1200 with PROBLEMS 0. TIGHT: dy -11 touches Lille's pill
        # and -13 Amsterdam's (1-2 px), so the next European city near here
        # re-scores this one first.
        "label_offset": ("end", -9, -12),
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

# --- REGIONS -----------------------------------------------------------------
#
# The macro map opens on ONE region and offers the others, rather than fitting
# the whole world. That is the owner's decision of 2026-09-21, recorded in
# docs/scaling_thresholds.md under "~12-15 cities": once the map spans
# continents a single fitted view is unreadable however the markers are drawn,
# so the answer is to stop trying to fit everything at once.
#
# THE SWITCHER RE-CENTRES AND DOES NOT RE-ZOOM, and that is the whole reason it
# is safe to add. Every `label_offset` above is in PIXELS, measured at the zoom
# `fit_view` produces for the United States set (1.4525). Pixel distance between
# two cities depends on the ZOOM alone, not on where the view is centred - so
# re-centring preserves every measured offset exactly, while re-fitting per
# region would change the zoom and invalidate all of them at once.
#
# A region whose cities sit much closer together than a continent may eventually
# want its own zoom; `zoom` below exists for that and is None everywhere today,
# meaning "keep the pinned one". Setting it on a region means re-measuring that
# region's label offsets, which is the cost this design defers rather than
# removes.
DEFAULT_REGION = "United States"

# Order is display order in the switcher. A new country appends here.
# CANADA IS SPLIT WEST/EAST, and the reason is geographic rather than
# political. Vancouver and Montréal are ~3,300 km apart - wider than the
# contiguous United States - so a single "Canada" view centred between them put
# every city near an edge with an empty prairie in the middle, which is the
# "default silently hides most of the site" failure docs/scaling_thresholds.md
# warns about. West is Vancouver, Calgary and Edmonton; East is Toronto and
# Montréal. Owner's decision 2026-09-22.
#
# This is the first region that is not a country, and it sets the precedent:
# a region is whatever groups cities into ONE readable view. Expect the same
# question for the United States eventually, and for any country with a
# comparable span.
#
# THE UNITED STATES IS SPLIT TOO, and it is a COMPOSITE rather than a third
# tag. Owner's decision 2026-09-22: West is California (San Diego, San
# Francisco, Los Angeles, and Seattle when it is built), East is Chicago and
# everything from Miami to Boston. But splitting it alone would have removed
# the landing view that shows the whole country - every region is fitted to its
# own cities now, so whatever a visitor lands on is all they see - and six of
# sixteen cities is a thin first impression for a portfolio.
#
# So "United States" survives as a region whose cities are the union of the two
# halves. A city still carries exactly ONE tag; a composite is resolved at
# lookup. That keeps the landing view byte-identical to the one this map has
# always had, because fitting all nine US cities is what fit_view was already
# doing.
REGION_MEMBERS = {
    "United States": ("United States West", "United States East"),
}

# Display order in the switcher, parent before its halves so a reader meets the
# familiar view first. A new country appends here; a new composite adds a line
# to REGION_MEMBERS as well.
REGION_ORDER = [
    "United States",
    "United States West",
    "United States East",
    "Canada West",
    "Canada East",
    "Mexico",
    # EUROPE IS ONE REGION, NOT ONE PER COUNTRY, and it was briefly the other
    # way. Spain arrived 2026-09-22 with Madrid as the first region outside
    # North America; Ireland and Italy followed the same day with Dublin and
    # Milan, and three regions holding four cities made the shape of the
    # problem obvious - the list would have grown by one entry per country
    # while the map it indexes stayed the same size. Collapsed on the owner's
    # decision the same day, before France's six cities could make it five.
    #
    # NOTE WHAT THIS IS NOT. North America is split (United States West/East,
    # Canada West/East) because those countries are 3,300 km wide and a single
    # frame shows a continent rather than a city. Europe's four cities span
    # Dublin to Milan - about 1,700 km - and frame together at a zoom where
    # each is still distinguishable, so the split that Canada needs, Europe
    # does not. Revisit it when a city appears far enough east or south to
    # force the frame open; that is a measurement (`check_macro_labels.py`
    # scores every city in every region at three widths), not a judgement.
    "Europe",
    # SOUTH AMERICA, not "Brazil" - the owner's call of 2026-09-24, so a
    # further country on the continent joins this view rather than adding one.
    # Brazil alone spans Porto Alegre to Fortaleza, about 3,200 km: the width
    # Canada was split for. It is one region because every city frames at a
    # zoom where each is distinguishable except São Paulo and Santos, 55 km
    # apart, whose labels are placed apart instead (scored by
    # check_macro_labels.py like every other region).
    "South America",
]

# The regions a city may actually be TAGGED with: everything that is not a
# composite. Tagging a city "United States" is now an error rather than a
# shorthand, and the validator below says so.
LEAF_REGIONS = [r for r in REGION_ORDER if r not in REGION_MEMBERS]


def cities_in(region):
    """Cities in a region, resolving a composite to its members.

    Order follows CITIES, not the member list, so the composite reads in
    implementation order like every other region.
    """
    members = REGION_MEMBERS.get(region, (region,))
    return [c for c in CITIES if c.get("region") in members]


REGIONS = [
    {"name": name, "cities": cities_in(name), "zoom": None}
    for name in REGION_ORDER
    if cities_in(name)
]


def elsewhere_counts(region):
    """(name, count) for the regions a given region does NOT cover.

    LEAVES ONLY, AND THAT IS THE WHOLE POINT. `REGIONS` holds composites and
    their halves, which overlap, so "every region except this one" counts the
    same city twice. Selecting "United States" described its own nine cities
    as "3 in United States West, 6 in United States East" *elsewhere*, on the
    default view of the front page; selecting a leaf listed the composite that
    contains it. Shipped with the Europe macro-region change and found on the
    live site 2026-09-22.

    The invariant a caller can rely on, and `scripts/check_macro_labels.py`
    asserts for every region: len(cities_in(region)) + sum of these counts
    == len(CITIES).
    """
    covered = set(REGION_MEMBERS.get(region, (region,)))
    return [(n, len(cities_in(n))) for n in REGION_ORDER
            if n in LEAF_REGIONS and n not in covered and cities_in(n)]

_untagged = [c["name"] for c in CITIES if c.get("region") not in LEAF_REGIONS]
if _untagged:
    raise ValueError(
        f"cities.py: {_untagged} have no region, or one not in LEAF_REGIONS "
        f"({LEAF_REGIONS}). A composite like 'United States' is a view, "
        f"not a tag - tag the half the city is in. "
        f"Every city needs one - the macro map opens on a region and a city "
        f"without one would be reachable only from the text list."
    )
