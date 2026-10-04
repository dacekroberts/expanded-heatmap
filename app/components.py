"""Small pieces of UI shared across pages.

Streamlit's multipage app has no shared layout/header mechanism of its own -
each page is its own top-to-bottom script - so anything meant to appear
identically on every page lives here once and gets called from each page,
rather than duplicated per page.
"""

import sys
from pathlib import Path
from typing import NamedTuple

import streamlit as st

from cities import CITIES, MAP_ONLY_NAV, SWITCHER_ORDER
from osm_notice import OSM_RAIL_BY_CITY, osm_rail_text

sys.path.insert(0, str(Path(__file__).parent.parent))
# pipeline/theme.py imports nothing, so it is safe for the lean deploy venv
# (streamlit + pandas only) - the same rule the city pages' config imports
# follow. It is the single source for every chrome colour, shared with the city
# maps' own CSS so a reskin cannot leave the macro map on the old palette.
from pipeline.theme import AMBIENT_THEME_JS, DARK, LIGHT, STREAMLIT_DARK, rgba  # noqa: E402
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

# The teal frame around every map, the city maps' embeds and the macro map
# alike (owner, 2026-10-02: a 3 px muted teal ring, a faint teal halo and
# glow, 8 px corners). Box-shadows only, so the map keeps its exact size: a
# city map's 650 px height is what keeps the OSM credit on screen
# (scripts/check_map_attribution.js), and a shadow adds no scrollable width
# at 375 px. The ring is each theme's teal mixed 45% into its page color; the
# halo and glow are the same teal at low alpha.
#
# light-dark() follows the PAGE's Streamlit theme, so the shadow goes on an
# element that inherits the page's color-scheme: Streamlit sets
# `color-scheme: normal` on the st.iframe element itself, where light-dark()
# always resolved to the light value (measured 2026-10-02). The first
# declaration is the fallback for a browser without light-dark() or
# color-mix(), which drops the second whole.
_FRAME_TEAL_DARK = STREAMLIT_DARK["primaryColor"]   # the page accent, not the maps'
MAP_FRAME_CSS = (
    f"box-shadow: 0 0 0 3px {rgba(LIGHT['accent'], 0.5)};"
    "box-shadow: 0 0 0 3px light-dark("
    f"color-mix(in srgb, {LIGHT['accent']} 45%, {LIGHT['page']}), "
    f"color-mix(in srgb, {_FRAME_TEAL_DARK} 45%, {DARK['page']})), "
    f"0 0 0 7px light-dark({rgba(LIGHT['accent'], 0.10)}, {rgba(_FRAME_TEAL_DARK, 0.10)}), "
    f"0 12px 32px -8px light-dark({rgba(LIGHT['accent'], 0.30)}, {rgba(_FRAME_TEAL_DARK, 0.18)});"
    "border-radius: 8px;"
)

_MACRO_THEME_CSS = """
<style>
/* The teal map frame (MAP_FRAME_CSS); overflow clips the map to its corners. */
[data-testid="stDeckGlJsonChart"] { position: relative; overflow: hidden; @@FRAME@@ }
#macro-theme-toggle {
    position: absolute; top: 10px; right: 52px; z-index: 20;
    font: 600 13px sans-serif; padding: 6px 12px; cursor: pointer;
    background: @@LIGHT_SURFACE@@; color: @@LIGHT_TEXT@@;
    border: 1px solid @@LIGHT_BORDER@@;
    /* The only color here deliberately left outside pipeline/theme.py: a
       black drop shadow is theme-agnostic, and it simply stops mattering on a
       dark surface rather than looking wrong. Same value in map_common.py. */
    border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
#macro-theme-toggle:focus-visible { outline: 2px solid @@LIGHT_ACCENT@@; outline-offset: 2px; }
body.dark-base #macro-theme-toggle { background: @@DARK_SURFACE@@; color: @@DARK_TEXT@@;
    border-color: @@DARK_BORDER@@; }
body.dark-base #macro-theme-toggle:hover { background: @@DARK_SURFACE_HOVER@@; }
/* Only the basemap canvas is filtered; the markers and labels are a separate
   canvas, so they keep their colors. Same filter as the city maps. */
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
    // CLAUDE.md: the OSM credit links to the OSM COPYRIGHT page, and CARTO's
    // terms send its credit to carto.com/attribution/. app/basemap.py writes
    // both into the style's own credit; CARTO's TileJSON carries /about/ and
    // /about-carto/ instead, so this guard corrects either href on every
    // re-render should that credit ever reach the map. Only the href changes -
    // the text and the credit stay Mapbox's.
    var OSM_COPYRIGHT = 'https://www.openstreetmap.org/copyright';
    var CARTO_ATTRIBUTION = 'https://carto.com/attribution/';
    function fixCredit() {
        var links = doc.querySelectorAll('[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a');
        for (var i = 0; i < links.length; i++) {
            if (/openstreetmap[.]org/.test(links[i].href) && links[i].href !== OSM_COPYRIGHT) {
                links[i].href = OSM_COPYRIGHT;
            }
            if (/(^|[/.])carto[.]com/.test(links[i].href) && links[i].href !== CARTO_ATTRIBUTION) {
                links[i].href = CARTO_ATTRIBUTION;
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
   the compact behavior is overridden rather than accepted.

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
   the TEXT color in light mode, not the accent: the teal accent is ~3.7:1 on
   white. check_macro_attribution.mjs measures all of this at 4.5:1. */
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib { background: @@LIGHT_SURFACE@@ !important; color: @@LIGHT_MUTED@@; }
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a { color: @@LIGHT_TEXT@@; }
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib { background: @@DARK_ATTRIB_BG@@ !important; color: @@DARK_MUTED@@; }
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a { color: @@DARK_ACCENT@@; }
/* deck.gl's tooltip is an HTML overlay (class `deck-tooltip`), so unlike the
   marker and label layers it CAN be themed. pydeck writes its colors inline
   from the `tooltip` style dict, hence !important. Without this the macro
   map's tooltip stayed the light-mode green-gray while every city map's
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
        .replace("@@FRAME@@", MAP_FRAME_CSS)
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
    keeps a wide table from squashing its columns before it scrolls. Colors
    are left to the theme, with a gray rule that reads in both.
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


# The header's two links, on every page because every page calls
# set_base_font() (owner, 2026-10-03; both URLs confirmed by the owner). The
# GitHub one also links the public repository from the page header, which IDFM's
# Licence Mobilités Art. 5.8 and ODbL s.4.6 lean on (the footer link stays).
# Inline SVG, no icon font or CDN: GitHub's mark is Octicons' mark-github (MIT),
# LinkedIn's the Simple Icons glyph (CC0). One line, so Markdown wraps no part
# of it in a paragraph.
_GITHUB_URL = "https://github.com/dacekroberts/expanded-heatmap"
_LINKEDIN_URL = "https://www.linkedin.com/in/dace-roberts-57381b279/"
_HEADER_LINKS_HTML = (
    '<div class="site-header-links">'
    f'<a href="{_GITHUB_URL}" target="_blank" rel="noopener noreferrer" '
    'aria-label="Code on GitHub (opens in a new tab)" title="Code on GitHub">'
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M8 0C3.58 '
    '0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49'
    '-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
    '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64'
    '-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32'
    '-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56'
    '.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 '
    '2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></a>'
    f'<a href="{_LINKEDIN_URL}" target="_blank" rel="noopener noreferrer" '
    'aria-label="LinkedIn profile (opens in a new tab)" title="LinkedIn">'
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.447 '
    '20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 '
    '2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 '
    '2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92'
    '-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 '
    '13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 '
    '24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>'
    '</svg></a></div>'
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

        /* A markdown table wider than the column scrolls inside its own box
        instead of widening the page: the French table on What Is Excluded
        (474 px in a 375 px viewport) and About the Data's tables (about
        2,800 px) pushed the whole page sideways on a phone (review lane 3,
        2026-09-30). scroll_table() does the same for tables built in code;
        this covers the ones the docs carry. */
        [data-testid="stMarkdownContainer"] table {
            display: block;
            overflow-x: auto;
            max-width: 100%;
        }

        /* The GitHub and LinkedIn links (_HEADER_LINKS_HTML), in the left end
        of Streamlit's own header strip. The right end holds Streamlit's
        toolbar (and, run locally, its Deploy button, which overlapped them
        there); the left end is empty while cities.MAP_ONLY_NAV hides the
        sidebar's expand control, and turning that off puts the control back
        in this corner, so move the links then. The element container itself
        is fixed, so it leaves the page's flow: it adds no gap above a city's
        title and pushes neither the title nor the map down. Above the header
        (z-index 999990). Icons take the theme's text color through
        currentColor, so they follow the light and dark themes. */
        [data-testid="stElementContainer"]:has(.site-header-links) {
            position: fixed !important;
            top: 0.85rem;
            left: 0.75rem;
            width: auto !important;
            z-index: 999991;
            margin: 0 !important;
        }
        .site-header-links { display: flex; gap: 0.15rem; align-items: center; }
        .site-header-links a {
            display: inline-flex; padding: 0.35rem; border-radius: 6px;
            color: inherit !important; opacity: 0.7; line-height: 0;
        }
        .site-header-links a:hover { opacity: 1; }
        .site-header-links a:focus-visible {
            opacity: 1; outline: 2px solid currentColor; outline-offset: 1px;
        }
        .site-header-links svg { width: 20px; height: 20px; fill: currentColor; }

        /* A city page's subtitle (render_city_title), set close under the
        city's name and quieter than it. */
        .st-key-city-title h1 { padding-bottom: 0.1rem; }
        .st-key-city-title p.city-subtitle {
            margin: 0;
            font-size: 1.05rem;
            opacity: 0.75;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if MAP_ONLY_NAV:
        # A separate call, not appended to the block above: that block is indented,
        # so text added after it is rendered as a Markdown code block.
        st.markdown(f"<style>{_MAP_ONLY_CSS}</style>", unsafe_allow_html=True)
    # Its own element and no <style> in it: render_city_title hides every
    # element container holding a <style>, which would hide the links too.
    st.markdown(_HEADER_LINKS_HTML, unsafe_allow_html=True)


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
ABOUT_DATA_PAGE = "pages/About_the_Data.py"
EXCLUSIONS_PAGE = "pages/What_Is_Excluded.py"
DIFFERENCES_PAGE = "pages/Why_the_Maps_Differ.py"
REPO_URL = "https://github.com/dacekroberts/expanded-heatmap"
NOTICES_PAGE = "pages/Required_Notices.py"


class Notice(NamedTuple):
    """One required source notice.

    number: its item in docs/data_sources.md's numbered list (two entries may
        share one: OpenStreetMap's basemap line and its rail-geometry line).
    cities: the city pages it is shown on, spelled exactly as app/cities.py
        spells them; scripts/check_provenance.py check N holds each to a real
        city.
    every_page: shown on every page as well, for a reason recorded beside the
        entry; check N pins that set to the owner's approval.
    per_city: a function giving the text a city's OWN page shows in place of
        `text`, which the Required notices page keeps whole (owner,
        2026-10-03: OpenStreetMap's rail notice, app/osm_notice.py).
    """
    number: int
    heading: str
    text: str
    verbatim: bool
    cities: tuple
    every_page: bool = False
    per_city: object = None


# Groups of cities one notice covers, spelled as app/cities.py spells them.
_MEXICO = ("Mexico City", "Guadalajara (Regional)", "Monterrey (Regional)")
_NORWAY = ("Oslo", "Bergen")
_DENMARK = ("Copenhagen", "Aarhus", "Odense")
_CZECHIA = ("Prague", "Brno", "Plzeň", "Olomouc", "Ostrava",
            "Liberec (Regional)", "Most (Regional)")
_BRAZIL = ("São Paulo", "Rio de Janeiro (Regional)", "Belo Horizonte (Regional)", "Brasília",
           "Salvador", "Fortaleza (Regional)", "Porto Alegre (Regional)",
           "Recife (Regional)", "Santos (Regional)")
_KOREA_SEMAS = ("Incheon", "Goyang", "Seongnam", "Yongin", "Suwon", "Bucheon",
                "Namyangju", "Ansan", "Uijeongbu", "Anyang")
_FRANCE = ("Paris", "Marseille", "Toulouse", "Lille (Regional)", "Rennes",
           "Le Mans", "Besançon", "Avignon", "Tours", "Dijon", "Reims", "Orléans",
           "Mulhouse", "Brest", "Saint-Étienne", "Nice", "Montpellier",
           "Strasbourg", "Le Havre", "Caen", "Rouen (Regional)",
           "Bordeaux (Regional)", "Nantes (Regional)", "Grenoble (Regional)",
           "Valenciennes (Regional)", "Angers")
# The UK tram and light-rail cities whose gate 3 reads NaPTAN (notice 86),
# and Merseyrail's, whose gate 3 reads NaPTAN's rail records.
_UK_SIX = ("Manchester (Regional)", "Birmingham (Regional)", "Edinburgh",
           "Sheffield", "Nottingham (Regional)", "Blackpool (Regional)")
_UK_NAPTAN = (*_UK_SIX, "Liverpool (Regional)")
# Every city the OpenStreetMap rail-geometry entry names, in its order. Adding
# a city to that sentence means adding it here, or its page omits the line.
_OSM_RAIL = (
    "Mexico City", "Guadalajara (Regional)", "Monterrey (Regional)",
    "Barcelona", "Lille (Regional)", "Oslo", "Bergen", "Copenhagen", "Aarhus",
    "Kitchener–Waterloo (Regional)", "Odense", "Liepāja", "Daugavpils",
    "Buffalo", "Sacramento", "Houston", "Ottawa", "Minneapolis", "Pittsburgh",
    "Dallas", "Kansas City", "Tucson", "New Orleans", "Florence", "Den Haag",
    "Göteborg", "Zurich", "Rome", "Palma", "Brno", "Plzeň", "Olomouc",
    "Ostrava", "Liberec (Regional)", "Most (Regional)", *_BRAZIL, "Prague",
    "Amsterdam", "Rotterdam", "Hong Kong", "Seoul", "Taichung", "Taoyuan",
    "Taipei (Regional)", "Daegu", "Busan", *_KOREA_SEMAS, "Sydney", "Melbourne",
    "Buenos Aires", "Seattle (Regional)", "London", "Glasgow",
    "Newcastle (Regional)", "Manchester (Regional)", "Birmingham (Regional)",
    "Edinburgh", "Sheffield", "Nottingham (Regional)", "Blackpool (Regional)",
    "Liverpool (Regional)", "Stockholm", "Bucharest", "Tbilisi", "Montpellier", "Strasbourg",
    "Le Havre", "Caen", "Rouen (Regional)", "Philadelphia",
)
# The cities whose rail is not OpenStreetMap's but whose English station names
# are (the twenty Japanese cities: MLIT N02 lines, OSM `name:en`). Kept apart
# from _OSM_RAIL so only rail-geometry cities get the rail wording; notice 1's
# sentence names these in a clause of their own, in this order.
_OSM_STATION_NAMES = (
    "Kobe", "Osaka", "Sapporo", "Fukuoka", "Kyoto", "Tokyo", "Yokohama",
    "Hiroshima", "Matsuyama", "Toyama", "Kumamoto", "Fukui", "Nagasaki",
    "Utsunomiya", "Kitakyushu", "Sakai", "Hakodate", "Kagoshima", "Okayama",
    "Kōchi",
    # Japan wave 2 (2026-10-03)
    "Kawasaki", "Yokosuka", "Himeji", "Nishinomiya", "Takamatsu", "Toyota", "Yokkaichi", "Ōtsu", "Nara",
    "Hamamatsu", "Higashiōsaka", "Kurume", "Sasebo", "Shimonoseki",
)

# Verbatim where verbatim is required. Each entry is a Notice, and the sources
# are recorded in docs/data_sources.md, "Notices this project MUST display
# when published" - read that before editing any of these.
#
# THESE ARE OBLIGATIONS, NOT CREDITS. Chicago's terms require its paragraph
# "at the site where the software application ... can be accessed", and
# SFMTA's licence requires its sentence in derivative works, so both are
# reproduced word for word and must not be paraphrased, trimmed or summarised.
# LA Metro's and MassDOT's prescribe no wording, only that they be
# acknowledged as the provider, so those two are this project's own phrasing.
#
# WHERE EACH ONE SHOWS (owner, 2026-10-02). Every notice is on its own
# city's page, inline and in full, and every notice is on the Required notices
# page (NOTICES_PAGE) in number order; every page links there. Five are on
# every page as well (every_page=True), for the reason given beside each:
# Chicago (2) and Kansas City (80), whose terms name the SITE; LA Metro (4),
# whose placement is set by guidelines that could not be read; INEGI (8) and
# Barcelona (21), whose disclosure duties may reach the Overview's derived
# figures. Ordnance Survey's notices moved off the other pages on the OGL's
# "including or linking to": each UK page shows its three statements in full
# and every page links to the full list. The per-notice evidence is in this
# branch's decisions draft, docs/decisions_drafts/nice-boyd-51dea8.md.
_NOTICES = [
    # The basemap credit, on every page: ODbL 1.0 wants it visible, and the
    # Overview's and every city's map carry it in their corners as well.
    Notice(1, "OpenStreetMap",
           "basemap © OpenStreetMap contributors, available under the "
           "Open Database License. The attribution also appears in the corner "
           "of every map, where its license requires it to stay visible. The "
           "overview map's basemap is © CARTO and © OpenMapTiles, from "
           "OpenStreetMap data. "
           # Approved by the owner, 2026-10-02: CARTO's terms (s10) make the
           # site the controller of the request data CARTO receives.
           "The overview map's basemap loads from CARTO, so your browser sends "
           "CARTO your IP address and browser details with each map request; "
           "CARTO processes them for this site.",
           False, (), every_page=True),
    Notice(2, "City of Chicago",
     "This site provides applications using data that has been modified for "
     "use from its original source, www.cityofchicago.org, the official "
     "website of the City of Chicago. The City of Chicago makes no claims as "
     "to the content, accuracy, timeliness, or completeness of any of the "
     "data provided at this site. The data provided at this site is subject "
     "to change at any time. It is understood that the data provided at this "
     "site is being used at one's own risk.",
     True, ("Chicago",), every_page=True),
    # SFMTA (notice 3), re-read 2026-10-03 against sfmta.com/reports/
    # gtfs-transit-data (updated 2024-10-01) and the stored copy in
    # docs/licenses/. Clause 12's notice is BOTH paragraphs after "shall bear
    # the following notice:", the "as is" paragraph included; until
    # 2026-10-03 only the first was shown. Clause 4 asks for its liability
    # disclaimer to be displayed "or" included in a use agreement; the site
    # has no use agreement, and on the cautious reading the disclaimer is
    # displayed instead. All three quoted parts are verbatim; the lead-in to
    # the third is this project's.
    Notice(3, "San Francisco Municipal Transportation Agency",
     "Reproduced with permission granted by the City and County of San "
     "Francisco. The information has been provided by means of a "
     "nonexclusive, limited, and revocable license granted by the City and "
     "County of San Francisco. The City and County of San Francisco does not "
     "guarantee the accuracy, adequacy, completeness or usefulness of any "
     "information. The City and County of San Francisco provides this "
     "information \"as is,\" without warranty of any kind, express or implied, "
     "including but not limited to warranties of merchantability or fitness "
     "for a particular purpose, and assumes no responsibility for anyone's use "
     "of the information. SFMTA's license, under which this site is the "
     "Licensee, also asks for this disclaimer to be displayed: “The "
     "Licensee agrees that the SFMTA and its employees, officers, directors and "
     "agents shall not be liable for damages of any kind arising from the use "
     "of Data or any application that uses the Data including but not limited "
     "to direct, indirect, incidental, punitive and consequential, and or "
     "special damages.”",
     True, ("San Francisco",)),
    Notice(4, "LA Metro",
     "Rail alignment data for Los Angeles provided by LA Metro. This project "
     "claims no ownership of that data.",
     False, ("Los Angeles (Regional)",), every_page=True),
    # New York City (notice 5): Local Law 11 forbids a licence, but the Open
    # Data Technical Standards Manual reserves DoITT's right to require the
    # SOURCE, VERSION and MODIFICATIONS of a republished data set. Until
    # 2026-10-03 the reference pages were read as meeting it and nothing
    # displayed it; check C now holds every numbered notice to a display, so
    # the three are stated here, on the city's page. Not verbatim: the manual
    # prescribes the content, not a sentence.
    Notice(5, "New York City",
     "Source: NYC Open Data, the Department of Health and Mental Hygiene's "
     "Restaurant Inspection Results (43nn-pn8j), the Department of Consumer "
     "and Worker Protection's Issued Licenses (w7w3-xahh) and the Borough "
     "Boundaries (gthc-hcne). Version: as downloaded on September 21, 2026. "
     "Modifications: the inspection history is reduced to one row per "
     "restaurant and the licenses to active premises licenses; the businesses "
     "are filtered to storefront categories, grouped into three categories of "
     "this project's own and measured by distance from subway stations, and a "
     "business found in two registers is counted once.",
     False, ("New York",)),
    Notice(7, "MassDOT / MBTA",
     "Rail alignment data for Boston provided by MassDOT/MBTA.",
     False, ("Boston",)),
    Notice(6, "Chicago Transit Authority",
     "Data provided by Chicago Transit Authority.",
     False, ("Chicago",)),
    # Canada, added with Vancouver (2026-09-21). All three are VERBATIM.
    #
    # The two municipal notices use each city's OWN wording and are not
    # interchangeable - Vancouver's is "Licence" with an en dash, Surrey's is
    # "License" with a hyphen. Both licences TERMINATE AUTOMATICALLY on breach
    # ("if you fail to comply with any of them, the rights granted to you
    # under this licence... will end automatically"), so these are not
    # cosmetic.
    Notice(9, "City of Vancouver",
     "Contains information licensed under the Open Government "
     "Licence – Vancouver.",
     True, ("Vancouver (Regional)",)),
    Notice(10, "City of Surrey",
     "Contains information licensed under the Open Government License - "
     "City of Surrey.",
     True, ("Vancouver (Regional)",)),
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
    Notice(19, "Ayuntamiento de Madrid",
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
     True, ("Madrid",)),
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
    Notice(20, "CRTM (Consorcio Regional de Transportes de Madrid)",
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
     True, ("Madrid",)),
    Notice(11, "TransLink",
     "Route and arrival data used in this product or service is provided by "
     "permission of TransLink. TransLink assumes no responsibility for the "
     "accuracy or currency of the Data used in this product or service.",
     True, ("Vancouver (Regional)",)),
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
    Notice(17, "Province of British Columbia",
     "Contains information licensed under the Open Government "
     "Licence – British Columbia.",
     True, ("Vancouver (Regional)",)),
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
    Notice(12, "Ville de Montréal",
     "Contains data from the Ville de Montréal, used under the Creative "
     "Commons Attribution 4.0 International licence. The data has been "
     "modified and interpretations have been drawn from it: it is filtered to "
     "storefront categories, grouped into three categories of this project's "
     "own, and measured by distance from transit stations. The Ville de "
     "Montréal does not endorse this project or its use of the data.",
     False, ("Montréal",)),
    Notice(13, "Société de transport de Montréal",
     "Métro route geometry and station locations for Montréal are the "
     "property of the Société de transport de Montréal, used under the "
     "Creative Commons Attribution 4.0 International licence.",
     False, ("Montréal",)),
    # The REM, added 2026-09-27 with the tram rescope (notice 51). CC BY 4.0
    # from the licence file bundled in the feed, which names no licensor, so
    # the credit goes to the creator feed_info/agency.txt identify - not
    # Pulsar, which serves the file. The licence prescribes no wording; it
    # requires the credit, a statement of modification and a licence link, and
    # forbids implying endorsement (s.2(a)(6)) or using the logo (s.2(b)(2)).
    # Wording approved by the owner 2026-09-27.
    Notice(51, "Réseau express métropolitain",
     "REM route geometry and station locations for Montréal are from the "
     "Réseau express métropolitain (REM) GTFS feed, used under the "
     "[Creative Commons Attribution 4.0 International licence]"
     "(https://creativecommons.org/licenses/by/4.0/). The data has been "
     "modified: its three services are drawn as one line, stations outside "
     "the agglomeration are removed, and two stations are merged with the "
     "Métro stations of the same name. The Réseau express métropolitain does "
     "not endorse this project or its use of the data.",
     False, ("Montréal",)),
    # Calgary, added 2026-09-21. ONE notice covers BOTH the business register
    # and Calgary Transit's GTFS - the only Canadian city where a single
    # licence does both, so this city adds one line where Vancouver added
    # three and Montréal two.
    #
    # VERBATIM, and note the en dash and the British "Licence" - Surrey's
    # sibling notice uses a hyphen and "License", and they are not
    # interchangeable. Like Toronto's, Vancouver's and Surrey's, this licence
    # TERMINATES AUTOMATICALLY on breach.
    Notice(14, "City of Calgary",
     "Contains information licensed under the Open Government "
     "Licence – City of Calgary.",
     True, ("Calgary",)),
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
    Notice(16, "City of Toronto",
     "Contains information licensed under the Open Government "
     "Licence – Toronto.",
     True, ("Toronto",)),
    Notice(15, "City of Edmonton",
     "Contains datasets made publicly available by the City of Edmonton under "
     "its Open Data Terms of Use, at "
     "https://www.edmonton.ca/sites/default/files/public-files/documents/"
     "Web-version2.1-OpenDataAgreement.pdf — which govern any further use of "
     "them and are passed on without additional restriction. The data has been "
     "modified and interpretations drawn from it: it is filtered to storefront "
     "categories, grouped into three categories of this project's own, and "
     "measured by distance from transit stations. The City of Edmonton does "
     "not endorse this project or its use of the data.",
     False, ("Edmonton",)),
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
    Notice(73, "Region of Waterloo (Kitchener–Waterloo)",
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
     False, ("Kitchener–Waterloo (Regional)",)),
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
    Notice(8, "INEGI",
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
     False, _MEXICO, every_page=True),
    # Mexico City's RAIL geometry is OpenStreetMap rather than the operator's
    # feed, because every *.cdmx.gob.mx host is unreachable (see
    # pipeline/mexico_city/config.py). ODbL 1.0 attribution was already
    # satisfied for the basemap by every rendered map's "© OpenStreetMap
    # contributors"; this line exists so the credit visibly covers the LINE
    # GEOMETRY too, which is data rather than tiles.
    Notice(1, "OpenStreetMap (rail geometry)",
     "Rail route geometry and station locations for Mexico City (Metro CDMX "
     "and Tren Ligero), Guadalajara (Tren Ligero), Monterrey (Metrorrey, with "
     "the boundaries of its four municipios) and Barcelona (Metro de "
     "Barcelona, including its FGC lines and both funiculars), and the route "
     "geometry of Lille's two métro lines, the per-line colors of "
     "Oslo's T-bane and tram lines, the color of Bergen's Bybanen line 1, "
     "and Copenhagen's Metro and S-tog lines "
     "and stations and the municipal boundaries used to select them, "
     "Aarhus's Letbane L2 line and its stops, the municipal boundaries used to "
     "select them and the address points used to place its businesses, "
     "Kitchener–Waterloo's ION line and its stops, "
     "Odense's Letbane line and its stops, the municipal boundary used to "
     "select them and the address points used to place its businesses, "
     "Liepāja's tram line and its stops and the city boundary used to select "
     "them and its businesses, Daugavpils's tram lines and their stops and the "
     "city boundary used to select them and its businesses, "
     "Buffalo's NFTA Metro Rail line and its stations, "
     "Sacramento's SacRT Blue and Gold Lines and their stations, and the "
     "municipal boundaries used to select them, "
     "Houston's METRORail Red, Green and Purple Lines and their stations, "
     "Ottawa's O-Train Lines 1, 2 and 4 and their stations, "
     "Minneapolis's METRO Blue and Green Lines and their stations, "
     "Pittsburgh's PRT Red, Blue and Silver Lines and their stations, "
     "Dallas's DART Light Rail Red, Blue, Green and Orange Lines and their stations, "
     "Kansas City's KC Streetcar, Tucson's Sun Link and New Orleans's five "
     "streetcar lines and their stops, "
     "Florence's T1 and T2 tram lines and their stops and the comune boundaries "
     "used to select them and its businesses, "
     "Den Haag's fourteen HTM tram lines and their stops and the municipal "
     "boundaries used to select them and its businesses, "
     "Göteborg's tram lines 1 to 13 and their stops and the kommun boundaries "
     "used to select them and its businesses, "
     "Zurich's sixteen VBZ tram lines and their stops and the municipal "
     "boundaries used to select them and its businesses, "
     "Rome's metro and Roma–Viterbo urban lines and their stations, "
     "Palma's Metro M1 and its stations, and the municipal boundaries used to "
     "select them, "
     "Brno's tram lines and the tram lines and stops of Plzeň, Olomouc, Ostrava, "
     "Liberec and Jablonec nad Nisou, and Most and Litvínov, with those towns' "
     "boundaries, "
     "the metro, VLT and suburban lines and stations of São Paulo (with its "
     "CPTM Linha 9), Rio de Janeiro (its VLT and SuperVia lines), Belo "
     "Horizonte, Brasília, Salvador, Fortaleza, Porto Alegre, Recife and "
     "Santos, and those cities' município boundaries, and "
     "Prague's, Amsterdam's, Rome's and Rotterdam's city boundaries, Hong Kong's MTR and "
     "Light Rail lines and stations, and its boundary, Seoul's subway lines and stations and "
     "its boundary, the subway, light-rail and Korail lines and stations of Daegu, Busan, "
     "Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu and "
     "Anyang, and those cities' boundaries, the train and metro routes of Sydney and "
     "Melbourne and their City boundaries, Buenos Aires's Subte and Premetro routes and "
     "its boundary, Seattle's Link 1 and 2 Lines, "
     "the lines and stations of London's Underground, DLR, Elizabeth line and "
     "Overground, the Glasgow Subway, the Tyne and Wear Metro, Manchester "
     "Metrolink, West Midlands Metro, Edinburgh Trams, Sheffield Supertram, "
     "Nottingham Express Transit, the Blackpool Tramway and Merseyrail, and the boundaries "
     "used to select them, Stockholm's Tunnelbana lines and stations and its "
     "kommun boundaries, Bucharest's metro lines and stations and its city and "
     "sector boundaries, the Tbilisi Metro's lines and stations and the city's "
     "boundary, the tram and métro line geometry of Montpellier, Strasbourg, "
     "Le Havre, Caen and Rouen, the location of Philadelphia's 11th Street "
     "station, which is closed for works and not drawn, "
     "the routes of Taichung's Green Line and Taoyuan's Airport MRT, the "
     "English station names, though not the lines or boundaries, of Kobe, "
     "Osaka, Sapporo, Fukuoka, Kyoto, Tokyo, Yokohama, Hiroshima, Matsuyama, "
     "Toyama, Kumamoto, Fukui, Nagasaki, Utsunomiya, Kitakyushu, Sakai, "
     "Hakodate, Kagoshima, Okayama, Kōchi, Kawasaki, Yokosuka, Himeji, "
     "Nishinomiya, Takamatsu, Toyota, Yokkaichi, Ōtsu, Nara, Hamamatsu, "
     "Higashiōsaka, Kurume, Sasebo and Shimonoseki, and the "
     "metro and light-rail lines and stations of Taipei and New Taipei are from OpenStreetMap, "
     "© OpenStreetMap contributors, available "
     "under the Open Database License. The alignments drawn are OSM's own "
     "geometry; stations, rings and categories are this project's work.",
     False, (*_OSM_RAIL, *_OSM_STATION_NAMES), per_city=osm_rail_text),
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
    Notice(21, "Ajuntament de Barcelona",
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
     False, ("Barcelona",), every_page=True),
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
    Notice(74, "Govern de les Illes Balears and Dirección General del Catastro (Palma)",
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
     False, ("Palma",)),
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
    Notice(22, "Tailte Éireann",
     "Contains Irish Public Sector Information licensed under a Creative "
     "Commons Attribution 4.0 International (CC BY 4.0) licence. The premises "
     "shown for Dublin are from Tailte Éireann's rateable valuation register, "
     "via its open API. This map filters, re-categorises and aggregates that "
     "data into density measures; the filtering, categories and densities are "
     "this project's own interpretation and are not produced or endorsed by "
     "Tailte Eireann. The data is published “as is”; Tailte Eireann "
     "gives no warranty as to its accuracy, completeness or currency.",
     False, ("Dublin",)),
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
    Notice(23, "Comune di Milano",
     "Contains data from the Comune di Milano, licensed under a Creative "
     "Commons Attribution 4.0 International (CC BY 4.0) licence. The premises "
     "shown for Milan are from six of the Comune's own registers of shops, "
     "bakers, artisan food makers, bars and restaurants, and personal "
     "services. This map filters, re-categorises and aggregates that data "
     "into density measures; the filtering, categories and densities are this "
     "project's own and are not produced or endorsed by the Comune di Milano.",
     False, ("Milan",)),
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
    Notice(24, "Île-de-France Mobilités",
     "Contient des informations de "
     "[Réseaux urbains et interurbains d'Île-de-France Mobilités (IDFM)]"
     "(https://transport.data.gouv.fr/datasets/"
     "reseau-urbain-et-interurbain-dile-de-france-mobilites), présentement "
     "mises à disposition aux conditions de la "
     "[« Licence Mobilités »](https://cloud.fabmob.io/s/CJCEzKosfqqNBEx)",
     True, ("Paris",)),
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
    Notice(25, "Tisséo (Toulouse)",
     "Contains information from Réseau urbain Tisséo, which is made available "
     "here under the Open Database License (ODbL). Métro, tramway and Téléo "
     "station locations and line geometry for Toulouse are redrawn from that "
     "feed; the stations kept, the rings, the categories and the densities "
     "are this project's own work and are not produced or endorsed by Tisséo "
     "or Toulouse Métropole.",
     True, ("Toulouse",)),
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
    Notice(26, "STAR (Rennes)",
     "Contains information from Réseau urbain STAR, which is made available "
     "here under the Open Database License (ODbL). Métro station locations and "
     "line geometry for Rennes are redrawn from that feed; the stations kept, "
     "the rings, the categories and the densities are this project's own work "
     "and are not produced or endorsed by STAR, Keolis Rennes or Rennes "
     "Métropole.",
     True, ("Rennes",)),
    # THE FRANCE TRAM BATCH'S THREE ODbL FEEDS (licence reads 2026-09-29): each
    # its own §4.3 notice naming its own database, as Tisséo's and STAR's are,
    # under the NAP's Conditions Particulières - the station tables are pure
    # extracts. Montpellier's and Le Havre's LINE GEOMETRY is OpenStreetMap's
    # (neither feed publishes shapes), which the OpenStreetMap notice covers, so
    # those two name only the stations; Grenoble's geometry is its feed's own.
    # No TaM logo, and LiA's colours are the project's own.
    Notice(69, "TaM (Montpellier)",
     "Contains information from Réseau urbain TaM, which is made available here "
     "under the Open Database License (ODbL). Tram station locations for "
     "Montpellier are drawn from that feed; the stations kept, the rings, the "
     "categories and the densities are this project's own work and are not "
     "produced or endorsed by TaM or Montpellier Méditerranée Métropole.",
     True, ("Montpellier",)),
    Notice(70, "M réso (Grenoble)",
     "Contains information from Réseau urbain TAG, which is made available here "
     "under the Open Database License (ODbL). Tram station locations and line "
     "geometry for Grenoble are redrawn from that feed; the stations kept, the "
     "rings, the categories and the densities are this project's own work and "
     "are not produced or endorsed by the SMMAG (M) or Grenoble-Alpes "
     "Métropole.",
     True, ("Grenoble (Regional)",)),
    Notice(71, "LiA (Le Havre)",
     "Contains information from Réseau urbain LiA, which is made available here "
     "under the Open Database License (ODbL). Tram station locations for Le "
     "Havre are drawn from that feed; the stations kept, the rings, the "
     "categories, the line colours and the densities are this project's own "
     "work and are not produced or endorsed by LiA or Le Havre Seine Métropole.",
     True, ("Le Havre",)),
    # ANGERS, MARK-FREE (owner, 2026-09-30): the Métropole's terms bar its
    # network brand and "any other mark" from anything built from the data
    # without consent, and the NAP dataset's title carries that brand. So the
    # database is named by its producer and its NAP id, which §4.3 allows: the
    # notice need only make a reader aware the content came from it.
    Notice(77, "Angers Loire Métropole (Angers)",
     "Contains information from Angers Loire Métropole's public transport "
     "timetable database ([transport.data.gouv.fr dataset "
     "6178cee254e3b3f0744a1318](https://transport.data.gouv.fr/datasets/6178cee254e3b3f0744a1318)), "
     "which is made available here under the Open Database License (ODbL). "
     "Tram station locations and line geometry for Angers are drawn from that "
     "feed; the stations kept, the rings, the categories and the densities "
     "are this project's own work and are not produced or endorsed by Angers "
     "Loire Métropole.",
     True, ("Angers",)),
    # BRØNNØYSUNDREGISTRENE - Oslo's business register. NLOD 2.0: section 5
    # says to attribute "as specified by the licensor", and Brønnøysund's API
    # documentation specifies nothing beyond "License: NLOD" (read
    # 2026-09-24) - so this is section 5's own default sentence, VERBATIM,
    # with the licence linked. Section 5 also requires changes to be
    # indicated clearly, which the second sentence does.
    Notice(27, "Brønnøysundregistrene (Oslo, Bergen)",
     "Contains data under the Norwegian licence for Open Government data "
     "(NLOD) distributed by Brønnøysundregistrene "
     "([NLOD 2.0](https://data.norge.no/nlod/en/2.0)). Oslo's and Bergen's "
     "business premises are selected, classified and placed by this project, and a "
     "sole trader's premises is shown by its address rather than its name; "
     "the categories and densities are this project's own work.",
     True, _NORWAY),
    # KARTVERKET - two datasets, one licensor, one licence (CC BY 4.0), so one
    # line: the address register (the coordinate join) and the kommune
    # boundaries (station scope and the naming of excluded stations).
    # Kartverket's own terms prescribe "© Kartverket" and a link; CC BY 4.0
    # 3(a) adds the licence link and a statement of modification. The
    # boundaries' municipality names come from SSR, whose rule asks for
    # "SSR ©Kartverket" - cheap, so included rather than argued.
    Notice(28, "Kartverket (Oslo, Bergen)",
     "© [Kartverket](https://www.kartverket.no). Oslo's and Bergen's address "
     "registers (Matrikkelen – Adresse) and the municipal boundaries of Oslo, "
     "Bærum and Bergen "
     "(Administrative enheter kommuner), under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); municipality "
     "names from SSR ©Kartverket. This project joins the addresses to the "
     "business register to place each premises, and uses the boundaries to "
     "select and label stations.",
     True, _NORWAY),
    # ENTUR - Ruter's GTFS. NLOD, and Entur SPECIFIES its credit: "Data made
    # available by Entur + (logo)" (developer.entur.org, read 2026-09-24).
    # The LOGO is shown on the Oslo page beside this data (owner's call
    # 2026-09-24: the old portal's instruction is still live, so it is
    # treated as owed) - Entur's own unaltered file,
    # app/assets/entur/Enturlogo_Blue_RGB.svg. NLOD section 6 bars using the
    # licensor's or other contributors' names to endorse, which reaches Ruter.
    Notice(29, "Entur (Oslo, Bergen)",
     "Data made available by Entur, under the Norwegian licence for Open "
     "Government data ([NLOD 2.0](https://data.norge.no/nlod/en/2.0)); source: "
     "Ruter's and Skyss's timetable data via [Entur](https://developer.entur.org). "
     "The T-bane, tram and Bybanen lines and stations are selected, limited to "
     "Oslo and Bergen kommunes and redrawn by this project, and the line colours "
     "are not from this data. Not produced or endorsed by Entur, Ruter, "
     "Sporveien or Skyss.",
     True, _NORWAY),
    # CVR - Copenhagen's business register, via Datafordeler. CC BY 4.0:
    # "Du skal kreditere Det Centrale Virksomhedsregister (CVR) på et
    # passende sted" (datafordeler.dk, read 2026-09-23). The name is
    # prescribed, the wording is not, so this string is this project's own;
    # its second sentence is CC BY 4.0 3(a)(1)'s modification duty. Wording
    # approved by the owner 2026-09-24.
    # Aarhus added 2026-09-29, owner-approved: the same register and cache.
    # Odense added 2026-09-30 (tram kit), the same again; approved by the
    # owner 2026-09-30 (call C1).
    Notice(30, "Det Centrale Virksomhedsregister (Copenhagen, Aarhus, Odense)",
     "Contains data from Det Centrale Virksomhedsregister (CVR), distributed by "
     "Datafordeler under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
     "Copenhagen's, Aarhus's and Odense's business premises are selected, classified and placed by this "
     "project, and a personally owned business is shown by its address rather "
     "than its name; the categories and densities are this project's own work "
     "and are not produced or endorsed by Erhvervsstyrelsen.",
     False, _DENMARK),
    # DAR - the coordinate join. CC BY 4.0 crediting Klimadatastyrelsen, which
    # lets the reuser choose the form of credit (read 2026-09-24 by the
    # licence-read agent). Named with the register as well, since Datafordeler's
    # general terms ask for "the responsible register". Wording approved by the
    # owner 2026-09-24.
    # Aarhus added 2026-09-29, owner-approved: it reads DAR's Adresse and
    # Husnummer, and takes the point from OSM's copy (osak:identifier).
    # Odense added 2026-09-30 (tram kit), Aarhus's placement; approved by the
    # owner 2026-09-30 (call C1).
    Notice(31, "Klimadatastyrelsen (Copenhagen, Aarhus, Odense)",
     "Contains data from Klimadatastyrelsen, Danmarks Adresseregister (DAR), via "
     "Datafordeler under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
     "This project joins the register's addresses and address points to the "
     "business register to place each premises; in Aarhus and Odense the points are "
     "OpenStreetMap's copies of them.",
     False, _DENMARK),
    # ČSÚ - Prague's activity, form and name data (RES). CC BY 4.0 for the web
    # pages, and the DATA paragraph ("Další podmínky použití dat ČSÚ") adds two
    # duties this notice discharges: state the licence conditions, preferably
    # by a direct link, and mark modified or derived data as such and never
    # present it as unchanged official statistics (read 2026-09-23/24).
    # Wording approved by the owner 2026-09-24.
    # The title lists every Czech city, as Norway's and Denmark's do (owner,
    # 2026-09-30): the text names none. ⚠ At landing, list only the Czech cities
    # that land - czech-build carries all six.
    Notice(32, "Czech Statistical Office (Prague, Brno, Plzeň, Olomouc, Ostrava, Liberec, Most)",
     "Contains data from the Czech Statistical Office's business register "
     "(Registr ekonomických subjektů, RES), used under the [ČSÚ conditions of use]"
     "(https://csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu) "
     "(CC BY 4.0). The activity, legal-form and name data are modified and derived by "
     "this project — joined to establishment locations, filtered to storefront "
     "categories and grouped into this project's own categories — and are not "
     "official statistics of the Czech Statistical Office.",
     False, _CZECHIA),
    # ČÚZK - RUIAN addresses. The Czech conditions page PRESCRIBES the credit
    # format "ČÚZK, [rok]" (the file's year), a link to the conditions, and a
    # description of the modification. Wording approved by the owner 2026-09-24.
    Notice(33, "ČÚZK (Prague, Brno, Plzeň, Olomouc, Ostrava, Liberec, Most)",
     "ČÚZK, 2026. Address points from the Registry of Territorial Identification, "
     "Addresses and Real Estate (RÚIAN), under the [ČÚZK conditions]"
     "(https://www.cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx) "
     "(CC BY 4.0). This project joins the addresses to the business register and "
     "converts their coordinates to place each establishment.",
     False, _CZECHIA),
    # ROPID / PID - Prague's metro. CC BY: name the author and any changes
    # (pid.cz/o-systemu/opendata/, read 2026-09-24). The PID, ROPID and IDSK
    # LOGOS need ROPID's consent and are not used. Wording approved by the
    # owner 2026-09-24.
    Notice(34, "ROPID (Prague)",
     "Metro lines and stations for Prague are redrawn from PID open data published "
     "by ROPID ([pid.cz/o-systemu/opendata](https://pid.cz/o-systemu/opendata/)), "
     "under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the "
     "three metro lines are selected and redrawn, stations are reduced to one point "
     "each, and line A's colour is lightened. Not "
     "produced or endorsed by ROPID or DPP.",
     False, ("Prague",)),
    # KORDIS JMK - Brno's tram stops. CC BY 4.0 under KORDIS's own grant
    # (idsjmk.cz/a/kontakty.html, read 2026-09-30); the feed's agency.txt
    # credits "IDS JMK (Data from: KORDIS JMK, DPMB)", which CC BY 3(a)(1)(A)
    # says to retain; data.brno.cz distributes it. No IDS JMK, KORDIS or DPMB
    # logos. Notice 78. Wording approved by the owner 2026-09-30, word for word.
    Notice(78, "KORDIS JMK (Brno)",
     "Tram stops for Brno come from the IDS JMK timetable data (GTFS) published by "
     "KORDIS JMK, a.s., with data from KORDIS JMK and DPMB, and distributed by the "
     "Statutory City of Brno at data.brno.cz, under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) "
     "([feed](https://kordis-jmk.cz/gtfs/gtfs.zip)). Changes: the 11 regular tram "
     "lines are selected, each stop is reduced to one point, and distance rings are "
     "computed around it. Not produced or endorsed by KORDIS JMK, DPMB or the City "
     "of Brno.",
     False, ("Brno",)),
    # PMDP - Plzeň's gate 3 only (its per-line stop counts); nothing from it is
    # drawn. Read 2026-09-30, PERMITTED; the record contradicts itself (CC BY in
    # the description, no-rights terms on the distribution), so it is credited
    # on the stricter CC BY reading. The credit sentence is the brief's (owner,
    # 2026-09-30); the framing around it is flagged for review. Never the city's
    # arms or PMDP's logo. Notice 79.
    Notice(79, "PMDP (Plzeň)",
     "Plzeň's tram stops are checked against Plzeňské městské dopravní podniky, a.s. "
     "(PMDP), GTFS published by the Statutory City of Plzeň at opendata.plzen.eu, "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), modified by this "
     "project: only its stop counts per line are used, and nothing from it is drawn. "
     "Not produced or endorsed by PMDP or the City of Plzeň.",
     False, ("Plzeň",)),
    # Gemeente Amsterdam - hospitality permits. The register's own licence is
    # SILENT (`Licentie: -`; a retired 2022 catalogue said CC BY), so CC BY 4.0
    # is displayed on the owner's choice of 2026-09-24, which satisfies both
    # readings. The BAG (Public Domain Mark) and GVB's data (CC0) need nothing.
    # Wording approved by the owner 2026-09-24.
    Notice(35, "Gemeente Amsterdam (Amsterdam)",
     "Hospitality permits for Amsterdam are from the Gemeente Amsterdam's register "
     "of hospitality operating permits (horeca exploitatievergunningen, "
     "[api.data.amsterdam.nl](https://api.data.amsterdam.nl/v1/)), used under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the permits "
     "are filtered to restaurants, cafés, takeaways, coffeeshops and nightclubs, "
     "grouped into one category, matched to the national buildings register by "
     "address, and mapped by distance to metro and tram stops. This is not the "
     "official permit record, and it is not produced or endorsed by the Gemeente "
     "Amsterdam.",
     False, ("Amsterdam",)),
    # Roma Capitale - the SUAP premises register. CC BY 4.0 on the dataset page
    # (read 2026-09-24): credit, link the licence, state the changes. Wording
    # approved by the owner 2026-09-24.
    Notice(36, "Roma Capitale (Rome)",
     "Premises data for Rome is from Roma Capitale's register of productive "
     "activities (SUAP, [dati.comune.roma.it](https://dati.comune.roma.it/)), used "
     "under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: the "
     "register is filtered to shops, food and drink, and personal services, sorted "
     "into three categories, placed at house-number level and mapped by distance "
     "to metro stations. Not produced or endorsed by Roma Capitale.",
     False, ("Rome",)),
    # ANNCSU - the national house-number archive that places SUAP's premises.
    # CC BY 4.0 (read 2026-09-24). Wording approved by the owner 2026-09-24.
    Notice(37, "ANNCSU (Rome)",
     "House-number coordinates for Rome are from ANNCSU, the national archive of "
     "street numbers kept by the Agenzia delle Entrate and ISTAT "
     "([anncsu.open.agenziaentrate.gov.it](https://anncsu.open.agenziaentrate.gov.it/)), "
     "used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). They are "
     "used here to place another register's premises on the map.",
     False, ("Rome",)),
    # IBGE - CNEFE 2022, the establishment register behind all nine Brazilian
    # cities. Free use by federal law (Decree 8.777/2016 art. 4, Lei
    # 14.129/2021 art. 29), crediting the source; no wording is prescribed, so
    # the Fonte line is IBGE's own citation form. Wording approved by the owner
    # 2026-09-24 with São Paulo's page.
    Notice(38, "IBGE (Brazil)",
     "Establishment data for Brazilian cities is from IBGE's Cadastro Nacional "
     "de Endereços para Fins Estatísticos (CNEFE). Fonte: IBGE, Cadastro "
     "Nacional de Endereços para Fins Estatísticos (CNEFE), Censo Demográfico "
     "2022. Changes: this project sorts each establishment's recorded "
     "description into three categories, leaves out those it cannot read, "
     "shows only the category at addresses that are also homes, and maps the "
     "rest by distance to stations. The categories are this project's "
     "reading, not IBGE's, and IBGE did not produce or endorse this map.",
     False, _BRAZIL),
    # IPP / DATA.RIO - Rio's metro stations and lines (layers 19 and 18). CC BY
    # 4.0 at service level (read 2026-09-23): the creator, the licence, a link,
    # and a statement that the data was modified - CC BY 4.0 s3(a)(1)(B), not
    # optional. Wording approved by the owner 2026-09-24.
    Notice(39, "IPP / DATA.RIO (Rio)",
     "Metro stations and lines for Rio de Janeiro: Prefeitura da Cidade do Rio "
     "de Janeiro / Instituto Pereira Passos (IPP), via DATA.RIO "
     "([pgeo3.rio.rj.gov.br](https://pgeo3.rio.rj.gov.br/arcgis/rest/services/"
     "Transporte_Trafego/Transporte_publico/MapServer)), licensed under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Reprojected, "
     "filtered and redrawn by this project; station rings and density figures "
     "are this project's own analysis.",
     False, ("Rio de Janeiro (Regional)",)),
    # CBS - the shop-vacancy share Rotterdam's page quotes. CC BY 4.0
    # (cbs.nl copyright page, read 2026-09-24): credit CBS, link the licence,
    # say when a figure is recalculated; no endorsement implied, no logo.
    # Wording approved by the owner 2026-09-24.
    Notice(40, "CBS (Rotterdam, Den Haag)",
     "The shop-vacancy figures for Rotterdam and Den Haag are from CBS (Statistics "
     "Netherlands), Landelijke Monitor Leegstand 2025, table 1, 1 January 2025, used under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) "
     "([cbs.nl](https://www.cbs.nl/)); the shares are rounded from CBS's counts. "
     "CBS did not produce or endorse this map.",
     False, ("Rotterdam", "Den Haag")),
    # FEHD's licence registers, via DATA.GOV.HK (Terms of Use v1.2, read
    # 2026-09-22), and FEHD's point for each licence from the same registers on
    # the CSDI Portal (its own terms, read 2026-09-24, add "identify clearly the
    # Government and the CSDI Portal as the source"). Both carry the same
    # uncapped indemnity, accepted by the owner. Identify the source,
    # acknowledge the Government's and FEHD's IP, and attribute the Government,
    # FEHD, DATA.GOV.HK and the CSDI Portal - in one paragraph. Wording
    # approved by the owner 2026-09-24.
    Notice(41, "FEHD / DATA.GOV.HK / CSDI (Hong Kong)",
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
     False, ("Hong Kong",)),
    # VZD cadastre open data (CC BY 4.0, adopted by VZD's own data-use rules,
    # read 2026-09-24): credit, licence link, a DESCRIPTION of the changes, and
    # no implied VZD approval. Wording approved by the owner 2026-09-24.
    # Liepāja and Daugavpils added 2026-09-30 (tram kit), approved by the owner
    # 2026-09-30 (call C1): its cadastre, and VZD's address register (aw_eka.csv, CC BY 4.0,
    # read 2026-09-30) - VZD's own source wording, the year, and the changes.
    Notice(42, "VZD (Riga, Liepāja, Daugavpils)",
     "Riga's, Liepāja's and Daugavpils's shops and services are from the State Land Service of Latvia's "
     "(Valsts zemes dienests) Cadastre Information System open data — premise groups and "
     "each city's cadastral map — via data.gov.lv, licensed under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by this project: "
     "premise groups of use class 1230 whose name reads as a shop or a service were selected, "
     "placed at their building's footprint by cadastre number and reprojected; those in "
     "buildings Riga lists as degrading were removed; all are shown as one \"Shops and "
     "services\" category and counted around tram stops. Liepāja's and Daugavpils's licensed food premises are "
     "placed by address on the State Address Register: Izmantoti Valsts adrešu reģistra "
     "informācijas sistēmas dati, 2026. gads (Valsts zemes dienests, via data.gov.lv, "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Modified by this project: "
     "the register's addresses were matched to the licences' addresses and their points used "
     "to place each premises; the address file itself is not shown. VZD has not approved these "
     "changes or this map.",
     False, ("Riga", "Liepāja", "Daugavpils")),
    # Riga municipality's GEO RĪGA layers (CC BY 4.0, read 2026-09-24). The
    # neighbourhoods "have no administrative-boundary status", so the merged
    # outline is never called the city's boundary. Approved by the owner 2026-09-24.
    Notice(43, "Riga municipality (Riga)",
     "Riga's address points, neighbourhood boundaries and list of degrading buildings are from "
     "Rīgas valstspilsētas pašvaldība (Riga State City Municipality), GEO RĪGA, via data.gov.lv, "
     "licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by "
     "this project: the address points place licensed food premises by address; the 58 "
     "neighbourhoods are merged into one outline used to select stations, which is not Riga's "
     "administrative boundary; the degrading-buildings list is used only to leave out shops in "
     "those buildings. None of the three is shown. The municipality does not endorse this map.",
     False, ("Riga",)),
    # Seoul's permit registers, all Korea Open Government License Type 1 (read
    # 2026-09-22 and 2026-09-24): KOGL's attribution form names the institution,
    # year, licence type and dataset titles, with a link where one is possible;
    # no implied sponsorship; and, under its moral-rights clause, the counts are
    # said to be this project's derivation. Wording approved by the owner
    # 2026-09-25. 유흥주점영업 is read and excluded, so it is not credited.
    Notice(18, "Seoul Metropolitan Government",
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
     False, ("Seoul",)),
    # Daegu: D-데이터허브's files declare no licence; the permission rests on the
    # portal's own policy and the Public Data Act, a reasoned position disclosed
    # and accepted by the owner (docs/data_sources.md, "Daegu and Busan"). The
    # credit is the suggested one, with Seoul's describe-the-changes and
    # non-endorsement lines kept. The edition's rows end 2025-09-02, and the
    # notice says so. Wording approved by the owner 2026-09-27.
    Notice(48, "Daegu Metropolitan City",
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
     False, ("Daegu",)),
    # Busan: PERMITTED WITH CONDITIONS - a reasonable source credit (the portal's
    # policy; 저작권법 제37조), no wording prescribed. The licence read's credit:
    # Big-데이터웨이브 (linked) as the channel, the Ministry's local-government
    # licence data as the source, and the snapshot date. Wording approved by the
    # owner 2026-09-27.
    Notice(49, "Busan Metropolitan City",
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
     False, ("Busan",)),
    # Taiwan: every source is OGDL v1 (read 2026-09-23 and 2026-09-25), whose
    # attribution statement is LOAD-BEARING - without it the grant is deemed never
    # made (§三(二)) - in the annex's prescribed form. The FIA's own declaration
    # adds: cite, no emblems, no endorsement, and do not present the filtered
    # points as the register. The FIA notice is NATIONAL: each Taiwanese city
    # adds its name to it and a notice of its own sources. Approved by the owner
    # 2026-09-25.
    Notice(44, "Fiscal Information Agency (Taiwan)",
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
     False, ("Taichung", "Taoyuan", "Taipei (Regional)")),
    Notice(45, "Taichung City Government and Taichung MRT (Taichung)",
     "提供機關／臺中市政府數位發展局 2026 臺中市115年1月至各月份GIS門牌資料 (the monthly file named in "
     "the page's snapshot caption), used to place Taichung's storefronts by address; and "
     "提供機關／臺中捷運股份有限公司 2026 臺中捷運綠線車站資訊, the Green Line's stations and their "
     "names. 此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守"
     "本條款各項規定之前提下，得利用之。 [data.gov.tw/license](https://data.gov.tw/license). The door "
     "plates themselves are not shown. Neither body endorses this map.",
     False, ("Taichung",)),
    # Taoyuan: three OGDL v1 sources (read 2026-09-25), one statement each. The
    # metro provider is named as the publisher's own portal names it (owner). The
    # portal's FAQ adds that reuse must not mislead the public or jeopardise the
    # City Government's interests - recorded and accepted (owner, 2026-09-25).
    Notice(46, "Taoyuan City Government, NLSC and Taoyuan Metro (Taoyuan)",
     "提供機關／桃園市政府民政局 2026 桃園市門牌位置坐標資料 (the monthly file named in the page's "
     "snapshot caption), used to place Taoyuan's storefronts by address; 提供機關／內政部國土測繪中心 "
     "2026 捷運車站, the Airport MRT's station locations; and 提供機關／桃園捷運公司 2026 "
     "桃園捷運路線車站基本資料, the line's stations and their names. 此開放資料依政府資料開放授權條款 "
     "(Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。 "
     "[data.gov.tw/license](https://data.gov.tw/license). The door plates themselves are not "
     "shown. None of these bodies endorses this map.",
     False, ("Taoyuan",)),
    # Taipei (Regional): three OGDL v1 sources (read 2026-09-23 and 2026-09-25),
    # one statement each. Taipei Metro's own open-data declaration adds: cite the
    # source, no logo or marks, no implied endorsement of a derivative, and
    # liability for malicious alteration - accepted by the owner 2026-09-25.
    Notice(47, "Taipei and New Taipei City Governments and Taipei Metro (Taipei (Regional))",
     "提供機關／臺北市政府民政局 2026 臺北市門牌位置數值資料 and 提供機關／新北市政府民政局 2026 "
     "新北市門牌位置數值資料 (the editions named in the page's snapshot caption), used to place the "
     "two cities' storefronts by address; and 提供機關／臺北大眾捷運股份有限公司 2026 "
     "臺北捷運路線車站資料服務, Taipei Metro's station list, used to check the map's stations. "
     "此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項"
     "規定之前提下，得利用之。 [data.gov.tw/license](https://data.gov.tw/license). The door plates "
     "themselves are not shown. None of these bodies endorses or approves this map.",
     False, ("Taipei (Regional)",)),
    # Kobe: the city's lists are CC BY 2.1 JP (the badge on each CSV; read
    # 2026-09-24), whose 出典 line and 「…を加工して作成」 are prescribed; MLIT's
    # 位置参照情報 and N02 are PDL 1.0 with their own credit lines; N03 (CC BY 4.0)
    # only picks stations and is never drawn (the Survey Act). The city's page
    # warns closed premises may remain, so nothing here says "open". Wording
    # approved by the owner 2026-09-27.
    Notice(50, "City of Kobe and MLIT (Kobe)",
     "Kobe's businesses: 出典：「生活衛生関係許可施設等の情報提供」（神戸市）"
     "（[https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html](https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html)）を加工して作成 "
     "(© City of Kobe; [CC BY 2.1 JP](https://creativecommons.org/licenses/by/2.1/jp/)). Their "
     "locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）"
     "を加工して作成. Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, "
     "stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; not drawn). This project "
     "selected the storefront permit types, placed each premises by its address, and counted them "
     "around stations. The list may include premises that have closed. The City of Kobe and MLIT "
     "did not make and do not endorse this map.",
     False, ("Kobe",)),
    # Osaka (notice 52): the city's three lists are CC BY 4.0 (each source page:
    # 「CC-BY4.0で提供いたします。」, read 2026-09-24 and again 2026-09-27), in
    # the city's prescribed 「…」（大阪市）（URL）を加工して作成 form, one title per
    # page; MLIT as in Kobe's. The map must not look like the city's own.
    # Wording approved by the owner 2026-09-28.
    Notice(52, "Osaka City and MLIT (Osaka)",
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
     False, ("Osaka",)),
    # Sapporo (notice 53): both datasets CC BY 4.0 on the city's own CKAN
    # (read 2026-09-24; the registers' package re-read 2026-09-28). No wording is
    # prescribed: credit 札幌市, both dataset titles and URLs, the licence link and
    # that the data was processed (the brief's example form); no endorsement, no
    # logos, never "operating". MLIT as in Kobe's and Osaka's. URLs are explicit
    # markdown links: bare ones ran on into the Japanese (fixed 2026-09-28).
    # Wording approved by the owner 2026-09-28.
    Notice(53, "Sapporo City and MLIT (Sapporo)",
     "Sapporo's businesses: 札幌市『札幌市内の食品営業許可施設一覧』（[https://ckan.pf-sapporo.jp/dataset/sapporo_food_business_licences](https://ckan.pf-sapporo.jp/dataset/sapporo_food_business_licences)）"
     "『札幌市内の環境衛生営業施設一覧』（[https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services](https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services)）"
     "（札幌市ICT活用プラットフォーム、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)）を加工して作成. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). This project selected the storefront permit "
     "types, placed each premises by its address, and counted them around stations. The lists may "
     "include premises that have closed. Sapporo City and MLIT did not make and do not endorse this map.",
     False, ("Sapporo",)),
    # Fukuoka (notice 54): the city's four lists on BODIK are CC BY 4.0 through
    # the city's own terms (odcs.bodik.jp/401307/tos/ 第７条: each dataset's 作成者,
    # the resource name with its date, the resource URL, that it was modified);
    # MHLW's open data is PDL 1.0 (the source, that it was processed and by
    # whom; its top page only; no completeness claim). MLIT as in Kobe's.
    # Every URL an explicit markdown link. Wording approved by the owner
    # 2026-09-28.
    Notice(54, "Fukuoka City, MHLW and MLIT (Fukuoka)",
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
     False, ("Fukuoka",)),
    # Kyoto (notice 55): the portal's three datasets are CC BY 4.0 with 京都市 as
    # 著作権者 (read 2026-09-24). MUST DISPLAY 京都市 as creator, the name
    # 京都市オープンデータ (the portal's terms ask for it), the dataset names and
    # URLs, the licence link and that the data was processed; never "operating"
    # (closures are invisible in a rebuilt register). MLIT as in Kobe's. Every
    # URL an explicit markdown link. Wording approved by the owner 2026-09-28.
    Notice(55, "Kyoto City and MLIT (Kyoto)",
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
     False, ("Kyoto",)),
    # Tokyo (notice 56): eight wards, each its own publisher, each credited in
    # the form its own terms prescribe - BUILT from pipeline/tokyo/credits.py,
    # which check_provenance.py holds to the roster (every file the build reads
    # has a credit). MHLW as in Fukuoka's; MLIT as in Kobe's. Wording approved
    # by the owner 2026-09-28.
    Notice(56, "Tokyo's wards, MHLW and MLIT (Tokyo)",
     "Tokyo's businesses: " + tokyo_credits.notice() + ". "
     "Processed by this project, which selected the storefront types, showed a premises in both a ward's "
     "list and the national filings once, placed each by its address, and counted them around stations. "
     "The national filings are not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. The wards, the Tokyo Metropolitan Government, MHLW and MLIT did not make and do not endorse "
     "this map.",
     False, ("Tokyo",)),
    # Yokohama (notice 75): the city's registers are CC BY 4.0 (the dataset
    # page and the city's open-data terms, read 2026-09-30), and the city
    # prescribes the credit for a modified work: 「この地図は、以下の著作物を改変
    # して利用しています。」, the title with its date, 神奈川県横浜市, and the licence
    # with its link. MUST NOT: present the map as the city's work, or imply its
    # endorsement. MLIT as in Kobe's. Written under the owner's pre-approval of
    # this build's prose (2026-09-30).
    Notice(75, "Yokohama City and MLIT (Yokohama)",
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
     False, ("Yokohama",)),
    # Hiroshima (notice 76): the city's full list is PDL 1.0 through DataEye
    # (dataset 5672; the owner accepted the reading for the full-list file,
    # 2026-09-24), with DataEye's prescribed 出典 pattern and who processed it;
    # MHLW as in Fukuoka's; MLIT as in Kobe's, N02 in its 2025 edition. Written
    # under the owner's pre-approval of this build's prose (2026-09-30), from
    # Fukuoka's approved wording.
    Notice(76, "Hiroshima City, MHLW and MLIT (Hiroshima)",
     "Hiroshima's businesses: 出典：「食品営業許可一覧」（広島広域都市圏・広島県オープンデータポータルサイト）"
     "（[https://hiroshima-opendata.dataeye.jp/datasets/5672](https://hiroshima-opendata.dataeye.jp/datasets/5672)）を加工して作成"
     "（「食品営業許可施設一覧（令和8年3月末時点）」, Hiroshima City); and "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, showed a premises in both lists "
     "once, placed each by its address or the ministry's own coordinates, and counted them around "
     "stations. The ministry's list holds only filings whose applicants agreed to publish them and is "
     "not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Hiroshima City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Hiroshima",)),
    # Matsuyama (notice 97): the city's five lists are CC BY 4.0 under its
    # open-data site's terms, in their prescribed form for a modified work;
    # MHLW as in Hiroshima's; MLIT as in Kobe's, N02 in its 2025 edition.
    # Written from Hiroshima's and Yokohama's approved wording under the owner's
    # pre-approval of template prose (2026-09-30).
    Notice(97, "Matsuyama City, MHLW and MLIT (Matsuyama)",
     "Matsuyama's businesses: この地図は以下の著作物を改変して利用しています。"
     "食品営業許可全施設一覧、理容所全施設一覧、美容所全施設一覧、クリーニング所全施設一覧、松山市、"
     "クリエイティブ・コモンズ・ライセンス 表示 4.0"
     "（[https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)）"
     "（[https://www.city.matsuyama.ehime.jp/shisei/opendata/top.html](https://www.city.matsuyama.ehime.jp/shisei/opendata/top.html)）. "
     "(This map modifies the City of Matsuyama's lists of food permits, barbers, beauty salons and "
     "laundries as of 31 March 2026, used under CC BY 4.0.) And "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, placed each by its address or "
     "the ministry's own coordinates, and counted them around stations. The ministry's list holds only "
     "filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Matsuyama City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Matsuyama",)),
    # Toyama (notice 98): the city's four lists are CC BY 4.0 under its CKAN's
    # terms, in their form for edited content; MHLW's file is used for its points
    # only; MLIT as in Kobe's, N02 in its 2025 edition. From Matsuyama's notice.
    Notice(98, "Toyama City, MHLW and MLIT (Toyama)",
     "Toyama's businesses: この地図は以下の著作物を改変して利用しています。"
     "食品営業許可施設、理容営業許可施設、美容営業許可施設、クリーニング営業許可施設、富山市、"
     "クリエイティブ・コモンズ・ライセンス 表示4.0国際"
     "（[https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)）"
     "（[https://opdt.city.toyama.lg.jp/](https://opdt.city.toyama.lg.jp/)）. "
     "(This map modifies the City of Toyama's list of food permits as of 30 June 2026 and its lists of "
     "barbers, beauty salons and laundries as of March 2026, used under CC BY 4.0.) And "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成, "
     "used only to place a premises the city's list also holds. "
     "Processed by this project, which selected the storefront types, placed each by its address or the "
     "ministry's own coordinates for the same premises, and counted them around stations. The ministry's "
     "list holds only filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Toyama City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Toyama",)),
    # Kumamoto (notice 99): the restaurant list PDL 1.0 in its catalogue's form,
    # the three lists CC BY 4.0 (and PDL 1.0 on BODIK), one credit for both; MHLW
    # as in Hiroshima's; MLIT as in Kobe's, N02 in its 2025 edition.
    Notice(99, "Kumamoto City, MHLW and MLIT (Kumamoto)",
     "Kumamoto's businesses: 「熊本市_食品衛生法に基づく飲食店営業許可施設一覧」「熊本市_理容所一覧」「熊本市_美容所一覧」"
     "「熊本市_クリーニング所一覧」（熊本市オープンデータカタログサイト）"
     "（[https://odcs.bodik.jp/431001/](https://odcs.bodik.jp/431001/)）をもとに作成 "
     "(PDL 1.0; the barber, beauty and laundry lists also "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)), as of 31 March 2026; and "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, showed a premises in both lists once, "
     "placed each by its address or the ministry's own coordinates, and counted them around stations. "
     "The ministry's list holds only filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Kumamoto City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Kumamoto",)),
    # Fukui (notice 100): the city's lists are CC BY-SA (the site policy's
    # default), so the Fukui outputs are offered under CC BY-SA 4.0 (owner,
    # 2026-10-01; LICENSE); MLIT as in Kobe's, N02 in its 2025 edition. The
    # wording is a proposal for review time (the drafts file).
    Notice(100, "Fukui City and MLIT (Fukui)",
     "Fukui's businesses: 出典：福井市「食品衛生法に基づく営業許可施設一覧」"
     "（[https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519.html](https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519.html)）、"
     "「環境衛生関係施設一覧」（[https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518.html](https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518.html)）"
     "を加工して作成（CC BY-SA）. (This map modifies the City of Fukui's lists of food permits and of barbers, "
     "beauty salons and laundries as of 31 August 2026, used under CC BY-SA.) This project offers the Fukui "
     "map, and the Fukui data it derived from these lists, under "
     "[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). "
     "Processed by this project, which selected the storefront types, placed each by its address and "
     "counted them around stations. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Fukui City and MLIT did not make and do not endorse this map.",
     False, ("Fukui",)),
    # Nagasaki (notice 101): the city's four BODIK lists, CC BY 4.0 with its own
    # attribution (no prescribed form); MHLW as in Hiroshima's; MLIT as in
    # Kobe's, N02 in its 2025 edition.
    Notice(101, "Nagasaki City, MHLW and MLIT (Nagasaki)",
     "Nagasaki's businesses: 長崎市「食品等営業許可・届出一覧（全許可・届出一覧）（長崎市）」"
     "（[https://data.bodik.jp/dataset/422011_food_business_all](https://data.bodik.jp/dataset/422011_food_business_all)）、「理容所一覧（全届出一覧）（長崎市）」"
     "（[https://data.bodik.jp/dataset/422011_riyosho_all](https://data.bodik.jp/dataset/422011_riyosho_all)）、「美容所一覧（全届出一覧）（長崎市）」"
     "（[https://data.bodik.jp/dataset/422011_biyosho_all](https://data.bodik.jp/dataset/422011_biyosho_all)）、「クリーニング業（洗い・取次店）一覧（全届出一覧）（長崎市）」"
     "（[https://data.bodik.jp/dataset/422011_cleners_all](https://data.bodik.jp/dataset/422011_cleners_all)）、"
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)、を加工して作成. "
     "(This map modifies the City of Nagasaki's lists of food permits as of 30 June 2023 and of barbers, "
     "beauty salons and laundries as of 31 March 2023, used under CC BY 4.0.) And "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, showed a premises in both lists once, "
     "placed each by its address or the ministry's own coordinates, and counted them around stations. "
     "The ministry's list holds only filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Nagasaki City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Nagasaki",)),
    # Utsunomiya (notice 102): the city's five lists, CC BY (no version) and PDL 1.0, in the
    # portal's pattern; MHLW as in Hiroshima's; MLIT as in Kobe's, N02 in its 2025 edition.
    Notice(102, "Utsunomiya City, MHLW and MLIT (Utsunomiya)",
     "Utsunomiya's businesses: 出典：「食品営業許可施設一覧」（宇都宮市）（[https://catalog.city.utsunomiya.tochigi.jp/dataset/s"
     "yokuhinneigyoukyoka](https://catalog.city.utsunomiya.tochigi.jp/dataset/syokuhinneigyoukyoka)）、「理容所一"
     "覧」（宇都宮市）（[https://catalog.city.utsunomiya.tochigi.jp/dataset/riyoujoichiran](https://catalog.city.ut"
     "sunomiya.tochigi.jp/dataset/riyoujoichiran)）、「美容所一覧」（宇都宮市）（[https://catalog.city.utsunomiya.tochigi."
     "jp/dataset/ubiyouzyo](https://catalog.city.utsunomiya.tochigi.jp/dataset/ubiyouzyo)）、「クリ－ニング(取次)一覧」（"
     "宇都宮市）（[https://catalog.city.utsunomiya.tochigi.jp/dataset/kuriiningutoritsugiichiran](https://catalo"
     "g.city.utsunomiya.tochigi.jp/dataset/kuriiningutoritsugiichiran)）、「クリ－ニング(一般)一覧」（宇都宮市）（[https://cata"
     "log.city.utsunomiya.tochigi.jp/dataset/kuriininguippanichiran](https://catalog.city.utsunomiya.tochi"
     "gi.jp/dataset/kuriininguippanichiran)）を加工して作成（クリエイティブ・コモンズ 表示）. (This map modifies the City of Utsun"
     "omiya's lists of food permits, barbers, beauty salons and laundries as of July 2026, used under CC B"
     "Y.) And 出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一"
     "覧」を加工して作成. Processed by this project, which selected the storefront types, showed a premises in both"
     " lists once, placed each by its address or the ministry's own coordinates, and counted them around s"
     "tations. The ministry's list holds only filings whose applicants agreed to publish them and is not c"
     "omplete. Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.m"
     "lit.go.jp/isj/)）を加工して作成. Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with 国土数値"
     "情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have closed. Utsunomiya City"
     ", MHLW and MLIT did not make and do not endorse this map.",
     False, ("Utsunomiya",)),
    # Kitakyushu (notice 103): the city's three BODIK lists, CC BY 4.0 with the 第6条 credit per
    # resource; MHLW as in Hiroshima's; MLIT as in Kobe's, N02 in its 2025 edition.
    Notice(103, "Kitakyushu City, MHLW and MLIT (Kitakyushu)",
     "Kitakyushu's businesses: 北九州市保健福祉局 保健衛生課「食品衛生法等許可施設一覧（2026(令和8)年3月中）」（[https://data.bodik.jp/dataset"
     "/822fb681-346a-444e-b482-33c67b50cac3/resource/afce5cb5-8582-4295-8a98-494db2e25466](https://data.bo"
     "dik.jp/dataset/822fb681-346a-444e-b482-33c67b50cac3/resource/afce5cb5-8582-4295-8a98-494db2e25466)）,"
     " 北九州市保健福祉局 東部・西部生活衛生課「理容所施設一覧（2026(令和8)年8月31日時点）」（[https://data.bodik.jp/dataset/8be510bd-5f67-4570-"
     "a250-b34ffdac8d37/resource/c0503e76-86d9-4f14-a052-f17ac06951d0](https://data.bodik.jp/dataset/8be51"
     "0bd-5f67-4570-a250-b34ffdac8d37/resource/c0503e76-86d9-4f14-a052-f17ac06951d0)）「美容所施設一覧（2026(令和8)年8月"
     "31日時点）」（[https://data.bodik.jp/dataset/c8266fc8-5d1f-4d3b-93aa-44486f5187ea/resource/e958d9fd-6e3d-4"
     "7bf-b557-96af0c3a44ca](https://data.bodik.jp/dataset/c8266fc8-5d1f-4d3b-93aa-44486f5187ea/resource/e"
     "958d9fd-6e3d-47bf-b557-96af0c3a44ca)）（[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)）を加工し"
     "て作成; and 出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出"
     "一覧」を加工して作成. Processed by this project, which selected the storefront types, kept the city's old perm"
     "its still in term at the end of August 2026, showed a premises in both lists once, placed each by it"
     "s address or the ministry's own coordinates, and counted them around stations. The ministry's list h"
     "olds only filings whose applicants agreed to publish them and is not complete. Their locations: 出典：位"
     "置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. Lines"
     " and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; not dr"
     "awn). The lists may include premises that have closed. Kitakyushu City, MHLW and MLIT did not make a"
     "nd do not endorse this map.",
     False, ("Kitakyushu",)),
    # Sakai (notice 104): the city's list and monthly files are CC BY 4.0 under
    # the 堺市オープンデータ利用規約 (3-2), in its prescribed form for a modified
    # work (3-3); MHLW as in Hiroshima's; MLIT as in Kobe's, N02 in its 2025
    # edition. Written from Matsuyama's approved wording under the owner's
    # pre-approval of template prose (2026-09-30).
    Notice(104, "Sakai City, MHLW and MLIT (Sakai)",
     "Sakai's businesses: この地図は以下の著作物を改変して利用しています。"
     "堺市 食品営業許可施設一覧（令和8年4月1日現在、令和8年4月分から8月分の許可施設及び廃業施設）、堺市、"
     "クリエイティブ・コモンズ・ライセンス 表示 4.0 国際"
     "（[https://creativecommons.org/licenses/by/4.0/deed.ja](https://creativecommons.org/licenses/by/4.0/deed.ja)）"
     "（[https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran/R8kyokaichiran.html](https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran/R8kyokaichiran.html)）. "
     "(This map modifies the City of Sakai's list of food permits as of 1 April 2026 and its monthly "
     "lists of new permits and closures to August 2026, used under CC BY 4.0.) And "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which rebuilt the city's list to 31 August 2026, selected the "
     "storefront types, placed each by its address or the ministry's own coordinates, and counted them "
     "around stations. The ministry's list holds only filings whose applicants agreed to publish them "
     "and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Sakai City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Sakai",)),
    # Hakodate (notice 105): the city's registers are CC BY 2.1 JP (the list
    # page), credited in Kobe's 出典 form with © and the licence link; MLIT as in
    # Kobe's, N02 in its 2025 edition. Written from Kobe's and Yokohama's
    # approved wording under the owner's pre-approval of template prose
    # (2026-09-30).
    Notice(105, "Hakodate City and MLIT (Hakodate)",
     "Hakodate's businesses: 出典：「環境衛生関係施設等の情報」（函館市）"
     "（[https://www.city.hakodate.hokkaido.jp/docs/2019072900024/](https://www.city.hakodate.hokkaido.jp/docs/2019072900024/)）を加工して作成 "
     "(© Hakodate City; [CC BY 2.1 JP](https://creativecommons.org/licenses/by/2.1/jp/)). "
     "(This map modifies the City of Hakodate's lists of barbers, beauty salons and laundries as of "
     "31 August 2026: this project selected the premises with a fixed place, placed each by its "
     "address, and counted them around stations.) The lists may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Hakodate and MLIT did not make "
     "and do not endorse this map.",
     False, ("Hakodate",)),
    # Kagoshima (notice 106): the city's old-law list, CC BY 4.0 in its prescribed credit for a
    # processed work; MHLW as in Hiroshima's; MLIT as in Kobe's, N02 in its 2025 edition.
    Notice(106, "Kagoshima City, MHLW and MLIT (Kagoshima)",
     "Kagoshima's businesses: この地図は以下の著作物を改変して利用しています。「食品営業許可全施設一覧」、鹿児島市、CCBY4.0（[https://creativecommons."
     "org/licenses/by/4.0/deed.ja](https://creativecommons.org/licenses/by/4.0/deed.ja)）（[https://www.city"
     ".kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/shokuopendata.html](https:"
     "//www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/shokuopendata.ht"
     "ml)）. (This map modifies the City of Kagoshima's list of food permits as of 30 June 2026, used under"
     " CC BY 4.0.) And 出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品"
     "等営業許可・届出一覧」を加工して作成. Processed by this project, which selected the storefront types, showed a premise"
     "s in both lists once, placed each by its address or the ministry's own coordinates, and counted them"
     " around stations. The ministry's list holds only filings whose applicants agreed to publish them and"
     " is not complete. Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https:"
     "//nlftp.mlit.go.jp/isj/)）を加工して作成. Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen "
     "with 国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have closed. Kagosh"
     "ima City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Kagoshima",)),
    # Okayama (notice 107): MHLW's open data alone, PDL 1.0 as in Hiroshima's; MLIT as in Kobe's,
    # N02 in its 2025 edition. The city's own pages are not used.
    Notice(107, "MHLW and MLIT (Okayama)",
     "Okayama's businesses: 出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)"
     "）の「食品等営業許可・届出一覧」を加工して作成. Processed by this project, which selected the storefront types, placed each"
     " by its address or the ministry's own coordinates, and counted them around stations. The ministry's "
     "list holds only filings whose applicants agreed to publish them and is not complete. Their locations"
     ": 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成."
     " Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; "
     "not drawn). The list may include premises that have closed. MHLW and MLIT did not make and do not en"
     "dorse this map.",
     False, ("Okayama",)),
    # Kōchi (notice 108): the city's lists are CC BY 4.0 (the page's open-data
    # rule and the 高知市オープンデータ利用規約), in its prescribed processed form
    # (第1); no city symbols or logos (第3). MLIT as in Kobe's, N02 in its 2025
    # edition. Written from Matsuyama's and Yokohama's approved wording under
    # the owner's pre-approval of template prose (2026-09-30).
    Notice(108, "Kōchi City and MLIT (Kōchi)",
     "Kōchi's businesses: 出典：「理容所一覧」「美容所一覧」（高知市）"
     "（[https://www.city.kochi.kochi.jp/soshiki/36/opendata.html](https://www.city.kochi.kochi.jp/soshiki/36/opendata.html)）を加工して作成 "
     "([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). "
     "(This map modifies the City of Kōchi's lists of barbers and beauty salons as of 31 March 2026 "
     "and its monthly lists of new premises to August 2026: this project selected the premises with a "
     "fixed place, placed each by its address, and counted them around stations.) The lists may "
     "include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Kōchi and MLIT did not make "
     "and do not endorse this map.",
     False, ("Kōchi",)),
    # Kawasaki (notice 115): the city's two datasets under its 利用規約 §2 (CC BY
    # 2.1 JP) and the pages' CC BY 4.0 badge, in the 規約's form for a modified
    # work, naming both versions (owner, 2026-10-02); MLIT as in Kobe's, N02 in
    # its 2025 edition. Written from Sakai's and Kōchi's approved wording under
    # the owner's pre-approval of template prose (2026-09-30).
    Notice(115, "Kawasaki City and MLIT (Kawasaki)",
     "Kawasaki's businesses: この地図は以下の著作物を改変して利用しています。"
     "食品営業許可施設一覧、川崎市、クリエイティブ・コモンズ・ライセンス 表示 "
     "[2.1](https://creativecommons.org/licenses/by/2.1/jp/) / [4.0](https://creativecommons.org/licenses/by/4.0/)"
     "（[https://www.city.kawasaki.jp/350/page/0000093741.html](https://www.city.kawasaki.jp/350/page/0000093741.html)）; "
     "環境衛生関係営業に関する情報、川崎市、クリエイティブ・コモンズ・ライセンス 表示 "
     "[2.1](https://creativecommons.org/licenses/by/2.1/jp/) / [4.0](https://creativecommons.org/licenses/by/4.0/)"
     "（[https://www.city.kawasaki.jp/350/page/0000120745.html](https://www.city.kawasaki.jp/350/page/0000120745.html)）. "
     "(This map modifies the City of Kawasaki's lists of food-business permits and of barbers, beauty "
     "salons and laundries as of 31 August 2026: this project selected the storefront types, placed each "
     "by its address, and counted them around stations.) The lists may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Kawasaki and MLIT did not make "
     "and do not endorse this map.",
     False, ("Kawasaki",)),
    # Yokosuka (notice 116): the city's BODIK datasets, CC BY 4.0 under the
    # catalogue's terms 第１条, in the brief's attribution (no form prescribed);
    # no logo (第３条), no completeness claim (第４条1). MLIT as in Kobe's, N02 in
    # its 2025 edition. Written from Kawasaki's and Kōchi's approved wording under
    # the owner's pre-approval of template prose (2026-09-30).
    Notice(116, "Yokosuka City and MLIT (Yokosuka)",
     "Yokosuka's businesses: 「【横須賀市】食品営業許可施設公開情報 （食品営業許可を取得している全施設）」"
     "（営業許可を取得している全施設　2026年8月末現在）"
     "（[https://data.bodik.jp/dataset/142018_00_18_syokuhin_all](https://data.bodik.jp/dataset/142018_00_18_syokuhin_all)）、"
     "「【横須賀市】環境衛生関係営業施設公開情報」の理容所一覧、美容所一覧、クリーニング所（一般店）一覧、クリーニング所（取次店）一覧"
     "（[https://data.bodik.jp/dataset/142018_00_19_environmental_sanitation_facilities](https://data.bodik.jp/dataset/142018_00_19_environmental_sanitation_facilities)）、"
     "横須賀市、クリエイティブ・コモンズ・ライセンス 表示4.0国際"
     "（[https://creativecommons.org/licenses/by/4.0/deed.ja](https://creativecommons.org/licenses/by/4.0/deed.ja)）を加工して作成. "
     "(This map modifies the City of Yokosuka's lists of food-business permits and of barbers, beauty "
     "salons and laundries as of 31 August 2026: this project selected the storefront types, placed each "
     "by its address, and counted them around stations.) The lists may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Yokosuka and MLIT did not make "
     "and do not endorse this map.",
     False, ("Yokosuka",)),
    # Himeji (notice 117): the city's four CKAN datasets, CC BY 4.0 (each
    # record's license_id; the catalogue's terms 1.4(1)), in the terms' 1.1
    # form per dataset; not presented as the city's own (1.1 ２). MLIT as in
    # Kobe's, N02 in its 2025 edition. Written from Kōchi's and Kawasaki's
    # approved wording under the owner's pre-approval of template prose
    # (2026-09-30).
    Notice(117, "Himeji City and MLIT (Himeji)",
     "Himeji's businesses: 出典：「食品営業許可施設一覧」（姫路市）"
     "（[https://city.himeji.gkan.jp/gkan/dataset/shokuhinn](https://city.himeji.gkan.jp/gkan/dataset/shokuhinn)）を加工して作成、"
     "「理容所一覧」（姫路市）（[https://city.himeji.gkan.jp/gkan/dataset/riyousyo](https://city.himeji.gkan.jp/gkan/dataset/riyousyo)）を加工して作成、"
     "「美容所一覧」（姫路市）（[https://city.himeji.gkan.jp/gkan/dataset/biyousyo](https://city.himeji.gkan.jp/gkan/dataset/biyousyo)）を加工して作成、"
     "「クリーニング所一覧」（姫路市）（[https://city.himeji.gkan.jp/gkan/dataset/kuriininngu](https://city.himeji.gkan.jp/gkan/dataset/kuriininngu)）を加工して作成 "
     "([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). "
     "(This map modifies the City of Himeji's lists of food-business permits and of barbers, beauty "
     "salons and laundries as of 10 September 2026: this project selected the storefront types, placed each "
     "by its address, and counted them around stations.) The lists may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Himeji and MLIT did not make "
     "and do not endorse this map.",
     False, ("Himeji",)),
    # Nishinomiya (notice 118): the city's five portal datasets under PDL 1.0
    # (the portal's terms 第1), in PDL's 1.1 form per dataset naming the
    # processor; MLIT as in Kobe's, N02 in its 2025 edition. Written from
    # Kōchi's and Toyama's approved wording under the owner's pre-approval of
    # template prose (2026-09-30).
    Notice(118, "Nishinomiya City and MLIT (Nishinomiya)",
     "Nishinomiya's businesses: 出典：「食品営業許可施設」（西宮市）"
     "（[https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=9](https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=9)）、"
     "「理容所情報」（西宮市）（[https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=49](https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=49)）、"
     "「美容所情報」（西宮市）（[https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=50](https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=50)）、"
     "「クリーニング所（一般）情報」（西宮市）（[https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=67](https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=67)）、"
     "「クリーニング所（取次）情報」（西宮市）（[https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=68](https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=68)）を加工して作成. "
     "Processed by this project, which selected the storefront types from the City of Nishinomiya's list of "
     "food-business permits as of 31 August 2026 and its registers of barbers, beauty salons and laundries "
     "of September 2026, placed each by its address, and counted them around stations. The lists may "
     "include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Nishinomiya and MLIT did not make "
     "and do not endorse this map.",
     False, ("Nishinomiya",)),
    # Takamatsu (notice 119): the city's four lists, CC BY 4.0 under its
    # open-data terms 第１条, in the brief's attribution (no form prescribed);
    # MHLW's notifications (PDL 1.0) as in Matsuyama's; MLIT as in Kobe's, N02
    # in its 2025 edition. Written from Matsuyama's approved wording under the
    # owner's pre-approval of template prose (2026-09-30).
    Notice(119, "Takamatsu City, MHLW and MLIT (Takamatsu)",
     "Takamatsu's businesses: 出典：「食品等営業許可施設一覧」「理容所新規開設一覧」「美容所新規開設一覧」"
     "「クリーニング所新規開設一覧」（高松市）"
     "（[https://opendata.smartcity-takamatsu.jp/odp/](https://opendata.smartcity-takamatsu.jp/odp/)）を加工して作成 "
     "([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). "
     "(This map modifies the City of Takamatsu's list of food-business permits and its registers of barbers, "
     "beauty salons and laundries as of 31 August 2026, used under CC BY 4.0.) And "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, showed a premises in both lists once, "
     "placed each by its address or the ministry's own coordinates, and counted them around stations. "
     "The ministry's list holds only filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have "
     "closed. Takamatsu City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Takamatsu",)),
    # Toyota (notice 120): the city's two BODIK datasets, CC BY 4.0 under its
    # catalogue terms, in their 3(2) form for a modified work (the food title
    # carries its edition's date); not presented as the city's own (3(1)).
    # MLIT as in Kobe's, N02 in its 2025 edition. Written from Kawasaki's
    # approved wording under the owner's pre-approval of template prose
    # (2026-09-30).
    Notice(120, "Toyota City and MLIT (Toyota)",
     "Toyota's businesses: この地図は、以下の著作物を改変して利用しています。 "
     "オープンデータ　食品営業許可施設一覧（2026年8月31日現在）"
     "（[https://data.bodik.jp/dataset/232114_permit_food_facility](https://data.bodik.jp/dataset/232114_permit_food_facility)）、"
     "環境衛生営業施設一覧"
     "（[https://data.bodik.jp/dataset/232114_environmental_health_service_facility](https://data.bodik.jp/dataset/232114_environmental_health_service_facility)）、"
     "豊田市、[クリエイティブ・コモンズ・ライセンス 表示4.0国際](https://creativecommons.org/licenses/by/4.0/deed.ja). "
     "(This map modifies the City of Toyota's list of food-business permits and its registers of barbers, "
     "beauty salons and laundries as of 31 August 2026: this project selected the storefront types, placed "
     "each by its address, and counted them around stations.) The lists may include premises that have "
     "closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Toyota and MLIT did not make "
     "and do not endorse this map.",
     False, ("Toyota",)),
    # Yokkaichi (notice 121): the city's five BODIK lists, CC BY 4.0 under the
    # 四日市市オープンデータ利用規約 (第1条), no form prescribed, so CC BY 4.0's
    # elements; no city logo (第3条). MLIT as in Kobe's, N02 in its 2025
    # edition. Written from Kōchi's and Kawasaki's approved wording under the
    # owner's pre-approval of template prose (2026-09-30).
    Notice(121, "Yokkaichi City and MLIT (Yokkaichi)",
     "Yokkaichi's businesses: 出典：「食品営業許可施設一覧」「食品営業届出施設一覧」「理容所一覧」「美容所一覧」「クリーニング所一覧」"
     "（四日市市、2026-08-31、[https://odcs.bodik.jp/242021/](https://odcs.bodik.jp/242021/)）を加工して作成 "
     "([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). "
     "(This map modifies the City of Yokkaichi's lists of food-business permits and notifications and of "
     "barbers, beauty salons and laundries as of 31 August 2026: this project selected the storefront types, "
     "placed each by its address, and counted them around stations.) The lists may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Yokkaichi and MLIT did not make "
     "and do not endorse this map.",
     False, ("Yokkaichi",)),
    # Ōtsu (notice 122): the city's food list (catalogued cc-by on its BODIK
    # portal, accepted as CC BY 4.0, owner 2026-10-02) and three BODIK registers,
    # in the 大津市オープンデータ利用規約's form for edited content (４(2)); no
    # city logo (５). MLIT as in Kobe's, N02 in its 2025 edition. Written from
    # Kawasaki's approved wording under the owner's pre-approval of template
    # prose (2026-09-30).
    Notice(122, "Ōtsu City and MLIT (Ōtsu)",
     "Ōtsu's businesses: この地図は以下の著作物を改変して利用しています。"
     "食品営業許可施設一覧、大津市、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際"
     "（[https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)）"
     "（[https://www.city.otsu.lg.jp/soshiki/021/1441/od/02594.html](https://www.city.otsu.lg.jp/soshiki/021/1441/od/02594.html)）; "
     "理容所一覧、美容所施設一覧、クリーニング所一覧、大津市、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際"
     "（[https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)）"
     "（[https://odcs.bodik.jp/252018/](https://odcs.bodik.jp/252018/)）. "
     "(This map modifies the City of Ōtsu's lists of food-business permits and of barbers, beauty "
     "salons and laundries as of 31 August 2026: this project selected the storefront types, placed each "
     "by its address, and counted them around stations.) The lists may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Ōtsu and MLIT did not make "
     "and do not endorse this map.",
     False, ("Ōtsu",)),
    # Nara (notice 123): the city's four lists under CC BY 2.1 JP (each page's
    # statement and the 奈良市オープンデータカタログ利用規約), in the terms' form
    # for an edited work (３); MHLW as in Hiroshima's and Kitakyushu's; MLIT as
    # in Kobe's, N02 in its 2025 edition. Written from Kitakyushu's and
    # Kawasaki's approved wording under the owner's pre-approval of template
    # prose (2026-09-30).
    Notice(123, "Nara City, MHLW and MLIT (Nara)",
     "Nara's businesses: この地図は以下の著作物を改変して利用しています。"
     "食品営業許可施設オープンデータ、奈良市、クリエイティブ・コモンズ・ライセンス 表示 2.1"
     "（[https://creativecommons.org/licenses/by/2.1/jp/](https://creativecommons.org/licenses/by/2.1/jp/)）"
     "（[https://www.city.nara.lg.jp/soshiki/97/10411.html](https://www.city.nara.lg.jp/soshiki/97/10411.html)）; "
     "理容所検査確認施設一覧、美容所検査確認施設一覧、クリーニング所検査確認施設一覧、奈良市、クリエイティブ・コモンズ・ライセンス 表示 2.1"
     "（[https://creativecommons.org/licenses/by/2.1/jp/](https://creativecommons.org/licenses/by/2.1/jp/)）"
     "（[https://www.city.nara.lg.jp/soshiki/97/9688.html](https://www.city.nara.lg.jp/soshiki/97/9688.html)）; and "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, kept the city's old permits still in "
     "term at the end of August 2026, showed a premises in both lists once, placed each by its address or "
     "the ministry's own coordinates, and counted them around stations. The ministry's list holds only "
     "filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have closed. "
     "Nara City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Nara",)),
    # Hamamatsu (notice 124): the city's four registers are CC BY 2.1 JP (the
    # portal's top and the 浜松市オープンデータ利用規約), in the terms' form for a
    # modified work; MLIT as in Kobe's, N02 in its 2025 edition. Written from
    # Kawasaki's and Hakodate's approved wording under the owner's pre-approval
    # of template prose (2026-09-30).
    Notice(124, "Hamamatsu City and MLIT (Hamamatsu)",
     "Hamamatsu's businesses: この地図は以下の著作物を改変して利用しています。"
     "理容所台帳、美容所台帳、クリーニング所(取次)台帳、クリーニング所(一般)台帳、浜松市、クリエイティブ・コモンズ・ライセンス 表示2.1"
     "（[http://creativecommons.org/licenses/by/2.1/jp/](https://creativecommons.org/licenses/by/2.1/jp/)）. "
     "(This map modifies the City of Hamamatsu's registers of barbers, beauty salons, laundry pick-up "
     "counters and general laundries, published 18 August 2026: this project placed each by its address "
     "or the city's own coordinates, and counted them around stations.) The registers may include premises "
     "that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Hamamatsu and MLIT did not make "
     "and do not endorse this map.",
     False, ("Hamamatsu",)),
    # Higashiōsaka (notice 125): the city's BODIK dataset is CC BY 4.0 (its
    # license_id and the 東大阪市オープンデータ利用規約 2), in the terms' form for an
    # edited work; MLIT as in Kobe's, N02 in its 2025 edition. Written from
    # Kawasaki's and Sakai's approved wording under the owner's pre-approval of
    # template prose (2026-09-30).
    Notice(125, "Higashiōsaka City and MLIT (Higashiōsaka)",
     "Higashiōsaka's businesses: この地図は以下の著作物を改変して利用しています。"
     "食品等営業許可一覧、東大阪市、クリエイティブ・コモンズ・ライセンス 表示 4.0"
     "（[https://creativecommons.org/licenses/by/4.0/deed.ja](https://creativecommons.org/licenses/by/4.0/deed.ja)）"
     "（[https://data.bodik.jp/dataset/b5eeed4c-cec0-4eef-8513-b4882d6a18ec](https://data.bodik.jp/dataset/b5eeed4c-cec0-4eef-8513-b4882d6a18ec)）. "
     "(This map modifies the City of Higashiōsaka's list of food-business permits as of 1 April 2026 and "
     "its monthly lists of new permits to 31 August 2026: this project rebuilt them into one list of the "
     "permits in term on 31 August 2026, selected the storefront types, placed each by its address, and "
     "counted them around stations.) The list may include premises that have closed. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The City of Higashiōsaka and MLIT did not make "
     "and do not endorse this map.",
     False, ("Higashiōsaka",)),
    # Kurume (notice 126): MHLW's open data alone, as in Okayama's (107); MLIT as
    # in Kobe's, N02 in its 2025 edition. Written from Okayama's approved
    # wording under the owner's pre-approval of template prose (2026-09-30).
    Notice(126, "MHLW and MLIT (Kurume)",
     "Kurume's businesses: 出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, placed each by its address or the "
     "ministry's own coordinates, and counted them around stations. The ministry's list holds only filings "
     "whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The list may include premises that have closed. "
     "MHLW and MLIT did not make and do not endorse this map.",
     False, ("Kurume",)),
    # Sasebo (notice 127): the city's old-law list on BODIK, CC BY 4.0 in the
    # 佐世保市オープンデータ利用規約's edited-use form (第3条(2)(イ)); MHLW as in
    # Hiroshima's and Kitakyushu's; MLIT as in Kobe's, N02 in its 2025 edition.
    # Written from Kitakyushu's and Kagoshima's approved wording under the
    # owner's pre-approval of template prose (2026-09-30).
    Notice(127, "Sasebo City, MHLW and MLIT (Sasebo)",
     "Sasebo's businesses: この地図は、以下の著作物を改変して利用しています。"
     "(令和8年4月末時点)法改正前食品営業許可施設一覧、佐世保市、CCライセンス"
     "（[http://creativecommons.org/licenses/by/4.0/deed.ja](http://creativecommons.org/licenses/by/4.0/deed.ja)）"
     "（[https://data.bodik.jp/dataset/422029_syokuhineigyoukyoka](https://data.bodik.jp/dataset/422029_syokuhineigyoukyoka)）; and "
     "出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）の「食品等営業許可・届出一覧」を加工して作成. "
     "Processed by this project, which selected the storefront types, kept the city's old permits still in "
     "term at the end of August 2026, showed a premises in both lists once, placed each by its address or "
     "the ministry's own coordinates, and counted them around stations. The ministry's list holds only "
     "filings whose applicants agreed to publish them and is not complete. "
     "Their locations: 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成. "
     "Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with "
     "国土数値情報（行政区域データ） (CC BY 4.0; not drawn). The lists may include premises that have closed. "
     "Sasebo City, MHLW and MLIT did not make and do not endorse this map.",
     False, ("Sasebo",)),
    # Shimonoseki (notice 128): MHLW's open data alone, PDL 1.0 as in Okayama's;
    # MLIT as in Kobe's, N02 in its 2025 edition. No city source is used.
    Notice(128, "MHLW and MLIT (Shimonoseki)",
     "Shimonoseki's businesses: 出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)"
     "）の「食品等営業許可・届出一覧」を加工して作成. Processed by this project, which selected the storefront types, placed each"
     " by its address or the ministry's own coordinates, and counted them around stations. The ministry's "
     "list holds only filings whose applicants agreed to publish them and is not complete. Their locations"
     ": 出典：位置参照情報ダウンロードサービス（国土交通省）（[https://nlftp.mlit.go.jp/isj/](https://nlftp.mlit.go.jp/isj/)）を加工して作成."
     " Lines and stations: 「国土数値情報（鉄道データ）」（国土交通省）をもとに作成, stations chosen with 国土数値情報（行政区域データ） (CC BY 4.0; "
     "not drawn). The list may include premises that have closed. MHLW and MLIT did not make and do not en"
     "dorse this map.",
     False, ("Shimonoseki",)),
    # Berlin (notice 57): VBB's GTFS, CC BY 4.0 per VBB's own dataset page -
    # the requested credit, the licence link, what was modified, the
    # disclaimer, no endorsement. IHK Berlin's register is CC0 and needs no
    # notice (its courtesy credit is on the Berlin page). Wording approved by
    # the owner 2026-09-28.
    Notice(57, "VBB Verkehrsverbund Berlin-Brandenburg (Berlin)",
     "Station locations and line geometry for Berlin are from VBB Verkehrsverbund "
     "Berlin-Brandenburg GmbH's timetable data (GTFS), used under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by this project: "
     "U-Bahn and S-Bahn stations were selected and those outside the Land of Berlin removed, "
     "one timetable shape was chosen per line, and the lines are drawn in this project's "
     "colours. VBB provides the data without warranty and does not endorse this map.",
     False, ("Berlin",)),
    # London (notice 58): the FSA's FHRS data under OGL v3 - the OGL statement linked, the
    # data date, what was modified, no endorsement. The credit avoids "the FHRS
    # name" (the FSA's imagery terms). Wording approved by the owner 2026-09-28.
    Notice(58, "Food Standards Agency (London)",
     "London's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted between 2026-09-09 and 2026-09-16. Contains public sector information "
     "licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade "
     "names shown where a business is registered under another name. No hygiene rating is "
     "shown. The Food Standards Agency does not endorse this map.",
     False, ("London",)),
    # London's postcode centroids (notice 59): Ordnance Survey's OGL v3 data -
    # the three statements verbatim from the licence file OS ships with it
    # (Doc/licence.txt, which OS's own terms name as the authority), the
    # licence link, no endorsement. The product's registered name is not used
    # (trademarks are outside the OGL). Wording approved by the owner 2026-09-28.
    Notice(59, "Ordnance Survey (London)",
     "Where the Food Standards Agency lists a London food business without a map point, it is "
     "placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("London",)),
    # Buenos Aires (notice 60): BA Data's three datasets under CC BY 2.5 AR -
    # author units, dataset titles and URIs, the licence URI, how the data was
    # changed, no endorsement, no GCBA or BA Data logo. Written to satisfy 2.5 AR
    # and 4.0 both (Parcelas' resources say 4.0). Approved by the owner 2026-09-28.
    Notice(60, "Gobierno de la Ciudad de Buenos Aires (Buenos Aires)",
     "Buenos Aires' storefronts are from the [Relevamiento Usos del Suelo 2022-2024]"
     "(https://data.buenosaires.gob.ar/dataset/relevamiento-usos-suelo) (Dirección General de "
     "Antropología Urbana, Subsecretaría de Planeamiento), placed using "
     "[Parcelas](https://data.buenosaires.gob.ar/dataset/parcelas) (Subsecretaría de Registro, "
     "Interpretación y Catastro), and the Subte's stations and lines are from "
     "[Subte: Estaciones](https://data.buenosaires.gob.ar/dataset/subte-estaciones) "
     "(Subterráneos de Buenos Aires, SBASE), all published by the Gobierno de la Ciudad de "
     "Buenos Aires on BA Data under the [Creative Commons Attribution 2.5 Argentina licence]"
     "(http://creativecommons.org/licenses/by/2.5/ar/). Modified by this project: filtered to "
     "storefronts, grouped into three categories, and placed at the center of each parcel, or "
     "of its block where the parcel is not listed; station names follow OpenStreetMap's "
     "spelling. The Gobierno de la Ciudad de Buenos Aires does not endorse this map.",
     False, ("Buenos Aires",)),
    # Glasgow (notice 61): Scotland's FHIS data, run by Food Standards Scotland and
    # published in the FSA's open-data files, under OGL v3 (FSS states v3 itself) - the
    # OGL statement linked, the extract date, what was modified, no endorsement by either
    # body. Never "FHRS": FHIS is a separate scheme. Wording approved by the owner 2026-09-28.
    Notice(61, "Food Standards Scotland (Glasgow)",
     "Glasgow's food businesses are from Food Standards Scotland, Food Hygiene Information "
     "Scheme data, via the Food Standards Agency, extracted on 2026-09-14. Contains public "
     "sector information licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected; premises without a location, at a flat address "
     "or registered as a childminder left out; trade names shown where a business is "
     "registered under another name. No inspection result is shown. Neither Food Standards "
     "Scotland nor the Food Standards Agency endorses this map.",
     False, ("Glasgow",)),
    # Newcastle (notice 62): the FSA's FHRS data for the five Tyne and Wear councils,
    # London's credit and conditions (England, FHRS). Wording approved by the owner
    # 2026-09-28.
    Notice(62, "Food Standards Agency (Newcastle)",
     "Newcastle's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted between 2026-09-09 and 2026-09-16. Contains public sector information "
     "licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Newcastle (Regional)",)),
    # Newcastle's postcode centroids (notice 63): London's Ordnance Survey notice, the
    # same file and edition. Wording approved by the owner 2026-09-28.
    Notice(63, "Ordnance Survey (Newcastle)",
     "Where the Food Standards Agency lists a Newcastle food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Newcastle (Regional)",)),
    # Sydney (notice 64): the City of Sydney's FES under CC BY 4.0 - creator and
    # copyright holder, the licence and the dataset linked, modification noted, the
    # warranty disclaimer, no endorsement (licence-read 2026-09-28; no wording is
    # prescribed). Wording approved by the owner 2026-09-28.
    Notice(64, "City of Sydney (Sydney)",
     "Business establishment locations: City of Sydney, Floor Space and Employment Survey 2022 "
     "([FES Industry of occupation](https://www.arcgis.com/home/item.html?id="
     "77ac8aa96bd34bacb881cfe8e5358ba0)), © City of Sydney, licensed under "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Modified by this project "
     "(filtered and grouped by category); provided as is, without warranty. The City of Sydney "
     "does not endorse this map.",
     False, ("Sydney",)),
    # Melbourne (notice 65): the City of Melbourne's CLUE under CC BY 4.0 - the credit,
    # the licence and the dataset linked, the modification noted, no endorsement
    # (licence-read 2026-09-28; no wording is prescribed). Wording approved by the
    # owner 2026-09-28.
    Notice(65, "City of Melbourne (Melbourne)",
     "Business establishments: City of Melbourne, Census of Land Use and Employment (CLUE) 2024 "
     "([dataset](https://data.melbourne.vic.gov.au/explore/dataset/"
     "business-establishments-with-address-and-industry-classification/)), "
     "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Filtered, categorised and "
     "aggregated by this project. The City of Melbourne does not endorse this map.",
     False, ("Melbourne",)),
    # Stockholm (notice 66): Stockholms stad's Livsmedelstillsyn register. Its licence
    # is SILENT (no licence on the item; the publisher's own Hub feed says public, with
    # CC0 on 8 of 109 datasets but not this one), so the notice credits the publisher
    # and states the changes without claiming a licence. Wording approved by the
    # owner 2026-09-29.
    Notice(66, "Stockholms stad (Stockholm)",
     "Food premises for Stockholm are from the City of Stockholm's food inspection "
     "register (Livsmedelstillsyn, Stockholms stad, miljöförvaltningen, "
     "[open-data-sthlm-miljo.hub.arcgis.com](https://open-data-sthlm-miljo.hub.arcgis.com/)), "
     "which the city publishes as public open data with no stated licence. Changes: the "
     "inspections are reduced to one record per premises, filtered to restaurants, cafés, "
     "bars and food shops, grouped into two categories, and mapped by distance to "
     "Tunnelbana stations. This is not the official register, and it is not produced or "
     "endorsed by Stockholms stad.",
     False, ("Stockholm",)),
    # Bucharest (notice 67): DSVSA București's registers. Licence SILENT (no terms page; the ANSVSA
    # footer's "all rights reserved" covers the website), so the notice credits the
    # publisher and states the changes without claiming a licence. Wording approved
    # by the owner 2026-09-29.
    Notice(67, "DSVSA București (Bucharest)",
     "Food premises for Bucharest are from the registers of the Sanitary-Veterinary and "
     "Food Safety Directorate of Bucharest (DSVSA București, "
     "[bucuresti.dsvsa.ro](https://bucuresti.dsvsa.ro/)), which it publishes with no stated "
     "licence. Changes: cancelled registrations are left out; the units are filtered to "
     "restaurants, cafés, bars and food shops, merged where one premises holds several "
     "registrations, grouped into two categories, placed by matching their addresses to "
     "OpenStreetMap's address points, and mapped by distance to metro stations. Company "
     "names are shown without their legal form, and sole traders by category only. This is "
     "not the official register, and it is not produced or endorsed by DSVSA or ANSVSA.",
     False, ("Bucharest",)),
    # SEMAS's 상가(상권)정보 (notice 68): data.go.kr 15083033, 이용허락범위 제한 없음. licence-read
    # 2026-09-29: PERMITTED WITH CONDITIONS - a source credit, no distortion of the
    # facts (so the categories are stated as this project's), SEMAS's website copyright
    # policy read as covering its homepage (owner, 2026-09-29, Daegu's reading). Written
    # under the owner's pre-approval of this build's prose. Covers every Korean city on
    # the register (Incheon; the Gyeonggi satellites add their names).
    Notice(68, "Small Enterprise and Market Service (Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang)",
     "Storefronts for Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu and Anyang are from the Small "
     "Enterprise and "
     "Market Service's "
     "commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via 공공데이터포털 "
     "[data.go.kr](https://www.data.go.kr/data/15083033/fileData.do)), "
     "이용허락범위 제한 없음. Changes: filtered to shops, food and drink and personal services, "
     "grouped into three categories, and mapped by distance to stations; the categories and "
     "counts are this project's, not SEMAS's. Not produced or endorsed by SEMAS.",
     False, _KOREA_SEMAS),
    # Ottawa: Ottawa Public Health's food-safety inspection feed and the City's
    # 2022-2026 wards, both under the Open Government Licence - City of Ottawa
    # v2.0 (the items' licenseInfo, read 2026-09-29). Its attribution sentence is
    # PRESCRIBED and is reproduced VERBATIM, with the en dash, linked to the
    # licence; the credit names Ottawa Public Health / City of Ottawa. The
    # licence bars implying official status or endorsement and using the City's
    # or OPH's names as marks. Written under the owner's pre-approval of this
    # build's prose (2026-09-29).
    Notice(72, "City of Ottawa (Ottawa)",
     "Contains information licensed under the [Open Government Licence – City of "
     "Ottawa](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0). "
     "Food premises for Ottawa are from Ottawa Public Health / City of Ottawa's public health "
     "inspection data (food safety), and the city boundary from the City's 2022-2026 wards. "
     "Changes: the premises are limited to those inspected in the last two years, "
     "institutional kitchens, clubs, mobile vendors and hotels are left out by name, and the "
     "rest are mapped by distance to O-Train stations; inspection results are not shown. This "
     "is not an official City of Ottawa or Ottawa Public Health product, and it is not "
     "endorsed by either.",
     False, ("Ottawa",)),
    # Kansas City (notice 80): the Data Terms of Use of Open Data KC
    # (data.kcmo.org/terms) prescribe this paragraph "at the site where the
    # software application ... can be accessed" - Chicago's wording on the same
    # portal template, so displayed site-wide as Chicago's is. Word for word,
    # the City's dead host www.data.kcmo.gov included (licence-read 2026-09-30).
    Notice(80, "City of Kansas City, Missouri (Kansas City)",
     "This site provides applications using data that has been modified for "
     "use from its original source, www.data.kcmo.gov, the official open data "
     "website of the City of Kansas City. The City of Kansas City makes no "
     "claims as to the content, accuracy, timeliness, or completeness of any "
     "of the data provided at this site. The data provided at this site is "
     "subject to change at any time. It is understood that the data provided "
     "at this site is being used at one’s own risk.",
     True, ("Kansas City",), every_page=True),
    # Tucson (notice 81): the BUSLIC layer's licence is silent, and the owner
    # took the permissive reading (2026-09-30) on condition that the City is
    # credited and the pins are never called complete. The owner's wording.
    Notice(81, "City of Tucson (Tucson)",
     "Business licence data: City of Tucson.",
     False, ("Tucson",)),
    # Florence (notice 82): the Comune di Firenze's four activity layers, CC BY
    # 4.0 (its Note legali and every dataset; licence read 2026-09-30, the
    # brief). Credit the Comune, link the licence, state the changes - Milan's
    # notice, the same licence; no wording prescribed, so this is the project's
    # own. Never the Comune's logo or the giglio.
    Notice(82, "Comune di Firenze (Florence)",
     "Contains data from the Comune di Firenze (Direzione Attività Economiche e "
     "Turismo), licensed under a [Creative Commons Attribution 4.0 International "
     "(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) licence: its "
     "layers of shops, food and drink premises, beauty businesses and laundries. "
     "This map filters, re-categorises and aggregates that data into density "
     "measures; the filtering, categories and densities are this project's own "
     "and are not produced or endorsed by the Comune di Firenze.",
     False, ("Florence",)),
    # Den Haag (notice 83): the Gemeente's Horecavergunningen layer. Its licence
    # is silent; the owner proceeds on Amsterdam's precedent (2026-09-30) on
    # condition that the Gemeente is credited and the layer is never called
    # current or complete. Wording approved by the owner 2026-09-30 (call C1).
    Notice(83, "Gemeente Den Haag (Den Haag)",
     "Hospitality permit data: Gemeente Den Haag. The permit layer was last "
     "edited on 23 May 2025 and is not a complete or current record. Changes: "
     "the permits are filtered to food and drink premises, grouped into one "
     "category, matched to the national buildings register by address, and "
     "mapped by distance to tram stops. Not produced or endorsed by the "
     "Gemeente Den Haag.",
     False, ("Den Haag",)),
    # Manchester (notice 84): the FSA's FHRS data for the seven Metrolink
    # districts, Newcastle's notice 62 with the city and date changed.
    Notice(84, "Food Standards Agency (Manchester)",
     "Manchester's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted on 2026-10-02. Contains public sector information licensed under the "
     "[Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Manchester (Regional)",)),
    # Manchester's postcode centroids (notice 85): Newcastle's notice 63, the
    # same file and edition.
    Notice(85, "Ordnance Survey (Manchester)",
     "Where the Food Standards Agency lists a Manchester food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Manchester (Regional)",)),
    # NaPTAN (notice 86): gate 3's second source for the UK tram and
    # light-rail cities, counted only. The OGL's default statement, since the
    # Department prescribes none (licence-read 2026-10-02). Wording approved
    # by the owner 2026-10-02.
    Notice(86, "Department for Transport, NaPTAN (United Kingdom)",
     "Stop and station counts on the UK's tram, light-rail and Merseyrail maps are checked "
     "against NaPTAN, the National Public Transport Access Nodes dataset published by the "
     "Department for Transport. Contains public sector information licensed under the "
     "[Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). The "
     "Department for Transport does not endorse this map.",
     False, _UK_NAPTAN),
    # Birmingham (notice 87): the FSA's FHRS data for the three West Midlands
    # Metro districts, Newcastle's notice 62 with the city and date changed.
    Notice(87, "Food Standards Agency (Birmingham)",
     "Birmingham's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted on 2026-10-02. Contains public sector information licensed under the "
     "[Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Birmingham (Regional)",)),
    # Birmingham's postcode centroids (notice 88): Newcastle's notice 63, the
    # same file and edition.
    Notice(88, "Ordnance Survey (Birmingham)",
     "Where the Food Standards Agency lists a Birmingham food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Birmingham (Regional)",)),
    # Edinburgh (notice 89): Scotland's FHIS data for the City of Edinburgh, Glasgow's
    # notice 61 with the city and date changed and Manchester's centroid clause added.
    Notice(89, "Food Standards Scotland (Edinburgh)",
     "Edinburgh's food businesses are from Food Standards Scotland, Food Hygiene Information "
     "Scheme data, via the Food Standards Agency, extracted on 2026-10-02. Contains public "
     "sector information licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected; premises at a flat address or registered as a "
     "childminder left out; premises without a location placed at their postcode's center, or "
     "left out where they have no full postcode; trade names shown where a business is "
     "registered under another name. No inspection result is shown. Neither Food Standards "
     "Scotland nor the Food Standards Agency endorses this map.",
     False, ("Edinburgh",)),
    # Edinburgh's postcode centroids (notice 90): Newcastle's notice 63, the
    # same file and edition.
    Notice(90, "Ordnance Survey (Edinburgh)",
     "Where the Food Standards Agency lists an Edinburgh food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Edinburgh",)),
    # Sheffield (notice 91): the FSA's FHRS data for the City of Sheffield,
    # Newcastle's notice 62 with the city and date changed.
    Notice(91, "Food Standards Agency (Sheffield)",
     "Sheffield's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted on 2026-10-02. Contains public sector information licensed under the "
     "[Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Sheffield",)),
    # Sheffield's postcode centroids (notice 92): Newcastle's notice 63, the
    # same file and edition.
    Notice(92, "Ordnance Survey (Sheffield)",
     "Where the Food Standards Agency lists a Sheffield food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Sheffield",)),
    # Nottingham (notice 93): the FSA's FHRS data for the four NET council
    # areas, Newcastle's notice 62 with the city and date changed.
    Notice(93, "Food Standards Agency (Nottingham)",
     "Nottingham's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted between 2026-10-01 and 2026-10-02. Contains public sector information "
     "licensed under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Nottingham (Regional)",)),
    # Nottingham's postcode centroids (notice 94): Newcastle's notice 63, the
    # same file and edition.
    Notice(94, "Ordnance Survey (Nottingham)",
     "Where the Food Standards Agency lists a Nottingham food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Nottingham (Regional)",)),
    # Blackpool (notice 95): the FSA's FHRS data for Blackpool and Wyre,
    # Newcastle's notice 62 with the city and date changed.
    Notice(95, "Food Standards Agency (Blackpool)",
     "Blackpool's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted on 2026-10-02. Contains public sector information licensed under the "
     "[Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Blackpool (Regional)",)),
    # Blackpool's postcode centroids (notice 96): Newcastle's notice 63, the
    # same file and edition.
    Notice(96, "Ordnance Survey (Blackpool)",
     "Where the Food Standards Agency lists a Blackpool food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Blackpool (Regional)",)),
    # Seattle (Regional) (notices 109-113, the session's claimed block):
    # King County's two required texts (owner, 2026-10-01: the permissive
    # reading rests on the Open Data terms' legend); the Liquor Board's list
    # date and its own data-transfer note while the lists page carries it
    # (owner, 2026-10-02); Snohomish County's credit in the owner's words;
    # Bellevue's credit (the condition of the owner's reading); Seattle's
    # credit, recommended and displayed by choice.
    Notice(109, "Public Health – Seattle & King County (Seattle (Regional))",
     "Food inspection data: Public Health – Seattle & King County. Data provided "
     "by permission of King County. Not endorsed by King County.",
     False, ("Seattle (Regional)",)),
    Notice(110, "Washington State Liquor and Cannabis Board (Seattle (Regional))",
     "Shops licensed to sell alcohol outside Seattle and Bellevue: the Washington "
     "State Liquor and Cannabis Board's off-premise licensee list of September 29, "
     "2026, not a complete or current list of shops. The Board notes that its list "
     "reports \"contain possible errors due to a known data transfer issue\".",
     False, ("Seattle (Regional)",)),
    Notice(111, "Snohomish County (Seattle (Regional))",
     "Lynnwood and Mountlake Terrace food establishments: Snohomish County, Food "
     "Service Establishments (2025). The list dates from 2025 and is not a current, "
     "complete or official record.",
     False, ("Seattle (Regional)",)),
    Notice(112, "City of Bellevue (Seattle (Regional))",
     "Business license data: City of Bellevue.",
     False, ("Seattle (Regional)",)),
    Notice(113, "City of Seattle (Seattle (Regional))",
     "Business license data: City of Seattle.",
     False, ("Seattle (Regional)",)),
    # Tbilisi (notice 114): Geostat's Terms of Use require naming Geostat as
    # the source (also Art. 43(6) of Georgia's statistics law); no logo, no
    # implied endorsement. Wording proposed by the brief, flagged for review.
    Notice(114, "Geostat (Tbilisi)",
     "Business data: National Statistics Office of Georgia (Geostat), Statistical "
     "Business Register, retrieved 2026-10-02; processed by this project. Not "
     "endorsed by Geostat.",
     False, ("Tbilisi",)),
    # Long Beach (notice 129, the extensions' block 129-136): the MapsLB Terms
    # of Use require nothing displayed; they bar any use that "suggests City's
    # endorsement". Displayed by choice, as Seattle's 113, with a
    # no-endorsement sentence. Wording from the licence read of 2026-10-03,
    # flagged for the owner at review time.
    Notice(129, "City of Long Beach (Los Angeles (Regional))",
     "Long Beach business licenses: City of Long Beach, Business Licenses Public "
     "View ([MapsLB](https://maps.longbeach.gov/datasets/LongBeachCA::business-"
     "licenses-public-view/about)), used under the City's [MapsLB Terms of Use]"
     "(https://maps.longbeach.gov/pages/termsofuse). This map selects, categorizes "
     "and aggregates the City's records; it is not a City of Long Beach product, "
     "and the City does not endorse it.",
     False, ("Los Angeles (Regional)",)),
    # Vancouver (Regional)'s extension (notices 130-132, 2026-10-03). Each
    # municipal OGL prescribes its own statement, VERBATIM and not
    # interchangeable: Burnaby prints the BC default ("Licence – British
    # Columbia", en dash; credited "City of Burnaby" with a link, owner
    # 2026-10-02), New Westminster "licenced" with a hyphen, Coquitlam
    # "Licence – Coquitlam" with an en dash. All terminate on breach.
    Notice(130, "City of Burnaby (Vancouver (Regional))",
     "City of Burnaby: Contains information licensed under the Open Government "
     "Licence – British Columbia. [Open Government Licence – City of Burnaby]"
     "(https://data.burnaby.ca/pages/open-government-licence)",
     True, ("Vancouver (Regional)",)),
    Notice(131, "City of New Westminster (Vancouver (Regional))",
     "Contains information licenced under the Open Government Licence - City of "
     "New Westminster. [Open Government Licence - City of New Westminster]"
     "(https://opendata.newwestcity.ca/pages/terms-of-use)",
     True, ("Vancouver (Regional)",)),
    Notice(132, "City of Coquitlam (Vancouver (Regional))",
     "Contains information licensed under the Open Government Licence – Coquitlam. "
     "Business license data © City of Coquitlam. [Open Government Licence – "
     "Coquitlam](https://www.coquitlam.ca/894/Open-Government-Licence)",
     True, ("Vancouver (Regional)",)),
    # Notices 137-140, from staging's licence reads of 2026-10-02
    # (docs/licence_positions.md, its update section). D.C.'s two ArcGIS items
    # carry CC BY 4.0 over the District's CC0 default: credit, licence link,
    # a link to the material, and the changes (s.3(a)). The boundary is
    # reprojected and used to select, never drawn.
    Notice(137, "DLCP and OCTO (Washington D.C.)",
     "Business locations for Washington D.C. are from the Department of "
     "Licensing and Consumer Protection's [Basic Business Licenses]"
     "(https://www.arcgis.com/home/item.html?id=85bf98d3915f412c8a4de706f2d13513), "
     "and the District's boundary from the Office of the Chief Technology "
     "Officer (DC GIS), [Washington DC Administrative Boundary]"
     "(https://www.arcgis.com/home/item.html?id=7241f6d500b44288ad983f0942b39663), "
     "both used under the [Creative Commons Attribution 4.0 International "
     "license](https://creativecommons.org/licenses/by/4.0/). The data has been "
     "modified: the licenses are filtered to storefront categories, grouped into "
     "three categories of this project's own and measured by distance from "
     "Metrorail stations, and the boundary is reprojected and used to select "
     "them, not drawn. Neither office endorses this project.",
     False, ("Washington D.C.",)),
    # Dublin's rail: the NTA's national GTFS, CC BY 4.0 with a prescribed
    # sentence (first, VERBATIM). The developer portal's Fair Usage Policy,
    # with its uncapped indemnity, is NOT accepted (owner, 2026-10-02: "plain
    # CC BY for dublin"); this credit still meets that Policy's s.7. Linked to
    # data.gov.ie, not nationaltransport.ie (that site's terms, clause 5, on
    # linking).
    Notice(138, "National Transport Authority (Dublin)",
     "This data is licensed under CC BY 4.0 and is attributed to the National "
     "Transport Authority. Luas and DART lines and stations for Dublin are from "
     "the NTA's [national GTFS feed](https://data.gov.ie/dataset/nta-gtfs), used "
     "under the [Creative Commons Attribution 4.0 International license]"
     "(https://creativecommons.org/licenses/by/4.0/). The data has been "
     "modified: three routes (Luas Red, Luas Green and DART) are extracted and "
     "redrawn, and the line colors are this map's own. It is provided “as "
     "is”. The National Transport Authority does not endorse this project.",
     False, ("Dublin",)),
    # geo.api.gouv.fr declares no licence; its source dataset ("Contours
    # administratifs", data.gouv 683424e996857155175d4f68) says ODbL, and IGN's
    # ADMIN EXPRESS, which it is built from, says Licence Ouverte. Owner,
    # 2026-10-02: show both, the ODbL s.4.3 notice and the Licence Ouverte
    # source-and-date line. ODbL s.4.6 rests on the repository link. The
    # dataset's last update is from its data.gouv record (read 2026-10-03).
    Notice(139, "geo.api.gouv.fr, Contours administratifs and IGN (France)",
     "Commune boundaries for the French cities on this site are from "
     "geo.api.gouv.fr. Contains information from Contours administratifs "
     "(data.gouv.fr), which is made available here under the [Open Database "
     "License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/). Source: "
     "IGN, ADMIN EXPRESS, under the [Licence Ouverte]"
     "(https://www.etalab.gouv.fr/licence-ouverte-open-licence/), as published "
     "in Contours administratifs, last updated May 5, 2025. The boundaries are "
     "used to select each city's stations and businesses and to name the "
     "commune of a station left out; they are not drawn.",
     False, _FRANCE),
    # MassGIS: public records, "can be used by anyone for any purpose"; a
    # credit is requested, not required, and is shown in the words MassGIS's
    # FAQ gives (read 2026-10-03), the office name as published.
    Notice(140, "MassGIS (Boston)",
     "Boston's boundary, and the town each station outside the city lies in, "
     "are from the Massachusetts Municipalities layer. Source: MassGIS (Bureau "
     "of Geographic Information), Commonwealth of Massachusetts EOTSS.",
     False, ("Boston",)),
    # Liverpool (notice 143): the FSA's FHRS data for the four Merseyrail
    # council areas, Newcastle's notice 62 as Manchester's 84, with the city
    # and date changed.
    Notice(143, "Food Standards Agency (Liverpool)",
     "Liverpool's food businesses are from the Food Standards Agency, UK food hygiene rating "
     "data, extracted on 2026-10-02. Contains public sector information licensed under the "
     "[Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Modified by "
     "this project: storefront types selected, premises at a flat address left out, premises "
     "without a location placed at their postcode's center, or left out where they have no "
     "full postcode, and trade names shown where a business is registered under another name. "
     "No hygiene rating is shown. The Food Standards Agency does not endorse this map.",
     False, ("Liverpool (Regional)",)),
    # Liverpool's postcode centroids (notice 153, staging's number,
    # 2026-10-04): Manchester's notice 85 with the city changed, the same file
    # and edition.
    Notice(153, "Ordnance Survey (Liverpool)",
     "Where the Food Standards Agency lists a Liverpool food business without a map point, it "
     "is placed at the center point of its postcode, from Ordnance Survey's postcode data, used "
     "under the [Open Government Licence v3.0]"
     "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Contains "
     "Ordnance Survey data © Crown copyright and database right 2026. Contains Royal Mail data "
     "© Royal Mail copyright and database right 2026. Contains National Statistics data © Crown "
     "copyright and database right 2026. Ordnance Survey does not endorse this map.",
     False, ("Liverpool (Regional)",)),
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
    "names and route colors are used only to identify each line as its "
    "riders know it. No agency logo, wordmark or route symbol is reproduced."
)

# The sources that neither grant nor forbid reuse, read in this project's
# favor, named in one paragraph (owner, 2026-10-02; first written 2026-09-21
# for Philadelphia alone). The commitment is broader than the standing removal
# commitment in docs/data_sources.md, which triggers on a publisher asking:
# here a publisher saying the use is not permitted is enough. Keep the wording
# consistent with docs/data_sources.md and docs/excluded_categories.md; all
# three say the same thing. Each source's full reading is on About the Data.
_UNSETTLED_TERMS = (
    "**Some sources neither grant nor forbid reuse, and this site reads them "
    "in its favor.** Philadelphia's data carries a City license that grants "
    "nothing and website terms that forbid republication; the City was asked "
    "for its position on 21 September 2026 and has not replied. Sources for "
    "Los Angeles, Miami, Tucson, Dallas, Seattle (King County, Bellevue and "
    "Snohomish County), Amsterdam, Den Haag, Stockholm, Bucharest and Daegu carry no "
    "license, or terms written for a website rather than its data, and "
    "Brazil's census addresses rest on federal law rather than a license. If "
    "any publisher says this use is not permitted, that city comes off the "
    "site without being asked twice, and silence is never treated as "
    "permission."
)

# MTA's terms and WMATA's §6 both forbid stating or implying that the data an
# application provides is "accurate, complete, or timely". This sentence is the
# positive form of that: it says what the maps ARE.
_AS_RECORDED = (
    "Every map here is a snapshot of a public register as it stood on the "
    "retrieval date recorded for that source, redrawn and filtered. Registers "
    "lag the street: a shop that closed last month may still appear, and one "
    "that opened last month may not. Read each map as what a city's own "
    "license records showed on that date, not as a census of what is open."
)


def notices_in_order():
    """Every notice, in docs/data_sources.md's number order."""
    return sorted(_NOTICES, key=lambda n: n.number)


def city_notices(city):
    """The notices a city's page shows as its own, in number order. A notice
    with `per_city` shows that city's own text (OpenStreetMap's rail notice);
    the Required notices page keeps every notice whole."""
    return [n._replace(text=n.per_city(city)) if n.per_city else n
            for n in notices_in_order() if city in n.cities]


# The per-city OpenStreetMap lines and the notice's cities must be one set:
# a city in one and not the other would show the full list, or a line on a
# page the notice does not reach.
_osm_rail = next(n for n in _NOTICES if n.per_city is osm_rail_text)
if set(_osm_rail.cities) != set(OSM_RAIL_BY_CITY):
    raise ValueError(
        "app/osm_notice.py and notice 1's cities differ: only in the notice "
        f"{sorted(set(_osm_rail.cities) - set(OSM_RAIL_BY_CITY))}, only in "
        f"osm_notice {sorted(set(OSM_RAIL_BY_CITY) - set(_osm_rail.cities))}")


def every_page_notices():
    """The notices shown on every page, in number order."""
    return [n for n in notices_in_order() if n.every_page]


def _notice_text(notices):
    return "\n\n".join(f"**{n.heading}** \u2014 {n.text}" for n in notices)


_NOTICES_INTRO = (
    "**Required source notices.** Reproduced as each source's terms "
    "require. Each source's full record, with the web address it was downloaded "
    "from and the date, is on "
    "the \u201cWhere this data comes from\u201d page."
)

# Long unbroken URLs (the Japanese credits carry several) would otherwise
# widen a 375 px page; wrapping them anywhere keeps the text inline and whole.
_NOTICE_STYLE = (
    "<style>.st-key-site-notices p { margin: 0 0 0.4rem; font-size: 0.8rem;"
    " line-height: 1.35; break-inside: avoid; }"
    ".st-key-site-notices p, .st-key-city-notices p, .st-key-all-notices p"
    " { overflow-wrap: anywhere; }"
    "@media (min-width: 900px) { .st-key-site-notices"
    " [data-testid='stCaptionContainer'] { column-count: 2;"
    " column-gap: 2rem; } }</style>"
)


def render_site_notices(city=None, show_links: bool = True,
                        lists_all: bool = False):
    """The footer every page ends with: the three reference pages, the city's
    own notices in full (with `city`, a name as app/cities.py spells it), then
    the notices every page carries and a link to the page that lists all of
    them.

    Called from EVERY page. `lists_all` is for the Required notices page alone,
    which has just shown every notice and so skips the every-page set and the
    link to itself.
    """
    st.divider()
    # The Required notices link sits in this row with the reference pages
    # (owner, 2026-10-03), above the notices; on a page without the row it
    # stands alone in the same place.
    if show_links:
        with st.container(horizontal=True, gap="medium",
                          vertical_alignment="center"):
            st.page_link(ABOUT_DATA_PAGE, label="Where this data comes from")
            st.page_link(EXCLUSIONS_PAGE, label="What is counted, and what is not")
            st.page_link(DIFFERENCES_PAGE, label="Why the maps differ")
            if not lists_all:
                st.page_link(NOTICES_PAGE, label="All required source notices")
    elif not lists_all:
        st.page_link(NOTICES_PAGE, label="All required source notices")
    # The public repository, linked from every page. IDFM's Licence Mobilités
    # Art. 5.8 (Paris) and ODbL 4.6 (Tisseo, TaM, TAG, LiA, Angers, STAR) are
    # each met by a public repository carrying the pipeline and the derived
    # data PROVIDED it is linked from the site; nothing linked it before
    # 2026-10-02. Outside `show_links`, so the reference pages carry it too.
    st.page_link(REPO_URL, label="Code, pipeline and derived data (GitHub)")
    st.markdown(_NOTICE_STYLE, unsafe_allow_html=True)

    # NOT in an st.expander, and that was a real mistake worth naming: these
    # were briefly collapsed behind one, which kept them out of the DOM until
    # a reader clicked. Chicago's terms require its paragraph "at the site
    # where the software application ... can be accessed", and this project's
    # own rule for the OSM attribution is that it must not sit "beneath UI,
    # behind toggles, or off-screen". A required notice behind a toggle is not
    # displayed. So they render inline, always.
    #
    # A city's own notices come first and at body size, not caption size:
    # TransLink's (11) and CRTM's (20) must be prominent, and the Ordnance
    # Survey statements legible, on their pages (owner, 2026-10-02).
    own = city_notices(city) if city else []
    if own:
        with st.container(key="city-notices"):
            st.markdown(_NOTICES_INTRO)
            st.markdown(_notice_text(own))
    st.caption(_AS_RECORDED)
    st.caption(_NON_AFFILIATION)

    if not lists_all:
        if not own:
            st.caption(_NOTICES_INTRO)
        # ONE block, not one element per notice (owner, 2026-10-02: condense
        # the scroll without hiding anything). Each st.caption was its own
        # element with a 16 px gap. All text stays inline and in the DOM; only
        # spacing, size and, from 900 px, two columns change.
        with st.container(key="site-notices"):
            st.caption(_notice_text(
                [n for n in every_page_notices() if n not in own]))
    st.caption(_UNSETTLED_TERMS)


def render_all_notices():
    """The Required notices page's body: every notice, verbatim, in number
    order, at body size."""
    st.markdown(_NOTICE_STYLE, unsafe_allow_html=True)
    st.markdown(_NOTICES_INTRO)
    with st.container(key="all-notices"):
        st.markdown(_notice_text(notices_in_order()))


# --- The city page's own pieces (format set by the owner, 2026-10-01) -------
#
# Order on every city page: render_city_title, then the map (st.iframe at
# height 650; scripts/check_map_attribution.js depends on that height), then
# the date caption and the city's own credits, then the page's bullets,
# render_map_help, render_country_links, and render_site_notices last.
# Nothing renders between the title block and the map, so a reader arriving
# from the macro map sees the map without scrolling.

# Title plus subtitle rather than one long title, which wrapped badly on a
# phone for names like "Kitchener–Waterloo (Regional)" (owner, 2026-10-01).
CITY_SUBTITLE = "Transit-centered commercial density heatmap"


def city_entry(name):
    """The city's entry in cities.CITIES; `name` is the same string the page
    passes to render_city_nav."""
    for city in CITIES:
        if city["name"] == name:
            return city
    raise KeyError(f"{name!r} is not a name in cities.CITIES")


def render_city_title(name):
    """The city's name, centered, with CITY_SUBTITLE beneath it. Also trims
    the empty space above it on city pages only, so more of the map shows on
    the first screen of a phone: the top padding (6rem by default), and the
    16 px gap each invisible element above the title (the style blocks, the
    hidden city links) adds, 64 px measured at 375 px.

    The map is centered under the title (owner, 2026-10-02). Its embed is
    1000 px wide, so this moves it only where the column is wider (1230 px at
    a 1400 px window); at 1000 px and below it already fills the column and
    auto margins resolve to 0.

    The map's teal frame (MAP_FRAME_CSS) goes on the same container, which is
    exactly the map's size at every width; the iframe only rounds its own
    corners to match."""
    st.markdown("<style>[data-testid='stMainBlockContainer'] "
                "{ padding-top: 3.5rem !important; }"
                "[data-testid='stElementContainer']:has(style),"
                "div:has(> .st-key-map-only-nav) { display: none; }"
                "[data-testid='stElementContainer']:has(> iframe[data-testid='stIFrame']) "
                f"{{ margin-left: auto; margin-right: auto; {MAP_FRAME_CSS} }}"
                "iframe[data-testid='stIFrame'] { border-radius: 8px; }</style>",
                unsafe_allow_html=True)
    with st.container(key="city-title"):
        st.title(name, anchor=False, text_alignment="center")
        st.markdown(f'<p class="city-subtitle">{CITY_SUBTITLE}</p>',
                    unsafe_allow_html=True, text_alignment="center")


def render_data_age(name):
    """The date caption under the map for a page that reads no provenance
    file: the city's data_age from cities.py, the text the Overview's city
    list shows."""
    st.caption(f"Data: {city_entry(name)['data_age']}.")


# The layer control's icon as the maps draw it: Leaflet 1.9.3's own image, from
# the CDN every heatmap.html already loads Leaflet from (pipeline/map_common.py
# inverts it on a dark map). Shown on a light tile, as the map's light-mode
# control draws it, so it reads in both page themes.
_LAYERS_ICON = (
    '<img src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/layers.png" '
    'srcset="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/layers-2x.png 2x" '
    'alt="layers icon" width="20" height="20" style="vertical-align:middle;'
    'background:#fff;border:1px solid rgba(0,0,0,0.25);border-radius:4px;'
    'padding:2px;margin:0 2px">'
)


def render_map_help(layers="business categories"):
    """How to use the map, the same on every city page: pipeline/map_common.py
    draws every map with the same controls. `layers` is the page's own name
    for its business layers ("business layer" on a one-bucket map, "three
    business categories (Retail, Food service and Personal services)")."""
    st.markdown(
        "**Using the map**\n\n"
        f"- The layer control {_LAYERS_ICON} in the top left turns the rings "
        f"around each station and the {layers} on and off.\n"
        "- Zoomed out, a business layer shows numbered circles, each counting "
        "the businesses in its area. Zoom in to see individual dots, and hover "
        "over a dot for its details.\n"
        "- Top right: a **Cities** menu and a **Global View** button for "
        "moving between maps, and a light/dark switch. The map opens in "
        "whichever mode the page is using; once you pick one, it carries "
        "across the other city maps.\n"
        "- The heat layer is illustrative: a visual blur, not a statistical "
        "density estimate. Read its color as “roughly where things cluster.”",
        unsafe_allow_html=True,   # the icon's <img>
    )


def render_excluded_stations(name):
    """The stations the city's map leaves out, collapsed under its bullets:
    the rows of outputs/<slug>/excluded_stations.csv, which a page's bullets
    point to as "listed below" (owner, 2026-10-01; What Is Excluded shows only
    a count per city). Nothing renders for a city with no file or an empty one.

    The files do not share a schema (app/station_scope.py). "Why" is the
    file's `reason` as written; a file without one records the place instead
    (located_in, state, commune or municipality), and a file with neither
    holds only stations outside the city's boundary (Madrid, and the
    distance_outside_m files), which station_scope counts the same way."""
    import csv
    from station_scope import slug

    path = (Path(__file__).parent.parent / "outputs" / slug(city_entry(name)["page"])
            / "excluded_stations.csv")
    if not path.exists():
        return
    with open(path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        rows = list(reader)
    if not rows:
        return
    lines_col = next((c for c in ("lines", "line") if c in columns), None)
    place_col = next((c for c in ("located_in", "state", "commune", "municipality")
                      if c in columns), None)

    def why(row):
        if (row.get("reason") or "").strip():
            return row["reason"].strip()
        if place_col and (row.get(place_col) or "").strip():
            return f"in {row[place_col].strip()}"
        return "outside the city"

    header = ["Station"] + (["Lines"] if lines_col else []) + ["Why"]
    body = [[row.get("station", "")] + ([row.get(lines_col, "")] if lines_col else [])
            + [why(row)] for row in rows]
    with st.expander(f"Stations left out ({len(rows):,})"):
        # Sortable by line or reason (owner, 2026-10-03): a button row above
        # the same styled table, not st.dataframe, whose header cannot take
        # the site's styling. "Line" only where the file records lines; the
        # station name breaks ties so a re-sort is stable.
        if len(body) > 1:
            options = ["As listed"] + (["Line"] if lines_col else []) + ["Why"]
            order = st.segmented_control(
                "Sort by", options, default="As listed",
                key=f"stations_left_out_sort_{slug(city_entry(name)['page'])}")
            if order in ("Line", "Why"):
                col = header.index("Lines" if order == "Line" else "Why")
                body = sorted(body, key=lambda r: (str(r[col]).casefold(),
                                                   str(r[0]).casefold()))
        scroll_table(header, body, min_width=480)


def render_country_links(name):
    """Links to the two reference pages, opened on the city's country. The
    deep-link contract with those pages: ?country=<the city's country value
    in cities.py>, which Streamlit URL-encodes."""
    country = city_entry(name)["country"]
    with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
        st.page_link(EXCLUSIONS_PAGE, query_params={"country": country},
                     label=f"What is counted, and what is not: {country}")
        st.page_link(ABOUT_DATA_PAGE, query_params={"country": country},
                     label=f"Where this data comes from: {country}")
