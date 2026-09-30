"""Write the France tram batch's section of docs/excluded_categories.md: one
section, a row per built city, after Rennes's. Rennes's section is the model
for the prose; the figures are each city's own (sirene_facts.json, the step 2
catch-all share passed in, excluded_stations.csv).

    python scripts/france_excluded_section.py le_mans=13.0 reims=11.9 ... [--write]

Each argument is <slug>=<96.09Z share in %> as step 2 printed it. Re-run with
every built city each time a landing group is added; the section is replaced
whole.
"""
import argparse
import csv
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
DOC = ROOT / "docs" / "excluded_categories.md"
HEAD = "### The French tram cities - Paris's register and rules, city by city"
INTRO = f"""{HEAD}

**Everything excluded in Paris is excluded in each of these cities, for the
same reasons** - the four no-premises trades, the wholesale laundry, funeral
services, and the two catch-alls `96.09Z` and `56.29B`. They were measured
again for each city rather than inherited: the `96.09Z` share below is the one
each city's own build printed, against 9.6-14.0% in Paris, Marseille,
Toulouse, Lille and Rennes.

**Stops beyond a commune boundary are excluded for being in another commune.**
Each line is drawn to its ends, but no ring is drawn around those stops, and
their businesses are not counted. They are listed, with the commune each lies
in, at `outputs/<city>/excluded_stations.csv`. Those communes' businesses are in
the same national register, so this is a scoping choice rather than a data
limit. A city marked "(Regional)" is scoped to every commune its lines serve,
so it leaves no stop out.

**The share withheld by INSEE is withheld by INSEE, not by this project**, with
the name, the address and the coordinates removed together, so those rows
cannot reach the map.

| City | `96.09Z` excluded | Withheld by INSEE | Stops left out, by commune |
|---|---|---|---|
"""


def row(slug, share):
    import scaffold_france_batch as sfb
    cfg = importlib.import_module(f"pipeline.{slug}.config")
    facts = json.loads((cfg.OUTPUTS / "sirene_facts.json").read_text(encoding="utf-8"))
    withheld = facts["masked"] / facts["active"] * 100
    if cfg.SCOPE == "regional":
        left = "none (regional scope)"
    elif cfg.EXCLUDED_STATIONS_CSV.exists():
        by = {}
        for r in csv.DictReader(open(cfg.EXCLUDED_STATIONS_CSV, encoding="utf-8")):
            place = re.sub(r"^in (.*?)(?: \(\d+\))?, outside commune \d+$", r"\1", r["reason"])
            by.setdefault(place, 0)
            by[place] += 1
        left = "; ".join(f"{n} in {p}" for p, n in by.items()) or "none"
    else:
        left = "none"
    return f"| {sfb.BATCH[slug]['name']} | {share}% | {withheld:.1f}% | {left} |"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pairs", nargs="+")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    body = INTRO + "\n".join(row(*p.split("=")) for p in args.pairs) + "\n\n"
    if not args.write:
        print(body)
        return
    doc = DOC.read_text(encoding="utf-8")
    if HEAD in doc:
        start = doc.index(HEAD)
        nxt = re.search(r"^#{2,3} ", doc[start + len(HEAD):], re.M)
        end = start + len(HEAD) + nxt.start()
        doc = doc[:start] + body + doc[end:]
    else:
        anchor = doc.index("### Rennes - ")
        nxt = re.search(r"^#{2,3} ", doc[anchor + 5:], re.M)
        at = anchor + 5 + nxt.start()
        doc = doc[:at] + body + doc[at:]
    DOC.write_text(doc, encoding="utf-8", newline="\n")
    print(f"wrote the section ({len(args.pairs)} cities)")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
