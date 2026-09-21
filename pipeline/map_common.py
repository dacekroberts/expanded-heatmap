"""Shared heatmap rendering, extracted from the San Diego and San Francisco
step3_map.py files once two cities existed (they had become ~90% identical
copies). A city's step3_map.py now only supplies what is genuinely
city-specific - map center, transit-line specs, station/business data
paths - and calls render_heatmap().

Nothing here may name a specific taxonomy. Category grouping, the tooltip's
field label, and legend text all come from the city's taxonomy module (see
pipeline/taxonomies/__init__.py for the interface), so a non-NAICS city
renders correctly with no changes to this file.

Standing map-build requirement (docs/project_context.md): every transit
line gets BOTH a permanent on-map label (add_line_label) AND a legend
entry (build_legend). render_heatmap does both for every line passed in.
"""

import html
import json
import re
import zipfile

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from folium.plugins import HeatMap, FastMarkerCluster

from pipeline.taxonomies import CATEGORY_BUCKETS, load_taxonomy_module
from pipeline.theme import AMBIENT_THEME_JS, DARK, LIGHT, css_vars, rgba

# Decimal places BUSINESS coordinates are rounded to before reaching the HTML.
# Folium emits a float's full repr - "40.76248502732357", 17 significant
# digits - for something drawn as a 5-pixel dot, and a city's map repeats that
# once per pin and per heat point. Six places is 0.11 m, which is half a pixel
# at OpenStreetMap's deepest zoom (19), so nothing is visibly moved; five would
# be 1.1 m, about 5 px there, which is why it is not five. Changing this
# re-renders every city: re-baseline the committed outputs and drift check.
#
# One thing is deliberately exempt: the LINE GEOMETRY drawn from a GTFS
# `shapes.txt`, which is emitted at full source precision. See the note in
# load_line_shapes(). Everything else here - business pins, both heat layers,
# station markers, ring centres, line labels - is rounded.
COORD_DP = 6

HEAT_RADIUS = 8
HEAT_BLUR = 10
HEAT_MIN_OPACITY = 0.35
HEAT_GRADIENT = {0.3: "#fee0d2", 0.5: "#fc9272", 0.7: "#fb6a4a", 0.85: "#de2d26", 1.0: "#a50f15"}

# Dark Mode toggle: a plain fixed-position button, NOT a Leaflet control. The
# map is a fixed 1000 px wide and Streamlit's content area is often narrower,
# so anything positioned against the map (Leaflet's top-right corner sits at
# x=1000) can be off-screen; `position: fixed` anchors to the visible iframe,
# as the legend does (checked at 1024 px and 375 px wide). It toggles a
# `dark-base` class on <body> and remembers the choice in localStorage (shared
# by every map served from the same origin, so Dark carries from map to map).
# Only the tile pane is filtered (invert + hue-rotate keeps water blue), so no
# second base layer or tile provider is needed; overlays are recoloured by the
# rules below. Palette is one variable block: retheme it there.
_THEME_TOGGLE_TEMPLATE = """
<style>
    #map-actions { position: fixed; top: 10px; right: 10px; z-index: 10000;
        display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end;
        max-width: calc(100% - 56px); }   /* clear of the zoom control on a phone */
    .map-btn {
        font: 600 13px sans-serif; padding: 6px 12px; cursor: pointer;
        background: @@LIGHT_SURFACE@@; color: @@LIGHT_TEXT@@;
        border: 1px solid @@LIGHT_BORDER@@;
        border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }
    .map-btn[hidden] { display: none; }
    .map-btn:focus-visible { outline: 2px solid @@LIGHT_ACCENT@@; outline-offset: 2px; }
    #city-menu { width: 84px; text-overflow: ellipsis; }
    @media (max-width: 480px) {
        #map-actions { gap: 6px; }
        .map-btn { padding: 6px 7px; font-size: 12px; }
        #city-menu { width: 78px; }
    }
    .dark-base { color-scheme: dark; @@DARK_VARS@@
        background: var(--dm-page); }
    .dark-base .leaflet-tile-pane {
        filter: invert(1) hue-rotate(180deg) brightness(0.85) contrast(0.9) saturate(0.7); }
    .dark-base .map-btn { background: var(--dm-surface); color: var(--dm-text);
        border-color: var(--dm-border); }
    .dark-base .map-btn:hover { background: var(--dm-surface-hover); }
    /* These two selectors match on the LIGHT ring and station colours, which
       is only safe because each is used nowhere else on the map. Both the
       selector and the drawing code below read the same LIGHT value, so they
       cannot drift apart - changing one used to silently break the other. */
    .dark-base path.leaflet-interactive[stroke="@@LIGHT_RING@@"] { stroke: var(--dm-ring); }
    .dark-base path.leaflet-interactive[stroke="@@LIGHT_STATION@@"] {
        stroke: var(--dm-station); fill: var(--dm-station); }
    .dark-base .leaflet-overlay-pane path[stroke-width="4"] { filter: brightness(1.55) saturate(0.9); }
    .dark-base .map-legend span[style*="height:3px"] { filter: brightness(1.55) saturate(0.9); }
    .dark-base .leaflet-marker-icon div[style*="text-shadow"] {
        filter: brightness(1.8);
        text-shadow: -1px -1px 0 var(--dm-page), 1px -1px 0 var(--dm-page),
                     -1px 1px 0 var(--dm-page), 1px 1px 0 var(--dm-page),
                     0 0 6px var(--dm-page) !important; }
    .dark-base .map-legend { background: var(--dm-surface) !important;
        color: var(--dm-text) !important; border-color: var(--dm-border) !important; }
    .dark-base .leaflet-bar, .dark-base .leaflet-control-layers {
        border: 1px solid var(--dm-border); box-shadow: none; }
    .dark-base .leaflet-bar a, .dark-base .leaflet-control-layers {
        background-color: var(--dm-surface); color: var(--dm-text); }
    .dark-base .leaflet-bar a { border-bottom-color: var(--dm-border); }
    .dark-base .leaflet-bar a:hover, .dark-base .leaflet-bar a:focus {
        background-color: var(--dm-surface-hover); }
    .dark-base .leaflet-bar a.leaflet-disabled {
        background-color: var(--dm-surface-disabled); color: var(--dm-disabled-text); }
    .dark-base .leaflet-control-layers-toggle { filter: invert(1); }
    .dark-base .leaflet-control-layers-separator { border-top-color: var(--dm-border); }
    .dark-base .leaflet-control-attribution { background: @@DARK_ATTRIB_BG@@; color: var(--dm-muted); }
    .dark-base .leaflet-control-attribution a { color: var(--dm-accent); }
    .dark-base .leaflet-tooltip { background: var(--dm-surface); color: var(--dm-text);
        border-color: var(--dm-border); box-shadow: 0 1px 4px rgba(0,0,0,0.5); }
    .dark-base .leaflet-tooltip-top:before { border-top-color: var(--dm-border); }
    .dark-base .leaflet-tooltip-bottom:before { border-bottom-color: var(--dm-border); }
    .dark-base .leaflet-tooltip-left:before { border-left-color: var(--dm-border); }
    .dark-base .leaflet-tooltip-right:before { border-right-color: var(--dm-border); }
</style>
<div id="map-actions">
    <select id="city-menu" class="map-btn" hidden aria-label="Go to another city">
        <option value="" selected disabled>Cities</option>
    </select>
    <button id="back-to-map" class="map-btn" type="button" hidden
        aria-label="Back to the map of all cities">&larr; All cities</button>
    <button id="theme-toggle" class="map-btn" type="button" aria-pressed="false">&#9790; Dark mode</button>
</div>
<script>
(function () {
    var KEY = 'expanded-heatmap-theme';
    var btn = document.getElementById('theme-toggle');
    function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
    function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
    function apply(dark) {
        document.body.classList.toggle('dark-base', dark);
        btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
        btn.textContent = dark ? '\\u2600 Light mode' : '\\u263E Dark mode';
    }
@@AMBIENT_JS@@
    // A remembered click wins; otherwise follow the surrounding page, so a map
    // embedded in a dark app page does not open as a white rectangle.
    var choice = saved();
    apply(choice === 'dark' || choice === 'light'
          ? choice === 'dark'
          : ambientPrefersDark());
    btn.addEventListener('click', function () {
        var dark = !document.body.classList.contains('dark-base');
        apply(dark);
        save(dark ? 'dark' : 'light');
    });
    window.addEventListener('storage', function (e) {
        if (e.key === KEY) apply(e.newValue === 'dark');
    });
    // Follow the OS preference while the visitor has made no explicit choice.
    // NOTE: devtools colour-scheme emulation updates matchMedia().matches
    // WITHOUT dispatching this event inside an iframe, so this listener can
    // only be tested with a real OS theme switch (docs/theming.md).
    if (window.matchMedia) {
        var mq = window.matchMedia('(prefers-color-scheme: dark)');
        if (mq.addEventListener) {
            mq.addEventListener('change', function (e) {
                if (!saved()) apply(e.matches);
            });
        }
    }

    // "All cities" button: only when this map is embedded in the app (it has a
    // parent page to go back to); opened on its own it stays hidden. It clicks
    // the app's own link to the Overview, so Streamlit navigates in place, and
    // saves the current theme first so the macro map opens in the same mode.
    var back = document.getElementById('back-to-map');
    function trimSlash(p) { while (p.length > 1 && p.charAt(p.length - 1) === '/') p = p.slice(0, -1); return p; }
    function overviewLink() {
        var doc = window.parent.document, links = doc.querySelectorAll('a[href]');
        for (var i = 0; i < links.length; i++) {          // the page's own link to the Overview
            if (links[i].textContent.indexOf('All cities') !== -1) return links[i];
        }
        var here = window.parent.location.pathname;      // else the link to the app's root
        var root = trimSlash(here.substring(0, here.lastIndexOf('/') + 1));
        for (var j = 0; j < links.length; j++) {
            if (trimSlash(links[j].pathname) === root) return links[j];
        }
        return null;
    }
    // City menu: the other cities, read from the hidden links the app page renders
    // (one per city, from app/cities.py), so a new city appears here without
    // regenerating any map. The city this page belongs to is left out.
    var menu = document.getElementById('city-menu');
    function cityLinks() {
        var box = window.parent.document.querySelector('.st-key-map-only-nav');
        var out = [];
        if (!box) return out;
        var links = box.querySelectorAll('a');
        for (var i = 0; i < links.length; i++) {
            if (links[i].textContent.indexOf('All cities') === -1) out.push(links[i]);
        }
        return out;
    }
    function currentCity() {                    // /Chicago_Heatmap -> Chicago
        var parts = window.parent.location.pathname.split('/').filter(Boolean);
        var seg = decodeURIComponent(parts.length ? parts[parts.length - 1] : '');
        var tail = '_Heatmap';
        if (seg.slice(-tail.length) === tail) seg = seg.slice(0, -tail.length);
        return seg.split('_').join(' ');
    }
    function fillMenu() {
        if (menu.options.length > 1) return;    // already built
        var here = currentCity(), links = cityLinks();
        for (var i = 0; i < links.length; i++) {
            var name = links[i].textContent.trim();
            if (name === here) continue;
            var o = document.createElement('option');
            o.value = name; o.textContent = name;
            menu.appendChild(o);
        }
        menu.hidden = menu.options.length < 2;
    }
    function goTo(link) {
        save(document.body.classList.contains('dark-base') ? 'dark' : 'light');
        if (link) link.click();
    }
    if (window.parent !== window) {
        back.hidden = false;
        back.addEventListener('click', function () { goTo(overviewLink()); });
        fillMenu();
        setTimeout(fillMenu, 800);              // the page's links may render just after this frame
        setTimeout(fillMenu, 2500);
        menu.addEventListener('mousedown', fillMenu);
        menu.addEventListener('change', function () {
            var links = cityLinks(), want = menu.value, hit = null;
            for (var i = 0; i < links.length; i++) {
                if (links[i].textContent.trim() === want) hit = links[i];
            }
            menu.selectedIndex = 0;
            goTo(hit);
        });
    }
})();
</script>
"""

# Resolved once, from pipeline/theme.py, so no colour is written twice. The
# template uses @@NAME@@ placeholders rather than str.format because it is full
# of literal CSS and JS braces.
THEME_TOGGLE_HTML = (
    _THEME_TOGGLE_TEMPLATE
    .replace("@@AMBIENT_JS@@", AMBIENT_THEME_JS)
    .replace("@@DARK_VARS@@", css_vars(DARK))
    .replace("@@DARK_ATTRIB_BG@@", rgba(DARK["page"], 0.8))
    .replace("@@LIGHT_SURFACE@@", LIGHT["surface"])
    .replace("@@LIGHT_TEXT@@", LIGHT["text"])
    .replace("@@LIGHT_BORDER@@", LIGHT["border"])
    .replace("@@LIGHT_ACCENT@@", LIGHT["accent"])
    .replace("@@LIGHT_RING@@", LIGHT["ring"])
    .replace("@@LIGHT_STATION@@", LIGHT["station"])
)
assert "@@" not in THEME_TOGGLE_HTML, "unresolved placeholder in THEME_TOGGLE_HTML"

# A native <details>/<summary>, so the legend collapses and expands with a
# click and needs no script. Open by default; collapsed it shrinks to a small
# "Legend" tab and stops covering the map.
LEGEND_HTML = """
<details open class="map-legend" style="
    position: fixed; bottom: 24px; right: 24px; z-index: 9999;
    background: white; padding: 8px 14px; border: 1px solid #999;
    border-radius: 4px; font-family: sans-serif; font-size: 13px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
">
  <summary style="font-weight: bold; cursor: pointer; user-select: none;
    outline: none;">Legend</summary>
  <div style="font-weight: bold; margin: 8px 0 6px;">Business Category</div>
  {category_rows}
  <div style="font-weight: bold; margin: 10px 0 6px;">Transit Lines</div>
  {line_rows}
</details>
"""
# The legend is position:fixed so it stays put while the map scrolls inside its
# iframe (the map lays out at _MAP_W, which is wider than the app's column).
# That has a cost: "fixed" anchors to the frame's VISIBLE width, so when the
# frame is narrower than the map the legend slides left, away from the
# bottom-right corner the label layout reserved for it (_layout_labels' legend
# obstacle is computed at _MAP_W). Measured 2026-09-21: at a 1024px browser
# window the frame is 854px, the legend shifts ~146px left, and it covers four
# of New York's line labels.
#
# So: collapse the legend exactly when the frame is too narrow to show the map
# at its true width. Collapsed it is a small "Legend" tab that covers nothing,
# and it is still one click from open. Wide frames are unaffected.
#
# A reader who opens or closes it themselves owns it from then on - the
# breakpoint stops fighting them (`touched`).
LEGEND_AUTOFIT_SCRIPT = """
<script>
(function () {
    var MAP_W = __MAP_W__;
    var legend = document.querySelector('details.map-legend');
    if (!legend) return;
    var touched = false;

    // Reader ownership is detected from an actual user gesture, NOT from the
    // `toggle` event. `toggle` also fires for programmatic changes, and Chrome
    // queues one for a <details open> element that lands AFTER this script
    // attaches its listener - on a wide load `fit()` returns early, so that
    // stray event used to set `touched` permanently and kill the breakpoint
    // for the rest of the page's life (found by deploy-verify, 2026-09-21: the
    // legend then covered four of New York's labels for anyone who narrowed
    // their window rather than loading narrow). A click on the <summary> is
    // unambiguous, and keyboard activation dispatches a click too.
    var summary = legend.querySelector('summary');
    if (summary) {
        summary.addEventListener('click', function () { touched = true; });
    }

    function fit() {
        if (touched) return;
        var narrow = (document.documentElement.clientWidth || window.innerWidth) < MAP_W;
        if (narrow !== !legend.open) legend.open = !narrow;
    }
    fit();
    // Second pass: the 1000px map forces scrollbars at load, so the first
    // measurement can read ~15px short; once PHONE_FIT_SCRIPT has resized the
    // container they are gone and the width is accurate.
    requestAnimationFrame(fit);
    window.addEventListener('resize', fit);
})();
</script>
"""
# The map is laid out at a fixed _MAP_W x _MAP_H because Leaflet.heat throws an
# uncaught IndexSizeError when its container's size is unresolved at init
# (github.com/Leaflet/Leaflet.heat/issues/95), which silently kills every layer
# added after it. That fixed width is correct at init and wrong afterwards: in a
# frame narrower than the map, the reader sees a 343px slice of a 1000px map and
# has to scroll inside the iframe to find anything. Measured 2026-09-21 at 375px:
# 1 of New York's 11 line labels visible, 0 of Chicago's 7.
#
# So the container keeps its fixed size for initialisation and is resized to the
# frame immediately afterwards. Resizing AFTER init is safe - the bug is about an
# unresolved size at construction, not a small one - and `invalidateSize()` is
# Leaflet's own supported way to do it. The view is then re-fitted to the station
# bounds, which Python supplies rather than the script sniffing marker colours.
#
# What this does NOT fix: label PLACEMENT. `_layout_labels` chooses label
# positions server-side against a _MAP_W x _MAP_H canvas, so at phone width they
# can overlap each other and the cluster badges. Going from "one label visible"
# to "most labels visible but some crowded" is the improvement; laying them out
# correctly for a phone would need a second render at phone dimensions. See
# PLAN.md.
PHONE_FIT_SCRIPT = """
<script>
(function () {
    var MAP_W = __MAP_W__, MAP_H = __MAP_H__;
    var BOUNDS = __BOUNDS__;            // [[south, west], [north, east]]
    var NAME = "__MAP_NAME__";
    var tries = 0;

    // Folium renders body HTML before the figure's script block, so this runs
    // before the map exists - poll for it rather than assuming.
    function ready() {
        var m = window[NAME];
        if (m && m.invalidateSize) return m;
        return null;
    }

    function apply(m) {
        var el = m.getContainer();
        var w = document.documentElement.clientWidth || window.innerWidth;
        var target = Math.min(w, MAP_W);
        if (Math.abs(el.getBoundingClientRect().width - target) < 1) return;
        el.style.width = target + "px";
        document.body.style.width = target + "px";
        m.invalidateSize();
        if (target < MAP_W && BOUNDS) {
            // Generous padding because BOUNDS holds label ANCHORS, and a label's
            // text box extends past its anchor by up to ~70px.
            m.fitBounds(L.latLngBounds(BOUNDS), {padding: [26, 18], animate: false});
        }
    }

    function start() {
        var m = ready();
        if (!m) {
            if (tries++ < 60) return setTimeout(start, 100);
            return;
        }
        // Applied more than once on purpose. At load the 1000px-wide map forces
        // a horizontal scrollbar, which costs enough height to force a vertical
        // one, so `clientWidth` reads ~15px short; once the first pass has
        // shrunk the container both scrollbars go away and the measurement is
        // right, but no resize event is dispatched to notice that. The later
        // passes also settle a transient seen on the heaviest map at phone
        // width, where the pane transform lagged a correct fit. apply() returns
        // immediately once the width already matches, so the extra passes are
        // free. (deploy-verify, 2026-09-21)
        apply(m);
        requestAnimationFrame(function () { apply(m); });
        [120, 400, 1200].forEach(function (d) {
            setTimeout(function () { apply(m); }, d);
        });
        var t = null;
        window.addEventListener("resize", function () {
            clearTimeout(t);
            t = setTimeout(function () { apply(m); }, 150);
        });
    }
    start();
})();
</script>
"""
LEGEND_ROW = """
  <div style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:11px; height:11px;
      border-radius:50%; background:{color}; margin-right:7px;
      border:1px solid rgba(0,0,0,0.3);"></span>{label}
  </div>
"""
# A short colored line swatch, not a dot - distinguishes transit lines from
# business categories at a glance, so a reader isn't relying on the on-map
# line labels alone (automatic placement can land imperfectly).
LEGEND_LINE_ROW = """
  <div style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:16px; height:3px;
      background:{color}; margin-right:7px;
      border-radius:2px;"></span>{label}
  </div>
"""


def load_line_shapes(gtfs_zip, line_specs, system_name):
    """Real line geometries from GTFS shapes.txt - the actual alignment,
    not straight lines between stations.

    line_specs: {key: (shape_id, color, real-world public name, label end)}
    where label end is None (automatic), "start" or "end" - which end of the
    line its label goes at (see add_line_label).

    `shape_id` may instead be a tuple/list of shape_ids, for a line that is one
    named thing to riders but several alignments in the feed. New York needs
    this: a subway trunk (the "6 Av (B/D/F/M)" line) runs as one line through
    the core and branches outside it, so its geometry is several shapes sharing
    one label, one colour and one legend entry. A single shape_id behaves
    exactly as before.

    Returns {key: (segments, color, label, end)} where `segments` is a list of
    coordinate lists, longest first - so `segments[0]` is the line's primary
    alignment, which is what the label is anchored to.
    """
    if not gtfs_zip.exists():
        print(f"No GTFS feed at {gtfs_zip} - skipping the {system_name} line overlay.")
        return {}
    with zipfile.ZipFile(gtfs_zip) as z, z.open("shapes.txt") as f:
        shapes = pd.read_csv(f, dtype=str)
    shapes["shape_pt_sequence"] = shapes["shape_pt_sequence"].astype(int)

    lines = {}
    for key, (shape_id, color, label, end) in line_specs.items():
        shape_ids = [shape_id] if isinstance(shape_id, str) else list(shape_id)
        segments = []
        for sid in shape_ids:
            pts = shapes[shapes["shape_id"] == sid].sort_values("shape_pt_sequence")
            if pts.empty:
                print(f"WARNING: shape_id {sid!r} for the {label} not in this "
                      "GTFS feed - check trips.txt for its current most-used shape_id.")
                continue
            # NOT rounded to COORD_DP, unlike every other coordinate in this
            # module, and the reason is licensing rather than precision.
            #
            # These vertices are the one place the project reproduces an
            # agency's data verbatim: a polyline IS the feed's own geometry.
            # Two agencies restrict altering it - LA Metro requires you "not
            # change, tamper, dismantle, augment, misrepresent or otherwise
            # modify the Transport Information", and the MTA's terms say "You
            # will not modify or delete any of the data" (while permitting "an
            # app that uses some but not all of the data", which is what
            # dropping commuter rail and drawing 29 services as 11 trunks is).
            # Rounding to 0.11 m is invisible and would almost certainly never
            # be anyone's idea of modifying a transit feed, but the project's
            # rule is to comply rather than to read such a clause generously.
            #
            # Measured 2026-09-21, over EVERY vertex rather than a sample -
            # sampling the first few thousand characters gave the wrong answer
            # for the one feed that matters:
            #   LA Metro  max 10 dp, 21.0% of coords over 6 dp  <- WAS rounded
            #   MTS       max  8 dp, 99.2% over 6 dp            <- WAS rounded
            #   CTA       max  8 dp, 99.2% over 6 dp            <- WAS rounded
            #   MTA       max  6 dp,  0.0% over 6 dp            <- no-op
            #   SFMTA     max  6 dp,  0.0% over 6 dp            <- no-op
            #   SEPTA     max  6 dp,  0.0% over 6 dp            <- no-op
            # So the old rounding really was altering LA Metro's geometry, on a
            # fifth of its vertices - the tightest licence in the project - and
            # this exemption is what makes the recorded verdict ("the rail
            # alignment is the feed's own geometry, displayed as that line")
            # literally true. MTA's clause, which prompted the check, turned
            # out to be moot: its feed is already 6 dp. MTS and CTA were being
            # rounded too, and neither restricts modification.
            #
            # PLAN.md also carries a live proposal to lower COORD_DP to 5 dp to
            # shrink New York's map. Keep this exemption if you do: at 5 dp the
            # old behaviour would have begun altering MTA's geometry as well,
            # as a silent side effect of a size tweak.
            #
            # Station coordinates deliberately stay rounded: most cities derive
            # them by averaging a parent station's platform stops, so they are
            # this project's own computed values rather than agency data - and
            # unrounded they emit 15 dp of floating-point noise.
            segments.append(list(zip(pts["shape_pt_lat"].astype(float),
                                     pts["shape_pt_lon"].astype(float))))
        if not segments:
            continue
        # Longest first: the trunk's main alignment anchors the label, and a
        # short branch never captures it.
        segments.sort(key=len, reverse=True)
        lines[key] = (segments, color, label, end)
    return lines


_M_PER_DEG_LAT = 110540.0
_M_PER_DEG_LON_EQUATOR = 111320.0


def _to_xy_m(points, ref_lat):
    """(lat, lon) pairs -> local planar metres (east, north). Accurate enough
    at city scale for comparing distances."""
    a = np.asarray(points, dtype=float)
    return np.column_stack([
        a[:, 1] * _M_PER_DEG_LON_EQUATOR * np.cos(np.radians(ref_lat)),
        a[:, 0] * _M_PER_DEG_LAT,
    ])


def _tail_end(coords, other_lines, forced=None):
    """Pick the end of `coords` to label and return (lat, lon, ux, uy): the
    tip and the unit vector pointing outward from it (east, north).

    The end chosen is the one farthest from every other line, i.e. the tail
    of the line that stands alone rather than the end tangled with other
    lines' labels and pins; `forced` ("start"/"end") overrides. The outward
    direction is measured a few points in from the tip so a wiggle in the
    last segment doesn't flip it."""
    ref_lat = coords[0][0]
    if forced in ("start", "end"):
        use_end = forced == "end"
    else:
        others = [c for c in other_lines if len(c)]
        if others:
            other_xy = _to_xy_m(np.vstack([np.asarray(c, dtype=float) for c in others]), ref_lat)
            gaps = []
            for tip in (coords[0], coords[-1]):
                tip_xy = _to_xy_m([tip], ref_lat)[0]
                gaps.append(np.sqrt(((other_xy - tip_xy) ** 2).sum(axis=1)).min())
            use_end = gaps[1] >= gaps[0]
        else:
            use_end = True
    k = min(6, len(coords) - 1)
    tip, inner = (coords[-1], coords[-1 - k]) if use_end else (coords[0], coords[k])
    d = _to_xy_m([tip], ref_lat)[0] - _to_xy_m([inner], ref_lat)[0]
    norm = float(np.hypot(*d)) or 1.0
    return tip[0], tip[1], d[0] / norm, d[1] / norm


def _label_offset(label, ux, uy):
    """Pixel offset (dx, dy; screen y grows downward) of a label's centre from
    its tip, and the label's half width/height. The label is pushed out along
    (ux, uy) just far enough that its own box clears the tip whatever the
    angle. ~14px bold text is ~8.2 px per character."""
    half_w = (len(label) * 8.2 + 10) / 2
    half_h = 11
    gap = 6
    reach = min(half_w / abs(ux) if abs(ux) > 1e-6 else 1e9, half_h / abs(uy) if abs(uy) > 1e-6 else 1e9)
    return ux * (reach + gap), -uy * (reach + gap), half_w, half_h


def add_line_label(feature_group, tip, label, color):
    """A permanent, always-visible line-name label at the tail end of the line
    - NOT a hover tooltip. Use the line's real public-facing name.

    `tip` is (lat, lon, ux, uy) from _tail_end: the label is centred just
    beyond the tip along the line's own direction, offset in pixels by the
    label's own size so it clears the line whatever the angle, and it stays
    put relative to the tip at every zoom."""
    lat, lon, ux, uy = tip
    dx, dy, _hw, _hh = _label_offset(label, ux, uy)
    # zIndexOffset lifts the label above the business-cluster badges: without
    # it a large downtown cluster is drawn on top of the label and hides it.
    folium.Marker(
        location=[round(lat, COORD_DP), round(lon, COORD_DP)],
        zIndexOffset=1000,
        icon=folium.DivIcon(
            icon_size=(0, 0),
            icon_anchor=(0, 0),
            html=f"""
            <div style="
                position: absolute; left: 0; top: 0;
                transform: translate(-50%, -50%) translate({dx:.1f}px, {dy:.1f}px);
                font-size: 14px; font-weight: bold; color: {color};
                text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff,
                             -1px 1px 0 #fff, 1px 1px 0 #fff,
                             0 0 6px #fff;
                white-space: nowrap; pointer-events: none;
            ">{html.escape(label)}</div>
        """),
    ).add_to(feature_group)


def _fit_view(points, px_w=1000, px_h=650, fill=0.85, min_zoom=8.0, max_zoom=15.0):
    """(centre, zoom) that shows every (lat, lon) in `points` inside a
    px_w x px_h Leaflet map with a margin. Leaflet's world is 256*2^z px wide,
    so ground metres per pixel = 156543.03*cos(lat)/2^z. The zoom is floored
    to a quarter step (the map is created with zoomSnap=0.25) so it can only
    err toward showing slightly more."""
    a = np.asarray(points, dtype=float)
    lat_c = (a[:, 0].max() + a[:, 0].min()) / 2
    lon_c = (a[:, 1].max() + a[:, 1].min()) / 2
    ext_x = max((a[:, 1].max() - a[:, 1].min()) * _M_PER_DEG_LON_EQUATOR * np.cos(np.radians(lat_c)), 1.0)
    ext_y = max((a[:, 0].max() - a[:, 0].min()) * _M_PER_DEG_LAT, 1.0)
    z = np.log2(fill * 156543.03 * np.cos(np.radians(lat_c)) * min(px_w / ext_x, px_h / ext_y))
    z = float(np.floor(z * 4) / 4)
    return [lat_c, lon_c], max(min_zoom, min(z, max_zoom))


_LABEL_ANGLES = (0, 40, -40, 80, -80)
_ALONG_FRACTIONS = (0.06, 0.12, 0.18, 0.25, 0.32, 0.40, 0.48)
_MAP_W, _MAP_H = 1000, 650


def _project_px(lat, lon, zoom):
    """Leaflet world-pixel coordinates of (lat, lon) at `zoom`."""
    scale = 256 * 2 ** zoom
    x = (lon + 180) / 360 * scale
    y = (0.5 - np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)) / (2 * np.pi)) * scale
    return x, y


def _unproject_px(x, y, zoom):
    scale = 256 * 2 ** zoom
    lon = x / scale * 360 - 180
    lat = np.degrees(2 * np.arctan(np.exp((0.5 - y / scale) * 2 * np.pi)) - np.pi / 2)
    return float(lat), float(lon)


def _boxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _label_candidates(coords, tip):
    """Places a line's label may go, best first, each (lat, lon, ux, uy).

    First the tail-end tip pointing straight out (and swung a little either
    way); then, if those are taken, spots further along the line from that
    tail, with the label sitting beside the line (either side)."""
    cands = []
    for angle in _LABEL_ANGLES:
        r = np.radians(angle)
        cands.append((tip[0], tip[1],
                      tip[2] * np.cos(r) - tip[3] * np.sin(r),
                      tip[2] * np.sin(r) + tip[3] * np.cos(r)))
    pts = list(coords)
    if np.hypot(pts[0][0] - tip[0], pts[0][1] - tip[1]) > np.hypot(pts[-1][0] - tip[0], pts[-1][1] - tip[1]):
        pts.reverse()   # so pts[0] is the tail end
    xy = _to_xy_m(pts, pts[0][0])
    seg = np.hypot(*np.diff(xy, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    total = cum[-1]
    if total <= 0:
        return cands
    for f in _ALONG_FRACTIONS:
        i = int(np.searchsorted(cum, f * total))
        i = min(max(i, 1), len(pts) - 2)
        tx, ty = xy[i + 1] - xy[i - 1]
        n = float(np.hypot(tx, ty)) or 1.0
        for sign in (1, -1):
            cands.append((pts[i][0], pts[i][1], -ty / n * sign, tx / n * sign))
    return cands


def _layout_labels(points, candidates, labels, n_lines, center, zoom):
    """Place every label on screen at `center`/`zoom` without overlapping
    each other, another label's anchor point, the open legend, the map's own
    controls, or the map edge.

    Returns None if a station would fall off the map at this view, else
    (cost, {key: (lat, lon, ux, uy)}) where cost counts labels that could not
    be placed cleanly (0 = all clean)."""
    cx, cy = _project_px(center[0], center[1], zoom)

    def to_screen(lat, lon):
        x, y = _project_px(lat, lon, zoom)
        return x - cx + _MAP_W / 2, y - cy + _MAP_H / 2

    for lat, lon in points:
        sx, sy = to_screen(lat, lon)
        if not (15 <= sx <= _MAP_W - 15 and 15 <= sy <= _MAP_H - 15):
            return None

    # The legend (open) sits bottom-right; the zoom and layer controls top-left.
    legend_h = 178 + 19 * n_lines
    obstacles = [(_MAP_W - 24 - 274, _MAP_H - 24 - legend_h, _MAP_W - 24, _MAP_H - 24), (0, 0, 60, 110)]
    placed, chosen, cost = [], {}, 0
    # Longest names first: they have the fewest places they fit.
    for key in sorted(candidates, key=lambda k: -len(labels[k])):
        best = None
        for cand in candidates[key]:
            lat, lon, ux, uy = cand
            sx, sy = to_screen(lat, lon)
            dx, dy, hw, hh = _label_offset(labels[key], ux, uy)
            box = (sx + dx - hw, sy + dy - hh, sx + dx + hw, sy + dy + hh)
            inside = box[0] >= 0 and box[1] >= 0 and box[2] <= _MAP_W and box[3] <= _MAP_H
            if best is None:
                best = (cand, box)   # fallback: the preferred spot, even if it collides
            if inside and not any(_boxes_overlap(box, o) for o in obstacles + placed):
                best = (cand, box)
                break
        else:
            cost += 1
        chosen[key] = best[0]
        placed.append(best[1])
        # keep later labels off this line's anchor point too
        lat, lon = best[0][0], best[0][1]
        sx, sy = to_screen(lat, lon)
        placed.append((sx - 5, sy - 5, sx + 5, sy + 5))
    return cost, chosen


def _choose_view(points, candidates, labels, n_lines, center=None, zoom=None):
    """Pick the default map view and every label's position together.

    Start from the fit that shows all stations and the labels' preferred
    (tail-end) tips. Labels that would land on top of each other (or under the
    open legend) move elsewhere along their own lines; if that still can't
    separate them, the view zooms out in quarter steps and shifts away from the
    legend, taking the closest view that works. Explicit `center`/`zoom` are
    respected (labels are still laid out around them).
    Returns (center, zoom, {key: (lat, lon, ux, uy)})."""
    first = {k: c[0] for k, c in candidates.items()}
    base_center, base_zoom = _fit_view(points + [(t[0], t[1]) for t in first.values()])
    fixed = center is not None and zoom is not None
    center = base_center if center is None else center
    zoom = base_zoom if zoom is None else zoom

    views = [(center, zoom)]
    if not fixed:
        shifts = [(0, 0), (-60, 0), (0, -60), (-60, -60), (-120, 0), (0, -120),
                  (-120, -60), (-60, -120), (-120, -120), (-180, -60), (-180, -120)]
        views = []
        for dz in (0.0, 0.25, 0.5, 0.75, 1.0):
            z = max(8.0, zoom - dz)
            bx, by = _project_px(center[0], center[1], z)
            for sx, sy in shifts:
                # the content moves by (sx, sy), so the centre moves the opposite way
                views.append((list(_unproject_px(bx - sx, by - sy, z)), z))
    best = None
    for c, z in views:
        result = _layout_labels(points, candidates, labels, n_lines, c, z)
        if result is None:
            continue
        if best is None or result[0] < best[0]:
            best = (result[0], c, z, result[1])
        if result[0] == 0:
            break
    if best is None:   # nothing fits with every station on screen: keep the fit as is
        return center, zoom, first
    return best[1], best[2], best[3]


def nearest_station_and_ring(businesses, stations, crs_geographic, crs_projected,
                             ring_edges_meters, ring_labels):
    """For each business: its nearest station and which ring band that
    distance falls in relative to that station - built only for the pin
    tooltip, separate from any aggregate ring analysis."""
    biz_gdf = gpd.GeoDataFrame(
        businesses,
        geometry=gpd.points_from_xy(businesses["longitude"], businesses["latitude"]),
        crs=crs_geographic,
    ).to_crs(crs_projected)
    sta_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=crs_geographic,
    ).to_crs(crs_projected)

    biz_xy = np.column_stack([biz_gdf.geometry.x, biz_gdf.geometry.y])
    sta_xy = np.column_stack([sta_gdf.geometry.x, sta_gdf.geometry.y])
    dist = np.sqrt(((biz_xy[:, None, :] - sta_xy[None, :, :]) ** 2).sum(axis=2))
    nearest_idx = dist.argmin(axis=1)
    nearest_dist = dist.min(axis=1)

    def band(d):
        for i, ring_label in enumerate(ring_labels):
            if ring_edges_meters[i] <= d < ring_edges_meters[i + 1]:
                return f"Ring {i + 1} ({ring_label})"
        outer_mi = ring_edges_meters[-1] / 1609.344
        return f"Beyond ring {len(ring_labels)} (>{outer_mi:.1f} mi)"

    return sta_gdf["station"].to_numpy()[nearest_idx], [band(d) for d in nearest_dist]


def _esc(value):
    """HTML-escape a value for the tooltip. Business names come from public
    datasets but are still free text - an unescaped '<' or '&' breaks the
    hover text or injects markup."""
    return "" if pd.isna(value) else html.escape(str(value), quote=True)


def add_pin_layer(m, rows, group_name, color, tooltip_field_label, value_column, show=True):
    """One toggleable, clustered, coloured pin layer for a category bucket.
    Returns the number of points (0 = nothing added)."""
    # Station name and ring band repeat once per pin - New York has 44k pins
    # over 496 stations and 4 bands - so each is emitted ONCE in a lookup table
    # and referenced by integer index. Nothing is lost: the callback resolves
    # them before display. Worth ~1.2 MB on New York's map. The business name
    # is deliberately NOT indexed: it is nearly unique per pin (38k distinct of
    # 44k), so a lookup table would only add a second copy.
    #
    # row[3] stays the raw category STRING, not an index:
    # scripts/check_personal_exposure.py parses these arrays out of the
    # rendered HTML and reads row[2] and row[3] directly.
    stations, bands, data = {}, {}, []
    for row in rows.itertuples():
        station = _esc(row.nearest_station)
        band = _esc(row.ring_band)
        data.append([
            round(row.latitude, COORD_DP), round(row.longitude, COORD_DP),
            _esc(row.business_name), _esc(getattr(row, value_column)),
            stations.setdefault(station, len(stations)),
            bands.setdefault(band, len(bands)),
        ])
    if not data:
        return 0
    # An IIFE returning the function, so the two tables are built once when
    # `var callback = ...` is assigned - NOT once per pin. FastMarkerCluster
    # injects this as a statement and then calls callback(row) in its loop.
    callback = f"""
        (function () {{
            var STATIONS = {json.dumps(list(stations))};
            var BANDS = {json.dumps(list(bands))};
            return function (row) {{
                var marker = L.circleMarker(new L.LatLng(row[0], row[1]), {{
                    radius: 5, color: '{color}', fillColor: '{color}',
                    fillOpacity: 0.85, weight: 1
                }});
                var html = '<b>' + row[2] + '</b><br>' +
                    '{tooltip_field_label}: ' + row[3] + '<br>' +
                    'Nearest station: ' + STATIONS[row[4]] + '<br>' +
                    BANDS[row[5]];
                marker.bindTooltip(html, {{sticky: true}});
                return marker;
            }};
        }})()
    """
    # Leaflet.markercluster's default cluster icon is a fixed 40x40px no
    # matter the count, so a small cluster's oversized hit area blocks
    # hover on the lone dot beside it. Scale icon size with child count.
    icon_create_function = f"""
        function (cluster) {{
            var count = cluster.getChildCount();
            var size = count <= 3 ? 18 : count <= 10 ? 26 : count <= 50 ? 34 : 42;
            var fontSize = Math.max(9, Math.round(size * 0.42));
            return new L.DivIcon({{
                html: '<div style="width:100%; height:100%; border-radius:50%; ' +
                    'background:{color}; opacity:0.85; ' +
                    'border:1px solid rgba(0,0,0,0.4); display:flex; ' +
                    'align-items:center; justify-content:center; color:#fff; ' +
                    'font-size:' + fontSize + 'px; font-weight:600;">' +
                    count + '</div>',
                className: 'business-cluster-icon',
                iconSize: new L.Point(size, size)
            }});
        }}
    """
    # FastMarkerCluster's own `show` parameter is NOT reliable for hiding
    # it at load. Wrap it in a FeatureGroup, which does respect show=.
    # Do not "simplify" this back to FastMarkerCluster(show=...).
    fg = folium.FeatureGroup(name=f"<b>Businesses: {group_name} ({len(data):,})</b>", show=show)
    FastMarkerCluster(data, callback=callback, icon_create_function=icon_create_function).add_to(fg)
    fg.add_to(m)
    return len(data)


def build_legend(bucket_colors, legend_label, lines):
    """Fixed-position legend generated from the buckets actually present
    and the taxonomy's own legend text - nothing taxonomy-specific here.

    bucket_colors: [(bucket name, color)]; legend_label: bucket -> text;
    lines: {key: (coords, color, label, end)}.
    """
    return LEGEND_HTML.format(
        category_rows="".join(
            LEGEND_ROW.format(color=color, label=html.escape(legend_label(name)))
            for name, color in bucket_colors
        ),
        line_rows="".join(
            LEGEND_LINE_ROW.format(color=color, label=html.escape(label))
            for _coords, color, label, _end in lines.values()
        ),
    ) + LEGEND_AUTOFIT_SCRIPT.replace("__MAP_W__", str(_MAP_W))


def _label_anchor_coords(coords, label_focus):
    """The part of a line to anchor its label on: the stretch inside
    `label_focus` (a shapely geometry in lon/lat, normally the city's
    boundary), if at least two points fall inside it, else the whole line.
    Lines that run far beyond the city (a regional light-rail line) would
    otherwise get their label at the midpoint of the entire route, off-screen
    in the city's default view."""
    if label_focus is None:
        return coords
    from shapely.geometry import Point
    from shapely.prepared import prep

    focus = prep(label_focus)
    inside = [c for c in coords if focus.contains(Point(c[1], c[0]))]
    return inside if len(inside) >= 2 else coords


# Contact details that must never reach a published pin. A registry's
# business-name field sometimes holds an email address or phone number instead
# of a trade name, which is a different exposure from a person's NAME and a
# worse one: a name at a commercial address identifies a business, an email
# address is a direct line to a person.
#
# Found 2026-09-21 by grepping the repo for an unrelated reason, not by any
# check this project ran - scripts/check_personal_exposure.py tested for
# person-like names and an email matches none of its patterns. One pin in
# 91,000 (a New York "Tobacco Retail Dealer" registered under a Gmail address).
#
# Enforced HERE, in the shared renderer, rather than in the city's step 2 that
# happened to have the problem: this is the one place every city's pins pass
# through, so a city added later cannot reintroduce it by forgetting. Decided
# 2026-09-21; see DECISIONS.md.
_CONTACT_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Conservative: a 10-digit run with separators, so a licence number or a long
# street number cannot match.
_CONTACT_PHONE = re.compile(r"(?:\+?1[ .\-]?)?\(?\d{3}\)?[ .\-]\d{3}[ .\-]\d{4}")


def _has_contact_details(name) -> bool:
    if pd.isna(name):
        return False
    text = str(name)
    return bool(_CONTACT_EMAIL.search(text)
                or _CONTACT_PHONE.search(_CONTACT_EMAIL.sub("", text)))


def drop_contact_details(businesses):
    """Remove rows whose displayed name carries an email address or phone
    number. Such a row has no usable public trade name, so it is dropped the
    way a blank one would be - masking would still leak a partial."""
    if "business_name" not in businesses.columns:
        return businesses
    flagged = businesses["business_name"].map(_has_contact_details)
    if int(flagged.sum()):
        print(f"Contact-detail scrub: dropped {int(flagged.sum()):,} row(s) "
              f"whose business name holds an email address or phone number "
              f"(no usable public trade name).")
    return businesses[~flagged]


def render_heatmap(*, output_path, map_title, city_name, system_name,
                   stations, businesses, taxonomy_system, lines,
                   crs_geographic, crs_projected, ring_edges_meters, ring_labels,
                   center=None, zoom=None, label_focus=None, rings_shown=True):
    """Render one city's heatmap to a standalone HTML file.

    stations: DataFrame(station, latitude, longitude). businesses: the
    city's businesses_clean.csv as a DataFrame (needs latitude, longitude,
    business_name and the taxonomy's VALUE_COLUMN). lines: output of
    load_line_shapes. system_name prefixes each line's layer name (e.g.
    "Trolley", "Muni Metro"). label_focus: optional shapely geometry (lon/lat)
    - line labels go at the tail ends of the part of each line inside it (see
    _label_anchor_coords); omit only for cities whose whole lines stay in view.
    center/zoom: leave None (the default) to fit the view to the stations and
    every line label together, so all labels are visible on first load; pass
    either to override.

    rings_shown: whether the concentric ring layers start switched on. True for
    every city whose stations are far enough apart for the rings to read
    individually. New York passes False: with 496 stations at a median 482 m
    apart, the rings merge into one indistinct wash over Manhattan and downtown
    Brooklyn, though they still read cleanly around the outer-borough and
    Staten Island stations - so they stay in the layer control to be switched
    on, rather than being dropped. Decided 2026-09-21; see DECISIONS.md.
    """
    taxonomy = load_taxonomy_module(taxonomy_system)
    bucket_colors = dict(CATEGORY_BUCKETS)

    businesses = businesses.dropna(subset=["latitude", "longitude"]).copy()
    businesses = drop_contact_details(businesses)
    businesses["nearest_station"], businesses["ring_band"] = nearest_station_and_ring(
        businesses, stations, crs_geographic, crs_projected, ring_edges_meters, ring_labels
    )
    in_rings = businesses[~businesses["ring_band"].str.startswith("Beyond")].copy()
    print(f"{len(businesses) - len(in_rings):,} of {len(businesses):,} businesses fall "
          f"outside every station's ring ({len(in_rings):,} remain within a ring).")

    # Where each line's label goes: the tail end of its in-city stretch,
    # chosen against the other lines' stretches. Worked out first so the
    # default view can be fitted to include every label.
    # segments[0] is the line's primary alignment (load_line_shapes sorts them
    # longest first); a multi-segment line is labelled against that.
    anchors = {key: _label_anchor_coords(segments[0], label_focus) for key, (segments, *_rest) in lines.items()}
    tips = {
        key: _tail_end(anchors[key], [a for k, a in anchors.items() if k != key], forced=end)
        for key, (_coords, _color, _label, end) in lines.items()
    }
    label_text = {key: label for key, (_c, _col, label, _e) in lines.items()}
    candidates = {key: _label_candidates(anchors[key], tips[key]) for key in tips}
    center, zoom, tips = _choose_view(
        [(r.latitude, r.longitude) for r in stations.itertuples()],
        candidates, label_text, len(lines), center=center, zoom=zoom,
    )

    # Fixed pixel width/height, NOT percentage sizing: Leaflet.heat has a
    # known open bug (github.com/Leaflet/Leaflet.heat/issues/95) where an
    # uncaught IndexSizeError fires on init if the container's size isn't
    # resolved yet, which silently stops every later .addTo(map) call in the
    # generated script - rings, markers and the layer control never render,
    # with no visible console error. The app pages embed the map at this
    # same fixed size; change them together.
    m = folium.Map(location=center, zoom_start=zoom, tiles=None, width=1000, height=650, zoomSnap=0.25)
    folium.TileLayer(tiles="OpenStreetMap", name=map_title).add_to(m)

    # Two heat layers, same tuning, different universe: within-rings is the
    # default; the whole-city one is an opt-in for context.
    HeatMap(in_rings[["latitude", "longitude"]].round(COORD_DP).values.tolist(),
            radius=HEAT_RADIUS, blur=HEAT_BLUR, min_opacity=HEAT_MIN_OPACITY,
            gradient=HEAT_GRADIENT, name="Commercial Density (Within Station Proximity)",
            show=True).add_to(m)
    HeatMap(businesses[["latitude", "longitude"]].round(COORD_DP).values.tolist(),
            radius=HEAT_RADIUS, blur=HEAT_BLUR, min_opacity=HEAT_MIN_OPACITY,
            gradient=HEAT_GRADIENT, name=f"Commercial Density (All {city_name} Businesses)",
            show=False).add_to(m)

    for i, label in enumerate(ring_labels):
        layer = folium.FeatureGroup(name=f"Concentric Ring {i + 1}: {label}",
                                    show=rings_shown)
        for _, station in stations.iterrows():
            folium.Circle(
                location=[round(station["latitude"], COORD_DP),
                          round(station["longitude"], COORD_DP)],
                radius=ring_edges_meters[i + 1],
                # Same LIGHT value the dark-mode selector matches on.
                color=LIGHT["ring"], weight=1, fill=False, opacity=0.5,
            ).add_to(layer)
        layer.add_to(m)

    station_layer = folium.FeatureGroup(name="Stations", control=False)
    for _, station in stations.iterrows():
        folium.CircleMarker(
            location=[round(station["latitude"], COORD_DP),
                      round(station["longitude"], COORD_DP)],
            radius=5, color=LIGHT["station"], fill=True, fill_opacity=0.9,
            tooltip=folium.Tooltip(f"<b>{html.escape(station['station'])}</b>", sticky=True),
        ).add_to(station_layer)
    station_layer.add_to(m)

    # Transit lines: always-on context, permanent label + legend entry each
    # (label tips were worked out above, before the map was created).
    for key, (segments, color, label, _end) in lines.items():
        rail_layer = folium.FeatureGroup(name=f"{system_name}: {label}", show=True, control=False)
        # One polyline per alignment; a branching trunk keeps one label and one
        # legend entry (see load_line_shapes).
        for segment in segments:
            folium.PolyLine(segment, color=color, weight=4, opacity=0.85).add_to(rail_layer)
        add_line_label(rail_layer, tips[key], label, color)
        rail_layer.add_to(m)

    # Category grouping via the city's own taxonomy, never a hardcoded one.
    # A multi-field taxonomy (Chicago) lists its extra columns in EXTRA_COLUMNS.
    class_cols = [taxonomy.VALUE_COLUMN, *getattr(taxonomy, "EXTRA_COLUMNS", ())]
    in_rings["_bucket"] = [
        taxonomy.classify(dict(zip(class_cols, values)))
        for values in zip(*(in_rings[c] for c in class_cols))
    ]
    unmatched = in_rings["_bucket"].isna().sum()
    if unmatched:
        print(f"WARNING: {unmatched} businesses matched no category bucket.")

    present = []
    for name, color in CATEGORY_BUCKETS:
        rows = in_rings[in_rings["_bucket"] == name]
        if add_pin_layer(m, rows, name, color, taxonomy.FIELD_LABEL, taxonomy.VALUE_COLUMN):
            present.append((name, color))

    m.get_root().html.add_child(folium.Element(
        build_legend(present, taxonomy.legend_label, lines)
    ))

    # Collapsed by default: many toggleable layers would otherwise cover a
    # large share of the map. Top-left, not Leaflet's top-right default -
    # the map has a fixed 1000px width and a top-right control can be
    # pushed off the visible edge when Streamlit's content area is narrower.
    folium.LayerControl(collapsed=True, position="topleft").add_to(m)
    m.get_root().html.add_child(folium.Element("""
        <style>
            .leaflet-control-layers-expanded {
                max-height: 480px;
                overflow-y: auto;
            }
        </style>
    """))
    m.get_root().html.add_child(folium.Element(THEME_TOGGLE_HTML))

    # Fit the map to a frame narrower than its own fixed layout width (phones,
    # and the app's column on a small laptop). See PHONE_FIT_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        PHONE_FIT_SCRIPT
        .replace("__MAP_W__", str(_MAP_W))
        .replace("__MAP_H__", str(_MAP_H))
        .replace("__MAP_NAME__", m.get_name())
        # Bounds include the LINE LABEL anchors, not just the stations. A label
        # sits beyond its line's tip, so fitting to stations alone crops labels
        # off a narrow frame - deploy-verify measured only 2 of San Francisco's
        # 6 and 4 of Los Angeles' 6 visible at 375px when this fitted stations
        # only. `_choose_view` already fits the desktop view to stations and
        # labels together; this matches it.
        .replace("__BOUNDS__", json.dumps([
            [min([float(stations["latitude"].min())] + [float(t[0]) for t in tips.values()]),
             min([float(stations["longitude"].min())] + [float(t[1]) for t in tips.values()])],
            [max([float(stations["latitude"].max())] + [float(t[0]) for t in tips.values()]),
             max([float(stations["longitude"].max())] + [float(t[1]) for t in tips.values()])],
        ]))
    ))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    print(f"Wrote {output_path}")
    print(f"{len(in_rings):,} points plotted (within-ring default) / "
          f"{len(businesses):,} available (all-{city_name} toggle), across {len(stations)} stations")
