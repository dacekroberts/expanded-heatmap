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
from pathlib import Path

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from folium.plugins import HeatMap, FastMarkerCluster
from folium.template import Template

from pipeline.linecolour import check_line_colours, contrast_ratio, dark_label_colours, label_colours
from pipeline.taxonomies import CATEGORY_BUCKETS, load_taxonomy_module
from pipeline.theme import AMBIENT_THEME_JS, DARK, FONT_VAR, LIGHT, css_vars, font_stack, rgba

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
# computed against: the size passed to folium.Map in render_heatmap and the
# size app/pages/*.py embeds with st.iframe. Defined up here, not beside the
# label-layout constants, because _LEGEND_BOTTOM_CSS needs its value at import
# time and the comment blocks below refer to it.
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
    .replace("@@FONT_STACK@@", FONT_VAR)
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
    content: "\\25BE\\00A0Hide"; font: 600 11px """ + FONT_VAR + """;
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
# bottom edge, and the map is a fixed _MAP_H tall (see the folium.Map call in
# render_heatmap). Those two edges are the same line at exactly one viewport
# height, _MAP_H. Any taller and the map's bottom edge rises while the legend
# stays pinned to the viewport, and the legend swallows the attribution.
#
# Measured 2026-09-23 on Toulouse, five points hit-tested along the
# attribution strip (document.elementFromPoint), unclamped:
#
#     1000x650  what app/pages/*.py embeds with st.iframe      0/5 covered
#     1024x768  outputs/<city>/heatmap.html opened directly    5/5 covered
#     375x812   after a reader re-opens the collapsed legend   5/5 covered
#
# EVERY city, not one: the geometry is entirely in this file. The embedded
# size passed on a 10 px margin with nothing pinning it there. CLAUDE.md makes
# the visible basemap credit a hard invariant (ODbL 1.0 requires it not to sit
# behind UI), and a change to the iframe height, a responsive embed, or a
# reader opening the file directly each breached it silently.
#
# `max()` clamps the legend's bottom to 24 px above the MAP's bottom edge
# rather than the viewport's. At the embedded size that is the same position
# as unclamped, so the embed is pixel-unchanged; at every taller viewport it
# clears the 14 px attribution strip by the same 10 px. Shorter than _MAP_H
# the map overflows and the page scrolls, and there `max()` picks 24px, with
# the attribution clear once scrolled to.
#
# It also keeps a model true: _layout_labels treats the open legend as an
# obstacle whose bottom sits at _MAP_H - 24 in map coordinates. Unclamped,
# that held only at a 650 px viewport; clamped, it holds at every height at
# or above that.
#
# DO NOT replace this with a plain offset. The offset that clears the
# attribution is a function of viewport height, so any single number is right
# at exactly one height, which is the bug, not the fix. Moving the
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
# legend's style sits in a double-quoted attribute, so until 2026-09-24 the
# first family name closed the attribute, and every legend lost its 13px size,
# its shadow and every fallback font, rendering in Leaflet's Latin-only default.
# CSS accepts either quote, so the inline copy uses single quotes.
_LEGEND_FONT_STACK = FONT_VAR.replace('"', "'")

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
# The full Travel version's legend: the same panel, with the line rows and
# the named route rows only and no section heading, since nothing else
# shares it (owner, 2026-10-08: map content only). Its map fills the window,
# so the bottom is a plain 24 px, which clears the 14 px credit strip at the
# map's (and window's) bottom edge by 10 px, as the clamp does on a site map.
LEGEND_FULL_HTML = """
<details open class="map-legend" style="
    position: fixed; bottom: 24px; right: 24px; z-index: 9999;
    background: white; padding: 8px 14px; border: 1px solid #999;
    border-radius: 4px; font-family: """ + _LEGEND_FONT_STACK + """; font-size: 13px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
">
  <summary style="font-weight: bold; cursor: pointer; user-select: none;
    outline: none; margin-bottom: 6px;">Legend</summary>
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
# A reader who opens or closes it owns it from then on: the breakpoint stops
# overriding them (`touched`).
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
# frame immediately afterwards. Resizing AFTER init is safe (the bug is about an
# unresolved size at construction, not a small one), and `invalidateSize()` is
# Leaflet's own supported way to do it. The view is then re-fitted to the station
# bounds, which Python supplies rather than the script sniffing marker colours.
#
# What this does NOT fix: label PLACEMENT. `_layout_labels` chooses label
# positions server-side against a _MAP_W x _MAP_H canvas, so at phone width they
# can overlap each other and the cluster badges. LABEL_CLAMP_SCRIPT (below)
# re-places a label that collides with another label or a control; it does not
# avoid cluster badges (PLAN.md, "Optional label follow-ups").
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
    // zoom buttons, the pins and the in-map controls all count. The one
    // exception is a touch that cannot move the map: see steering() below.
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

    // A touch that cannot move the map is not steering. With one-finger
    // dragging off (TOUCH_GESTURE_SCRIPT, on a touch screen) a single finger
    // only scrolls the page, so its touchstart and pointerdown leave the guard
    // running; two fingers, or a tap (which goes on to send mousedown and
    // click, a scroll sends neither), still end it. With dragging on, every
    // touch counts, as before.
    function steering(m, e) {
        if (e.type === "touchstart") return e.touches.length > 1 || m.dragging.enabled();
        if (e.type === "pointerdown" && e.pointerType === "touch") return m.dragging.enabled();
        return true;
    }

    function armGuard(m) {
        var el = m.getContainer();
        ["pointerdown", "mousedown", "click", "touchstart", "wheel", "keydown"].forEach(
            function (ev) {
                el.addEventListener(ev, function (e) {
                    if (!steering(m, e)) return;
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
# KEEPS EVERY LINE LABEL INSIDE THE FRAME, by sliding it, never by zooming.
#
# A label's text reaches up to ~220px past the anchor at its line's tip, and
# PHONE_FIT_SCRIPT fits the ANCHORS (with 26px of padding), so on a phone a
# label at the tail of an outlying line ran off the frame: 22 of 25 cities,
# 35 of 155 labels at 375px and 33 at 343px, measured 2026-09-23 by
# scripts/check_map_labels.js (Rennes' "Métro b" cut to "Métr" in the app).
#
# Zooming out until every label fitted was measured and rejected: it removed
# every clip but took New York from 9.5 to 8.75 at 343px, shrinking the city
# to a knot of stacked labels, and raised overlapping label pairs across the
# 25 cities from 28 to 49. Sliding keeps the view exactly as it was (zoom,
# centre, PHONE_FIT_SCRIPT and its guard are untouched) and moves only a
# label that would otherwise be cut, only as far as it must, and only while
# its line's tip is on screen: once a reader pans the tip away, the label
# leaves with it.
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
# own line's tip (mirrored, above, below, right, left, a step further out)
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
# A SECOND, WIDER PHONE PLACER, for a map whose desktop layout already needed
# the wide label tier (_LABEL_WIDE_CLEARANCES). Added 2026-09-29.
#
# LABEL_CLAMP_SCRIPT re-places a colliding label among 15 spots around its own
# tip, which is enough for every map but one: Osaka's 34 labels had 22
# overlapping pairs at 343px and 12 at 375px (2026-09-29,
# scripts/check_map_labels.js). At the phone fit (zoom 10.75 on a 343 x 650
# frame) the labels cover 43% of the frame and most start in one knot of line
# tips, so every spot beside a tip is taken.
#
# So after the clamp has run, this moves ONLY a label that still overlaps
# another label or a control, measured with no margin (a label 1px clear of
# its neighbour is readable and stays put; with a margin, a desktop Osaka
# label moved), in two steps:
#   1. the nearest spot that collides less, from a grid of about a thousand
#      around its tip (the tip under the box or beside it, the box level with
#      the tip or in rows above and below), never more than __LABEL_REACH__ px
#      from the tip, the widest stand-off the desktop layout itself allows
#      (owner, 2026-09-27);
#   2. if it still overlaps, a spot blocked only by one or two labels that
#      each have a clean spot of their own to move to, all or nothing.
# Measured on Osaka: 22 -> 0 overlaps at 343px, 12 -> 0 at 375px, no label
# moved at 854 or 1280, about 20 ms a run on the dev machine (the clamp itself
# takes 35-70). It runs on every moveend, so the cutoffs in hits() and clean()
# matter: without them a run took 240 ms.
#
# INJECTED ONLY WHERE THE WIDE TIER WAS USED, so no other map changes by a
# byte (the third label pass's argument, one block on). Written into
# LABEL_CLAMP_SCRIPT it would have changed every committed map and failed
# check_render_current.py until a full re-render. On 2026-09-29 Osaka was the
# only one of 68 committed maps with a wide-tier label. It also clears
# Madrid's one 343px overlap (measured by injecting it); reaching Madrid is a
# change to the trigger in render_heatmap() plus Madrid's re-render.
#
# It runs after the clamp on every event the clamp listens to (a timeout puts
# it after every synchronous handler, whichever registered first), and undoes
# its own last move when the clamp has not reset the label since.
DENSE_LABEL_SCRIPT = """
<script>
(function () {
    var NAME = "__MAP_NAME__";
    var MARGIN = 6;     // as LABEL_CLAMP_SCRIPT: px from the frame edge
    var CLEAR = 2;      // as LABEL_CLAMP_SCRIPT: px from a button, control or legend
    var GAP = 4;        // px between a label and its line's tip
    var REACH = __LABEL_REACH__;   // px: no label box further than this from its own tip
    var STEP_X = 8, STEP_Y = 6;
    var PASSES = 8;
    var tries = 0, waits = 0;

    function box(x0, y0, x1, y1) { return {x0: x0, y0: y0, x1: x1, y1: y1}; }
    function shift(b, sx, sy) { return box(b.x0 + sx, b.y0 + sy, b.x1 + sx, b.y1 + sy); }
    function area(a, b) {
        var w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
        var h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
        return w > 0 && h > 0 ? w * h : 0;
    }
    function reach(b, p) {
        var dx = Math.max(b.x0 - p.x, 0, p.x - b.x1);
        var dy = Math.max(b.y0 - p.y, 0, p.y - b.y1);
        return Math.sqrt(dx * dx + dy * dy);
    }

    function place(m) {
        var size = m.getSize();
        if (!size.x || !size.y) return;
        var c = m.getContainer(), mr = c.getBoundingClientRect();
        var att = c.querySelector(".leaflet-control-attribution");
        var bottom = size.y - MARGIN - (att ? att.getBoundingClientRect().height : 0);
        function inside(b) {
            var dx = Math.max(0, MARGIN - b.x0) - Math.max(0, b.x1 - (size.x - MARGIN));
            var dy = Math.max(0, MARGIN - b.y0) - Math.max(0, b.y1 - bottom);
            return shift(b, dx, dy);
        }
        var obs = [], bare = [];
        function add(el) {
            if (!el) return;
            var r = el.getBoundingClientRect();
            if (r.width && r.height) {
                obs.push(box(r.left - mr.left - CLEAR, r.top - mr.top - CLEAR,
                             r.right - mr.left + CLEAR, r.bottom - mr.top + CLEAR));
                bare.push(box(r.left - mr.left, r.top - mr.top,
                              r.right - mr.left, r.bottom - mr.top));
            }
        }
        add(document.getElementById("map-actions"));
        var legend = document.querySelector("details.map-legend");
        if (legend && !legend.open) add(legend);
        c.querySelectorAll(".leaflet-top.leaflet-left .leaflet-control").forEach(add);

        // Every label where LABEL_CLAMP_SCRIPT left it. Undo this script's own
        // last move first if the clamp has not re-run since (its handler
        // resets every label to its baked transform, ours then appends).
        var labels = [], early = false;
        m.eachLayer(function (layer) {
            if (!layer._icon || !layer.getLatLng) return;
            var d = layer._icon.querySelector(".hm-line-label");
            if (!d) return;
            if (d.dataset.base === undefined) early = true;
            if (d.dataset.dense !== undefined && d.style.transform === d.dataset.dense) {
                d.style.transform = d.dataset.preDense;
            }
            var i = layer._icon.getBoundingClientRect();
            var r = d.getBoundingClientRect();
            if (!r.width) return;
            var p = m.latLngToContainerPoint(layer.getLatLng());
            if (p.x < 0 || p.y < 0 || p.x > size.x || p.y > size.y) return;
            var b = box(p.x + (r.left - i.left), p.y + (r.top - i.top),
                        p.x + (r.right - i.left), p.y + (r.bottom - i.top));
            labels.push({d: d, p: p, b0: b, b: b});
        });
        // LABEL_CLAMP_SCRIPT has not placed the labels yet (it records each
        // baked transform as data-base on its first run): wait for it, or it
        // would record this script's move as the baked position.
        if (early) {
            if (waits++ < 50) setTimeout(function () { place(m); }, 100);
            return;
        }

        // How much of box b is covered by other labels (each with a pixel of
        // margin) and obstacles - summed only until it reaches `upto`, since a
        // spot that bad is rejected whatever the rest adds.
        function hits(L, b, upto) {
            var k = 0, i, o, w, h;
            upto = upto === undefined ? Infinity : upto;
            for (i = 0; i < obs.length && k < upto; i++) k += area(b, obs[i]);
            for (i = 0; i < labels.length && k < upto; i++) {
                o = labels[i];
                if (o === L) continue;
                w = Math.min(b.x1, o.b.x1 + 1) - Math.max(b.x0, o.b.x0 - 1);
                h = Math.min(b.y1, o.b.y1 + 1) - Math.max(b.y0, o.b.y0 - 1);
                if (w > 0 && h > 0) k += w * h;
            }
            return k;
        }
        // hits(L, b) === 0, stopping at the first collision: step 2 asks it of
        // every spot a blocker might move to, and most collide.
        function clean(L, b) {
            var i, o;
            for (i = 0; i < obs.length; i++) if (area(b, obs[i])) return false;
            for (i = 0; i < labels.length; i++) {
                o = labels[i];
                if (o !== L && o.b.x0 - 1 < b.x1 && b.x0 < o.b.x1 + 1 &&
                    o.b.y0 - 1 < b.y1 && b.y0 < o.b.y1 + 1) return false;
            }
            return true;
        }
        // Whether a label really overlaps something, with no margin. Only such
        // a label moves: the margins in hits() choose between spots, but a
        // label 1 px clear of its neighbour is readable and stays put (a
        // desktop Osaka label did move, before this).
        function overlapped(L) {
            return labels.some(function (o) { return o !== L && area(L.b, o.b); }) ||
                   bare.some(function (o) { return area(L.b, o); });
        }
        // Spots for the label's box, nearest its own tip first: the tip under
        // the box anywhere along its width, or the box beside the tip; the box
        // level with the tip or in rows above and below it - never further
        // from the tip than REACH.
        function spots(L) {
            if (!L.spots) L.spots = spotsFor(L);
            return L.spots;
        }
        function spotsFor(L) {
            var w = L.b0.x1 - L.b0.x0, h = L.b0.y1 - L.b0.y0, p = L.p;
            var xs = [], ys = [], out = [], f, d;
            for (f = 0; f <= 8; f++) xs.push(p.x - f / 8 * w);
            for (d = GAP; d <= REACH; d += STEP_X) xs.push(p.x + d, p.x - w - d);
            for (f = -2; f <= 2; f++) ys.push(p.y - h / 2 + f / 4 * h);
            for (d = GAP; d <= REACH; d += STEP_Y) ys.push(p.y + d, p.y - h - d);
            xs.forEach(function (x) {
                ys.forEach(function (y) {
                    var b = inside(box(x, y, x + w, y + h));
                    var r = reach(b, p);
                    if (r <= REACH) out.push({b: b, r: r});
                });
            });
            out.sort(function (a, b) { return a.r - b.r; });
            return out;
        }

        // 1. A label that still overlaps something takes the nearest spot that
        //    collides less, the most-crowded label first.
        for (var pass = 0; pass < PASSES; pass++) {
            var moved = false;
            labels.slice().sort(function (a, b) { return hits(b, b.b) - hits(a, a.b); })
                .forEach(function (L) {
                    if (!overlapped(L)) return;
                    var best = hits(L, L.b), to = null;
                    spots(L).some(function (s) {
                        var k = hits(L, s.b, best);
                        if (k < best) { best = k; to = s.b; }
                        return !best;
                    });
                    if (to) { L.b = to; moved = true; }
                });
            if (!moved) break;
        }

        // 2. A label still colliding may make room: it takes a spot blocked
        //    only by one or two other labels, if each of those has a clean spot
        //    of its own to move to. All or nothing.
        labels.filter(overlapped)
            .sort(function (a, b) { return (b.b0.x1 - b.b0.x0) - (a.b0.x1 - a.b0.x0); })
            .forEach(function (L) {
                if (!overlapped(L)) return;
                spots(L).some(function (s) {
                    var blockers = labels.filter(function (o) {
                        return o !== L && area(s.b, box(o.b.x0 - 1, o.b.y0 - 1, o.b.x1 + 1, o.b.y1 + 1));
                    });
                    if (!blockers.length || blockers.length > 2) return false;
                    if (obs.some(function (o) { return area(s.b, o); })) return false;
                    var was = [L.b].concat(blockers.map(function (o) { return o.b; }));
                    L.b = s.b;
                    var ok = blockers.every(function (o) {
                        var hold = o.b;
                        o.b = box(-1e6, -1e6, -1e6, -1e6);   // out of its own way
                        var to = null;
                        spots(o).some(function (t) {
                            if (clean(o, t.b)) { to = t.b; return true; }
                            return false;
                        });
                        o.b = to || hold;
                        return !!to;
                    });
                    if (ok && clean(L, L.b)) return true;
                    L.b = was[0];
                    blockers.forEach(function (o, n) { o.b = was[n + 1]; });
                    return false;
                });
            });

        labels.forEach(function (L) {
            var sx = L.b.x0 - L.b0.x0, sy = L.b.y0 - L.b0.y0;
            if (!sx && !sy) return;
            L.d.dataset.preDense = L.d.style.transform;
            L.d.style.transform += " translate(" + sx.toFixed(1) + "px, " + sy.toFixed(1) + "px)";
            L.d.dataset.dense = L.d.style.transform;
        });
    }

    function start() {
        var m = window[NAME];
        if (!m || !m.getSize) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        var later = function () { setTimeout(function () { place(m); }, 0); };
        m.on("moveend zoomend resize viewreset", later);
        var legend = document.querySelector("details.map-legend");
        if (legend) legend.addEventListener("toggle", later);
        later();
    }
    start();
})();
</script>
"""
# TRAVEL MODE, THE HALF VERSION (owner, 2026-10-07; DECISIONS drafts, "Two
# travel versions"). Only in a map rendered with open_basemap. Picking the
# "Travel" base layer takes the business layers off the map (pins, both heat
# layers, the rings) and folds the legend's business section away; they stay
# in the layer menu, so a reader can turn any back on. Picking "Business"
# restores each layer's render-time default. The choice is remembered for the
# viewer (localStorage, wrapped: it can be absent or throw), so a reader who
# picked Travel opens the next city in Travel. The page still carries the
# register data either way: its notices and obligations do not change.
TRAVEL_MODE_SCRIPT = """
<style>
.map-legend.hm-travel .hm-biz { display: none; }
.map-legend:not(.hm-travel) .hm-travel-only { display: none; }
</style>
<script>
(function () {
    var NAME = "__MAP_NAME__", STD = "__STD_NAME__", OPEN = "__OPEN_NAME__";
    var BUSINESS = __BUSINESS__;
    var KEY = "expanded-heatmap-basemap";
    var tries = 0;
    function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
    function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
    function start() {
        var m = window[NAME], std = window[STD], open = window[OPEN];
        if (!m || !std || !open) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        var legend = document.querySelector("details.map-legend");
        var rows = legend && legend.querySelector(".hm-biz");
        if (rows && rows.previousElementSibling) rows.previousElementSibling.classList.add("hm-biz");
        function business(travel) {
            if (legend) legend.classList.toggle("hm-travel", travel);
            BUSINESS.forEach(function (b) {
                var layer = window[b[0]];
                if (!layer) return;
                var want = travel ? false : b[1];
                try {
                    if (want && !m.hasLayer(layer)) m.addLayer(layer);
                    if (!want && m.hasLayer(layer)) m.removeLayer(layer);
                } catch (err) {}
            });
        }
        // Deferred: the layer menu builds its add and remove lists from its
        // checkboxes before applying them and refreshes those checkboxes only
        // once its click is handled, so a change made inside the click is
        // undone or left showing stale ticks (measured 2026-10-07).
        m.on("baselayerchange", function (e) {
            var travel = e.layer === open;
            save(travel ? "travel" : "business");
            setTimeout(function () { business(travel); }, 0);
        });
        if (saved() === "travel") {
            m.removeLayer(std);
            m.addLayer(open);
        }
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
</script>
"""
# Blocks render_heatmap() injects into SOME maps only. check_render_current.py
# holds a map that carries one to its current version, and does not ask for it
# in a map that has none.
CONDITIONAL_BLOCKS = ("DENSE_LABEL_SCRIPT", "TRAVEL_MODE_SCRIPT", "FULL_TRAVEL_SCRIPT", "LEGEND_FULL_HTML")
# Mouse-wheel zoom. Measured 2026-09-23 on Paris and Toulouse (median of three
# fresh loads; DECISIONS.md has the tables). The wheel lagged behind +/- for a
# reason other than speed: Leaflet's _tryAnimatedZoom returns early while a
# zoom animation is running, so every wheel step that fires during the 250 ms
# animation is DISCARDED. A five-notch roll zoomed Paris 1.5 levels and three
# quick notches 0.75, so the reader rolled again and waited again. One notch
# was also 0.75 of a level against the buttons' 1, because the wheel snaps to
# zoomSnap (0.25).
#
# So the map's wheel handler is replaced with one that:
#   * never discards: a step due while an animation runs waits for it to land
#     and is merged with whatever else arrived meanwhile;
#   * zooms a NOTCHED wheel one whole level per notch, like one click on +/-
#     (owner's decision 2026-09-23), capped at zoomAnimationThreshold so a big
#     roll still animates;
#   * leaves anything finer (a trackpad) on Leaflet's own curve and snap.
#     Whole levels there were measured and rejected: with nothing discarded,
#     a half-second trackpad swipe went from 12.5 to 19.
#
# zoomSnap stays 0.25: _fit_view, PHONE_FIT_SCRIPT's guard and
# scripts/check_map_view.js all depend on it. A whole-level step from x.5
# lands on x.5, so the wheel and the buttons share one ladder of zooms.
#
# The guard's touch detection is unaffected: it listens for `wheel` on the
# container in the CAPTURE phase, which runs before this handler, so a wheel
# zoom still ends the guard.
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
# LEAFLET'S OWN CREDIT OPENS IN A NEW TAB (owner, 2026-10-03), as the OSM credit
# does (OSM_ATTRIBUTION): every map sits in an iframe, so a plain link replaced
# the map with the linked site inside the frame. The prefix is Leaflet's own,
# flag and all, with only a target added; setPrefix survives the control's
# re-renders, where editing its links in the DOM would not.
CREDIT_TAB_SCRIPT = """
<script>
(function () {
    var NAME = "__MAP_NAME__";
    function start() {
        var m = window[NAME], ac = m && m.attributionControl;
        if (!ac || typeof ac.options.prefix !== "string") return;
        var p = ac.options.prefix;
        if (p.indexOf("target=") === -1) {
            ac.setPrefix(p.replace(/<a /g, '<a target="_blank" rel="noopener noreferrer" '));
        }
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
</script>
"""
# PICK ONE LINE OUT (owner, 2026-09-30, from the live site on an iPhone).
# Where lines share track, the one drawn last covers the rest completely:
# Daugavpils' line 2 was never visible under the purple, Saint-Etienne's trams
# hid one another, Reims' T1 sat under T2. Tapping a line's LEGEND row, or the
# line itself, draws that whole line on top and thicker and fades the others;
# tapping it again, empty map, or another line restores or switches. A mouse
# hovering a line or a row previews the same. A line hidden end to end can
# only be reached through the legend, which is why every row is a button.
#
# Nothing is redrawn. Each line's polylines carry `hm-line hm-line-<n>` and
# its label and legend row `data-line="<n>"` (render_heatmap, n = the line's
# order), and a state is two CSS classes on the paths plus a reorder of the
# line paths INSIDE their own run of the SVG - so a picked line goes above the
# other lines but stays under the business dots, which are added after it.
# CSS stroke-width overrides the attribute, so the dark theme's
# `path[stroke-width="4"]` rule still matches a thickened line.
#
# A tap on the map is matched to a line by distance, not by what was hit: a
# 4 px line is too thin to tap, and the hidden line is never what was hit.
# Leaflet's own clipped, projected `_parts` are measured, as its
# _containsPoint does. A tap on a business dot, station or ring is left alone.
# The legend's open/collapsed state is never touched. On a touch screen a tap
# reaches here only when TAP_SELECT_SCRIPT found no dot, station or cluster
# nearer than the nearest line.
LINE_HIGHLIGHT_SCRIPT = """
<style>
.map-legend .hm-line-row { cursor: pointer; border-radius: 3px; }
.map-legend .hm-line-row:focus-visible { outline: none;
    background: rgba(127,127,127,0.16); box-shadow: 0 0 0 3px rgba(127,127,127,0.16); }
@media (hover: hover) {
    .map-legend .hm-line-row:hover { background: rgba(127,127,127,0.16);
        box-shadow: 0 0 0 3px rgba(127,127,127,0.16); } }
.map-legend .hm-line-row.hm-on { background: rgba(127,127,127,0.28);
    box-shadow: 0 0 0 3px rgba(127,127,127,0.28); }
.map-legend .hm-line-row.hm-on > span { transform: scaleY(2); }
.map-legend.hm-picking .hm-line-row:not(.hm-on) { opacity: 0.6; }
.leaflet-overlay-pane path.hm-line.hm-dim { stroke-opacity: 0.25; }
.leaflet-overlay-pane path.hm-line.hm-hot { stroke-width: 7px; stroke-opacity: 1; }
</style>
<script>
(function () {
    var NAME = "__MAP_NAME__";
    var tries = 0;

    function start() {
        var m = window[NAME];
        if (!m || !m.eachLayer) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        var lines = {};
        function line(k) { return lines[k] || (lines[k] = {polys: [], label: null}); }
        m.eachLayer(function (layer) {
            var c = layer.options && layer.options.className;
            var hit = typeof c === "string" && /\\bhm-line-(\\d+)\\b/.exec(c);
            if (hit && layer._path) {
                line(hit[1]).polys.push(layer);
                layer._path._hmLine = true;
            } else if (layer._icon) {
                var d = layer._icon.querySelector(".hm-line-label[data-line]");
                if (d) line(d.getAttribute("data-line")).label = layer;
            }
        });
        var keys = Object.keys(lines).filter(function (k) {
            return lines[k].polys.length;
        }).sort(function (a, b) { return a - b; });
        if (!keys.length) return;
        var legend = document.querySelector("details.map-legend");
        var rows = legend ? legend.querySelectorAll(".hm-line-row[data-line]") : [];
        var mq = function (q) { return !!(window.matchMedia && window.matchMedia(q).matches); };
        var HOVER = mq("(hover: hover) and (pointer: fine)");
        // 22 on a touch screen is TAP_SELECT_SCRIPT's REACH: a 44 px target.
        var TOL = mq("(pointer: coarse)") ? 22 : 7;
        var sel = null, hov = null, shown = null, outTimer = null;

        // The picked line's paths go last within the run of line paths, so
        // above every other line and still under anything drawn after them.
        function restack(top) {
            var paths = [];
            keys.forEach(function (k) {
                if (k !== top) lines[k].polys.forEach(function (p) { paths.push(p._path); });
            });
            if (top !== null) lines[top].polys.forEach(function (p) { paths.push(p._path); });
            var g = paths[0].parentNode;
            if (!g) return;
            var last = g.lastChild;
            while (last && !last._hmLine) last = last.previousSibling;
            var ref = last ? last.nextSibling : null;
            // Already in this order? Then touch nothing: re-inserting the path
            // under the pointer detaches it, and the browser never sends it
            // mouseout - which left a hover stuck on (map-refresh check).
            var run = [], n = last;
            while (n && run.length < paths.length) {
                if (n._hmLine) run.unshift(n);
                n = n.previousSibling;
            }
            if (run.length === paths.length && run.every(function (x, i) { return x === paths[i]; })) return;
            paths.forEach(function (p) { if (p.parentNode === g) g.insertBefore(p, ref); });
        }

        function show() {
            var want = hov !== null ? hov : sel;
            if (want === shown) return;
            shown = want;
            keys.forEach(function (k) {
                var on = k === want, rec = lines[k];
                rec.polys.forEach(function (p) {
                    p._path.classList.toggle("hm-hot", on);
                    p._path.classList.toggle("hm-dim", want !== null && !on);
                });
                if (rec.label) rec.label.setZIndexOffset(on ? 1500 : 1000);
            });
            for (var i = 0; i < rows.length; i++) {
                var on = rows[i].getAttribute("data-line") === want;
                rows[i].classList.toggle("hm-on", on);
                rows[i].setAttribute("aria-pressed", on ? "true" : "false");
            }
            if (legend) legend.classList.toggle("hm-picking", want !== null);
            restack(want);
        }
        function pick(k) { sel = sel === k ? null : k; show(); }
        // A short delay before a hover ends, so moving from one line onto the
        // line beside it, or a path being restacked under the pointer, does
        // not flash the whole map back to normal in between.
        function hover(k) {
            clearTimeout(outTimer);
            if (k !== null) { hov = k; show(); return; }
            outTimer = setTimeout(function () { hov = null; show(); }, 80);
        }

        function distance(rec, p) {
            var d = Infinity;
            rec.polys.forEach(function (layer) {
                (layer._parts || []).forEach(function (part) {
                    for (var i = 1; i < part.length; i++) {
                        d = Math.min(d, L.LineUtil.pointToSegmentDistance(p, part[i - 1], part[i]));
                    }
                });
            });
            return d;
        }

        m.on("click", function (e) {
            // On a touch screen TAP_SELECT_SCRIPT has already measured this
            // tap from where the finger lifted and sent it on as a line tap.
            var tap = window.__HEATMAP_TAP && window.__HEATMAP_TAP.last;
            var mine = !!(tap && tap.event === e.originalEvent);
            var at = mine ? m.containerPointToLayerPoint(tap.point) : e.layerPoint;
            var t = e.originalEvent && e.originalEvent.target;
            if (!mine && t && t.classList && t.classList.contains("leaflet-interactive") && !t._hmLine) return;
            var found = [];
            keys.forEach(function (k, i) {
                var d = distance(lines[k], at);
                if (d <= TOL) found.push({k: k, d: d, z: k === shown ? keys.length : i});
            });
            if (!found.length) { clearTimeout(outTimer); sel = null; hov = null; show(); return; }
            var near = Math.min.apply(null, found.map(function (f) { return f.d; }));
            var best = null;
            found.forEach(function (f) {
                if (f.d <= near + 1 && (!best || f.z > best.z)) best = f;
            });
            pick(best.k);
        });

        for (var i = 0; i < rows.length; i++) {
            (function (row) {
                var k = row.getAttribute("data-line");
                if (!lines[k]) return;
                row.addEventListener("click", function () { pick(k); });
                row.addEventListener("keydown", function (e) {
                    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(k); }
                });
                if (HOVER) {
                    row.addEventListener("mouseenter", function () { hover(k); });
                    row.addEventListener("mouseleave", function () { hover(null); });
                }
            })(rows[i]);
        }
        if (HOVER) {
            keys.forEach(function (k) {
                lines[k].polys.forEach(function (layer) {
                    layer.on("mouseover", function () { hover(k); });
                    layer.on("mouseout", function () { hover(null); });
                });
            });
            m.on("mousemove", function (e) {
                if (hov === null || !lines[hov]) return;
                var t = e.originalEvent && e.originalEvent.target;
                if (legend && t && legend.contains(t)) return;
                if (distance(lines[hov], e.layerPoint) > TOL) hover(null);
            });
        }
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && (sel !== null || hov !== null)) {
                clearTimeout(outTimer); sel = null; hov = null; show();
            }
        });
    }
    start();
})();
</script>
"""
# ONE FINGER SCROLLS THE PAGE, TWO MOVE THE MAP, on a touch screen (owner,
# 2026-10-02, the cooperative gestures Google Maps uses on websites). A city
# page embeds its map at 1000x650; at 375 px the frame is 333 px wide and
# nearly a whole phone screen tall, and Leaflet took every one-finger drag as
# a pan, so a reader whose swipe landed on the map could not scroll past it.
#
# On a device whose primary pointer is coarse, map.dragging is disabled.
# Leaflet then drops `leaflet-touch-drag` from the container, whose CSS falls
# back to `.leaflet-touch-zoom`'s `touch-action: pan-x pan-y`: the browser
# scrolls a one-finger swipe, and the map document (no taller than its frame)
# hands the scroll to the page around it. touchZoom stays on, and Leaflet's
# pinch handler moves the map with the midpoint of the two fingers, so a
# two-finger drag pans and a pinch zooms; dragging never has to come back
# for it (Leaflet's Draggable ignores a second finger anyway). Taps are not
# drags: dots, tooltips, line picking and every control are unchanged.
# Mouse, trackpad and a touch laptop with a mouse as its primary pointer keep
# one-finger (one-button) dragging; a change of primary pointer re-applies.
#
# A one-finger drag that starts on the map shows a hint for HINT_MS. It sits
# in the map container at z-index 900: above the panes and popups (700),
# under Leaflet's control corners (1000), which hold the zoom buttons, the
# layer control and the OSM credit, and under the legend and the button row,
# which are fixed in the body. So it can sit over a control's area without
# ever covering one. Movement is read in SCREEN coordinates: while the page
# scrolls, the frame travels with the finger and the finger's position inside
# the frame barely changes. The text is set on each showing, into a polite
# live region, and cleared once it has faded.
#
# PHONE_FIT_SCRIPT's guard reads map.dragging to tell a scroll from steering:
# a one-finger swipe that only scrolls the page leaves it running, so a
# reader who scrolls past a map early does not switch off the repair of a
# wrong first view (see steering() there).
_TOUCH_GESTURE_TEMPLATE = """
<style>
.hm-touch-hint { position: absolute; left: 50%; top: 50%; z-index: 900;
    transform: translate(-50%, -50%); pointer-events: none; opacity: 0;
    transition: opacity 0.25s; max-width: calc(100% - 48px); box-sizing: border-box;
    padding: 8px 14px; border-radius: 4px; text-align: center;
    font: 600 14px @@FONT_STACK@@;
    background: @@LIGHT_SURFACE@@; color: @@LIGHT_TEXT@@; border: 1px solid @@LIGHT_BORDER@@;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3); }
.hm-touch-hint:empty { display: none; }
.hm-touch-hint.hm-shown { opacity: 1; }
.dark-base .hm-touch-hint { background: var(--dm-surface); color: var(--dm-text);
    border-color: var(--dm-border); box-shadow: 0 1px 4px rgba(0,0,0,0.5); }
</style>
<script>
(function () {
    var NAME = "__MAP_NAME__";
    var TEXT = "Use two fingers to move the map";
    var HINT_MS = 1500;     // shown this long after the last one-finger move
    var FADE_MS = 300;      // a little over the CSS transition
    var MOVE_PX = 10;       // a tap's jitter stays under this
    var tries = 0;

    function start() {
        var m = window[NAME];
        if (!m || !m.dragging || !m.getContainer) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        var el = m.getContainer();
        var mq = window.matchMedia ? window.matchMedia("(pointer: coarse)") : null;
        var coop = false, disabledHere = false;

        function apply() {
            coop = !!(mq && mq.matches);
            if (coop && m.dragging.enabled()) { m.dragging.disable(); disabledHere = true; }
            else if (!coop && disabledHere) { m.dragging.enable(); disabledHere = false; }
            window.__HEATMAP_TOUCH = {cooperative: coop, dragging: m.dragging.enabled()};
        }
        apply();
        if (mq) {
            if (mq.addEventListener) mq.addEventListener("change", apply);
            else if (mq.addListener) mq.addListener(apply);
        }

        var hint = document.createElement("div");
        hint.className = "hm-touch-hint";
        hint.setAttribute("role", "status");
        hint.setAttribute("aria-live", "polite");
        el.appendChild(hint);
        var hideTimer = null, clearTimer = null;
        function hide() {
            clearTimeout(hideTimer);
            hint.classList.remove("hm-shown");
            clearTimeout(clearTimer);
            clearTimer = setTimeout(function () { hint.textContent = ""; }, FADE_MS);
        }
        function show() {
            clearTimeout(clearTimer);
            if (hint.textContent !== TEXT) hint.textContent = TEXT;
            hint.classList.add("hm-shown");
            clearTimeout(hideTimer);
            hideTimer = setTimeout(hide, HINT_MS);
        }

        function pos(t) {
            return t.screenX || t.screenY ? [t.screenX, t.screenY] : [t.clientX, t.clientY];
        }
        var from = null;
        el.addEventListener("touchstart", function (e) {
            from = null;
            if (!coop) return;
            if (e.touches.length !== 1) { hide(); return; }
            var t = e.target;
            if (t && t.closest && t.closest(".leaflet-control")) return;
            from = pos(e.touches[0]);
        }, {passive: true});
        el.addEventListener("touchmove", function (e) {
            if (!from) return;
            if (e.touches.length !== 1) { from = null; hide(); return; }
            var p = pos(e.touches[0]);
            if (Math.abs(p[0] - from[0]) + Math.abs(p[1] - from[1]) >= MOVE_PX) show();
        }, {passive: true});
        el.addEventListener("touchend", function (e) {
            if (!e.touches.length) from = null;
        }, {passive: true});
        el.addEventListener("touchcancel", function () { from = null; }, {passive: true});
    }
    start();
})();
</script>
"""
TOUCH_GESTURE_SCRIPT = (
    _TOUCH_GESTURE_TEMPLATE
    .replace("@@FONT_STACK@@", FONT_VAR)
    .replace("@@LIGHT_SURFACE@@", LIGHT["surface"])
    .replace("@@LIGHT_TEXT@@", LIGHT["text"])
    .replace("@@LIGHT_BORDER@@", LIGHT["border"])
)
assert "@@" not in TOUCH_GESTURE_SCRIPT, "unresolved placeholder in TOUCH_GESTURE_SCRIPT"
# A TAP SELECTS THE NEAREST THING WITHIN REACH, on a touch screen (owner,
# 2026-10-03, from an iPhone). A business dot is drawn 5 px across plus a 1 px
# stroke, so its SVG hit area is 11 px wide, a station's 13 px, and stations
# sit UNDER their lines (drawn later), so a tap on a station's centre hit the
# line. Measured before this script (DECISIONS.md 2026-10-03, "A tap on a phone",
# CDP touch emulation at 375 px on Edmonton, Paris, Tokyo and Odense): with no
# touch adjustment (WebKit's case) 0 of 43 taps 8 px off a dot opened it, and
# 0 of 6 taps on Tokyo's station centres opened the station. A spiderfied
# group closed under every second tap, even one dead on a dot: a path's
# click bubbles to the map (bubblingMouseEvents) and Leaflet.markercluster
# unspiderfies on any map click.
#
# So on a device whose primary pointer is coarse (the same test as
# TOUCH_GESTURE_SCRIPT), a capture listener on the map container sees every
# tap's click before Leaflet does and finds what is nearest, by geometry, not
# by what was hit: a dot or station within REACH px of its centre, a cluster
# within REACH of its centre or anywhere on its badge, a line within REACH of
# its centreline (LINE_HIGHLIGHT_SCRIPT's own tolerance on a touch screen is
# the same REACH). REACH 22 makes a 44 px target (WCAG 2.5.5, Apple's HIG).
# The nearest EDGE wins, and within TIE_PX a dot or station beats a cluster,
# which beats a line: a tap on a station's centre opens the station, a tap on
# the line beside it picks the line. While a group is spiderfied its own dots
# within reach win outright: the reader has just opened it, and a group beside
# a line otherwise lost taps 8 px out to the line (Tokyo, Odense).
#
# - A dot or station: the click goes no further (so Leaflet never sees an
#   empty-map click: a spiderfied group stays open, which is what closed it
#   under a reader's second tap), its tooltip text goes into a panel pinned
#   bottom-left, and a ring marks the dot. A tooltip anchored to the dot ran
#   off the 343 px map's left edge (Odense, owner's screenshot), so on a
#   touch screen the tooltip pane is hidden and the panel replaces it.
# - A cluster: the click is re-sent to the cluster's own badge, so
#   Leaflet.markercluster zooms or spiderfies exactly as for a direct tap.
#   A spiderfied cluster is skipped, so a tap among its legs finds a dot.
# - A line, or nothing within reach: the panel closes and the click goes on
#   to Leaflet unchanged (line picking, closing a spiderfied group).
#
# The panel is fixed in the body like the legend, above the OSM credit (24 px
# from the map's bottom edge, the legend's clamp) and above the legend when
# the legend leaves ROOM_PX over it, else beside it; it is re-placed on each
# showing, on resize and when the legend opens or closes. It closes on its
# own button, Escape, a tap on empty map or a line, and a new selection moves
# it. The ring follows its dot when a spiderfied group closes (the dot's
# `move`). PHONE_FIT_SCRIPT's guard is untouched: its capture listener on the
# same container still sees the tap's mousedown and click. Mouse and trackpad
# readers never reach any of this; their tooltips are unchanged.
_TAP_SELECT_TEMPLATE = """
<style>
.hm-tap-panel { display: none; position: fixed; z-index: 10000; box-sizing: border-box;
    left: 10px; bottom: 24px; max-width: 420px; overflow-y: auto;
    padding: 8px 40px 8px 12px; border-radius: 4px; overflow-wrap: anywhere;
    font: 13px/1.4 @@FONT_STACK@@;
    background: @@LIGHT_SURFACE@@; color: @@LIGHT_TEXT@@; border: 1px solid @@LIGHT_BORDER@@;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3); }
.hm-tap-panel.hm-shown { display: block; }
.hm-tap-close { position: absolute; top: 0; right: 0; width: 40px; height: 40px;
    padding: 0; border: 0; background: none; color: inherit; cursor: pointer;
    font: 22px/40px @@FONT_STACK@@; }
.dark-base .hm-tap-panel { background: var(--dm-surface); color: var(--dm-text);
    border-color: var(--dm-border); box-shadow: 0 1px 4px rgba(0,0,0,0.5); }
.hm-tap-ring { box-sizing: border-box; border-radius: 50%; pointer-events: none;
    border: 2px solid #fff; box-shadow: 0 0 0 2px #111, 0 0 6px 2px rgba(0,0,0,0.45); }
@media (pointer: coarse) { .leaflet-tooltip-pane { display: none; } }
</style>
<script>
(function () {
    var NAME = "__MAP_NAME__";
    var REACH = 22;         // px from a centre or centreline: a 44 px target
    var TIE_PX = 2;         // edges this close count as a tie, broken by kind
    var ROOM_PX = 200;      // map height the panel needs above the legend
    var RING_PX = 26;       // the selection ring's outer diameter
    var LIFT_MS = 800;      // a click this soon after a touchend is that tap's
    var tries = 0;

    function start() {
        var m = window[NAME];
        if (!m || !m.getContainer || !m.eachLayer) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        var el = m.getContainer();
        var mq = window.matchMedia ? window.matchMedia("(pointer: coarse)") : null;
        var legend = document.querySelector("details.map-legend");
        var TAP = window.__HEATMAP_TAP = {reach: REACH, last: null};

        var panel = document.createElement("div");
        panel.className = "hm-tap-panel";
        var body = document.createElement("div");
        body.setAttribute("role", "status");
        body.setAttribute("aria-live", "polite");
        var close = document.createElement("button");
        close.type = "button";
        close.className = "hm-tap-close";
        close.setAttribute("aria-label", "Close");
        close.innerHTML = "&times;";
        panel.appendChild(body);
        panel.appendChild(close);
        document.body.appendChild(panel);

        var ring = null, picked = null, passing = false;
        function follow() { if (ring && picked) { ring.setLatLng(picked.getLatLng()); place(); } }
        function clear() {
            panel.classList.remove("hm-shown");
            panel.removeAttribute("data-for");
            body.innerHTML = "";
            if (ring) { m.removeLayer(ring); ring = null; }
            if (picked) { picked.off("move", follow); picked = null; }
        }

        // Pinned bottom-left, clear of the OSM credit and of the legend.
        function place() {
            if (!panel.classList.contains("hm-shown")) return;
            var c = el.getBoundingClientRect();
            var vw = document.documentElement.clientWidth || window.innerWidth;
            var vh = document.documentElement.clientHeight || window.innerHeight;
            var top = Math.max(c.top, 0), bot = Math.min(c.bottom, vh);
            var left = Math.max(c.left, 0) + 10, right = vw - Math.min(c.right, vw) + 10;
            var bottom = vh - bot + 24;
            var lg = legend ? legend.getBoundingClientRect() : null;
            if (lg && lg.width && lg.left < vw - right && lg.top < bot - 24) {
                if (lg.top - top >= ROOM_PX) bottom = Math.max(bottom, vh - lg.top + 8);
                else right = Math.max(right, vw - lg.left + 8);
            }
            panel.style.left = left + "px";
            panel.style.right = right + "px";
            panel.style.top = "auto";
            panel.style.bottom = bottom + "px";
            panel.style.maxHeight = Math.max(80, Math.round(0.45 * (bot - top))) + "px";
            // Never over the dot it describes: then it goes to the top, under
            // the zoom and layer controls and the button row.
            if (ring && ring._icon && overlaps(ring._icon.getBoundingClientRect(), panel.getBoundingClientRect())) {
                var under = top;
                [el.querySelector(".leaflet-top.leaflet-left"), document.getElementById("map-actions")]
                    .forEach(function (n) { if (n) under = Math.max(under, n.getBoundingClientRect().bottom); });
                panel.style.bottom = "auto";
                panel.style.top = (under + 8) + "px";
                if (overlaps(ring._icon.getBoundingClientRect(), panel.getBoundingClientRect())) {
                    panel.style.top = "auto";
                    panel.style.bottom = bottom + "px";
                }
            }
        }
        function overlaps(a, b) {
            return a.right + 8 > b.left && a.left - 8 < b.right && a.bottom + 8 > b.top && a.top - 8 < b.bottom;
        }
        window.addEventListener("resize", place);
        m.on("moveend", place);
        if (legend) legend.addEventListener("toggle", place);
        close.addEventListener("click", clear);
        document.addEventListener("keydown", function (e) { if (e.key === "Escape") clear(); });

        function select(layer) {
            var tip = layer.getTooltip(), text = tip.getContent();
            if (typeof text === "function") text = text(layer);
            if (picked !== layer) { clear(); }
            if (typeof text === "string") body.innerHTML = text;
            else if (text && text.cloneNode) { body.innerHTML = ""; body.appendChild(text.cloneNode(true)); }
            panel.setAttribute("data-for", String(L.stamp(layer)));
            panel.classList.add("hm-shown");
            if (!ring) {
                ring = L.marker(layer.getLatLng(), {
                    interactive: false, keyboard: false,
                    icon: L.divIcon({className: "hm-tap-ring", iconSize: [RING_PX, RING_PX]})
                }).addTo(m);
            }
            if (picked !== layer) { picked = layer; layer.on("move", follow); }
            place();
            if (layer.isTooltipOpen()) layer.closeTooltip();
        }

        function isLine(l) {
            return (" " + (l.options.className || "") + " ").indexOf(" hm-line ") >= 0;
        }
        // Where the finger actually lifted. Chromium's touch adjustment moves
        // a tap's click onto a nearby target (a spiderfied cluster's badge,
        // say) and reports the moved point; the touch events keep the real one.
        var lift = null;
        el.addEventListener("touchend", function (e) {
            var t = e.changedTouches && e.changedTouches[0];
            lift = t ? {x: t.clientX, y: t.clientY, at: Date.now()} : null;
        }, {capture: true, passive: true});
        function tapPoint(e) {
            if (lift && Date.now() - lift.at < LIFT_MS &&
                Math.abs(lift.x - e.clientX) + Math.abs(lift.y - e.clientY) <= 2 * REACH) {
                return m.mouseEventToContainerPoint({clientX: lift.x, clientY: lift.y});
            }
            return m.mouseEventToContainerPoint(e);
        }

        // The nearest dot, station, cluster or line within reach of a tap.
        function nearest(p) {
            var lp = m.containerPointToLayerPoint(p);
            var best = null, fanned = null;
            function consider(kind, layer, d, reach, edge, rank) {
                if (d > reach) return;
                // Equal distance and kind: the later layer, drawn on top, is
                // the one the reader sees (categories cluster separately, so
                // two badges can share one point).
                if (!best || edge < best.edge - TIE_PX ||
                    (edge <= best.edge + TIE_PX && rank < best.rank) ||
                    (rank === best.rank && Math.abs(edge - best.edge) < 0.5)) {
                    best = {kind: kind, layer: layer, edge: edge, rank: rank};
                }
                // A dot of a spiderfied group the reader has just opened.
                if (layer._spiderLeg && (!fanned || edge < fanned.edge)) {
                    fanned = {kind: kind, layer: layer, edge: edge, rank: rank};
                }
            }
            m.eachLayer(function (l) {
                var q, r, d;
                if (l instanceof L.CircleMarker) {
                    // Rings (L.Circle) carry no tooltip and are not targets.
                    if (l instanceof L.Circle || !l.getTooltip || !l.getTooltip() || !l._point) return;
                    q = m.latLngToContainerPoint(l.getLatLng());
                    r = l._radius + (l.options.stroke ? l.options.weight / 2 : 0);
                    d = q.distanceTo(p);
                    consider("point", l, d, Math.max(REACH, r), d - r, 0);
                } else if (L.MarkerCluster && l instanceof L.MarkerCluster && l._icon) {
                    if (l._group && l._group._spiderfied === l) return;
                    q = m.latLngToContainerPoint(l.getLatLng());
                    r = l._icon.offsetWidth / 2;
                    d = q.distanceTo(p);
                    consider("cluster", l, d, Math.max(REACH, r), d - r, 1);
                } else if (l instanceof L.Polyline && l._parts && isLine(l)) {
                    d = Infinity;
                    l._parts.forEach(function (part) {
                        for (var i = 1; i < part.length; i++) {
                            d = Math.min(d, L.LineUtil.pointToSegmentDistance(lp, part[i - 1], part[i]));
                        }
                    });
                    consider("line", l, d, REACH, d - l.options.weight / 2, 2);
                }
            });
            return fanned || best;
        }

        el.addEventListener("click", function (e) {
            if (passing || !(mq && mq.matches)) return;
            var t = e.target;
            if (t && t.closest && t.closest(".leaflet-control")) return;
            var p = tapPoint(e), best = nearest(p);
            if (!best || best.kind === "line") {
                // On to Leaflet; LINE_HIGHLIGHT_SCRIPT reads this point.
                if (best) TAP.last = {event: e, point: p};
                clear();
                return;
            }
            e.stopPropagation();
            if (best.kind === "point") { select(best.layer); return; }
            clear();
            passing = true;
            try {
                best.layer._icon.dispatchEvent(new MouseEvent("click", {
                    bubbles: true, cancelable: true, view: window,
                    clientX: e.clientX, clientY: e.clientY}));
            } finally { passing = false; }
        }, true);
    }
    start();
})();
</script>
"""
TAP_SELECT_SCRIPT = (
    _TAP_SELECT_TEMPLATE
    .replace("@@FONT_STACK@@", FONT_VAR)
    .replace("@@LIGHT_SURFACE@@", LIGHT["surface"])
    .replace("@@LIGHT_TEXT@@", LIGHT["text"])
    .replace("@@LIGHT_BORDER@@", LIGHT["border"])
)
assert "@@" not in TAP_SELECT_SCRIPT, "unresolved placeholder in TAP_SELECT_SCRIPT"
LEGEND_ROW = """
  <div style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:11px; height:11px;
      border-radius:50%; background:{color}; margin-right:7px;
      border:1px solid rgba(0,0,0,0.3);"></span>{label}
  </div>
"""
# A short coloured line swatch, not a dot: it distinguishes transit lines from
# business categories at a glance, so a reader isn't relying on the on-map
# line labels alone (automatic placement can land imperfectly). Each row is
# also the button that picks its line out (LINE_HIGHLIGHT_SCRIPT); `line` is
# the line's order, the same n as its polylines' hm-line-<n> class.
LEGEND_LINE_ROW = """
  <div class="hm-line-row" data-line="{line}" role="button" tabindex="0" aria-pressed="false"
    style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:16px; height:3px;
      background:{color}; margin-right:7px;
      border-radius:2px;"></span>{label}
  </div>
"""
# A hollow station swatch, under its own heading: only on a map that draws
# stations with no business data (Tokyo's wards; owner 2026-09-28).
LEGEND_NO_DATA_ROWS = """
  <div style="font-weight: bold; margin: 10px 0 6px;">Stations</div>
  <div style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:9px; height:9px;
      border-radius:50%; background:transparent; margin-right:7px;
      border:2px solid {color};"></span>No business data (ward publishes no usable food-permit list)
  </div>
"""


def load_line_shapes(gtfs_zip, line_specs, system_name):
    """Return real line geometries from GTFS shapes.txt: the actual alignment,
    not straight lines between stations.

    line_specs: {key: (shape_id, color, real-world public name, label end)}
    where label end is None (automatic), "start" or "end": which end of the
    line its label goes at (see add_line_label).

    `shape_id` may instead be a tuple/list of shape_ids, for a line that is one
    named thing to riders but several alignments in the feed. New York needs
    this: a subway trunk (the "6 Av (B/D/F/M)" line) runs as one line through
    the core and branches outside it, so its geometry is several shapes sharing
    one label, one colour and one legend entry.

    Returns {key: (segments, color, label, end)} where `segments` is a list of
    coordinate lists, longest first, so `segments[0]` is the line's primary
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
            # Two agencies restrict altering it: LA Metro requires you "not
            # change, tamper, dismantle, augment, misrepresent or otherwise
            # modify the Transport Information", and the MTA's terms say "You
            # will not modify or delete any of the data" (while permitting "an
            # app that uses some but not all of the data", which is what
            # dropping commuter rail and drawing 29 services as 11 trunks is).
            # Rounding to 0.11 m is invisible, but the project's rule is to
            # comply rather than to read such a clause generously.
            #
            # Measured 2026-09-21 over EVERY vertex (sampling the first few
            # thousand characters gave the wrong answer for LA Metro):
            #   LA Metro  max 10 dp, 21.0% of coords over 6 dp  <- WAS rounded
            #   MTS       max  8 dp, 99.2% over 6 dp            <- WAS rounded
            #   CTA       max  8 dp, 99.2% over 6 dp            <- WAS rounded
            #   MTA       max  6 dp,  0.0% over 6 dp            <- no-op
            #   SFMTA     max  6 dp,  0.0% over 6 dp            <- no-op
            #   SEPTA     max  6 dp,  0.0% over 6 dp            <- no-op
            # So rounding altered LA Metro's geometry (the tightest licence in
            # the project) on a fifth of its vertices, and this exemption is
            # what makes the recorded verdict ("the rail alignment is the
            # feed's own geometry, displayed as that line") literally true.
            # MTA's feed is already 6 dp. MTS and CTA were being rounded too,
            # and neither restricts modification.
            #
            # Keep this exemption if COORD_DP is ever lowered to 5 dp (a
            # PLAN.md proposal, to shrink New York's map): at 5 dp, rounding
            # would alter MTA's geometry too, as a silent side effect of a size
            # tweak.
            #
            # Station coordinates deliberately stay rounded: most cities derive
            # them by averaging a parent station's platform stops, so they are
            # this project's own computed values rather than agency data, and
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
    """Return real line geometries from OpenStreetMap route relations, with the
    same return contract as load_line_shapes, for a city whose agency publishes
    no reachable feed.

    THIS EXISTS BECAUSE GTFS IS NOT THE ONLY SHAPE OF RAIL DATA, and all
    fourteen cities built before Mexico City happened to use it. Every
    `*.cdmx.gob.mx` host is unreachable, so CDMX's geometry is OSM's; Taipei's
    TDX, Sao Paulo's GeoSampa WFS and Israel's shapefiles are all non-GTFS too.
    Keeping both loaders here, returning the same thing, is what stops a city
    forking render_heatmap (the project's standing rule).

    line_specs: {key: (ref, color, real-world public name, label end)}, the
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


def add_line_label(feature_group, tip, label, color, dark=None, line=None):
    """Add a permanent, always-visible line-name label at the tail end of the
    line (NOT a hover tooltip). Use the line's real public-facing name.

    `tip` is (lat, lon, ux, uy) from _tail_end, or the same with a fifth
    element (extra pixels of clearance) from _label_candidates: the label is
    centred just beyond the tip along the line's own direction, offset in
    pixels by the label's own size so it clears the line whatever the angle,
    and it stays put relative to the tip at every zoom.

    `line`: the line's order in render_heatmap, written as data-line so
    LINE_HIGHLIGHT_SCRIPT can lift this label with its line."""
    lat, lon, ux, uy = tip[:4]
    data_line = "" if line is None else f' data-line="{int(line)}"'
    dx, dy, _hw, _hh = _label_offset(label, ux, uy, _clearance(tip))
    # Both themes read at 4.5:1: the light theme's colour and halo (a yellow
    # keeps its colour on a dark halo rather than turning olive), and the dark
    # theme's colour, applied by the .dark-base rule - see
    # pipeline/linecolour.py, "LINE LABELS". `dark` comes from the city-level
    # dark_label_colours(), which keeps two lines' labels apart.
    light, halo, dark = label_colours(color, light_halo=LIGHT_LABEL_HALO,
                                      dark_halo=DARK["page"], dark=dark)
    # zIndexOffset lifts the label above the business-cluster badges: without
    # it a large downtown cluster is drawn on top of the label and hides it.
    folium.Marker(
        location=[round(lat, COORD_DP), round(lon, COORD_DP)],
        zIndexOffset=1000,
        icon=folium.DivIcon(
            icon_size=(0, 0),
            icon_anchor=(0, 0),
            html=f"""
            <div class="hm-line-label"{data_line} style="
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
# A THIRD tier, reached only by a THIRD view search that runs only when the
# second still leaves a label unplaceable - so no city that already placed
# every label can move (the two-pass argument in _choose_view, one pass on).
# Osaka forced it (2026-09-27, owner): 34 lines, and the Osaka Loop, JR Hanwa
# and JR Kobe lines' whole in-city track lies in the densest core, where no
# spot within 44 px of the line is free in any of 55 views.
_LABEL_WIDE_CLEARANCES = (66.0, 88.0)


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
    otherwise have been drawn on top of something. That is why the clearance
    tier moved no label in the seventeen cities that were already placing all
    of theirs (drift_check showed it). Never insert a new kind of candidate in
    the middle."""
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
                        for clear in _LABEL_CLEARANCES + _LABEL_WIDE_CLEARANCES for c in cands]
    for f in _ALONG_FRACTIONS:
        i = int(np.searchsorted(cum, f * total))
        i = min(max(i, 1), len(pts) - 2)
        tx, ty = xy[i + 1] - xy[i - 1]
        n = float(np.hypot(tx, ty)) or 1.0
        for sign in (1, -1):
            cands.append((pts[i][0], pts[i][1], -ty / n * sign, tx / n * sign, 0.0))
    # the wide tier last: appended, never inserted (the order contract above)
    return cands + [(c[0], c[1], c[2], c[3], clear)
                    for clear in _LABEL_CLEARANCES + _LABEL_WIDE_CLEARANCES for c in cands]


def _layout_labels(points, candidates, labels, n_lines, center, zoom):
    """Place every label on screen at `center`/`zoom` without overlapping
    each other, another label's anchor point, the open legend, the map's own
    controls, or the map edge.

    Returns None if a station would fall off the map at this view, else
    (cost, {key: (lat, lon, ux, uy)}, [keys that could not be placed]) where
    cost counts labels that could not be placed cleanly (0 = all clean).

    The unplaced keys are carried out rather than just counted so the failure
    can name the line: "1 label could not be placed" sends a reader looking at
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
    obstacles = [(_MAP_W - 24 - LEGEND_MODEL_W, _MAP_H - 24 - legend_h, _MAP_W - 24, _MAP_H - 24), (0, 0, 60, 110)]
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
    Francisco's map centre ~1 km west and sent one label off its line, in a
    city whose labels were all placed cleanly already. Two passes keep the rule
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
        # Pass 2: exactly the candidates it always had (no wide tier), so a
        # city it rescued before the wide tier existed is rescued identically.
        relaxed = search({k: [c for c in v if _clearance(c) not in _LABEL_WIDE_CLEARANCES]
                          for k, v in candidates.items()})
        if relaxed is not None and relaxed[0] < best[0]:
            best = relaxed
    if best is not None and best[0]:
        # Pass 3 (Osaka): a label may stand up to 88 px off its line.
        wide = search(candidates)
        if wide is not None and wide[0] < best[0]:
            best = wide
    if best is None:   # nothing fits with every station on screen: keep the fit as is
        return center, zoom, first

    # A RESIDUAL COST IS A LABEL NOBODY CAN READ, AND IT USED TO SHIP SILENTLY.
    #
    # `_layout_labels` falls back to "the preferred spot, even if it collides"
    # and counts one per unplaced label; this function then kept the cheapest
    # view and threw the count away. Madrid shipped that way on 2026-09-22:
    # three overlapping pairs, with **Línea 2 drawn underneath the Ramal label
    # and invisible at every width**. The legend row was there, so nothing in
    # the build or the legend looked wrong; only a rendered view showed it.
    #
    # Raising rather than warning, because this is the project's oldest
    # invariant (every drawn line gets a permanent on-map label AND a legend
    # entry), and a warning in a build that prints hundreds of lines is a
    # warning nobody reads. Seventeen of eighteen cities were already at cost 0
    # when this was added, so it fails only where a label really is unreadable.
    #
    # To clear it: pass an explicit `center`/`zoom` for the city (a dense radial
    # network gives the solver little room), or force the crowded lines' label
    # ends with "start"/"end" in their spec. A forced end is no help to a
    # CIRCULAR line, whose two ends are the same point; Madrid's needed the
    # second pass above.
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


# WHY THE BIG ARRAYS ARE SHIPPED AS JSON.parse("...") AND NOT AS LITERALS
# (2026-09-27). WebKit (every iOS browser) refuses to compile one inline
# array literal above roughly 107k-131k elements ("RangeError: Maximum call
# stack size exceeded"), and the map goes blank with no visible error. Every
# map that failed on the owner's iPhone had a heat literal of 133,335+ points;
# every map that loaded was at 106,652 or below. JSON.parse of the same data
# as one string loaded, because a string literal is one token to the compiler.
# See DECISIONS 2026-09-27 and PLAN's "Seoul's map still 24 MB" item.
#
# So the two Folium elements that carry per-business data are subclassed with
# their own templates, identical to Folium 0.20's except the data line. Folium
# keeps no template source to patch, so these are copies: a Folium upgrade
# does not change them, and scripts/check_inline_arrays.py fails any committed
# map that has an oversized inline literal again, whatever the cause.
#
# COUPLED TO scripts/check_personal_exposure.py, which parses the pin arrays
# back out of the rendered HTML. Change the two together.


def _js_json(data):
    """`data` as a JavaScript string literal holding its JSON, safe to place
    inside a <script> element: JSON inside a JS string inside HTML.

    Built only from library calls, never by hand: json.dumps of the data, then
    json.dumps of that text (a JSON string is a valid JS string literal), then
    the characters HTML or old engines could still misread are replaced with
    their \\u escapes, which decode back to the same characters inside the
    string: `<` (so no `</script>` or `<!--` can close or confuse the
    element), `>`, `&`, and U+2028/U+2029 (line terminators in pre-2019 JS).

    allow_nan=False because JSON.parse rejects NaN: a bad row must fail the
    BUILD here, not blank the published map."""
    inner = json.dumps(data, allow_nan=False, ensure_ascii=False, separators=(",", ":"))
    outer = json.dumps(inner, ensure_ascii=False)
    for ch, esc in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"),
                    (" ", "\\u2028"), (" ", "\\u2029")):
        outer = outer.replace(ch, esc)
    return outer


class ParsedHeatMap(HeatMap):
    """Folium's HeatMap, with its points shipped as JSON.parse("...")."""
    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.heatLayer(
                JSON.parse({{ this.data_js }}),
                {{ this.options|tojavascript }}
            );
        {% endmacro %}
        """
    )

    @property
    def data_js(self):
        return _js_json(self.data)


class ParsedFastMarkerCluster(FastMarkerCluster):
    """Folium's FastMarkerCluster, with its rows shipped as JSON.parse("...")."""
    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = (function(){
                {{ this.callback }}

                var data = JSON.parse({{ this.data_js }});
                var cluster = L.markerClusterGroup({{ this.options|tojavascript }});
                {%- if this.icon_create_function is not none %}
                cluster.options.iconCreateFunction =
                    {{ this.icon_create_function.strip() }};
                {%- endif %}

                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var marker = callback(row);
                    marker.addTo(cluster);
                }

                cluster.addTo({{ this._parent.get_name() }});
                return cluster;
            })();
        {% endmacro %}"""
    )

    @property
    def data_js(self):
        return _js_json(self.data)


def _esc(value):
    """HTML-escape a value for the tooltip. Business names come from public
    datasets but are still free text: an unescaped '<' or '&' breaks the
    hover text or injects markup."""
    return "" if pd.isna(value) else html.escape(str(value), quote=True)


def add_pin_layer(m, rows, group_name, color, tooltip_field_label,
                  value_column, show=True, display=None, animate=False, registry=None):
    """Add one toggleable, clustered, coloured pin layer for a category bucket.
    Return the number of points (0 = nothing added). `animate`: see
    render_heatmap's `animate_clusters`. `registry`: a list the layer's JS
    variable name is appended to (TRAVEL_MODE_SCRIPT's business layers)."""
    # Station name, ring band AND the classification value each repeat once per
    # pin, so each is emitted ONCE in a lookup table and referenced by integer
    # index. Nothing is lost: the callback resolves them before display.
    #
    # The classification value is indexed since 2026-09-22, because of Mexico
    # City: its `scian_actividad` has **106 distinct values across 283,345
    # rows**, averaging 55 characters ("Comercio al por menor en tiendas de
    # abarrotes, ultramarinos y misceláneas" appears 12,462 times in one
    # rendered file). Inline that is ~7 MB of a 19 MB map. Every city benefits:
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
    # "Use: -, SHOP" on 88.9% of its pins while the classifier dropped the
    # placeholder.
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
    # `var callback = ...` is assigned, NOT once per pin. FastMarkerCluster
    # injects this as a statement and then calls callback(row) in its loop.
    callback = f"""
        (function () {{
            var CATEGORIES = {json.dumps(list(cats))};
            var STATIONS = {json.dumps(list(stations))};
            var BANDS = {json.dumps(list(bands))};
            return function (row) {{
                // bubblingMouseEvents false: a click on a dot of a spiderfied
                // group no longer reaches the map, where Leaflet.markercluster
                // unspiderfies on any click (desktop; owner, 2026-10-04).
                var marker = L.circleMarker(new L.LatLng(row[0], row[1]), {{
                    radius: 5, color: '{color}', fillColor: '{color}',
                    fillOpacity: 0.85, weight: 1, bubblingMouseEvents: false
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
    ParsedFastMarkerCluster(data, callback=callback, icon_create_function=icon_create_function,
                            options={"animate": animate}).add_to(fg)
    fg.add_to(m)
    if registry is not None:
        registry.append((fg.get_name(), show))
    return len(data)


# The open legend's width as _layout_labels models it (the obstacle every
# label is placed around). A legend sizes to its longest row; every map's rows
# fitted this until Tokyo's "code + full name" rows ("JO  JR Yokosuka / Sobu
# Rapid Line") made its legend 409 px wide and it covered 5 labels at the 1000
# px frame (2026-09-28). A map with legend_names is therefore
# capped at this width and its long rows wrap, so the model stays true.
LEGEND_MODEL_W = 274
_LEGEND_CAP_STYLE = f"<style>.map-legend {{ max-width: {LEGEND_MODEL_W}px; }}</style>"


def build_legend(bucket_colors, legend_label, lines, no_data_stations=False, legend_names=None,
                 travel=False, routes=(), full=False):
    """Build the fixed-position legend from the buckets actually present
    and the taxonomy's own legend text; nothing taxonomy-specific here.

    bucket_colors: [(bucket name, color)]; legend_label: bucket -> text;
    lines: {key: (coords, color, label, end)}. no_data_stations: the map draws
    hollow stations (Tokyo's wards with no data), so the legend says what a
    hollow station means; a map without them keeps its legend byte for byte.
    legend_names: {key: full name} where the on-map label is a line code
    (render_heatmap); the row reads "code  full name", or the full name
    alone when it already starts with the label (Newcastle's "Green line
    (Tyne and Wear Metro)", owner 2026-10-02).
    travel: wrap the business section in `.hm-biz`, which TRAVEL_MODE_SCRIPT
    folds away in Travel; False leaves the legend byte for byte as before.
    routes: [(kind, name)] of the NAMED ferry and cable-car routes the Travel
    pack holds; each gets a row under the transit lines with its own name
    ("Arno Boat"), drawn as on the Travel map and shown in Travel only. A
    generic "Ferry" row is deliberately absent and an unnamed route gets no
    row: what a dashed line means belongs to the app's own info page, and
    the map carries map content only (owner, 2026-10-08).
    full: the full Travel version's legend (LEGEND_FULL_HTML): the line rows
    and route rows only, in the full variant's colours; bucket_colors and
    legend_label are ignored.
    """
    names = legend_names or {}
    if full:
        bucket_colors, travel = (), True
    line_rows = "".join(
        LEGEND_LINE_ROW.format(line=n, color=color, label=html.escape(
            names[key] if key in names and names[key].startswith(label)
            else f"{label} {names[key]}" if key in names else label))
        for n, (key, (_coords, color, label, _end)) in enumerate(lines.items())
    )
    if no_data_stations:
        line_rows += LEGEND_NO_DATA_ROWS.format(color=LIGHT["station"])
    named = [(kind, name) for kind, name in routes if name and kind in TRAVEL_ROUTE_ROWS]
    if travel and named:
        route_rows = "".join(
            TRAVEL_ROUTE_ROWS[kind].format(color=TRAVEL_ROUTE_COLOURS["full" if full else "site"][kind],
                                           label=html.escape(name))
            for kind, name in sorted(set(named), key=lambda r: (r[0] != "ferry", r[1])))
        line_rows += route_rows if full else f'<div class="hm-travel-only">{route_rows}</div>'
    if full:
        return (_LEGEND_CSS + (_LEGEND_CAP_STYLE if names else "")
                + LEGEND_FULL_HTML.format(line_rows=line_rows)
                + LEGEND_AUTOFIT_SCRIPT.replace("__MAP_W__", str(_MAP_W)))
    # _LEGEND_CSS is prepended AFTER formatting, not concatenated into
    # LEGEND_HTML: .format() would otherwise try to read every CSS brace as a
    # replacement field and raise KeyError on the first selector.
    category_rows = "".join(
        LEGEND_ROW.format(color=color, label=html.escape(legend_label(name)))
        for name, color in bucket_colors
    )
    # Only the slot's own content is wrapped, so LEGEND_HTML's fixed text stays
    # verbatim for check_render_current.py; TRAVEL_MODE_SCRIPT gives the
    # heading just before the wrap the same class.
    if travel:
        category_rows = f'<div class="hm-biz">{category_rows}</div>'
    legend = LEGEND_HTML.format(category_rows=category_rows, line_rows=line_rows)
    return (_LEGEND_CSS + (_LEGEND_CAP_STYLE if names else "") + legend
            + LEGEND_AUTOFIT_SCRIPT.replace("__MAP_W__", str(_MAP_W)))


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
# Found 2026-09-21, outside any check: scripts/check_personal_exposure.py
# tests for person-like names, and an email matches none of its patterns. One
# pin in 91,000 (a New York "Tobacco Retail Dealer" registered under a Gmail
# address).
#
# Enforced HERE, in the shared renderer, rather than in the city's step 2 that
# had the problem: this is the one place every city's pins pass
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
    way a blank one would be; masking would still leak a partial."""
    if "business_name" not in businesses.columns:
        return businesses
    flagged = businesses["business_name"].map(_has_contact_details)
    if int(flagged.sum()):
        print(f"Contact-detail scrub: dropped {int(flagged.sum()):,} row(s) "
              f"whose business name holds an email address or phone number "
              f"(no usable public trade name).")
    return businesses[~flagged]


# Han, kana, Hangul and CJK compatibility/extension ranges: enough to tell that
# a register's names are in a CJK script, not to classify which one.
_CJK_RE = re.compile("[぀-ヿ㐀-䶿一-鿿가-힯豈-﫿\U00020000-\U0002ebef]")


def _require_lang_for_cjk(businesses, lang, city_name):
    """Refuse to render CJK business names without a declared map language.

    Without one, the shared font stack's first CJK face draws every Han
    character, and Hong Kong's signs rendered in Japanese forms until
    2026-09-24. The lesson lived in a skill; this puts it where the next CJK
    city (Taiwan, Seoul, Japan) must pass through it, per osm-rail's rule."""
    if lang is not None or "business_name" not in businesses.columns:
        return
    names = businesses["business_name"].dropna().astype(str)
    n = int(names.map(lambda s: bool(_CJK_RE.search(s))).sum())
    if n:
        raise ValueError(
            f"{city_name}: {n:,} business names contain Chinese, Japanese or "
            f"Korean characters, but render_heatmap() was given no lang. Pass "
            f"lang='zh-HK', 'zh-TW', 'zh-CN', 'ja' or 'ko' so the map's CJK "
            f"faces are ordered for its script - see pipeline/theme.font_stack "
            f"and the cjk-text skill.")


# The basemap credit ODbL requires, linked to OSM's copyright page and opened
# in a new tab (see the TileLayer in render_heatmap).
OSM_ATTRIBUTION = (
    '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" '
    'rel="noopener noreferrer">OpenStreetMap</a> contributors'
)


# THE OPEN BASEMAP (PROTOTYPE, DECISIONS.md 2026-10-07 "Four ideas assessed",
# item 4). tile.openstreetmap.org forbids offline use and CARTO's terms forbid
# caching, so the open choice is Protomaps' OpenStreetMap build (code BSD-3,
# styles CC0, tiles an ODbL produced work) in one PMTiles file per city, read
# by HTTP range request and drawn by MapLibre GL (BSD-3) inside Leaflet
# through maplibre-gl-leaflet (ISC). Its credit is OSM_ATTRIBUTION, carried
# by the outer layer, so it stays in Leaflet's own control and never doubles:
# the GL layer is built with attributionControl false, which makes the
# plugin add nothing. The libraries load only when a reader picks "Travel",
# so the default view costs nothing new. Versions are pinned: maplibre-gl 6
# ships ES modules only, which the plugin cannot read.
OPEN_BASEMAP_LIBS = (
    "https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.0/dist/maplibre-gl.css",
    "https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.0/dist/maplibre-gl.js",
    "https://cdn.jsdelivr.net/npm/@maplibre/maplibre-gl-leaflet@0.1.4/leaflet-maplibre-gl.js",
    "https://cdn.jsdelivr.net/npm/pmtiles@4.5.0/dist/pmtiles.js",
    "https://cdn.jsdelivr.net/npm/@protomaps/basemaps@5.7.2/dist/basemaps.js",
)
# Glyphs and sprites for the Protomaps style. Its own hosted copy for the
# prototype; a release self-hosts them beside the packs.
OPEN_BASEMAP_ASSETS = "https://protomaps.github.io/basemaps-assets"
# The shared Travel style (pipeline/travel_style.js): one file for the site's
# Travel view, the full Travel version and transit-globe's reference, so the
# three never drift apart. Inlined into each OpenBasemap layer.
TRAVEL_STYLE_JS = Path(__file__).with_name("travel_style.js").read_text(encoding="utf-8")
# Ferry and lift colours read from the style itself, so a legend swatch can
# never drift from the line it explains.
_FERRY = re.search(r'var FERRY = \{site: "(#[0-9a-f]{6})", full: "(#[0-9a-f]{6})"', TRAVEL_STYLE_JS)
_AERIAL = re.search(r'var AERIALWAY = \{color: "(#[0-9a-f]{6})"', TRAVEL_STYLE_JS)
if not (_FERRY and _AERIAL):
    raise ValueError("pipeline/travel_style.js: FERRY or AERIALWAY colours not found")
TRAVEL_ROUTE_COLOURS = {"site": {"ferry": _FERRY[1], "aerialway": _AERIAL[1]},
                        "full": {"ferry": _FERRY[2], "aerialway": _AERIAL[1]}}
# Legend rows for the routes, drawn as the map draws them: ferries dashed,
# lifts a thin line with cross ticks. Same row layout as LEGEND_LINE_ROW, but
# not .hm-line-row: these are basemap features, not lines a reader can
# highlight, and the label and coverage checks count .hm-line-row as lines.
TRAVEL_ROUTE_ROWS = {
    "ferry": """
  <div class="hm-route-row" style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:16px; height:3px; margin-right:7px;
      background:repeating-linear-gradient(90deg, {color} 0 5px, transparent 5px 8px);"></span>{label}
  </div>""",
    "aerialway": """
  <div class="hm-route-row" style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:16px; height:9px; margin-right:7px;
      background:linear-gradient({color}, {color}) center / 100% 2px no-repeat,
        repeating-linear-gradient(90deg, {color} 0 1.5px, transparent 1.5px 6px);"></span>{label}
  </div>""",
}


class OpenBasemap(folium.map.Layer):
    """A base layer drawn from one city's PMTiles pack, loaded on first use.

    pmtiles_url: an absolute http(s) URL the browser can range-request.
    local_lang: the city's language as Protomaps names it ("es", "ja"), or
    None. Labels are English by default in every city, falling back to the
    feature's own name where OSM has no English one (owner, 2026-10-08);
    with local_lang set, a small "EN | local" pill under the layer menu (top left),
    shown only while this layer is on, switches them to the local language
    and is remembered. Both come from the same pack, which carries every
    name a feature has, so switching fetches nothing.
    local_name: the pill's text for the local language (default the code
    in capitals).
    variant: "site" (the site's Travel view) or "full" (the full Travel
    version; travel_style.js gives it its own ferry colour). libs and
    assets: the library URLs and the glyph folder, relative to the page or
    absolute; default the pinned CDN copies. pmtiles_url and assets may be
    relative: the script resolves them against the page.
    """

    _template = Template("""
        {% macro script(this, kwargs) %}
        var {{ this.get_name() }} = (function () {
            var LIBS = {{ this.libs|tojson }}, loading = null;
            function load() {
                if (loading) return loading;
                loading = LIBS.reduce(function (p, url) {
                    return p.then(function () {
                        return new Promise(function (ok, fail) {
                            var css = /[.]css$/.test(url);
                            var el = document.createElement(css ? "link" : "script");
                            if (css) { el.rel = "stylesheet"; el.href = url; }
                            else { el.src = url; }
                            el.onload = ok; el.onerror = fail;
                            document.head.appendChild(el);
                        });
                    });
                }, Promise.resolve()).then(function () {
                    var protocol = new pmtiles.Protocol();
                    maplibregl.addProtocol("pmtiles", protocol.tile);
                });
                return loading;
            }
            {{ this.travel_style_js }}
            var LOCAL = {{ this.local_lang|tojson }}, LOCAL_NAME = {{ this.local_name|tojson }};
            var LANG_KEY = "expanded-heatmap-labels";
            function savedLang() {
                try { return localStorage.getItem(LANG_KEY) === "local" && LOCAL ? LOCAL : "en"; }
                catch (e) { return "en"; }
            }
            var lang = savedLang();
            function styleFor(code) {
                return {
                    version: 8,
                    glyphs: new URL({{ this.assets|tojson }}, location.href).href + "/fonts/{fontstack}/{range}.pbf",
                    sources: {protomaps: {
                        type: "vector",
                        url: "pmtiles://" + new URL({{ this.pmtiles_url|tojson }}, location.href).href
                    }},
                    layers: travelStyle(basemaps.layers("protomaps",
                        basemaps.namedFlavor("light"), {lang: code}),
                        {flavor: "light", variant: {{ this.variant|tojson }}, lang: code})
                };
            }
            // The label pill: two buttons in a Leaflet bar stacked under the
            // layer menu (top left; the top right is under the fixed
            // #map-actions buttons, which hid the pill and took its taps,
            // measured 2026-10-08), added and removed with this layer, so the
            // Business view never shows it.
            var PILL_CSS = ".hm-lang{display:flex;overflow:hidden}" +
                ".hm-lang button{border:0;margin:0;padding:0 10px;min-width:40px;height:34px;" +
                "background:#fff;color:#333;font:600 13px/34px var(--hm-font,sans-serif);cursor:pointer}" +
                ".hm-lang button+button{border-left:1px solid #ccc}" +
                ".hm-lang button[aria-pressed=true]{background:#333;color:#fff}" +
                ".dark-base .hm-lang button{background:var(--dm-surface);color:var(--dm-text)}" +
                ".dark-base .hm-lang button+button{border-left-color:var(--dm-border)}" +
                ".dark-base .hm-lang button[aria-pressed=true]{background:var(--dm-text);color:var(--dm-surface)}";
            var Pill = L.Control.extend({
                options: {position: "topleft"},
                onAdd: function () {
                    if (!document.getElementById("hm-lang-css")) {
                        var css = document.createElement("style");
                        css.id = "hm-lang-css"; css.textContent = PILL_CSS;
                        document.head.appendChild(css);
                    }
                    var box = L.DomUtil.create("div", "leaflet-bar hm-lang");
                    box.setAttribute("role", "group");
                    box.setAttribute("aria-label", "Map label language");
                    var self = this;
                    self._buttons = [["en", "EN"], [LOCAL, LOCAL_NAME]].map(function (b) {
                        var btn = L.DomUtil.create("button", "", box);
                        btn.type = "button"; btn.textContent = b[1];
                        btn.setAttribute("data-lang", b[0]);
                        btn.addEventListener("click", function () { self.choose(b[0]); });
                        return btn;
                    });
                    L.DomEvent.disableClickPropagation(box);
                    self.mark();
                    return box;
                },
                mark: function () {
                    (this._buttons || []).forEach(function (btn) {
                        btn.setAttribute("aria-pressed", btn.getAttribute("data-lang") === lang ? "true" : "false");
                    });
                },
                choose: function (code) {
                    if (code === lang) return;
                    lang = code;
                    try { localStorage.setItem(LANG_KEY, code === "en" ? "en" : "local"); } catch (e) {}
                    this.mark();
                    if (layer._gl && layer._gl.getMaplibreMap()) layer._gl.getMaplibreMap().setStyle(styleFor(lang));
                }
            });
            var pill = LOCAL ? new Pill() : null;
            // A zoom range as OSM's tiles give it, registered the way Leaflet's
            // tile layers register theirs (beforeAdd / onRemove): the map takes
            // its maximum zoom only from such layers, and with this one alone
            // Leaflet.markercluster threw "Map has no maxZoom specified" when a
            // pin layer was turned back on (measured 2026-10-07). The GL map
            // overzooms past the pack's own zoom 15.
            var Layer = L.Layer.extend({
                options: {attribution: {{ this.attribution|tojson }}, minZoom: 0, maxZoom: 19},
                beforeAdd: function (map) {
                    if (map._addZoomLimit) map._addZoomLimit(this);
                },
                onAdd: function (map) {
                    var self = this;
                    self._active = true;
                    if (pill) pill.addTo(map);
                    load().then(function () {
                        if (!self._active) return;
                        if (!self._gl) {
                            self._gl = L.maplibreGL({attributionControl: false, style: styleFor(lang)});
                        }
                        self._gl.addTo(map);
                    });
                },
                onRemove: function (map) {
                    this._active = false;
                    if (pill) pill.remove();
                    if (this._gl) map.removeLayer(this._gl);
                    if (map._removeZoomLimit) map._removeZoomLimit(this);
                }
            });
            var layer = new Layer();
            return layer;
        })();
        {% endmacro %}
    """)

    def __init__(self, pmtiles_url, *, name="Travel", local_lang=None, local_name=None, show=False,
                 variant="site", libs=None, assets=None, control=True):
        super().__init__(name=name, overlay=False, control=control, show=show)
        self._name = "OpenBasemap"
        self.pmtiles_url = pmtiles_url
        self.local_lang = local_lang if local_lang and local_lang != "en" else None
        self.local_name = local_name or (self.local_lang or "").upper()
        if variant not in ("site", "full"):
            raise ValueError(f"OpenBasemap variant {variant!r}: 'site' or 'full'")
        self.variant = variant
        self.libs = list(libs or OPEN_BASEMAP_LIBS)
        self.assets = assets or OPEN_BASEMAP_ASSETS
        self.travel_style_js = TRAVEL_STYLE_JS
        self.attribution = OSM_ATTRIBUTION


# THE FULL TRAVEL VERSION (owner, 2026-10-07/08; the drafts log has the
# reasoning). The Travel basemap alone, stations, lines, their legend and the
# OSM credit, with no business data at all; a template for the travel app,
# so map content only. It differs from the site's Travel view in:
#   * no Business base layer, no heat, rings or pins, no business legend;
#   * the page fills its window and loads nothing from outside its own
#     folder when given `lib` (offline);
#   * lines carry casings and stations are white dots with a dark ring,
#     both sized by zoom from FULL_ZOOM_TABLE;
#   * line labels are pills that follow the part of each line in view;
#   * a "Station names" item in the layer menu;
#   * one finger pans the map (no cooperative gestures: the page is the map,
#     with no page around it to scroll).
# Leaflet 1.9.3 (folium 0.20's pin) and the Travel view's own libraries.
FULL_TRAVEL_CDN = {
    "leaflet.js": "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js",
    "leaflet.css": "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css",
}
# OPEN_BASEMAP_LIBS by file name, as they sit in the offline `lib` folder.
FULL_TRAVEL_GL_FILES = ("maplibre-gl.css", "maplibre-gl.js", "leaflet-maplibre-gl.js",
                        "pmtiles.js", "basemaps.js")
# (zoom, station dot radius px, line width px), interpolated between rows; an
# interchange's dot is FULL_INTERCHANGE_STEP px larger, and a casing adds
# FULL_CASING_PX each side. A pilot table, set on screenshots of the densest
# network (Tokyo) in light and dark; the app draws the same idea as a
# MapLibre zoom curve. Touch reach does not shrink with the dot:
# TAP_SELECT_SCRIPT's REACH keeps a 44 px target at every size.
FULL_ZOOM_TABLE = ((10, 2.0, 2.0), (12, 3.0, 3.0), (13, 4.0, 3.5), (14, 5.0, 4.5),
                   (15, 6.0, 5.5), (17, 8.0, 7.0))
FULL_INTERCHANGE_STEP = 1.5
FULL_CASING_PX = 1.5
# The station ring: dark, and deliberately not LIGHT["station"], which the
# site's dark-theme rule recolours.
FULL_DOT_RING = "#222222"
# Layer names the full version may never carry (the owner's hard line,
# 2026-10-07): checked on the written file, so no path can slip one in.
FULL_FORBIDDEN = ("Concentric Ring", "Commercial Density", "Business Category",
                  "markerClusterGroup", "L.heatLayer", "heatLayer(")

FULL_TRAVEL_SCRIPT = """
<style>
.hm-pill-icon { background: none; border: 0; }
.leaflet-container { background: #f2f1ee; }
.dark-base .leaflet-container { background: var(--dm-page); }
.hm-line-pill { position: absolute; left: 0; top: 0; transform: translate(-50%, -50%);
    padding: 1px 8px; border-radius: 999px; border: 1.5px solid #fff;
    font: 700 12px/16px @@FONT@@; white-space: nowrap; cursor: pointer;
    box-shadow: 0 1px 3px rgba(0,0,0,0.35); }
.dark-base .hm-line-pill { border-color: var(--dm-page); }
.hm-line-pill.hm-dim { opacity: 0.35; }
.hm-off { display: none !important; }
.hm-stn-name { position: absolute; left: 0; top: 0; white-space: nowrap; pointer-events: none;
    font: 600 12px/14px @@FONT@@; color: @@TEXT@@;
    text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff, 0 0 4px #fff; }
.dark-base .hm-stn-name { color: var(--dm-text);
    text-shadow: -1px -1px 0 var(--dm-page), 1px -1px 0 var(--dm-page), -1px 1px 0 var(--dm-page),
                 1px 1px 0 var(--dm-page), 0 0 4px var(--dm-page); }
.hm-stn-name.hm-dim { opacity: 0.45; }
.hm-stn-name.hm-hot { color: var(--hm-c-light); }
.dark-base .hm-stn-name.hm-hot { color: var(--hm-c-dark); }
.leaflet-overlay-pane path.hm-casing { stroke: #ffffff; }
.dark-base .leaflet-overlay-pane path.hm-casing { stroke: var(--dm-page); }
.leaflet-overlay-pane path.hm-casing.hm-dim { stroke-opacity: 0.25; }
.dark-base .leaflet-overlay-pane path.hm-line { filter: brightness(1.55) saturate(0.9); }
.leaflet-overlay-pane path.hm-line.hm-hot { stroke-width: var(--hm-hot-w, 7px); }
</style>
<script>
(function () {
    var NAME = "__MAP_NAME__", BASE = "__BASE_NAME__", NAMES = "__NAMES_NAME__";
    var LINES = __LINES__, TABLE = __ZOOM_TABLE__, STEP = __STEP__, CASING = __CASING__;
    var BOUNDS = __BOUNDS__, CREDITS = __CREDITS__;
    var MARGIN = 6;        // px kept clear inside the map's edge
    var MIN_RUN = 40;       // px of a line in view before it earns a label
    var GAP = 3;            // px between any two labels
    var STEP_PX = 16;       // px between the spots a label tries along its line
    var tries = 0;

    function size(z, col) {
        if (z <= TABLE[0][0]) return TABLE[0][col];
        for (var i = 1; i < TABLE.length; i++) {
            if (z <= TABLE[i][0]) {
                var a = TABLE[i - 1], b = TABLE[i], t = (z - a[0]) / (b[0] - a[0]);
                return a[col] + t * (b[col] - a[col]);
            }
        }
        return TABLE[TABLE.length - 1][col];
    }
    function classes(l) {
        var c = l.options && l.options.className;
        return typeof c === "string" ? c.split(" ") : [];
    }
    function suffix(cs, prefix) {
        for (var i = 0; i < cs.length; i++) {
            if (cs[i].indexOf(prefix) === 0 && cs[i].length > prefix.length) return cs[i].slice(prefix.length);
        }
        return null;
    }

    function start() {
        var m = window[NAME], base = BASE ? window[BASE] : null, group = window[NAMES];
        if (!m || (BASE && !base) || !group) {
            if (tries++ < 60) setTimeout(start, 100);
            return;
        }
        if (base && !m.hasLayer(base)) m.addLayer(base);
        // Credits the lines and stations need beside the basemap's own
        // (or in place of it, on a page with no basemap).
        CREDITS.forEach(function (c) { m.attributionControl.addAttribution(c); });
        var el = m.getContainer();
        var polys = {}, casings = {}, dots = [];
        m.eachLayer(function (l) {
            var cs = classes(l), k;
            if (cs.indexOf("hm-line") >= 0 && (k = suffix(cs, "hm-line-")) !== null) {
                (polys[k] = polys[k] || []).push(l);
            } else if ((k = suffix(cs, "hm-casing-")) !== null) {
                (casings[k] = casings[k] || []).push(l);
            } else if (cs.indexOf("hm-stn") >= 0) {
                dots.push({layer: l, xfer: cs.indexOf("hm-xfer") >= 0,
                           on: cs.filter(function (c) { return c.indexOf("hm-on-") === 0; })
                                 .map(function (c) { return c.slice(6); })});
            }
        });
        var byLine = {};
        LINES.forEach(function (ln) { byLine[String(ln.n)] = ln; });

        // One pill per line, moved to the part of its line in view.
        var pills = LINES.map(function (ln) {
            var html = '<div class="hm-line-pill" data-line="' + ln.n + '" style="background:' + ln.bg +
                       ';color:' + ln.fg + '">' + ln.html + '</div>';
            var mk = L.marker(m.getCenter(), {keyboard: false, zIndexOffset: 1000,
                icon: L.divIcon({className: "hm-pill-icon", html: html, iconSize: [0, 0], iconAnchor: [0, 0]})});
            // A pill picks its line, as its legend row does.
            mk.on("click", function () {
                var row = document.querySelector('.map-legend .hm-line-row[data-line="' + ln.n + '"]');
                if (row) row.click();
            });
            return {ln: ln, mk: mk, w: 0, h: 0, at: null};
        });
        function pillEl(p) { return p.mk._icon ? p.mk._icon.firstChild : null; }

        function rectOf(node) {
            var a = node.getBoundingClientRect(), c = el.getBoundingClientRect();
            return {l: a.left - c.left, t: a.top - c.top, r: a.right - c.left, b: a.bottom - c.top};
        }
        function hit(a, b) {
            return a.l < b.r + GAP && a.r > b.l - GAP && a.t < b.b + GAP && a.b > b.t - GAP;
        }
        function hitAny(a, list) {
            for (var i = 0; i < list.length; i++) if (hit(a, list[i])) return true;
            return false;
        }
        function inside(a, s) {
            return a.l >= MARGIN && a.t >= MARGIN && a.r <= s.x - MARGIN && a.b <= s.y - MARGIN;
        }
        function controls() {
            var out = [], nodes = el.querySelectorAll(".leaflet-control");
            for (var i = 0; i < nodes.length; i++) out.push(rectOf(nodes[i]));
            ["map-actions"].forEach(function (id) {
                var n = document.getElementById(id);
                if (n) out.push(rectOf(n));
            });
            var lg = document.querySelector("details.map-legend"), tp = document.querySelector(".hm-tap-panel.hm-shown");
            if (lg) out.push(rectOf(lg));
            if (tp) out.push(rectOf(tp));
            return out.filter(function (r) { return r.r > r.l && r.b > r.t; });
        }

        // The part of line k inside the map, in container pixels, as runs
        // of clipped segments with their distance along the visible part.
        // Projected from the line's own coordinates, not Leaflet's `_parts`:
        // those are re-projected only after `zoomend` and `moveend` have
        // fired (on `viewreset`), so a label placed from them after a zoom
        // landed up to 600 px off its line (Tokyo, measured 2026-10-08).
        function visible(k, s) {
            var box = L.bounds([MARGIN, MARGIN], [s.x - MARGIN, s.y - MARGIN]);
            var view = m.getBounds().pad(0.05);
            var segs = [], total = 0;
            (polys[k] || []).forEach(function (p) {
                if (!view.intersects(p.getBounds())) return;
                var ll = p.getLatLngs();
                (L.LineUtil.isFlat(ll) ? [ll] : ll).forEach(function (run) {
                    var prev = null;
                    run.forEach(function (x) {
                        var b = m.latLngToContainerPoint(x);
                        if (prev) {
                            var c = L.LineUtil.clipSegment(prev, b, box, false, false);
                            var len = c ? c[0].distanceTo(c[1]) : 0;
                            if (len) {
                                segs.push({a: c[0], b: c[1], from: total, len: len});
                                total += len;
                            }
                        }
                        prev = b;
                    });
                });
            });
            return {segs: segs, total: total};
        }
        function along(run, d) {
            for (var i = 0; i < run.segs.length; i++) {
                var g = run.segs[i];
                if (d <= g.from + g.len) {
                    var t = (d - g.from) / g.len;
                    return L.point(g.a.x + t * (g.b.x - g.a.x), g.a.y + t * (g.b.y - g.a.y));
                }
            }
            return null;
        }

        var shown = null;       // the highlighted line, as LINE_HIGHLIGHT_SCRIPT draws it
        function place() {
            var s = m.getSize(), taken = controls(), dotRects = [];
            dots.forEach(function (d) {
                if (!d.layer._map) return;
                var q = m.latLngToContainerPoint(d.layer.getLatLng()), r = d.layer.getRadius() + 2;
                d.q = q; d.r = r;
                dotRects.push({l: q.x - r, t: q.y - r, r: q.x + r, b: q.y + r, dot: d});
            });
            var runs = {};
            pills.forEach(function (p) { runs[p.ln.n] = visible(String(p.ln.n), s); });
            var order = pills.slice().sort(function (a, b) {
                var ha = String(a.ln.n) === shown ? 0 : 1, hb = String(b.ln.n) === shown ? 0 : 1;
                if (ha !== hb) return ha - hb;
                var pa = a.at ? 0 : 1, pb = b.at ? 0 : 1;
                if (pa !== pb) return pa - pb;
                return runs[b.ln.n].total - runs[a.ln.n].total;
            });
            var placed = [];
            order.forEach(function (p) {
                var run = runs[p.ln.n];
                // The picked line always gets its pill while any of it is in
                // view, even zoomed far out (owner, 2026-10-08): it needs no
                // minimum run, and when no clear spot is left it may cover
                // station dots (a second pass below).
                var hot = String(p.ln.n) === shown;
                if (run.total < (hot ? 1 : MIN_RUN)) { hide(p); return; }
                if (!p.mk._map) p.mk.addTo(m);
                var div = pillEl(p);
                div.classList.remove("hm-off");
                p.w = div.offsetWidth; p.h = div.offsetHeight;
                var spots = [];
                // Keep the last spot while it still works, so a pan does not
                // make a label jump along its line.
                if (p.at) spots.push(m.latLngToContainerPoint(p.at));
                // Then every STEP_PX along the part in view, middle first.
                var n = Math.max(1, Math.floor(run.total / STEP_PX)), ds = [];
                for (var j = 0; j <= n; j++) ds.push(j * run.total / n);
                ds.sort(function (a, b) { return Math.abs(a - run.total / 2) - Math.abs(b - run.total / 2); });
                ds.forEach(function (d) { spots.push(along(run, d)); });
                var won = null;
                for (var pass = 0; pass < (hot ? 2 : 1) && !won; pass++) {
                    for (var i = 0; i < spots.length && !won; i++) {
                        var q = spots[i];
                        if (!q) continue;
                        var box = {l: q.x - p.w / 2, t: q.y - p.h / 2, r: q.x + p.w / 2, b: q.y + p.h / 2};
                        if (!inside(box, s) || hitAny(box, taken) || hitAny(box, placed)) continue;
                        if (pass === 0 && hitAny(box, dotRects)) continue;
                        won = {q: q, box: box};
                    }
                }
                if (!won) { hide(p); return; }
                p.at = m.containerPointToLatLng(won.q);
                p.mk.setLatLng(p.at);
                placed.push(won.box);
            });
            names(s, taken.concat(placed), dotRects);
        }
        function hide(p) {
            p.at = null;
            var div = pillEl(p);
            if (div) div.classList.add("hm-off");
        }

        // Station names, when the layer menu has them on: interchanges first,
        // then the highlighted line's stations, each beside its dot on the
        // first side clear of every label, control and other dot.
        function names(s, taken, dotRects) {
            if (!m.hasLayer(group)) return;
            var items = [];
            group.eachLayer(function (mk) {
                var div = mk._icon && mk._icon.firstChild;
                if (!div) return;
                var i = +div.getAttribute("data-stn"), d = dots[i];
                items.push({div: div, d: d, rank: (d && d.xfer ? 0 : 2) -
                            (d && shown !== null && d.on.indexOf(shown) >= 0 ? 1 : 0), i: i});
            });
            items.sort(function (a, b) { return a.rank - b.rank || a.i - b.i; });
            var placed = [];
            items.forEach(function (it) {
                var div = it.div, d = it.d;
                if (!d || !d.q) { div.classList.add("hm-off"); return; }
                div.classList.remove("hm-off");
                div.style.transform = "none";
                var w = div.offsetWidth, h = div.offsetHeight, q = d.q, r = d.r + 1;
                var sides = [
                    [r, -h / 2], [-w - r, -h / 2], [-w / 2, -h - r], [-w / 2, r]
                ];
                var won = null;
                for (var j = 0; j < sides.length && !won; j++) {
                    var box = {l: q.x + sides[j][0], t: q.y + sides[j][1]};
                    box.r = box.l + w; box.b = box.t + h;
                    if (!inside(box, s) || hitAny(box, taken) || hitAny(box, placed)) continue;
                    var blocked = false;
                    for (var k = 0; k < dotRects.length && !blocked; k++) {
                        if (dotRects[k].dot !== d && hit(box, dotRects[k])) blocked = true;
                    }
                    if (!blocked) won = {box: box, dx: sides[j][0], dy: sides[j][1]};
                }
                if (!won) { div.classList.add("hm-off"); return; }
                div.style.transform = "translate(" + won.dx.toFixed(1) + "px," + won.dy.toFixed(1) + "px)";
                placed.push(won.box);
                var on = shown !== null && d.on.indexOf(shown) >= 0;
                div.classList.toggle("hm-hot", on);
                div.classList.toggle("hm-dim", shown !== null && !on);
                if (on) {
                    div.style.setProperty("--hm-c-light", byLine[shown].light);
                    div.style.setProperty("--hm-c-dark", byLine[shown].dark);
                }
            });
        }

        // Sizes by zoom: dots, lines and casings from the table.
        function resize() {
            var z = m.getZoom(), r = size(z, 1), w = size(z, 2);
            el.style.setProperty("--hm-hot-w", (w + 3).toFixed(1) + "px");
            Object.keys(polys).forEach(function (k) {
                polys[k].forEach(function (p) { p.setStyle({weight: w}); });
            });
            Object.keys(casings).forEach(function (k) {
                casings[k].forEach(function (p) { p.setStyle({weight: w + 2 * CASING}); });
            });
            dots.forEach(function (d) { d.layer.setRadius(d.xfer ? r + STEP : r); });
        }

        // The highlight is LINE_HIGHLIGHT_SCRIPT's: it marks the picked
        // line's paths `hm-hot`. Casings, pills and names follow it.
        function follow() {
            var h = null;
            Object.keys(polys).forEach(function (k) {
                if (polys[k].some(function (p) { return p._path && p._path.classList.contains("hm-hot"); })) h = k;
            });
            if (h === shown) return;
            shown = h;
            Object.keys(casings).forEach(function (k) {
                casings[k].forEach(function (p) {
                    if (p._path) p._path.classList.toggle("hm-dim", h !== null && k !== h);
                });
            });
            pills.forEach(function (p) {
                var div = pillEl(p);
                if (!div) return;
                div.classList.toggle("hm-dim", h !== null && String(p.ln.n) !== h);
                // An edited code shows the official one beside it while picked.
                if (p.ln.official) {
                    div.innerHTML = p.ln.html + (String(p.ln.n) === h ? " &middot; signed " + p.ln.official : "");
                }
            });
            place();
        }
        var watch = new MutationObserver(follow);
        Object.keys(polys).forEach(function (k) {
            polys[k].forEach(function (p) {
                if (p._path) watch.observe(p._path, {attributes: true, attributeFilter: ["class"]});
            });
        });

        // Placed on the next frame, once every handler of the move (the
        // renderer's included) has run, and once however many events fired.
        var frame = null;
        function later() {
            if (frame !== null) cancelAnimationFrame(frame);
            frame = requestAnimationFrame(function () { frame = null; place(); });
        }
        m.on("zoomend", function () { resize(); later(); });
        m.on("moveend viewreset overlayadd overlayremove", later);
        window.addEventListener("resize", later);
        var legend = document.querySelector("details.map-legend");
        if (legend) legend.addEventListener("toggle", later);

        // THE CREDIT STAYS UNCOVERED. A line source's credit beside OSM's can
        // wrap to three lines on a phone (Tokyo's, 2026-10-08), so the legend
        // and the tap panel, both fixed 24 px above the bottom, would cover
        // it. Both sit CLEAR px above the credit's top instead, whatever its
        // height; the panel is re-checked whenever its script moves it.
        var CLEAR = 10;
        function creditTop() {
            var a = el.querySelector(".leaflet-control-attribution");
            if (!a) return 24;
            var vh = document.documentElement.clientHeight || window.innerHeight;
            return Math.max(24, Math.ceil(vh - a.getBoundingClientRect().top) + CLEAR);
        }
        // A station tapped on a phone folds an open legend away, so the
        // station's panel gets the room (owner, 2026-10-08, on trial). Safe
        // because taps never pass through the legend: it sits outside the
        // map, and station taps are caught by the map alone.
        var coarse = window.matchMedia ? window.matchMedia("(pointer: coarse)") : null;
        var panelWasShown = false;
        function foldOnTap(panel) {
            var shown = panel.classList.contains("hm-shown");
            if (shown && !panelWasShown && coarse && coarse.matches && legend && legend.open) {
                legend.open = false;
            }
            panelWasShown = shown;
        }
        // And the other way round (owner, 2026-10-08, on trial): opening the
        // legend closes a station's panel, through the panel's own close
        // button so its ring goes too. The side-by-side layout of an open
        // legend and panel stays as the fallback for anything unusual.
        if (legend) legend.addEventListener("toggle", function () {
            if (!legend.open) return;
            var panel = document.querySelector(".hm-tap-panel.hm-shown");
            var close = panel && panel.querySelector(".hm-tap-close");
            if (close) close.click();
        });
        // The panel is made by TAP_SELECT_SCRIPT, which may start after this
        // script, so it is watched from the first time it is found.
        var watched = false;
        function clearCredit() {
            var b = creditTop() + "px";
            if (legend && legend.style.bottom !== b) legend.style.bottom = b;
            // Raised, the legend must also stop below the button row: the
            // shared cap assumes a 24 px bottom, and Tokyo's 52 rows then
            // ran up under Dark mode on a phone (owner, 2026-10-08).
            if (legend) {
                var vh = document.documentElement.clientHeight || window.innerHeight;
                var top = __TOP_CLEAR__;
                var actions = document.getElementById("map-actions");
                if (actions) top = Math.max(top, actions.getBoundingClientRect().bottom + 8);
                var cap = Math.max(80, Math.floor(vh - creditTop() - top)) + "px";
                if (legend.style.maxHeight !== cap) legend.style.maxHeight = cap;
            }
            var panel = document.querySelector(".hm-tap-panel");
            if (!panel) return;
            if (!watched) {
                watched = true;
                new MutationObserver(function () { foldOnTap(panel); clearCredit(); })
                    .observe(panel, {attributes: true, attributeFilter: ["style", "class"]});
            }
            if (panel.style.bottom && panel.style.bottom !== "auto" &&
                parseFloat(panel.style.bottom) < creditTop()) panel.style.bottom = b;
        }
        window.addEventListener("resize", clearCredit);
        m.on("moveend", clearCredit);
        clearCredit();
        setTimeout(clearCredit, 500);
        // Fitted once the map has a size: a page opened in a hidden tab
        // measures 0 x 0 and would fit to the maximum zoom.
        function fit(n) {
            m.invalidateSize(false);
            var s = m.getSize();
            if ((!s.x || !s.y) && n < 150) { setTimeout(function () { fit(n + 1); }, 200); return; }
            m.fitBounds(BOUNDS, {padding: [32, 32], animate: false});
            resize();
            later();
        }
        fit(0);
    }
    start();
})();
</script>
"""


def _station_lines(stations, lines, crs_geographic, crs_projected, reach_m=100.0):
    """{station row position: [line order n, ...]}, for the full version's
    interchange dots and station-name colours. From the stations' own
    `lines` column where it names line keys (187 of 206 cities, 2026-10-08),
    else every line within reach_m of the station, measured in the city's
    projected CRS (never in degrees)."""
    from pyproj import Transformer
    from shapely.geometry import LineString, Point

    order = {key: n for n, key in enumerate(lines)}
    to_m = Transformer.from_crs(crs_geographic, crs_projected, always_xy=True)
    shapes = {}
    for key, (segments, *_rest) in lines.items():
        shapes[key] = [LineString([to_m.transform(lon, lat) for lat, lon in seg])
                       for seg in segments if len(seg) > 1]
    out = {}
    for i, row in enumerate(stations.itertuples()):
        named = getattr(row, "lines", None)
        keys = [k for k in re.split(r"[\s,;|/]+", named) if k in order] if isinstance(named, str) else []
        if not keys:
            p = Point(to_m.transform(row.longitude, row.latitude))
            keys = [k for k, shp in shapes.items() if any(s.distance(p) <= reach_m for s in shp)]
        out[i] = sorted({order[k] for k in keys})
    return out


def _render_full_travel(*, output_path, city_name, system_name, stations, lines,
                        crs_geographic, crs_projected, center, zoom, lang, names,
                        pmtiles_url, local_lang=None, local_name=None, routes=(), lib=None,
                        credits=(), labels=None, colors=None):
    """The full Travel version, for render_heatmap(full_travel=...).

    lib: a folder (relative to the page) holding every library, the glyphs
    (lib/fonts/<fontstack>/<range>.pbf) and nothing else: given, the page
    loads nothing from any other host (checked on the written file).
    Omitted, the pinned CDN copies (for development only).
    pmtiles_url None: no basemap at all, the lines on a plain ground (a test
    page whose city has no pack); the OSM credit is then shown on its own,
    since the stations' English names, at least, come from OSM.
    credits: HTML credits the lines and stations need (a feed's or a
    government layer's), added to the map's credit corner.
    labels: {line key: on-map label} replacing the site's labels here only.
    Every line's label must differ from every other's (owner, 2026-10-08):
    the site gives an operator's lines one code where its station numbering
    does (Tokyo's KS, KK, SI, TS), which the full version does not.
    colors: {line key: hex} replacing the site's drawn colours here only.
    The site moves operators' colours to clear its business pins; the full
    version has none, so it can draw the official colours (owner,
    2026-10-08: as close to official as possible; distinguishing calls
    between an operator's same-coloured lines come later)."""
    if colors:
        lines = {k: (segs, colors.get(k, color), label, end)
                 for k, (segs, color, label, end) in lines.items()}
    # Where a label is edited, the site's own label is the official one (the
    # code on the operator's signs): the legend row and the station details
    # give it alongside, and the line's pill adds it while the line is
    # picked (owner, 2026-10-08), so a rider reading "KK" on the signs is
    # never puzzled by the map's "KKA".
    official = {}
    if labels:
        official = {k: label for k, (_s, _c, label, _e) in lines.items()
                    if labels.get(k, label) != label}
        lines = {k: (segs, color, labels.get(k, label), end)
                 for k, (segs, color, label, end) in lines.items()}
        names = {k: (f"{names.get(k, lines[k][2])} (signed {official[k]})" if k in official
                     else names.get(k)) for k in lines if k in official or k in names}
    seen = {}
    for k, (_segs, _color, label, _end) in lines.items():
        seen.setdefault(label, []).append(k)
    shared = {label: keys for label, keys in seen.items() if len(keys) > 1}
    if shared:
        raise ValueError(f"{city_name}: lines share an on-map label in the full version: {shared}; "
                         f"give each its own with full_travel['labels']")
    pts = [(float(r.latitude), float(r.longitude)) for r in stations.itertuples()]
    c, z = _fit_view(pts)
    center = center or c
    zoom = z if zoom is None else zoom
    m = folium.Map(location=center, zoom_start=zoom, tiles=None, width="100%", height="100%",
                   zoomSnap=0.25)
    # Leaflet only: folium's jQuery, Bootstrap and icon fonts serve nothing
    # this page draws, and each would be a request to another host.
    m.default_js = [("leaflet", f"{lib}/leaflet.js" if lib else FULL_TRAVEL_CDN["leaflet.js"])]
    m.default_css = [("leaflet_css", f"{lib}/leaflet.css" if lib else FULL_TRAVEL_CDN["leaflet.css"])]
    base = OpenBasemap(
        pmtiles_url, local_lang=local_lang, local_name=local_name, show=True, control=False,
        variant="full", libs=[f"{lib}/{f}" for f in FULL_TRAVEL_GL_FILES] if lib else None,
        assets=lib or None,
    ).add_to(m) if pmtiles_url else None
    credits = list(credits) + ([] if base else [OSM_ATTRIBUTION])

    # Casings first, so no casing ever covers another line.
    casing_layer = folium.FeatureGroup(name="Casings", control=False)
    for n, (key, (segments, _color, _label, _end)) in enumerate(lines.items()):
        for segment in segments:
            folium.PolyLine(segment, color="#ffffff", weight=4 + 2 * FULL_CASING_PX, opacity=1,
                            interactive=False, class_name=f"hm-casing hm-casing-{n}").add_to(casing_layer)
    casing_layer.add_to(m)
    for n, (key, (segments, color, label, _end)) in enumerate(lines.items()):
        rail_layer = folium.FeatureGroup(name=f"{system_name}: {names.get(key, label)}", show=True,
                                         control=False)
        for segment in segments:
            folium.PolyLine(segment, color=color, weight=4, opacity=1,
                            class_name=f"hm-line hm-line-{n}").add_to(rail_layer)
        rail_layer.add_to(m)

    on = _station_lines(stations, lines, crs_geographic, crs_projected)
    # A station's tooltip (and its tap panel) lists the lines it serves, each
    # with its swatch and its legend name (owner, 2026-10-08).
    served = []
    for key, (_segments, color, label, _end) in lines.items():
        name = (names[key] if key in names and names[key].startswith(label)
                else f"{label} {names[key]}" if key in names else label)
        served.append(f'<div style="white-space:nowrap"><span style="display:inline-block;width:14px;'
                      f'height:3px;margin-right:6px;vertical-align:middle;background:{color}"></span>'
                      f'{html.escape(name)}</div>')
    station_layer = folium.FeatureGroup(name="Stations", control=False)
    names_layer = folium.FeatureGroup(name="Station names", show=False)
    for i, station in enumerate(stations.itertuples()):
        ns = on.get(i, [])
        where = [round(float(station.latitude), COORD_DP), round(float(station.longitude), COORD_DP)]
        text = html.escape(str(station.station))
        folium.CircleMarker(
            location=where, radius=4, color=FULL_DOT_RING, weight=1.5, opacity=1,
            fill=True, fill_color="#ffffff", fill_opacity=1,
            class_name=" ".join(["hm-stn"] + (["hm-xfer"] if len(ns) > 1 else [])
                                + [f"hm-on-{n}" for n in ns]),
            tooltip=folium.Tooltip(f"<b>{text}</b>" + "".join(served[n] for n in ns), sticky=True),
        ).add_to(station_layer)
        folium.Marker(
            location=where, interactive=False, keyboard=False,
            icon=folium.DivIcon(icon_size=(0, 0), icon_anchor=(0, 0), class_name="hm-pill-icon",
                                html=f'<div class="hm-stn-name hm-off" data-stn="{i}">{text}</div>'),
        ).add_to(names_layer)
    station_layer.add_to(m)
    names_layer.add_to(m)

    dark_labels = dark_label_colours({k: v[1] for k, v in lines.items()}, dark_halo=DARK["page"],
                                     city=city_name)
    pills = []
    for n, (key, (_segments, color, label, _end)) in enumerate(lines.items()):
        light, _halo, dark = label_colours(color, light_halo=LIGHT_LABEL_HALO,
                                           dark_halo=DARK["page"], dark=dark_labels[key])
        fg = "#ffffff" if contrast_ratio(color, "#ffffff") >= contrast_ratio(color, "#111111") else "#111111"
        pills.append({"n": n, "html": html.escape(label), "bg": color, "fg": fg,
                      "light": light, "dark": dark,
                      "official": html.escape(official[key]) if key in official else None})

    m.get_root().html.add_child(folium.Element(
        build_legend((), None, lines, legend_names=names, routes=tuple(routes), full=True)))
    folium.LayerControl(collapsed=True, position="topleft").add_to(m)
    m.get_root().html.add_child(folium.Element(THEME_TOGGLE_HTML))
    for block in (WHEEL_ZOOM_SCRIPT, CREDIT_TAB_SCRIPT, LINE_HIGHLIGHT_SCRIPT, TAP_SELECT_SCRIPT):
        m.get_root().html.add_child(folium.Element(block.replace("__MAP_NAME__", m.get_name())))
    m.get_root().html.add_child(folium.Element(
        FULL_TRAVEL_SCRIPT
        .replace("@@FONT@@", FONT_VAR).replace("@@TEXT@@", LIGHT["text"])
        .replace("__MAP_NAME__", m.get_name())
        .replace("__BASE_NAME__", base.get_name() if base else "")
        .replace("__CREDITS__", json.dumps(credits))
        .replace("__TOP_CLEAR__", str(_LEGEND_TOP_CLEAR))
        .replace("__NAMES_NAME__", names_layer.get_name())
        .replace("__LINES__", json.dumps(pills))
        .replace("__ZOOM_TABLE__", json.dumps(FULL_ZOOM_TABLE))
        .replace("__STEP__", str(FULL_INTERCHANGE_STEP))
        .replace("__CASING__", str(FULL_CASING_PX))
        .replace("__BOUNDS__", json.dumps([[min(p[0] for p in pts), min(p[1] for p in pts)],
                                           [max(p[0] for p in pts), max(p[1] for p in pts)]]))))
    m.get_root().header.add_child(folium.Element(f"<title>{html.escape(city_name)}</title>"))
    if lang is not None:
        m.get_root().header.add_child(folium.Element(
            f"<style>:root {{ --hm-font: {font_stack(lang)}; }}</style>"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    doc = output_path.read_text(encoding="utf-8")
    if lang is not None:
        if "<html>" not in doc:
            raise ValueError(f"{output_path}: no bare <html> tag to give lang={lang!r}")
        doc = doc.replace("<html>", f'<html lang="{lang}">', 1)
        output_path.write_text(doc, encoding="utf-8")
    bad = [w for w in FULL_FORBIDDEN if w in doc]
    if bad:
        output_path.unlink()
        raise ValueError(f"{output_path}: the full version carries {bad}, a business layer (hard line)")
    if lib:
        outside = re.findall(r"""<(?:script|link)[^>]+(?:src|href)=["']?(https?://[^"' >]+)""", doc)
        if outside:
            output_path.unlink()
            raise ValueError(f"{output_path}: offline page loads from another host: {outside}")
    print(f"Wrote {output_path}: full Travel version, {len(stations)} stations, {len(lines)} lines")


_FINGERPRINT_TABLE = Path(__file__).with_name("fingerprint_marks.json")
_fingerprint_cache = {}


def fingerprint_mark(ident):
    """`ehm:v1:<ident>:<check>` from pipeline/fingerprint_marks.json, or None
    when the table has no entry (scripts/fingerprint.py explains the marks)."""
    if not _fingerprint_cache and _FINGERPRINT_TABLE.exists():
        _fingerprint_cache.update(json.loads(_FINGERPRINT_TABLE.read_text(encoding="utf-8")))
    check = _fingerprint_cache.get(ident)
    return f"ehm:v1:{ident}:{check}" if check else None


def render_heatmap(*, output_path, map_title, city_name, system_name,
                   stations, businesses, taxonomy_system, lines,
                   crs_geographic, crs_projected, ring_edges_meters, ring_labels,
                   center=None, zoom=None, label_focus=None, rings_shown=False,
                   all_city_heat=True, animate_clusters=False, lang=None, pins=True,
                   legend_names=None, open_basemap=None, full_travel=None):
    """Render one city's heatmap to a standalone HTML file.

    full_travel: optional dict(pmtiles_url=..., local_lang=..., local_name=...,
    routes=..., lib=...), the FULL Travel version instead (owner,
    2026-10-07/08): the Travel basemap alone, stations, lines and their
    legend, and no business data, so `businesses` must be None and the
    heat, rings, pins and business legend never exist. Map content only;
    it is the travel app's template. See _render_full_travel. A pilot: no
    city's step passes it.

    open_basemap: optional dict(pmtiles_url=..., local_lang=..., local_name=...), a city's
    Protomaps pack (see OpenBasemap). Given, the layer menu offers two base
    layers, "Business" (OSM's tiles, still the default) and "Travel". Omitted,
    the map renders exactly as before. A prototype: no city passes it. Its
    optional routes=[(kind, name)] lists the named ferry and cable-car routes
    the pack holds (from the build's pack summary); each gets a legend row
    under the transit lines with its own name, shown in Travel only.

    legend_names: optional {line key: full public name}, for a city whose
    on-map labels are the operators' LINE CODES (Tokyo's 52 lines, owner
    2026-09-28: full names left 9 labels unplaceable at 1000 px and short names
    59 overlapping pairs at 343 px; the codes place all 52 at both). The line
    spec's label is then the code drawn on the map, and the legend row reads
    "code  full name", so every line keeps a permanent label AND a legend
    entry, and check_map_labels.js still finds each label in the legend. The
    colour checks and layer names use the full name, since one operator may
    give several lines one code (Seibu's SI). Omitted, nothing changes.

    lang: the language the map's own names are written in, as a BCP 47 tag
    ("zh-HK", "zh-TW", "ko", "ja"), or None. It sets <html lang> and orders the
    CJK faces for that script (pipeline/theme.font_stack). Han characters share
    code points across Chinese and Japanese, so without it the first CJK face in
    the stack decides their glyph forms. Hong Kong's signs rendered Japanese.

    stations: DataFrame(station, latitude, longitude). businesses: the
    city's businesses_clean.csv as a DataFrame (needs latitude, longitude,
    business_name and the taxonomy's VALUE_COLUMN). lines: output of
    load_line_shapes. system_name prefixes each line's layer name (e.g.
    "Trolley", "Muni Metro"). label_focus: optional shapely geometry (lon/lat);
    line labels go at the tail ends of the part of each line inside it (see
    _label_anchor_coords); omit only for cities whose whole lines stay in view.
    center/zoom: leave None (the default) to fit the view to the stations and
    every line label together, so all labels are visible on first load; pass
    either to override.

    rings_shown: whether the concentric ring layers start switched on.
    **FALSE for every city since 2026-09-21**: the owner's call, for a cleaner
    first view. The rings stay in the layer control, one click away, and each
    business is still assigned to its NEAREST station whatever the rings show,
    so nothing about the counts depends on this.

    Before that it was True by default, with New York and Miami off on
    measured grounds: New York's 496 stations sit a median 482 m apart and
    Miami's nineteen Metromover stations a median 235 m, so in both the rings
    merged into one indistinct wash downtown. That is why the toggle exists,
    and every city's downtown cluster does some of it. Passing True is still
    supported for a city whose stations are sparse enough to want them on.

    animate_clusters: whether Leaflet.markercluster animates clusters splitting
    and merging at the end of each zoom. **FALSE for every city since
    2026-09-23**: the owner's call, on measurement. The animation runs a
    further ~300 ms after the map's own zoom animation, and turning it off took
    a Paris cluster click from 828 ms to settle to 408 ms (Toulouse 615 to 311)
    and a +/- click from 653 to 384 ms. The map's zoom still animates; the
    clusters simply regroup at the end instead of flying apart. Kept as a
    per-city switch so a light map can have it back; the owner's suggested
    rule is a measured lag threshold, and PLAN.md holds that open item.
    """
    full = full_travel is not None
    names = legend_names or {}
    if full:
        # The hard line (owner, 2026-10-07): the full version carries no
        # business data by any path, so it never reaches this file's HTML.
        if businesses is not None:
            raise ValueError("full_travel draws no business data: pass businesses=None")
        if open_basemap:
            raise ValueError("full_travel and open_basemap are two versions of a map: pass one")
        return _render_full_travel(
            output_path=output_path, city_name=city_name, system_name=system_name,
            stations=stations, lines=lines, crs_geographic=crs_geographic,
            crs_projected=crs_projected, center=center, zoom=zoom, lang=lang,
            names=names, **full_travel)

    taxonomy = load_taxonomy_module(taxonomy_system)
    bucket_colors = dict(CATEGORY_BUCKETS)

    # A line the reader cannot tell from the pins drawn on top of it is not a
    # drawn line. Measured here, at render, because Calgary's Blue Line shipped
    # Delta-E 3.3 from Retail blue (the same colour) and went unnoticed until
    # another city's build first ran the check. Raises only in
    # genuine-duplicate range; agency colours below the preferred figure are
    # reported every render and kept, per the owner's branding decision. See
    # pipeline/linecolour.py for why there are two thresholds.
    check_line_colours(
        {names.get(key, label): color for key, (_coords, color, label, _end) in lines.items()},
        bucket_colors, city=city_name)

    businesses = businesses.dropna(subset=["latitude", "longitude"]).copy()
    businesses = drop_contact_details(businesses)
    _require_lang_for_cjk(businesses, lang, city_name)
    # Stations in a ward with NO business data (a `no_data` column; Tokyo's,
    # owner 2026-09-28) are drawn hollow and get no rings, and no business is
    # counted to them: a business near a ward edge goes to its nearest station
    # WITH data. Ward boundaries cannot be drawn (N03, the Survey Act), so the
    # hollow station is the only place the map says so. A city without the
    # column is unaffected.
    no_data = (stations["no_data"].fillna(False).astype(bool) if "no_data" in stations.columns
               else pd.Series(False, index=stations.index))
    ringed = stations[~no_data] if no_data.any() else stations
    businesses["nearest_station"], businesses["ring_band"] = nearest_station_and_ring(
        businesses, ringed, crs_geographic, crs_projected, ring_edges_meters, ring_labels
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
    # generated script (rings, markers and the layer control never render),
    # with no visible console error. The app pages embed the map at this
    # same fixed size; change them together.
    m = folium.Map(location=center, zoom_start=zoom, tiles=None, width=1000, height=650, zoomSnap=0.25)
    # The credit opens OSM's copyright page in a NEW TAB (owner, 2026-10-03):
    # every map is embedded in an iframe, and openstreetmap.org sends
    # X-Frame-Options: SAMEORIGIN, so a plain link loaded the page inside the
    # map's frame and showed "refused to connect". check_provenance.py
    # requires the target on every map.
    std_base = folium.TileLayer(
        tiles="OpenStreetMap", name="Business" if open_basemap else map_title,
        attr=OSM_ATTRIBUTION,
    ).add_to(m)
    basemap_args = dict(open_basemap or {})
    routes = tuple(basemap_args.pop("routes", ()))
    open_base = OpenBasemap(**basemap_args).add_to(m) if open_basemap else None
    # (JS variable name, shown at render) of every business layer, for
    # TRAVEL_MODE_SCRIPT: the heat layers, the rings and the pins.
    business_layers = []

    # Two heat layers, same tuning, different universe: within-rings is the
    # default; the whole-city one is an opt-in for context.
    heat = ParsedHeatMap(in_rings[["latitude", "longitude"]].round(COORD_DP).values.tolist(),
                         radius=HEAT_RADIUS, blur=HEAT_BLUR, min_opacity=HEAT_MIN_OPACITY,
                         gradient=HEAT_GRADIENT, name="Commercial Density (Within Station Proximity)",
                         show=True).add_to(m)
    business_layers.append((heat.get_name(), True))
    # The whole-city layer is OPT-OUT PER CITY, because it carries one
    # coordinate pair per business in the city and nothing filters it. In most
    # cities that is a modest cost; in Mexico City it is 283,345 pairs against
    # 133,362 in the default layer, and DENUE is an establishment census rather
    # than a licence register, so the gap is structural rather than a quirk.
    # Passing False drops the layer and says so on the city page: the map's
    # own question is density AROUND stations, and this layer is context.
    if all_city_heat:
        heat_all = ParsedHeatMap(businesses[["latitude", "longitude"]].round(COORD_DP).values.tolist(),
                                 radius=HEAT_RADIUS, blur=HEAT_BLUR, min_opacity=HEAT_MIN_OPACITY,
                                 gradient=HEAT_GRADIENT,
                                 name=f"Commercial Density (All {city_name} Businesses)",
                                 show=False).add_to(m)
        business_layers.append((heat_all.get_name(), False))

    for i, label in enumerate(ring_labels):
        layer = folium.FeatureGroup(name=f"Concentric Ring {i + 1}: {label}",
                                    show=rings_shown)
        for _, station in ringed.iterrows():
            folium.Circle(
                location=[round(station["latitude"], COORD_DP),
                          round(station["longitude"], COORD_DP)],
                radius=ring_edges_meters[i + 1],
                # Same LIGHT value the dark-mode selector matches on.
                color=LIGHT["ring"], weight=1, fill=False, opacity=0.5,
            ).add_to(layer)
        layer.add_to(m)
        business_layers.append((layer.get_name(), rings_shown))

    station_layer = folium.FeatureGroup(name="Stations", control=False)
    for _, station in ringed.iterrows():
        folium.CircleMarker(
            location=[round(station["latitude"], COORD_DP),
                      round(station["longitude"], COORD_DP)],
            radius=5, color=LIGHT["station"], fill=True, fill_opacity=0.9,
            tooltip=folium.Tooltip(f"<b>{html.escape(station['station'])}</b>", sticky=True),
        ).add_to(station_layer)
    # Hollow: filled at opacity 0, not unfilled, so the whole disc takes the
    # hover, and the dark-theme rule that recolours a station's stroke AND fill
    # (matched on LIGHT["station"]) leaves it hollow there too.
    for _, station in stations[no_data].iterrows():
        reason = station.get("no_data_reason")
        reason = reason if isinstance(reason, str) and reason else "No business data"
        folium.CircleMarker(
            location=[round(station["latitude"], COORD_DP),
                      round(station["longitude"], COORD_DP)],
            radius=5, color=LIGHT["station"], weight=2, fill=True, fill_opacity=0,
            tooltip=folium.Tooltip(f"<b>{html.escape(station['station'])}</b><br>{html.escape(reason)}",
                                   sticky=True),
        ).add_to(station_layer)

    # Transit lines: always-on context, permanent label + legend entry each
    # (label tips were worked out above, before the map was created).
    # Dark-theme label colours are chosen for the whole city at once, so two
    # different lines never share one; see linecolour.dark_label_colours.
    dark_labels = dark_label_colours({k: v[1] for k, v in lines.items()},
                                     dark_halo=DARK["page"], city=city_name)
    # `n` ties a line's polylines, label and legend row together for
    # LINE_HIGHLIGHT_SCRIPT; build_legend numbers its rows in this same order.
    for n, (key, (segments, color, label, _end)) in enumerate(lines.items()):
        rail_layer = folium.FeatureGroup(name=f"{system_name}: {names.get(key, label)}", show=True, control=False)
        # One polyline per alignment; a branching trunk keeps one label and one
        # legend entry (see load_line_shapes).
        for segment in segments:
            folium.PolyLine(segment, color=color, weight=4, opacity=0.85,
                            class_name=f"hm-line hm-line-{n}").add_to(rail_layer)
        add_line_label(rail_layer, tips[key], label, color, dark=dark_labels[key], line=n)
        rail_layer.add_to(m)
    # Stations after the lines, so they draw above them: a mouse over a
    # station's centre now finds the station, not the line through it (0 of 6
    # on Paris and Tokyo before; owner, 2026-10-04).
    station_layer.add_to(m)

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
        # pins=False draws no business dots at all; the legend then lists only
        # lines. Added for "mobile mode" (2026-09-25), which was retired
        # 2026-09-27: the blank phone maps were WebKit refusing a large
        # literal, not memory, and the JSON.parse data fixed them. No city
        # passes it now; it stays as an option.
        if pins and add_pin_layer(m, rows, layer_label(name), color, taxonomy.FIELD_LABEL,
                         taxonomy.VALUE_COLUMN,
                         display=getattr(taxonomy, "display_value", None),
                         animate=animate_clusters, registry=business_layers):
            present.append((name, color))

    m.get_root().html.add_child(folium.Element(
        build_legend(present, taxonomy.legend_label, lines, no_data_stations=bool(no_data.any()),
                     legend_names=names, travel=bool(open_basemap), routes=routes)
    ))

    # Collapsed by default: many toggleable layers would otherwise cover a
    # large share of the map. Top-left, not Leaflet's top-right default:
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
        # off a narrow frame: only 2 of San Francisco's 6 and 4 of Los Angeles'
        # 6 were visible at 375px when this fitted stations only.
        # `_choose_view` already fits the desktop view to stations and labels
        # together; this matches it.
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
    # A map that needed labels standing in the wide tier on the desktop gets
    # the wider phone placer too, and only such a map, so no other changes.
    # See DENSE_LABEL_SCRIPT.
    if any(_clearance(t) in _LABEL_WIDE_CLEARANCES for t in tips.values()):
        m.get_root().html.add_child(folium.Element(
            DENSE_LABEL_SCRIPT.replace("__MAP_NAME__", m.get_name())
            .replace("__LABEL_REACH__", f"{max(_LABEL_WIDE_CLEARANCES):g}")))
    # Mouse-wheel zoom that neither drops notches nor moves less than a click.
    # See WHEEL_ZOOM_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        WHEEL_ZOOM_SCRIPT.replace("__MAP_NAME__", m.get_name())))
    # Leaflet's own credit opens in a new tab. See CREDIT_TAB_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        CREDIT_TAB_SCRIPT.replace("__MAP_NAME__", m.get_name())))
    # A line's legend row, or the line itself, picks it out above the others.
    # See LINE_HIGHLIGHT_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        LINE_HIGHLIGHT_SCRIPT.replace("__MAP_NAME__", m.get_name())))
    # The half travel version: Travel takes the business layers off the map.
    # See TRAVEL_MODE_SCRIPT.
    if open_base is not None:
        m.get_root().html.add_child(folium.Element(
            TRAVEL_MODE_SCRIPT.replace("__MAP_NAME__", m.get_name())
            .replace("__STD_NAME__", std_base.get_name())
            .replace("__OPEN_NAME__", open_base.get_name())
            .replace("__BUSINESS__", json.dumps([[n, bool(s)] for n, s in business_layers]))))
    # On a touch screen one finger scrolls the page and two move the map.
    # See TOUCH_GESTURE_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        TOUCH_GESTURE_SCRIPT.replace("__MAP_NAME__", m.get_name())))
    # On a touch screen a tap selects the nearest dot, station, cluster or
    # line within reach, and a dot's details go in a fixed panel.
    # See TAP_SELECT_SCRIPT.
    m.get_root().html.add_child(folium.Element(
        TAP_SELECT_SCRIPT.replace("__MAP_NAME__", m.get_name())))

    # A declared language: its font order on --hm-font, which every shared
    # block reads through theme.FONT_VAR, so the shared blocks stay identical.
    if lang is not None:
        m.get_root().header.add_child(folium.Element(
            f"<style>:root {{ --hm-font: {font_stack(lang)}; }}</style>"))

    # The authorship mark (scripts/fingerprint.py; owner, 2026-10-04):
    # metadata only, never visible, read from the committed table, so no key
    # is needed to render. A map with no table entry renders unmarked and
    # `fingerprint.py coverage` fails it.
    mark = fingerprint_mark(f"map/{output_path.parent.name}")
    if mark:
        m.get_root().header.add_child(folium.Element(
            f'<meta name="generator" content="expanded-heatmap ehm:v1">\n<!-- {mark} -->'))
        m.get_root().html.add_child(folium.Element(f'<div hidden data-ehm="{mark}"></div>'))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    if lang is not None:
        # folium's template has no slot for it, so it goes in after saving.
        # lang also lets a browser choose the right system fallback face for
        # any character no listed face carries.
        doc = output_path.read_text(encoding="utf-8")
        if "<html>" not in doc:
            raise ValueError(f"{output_path}: no bare <html> tag to give lang={lang!r}")
        output_path.write_text(doc.replace("<html>", f'<html lang="{lang}">', 1), encoding="utf-8")
    print(f"Wrote {output_path}")
    if all_city_heat:
        print(f"{len(in_rings):,} points plotted (within-ring default) / "
              f"{len(businesses):,} available (all-{city_name} toggle), "
              f"across {len(stations)} stations")
    else:
        # Do not advertise a toggle that was not built. This line once said
        # "283,345 available (all-Mexico City toggle)" after the layer was
        # dropped: the stale-prose failure this project greps city pages for.
        print(f"{len(in_rings):,} points plotted (within-ring), across "
              f"{len(stations)} stations. The all-{city_name} heat layer is "
              f"OFF for this city ({len(businesses):,} businesses not drawn).")
