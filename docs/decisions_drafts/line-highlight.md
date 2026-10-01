# DECISIONS drafts - branch `line-highlight` (line highlight build agent)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - A line's legend row, or the line itself, picks it out above the others

**The problem** (owner, 2026-09-30, from the live site on an iPhone): where
lines share track, the one drawn last hides the others completely - Daugavpils'
line 2 under the purple, Göteborg's 4/9 and 6/7/11, Reims' T1 under T2, Brest's
téléphérique, every Saint-Étienne tram, Nice's T2, Strasbourg's A, Liberec's 5,
Most's 1. **The owner chose** a highlight, with striping shared track left for
later where this is not enough.

**Built** once, in `pipeline/map_common.py`: a new shared block,
`LINE_HIGHLIGHT_SCRIPT` (one `<style>` and one `<script>`), plus three markers
the renderer now writes - each line's polylines carry the class
`hm-line hm-line-<n>`, its label and its legend row `data-line="<n>"`, where
`n` is the line's order in `render_heatmap()`. Tapping a legend row, or the map
within reach of a line, draws that whole line on top at 7 px and full opacity
and fades every other line to a quarter; tapping it again, empty map, or
Escape restores, and another line switches. A mouse hovering a line or a row
previews the same, and a click still toggles. City `step3_map.py` files are
untouched. Rendered for Reims, Göteborg, Saint-Étienne, Most and Madrid only;
the other 119 maps wait for the full re-render, and `check_render_current.py`
names each of them for `LINE_HIGHLIGHT_SCRIPT` alone until then.

Judgment calls inside the owner's design, each proposed for review time:

- **The picked line goes above the other lines, not above everything.** Its
  paths move to the end of the run of line paths in the SVG, so business dots
  (drawn after the lines) still sit on top of it and stations stay where they
  were. Heat layer, dots, stations, rings and the attribution are untouched.
- **Nothing is redrawn.** A state is two CSS classes on the paths plus that
  reorder. CSS `stroke-width` overrides the SVG attribute, so the dark theme's
  `path[stroke-width="4"]` brightening still applies to a thickened line
  (measured: `brightness(1.55) saturate(0.9)` on the picked Madrid line).
- **A map tap is matched by distance, not by what the finger hit**: within
  16 px on a coarse pointer, 7 px on a mouse, measured against Leaflet's own
  clipped `_parts` as its `_containsPoint` does. A 4 px line is too thin to
  tap, and a hidden line is never what was hit. Where two lines are equally
  near (shared track), the one currently on top wins, so a second tap on a
  picked line restores rather than switching to the line under it - which is
  why a fully hidden line is reached through the legend. A tap on a business
  dot, station or ring is left alone.
- **Hover only where a fine pointer can hover** (`(hover: hover) and
  (pointer: fine)`), with an 80 ms grace before a hover ends so moving between
  touching lines does not flash the map back to normal.
- **Labels stay as they are**; the picked line's label is lifted above the
  others (z-index 1500 against 1000). Other labels are not faded.
- **The legend's layout does not change.** The picked row gets a tint and a
  doubled swatch (`transform`), the other line rows drop to 0.6 opacity, and no
  text goes bold - a bolder row can widen the legend, which `_layout_labels`
  models at a fixed width. Rows are `role="button"` with `aria-pressed` and
  answer Enter and Space. The legend's open or collapsed state is never
  touched.

**Verified** in the browser pane at 1280, 375 and 343 px, light and dark, on
all five maps: every legend row highlights its whole line on top (its paths
last in the line run, only its paths thick, every other line faded) and a
second tap restores the original order; real taps restored on empty map and
picked Göteborg's Tram 8 from 9 px off its line; desktop hover on Madrid's
Línea 10 in dark mode. `check_map_labels.js` and `check_map_attribution.js`
PROBLEMS 0 on every map at every width; `check_map_markup.py` PROBLEMS 0;
`check_inline_arrays.py` 0 over the cap; `check_all.py` 28 of 29, the one
failure being `check_render_current.py` on the 119 maps not re-rendered, each
for `LINE_HIGHLIGHT_SCRIPT is MISSING` and nothing else.
