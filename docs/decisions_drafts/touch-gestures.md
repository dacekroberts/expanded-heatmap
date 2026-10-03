### 2026-10-02 - Touch gestures: one finger scrolls the page, two move the map

- **The map-view guard no longer stops for a one-finger touch that only
  scrolls the page (owner, 2026-10-02).** With one-finger dragging off on a
  touch screen, a single finger cannot move the map, yet PHONE_FIT_SCRIPT
  still counted its touchstart and pointerdown as the reader steering, so a
  reader who scrolled past a map in its first seconds switched off the
  repair of a wrong first view. `steering()` now reads `map.dragging`: with
  dragging off, a one-finger touchstart or a touch pointerdown leaves the
  guard running; a second finger, and a tap (which goes on to send
  mousedown and click, which a scroll does not, so `click` joined the
  listened events), still stop it; with dragging on, every touch counts as
  before. This narrows the skill's "never weaken this" rule only for a
  touch that cannot move the map; `.claude/skills/map-view/SKILL.md` says
  so. Measured on Edmonton, Paris and Tokyo (375 x 812, real CDP touch,
  embedded): the guard's `touched` stayed false after a one-finger vertical
  and a sideways swipe, and turned true after a two-finger pan, after a
  single tap on a fresh load, and after a desktop mouse drag; after a swipe,
  a forced zoom of 8.25 was put back to the expected zoom (11.5, 11, 9.75)
  within 1.5 s, `corrections` 1 each. Every map re-rendered again (measured
  peak 1.61 GB; Bucheon's write hit a transient Windows `OSError 22` between
  Folium's save and the `lang` rewrite and was re-rendered alone), and all
  144 differ from the previous commit only by PHONE_FIT_SCRIPT's new text
  once ids and whitespace-only lines are normalized; 37 CJK maps converted
  CRLF to LF again. `check_map_view.js` and `check_map_attribution.js` on the
  same six maps, four viewports, two themes: 0 problems, 0 corrections in
  48 loads, and the forced-on hint covered nothing in all 48.
- **On a touch screen a one-finger swipe on a city map now scrolls the page;
  two fingers pan and pinch-zoom the map (owner, 2026-10-02).** At 375 px a
  city page's map frame is 333 x 650, nearly a whole phone screen, and
  Leaflet took every one-finger drag as a pan, so a swipe that landed on the
  map could not scroll past it and the 21 px side margins were too narrow to
  hit reliably. `TOUCH_GESTURE_SCRIPT` in `pipeline/map_common.py` disables
  `map.dragging` when the primary pointer is coarse (`matchMedia("(pointer:
  coarse)")`, re-applied on change). Leaflet then drops `leaflet-touch-drag`
  and the container's CSS falls back to `touch-action: pan-x pan-y`, so the
  browser scrolls the swipe and hands it to the page around the frame;
  `touchZoom` stays on, and Leaflet's pinch handler moves the map with the
  two fingers' midpoint, so a two-finger drag pans without dragging ever
  being re-enabled. Rejected: enabling dragging while two touches are down,
  as first proposed, because Leaflet's Draggable ignores a second finger and
  the pinch handler already pans. Mouse, trackpad and a touch laptop whose
  primary pointer is a mouse are unchanged.
  A one-finger drag that starts on the map (not on a Leaflet control) shows
  "Use two fingers to move the map" in a polite live region, centered, for
  1.5 s after the last move. It sits in the map container at z-index 900,
  under Leaflet's control corners (1000: zoom, layers, the OSM credit) and
  under the body-fixed legend and button row, so it can never cover a
  control or the credit; it takes the button colors in both themes.
  Movement is read in screen coordinates, because while the page scrolls the
  frame travels with the finger. Every committed map re-rendered with
  `drift_check.py --render-only` (measured peak 1.94 GB): all 144 drifted,
  and all 144 match HEAD exactly once the new block, Folium's 32-hex ids
  and one whitespace-only line are set aside. 37 CJK maps came out CRLF
  (the post-save `lang` rewrite) and were converted to LF before staging.
  Measured with real CDP touch input in headless Edge, each map embedded as
  the app embeds it (srcdoc frame 333 x 650 at 375 x 812, touch emulated),
  on Edmonton, Paris, Tokyo and Angers: a one-finger 300 px swipe on the
  map scrolled the page 362 to 367 px with the map unmoved, and showed the
  hint, gone and cleared 2.7 s later; a one-finger sideways swipe moved
  nothing; a two-finger drag panned the map with the zoom unchanged and the
  page unscrolled; a pinch zoomed in 1.25 levels; one-finger taps on +, the
  layer control, the theme toggle (twice) and a business cluster all
  responded; a tap on a dot opened its tooltip on Edmonton and Paris (no
  uncovered dot in view on the other two). At 1200 px without touch,
  dragging stayed on, `touch-action` stayed `none` and a mouse drag panned
  as before. No console errors. `check_map_view.js` and
  `check_map_attribution.js` on Edmonton, Paris, Tokyo, Amsterdam, New
  York and Angers at 375 x 650, 375 x 812, 1200 x 650 and 1200 x 900, light
  and dark: 0 problems, 0 corrections, in all 48 loads. With the hint forced
  on, hit-testing the zoom buttons, layer toggle, theme and Global View
  buttons, legend header and OSM credit found none covered (Edmonton,
  Amsterdam, Tokyo; 24 loads); its text is rgb(28,43,42) on white in light
  and rgb(230,237,247) on rgb(19,28,46) in dark.
- **The Overview's macro map was left as it is: deck.gl cannot give the same
  behavior through Streamlit.** Streamlit 1.64's `DeckGlJsonChart` builds its
  `<DeckGL>` with a fixed prop list (viewState, layers, getTooltip,
  parameters, views, controller, onClick), so deck's `touchAction` (default
  `none`) and `eventRecognizerOptions` cannot be set from pydeck, and with
  `touch-action: none` on the canvas the browser never scrolls the page
  through it. A view controller of `{dragPan: false}` does reach deck, but
  alone it would make a one-finger swipe do nothing at all, and it would
  disable mouse dragging on the desktop too, because the server cannot tell
  a phone from a desktop. Reaching into deck's event manager from the
  parent page's script was rejected as forcing it. The macro map is 460 px
  tall, full width, so the page stays scrollable above and below it.
