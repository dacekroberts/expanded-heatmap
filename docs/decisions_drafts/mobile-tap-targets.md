# Decisions drafts: mobile-tap-targets

Drafts from the `mobile-tap-targets` branch, newest first, for the cleanup
session to fold into `DECISIONS.md`.

### 2026-10-03 - A tap on a phone selects the nearest dot, station, cluster or line within 22 px; a dot's details go in a fixed panel (PROPOSED, awaiting the owner)

- **Measured why tapping dots and lines on a phone was hard, before changing
  anything (owner's report, 2026-10-03).** Headless Edge over CDP at 375 x 812
  with touch emulation (`pointer: coarse`, so `TOUCH_GESTURE_SCRIPT` had
  dragging off, as on a phone), each map embedded in a 343 x 650 frame as the
  app embeds it, on Edmonton, Paris, Tokyo and Odense. Targets were chosen
  with at least 20 px of clear map around the tap point, and tapped at 0, 8,
  15 and 22 px off centre. Two kinds of tap: Chromium's own touch events,
  which go through its touch adjustment (it snaps a tap to a nearby
  `cursor: pointer` element, as Android Chrome does), and a press and release
  at the exact point, which models a browser that does no such snapping
  (WebKit on the owner's iPhone). Rendered sizes: every dot an SVG circle of
  radius 5 with a 1 px stroke (hit radius 5.5 px, an 11 px target), stations
  radius 5 with a 3 px stroke (6.5 px), lines 4 px strokes, SVG renderer
  throughout (no canvas, so no renderer tolerance applies).
  Exact-point taps: a dot opened on 43 of 43 taps on its centre and 0 of 43
  at 8, 15 or 22 px. A station opened on 2 of 22 taps on its centre: stations
  are drawn before the lines, so a line covers every station's centre and the
  tap picked the line instead (Tokyo 0 of 6, Edmonton 0 of 6, Odense 0 of 6).
  A line was picked on 10 of 10 taps up to 15 px (`LINE_HIGHLIGHT_SCRIPT`
  already matched lines by distance, 16 px on a touch screen) and 0 of 10 at
  22 px (no Tokyo line point had 20 px of clear map around it). With Chromium's touch adjustment the dot figures were 38 of 43 at
  8 px, 39 of 43 at 15 px and 0 of 43 at 22 px, so an Android phone fared
  better than an iPhone but not at a 44 px target. The one-finger handling
  swallowed nothing: centre taps succeeded on every dot with or without a
  6 px finger slide, the hint overlay has `pointer-events: none`, and its
  listeners are passive.

- **Found why a spiderfied group closed under the second tap (owner's
  addition, 2026-10-03).** Businesses that share one point spiderfy at any
  zoom. In the same emulation, on 14 such groups of 3 to 12 (dense hubs in
  all four cities), the second tap selected the dot on 0 of the 46 tries
  where the first tap had opened the group, at every offset from 0 to 22 px,
  with and without touch adjustment; the group collapsed every time. Cause,
  traced on Paris: a Leaflet path's `bubblingMouseEvents` defaults to true, so
  a click on a dot also fires the map's `click`, and Leaflet.markercluster
  unspiderfies on any map click. A tap that missed the 11 px dot collapsed it
  for the plainer reason that it was an empty-map click.

- **Measured the tooltip clipping in the owner's Odense screenshot.** Of the
  dots whose tooltip opened, 20 of 43 ran past the 343 px map's edges (Odense
  10 of 12), although the test dots were all at least 30 px inside the frame.

- **Proposed: `TAP_SELECT_SCRIPT` in `pipeline/map_common.py`, active only
  when the primary pointer is coarse.** A capture listener on the map
  container sees each tap's click before Leaflet and finds the nearest target
  by geometry from where the finger lifted (the `touchend` point, since
  Chromium's adjustment reports a moved click point): a dot or station within
  22 px of its centre, a cluster within 22 px of its centre or anywhere on its
  badge, a line within 22 px of its centreline. Nearest edge wins; within 2 px
  a dot or station beats a cluster, which beats a line, so a station's centre
  opens the station and the track beside it picks the line. A dot or station
  is selected and the click stops there, so Leaflet sees no map click and a
  spiderfied group stays open. A cluster gets the click re-sent to its own
  badge, so it zooms or spiderfies as before. A line, or nothing in reach,
  closes the panel and passes the click on unchanged; `LINE_HIGHLIGHT_SCRIPT`
  now uses the same point and the same 22 px on a touch screen (was 16).
  22 px from a centre is a 44 px target (WCAG 2.5.5, Apple's HIG).
  Rejected: `L.canvas({tolerance})` (the dark theme recolours lines and
  stations by matching SVG path attributes, and line picking reorders SVG
  paths, so a canvas renderer would break both); invisible wider hit circles
  under every dot (doubles the markers, on maps of up to 133,362 pins in
  Mexico City).

- **Proposed: the selected dot's details in a fixed panel, and a ring on the
  dot (owner's addition, 2026-10-03).** On a touch screen the tooltip pane is
  hidden (`@media (pointer: coarse)`) and the tooltip's own text goes into a
  panel fixed bottom-left, 10 px from each side, 24 px above the map's bottom
  edge (clear of the OSM credit, the legend's own clamp) and 8 px above the
  legend; beside the legend when an open legend leaves under 200 px above it;
  and at the top, under the zoom and layer controls and the button row, when
  it would cover the dot it describes. It closes on its button, Escape, a tap
  on empty map or a line, and moves on a new selection. The ring is a 26 px
  white ring with a near-black outer ring and shadow, not interactive, so it
  reads on light and dark tiles alike; it follows its dot when a spiderfied
  group closes. Mouse and trackpad readers are unchanged: no panel, no ring,
  the same tooltips. New visible text: the close button's accessible name
  "Close" and its "×" glyph, flagged here as a proposal.

- **Two refinements found by the after-measurement.** While a group is
  spiderfied, its own dots within reach win outright: in Tokyo and Odense a
  group sat beside a line, and taps 8 to 22 px out from its dots were nearer
  the line, picked it and closed the group (8 of 42 taps at 8 to 22 px on
  open groups, before the rule).
  And at equal distance the later layer wins, because it is the one drawn on
  top: each business category clusters separately, and in Tokyo three
  categories' badges sat on one point, where the first-found (bottom) badge
  had been opening instead of the one the reader sees.

- **After, same emulation, same targets (prototype injected into copies of
  the committed maps; nothing re-rendered).** Exact-point taps (the iPhone
  case): a dot opened on 43 of 43 taps at 0, 8, 15 and 20 px (was 43, 0, 0,
  and untested) and 29 of 43 at 22 px, the boundary (was 0); a station
  centre on 22 of 22 (was 2); a line on 10 of 10 up to 20 px and 7 of 10 at
  22 px (was 0 at 22 px). Off a station's centre, Edmonton and Odense
  stations opened on 6 of 6 taps up to 15 px; in Paris and Tokyo a tap 8 px
  or more off a station usually landed nearer the line through it and picked
  the line, as the rule intends. With Chromium's touch adjustment (the
  Android case): dots 43 of 43 up to 20 px and 39 of 43 at 22 px.
  Spiderfied groups, exact-point taps: the second tap selected the dot on
  60 of 60 tries where the first had opened the group, at every offset from
  0 to 22 px, and no group closed (was 0 of 46, every one closed). The two
  Edmonton groups the run counted as not opening each sat under another
  category's badge at the same point: the tap opens the badge on top, and a
  further tap on the same spot opens the one beneath. A details
  panel ran past the map's edge on 0 of every selection (tooltips had on 20
  of 43). Dark theme (Paris, Odense): the same figures as light. Desktop,
  mouse at 1200 px on Edmonton, Paris and Tokyo, hover and click at 0, 4, 8
  and 15 px off dots, stations and lines: identical before and after, row
  for row.

- **Checks on the prototypes.** `scripts/check_map_view.js` on Edmonton,
  Paris and Tokyo, light and dark, embedded at 375 and standalone at 1200,
  two fresh loads each: 24 of 24 at the expected zoom (11.75/11.5, 11/12.5,
  10/11), 0 guard corrections. `scripts/check_map_attribution.js` at 375 x
  650, 375 x 812, 1200 x 650 and 1200 x 900, light and dark: 0 points covered
  in 24 runs; with a dot's panel open (Paris, 375 x 812) the panel sat at
  y 491-581 above the collapsed legend and at x 10-144, y 426-626 beside the
  open legend, and the credit (y 636-650) hit-tested 5 of 5 both times.
  `check_map_markup.py` (pointed at the four prototypes): 0 problems.
  `check_inline_arrays.py`: 0 arrays over the cap. No page exceptions.

- **Not changed, for the owner.** On desktop a mouse over a station's centre
  shows the line, not the station (Paris and Tokyo 0 of 6 before and after),
  because lines are drawn over stations; and a click on a spiderfied dot
  still closes the group there, though its tooltip opens on hover first.
  Raising stations above lines, or the panel on desktop, would change the
  desktop map, so both wait for the owner.
