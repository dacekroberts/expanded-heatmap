"""Run the place-search rollout's script-only steps for a list of waves, with
no session attending, and leave ONE morning report of what needs a person.

    python scripts/place_search_night.py --waves FILE --plan FILE --report FILE --state FILE --session NAME [--hosts A,B] [--max-hours H] [--retry-failed] [--dry-run]
    python scripts/place_search_night.py --selftest

WAVES is {"date": "YYYY-MM-DD", "waves": [{"name": "wave2", "cities": [...]}]};
its date names the caches the fetch writes (osm_places_<date>.json), so it is
the date of the night. PLAN is a plan of scripts/place_search_scaffold.py that
covers those cities, a draft or not: the runner scaffolds from a copy without
the draft marker, holding only the cities whose entry is complete. REPORT is
Markdown, rewritten after every city, so a crash still leaves a report. STATE
is JSON: a rerun with the same file resumes and repeats no finished step.

PER WAVE, IN ORDER (place-search-city skill, "The rollout: the cheap path"):

  1. Area lookup for the plan entries with no relations
     (scripts/place_search_area_lookup.py), on a mirror that answers. Data
     months old is accepted for this step only.
  2. Scaffold (scripts/place_search_scaffold.py's run_plan, writing). A city
     the script refuses goes to the report with its reason. A city whose
     language is not in place_index.LANGUAGE_NAMES, or has no built city yet,
     is NOT scaffolded: a new language is done first and by hand.
  3. Fetch: one queue per healthy mirror, each a child process of
     scripts/place_search_fetch_queue.py with --host, never the same city in
     two queues. Heavy cities (HEAVY_STATIONS, config.PLACE_SPLIT) go to
     HEAVY_MIRROR only. Each queue's log is read for the per-city outcome.
  4. For each city whose caches are in: its index step through the job gate
     (scripts/heavy_job.py run), then the checks that need no rendered map:
     check_place_search.py's index keys, id file, crossings, street lines
     (J), junk (F), leak words (E), visitable homes (G) and coverage (H), and
     check_place_scope.py. NOT rule A: no map is rendered at night.
  5. The wave's rows in the report.

WHAT LATER WAVES TAKE FROM EARLIER ONES. Each rule is a constant below with
its reason, and every decision is written to the report under "What the
runner changed": a mirror whose last MIRROR_FAIL_WINDOW fetches failed, or
whose answer the age guard refused, is set aside for place fetches and its
cities move; with no healthy mirror fetching stops, the other steps go on,
and the mirrors are tried again every RETRY_MIN minutes; a city that failed
CITY_MAX_TRIES times is not tried again that night; a later wave starts only
when every city of the earlier one was attempted, with the kinds that failed
earlier (by country, by heavy or light) moved last; an index or street file
larger than the largest at the start is flagged, never a stop.

IT REFUSES TO RUN on master or worktree-cleanup, on a detached HEAD, and on a
working tree that is not clean at the start: a scaffolded wave lives on its
own branch, and fails check_place_search.py until its render. A resumed run
accepts the changes of the cities it has itself started and nothing else.
The state file is one night's: a failed fetch and a mirror set aside stay so
on a rerun. The next night takes a new state file, or --retry-failed, which
clears every failed step and puts every mirror back in use.

WHAT IT NEVER DOES. It commits nothing, pushes nothing, renders no map and
runs no step*_map.py. It makes no Overpass request itself and holds no lock:
the lookup and the fetch are child processes that hold the mirror's FetchLock
(pipeline/place_index_fetch.py), and pipeline/osm.py holds the wait after a
504 or 429 inside each. Between children the runner keeps that same minute
(OVERLOAD_WAIT_S) before it starts another on a mirror that just refused.

EXIT CODE. 0 when it ran to the end, whatever it found; 2 when it could not
run (a refusal, an unreadable file); 130 when interrupted from the keyboard,
after stopping its queues and saving its state. --dry-run prints the whole
plan of action, starts nothing and writes nothing.
"""
import argparse
import datetime
import gzip
import importlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# pipeline/osm.py's OVERPASS_HOSTS by name, repeated as the fetch queue
# repeats them, so nothing that can fetch is imported here (the selftest
# fails if the lists differ).
MIRRORS = ("overpass-api.de", "overpass.kumi.systems")
# The one mirror a heavy city may ask: overpass.kumi.systems has read-timed
# out on heavy queries (pipeline/osm.py; place-search-city skill, step 3).
HEAVY_MIRROR = "overpass-api.de"
# The order mirrors are tried for area lookups. A lookup accepts old data, so
# the mirror serving old data (useless for places on 2026-10-12) goes first
# and overpass-api.de is kept for the place queries.
LOOKUP_ORDER = ("overpass.kumi.systems", "overpass-api.de")
# A city is heavy at this many map stations, or with config.PLACE_SPLIT. The
# station count is the only size known offline before a fetch, and it is a
# rough proxy. Measured on the 19 built cities (2026-10-13): every city whose
# first query needed tiles has 109 stations or more (Sao Paulo 109, London
# 387, Tokyo 490), and Mexico City (180) answered whole in 170 s of a 180 s
# limit; under 100 stations the largest cache is Montreal's 72 MB, which
# answered whole. Re-measure when a wave shows a light city timing out.
HEAVY_STATIONS = 100
# A mirror whose last this-many fetches all failed is set aside (owner's
# brief, 2026-10-13). An answer the age guard refused sets it aside at once:
# the next city would be refused the same way.
MIRROR_FAIL_WINDOW = 3
# With no healthy mirror, the mirrors are tried again this often, with one
# city each, until --max-hours.
RETRY_MIN = 60
# A city that failed this many fetches is not tried again that night. A
# refusal by the age guard is the mirror's failure and is not counted.
CITY_MAX_TRIES = 2
# Cities handed to a mirror's queue at a time. Small, so that a mirror going
# bad costs few cities before it is set aside: two cities and the queue's own
# retry of each are four fetches, the fewest that can fill
# MIRROR_FAIL_WINDOW in one batch while the retry of the first city still
# comes after the second, not straight after its own failure.
QUEUE_BATCH = 2
# --retries for a city fetched in tiles, which goes alone: each run keeps the
# tiles that answered and must be repeated until all are in (the fetch
# queue's docstring). Its queue's own verdict then stands for the night.
SPLIT_RETRIES = 3
# pipeline/osm.py's OVERLOAD_WAIT_S: the owner's floor after a 504 or 429.
# Each child keeps it inside itself; this keeps it between two children.
OVERLOAD_WAIT_S = 60
# Seconds between two looks at the running queues.
POLL_S = 15
# The index build's declared peak for the job gate. The largest of the
# builds in the gate's history is Sao Paulo's 0.82 GB (2026-10-13); the
# gate's default of 8 GB would refuse builds the machine has room for.
BUILD_PEAK_GB = 1.0
BUILD_ESTIMATE = "the largest measured index build, sao_paulo 0.82 GB"
# Minutes a build waits at the gate, and its limit once admitted. No index
# build on record took a tenth of the limit; a build past it is stopped.
BUILD_WAIT_MIN = 30
BUILD_TIMEOUT_MIN = 60
# Minutes a lookup waits for its mirror's lock, and the minutes a city may
# cost on top of that wait (the lookup's own REQUEST_DEADLINE_S is 5).
LOOKUP_WAIT_MIN = 30
LOOKUP_MIN_PER_CITY = 6
# How much of a long list one report line carries.
RULE_E_SHOWN = 20
CANDIDATES_SHOWN = 8
# A municipality of a wider area holding this many stations or fewer is
# flagged: the single-station call is the owner's (regional-extension skill).
THIN_STATIONS = 1
PROTECTED_BRANCHES = ("master", "worktree-cleanup")
LOOKUP_SCRIPT = "scripts/place_search_area_lookup.py"
QUEUE_SCRIPT = "scripts/place_search_fetch_queue.py"
GATE_SCRIPT = "scripts/heavy_job.py"
_PLACE_AREA_RE = re.compile(r"(?m)^PLACE_AREA\s*=")
_LOG_RE = re.compile(r"^\S+Z (\S+) (fetched|skipped|retried and fetched|failed twice|failed again|"
                     r"failed \d+ times|failed|not queued)\b:? ?(.*)$")
AREA_DONE = ("in plan", "resolved", "unresolved", "skipped")
SCAFFOLDED = ("done", "already")
FETCH_DONE = ("fetched", "cached", "failed", "scope stop")
FETCH_IN = ("fetched", "cached")
BUILD_DONE = ("built", "failed")
# The report's "Needs your call" groups, in order.
KINDS = (
    ("area", "An area that could not be resolved"),
    ("scope", "A municipality with none of the map's stations"),
    ("coverage", "Stations outside the area, or rule H coverage"),
    ("fetch", "A fetch that failed twice, or data the age guard refused"),
    ("language", "A local language under the coverage floor"),
    ("new language", "A new language"),
    ("size", "A size over the bar"),
    ("leak", "Rule E names: a business or home word in a name"),
    ("thin", "A municipality holding a single station"),
    ("check", "Other check and build failures"),
    ("scaffold", "Cities the scaffold refused"),
    ("waiting", "Not fetched this night"),
)

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def _read_json(path):
    return json.loads(Path(path).read_bytes().decode("utf-8"))


def _write_bytes(path, text):
    """Text written as UTF-8 bytes with LF line endings."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def _last_line(text, skip=("ENDED:", "ADMITTED:", "DECLARED:")):
    """The last non-empty line of a child's output that is not the job
    gate's own."""
    for line in reversed(str(text).splitlines()):
        line = line.strip()
        if line and not line.startswith(skip):
            return line
    return ""


def is_heavy(stations, split):
    """True for a city that may only ask HEAVY_MIRROR. A city whose stations
    cannot be counted is taken as heavy: the cautious reading."""
    return bool(split) or stations is None or stations >= HEAVY_STATIONS


def parse_queue_log(text):
    """{city: [event, ...]} from a fetch queue's log, in the order written.
    An event is {"what": "fetched" | "skipped" | "failed" | "not queued",
    "final": bool, "exit": int or None, "seconds": float, "last": str}."""
    out = {}
    for line in str(text).splitlines():
        m = _LOG_RE.match(line.strip())
        if not m:
            continue
        city, word, rest = m.groups()
        code = re.search(r"exit=(-?\d+)", rest)
        secs = re.search(r" ([\d.]+)s ", rest + " ")
        last = re.search(r"(?:last|reason): (.*)$", rest)
        what = ("fetched" if "fetched" in word else "skipped" if word == "skipped"
                else "not queued" if word == "not queued" else "failed")
        out.setdefault(city, []).append({
            "what": what, "final": word.startswith("failed") and word not in ("failed", "failed again"),
            "exit": int(code.group(1)) if code else None,
            "seconds": float(secs.group(1)) if secs else 0.0,
            "last": last.group(1) if last else rest})
    return out


def classify_failure(exit_code, last):
    """(kind, HTTP codes) for one failed fetch, from the child's last line.
    "scope" is the fetch's own stop on the boundary; "stale" the age guard;
    "lock" another fetch holding the mirror; "timeout" a child stopped by the
    queue; "mirror" every try refused; "other" anything else."""
    codes = sorted(set(re.findall(r"HTTPError (\d{3})", last)))
    if ("breaks the scope rule" in last or "not a closed boundary" in last
            or "names no boundary" in last):
        return "scope", codes
    if "data dated" in last and "older than" in last:
        return "stale", codes
    if "place fetch is running" in last or "place fetch holding every mirror" in last:
        return "lock", codes
    if exit_code == 124:
        return "timeout", codes
    if "Overpass mirror failed" in last:
        return "mirror", codes
    return "other", codes


def parse_scaffold(lines):
    """{city: (status, reason)} from run_plan's closing table."""
    out, table = {}, False
    for line in lines:
        if line.startswith("CITY") and "RESULT" in line:
            table = True
            continue
        if not table or not line.strip():
            continue
        city, _, rest = line.strip().partition(" ")
        rest = rest.strip()
        if rest.startswith("refused"):
            out[city] = ("refused", rest.partition(":")[2].strip() or "refused")
        elif rest in ("done", "would do"):
            out[city] = ("done", None)
    return out


def findings_of(raw, bars):
    """[{"kind", "text"}] for one built city, from what the checks returned
    (`raw`: Real.checks) and the size bars measured at the start."""
    out, leaks = [], []
    for p in raw.get("problems", []):
        m = re.match(r"E: (.+) carries (.+?): drop it by a rule", p)
        if m:
            leaks.append(f"{m.group(1)} ({m.group(2)})")
        elif p.startswith("H:"):
            out.append({"kind": "coverage", "text": p})
        elif ("local language" in p and "under" in p) or "no language reaches the bar" in p:
            out.append({"kind": "language", "text": p})
        else:
            out.append({"kind": "check", "text": p})
    if leaks:
        shown = "; ".join(leaks[:RULE_E_SHOWN])
        more = f"; and {len(leaks) - RULE_E_SHOWN} more" if len(leaks) > RULE_E_SHOWN else ""
        out.append({"kind": "leak", "text": f"{len(leaks)} name(s): {shown}{more}"})
    for p in raw.get("scope_problems", []):
        out.append({"kind": "scope" if " B. " in p else "check", "text": p})
    area = raw.get("area") or []
    counted = [m for m in area if m.get("stations") is not None]
    total = raw.get("stations")
    if total is not None and counted and len(counted) == len(area):
        outside = total - sum(m["stations"] for m in area)
        if outside > 0:
            out.append({"kind": "coverage", "text": f"{outside} of {total} map stations sit outside "
                                                    f"every municipality of the area"})
    if len(area) > 1:
        thin = [f"{m.get('name')} ({m['stations']})" for m in counted
                if 0 < m["stations"] <= THIN_STATIONS and not m.get("kept")]
        if thin:
            out.append({"kind": "thin", "text": "in the area on few stations: " + ", ".join(thin)})
    for key, label in (("index", "index"), ("streets", "street lines file")):
        size = (raw.get(key) or [0])[0]
        bar = bars.get(key) or 0
        if bar and size > bar:
            out.append({"kind": "size", "text": f"the {label} is {size:,} bytes, over the largest at "
                                                f"the start ({bar:,}, {bars.get(key + '_city')})"})
    return out


def calls_of(c):
    """[(kind, text)] of everything in one city's record that needs a
    person, for the report's "Needs your call"."""
    calls = []
    area = c.get("area") or {}
    if area.get("status") in ("unresolved", "failed", "skipped"):
        cands = area.get("candidates") or []
        text = str(area.get("reason"))
        if cands:
            text += ". Candidates: " + "; ".join(
                f"{r.get('name') or '(no name)'} (level {r.get('level')}, relation {r.get('id')})"
                for r in cands[:CANDIDATES_SHOWN])
            if len(cands) > CANDIDATES_SHOWN:
                text += f"; and {len(cands) - CANDIDATES_SHOWN} more"
        calls.append(("area", text))
    sc = c.get("scaffold") or {}
    if sc.get("status") == "held" and sc.get("kind") == "new language":
        calls.append(("new language", sc["reason"]))
    elif sc.get("status") == "refused":
        calls.append(("scaffold", sc["reason"]))
    fetch = c.get("fetch") or {}
    tries = fetch.get("attempts") or []
    said = "; ".join(f"{a['mirror']}: {a['kind']}" + (f", HTTP {', '.join(a['codes'])}" if a.get("codes") else "")
                     for a in tries if a.get("kind") != "ok")
    if fetch.get("status") == "scope stop":
        calls.append(("scope", f"the fetch stopped before its place queries: \"{fetch.get('reason')}\""))
    elif fetch.get("status") == "failed":
        calls.append(("fetch", f"not fetched ({said or 'no try on record'}). Last line: "
                               f"\"{str(fetch.get('reason'))[:400]}\""))
    elif fetch.get("status") == "waiting":
        calls.append(("waiting", str(fetch.get("reason")) + (f" Tries so far: {said}." if said else "")))
    build = c.get("build") or {}
    if build.get("status") == "failed":
        calls.append((build.get("kind") or "check",
                      f"the index step stopped (exit {build.get('exit')}): \"{str(build.get('reason'))[:400]}\""))
    elif build.get("status") == "gate refused":
        calls.append(("check", "the job gate refused the index build; a rerun with the same state "
                               "file builds it"))
    for f in (c.get("checks") or {}).get("findings", []):
        calls.append((f["kind"], f["text"]))
    return calls


def _kb(pair):
    """"raw / gzipped" in KB for a (raw bytes, gzipped bytes) pair."""
    if not pair:
        return ""
    return f"{pair[0] / 1024:,.0f} / {pair[1] / 1024:,.0f}"


def render_report(state, waves, meta):
    """The morning report, Markdown, from the state alone."""
    cities = state["cities"]
    order = [(name, city) for name, names in waves for city in names if city in cities]

    def n(test):
        return sum(1 for _, city in order if test(cities[city]))

    def status(c, step):
        return (c.get(step) or {}).get("status")

    built = [city for _, city in order if status(cities[city], "build") == "built"]
    calls = {city: calls_of(cities[city]) for _, city in order}
    clean = [city for city in built if not calls[city]]
    hours = state.get("elapsed_s", 0) / 3600
    lines = [f"# Place search rollout: the night run of {meta['date']}", ""]
    lines.append(f"Ran from {state.get('started')} to {meta['now']} (UTC), {hours:.1f} hours over "
                 f"{state.get('runs', 1)} run(s), session {meta['session']}, on branch {meta['branch']}. "
                 f"Waves: {', '.join(name for name, _ in waves)}. "
                 + ("The run reached its end." if state.get("finished")
                    else "THE RUN HAS NOT REACHED ITS END: this is the report as of its last step."))
    for note in state.get("top", []):
        lines += ["", f"**{note}**"]
    lines += ["",
              f"- Cities in the waves: {len(order)}",
              f"- Areas looked up: {n(lambda c: status(c, 'area') == 'resolved')} resolved, "
              f"{n(lambda c: status(c, 'area') in ('unresolved', 'failed', 'skipped'))} left for a person",
              f"- Scaffolded: {n(lambda c: status(c, 'scaffold') == 'done')} "
              f"(already scaffolded before the run: {n(lambda c: status(c, 'scaffold') == 'already')})",
              f"- Fetched: {n(lambda c: status(c, 'fetch') == 'fetched')} "
              f"(caches already on disk: {n(lambda c: status(c, 'fetch') == 'cached')})",
              f"- Built: {len(built)}",
              f"- Clean (built, no finding): {len(clean)}",
              f"- Needing a call: {sum(1 for city in calls if calls[city])}",
              "",
              "Rule A of check_place_search.py (each map carries its index's current hash) was not "
              "run: no map is rendered at night. It fails for every city built here until the wave's "
              "one re-render. Nothing was committed, pushed or rendered.",
              "", "## Needs your call", ""]
    any_call = False
    for kind, title in KINDS:
        rows = [(name, city, text) for name, city in order for k, text in calls[city] if k == kind]
        if not rows:
            continue
        any_call = True
        lines += [f"### {title}", ""]
        for name, city, text in rows:
            lines.append(f"- **{city}** ({cities[city].get('country') or 'country unknown'}, {name}): {text}")
        lines.append("")
    if not any_call:
        lines += ["Nothing.", ""]
    lines += ["## Still owed by a session", ""]
    if built:
        lines += ["For every built city: the eye read (the place-read agent, one city a call) and "
                  "acting on it (PLACE_DROPPED by id, PLACE_REVIEWED by name, a rule through the "
                  "rule-change protocol, questions for the owner). Then, once per wave: the one "
                  "re-render of every map through the job gate, the browser test with one street "
                  "picked, the full checks with rule A, the drafts entry and the landing.", ""]
        for name, names in waves:
            mine = [city for city in names if city in built]
            if mine:
                lines.append(f"- {name} ({len(mine)} built): {', '.join(mine)}")
        lines.append("")
    else:
        lines += ["No city was built.", ""]
    lines += ["## What the runner changed", ""]
    lines += [f"- {text}" for text in state.get("changes", [])] or [
        "Nothing: no mirror was set aside, no city moved and no wave was reordered."]
    lines += ["", "## Per city", ""]
    for name, names in waves:
        lines += [f"### {name}", "",
                  "| City | Country | Stations | Area | Scaffold | Fetch | Min | Rows | Index KB raw / gz "
                  "| Streets KB raw / gz | Languages | Findings |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for city in names:
            c = cities.get(city)
            if c is None:
                continue
            fetch = c.get("fetch") or {}
            tries = fetch.get("attempts") or []
            mirror = tries[-1]["mirror"] if tries else ""
            minutes = sum(a.get("seconds") or 0 for a in tries) / 60
            checks = c.get("checks") or {}
            area = c.get("area") or {}
            cells = [city, c.get("country") or "", "" if c.get("stations") is None else str(c["stations"])
                     + (" heavy" if c.get("heavy") else ""),
                     (area.get("status") or "not reached")
                     + (f" ({len(area['relations'])})" if area.get("relations") else ""),
                     status(c, "scaffold") or "not reached",
                     (fetch.get("status") or "not reached") + (f" on {mirror}" if mirror else ""),
                     f"{minutes:.0f}" if tries else "",
                     f"{checks['rows']:,}" if checks.get("rows") is not None else (status(c, "build") or ""),
                     _kb(checks.get("index")), _kb(checks.get("streets")),
                     str(checks.get("languages") or ""), str(len(calls[city]))]
            lines.append("| " + " | ".join(str(x).replace("|", "/") for x in cells) + " |")
        found = [(city, kind, text) for city in names if city in cities for kind, text in calls[city]]
        if found:
            lines += ["", "Findings:", ""]
            lines += [f"- {city}: [{kind}] {text}" for city, kind, text in found]
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


class _Child:
    """A started child process whose output goes to a file."""

    def __init__(self, argv, out_path):
        self.out_path = Path(out_path)
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self._file = open(self.out_path, "wb")
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        self._proc = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=self._file,
                                      stderr=subprocess.STDOUT)

    def poll(self):
        code = self._proc.poll()
        if code is not None and not self._file.closed:
            self._file.close()
        return code

    def stop(self):
        """Stop the child and what it started (the gate's own child)."""
        try:
            import psutil
            for p in psutil.Process(self._proc.pid).children(recursive=True):
                p.kill()
        except Exception:
            pass
        self._proc.kill()
        self._proc.wait()
        self.poll()

    def text(self):
        try:
            return self.out_path.read_bytes().decode("utf-8", errors="replace")
        except OSError:
            return ""


def _fresh_config(city):
    """A city's config module as it is on disk NOW: the scaffold appends to
    it during the run, and a module imported before that is stale."""
    name = f"pipeline.{city}.config"
    sys.modules.pop(name, None)
    return importlib.import_module(name)


class Real:
    """Every effect of the runner on the world outside it. The selftest
    passes a stand-in with the same methods."""

    def clock(self):
        return time.time()

    def sleep(self, seconds):
        time.sleep(seconds)

    def now(self):
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def git(self, args):
        proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
        return proc.stdout

    def spawn(self, argv, out_path):
        return _Child(argv, out_path)

    def run(self, argv, timeout_min, out_path):
        """Start a child, wait for it to the end and return (exit code,
        output). A child past timeout_min is stopped and reported as 124."""
        child = self.spawn(argv, out_path)
        until = time.time() + timeout_min * 60
        while child.poll() is None:
            if time.time() >= until:
                child.stop()
                return 124, child.text() + f"\nstopped after {timeout_min:g} min with no end"
            time.sleep(2)
        return child.poll(), child.text()

    def scaffold(self, plan, label):
        import place_search_scaffold
        return place_search_scaffold.run_plan(ROOT, plan, True, plan_label=label)

    def listing(self):
        import place_search_area_lookup
        return place_search_area_lookup.city_listing(ROOT)

    def facts(self, city):
        """What is known offline about a city now: its station count, whether
        it is fetched in tiles, whether it is scaffolded, and what its caches
        lack (None when all three are whole)."""
        import place_search_fetch_queue as queue
        from pipeline import place_index
        path = ROOT / "pipeline" / city / "config.py"
        if not path.is_file():
            return {"error": f"no pipeline/{city}/config.py"}
        scaffolded = bool(_PLACE_AREA_RE.search(path.read_bytes().decode("utf-8")))
        try:
            config = _fresh_config(city)
            stations = place_index.map_stations(config)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:
            return {"error": f"pipeline.{city}.config: {type(exc).__name__}: {exc}"}
        caches = "not scaffolded"
        if scaffolded:
            json_path, extra_path, why = queue.read_place_paths(city, importer=lambda name: config)
            caches = why or queue.real_cached(city, json_path, extra_path)
        return {"stations": None if stations is None else len(stations),
                "split": bool(getattr(config, "PLACE_SPLIT", None)),
                "scaffolded": scaffolded, "caches": caches}

    def languages(self):
        """(codes place_index names, codes that have a built city): a
        language is built when a config declaring it in PLACE_LANGUAGES has
        its index under app/static/places/."""
        import ast
        from pipeline import place_index
        built = set()
        for index in place_index.STATIC_DIR.glob("*.json"):
            config = ROOT / "pipeline" / index.stem / "config.py"
            try:
                tree = ast.parse(config.read_bytes().decode("utf-8"))
            except (OSError, SyntaxError, UnicodeDecodeError):
                continue
            for node in tree.body:
                if (isinstance(node, ast.Assign) and len(node.targets) == 1
                        and getattr(node.targets[0], "id", "") == "PLACE_LANGUAGES"):
                    try:
                        built.update(ast.literal_eval(node.value))
                    except (ValueError, TypeError, SyntaxError):
                        pass
        return set(place_index.LANGUAGE_NAMES), built

    def bars(self):
        """The largest index and street lines file on the tree at the start."""
        from pipeline import place_index
        out = {}
        for key, folder in (("index", place_index.STATIC_DIR), ("streets", place_index.STATIC_DIR / "streets")):
            files = sorted(folder.glob("*.json"), key=lambda p: p.stat().st_size)
            out[key] = files[-1].stat().st_size if files else 0
            out[key + "_city"] = files[-1].stem if files else None
        return out

    def pages(self, city):
        """The app pages that read a city's config, as paths from the root."""
        out = []
        for page in sorted((ROOT / "app" / "pages").glob("*.py")):
            if f"pipeline.{city}.config" in page.read_bytes().decode("utf-8", errors="replace"):
                out.append(page.relative_to(ROOT).as_posix())
        return out

    def checks(self, city):
        """The checks that need no rendered map, on one built city, with its
        sizes and languages line. Rule A (the map's hash) is not run."""
        import check_place_scope
        import check_place_search as cps
        from pipeline import place_index
        config = _fresh_config(city)
        index_bytes = place_index.index_path(city).read_bytes()
        index = json.loads(index_bytes.decode("utf-8"))
        summary = _read_json(place_index.summary_path(city))
        problems = (cps.check_index(city, index, summary)
                    + cps.check_ids(city, index_bytes, index, place_index.ids_path(city))
                    + cps.check_crossings(city, index) + cps.check_streets(city, index)
                    + cps.check_junk(index)
                    + cps.check_leaks(city, index, getattr(config, "PLACE_REVIEWED", {}))
                    + cps.check_visitable(city, getattr(config, "PLACE_VISITABLE", {})))
        stations = place_index.map_stations(config)
        if stations is None:
            problems.append("rule H not checked: no stations file on this machine")
        else:
            problems += cps.check_coverage(city, index, stations)
        scope_problems, notes = check_place_scope.check_city(place_index.summary_path(city), ROOT)

        def sizes(path):
            data = path.read_bytes() if path.is_file() else b""
            return [len(data), len(gzip.compress(data, 9))]

        langs = index.get("languages", {})
        return {"rows": len(index.get("rows", [])), "index": sizes(place_index.index_path(city)),
                "streets": sizes(place_index.streets_path(city)),
                "crossings": sizes(place_index.crossings_path(city)),
                "languages": f"{langs.get('coverage')} -> {langs.get('listed')}",
                "area": summary.get("area") or [], "stations": None if stations is None else len(stations),
                "problems": problems, "scope_problems": scope_problems, "notes": notes}


class Night:
    """One run of the runner. Every effect goes through `fx`."""

    def __init__(self, *, waves_path, plan_path, report_path, state_path, hosts, session,
                 max_hours, fx, out=print, retry_failed=False):
        # Absolute, since every child runs from the repository root.
        self.waves_path, self.plan_path = Path(waves_path).resolve(), Path(plan_path).resolve()
        self.report_path, self.state_path = Path(report_path).resolve(), Path(state_path).resolve()
        self.running = {}
        self.workdir = self.state_path.parent / (self.state_path.stem + "_files")
        self.hosts = [h for h in MIRRORS if h in hosts]
        self.session, self.max_hours = session, max_hours
        self.fx, self.out, self.retry_failed = fx, out, retry_failed
        self.not_before = {}
        self.started_queues = 0
        self.branch = ""

    # --- what the run reads -------------------------------------------------

    def load(self):
        """Read the waves, the plan and the state. Returns why it cannot run,
        or None."""
        try:
            waves = _read_json(self.waves_path)
            self.plan = _read_json(self.plan_path)
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            return f"cannot read the waves or the plan: {exc}"
        if (not isinstance(waves, dict) or not isinstance(waves.get("waves"), list)
                or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(waves.get("date")))):
            return f"{self.waves_path}: needs an ISO date and a waves list"
        if not isinstance(self.plan, dict) or not isinstance(self.plan.get("cities"), dict):
            return f"{self.plan_path}: the plan must be a JSON object with a cities object"
        self.date = waves["date"]
        self.waves, seen = [], set()
        for wave in waves["waves"]:
            if not isinstance(wave, dict) or not wave.get("name") or not isinstance(wave.get("cities"), list):
                return f"{self.waves_path}: each wave needs a name and a cities list"
            twice = [c for c in wave["cities"] if c in seen]
            if twice or len(set(wave["cities"])) != len(wave["cities"]):
                return f"{self.waves_path}: a city is named twice ({', '.join(twice) or wave['name']})"
            seen.update(wave["cities"])
            self.waves.append((str(wave["name"]), [str(c) for c in wave["cities"]]))
        if not self.hosts:
            return "no mirror named in --hosts is one of " + ", ".join(MIRRORS)
        self.state = {"schema": 1, "runs": 0, "elapsed_s": 0.0, "cities": {}, "mirrors": {},
                      "changes": [], "top": []}
        self.resumed = self.state_path.is_file()
        if self.resumed:
            try:
                self.state = _read_json(self.state_path)
            except (OSError, ValueError, UnicodeDecodeError) as exc:
                return f"cannot read the state file {self.state_path}: {exc}"
        return None

    def refusal(self):
        """Why the run is refused on this branch and tree, or None."""
        self.branch = self.fx.git(["branch", "--show-current"]).strip()
        if not self.branch or self.branch in PROTECTED_BRANCHES:
            return (f"the current branch is {self.branch or 'a detached HEAD'}: a scaffolded wave "
                    f"lives on its own branch, made from master, and is never built on "
                    f"{' or '.join(PROTECTED_BRANCHES)}. Make the wave's branch, then run again.")
        own_files = {self.report_path, self.state_path, self.plan_path, self.waves_path}
        own = set()
        for path in own_files:
            try:
                own.add(path.resolve().relative_to(ROOT.resolve()).as_posix())
            except ValueError:
                pass
        try:
            work = self.workdir.resolve().relative_to(ROOT.resolve()).as_posix() + "/"
        except ValueError:
            work = None
        started = [c for c, rec in self.state["cities"].items() if rec.get("started")]
        allowed = set()
        for city in started:
            allowed.update(self.fx.pages(city))
            allowed.update({f"app/static/places/{city}.json", f"app/static/places/crossings/{city}.json",
                            f"app/static/places/streets/{city}.json"})
        foreign = []
        for line in self.fx.git(["status", "--porcelain", "--untracked-files=all"]).splitlines():
            path = line[3:].split(" -> ")[-1].strip().strip('"')
            if not path or path in own or (work and path.startswith(work)) or path in allowed:
                continue
            if any(path.startswith((f"pipeline/{c}/", f"outputs/{c}/")) for c in started):
                continue
            foreign.append(path)
        if foreign:
            return (f"the working tree holds {len(foreign)} change(s) that are not this run's own "
                    f"({', '.join(foreign[:5])}{', ...' if len(foreign) > 5 else ''}). A scaffolded "
                    f"wave lives on its own branch, clean at the start: commit them or set them "
                    f"aside, then run again.")
        return None

    # --- small helpers --------------------------------------------------------

    def c(self, city):
        return self.state["cities"][city]

    def hhmm(self):
        return self.fx.now()[11:16]

    def change(self, text):
        self.state["changes"].append(f"{self.hhmm()} {text}")
        self.out(f"  changed: {text}")

    def top(self, text):
        if text not in self.state["top"]:
            self.state["top"].append(text)

    def out_of_time(self):
        return self.fx.clock() - self.t0 >= self.max_hours * 3600

    def save(self):
        self.state["elapsed_s"] = self.elapsed_before + (self.fx.clock() - self.t0)
        _write_bytes(self.state_path, json.dumps(self.state, ensure_ascii=False, indent=1) + "\n")
        meta = {"date": self.date, "now": self.fx.now(), "session": self.session, "branch": self.branch}
        _write_bytes(self.report_path, render_report(self.state, self.waves, meta))

    def mirror(self, host):
        return self.state["mirrors"].setdefault(host, {"recent": [], "aside": None, "probe": False})

    def usable(self, host):
        m = self.mirror(host)
        return m["aside"] is None or m["probe"]

    def wait_for(self, host):
        """Keep the minute after a refusal before another child asks `host`."""
        left = self.not_before.get(host, 0) - self.fx.clock()
        if left > 0:
            self.fx.sleep(left)

    def python(self, script, *args):
        return [sys.executable, script, *args]

    # --- the start -----------------------------------------------------------

    def prepare(self):
        self.t0 = self.fx.clock()
        self.elapsed_before = self.state.get("elapsed_s", 0.0)
        self.state["runs"] = self.state.get("runs", 0) + 1
        self.state.setdefault("started", self.fx.now())
        self.state["finished"] = False
        if "bars" not in self.state:
            self.state["bars"] = self.fx.bars()
        listing = self.fx.listing()
        for name, cities in self.waves:
            for city in cities:
                rec = self.state["cities"].setdefault(city, {})
                rec["wave"] = name
                if "heavy" not in rec:
                    facts = self.fx.facts(city)
                    rec["country"] = (listing.get(city) or (None, None))[0]
                    rec["stations"] = facts.get("stations")
                    rec["split"] = bool(facts.get("split"))
                    rec["heavy"] = is_heavy(rec["stations"], rec["split"])
                    if facts.get("error"):
                        rec["area"] = {"status": "skipped", "reason": facts["error"]}
        if self.retry_failed:
            cleared = []
            for city, rec in self.state["cities"].items():
                hit = False
                for step, bad in (("area", ("failed",)), ("scaffold", ("refused",)),
                                  ("fetch", ("failed", "scope stop", "waiting")), ("build", ("failed",))):
                    if (rec.get(step) or {}).get("status") in bad:
                        rec.pop(step)
                        hit = True
                if hit:
                    rec.pop("checks", None)
                    cleared.append(city)
            for m in self.state["mirrors"].values():
                m.update(recent=[], aside=None, probe=False)
            if cleared:
                self.change(f"--retry-failed: the failed steps of {len(cleared)} cities were cleared "
                            f"and every mirror is back in use ({', '.join(cleared)})")

    # --- rule d: the order inside a later wave ---------------------------------

    def order_wave(self, index):
        """Move the kinds that failed earlier to the end of a later wave: by
        country, and by heavy or light. A stable sort on the number of
        earlier failures of a city's country plus those of its weight."""
        name, cities = self.waves[index]
        earlier = {c for _, names in self.waves[:index] for c in names}
        by_country, by_weight = {}, {}
        for city in earlier:
            rec = self.state["cities"].get(city) or {}
            failed = ((rec.get("fetch") or {}).get("status") in ("failed", "scope stop")
                      or (rec.get("build") or {}).get("status") == "failed")
            if failed:
                by_country[rec.get("country")] = by_country.get(rec.get("country"), 0) + 1
                weight = "heavy" if rec.get("heavy") else "light"
                by_weight[weight] = by_weight.get(weight, 0) + 1
        if not by_country:
            return

        def score(city):
            rec = self.c(city)
            return by_country.get(rec.get("country"), 0) + by_weight.get("heavy" if rec.get("heavy") else "light", 0)

        ordered = sorted(cities, key=score)
        if ordered != cities:
            said = ", ".join(f"{k} {v}" for k, v in sorted({**by_country, **by_weight}.items(), key=str))
            self.change(f"{name}: reordered so the kinds that failed in earlier waves go last "
                        f"(failures so far: {said}); last now: {', '.join(ordered[-3:])}")
            self.waves[index] = (name, ordered)

    # --- step 1: the area lookup ---------------------------------------------

    def step_lookup(self, name, cities):
        need = []
        for city in cities:
            rec = self.c(city)
            spec = self.plan["cities"].get(city)
            status = (rec.get("area") or {}).get("status")
            # An area left for a person and since filled in the plan by hand
            # is read again; every other finished lookup stands.
            filled = status == "unresolved" and isinstance(spec, dict) and spec.get("relations")
            if status in AREA_DONE and not filled:
                continue
            if not isinstance(spec, dict):
                rec["area"] = {"status": "skipped", "reason": "not in the plan"}
            elif spec.get("relations"):
                rec["area"] = {"status": "in plan", "relations": list(spec["relations"])}
            else:
                need.append(city)
        for host in [h for h in LOOKUP_ORDER if h in self.hosts]:
            if not need or self.out_of_time():
                break
            self.wait_for(host)
            report = self.workdir / f"lookup_{name}_{host}.json"
            if report.exists():
                report.unlink()
            argv = self.python(LOOKUP_SCRIPT, str(self.plan_path), *need, "--host", host,
                               "--wait", str(LOOKUP_WAIT_MIN), "--report", str(report))
            self.out(f"{name}: area lookup of {len(need)} cities on {host}")
            code, text = self.fx.run(argv, LOOKUP_WAIT_MIN + LOOKUP_MIN_PER_CITY * len(need),
                                     self.workdir / f"lookup_{name}_{host}.out")
            try:
                entries = {e["city"]: e for e in _read_json(report)["cities"]}
            except (OSError, ValueError, KeyError, UnicodeDecodeError):
                entries = {}
            still = []
            for city in need:
                e = entries.get(city) or {"status": "failed", "reason": f"the lookup left no entry for it "
                                          f"(exit {code}): {_last_line(text)}"}
                if e["status"] in ("failed", "not asked"):
                    still.append(city)
                    self.c(city)["area"] = {"status": "failed", "mirror": host,
                                            "reason": f"area lookup: {e.get('reason')}"}
                else:
                    self.c(city)["area"] = {
                        "status": e["status"], "mirror": host, "level": e.get("level"),
                        "reason": e.get("reason"), "relations": [r["id"] for r in e.get("relations") or []],
                        "candidates": e.get("candidates") or []}
            if still:
                self.not_before[host] = self.fx.clock() + OVERLOAD_WAIT_S
            need = still
            try:
                self.plan = _read_json(self.plan_path)
            except (OSError, ValueError, UnicodeDecodeError):
                pass
            self.save()

    # --- step 2: the scaffold ------------------------------------------------

    def step_scaffold(self, name, cities):
        named, built = self.fx.languages()
        todo = {}
        for city in cities:
            rec = self.c(city)
            was = rec.get("scaffold") or {}
            # A city held for want of an area is looked at again each run:
            # its lookup may have answered since, or a person filled it in.
            if (was.get("status") and was.get("kind") != "area") or self.out_of_time():
                continue
            spec = self.plan["cities"].get(city)
            facts = self.fx.facts(city)
            if facts.get("scaffolded"):
                rec["scaffold"] = {"status": "already"}
                rec["started"] = True
            elif not isinstance(spec, dict) or not spec.get("relations"):
                rec["scaffold"] = {"status": "held", "kind": "area", "reason": "no area in the plan"}
            else:
                new = [code for code in spec.get("languages") or [] if code not in named or code not in built]
                if new:
                    why = "; ".join(f"{code!r} is not in place_index.LANGUAGE_NAMES" if code not in named
                                    else f"{code!r} has no built city yet" for code in new)
                    rec["scaffold"] = {"status": "held", "kind": "new language",
                                       "reason": f"not scaffolded, a new language is done first and by "
                                                 f"hand: {why}"}
                else:
                    todo[city] = {k: spec.get(k) for k in ("relations", "languages", "fold")}
        if todo:
            # Marked before anything is written, so a run stopped in the
            # middle of the scaffold still knows these cities' files as its
            # own when it resumes.
            for city in todo:
                self.c(city)["started"] = True
            self.save()
            copy = {"date": self.date, "cities": todo}
            copy_path = self.workdir / f"plan_{name}.json"
            _write_bytes(copy_path, json.dumps(copy, ensure_ascii=False, indent=2) + "\n")
            self.out(f"{name}: scaffolding {len(todo)} cities")
            try:
                _, lines = self.fx.scaffold(copy, str(copy_path))
            except Exception as exc:
                lines = [f"scaffold error: {type(exc).__name__}: {exc}"]
            results = parse_scaffold(lines)
            for city in todo:
                status, reason = results.get(city, ("refused", "the scaffold gave no result for it: "
                                                    + (_last_line("\n".join(lines)) or "no output")))
                self.c(city)["scaffold"] = {"status": status, "reason": reason}
        self.save()

    # --- step 3: the fetch queues ----------------------------------------------

    def set_aside(self, host, why):
        m = self.mirror(host)
        first = m["aside"] is None
        m.update(aside={"why": why, "at": self.fx.clock()}, probe=False)
        if first:
            other = [h for h in self.hosts if h != host and self.usable(h)]
            moved = (f"its remaining cities move to {other[0]}"
                     + ("" if other[0] == HEAVY_MIRROR else ", the heavy ones wait: only "
                        f"{HEAVY_MIRROR} takes them") if other
                     else "no mirror is left for place fetches")
            self.change(f"set {host} aside for place fetches: {why}; {moved}")
        if not any(self.usable(h) for h in self.hosts):
            self.top(f"No Overpass mirror was healthy for place fetches from {self.hhmm()} UTC: "
                     f"fetching stopped while lookups, scaffolds and builds of cached cities went on, "
                     f"and the mirrors were tried again every {RETRY_MIN} minutes.")

    def maybe_probe(self):
        """Rule b: with every mirror set aside for RETRY_MIN minutes, give
        each one city to show whether it is back."""
        states = [self.mirror(h) for h in self.hosts]
        if any(m["aside"] is None or m["probe"] for m in states):
            return
        if self.fx.clock() - max(m["aside"]["at"] for m in states) < RETRY_MIN * 60:
            return
        for m in states:
            m["probe"] = True
        self.change(f"no mirror healthy for {RETRY_MIN} minutes: each is tried again with one city")

    def take_batch(self, host, pending):
        """The next cities for `host`'s queue, taken out of `pending`: light
        ones for any mirror, heavy ones for HEAVY_MIRROR only, a city fetched
        in tiles alone, one city only for a mirror being tried again."""
        size = 1 if self.mirror(host)["probe"] else QUEUE_BATCH
        batch = []
        for city in list(pending):
            rec = self.c(city)
            if rec.get("heavy") and host != HEAVY_MIRROR:
                continue
            if rec.get("split"):
                if batch:
                    continue
                batch = [city]
                break
            batch.append(city)
            if len(batch) == size:
                break
        for city in batch:
            pending.remove(city)
        return batch

    def absorb(self, host, batch, text, code, pending):
        """Read one finished queue's log into the cities' records and the
        mirror's health; a city that may be tried again goes back to
        `pending`."""
        events = parse_queue_log(text)
        m = self.mirror(host)
        on_probe, mirror_failed, mirror_ok, refused = m["probe"], False, False, False
        for city in batch:
            rec = self.c(city)
            fetch = rec.setdefault("fetch", {"tries": 0, "attempts": []})
            fetch["status"], last, stale = None, "", False
            mine = events.get(city) or [{"what": "failed", "final": True, "exit": code, "seconds": 0.0,
                                         "last": f"the queue left no line for it (exit {code}): "
                                                 f"{_last_line(text)}"}]
            for ev in mine:
                if ev["what"] in ("fetched", "skipped"):
                    fetch["status"] = "fetched" if ev["what"] == "fetched" else "cached"
                    fetch["attempts"].append({"mirror": host, "kind": "ok", "seconds": ev["seconds"]})
                    mirror_ok = True
                    m["recent"] = (m["recent"] + [True])[-MIRROR_FAIL_WINDOW:]
                    continue
                if ev["what"] == "not queued":
                    fetch.update(status="failed", reason=f"not queued: {ev['last']}")
                    fetch["attempts"].append({"mirror": host, "kind": "other", "seconds": 0.0})
                    continue
                kind, codes = classify_failure(ev["exit"], ev["last"])
                last = ev["last"]
                fetch["attempts"].append({"mirror": host, "kind": kind, "codes": codes,
                                          "seconds": ev["seconds"], "exit": ev["exit"]})
                if kind == "scope":
                    fetch.update(status="scope stop", reason=ev["last"])
                elif kind == "stale":
                    refused = mirror_failed = stale = True
                    dated = re.search(r"data dated (\S+?),", ev["last"])
                    if m["aside"] is None or m["probe"]:
                        self.set_aside(host, f"the age guard refused its answer for {city} (data dated "
                                             f"{dated.group(1) if dated else 'unknown'})")
                else:
                    fetch["tries"] += 1
                    if kind in ("mirror", "timeout"):
                        refused = mirror_failed = True
                        m["recent"] = (m["recent"] + [False])[-MIRROR_FAIL_WINDOW:]
                        if (m["aside"] is None and len(m["recent"]) == MIRROR_FAIL_WINDOW
                                and not any(m["recent"])):
                            self.set_aside(host, f"its last {MIRROR_FAIL_WINDOW} fetches all failed "
                                                 f"(the last, {city}"
                                                 + (f", HTTP {', '.join(codes)}" if codes else "") + ")")
            if fetch["status"] is None:
                fetch["reason"] = last
                # A city fetched in tiles had its SPLIT_RETRIES rounds inside
                # the queue; a refusal by the age guard counts against no city.
                if fetch["tries"] >= CITY_MAX_TRIES or (rec.get("split") and not stale):
                    fetch["status"] = "failed"
                else:
                    pending.insert(0, city)
        if on_probe:
            if mirror_failed:
                m.update(probe=False)
                m["aside"]["at"] = self.fx.clock()
                self.change(f"{host} tried again with {', '.join(batch)}: still failing")
            elif mirror_ok:
                m.update(probe=False, aside=None, recent=[True])
                self.change(f"{host} tried again with {', '.join(batch)}: it answered and is back in use")
        if refused:
            self.not_before[host] = self.fx.clock() + OVERLOAD_WAIT_S

    def step_fetch(self, name, cities):
        pending = []
        for city in cities:
            rec = self.c(city)
            if (rec.get("scaffold") or {}).get("status") not in SCAFFOLDED:
                continue
            if (rec.get("fetch") or {}).get("status") in FETCH_DONE:
                continue
            facts = self.fx.facts(city)
            if facts.get("caches") is None and not facts.get("error"):
                rec.setdefault("fetch", {"tries": 0, "attempts": []})["status"] = "cached"
            else:
                pending.append(city)
        running = self.running
        while True:
            self.maybe_probe()
            for host in self.hosts:
                if (host in running or not self.usable(host) or self.out_of_time()
                        or self.fx.clock() < self.not_before.get(host, 0)):
                    continue
                batch = self.take_batch(host, pending)
                if not batch:
                    continue
                flying = {c for _, b, _ in running.values() for c in b}
                assert not flying & set(batch), "a city in two queues"
                self.started_queues += 1
                log = self.workdir / f"queue_{name}_{self.state['runs']}_{self.started_queues}_{host}.log"
                split = any(self.c(c).get("split") for c in batch)
                argv = self.python(QUEUE_SCRIPT, *batch, "--log", str(log), "--host", host,
                                   "--retries", str(SPLIT_RETRIES if split else 1))
                self.out(f"{name}: queue on {host}: {', '.join(batch)}")
                running[host] = (self.fx.spawn(argv, log.with_suffix(".out")), batch, log)
            if not running:
                waits = [self.not_before[h] - self.fx.clock() for h in self.hosts
                         if self.usable(h) and self.not_before.get(h, 0) > self.fx.clock()
                         and any(not self.c(c).get("heavy") or h == HEAVY_MIRROR for c in pending)]
                if pending and waits and not self.out_of_time():
                    self.fx.sleep(min(waits))
                    continue
                break
            done = [h for h in running if running[h][0].poll() is not None]
            if not done:
                if not self.build_one(cities):
                    self.fx.sleep(POLL_S)
                continue
            for host in done:
                child, batch, log = running.pop(host)
                try:
                    text = log.read_bytes().decode("utf-8", errors="replace")
                except OSError:
                    text = ""
                self.absorb(host, batch, text, child.poll(), pending)
                self.save()
        for city in pending:
            rec = self.c(city)
            if self.out_of_time():
                why = f"not started: the run reached its {self.max_hours:g} hours."
            elif rec.get("heavy") and not (HEAVY_MIRROR in self.hosts and self.usable(HEAVY_MIRROR)):
                why = (f"a heavy city ({rec.get('stations')} stations"
                       + (", fetched in tiles" if rec.get("split") else "") + f"), and {HEAVY_MIRROR}, "
                       f"the only mirror it may ask, is set aside or not in --hosts.")
            else:
                why = "no mirror was healthy for place fetches."
            rec.setdefault("fetch", {"tries": 0, "attempts": []}).update(status="waiting", reason=why)
        self.save()

    # --- step 4: the index builds and their checks -----------------------------

    def build_one(self, cities):
        """Build the first city of the wave whose caches are in and whose
        index is not built. False when there is none."""
        for city in cities:
            rec = self.c(city)
            if ((rec.get("fetch") or {}).get("status") in FETCH_IN
                    and (rec.get("build") or {}).get("status") not in BUILD_DONE
                    and not rec.get("gate_refused_this_run") and not self.out_of_time()):
                self.build(city)
                return True
        return False

    def build(self, city):
        rec = self.c(city)
        argv = self.python(GATE_SCRIPT, "run", "--label", f"{city}-place-index",
                           "--peak-gb", f"{BUILD_PEAK_GB:g}", "--estimate", BUILD_ESTIMATE,
                           "--session", self.session, "--wait", str(BUILD_WAIT_MIN), "--",
                           sys.executable, f"pipeline/{city}/step2b_place_index.py")
        self.out(f"{rec['wave']}: index build of {city}")
        began = self.fx.clock()
        code, text = self.fx.run(argv, BUILD_WAIT_MIN + BUILD_TIMEOUT_MIN,
                                 self.workdir / f"build_{city}.out")
        minutes = round((self.fx.clock() - began) / 60, 1)
        if code == 0:
            rec["build"] = {"status": "built", "minutes": minutes}
            try:
                raw = self.fx.checks(city)
                raw["findings"] = findings_of(raw, self.state["bars"])
            except Exception as exc:
                raw = {"findings": [{"kind": "check", "text": f"the checks could not be run: "
                                                              f"{type(exc).__name__}: {exc}"}]}
            for key in ("problems", "scope_problems"):
                raw.pop(key, None)
            rec["checks"] = raw
        elif code == 3 and "REFUSED:" in text:
            # Not a finished step: the gate had no room. A rerun builds it.
            rec["build"] = {"status": "gate refused", "minutes": minutes}
            rec["gate_refused_this_run"] = True
        else:
            reason = _last_line(text)
            kind = ("coverage" if "have no indexed place within" in text
                    else "language" if "declared local language" in text else "check")
            rec["build"] = {"status": "failed", "exit": code, "minutes": minutes,
                            "kind": kind, "reason": reason}
        self.save()

    def step_build(self, cities):
        while self.build_one(cities):
            pass

    # --- the night -------------------------------------------------------------

    def waiting(self):
        return [c for c, rec in self.state["cities"].items()
                if (rec.get("fetch") or {}).get("status") == "waiting"]

    def run(self):
        self.prepare()
        for rec in self.state["cities"].values():
            rec.pop("gate_refused_this_run", None)
        self.save()
        for index in range(len(self.waves)):
            # Rule d: this wave starts only now, when every city of the one
            # before has been taken as far as it could go.
            self.order_wave(index)
            name, cities = self.waves[index]
            self.out(f"== {name}: {len(cities)} cities")
            self.step_lookup(name, cities)
            self.step_scaffold(name, cities)
            self.step_fetch(name, cities)
            self.step_build(cities)
        # Rule b: cities still waiting because no mirror is healthy are
        # tried again every RETRY_MIN minutes until the hours run out.
        while self.waiting() and not any(self.usable(h) for h in self.hosts) and not self.out_of_time():
            states = [self.mirror(h) for h in self.hosts]
            wait = max(m["aside"]["at"] for m in states) + RETRY_MIN * 60 - self.fx.clock()
            if wait > self.t0 + self.max_hours * 3600 - self.fx.clock():
                break
            if wait > 0:
                self.fx.sleep(wait)
            before = self.started_queues
            for name, cities in self.waves:
                self.step_fetch(name, cities)
                self.step_build(cities)
            if self.started_queues == before:
                break
        if self.out_of_time():
            unreached = [c for _, names in self.waves for c in names
                         if not (self.c(c).get("scaffold") or {}).get("status")]
            self.top(f"The run reached its {self.max_hours:g} hours and started no new work after "
                     f"that" + (f"; {len(unreached)} cities were not reached." if unreached else "."))
        self.state["finished"] = True
        self.save()
        self.out(f"Report: {self.report_path}")
        return 0

    def dry_run(self, refusal):
        """Print the whole plan of action from what is on disk. Starts no
        child, takes no lock and writes no file."""
        out = self.out
        if refusal:
            out(f"A real run would be REFUSED here: {refusal}")
        named, built = self.fx.languages()
        listing = self.fx.listing()
        out(f"Night of {self.date}: {len(self.waves)} wave(s), mirrors {', '.join(self.hosts)}, at most "
            f"{self.max_hours:g} hours, session {self.session}"
            + (" (resuming the state file)" if self.resumed else ""))
        for name, cities in self.waves:
            out("")
            out(f"== {name}: {len(cities)} cities")
            look, scaffold, heavy, light, cached = [], [], [], [], []
            for city in cities:
                spec = self.plan["cities"].get(city)
                facts = self.fx.facts(city)
                country = (listing.get(city) or (None, None))[0]
                weight = "heavy" if is_heavy(facts.get("stations"), facts.get("split")) else "light"
                parts = [f"{country or 'country unknown'}, {facts.get('stations')} stations, {weight}"]
                ok = True
                if facts.get("error"):
                    parts.append(f"SKIPPED: {facts['error']}")
                    ok = False
                elif not isinstance(spec, dict):
                    parts.append("SKIPPED: not in the plan")
                    ok = False
                elif spec.get("relations"):
                    parts.append(f"area in the plan ({len(spec['relations'])} relation(s))")
                else:
                    parts.append("area: to look up; scaffolded only if it resolves")
                    look.append(city)
                if ok:
                    new = [code for code in spec.get("languages") or [] if code not in named or code not in built]
                    if facts.get("scaffolded"):
                        parts.append("already scaffolded")
                    elif new:
                        parts.append(f"HELD, new language {', '.join(new)}: done first and by hand")
                        ok = False
                    else:
                        parts.append("scaffold")
                        scaffold.append(city)
                if ok:
                    if facts.get("caches") is None:
                        parts.append("caches on disk, no fetch")
                        cached.append(city)
                    else:
                        parts.append(f"fetch on {HEAVY_MIRROR} only" if weight == "heavy"
                                     else "fetch on either mirror")
                        (heavy if weight == "heavy" else light).append(city)
                    parts.append("index build through the job gate, then the checks")
                out(f"  {city}: " + "; ".join(parts))
            lookup_hosts = [h for h in LOOKUP_ORDER if h in self.hosts]
            if look:
                out("  1. " + " ".join(self.python(LOOKUP_SCRIPT, str(self.plan_path), f"<{len(look)} cities>",
                                                   "--host", lookup_hosts[0], "--wait", str(LOOKUP_WAIT_MIN),
                                                   "--report", "<file>")))
            out(f"  2. scaffold up to {len(scaffold)} cities from a plan copy dated {self.date}")
            out(f"  3. fetch queues of {QUEUE_BATCH}: {len(heavy)} heavy on {HEAVY_MIRROR}, {len(light)} light "
                f"on {' and '.join(self.hosts)}; {len(cached)} cached")
            out("  4. per city: " + " ".join(self.python(
                GATE_SCRIPT, "run", "--label", "<city>-place-index", "--peak-gb", f"{BUILD_PEAK_GB:g}",
                "--estimate", "<basis>", "--session", self.session, "--wait", str(BUILD_WAIT_MIN), "--",
                "python", "pipeline/<city>/step2b_place_index.py")))
        out("")
        out("dry run: no child was started, no lock taken and nothing written")
        return 0


def main(argv=None, fx=None, out=print):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--waves", required=True, metavar="FILE", help="the waves JSON")
    ap.add_argument("--plan", required=True, metavar="FILE", help="the scaffold plan covering them")
    ap.add_argument("--report", required=True, metavar="FILE", help="the morning report, Markdown")
    ap.add_argument("--state", required=True, metavar="FILE", help="the state JSON a rerun resumes from")
    ap.add_argument("--session", required=True, metavar="NAME", help="the name given to the job gate")
    ap.add_argument("--hosts", default=",".join(MIRRORS), metavar="A,B",
                    help="the mirrors to use: " + ", ".join(MIRRORS))
    ap.add_argument("--max-hours", type=float, default=10.0, metavar="H",
                    help="start no new work after this many hours (default 10)")
    ap.add_argument("--retry-failed", action="store_true",
                    help="clear the failed steps the state file holds and try them again")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the whole plan of action; start nothing, write nothing")
    args = ap.parse_args(argv)
    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    unknown = [h for h in hosts if h not in MIRRORS]
    if unknown:
        ap.error(f"--hosts: {', '.join(unknown)} is not one of {', '.join(MIRRORS)}")
    night = Night(waves_path=args.waves, plan_path=args.plan, report_path=args.report,
                  state_path=args.state, hosts=hosts, session=args.session,
                  max_hours=args.max_hours, fx=fx or Real(), out=out,
                  retry_failed=args.retry_failed)
    why = night.load()
    if why:
        out(f"Cannot run: {why}")
        return 2
    try:
        refusal = night.refusal()
    except RuntimeError as exc:
        out(f"Cannot run: {exc}")
        return 2
    if args.dry_run:
        return night.dry_run(refusal)
    if refusal:
        out(f"Refused: {refusal}")
        return 2
    try:
        return night.run()
    except KeyboardInterrupt:
        # No queue is left running with nobody to read its log: an orphaned
        # child would hold its mirror's lock and its memory.
        for child, batch, _ in night.running.values():
            if hasattr(child, "stop"):
                child.stop()
            out(f"interrupted: stopped the queue of {', '.join(batch)}")
        night.running.clear()
        night.save()
        out(f"interrupted: the state is saved, a rerun resumes. Report so far: {night.report_path}")
        return 130


def selftest():
    import tempfile

    import place_search_fetch_queue as queue

    cases = []

    def report(label, ok):
        cases.append((label, bool(ok)))
        print(f"  {'ok ' if ok else 'BAD'} {label}")

    stale_line = ("RuntimeError: the pinned Overpass mirror failed, which is a HOST problem or an "
                  "over-expensive QUERY and not a fact about this city - overpass.kumi.systems: data "
                  "dated 2026-05-31T00:00:00Z, older than 7 days")
    http_line = ("RuntimeError: the pinned Overpass mirror failed, which is a HOST problem or an "
                 "over-expensive QUERY and not a fact about this city - overpass-api.de: HTTPError 504 "
                 "(504/429/timeout - try nodes-only, drop out center)")
    scope_line = ("s1: the search area breaks the scope rule, nothing else fetched: Beta (relation/2) "
                  "holds none of the map's stations and has no entry in config.PLACE_AREA_KEPT. Take it "
                  "out of config.PLACE_AREA, or record the owner's word for it in PLACE_AREA_KEPT")
    clean = {"rows": 1200, "index": [500, 200], "streets": [400, 150], "crossings": [100, 40],
             "languages": "{'en': 0.99} -> ['English']", "stations": 10,
             "area": [{"osm": "relation/1", "name": "Alpha", "stations": 10}],
             "problems": [], "scope_problems": [], "notes": []}

    class Fake:
        """Stands in for every effect: a clock that only sleep() moves, git
        answers, the real fetch queue driven by a stand-in runner, and
        canned lookups, scaffolds, builds and checks."""

        def __init__(self, tmp, *, branch="wave-2", dirty=(), stations=None, fetch=None,
                     cached=(), lookup=None, refuse=None, checks=None, build=None, splits=()):
            self.tmp, self.branch, self.dirty = Path(tmp), branch, list(dirty)
            self.stations, self.fetch = stations or {}, fetch or {}
            self.have, self.lookup_plan = set(cached), lookup or {}
            self.refuse, self.check_plan, self.build_plan = refuse or {}, checks or {}, build or {}
            self.splits, self.scaffolded = set(splits), set()
            self.t, self.slept = 0.0, []
            self.queues, self.lookups, self.scaffolds, self.builds = [], [], [], []
            self.tries, self.open, self.max_open, self.shared = {}, {}, 0, False

        def clock(self):
            return self.t

        def sleep(self, seconds):
            self.slept.append(seconds)
            self.t += seconds

        def now(self):
            base = datetime.datetime(2026, 10, 13, 20, 0, tzinfo=datetime.timezone.utc)
            return (base + datetime.timedelta(seconds=self.t)).strftime("%Y-%m-%dT%H:%M:%SZ")

        def git(self, args):
            return self.branch + "\n" if args[0] == "branch" else "".join(f" M {p}\n" for p in self.dirty)

        def listing(self):
            return {c: (("Japan" if c.startswith("j") else "Testland"), c.title()) for c in self.stations}

        def facts(self, city):
            if city not in self.stations:
                return {"error": f"no pipeline/{city}/config.py"}
            return {"stations": self.stations[city], "split": city in self.splits,
                    "scaffolded": city in self.scaffolded,
                    "caches": None if city in self.have and city in self.scaffolded else "PLACE_OSM_JSON missing"}

        def languages(self):
            return {"en", "ja", "de"}, {"en", "ja"}

        def bars(self):
            return {"index": 1000, "index_city": "big", "streets": 1000, "streets_city": "big"}

        def pages(self, city):
            return [f"app/pages/1_{city}_Heatmap.py"]

        def scaffold(self, plan, label):
            self.scaffolds.append(sorted(plan["cities"]))
            lines = ["", f"{'CITY':<26} RESULT"]
            for city in plan["cities"]:
                if city in self.refuse:
                    lines.append(f"{city:<26} refused: {self.refuse[city]}")
                else:
                    self.scaffolded.add(city)
                    lines.append(f"{city:<26} done")
            return not self.refuse, lines

        def checks(self, city):
            return json.loads(json.dumps(self.check_plan.get(city, clean)))

        def outcome(self, city, host):
            plan = self.fetch.get((city, host), self.fetch.get(host, self.fetch.get(city, "ok")))
            if isinstance(plan, list):
                return plan.pop(0) if plan else "ok"
            return plan

        def spawn(self, argv, out_path):
            cities = argv[2:argv.index("--log")]
            host, log = argv[argv.index("--host") + 1], argv[argv.index("--log") + 1]
            retries = int(argv[argv.index("--retries") + 1])
            if any(set(cities) & set(other) for other in self.open.values()):
                self.shared = True
            self.open[host] = cities
            self.max_open = max(self.max_open, len(self.open))
            self.queues.append((host, list(cities)))
            fake = self

            class Handle:
                code = None

                def poll(self):
                    if self.code is None:
                        def runner(city):
                            fake.tries[city] = fake.tries.get(city, 0) + 1
                            what = fake.outcome(city, host)
                            if what == "ok":
                                fake.have.add(city)
                                return 0, "recorded in outputs/x/provenance.json as osm_places_extra"
                            return 1, {"504": http_line, "stale": stale_line, "scope": scope_line}[what]
                        self.code = queue.run_queue(
                            cities, runner=runner, config_reader=lambda c: (c, c, None),
                            cached=lambda c, a, b: None if c in fake.have else "PLACE_OSM_JSON missing",
                            out=lambda line: None, log=Path(log), retries=retries)
                        fake.t += 600
                        del fake.open[host]
                    return self.code

            Path(log).parent.mkdir(parents=True, exist_ok=True)
            return Handle()

        def run(self, argv, timeout_min, out_path):
            if argv[1] == LOOKUP_SCRIPT:
                plan_path = Path(argv[2])
                cities = argv[3:argv.index("--host")]
                host, rep = argv[argv.index("--host") + 1], argv[argv.index("--report") + 1]
                self.lookups.append((host, list(cities)))
                plan = _read_json(plan_path)
                entries = []
                for city in cities:
                    got = self.lookup_plan.get((city, host), self.lookup_plan.get(city, [77]))
                    if got == "failed":
                        entries.append({"city": city, "status": "failed", "reason": f"lookup failed on {host}"})
                    elif isinstance(got, str):
                        entries.append({"city": city, "status": "unresolved", "reason": got, "level": None,
                                        "relations": [], "candidates": [{"id": 5, "name": "Cand", "level": 6}]})
                    else:
                        plan["cities"][city]["relations"] = got
                        entries.append({"city": city, "status": "resolved", "level": 8, "reason": None,
                                        "relations": [{"id": r, "name": "R", "level": 8} for r in got]})
                _write_bytes(plan_path, json.dumps(plan))
                _write_bytes(rep, json.dumps({"cities": entries}))
                return 0, ""
            city = argv[argv.index("--label") + 1].replace("-place-index", "")
            self.builds.append(list(argv))
            self.t += 120
            return self.build_plan.get(city, (0, "ENDED: x: exit 0, measured peak 0.20 GB"))

    def night(tmp, fake, waves, specs, **kw):
        """One run in a temporary folder; returns (exit code, state, report
        text, printed lines). The plan and waves files are written only when
        they are not there yet, so a second call resumes."""
        tmp = Path(tmp)
        if not (tmp / "plan.json").exists():
            _write_bytes(tmp / "plan.json", json.dumps({"draft": True, "date": "2026-10-13", "cities": {
                c: {"relations": rel, "languages": [lang], "fold": None} for c, (rel, lang) in specs.items()}}))
            _write_bytes(tmp / "waves.json", json.dumps({"date": "2026-10-14", "waves": [
                {"name": n, "cities": cs} for n, cs in waves]}))
        lines = []
        argv = ["--waves", str(tmp / "waves.json"), "--plan", str(tmp / "plan.json"),
                "--report", str(tmp / "report.md"), "--state", str(tmp / "state.json"),
                "--session", "night-test", "--max-hours", str(kw.pop("max_hours", 10))] + kw.pop("extra", [])
        code = main(argv, fx=fake, out=lines.append)
        state = _read_json(tmp / "state.json") if (tmp / "state.json").exists() else None
        text = (tmp / "report.md").read_bytes().decode("utf-8") if (tmp / "report.md").exists() else ""
        return code, state, text, "\n".join(lines)

    one = [("wave2", ["a", "b"])]
    two_specs = {"a": ([1], "en"), "b": ([2], "en")}

    # Written out, not read from PROTECTED_BRANCHES: a branch dropped from
    # the constant must fail here.
    for branch in ("master", "worktree-cleanup", ""):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Fake(tmp, branch=branch, stations={"a": 10, "b": 10})
            code, state, text, said = night(tmp, fake, one, two_specs)
            report(f"refuses on {branch or 'a detached HEAD'}, naming the wave's own branch, and starts nothing",
                   code == 2 and "lives on its own branch" in said and state is None and not text
                   and not fake.queues and not fake.scaffolds and not fake.builds)
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, dirty=["pipeline/place_index.py"], stations={"a": 10, "b": 10})
        code, state, text, said = night(tmp, fake, one, two_specs)
        report("refuses on a working tree that is not clean at the start",
               code == 2 and "pipeline/place_index.py" in said and "clean at the start" in said
               and state is None and not fake.scaffolds)

    # The whole path on two waves: a lookup, a new language, an unresolved
    # area, a heavy city, a scope stop, a rule E name, a size over the bar.
    import check_place_search as cps
    leak_index = {"languages": {"local": ["ja"]}, "rows": [[0, 1, 2, "リッチモンドホテル", "", 0]]}
    leaky = dict(clean, problems=cps.check_leaks("x", leak_index, {}), index=[5000, 900])
    stations = {"a": 10, "b": 20, "h": 150, "n": 10, "u": 10, "s1": 10, "e": 10, "r": 10, "j1": 10}
    specs = {"a": ([1], "en"), "b": ([], "en"), "h": ([3], "en"), "n": ([4], "de"), "u": ([], "en"),
             "s1": ([6, 7], "en"), "e": ([8], "ja"), "r": ([9], "en"), "j1": ([10], "ja")}
    waves = [("wave2", ["a", "b", "h", "n", "u"]), ("wave3", ["s1", "e", "r", "j1"])]
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=stations, fetch={"s1": "scope"}, lookup={"b": [22, 21], "u": "no built city in Testland"},
                    refuse={"r": "page already contains search="}, checks={"e": leaky})
        code, state, text, said = night(tmp, fake, waves, specs)
        cities = state["cities"]
        report("the run ends with exit 0 whatever it found, and says it reached its end",
               code == 0 and state["finished"] and "The run reached its end." in text)
        report("only the entries with no relations are looked up, once, on the mirror kept for lookups",
               fake.lookups == [(LOOKUP_ORDER[0], ["b", "u"])] and cities["b"]["area"]["status"] == "resolved")
        report("a new language and an unresolved area are not scaffolded; the rest are, per wave",
               fake.scaffolds == [["a", "b", "h"], ["e", "j1", "r", "s1"]]
               and cities["n"]["scaffold"]["kind"] == "new language"
               and cities["u"]["scaffold"]["status"] == "held")
        report("two queues run at once and never share a city",
               fake.max_open == 2 and not fake.shared
               and sorted(c for _, cs in fake.queues for c in cs) == sorted(["a", "b", "h", "s1", "e", "j1"]))
        report("a heavy city is only ever asked of the heavy mirror",
               all(host == HEAVY_MIRROR for host, cs in fake.queues if "h" in cs) and cities["h"]["heavy"])
        gate = fake.builds[0]
        report("each index build starts through the job gate, with the session's name",
               gate[1:3] == [GATE_SCRIPT, "run"] and gate[gate.index("--session") + 1] == "night-test"
               and gate[-1].startswith("pipeline/") and gate[-1].endswith("/step2b_place_index.py")
               and "--wait" in gate and gate[gate.index("--") + 1] == sys.executable
               and sorted(g[g.index("--label") + 1] for g in fake.builds)
               == sorted(f"{c}-place-index" for c in ("a", "b", "h", "e", "j1")))
        report("the report lists the scope stop with the fetch's own message",
               "### A municipality with none of the map's stations" in text
               and "Beta (relation/2) holds none of the map's stations" in text
               and cities["s1"]["fetch"]["status"] == "scope stop")
        report("the report lists a rule E name, read from the real check's message",
               "### Rule E names" in text and "リッチモンドホテル" in text and "1 name(s)" in text)
        report("the report lists the new language, the unresolved area with a candidate, and the refusal",
               "### A new language" in text and "'de' has no built city yet" in text
               and "Cand (level 6, relation 5)" in text and "page already contains search=" in text)
        report("a size over the bar is flagged and stops nothing",
               "### A size over the bar" in text and "5,000 bytes" in text
               and cities["e"]["build"]["status"] == "built")
        report("the report says rule A was not run, what a session still owes, and has a row per city",
               "Rule A of check_place_search.py" in text and "## Still owed by a session" in text
               and "the browser test with one street picked" in text and "| j1 | Japan |" in text
               and "- Clean (built, no finding): 4" in text and "- Needing a call: 5" in text)
        report("the report holds no em dash and no carriage return",
               chr(0x2014) not in text and b"\r" not in (Path(tmp) / "report.md").read_bytes())
        report("the scaffold's plan copy carries the night's date and no draft marker",
               _read_json(Path(tmp) / "state_files" / "plan_wave2.json")
               == {"date": "2026-10-14", "cities": {
                   "a": {"relations": [1], "languages": ["en"], "fold": None},
                   "b": {"relations": [22, 21], "languages": ["en"], "fold": None},
                   "h": {"relations": [3], "languages": ["en"], "fold": None}}})

        # A second run with the same state: nothing finished is done again.
        counts = (len(fake.queues), len(fake.lookups), len(fake.scaffolds), len(fake.builds), dict(fake.tries))
        fake.dirty = ["pipeline/a/config.py", "app/static/places/streets/b.json", "outputs/h/place_search.json",
                      "app/pages/1_a_Heatmap.py"]
        code, state2, text2, said = night(tmp, fake, waves, specs)
        report("a resumed run accepts its own cities' files and repeats nothing",
               code == 0 and state2["runs"] == 2
               and counts == (len(fake.queues), len(fake.lookups), len(fake.scaffolds), len(fake.builds),
                              dict(fake.tries)))
        fake.dirty.append("pipeline/map_common.py")
        code, _, _, said = night(tmp, fake, waves, specs)
        report("a resumed run still refuses a change that is not its own",
               code == 2 and "pipeline/map_common.py" in said and "pipeline/a/config.py" not in said)
        fake.dirty = []
        code, state3, _, _ = night(tmp, fake, waves, specs, extra=["--retry-failed"])
        report("--retry-failed clears the failed steps and tries them once more",
               code == 0 and fake.scaffolds[-1] == ["r"] and fake.tries["s1"] == 4
               and any("--retry-failed" in c for c in state3["changes"]))

    # Rule a: a mirror set aside after its last fetches all failed.
    lights = {f"l{i}": 10 for i in range(1, 7)}
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=dict(lights, h1=300, h2=120), fetch={MIRRORS[1]: "504"})
        names = ["h1", "l1", "l2", "l3", "l4", "h2", "l5", "l6"]
        code, state, text, _ = night(tmp, fake, [("wave2", names)], {c: ([1], "en") for c in names})
        kumi = [cs for host, cs in fake.queues if host == MIRRORS[1]]
        burned = [c for c in names if state["cities"][c]["fetch"]["status"] == "failed"]
        report("a mirror whose last fetches all failed is set aside after one batch",
               len(kumi) == 1 and state["mirrors"][MIRRORS[1]]["aside"] is not None
               and "set overpass.kumi.systems aside" in text and "HTTP 504" in text)
        report("its light cities move to the other mirror, and no heavy city ever asked it",
               all(not state["cities"][c]["heavy"] for cs in kumi for c in cs)
               and sorted(burned) == sorted(kumi[0])
               and all(state["cities"][c]["fetch"]["status"] == "fetched" for c in names if c not in burned)
               and all(a["mirror"] == HEAVY_MIRROR for c in ("h1", "h2")
                       for a in state["cities"][c]["fetch"]["attempts"]))
        report("a city that failed twice is not tried a third time, and is listed",
               all(fake.tries[c] == CITY_MAX_TRIES for c in burned)
               and "### A fetch that failed twice" in text and f"**{burned[0]}**" in text)
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=dict(lights, h1=300), fetch={HEAVY_MIRROR: "504"})
        names = ["l1", "l2", "h1", "l3", "l4", "l5", "l6"]
        code, state, text, _ = night(tmp, fake, [("wave2", names)], {c: ([1], "en") for c in names})
        report("with the heavy mirror set aside, heavy cities wait and are never moved to the other",
               state["cities"]["h1"]["fetch"]["status"] == "waiting"
               and all("h1" not in cs for host, cs in fake.queues if host == MIRRORS[1])
               and "### Not fetched this night" in text and "the only mirror it may ask" in text
               and "the heavy ones wait" in text)
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=lights, fetch={MIRRORS[1]: "stale"})
        names = sorted(lights)
        code, state, text, _ = night(tmp, fake, [("wave2", names)], {c: ([1], "en") for c in names})
        report("an answer the age guard refused sets the mirror aside at once, and the city is fetched elsewhere",
               len([1 for host, _ in fake.queues if host == MIRRORS[1]]) == 1
               and "the age guard refused its answer" in text and "2026-05-31" in text
               and all(state["cities"][c]["fetch"]["status"] == "fetched" for c in names))

    # Rule b: no healthy mirror.
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=dict(lights, c1=10), cached=("c1",),
                    fetch={MIRRORS[0]: "504", MIRRORS[1]: "504"})
        fake.scaffolded.add("c1")
        names = ["c1"] + sorted(lights)
        code, state, text, _ = night(tmp, fake, [("wave2", names)], {c: ([1], "en") for c in names},
                                     max_hours=4)
        probes = [cs for _, cs in fake.queues[2:]]
        report("with no healthy mirror fetching stops, and the cached city is still built",
               code == 0 and state["cities"]["c1"]["build"]["status"] == "built"
               and state["cities"]["c1"]["fetch"]["status"] == "cached"
               and len(fake.builds) == 1 and "No Overpass mirror was healthy for place fetches" in text
               and text.index("No Overpass mirror was healthy") < text.index("## Needs your call"))
        report("the mirrors are tried again with one city each, every RETRY_MIN, until the hours run out",
               probes and all(len(cs) == 1 for cs in probes)
               and any(s >= RETRY_MIN * 60 - 1300 for s in fake.slept)
               and fake.t <= 4 * 3600 + 1300 and "each is tried again with one city" in text)
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=lights,
                    fetch={MIRRORS[0]: ["504"] * 4, MIRRORS[1]: ["504"] * 4})
        names = sorted(lights)
        code, state, text, _ = night(tmp, fake, [("wave2", names)], {c: ([1], "en") for c in names})
        report("a mirror that answers when tried again is back in use and the waiting cities are fetched",
               "it answered and is back in use" in text
               and sum(1 for c in names if state["cities"][c]["fetch"]["status"] == "fetched") == 2
               and not [c for c in names if state["cities"][c]["fetch"]["status"] == "waiting"])

    # Rule d: the kinds that failed earlier go last in a later wave.
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations={"j1": 10, "t1": 10, "j2": 10, "t2": 10, "j3": 10},
                    fetch={"j1": "scope"})
        waves = [("wave2", ["j1", "t1"]), ("wave3", ["j2", "t2", "j3"])]
        code, state, text, _ = night(tmp, fake, waves, {c: ([1], "en") for c in fake.stations})
        later = [c for _, cs in fake.queues for c in cs if c in ("j2", "t2", "j3")]
        report("a later wave puts the country that failed earlier last, and says so",
               later[0] == "t2" and "wave3: reordered" in text and "Japan 1" in text)

    # The lookup's second mirror, and an area a person filled in afterwards.
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations={"a": 10, "b": 10},
                    lookup={("a", LOOKUP_ORDER[0]): "failed", "b": "several admin levels"})
        code, state, text, _ = night(tmp, fake, one, {"a": ([], "en"), "b": ([], "en")})
        report("a lookup that failed on one mirror is asked of the other, and only the failed city",
               fake.lookups == [(LOOKUP_ORDER[0], ["a", "b"]), (LOOKUP_ORDER[1], ["a"])]
               and state["cities"]["a"]["area"]["status"] == "resolved"
               and state["cities"]["a"]["build"]["status"] == "built"
               and state["cities"]["b"]["scaffold"]["kind"] == "area")
        plan = _read_json(Path(tmp) / "plan.json")
        plan["cities"]["b"]["relations"] = [55]
        _write_bytes(Path(tmp) / "plan.json", json.dumps(plan))
        fake.dirty = ["pipeline/a/config.py"]
        code, state, text, _ = night(tmp, fake, one, {})
        report("an area a person filled in the plan afterwards is taken up by the next run",
               len(fake.lookups) == 2 and fake.scaffolds[-1] == ["b"]
               and state["cities"]["b"]["area"]["status"] == "in plan"
               and state["cities"]["b"]["build"]["status"] == "built"
               and "An area that could not be resolved" not in text)

    # --max-hours, the job gate's refusal, a build that stops.
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations=lights)
        names = sorted(lights)
        code, state, text, _ = night(tmp, fake, [("wave2", names[:2]), ("wave3", names[2:])],
                                     {c: ([1], "en") for c in names}, max_hours=0.1)
        report("no new work starts after --max-hours, and the report says so at the top",
               code == 0 and all(c in names[:2] for _, cs in fake.queues for c in cs)
               and "started no new work" in text and "4 cities were not reached" in text)
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, stations={"a": 10, "b": 10},
                    build={"a": (3, "REFUSED: a-place-index: no room"),
                           "b": (1, "2 station(s) on the b map have no indexed place within 1 km: X, Y. "
                                    "config.PLACE_AREA does not cover the whole map\nENDED: b: exit 1")})
        code, state, text, _ = night(tmp, fake, one, two_specs)
        first = len(fake.builds)
        fake.build_plan = {}
        code, state2, text2, _ = night(tmp, fake, one, two_specs)
        report("a build the gate refused is not a finished step: the rerun builds it, and only it",
               state["cities"]["a"]["build"]["status"] == "gate refused" and first == 2
               and len(fake.builds) == 3 and state2["cities"]["a"]["build"]["status"] == "built")
        report("an index step stopped by its coverage rule is listed under coverage, with its message",
               state["cities"]["b"]["build"]["kind"] == "coverage"
               and "### Stations outside the area, or rule H coverage" in text
               and "have no indexed place within 1 km" in text)

    # The dry run.
    with tempfile.TemporaryDirectory() as tmp:
        fake = Fake(tmp, branch="master", stations={"a": 10, "h": 150, "n": 10, "u": 10})
        code, state, text, said = night(tmp, fake, [("wave2", ["a", "h", "n", "u"])],
                                        {"a": ([1], "en"), "h": ([2], "en"), "n": ([3], "de"), "u": ([], "en")},
                                        extra=["--dry-run"])
        left = sorted(p.name for p in Path(tmp).iterdir())
        report("a dry run prints the whole plan, says a real run would be refused, and touches nothing",
               code == 0 and "would be REFUSED" in said and "h: Testland, 150 stations, heavy" in said
               and "HELD, new language de" in said and "area: to look up" in said
               and "heavy_job.py run --label <city>-place-index" in said.replace("\\", "/")
               and left == ["plan.json", "waves.json"] and not fake.queues and not fake.lookups
               and not fake.scaffolds and not fake.builds)

    # The parsers, against the real scripts' own output.
    import place_search_scaffold
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_bytes(root / "pipeline" / "place_index.py",
                     'LANGUAGE_NAMES = {"en": "English"}\nFOLDS = (None, "ja")\n')
        _write_bytes(root / "pipeline" / "has_area" / "config.py", 'PLACE_AREA = "(id:1)"\n')
        plan = {"date": "2026-10-14", "cities": {
            "nowhere": {"relations": [1], "languages": ["en"], "fold": None},
            "has_area": {"relations": [1], "languages": ["en"], "fold": None}}}
        _, lines = place_search_scaffold.run_plan(root, plan, True)
        report("the scaffold's own table is read city by city, with each refusal's reason",
               parse_scaffold(lines) == {"nowhere": ("refused", "no config.py"),
                                         "has_area": ("refused", "config already contains PLACE_AREA")})
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "q.log"
        plan = {"a": [(1, http_line), (0, "ok")], "b": [(1, stale_line), (1, stale_line)], "c": [(0, "ok")]}
        have = set()

        def runner(city):
            code, last = plan[city].pop(0)
            if code == 0:
                have.add(city)
            return code, last

        queue.run_queue(["a", "b", "c", "d"], runner=runner, out=lambda line: None, log=log,
                        config_reader=lambda c: (None, None, "no config") if c == "d" else (c, c, None),
                        cached=lambda c, a, b: None if c in have else "PLACE_OSM_JSON missing")
        events = parse_queue_log(log.read_bytes().decode("utf-8"))
        report("the fetch queue's own log is read: a retry that fetched, a final failure, a city not queued",
               [e["what"] for e in events["a"]] == ["failed", "fetched"]
               and [(e["what"], e["final"]) for e in events["b"]] == [("failed", False), ("failed", True)]
               and events["c"][0]["what"] == "fetched" and events["d"][0]["what"] == "not queued"
               and classify_failure(events["a"][0]["exit"], events["a"][0]["last"]) == ("mirror", ["504"])
               and classify_failure(1, events["b"][1]["last"])[0] == "stale")
    report("failures are told apart: the scope stop, a held lock, a stopped child, anything else",
           classify_failure(1, scope_line)[0] == "scope"
           and classify_failure(1, "Another place fetch is running: x (pid 1, since y)")[0] == "lock"
           and classify_failure(124, "stopped after 180 min with no end")[0] == "timeout"
           and classify_failure(1, "ModuleNotFoundError: No module named 'x'")[0] == "other")
    thin = findings_of(dict(clean, stations=12, area=[{"name": "Alpha", "stations": 10},
                                                      {"name": "Beta", "stations": 1}],
                            scope_problems=["x: B. Gamma (relation/3) holds none of the map's stations"]),
                       {"index": 1000, "streets": 1000})
    report("findings: a station outside the area, a municipality on one station, a scope problem",
           sorted(f["kind"] for f in thin) == ["coverage", "scope", "thin"]
           and "1 of 12 map stations" in " ".join(f["text"] for f in thin))
    report("heavy is measured: the station count, tiles, or stations that cannot be counted",
           is_heavy(HEAVY_STATIONS, False) and not is_heavy(HEAVY_STATIONS - 1, False)
           and is_heavy(5, True) and is_heavy(None, False))

    osm_text = (ROOT / "pipeline" / "osm.py").read_bytes().decode("utf-8")
    block = osm_text.split("OVERPASS_HOSTS = (", 1)[1].split(")", 1)[0]
    wait = re.search(r"(?m)^OVERLOAD_WAIT_S = (\d+)", osm_text)
    report("MIRRORS and OVERLOAD_WAIT_S are pipeline/osm.py's, and the scripts named exist",
           tuple(re.findall(r"https://([^/]+)/", block)) == MIRRORS == queue.MIRRORS
           and HEAVY_MIRROR in MIRRORS and set(LOOKUP_ORDER) == set(MIRRORS)
           and wait and int(wait.group(1)) == OVERLOAD_WAIT_S
           and all((ROOT / s).is_file() for s in (LOOKUP_SCRIPT, QUEUE_SCRIPT, GATE_SCRIPT)))

    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
