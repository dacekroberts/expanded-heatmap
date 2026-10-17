// Every station and every transit line DRAWN on a searched map is found by
// that map's own search box (owner, 2026-10-13: the floor for the place-search
// rollout, "all drawn lines and stations are searchable (bare minimum)").
//
//   node scripts/check_map_search.js [<city> ...] [--json <file>]
//                                    [--browser <exe>] [--list <n>] [--query <text> ...]
//
// No city named: every city with an index in app/static/places/. Exits 1 when
// any drawn station or line is not found, or a searched map could not be
// measured; 0 otherwise. A map with no search block is said so and skipped.
// --query (repeatable) prints what the page's search() returns for that text
// on each map, kind and name, wide-screen cap; it decides nothing.
//
// WHAT IT ASKS. A drawn station is typed as the map labels it (the <b> of its
// tooltip), a drawn line as its legend row reads. Each name goes through the
// page's REAL search(): the function the box calls, with the index loaded, the
// index's languages switched on and OpenStreetMap's stations linked. Nothing
// of the matcher is copied here, so a change to it is measured, not mirrored.
//
// THREE OUTCOMES A NAME.
//   found      its own station or line is among the results search() returns.
//   warning    the matcher takes it, but it ranks past the cap on the map's
//              own results (caps().own), so the box does not show it; or it
//              shows on a wide screen and ranks past a phone's shorter cap.
//              The rank is reported.
//   not found  the matcher does not return it at all. This fails the check.
//
// INDEPENDENT, NOT SELF-REPORTED (the rule of check_map_view.js). The drawn
// stations and lines are read from the Leaflet layers and the legend's rows,
// not from the search's own list: a station the search never listed (no
// tooltip, a legend row with no polyline) is a miss, not an absence.
//
// WHY NODE AND A DEBUGGING PORT, NOT THE JAVASCRIPT TOOL. check_map_view.js
// is pasted into the page. The search code is one closure
// (pipeline/map_common.py, PLACE_SEARCH_SCRIPT) and exposes nothing on
// window, so page script cannot reach search(). The DevTools protocol can:
// the input's "input" listener is render(), and its [[Scopes]] hold search,
// hits, words, data and the rest. So this starts a headless Chromium browser
// (Edge or Chrome, no npm package), reads those scopes and calls the
// functions in the page. If the search block ever renames them, the check
// says which name it could not find; it never guesses.
//
// THE PAGE NEEDS ITS INDEX, AND AT THE SITE'S PATH. The map fetches
// /app/static/places/<city>.json; without it the box answers from the map's
// own names only, with no language words and no linked names, which is not
// the search a reader gets. A server inside this process serves exactly two
// things, on 127.0.0.1 and an ephemeral port, and closes at exit:
// outputs/<city>/heatmap.html and app/static/places/. Images (basemap tiles)
// from any other host are refused; the map's scripts load as usual, so the
// machine needs the network a reader's browser would.
//
// No selftest: check_map_view.js has none, and a browser-free one would have
// to copy the matcher this check exists to call. Not in check_all.py (the
// pre-push hook has no browser).
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const http = require("http");
const { spawn } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const PLACES = path.join(ROOT, "app", "static", "places");
const OUTPUTS = path.join(ROOT, "outputs");
// The map's own results a phone shows is read from the page (caps()) at this
// width; the search itself runs at the wide one.
const WIDE = [1280, 900], PHONE = [375, 812];
const LOAD_MS = 180000, INDEX_MS = 90000, CALL_MS = 600000;
const NEEDED = ["search", "hits", "words", "isOwn", "STOP", "data"];
let QUERIES = [];
const OPTIONAL = ["JUNK_Q", "caps", "STATION_COLOR", "byIndex", "NEAR_M", "LINK_M"];

function usage(msg) {
  if (msg) console.error(msg);
  console.error("usage: node scripts/check_map_search.js [<city> ...] [--json <file>] " +
                "[--browser <exe>] [--list <n>] [--query <text> ...]");
  process.exit(2);
}

function parseArgs(argv) {
  const a = { cities: [], json: null, browser: null, list: 15, queries: [] };
  for (let i = 0; i < argv.length; i++) {
    const v = argv[i];
    if (v === "--json") a.json = argv[++i] || usage("--json needs a file");
    else if (v === "--browser") a.browser = argv[++i] || usage("--browser needs a path");
    else if (v === "--list") a.list = Number(argv[++i]);
    else if (v === "--query") a.queries.push(argv[++i] || usage("--query needs a text"));
    else if (v.startsWith("--")) usage("unknown option " + v);
    else a.cities.push(v);
  }
  if (!(a.list >= 0)) usage("--list needs a number");
  return a;
}

function searchedCities() {
  return fs.readdirSync(PLACES).filter((f) => f.endsWith(".json"))
    .map((f) => f.slice(0, -5)).sort();
}

function findBrowser(given) {
  if (given) return given;
  const pf = [process.env["ProgramFiles(x86)"], process.env.ProgramFiles, process.env.LOCALAPPDATA]
    .filter(Boolean);
  const cands = [];
  pf.forEach((p) => {
    cands.push(path.join(p, "Microsoft", "Edge", "Application", "msedge.exe"));
    cands.push(path.join(p, "Google", "Chrome", "Application", "chrome.exe"));
  });
  cands.push("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
             "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
             "/usr/bin/microsoft-edge");
  return cands.find((c) => fs.existsSync(c)) || null;
}

// The two things the page asks this host for, and nothing else of the tree.
const MAP_PATH = /^\/([a-z0-9_]+)\/heatmap\.html$/;
const INDEX_PATH = /^\/app\/static\/places\/((?:crossings\/|streets\/)?[a-z0-9_]+\.json)$/;
function startServer() {
  const server = http.createServer((req, res) => {
    const p = decodeURIComponent((req.url || "").split("?")[0]);
    let file = null, type = "application/json";
    let m = MAP_PATH.exec(p);
    if (m) { file = path.join(OUTPUTS, m[1], "heatmap.html"); type = "text/html; charset=utf-8"; }
    else if ((m = INDEX_PATH.exec(p))) file = path.join(PLACES, m[1]);
    if (!file || !fs.existsSync(file)) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-store" });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => server.listen(0, "127.0.0.1", () => resolve(server)));
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// A minimal DevTools protocol client over the browser's one socket.
class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.next = 1;
    this.waiting = new Map();
    this.handlers = [];
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.waiting.has(msg.id)) {
        const w = this.waiting.get(msg.id);
        this.waiting.delete(msg.id);
        clearTimeout(w.timer);
        if (msg.error) w.reject(new Error(w.method + ": " + msg.error.message));
        else w.resolve(msg.result);
      } else if (msg.method) {
        this.handlers.forEach((h) => h(msg));
      }
    });
  }
  send(method, params, sessionId, timeout) {
    const id = this.next++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.waiting.delete(id);
        reject(new Error(method + ": no answer in " + (timeout || 60000) + " ms"));
      }, timeout || 60000);
      this.waiting.set(id, { resolve, reject, timer, method });
      const msg = { id, method, params: params || {} };
      if (sessionId) msg.sessionId = sessionId;
      this.ws.send(JSON.stringify(msg));
    });
  }
}

async function startBrowser(exe) {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "check_map_search_"));
  const child = spawn(exe, [
    "--headless=new", "--remote-debugging-port=0", "--user-data-dir=" + profile,
    "--no-first-run", "--no-default-browser-check", "--disable-extensions",
    "--disable-background-networking", "--disable-sync", "--mute-audio",
    "--window-size=" + WIDE.join(","), "about:blank",
  ], { stdio: "ignore" });
  const portFile = path.join(profile, "DevToolsActivePort");
  let lines = null;
  for (let i = 0; i < 150 && !lines; i++) {
    await sleep(200);
    if (fs.existsSync(portFile)) {
      const t = fs.readFileSync(portFile, "utf8").trim().split(/\r?\n/);
      if (t.length >= 2) lines = t;
    }
  }
  if (!lines) {
    child.kill();
    throw new Error("the browser opened no debugging port: " + exe);
  }
  const ws = new WebSocket("ws://127.0.0.1:" + lines[0] + lines[1]);
  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve);
    ws.addEventListener("error", () => reject(new Error("no socket to the browser")));
  });
  return { child, profile, cdp: new Cdp(ws), ws };
}

async function stopBrowser(b) {
  try { await b.cdp.send("Browser.close", {}, null, 5000); } catch (e) { /* closing anyway */ }
  try { b.ws.close(); } catch (e) { /* closed */ }
  await sleep(500);
  try { b.child.kill(); } catch (e) { /* gone */ }
  for (let i = 0; i < 10; i++) {
    try { fs.rmSync(b.profile, { recursive: true, force: true }); break; }
    catch (e) { await sleep(500); }
  }
}

// RUNS IN THE PAGE. Arguments are the page's own objects, taken from the
// search closure. Returns plain data.
function measureInPage(search, hits, words, isOwn, STOP, data, JUNK_Q, STATION_COLOR) {
  var L = window.L;
  var map = Object.values(window).find(function (v) { return v && v instanceof L.Map; });
  var own = data.filter(isOwn);
  var stations = [], lines = [], seen = {};
  // Drawn stations: the station layer's markers (render_heatmap draws both the
  // filled and the hollow no-data ones in the station colour).
  map.eachLayer(function (l) {
    if (!(l instanceof L.CircleMarker) || l instanceof L.Circle) return;
    if (l.options.color !== STATION_COLOR) return;
    var ll = l.getLatLng(), name = "";
    if (l.getTooltip()) {
      var c = l.getTooltip().getContent(), tmp = document.createElement("div");
      tmp.innerHTML = typeof c === "string" ? c : (c && c.innerHTML) || "";
      name = ((tmp.querySelector("b") || tmp).textContent || "").trim();
    }
    var key = name + "@" + ll.lat + "," + ll.lng;
    if (seen[key]) return;
    seen[key] = 1;
    stations.push({ kind: "station", name: name, lat: ll.lat, lon: ll.lng,
      item: own.find(function (d) {
        return d.kind === "mapstation" && d.name === name && d.lat === ll.lat && d.lon === ll.lng;
      }) || null });
  });
  document.querySelectorAll(".map-legend .hm-line-row[data-line]").forEach(function (row) {
    lines.push({ kind: "line", name: (row.textContent || "").trim(),
      item: own.find(function (d) { return d.kind === "line" && d.row === row; }) || null });
  });

  function ask(t) {
    var r = { kind: t.kind, name: t.name, status: "not_found", rank: null, why: null };
    if (t.lat !== undefined) { r.lat = t.lat; r.lon = t.lon; }
    if (!t.name) { r.why = "drawn with no name to type"; return r; }
    if (!t.item) { r.why = "not in the search's own list (no tooltip, or a legend row with no polyline)"; return r; }
    if (JUNK_Q && JUNK_Q.test(t.name)) { r.why = "the box refuses the name as an error value"; return r; }
    var res = search(t.name), at = res.indexOf(t.item);
    if (at >= 0) {
      r.status = "found";
      r.rank = at + 1;
      // Linked names, for reading a miss elsewhere against a hit here.
      if (t.item.names.length > 1) r.linked = t.item.names.length - 1;
      return r;
    }
    var qs = words(t.name).filter(function (w) { return !STOP[w]; });
    r.words = qs;
    if (!qs.length) { r.why = "every word of the name is one the matcher drops"; return r; }
    var lost = qs.filter(function (w) { return !hits(t.item, [w]); });
    if (lost.length) { r.why = "the matcher does not find these words in the name"; r.lost = lost; return r; }
    hits(t.item, qs);
    if (t.item._weak) { r.why = "matched inside a word only, which the map's own results leave out"; return r; }
    // Matched and ranked, but past the cap: its place among the map's own
    // matches, by the score search() has just given each.
    var mine = data.filter(function (d) { return isOwn(d) && hits(d, qs) && !d._weak; });
    mine.sort(function (a, b) { return a._s - b._s; });
    r.status = "past_cap";
    r.rank = mine.indexOf(t.item) + 1;
    r.of = mine.length;
    r.ahead = mine.slice(0, 3).map(function (d) { return d.name; });
    return r;
  }
  return JSON.stringify({ stations: stations.map(ask), lines: lines.map(ask),
                          own_stations: own.filter(function (d) { return d.kind === "mapstation"; }).length,
                          own_lines: own.filter(function (d) { return d.kind === "line"; }).length,
                          rows: data.length });
}

// RUNS IN THE PAGE. The index's OWN station rows, which the drawn-name test
// above never reaches. A row joined to a pin is not listed; one left listed
// is labeled "Station not on this map". Fails a listed row within NEAR_M
// (150 m where the page names none) of a drawn pin: there it is the pin's
// own stop under another spelling. Warns where a joined row's own name,
// typed, does not show the pin holding it. Joins farther than NEAR_M are
// listed for reading (Philadelphia's "Girard Avenue & 5th Street" opened
// "Girard Av & 7th St", 243 m away). A row whose name no pin within LINK_M
// holds was dropped as a far duplicate (link() in the search block).
function indexStationsInPage(search, data, byIndex, NEAR_M, LINK_M) {
  var near = NEAR_M || 150, link = LINK_M || 300;
  var pins = data.filter(function (d) { return d.kind === "mapstation"; });
  function m(a, b) {
    var k = Math.cos((a.lat + b.lat) / 2 * Math.PI / 180);
    return Math.sqrt(Math.pow((a.lat - b.lat) * 110540, 2) + Math.pow((a.lon - b.lon) * 111320 * k, 2));
  }
  var out = { rows: 0, listed: 0, joined: 0, dropped: 0, near_listed: [], unfound: [], joined_far: [] };
  var listed = new Set(data);
  byIndex.forEach(function (r) {
    if (r.kind !== "station") return;
    out.rows += 1;
    if (listed.has(r)) {
      out.listed += 1;
      var best = null, bm = Infinity;
      pins.forEach(function (p) { var x = m(r, p); if (x < bm) { bm = x; best = p; } });
      if (best && bm <= near) out.near_listed.push({ name: r.name, pin: best.name, m: Math.round(bm) });
      return;
    }
    var holder = null, hm = Infinity;
    pins.forEach(function (p) {
      if (p.names.indexOf(r.name) < 0) return;
      var x = m(r, p);
      if (x < hm) { hm = x; holder = p; }
    });
    if (!holder || hm > link) { out.dropped += 1; return; }
    out.joined += 1;
    if (hm > near) out.joined_far.push({ name: r.name, pin: holder.name, m: Math.round(hm) });
    if (search(r.name).indexOf(holder) < 0) out.unfound.push({ name: r.name, pin: holder.name });
  });
  return JSON.stringify(out);
}

// RUNS IN THE PAGE. The box itself, once a city: the name typed into the
// input, and the pills it shows. Holds the closure's search() to what a
// reader sees.
function probeBoxInPage(name) {
  var input = document.querySelector(".hm-search-input");
  input.value = name;
  input.dispatchEvent(new Event("input", { bubbles: true }));
  var pills = Array.prototype.map.call(document.querySelectorAll(".hm-search-pill"),
    function (p) { return (p.textContent || "").trim(); });
  input.value = "";
  input.dispatchEvent(new Event("input", { bubbles: true }));
  return JSON.stringify(pills);
}

async function checkCity(b, origin, city) {
  const out = { city, status: "ok", problems: [], warnings: [] };
  const html = path.join(OUTPUTS, city, "heatmap.html");
  if (!fs.existsSync(html)) {
    out.status = "error";
    out.problems.push("no outputs/" + city + "/heatmap.html");
    return out;
  }
  if (!fs.readFileSync(html, "utf8").includes("hm-search-input")) {
    out.status = "skipped";
    out.note = "the map carries no search block";
    return out;
  }
  const cdp = b.cdp;
  const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
  const S = (method, params, timeout) => cdp.send(method, params, sessionId, timeout);
  const evalJs = async (expression) => {
    const r = await S("Runtime.evaluate", { expression, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + " in " + expression);
    return r.result.value;
  };
  const size = (wh) => S("Emulation.setDeviceMetricsOverride",
    { width: wh[0], height: wh[1], deviceScaleFactor: 1, mobile: false });
  const onEvent = (msg) => {
    if (msg.sessionId !== sessionId || msg.method !== "Fetch.requestPaused") return;
    const local = msg.params.request.url.startsWith(origin + "/") ||
                  msg.params.request.url.startsWith("data:");
    cdp.send(local ? "Fetch.continueRequest" : "Fetch.failRequest",
      local ? { requestId: msg.params.requestId }
            : { requestId: msg.params.requestId, errorReason: "BlockedByClient" },
      sessionId).catch(() => {});
  };
  cdp.handlers.push(onEvent);
  try {
    await S("Page.enable");
    await S("Runtime.enable");
    await S("Fetch.enable", { patterns: [{ urlPattern: "*", resourceType: "Image" }] });
    await size(WIDE);
    await S("Page.navigate", { url: origin + "/" + city + "/heatmap.html" });

    let t0 = Date.now(), ready = false;
    while (Date.now() - t0 < LOAD_MS && !ready) {
      await sleep(500);
      try {
        ready = await evalJs("document.readyState === 'complete' && " +
                             "!!document.querySelector('.hm-search-btn')");
      } catch (e) { ready = false; }
    }
    if (!ready) throw new Error("the page did not finish loading with a search box in " +
                                LOAD_MS / 1000 + " s (its scripts need the network)");

    // Opening the box is what loads the index (open() in the search block).
    await evalJs("document.querySelector('.hm-search-btn').click()");
    t0 = Date.now();
    let loaded = null;
    while (Date.now() - t0 < INDEX_MS && loaded === null) {
      await sleep(300);
      loaded = await evalJs("(function () { var b = document.querySelector('.hm-search');" +
        " if (b.hasAttribute('data-load-ms')) return 'index';" +
        " var n = document.querySelector('.hm-search-list');" +
        " return n && n.textContent.indexOf('searchable on the site') >= 0 ? 'own-only' : null; })()");
    }
    if (loaded !== "index") {
      throw new Error("the map did not load its index (" + (loaded || "no answer") +
                      "): the search measured would not be the reader's");
    }

    // render() is the input's "input" listener; its scopes hold the matcher.
    const el = await S("Runtime.evaluate", { expression: "document.querySelector('.hm-search-input')",
      objectGroup: "check_map_search" });
    const ls = await S("DOMDebugger.getEventListeners", { objectId: el.result.objectId });
    const listener = ls.listeners.find((l) => l.type === "input" && l.handler && l.handler.objectId);
    if (!listener) throw new Error("the search input has no 'input' listener to read the matcher from");
    const fn = await S("Runtime.getProperties", { objectId: listener.handler.objectId, ownProperties: true });
    const scopes = (fn.internalProperties || []).find((p) => p.name === "[[Scopes]]");
    if (!scopes) throw new Error("the listener's scopes could not be read");
    const chain = await S("Runtime.getProperties", { objectId: scopes.value.objectId, ownProperties: true });
    const got = {};
    for (const sc of chain.result) {
      if (!sc.value || !sc.value.objectId || /^Global/.test(sc.value.description || "")) continue;
      const vars = await S("Runtime.getProperties", { objectId: sc.value.objectId, ownProperties: true });
      for (const v of vars.result) {
        if (NEEDED.concat(OPTIONAL).includes(v.name) && !(v.name in got) && v.value) got[v.name] = v.value;
      }
    }
    const missing = NEEDED.filter((n) => !got[n] || !got[n].objectId);
    if (missing.length) {
      throw new Error("the search block has no " + missing.join(", ") +
                      " in its closure: the check must be brought up to the block's names");
    }
    const arg = (n) => {
      const v = got[n];
      if (!v) return { value: null };
      return v.objectId ? { objectId: v.objectId } : { value: v.value };
    };
    const call = async (f, args) => {
      const r = await S("Runtime.callFunctionOn", { functionDeclaration: f.toString(),
        objectId: listener.handler.objectId, arguments: args, returnByValue: true }, CALL_MS);
      if (r.exceptionDetails) {
        const ex = r.exceptionDetails;
        throw new Error("in the page: " + ((ex.exception && ex.exception.description) || ex.text));
      }
      return r.result.value;
    };

    // The cap on the map's own results, a phone's and a wide screen's.
    const capOf = "function (caps) { return caps ? caps().own : null; }";
    await size(PHONE);
    out.cap_phone = await call(capOf, [arg("caps")]);
    await size(WIDE);
    out.cap_wide = await call(capOf, [arg("caps")]);

    const m = JSON.parse(await call(measureInPage, ["search", "hits", "words", "isOwn", "STOP", "data",
      "JUNK_Q", "STATION_COLOR"].map(arg)));
    out.index_rows = m.rows;
    out.own_listed = { stations: m.own_stations, lines: m.own_lines };
    for (const kind of ["stations", "lines"]) {
      const rows = m[kind];
      const missed = rows.filter((r) => r.status === "not_found");
      const past = rows.filter((r) => r.status === "past_cap");
      const low = rows.filter((r) => r.status === "found" && out.cap_phone && r.rank > out.cap_phone);
      out[kind] = { drawn: rows.length, found: rows.length - missed.length - past.length,
                    not_found: missed.length, past_cap: past.length, past_phone_cap: low.length,
                    missed, past, low };
      missed.forEach((r) => out.problems.push(kind.slice(0, -1) + " not found: " + JSON.stringify(r.name) +
        " (" + r.why + (r.lost ? ": " + r.lost.join(", ") : "") + ")"));
      past.forEach((r) => out.warnings.push(kind.slice(0, -1) + " " + JSON.stringify(r.name) +
        " is matched at rank " + r.rank + " of " + r.of + ", past the cap of " + out.cap_wide +
        " (ahead: " + r.ahead.join("; ") + ")"));
      low.forEach((r) => out.warnings.push(kind.slice(0, -1) + " " + JSON.stringify(r.name) +
        " is shown at rank " + r.rank + ", past a phone's " + out.cap_phone));
    }
    if (m.stations.length + m.lines.length === 0) {
      out.problems.push("no drawn station or line was read from the page");
    }

    // The index's own station rows (lane 2, 2026-10-16).
    if (got.byIndex && got.byIndex.objectId) {
      const ir = JSON.parse(await call(indexStationsInPage, ["search", "data", "byIndex", "NEAR_M", "LINK_M"].map(arg)));
      out.index_stations = ir;
      ir.near_listed.forEach((r) => out.problems.push("index station " + JSON.stringify(r.name) +
        " is listed as not on this map " + r.m + " m from the drawn " + JSON.stringify(r.pin)));
      ir.unfound.forEach((r) => out.warnings.push("index station " + JSON.stringify(r.name) +
        " is joined to " + JSON.stringify(r.pin) + " but typing it does not show that pin"));
    } else {
      out.problems.push("UNMEASURED index stations: the search block has no byIndex in its closure");
    }

    // The box against the closure, on the first station the closure found.
    out.queries = {};
    for (const q of QUERIES) {
      out.queries[q] = JSON.parse(await call(function (search, text) {
        return JSON.stringify(search(text).map(function (d) { return d.kind + ": " + d.name; }));
      }, [arg("search"), { value: q }]));
    }

    const first = m.stations.find((r) => r.status === "found" && r.rank <= (out.cap_wide || 1));
    if (first) {
      const pills = JSON.parse(await call(probeBoxInPage, [{ value: first.name }]));
      out.box_probe = { typed: first.name, pills: pills.length, shown: pills.includes(first.name) };
      if (!out.box_probe.shown) {
        out.problems.push("the box does not show " + JSON.stringify(first.name) +
                          " though search() returns it: the check and the box disagree");
      }
    }
    if (out.problems.length) out.status = "fail";
  } catch (e) {
    out.status = "error";
    out.problems.push("UNMEASURED: " + e.message);
  } finally {
    cdp.handlers.splice(cdp.handlers.indexOf(onEvent), 1);
    try { await cdp.send("Target.closeTarget", { targetId }, null, 10000); } catch (e) { /* closing */ }
  }
  return out;
}

function printCity(r, listMax) {
  if (r.status === "skipped") { console.log(r.city + ": skipped, " + r.note); return; }
  if (r.status === "error") { console.log(r.city + ": ERROR " + r.problems.join("; ")); return; }
  const s = r.stations, l = r.lines;
  console.log(r.city + ": " + (r.status === "ok" ? "OK" : "FAIL") +
    "  stations " + s.drawn + " drawn, " + s.found + " found, " + s.not_found + " not found" +
    (s.past_cap ? ", " + s.past_cap + " past the cap" : "") +
    ";  lines " + l.drawn + " drawn, " + l.found + " found, " + l.not_found + " not found" +
    (l.past_cap ? ", " + l.past_cap + " past the cap" : "") +
    (r.warnings.length ? ";  " + r.warnings.length + " warning(s)" : ""));
  Object.keys(r.queries || {}).forEach((q) => console.log("    query " + JSON.stringify(q) + ": " +
    (r.queries[q].join(" | ") || "(nothing)")));
  const ix = r.index_stations;
  if (ix) {
    console.log("    index stations " + ix.rows + ": " + ix.joined + " joined (" + ix.joined_far.length +
      " farther than 150 m), " + ix.dropped + " dropped as duplicates, " + ix.listed +
      " listed as not on this map (" + ix.near_listed.length +
      " near a pin)");
  }
  const show = (label, items) => {
    items.slice(0, listMax).forEach((t) => console.log("    " + label + " " + t));
    if (items.length > listMax) console.log("    ... and " + (items.length - listMax) + " more (see --json)");
  };
  show("FAIL", r.problems);
  show("warn", r.warnings);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  QUERIES = args.queries;
  const cities = args.cities.length ? args.cities : searchedCities();
  if (!cities.length) usage("no searched city: app/static/places/ holds no index");
  const bad = cities.filter((c) => !/^[a-z0-9_]+$/.test(c));
  if (bad.length) usage("not a city slug: " + bad.join(", "));
  const exe = findBrowser(args.browser);
  if (!exe || !fs.existsSync(exe)) usage("no Edge or Chrome found; name one with --browser <exe>");
  if (typeof WebSocket === "undefined") usage("this needs Node 22 or later (a built-in WebSocket)");

  const server = await startServer();
  const origin = "http://127.0.0.1:" + server.address().port;
  let browser = null;
  const results = [];
  try {
    browser = await startBrowser(exe);
    for (const city of cities) {
      const r = await checkCity(browser, origin, city);
      results.push(r);
      printCity(r, args.list);
    }
  } finally {
    if (browser) await stopBrowser(browser);
    server.closeAllConnections();
    await new Promise((r) => server.close(r));
  }

  const failed = results.filter((r) => r.status === "fail" || r.status === "error");
  const sum = (k, f) => results.reduce((n, r) => n + (r[k] ? r[k][f] : 0), 0);
  console.log("\n" + results.filter((r) => r.status === "ok").length + " OK, " + failed.length +
    " failing, " + results.filter((r) => r.status === "skipped").length + " skipped;  stations " +
    sum("stations", "drawn") + " drawn, " + sum("stations", "not_found") + " not found;  lines " +
    sum("lines", "drawn") + " drawn, " + sum("lines", "not_found") + " not found");
  if (args.json) {
    fs.writeFileSync(args.json, Buffer.from(JSON.stringify(
      { browser: path.basename(exe), cities: results }, null, 2) + "\n", "utf8"));
    console.log("wrote " + args.json);
  }
  process.exit(failed.length ? 1 : 0);
}

main().catch((e) => { console.error(e.stack || String(e)); process.exit(2); });
