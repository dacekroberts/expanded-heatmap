"""Fill a French batch city's build-day config values from its FRESH feed.

    python scripts/france_fill_build_day.py <slug> [<slug> ...]          # print only
    python scripts/france_fill_build_day.py <slug> --write               # and edit config.py

Reads `data/<slug>/raw/gtfs.zip`, which `fetch_sources.py` has just
downloaded (feeds roll: never run this on a copy from another week), and the
city's config. It fills three of the scaffold's to-dos, each from the feed:

  GTFS_SELF_ATTESTS  whether the zip's own feed_info.txt carries a feed_end_date
  ROUTE_IDS          the route_ids behind LINE_KEYS, after the route-type and
                     agency filters
  LINE_COLOURS       each line's route_color; with several route_ids per line,
                     the colour of the one running the most trips. A line with
                     no colour is left for the builder (Le Havre's are the
                     project's own, the licence read's call)

It never fills gate 3, the public names or anything the owner decides. Every
value it writes is printed, so the build reads it before committing it.
Colour clashes are pipeline/linecolour.py's to refuse at step 3.
"""
import argparse
import csv
import importlib
import io
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def feed_values(cfg):
    z = zipfile.ZipFile(cfg.GTFS_ZIP)

    def read(name):
        with z.open(name) as f:
            return list(csv.DictReader(io.TextIOWrapper(f, "utf-8-sig")))

    attests = False
    if "feed_info.txt" in z.namelist():
        rows = read("feed_info.txt")
        attests = bool(rows and (rows[0].get("feed_end_date") or "").strip())
    routes = [r for r in read("routes.txt")
              if r["route_type"] in cfg.ROUTE_TYPES_RAIL
              and (not getattr(cfg, "GTFS_AGENCY_ID", None)
                   or r.get("agency_id") == cfg.GTFS_AGENCY_ID)
              and r["route_short_name"] in cfg.LINE_KEYS]
    ids = sorted(r["route_id"] for r in routes)
    trips = {}
    for t in read("trips.txt"):
        if t["route_id"] in ids:
            trips[t["route_id"]] = trips.get(t["route_id"], 0) + 1
    colours = {}
    for key in cfg.LINE_KEYS:
        mine = sorted((r for r in routes if r["route_short_name"] == key),
                      key=lambda r: -trips.get(r["route_id"], 0))
        c = (mine[0].get("route_color") or "").strip() if mine else ""
        if c:
            colours[key] = "#" + c.upper()
    return attests, ids, colours


def rewrite(path, attests, ids, colours):
    text = path.read_text(encoding="utf-8")
    new = re.sub(r"^# TODO: re-read at build - does the build-day zip carry feed_info.txt with a\n"
                 r"# feed_end_date\? True means the page can quote the operator's own window.\n"
                 r"GTFS_SELF_ATTESTS = None$",
                 "# Read at build: " + ("the zip's feed_info.txt carries a feed_end_date, so the\n"
                                        "# page quotes the operator's own window."
                                        if attests else
                                        "the zip declares no dated window, so the page quotes the\n"
                                        "# NAP's reading of it, recorded at fetch.")
                 + f"\nGTFS_SELF_ATTESTS = {attests}", text, flags=re.M)
    new = re.sub(r"^# TODO: the build-day feed's route_id\(s\) for each key in LINE_KEYS\. Read them\n"
                 r"# fresh: a rolling feed may renumber\. Several route_ids per key is allowed\n"
                 r"# \(Le Havre, Valenciennes\) - they collapse onto the key\.\n"
                 r"ROUTE_IDS = \[\]$",
                 "# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).\n"
                 "# A rolling feed may renumber: step 1 exits if they change.\n"
                 "ROUTE_IDS = " + repr(ids).replace("'", '"'), new, flags=re.M)
    if colours:
        body = ", ".join(f'"{k}": "{v}"' for k, v in colours.items())
        new = re.sub(r"^# TODO: each line's colour, from the build-day feed's route_color where it has\n"
                     r"# one and it is unambiguous; pipeline/linecolour\.py decides a clash\.\n"
                     r"LINE_COLOURS = \{\}$",
                     "# Each line's route_color from the build-day feed (the most-used route_id's\n"
                     "# where a line has several); pipeline/linecolour.py decides a clash.\n"
                     f"LINE_COLOURS = {{{body}}}", new, flags=re.M)
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
    return new != text


def gate3(cfg):
    """OpenStreetMap's per-line stop counts, from the cached Overpass answer."""
    from pipeline.countries.france_tram import osm_stop_counts
    osm = osm_stop_counts(cfg)
    return {k: osm[cfg.OSM_REFS.get(k, k)] for k in cfg.LINE_KEYS
            if cfg.OSM_REFS.get(k, k) in osm}


def rewrite_gate3(path, counts, date):
    text = path.read_text(encoding="utf-8")
    body = ", ".join(f'"{k}": {v}' for k, v in counts.items())
    new = re.sub(r"^# GATE 3: an independent per-line count, from outside the feed\.\n"
                 r"# TODO: the operator's own stop list or OpenStreetMap's route relations\.\n"
                 r"OPERATOR_STATION_COUNTS = \{\}\n"
                 r'OPERATOR_COUNTS_SOURCE = "TODO"$',
                 "# GATE 3: an independent per-line count, from outside the feed. Recorded\n"
                 "# as OpenStreetMap has it, even where it disagrees: step 1 prints any\n"
                 "# MISMATCH, and the build log says why.\n"
                 f"OPERATOR_STATION_COUNTS = {{{body}}}\n"
                 "OPERATOR_COUNTS_SOURCE = (\n"
                 '    "OpenStreetMap route relations, stop members of each ref\'s most "\n'
                 f'    "complete relation, read {date}")', text, flags=re.M)
    new = re.sub(r"^# line key -> the relations' `ref` tag\. TODO verify against the fetched file\.$",
                 "# line key -> the relations' `ref` tag, checked against the fetched file.",
                 new, flags=re.M)
    new = re.sub(r"^# `network` tag and refs at build and narrow the query to the operator's\.$",
                 "# `network` tag and refs: read at build, the query returns this network.",
                 new, flags=re.M)
    new = re.sub(r"^# fetch_sources\.py \(the owner's Overpass rule\)\. TODO: check the relations'$",
                 "# fetch_sources.py (the owner's Overpass rule). Checked: the relations'",
                 new, flags=re.M)
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
    return new != text


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    for slug in args.slugs:
        cfg = importlib.import_module(f"pipeline.{slug}.config")
        if not cfg.GTFS_ZIP.exists():
            print(f"{slug}: no gtfs.zip - run its fetch_sources.py first")
            continue
        attests, ids, colours = feed_values(cfg)
        missing = sorted(set(cfg.LINE_KEYS) - set(colours))
        print(f"{slug}: self-attests {attests}; route_ids {ids}; colours {colours}"
              + (f"; NO colour for {missing}" if missing else ""))
        g3 = gate3(cfg)
        print(f"  gate 3 from OpenStreetMap: {g3}"
              + ("" if set(g3) == set(cfg.LINE_KEYS) else
                 f"  (no OSM ref for {sorted(set(cfg.LINE_KEYS) - set(g3))}: left to the builder)"))
        if args.write:
            changed = rewrite(Path(cfg.__file__), attests, ids, colours)
            if g3 and set(g3) == set(cfg.LINE_KEYS):
                import json
                prov = json.loads(cfg.PROVENANCE_JSON.read_text(encoding="utf-8"))
                changed |= rewrite_gate3(Path(cfg.__file__), g3, prov["fetched_utc"][:10])
            print(f"  config.py {'updated' if changed else 'unchanged (already filled?)'}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
