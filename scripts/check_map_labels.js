// Run in the browser via the javascript tool, against EITHER a standalone
// heatmap (the `heatmap-static` preview at /<city_slug>/heatmap.html) OR a
// city page on the deployed app - it finds the map two frames deep on its own,
// as check_map_view.js does. Evaluates to a JSON string; the map is fine when
// `problems` is empty.
//
// Checks: every line label (the bold 14px divs inside .leaflet-marker-icon;
// the numeric cluster badges are ignored) is inside the map box, clear of the
// open legend, and not overlapping another line label; each label has a legend
// row; the legend collapses and re-expands; and the Dark Mode button is in
// view and flips and restores the theme.
//
// RUN IT AT A PHONE WIDTH AS WELL AS A DESKTOP ONE - 375 standalone, and 343,
// which is the map frame's width inside the app on a 375 phone. Until
// 2026-09-23 this ran only at 854 and 1280, and a label running off the edge
// of the map on a phone - Rennes' "Métro b" cut to "Métr" in the app,
// Marseille's "Tramway 1" by ~33px - was invisible to it. At or above the
// map's layout width (1000) PHONE_FIT_SCRIPT never fits to bounds, so a
// desktop-only run does not exercise the narrow path at all; `notes` says so.
// Every clipped label is reported with how many pixels, and what share of its
// width, fall outside the map.
//
// LABEL POSITIONS COME FROM THE MAP OBJECT, NOT FROM WHERE THE DOM LAST DREW
// THEM. Found 2026-09-23: with the browser pane hidden
// (document.visibilityState "hidden"), the map had already fitted to zoom 12.25
// while every label's element still sat at its desktop position - Rennes'
// "Métro a" read x 617 on a 375px map for six seconds and was reported "out of
// view", while a screenshot (which forces a frame) showed it at 221, fully
// visible. The redraw waits for a frame a hidden page never gets, and it is
// intermittent: some hidden loads were fresh. So each label box is the
// marker's latLngToContainerPoint plus the label's offset from its own icon -
// both independent of the stale transform - and a DOM that disagrees is
// recorded in `notes` as stale, never scored.
await new Promise(r => setTimeout(r, 1500));

// Below this the frame is not laid out - same threshold and reasoning as
// check_map_view.js.
const MIN_REAL_WIDTH = 280;
// Sub-pixel rounding at an exact edge is not a clipped label.
const CLIP_TOLERANCE_PX = 0.5;

const findMap = () => {
  const here = (w) => {
    try {
      if (!w.L) return null;
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
let result = {problems, notes};

if (!found) {
  problems.push('no Leaflet map found - has the page loaded?');
} else {
  const {w, m} = found;
  const doc = w.document;
  const width = doc.documentElement.clientWidth || w.innerWidth;
  const view = w.__HEATMAP_VIEW;
  const mapRect = m.getContainer().getBoundingClientRect();
  // What a reader can see of the map: its box, cut to the frame's own width.
  const box = {left: Math.max(mapRect.left, 0), right: Math.min(mapRect.right, width),
               top: mapRect.top, bottom: mapRect.bottom};
  const overlaps = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;

  const labels = [];
  let stale = 0;
  m.eachLayer(layer => {
    if (!layer._icon || !layer.getLatLng) return;
    const d = [...layer._icon.querySelectorAll('div')]
      .find(x => x.style.fontSize === '14px' && !/^\d+$/.test(x.textContent.trim()));
    if (!d) return;
    const icon = layer._icon.getBoundingClientRect();
    const dom = d.getBoundingClientRect();
    const p = m.latLngToContainerPoint(layer.getLatLng());
    const left = mapRect.left + p.x + (dom.left - icon.left);
    const top = mapRect.top + p.y + (dom.top - icon.top);
    if (Math.abs(dom.left - left) > 1 || Math.abs(dom.top - top) > 1) stale++;
    labels.push({text: d.textContent.trim(),
                 r: {left, top, right: left + dom.width, bottom: top + dom.height,
                     width: dom.width}});
  });
  if (stale) notes.push(`${stale} label(s) had a STALE DOM position (page ` +
                        `${doc.visibilityState}) - measured from the map object instead`);

  const legend = doc.querySelector('details');
  const legendRect = legend.getBoundingClientRect();
  const legendText = legend.textContent;

  if (width < MIN_REAL_WIDTH) {
    problems.push(`UNMEASURED: the map frame is ${width}px wide, below ` +
                  `${MIN_REAL_WIDTH}px, so it is not laid out. Is the browser ` +
                  `pane collapsed? Bring it forward at a real size and reload.`);
  } else if (view && view.touched) {
    notes.push('UNMEASURED clipping: the map has been touched, so it shows the ' +
               'reader\'s view, not the render\'s. Reload and run again.');
  } else {
    for (const l of labels) {
      const cut = {left: box.left - l.r.left, right: l.r.right - box.right,
                   top: box.top - l.r.top, bottom: l.r.bottom - box.bottom};
      const sides = Object.entries(cut).filter(([, px]) => px > CLIP_TOLERANCE_PX);
      if (!sides.length) continue;
      const horiz = Math.max(cut.left, 0) + Math.max(cut.right, 0);
      const share = Math.min(100, Math.round(100 * horiz / l.r.width));
      problems.push(`clipped at width ${width}: ${l.text} - ` +
        sides.map(([s, px]) => `${Math.round(px)}px off the ${s}`).join(', ') +
        (horiz > 0 ? ` (${share}% of its ${Math.round(l.r.width)}px width)` : ''));
    }
  }
  if (view && width >= view.mapW) {
    notes.push(`width ${width} is at or above the map's layout width ` +
               `(${view.mapW}), so the phone fit was NOT exercised - run at 375 ` +
               `and 343 as well`);
  }
  for (const l of labels) {
    if (overlaps(l.r, legendRect)) problems.push(`under legend: ${l.text}`);
    if (!legendText.includes(l.text)) problems.push(`no legend row: ${l.text}`);
  }
  for (let i = 0; i < labels.length; i++)
    for (let j = i + 1; j < labels.length; j++)
      if (overlaps(labels[i].r, labels[j].r)) problems.push(`overlap: ${labels[i].text} / ${labels[j].text}`);

  // DO NOT assume the legend starts open. It does not at narrow widths: on a
  // fresh load at 854px, Chicago's and Boston's legends both report
  // `open: false` with no `open` attribute and a height of 37px. The previous
  // version of this check read the height as-found, called that `openH`, then
  // set `open = false` and compared - so it measured 37 against 37 and reported
  // "legend does not collapse" on EVERY city. A false failure, found 2026-09-21
  // while verifying nine maps before a deploy.
  //
  // So drive both states explicitly and restore whatever the page chose, since
  // the label/legend overlap checks above depend on the real rendered state.
  // The awaits are for reflow after setting `open`.
  const wasOpen = legend.open;
  legend.open = true;
  await new Promise(r => setTimeout(r, 250));
  const openH = legend.getBoundingClientRect().height;
  legend.open = false;
  await new Promise(r => setTimeout(r, 250));
  const closedH = legend.getBoundingClientRect().height;
  legend.open = wasOpen;
  await new Promise(r => setTimeout(r, 250));
  if (!(closedH < openH)) problems.push(`legend does not collapse (open ${Math.round(openH)}px, closed ${Math.round(closedH)}px)`);
  if (legend.open !== wasOpen) problems.push('legend state not restored');

  // Top-right buttons ("All cities" when embedded, and Dark Mode): inside the
  // visible viewport (it is position: fixed, unlike Leaflet's top-right
  // corner), not over a label, and it toggles and restores.
  const toggle = doc.getElementById('theme-toggle');
  let darkWorks = null;
  if (!toggle) problems.push('no theme toggle');
  else {
    const tr = (doc.getElementById('map-actions') || toggle).getBoundingClientRect();
    if (tr.left < 0 || tr.right > width || tr.top < 0) problems.push('theme toggle out of view');
    for (const l of labels) if (overlaps(l.r, tr)) problems.push(`under theme toggle: ${l.text}`);
    const was = doc.body.classList.contains('dark-base');
    toggle.click();
    const flipped = doc.body.classList.contains('dark-base') !== was;
    toggle.click();
    darkWorks = flipped && doc.body.classList.contains('dark-base') === was;
    if (!darkWorks) problems.push('theme toggle does not flip and restore');
  }
  result = {width, zoom: m.getZoom(), labels: labels.map(l => l.text), problems, notes,
            legendOpenHeight: Math.round(openH), legendClosedHeight: Math.round(closedH),
            darkToggleWorks: darkWorks};
}
JSON.stringify(result);
