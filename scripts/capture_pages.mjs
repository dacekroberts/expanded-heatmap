// Capture app pages for a review lane: a screenshot, the page's text (the
// Streamlit page and the map inside it) and its console errors, for every
// page x width x theme. One headless Edge, one page at a time.
//
//   node scripts/capture_pages.mjs --out <dir> [--base http://localhost:8831]
//        [--pages Overview,About_the_Data,Edmonton_Heatmap | --pages all | --pages cities]
//        [--widths 375,768,1200] [--themes light,dark] [--settle 15] [--cdp 9341]
//        [--tall]
//
// Writes <out>/<page>_<width>_<theme>.png and .txt, and <out>/errors.json
// (console errors and exceptions per capture; an empty list is the pass).
// `--pages all` reads every page from docs/rendered_surfaces.md (the Overview,
// the fixed pages and every city page); `cities` only the city pages.
// `--tall` sizes the viewport to the whole page (up to 8000 px) so one image
// holds everything; without it the image is the first screen, as a reader
// sees it.
//
// WHY IT EXISTS (review lesson 4, docs/review_lanes_2026-09-30.md): each lane
// of the mega-review wrote its own click scripts, and one sweep drove three
// browsers at once and measured 7.43 GB against 3 GB declared. This drives ONE
// Edge, sequentially: declare --peak-gb 1.5 to scripts/heavy_job.py. Give each
// lane its own --cdp port (docs/review_lane_kit.md): two captures on one port
// fight over the same browser.
//
// THEME: the app follows the system theme, so the capture emulates
// prefers-color-scheme rather than clicking the theme button (which would
// persist in the profile). Each capture loads fresh: a resized page measures a
// stale layout (scripts/check_map_view.js's rule).
import { spawn } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const arg = (name, dflt) => {
  const i = process.argv.indexOf('--' + name);
  return i > 0 && i + 1 < process.argv.length ? process.argv[i + 1] : dflt;
};
const flag = (name) => process.argv.includes('--' + name);

const EDGE = process.env.EDGE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const base = arg('base', 'http://localhost:8501').replace(/[/]$/, '');
const out = arg('out');
if (!out) { console.error('--out <dir> is required (a scratchpad folder, never the repo)'); process.exit(2); }
const widths = arg('widths', '375,768,1200').split(',').map(Number);
const themes = arg('themes', 'light,dark').split(',');
const settle = +arg('settle', '15') * 1000;
const PORT = +arg('cdp', '9341');
const tall = flag('tall');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// Page names are given WITHOUT a leading slash (Overview, About_the_Data,
// Edmonton_Heatmap): Git Bash rewrites an argument that starts with "/" into a
// Windows path ("/" became C:\...\git\), so a slash form is accepted but never
// needed.
function norm(p) {
  if (/[:\\]/.test(p)) {
    console.error(`page ${JSON.stringify(p)} looks like a path Git Bash rewrote: pass page names without the leading slash`);
    process.exit(2);
  }
  p = p.replace(/^\//, '');
  return p === '' || p === 'Overview' ? '/' : '/' + p;
}

function pageList(spec) {
  if (spec !== 'all' && spec !== 'cities') return spec.split(',').map(norm);
  const doc = readFileSync(new URL('../docs/rendered_surfaces.md', import.meta.url), 'utf8');
  const city = [...doc.matchAll(/^\| `(\/[A-Za-z0-9_]+_Heatmap)` \|/gm)].map(m => m[1]);
  if (spec === 'cities') return city;
  const fixed = [...doc.matchAll(/^\| `(\/[A-Za-z0-9_]+)` \| `app\/pages\/2\d\d_/gm)].map(m => m[1]);
  return ['/', ...fixed, ...city];
}
const pages = pageList(arg('pages', 'Overview'));
mkdirSync(out, { recursive: true });

const profileDir = join(tmpdir(), `heatmap-capture-${PORT}`);
rmSync(profileDir, { recursive: true, force: true });
mkdirSync(profileDir, { recursive: true });
const edge = spawn(EDGE, ['--headless=new', `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${profileDir}`, '--window-size=1200,900', '--no-first-run',
  '--disable-extensions', 'about:blank'], { stdio: 'ignore' });

let targets;
for (let i = 0; i < 50; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); break; }
  catch (e) { await sleep(200); }
}
if (!targets) { console.error(`no browser on CDP port ${PORT}`); edge.kill(); process.exit(1); }
const target = targets.find(t => t.type === 'page');
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); let errors = [];
ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); return; }
  if (msg.method === 'Runtime.exceptionThrown') {
    errors.push('exception: ' + (msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text));
  } else if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
    errors.push('console: ' + msg.params.args.map(a => a.value ?? a.description ?? '').join(' '));
  } else if (msg.method === 'Log.entryAdded' && msg.params.entry.level === 'error'
             // The live app's /~/+ route: Streamlit probes _stcore/health and
             // host-config under the page's sub-path, which 404s there and
             // only there (measured 2026-10-01). Noise, not a page defect.
             && !/\/_stcore\/(health|host-config)$/.test(msg.params.entry.url || '')) {
    errors.push('log: ' + msg.params.entry.text + (msg.params.entry.url ? ' ' + msg.params.entry.url : ''));
  }
});
const send = (method, params = {}) => new Promise((res, rej) => {
  const i = ++id; pending.set(i, (m) => m.error ? rej(new Error(method + ': ' + JSON.stringify(m.error))) : res(m.result));
  ws.send(JSON.stringify({ id: i, method, params }));
});
const evalJs = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  return r.exceptionDetails ? null : r.result.value;
};
await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');

// The page's own text, then each same-origin frame's (the map: its legend,
// labels and notices), so a lane can read the prose without a screenshot.
const TEXT = `(() => {
  const parts = [document.body ? document.body.innerText : ''];
  const walk = (doc, depth) => {
    for (const f of doc.querySelectorAll('iframe')) {
      try {
        const d = f.contentDocument;
        if (d && d.body) { parts.push('\\n--- frame ' + depth + ' ---\\n' + d.body.innerText); walk(d, depth + 1); }
      } catch (e) { parts.push('\\n--- frame ' + depth + ': cross-origin, not read ---'); }
    }
  };
  walk(document, 1);
  return parts.join('\\n');
})()`;
const HEIGHT = `(() => {
  const main = document.querySelector('[data-testid="stMain"], section.main, [data-testid="stAppViewContainer"]');
  return Math.max(document.documentElement.scrollHeight, main ? main.scrollHeight : 0);
})()`;

const report = {};
const name = (p) => (p === '/' ? 'Overview' : p.replace(/^\//, ''));
for (const p of pages) {
  for (const w of widths) {
    for (const theme of themes) {
      const key = `${name(p)}_${w}_${theme}`;
      errors = [];
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 768 });
      await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: theme }] });
      await send('Page.navigate', { url: base + p });
      await sleep(settle);
      if (tall) {
        const h = Math.min(8000, (await evalJs(HEIGHT)) || 900);
        await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: w < 768 });
        await sleep(2000);
      }
      const shot = await send('Page.captureScreenshot', { format: 'png' });
      writeFileSync(join(out, key + '.png'), Buffer.from(shot.data, 'base64'));
      writeFileSync(join(out, key + '.txt'), (await evalJs(TEXT)) || '');
      report[key] = errors;
      console.log(`${key}: ${errors.length ? errors.length + ' error(s)' : 'ok'}`);
    }
  }
}
writeFileSync(join(out, 'errors.json'), JSON.stringify(report, null, 1));
const bad = Object.entries(report).filter(([, e]) => e.length);
console.log(`\n${Object.keys(report).length} capture(s) in ${out}; ${bad.length} with console errors (errors.json)`);
ws.close(); edge.kill();
process.exit(0);
