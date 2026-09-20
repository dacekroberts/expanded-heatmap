# Dark Mode for the city heatmaps and the macro map - implementation notes

A proposal, not a decision: nothing here has been applied or verified in this
repo. It describes a way to add a Dark Mode toggle to `pipeline/map_common.py`'s
`render_heatmap()` (shared by every city, so it is implemented once) and to the
macro map. Log the go/no-go, the toggle placement and the palette choice in
`DECISIONS.md` when they are made.

## Scope

- **Every city map and the macro map** get a Dark Mode, and **every UI element
  is recoloured** on it: legend, zoom buttons, layer control, attribution, hover
  tooltips, ring outlines, and (for the macro map) markers, labels and tooltip.
- **The toggle** is either a base-map radio in the Leaflet layer control (the
  mechanism below) or a separate button in the top-right of the map UI. Open
  question; the trade-offs are for a decision before building.
- The macro map is a pydeck map, not Leaflet: the CSS mechanism below does not
  apply to it. Carto's public basemap (already used there) has a `dark` style,
  so its Dark Mode is a basemap style plus recoloured markers and labels, not a
  CSS filter.
- Not decided: whether the choice persists between maps and pages, and whether
  the surrounding Streamlit page also goes dark (it stays light/teal today).

## What it does (city maps)

The Leaflet layer control gets a second **base map** radio option: "Light Mode"
(default, today's map) and "Dark Mode". Dark Mode is the same OpenStreetMap
tiles recoloured in the browser by a CSS filter. No new tile provider and no
API key (CartoDB and other dark raster styles were ruled out on
keys/licensing). Rings, heat, pins and lines are overlays in other panes, so
the filter does not touch them. While Dark Mode is on, a `dark-base` class on
`<body>` restyles the map chrome (legend, zoom buttons, layer control,
attribution, hover tooltip) and lightens the ring outlines. As written it is
not persisted: every visitor starts on Light.

## How the mechanism works (read this before copying)

1. **Second base layer with a class.** `folium.TileLayer(..., class_name="dark-osm-tiles", show=False)`.
   Folium 0.20 turns `class_name` into Leaflet's `className` option, which
   lands on that layer's tile container, so the filter hits only its tiles.
   Two base layers make Leaflet render radios automatically.
2. **CSS filter** on `.dark-osm-tiles`: `invert(1) hue-rotate(180deg)`
   flips light to dark while `hue-rotate` undoes the colour inversion (water
   stays blue, not orange); brightness/contrast/saturate tame the glare.
3. **`baselayerchange` handler** toggles `dark-base` on `document.body`, not
   on the Leaflet container. Reason: the legend is appended to the page
   outside the map container, so a container class would not reach it.
4. **The handler must be a `folium.MacroElement`**, not a bare
   `folium.Element` on `get_root().script`. A bare script Element renders
   *above* `var map_xxx = L.map(...)`, so `map_xxx.on(...)` throws
   `ReferenceError` and the map silently loses the toggle. The MacroElement's
   `script` macro renders after the map exists.
5. **`!important` on the legend rules**, because its light styling is inline
   (`background: white; border: 1px solid #999`).
6. **Ring outlines** are the only stroke `#2c3e50` (`map_common.py` ~line
   544), so `path.leaflet-interactive[stroke="#2c3e50"]` targets them and
   nothing else. That colour is invisible on dark tiles.
7. The layer-control toggle icon is a dark-on-white image; `filter: invert(1)`
   fixes it. `color-scheme: dark` on the expanded control darkens its
   scrollbar.

## Things to adapt in this repo

- **Legend is a `<details>`, not a `<div>`.** Add `class="map-legend"` to
  the `<details ...>` in `LEGEND_HTML` (line ~37). The `<summary>` inherits
  the colour, so no separate rule is needed.
- **The site theme is light/teal.** The dark palette should suit it; the values
  below are suggestions tinted toward teal, and substitute freely. Everything is
  a CSS variable, so the palette lives in one block.
- **Base layer naming.** Here the base layer is named `map_title`
  (`folium.TileLayer(tiles="OpenStreetMap", name=map_title)`). Decide whether to
  replace that label with "Light Mode" / "Dark Mode" (simple, unambiguous) or
  keep `map_title` for the light option and use e.g. `f"{map_title} (dark)"`. If
  you rename, keep the name in one constant so the JS check cannot drift
  from it.
- **Each city has its own committed `outputs/<city>/heatmap.html`.** The
  change is in the shared renderer, but every city's map must be
  regenerated to pick it up (Folium's random ids make the HTML diff noisy;
  that is cosmetic).
- **Transit line colours are real brand colours** and vary per city (e.g.
  dark blue/purple lines). Check each on the dark base; a few may need a
  lighter variant while Dark Mode is on (a `.dark-base path[stroke="#..."]`
  override per colour, or skip if legible).
- **Station dots are `#1a5490`** (dark blue, line ~552) and the on-map line
  labels use a white text-shadow halo (`add_line_label`). Station dots on dark
  tiles should be eyeballed, and a lighter dot stroke may help; the label halo
  needs a dark variant.
- **The surrounding Streamlit page stays light** unless it is included in
  the scope above. Dark Mode restyles only the map iframe, so expect a dark
  rectangle on a light page.
- **`requirements.txt` is untouched.** `jinja2` (for `Template`) ships with
  folium and this is pipeline-only code, so nothing changes for the deploy.

## The code

### 1. Import (top of `map_common.py`)

```python
from jinja2 import Template
```

### 2. Legend gets a class (`LEGEND_HTML`)

```python
<details open class="map-legend" style="
    position: fixed; ...
```

### 3. Second base layer (in `render_heatmap`, right after the first `TileLayer`)

```python
folium.TileLayer(tiles="OpenStreetMap", name=LIGHT_MODE_NAME).add_to(m)  # was name=map_title
folium.TileLayer(
    tiles="OpenStreetMap",
    name=DARK_MODE_NAME,
    class_name="dark-osm-tiles",
    show=False,
).add_to(m)
```

with module constants `LIGHT_MODE_NAME = "Light Mode"` and
`DARK_MODE_NAME = "Dark Mode"` (or whatever you decide above).

### 4. CSS (extend the existing `<style>` that already holds
`.leaflet-control-layers-expanded`)

Palette variables are suggestions; the *structure* is what carries over.

```css
.dark-osm-tiles {
    filter: invert(1) hue-rotate(180deg) brightness(0.85)
            contrast(0.9) saturate(0.7);
}
.dark-base {
    --dm-page: #0f1716;          /* body behind the map */
    --dm-surface: #182322;       /* legend, controls, tooltip */
    --dm-surface-hover: #1f2d2c;
    --dm-surface-disabled: #131c1b;
    --dm-border: #2e403e;
    --dm-text: #e6efee;
    --dm-muted: #8fa3a1;
    --dm-disabled-text: #4a5b59;
    --dm-accent: #5eead4;        /* attribution links */
    --dm-ring: #cfe0de;          /* ring outlines */
    background: var(--dm-page);
}
.dark-base path.leaflet-interactive[stroke="#2c3e50"] { stroke: var(--dm-ring); }
.dark-base .map-legend {
    background: var(--dm-surface) !important;
    color: var(--dm-text) !important;
    border-color: var(--dm-border) !important;
}
.dark-base .leaflet-bar,
.dark-base .leaflet-control-layers {
    border: 1px solid var(--dm-border);
    box-shadow: none;
}
.dark-base .leaflet-bar a,
.dark-base .leaflet-control-layers {
    background-color: var(--dm-surface);
    color: var(--dm-text);
}
.dark-base .leaflet-bar a { border-bottom-color: var(--dm-border); }
.dark-base .leaflet-bar a:hover,
.dark-base .leaflet-bar a:focus { background-color: var(--dm-surface-hover); }
.dark-base .leaflet-bar a.leaflet-disabled {
    background-color: var(--dm-surface-disabled);
    color: var(--dm-disabled-text);
}
.dark-base .leaflet-control-layers-toggle { filter: invert(1); }
.dark-base .leaflet-control-layers-expanded { color-scheme: dark; }
.dark-base .leaflet-control-layers-separator { border-top-color: var(--dm-border); }
.dark-base .leaflet-control-attribution {
    background: rgba(15, 23, 22, 0.8);
    color: var(--dm-muted);
}
.dark-base .leaflet-control-attribution a { color: var(--dm-accent); }
.dark-base .leaflet-tooltip {
    background: var(--dm-surface);
    color: var(--dm-text);
    border-color: var(--dm-border);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.5);
}
.dark-base .leaflet-tooltip-top:before    { border-top-color: var(--dm-border); }
.dark-base .leaflet-tooltip-bottom:before { border-bottom-color: var(--dm-border); }
.dark-base .leaflet-tooltip-left:before   { border-left-color: var(--dm-border); }
.dark-base .leaflet-tooltip-right:before  { border-right-color: var(--dm-border); }
```

Variables make retheming a one-block edit.

### 5. The toggle handler (after the `<style>` Element, before `m.save`)

```python
dark_toggle = folium.MacroElement()
dark_toggle._template = Template("""
    {% macro script(this, kwargs) %}
        {{ this._parent.get_name() }}.on('baselayerchange', function (e) {
            document.body.classList.toggle('dark-base', e.name === __DARK_NAME__);
        });
    {% endmacro %}
""".replace("__DARK_NAME__", json.dumps(DARK_MODE_NAME)))
m.add_child(dark_toggle)
```

(Needs `import json`. Hardcoding `'Dark Mode'` in the JS would let it drift from
the constant, so it is filled in with `.replace`, not `%` formatting: the
template contains literal `{% ... %}` tags that `%` formatting would choke on.)

## If the toggle is a separate top-right button instead

A Leaflet custom control (`L.Control` at `topright`) holding a button that
toggles the same `dark-base` class on `<body>` and swaps the tile layer's
visibility. Trade-offs to weigh before choosing: a button is more discoverable
than a radio inside a collapsed layer control, and one button style can be
shared with the macro map; but it is more code than the built-in radios, needs
its own dark styling, and has to keep the tile layer and the class in step
(the radio approach gets that for free from Leaflet).

## Verify

Use the `deploy-verify` agent per CLAUDE.md, plus these map-specific checks
in the embedded iframe (`document.querySelector('iframe').contentDocument`):

1. Layer control lists exactly two base radios, Light selected by default;
   overlay list and defaults unchanged from before.
2. Click the Dark radio: `document.body.classList.contains('dark-base')` is
   `true` and `.dark-osm-tiles` exists in the tile pane. Click Light: both
   revert, and computed styles for `.map-legend`, `.leaflet-bar a`,
   `.leaflet-control-layers` are white again and a ring path's computed
   stroke is back to `rgb(44, 62, 80)`.
3. Screenshot each city's Dark Mode with the layer control expanded (add
   class `leaflet-control-layers-expanded` to `.leaflet-control-layers`
   via JS) and with the legend visible.
4. Tooltips are hard to trigger (pins only render at high zoom), so
   inject a synthetic one to check styling:
   `pane.innerHTML='<div class="leaflet-tooltip leaflet-tooltip-right" style="left:400px;top:250px;opacity:1"><b>Test</b></div>'`
   in `.leaflet-tooltip-pane`, then read computed styles.
5. Check the heat layer (Reds gradient here) reads well on the dark base,
   every city's line colours are legible, and station dots (`#1a5490`) are
   visible.
6. The macro map: Dark Mode basemap, marker and label contrast, tooltip
   styling, and that the click-to-open behaviour still works.
7. Console: only Streamlit's `_stcore/health` and `host-config` 404s when
   previewing at a `/Page` path are expected; those are unrelated.

Regenerate all city maps, commit per the "commit after each green step" rule,
and remember `outputs/<city>/heatmap.html` is committed.

## Copy to update

The Heatmap page prose says features are "toggleable via the layer control in
the top left". Whether to mention Dark Mode there (and on which pages) is a
copy decision (draft it in chat first per CLAUDE.md), not part of the
implementation.
