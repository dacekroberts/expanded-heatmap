// Run in the browser against a city's standalone heatmap (e.g. served by the
// `heatmap-static` preview at /<city_slug>/heatmap.html) via the javascript
// tool. Evaluates to a JSON string; the map is fine when `problems` is empty.
//
// WHAT IT GUARDS. CLAUDE.md makes the basemap credit a hard invariant: ODbL
// 1.0 requires it to stay visible, "not hidden behind UI or a toggle".
// check_provenance.py already refuses a committed map that does not CONTAIN
// the credit. Nothing measured whether a reader could SEE it until
// 2026-09-23, when the legend turned out to cover it completely, in every
// city, at any viewport taller than the map. See _LEGEND_BOTTOM_CSS in
// pipeline/map_common.py for the mechanism and the measurements.
//
// HIT-TESTING, NOT RECTANGLES. `.claude/agents/deploy-verify.md` records that
// getBoundingClientRect() in this browser pane can report a pre-fit position
// while the render is correct, and that it produced convincing false
// failures. So the question is asked the way a reader's eye asks it:
// document.elementFromPoint at five points along the strip must come back
// with the attribution itself. Whatever else comes back is NAMED in the
// failure, which is why this catches any future overlay and not only the
// legend it was written for.
//
// THE LEGEND IS FORCED OPEN, because that is the worst case and it is
// reachable at every width. Below _MAP_W the legend loads collapsed, but a
// reader who clicks "Show" sets LEGEND_AUTOFIT_SCRIPT's `touched` and it
// stays open from then on. Whatever state the page chose is restored at the
// end.
//
// ONE RUN MEASURES ONE VIEWPORT - a page script cannot resize the window, so
// the caller does it between runs (deploy-verify step 5 uses 650, the
// embedded height, then 768 and 812). What lets a single run generalise is
// `clamp` at the end: it checks the legend's computed `bottom` against the
// value the map's own measured bottom edge requires, so a pass says the
// clamping MECHANISM is in force, not merely that this one height happened to
// clear. A run whose `covered` is 0 but whose `clamp.ok` is false is a map
// that is one viewport resize away from breaching.
await new Promise(r => setTimeout(r, 1500));

const problems = [];
const att = document.querySelector('.leaflet-control-attribution');
const legend = document.querySelector('details.map-legend');
const mapEl = document.querySelector('.folium-map');
if (!att) problems.push('no .leaflet-control-attribution: the basemap credit is missing entirely');
if (!mapEl) problems.push('no .folium-map');

// A readable name for whatever is sitting on top of the credit, so a failure
// says WHICH overlay rather than just "covered".
const describe = (el) => {
  if (!el) return 'nothing';
  const cls = typeof el.className === 'string' ? el.className.trim().split(/\s+/).join('.') : '';
  return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (cls ? '.' + cls : '');
};

let wasOpen = null;
let covered = 0;
let offscreen = 0;
let hits = [];
let style = null;
let clamp = null;

if (att && mapEl) {
  // Worst case first: the legend as a reader who clicked "Show" leaves it.
  if (legend) {
    wasOpen = legend.open;
    legend.open = true;
    await new Promise(r => setTimeout(r, 300));
  }

  const a = att.getBoundingClientRect();
  if (a.width <= 0 || a.height <= 0) {
    problems.push(`attribution has a zero box (${Math.round(a.width)}x${Math.round(a.height)})`);
  }

  // A POINT OUTSIDE THE VIEWPORT IS UNMEASURABLE, NOT COVERED. elementFromPoint
  // returns null for a coordinate off-screen, and null is indistinguishable
  // from "something opaque is on top" unless you check. Caught 2026-09-23
  // while verifying this very fix: resizing an already-loaded page from 1024 to
  // 375 left the attribution's rect reading x 803-1000 from the previous
  // layout, so all five probes landed off a 375px-wide viewport and the check
  // reported "covered 5/5 by: nothing". Nothing was on top - the map simply had
  // not re-fitted yet. That is exactly the stale-rect false failure
  // .claude/agents/deploy-verify.md warns about, so it is called out by name
  // rather than counted as a breach.
  for (let i = 0; i < 5; i++) {
    const x = a.left + a.width * (i + 0.5) / 5;
    const y = a.top + a.height / 2;
    if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) {
      offscreen++;
      hits.push({ x: Math.round(x), y: Math.round(y), on: 'offscreen', clear: null });
      continue;
    }
    const el = document.elementFromPoint(x, y);
    const clear = !!(el && (el === att || att.contains(el)));
    if (!clear) covered++;
    hits.push({ x: Math.round(x), y: Math.round(y), on: describe(el), clear });
  }
  if (offscreen) {
    problems.push(`${offscreen}/5 probe points fall outside the ${innerWidth}x${innerHeight} ` +
                  `viewport, so coverage is UNMEASURED here, not clear and not breached. The ` +
                  `attribution's rect is stale - reload the page at this size instead of ` +
                  `resizing a loaded one, and re-run`);
  }
  if (covered) {
    const by = [...new Set(hits.filter(h => h.clear === false).map(h => h.on))].join(', ');
    problems.push(`attribution covered at ${covered}/5 points along the strip, by: ${by}`);
  }

  // Hidden or shrunk rather than covered - the other ways a credit stops
  // being visible while still being present in the HTML.
  const cs = getComputedStyle(att);
  style = {
    display: cs.display, visibility: cs.visibility,
    opacity: Number(cs.opacity), fontSize: cs.fontSize,
    clipPath: cs.clipPath, box: [Math.round(a.width), Math.round(a.height)],
  };
  if (cs.display === 'none') problems.push('attribution is display:none');
  if (cs.visibility !== 'visible') problems.push(`attribution is visibility:${cs.visibility}`);
  if (Number(cs.opacity) < 0.3) problems.push(`attribution is opacity:${cs.opacity}`);
  if (parseFloat(cs.fontSize) < 9) problems.push(`attribution shrunk to ${cs.fontSize}`);
  if (cs.clipPath && cs.clipPath !== 'none') problems.push(`attribution is clipped: ${cs.clipPath}`);
  if (!/OpenStreetMap/i.test(att.textContent)) problems.push('attribution does not name OpenStreetMap');
  if (!att.querySelector('a[href*="openstreetmap.org/copyright"]'))
    problems.push('attribution is not linked to the OSM copyright page');

  // The clamp. Expressed against the MAP's own measured bottom edge, not
  // against _MAP_H, so this stays true if that constant ever changes.
  if (legend) {
    const m = mapEl.getBoundingClientRect();
    const need = Math.max(24, Math.round(innerHeight - m.bottom + 24));
    const got = Math.round(parseFloat(getComputedStyle(legend).bottom));
    clamp = { need, got, mapBottom: Math.round(m.bottom), innerHeight, ok: Math.abs(got - need) <= 2 };
    if (!clamp.ok)
      problems.push(`legend bottom is ${got}px, needs ${need}px to stay clear of the ` +
                    `map's bottom edge at this viewport - the clamp is not in force ` +
                    `(see _LEGEND_BOTTOM_CSS in pipeline/map_common.py)`);
  }

  if (legend && wasOpen !== null) {
    legend.open = wasOpen;
    await new Promise(r => setTimeout(r, 200));
    if (legend.open !== wasOpen) problems.push('legend state not restored');
  }
}

JSON.stringify({
  viewport: [innerWidth, innerHeight],
  legendForcedOpenFrom: wasOpen,
  covered, offscreen, hits, style, clamp, problems,
});
