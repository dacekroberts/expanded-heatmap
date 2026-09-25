// Is the front page's basemap credit ON TOP, or is something painted over it?
//
//   node scripts/check_macro_attribution.mjs [baseUrl] [widths]
//   node scripts/check_macro_attribution.mjs http://localhost:8822 375,768,1200
//   node scripts/check_macro_attribution.mjs https://<app>.streamlit.app/~/+ 375,1200
//
// WHY THIS EXISTS. CLAUDE.md makes the OSM credit a hard invariant, and
// "visible" is a fact about the RENDER. check_map_attribution.js hit-tests the
// city maps; nothing tested the Overview's macro map until 2026-09-24, when
// Rotterdam's deploy check saw a city dot land on the credit strip at 800x700.
// The cause was structural, not that one dot: deck.gl puts the whole Mapbox
// basemap - its credit included - in a `z-index: -1` layer beneath its own
// drawing canvas, so ANY dot or name pill could paint over the credit at any
// width. Whether one does on a given day depends on where the reader pans.
//
// So the question is paint order, not whether a dot happens to be there now:
// at five points along the credit, the TOPMOST element must be the credit
// itself. A transparent canvas above it still counts as covering it, because
// that canvas draws whatever lands there.
//
// THE WHOLE STACK, NOT JUST THE TOP ELEMENT. Two traps, both hit while
// writing this:
//   - deck.gl's canvas is `pointer-events: none`, and document.elementFromPoint
//     skips such elements - it reports the credit as topmost while the canvas
//     paints over it. So every element in the chart is made hit-testable for
//     the duration of the measurement.
//   - deck.gl also spreads a transparent full-map container over everything
//     (`div.fill`, which holds the hover tooltip). It paints nothing, and a
//     check that counted it failed every width for no reason.
// So the stack above the credit is read with elementsFromPoint and only what
// CAN PAINT there counts: a canvas (it draws whatever lands on it), an image,
// or an element with a visible background or its own text.
//
// The deployed app serves its page inside an iframe; pass the `/~/+` URL, which
// serves the app document directly. Exit status is non-zero on any failure.
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const EDGE = process.env.EDGE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const base = (process.argv[2] || 'http://localhost:8822').replace(/[/]$/, '');
const widths = (process.argv[3] || '375,768,1200').split(',').map(Number);
const H = 1000;
const PORT = +(process.env.CDP_PORT || 9334);
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const profileDir = join(tmpdir(), 'heatmap-macro-attribution');
mkdirSync(profileDir, { recursive: true });
const edge = spawn(EDGE, ['--headless=new', `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${profileDir}`, `--window-size=1200,${H}`, '--no-first-run',
  '--disable-extensions', 'about:blank'], { stdio: 'ignore' });

let targets;
for (let i = 0; i < 50; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); break; }
  catch (e) { await sleep(200); }
}
const page = targets.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map();
ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
});
const send = (method, params = {}) => new Promise((res, rej) => {
  const i = ++id; pending.set(i, (m) => m.error ? rej(new Error(method + ': ' + JSON.stringify(m.error))) : res(m.result));
  ws.send(JSON.stringify({ id: i, method, params }));
});
const evalJs = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
  return r.result.value;
};

await send('Page.enable'); await send('Runtime.enable'); await send('DOM.enable');

// Evaluated in the page: for each point, what above the credit can paint there.
const STACK = (pts) => `(() => {
  const host = document.querySelector('[data-testid="stDeckGlJsonChart"]');
  const credit = host.querySelector('.mapboxgl-ctrl-attrib');
  const force = document.createElement('style');
  force.textContent = '[data-testid="stDeckGlJsonChart"] * { pointer-events: auto !important; }';
  document.head.appendChild(force);
  const name = (el) => {
    const cls = typeof el.className === 'string' ? el.className.trim().split(/ +/).slice(0, 2).join('.') : '';
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (cls ? '.' + cls : '');
  };
  const paints = (el) => {
    if (el.tagName === 'CANVAS' || el.tagName === 'IMG') return true;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const bg = cs.backgroundColor;
    if (bg && bg !== 'transparent' && !/rgba\\([^)]*,\\s*0\\)$/.test(bg)) return true;
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return true;
    return [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  };
  try {
    return ${JSON.stringify(pts)}.map(([x, y]) => {
      const stack = document.elementsFromPoint(x, y);
      const i = stack.findIndex(el => credit.contains(el));
      if (i < 0) return ['credit not in the stack at this point'];
      return stack.slice(0, i).filter(el => !credit.contains(el) && paints(el)).map(name);
    });
  } finally { force.remove(); }
})()`;

const problems = [];
for (const w of widths) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: H, deviceScaleFactor: 1, mobile: w < 768 });
  await send('Page.navigate', { url: `${base}/?attribution_check=${w}_${Date.now()}` });
  let rect = null;
  for (let i = 0; i < 60 && !rect; i++) {
    await sleep(500);
    rect = await evalJs(`(() => {
      const host = document.querySelector('[data-testid="stDeckGlJsonChart"]');
      const a = host && host.querySelector('.mapboxgl-ctrl-attrib');
      if (!a || !host.querySelector('#deckgl-overlay')) return null;
      host.scrollIntoView({ block: 'center' });
      const r = a.getBoundingClientRect();
      return r.width > 0 ? { x: r.left, y: r.top, w: r.width, h: r.height } : null;
    })()`);
  }
  if (!rect) { problems.push(`${w}px: no visible macro-map credit found within 30 s`); continue; }
  await sleep(1500);
  rect = await evalJs(`(() => { const r = document.querySelector('[data-testid="stDeckGlJsonChart"] .mapboxgl-ctrl-attrib').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; })()`);
  const pts = [0.1, 0.3, 0.5, 0.7, 0.9].map(f =>
    [Math.round(rect.x + rect.w * f), Math.round(rect.y + rect.h / 2)]);
  const above = await evalJs(STACK(pts));
  const covered = above.filter(a => a.length);
  const what = [...new Set(covered.flat())];
  console.log(`${w}px  credit ${Math.round(rect.w)}x${Math.round(rect.h)} at (${Math.round(rect.x)},${Math.round(rect.y)})  ` +
              (covered.length ? `painted over at ${covered.length} of 5 points by ${what.join(', ')}` : 'on top at all 5 points'));
  if (covered.length) problems.push(`${w}px: ${covered.length} of 5 points along the credit have ${what.join(', ')} able to paint over it`);
}
ws.close(); edge.kill();

if (problems.length) {
  console.log(`\nPROBLEMS ${problems.length}`);
  for (const p of problems) console.log('  ' + p);
  process.exit(1);
}
console.log(`\nPROBLEMS 0 - the macro map's basemap credit is topmost at every point tested, at ${widths.join(', ')} px`);
