"""Re-match the coverage sweep's rail-city universe against the master list.

The sweep of 2026-10-03 classified every city with a metro, light rail or
tram (`docs/coverage_sweep/`); the remainder count of 2026-10-04 came from
this re-match. It answers one question: which universe cities does
`docs/city_master_list.md` not name at all? A name on the list is not proof
of a verdict, and spellings vary (Hanover and Hannover), so every figure is
coarse (about 10% either way); the far-future re-probe in
`docs/recheck_calendar.md` ("The screen itself") starts here.

Usage:
    python scripts/coverage_sweep/recount.py [--gaps-only]

By default every universe row that is in mode and not out by policy is
checked; `--gaps-only` checks only the rows the sweep found with no verdict.
Japan is checked from the romaji groups of the sweep's Japan section, since
the scoping CSV (`japan_universe_mhlw.csv`) names municipalities in kanji.
Reads files only; never fetches.
"""
import argparse
import collections
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "docs")
SWEEP = os.path.join(DOCS, "coverage_sweep")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from universe_europe import U as U_EUROPE  # noqa: E402
from universe_france import U_FR  # noqa: E402

# The sweep's Japan section, groups B to D, in romaji without macrons.
JAPAN = {
    "wave-2 remainder": "Maebashi, Takasaki, Shizuoka, Fukuyama, Funabashi, Matsudo, Ichikawa, Kanazawa, Kurashiki, Sagamihara, Naha, Hachioji, Saitama, Niigata, Tottori, Yamagata, Morioka, Yao, Kure, Mito, Takatsuki, Kofu, Chigasaki, Matsumoto, Miyazaki",
    "neighbour mentions": "Suita, Toyonaka, Moriguchi, Kadoma, Settsu, Amagasaki, Akashi, Fujisawa, Chofu, Nishitokyo, Machida, Uji, Okazaki, Nisshin, Ino, Nankoku, Imizu, Ichihara, Nagakute, Tokushima",
    "mode cities": "Tachikawa, Hino, Tama, Higashimurayama, Higashiyamato, Kawaguchi, Kamakura, Urayasu, Ibaraki, Minoh, Urasoe, Sakura, Ina, Wako, Toyokawa, Tokorozawa, Ageo",
    "JR and private rail, core or 200k+": "Gifu, Hirakata, Kashiwa, Kawagoe, Koshigaya, Asahikawa, Iwaki, Koriyama, Akita, Aomori, Fukushima, Oita, Matsue, Hachinohe, Nagaoka, Ichinomiya, Kasugai, Kakogawa, Takarazuka, Neyagawa, Tsu, Fuji, Ota, Yamato, Kasukabe, Yachiyo, Itami, Isesaki, Saga, Soka, Tsukuba, Atsugi, Hiratsuka, Fuchu",
}


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def key(name):
    """The first plain name of a row: bold, parentheticals and groupings dropped."""
    n = re.sub(r"\*", "", name)
    return re.split(r" \(|/| - |,", n)[0].strip()


def on_list(text, names):
    for n in names:
        k = fold(key(n))
        if len(k) >= 3 and re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", text):
            return True
    return False


def kind(status):
    s = status.upper()
    if s.startswith("OUT"):
        return "out"
    if "RULED OUT" in s:
        return "policy"
    if any(w in s for w in ("NEVER", "SIBLING", "COUNTRY-ONLY", "COUNTRY OR SIBLING", "NOTED")):
        return "gap"
    return "verdict"


def md_rows(path, region):
    """Rows of every table in a sweep report whose header has City and Status."""
    rows, hdr = [], None
    for ln in open(path, encoding="utf-8").read().splitlines():
        if not ln.startswith("|"):
            hdr = None
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if hdr is None:
            hdr = cells
            continue
        if set(ln) <= set("|-: "):
            continue
        if "Status" in hdr and "City" in hdr[0] and len(cells) > hdr.index("Status"):
            rows.append((region, cells[0], [cells[0]], cells[hdr.index("Status")]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gaps-only", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    ml = fold(open(os.path.join(DOCS, "city_master_list.md"), encoding="utf-8").read())

    aliases = {r[0]: r[3] for r in U_EUROPE + U_FR}
    rows = [("Europe", r["city"], [r["city"]] + aliases.get(r["city"], []), r["status"])
            for r in json.load(open(os.path.join(SWEEP, "europe_classified.json"), encoding="utf-8"))]
    rows += md_rows(os.path.join(SWEEP, "americas_oceania.md"), "Americas and Oceania")
    rows += md_rows(os.path.join(SWEEP, "asia_mideast_africa.md"), "Asia, Middle East, Africa")

    tally = collections.defaultdict(collections.Counter)
    absent = collections.defaultdict(list)
    for region, city, names, status in rows:
        k = kind(status)
        if k in ("out", "policy") or (a.gaps_only and k != "gap"):
            tally[region][k] += 1
            continue
        if on_list(ml, names):
            tally[region]["named on the list"] += 1
        else:
            tally[region]["absent"] += 1
            absent[region].append(re.sub(r"\*", "", city)[:40])

    for group, names in JAPAN.items():
        for n in (x.strip() for x in names.split(",")):
            if on_list(ml, [n]):
                tally["Japan"]["named on the list"] += 1
            else:
                tally["Japan"]["absent"] += 1
                absent["Japan"].append(n)

    for region, c in tally.items():
        print(f"{region}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
    for region, names in absent.items():
        print(f"\nAbsent from the master list, {region} ({len(names)}):")
        print("; ".join(names))


if __name__ == "__main__":
    main()
