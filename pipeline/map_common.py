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

from pipeline.linecolour import check_line_colours, label_colours
from pipeline.taxonomies import CATEGORY_BUCKETS, load_taxonomy_module
from pipeline.theme import AMBIENT_THEME_JS, DARK, FONT_STACK, LIGHT, css_vars, rgba

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
# A SINGLE-HUE burnt-orange ramp, adopted 2026-09-21 from the sister project
# that originated this map's schematic. It replaces a ColorBrewer Reds ramp,
# and the change is inseparable from Food service moving to magenta (see
# pipeline/taxonomies/CATEGORY_BUCKETS): the old red ramp sat 3.1 degrees of
# hue from the old food orange, so pins and wash were nearly the same colour.
#
# Three things the hex list alone does not say, carried over from the source:
#
#   1. SINGLE-HUE IS THE POINT. Leaflet.heat's default runs blue -> cyan ->
#      lime -> yellow -> red, and at realistic densities most of a map sits in
#      blue/cyan, which reads as COLD for a density layer. One hue getting
#      stronger reads as one quantity increasing.
#   2. THE FLOOR IS DELIBERATELY MORE SATURATED THAN IT LOOKS LIKE IT SHOULD
#      BE. Leaflet.heat multiplies opacity by density, so the palest stop is
#      faded twice; the source's first attempt used #FDD0A2 and it vanished on
#      light OSM tiles. #FBB878 is the corrected floor. **Its own note says a
#      dark basemap wants the OPPOSITE correction, and this site defaults to
#      dark** - measured here, #FBB878 scores Delta-E 44.8 against the light
#      land fill and 85.3 against the dark one, so the floor is ~1.9x more
#      prominent in the mode readers see first. Left as the source has it
#      rather than re-tuned blind; revisit by eye, not by arithmetic.
#   3. RADIUS AND BLUR ARE PIXEL-SPACE AND ZOOM-SPECIFIC, with no statistical
#      meaning. HEAT_RADIUS/HEAT_BLUR above already match the source exactly
#      (8/10, against Leaflet's 12/18 which collapsed into one wash), so
#      nothing there had to change - but they are tuned for a city-wide view,
#      and a city opening at a different zoom should re-tune by eye.
HEAT_GRADIENT = {0.3: "#FBB878", 0.5: "#F97316", 0.7: "#DE6412",
                 0.85: "#C0570F", 1.0: "#8F3A05"}

# The canvas every fixed-position overlay and the whole label layout are
# computed against - the size passed to folium.Map in render_heatmap and the
# size app/pages/*.py embeds with st.iframe. Defined here rather than beside
# the label-layout constants, where it used to live: three comment blocks
# below this line name it before it was defined, and _LEGEND_BOTTOM_CSS needs
# its value at import time.
_MAP_W, _MAP_H = 1000, 650

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
        font: 600 13px @@FONT_STACK@@; padding: 6px 12px; cursor: pointer;
        background: @@LIGHT_SURFACE@@; color: @@LIGHT_TEXT@@;
        border: 1px solid @@LIGHT_BORDER@@;
        border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }
    .map-btn[hidden] { display: none; }
    /* THE TOOLTIP IS WHERE BUSINESS NAMES APPEAR, so it needs the font stack
       more than anything else on the map does. Leaflet's own CSS sets
       `"Helvetica Neue", Arial, Helvetica, sans-serif` on .leaflet-tooltip,
       which is Latin-only - so without this rule a Japanese, Korean or Greek
       shop name would render in whatever the browser substituted, as tofu
       boxes or at metrics that outgrow the tooltip's own box. Added
       2026-09-21 alongside pipeline/theme.FONT_STACK, whose own note explains
       why the fallback ORDER matters (browsers fall through per glyph, not
       per string). */
    .leaflet-tooltip { font-family: @@FONT_STACK@@; }
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
    /* NO FILTER on a line label: a brightness() filter here once lifted the
       halo with the text, so the dark page colour rendered #132039 and every
       contrast figure measured a halo nobody saw. Each label carries its own
       dark-theme colour in --dm-label instead (pipeline/linecolour.py,
       "LINE LABELS"), read at 4.5:1 against exactly this halo. */
    .dark-base .leaflet-marker-icon div[style*="text-shadow"] {
        text-shadow: -1px -1px 0 var(--dm-page), 1px -1px 0 var(--dm-page),
                     -1px 1px 0 var(--dm-page), 1px 1px 0 var(--dm-page),
                     0 0 6px var(--dm-page) !important; }
    .dark-base .hm-line-label { color: var(--dm-label) !important; }
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
        aria-label="Back to the Global View map">&larr; Global View</button>
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

    // "Global View" button: only when this map is embedded in the app (it has a
    // parent page to go back to); opened on its own it stays hidden. It clicks
    // the app's own link to the Overview, so Streamlit navigates in place, and
    // saves the current theme first so the macro map opens in the same mode.
    var back = document.getElementById('back-to-map');
    function trimSlash(p) { while (p.length > 1 && p.charAt(p.length - 1) === '/') p = p.slice(0, -1); return p; }
    function overviewLink() {
        var doc = window.parent.document, links = doc.querySelectorAll('a[href]');
        for (var i = 0; i < links.length; i++) {          // the page's own link to the Overview:
            var t = links[i].textContent;                 // hidden "All cities", switcher "Global View"
            if (t.indexOf('All cities') !== -1 || t.indexOf('Global View') !== -1) return links[i];
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
    // Identify "which page is this" by PAGE SLUG, not by display label.
    //
    // This used to derive a city name from the URL ("/Miami_Heatmap" -> "Miami")
    // and compare it to the link's text. That breaks as soon as a city's
    // display name is not its filename: Miami's label is "Miami (Regional)",
    // so the comparison never matched and Miami's own map listed Miami in its
    // "Cities" dropdown. Comparing slug to slug is immune to the label, which
    // matters because a regional map's name will keep diverging from its
    // filename (a Seattle build spanning twelve municipalities is the next).
    function lastSegment(path) {
        var parts = String(path || '').split('?')[0].split('#')[0]
            .split('/').filter(Boolean);
        return decodeURIComponent(parts.length ? parts[parts.length - 1] : '');
    }
    function fillMenu() {
        if (menu.options.length > 1) return;    // already built
        var here = lastSegment(window.parent.location.pathname);
        var links = cityLinks();
        for (var i = 0; i < links.length; i++) {
            var name = links[i].textContent.trim();
            if (lastSegment(links[i].getAttribute('href')) === here) continue;
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
    .replace("@@FONT_STACK@@", FONT_STACK)
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
# KEPT OUT OF LEGEND_HTML ON PURPOSE: that string goes through .format(), so
# every CSS brace in it would have to be doubled, and a single missed one is a
# KeyError at render time rather than a visible mistake. Concatenated instead.
#
# How far below the map's top edge the open legend must stop: the button row
# (#map-actions, top 10px, ~30 px tall) plus a gap. _layout_labels caps its
# legend obstacle with the same number, so the model and the render agree.
_LEGEND_TOP_CLEAR = 56
_LEGEND_CSS = """
<style>
/* THE HEADER IS THE CONTROL, AND IT HAS TO SAY SO. A native <summary> does
   render a disclosure triangle - `list-style-type` computes to
   `disclosure-open` here - but it is a ~6 px glyph in the same colour and
   weight as the text beside it, and on a dense map it reads as punctuation
   rather than as something to click. Replaced with an explicit chevron plus a
   VERB, because the chevron alone is ambiguous: this panel is anchored
   bottom-right, so its box grows upward while its content flows downward, and
   no arrow direction is honestly self-explanatory. "Hide"/"Show" is.

   Laid out as a flex row with space-between, which keeps the marker INSIDE the
   legend's existing width rather than extending it. That matters: the label
   layout in _layout_labels models the open legend as a hardcoded 274 px
   obstacle, and a wider panel would start covering line labels it currently
   clears. Verified after the change that the open width is unchanged.

   No script: the collapse is still the browser's own <details> behaviour, so
   this is presentation only and scripts/check_map_labels.js keeps working. The
   colour is `currentColor`, so it follows .dark-base .map-legend's own
   `color` and needs no dark-mode rule of its own. */
.map-legend > summary { list-style: none; display: flex;
    align-items: baseline; justify-content: space-between; gap: 12px; }
.map-legend > summary::-webkit-details-marker { display: none; }
.map-legend > summary::after {
    content: "\\25BE\\00A0Hide"; font: 600 11px """ + FONT_STACK + """;
    opacity: 0.7; white-space: nowrap; }
.map-legend:not([open]) > summary::after { content: "\\25B8\\00A0Show"; }
.map-legend > summary:hover::after { opacity: 1; text-decoration: underline; }
.map-legend > summary:focus-visible { outline: 2px solid currentColor;
    outline-offset: 2px; }
/* THE OPEN LEGEND IS CAPPED BELOW THE BUTTON ROW, AND SCROLLS. Amsterdam
   (2026-09-24) was the first map with 21 lines: open, its legend was 634 px
   tall at the 650 px embed, so its top sat at y = -8 and its header and Hide
   control were under the "Global View" and theme buttons (#map-actions, fixed
   at top 10px, ~30 px tall) - found by deploy-verify. Every earlier legend was
   shorter than the cap (Paris's the tallest, its top at y 84), so none of
   them changes. min(100vh, MAP_H) is the visible map height whichever way
   _LEGEND_BOTTOM_CSS resolves; border-box so the cap is the whole panel. The
   header sticks, so Hide stays in reach while the rows scroll. Its background
   is set, NOT `inherit`: a <summary> is slotted into the <details> shadow
   root, so it inherits from a transparent slot - measured, the rows showed
   through the header in dark mode. */
.map-legend { box-sizing: border-box; overflow-y: auto;
    overscroll-behavior: contain;
    max-height: calc(min(100vh, """ + str(_MAP_H) + """px) - """ + str(24 + _LEGEND_TOP_CLEAR) + """px); }
.map-legend > summary { position: sticky; top: -8px; z-index: 1;
    padding-top: 8px; margin-top: -8px; background: white; }
.dark-base .map-legend > summary { background: var(--dm-surface); }
</style>
"""

# WHY THE LEGEND'S BOTTOM IS CLAMPED AND NOT SIMPLY `24px`.
#
# The legend is `position: fixed`, so its bottom is measured from the
# VIEWPORT's bottom edge. Leaflet's basemap attribution is `position:
# absolute` inside the map container, so its bottom is measured from the MAP's
# bottom edge - and the map is a fixed _MAP_H tall (see the folium.Map call in
# render_heatmap). Those two edges are the same line at exactly one viewport
# height, _MAP_H. Any taller and the map's bottom edge rises while the legend
# stays pinned to the viewport, and the legend swallows the attribution.
#
# Measured 2026-09-23 on Toulouse, hit-testing five points along the
# attribution strip with document.elementFromPoint:
#
#     1000x650  what app/pages/*.py embeds with st.iframe      0/5 covered
#     1024x768  outputs/<city>/heatmap.html opened directly    5/5 covered
#     375x812   after a reader re-opens the collapsed legend   5/5 covered
#
# EVERY city, not one - the geometry is entirely in this file. The embedded
# size passed on a 10 px margin, and nothing pinned it there: that is the real
# defect. CLAUDE.md makes the visible basemap credit a hard invariant (ODbL
# 1.0 requires it not to sit behind UI), so a change to the iframe height, a
# responsive embed, or a reader opening the file directly each breached it
# silently.
#
# `max()` clamps the legend's bottom to 24 px above the MAP's bottom edge
# rather than the viewport's. At the embedded size that is the same position
# it already had, so the embed is pixel-unchanged; at every taller viewport it
# clears the 14 px attribution strip by the same 10 px. Shorter than _MAP_H
# the map overflows and the page scrolls, and there `max()` picks 24px -
# today's behaviour, with the attribution clear once scrolled to.
#
# It also repairs a model that was quietly wrong: _layout_labels treats the
# open legend as an obstacle whose bottom sits at _MAP_H - 24 in map
# coordinates. That held only at a 650 px viewport. It now holds at every
# height at or above one.
#
# DO NOT replace this with a plain offset. The offset that clears the
# attribution is a function of viewport height, so any single number is right
# at exactly one height - which is the bug, not the fix. Moving the
# attribution to the bottom-LEFT does not work either: measured at 375 px, the
# open legend occupies x 133-351 and a bottom-left attribution would occupy
# x 0-197, so they still overlap.
#
# scripts/check_map_attribution.js re-measures this in a real browser at
# several viewport heights; scripts/check_provenance.py (check K) refuses a
# committed map whose legend is not clamped, and is the half that still runs
# when a pipeline-only change skips deploy-verify.
_LEGEND_BOTTOM_CSS = f"max(24px, calc(100vh - {_MAP_H - 24}px))"

# FONT_STACK quotes its family names with DOUBLE quotes ("Segoe UI"), and the
# legend's style sits in a double-quoted attribute - so until 2026-09-24 the
# first family name closed the attribute, and every legend lost its 13px size,
# its shadow and every fallback font, rendering in Leaflet's Latin-only default
# (Brazil's deploy check found it; Chicago's map had the same markup). CSS
# accepts either quote, so the inline copy uses single quotes.
_LEGEND_FONT_STACK = FONT_STACK.replace('"', "'")

LEGEND_HTML = """
<details open class="map-legend" style="
    position: fixed; bottom: """ + _LEGEND_BOTTOM_CSS + """; right: 24px; z-index: 9999;
    background: white; padding: 8px 14px; border: 1px solid #999;
    border-radius: 4px; font-family: """ + _LEGEND_FONT_STACK + """; font-size: 13px;
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
    // The view Folium baked in, captured before any fit runs. apply() restores
    // it when the map returns to full width - see the else branch there.
    var HOME = null;
    // The width the CURRENT view was fitted for, which is not the same thing as
    // the container's width. See apply(): a view fitted while the container was
    // still laying out stays wrong until something notices the mismatch, and
    // comparing widths alone cannot notice it.
    var FITTED_AT = null;

    // THE GUARD - owner's decision 2026-09-23, after the same race surfaced a
    // THIRD way. Edmonton (2026-09-21) and Paris (2026-09-23 morning) were each
    // fixed at the point where they broke; that afternoon Lille's embedded map
    // loaded at zoom 8.25 against a baked 11.75 - Edmonton's exact number - and
    // a reload fixed it. Four further loads would not reproduce it. A race that
    // cannot be reproduced on demand cannot be fixed one trigger at a time, so
    // this stops chasing triggers and checks the OUTCOME instead: until the
    // reader touches the map, the view is compared with what it should be for
    // the frame's current width, and re-fitted when it is not.
    //
    // "What it should be" is exactly what apply() produces - HOME at full
    // width, fitBounds(BOUNDS, padding 26/18 each side) when narrow - computed
    // with getBoundsZoom rather than by calling fitBounds, so a correct view is
    // never touched and the common case stays pixel-identical.
    //
    // TOUCHED ends it for good. Any pointer, wheel, touch or key event inside
    // the map means the reader is steering, and a guard that restored the
    // view under them would be a new bug. Captured on the container, so the
    // zoom buttons, the pins and the in-map controls all count.
    //
    // __HEATMAP_VIEW is read by scripts/check_map_view.js. It exposes the
    // INPUTS (home, bounds, padding) as well as the guard's own bookkeeping, so
    // the check can recompute the expected zoom independently instead of
    // trusting the thing it is checking.
    var TOUCHED = false;
    var PAD = [26, 18];
    var VIEW = window.__HEATMAP_VIEW = {
        bounds: BOUNDS, mapW: MAP_W, padding: PAD, home: null,
        expected: null, actual: null, touched: false, corrections: 0};

    function wantedZoom(m, target) {
        if (target < MAP_W && BOUNDS) {
            return m.getBoundsZoom(L.latLngBounds(BOUNDS), false,
                                   L.point(2 * PAD[0], 2 * PAD[1]));
        }
        return HOME ? HOME.zoom : null;
    }

    function guard(m) {
        if (TOUCHED || !HOME) return;
        var w = document.documentElement.clientWidth || window.innerWidth;
        var target = Math.min(w, MAP_W);
        if (!target) return;
        var want = wantedZoom(m, target);
        VIEW.expected = want;
        VIEW.actual = m.getZoom();
        if (want === null || Math.abs(m.getZoom() - want) < 0.01) return;
        VIEW.corrections += 1;
        FITTED_AT = null;   // make apply() re-fit instead of trusting the width
        apply(m);
        VIEW.actual = m.getZoom();
    }

    function armGuard(m) {
        var el = m.getContainer();
        ["pointerdown", "mousedown", "touchstart", "wheel", "keydown"].forEach(
            function (ev) {
                el.addEventListener(ev, function () {
                    TOUCHED = true;
                    VIEW.touched = true;
                }, {capture: true, passive: true});
            });
        // Bounded polling for the load itself - every earlier variant of the
        // race resolved or struck inside the first seconds...
        var ticks = 0;
        var iv = setInterval(function () {
            guard(m);
            if (TOUCHED || ++ticks >= 40) clearInterval(iv);
        }, 500);
        // ...and event triggers for everything slower: a page opened in a
        // background tab (timers throttled, layout late), an embed below the
        // fold, a bfcache restore.
        document.addEventListener("visibilitychange", function () {
            if (!document.hidden) guard(m);
        });
        window.addEventListener("pageshow", function () { guard(m); });
        if (window.IntersectionObserver) {
            new IntersectionObserver(function (entries) {
                if (entries.some(function (e) { return e.isIntersecting; })) guard(m);
            }).observe(el);
        }
    }

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
        // A ZERO TARGET IS ALWAYS A BAD MEASUREMENT, NEVER A REAL WIDTH.
        //
        // Added 2026-09-23 after Paris rendered BLANK on first load, with
        // `width: 0px` written onto the container and Leaflet.heat throwing
        // "IndexSizeError: getImageData ... source width is 0". A pass that
        // runs before the document has laid out reads clientWidth 0, and the
        // old code wrote that straight through.
        //
        // It is the same RACE the else branch below documents for Edmonton -
        // intermittent, not specific to a city, and the same page reloaded
        // rendered correctly - but this manifestation is worse: a narrow fit
        // is a bad view, a zero width is no map at all plus a console error.
        // Paris is the city that exposed it because it is the heaviest map
        // here (84,125 points), which widens the window before layout settles.
        //
        // Returning leaves the container alone for the later passes - immediate,
        // rAF, 120 ms, 400 ms, 1200 ms and resize - one of which measures a
        // laid-out document. Correct renders are untouched, because `target` is
        // only 0 when the measurement is meaningless.
        if (!target) return;
        // THE EARLY RETURN USED TO BE A CORRECTNESS BUG, not just an
        // optimisation. It read "the width already matches, so there is
        // nothing to do" - but the VIEW can be wrong while the WIDTH is right.
        //
        // Observed on the deployed site 2026-09-23, on Paris: the embedded map
        // sat at zoom 9 against its baked 12.5, showing the whole Ile-de-France
        // with every line label flung to the frame edges. Sequence: an early
        // pass measured the container mid-layout at some narrow width and
        // fitted BOUNDS for THAT width; a later pass found the container now at
        // its real 854 px, matched `target`, and returned - so the zoom from
        // the narrow fit was never undone. Intermittent, and it survived the
        // 2026-09-21 fix because that one only added an `else` branch AFTER
        // this return.
        //
        // So the state that matters is "what width was the current view fitted
        // for", not "what width is the container". FITTED_AT records it, and a
        // mismatch re-fits even when the width needs no change.
        var atWidth = Math.abs(el.getBoundingClientRect().width - target) < 1;
        if (atWidth && FITTED_AT === target) return;
        if (!atWidth) {
            el.style.width = target + "px";
            document.body.style.width = target + "px";
            m.invalidateSize();
        }
        FITTED_AT = target;
        if (target < MAP_W && BOUNDS) {
            // Generous padding because BOUNDS holds label ANCHORS, and a label's
            // text box extends past its anchor by up to ~70px.
            // PAD, not a literal: the guard computes the zoom this call lands
            // on, and a padding that drifted between the two would make it
            // "correct" a right view forever.
            m.fitBounds(L.latLngBounds(BOUNDS), {padding: PAD, animate: false});
        } else if (HOME) {
            // BACK AT FULL WIDTH, AND THIS BRANCH IS A BUG FIX, NOT SYMMETRY.
            //
            // Until 2026-09-21 there was no else. A pass that ran while the
            // iframe was still laying out measured a narrow clientWidth,
            // fitted BOUNDS at that width - which is a much lower zoom - and
            // then the later full-width pass restored the WIDTH and left the
            // ZOOM alone, because re-fitting was conditional on being narrow.
            // Nothing afterwards ever corrected it, so the map sat at the
            // narrow-width zoom at full width: Edmonton was caught embedded at
            // zoom 8.25 against its baked 11.5, showing the whole region with
            // every pin in one cluster. It is a RACE, so it is intermittent and
            // not specific to a city - the same page reloaded rendered
            // correctly, and Calgary's rendered correctly alongside the broken
            // Edmonton.
            //
            // Restoring HOME rather than re-fitting BOUNDS is deliberate:
            // Folium's baked view is what every full-width map has always
            // shown, and a runtime fitBounds lands a quarter-step tighter
            // (Edmonton 11.75 against 11.5). So this repairs the broken case
            // and leaves the normal one pixel-identical.
            m.setView(HOME.center, HOME.zoom, {animate: false});
        }
    }

    function start() {
        var m = ready();
        if (!m) {
            if (tries++ < 60) return setTimeout(start, 100);
            return;
        }
        // Before the first apply(), so this is Folium's own fitted view and not
        // something a narrow-width pass has already moved.
        if (!HOME) {
            HOME = {center: m.getCenter(), zoom: m.getZoom()};
            VIEW.home = {center: [HOME.center.lat, HOME.center.lng], zoom: HOME.zoom};
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
            t = setTimeout(function () { apply(m); guard(m); }, 150);
        });
        armGuard(m);
    }
    start();
})();
</script>
"""
# KEEPS EVERY LINE LABEL INSIDE THE FRAME, by sliding it - never by zooming.
#
# A label's text reaches up to ~220px past the anchor at its line's tip, and
# PHONE_FIT_SCRIPT fits the ANCHORS (with 26px of padding), so on a phone a
# label at the tail of an outlying line ran off the frame: 22 of 25 cities,
# 35 of 155 labels at 375px and 33 at 343px, measured 2026-09-23 by
# scripts/check_map_labels.js - Rennes' "Métro b" cut to "Métr" in the app.
#
# Zooming out until every label fitted was built and measured first, and
# rejected: it removed every clip but took New York from 9.5 to 8.75 at 343px,
# shrinking the city to a knot of stacked labels, and raised overlapping label
# pairs across the 25 cities from 28 to 49. Sliding keeps the view exactly
# as it was - zoom, centre, PHONE_FIT_SCRIPT and its guard are untouched - and
# moves only a label that would otherwise be cut, only as far as it must, and
# only while its line's tip is on screen: once a reader pans the tip away, the
# label leaves with it, as it always did.
#
# Re-run on every moveend/zoomend/resize, from the label's baked transform, so
# a slide never accumulates. The measurement is the label box relative to its
# own 0x0 icon plus latLngToContainerPoint, which stays right even when a
# hidden page has not redrawn its markers yet.
#
# AND IT RE-PLACES A LABEL THAT COLLIDES (2026-09-24). _label_candidates and
# _tail_end place every label ONCE, in Python, against the full-width view;
# when the phone fit zooms out, line tips crowd together while labels keep
# their size, and nothing moved them. Amsterdam shipped with 11 overlapping
# pairs at 375px and 17 at 343px; seven other cities had 28 between them. So
# after the slide, any label overlapping another label, the fixed buttons,
# Leaflet's top-left controls or the COLLAPSED legend tries spots around its
# own line's tip - mirrored, above, below, right, left, a step further out -
# and takes the first clear one, or the least-overlapping. A label that
# collides with nothing never moves, so every desktop view, already laid out
# clean in Python, is unchanged. The open legend is not an obstacle: opening
# it is the reader choosing to cover part of the map.
LABEL_CLAMP_SCRIPT = """
<script>
(function () {
    var NAME = "__MAP_NAME__";
    var MARGIN = 6;     // px kept between a label's text and the frame edge
    var GAP = 4;        // px between a re-placed label and its line's tip
    var CLEAR = 2;      // px a label keeps from a button, control or legend
    var PASSES = 4;
    var tries = 0;

    function box(x0, y0, x1, y1) { return {x0: x0, y0: y0, x1: x1, y1: y1}; }
    function shift(b, sx, sy) { return box(b.x0 + sx, b.y0 + sy, b.x1 + sx, b.y1 + sy); }
    function area(a, b) {
        var w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
        var h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
        return w > 0 && h > 0 ? w * h : 0;
    }

    // What a label must stay clear of, in the map container's coordinates:
    // the fixed "Global View"/theme buttons, Leaflet's own top-left controls,
    // and the legend while it is COLLAPSED. An open legend is the reader's
    // choice to cover part of the map; shuffling labels out from under it
    // would only crowd them elsewhere.
    function obstacles(m) {
        var c = m.getContainer(), mr = c.getBoundingClientRect(), out = [];
        function add(el) {
            if (!el) return;
            var r = el.getBoundingClientRect();
            if (r.width && r.height) {
                out.push(box(r.left - mr.left, r.top - mr.top,
                             r.right - mr.left, r.bottom - mr.top));
            }
        }
        add(document.getElementById("map-actions"));
        var legend = document.querySelector("details.map-legend");
        if (legend && !legend.open) add(legend);
        c.querySelectorAll(".leaflet-top.leaflet-left .leaflet-control").forEach(add);
        return out;
    }

    function place(m) {
        var size = m.getSize();
        if (!size.x || !size.y) return;
        // Never slide a label ONTO the basemap credit, which must stay
        // visible (ODbL). The credit is a strip along the bottom edge, so the
        // bottom limit clears its height as well as MARGIN.
        var att = m.getContainer().querySelector(".leaflet-control-attribution");
        var bottom = size.y - MARGIN - (att ? att.getBoundingClientRect().height : 0);
        function inside(b) {
            var dx = Math.max(0, MARGIN - b.x0) - Math.max(0, b.x1 - (size.x - MARGIN));
            var dy = Math.max(0, MARGIN - b.y0) - Math.max(0, b.y1 - bottom);
            return [dx, dy];
        }

        // 1. Every label at its baked position, slid inside the frame if it
        //    would be cut - exactly as before this placer existed.
        var labels = [];
        m.eachLayer(function (layer) {
            if (!layer._icon || !layer.getLatLng) return;
            var d = layer._icon.querySelector(".hm-line-label");
            if (!d) return;
            if (d.dataset.base === undefined) d.dataset.base = d.style.transform;
            d.style.transform = d.dataset.base;
            var i = layer._icon.getBoundingClientRect();
            var r = d.getBoundingClientRect();
            if (!r.width) return;
            var p = m.latLngToContainerPoint(layer.getLatLng());
            if (p.x < 0 || p.y < 0 || p.x > size.x || p.y > size.y) return;
            var base = box(p.x + (r.left - i.left), p.y + (r.top - i.top),
                           p.x + (r.right - i.left), p.y + (r.bottom - i.top));
            var s = inside(base);
            labels.push({d: d, p: p, base: base, sx: s[0], sy: s[1],
                         b: shift(base, s[0], s[1])});
        });

        // 2. Re-place only a label that overlaps another label or an obstacle,
        //    trying spots around its own line's tip, so it still names that
        //    line. A label that collides with nothing never moves, so a map
        //    that was already clean - every desktop view - is unchanged.
        var obs = obstacles(m);
        function cost(L, b) {
            var c = 0;
            labels.forEach(function (o) {
                if (o !== L) c += area(b, box(o.b.x0 - 1, o.b.y0 - 1, o.b.x1 + 1, o.b.y1 + 1));
            });
            // Obstacles count with CLEAR px of margin: Edmonton's Valley Line
            // tip sits under the collapsed legend, and the best spot beside it
            // still overlapped the legend by one pixel - which reads as
            // touching and which the check rightly refuses.
            obs.forEach(function (o) {
                c += area(b, box(o.x0 - CLEAR, o.y0 - CLEAR, o.x1 + CLEAR, o.y1 + CLEAR));
            });
            return c;
        }
        function candidates(L) {
            var b = L.base, p = L.p;
            var w = b.x1 - b.x0, h = b.y1 - b.y0;
            var cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2;
            var at = function (x, y) { return [x - cx, y - cy]; };
            return [
                [2 * (p.x - cx), 0],                       // mirrored across the tip
                [0, 2 * (p.y - cy)],
                at(p.x, p.y - h / 2 - GAP),                // above the tip
                at(p.x, p.y + h / 2 + GAP),                // below
                at(p.x + w / 2 + GAP, p.y),                // right
                at(p.x - w / 2 - GAP, p.y),                // left
                [2 * (p.x - cx), 2 * (p.y - cy)],
                at(p.x, p.y - 1.5 * h - 2 * GAP),          // a step further out
                at(p.x, p.y + 1.5 * h + 2 * GAP),
                at(p.x + w / 2 + GAP, p.y - h / 2 - GAP),  // the four diagonals
                at(p.x - w / 2 - GAP, p.y - h / 2 - GAP),
                at(p.x + w / 2 + GAP, p.y + h / 2 + GAP),
                at(p.x - w / 2 - GAP, p.y + h / 2 + GAP),
                at(p.x, p.y - 2.5 * h - 3 * GAP),          // for a tip buried
                at(p.x, p.y + 2.5 * h + 3 * GAP)           // under an obstacle
            ];
        }
        for (var pass = 0; pass < PASSES; pass++) {
            var moved = false;
            labels.forEach(function (L) {
                var best = cost(L, L.b);
                if (!best) return;
                candidates(L).forEach(function (c) {
                    if (!best) return;
                    var b = shift(L.base, c[0], c[1]);
                    var s = inside(b);
                    b = shift(b, s[0], s[1]);
                    var k = cost(L, b);
                    if (k < best) {
                        best = k; L.b = b;
                        L.sx = c[0] + s[0]; L.sy = c[1] + s[1];
                        moved = true;
                    }
                });
            });
            if (!moved) break;
        }

        labels.forEach(function (L) {
            if (L.sx || L.sy) {
                L.d.style.transform = L.d.dataset.base + " translate(" +
                    L.sx.toFixed(1) + "px, " + L.sy.toFixed(1) + "px)";
            }
        });
    }

    function start() {
        var m = window[NAME];
        if (!m || !m.getSize) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        m.on("moveend zoomend resize viewreset", function () { place(m); });
        // The collapsed legend is an obstacle and the open one is not, so a
        // reader opening or closing it re-runs the placement.
        var legend = document.querySelector("details.map-legend");
        if (legend) legend.addEventListener("toggle", function () { place(m); });
        place(m);
    }
    start();
})();
</script>
"""
# Mouse-wheel zoom. Measured 2026-09-23 on Paris and Toulouse (headless Edge,
# trusted input over CDP, median of three fresh loads; DECISIONS.md has the
# tables). The wheel felt laggier than +/- for a reason that was not speed:
# Leaflet's _tryAnimatedZoom returns early while a zoom animation is running,
# so every wheel step that fires during the 250 ms animation is DISCARDED. A
# five-notch roll zoomed Paris 1.5 levels and three quick notches 0.75, so the
# reader rolled again and waited again. One notch was also 0.75 of a level
# against the buttons' 1, because the wheel snaps to zoomSnap (0.25).
#
# So the map's wheel handler is replaced with one that:
#   * never discards: a step due while an animation runs waits for it to land
#     and is merged with whatever else arrived meanwhile;
#   * zooms a NOTCHED wheel one whole level per notch, like one click on +/-
#     (owner's decision 2026-09-23), capped at zoomAnimationThreshold so a big
#     roll still animates;
#   * leaves anything finer - a trackpad - on Leaflet's own curve and snap.
#     Whole levels there were measured and rejected: with nothing discarded,
#     a half-second trackpad swipe went from 12.5 to 19.
#
# zoomSnap stays 0.25 - _fit_view, PHONE_FIT_SCRIPT's guard and
# scripts/check_map_view.js all depend on it. A whole-level step from x.5
# lands on x.5, so the wheel and the buttons now share one ladder of zooms.
#
# The guard's touch detection is untouched: it listens for `wheel` on the
# container in the CAPTURE phase, which runs before this handler, so a wheel
# zoom still ends the guard exactly as before.
WHEEL_ZOOM_SCRIPT = """
<script>
(function () {
    var NAME = "__MAP_NAME__";
    // One event of at least this many normalised units (L.DomEvent.
    // getWheelDelta) marks a notched wheel: Chrome and Edge on Windows give
    // 50 per notch, Firefox's line mode 60. Trackpads send many events of a
    // few units each.
    var NOTCH = 25;

    function install(m) {
        var h = m.scrollWheelZoom;
        if (!h) return;
        // Re-registering is the only way in: Leaflet bound the listener to the
        // handler's own _onWheelScroll when it enabled it.
        var was = h.enabled();
        h.disable();
        h._onWheelScroll = function (e) {
            var delta = L.DomEvent.getWheelDelta(e);
            this._delta += delta;
            this._maxEvent = Math.max(this._maxEvent || 0, Math.abs(delta));
            this._lastMousePos = this._map.mouseEventToContainerPoint(e);
            if (!this._startTime) this._startTime = +new Date();
            var left = Math.max(this._map.options.wheelDebounceTime -
                                (+new Date() - this._startTime), 0);
            clearTimeout(this._timer);
            this._timer = setTimeout(L.bind(this._performZoom, this), left);
            L.DomEvent.stop(e);
        };
        h._performZoom = function () {
            var map = this._map;
            if (map._animatingZoom) {
                clearTimeout(this._timer);
                this._timer = setTimeout(L.bind(this._performZoom, this), 20);
                return;
            }
            var zoom = map.getZoom(), step;
            map._stop();
            if (this._maxEvent >= NOTCH) {
                step = Math.min(Math.max(Math.round(Math.abs(this._delta) / this._maxEvent), 1),
                                map.options.zoomAnimationThreshold);
            } else {
                // Leaflet 1.9's own curve and snap, verbatim.
                var snap = map.options.zoomSnap || 0,
                    d2 = this._delta / (map.options.wheelPxPerZoomLevel * 4),
                    d3 = 4 * Math.log(2 / (1 + Math.exp(-Math.abs(d2)))) / Math.LN2;
                step = snap ? Math.ceil(d3 / snap) * snap : d3;
            }
            var delta = map._limitZoom(zoom + (this._delta > 0 ? step : -step)) - zoom;
            this._delta = 0;
            this._maxEvent = 0;
            this._startTime = null;
            if (!delta) return;
            if (map.options.scrollWheelZoom === "center") map.setZoom(zoom + delta);
            else map.setZoomAround(this._lastMousePos, zoom + delta);
        };
        if (was) h.enable();
    }

    // Folium's map script is inline at the end of the body, so the map exists
    // once parsing is done.
    function start() { if (window[NAME]) install(window[NAME]); }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
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


def load_osm_line_shapes(osm_routes_json, line_specs, system_name):
    """Real line geometries from OpenStreetMap route relations - the same
    return contract as load_line_shapes, for a city whose agency publishes no
    reachable feed.

    THIS EXISTS BECAUSE GTFS IS NOT THE ONLY SHAPE OF RAIL DATA, and all
    fourteen cities built before Mexico City happened to use it. Every
    `*.cdmx.gob.mx` host is unreachable, so CDMX's geometry is OSM's; Taipei's
    TDX, Sao Paulo's GeoSampa WFS and Israel's shapefiles are all non-GTFS too.
    Keeping both loaders here, returning the same thing, is what stops a city
    forking render_heatmap - the project's standing rule.

    line_specs: {key: (ref, color, real-world public name, label end)} - the
    same 4-tuple as the GTFS loader, with OSM's `ref` tag standing in for a
    shape_id. `ref` is what riders see on the line ("1", "A", "12"), and in
    CDMX it is populated on all 26 relations.

    Returns {key: (segments, color, label, end)}, segments longest first.
    """
    from shapely.geometry import MultiLineString
    from shapely.ops import linemerge

    if not osm_routes_json.exists():
        print(f"No OSM route file at {osm_routes_json} - skipping the "
              f"{system_name} line overlay.")
        return {}
    data = json.loads(osm_routes_json.read_text(encoding="utf-8"))
    rels = [e for e in data.get("elements", []) if e.get("type") == "relation"]
    if not rels:
        raise ValueError(
            f"{osm_routes_json} holds no route relations. An empty Overpass "
            "result must not be read as 'this city has no lines'."
        )

    lines = {}
    for key, (ref, color, label, end) in line_specs.items():
        mine = [r for r in rels if r.get("tags", {}).get("ref") == ref]
        if not mine:
            print(f"WARNING: OSM ref {ref!r} for the {label} is not in "
                  f"{osm_routes_json.name} - check the relation's tags.")
            continue
        # ONE ALIGNMENT PER LINE, chosen as the most complete of the direction
        # relations. A route in OSM is usually two relations, one per
        # direction, whose geometry is the same alignment traversed opposite
        # ways - drawing both would lay a line on top of itself and double the
        # vertex count for no visible gain. This mirrors what the GTFS cities
        # already do by taking each route's single most-used trip shape rather
        # than every shape it runs.
        def total_points(rel):
            return sum(len(m.get("geometry") or ())
                       for m in rel.get("members", ())
                       if m.get("type") == "way")

        best = max(mine, key=total_points)
        ways = [[(p["lat"], p["lon"]) for p in m["geometry"]]
                for m in best.get("members", ())
                if m.get("type") == "way" and m.get("geometry")]
        if not ways:
            print(f"WARNING: OSM ref {ref!r} ({label}) carried no way geometry.")
            continue

        # Stitch the member ways into as few continuous segments as possible.
        # A relation's ways are ordered but not merged, and a gap (a way the
        # mapper has not connected) legitimately splits a line into pieces -
        # so this keeps whatever linemerge produces rather than assuming one.
        merged = linemerge(MultiLineString([[(lon, lat) for lat, lon in w]
                                            for w in ways]))
        geoms = getattr(merged, "geoms", None)
        pieces = list(geoms) if geoms is not None else [merged]
        # Back to (lat, lon), which is what every other coordinate in this
        # module and in Folium uses.
        #
        # NOT rounded to COORD_DP, for the same reason the GTFS branch above is
        # not: these vertices are the source's own geometry. OSM is ODbL 1.0,
        # which requires attribution rather than forbidding modification, so
        # rounding would be permitted here - the exemption is kept anyway so
        # both loaders behave identically and a reader does not have to know
        # which source a city used to know what was done to its geometry.
        segments = [[(lat, lon) for lon, lat in g.coords] for g in pieces]
        segments.sort(key=len, reverse=True)
        lines[key] = (segments, color, label, end)
    return lines


def load_geojson_line_shapes(geojson_path, line_specs, system_name,
                             key_property="line"):
    """Line geometries from a GeoJSON the city's own step 1 produced - the same
    return contract as the GTFS and OSM loaders.

    THE THIRD SHAPE OF RAIL DATA, and the reason it is here rather than in a
    city's own file is the project's standing rule: a city that needs
    behaviour map_common lacks EXTENDS it, so nothing forks render_heatmap.
    GTFS came first, OSM second (Mexico City), and Madrid is the first city
    whose operator publishes its network as an ArcGIS feature service - CRTM
    stopped refreshing its Metro GTFS while still maintaining the layers, and
    its licence obliges a reuser to display current data. Step 1 writes those
    layers out as GeoJSON in WGS84; this reads them back.

    Expects one feature per line, its geometry a LineString or MultiLineString
    in lon/lat, identified by `key_property` (default "line") matching the keys
    of `line_specs`.

    line_specs: {key: (source_key, color, real-world public name, label end)} -
    the same 4-tuple as the other two loaders. `source_key` is matched against
    the feature property, standing in for a shape_id or an OSM ref.

    Returns {key: (segments, color, label, end)}, segments longest first.
    """
    if not geojson_path.exists():
        print(f"No line GeoJSON at {geojson_path} - skipping the "
              f"{system_name} line overlay.")
        return {}
    data = json.loads(geojson_path.read_text(encoding="utf-8"))
    feats = data.get("features") or []
    if not feats:
        # Same guard as the OSM loader's: an empty file is a failed step 1, not
        # a city without lines, and reading it as the latter is how a vacuous
        # pass gets recorded as a real one.
        raise ValueError(f"{geojson_path} holds no features. An empty line file "
                         "must not be read as 'this city has no lines'.")

    by_key = {}
    for f in feats:
        by_key.setdefault(str((f.get("properties") or {}).get(key_property)), f)

    lines = {}
    for key, (source_key, color, label, end) in line_specs.items():
        feat = by_key.get(str(source_key))
        if feat is None:
            print(f"WARNING: {key_property}={source_key!r} for the {label} is "
                  f"not in {geojson_path.name} - check step 1's output.")
            continue
        geom = feat.get("geometry") or {}
        if geom.get("type") == "LineString":
            parts = [geom["coordinates"]]
        elif geom.get("type") == "MultiLineString":
            parts = geom["coordinates"]
        else:
            print(f"WARNING: {label} has geometry {geom.get('type')!r}, which "
                  "is not a line - skipped.")
            continue
        # (lon, lat) -> (lat, lon), which is what the rest of this module and
        # Folium use. NOT rounded to COORD_DP, for the same reason the other two
        # loaders are not: these vertices are the source's own geometry.
        segments = [[(lat, lon) for lon, lat, *_ in part]
                    for part in parts if len(part) >= 2]
        if not segments:
            print(f"WARNING: {label} carried no drawable geometry.")
            continue
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


def _label_offset(label, ux, uy, clear=0.0):
    """Pixel offset (dx, dy; screen y grows downward) of a label's centre from
    its tip, and the label's half width/height. The label is pushed out along
    (ux, uy) just far enough that its own box clears the tip whatever the
    angle. ~14px bold text is ~8.2 px per character.

    `clear` is extra clearance in PIXELS, not metres, so a label that stands
    off its line keeps that distance at every zoom - an offset anchored in
    ground distance would look attached when zoomed out and adrift when zoomed
    in. See _label_candidates for why a label ever wants the extra room."""
    half_w = (len(label) * 8.2 + 10) / 2
    half_h = 11
    gap = 6 + clear
    reach = min(half_w / abs(ux) if abs(ux) > 1e-6 else 1e9, half_h / abs(uy) if abs(uy) > 1e-6 else 1e9)
    return ux * (reach + gap), -uy * (reach + gap), half_w, half_h


def _clearance(tip):
    """A label position is (lat, lon, ux, uy) or (lat, lon, ux, uy, clear).
    `_tail_end` returns the four-element form, `_label_candidates` the five,
    and both reach the same two consumers - so read the fifth defensively
    rather than making every producer carry it."""
    return tip[4] if len(tip) > 4 else 0.0


# The light theme's default label halo. A label that cannot read on it takes
# the dark theme's page colour instead (label_colours decides, per label).
LIGHT_LABEL_HALO = "#ffffff"


def add_line_label(feature_group, tip, label, color):
    """A permanent, always-visible line-name label at the tail end of the line
    - NOT a hover tooltip. Use the line's real public-facing name.

    `tip` is (lat, lon, ux, uy) from _tail_end, or the same with a fifth
    element - extra pixels of clearance - from _label_candidates: the label is
    centred just beyond the tip along the line's own direction, offset in
    pixels by the label's own size so it clears the line whatever the angle,
    and it stays put relative to the tip at every zoom."""
    lat, lon, ux, uy = tip[:4]
    dx, dy, _hw, _hh = _label_offset(label, ux, uy, _clearance(tip))
    # Both themes read at 4.5:1: the light theme's colour and halo (a yellow
    # keeps its colour on a dark halo rather than turning olive), and the dark
    # theme's colour, applied by the .dark-base rule - see
    # pipeline/linecolour.py, "LINE LABELS".
    light, halo, dark = label_colours(color, light_halo=LIGHT_LABEL_HALO,
                                      dark_halo=DARK["page"])
    # zIndexOffset lifts the label above the business-cluster badges: without
    # it a large downtown cluster is drawn on top of the label and hides it.
    folium.Marker(
        location=[round(lat, COORD_DP), round(lon, COORD_DP)],
        zIndexOffset=1000,
        icon=folium.DivIcon(
            icon_size=(0, 0),
            icon_anchor=(0, 0),
            html=f"""
            <div class="hm-line-label" style="
                position: absolute; left: 0; top: 0;
                transform: translate(-50%, -50%) translate({dx:.1f}px, {dy:.1f}px);
                font-size: 14px; font-weight: bold; color: {light}; --dm-label: {dark};
                text-shadow: -1px -1px 0 {halo}, 1px -1px 0 {halo},
                             -1px 1px 0 {halo}, 1px 1px 0 {halo},
                             0 0 6px {halo};
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
# Extra pixels of air between a label and its own line, tried only after every
# position at the normal 6px gap has failed. A CIRCULAR line is what forced
# this: Madrid's Línea 6 rings the centre, which is precisely where the other
# twelve lines converge, so all nineteen of its positions sat in the same jam
# and one label was drawn unreadable. Standing it off the ring clears it while
# it stays anchored to a point on its own line.
_LABEL_CLEARANCES = (22.0, 44.0)


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
    """Places a line's label may go, best first, each (lat, lon, ux, uy, clear).

    First the tail-end tip pointing straight out (and swung a little either
    way); then, if those are taken, spots further along the line from that
    tail, with the label sitting beside the line (either side); then all of
    those again with the label standing further off the line.

    ORDER IS THE CONTRACT. `_layout_labels` takes the first candidate that is
    clean, so anything appended here can only be reached by a label that would
    otherwise have been drawn on top of something - which is why the clearance
    tier could be added without moving a single label in the seventeen cities
    that were already placing all of theirs (confirmed by drift_check, not
    assumed). Never insert a new kind of candidate in the middle."""
    cands = []
    for angle in _LABEL_ANGLES:
        r = np.radians(angle)
        cands.append((tip[0], tip[1],
                      tip[2] * np.cos(r) - tip[3] * np.sin(r),
                      tip[2] * np.sin(r) + tip[3] * np.cos(r), 0.0))
    pts = list(coords)
    if np.hypot(pts[0][0] - tip[0], pts[0][1] - tip[1]) > np.hypot(pts[-1][0] - tip[0], pts[-1][1] - tip[1]):
        pts.reverse()   # so pts[0] is the tail end
    xy = _to_xy_m(pts, pts[0][0])
    seg = np.hypot(*np.diff(xy, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    total = cum[-1]
    if total <= 0:
        return cands + [(c[0], c[1], c[2], c[3], clear)
                        for clear in _LABEL_CLEARANCES for c in cands]
    for f in _ALONG_FRACTIONS:
        i = int(np.searchsorted(cum, f * total))
        i = min(max(i, 1), len(pts) - 2)
        tx, ty = xy[i + 1] - xy[i - 1]
        n = float(np.hypot(tx, ty)) or 1.0
        for sign in (1, -1):
            cands.append((pts[i][0], pts[i][1], -ty / n * sign, tx / n * sign, 0.0))
    return cands + [(c[0], c[1], c[2], c[3], clear)
                    for clear in _LABEL_CLEARANCES for c in cands]


def _layout_labels(points, candidates, labels, n_lines, center, zoom):
    """Place every label on screen at `center`/`zoom` without overlapping
    each other, another label's anchor point, the open legend, the map's own
    controls, or the map edge.

    Returns None if a station would fall off the map at this view, else
    (cost, {key: (lat, lon, ux, uy)}, [keys that could not be placed]) where
    cost counts labels that could not be placed cleanly (0 = all clean).

    The unplaced keys are carried out rather than just counted so the failure
    can name the line: "1 label could not be placed" sends you looking at
    thirteen lines, and the label in question is the one fact the solver
    already knows."""
    cx, cy = _project_px(center[0], center[1], zoom)

    def to_screen(lat, lon):
        x, y = _project_px(lat, lon, zoom)
        return x - cx + _MAP_W / 2, y - cy + _MAP_H / 2

    for lat, lon in points:
        sx, sy = to_screen(lat, lon)
        if not (15 <= sx <= _MAP_W - 15 and 15 <= sy <= _MAP_H - 15):
            return None

    # The legend (open) sits bottom-right; the zoom and layer controls top-left.
    # Capped as _LEGEND_CSS caps it (only a map past ~20 lines reaches it).
    legend_h = min(178 + 19 * n_lines, _MAP_H - 24 - _LEGEND_TOP_CLEAR)
    obstacles = [(_MAP_W - 24 - 274, _MAP_H - 24 - legend_h, _MAP_W - 24, _MAP_H - 24), (0, 0, 60, 110)]
    placed, chosen, unplaced = [], {}, []
    # Longest names first: they have the fewest places they fit.
    for key in sorted(candidates, key=lambda k: -len(labels[k])):
        best = None
        for cand in candidates[key]:
            lat, lon, ux, uy = cand[:4]
            sx, sy = to_screen(lat, lon)
            dx, dy, hw, hh = _label_offset(labels[key], ux, uy, _clearance(cand))
            box = (sx + dx - hw, sy + dy - hh, sx + dx + hw, sy + dy + hh)
            inside = box[0] >= 0 and box[1] >= 0 and box[2] <= _MAP_W and box[3] <= _MAP_H
            if best is None:
                best = (cand, box)   # fallback: the preferred spot, even if it collides
            if inside and not any(_boxes_overlap(box, o) for o in obstacles + placed):
                best = (cand, box)
                break
        else:
            unplaced.append(key)
        chosen[key] = best[0]
        placed.append(best[1])
        # keep later labels off this line's anchor point too
        lat, lon = best[0][0], best[0][1]
        sx, sy = to_screen(lat, lon)
        placed.append((sx - 5, sy - 5, sx + 5, sy + 5))
    return len(unplaced), chosen, unplaced


def _choose_view(points, candidates, labels, n_lines, center=None, zoom=None):
    """Pick the default map view and every label's position together.

    Start from the fit that shows all stations and the labels' preferred
    (tail-end) tips. Labels that would land on top of each other (or under the
    open legend) move elsewhere along their own lines; if that still can't
    separate them, the view zooms out in quarter steps and shifts away from the
    legend, taking the closest view that works. Explicit `center`/`zoom` are
    respected (labels are still laid out around them).
    Returns (center, zoom, {key: (lat, lon, ux, uy, clear)}).

    THE WHOLE VIEW SEARCH RUNS TWICE, and the second pass is what lets a label
    stand off its line. It has to be a separate pass rather than extra
    candidates in one: the search stops at the first view that places
    everything, so a candidate that rescues an EARLIER view silently changes
    which view a city gets. Added in one pass, the clearance tier moved San
    Francisco's map centre ~1 km west and sent one label off its line - a city
    whose labels were all placed cleanly already. Two passes keep the rule
    "nothing changes for a city that was already clean" true rather than
    plausible, and drift_check is what proves it."""
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
    def search(cands):
        found = None
        for c, z in views:
            result = _layout_labels(points, cands, labels, n_lines, c, z)
            if result is None:
                continue
            if found is None or result[0] < found[0]:
                found = (result[0], c, z, result[1], result[2])
            if result[0] == 0:
                break
        return found

    # Pass 1: every label hugging its own line, exactly the candidate set that
    # existed before stand-off labels were possible. Pass 2 only runs when a
    # label would otherwise be drawn unreadable, so a city that passes 1 can
    # never be changed by anything pass 2 does.
    best = search({k: [c for c in v if _clearance(c) == 0] for k, v in candidates.items()})
    if best is not None and best[0]:
        relaxed = search(candidates)
        if relaxed is not None and relaxed[0] < best[0]:
            best = relaxed
    if best is None:   # nothing fits with every station on screen: keep the fit as is
        return center, zoom, first

    # A RESIDUAL COST IS A LABEL NOBODY CAN READ, AND IT USED TO SHIP SILENTLY.
    #
    # `_layout_labels` falls back to "the preferred spot, even if it collides"
    # and counts one per unplaced label; this function then kept the cheapest
    # view and threw the count away. Madrid shipped that way on 2026-09-22:
    # three overlapping pairs, with **Línea 2 drawn underneath the Ramal label
    # and invisible at every width**. The legend row was there, so nothing in
    # the build or the legend looked wrong - it took a rendered screenshot in
    # deploy-verify to see it, one commit before a deploy.
    #
    # Raising rather than warning, because this is the project's oldest
    # invariant - every drawn line gets a permanent on-map label AND a legend
    # entry - and a warning in a build that prints hundreds of lines is a
    # warning nobody reads. Seventeen of eighteen cities were already at cost 0
    # when this was added, so it fails only where a label really is unreadable.
    #
    # To clear it: pass an explicit `center`/`zoom` for the city (a dense radial
    # network gives the solver little room), or force the crowded lines' label
    # ends with "start"/"end" in their spec - though note that a forced end is
    # no help at all to a CIRCULAR line, whose two ends are the same point.
    # That is what Madrid turned out to need, and why the second pass above
    # exists instead.
    if best[0]:
        named = ", ".join(f"{labels[k]!r} (line key {k!r})" for k in best[4])
        raise ValueError(
            f"{best[0]} transit-line label(s) could not be placed without "
            f"overlapping another label, the legend or the map edge, across "
            f"{len(views)} candidate view(s): {named}. They would be drawn on "
            f"top of something and be unreadable - which is not a cosmetic "
            f"issue but the every-line-is-labelled invariant. Set CENTER/ZOOM "
            f"for this city, or force the crowded lines' label ends "
            f"('start'/'end') in their line specs.")
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


def add_pin_layer(m, rows, group_name, color, tooltip_field_label,
                  value_column, show=True, display=None, animate=False):
    """One toggleable, clustered, coloured pin layer for a category bucket.
    Returns the number of points (0 = nothing added). `animate`: see
    render_heatmap's `animate_clusters`."""
    # Station name, ring band AND the classification value each repeat once per
    # pin, so each is emitted ONCE in a lookup table and referenced by integer
    # index. Nothing is lost: the callback resolves them before display.
    #
    # The classification value was added to this 2026-09-22, and Mexico City is
    # why. Its `scian_actividad` has **106 distinct values across 283,345
    # rows**, averaging 55 characters - "Comercio al por menor en tiendas de
    # abarrotes, ultramarinos y misceláneas" appears 12,462 times in one
    # rendered file. Inline that is ~7 MB of a 19 MB map. Every city benefits:
    # a classification field is a code or a category name drawn from a small
    # vocabulary, which is the definition of a good index candidate. Station
    # and band indexing was already worth ~1.2 MB on New York.
    #
    # The business name is deliberately NOT indexed: it is nearly unique per
    # pin (Mexico City has 97,440 distinct names across 133,362 pins, New York
    # 38k of 44k), so a lookup table would only add a second copy.
    #
    # COUPLED TO scripts/check_personal_exposure.py, which parses these arrays
    # out of the rendered HTML and reads row[2] and row[3]. Its `pins()`
    # resolves CATEGORIES by pairing the Nth table with the Nth `var data` in
    # document order, and still accepts a bare string at row[3] so a map
    # rendered before this change reads correctly. Change the two together.
    # A taxonomy may define display_value() to say how its classification
    # column should READ, as distinct from how it classifies. Dublin's
    # register pads unused use-slots with "-", so the raw column rendered as
    # "Use: -, SHOP" on 88.9% of its pins while the classifier had been
    # dropping the placeholder all along.
    _display = display or (lambda v: v)
    stations, bands, cats, data = {}, {}, {}, []
    for row in rows.itertuples():
        station = _esc(row.nearest_station)
        band = _esc(row.ring_band)
        cat = _esc(_display(getattr(row, value_column)))
        data.append([
            round(row.latitude, COORD_DP), round(row.longitude, COORD_DP),
            _esc(row.business_name),
            cats.setdefault(cat, len(cats)),
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
            var CATEGORIES = {json.dumps(list(cats))};
            var STATIONS = {json.dumps(list(stations))};
            var BANDS = {json.dumps(list(bands))};
            return function (row) {{
                var marker = L.circleMarker(new L.LatLng(row[0], row[1]), {{
                    radius: 5, color: '{color}', fillColor: '{color}',
                    fillOpacity: 0.85, weight: 1
                }});
                var html = '<b>' + row[2] + '</b><br>' +
                    '{tooltip_field_label}: ' + CATEGORIES[row[3]] + '<br>' +
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
    FastMarkerCluster(data, callback=callback, icon_create_function=icon_create_function,
                      options={"animate": animate}).add_to(fg)
    fg.add_to(m)
    return len(data)


def build_legend(bucket_colors, legend_label, lines):
    """Fixed-position legend generated from the buckets actually present
    and the taxonomy's own legend text - nothing taxonomy-specific here.

    bucket_colors: [(bucket name, color)]; legend_label: bucket -> text;
    lines: {key: (coords, color, label, end)}.
    """
    # _LEGEND_CSS is prepended AFTER formatting, not concatenated into
    # LEGEND_HTML: .format() would otherwise try to read every CSS brace as a
    # replacement field and raise KeyError on the first selector.
    return _LEGEND_CSS + LEGEND_HTML.format(
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
                   center=None, zoom=None, label_focus=None, rings_shown=False,
                   all_city_heat=True, animate_clusters=False):
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

    rings_shown: whether the concentric ring layers start switched on.
    **FALSE for every city since 2026-09-21** - the owner's call, for a cleaner
    first view. The rings stay in the layer control, one click away, and each
    business is still assigned to its NEAREST station whatever the rings show,
    so nothing about the counts depends on this.

    It had been True by default, with New York and Miami the two exceptions on
    measured grounds: New York's 496 stations sit a median 482 m apart and
    Miami's nineteen Metromover stations a median 235 m, so in both the rings
    merged into one indistinct wash downtown. That reasoning is kept here
    because it is why the toggle exists at all - but it turned out to describe
    the general case rather than two special ones, since every city's downtown
    cluster does some of this. Passing True is still supported for a city whose
    stations are sparse enough to want them on.

    animate_clusters: whether Leaflet.markercluster animates clusters splitting
    and merging at the end of each zoom. **FALSE for every city since
    2026-09-23** - the owner's call, on measurement: the animation runs a
    further ~300 ms after the map's own zoom animation, and turning it off took
    a Paris cluster click from 828 ms to settle to 408 ms (Toulouse 615 to 311)
    and a +/- click from 653 to 384 ms. The map's zoom still animates; the
    clusters simply regroup at the end instead of flying apart. Kept as a
    per-city switch so a light map can have it back - the owner's suggested
    rule is a measured lag threshold, and PLAN.md holds that open item.
    """
    taxonomy = load_taxonomy_module(taxonomy_system)
    bucket_colors = dict(CATEGORY_BUCKETS)

    # A line the reader cannot tell from the pins drawn on top of it is not a
    # drawn line. Measured here, at render, because Calgary's Blue Line shipped
    # Delta-E 3.3 from Retail blue - the same colour - and went unnoticed until
    # a different city's build ran the check for the first time. Raises only in
    # genuine-duplicate range; agency colours below the preferred figure are
    # reported every render and kept, per the owner's branding decision. See
    # pipeline/linecolour.py for why there are two thresholds.
    check_line_colours(
        {label: color for _coords, color, label, _end in lines.values()},
        bucket_colors, city=city_name)

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
    # The whole-city layer is OPT-OUT PER CITY, because it carries one
    # coordinate pair per business in the city and nothing filters it. In most
    # cities that is a modest cost; in Mexico City it is 283,345 pairs against
    # 133,362 in the default layer, and DENUE is an establishment census rather
    # than a licence register, so the gap is structural rather than a quirk.
    # Passing False drops the layer and says so on the city page - the map's
    # own question is density AROUND stations, and this layer is context.
    if all_city_heat:
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

    # A taxonomy may define layer_label() to name a bucket's layer the way its
    # legend names it. Amsterdam's legend reads "Shops and services" for the
    # Retail bucket (a building register cannot split retail from personal
    # services), and until 2026-09-24 its layer control still said "Retail".
    # Not legend_label() itself: NAICS's appends its code prefixes.
    layer_label = getattr(taxonomy, "layer_label", lambda bucket: bucket)
    present = []
    for name, color in CATEGORY_BUCKETS:
        rows = in_rings[in_rings["_bucket"] == name]
        if add_pin_layer(m, rows, layer_label(name), color, taxonomy.FIELD_LABEL,
                         taxonomy.VALUE_COLUMN,
                         display=getattr(taxonomy, "display_value", None),
                         animate=animate_clusters):
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
    # Anchors are fitted above; the labels' TEXT is kept inside the frame by
    # sliding it, not by zooming. See LABEL_CLAMP_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        LABEL_CLAMP_SCRIPT.replace("__MAP_NAME__", m.get_name())))
    # Mouse-wheel zoom that neither drops notches nor moves less than a click.
    # See WHEEL_ZOOM_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        WHEEL_ZOOM_SCRIPT.replace("__MAP_NAME__", m.get_name())))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    print(f"Wrote {output_path}")
    if all_city_heat:
        print(f"{len(in_rings):,} points plotted (within-ring default) / "
              f"{len(businesses):,} available (all-{city_name} toggle), "
              f"across {len(stations)} stations")
    else:
        # Do not advertise a toggle that was not built. This line said
        # "283,345 available (all-Mexico City toggle)" for one render after
        # the layer was dropped, which is the stale-prose failure this project
        # greps city pages for.
        print(f"{len(in_rings):,} points plotted (within-ring), across "
              f"{len(stations)} stations. The all-{city_name} heat layer is "
              f"OFF for this city ({len(businesses):,} businesses not drawn).")
