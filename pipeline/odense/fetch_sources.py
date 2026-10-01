"""Download Odense's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/odense/fetch_sources.py

EVERYTHING HERE IS KEYLESS OPENSTREETMAP, as Aarhus's. Three Overpass answers,
each cached once and re-read thereafter:

  * the Letbane's `route=tram` relations with geometry, their stop nodes, and
    every `railway=tram_stop` node in the box - the last so step 1 can add SDU
    Syd/Hospital Nord, a tagged stop on no route relation (config.STATION_ADD);
  * the kommune boundaries around them (admin_level 7);
  * the address points inside Odense Kommune that carry `osak:identifier` -
    the DAR Husnummer id - as CSV.

**CVR IS NOT FETCHED.** It is the national cache Copenhagen took through the
owner's Datafordeler key, shared by every Danish city; a refresh here would
change Copenhagen's and Aarhus's inputs. This script only RECORDS which
generations it found, in provenance.

**REJSEPLANEN IS NEVER FETCHED** (owner, 2026-09-29): its Labs guidelines ask
that the data not be changed and describe access as by request.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.countries import denmark as DK  # noqa: E402
from pipeline.odense import config  # noqa: E402

# Odense Letbane end to end (Tarup Center - Hjallese Station), with margin.
RAIL_BBOX = (55.33, 10.28, 55.46, 10.47)          # south, west, north, east


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_rail_and_kommuner():
    s, w, n, e = RAIL_BBOX
    # `out geom` on the relations: step 1 needs the member lists and
    # map_common.load_osm_line_shapes the way geometry. The stop nodes of the
    # relations AND every tram_stop in the box, `out body` (tags and lat/lon).
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no tram relations came back - a FAILED fetch, not a negative")
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    missing = [i for i in config.STATION_ADD if not any(
        x["type"] == "node" and x["id"] == i for x in els)]
    if missing:
        sys.exit(f"  STATION_ADD node(s) {missing} did not come back")
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
    osak:identifier. Cached; an answer with fewer than 1,000 data rows is
    refused, never written - an empty result is a failed fetch. A 504 or 429
    waits at least 60 s before the next try (the owner's Overpass rule,
    2026-09-30)."""
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
                if r.status_code in (429, 504):
                    time.sleep(60)
                continue
            text = r.content.decode("utf-8")
            rows = text.count("\n") - 1
            if rows < 1000:
                problems.append(f"{name}: {rows} rows - not trusted")
                continue
            dest.write_bytes(r.content)   # as served: no CRLF translation
            print(f"  address points: {rows:,} rows via {name}")
            return name
        time.sleep(60 * (attempt + 1))
    sys.exit("  every Overpass mirror failed for the address points: "
             + "; ".join(problems))


def registers_found():
    """The cached CVR generations - read, never refreshed."""
    if not DK.MANIFEST_JSON.exists():
        sys.exit(f"  no national CVR cache at {DK.SHARED_RAW}; it is Copenhagen's, "
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
    print("\nCVR (cached nationally, not fetched):")
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
