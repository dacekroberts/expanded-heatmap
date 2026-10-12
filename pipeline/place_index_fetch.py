"""Download a city's PLACES from OpenStreetMap for the place search. NOT a
step: drift_check.py never runs this file, and the index step exits naming it
when its cache is missing.

    python pipeline/place_index_fetch.py <city> [--force] [--wait MINUTES]
    python pipeline/place_index_fetch.py --selftest      # the lock's cases

One run of this script at a time on this machine (FetchLock, below).

Two Overpass queries per city, one after the other (the owner's rule: one in
flight per session, none in parallel, 60 s after a 504 or 429, all in
pipeline/osm.py), cut by the city's own boundary (config.PLACE_AREA): QUERY,
cached at config.PLACE_OSM_JSON, and EXTRA_QUERY, at
config.PLACE_OSM_EXTRA_JSON; each recorded in outputs/<slug>/provenance.json
("osm_places", "osm_places_extra"; a cache already on disk is recorded
without a query). Together:

  * every named highway way, with its node ids, and those nodes' positions
    (streets, and the intersections derived from shared nodes);
  * named junction nodes (Japan signs its intersections: 四条烏丸);
  * places, as nodes or areas (wards, districts, neighborhoods, the 町 of
    Kyoto; Sydney's Darling Harbour is an area);
  * stations and tram stops;
  * landmarks: attractions, museums, viewpoints, artworks, historic sites,
    places of worship, parks, gardens and stadiums, universities, town halls,
    libraries, theaters and arts centres, airports, peaks, beaches, bays,
    rivers, named markets (kept only when notable, owner 2026-10-07). The
    sample cities found Wrigley Field, Cloud Gate and the airports missing
    (2026-10-08).

Places only, never business records (owner, 2026-10-07): nothing here is
queried by shop, office, craft or a commercial amenity, and the index step
drops any landmark that carries one of those tags.

ODbL 1.0: the index built from this is a Derivative Database (OSMF's
Substantial guideline), published under ODbL with the credit every map already
shows; docs/data_sources.md has the row.
"""
import argparse
import datetime
import hashlib
import importlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline import osm, place_index  # noqa: E402

QUERY = """[out:json][timeout:170];
area{area}->.a;
way["highway"]["name"](area.a)->.w;
.w out body qt;
node(w.w);
out skel qt;
(
  node["place"]["name"](area.a);
  node["name"]["highway"="traffic_signals"](area.a);
  node["name"]["junction"](area.a);
  nwr["railway"~"^(station|halt|tram_stop)$"]["name"](area.a);
  nwr["public_transport"="station"]["name"](area.a);
  nwr["tourism"~"^(attraction|museum|viewpoint|gallery|zoo|aquarium|theme_park)$"]["name"](area.a);
  nwr["historic"]["name"](area.a);
  nwr["amenity"="place_of_worship"]["name"](area.a);
  nwr["leisure"~"^(park|garden)$"]["name"](area.a);
  nwr["amenity"~"^(university|college)$"]["name"](area.a);
  nwr["amenity"="marketplace"]["name"](area.a);
  node["natural"="peak"]["name"](area.a);
  way["waterway"="river"]["name"](area.a);
);
out tags center qt;
"""
# The classes the sample cities found missing (2026-10-08: Chicago's Wrigley
# Field and Cloud Gate, Sydney's Darling Harbour, every airport), in a query
# of their own: added to QUERY they timed it out at 174 s on Chicago and
# Vancouver. Places as areas (QUERY has the nodes), stadiums, artworks,
# civic buildings, airports, beaches and bays.
EXTRA_QUERY = """[out:json][timeout:170];
area{area}->.a;
(
  way["place"]["name"](area.a);
  rel["place"]["name"](area.a);
  nwr["tourism"="artwork"]["name"](area.a);
  nwr["leisure"="stadium"]["name"](area.a);
  nwr["amenity"~"^(townhall|library|theatre|arts_centre)$"]["name"](area.a);
  nwr["aeroway"="aerodrome"]["name"](area.a);
  nwr["natural"~"^(beach|bay)$"]["name"](area.a);
);
out tags center qt;
"""


def record(config, path, key, how):
    """Record one cache in outputs/<slug>/provenance.json under `key`
    ("osm_places", "osm_places_extra"), in the shape the city's other OSM
    downloads use (japan_fetch.record): the file, its bytes and sha256, the
    element count, the host, OSM's own timestamp (osm_base), the exact query
    and when it was written. A cache already on disk is recorded as kept,
    dated by its modification time."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    prov_path = getattr(config, "PROVENANCE_JSON", None) or (
        Path(__file__).parent.parent / "outputs" / place_index.city_of(config)[0] / "provenance.json")
    prov = json.loads(prov_path.read_text(encoding="utf-8")) if prov_path.exists() else {}
    data = path.read_bytes()
    prov[key] = {
        "bytes": len(data),
        "elements": len(payload.get("elements") or []),
        "file": path.name,
        "host": payload.get("_fetched_from"),
        "how": how,
        "osm_base": payload.get("osm3s", {}).get("timestamp_osm_base"),
        "query": payload.get("_query"),
        "retrieved": datetime.datetime.fromtimestamp(
            path.stat().st_mtime, datetime.timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    prov_path.parent.mkdir(parents=True, exist_ok=True)
    # Bytes, so the committed file stays LF on Windows.
    prov_path.write_bytes((json.dumps(prov, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
    return prov_path


def tiles(split):
    """The bbox filters, "(s,w,n,e)", of a config.PLACE_SPLIT: its bbox cut
    into rows x cols equal tiles, south-west first."""
    s, w, n, e = split["bbox"]
    rows, cols = split["rows"], split["cols"]
    dlat, dlon = (n - s) / rows, (e - w) / cols
    return [f"({s + r * dlat:.5f},{w + c * dlon:.5f},{s + (r + 1) * dlat:.5f},{w + (c + 1) * dlon:.5f})"
            for r in range(rows) for c in range(cols)]


def fetch_split(config, path, force):
    """QUERY for a city too large for one answer (batch 3, 2026-10-11: London
    and the other size tests), asked once per tile of config.PLACE_SPLIT, one
    after the other, each tile still cut by the city's own area, then merged
    by OSM id into the one cache the index step reads. A way crossing a tile
    edge comes whole, with all its nodes, in both tiles. Each tile's answer
    stays beside the cache (<name>.tile<N>.json), so a refused tile is the
    only one asked again. The merged cache records every tile's query and
    host, and the OLDEST osm_base among them."""
    if path.exists() and not force:
        return osm.fetch("", path)
    merged, seen, hosts, queries, bases = [], set(), [], [], []
    for i, tile in enumerate(tiles(config.PLACE_SPLIT)):
        query = QUERY.format(area=config.PLACE_AREA).replace("(area.a)", "(area.a)" + tile)
        part = path.with_name(f"{path.stem}.tile{i}.json")
        try:
            els, host = osm.fetch(query, part, force=force, timeout=180, deadline=900)
        except RuntimeError as exc:
            # A tile with nothing in it (a corner of the bbox outside the
            # area) answers empty on every host, which osm.fetch does not
            # trust; a tile any host refused is a failure, never empty.
            if "empty 200" in str(exc) and "Error" not in str(exc).split(" - ", 1)[-1] \
                    and "remark" not in str(exc):
                print(f"tile {i} {tile}: empty on every host, taken as empty")
                continue
            raise
        print(f"tile {i} {tile}: {len(els):,} elements from {host}")
        payload = json.loads(part.read_text(encoding="utf-8"))
        hosts.append(host)
        queries.append(query)
        bases.append(payload.get("osm3s", {}).get("timestamp_osm_base"))
        for e in els:
            if (e["type"], e["id"]) not in seen:
                seen.add((e["type"], e["id"]))
                merged.append(e)
    out = {"osm3s": {"timestamp_osm_base": min(b for b in bases if b)}, "elements": merged,
           "_fetched_from": ", ".join(dict.fromkeys(hosts)), "_query": "\n".join(queries)}
    path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return merged, out["_fetched_from"]

# ONE PLACE FETCH ON THIS MACHINE AT A TIME (owner, 2026-10-12). The Overpass
# rule is one query in flight; pipeline/osm.py holds it inside one process,
# and nothing held it between processes. The rollout runs an unattended queue
# and may be driven by an outside model, which a session hook does not see,
# so the rule is a lock file here: data/_place_fetch.lock, in the data folder
# every worktree shares. It names its holder (pid, city, since). A holder
# whose process is gone is replaced; a live one makes this script exit
# non-zero naming it, or wait with --wait MINUTES. PLACE_FETCH_LOCK_DIR moves
# the file (the selftest's).
LOCK_NAME = "_place_fetch.lock"
LOCK_POLL_S = 5


def lock_path():
    return Path(os.environ.get("PLACE_FETCH_LOCK_DIR", Path(__file__).parent.parent / "data")) / LOCK_NAME


def _pid_alive(pid):
    import psutil
    return psutil.pid_exists(pid)


class FetchLock:
    """Held for a whole run of this script. alive and sleep are injected by
    the selftest."""

    def __init__(self, city, wait_min=0, path=None, alive=_pid_alive, sleep=time.sleep):
        self.city, self.wait_s = city, wait_min * 60
        self.path = Path(path) if path else lock_path()
        self.alive, self.sleep = alive, sleep

    def holder(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, ValueError):
            return None

    def __enter__(self):
        waited = 0
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                held = self.holder()
                # An unreadable file is a writer caught between create and
                # write, or a crash there: given one poll, then replaced.
                if held is None and waited == 0 and self.wait_s == 0:
                    self.sleep(1)
                    held = self.holder()
                if held is None or not self.alive(held.get("pid", -1)):
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                if waited >= self.wait_s:
                    raise SystemExit(
                        f"Another place fetch is running: {held.get('city')} (pid {held.get('pid')}, "
                        f"since {held.get('since')}). One Overpass query at a time on this machine: "
                        f"wait for it, or pass --wait MINUTES.")
                self.sleep(LOCK_POLL_S)
                waited += LOCK_POLL_S
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump({"pid": os.getpid(), "city": self.city,
                           "since": datetime.datetime.now().isoformat(timespec="seconds")}, f)
            return self

    def __exit__(self, *exc):
        held = self.holder()
        if held and held.get("pid") == os.getpid():
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


def selftest():
    import tempfile
    cases = []
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / LOCK_NAME
        with FetchLock("a", path=path):
            cases.append(("a free lock is taken and names its holder",
                          (FetchLock("a", path=path).holder() or {}).get("city") == "a"))
            try:
                FetchLock("b", path=path, alive=lambda pid: True, sleep=lambda s: None).__enter__()
                refused = False
            except SystemExit as exc:
                refused = "a (pid" in str(exc)
            cases.append(("a second fetch is refused while the first runs, naming it", refused))
            slept = []
            try:
                FetchLock("b", wait_min=1, path=path, alive=lambda pid: True, sleep=slept.append).__enter__()
                waited = False
            except SystemExit:
                waited = sum(slept) >= 60
            cases.append(("--wait polls for its minutes before refusing", waited))
        cases.append(("the lock is released on exit", not path.exists()))
        path.write_text(json.dumps({"pid": 1, "city": "gone", "since": "x"}), encoding="utf-8")
        with FetchLock("c", path=path, alive=lambda pid: False):
            took = (FetchLock("c", path=path).holder() or {}).get("city") == "c"
        cases.append(("a holder whose process is gone is replaced", took))
        path.write_text("", encoding="utf-8")
        with FetchLock("d", path=path, sleep=lambda s: None):
            took = (FetchLock("d", path=path).holder() or {}).get("city") == "d"
        cases.append(("an unreadable lock file is replaced", took))
        other = Path(d) / "other.lock"
        other.write_text(json.dumps({"pid": -5, "city": "x", "since": "x"}), encoding="utf-8")
        FetchLock("e", path=other).__exit__()
        cases.append(("exit never removes another holder's lock", other.exists()))
    for label, ok in cases:
        print(f"  {'ok ' if ok else 'BAD'} {label}")
    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("city")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--wait", type=int, default=0, metavar="MINUTES",
                    help="wait this long for another place fetch to finish, then exit non-zero")
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    with FetchLock(args.city, args.wait):
        fetch_city(config, args.force)


def fetch_city(config, force):
    args = argparse.Namespace(force=force)
    # One after the other, never in parallel (the owner's Overpass rule).
    for query, path, key in ((QUERY, config.PLACE_OSM_JSON, "osm_places"),
                             (EXTRA_QUERY, config.PLACE_OSM_EXTRA_JSON, "osm_places_extra")):
        kept = path.exists() and not args.force
        if query is QUERY and getattr(config, "PLACE_SPLIT", None):
            els, host = fetch_split(config, path, args.force)
        else:
            els, host = osm.fetch(query.format(area=config.PLACE_AREA), path, force=args.force,
                                  timeout=180, deadline=900)
        kinds = {}
        for e in els:
            kinds[e["type"]] = kinds.get(e["type"], 0) + 1
        print(f"{path.name}: {len(els):,} elements from {host} {kinds}")
        prov = record(config, path, key, "kept (on disk from an earlier run)" if kept else "fetched")
        print(f"recorded in {prov.relative_to(Path(__file__).parent.parent)} as {key}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(selftest() if "--selftest" in sys.argv else main())
