"""Small pieces of UI shared across pages.

Streamlit's multipage app has no shared layout/header mechanism of its own -
each page is its own top-to-bottom script - so anything meant to appear
identically on every page lives here once and gets called from each page,
rather than duplicated per page.
"""

import sys
from pathlib import Path

import streamlit as st

from cities import CITIES, MAP_ONLY_NAV

sys.path.insert(0, str(Path(__file__).parent.parent))
# pipeline/theme.py imports nothing, so it is safe for the lean deploy venv
# (streamlit + pandas only) - the same rule the city pages' config imports
# follow. It is the single source for every chrome colour, shared with the city
# maps' own CSS so a reskin cannot leave the macro map on the old palette.
from pipeline.theme import DARK, LIGHT, rgba  # noqa: E402

OVERVIEW_PAGE = "Overview_&_Introduction.py"


def render_city_nav(current: str):
    """A row at the top of a city page: a link back to the macro map, then
    every mapped city (the current one shown as plain bold text). Lets a
    visitor hop city to city without returning to the map each time.
    `current` must match a name in cities.CITIES.

    In the map-only pilot (cities.MAP_ONLY_NAV) there is no visible switcher.
    The links are still rendered, hidden (see set_base_font): one to the Overview
    and one per city, because the city map's own "All cities" button and city
    menu navigate by clicking them (and read the city names from them)."""
    if MAP_ONLY_NAV:
        with st.container(key="map-only-nav"):
            st.page_link(OVERVIEW_PAGE, label="All cities")
            for city in CITIES:
                st.page_link(city["page"], label=city["name"])
        return
    # A horizontal container sizes each item to its content and wraps onto a
    # second line when the row is too narrow; fixed-width columns clipped the
    # longer city names once a fourth city was added.
    with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
        st.page_link(OVERVIEW_PAGE, label="← All cities (map)")
        for city in CITIES:
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
    apply(saved() === 'dark');
    ensure();
    new window.parent.MutationObserver(ensure).observe(doc.body, { childList: true, subtree: true });
})();
</script>
"""

# Dark styling for the pydeck/mapbox controls (zoom buttons, attribution).
_MACRO_CONTROLS_CSS = """
/* Invert the whole zoom group (white -> near-black, dark glyph -> light); the
   glyph is the button's own background image, so it cannot be inverted alone. */
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-group { filter: invert(0.9); }
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib { background: @@DARK_ATTRIB_BG@@ !important; color: @@DARK_MUTED@@; }
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib a { color: @@DARK_ACCENT@@; }
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
        .replace("@@DARK_ATTRIB_BG@@", rgba(DARK["page"], 0.8))
    )
    assert "@@" not in css, "unresolved placeholder in _MACRO_THEME_CSS"
    st.markdown(css, unsafe_allow_html=True)
    # st.iframe rejects a height of 0, so the script-only frame is 1 px tall; it only
    # needs to run (same-origin access to the page is what lets it add the button).
    st.iframe(_MACRO_THEME_JS.replace("@@KEY@@", MACRO_THEME_KEY), height=1)


# Map-only pilot: hide Streamlit's sidebar (its page list is the other way to reach
# a city) and its expand control, and the hidden links the map's buttons click.
# Turned off by cities.MAP_ONLY_NAV = False; see docs/navigation_sidebar_and_city_links.md.
_MAP_ONLY_CSS = """
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"] { display: none !important; }
.st-key-map-only-nav { display: none; }
"""


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
