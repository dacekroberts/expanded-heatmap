// Zoom-lag profiler: how long a map takes to settle after a wheel roll, a +/-
// click or a cluster click, measured the way a reader produces them.
//
//   node scripts/profile_zoom.mjs <baseUrl> <city,city> [reps] [scenario,...]
//   e.g. node scripts/profile_zoom.mjs http://localhost:8813 paris,toulouse 3
//
// Serve outputs/ first (the `heatmap-static` preview). Prints one JSON line per
// run on stdout and a median table per (city, scenario) on stderr. Written
// 2026-09-23 for the wheel/cluster lag fix; DECISIONS.md, "Wheel zoom stops
// discarding notches; cluster animation off", holds what it measured.
//
// WHY HEADLESS EDGE OVER CDP AND NOT THE BROWSER PANE. A hidden pane pauses
// animation frames, so no zoom animation ever completes there and every run
// records nothing. And a synthetic WheelEvent dispatched from page script is
// not what a mouse sends: Input.dispatchMouseEvent produces TRUSTED input that
// goes through the browser's own wheel path.
//
// WHAT "SETTLE" MEANS: the time from the first input to the last map event
// handled (profile_zoom_page.js times every map.fire). A wheel notch the map
// DISCARDS fires nothing, so compare `zooms` (the zoom after each zoomend), not
// only the time - the defect this was written for made the wheel look fast by
// doing less.
//
// LEVER=<file.js> evaluates a script in the page before profiling, to try an
// override without re-rendering 25 maps. The browser profile goes to the OS
// temp directory, never the repo.
import { spawn } from 'node:child_process';
import { readFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const EDGE = process.env.EDGE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const base = process.argv[2] || 'http://localhost:8813';
const cities = (process.argv[3] || 'paris,toulouse').split(',');
const reps = +(process.argv[4] || 3);
const only = process.argv[5] ? process.argv[5].split(',') : null;
const W = +(process.env.VW || 1280), H = +(process.env.VH || 900);
const PROF = readFileSync(join(HERE, 'profile_zoom_page.js'), 'utf8');
const LEVER = process.env.LEVER ? readFileSync(process.env.LEVER, 'utf8') : null;
const PORT = +(process.env.CDP_PORT || 9333);
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const profileDir = join(tmpdir(), 'heatmap-profile-zoom');
mkdirSync(profileDir, { recursive: true });
const edge = spawn(EDGE, ['--headless=new', `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${profileDir}`, `--window-size=${W},${H}`, '--no-first-run',
  '--disable-extensions', 'about:blank'], { stdio: 'ignore' });

let targets;
for (let i = 0; i < 50; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); break; }
  catch (e) { await sleep(200); }
}
const page = targets.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); const waiters = [];
ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  else if (msg.method) waiters.filter(w => w.method === msg.method).forEach(w => w.fn(msg));
});
const send = (method, params = {}) => new Promise((res, rej) => {
  const i = ++id; pending.set(i, (m) => m.error ? rej(new Error(method + ': ' + JSON.stringify(m.error))) : res(m.result));
  ws.send(JSON.stringify({ id: i, method, params }));
});
const once = (method) => new Promise(res => { const w = { method, fn: (m) => { waiters.splice(waiters.indexOf(w), 1); res(m); } }; waiters.push(w); });
const evalJs = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
  return r.result.value;
};

await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });

async function fresh(url) {
  const loaded = once('Page.loadEventFired');
  await send('Page.navigate', { url });
  await loaded;
  await sleep(3500);
  if (LEVER) await evalJs(LEVER);
  await evalJs(PROF);
  return evalJs('__prof.targets()');
}
const mouse = (type, x, y, extra = {}) => send('Input.dispatchMouseEvent', { type, x, y, ...extra });
async function click(x, y) {
  await mouse('mouseMoved', x, y);
  await mouse('mousePressed', x, y, { button: 'left', clickCount: 1 });
  await mouse('mouseReleased', x, y, { button: 'left', clickCount: 1 });
}
// deltaY 100 is one notch of a Windows mouse wheel as Chrome/Edge report it.
async function wheel(x, y, n, gap, dy = -100) {
  await mouse('mouseMoved', x, y);
  for (let i = 0; i < n; i++) {
    await mouse('mouseWheel', x, y, { deltaX: 0, deltaY: dy });
    if (i < n - 1) await sleep(gap);
  }
}

const SCEN = {
  'button+1': async (t) => { await click(t.zoomIn.x, t.zoomIn.y); },
  'button+3': async (t) => { for (let i = 0; i < 3; i++) { await click(t.zoomIn.x, t.zoomIn.y); await sleep(350); } },
  'wheel1': async (t) => { await wheel(t.center.x, t.center.y, 1, 0); },
  'wheel3fast': async (t) => { await wheel(t.center.x, t.center.y, 3, 25); },
  'wheel5': async (t) => { await wheel(t.center.x, t.center.y, 5, 60); },
  // Batches just past Leaflet's 40 ms debounce: each can fire before the
  // previous zoom's animation has started on the next frame.
  'wheel45': async (t) => { await wheel(t.center.x, t.center.y, 5, 45); },
  'wheelslow':async (t) => { await wheel(t.center.x, t.center.y, 4, 300); },
  // Many small pixel deltas, the shape a trackpad sends.
  'trackpad': async (t) => { await wheel(t.center.x, t.center.y, 30, 16, -8); },
  'wheel5out': async (t) => { await wheel(t.center.x, t.center.y, 5, 60, 100); },
  // The largest cluster that is TOPMOST at its centre - see targets().
  'cluster': async (t) => { const c = t.clusters[0]; if (!c) throw new Error('no cluster'); await click(c.x, c.y); },
};

const results = [];
for (const city of cities) {
  for (const [name, fn] of Object.entries(SCEN)) {
    if (only && !only.includes(name)) continue;
    for (let r = 0; r < reps; r++) {
      const t = await fresh(`${base}/${city}/heatmap.html`);
      await evalJs('__prof.begin()');
      await fn(t);
      const res = await evalJs('__prof.end(900)');
      const after = await evalJs('__prof.targets()');
      res.city = city; res.scen = name; res.rep = r;
      res.clusterN = name === 'cluster' ? t.clusters[0].n : undefined;
      res.touched = after.view && after.view.touched;
      res.corrections = after.view && after.view.corrections;
      results.push(res);
      console.log(JSON.stringify(res));
    }
  }
}
ws.close(); edge.kill();

const med = (xs) => { const s = [...xs].sort((a, b) => a - b); return s.length ? s[Math.floor(s.length / 2)] : null; };
const groups = new Map();
for (const r of results) {
  const k = `${r.city} ${r.scen}`;
  if (!groups.has(k)) groups.set(k, []);
  groups.get(k).push(r);
}
console.error('city scenario | zooms (first run) | settle ms | heat redraws/ms | longest task ms | zoomend ms | moveend ms');
for (const [k, rs] of groups) {
  const ev = (e, i) => med(rs.map(r => (r.events[e] || [0, 0, 0])[i]));
  console.error(`${k} | ${JSON.stringify(rs[0].zooms)} | ${med(rs.map(r => r.settledMs))} | ` +
    `${med(rs.map(r => r.heat[0]))}/${med(rs.map(r => r.heat[1]))} | ` +
    `${med(rs.map(r => Math.max(0, ...r.longtasks)))} | ${ev('zoomend', 1)} | ${ev('moveend', 1)}`);
}
process.exit(0);
