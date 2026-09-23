// Run in the browser via the javascript tool, against EITHER a standalone
// heatmap (the `heatmap-static` preview at /<city_slug>/heatmap.html) OR a
// city page on the deployed app - it finds the map two frames deep on its own.
// Evaluates to a JSON string; the view is right when `problems` is empty.
//
// WHAT IT GUARDS. An embedded map has loaded at the WRONG ZOOM three times, in
// three different ways, each fixed where it broke: Edmonton (zoom 8.25 against
// a baked 11.5), Paris (9 against 12.5, then a blank 0px map), Lille (8.25
// against 11.75). All were a race in PHONE_FIT_SCRIPT, all were intermittent,
// and all were fixed by a reload - which is exactly why a screenshot misses
// them and why this reads the MAP OBJECT instead. Since 2026-09-23 the fit
// script also carries a GUARD that re-fits a wrong view until the reader
// touches the map; this check is how a publish confirms the guard is present
// and the view it produced is right. See .claude/skills/map-view/.
//
// INDEPENDENT, NOT SELF-REPORTED. The guard exposes window.__HEATMAP_VIEW. This
// check reads its INPUTS - the baked home view, the bounds, the padding, the
// full map width - and recomputes the expected zoom itself, rather than
// trusting the guard's own `expected`. A check that asks the code it checks
// whether it is right proves nothing.
//
// HOW TO RUN IT - and each rule below is a way this has already been got wrong:
//   * LOAD FRESH at each size. Resizing a loaded page measures a stale layout.
//   * DO NOT TOUCH THE MAP before running it - no click, no wheel, no key.
//     A touched map shows the reader's view, not the render's, so `touched`
//     comes back as UNMEASURED rather than as a pass or a failure.
//   * RUN IT MORE THAN ONCE. The race is intermittent: one clean load proves
//     little. `corrections` > 0 on any load means the race fired and the guard
//     repaired it - record that, it is the only measure of how often it fires.
//   * An embedded run needs the Streamlit page to have settled (~15 s).
await new Promise(r => setTimeout(r, 1200));

// Below this the frame is not laid out - see the width test further down.
// 280 sits under the narrowest real phone column and far above the 0 and 16px
// readings a collapsed or hidden frame produces.
const MIN_REAL_WIDTH = 280;

const findMap = () => {
  const here = (w) => {
    try {
      if (!w.L || !w.__HEATMAP_VIEW) return null;
      const m = Object.values(w).find(v => v && v instanceof w.L.Map);
      return m ? {w, m} : null;
    } catch (e) { return null; }
  };
  const top = here(window);
  if (top) return top;
  // The deployed app: page -> Streamlit app frame -> st.iframe map frame.
  for (const a of document.querySelectorAll('iframe')) {
    let d; try { d = a.contentDocument; } catch (e) { continue; }
    if (!d) continue;
    for (const b of d.querySelectorAll('iframe')) {
      const hit = here(b.contentWindow);
      if (hit) return hit;
    }
    const direct = here(a.contentWindow);
    if (direct) return direct;
  }
  return null;
};

const problems = [];
const notes = [];
const found = findMap();
let out = {problems, notes};

if (!found) {
  problems.push('no map carrying __HEATMAP_VIEW found - either the page has not ' +
                'loaded, or this map was rendered before the 2026-09-23 guard and ' +
                'needs re-rendering');
} else {
  const {w, m} = found;
  const v = w.__HEATMAP_VIEW;
  const width = w.document.documentElement.clientWidth || w.innerWidth;
  const target = Math.min(width, v.mapW);
  const zoom = m.getZoom();
  let expected = null;
  if (target < v.mapW && v.bounds) {
    expected = m.getBoundsZoom(w.L.latLngBounds(v.bounds), false,
                               w.L.point(2 * v.padding[0], 2 * v.padding[1]));
  } else if (v.home) {
    expected = v.home.zoom;
  }
  out = {width, mapW: v.mapW, zoom, expected, home: v.home && v.home.zoom,
         corrections: v.corrections, touched: v.touched, problems, notes};

  if (width < MIN_REAL_WIDTH) {
    // A FRAME THIS SMALL IS NOT LAID OUT, so there is nothing to compare. Found
    // 2026-09-23 on the check's first live run: the map reported width 16 at
    // zoom 19 and the check PASSED it, because the expected zoom was computed
    // from the same meaningless width. The cause was the harness - the
    // browser pane was collapsed, Streamlit's app frame measured 0 px wide and
    // squeezed the map iframe to 16 - but a check that agrees with a bogus
    // measurement is worse than no check. Same reasoning as apply()'s refusal
    // of a zero width. No real reader sees a map narrower than a phone.
    problems.push(`UNMEASURED: the map frame is ${width}px wide, below ` +
                  `${MIN_REAL_WIDTH}px, so it is not laid out and no expected zoom ` +
                  `means anything. Is the browser pane collapsed or hidden? Bring ` +
                  `it forward at a real size, reload, and run again.`);
  } else if (v.touched) {
    notes.push('UNMEASURED: the map has been touched, so it shows the reader\'s ' +
               'view, not the render\'s. Reload and run again without interacting.');
  } else if (expected === null) {
    problems.push('no expected view could be computed - no home view and no bounds');
  } else if (Math.abs(zoom - expected) > 0.01) {
    problems.push(`zoom ${zoom} but ${expected} expected at width ${width} ` +
                  `(home ${v.home && v.home.zoom}) - the view is wrong and the ` +
                  `guard did not repair it`);
  }
  if (v.corrections > 0) {
    notes.push(`the race FIRED on this load and the guard repaired it ` +
               `(${v.corrections} correction(s)) - worth recording`);
  }
}
JSON.stringify(out);
