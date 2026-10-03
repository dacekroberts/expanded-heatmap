### 2026-10-02 - Touch gestures: one finger scrolls the page, two move the map

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
