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
from pipeline.theme import AMBIENT_THEME_JS, DARK, LIGHT, rgba  # noqa: E402

OVERVIEW_PAGE = "Overview.py"


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
    ensure();
    new window.parent.MutationObserver(ensure).observe(doc.body, { childList: true, subtree: true });
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
/* The (i) toggle itself, and the pseudo-element some versions draw it with. */
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib-button,
[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib.mapboxgl-compact::after {
    display: none !important; }
/* Invert the whole zoom group (white -> near-black, dark glyph -> light); the
   glyph is the button's own background image, so it cannot be inverted alone. */
body.dark-base [data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-group { filter: invert(0.9); }
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
ABOUT_DATA_PAGE = "pages/90_About_the_Data.py"
EXCLUSIONS_PAGE = "pages/91_What_Is_Excluded.py"

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
     "Powered by CRTM - www.crtm.es. Metro de Madrid station locations and "
     "line geometry are from CRTM's open data, last updated by CRTM on "
     "5 June 2026 and shown here as recorded on that date. Used as datos "
     "explotados "
     "rather than en bruto: the network has been redrawn, its 293 "
     "station-per-line records collapsed to one point per station, stations "
     "outside the termino municipal removed, and each line's eighteen "
     "published codes collapsed to its thirteen real lines. CRTM does not "
     "participate in, sponsor or support this project.",
     True),
    ("TransLink",
     "Route and arrival data used in this product or service is provided by "
     "permission of TransLink. TransLink assumes no responsibility for the "
     "accuracy or currency of the Data used in this product or service.",
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
     "(DENUE). Business locations for Mexico City and Guadalajara are from "
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
    ("OpenStreetMap (Mexican rail)",
     "Rail route geometry and station locations for Mexico City (Metro CDMX "
     "and Tren Ligero) and Guadalajara (Tren Ligero) are from OpenStreetMap, "
     "© OpenStreetMap contributors, available "
     "under the Open Database License. The alignments drawn are OSM's own "
     "geometry; stations, rings and categories are this project's work.",
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
    """The site-level footer: the two data documents, then every notice that
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
