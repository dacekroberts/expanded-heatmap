# DECISIONS drafts - map border (`claude/nice-bell-e3501b`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - A teal frame around every map (owner's pick, T3)

- **Every city map's embed and the Overview's macro map now sit in a 3 px
  muted teal ring with a faint teal halo and glow, and 8 px corners** (owner,
  2026-10-02: "add a nice border to all maps that aligns with our midnight
  slate theme"). CSS only, in `app/components.py`: `MAP_FRAME_CSS`, applied
  by `render_city_title()` to the map's element container on city pages and
  by `render_macro_map_theme()` to `stDeckGlJsonChart` on the Overview.
  `pipeline/map_common.py` and the 144 committed maps are untouched.
- **How it got there.** Three slate variants went to the owner first (a 1 px
  hairline; hairline and soft shadow; both with 8 px corners). The owner asked
  for teal, the site's own accent, then for a thicker ring, and picked the
  muted ring with a halo (T3) over the full-strength accent (T1) and the
  muted ring alone (T2). The ring is each theme's teal mixed 45% into its
  page color: `#0d9488` into `#ffffff` in light, the dark page accent
  `#2dd4bf` into `#0B1220` in dark. Mixing them in CSS (`color-mix()`) keeps
  the colors derived from `pipeline/theme.py` rather than typed in as new
  literals. The dark theme's own border token, `#23304A`, was rejected early
  because it was nearly invisible against the dark basemap.
- **Box-shadows only, so the map keeps its exact size.** Measured in the
  preview: the map stays 1000x650 at a 1200 px page and 333x650 at 375 px,
  the macro map stays 1030x460 and 333x460, and the main column's
  scrollWidth equals its clientWidth at 375 px (no horizontal scroll).
- **The shadow is on the container, not the iframe.** Streamlit sets
  `color-scheme: normal` on the `st.iframe` element, so `light-dark()` there
  always resolved to the light color, and the first dark mockups showed
  light-mode rings. The element container is exactly the map's size at every
  width and inherits the page's scheme. The iframe only rounds its own
  corners. A browser without `light-dark()` or `color-mix()` gets a plain
  half-alpha teal ring instead (the first declaration).
- **The OSM credit is not clipped by the rounded corner.** A parent-level
  `elementFromPoint` test at the corners and center of the credit's text box
  (Le Mans, light and dark, 1200 and 375 px) returned the map every time, and
  the frame's own corner pixel returned the page, so the test does tell the
  two apart. On the macro map (`overflow: hidden` now clips it to the
  corners) the credit hit-tests as itself at 1200 and 375 px in both themes,
  its text ending 5 px from the right and 2 px from the bottom at 1200 px,
  inside the 8 px curve. The theme button stays inside the frame.
  `check_map_attribution.js`'s logic run on the standalone Le Mans, Seattle
  and Kyoto maps at 1000x650, 1000x768 and 375x812: 0 covered, clamp in
  force, no problems.
- The owner's mockups were taken in the browser pane, not with
  `capture_pages.mjs`. The heavy-job gate refused the headless capture (3.3 GB
  available against the 4.5 GB it needed), and the gate was not overridden.
