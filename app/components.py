"""Small pieces of UI shared across pages.

Streamlit's multipage app has no shared layout/header mechanism of its own -
each page is its own top-to-bottom script - so anything meant to appear
identically on every page lives here once and gets called from each page,
rather than duplicated per page.
"""

import sys
from pathlib import Path

import streamlit as st

from cities import MAP_ONLY_NAV, SWITCHER_ORDER

sys.path.insert(0, str(Path(__file__).parent.parent))
# pipeline/theme.py imports nothing, so it is safe for the lean deploy venv
# (streamlit + pandas only) - the same rule the city pages' config imports
# follow. It is the single source for every chrome colour, shared with the city
# maps' own CSS so a reskin cannot leave the macro map on the old palette.
from pipeline.theme import AMBIENT_THEME_JS, DARK, LIGHT, rgba  # noqa: E402
from pipeline.tokyo import credits as tokyo_credits  # noqa: E402 - pure data, no imports

OVERVIEW_PAGE = "Overview.py"


def render_city_nav(current: str):
    """A row at the top of a city page: a link back to the macro map, then
    every mapped city (the current one shown as plain bold text). Lets a
    visitor hop city to city without returning to the map each time.
    `current` must match a name in cities.CITIES.

    In the map-only pilot (cities.MAP_ONLY_NAV) there is no visible switcher.
    The links are still rendered, hidden (see set_base_font): one to the Overview
    and one per city, because the city map's own "Global View" button and city
    menu navigate by clicking them (and read the city names from them)."""
    if MAP_ONLY_NAV:
        with st.container(key="map-only-nav"):
            # Keep this text: the maps' JS finds this link, and leaves it out of
            # the Cities menu, by "All cities" (pipeline/map_common.py).
            st.page_link(OVERVIEW_PAGE, label="All cities")
            for city in SWITCHER_ORDER:   # grouped by country; see cities.py
                st.page_link(city["page"], label=city["name"])
        return
    # A horizontal container sizes each item to its content and wraps onto a
    # second line when the row is too narrow; fixed-width columns clipped the
    # longer city names once a fourth city was added.
    with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
        st.page_link(OVERVIEW_PAGE, label="← Global View")
        for city in SWITCHER_ORDER:
            if city["name"] == current:
                st.markdown(f"**{city['name']}**")
            else:
                st.page_link(city["page"], label=city["name"])


MACRO_THEME_KEY = "expanded-heatmap-theme"   # the same key the city maps use

_MACRO_THEME_CSS = """
<style>
[data-testid="stDeckGlJsonChart"] { position: relative; }
#macro-theme-toggle {
    position: absolute; top: 10px; right: 52px; z-index: 20;
    font: 600 13px sans-serif; padding: 6px 12px; cursor: pointer;
    background: @@LIGHT_SURFACE@@; color: @@LIGHT_TEXT@@;
    border: 1px solid @@LIGHT_BORDER@@;
    /* The only colour here deliberately left outside pipeline/theme.py: a
       black drop shadow is theme-agnostic, and it simply stops mattering on a
       dark surface rather than looking wrong. Same value in map_common.py. */
    border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
#macro-theme-toggle:focus-visible { outline: 2px solid @@LIGHT_ACCENT@@; outline-offset: 2px; }
body.dark-base #macro-theme-toggle { background: @@DARK_SURFACE@@; color: @@DARK_TEXT@@;
    border-color: @@DARK_BORDER@@; }
body.dark-base #macro-theme-toggle:hover { background: @@DARK_SURFACE_HOVER@@; }
/* Only the basemap canvas is filtered; the markers and labels are a separate
   canvas, so they keep their colours. Same filter as the city maps. */
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-canvas {
    filter: invert(1) hue-rotate(180deg) brightness(0.85) contrast(0.9) saturate(0.7); }
@@CONTROLS@@
</style>
"""

# JS: put a toggle button on the map's frame, keep the choice in localStorage
# (shared with the city maps: the embedded map iframes and this page share an
# origin) and toggle a `dark-base` class on the page's <body>. The button is
# re-added by a MutationObserver if Streamlit re-renders the chart; if the
# chart container is not found there is simply no button and the map stays light.
_MACRO_THEME_JS = """
<!-- This frame is script-only and exists to run JS, not to be seen. st.iframe
     rejects height=0, so it renders 1 px tall - and that 1 px WAS VISIBLE on
     the deployed site (reported 2026-09-21): a faint dash above the page
     title, because a document with no background paints the browser's default
     canvas colour, white, and one row of white on a dark page reads as a mark.

     Fixed here rather than with CSS in the parent page. Streamlit gives this
     iframe no `height` attribute and no inline style - its 1 px comes from a
     hashed emotion class that changes between versions - so any selector
     written against the parent DOM would be version-fragile, and `display:
     none` on an iframe risks its script never running, which would cost the
     theme button. Making the frame's own canvas transparent is
     version-independent and leaves the script untouched. -->
<style>html, body { margin: 0; padding: 0; background: transparent; }</style>
<script>
(function () {
    var KEY = '@@KEY@@';
    var doc = window.parent.document;
    function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
    function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
    function label(btn, dark) {
        btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
        btn.textContent = dark ? '\\u2600 Light mode' : '\\u263E Dark mode';
    }
    function apply(dark) {
        doc.body.classList.toggle('dark-base', dark);
        var b = doc.getElementById('macro-theme-toggle');
        if (b) label(b, dark);
    }
    function ensure() {
        var host = doc.querySelector('[data-testid="stDeckGlJsonChart"]');
        if (!host || doc.getElementById('macro-theme-toggle')) return;
        var b = doc.createElement('button');
        b.id = 'macro-theme-toggle'; b.type = 'button';
        b.addEventListener('click', function () {
            var dark = !doc.body.classList.contains('dark-base');
            apply(dark); save(dark ? 'dark' : 'light');
        });
        host.appendChild(b);
        label(b, doc.body.classList.contains('dark-base'));
    }
@@AMBIENT_JS@@
    // A remembered click wins; otherwise follow the page this map sits on, so
    // the macro map matches the Streamlit theme the visitor chose instead of
    // opening light on a dark page. `ambientPrefersDark` reads window.parent,
    // which from this 1px script frame is that page.
    var choice = saved();
    apply(choice === 'dark' || choice === 'light'
          ? choice === 'dark'
          : ambientPrefersDark());
    // CLAUDE.md: the OSM credit links to the OSM COPYRIGHT page. CARTO's style
    // ships it pointing at /about/; the credit is Mapbox's own element, built
    // from the style, so it is corrected here, on every re-render, rather than
    // replaced. Only the href changes - the text and the credit stay Mapbox's.
    var OSM_COPYRIGHT = 'https://www.openstreetmap.org/copyright';
    function fixCredit() {
        var links = doc.querySelectorAll('[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a');
        for (var i = 0; i < links.length; i++) {
            if (/openstreetmap[.]org/.test(links[i].href) && links[i].href !== OSM_COPYRIGHT) {
                links[i].href = OSM_COPYRIGHT;
            }
        }
    }
    ensure(); fixCredit();
    new window.parent.MutationObserver(function () { ensure(); fixCredit(); })
        .observe(doc.body, { childList: true, subtree: true });
    if (window.matchMedia) {
        var mq = window.matchMedia('(prefers-color-scheme: dark)');
        if (mq.addEventListener) {
            mq.addEventListener('change', function (e) {
                if (!saved()) apply(e.matches);
            });
        }
    }
})();
</script>
"""

# Styling for the pydeck/mapbox controls (zoom buttons, attribution).
_MACRO_CONTROLS_CSS = """
/* THE ATTRIBUTION STAYS OPEN AT EVERY WIDTH, AND THIS IS A LICENCE TERM RATHER
   THAN A STYLE CHOICE. Below ~640 px mapbox-gl adds `mapboxgl-compact` to its
   attribution control, which sets the inner text to `display: none` and leaves
   an (i) button that reveals it on tap. Measured 2026-09-22: at a 375 px
   viewport the macro map showed the button and no credit, while 768 and 1200
   showed the full text.

   That is precisely the arrangement this project has committed not to ship.
   ODbL 1.0 requires the credit to stay visible, CLAUDE.md states it must not
   sit "beneath UI, behind toggles, or off-screen", and render_site_notices()
   below already refuses an st.expander for the same reason - a required notice
   behind a toggle is not displayed. A library default is not an exemption, so
   the compact behaviour is overridden rather than accepted.

   Not scoped to `body.dark-base`: the obligation does not depend on the theme.
   The city maps are Leaflet, whose attribution control has no compact mode, so
   they need no equivalent. */
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib.mapboxgl-compact {
    min-height: 0; padding: 0 5px; border-radius: 3px; margin: 0 10px 10px 0; }
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib.mapboxgl-compact
    .mapboxgl-ctrl-attrib-inner { display: block !important; }
/* THE CREDIT MUST SIT ABOVE THE CITY DOTS, and deck.gl stacks it below them.
   deck.gl wraps the whole Mapbox basemap - its controls and credit included -
   in a `z-index: -1` layer beneath its own drawing canvas, so any dot or name
   pill could paint over "(c) OpenStreetMap contributors" wherever a city
   landed. Rotterdam's deploy check saw a dot there at 800x700 (2026-09-24);
   scripts/check_macro_attribution.mjs found the canvas above the credit at
   every point at 375, 768 and 1200 px.

   A child cannot rise out of a z-index:-1 parent, so the wrapper is flattened
   and the three layers ordered explicitly inside deck.gl's own wrapper:
   basemap (auto) < deck.gl canvas (1) < Mapbox's controls (2, their default).
   Found by the element it wraps, not by its position, so a deck.gl release
   that reorders the wrapper's children does not silently undo this. */
[data-testid="stDeckGlJsonChart"] div:has(> .mapboxgl-map) { z-index: auto !important; }
[data-testid="stDeckGlJsonChart"] #deckgl-overlay { z-index: 1; }
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-bottom-right,
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-top-right { z-index: 2; }
/* The (i) toggle itself, and the pseudo-element some versions draw it with. */
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib-button,
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib.mapboxgl-compact::after {
    display: none !important; }
/* Invert the whole zoom group (white -> near-black, dark glyph -> light); the
   glyph is the button's own background image, so it cannot be inverted alone. */
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-group { filter: invert(0.9); }
/* THE CREDIT'S OWN COLOURS, IN BOTH THEMES, ON AN OPAQUE STRIP. Until
   2026-09-24 only dark mode was styled, so in light mode the credit inherited
   the (dark-themed) page's near-white text - rgb(230,237,247) on Mapbox's
   half-white strip - and read only as its two links. The strip was also
   half-transparent, so a name pill under it showed through the text. Links use
   the TEXT colour in light mode, not the accent: the teal accent is ~3.7:1 on
   white. check_macro_attribution.mjs measures all of this at 4.5:1. */
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib { background: @@LIGHT_SURFACE@@ !important; color: @@LIGHT_MUTED@@; }
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a { color: @@LIGHT_TEXT@@; }
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib { background: @@DARK_ATTRIB_BG@@ !important; color: @@DARK_MUTED@@; }
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a { color: @@DARK_ACCENT@@; }
/* deck.gl's tooltip is an HTML overlay (class `deck-tooltip`), so unlike the
   marker and label layers it CAN be themed. pydeck writes its colours inline
   from the `tooltip` style dict, hence !important. Without this the macro
   map's tooltip stayed the light-mode green-grey while every city map's
   tooltip was slate. */
body.dark-base [data-testid="stDeckGlJsonChart"] .deck-tooltip {
    background: @@DARK_SURFACE@@ !important; color: @@DARK_TEXT@@ !important;
    border: 1px solid @@DARK_BORDER@@; border-radius: 4px; }
/* Both themes, every width: the tooltip is a panel in the map's BOTTOM-LEFT
   corner, not a box at the cursor. deck.gl anchors it right of the cursor by
   an inline transform (hence !important), and with the five-line tooltip
   (tier, storefronts, placement, data age; 2026-09-28) it ran off the map's
   right edge: 343 px wide and mostly clipped at 343 px (Osaka), 176 px clipped
   at 1200 px even under a 240 px cap (Barcelona). Its containing block is a
   zero-height box at the map's bottom-left, so `bottom: 8px` puts the panel
   inside the map there; measured inside at 1200 and 375 px (2026-09-28). */
[data-testid="stDeckGlJsonChart"] .deck-tooltip {
    transform: none !important; left: 8px !important; right: auto !important;
    top: auto !important; bottom: 8px !important;
    max-width: min(260px, calc(100vw - 48px)) !important;
    white-space: normal !important; overflow-wrap: anywhere; line-height: 1.35; }
"""


def render_macro_map_theme():
    """Dark Mode for the macro map: the toggle button on the map's frame and the
    CSS that darkens its basemap and controls. Shares its stored choice with
    the city maps (see _MACRO_THEME_JS). Call once on the Overview page."""
    css = (
        _MACRO_THEME_CSS.replace("@@CONTROLS@@", _MACRO_CONTROLS_CSS)
        .replace("@@LIGHT_SURFACE@@", LIGHT["surface"])
        .replace("@@LIGHT_TEXT@@", LIGHT["text"])
        .replace("@@LIGHT_BORDER@@", LIGHT["border"])
        .replace("@@LIGHT_ACCENT@@", LIGHT["accent"])
        .replace("@@DARK_SURFACE@@", DARK["surface"])
        .replace("@@DARK_SURFACE_HOVER@@", DARK["surface_hover"])
        .replace("@@DARK_TEXT@@", DARK["text"])
        .replace("@@DARK_BORDER@@", DARK["border"])
        .replace("@@DARK_MUTED@@", DARK["muted"])
        .replace("@@DARK_ACCENT@@", DARK["accent"])
        .replace("@@DARK_ATTRIB_BG@@", DARK["page"])   # opaque: see the credit's CSS
        .replace("@@LIGHT_MUTED@@", LIGHT["muted"])
    )
    assert "@@" not in css, "unresolved placeholder in _MACRO_THEME_CSS"
    st.markdown(css, unsafe_allow_html=True)
    # st.iframe rejects a height of 0, so the script-only frame is 1 px tall; it only
    # needs to run (same-origin access to the page is what lets it add the button).
    js = (_MACRO_THEME_JS
          .replace("@@KEY@@", MACRO_THEME_KEY)
          .replace("@@AMBIENT_JS@@", AMBIENT_THEME_JS))
    assert "@@" not in js, "unresolved placeholder in _MACRO_THEME_JS"
    st.iframe(js, height=1)


# Map-only pilot: hide Streamlit's sidebar (its page list is the other way to reach
# a city) and its expand control, and the hidden links the map's buttons click.
# Turned off by cities.MAP_ONLY_NAV = False; see docs/navigation_sidebar_and_city_links.md.
_MAP_ONLY_CSS = """
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"] { display: none !important; }
.st-key-map-only-nav { display: none; }
"""


def scroll_table(columns, rows, right=(), min_width=None):
    """Render a table that scrolls sideways inside its own box on a phone,
    instead of widening the whole page.

    A markdown table wider than the column pushes the page itself sideways at
    375 px (Tokyo's ward table, 469 px in a 343 px column, deploy-verify
    2026-09-28), and st.dataframe drew collapsed on page 91 in the lean venv
    (2026-09-23). An HTML table in an overflow box does neither, and its text
    stays in the page. `rows` are sequences of already-formatted strings;
    `right` names the columns to right-align (figures); `min_width` (px)
    keeps a wide table from squashing its columns before it scrolls. Colours
    are left to the theme, with a grey rule that reads in both.
    """
    import html

    cell = "padding:0.3rem 0.6rem;border-bottom:1px solid rgba(128,128,128,0.3);"

    def align(col):
        return "right" if col in right else "left"

    head = "".join(f'<th style="{cell}text-align:{align(c)};vertical-align:bottom">'
                   f"{html.escape(c)}</th>" for c in columns)
    body = "".join(
        "<tr>" + "".join(f'<td style="{cell}text-align:{align(c)}">{html.escape(str(v))}</td>'
                         for c, v in zip(columns, r)) + "</tr>"
        for r in rows)
    st.markdown(
        '<div style="overflow-x:auto;max-width:100%">'
        f'<table style="border-collapse:collapse;font-size:0.9rem{f";min-width:{min_width}px" if min_width else ""}">'
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>",
        unsafe_allow_html=True,
    )


def set_base_font():
    """Swaps Streamlit's default typeface for Space Grotesk on base page
    text only.

    Space Grotesk is a geometric grotesk with more character than the
    neutral defaults, chosen as a clearly deliberate typographic identity
    (paired with the teal theme in .streamlit/config.toml). Loaded via
    Google Fonts rather than a pip dependency, keeping requirements.txt
    lean.

    Scoped, not a blanket override: code stays monospace, and Streamlit's
    own icon glyphs are restored (the wildcard would otherwise turn the
    sidebar arrow into literal ligature text). If the app ever draws Altair
    charts, add a reset for chart text here too - it sits in the page's own
    DOM rather than an iframe, unlike the embedded Folium maps, which are
    already isolated from this CSS.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

        [data-testid="stAppViewContainer"] *,
        [data-testid="stSidebar"] *,
        [data-testid="stHeader"] * {
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif !important;
        }

        [data-testid="stAppViewContainer"] code,
        [data-testid="stAppViewContainer"] pre,
        [data-testid="stAppViewContainer"] kbd,
        [data-testid="stAppViewContainer"] samp,
        [data-testid="stSidebar"] code {
            font-family: "Source Code Pro", Menlo, Consolas, monospace !important;
        }

        /* Streamlit's own UI glyphs (sidebar collapse/expand arrow, etc.)
        render as ligatures in the Material Symbols icon font, not images;
        the wildcard above would break them into literal ligature-name
        text instead of the arrow icon. */
        [data-testid="stIconMaterial"] {
            font-family: "Material Symbols Rounded" !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if MAP_ONLY_NAV:
        # A separate call, not appended to the block above: that block is indented,
        # so text added after it is rendered as a Markdown code block.
        st.markdown(f"<style>{_MAP_ONLY_CSS}</style>", unsafe_allow_html=True)


# --- Site identity and the notices that publishing requires ----------------

# The public name. The repository stays `expanded-heatmap` (that is the
# directory and the git remote); this is what a reader sees. Chosen
# 2026-09-21; a standing invariant is that the project is never named after a
# city, which is why this describes the measurement instead.
SITE_NAME = "Storefronts Near Transit"

# Numbered 90/91, not 10/11: Streamlit sorts pages numerically, and city pages
# take 1..n. At nine cities the next city would be page 10 - which these two
# already occupied. Moving them to the 90s leaves 10-89 free for cities and
# keeps them last in the sidebar, which is where they belong.
ABOUT_DATA_PAGE = "pages/200_About_the_Data.py"
EXCLUSIONS_PAGE = "pages/201_What_Is_Excluded.py"
DIFFERENCES_PAGE = "pages/202_Why_the_Maps_Differ.py"

# Verbatim where verbatim is required. Each entry is (heading, text, verbatim?)
# and the sources are recorded in docs/data_sources.md, "Notices this project
# MUST display when published" - read that before editing any of these.
#
# THESE ARE OBLIGATIONS, NOT CREDITS. Chicago's terms require its paragraph
# "at the site where the software application ... can be accessed", and
# SFMTA's licence requires its sentence in derivative works, so both are
# reproduced word for word and must not be paraphrased, trimmed or summarised.
# LA Metro's and MassDOT's prescribe no wording, only that they be
# acknowledged as the provider, so those two are this project's own phrasing.
#
# A notice on one city's page is NOT enough: the requirement is site-level,
# which is why render_site_notices() is called from every page including the
# Overview.
_NOTICES = [
    ("City of Chicago",
     "This site provides applications using data that has been modified for "
     "use from its original source, www.cityofchicago.org, the official "
     "website of the City of Chicago. The City of Chicago makes no claims as "
     "to the content, accuracy, timeliness, or completeness of any of the "
     "data provided at this site. The data provided at this site is subject "
     "to change at any time. It is understood that the data provided at this "
     "site is being used at one's own risk.",
     True),
    ("San Francisco Municipal Transportation Agency",
     "Reproduced with permission granted by the City and County of San "
     "Francisco. The information has been provided by means of a "
     "nonexclusive, limited, and revocable license granted by the City and "
     "County of San Francisco.",
     True),
    ("LA Metro",
     "Rail alignment data for Los Angeles provided by LA Metro. This project "
     "claims no ownership of that data.",
     False),
    ("MassDOT / MBTA",
     "Rail alignment data for Boston provided by MassDOT/MBTA.",
     False),
    ("Chicago Transit Authority",
     "Data provided by Chicago Transit Authority.",
     False),
    # Canada, added with Vancouver (2026-09-21). All three are VERBATIM.
    #
    # The two municipal notices use each city's OWN wording and are not
    # interchangeable - Vancouver's is "Licence" with an en dash, Surrey's is
    # "License" with a hyphen. Both licences TERMINATE AUTOMATICALLY on breach
    # ("if you fail to comply with any of them, the rights granted to you
    # under this licence... will end automatically"), so these are not
    # cosmetic.
    ("City of Vancouver",
     "Contains information licensed under the Open Government "
     "Licence – Vancouver.",
     True),
    ("City of Surrey",
     "Contains information licensed under the Open Government License - "
     "City of Surrey.",
     True),
    # TransLink's Legend, required "prominently displayed" in exactly this
    # wording. THE TRAP: TransLink mandates TWO different legends and this is
    # the GTFS STATIC one. Its Open API terms mandate a different text
    # beginning "Some of the data used in this product or service...", which
    # would NOT satisfy the GTFS terms. This project uses static GTFS. See
    # docs/licenses/translink-gtfs-static-terms-of-use.txt - the other file in
    # that directory is kept only because it looks like it governs and does
    # not. One Legend covers both cities: Surrey has no rail of its own.
    # MADRID, added 2026-09-22 with the city. TWO notices from TWO licences,
    # because the premises and the rail have different owners - the same split
    # Montreal needed for the City and the STM.
    #
    # The Ayuntamiento's Condiciones generales are BINDING BY USE - "obligan a
    # cualquier persona y/o empresa que reutilice datos por el mero hecho de
    # hacer uso" - and CC BY 4.0 is not the whole instrument. Three duties land
    # in this sentence:
    #   * cite the source, in a form the conditions themselves offer:
    #     "Origen de los datos: Ayuntamiento de Madrid"
    #   * STATE THE LAST-UPDATE DATE of the documents reused, which no other
    #     notice in this list has to carry
    #   * do not indicate, insinuate or suggest that the Ayuntamiento
    #     participates in, sponsors or supports the reuse
    #
    # Marked VERBATIM because the attribution form is prescribed; the
    # transformation sentence around it is this project's own wording, the way
    # INEGI's is.
    ("Ayuntamiento de Madrid",
     "Origen de los datos: Ayuntamiento de Madrid. Business locations for "
     "Madrid are from the Censo de locales, sus actividades y terrazas de "
     "hosteleria y restauracion, as published on datos.madrid.es and "
     "last updated 22 September 2026. The data shown here has been filtered, "
     "grouped and measured by this project and not by the Ayuntamiento de "
     "Madrid: it is restricted to premises the register records as open and in "
     "retail, food service or personal services categories, grouped into three "
     "categories of this project's own, and measured by distance from Metro "
     "stations. The Ayuntamiento de Madrid does not endorse this project or "
     "its use of the data.",
     True),
    # CRTM's licence prescribes the WORDING "Powered by CRTM" and requires a
    # link to its site, which is why this is marked verbatim and why the phrase
    # is in English inside an otherwise Spanish credit - the licence says so.
    #
    # It ALSO requires citation "especificando si son datos en bruto o
    # explotados", which is a DISCLOSURE-OF-TRANSFORMATION duty rather than a
    # louder attribution - the same split as the Ville de Montreal's "ou si des
    # interpretations en ont ete tirees" and INEGI's 1(g). This project draws
    # and relabels the network, so the answer is "explotados" and a bare credit
    # would not satisfy it.
    ("CRTM (Consorcio Regional de Transportes de Madrid)",
     # Amended 2026-09-27 for Metro Ligero ML1 (the tram rescope), from the
     # M10_Red layers: same licence, same 5 June 2026 edit date. Wording
     # approved by the owner 2026-09-27; "Powered by CRTM" stays verbatim.
     "Powered by CRTM - www.crtm.es. Metro de Madrid and Metro Ligero "
     "station locations and line geometry are from CRTM's open data, last "
     "updated by CRTM on 5 June 2026 and shown here as recorded on that "
     "date. Used as datos explotados rather than en bruto: the network has "
     "been redrawn, its station-per-line records collapsed to one point per "
     "station, stations outside the término municipal removed, the Metro's "
     "eighteen published codes collapsed to its thirteen real lines, and of "
     "Metro Ligero only line ML1 drawn. CRTM does not participate in, "
     "sponsor or support this project.",
     True),
    ("TransLink",
     "Route and arrival data used in this product or service is provided by "
     "permission of TransLink. TransLink assumes no responsibility for the "
     "accuracy or currency of the Data used in this product or service.",
     True),
    # Province of British Columbia, added 2026-09-22, and it is the first
    # PROVINCIAL / STATE-level publisher in the project. Neither Vancouver's
    # nor Surrey's municipal OGL reaches it: the BC ABMS municipalities layer
    # is the Province's, read over WFS from openmaps.gov.bc.ca, and it is what
    # NAMES the 30 SkyTrain stations that fall outside both cities in
    # outputs/vancouver/excluded_stations.csv. That file is committed and
    # public, so the Information is distributed and the attribution clause
    # engages.
    #
    # It was missed for a day because the source is not a business registry, a
    # transit feed or the city boundary - it is the NAMING layer, the fourth
    # kind of input, and the one no per-city checklist had a slot for.
    #
    # VERBATIM, and it is the third en-dash-and-British-"Licence" wording in
    # this list: Vancouver's, Calgary's and now the Province's. Surrey's is the
    # odd one with a hyphen and "License". They are not interchangeable.
    # Terminates automatically on breach, like the four municipal OGLs.
    ("Province of British Columbia",
     "Contains information licensed under the Open Government "
     "Licence – British Columbia.",
     True),
    # Montréal, added 2026-09-21. TWO credits for one city, because the
    # business data and the transit data have different OWNERS - the STM's
    # datasets are hosted on the City's portal but are STM's property, and its
    # own dataset note says so: "selon la clause d'attribution de la licence
    # Creative Commons 4.0, la paternité des données doit être attribuée à la
    # Société de transport de Montréal."
    #
    # THE CITY'S CONDITION IS BROADER THAN STANDARD CC-BY, and this notice is
    # written to satisfy the broad part. Verified verbatim on the City's own
    # licence page (donnees.montreal.ca/pages/licence-d-utilisation): "Vous
    # devez créditer les données et les contenus que vous utilisez et préciser
    # si des modifications ont été effectuées **ou si des interprétations en
    # ont été tirées**."
    #
    # This project always draws interpretations - ring density, category
    # bucketing, storefront filtering - so a bare "data from the Ville de
    # Montréal" would NOT comply. The wording below states the transformation
    # explicitly. Not marked verbatim because the City prescribes the
    # OBLIGATION rather than a sentence; the disclosure is what is required.
    ("Ville de Montréal",
     "Contains data from the Ville de Montréal, used under the Creative "
     "Commons Attribution 4.0 International licence. The data has been "
     "modified and interpretations have been drawn from it: it is filtered to "
     "storefront categories, grouped into three categories of this project's "
     "own, and measured by distance from transit stations. The Ville de "
     "Montréal does not endorse this project or its use of the data.",
     False),
    ("Société de transport de Montréal",
     "Métro route geometry and station locations for Montréal are the "
     "property of the Société de transport de Montréal, used under the "
     "Creative Commons Attribution 4.0 International licence.",
     False),
    # The REM, added 2026-09-27 with the tram rescope (notice 51). CC BY 4.0
    # from the licence file bundled in the feed, which names no licensor, so
    # the credit goes to the creator feed_info/agency.txt identify - not
    # Pulsar, which serves the file. The licence prescribes no wording; it
    # requires the credit, a statement of modification and a licence link, and
    # forbids implying endorsement (s.2(a)(6)) or using the logo (s.2(b)(2)).
    # Wording approved by the owner 2026-09-27.
    ("Réseau express métropolitain",
     "REM route geometry and station locations for Montréal are from the "
     "Réseau express métropolitain (REM) GTFS feed, used under the "
     "[Creative Commons Attribution 4.0 International licence]"
     "(https://creativecommons.org/licenses/by/4.0/). The data has been "
     "modified: its three services are drawn as one line, stations outside "
     "the agglomeration are removed, and two stations are merged with the "
     "Métro stations of the same name. The Réseau express métropolitain does "
     "not endorse this project or its use of the data.",
     False),
    # Calgary, added 2026-09-21. ONE notice covers BOTH the business register
    # and Calgary Transit's GTFS - the only Canadian city where a single
    # licence does both, so this city adds one line where Vancouver added
    # three and Montréal two.
    #
    # VERBATIM, and note the en dash and the British "Licence" - Surrey's
    # sibling notice uses a hyphen and "License", and they are not
    # interchangeable. Like Toronto's, Vancouver's and Surrey's, this licence
    # TERMINATES AUTOMATICALLY on breach.
    ("City of Calgary",
     "Contains information licensed under the Open Government "
     "Licence – City of Calgary.",
     True),
    # Edmonton, added 2026-09-21. ONE notice covers BOTH the business register
    # and ETS's GTFS, as Calgary's does - the feed is published through the same
    # Open Data Catalogue and governed by the same Terms of Use.
    #
    # **EDMONTON WAS RECORDED AS NEEDING NO NOTICE AT ALL, AND THAT WAS WRONG.**
    # Its Terms of Use say credit is "not required" but "encouraged", which is
    # how the Canada profile and the build brief both concluded it was the one
    # Canadian city with nothing to display. The obligation is in a different
    # clause, and it is not about credit:
    #
    #   "If you distribute or provide access to the datasets to any other
    #    person, whether in original or modified form, you agree to include a
    #    copy of, or this Uniform Resource Locator (URL) for, these Terms of
    #    Use and to ensure any such person agrees to, and is bound by, them
    #    without introducing any further restrictions of any kind."
    #
    # `outputs/edmonton/` is committed to a public repository and carries the
    # register's business names, categories and coordinates - the datasets in
    # modified form. So the clause engages, and what it requires is the URL.
    # The harder half, "without introducing any further restrictions", is
    # already satisfied: the repository's own LICENSE explicitly disclaims MIT
    # over everything under `outputs/` and points at docs/data_sources.md.
    #
    # Not marked verbatim: the City prescribes that the URL accompany the data,
    # not a sentence to reproduce. The credit is included because the terms
    # encourage it, and the transformation is stated because this project always
    # draws interpretations.
    # Toronto, added 2026-09-21. ONE notice covers BOTH the MLS business
    # register and the TTC's GTFS - both are City of Toronto CKAN resources
    # under the same licence, so this city adds one line where Vancouver added
    # three. VERBATIM, en dash, British "Licence". Like Vancouver's, Surrey's
    # and Calgary's, this licence TERMINATES AUTOMATICALLY on breach.
    ("City of Toronto",
     "Contains information licensed under the Open Government "
     "Licence – Toronto.",
     True),
    ("City of Edmonton",
     "Contains datasets made publicly available by the City of Edmonton under "
     "its Open Data Terms of Use, at "
     "https://www.edmonton.ca/sites/default/files/public-files/documents/"
     "Web-version2.1-OpenDataAgreement.pdf — which govern any further use of "
     "them and are passed on without additional restriction. The data has been "
     "modified and interpretations drawn from it: it is filtered to storefront "
     "categories, grouped into three categories of this project's own, and "
     "measured by distance from transit stations. The City of Edmonton does "
     "not endorse this project or its use of the data.",
     False),
    # Kitchener–Waterloo: Region of Waterloo Public Health's food and personal
    # services inspection layers and bulk tables, and the Region's Cities and
    # Towns layer, under the Region of Waterloo Open Data Licence (read
    # 2026-09-30; the bulk tables' item pages name no licence, and the owner
    # read the portal's "By downloading the data on the portal, you are
    # agreeing to the Open Data License" as covering them, 2026-09-30). Credit
    # is OPTIONAL under the licence, but it prescribes the sentence to use if
    # one is given; it is reproduced VERBATIM. The licence bars suggesting
    # official status or endorsement and misrepresenting the data or its
    # source; the layers' descriptions add that no endorsement of any premises
    # is implied. Written under the owner's pre-approval of this build's prose
    # (2026-09-30).
    ("Region of Waterloo (Kitchener–Waterloo)",
     "Contains information provided by the Regional Municipality of Waterloo under licence "
     "([Region of Waterloo Open Data Licence](https://www.regionofwaterloo.ca/"
     "government-and-council/transparency-and-accountability/open-data/)). Food premises "
     "and personal services for Kitchener–Waterloo are from Region of Waterloo Public "
     "Health's inspection data, and the boundaries of Kitchener and Waterloo from the "
     "Region's Cities and Towns layer. Changes: the premises are limited to the two cities "
     "and to those inspected in the last two years; institutional kitchens, caterers, "
     "market stalls, clubs and venues, pharmacies and mobile units are left out by type or "
     "by name; and the rest are mapped by distance to ION stops. Inspection results are not "
     "shown, and a pin is not a rating or an endorsement of the premises. This is not an "
     "official Region of Waterloo product, and it is not endorsed by the Region.",
     False),
    # Mexico City, added 2026-09-22. TWO OBLIGATIONS IN ONE NOTICE, and the
    # second is the one a source credit does not discharge.
    #
    # INEGI's Terminos de Libre Uso (docs/licenses/
    # inegi-terminos-libre-uso-informacion.pdf) are unusually generous -
    # sections 1(b) to 1(e) permit publishing, adapting, extracting and even
    # COMMERCIAL use - in exchange for three things:
    #
    #   1(f)  credit INEGI as author and, where technically possible, name the
    #         source as "Fuente: INEGI, nombre del producto..." plus the update
    #         date. The prescribed shape is followed below.
    #   1(g)  "Asegurarse de notificar al usuario final de cualquier analisis o
    #         transformacion que haga a la informacion y que la misma no sea
    #         presentada de tal manera que sugiera que dicho analisis o
    #         transformacion fue realizada por parte del INEGI."
    #   1(h)  the use must not appear to represent an official INEGI position,
    #         nor to be endorsed, sponsored or supported by the source.
    #
    # 1(g) IS A SEPARATE DUTY, NOT A LOUDER VERSION OF 1(f) - the same split as
    # the Ville de Montreal's "ou si des interpretations en ont ete tirees", and
    # this project triggers it on every map: ring assignment, bucketing into
    # three categories, the storefront filter and the Fijo-only filter are all
    # transformations. A bare "data from INEGI" would credit and not disclose.
    #
    # Not marked verbatim: INEGI prescribes the attribution FORM and the
    # disclosure OBLIGATION, but no sentence for the latter.
    #
    # NAMES EVERY MEXICAN CITY, and it did not until 2026-09-22. This notice
    # read "Business locations for Mexico City are from DENUE" while Guadalajara
    # was also built from DENUE (entidad 14), so that city's use was covered by
    # no notice at all - and the build write-up had claimed the notice "names
    # the register rather than the city", which was wrong about text in this
    # file. §1(f) and §1(g) are per-USE duties, so a city the notice does not
    # name is a city whose transformation is undisclosed.
    #
    # ADD EACH NEW MEXICAN CITY TO THIS SENTENCE. It is the one notice here
    # that has to grow with the country, because DENUE is one register serving
    # many cities - every other source in this list serves exactly one.
    ("INEGI",
     "Fuente: INEGI, Directorio Estadístico Nacional de Unidades Económicas "
     "(DENUE). Business locations for Mexico City, Guadalajara and Monterrey "
     "are from "
     "DENUE, published by "
     "the Instituto Nacional de Estadística y Geografía, used under the "
     "Términos de Libre Uso de la Información del INEGI. The data has been "
     "analysed and transformed by this project and not by INEGI: it is "
     "filtered to fixed premises in storefront categories, grouped into three "
     "categories of this project's own, and measured by distance from transit "
     "stations. INEGI does not endorse this project or its use of the data, "
     "and nothing here represents an official INEGI position.",
     False),
    # Mexico City's RAIL geometry is OpenStreetMap rather than the operator's
    # feed, because every *.cdmx.gob.mx host is unreachable (see
    # pipeline/mexico_city/config.py). ODbL 1.0 attribution was already
    # satisfied for the basemap by every rendered map's "© OpenStreetMap
    # contributors"; this line exists so the credit visibly covers the LINE
    # GEOMETRY too, which is data rather than tiles.
    ("OpenStreetMap (rail geometry)",
     "Rail route geometry and station locations for Mexico City (Metro CDMX "
     "and Tren Ligero), Guadalajara (Tren Ligero), Monterrey (Metrorrey, with "
     "the boundaries of its four municipios) and Barcelona (Metro de "
     "Barcelona, including its FGC lines and both funiculars), and the route "
     "geometry of Lille's two métro lines, the per-line colours of "
     "Oslo's T-bane and tram lines, the colour of Bergen's Bybanen line 1, "
     "and Copenhagen's Metro and S-tog lines "
     "and stations and the municipal boundaries used to select them, "
     "Aarhus's Letbane L2 line and its stops, the municipal boundaries used to "
     "select them and the address points used to place its businesses, "
     "Kitchener–Waterloo's ION line and its stops, "
     "Buffalo's NFTA Metro Rail line and its stations, "
     "Sacramento's SacRT Blue and Gold Lines and their stations, and the "
     "municipal boundaries used to select them, "
     "Houston's METRORail Red, Green and Purple Lines and their stations, "
     "Ottawa's O-Train Lines 1, 2 and 4 and their stations, "
     "Minneapolis's METRO Blue and Green Lines and their stations, "
     "Pittsburgh's PRT Red, Blue and Silver Lines and their stations, "
     "Rome's metro and Roma–Viterbo urban lines and their stations, "
     "Palma's Metro M1 and its stations, and the municipal boundaries used to "
     "select them, "
     "the metro, VLT and suburban lines and stations of São Paulo (with its "
     "CPTM Linha 9), Rio de Janeiro (its VLT and SuperVia lines), Belo "
     "Horizonte, Brasília, Salvador, Fortaleza, Porto Alegre, Recife and "
     "Santos, and those cities' município boundaries, and "
     "Prague's, Amsterdam's, Rome's and Rotterdam's city boundaries, Hong Kong's MTR and "
     "Light Rail lines and stations, and its boundary, Seoul's subway lines and stations and "
     "its boundary, the routes of Taichung's Green Line and Taoyuan's Airport MRT, and the "
     "metro and light-rail lines and stations of Taipei and New Taipei are from OpenStreetMap, "
     "© OpenStreetMap contributors, available "
     "under the Open Database License. The alignments drawn are OSM's own "
     "geometry; stations, rings and categories are this project's work.",
     False),
    # Barcelona's terms prescribe the source wording AND require modifications
    # to be identified at distribution - the disclosure-of-transformation
    # family for the fourth time, after Montreal, INEGI and Madrid. A credit
    # alone does not discharge the second. See docs/data_sources.md item 21.
    #
    # The separate duty to NOTIFY the Council of every derived project is an
    # affirmative act owed to the publisher, not text on a page, so it is not
    # dischargeable here and is tracked as an owner action instead.
    #
    # The closing sentence reports the STATUS of that act and must never be
    # worded as though it performed it. It is here because the notification
    # could not be delivered: on 2026-09-22 the portal's own contact form
    # stalled after its hCaptcha, and the enquiry channel the terms themselves
    # name (bcn.cat/cgi-bin/consultesIRIS?id=241, redirecting to
    # atencioenlinia.ajuntament.barcelona.cat) did not respond from two
    # independent networks while seuelectronica.ajuntament.barcelona.cat
    # answered in 2.4s from the same /24. The attempt log lives in
    # docs/notifications/barcelona-city-council.md; when it is sent, update
    # this sentence and that file together.
    ("Ajuntament de Barcelona",
     "Source of the data: Barcelona City Council. The premises shown for "
     "Barcelona are from the Cens de locals en planta baixa amb activitat "
     "economica, 2022 survey, used under CC BY 4.0. The data has been "
     "modified by this project and not by the Ajuntament: vacant premises are "
     "removed, it is filtered to storefront categories, grouped into three "
     "categories of this project's own, and measured by distance from metro "
     "stations. The Ajuntament does not endorse this project or its use of "
     "the data. Those terms also require reusers to inform the Ajuntament of "
     "every derived project. That notification is written and not yet "
     "delivered: on 22 September 2026 the portal's own contact form stalled, "
     "and the enquiry channel the terms themselves name did not respond. It "
     "will be sent when that service is reachable again.",
     False),
    # Palma: the Consell de Mallorca's restaurant register, on the GOIB
    # catalogue (dataset licence "cc-by"; GOIB's terms link CC BY 3.0 ES), and
    # Catastro's INSPIRE addresses (CC BY 4.0 DG Catastro), both read
    # 2026-09-29 with the owner's three calls (DECISIONS). GOIB's terms require
    # the source credit, the author, the title, the licence link, the dataset
    # URI, the date of last update and a statement that the data were modified,
    # and bar implying endorsement; Catastro's ask that the Dirección General
    # del Catastro be named as author and owner, the licence, a statement of
    # the join and the access date. Written under the owner's pre-approval of
    # this build's prose (2026-09-30).
    ("Govern de les Illes Balears and Dirección General del Catastro (Palma)",
     "Font de les dades: Govern de les Illes Balears. Bars, cafés and restaurants for Palma "
     "are from the Registre d'Establiments de Restauració i Entreteniment de Mallorca "
     "(author: Consell de Mallorca, Direcció Insular de Transició i Ordenació Turística), "
     "[dataset](https://intranet.caib.es/opendatacataleg/dataset/"
     "empreses-restauracio-entreteniment-mallorca), last updated 2026-09-07, used under "
     "[CC BY 3.0 ES](https://creativecommons.org/licenses/by/3.0/es/). Premises without "
     "coordinates are placed at the address points of the Dirección General del Catastro "
     "(Ministerio de Hacienda), author and owner of that information, INSPIRE Addresses for "
     "Palma, accessed 2026-09-30, used under [CC BY 4.0](https://creativecommons.org/"
     "licenses/by/4.0/). Both have been modified by this project: the register is limited "
     "to active premises in Palma, caterers, clubs, venues and hotels are left out, "
     "addresses are joined to Catastro's points, and the rest are mapped by distance to "
     "Metro stations. Neither the Govern, the Consell nor Catastro endorses this map.",
     False),
    # TAILTE EIREANN - Dublin. CC BY 4.0, confirmed from data.gov.ie's
    # package_show. NO wording is prescribed, so the string is this project's
    # own; what is NOT optional is the second sentence, because CC BY 4.0
    # 3(a)(1) requires a reuser to "indicate if You modified the Licensed
    # Material" and a bare source credit does not do that. Fifth time this
    # project has met the disclosure-of-transformation duty, after Montreal,
    # INEGI, Madrid and Barcelona.
    #
    # NOTHING IS OWED AS AN ACT here - no notification, no registration - which
    # is explicitly the opposite of Barcelona above and is recorded positively
    # in docs/data_sources.md so it is not re-opened.
    #
    # The accuracy sentence is required in substance: Tailte disclaims
    # accuracy, completeness and currency, and tailte.ie/home/api/ states the
    # API "is not guaranteed to be complete".
    ("Tailte Éireann",
     "Contains Irish Public Sector Information licensed under a Creative "
     "Commons Attribution 4.0 International (CC BY 4.0) licence. The premises "
     "shown for Dublin are from Tailte Éireann's rateable valuation register, "
     "via its open API. This map filters, re-categorises and aggregates that "
     "data into density measures; the filtering, categories and densities are "
     "this project's own interpretation and are not produced or endorsed by "
     "Tailte Eireann. The data is published “as is”; Tailte Eireann "
     "gives no warranty as to its accuracy, completeness or currency.",
     False),
    # COMUNE DI MILANO - Milan. CC BY 4.0, and the version is the point: CKAN
    # reports `license_id: cc-by` with NO version, and only the portal's
    # DCAT-AP_IT serialisation carries owl:versionInfo "4.0". Milan's brief
    # pins its licence check to the .ttl for that reason.
    #
    # No wording prescribed, so this string is this project's own. The second
    # sentence is again the CC BY 4.0 3(a)(1) modification duty - the sixth
    # time - and it is the weaker form: 4.0 requires disclosing MODIFICATION
    # and says nothing about interpretation, where Montreal's licence names
    # both. Nothing is owed as an act.
    ("Comune di Milano",
     "Contains data from the Comune di Milano, licensed under a Creative "
     "Commons Attribution 4.0 International (CC BY 4.0) licence. The premises "
     "shown for Milan are from six of the Comune's own registers of shops, "
     "bakers, artisan food makers, bars and restaurants, and personal "
     "services. This map filters, re-categorises and aggregates that data "
     "into density measures; the filtering, categories and densities are this "
     "project's own and are not produced or endorsed by the Comune di Milano.",
     False),
    # ILE-DE-FRANCE MOBILITES - Paris. THE ONLY NOTICE HERE THAT PRESCRIBES
    # MARKUP, not just words.
    #
    # Licence Mobilites is not a standard public licence: it covers 2 of the
    # NAP's 799 datasets, there is no government-hosted text, and the
    # authoritative document is a 14-page PDF behind a community wiki. Art. 3.1
    # grants public display; Art. 5.4(a) prescribes BOTH the sentence and its
    # LINKING - the database name hyperlinks to the dataset URI, and
    # « Licence Mobilites » to the licence text. Hence the markdown links: they
    # are the obligation, not decoration. st.caption renders markdown.
    #
    # Added 2026-09-23 after a verification pass found it MISSING from every
    # map page while `docs/data_sources.md` had been calling it "a deploy
    # blocker for Paris specifically" since the day it was written. Nothing
    # automated caught that: check_provenance.py prints "24 numbered, N
    # displayed" and passes regardless.
    #
    # Art. 5.7 also requires the data's date and update interval to be shown.
    # That half is Paris-specific and lives on the city page, which reads
    # outputs/paris/provenance.json - it cannot live here, because this block
    # renders on every page and the date belongs to one city's snapshot.
    ("Île-de-France Mobilités",
     "Contient des informations de "
     "[Réseaux urbains et interurbains d'Île-de-France Mobilités (IDFM)]"
     "(https://transport.data.gouv.fr/datasets/"
     "reseau-urbain-et-interurbain-dile-de-france-mobilites), présentement "
     "mises à disposition aux conditions de la "
     "[« Licence Mobilités »](https://cloud.fabmob.io/s/CJCEzKosfqqNBEx)",
     True),
    # TISSEO - Toulouse. ODbL 1.0 via the National Access Point, and the
    # FIRST sentence here is ODbL 4.3's own notice template with the database
    # named, so it is verbatim rather than this project's wording.
    #
    # ⚠ THE EXISTING OPENSTREETMAP NOTICE DOES NOT DISCHARGE THIS. Both are
    # ODbL, which is exactly why it is easy to assume one credit covers both -
    # but 4.3 requires the notice to name WHICH database, and "OpenStreetMap"
    # does not name Tisséo's. Two ODbL sources need two notices.
    #
    # ODbL 4.6 (offer the derivative database, or the method) is satisfied by
    # the public repository carrying the pipeline and the derived CSVs -
    # PROVIDED it stays linked from the site, which is the same condition
    # IDFM's Art. 5.8 already imposes.
    #
    # The publisher's own CGU was read 2026-09-23 and adds nothing: no
    # indemnity, and its marks clause is Opendatasoft's with « les données
    # publiées sur le DOMAINE » expressly excluded - so naming Tisséo on the
    # map is not barred. That was the specific risk, since Grand Lyon's
    # equivalent clause is why Lyon is deferred.
    ("Tisséo (Toulouse)",
     "Contains information from Réseau urbain Tisséo, which is made available "
     "here under the Open Database License (ODbL). Métro, tramway and Téléo "
     "station locations and line geometry for Toulouse are redrawn from that "
     "feed; the stations kept, the rings, the categories and the densities "
     "are this project's own work and are not produced or endorsed by Tisséo "
     "or Toulouse Métropole.",
     True),
    # STAR - Rennes. ODbL 1.0, the same licence and the same reading as Tisséo
    # above (docs/licenses/odbl-toulouse-rennes.md), and the first sentence is
    # again ODbL 4.3's own template with the database named.
    #
    # ⚠ NEITHER NOTICE ABOVE DISCHARGES THIS. Three ODbL sources now -
    # OpenStreetMap, Tisséo, STAR - and 4.3 asks each notice to name its own
    # database.
    #
    # The portal's CGU is the same Opendatasoft template as Toulouse
    # Métropole's, read 2026-09-23: no indemnity, marks clause Opendatasoft's
    # own with the published data excluded - so naming STAR is not barred.
    ("STAR (Rennes)",
     "Contains information from Réseau urbain STAR, which is made available "
     "here under the Open Database License (ODbL). Métro station locations and "
     "line geometry for Rennes are redrawn from that feed; the stations kept, "
     "the rings, the categories and the densities are this project's own work "
     "and are not produced or endorsed by STAR, Keolis Rennes or Rennes "
     "Métropole.",
     True),
    # THE FRANCE TRAM BATCH'S THREE ODbL FEEDS (licence reads 2026-09-29): each
    # its own §4.3 notice naming its own database, as Tisséo's and STAR's are,
    # under the NAP's Conditions Particulières - the station tables are pure
    # extracts. Montpellier's and Le Havre's LINE GEOMETRY is OpenStreetMap's
    # (neither feed publishes shapes), which the OpenStreetMap notice covers, so
    # those two name only the stations; Grenoble's geometry is its feed's own.
    # No TaM logo, and LiA's colours are the project's own.
    ("TaM (Montpellier)",
     "Contains information from Réseau urbain TaM, which is made available here "
     "under the Open Database License (ODbL). Tram station locations for "
     "Montpellier are drawn from that feed; the stations kept, the rings, the "
     "categories and the densities are this project's own work and are not "
     "produced or endorsed by TaM or Montpellier Méditerranée Métropole.",
     True),
    ("M réso (Grenoble)",
     "Contains information from Réseau urbain TAG, which is made available here "
     "under the Open Database License (ODbL). Tram station locations and line "
     "geometry for Grenoble are redrawn from that feed; the stations kept, the "
     "rings, the categories and the densities are this project's own work and "
     "are not produced or endorsed by the SMMAG (M) or Grenoble-Alpes "
     "Métropole.",
     True),
    ("LiA (Le Havre)",
     "Contains information from Réseau urbain LiA, which is made available here "
     "under the Open Database License (ODbL). Tram station locations for Le "
     "Havre are drawn from that feed; the stations kept, the rings, the "
     "categories, the line colours and the densities are this project's own "
     "work and are not produced or endorsed by LiA or Le Havre Seine Métropole.",
     True),
    # BRØNNØYSUNDREGISTRENE - Oslo's business register. NLOD 2.0: section 5
    # says to attribute "as specified by the licensor", and Brønnøysund's API
    # documentation specifies nothing beyond "License: NLOD" (read
    # 2026-09-24) - so this is section 5's own default sentence, VERBATIM,
    # with the licence linked. Section 5 also requires changes to be
    # indicated clearly, which the second sentence does.
    ("Brønnøysundregistrene (Oslo, Bergen)",
     "Contains data under the Norwegian licence for Open Government data "
     "(NLOD) distributed by Brønnøysundregistrene "
     "([NLOD 2.0](https://data.norge.no/nlod/en/2.0)). Oslo's and Bergen's "
     "business premises are selected, classified and placed by this project, and a "
     "sole trader's premises is shown by its address rather than its name; "
     "the categories and densities are this project's own work.",
     True),
    # KARTVERKET - two datasets, one licensor, one licence (CC BY 4.0), so one
    # line: the address register (the coordinate join) and the kommune
    # boundaries (station scope and the naming of excluded stations).
    # Kartverket's own terms prescribe "© Kartverket" and a link; CC BY 4.0
    # 3(a) adds the licence link and a statement of modification. The
    # boundaries' municipality names come from SSR, whose rule asks for
    # "SSR ©Kartverket" - cheap, so included rather than argued.
    ("Kartverket (Oslo, Bergen)",
     "© [Kartverket](https://www.kartverket.no). Oslo's and Bergen's address "
     "registers (Matrikkelen – Adresse) and the municipal boundaries of Oslo, "
     "Bærum and Bergen "
     "(Administrative enheter kommuner), under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); municipality "
     "names from SSR ©Kartverket. This project joins the addresses to the "
     "business register to place each premises, and uses the boundaries to "
     "select and label stations.",
     True),
    # ENTUR - Ruter's GTFS. NLOD, and Entur SPECIFIES its credit: "Data made
    # available by Entur + (logo)" (developer.entur.org, read 2026-09-24).
    # The LOGO is shown on the Oslo page beside this data (owner's call
    # 2026-09-24: the old portal's instruction is still live, so it is
    # treated as owed) - Entur's own unaltered file,
    # app/assets/entur/Enturlogo_Blue_RGB.svg. NLOD section 6 bars using the
    # licensor's or other contributors' names to endorse, which reaches Ruter.
    ("Entur (Oslo, Bergen)",
     "Data made available by Entur, under the Norwegian licence for Open "
     "Government data ([NLOD 2.0](https://data.norge.no/nlod/en/2.0)); source: "
     "Ruter's and Skyss's timetable data via [Entur](https://developer.entur.org). "
     "The T-bane, tram and Bybanen lines and stations are selected, limited to "
     "Oslo and Bergen kommunes and redrawn by this project, and the line colours "
     "are not from this data. Not produced or endorsed by Entur, Ruter, "
     "Sporveien or Skyss.",
     True),
    # CVR - Copenhagen's business register, via Datafordeler. CC BY 4.0:
    # "Du skal kreditere Det Centrale Virksomhedsregister (CVR) på et
    # passende sted" (datafordeler.dk, read 2026-09-23). The name is
    # prescribed, the wording is not, so this string is this project's own;
    # its second sentence is CC BY 4.0 3(a)(1)'s modification duty. Wording
    # approved by the owner 2026-09-24.
    # Aarhus added 2026-09-29, owner-approved: the same register and cache.
    ("Det Centrale Virksomhedsregister (Copenhagen, Aarhus)",
     "Contains data from Det Centrale Virksomhedsregister (CVR), distributed by "
     "Datafordeler under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
     "Copenhagen's and Aarhus's business premises are selected, classified and placed by this "
     "project, and a personally owned business is shown by its address rather "
     "than its name; the categories and densities are this project's own work "
     "and are not produced or endorsed by Erhvervsstyrelsen.",
     False),
    # DAR - the coordinate join. CC BY 4.0 crediting Klimadatastyrelsen, which
    # lets the reuser choose the form of credit (read 2026-09-24 by the
    # licence-read agent). Named with the register as well, since Datafordeler's
    # general terms ask for "the responsible register". Wording approved by the
    # owner 2026-09-24.
    # Aarhus added 2026-09-29, owner-approved: it reads DAR's Adresse and
    # Husnummer, and takes the point from OSM's copy (osak:identifier).
    ("Klimadatastyrelsen (Copenhagen, Aarhus)",
     "Contains data from Klimadatastyrelsen, Danmarks Adresseregister (DAR), via "
     "Datafordeler under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
     "This project joins the register's addresses and address points to the "
     "business register to place each premises; in Aarhus the points are "
     "OpenStreetMap's copies of them.",
     False),
    # ČSÚ - Prague's activity, form and name data (RES). CC BY 4.0 for the web
    # pages, and the DATA paragraph ("Další podmínky použití dat ČSÚ") adds two
    # duties this notice discharges: state the licence conditions, preferably
    # by a direct link, and mark modified or derived data as such and never
    # present it as unchanged official statistics (read 2026-09-23/24).
    # Wording approved by the owner 2026-09-24.
    ("Czech Statistical Office (Prague)",
     "Contains data from the Czech Statistical Office's business register "
     "(Registr ekonomických subjektů, RES), used under the [ČSÚ conditions of use]"
     "(https://csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu) "
     "(CC BY 4.0). The activity, legal-form and name data are modified and derived by "
     "this project — joined to establishment locations, filtered to storefront "
     "categories and grouped into this project's own categories — and are not "
     "official statistics of the Czech Statistical Office.",
     False),
    # ČÚZK - RUIAN addresses. The Czech conditions page PRESCRIBES the credit
    # format "ČÚZK, [rok]" (the file's year), a link to the conditions, and a
    # description of the modification. Wording approved by the owner 2026-09-24.
    ("ČÚZK (Prague)",
     "ČÚZK, 2026. Address points from the Registry of Territorial Identification, "
     "Addresses and Real Estate (RÚIAN), under the [ČÚZK conditions]"
     "(https://www.cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx) "
     "(CC BY 4.0). This project joins the addresses to the business register and "
     "converts their coordinates to place each establishment.",
     False),
    # ROPID / PID - Prague's metro. CC BY: name the author and any changes
    # (pid.cz/o-systemu/opendata/, read 2026-09-24). The PID, ROPID and IDSK
    # LOGOS need ROPID's consent and are not used. Wording approved by the
    # owner 2026-09-24.
    ("ROPID (Prague)",
     "Metro lines and stations for Prague are redrawn from PID open data published "
     "by ROPID ([pid.cz/o-systemu/opendata](https://pid.cz/o-systemu/opendata/)), "
     "under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the "
     "three metro lines are selected and redrawn, stations are reduced to one point "
     "each, and line A's colour is lightened. Not "
     "produced or endorsed by ROPID or DPP.",
     False),
    # Gemeente Amsterdam - hospitality permits. The register's own licence is
    # SILENT (`Licentie: -`; a retired 2022 catalogue said CC BY), so CC BY 4.0
    # is displayed on the owner's choice of 2026-09-24, which satisfies both
    # readings. The BAG (Public Domain Mark) and GVB's data (CC0) need nothing.
    # Wording approved by the owner 2026-09-24.
    ("Gemeente Amsterdam (Amsterdam)",
     "Hospitality permits for Amsterdam are from the Gemeente Amsterdam's register "
     "of hospitality operating permits (horeca exploitatievergunningen, "
     "[api.data.amsterdam.nl](https://api.data.amsterdam.nl/v1/)), used under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the permits "
     "are filtered to restaurants, cafés, takeaways, coffeeshops and nightclubs, "
     "grouped into one category, matched to the national buildings register by "
     "address, and mapped by distance to metro and tram stops. This is not the "
     "official permit record, and it is not produced or endorsed by the Gemeente "
     "Amsterdam.",
     False),
    # Roma Capitale - the SUAP premises register. CC BY 4.0 on the dataset page
    # (read 2026-09-24): credit, link the licence, state the changes. Wording
    # approved by the owner 2026-09-24.
    ("Roma Capitale (Rome)",
     "Premises data for Rome is from Roma Capitale's register of productive "
     "activities (SUAP, [dati.comune.roma.it](https://dati.comune.roma.it/)), used "
     "under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the "
     "register is filtered to shops, food and drink, and personal services, sorted "
     "into three categories, placed at house-number level and mapped by distance "
     "to metro stations. Not produced or endorsed by Roma Capitale.",
     False),
    # ANNCSU - the national house-number archive that places SUAP's premises.
    # CC BY 4.0 (read 2026-09-24). Wording approved by the owner 2026-09-24.
    ("ANNCSU (Rome)",
     "House-number coordinates for Rome are from ANNCSU, the national archive of "
     "street numbers kept by the Agenzia delle Entrate and ISTAT "
     "([anncsu.open.agenziaentrate.gov.it](https://anncsu.open.agenziaentrate.gov.it/)), "
     "used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). They are "
     "used here to place another register's premises on the map.",
     False),
    # IBGE - CNEFE 2022, the establishment register behind all nine Brazilian
    # cities. Free use by federal law (Decree 8.777/2016 art. 4, Lei
    # 14.129/2021 art. 29), crediting the source; no wording is prescribed, so
    # the Fonte line is IBGE's own citation form. Wording approved by the owner
    # 2026-09-24 with São Paulo's page.
    ("IBGE (Brazil)",
     "Establishment data for Brazilian cities is from IBGE's Cadastro Nacional "
     "de Endereços para Fins Estatísticos (CNEFE). Fonte: IBGE, Cadastro "
     "Nacional de Endereços para Fins Estatísticos (CNEFE), Censo Demográfico "
     "2022. Changes: this project sorts each establishment's recorded "
     "description into three categories, leaves out those it cannot read, "
     "shows only the category at addresses that are also homes, and maps the "
     "rest by distance to stations. The categories are this project's "
     "reading, not IBGE's, and IBGE did not produce or endorse this map.",
     False),
    # IPP / DATA.RIO - Rio's metro stations and lines (layers 19 and 18). CC BY
    # 4.0 at service level (read 2026-09-23): the creator, the licence, a link,
    # and a statement that the data was modified - CC BY 4.0 s3(a)(1)(B), not
    # optional. Wording approved by the owner 2026-09-24.
    ("IPP / DATA.RIO (Rio)",
     "Metro stations and lines for Rio de Janeiro: Prefeitura da Cidade do Rio "
     "de Janeiro / Instituto Pereira Passos (IPP), via DATA.RIO "
     "([pgeo3.rio.rj.gov.br](https://pgeo3.rio.rj.gov.br/arcgis/rest/services/"
     "Transporte_Trafego/Transporte_publico/MapServer)), licensed under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Reprojected, "
     "filtered and redrawn by this project; station rings and density figures "
     "are this project's own analysis.",
     False),
    # CBS - the shop-vacancy share Rotterdam's page quotes. CC BY 4.0
    # (cbs.nl copyright page, read 2026-09-24): credit CBS, link the licence,
    # say when a figure is recalculated; no endorsement implied, no logo.
    # Wording approved by the owner 2026-09-24.
    ("CBS (Rotterdam)",
     "The shop-vacancy figure for Rotterdam is from CBS (Statistics Netherlands), "
     "Landelijke Monitor Leegstand 2025, table 1, 1 January 2025, used under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) "
     "([cbs.nl](https://www.cbs.nl/)); the share is rounded from CBS's counts. "
     "CBS did not produce or endorse this map.",
     False),
    # FEHD's licence registers, via DATA.GOV.HK (Terms of Use v1.2, read
    # 2026-09-22), and FEHD's point for each licence from the same registers on
    # the CSDI Portal (its own terms, read 2026-09-24, add "identify clearly the
    # Government and the CSDI Portal as the source"). Both carry the same
    # uncapped indemnity, accepted by the owner. Identify the source,
    # acknowledge the Government's and FEHD's IP, and attribute the Government,
    # FEHD, DATA.GOV.HK and the CSDI Portal - in one paragraph. Wording
    # approved by the owner 2026-09-24.
    ("FEHD / DATA.GOV.HK / CSDI (Hong Kong)",
     "Hong Kong's restaurants, food shops and bathhouses are from the Food and Environmental "
     "Hygiene Department's licence registers for restaurants, other food premises and non-food "
     "premises, obtained from DATA.GOV.HK ([data.gov.hk](https://data.gov.hk)), with each "
     "licence's location from the same registers on the Common Spatial Data Infrastructure "
     "(CSDI) Portal ([portal.csdi.gov.hk](https://portal.csdi.gov.hk)). The Government of the "
     "Hong Kong Special Administrative Region and the Food and Environmental Hygiene Department "
     "own the intellectual property in this data. Source: the Government of the Hong Kong SAR "
     "and the Food and Environmental Hygiene Department, via DATA.GOV.HK and the CSDI Portal. "
     "Filtered and redrawn by this project; station rings and density figures are this "
     "project's own analysis.",
     False),
    # VZD cadastre open data (CC BY 4.0, adopted by VZD's own data-use rules,
    # read 2026-09-24): credit, licence link, a DESCRIPTION of the changes, and
    # no implied VZD approval. Wording approved by the owner 2026-09-24.
    ("VZD (Riga)",
     "Riga's shops and services are from the State Land Service of Latvia's (Valsts zemes "
     "dienests) Cadastre Information System open data — premise groups and the Riga cadastral "
     "map — via data.gov.lv, licensed under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by this project: "
     "premise groups of use class 1230 whose name reads as a shop or a service were selected, "
     "placed at their building's footprint by cadastre number and reprojected; those in "
     "buildings the city lists as degrading were removed; all are shown as one \"Shops and "
     "services\" category and counted around tram stops. VZD has not approved these changes or "
     "this map.",
     False),
    # Riga municipality's GEO RĪGA layers (CC BY 4.0, read 2026-09-24). The
    # neighbourhoods "have no administrative-boundary status", so the merged
    # outline is never called the city's boundary. Approved by the owner 2026-09-24.
    ("Riga municipality (Riga)",
     "Riga's address points, neighbourhood boundaries and list of degrading buildings are from "
     "Rīgas valstspilsētas pašvaldība (Riga State City Municipality), GEO RĪGA, via data.gov.lv, "
     "licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by "
     "this project: the address points place licensed food premises by address; the 58 "
     "neighbourhoods are merged into one outline used to select stations, which is not Riga's "
     "administrative boundary; the degrading-buildings list is used only to leave out shops in "
     "those buildings. None of the three is shown. The municipality does not endorse this map.",
     False),
    # Seoul's permit registers, all Korea Open Government License Type 1 (read
    # 2026-09-22 and 2026-09-24): KOGL's attribution form names the institution,
    # year, licence type and dataset titles, with a link where one is possible;
    # no implied sponsorship; and, under its moral-rights clause, the counts are
    # said to be this project's derivation. Wording approved by the owner
    # 2026-09-25. 유흥주점영업 is read and excluded, so it is not credited.
    ("Seoul Metropolitan Government",
     "Seoul's storefronts are from permit registers published by the Seoul Metropolitan "
     "Government (서울특별시) in 2026 on Seoul Open Data Plaza "
     "([data.seoul.go.kr](https://data.seoul.go.kr)) under the Korea Open Government License "
     "Type 1 ([공공누리 제1유형](https://www.kogl.or.kr/info/licenseType1.do)): 서울시 일반음식점, "
     "휴게음식점, 단란주점영업, 미용업, 이용업, 세탁업, 목욕장업, 제과점영업, 즉석판매제조가공업, "
     "식품판매업(기타), 축산판매업, 담배소매업, 대규모점포, 건강기능식품일반판매업, 숙박업 and 동물병원 "
     "인허가 정보. Modified by this project: open premises were selected, sorted into three "
     "categories, counted once per building, placed at their building (or at another permit's "
     "location at the same address where a permit has none) and counted around subway "
     "stations. The categories and counts are this project's own, not figures published by the "
     "Seoul Metropolitan Government, which does not sponsor or endorse this map.",
     False),
    # Daegu: D-데이터허브's files declare no licence; the permission rests on the
    # portal's own policy and the Public Data Act, a reasoned position disclosed
    # and accepted by the owner (docs/data_sources.md, "Daegu and Busan"). The
    # credit is the suggested one, with Seoul's describe-the-changes and
    # non-endorsement lines kept. The edition's rows end 2025-09-02, and the
    # notice says so. Wording approved by the owner 2026-09-27.
    ("Daegu Metropolitan City",
     "Daegu's storefronts are from the permit data (인허가데이터) published by Daegu "
     "Metropolitan City (대구광역시) on D-데이터허브 ([data.daegu.go.kr](https://data.daegu.go.kr)), "
     "originally from 한국지역정보개발원: 일반음식점, 휴게음식점, 단란주점영업, 미용업, 이용업, 세탁업, "
     "목욕장업, 제과점영업, 즉석판매제조가공업, 식품판매업(기타), 축산판매업, 담배소매업, 대규모점포 and "
     "건강기능식품일반판매업, in the edition published as August 2026 (records to 2025-09-02). "
     "Modified by this project: open premises were selected, sorted into three categories, "
     "counted once per building, placed at their building (or at another permit's location at "
     "the same address where a permit has none) and counted around subway stations. The "
     "categories and counts are this project's own, not figures published by Daegu Metropolitan "
     "City, which does not sponsor or endorse this map.",
     False),
    # Busan: PERMITTED WITH CONDITIONS - a reasonable source credit (the portal's
    # policy; 저작권법 제37조), no wording prescribed. The licence read's credit:
    # Big-데이터웨이브 (linked) as the channel, the Ministry's local-government
    # licence data as the source, and the snapshot date. Wording approved by the
    # owner 2026-09-27.
    ("Busan Metropolitan City",
     "Busan's storefronts are from the local-government licensing data (지방행정 인허가데이터) of "
     "the Ministry of the Interior and Safety (행정안전부), served by Busan Metropolitan City's "
     "Big-데이터웨이브 ([data.busan.go.kr](https://data.busan.go.kr)) through its 구군 인허가포털 "
     "Open API: 일반음식점, 휴게음식점, 단란주점영업, 미용업, 이용업, 세탁업, 목욕장업, 제과점영업, "
     "즉석판매제조가공업, 식품판매업(기타), 축산판매업, 담배소매업, 대규모점포 and 건강기능식품일반판매업, as "
     "last updated on 2026-04-15. Modified by this project: open premises were selected, sorted "
     "into three categories, counted once per building, placed at their building (or at another "
     "permit's location at the same address where a permit has none) and counted around subway "
     "stations. The categories and counts are this project's own, not figures published by Busan "
     "Metropolitan City or the Ministry, neither of which sponsors or endorses this map.",
     False),
    # Taiwan: every source is OGDL v1 (read 2026-09-23 and 2026-09-25), whose
    # attribution statement is LOAD-BEARING - without it the grant is deemed never
    # made (§三(二)) - in the annex's prescribed form. The FIA's own declaration
    # adds: cite, no emblems, no endorsement, and do not present the filtered
    # points as the register. The FIA notice is NATIONAL: each Taiwanese city
    # adds its name to it and a notice of its own sources. Approved by the owner
    # 2026-09-25.
    ("Fiscal Information Agency (Taiwan)",
     "Taichung's, Taoyuan's, Taipei's and New Taipei's storefronts are from 財政部財政資訊中心 2026 "
     "全國營業(稅籍)登記資料集 — Taiwan's "
     "national business tax register, published by the Fiscal Information Agency, Ministry of "
     "Finance (the data date is in each page's snapshot caption). 此開放資料依政府資料開放授權條款 "
     "(Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。 "
     "[data.gov.tw/license](https://data.gov.tw/license). This map is not the register: this "
     "project selected the storefront industries, left out online sellers and office-like "
     "head-office rows, placed each location by matching its address to the city's door plates, "
     "showed a sole proprietor's name only where it is clearly a trade name, and counted the "
     "results around stations. The Fiscal Information Agency does not endorse this map.",
     False),
    ("Taichung City Government and Taichung MRT (Taichung)",
     "提供機關／臺中市政府數位發展局 2026 臺中市115年1月至各月份GIS門牌資料 (the monthly file named in "
     "the page's snapshot caption), used to place Taichung's storefronts by address; and "
     "提供機關／臺中捷運股份有限公司 2026 臺中捷運綠線車站資訊, the Green Line's stations and their "
     "names. 此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守"
     "本條款各項規定之前提下，得利用之。 [data.gov.tw/license](https://data.gov.tw/license). The door "
     "plates themselves are not shown. Neither body endorses this map.",
     False),
    # Taoyuan: three OGDL v1 sources (read 2026-09-25), one statement each. The
    # metro provider is named as the publisher's own portal names it (owner). The
    # portal's FAQ adds that reuse must not mislead the public or jeopardise the
    # City Government's interests - recorded and accepted (owner, 2026-09-25).
    ("Taoyuan City Government, NLSC and Taoyuan Metro (Taoyuan)",
     "提供機關／桃園市政府民政局 2026 桃園市門牌位置坐標資料 (the monthly file named in the page's "
     "snapshot caption), used to place Taoyuan's storefronts by address; 提供機關／內政部國土測繪中心 "
     "2026 捷運車站, the Airport MRT's station locations; and 提供機關／桃園捷運公司 2026 "
     "桃園捷運路線車站基本資料, the line's stations and their names. 此開放資料依政府資料開放授權條款 "
     "(Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。 "
     "[data.gov.tw/license](https://data.gov.tw/license). The door plates themselves are not "
     "shown. None of these bodies endorses this map.",
     False),
    # Taipei (Regional): three OGDL v1 sources (read 2026-09-23 and 2026-09-25),
    # one statement each. Taipei Metro's own open-data declaration adds: cite the
    # source, no logo or marks, no implied endorsement of a derivative, and
    # liability for malicious alteration - accepted by the owner 2026-09-25.
    ("Taipei and New Taipei City Governments and Taipei Metro (Taipei (Regional))",
     "提供機關／臺北市政府民政局 2026 臺北市門牌位置數值資料 and 提供機關／新北市政府民政局 2026 "
     "新北市門牌位置數值資料 (the editions named in the page's snapshot caption), used to place the "
     "two cities' storefronts by address; and 提供機關／臺北大眾捷運股份有限公司 2026 "
     "臺北捷運路線車站資料服務, Taipei Metro's station list, used to check the map's stations. "
     "此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項"
     "規定之前提下，得利用之。 [data.gov.tw/license](https://data.gov.tw/license). The door plates "
     "themselves are not shown. None of these bodies endorses or approves this map.",
     False),
    # Kobe: the city's lists are CC BY 2.1 JP (the badge on each CSV; read
    # 2026-09-24), whose 出典 line and 「…を加工して作成」 are prescribed; MLIT's
    # 位置参照情報 and N02 are PDL 1.0 with their own credit lines; N03 (CC BY 4.0)
    # only picks stations and is never drawn (the Survey Act). The city's page
    # warns closed premises may remain, so nothing here says "open". Wording
    # approved by the owner 2026-09-27.
    ("City of Kobe and MLIT (Kobe)",
     "Kobe's businesses: 出典：「生活衛生関係許可施設等の情報提供」（神戸市）"
     "（[https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html](https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html)）を加工して作成 "
     "(© City of Kobe; [CC BY 2.1 JP](https://creativecommons.org/licenses/by/2.1/jp/)). Their "
     "locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）"
     "を加工して作成. Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, "
     "stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; not drawn). This project "
     "selected the storefront permit types, placed each premises by its address, and counted them "
     "around stations. The list may include premises that have closed. The City of Kobe and MLIT "
     "did not make and do not endorse this map.",
     False),
    # Osaka (notice 52): the city's three lists are CC BY 4.0 (each source page:
    # 「CC-BY4.0で提供いたします。」, read 2026-09-24 and again 2026-09-27), in
    # the city's prescribed 「…」（大阪市）（URL）を加工して作成 form, one title per
    # page; MLIT as in Kobe's. The map must not look like the city's own.
    # Wording approved by the owner 2026-09-28.
    ("Osaka City and MLIT (Osaka)",
     "Osaka's businesses: 「食品営業許可施設一覧」（大阪市）"
     "（[https://www.city.osaka.lg.jp/kenko/page/0000575579.html](https://www.city.osaka.lg.jp/kenko/page/0000575579.html)）、「理容所及び美容所の開設施設一覧」"
     "（大阪市）（[https://www.city.osaka.lg.jp/kenko/page/0000431136.html](https://www.city.osaka.lg.jp/kenko/page/0000431136.html)）、「クリーニング所の開設施設一覧」"
     "（大阪市）（[https://www.city.osaka.lg.jp/kenko/page/0000552712.html](https://www.city.osaka.lg.jp/kenko/page/0000552712.html)）を加工して作成 "
     "([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Their locations: "
     "出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). This project selected the storefront permit "
     "types, placed each premises by its address, and counted them around stations. The lists may "
     "include premises that have closed. Osaka City and MLIT did not make and do not endorse this map.",
     False),
    # Sapporo (notice 53): both datasets CC BY 4.0 on the city's own CKAN
    # (read 2026-09-24; the registers' package re-read 2026-09-28). No wording is
    # prescribed: credit 札幌市, both dataset titles and URLs, the licence link and
    # that the data was processed (the brief's example form); no endorsement, no
    # logos, never "operating". MLIT as in Kobe's and Osaka's. URLs are explicit
    # markdown links: bare ones ran on into the Japanese (fixed 2026-09-28).
    # Wording approved by the owner 2026-09-28.
    ("Sapporo City and MLIT (Sapporo)",
     "Sapporo's businesses: 札幌市『札幌市内の食品営業許可施設一覧』（[https://ckan.pf-sapporo.jp/dataset/sapporo_food_business_licences](https://ckan.pf-sapporo.jp/dataset/sapporo_food_business_licences)）"
     "『札幌市内の環境衛生営業施設一覧』（[https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services](https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services)）"
     "（札幌市ICT活用プラットフォーム、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)）を加工して作成. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). This project selected the storefront permit "
     "types, placed each premises by its address, and counted them around stations. The lists may "
     "include premises that have closed. Sapporo City and MLIT did not make and do not endorse this map.",
     False),
    # Fukuoka (notice 54): the city's four lists on BODIK are CC BY 4.0 through
    # the city's own terms (odcs.bodik.jp/401307/tos/ 第７条: each dataset's 作成者,
    # the resource name with its date, the resource URL, that it was modified);
    # MHLW's open data is PDL 1.0 (the source, that it was processed and by
    # whom; its top page only; no completeness claim). MLIT as in Kobe's.
    # Every URL an explicit markdown link. Wording approved by the owner
    # 2026-09-28.
    ("Fukuoka City, MHLW and MLIT (Fukuoka)",
     "Fukuoka's businesses: 福岡市保健医療局 食品安全推進課「福岡市内飲食店営業等営業許可施設一覧（令和8年8月31日現在）」"
     "（[https://data.bodik.jp/dataset/5925a9fb-3326-4499-9acd-7b18c03d5e32/resource/70d22acf-2353-4bc1-b45d-f12d45da5216](https://data.bodik.jp/dataset/5925a9fb-3326-4499-9acd-7b18c03d5e32/resource/70d22acf-2353-4bc1-b45d-f12d45da5216)）, "
     "福岡市保健福祉局「福岡市内理容所検査確認済施設一覧（令和８年８月31日現在）」"
     "（[https://data.bodik.jp/dataset/5ff384ca-dcc8-401f-9ce6-59d5b139e921/resource/58e0494e-bc04-4298-a031-2caa64c2e254](https://data.bodik.jp/dataset/5ff384ca-dcc8-401f-9ce6-59d5b139e921/resource/58e0494e-bc04-4298-a031-2caa64c2e254)）"
     "「福岡市内美容所検査確認済施設一覧（令和８年８月31日現在）」"
     "（[https://data.bodik.jp/dataset/bcfa330c-cfd4-4eaf-9568-52436dc0e20d/resource/f029fc9e-b2f5-46a5-a2b6-e62d8113dbc1](https://data.bodik.jp/dataset/bcfa330c-cfd4-4eaf-9568-52436dc0e20d/resource/f029fc9e-b2f5-46a5-a2b6-e62d8113dbc1)）, "
     "福岡市保健福祉局 生活衛生課「福岡市内クリーニング所検査確認済施設一覧（令和８年３月31日現在）」"
     "（[https://data.bodik.jp/dataset/81520f4a-437b-422d-b136-fdf21af38b11/resource/2c00764a-ddfb-4193-aa61-0712d35f325b](https://data.bodik.jp/dataset/81520f4a-437b-422d-b136-fdf21af38b11/resource/2c00764a-ddfb-4193-aa61-0712d35f325b)）"
     "（[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)）を加工して作成; and "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, showed a premises in both lists "
     "once, placed each by its address or the ministry's own coordinates, and counted them around "
     "stations. The ministry's list holds only filings whose applicants agreed to publish them and is "
     "not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Fukuoka City, MHLW and MLIT did not make and do not endorse this map.",
     False),
    # Kyoto (notice 55): the portal's three datasets are CC BY 4.0 with 京都市 as
    # 著作権者 (read 2026-09-24). MUST DISPLAY 京都市 as creator, the name
    # 京都市オープンデータ (the portal's terms ask for it), the dataset names and
    # URLs, the licence link and that the data was processed; never "operating"
    # (closures are invisible in a rebuilt register). MLIT as in Kobe's. Every
    # URL an explicit markdown link. Wording approved by the owner 2026-09-28.
    ("Kyoto City and MLIT (Kyoto)",
     "Kyoto's businesses: 出典：京都市オープンデータ「食品営業許可施設一覧について」"
     "（[https://data.city.kyoto.lg.jp/dataset/00414/](https://data.city.kyoto.lg.jp/dataset/00414/)）"
     "「食品営業許可施設一覧について（令和3年6月以降）」"
     "（[https://data.city.kyoto.lg.jp/dataset/00541/](https://data.city.kyoto.lg.jp/dataset/00541/)）"
     "「理容所・美容所・クリーニング所の施設一覧について」"
     "（[https://data.city.kyoto.lg.jp/dataset/00530/](https://data.city.kyoto.lg.jp/dataset/00530/)）"
     "（京都市、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.ja)）を加工して作成. "
     "This project rebuilt the food register from the 2021 list and the monthly lists, keeping permits "
     "in term on 31 July 2026, selected the storefront permit types, placed each premises by its "
     "address, and counted them around stations. Closures are not published, so the lists may include "
     "premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). Kyoto City and MLIT did not make and do not "
     "endorse this map.",
     False),
    # Tokyo (notice 56): eight wards, each its own publisher, each credited in
    # the form its own terms prescribe - BUILT from pipeline/tokyo/credits.py,
    # which check_provenance.py holds to the roster (every file the build reads
    # has a credit). MHLW as in Fukuoka's; MLIT as in Kobe's. Wording approved
    # by the owner 2026-09-28.
    ("Tokyo's wards, MHLW and MLIT (Tokyo)",
     "Tokyo's businesses: " + tokyo_credits.notice() + ". "
     "Processed by this project, which selected the storefront types, showed a premises in both a ward's "
     "list and the national filings once, placed each by its address, and counted them around stations. "
     "The national filings are not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. The wards, the Tokyo Metropolitan Government, MHLW and MLIT did not make and do not endorse "
     "this map.",
     False),
    # Yokohama (notice 75): the city's registers are CC BY 4.0 (the dataset
    # page and the city's open-data terms, read 2026-09-30), and the city
    # prescribes the credit for a modified work: 「この地図は、以下の著作物を改変
    # して利用しています。」, the title with its date, 神奈川県横浜市, and the licence
    # with its link. MUST NOT: present the map as the city's work, or imply its
    # endorsement. MLIT as in Kobe's. Written under the owner's pre-approval of
    # this build's prose (2026-09-30).
    ("Yokohama City and MLIT (Yokohama)",
     "Yokohama's businesses: この地図は、以下の著作物を改変して利用しています。"
     "環境衛生関係施設一覧（理容所・美容所・クリーニング所施設一覧、令和８年４月１日現在）、神奈川県横浜市"
     "（[https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.html](https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.html)）、"
     "クリエイティブ・コモンズ・ライセンス 表示4.0 国際"
     "（[https://creativecommons.org/licenses/by/4.0/deed.ja](https://creativecommons.org/licenses/by/4.0/deed.ja)）. "
     "(This map modifies the City of Yokohama's lists of barbers, beauty salons and laundries as of "
     "1 April 2026, used under CC BY 4.0: this project selected the premises with a fixed place, placed "
     "each by its address, and counted them around stations.) The lists may include premises that have "
     "closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Yokohama and MLIT did not make "
     "and do not endorse this map.",
     False),
    # Berlin (notice 57): VBB's GTFS, CC BY 4.0 per VBB's own dataset page -
    # the requested credit, the licence link, what was modified, the
    # disclaimer, no endorsement. IHK Berlin's register is CC0 and needs no
    # notice (its courtesy credit is on the Berlin page). Wording approved by
    # the owner 2026-09-28.
    ("VBB Verkehrsverbund Berlin-Brandenburg (Berlin)",
     "Station locations and line geometry for Berlin are from VBB Verkehrsverbund "
     "Berlin-Brandenburg GmbH's timetable data (GTFS), used under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by this project: "
     "U-Bahn and S-Bahn stations were selected and those outside the Land of Berlin removed, "
     "one timetable shape was chosen per line, and the lines are drawn in this project's "
     "colours. VBB provides the data without warranty and does not endorse this map.",
     False),
    # London (notice 58): the FSA's FHRS data under OGL v3 - the OGL statement linked, the
    # data date, what was modified, no endorsement. The credit avoids "the FHRS
    # name" (the FSA's imagery terms). Wording approved by the owner 2026-09-28.
    ("Food Standards Agency (London)",
     "London's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted between 2026-09-09 and 2026-09-16. Contains public sector information "
     "licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's centre, or left out where they have no "
     "full postcode, and trade "
     "names shown where a business is registered under another name. No hygiene rating is "
     "shown. The Food Standards Agency does not endorse this map.",
     False),
    # London's postcode centroids (notice 59): Ordnance Survey's OGL v3 data -
    # the three statements verbatim from the licence file OS ships with it
    # (Doc/licence.txt, which OS's own terms name as the authority), the
    # licence link, no endorsement. The product's registered name is not used
    # (trademarks are outside the OGL). Wording approved by the owner 2026-09-28.
    ("Ordnance Survey (London)",
     "Where the Food Standards Agency lists a London food business without a map point, it is "
     "placed at the centre point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False),
    # Buenos Aires (notice 60): BA Data's three datasets under CC BY 2.5 AR -
    # author units, dataset titles and URIs, the licence URI, how the data was
    # changed, no endorsement, no GCBA or BA Data logo. Written to satisfy 2.5 AR
    # and 4.0 both (Parcelas' resources say 4.0). Approved by the owner 2026-09-28.
    ("Gobierno de la Ciudad de Buenos Aires (Buenos Aires)",
     "Buenos Aires' storefronts are from the [Relevamiento Usos del Suelo 2022-2024]"
     "(https://data.buenosaires.gob.ar/dataset/relevamiento-usos-suelo) (Dirección General de "
     "Antropología Urbana, Subsecretaría de Planeamiento), placed using "
     "[Parcelas](https://data.buenosaires.gob.ar/dataset/parcelas) (Subsecretaría de Registro, "
     "Interpretación y Catastro), and the Subte's stations and lines are from "
     "[Subte: Estaciones](https://data.buenosaires.gob.ar/dataset/subte-estaciones) "
     "(Subterráneos de Buenos Aires, SBASE), all published by the Gobierno de la Ciudad de "
     "Buenos Aires on BA Data under the [Creative Commons Attribution 2.5 Argentina licence]"
     "(http://creativecommons.org/licenses/by/2.5/ar/). Modified by this project: filtered to "
     "storefronts, grouped into three categories, and placed at the centre of each parcel, or "
     "of its block where the parcel is not listed; station names follow OpenStreetMap's "
     "spelling. The Gobierno de la Ciudad de Buenos Aires does not endorse this map.",
     False),
    # Glasgow (notice 61): Scotland's FHIS data, run by Food Standards Scotland and
    # published in the FSA's open-data files, under OGL v3 (FSS states v3 itself) - the
    # OGL statement linked, the extract date, what was modified, no endorsement by either
    # body. Never "FHRS": FHIS is a separate scheme. Wording approved by the owner 2026-09-28.
    ("Food Standards Scotland (Glasgow)",
     "Glasgow's food businesses are from Food Standards Scotland, Food Hygiene Information "
     "Scheme data, via the Food Standards Agency, extracted on 2026-09-14. Contains public "
     "sector information licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected; premises without a location, at a flat address "
     "or registered as a childminder left out; trade names shown where a business is "
     "registered under another name. No inspection result is shown. Neither Food Standards "
     "Scotland nor the Food Standards Agency endorses this map.",
     False),
    # Newcastle (notice 62): the FSA's FHRS data for the five Tyne and Wear councils,
    # London's credit and conditions (England, FHRS). Wording approved by the owner
    # 2026-09-28.
    ("Food Standards Agency (Newcastle)",
     "Newcastle's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted between 2026-09-09 and 2026-09-16. Contains public sector information "
     "licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's centre, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False),
    # Newcastle's postcode centroids (notice 63): London's Ordnance Survey notice, the
    # same file and edition. Wording approved by the owner 2026-09-28.
    ("Ordnance Survey (Newcastle)",
     "Where the Food Standards Agency lists a Newcastle food business without a map point, it "
     "is placed at the centre point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False),
    # Sydney (notice 64): the City of Sydney's FES under CC BY 4.0 - creator and
    # copyright holder, the licence and the dataset linked, modification noted, the
    # warranty disclaimer, no endorsement (licence-read 2026-09-28; no wording is
    # prescribed). Wording approved by the owner 2026-09-28.
    ("City of Sydney (Sydney)",
     "Business establishment locations: City of Sydney, Floor Space and Employment Survey 2022 "
     "([FES Industry of occupation](https://www.arcgis.com/home/item.html?id="
     "77ac8aa96bd34bacb881cfe8e5358ba0)), © City of Sydney, licensed under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by this project "
     "(filtered and grouped by category); provided as is, without warranty. The City of Sydney "
     "does not endorse this map.",
     False),
    # Melbourne (notice 65): the City of Melbourne's CLUE under CC BY 4.0 - the credit,
    # the licence and the dataset linked, the modification noted, no endorsement
    # (licence-read 2026-09-28; no wording is prescribed). Wording approved by the
    # owner 2026-09-28.
    ("City of Melbourne (Melbourne)",
     "Business establishments: City of Melbourne, Census of Land Use and Employment (CLUE) 2024 "
     "([dataset](https://data.melbourne.vic.gov.au/explore/dataset/"
     "business-establishments-with-address-and-industry-classification/)), "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Filtered, categorised and "
     "aggregated by this project. The City of Melbourne does not endorse this map.",
     False),
    # Stockholm (notice 66): Stockholms stad's Livsmedelstillsyn register. Its licence
    # is SILENT (no licence on the item; the publisher's own Hub feed says public, with
    # CC0 on 8 of 109 datasets but not this one), so the notice credits the publisher
    # and states the changes without claiming a licence. Wording approved by the
    # owner 2026-09-29.
    ("Stockholms stad (Stockholm)",
     "Food premises for Stockholm are from the City of Stockholm's food inspection "
     "register (Livsmedelstillsyn, Stockholms stad, miljöförvaltningen, "
     "[open-data-sthlm-miljo.hub.arcgis.com](https://open-data-sthlm-miljo.hub.arcgis.com/)), "
     "which the city publishes as public open data with no stated licence. Changes: the "
     "inspections are reduced to one record per premises, filtered to restaurants, cafés, "
     "bars and food shops, grouped into two categories, and mapped by distance to "
     "Tunnelbana stations. This is not the official register, and it is not produced or "
     "endorsed by Stockholms stad.",
     False),
    # Bucharest (notice 67): DSVSA București's registers. Licence SILENT (no terms page; the ANSVSA
    # footer's "all rights reserved" covers the website), so the notice credits the
    # publisher and states the changes without claiming a licence. Wording approved
    # by the owner 2026-09-29.
    ("DSVSA București (Bucharest)",
     "Food premises for Bucharest are from the registers of the Sanitary-Veterinary and "
     "Food Safety Directorate of Bucharest (DSVSA București, "
     "[bucuresti.dsvsa.ro](https://bucuresti.dsvsa.ro/)), which it publishes with no stated "
     "licence. Changes: cancelled registrations are left out; the units are filtered to "
     "restaurants, cafés, bars and food shops, merged where one premises holds several "
     "registrations, grouped into two categories, placed by matching their addresses to "
     "OpenStreetMap's address points, and mapped by distance to metro stations. Company "
     "names are shown without their legal form, and sole traders by category only. This is "
     "not the official register, and it is not produced or endorsed by DSVSA or ANSVSA.",
     False),
    # SEMAS's 상가(상권)정보 (notice 68): data.go.kr 15083033, 이용허락범위 제한 없음. licence-read
    # 2026-09-29: PERMITTED WITH CONDITIONS - a source credit, no distortion of the
    # facts (so the categories are stated as this project's), SEMAS's website copyright
    # policy read as covering its homepage (owner, 2026-09-29, Daegu's reading). Written
    # under the owner's pre-approval of this build's prose. Covers every Korean city on
    # the register (Incheon; the Gyeonggi satellites add their names).
    ("Small Enterprise and Market Service (Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon)",
     "Storefronts for Incheon, Goyang, Seongnam, Yongin, Suwon and Bucheon are from the Small "
     "Enterprise and "
     "Market Service's "
     "commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via 공공데이터포털 "
     "[data.go.kr](https://www.data.go.kr/data/15083033/fileData.do)), "
     "이용허락범위 제한 없음. Changes: filtered to shops, food and drink and personal services, "
     "grouped into three categories, and mapped by distance to stations; the categories and "
     "counts are this project's, not SEMAS's. Not produced or endorsed by SEMAS.",
     False),
    # Ottawa: Ottawa Public Health's food-safety inspection feed and the City's
    # 2022-2026 wards, both under the Open Government Licence - City of Ottawa
    # v2.0 (the items' licenseInfo, read 2026-09-29). Its attribution sentence is
    # PRESCRIBED and is reproduced VERBATIM, with the en dash, linked to the
    # licence; the credit names Ottawa Public Health / City of Ottawa. The
    # licence bars implying official status or endorsement and using the City's
    # or OPH's names as marks. Written under the owner's pre-approval of this
    # build's prose (2026-09-29).
    ("City of Ottawa (Ottawa)",
     "Contains information licensed under the [Open Government Licence – City of "
     "Ottawa](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0). "
     "Food premises for Ottawa are from Ottawa Public Health / City of Ottawa's public health "
     "inspection data (food safety), and the city boundary from the City's 2022-2026 wards. "
     "Changes: the premises are limited to those inspected in the last two years, "
     "institutional kitchens, clubs, mobile vendors and hotels are left out by name, and the "
     "rest are mapped by distance to O-Train stations; inspection results are not shown. This "
     "is not an official City of Ottawa or Ottawa Public Health product, and it is not "
     "endorsed by either.",
     False),
]

# The owner's branding decision (2026-09-21): keep each agency's official route
# colours and real line names, and say plainly that this is not affiliated with
# them. That is what those clauses actually prohibit - MTS, LA Metro, CTA, MTA,
# SEPTA and WMATA all bar stating or implying affiliation, sponsorship or
# endorsement, and WMATA's also names "confusingly similar variants". Nothing
# here reproduces a logo, wordmark or route-bullet artwork.
_NON_AFFILIATION = (
    "This is an independent project. It is not affiliated with, sponsored by "
    "or endorsed by any transit agency or city government named here. Line "
    "names and route colours are used only to identify each line as its "
    "riders know it. No agency logo, wordmark or route symbol is reproduced."
)

# Two cities' sources neither grant nor forbid reuse, and this says so on the
# page rather than waiting on third parties to answer. The owner's decision
# (2026-09-21): disclose the gap alongside the attributions, and commit in
# advance to removing a city if its publisher's position turns out not to
# permit this use.
#
# That last part is BROADER than the standing removal commitment in
# docs/data_sources.md, which triggers on a publisher *asking*. This one
# triggers on finding out - no request needed. Keep the wording here
# consistent with that document and with docs/excluded_categories.md; all
# three are meant to say the same thing.
_UNSETTLED_TERMS = (
    "**One city rests on terms that are unresolved, and that is stated rather "
    "than glossed.** Philadelphia's business licences and city limits carry "
    "the “City of Philadelphia License”, which reserves the City's "
    "rights without granting any — and the dataset page also binds a "
    "reader to the City's separate Terms of Use, which permit residents to "
    "print single pages of the City's website and otherwise state that "
    "“distribution or republication in any other form or for any other "
    "purpose … and any modification whatsoever, are strictly prohibited "
    "without the prior written permission of the City”. Read literally "
    "and applied to a dataset, that would not permit this map, which filters "
    "and redraws what it publishes. Read as what it appears to be — terms "
    "written for web pages, sitting beside a dataset licence that contains no "
    "such prohibition, under an Open Data Program whose purpose is public "
    "reuse — it would. **That question is open, it has not been resolved "
    "in this project's favour, and if the City confirms the restrictive "
    "reading Philadelphia comes off this site** — the same way a request "
    "about a single listing is honoured rather than argued. A written request "
    "for the City's position was sent on 21 September 2026. Whatever comes "
    "back, silence will not be treated as permission."
)

# MTA's terms and WMATA's §6 both forbid stating or implying that the data an
# application provides is "accurate, complete, or timely". This sentence is the
# positive form of that: it says what the maps ARE.
_AS_RECORDED = (
    "Every map here is a snapshot of a public register as it stood on the "
    "retrieval date recorded for that source, redrawn and filtered. Registers "
    "lag the street: a shop that closed last month may still appear, and one "
    "that opened last month may not. Read each map as what a city's own "
    "licence records showed on that date, not as a census of what is open."
)


def render_site_notices(show_links: bool = True):
    """The site-level footer: the three reference pages, then every notice that
    publishing these maps requires.

    Called from EVERY page. See _NOTICES above for why a single city page
    carrying its own credit does not discharge these.
    """
    st.divider()
    if show_links:
        with st.container(horizontal=True, gap="medium",
                          vertical_alignment="center"):
            st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")
            st.page_link(EXCLUSIONS_PAGE, label="What is counted, and what is not")
            st.page_link(DIFFERENCES_PAGE, label="Why the maps differ")
    st.caption(_AS_RECORDED)
    st.caption(_NON_AFFILIATION)

    # NOT in an st.expander, and that was a real mistake worth naming: these
    # were briefly collapsed behind one, which kept them out of the DOM until
    # a reader clicked. Chicago's terms require its paragraph "at the site
    # where the software application ... can be accessed", and this project's
    # own rule for the OSM attribution is that it must not sit "beneath UI,
    # behind toggles, or off-screen". A required notice behind a toggle is not
    # displayed. So they render inline, always, in small type.
    st.caption(
        "**Required source notices.** Reproduced as each source's terms "
        "require. Full provenance, with endpoints and retrieval dates, is on "
        "the \u201cWhere this data comes from\u201d page."
    )
    for heading, text, verbatim in _NOTICES:
        st.caption(f"**{heading}** \u2014 {text}")
    st.caption(
        "**OpenStreetMap** \u2014 basemap \u00a9 OpenStreetMap contributors, "
        "available under the Open Database License. The attribution also "
        "appears in the corner of every map, where its licence requires it to "
        "stay visible. The overview map's basemap is \u00a9 CARTO."
    )
    st.caption(_UNSETTLED_TERMS)
