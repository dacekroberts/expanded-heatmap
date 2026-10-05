"""Parse Wikipedia's "List of tram and light rail transit systems" wikitext into rows.

The coverage sweep of 2026-10-03 started from this list and "List of metro
systems"; `universe_europe.py` and `universe_france.py` were curated from the
rows this writes, and the Americas and Asia reports in `docs/coverage_sweep/`
from the same pages. Reads a local copy and never fetches: save the wikitext
first (the MediaWiki parse API, `action=parse&prop=wikitext`, because the
rendered page truncates), as `docs/coverage_sweep/README.md` describes.

Usage:
    python scripts/coverage_sweep/parse_wiki_tram.py [--wiki PATH] [--out PATH]

Defaults read and write under `data/_coverage_sweep/` (gitignored). Rows the
parser cannot shape into the eight-column layout are kept with a `raw` key and
counted on exit, so a changed table layout shows up as a jump in that count.
"""
import argparse
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DIR = os.path.join(ROOT, "data", "_coverage_sweep")


def clean(s):
    """Strip references, templates, links and tags down to the visible text."""
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref.*$", "", s, flags=re.S)
    s = re.sub(r"\{\{flag(?:country|icon)?\|([^}|]+)[^}]*\}\}", r"\1", s, flags=re.I)
    s = re.sub(r"\{\{convert\|([0-9.]+)\|[^}]*\}\}", r"\1 km", s)
    s = re.sub(r"\{\{([A-Z]{3})\}\}", r"\1", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def cellval(c):
    """Return (text, rowspan) for one table cell, dropping its attributes."""
    m = re.match(r"^\s*((?:rowspan|style|colspan|data-sort-value|align)[^|]*)\|(?!\|)(.*)$", c, flags=re.S)
    attrs = ""
    if m and "[[" not in m.group(1):
        attrs, c = m.group(1), m.group(2)
    rs = re.search(r'rowspan\s*=\s*"?(\d+)', attrs)
    return clean(c), int(rs.group(1)) if rs else 1


def parse(text):
    rows, section, cur = [], None, None
    for ln in text.split("\n"):
        if ln.startswith("==") and not ln.startswith("==="):
            section = ln.strip("= ")
            continue
        if ln.startswith("|-") or ln.startswith("|}"):
            if cur:
                rows.append((section, cur))
            cur = [] if ln.startswith("|-") else None
            continue
        if cur is not None and ln.startswith("|") and not ln.startswith("|+"):
            cur.extend(ln[1:].split("||"))
        elif cur is not None and cur and not ln.startswith("!"):
            cur[-1] += "\n" + ln

    out, country_carry = [], None
    for section, cells in rows:
        vals = [cellval(c) for c in cells]
        if not vals:
            continue
        # Eight columns: location, country, system, year, stations, lines, length, type.
        # A seven-column row inherits the country of the rowspan above it.
        if len(vals) >= 8:
            country_carry = vals[1][0]
            v = [x[0] for x in vals]
            out.append(dict(section=section, loc=v[0], country=v[1], system=v[2], year=v[3],
                            stations=v[4], lines=v[5], length=v[6], type=v[7]))
        elif len(vals) == 7:
            v = [x[0] for x in vals]
            out.append(dict(section=section, loc=v[0], country=country_carry, system=v[1], year=v[2],
                            stations=v[3], lines=v[4], length=v[5], type=v[6]))
        else:
            out.append(dict(section=section, raw=[x[0] for x in vals], country=country_carry))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wiki", default=os.path.join(DEFAULT_DIR, "List_of_tram_and_light_rail_transit_systems.wiki"))
    ap.add_argument("--out", default=os.path.join(DEFAULT_DIR, "tram_rows.json"))
    a = ap.parse_args()
    if not os.path.exists(a.wiki):
        raise SystemExit(f"No wikitext at {a.wiki}; save it first (docs/coverage_sweep/README.md).")
    out = parse(open(a.wiki, encoding="utf-8").read())
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    shaped = [r for r in out if "raw" not in r]
    print(f"{len(shaped)} rows shaped, {len(out) - len(shaped)} kept raw -> {a.out}")
    for (sec, n) in Counter(r["section"] for r in shaped).most_common():
        print(f"  {sec}: {n}")


if __name__ == "__main__":
    main()
