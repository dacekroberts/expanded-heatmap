"""Download Aarhus's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/aarhus/fetch_sources.py

EVERYTHING HERE IS KEYLESS OPENSTREETMAP. Three Overpass answers, each cached
once and re-read thereafter:

  * the Letbane's route relations, with geometry and their stop nodes;
  * the kommune boundaries around them (admin_level 7), so step 1 can name the
    kommune of every station it drops;
  * the address points inside Aarhus Kommune that carry `osak:identifier` -
    the DAR Husnummer id - as CSV, which keeps ~114,000 points to a few MB.

**CVR AND DAR ARE NOT FETCHED.** They are the national caches Copenhagen took
through the owner's Datafordeler key (CVR generation 505, DAR generation 761),
shared by both cities; a refresh here would change Copenhagen's inputs. This
script only RECORDS which generations it found, in provenance.

**REJSEPLANEN IS NEVER FETCHED** (owner, 2026-09-29): its Labs guidelines ask
that the data not be changed and describe access as by request. The page's
frequency statement rests on Midttrafik's own published timetables.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.aarhus import config  # noqa: E402
from pipeline.countries import denmark as DK  # noqa: E402

# The whole Letbane, Odder to Grenaa, so step 1 can name the kommune of every
# station outside Aarhus Kommune.
RAIL_BBOX = (55.90, 9.90, 56.50, 10.95)          # south, west, north, east


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_rail_and_kommuner():
    s, w, n, e = RAIL_BBOX
    # `out geom` on the relations: step 1 needs the member lists and
    # map_common.load_osm_line_shapes the way geometry. Only light_rail: the
    # Letbane is the only rail this city draws.
    rail = ("[out:json][timeout:240];"
            '(relation["type"="route"]["route"="light_rail"]'
            f"({s},{w},{n},{e}););"
            "out geom;node(r);out tags center;")
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no light_rail relations came back - a FAILED fetch, not a negative")
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    print(f"  rail: {len(rels)} relations via {host}")

    kom = ('[out:json][timeout:240];'
           f'relation["boundary"="administrative"]["admin_level"="{DK.OSM_KOMMUNE_LEVEL}"]'
           f"({s},{w},{n},{e});out geom;")
    els, host2 = osm.fetch(kom, config.OSM_KOMMUNER_JSON)
    refs = {x.get("tags", {}).get("ref") for x in els}
    missing = set(config.KOMMUNER) - refs
    if missing:
        sys.exit(f"  kommune boundaries missing refs {sorted(missing)}")
    print(f"  kommuner: {len(els)} boundary relations via {host2}")
    return host, host2


def fetch_address_points():
    """Overpass CSV, tab-separated with a header: @id, @lat, @lon,
    osak:identifier. Cached; an answer with no data rows is refused, never
    written - an empty result is a failed fetch."""
    dest = config.OSM_ADDRESS_POINTS_TSV
    if dest.exists():
        print(f"  address points: cached ({dest.stat().st_size:,} bytes)")
        return "cache"
    area = 3600000000 + config.OSM_KOMMUNE_RELATION
    q = ('[out:csv(::id,::lat,::lon,"osak:identifier")][timeout:240];'
         f'area({area})->.m;nwr["osak:identifier"](area.m);out center;')
    problems = []
    for attempt in range(3):
        for host in osm.OVERPASS_HOSTS:
            name = host.split("/")[2]
            try:
                r = requests.post(host, data={"data": q}, timeout=300,
                                  headers={"User-Agent": osm.OVERPASS_USER_AGENT})
            except requests.RequestException as exc:
                problems.append(f"{name}: {type(exc).__name__}")
                continue
            if r.status_code != 200:
                problems.append(f"{name}: HTTP {r.status_code}")
                continue
            text = r.content.decode("utf-8")
            rows = text.count("\n") - 1
            if rows < 1000:
                problems.append(f"{name}: {rows} rows - not trusted")
                continue
            dest.write_bytes(r.content)   # as served: no CRLF translation
            print(f"  address points: {rows:,} rows via {name}")
            return name
        # At least the owner's 60 s after a 504 or 429 (CLAUDE.md, 2026-09-30).
        time.sleep(osm.OVERLOAD_WAIT_S * (attempt + 1))
    sys.exit("  every Overpass mirror failed for the address points: "
             + "; ".join(problems))


def registers_found():
    """The cached CVR and DAR generations - read, never refreshed."""
    if not DK.MANIFEST_JSON.exists():
        sys.exit(f"  no national CVR/DAR cache at {DK.SHARED_RAW}; it is Copenhagen's, "
                 f"fetched with the owner's key - ask before fetching it")
    man = json.loads(DK.MANIFEST_JSON.read_text(encoding="utf-8"))["files"]
    keep = {p: {k: v[k] for k in ("register", "entity", "filename", "generation", "generation_time",
                                  "fetched_utc", "csv_sha256") if k in v}
            for p, v in man.items() if not p.startswith("dar/Adressepunkt_")}
    gens = {(v["register"], v["generation"]) for v in keep.values()}
    print("  national caches: " + ", ".join(f"{r} generation {g}" for r, g in sorted(gens)))
    return keep


if __name__ == "__main__":
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("OpenStreetMap (keyless):")
    rail_host, kom_host = fetch_rail_and_kommuner()
    pts_host = fetch_address_points()
    print("\nCVR and DAR (cached nationally, not fetched):")
    regs = registers_found()

    def stamp(path):
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
            timespec="seconds")

    prov = {"written_utc": _now(), "osm_bbox": RAIL_BBOX,
            "osm": {"rail": {"host": rail_host, "file_utc": stamp(config.OSM_ROUTES_JSON)},
                    "kommuner": {"host": kom_host, "file_utc": stamp(config.OSM_KOMMUNER_JSON)},
                    "address_points": {"host": pts_host,
                                       "file_utc": stamp(config.OSM_ADDRESS_POINTS_TSV)}},
            "datafordeler": regs}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these "
          f"files and never fetch.")
