# Handoff: hard-to-tap dots, lines and clusters on a phone (Leaflet heatmap)

For another project that renders a Leaflet map with business (or point) dots,
transit lines and marker clusters, and has the same symptoms on phones. File
and variable names below are placeholders for whatever that project uses; the
implementation is exact, taken from a fix that was measured, approved and
shipped in a sister project on 2026-10-03.

**Read section 2 before writing any code.** The causes are measurable in an
afternoon, and two of them (spiderfied groups collapsing, stations under
lines) are not tap-size problems at all.

---

## 1. Symptoms this fixes

- On a phone, tapping a business dot or a transit line is very hard; it
  takes several tries.
- Tapping a cluster fans it out ("spiderfies"), but the next tap, meant for
  one dot of the group, closes the group instead of showing that dot.
- A dot's tooltip runs off the edge of a narrow map (part of the name and
  category cut off).
- Tapping a station's center selects or highlights the line through it
  instead of showing the station.
- No visible link between the info shown and the dot it describes.

## Applies when the map has

- **Leaflet 1.9.x** with the default **SVG renderer** (no `preferCanvas`).
- Dots and stations drawn as `L.circleMarker` with `bindTooltip(...)`
  (sticky or not).
- Clusters from **Leaflet.markercluster 1.x** (`spiderfyOnMaxZoom` on, the
  default), possibly one cluster group per category.
- Lines as `L.polyline`, ideally with a class name you can match.
- Optional but common: a "cooperative gestures" mode on touch screens (one
  finger scrolls the page, two move the map: `map.dragging.disable()` when
  `(pointer: coarse)`), and a script that picks a line by distance on click.

If the project uses a canvas renderer, section 4 still applies, but the
measurements and the line-picking integration differ.

---

## 2. Measure first (do not skip)

Two reasons. First, the causes are not all "the target is small". Second, the
usual quick test, a desktop browser's device mode, flatters the map:
**Chromium snaps a tap to a nearby `cursor: pointer` element ("touch
adjustment")**, so taps 8 to 15 px off a dot succeed in Chrome and Android but
miss on an iPhone. Measure both kinds of tap.

### Harness (Node + raw CDP, headless Chrome or Edge, no Playwright needed)

1. Serve a scratch folder over HTTP (`python -m http.server <port>`) holding
   copies of the map HTML (`maps/before/<name>.html`, later
   `maps/after/<name>.html`) and a wrapper page that embeds a map the way the
   site does. Same origin, so the test can reach into the frame:

   ```html
   <meta name="viewport" content="width=device-width,initial-scale=1">
   <style>body{margin:0;padding:0 16px} iframe{display:block;border:0;width:100%;height:650px}</style>
   <div style="height:120px"></div><iframe id="f"></iframe><div style="height:1200px"></div>
   <script>document.getElementById('f').src=new URLSearchParams(location.search).get('src')</script>
   ```

2. Launch the browser with `--headless=new --remote-debugging-port=<port>
   --user-data-dir=<temp>`, connect to the page's `webSocketDebuggerUrl`
   (Node 22+ has a global `WebSocket`), then:

   ```js
   await send('Emulation.setDeviceMetricsOverride', {width: 375, height: 812, deviceScaleFactor: 1, mobile: true});
   await send('Emulation.setTouchEmulationEnabled', {enabled: true, maxTouchPoints: 5});
   await send('Emulation.setEmulatedMedia', {features: [{name: 'prefers-color-scheme', value: 'light'}]});
   ```

   Confirm inside the frame that `matchMedia('(pointer: coarse)').matches` is
   true, or the touch code paths never run.

3. **Two kinds of tap**, both needed:

   ```js
   // A real touch tap: goes through Chromium's touch adjustment (Android-like).
   await send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x, y, radiusX: 1, radiusY: 1, force: 1, id: 0}]});
   await send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
   // An exact-point tap: a press and release at the pixel, with touch emulation
   // still on. Models a browser that does no snapping (WebKit / iPhone).
   await send('Input.dispatchMouseEvent', {type: 'mouseMoved', x, y});
   await send('Input.dispatchMouseEvent', {type: 'mousePressed', x, y, button: 'left', clickCount: 1});
   await send('Input.dispatchMouseEvent', {type: 'mouseReleased', x, y, button: 'left', clickCount: 1});
   ```

   Neither `--disable-touch-adjustment` nor overriding `cursor` to `default`
   turned the snapping off in a 2026 Edge; the exact-point tap is the reliable
   way to model the no-snapping case.

4. Inject a helper into the frame (`frame.contentWindow.eval(src)`) that finds
   the map (`Object.values(window).find(v => v instanceof L.Map)`), stops the
   map's own startup logic from fighting programmatic moves if it has any
   (dispatch a synthetic `keydown` on the container if a "first interaction"
   flag exists), and lists targets **with clear space around them**:
   - every visible `L.CircleMarker` (dots have `__parent`, set by
     markercluster; stations do not), with hit radius
     `_radius + weight / 2`;
   - every line polyline, its `_parts` converted with
     `layerPointToContainerPoint`;
   - every cluster badge and label icon, as rectangles; every control,
     legend and fixed button, as obstacles.

   Keep a target only if a tap point 22 px from it, in its clearest
   direction, is at least 20 px from every other feature, and the target is
   at least 30 px inside the map. Otherwise a "miss" may really be a hit on a
   neighbor. For dots, zoom in (`setView(station, 17, {animate: false})`, wait
   ~700 ms for clusters to settle) until isolated singles appear.

5. Tap each target at **0, 8, 15, 20 and 22 px** off center (perpendicular to
   the segment for lines). Success: the target's own tooltip is open
   (`layer.getTooltip() && layer.isTooltipOpen()`, and note `isTooltipOpen()`
   throws on a layer with no tooltip), or after the fix the panel names it
   (`data-for == L.stamp(layer)`), or the line is highlighted. Record any
   OTHER tooltip or line that reacted, and how far the tooltip's rect runs
   past the map container's rect (clipping).

6. **The spiderfy scenario.** Find clusters whose children share one point
   (they spiderfy at any zoom):

   ```js
   var b = c; while (b._childClusters.length === 1) b = b._childClusters[0];
   var samePoint = b._zoom === c._group._maxZoom && b._childCount === c._childCount;
   ```

   Tap the badge, wait ~700 ms, confirm `c._group._spiderfied === c`, take a
   fanned-out child (`c.getAllChildMarkers().filter(k => k._spiderLeg)`), tap
   it at 0 to 22 px measured outward from the group's center, and record
   whether its info opened and whether the group collapsed. **Check which
   badge is on top**: separate category groups can stack badges on exactly
   the same point; `document.elementFromPoint` at the center tells you which
   one a tap really opens. Track that one, or your harness reports false
   failures.

7. **Desktop control.** Repeat at 1200 px with touch emulation off, using
   mouse hover then click, before and after. Every row must be identical, or
   the fix leaked into desktop.

Route the browser through whatever memory gate the project has; one headless
browser on one map measured about 0.1 GB for the Node tree. Kill the browser
tree on exit (`taskkill /T /F /PID` on Windows); `process.kill()` leaves
orphans that hold the profile.

### Reference numbers (sister project, four cities, before the fix)

| Exact-point tap (iPhone case) | Result |
|---|---|
| Dot, dead center | 43/43 |
| Dot, 8 / 15 / 22 px off | 0/43 each |
| Station, dead center | 2/22 (the line on top took it) |
| Line, up to 15 px (existing 16 px pick tolerance) | 10/10; at 22 px 0/10 |
| Fanned-out dot, second tap, 0 to 22 px | 0/46, group collapsed every time |
| Tooltip running past the map edge | 20/43 |

With Chromium's touch adjustment: dots 38/43 at 8 px, 39/43 at 15 px, 0/43 at
22 px. The cooperative-gesture handler swallowed no taps (its hint overlay had
`pointer-events: none`, its listeners were passive).

---

## 3. The causes

1. **Hit areas are the drawn shapes.** An SVG `circleMarker` of radius 5 with
   a 1 px stroke is an 11 px target. Leaflet's renderer `tolerance` only
   applies to the canvas renderer.
2. **Stations under lines.** If the station layer is added before the line
   layers, every line's path covers every station's center in the SVG, so a
   tap there hits the line.
3. **Spiderfied groups collapse on any map click, including a hit on their
   own dot.** Leaflet paths default to `bubblingMouseEvents: true`, so
   `_fireDOMEvent` fires `click` on the dot AND then on the map, and
   Leaflet.markercluster binds `map.on('click', this._unspiderfyWrapper)`.
   A miss collapses it for the plainer reason that it is a map click.
4. **Tooltips are anchored to the dot**, so near an edge of a ~340 px map
   they run off it.
5. **Touch adjustment moves the click point.** In Chromium the `click`
   after a tap reports the snapped point (often the center of a nearby badge),
   not the finger's. Any distance-based logic must read the `touchend` point.

---

## 4. The fix (touch screens only)

One script, added after the map's own script. It is inert unless
`(pointer: coarse)` matches at tap time, so desktop is untouched.

**What it does.** A capture-phase `click` listener on the map container sees
every tap before Leaflet. It measures from where the finger lifted and finds
the nearest target within REACH = 22 px (a 44 px target, WCAG 2.5.5 / Apple
HIG):

- a dot or station within 22 px of its center;
- a cluster within 22 px of its center or anywhere on its badge (spiderfied
  clusters skipped);
- a line within 22 px of its centerline.

**How it decides.** The nearest EDGE wins. Within 2 px, a dot or station beats
a cluster, which beats a line, so a tap on a station's center opens the
station and the track beside it picks the line. At equal distance and kind,
the later layer (drawn on top) wins. While a group is spiderfied, its own dots
within reach win outright.

**What happens next.**
- **Dot or station:** `stopPropagation()` (so Leaflet never sees a map
  click and the group stays open). The tooltip's own content goes into a
  fixed panel, and a ring marks the dot.
- **Cluster:** the click is re-sent to the cluster's badge element, so
  markercluster zooms or spiderfies exactly as for a direct tap.
- **Line, or nothing in reach:** the panel closes and the click continues to
  Leaflet unchanged. The line picker reads the resolver's point.

**Where the panel goes.** It is fixed in the page, bottom-left, 10 px from
each side and 24 px above the map's bottom edge (clear of the OSM credit
strip). It sits 8 px above the legend when the legend leaves 200 px or more
above it, and beside the legend otherwise. It moves to the top, under the
top-left controls and any top-right button row, when it would cover the dot
it describes. It is re-placed on resize, on map `moveend`, and on the legend's
`toggle` event. It closes on its own button, Escape, a tap on empty map, or a
tap on a line. The ring follows its dot when a spiderfied group closes (the
dot's `move` event).

On touch screens the tooltip pane is hidden with CSS, since the panel replaces
it.

### Placeholders to fill in

| Placeholder | Meaning |
|---|---|
| `MAP_VAR` | The global name of the `L.Map` (Folium: `m.get_name()`) |
| `LINE_CLASS` | A class every transit-line polyline carries (`className` option) |
| `LEGEND_SELECTOR` | The legend element, if any (its `toggle` event is used if it is a `<details>`) |
| `TOP_RIGHT_SELECTOR` | A fixed button row at the top-right, if any |
| `DARK_CLASS` | The class that switches the page to dark mode, if any |
| colors and font | The panel's light colors, the dark-mode variables, the map's font stack |

### CSS

```css
.tap-panel { display: none; position: fixed; z-index: 10000; box-sizing: border-box;
    left: 10px; bottom: 24px; max-width: 420px; overflow-y: auto;
    padding: 8px 40px 8px 12px; border-radius: 4px; overflow-wrap: anywhere;
    font: 13px/1.4 system-ui, sans-serif;
    background: #fff; color: #222; border: 1px solid #999;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3); }
.tap-panel.shown { display: block; }
.tap-close { position: absolute; top: 0; right: 0; width: 40px; height: 40px;
    padding: 0; border: 0; background: none; color: inherit; cursor: pointer;
    font: 22px/40px system-ui, sans-serif; }
.DARK_CLASS .tap-panel { background: #1b2433; color: #e6e9ef; border-color: #3a4558;
    box-shadow: 0 1px 4px rgba(0,0,0,0.5); }
/* White inner ring, near-black outer ring and shadow: reads on light and dark tiles. */
.tap-ring { box-sizing: border-box; border-radius: 50%; pointer-events: none;
    border: 2px solid #fff; box-shadow: 0 0 0 2px #111, 0 0 6px 2px rgba(0,0,0,0.45); }
@media (pointer: coarse) { .leaflet-tooltip-pane { display: none; } }
```

### Script

```js
(function () {
    var NAME = "MAP_VAR";
    var REACH = 22;         // px from a center or centerline: a 44 px target
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
        var legend = document.querySelector("LEGEND_SELECTOR");
        // Read by the line-picking code; see "Integration" below.
        var TAP = window.__MAP_TAP = {reach: REACH, last: null};

        var panel = document.createElement("div");
        panel.className = "tap-panel";
        var body = document.createElement("div");
        body.setAttribute("role", "status");
        body.setAttribute("aria-live", "polite");
        var close = document.createElement("button");
        close.type = "button";
        close.className = "tap-close";
        close.setAttribute("aria-label", "Close");
        close.innerHTML = "&times;";
        panel.appendChild(body);
        panel.appendChild(close);
        document.body.appendChild(panel);

        var ring = null, picked = null, passing = false;
        function follow() { if (ring && picked) { ring.setLatLng(picked.getLatLng()); place(); } }
        function clear() {
            panel.classList.remove("shown");
            panel.removeAttribute("data-for");
            body.innerHTML = "";
            if (ring) { m.removeLayer(ring); ring = null; }
            if (picked) { picked.off("move", follow); picked = null; }
        }

        // Pinned bottom-left, clear of the basemap credit and of the legend.
        function place() {
            if (!panel.classList.contains("shown")) return;
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
            // the top-left controls and any top-right button row.
            if (ring && ring._icon && overlaps(ring._icon.getBoundingClientRect(), panel.getBoundingClientRect())) {
                var under = top;
                [el.querySelector(".leaflet-top.leaflet-left"), document.querySelector("TOP_RIGHT_SELECTOR")]
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
            // The tooltip's own content, already escaped when the map was built.
            if (typeof text === "string") body.innerHTML = text;
            else if (text && text.cloneNode) { body.innerHTML = ""; body.appendChild(text.cloneNode(true)); }
            panel.setAttribute("data-for", String(L.stamp(layer)));
            panel.classList.add("shown");
            if (!ring) {
                ring = L.marker(layer.getLatLng(), {
                    interactive: false, keyboard: false,
                    icon: L.divIcon({className: "tap-ring", iconSize: [RING_PX, RING_PX]})
                }).addTo(m);
            }
            if (picked !== layer) { picked = layer; layer.on("move", follow); }
            place();
            if (layer.isTooltipOpen()) layer.closeTooltip();
        }

        function isLine(l) {
            return (" " + (l.options.className || "") + " ").indexOf(" LINE_CLASS ") >= 0;
        }
        // Where the finger actually lifted. Chromium's touch adjustment moves
        // a tap's click onto a nearby target and reports the moved point; the
        // touch events keep the real one.
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
                // Equal distance and kind: the later layer, drawn on top, wins
                // (categories cluster separately, so badges can share a point).
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
                    // L.Circle (radius in meters, e.g. distance rings) and
                    // markers without a tooltip are not targets.
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
                // On to Leaflet; the line picker reads this point.
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
```

### Integration with existing line picking (if the map has it)

If a `map.on("click")` handler picks the nearest line by distance, give it the
same tolerance on touch screens and the resolver's point:

```js
var TOL = matchMedia("(pointer: coarse)").matches ? 22 : 7;   // 22 = REACH
map.on("click", function (e) {
    var tap = window.__MAP_TAP && window.__MAP_TAP.last;
    var mine = !!(tap && tap.event === e.originalEvent);
    var at = mine ? map.containerPointToLayerPoint(tap.point) : e.layerPoint;
    var t = e.originalEvent && e.originalEvent.target;
    // The usual "a tap on a dot or station is not a line tap" early return,
    // skipped when the resolver has already decided this is a line tap.
    if (!mine && t && t.classList && t.classList.contains("leaflet-interactive") && !t._isLinePath) return;
    // ... measure each line's distance from `at` instead of e.layerPoint ...
});
```

Identity on the DOM event (`tap.event === e.originalEvent`) is exact: Leaflet
hands its handlers the same event object the capture listener saw.

### Interaction with other touch code

- **Cooperative gestures** (dragging off on touch): unaffected. A tap is
  still a tap; the resolver only reads `touchend` passively.
- **A "first interaction" guard** that re-fits the view until the reader
  touches the map: if it listens for `click`/`mousedown` in the capture
  phase on the same container and was registered earlier, it still sees
  every tap. `stopPropagation` does not stop other listeners on the same
  node.
- **Double-tap zoom:** Leaflet 1.9 simulates `dblclick` from two `click`s on
  the container; intercepted taps never reach it, so two quick taps on two
  dots no longer zoom the map. That is the intended behavior.

---

## 5. Rejected alternatives, and why

- **`L.canvas({tolerance: N})`** widens hits for canvas paths only. Switching
  renderers breaks anything that styles or reorders SVG paths: dark themes
  that recolor by `path[stroke=...]` selectors, line highlighting that
  restacks paths, `path` CSS filters.
- **Invisible wider hit circles under every dot** double the marker count.
  Big maps carry 100,000+ pins.
- **A larger dot radius** changes the look on every device.
- **Bigger tooltips or `direction: 'auto'`** still anchor to the dot, so
  they still clip on a narrow map.
- **`bubblingMouseEvents: false` on dots** stops the spiderfy collapse on a
  direct hit, but not on a near miss, and changes desktop behavior.

---

## 6. Verify before shipping

- Tap harness, exact-point and touch-adjusted, light and dark, on three or
  more maps (one dense, one with clusters, one with a narrow embed). Targets
  from the reference run after the fix: dots 100% at 0 to 20 px (22 px is
  the boundary, about 70%); station centers 100%; lines 100% to 20 px;
  fanned-out dots 100% with no collapse; panel clipping 0.
- Desktop mouse rows identical before and after.
- The map still opens at the right zoom, at phone width and full width, with
  no correction needed (if the project has a view guard, read its outcome).
- The basemap credit stays visible: hit-test five points along the
  attribution strip with `document.elementFromPoint`, with the panel open,
  with the legend both collapsed and open, at more than one viewport height.
- No page exceptions; the project's own markup and size checks pass.
- After approval, re-render every map once and diff (normalize Folium's
  random element IDs and line endings before comparing).

## 7. Pitfalls met along the way

- A browser pane screenshot can lag one action behind; read the DOM state to
  decide, and take the picture for people only.
- Picking "the first cluster" registered by a helper across several views
  tracks a badge that is no longer on the map; register per view and use the
  latest.
- Stacked badges at one point (one per category) look like "the cluster
  didn't open" in a harness. Check `elementFromPoint` at the center.
- When a tap is nearer a line than a spiderfied dot, a plain nearest-wins
  rule picks the line and collapses the group. That is why fanned dots win
  outright while the group is open.
- A bottom panel can hide the very dot it describes when the dot is low on
  the map; hence the flip to the top.
- Run each measurement series as one job and stop the browser tree after it.
  An interrupted run leaves the browser and the static server running.

## 8. Not covered (raise with the owner instead)

- **Desktop stations under lines:** hovering a station's center shows the
  line, not the station. The fix would be adding stations after lines, or
  putting them in a higher pane, which changes the desktop map.
- **Desktop spiderfied groups** still close on a click (hover shows the
  tooltip first).
- **The details panel on desktop** is a design call; the reference project
  kept it to touch screens.
