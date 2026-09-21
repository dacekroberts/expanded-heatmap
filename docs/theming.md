# Theming

One document for how this project is themed: what exists, what was decided and
why, what is left to build, and the traps that cost time. It replaces
`dark_mode_handoff.md` and `midnight_slate_theme_handoff.md`, merged
2026-09-21 — two overlapping handoffs describing the same surface was the same
two-sources-of-truth problem that left San Francisco's boundary endpoint
recorded nowhere.

Sections are ordered by usefulness: current state first, superseded designs
last. Anything under "Superseded" is provenance, not instructions.

---

## Current state — implemented

**City maps and the macro map have dark mode. The surrounding Streamlit page
does not.**

- **The toggle** is a plain fixed-position button at the map's top right, part
  of the `#map-actions` group alongside "All cities" and the Cities dropdown.
  Not a Leaflet control — see Superseded for why the base-layer radio lost.
- **The dark basemap is one CSS filter** on the tile pane:
  `invert(1) hue-rotate(180deg) brightness(0.85) contrast(0.9) saturate(0.7)`.
  The `hue-rotate` is what keeps water blue rather than orange after the
  invert. No second tile provider and no API key — dark raster styles were
  ruled out on keys and licensing.
- **`dark-base` goes on `<body>`, not the Leaflet container**, because the
  legend is appended outside the map container and a container class would
  never reach it.
- **The choice persists** in `localStorage` under one key,
  `expanded-heatmap-theme`, shared by the app page and every same-origin map
  iframe — so dark carries from map to map and from the Overview into a city.
- **With no stored choice, a map follows the page it is embedded in**, so a map
  never opens as a white rectangle on a dark page. An explicit click wins from
  then on. A standalone map (served from `outputs/`, no host page) follows the
  OS `prefers-color-scheme` instead. The rule lives once, in
  `AMBIENT_THEME_JS` (`pipeline/theme.py`), used by both the city maps and the
  macro map.
  **Why it reads a background colour rather than asking Streamlit:** Streamlit
  exposes no theme signal at all — no `data-theme` on `<html>` or `<body>`, no
  CSS custom property (checked 2026-09-21). But the page background reflects
  whichever of System / Light / Dark the visitor picked, and a map iframe is
  same-origin with its host, so reading it detects all three.
  `prefers-color-scheme` alone would only match the default System case and
  would be wrong the moment someone chose Light or Dark explicitly.
- **The palette is eleven CSS variables** in a single block on `.dark-base` in
  `THEME_TOGGLE_HTML` (`pipeline/map_common.py`). Retheming is a one-block
  edit, by design.

| Variable | Current (teal-slate) | Drives |
|---|---|---|
| `--dm-page` | `#0f1716` | body behind the map |
| `--dm-surface` | `#182322` | legend, controls, tooltip |
| `--dm-surface-hover` | `#1f2d2c` | control hover |
| `--dm-surface-disabled` | `#131c1b` | disabled zoom button |
| `--dm-border` | `#2e403e` | all chrome borders |
| `--dm-text` | `#e6efee` | chrome text |
| `--dm-muted` | `#8fa3a1` | attribution |
| `--dm-disabled-text` | `#4a5b59` | disabled zoom button text |
| `--dm-accent` | `#5eead4` | attribution links |
| `--dm-ring` | `#cfe0de` | concentric ring outlines |
| `--dm-station` | `#7cc0ff` | station dots |

### Two asymmetries to know before retheming

1. **Light values are hardcoded, dark values are variables.** `.map-btn` carries
   `background: #fff; color: #1c2b2a; border: 1px solid #999` literally, and
   the legend's light styling is inline in `LEGEND_HTML` (which is why the dark
   rules need `!important`). A *dark* reskin is a one-block edit; changing the
   **light** look means lifting those into variables first.
2. **The palette drives only the chrome — about 15% of a city page's pixels.**
   Measured 2026-09-21 by rendering a candidate palette and comparing against
   the current one from an identical view. The map body barely changes, for
   structural reasons: the basemap is produced by a CSS *filter* that no
   variable touches, and pin and line colours are fixed category and transit
   brand values held deliberately outside the theme. **This is why a
   map-chrome-only reskin is not worth doing on its own.**

---

## Decided 2026-09-21 — midnight slate, as one palette

Full reasoning and the rejected alternatives are in `DECISIONS.md`. In short:

- **Stay on Streamlit.** The apparent blocker was that an explicit `[theme]`
  block forces the site dark-only; separate `[theme.light]` and `[theme.dark]`
  blocks keep the toggle (tested, not assumed). Replacing Streamlit with a
  static site was considered and rejected *for now* — the coupling is small and
  one-directional, so going static later costs no more than going static now.
- **Page and map ship together, page first.** They come from one palette, and a
  map surface can only be judged against the page behind it.

### The palette

Cool blue-navy chrome, leaving the data colours to carry the accent. Every
contrast figure below was recomputed rather than taken on trust, and matched to
the stated decimal.

| Role | Hex | vs page `#0B1220` |
|---|---|---|
| Page background | `#0B1220` | — |
| Surface | `#131C2E` | — |
| Border | `#23304A` | 1.4:1 (decorative only) |
| Body text | `#E6EDF7` | 15.9:1 (14.5 on surface) |
| Muted text | `#8B9AB5` | 6.6:1 (6.0 on surface) |
| Link | `#7CB7FF` | 9.0:1 (8.2 on surface) |
| **Accent — keep our teal** `#5eead4` | | **12.7:1** (11.5 on surface) |

Draft `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
primaryColor = "#2dd4bf"            # teal, lightened for dark
backgroundColor = "#0B1220"
secondaryBackgroundColor = "#131C2E"
textColor = "#E6EDF7"
linkColor = "#7CB7FF"
borderColor = "#23304A"
```

Use `[theme.light]` and `[theme.dark]` blocks instead of a bare `[theme]` if
the light/dark toggle is to survive.

Matching `--dm-*` values:

| Variable | Slate |
|---|---|
| `--dm-page` | `#0B1220` |
| `--dm-surface` | `#131C2E` |
| `--dm-surface-hover` | `#1A2740` |
| `--dm-surface-disabled` | `#0F1626` |
| `--dm-border` | `#23304A` |
| `--dm-text` | `#E6EDF7` |
| `--dm-muted` | `#8B9AB5` |
| `--dm-disabled-text` | **`#5A6B8C`** — not the originally suggested `#4A5A78` |
| `--dm-accent` | `#5eead4` (keep the teal) |
| `--dm-ring` | `#C9D6EA` |
| `--dm-station` | `#7cc0ff` (already blue; suits slate) |

**Two deliberate deviations from the source palette, both measured:**

- **Accent stays teal.** The original `#4C9AFF` is described by its own author
  as a placeholder that "reads as another project's look."
- **`--dm-disabled-text` is not `#4A5A78`**, which measures 2.7:1 on page and
  2.5:1 on surface — below the 3:1 non-text floor. It was one of four values
  marked "(suggested)" rather than designed, so the source's own caveat flagged
  the right one.

---

## Not yet built

Done 2026-09-21: `.streamlit/config.toml` with both blocks, the `--dm-*` swap,
the shared palette module, and ambient-following with a manual override.
Remaining:

1. **The hardcoded-colour sweep — the real work, and only partly done.**
   `app/components.py` is clean (it now builds from `pipeline/theme.py`), but
   `app/Overview_&_Introduction.py` still has literal `white` and `#1c2b2a`
   for the macro map's markers and labels. Check those numerically against
   `#0B1220` rather than by eye: doing this once elsewhere produced a label at
   **1.01:1** — invisible, and nobody caught it by looking — and icons at
   **2.77:1**, below the 3:1 non-text minimum.
2. The city pages' prose says features are "toggleable via the layer control in
   the top left" — decide whether to mention the theme toggle, and draft the
   wording in chat first per `CLAUDE.md`.
3. Consider whether the light palette in `pipeline/theme.py` should drive
   `[theme.light]` more closely; today only the four Streamlit keys are
   checked against it by `scripts/check_theme_sync.py`.

---

## Traps that cost time

Each of these was paid for once already.

**Streamlit**

- An explicit `[theme]` block **removes** Streamlit's built-in light/dark
  toggle, making the site dark-only. Separate `[theme.light]` and
  `[theme.dark]` blocks bring it back.
- `st.dataframe` is canvas-rendered: header styling cannot be set from CSS, it
  follows the theme's own colours only.
- Theme keys are version-dependent (`borderColor`, fonts, radii, chart
  palettes). These notes come from 1.64, which is what `requirements.txt`
  pins as `>=1.64,<2`.
- A theme change needs **no new dependency**. Do not add one.

**Embedded maps**

- A map iframe is a separate document. A light map on a dark page is a white
  box. Already handled here — the maps theme themselves and share the
  `localStorage` key — but it is the first thing to break if that link is cut.
- **Script ordering inside the rendered map.** Folium renders body HTML
  *before* the figure's script block, so a `<script>` added via
  `get_root().html` runs before `var map_xxx = L.map(...)` exists. A bare
  reference to the map from there throws `ReferenceError` and the feature
  silently does nothing. Either use a `folium.MacroElement` (its `script` macro
  renders after the map) or poll for the map object, which is what
  `PHONE_FIT_SCRIPT` does.
- **The legend's light styling is inline**, so dark rules targeting it need
  `!important`.
- **Two stroke colours are load-bearing selectors**: ring outlines are the only
  `#2c3e50` and station dots the only `#1a5490`, which is what lets
  `path.leaflet-interactive[stroke="..."]` target them precisely. Changing
  either colour in the light theme silently breaks its dark rule.
- **Transit line colours are real agency brand colours** and vary per city;
  they are brightened in dark mode rather than replaced. Staten Island Railway
  is the one line not using its agency's colour, because MTA's `#08179C` was
  too dark for its on-map label (see `DECISIONS.md`).

**Editing an imported module and testing it**

- **Streamlit serves a stale `components.py` across a rerun.** Editing a module
  the entry script imports and reloading the page is not enough — Python's
  bytecode cache and Streamlit's watcher combine to keep the old version. This
  cost a full debugging cycle on 2026-09-21: the theme-following code was
  correct, but the live iframe's `srcdoc` did not contain it, which read
  exactly like a logic bug. **Stop the server, delete `__pycache__` under
  `app/` and `pipeline/`, restart.** Confirm the new code is actually live
  before debugging behaviour — `iframe.getAttribute('srcdoc').includes(...)`
  for an injected script is a two-second check that would have saved the cycle.

**Measuring**

- **`getBoundingClientRect()` on an on-map label is unreliable in an automated
  browser pane** and produces convincing false failures: a marker reported a
  rect at x=490 while its own transform said 212px, pane at identity, no page
  scaling. Screenshots showed every label correctly placed. For label geometry,
  **the screenshot is the authority**; properties (`details.open`, computed
  colour, `style.width`, cluster counts) stay reliable.
- **Devtools colour-scheme emulation updates `matchMedia().matches` without
  dispatching the `change` event inside an iframe**, so a
  `prefers-color-scheme` listener cannot be tested that way — it needs a real
  OS theme switch in an ordinary browser.
- **Measurements taken mid-transition, or in a pane that is not compositing,
  are wrong.** CSS transitions freeze at frame 0 when a pane is not rendering.
  Let state settle, then measure — a reading taken in the same round trip as a
  page load gave "1 of 11 labels visible" where the settled figure was 9.
- Prefer computed styles over screenshots for **colour** claims; a 1.01:1 label
  looks like empty space rather than a bug.

---

## Verifying a theme change

Run the `deploy-verify` agent with the scope that fits (`map-chrome` for map
chrome, `full` before a deploy) — see `CLAUDE.md`. Then specifically:

1. Toggle dark on a city map: `document.body.classList.contains('dark-base')`
   flips, computed styles for `.map-legend`, `.leaflet-bar a` and
   `.leaflet-control-layers` change, and a ring path's computed stroke moves
   off `rgb(44, 62, 80)`. Toggle back and confirm both revert.
2. The choice survives a reload and carries to another city and to the
   Overview.
3. Tooltips are hard to trigger, so inject a synthetic one into
   `.leaflet-tooltip-pane` and read computed styles rather than hovering.
4. Check the heat layer's Reds gradient still reads on the dark base, every
   city's line colours are legible, and station dots are visible.
5. The macro map is pydeck, not Leaflet: only `.mapboxgl-canvas` is filtered,
   never `#deckgl-overlay`, so markers and labels keep their colours.
6. Regenerate **every** city (`outputs/<city>/heatmap.html` is committed), run
   `pipeline/drift_check.py`, and commit per the "commit after each green step"
   rule. Folium's random ids make the diff noisy; that is cosmetic.

---

## Superseded — provenance only, do not implement

The original dark-mode design used **two base tile layers and Leaflet's
automatic radio buttons**, with a `baselayerchange` handler toggling
`dark-base`, and a `class_name="dark-osm-tiles"` filter hitting only the second
layer's tiles.

**A fixed-position button replaced it**, because: the map is a fixed 1000px
wide while Streamlit's column is often narrower, so anything anchored to
Leaflet's own top-right corner (x=1000) can sit off-screen, whereas
`position: fixed` anchors to the visible frame; a button is more discoverable
than a radio inside a collapsed layer control; and one button style is shared
with the macro map and the navigation controls beside it. The radio approach
kept the tile layer and the body class in step for free, which the button has
to do itself — that is the trade that was accepted.

The original design also did not persist the choice; the shipped one does.

The full superseded code is in git history (`docs/dark_mode_handoff.md`, before
2026-09-21).
