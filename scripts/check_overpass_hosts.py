"""Every Overpass host this repository can query is a GLOBAL mirror.

    python scripts/check_overpass_hosts.py            # static: every host named in pipeline/ and scripts/
    python scripts/check_overpass_hosts.py --live     # also ask each host about two far-apart places
    python scripts/check_overpass_hosts.py --selftest # watch it refuse a regional extract; touches nothing

WHY. overpass.osm.ch serves a Swiss-only extract. For any query outside
Switzerland it answers HTTP 200 with an empty result, or zero counts for
`out count`, shaped exactly like "nothing here". It sat in three host lists
(pipeline/osm.py, pipeline/countries/mexico.py, scripts/brief_check.py) until
2026-09-27, when a screen got zeros for Daugavpils, Aarhus, Zoetermeer and
Amstelveen. The fetchers reject a fully empty answer,
but a rotation that lands on a regional extract is a silent hazard for any
new query shape, so the list itself is checked.

STATIC mode fails on a host that is known to be regional, and on any host not
in GLOBAL_HOSTS: a new mirror is added here only after `--live` has shown it
answering for places on different continents. LIVE mode queries each host
found for a count of railway stations in two small boxes (central Tokyo and
central São Paulo) and fails on zero from either. Live mode reaches the
network; it is a person's check, never part of a pipeline step.
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOBAL_HOSTS = {"overpass-api.de", "overpass.kumi.systems"}
KNOWN_REGIONAL = {"overpass.osm.ch": "Swiss-only extract - empty/zero answers elsewhere (2026-09-27)"}
HOST_RE = re.compile(r"https?://([A-Za-z0-9.-]+)/api/interpreter")
PROBES = {"Tokyo": (35.67, 139.75, 35.70, 139.78), "São Paulo": (-23.56, -46.65, -23.53, -46.62)}


def hosts_in(text):
    return set(HOST_RE.findall(text))


def scan():
    found = {}
    for sub in ("pipeline", "scripts"):
        for p in (ROOT / sub).rglob("*"):
            if (p.suffix not in (".py", ".mjs", ".js") or "__pycache__" in p.parts
                    or p.resolve() == Path(__file__).resolve()):   # its own selftest strings
                continue
            for h in hosts_in(p.read_text(encoding="utf-8", errors="replace")):
                found.setdefault(h, []).append(p.relative_to(ROOT).as_posix())
    return found


def verdicts(found):
    bad = []
    for h, files in sorted(found.items()):
        if h in KNOWN_REGIONAL:
            bad.append(f"{h} is a regional extract ({KNOWN_REGIONAL[h]}) - in {', '.join(files)}")
        elif h not in GLOBAL_HOSTS:
            bad.append(f"{h} is not a known global mirror - in {', '.join(files)}. Run --live, "
                       f"and add it to GLOBAL_HOSTS only if it answers for both probes")
    return bad


def live(hosts):
    bad = []
    for h in sorted(hosts):
        for place, (s, w, n, e) in PROBES.items():
            q = f'[out:json][timeout:60];node["railway"="station"]({s},{w},{n},{e});out count;'
            try:
                req = urllib.request.Request(f"https://{h}/api/interpreter", data=q.encode(),
                                             headers={"User-Agent": "expanded-heatmap host check"})
                with urllib.request.urlopen(req, timeout=90) as r:
                    els = json.loads(r.read().decode("utf-8")).get("elements") or []
                total = int((els[0].get("tags") or {}).get("nodes", 0)) if els else 0
                print(f"  {h:28} {place:10} {total} stations")
                if total == 0:
                    bad.append(f"{h} answered zero stations for {place} - not a global mirror")
            except Exception as exc:  # noqa: BLE001 - an outage is reported, not a regional verdict
                print(f"  {h:28} {place:10} unreachable ({type(exc).__name__})")
    return bad


def selftest():
    cases = [
        ('X = ("https://overpass.osm.ch/api/interpreter",)', "regional extract"),
        ('X = ("https://overpass.example.org/api/interpreter",)', "not a known global mirror"),
        ('X = ("https://overpass-api.de/api/interpreter",)', None),
    ]
    failed = 0
    for text, want in cases:
        got = verdicts({h: ["<selftest>"] for h in hosts_in(text)})
        ok = (not got) if want is None else (len(got) == 1 and want in got[0])
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {text[5:60]!r} -> {got[0][:70] if got else 'passes'}")
    print("selftest passed" if not failed else f"selftest FAILED: {failed}")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    found = scan()
    bad = verdicts(found)
    if a.live:
        bad += live(found)
    for b in bad:
        print("FAIL", b)
    print(f"{len(found)} Overpass host(s) named in the repository: {', '.join(sorted(found))}; "
          f"{len(bad)} problem(s).")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py
    # crashed on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
