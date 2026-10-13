"""Answer an Overpass area query from a regional OpenStreetMap extract
(.osm.pbf) read on this machine. The GENERAL half: nothing here knows what a
caller asks for, and nothing runs on import.

    python pipeline/osm_extract.py --selftest
    python pipeline/osm_extract.py index                       # index-v1.json, once
    python pipeline/osm_extract.py region LAT LON [LAT LON ..]  # smallest region holding the points
    python pipeline/osm_extract.py download REGION_ID [--dated YYMMDD] [--max-mb N]

What it holds, in the order a caller uses it:

  * WHICH EXTRACT: smallest_region() picks the smallest Geofabrik region that
    covers a geometry, from the server's index-v1.json (cached on disk).
  * SEVERAL REGIONS AS ONE (owner, 2026-10-13): when the geometry crosses a
    region border and the one region covering it is over a size cap,
    choose_regions() picks the smallest set of regions, by bytes, that
    together cover it, download_set() holds or downloads them as one dated
    run, and query() and boundaries_holding() take a list of files. Every
    id is taken once (_Once has the rule for two copies), and a set whose
    files do not state one data timestamp is refused (SET_MAX_SPREAD_S).
  * THE DOWNLOAD: fetch() is the only function that opens a connection, one
    request per call, to DOWNLOAD_HOST only, never following a redirect by
    itself. download_extract() is the conduct around it (the publisher's
    "Download responsibly!" requests, 2026-10-13 read): a dated file already
    held is never asked for again, a file once downloaded and since removed is
    refused by the ledger, the `-latest` name is resolved to its dated file
    with a HEAD first, and a held extract young enough is used with no
    request at all.
  * THE AREA: Area holds one polygon per boundary, holes cut out, and applies
    the five rules below.
  * THE CLAUSES: parse_union() reads the statements of an Overpass union
    (`nwr["k"~"v"]["name"](area.a);`) into Clause objects, one per line, and
    raises on a statement it cannot represent.
  * THE READ: query() makes three passes over the extract and returns the
    boundaries, the Area and every matching element per union, in a
    DETERMINISTIC order: nodes, ways, relations, each by ascending id.
    Overpass's own `qt` order is not reproduced.

THE FIVE RULES THAT MAKE THE ANSWER EQUAL OVERPASS'S, each learned from a
measured difference against an Overpass answer of the same day (Tbilisi and
Seattle, 2026-10-13; the osm-extract skill has the measurements):

  1. Each boundary is tested on its own, never the union of them. A way
     lying on the border two included municipalities share is inside neither
     area (60 of Seattle's street ways).
  2. Inner rings are holes: an enclave is not in the area.
  3. A way is in when one of its nodes is strictly inside a boundary, or its
     line passes through a boundary's interior. Touching the boundary line,
     at a point or along it, is not enough.
  4. A relation is in when one of its member nodes or member ways is in by
     rule 3. Member relations are not followed.
  5. `out center` is the middle of the bounding box of the element's nodes,
     not a centroid, rounded to 7 decimals.

LIFTING THIS FILE INTO ANOTHER PROJECT: it needs osmium (pyosmium 4), shapely
2 and numpy. The one project-specific line is _refuse_if_offline(), which
defers to pipeline/offline.py when that module exists and is a no-op without
it.

ODbL 1.0: an extract is OpenStreetMap data, credited to OpenStreetMap
contributors. No credit to the extract's publisher is required
(docs/data_sources.md has the row and the conduct rules).
"""
import datetime
import hashlib
import json
import re
from pathlib import Path

DOWNLOAD_HOST = "download.geofabrik.de"
INDEX_URL = f"https://{DOWNLOAD_HOST}/index-v1.json"
# Names no person and no address: a download server needs to know what kind
# of client this is, nothing about who runs it.
USER_AGENT = "osm-extract-filter/1 (reads one regional extract per city; no file requested twice)"
LEDGER_NAME = "downloads.json"
DATED = re.compile(r"^(?P<region>.+)-(?P<date>\d{6})\.osm\.pbf$")
# Overpass area ids: 3600000000 + a relation's id, 2400000000 + a way's.
AREA_RELATION_BASE = 3600000000
AREA_WAY_BASE = 2400000000


# ---------------------------------------------------------------- the download

def _refuse_if_offline(what, hint=""):
    """pipeline/offline.py's switch when this file sits in the project it was
    written for; nothing when it has been lifted elsewhere."""
    try:
        from pipeline.offline import refuse_if_offline
    except ImportError:
        try:
            from offline import refuse_if_offline
        except ImportError:
            return
    refuse_if_offline(what, hint)


def check_url(url):
    """Exit unless `url` is https on DOWNLOAD_HOST. The server with user
    metadata (osm-internal) needs an OSM login and is never asked."""
    from urllib.parse import urlsplit
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.hostname != DOWNLOAD_HOST:
        raise SystemExit(f"Refused {url}: only https://{DOWNLOAD_HOST}/ is requested, never another "
                         f"host and never osm-internal.")
    return url


def fetch(url, dest=None, *, method="GET", transport=None, max_bytes=None):
    """ONE request to DOWNLOAD_HOST: the only place this module opens a
    connection. A redirect is returned, never followed. Returns (status,
    headers with lower-case names, bytes written).

    With `dest` the body is streamed to dest + ".part" and renamed once the
    byte count matches Content-Length; a .part left by an interrupted run is
    continued with a Range request, so no byte is asked for twice. A body
    larger than `max_bytes` is refused before it is read.

    `transport(method, url, headers)` -> (status, headers, readable or None)
    replaces the network (the selftest's)."""
    check_url(url)
    _refuse_if_offline(url, "Run the download by hand, outside a drift check.")
    headers = {"User-Agent": USER_AGENT}
    part = Path(str(dest) + ".part") if dest else None
    have = part.stat().st_size if part is not None and part.exists() else 0
    if have:
        headers["Range"] = f"bytes={have}-"
    if transport is None:
        import urllib.error
        import urllib.request

        class _NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None

        def transport(method, url, headers):
            opener = urllib.request.build_opener(_NoRedirect)
            try:
                resp = opener.open(urllib.request.Request(url, headers=headers, method=method), timeout=120)
            except urllib.error.HTTPError as exc:
                return exc.code, dict(exc.headers.items()), None
            return resp.status, dict(resp.headers.items()), resp
    status, got, body = transport(method, url, headers)
    got = {k.lower(): v for k, v in got.items()}
    if method != "GET" or dest is None or status not in (200, 206):
        if body is not None:
            body.close()
        return status, got, 0
    if status == 200 and have:
        have = 0                       # the server ignored the Range: start over
    length = got.get("content-length")
    total = have + int(length) if length is not None else None
    if max_bytes is not None and (total is None or total > max_bytes):
        body.close()
        raise SystemExit(f"Refused {url}: {total} bytes, over the {max_bytes:,} byte limit given.")
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    with open(part, "ab" if have else "wb") as out:
        while True:
            chunk = body.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
    body.close()
    size = part.stat().st_size
    if total is not None and size != total:
        raise SystemExit(f"{url}: {size:,} of {total:,} bytes arrived. The partial file is kept "
                         f"({part.name}); the same command continues it.")
    part.replace(dest)
    return status, got, size


def load_index(path, *, transport=None):
    """The server's region index (GeoJSON features: id, name, urls, a
    polygon), from `path`; downloaded there once when absent."""
    path = Path(path)
    if not path.exists():
        status, _, _ = fetch(INDEX_URL, path, transport=transport)
        if status != 200:
            raise SystemExit(f"{INDEX_URL} answered {status}")
    return json.loads(path.read_bytes().decode("utf-8"))


def regions_covering(index, geom):
    """The index features whose polygon covers `geom` (shapely, EPSG:4326),
    smallest first. Area in square degrees: only the order is used, and the
    regions nest."""
    from shapely.geometry import shape
    minx, miny, maxx, maxy = geom.bounds
    out = []
    for f in index["features"]:
        if not f.get("geometry") or "pbf" not in f["properties"].get("urls", {}):
            continue
        shp = shape(f["geometry"])
        bx0, by0, bx1, by1 = shp.bounds
        if bx0 <= minx and by0 <= miny and bx1 >= maxx and by1 >= maxy and shp.covers(geom):
            out.append((shp.area, f))
    return [f for _, f in sorted(out, key=lambda t: (t[0], t[1]["properties"]["id"]))]


def smallest_region(index, geom):
    """The smallest region covering `geom`, or exit: the publisher asks for
    the smallest file that holds what is needed."""
    found = regions_covering(index, geom)
    if not found:
        raise SystemExit("No region in the index covers the whole geometry.")
    return found[0]


def has_subregions(index, feature):
    """True when the index cuts this region into smaller ones (a country
    with states, a continent). A set of points whose smallest covering
    region has subregions spans more than one of them."""
    rid = feature["properties"]["id"]
    return any(f["properties"].get("parent") == rid for f in index["features"])


def region_by_id(index, region_id):
    for f in index["features"]:
        if f["properties"]["id"] == region_id:
            return f
    raise SystemExit(f"No region {region_id!r} in the index.")


def region_short(feature):
    """"washington" for .../us/washington-latest.osm.pbf: the folder an
    extract is kept in and the stem of its dated files."""
    return feature["properties"]["urls"]["pbf"].rsplit("/", 1)[-1].replace("-latest.osm.pbf", "")


def held_extracts(root, short):
    """The dated extracts of a region on disk, newest name last."""
    folder = Path(root) / short
    return sorted(p for p in folder.glob(f"{short}-*.osm.pbf") if DATED.match(p.name))


def _ledger(root):
    path = Path(root) / LEDGER_NAME
    return json.loads(path.read_bytes().decode("utf-8")) if path.exists() else []


def _ledger_add(root, entry):
    rows = _ledger(root) + [entry]
    (Path(root) / LEDGER_NAME).write_bytes((json.dumps(rows, indent=1) + "\n").encode("utf-8"))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


LOCK_NAME = "_download.lock"
LOCK_POLL_S = 5


def _pid_alive(pid):
    try:
        import psutil
    except ImportError:
        return True
    return psutil.pid_exists(pid)


class DownloadLock:
    """One download from the server at a time on this machine, across
    processes: root/_download.lock names its holder's pid. A second caller
    waits (up to wait_s) and then finds the first one's file held; a lock
    whose process is gone is replaced. alive and sleep are injected by the
    selftest."""

    def __init__(self, root, wait_s=3600, alive=_pid_alive, sleep=None):
        import time
        self.path = Path(root) / LOCK_NAME
        self.wait_s, self.alive, self.sleep = wait_s, alive, sleep or time.sleep

    def __enter__(self):
        import os
        self.path.parent.mkdir(parents=True, exist_ok=True)
        waited = 0
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    pid = int(self.path.read_text(encoding="utf-8").strip() or -1)
                except (OSError, ValueError):
                    pid = -1
                if pid != -1 and not self.alive(pid):
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                if waited >= self.wait_s:
                    raise SystemExit(f"Another download is running (pid {pid}, {self.path}); waited "
                                     f"{waited} s. Run again when it has finished.")
                self.sleep(LOCK_POLL_S)
                waited += LOCK_POLL_S
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(str(os.getpid()))
            return self

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def download_extract(feature, root, *, lock=None, **kwargs):
    """_download_extract() under the machine's DownloadLock, so two runs that
    need one regional file never both download it: the second waits, then
    finds the file held."""
    with (lock or DownloadLock(root)):
        return _download_extract(feature, root, **kwargs)


def _download_extract(feature, root, *, dated=None, max_age_days=None, max_bytes=None,
                      transport=None, now=None, out=print):
    """The path of a region's extract under root/<region>/, downloading at
    most one file. In order:

      1. a held extract no older than `max_age_days` (by its own header
         timestamp) is returned with no request;
      2. otherwise the `-latest` name is resolved to its dated file with one
         HEAD (or `dated` names it, YYMMDD);
      3. that dated file already held: returned, no download;
      4. that dated file in the ledger (downloaded once, since removed):
         refused. The same file is never downloaded twice;
      5. one GET, recorded in root/downloads.json with its bytes and sha256.

    A region updated more often than weekly should be brought forward with
    the publisher's diffs instead (osmium / pyosmium-up-to-date), which this
    function does not do."""
    root = Path(root)
    short = region_short(feature)
    latest = check_url(feature["properties"]["urls"]["pbf"])
    held = held_extracts(root, short)
    if dated is None and held and max_age_days is not None:
        age = age_days(extract_timestamp(held[-1]), now)
        if age is not None and age <= max_age_days:
            out(f"{held[-1].name}: held, {age:.1f} days old, no request made")
            return held[-1]
    if dated is None:
        status, got, _ = fetch(latest, method="HEAD", transport=transport)
        url = got.get("location")
        if status not in (301, 302, 303, 307, 308) or not url:
            raise SystemExit(f"{latest} answered {status} with no redirect to a dated file; "
                             f"name one with --dated YYMMDD.")
        from urllib.parse import urljoin
        url = check_url(urljoin(latest, url))
    else:
        if not re.fullmatch(r"\d{6}", dated):
            raise SystemExit(f"--dated takes YYMMDD, not {dated!r}")
        url = latest.replace("-latest.osm.pbf", f"-{dated}.osm.pbf")
    name = url.rsplit("/", 1)[-1]
    if not DATED.match(name):
        raise SystemExit(f"{url} is not a dated extract (<region>-YYMMDD.osm.pbf).")
    dest = root / short / name
    if dest.exists():
        out(f"{name}: held, not downloaded again")
        return dest
    if any(row["file"] == name for row in _ledger(root)):
        raise SystemExit(f"{name} was downloaded once already ({root / LEDGER_NAME}) and is no longer "
                         f"on disk. The same file is never requested twice: restore it, or wait for "
                         f"the next dated file.")
    status, got, size = fetch(url, dest, transport=transport, max_bytes=max_bytes)
    if status not in (200, 206):
        raise SystemExit(f"{url} answered {status}")
    _ledger_add(root, {"file": name, "url": url, "bytes": dest.stat().st_size, "sha256": sha256_of(dest),
                       "downloaded_utc": (now or datetime.datetime.now(datetime.timezone.utc))
                       .isoformat(timespec="seconds")})
    out(f"{name}: downloaded, {dest.stat().st_size:,} bytes")
    return dest


def extract_timestamp(pbf):
    """The data date an extract's own header states (ISO, UTC), or None."""
    import osmium
    reader = osmium.io.Reader(str(pbf))
    try:
        header = reader.header()
        return header.get("osmosis_replication_timestamp") or header.get("timestamp") or None
    finally:
        reader.close()


def age_days(timestamp, now=None):
    """Days from an ISO timestamp to now; None when it does not parse."""
    try:
        then = datetime.datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
    except ValueError:
        return None
    if then.tzinfo is None:
        then = then.replace(tzinfo=datetime.timezone.utc)
    return ((now or datetime.datetime.now(datetime.timezone.utc)) - then).total_seconds() / 86400


# ------------------------------------------------- several regions read as one

# The most regions read as one. Philadelphia needs two and no measured city
# more than three (2026-10-13); an area needing more than four is nearer a
# country than a city, and a person's call.
SET_MAX_REGIONS = 4
# The files of a set must state ONE data timestamp. Measured on the 23
# extracts held on 2026-10-13: every file of one daily run carries the same
# timestamp to the second (19 of 2026-10-12T20:21:35Z, 4 of
# 2026-10-08T20:21:06Z, across four continents), and two runs are a day
# apart. No bound between zero and a day therefore tells anything apart, and
# a day is too much: an object moved over the cut between two snapshots can
# be in neither file, which no comparison of copies can see. Re-measure if
# the publisher starts stamping regions separately.
SET_MAX_SPREAD_S = 0


class NoRegionSet(SystemExit):
    """No region and no set of regions answers for a geometry under the
    rules given: choose_regions()'s refusal, for a caller that goes on."""


class ExtractSet(tuple):
    """The extracts of several regions read as ONE, in the order chosen: a
    tuple of paths that also answers the few questions callers ask of a
    single extract's path (name, exists(), Path(x).name), so a line written
    for one file names the whole set."""

    @property
    def name(self):
        return " + ".join(p.name for p in self)

    def exists(self):
        return all(p.exists() for p in self)

    def __fspath__(self):
        return self.name

    def __str__(self):
        return " + ".join(str(p) for p in self)


def as_files(pbf):
    """[Path] for one extract or for a set of them."""
    if isinstance(pbf, (list, tuple)):
        return [Path(p) for p in pbf]
    return [Path(pbf)]


def one_or_set(pbf):
    """A Path for one extract, an ExtractSet for several."""
    files = as_files(pbf)
    return files[0] if len(files) == 1 else ExtractSet(files)


def set_timestamp(pbf, max_spread_s=SET_MAX_SPREAD_S):
    """The data date of one extract, or of a set: the oldest of its files'.
    Exits when the files of a set state timestamps more than `max_spread_s`
    apart (SET_MAX_SPREAD_S has the reason), or one states none."""
    files = as_files(pbf)
    stamps = [extract_timestamp(f) for f in files]
    if len(files) == 1:
        return stamps[0]
    ages = [age_days(s, datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)) for s in stamps]
    listed = ", ".join(f"{f.name} {s}" for f, s in zip(files, stamps))
    if any(a is None for a in ages):
        raise SystemExit(f"A set of extracts is read as one only when every file states its data date: {listed}.")
    spread = (max(ages) - min(ages)) * 86400
    if spread > max_spread_s + 1e-6:
        raise SystemExit(f"The extracts are not one snapshot: {listed} ({spread:,.0f} s apart, the bound is "
                         f"{max_spread_s} s). An object moved across the cut between two dates can be in "
                         f"neither file. Download the set as one dated run (download ... --dated YYMMDD).")
    return stamps[ages.index(min(ages))]


def regions_meeting(index, geom):
    """[(feature, polygon)] for the index regions with an extract whose
    polygon meets `geom`, by region id."""
    from shapely.geometry import shape
    minx, miny, maxx, maxy = geom.bounds
    out = []
    for f in index["features"]:
        if not f.get("geometry") or "pbf" not in f["properties"].get("urls", {}):
            continue
        shp = shape(f["geometry"])
        bx0, by0, bx1, by1 = shp.bounds
        if bx0 <= maxx and bx1 >= minx and by0 <= maxy and by1 >= miny and shp.intersects(geom):
            out.append((f, shp))
    return sorted(out, key=lambda t: t[0]["properties"]["id"])


def choose_regions(index, geom, size_of, *, max_bytes=None, max_regions=SET_MAX_REGIONS):
    """([feature, ...], why) for the extract(s) that answer for `geom`.

    ONE region whenever one will do: the smallest region covering the
    geometry, when no other region meets it (the usual case, decided with no
    request), when no size cap is given, or when its file is no larger than
    `max_bytes`. `why` is then None.

    Otherwise the SMALLEST SET, by total bytes, of at most `max_regions`
    regions that each cover part of the geometry, are each no larger than
    `max_bytes`, and whose polygons together cover all of it. `why` says
    which single region was passed over and what the set weighs.

    `size_of(feature)` -> bytes is asked only for the regions a decision
    needs. Raises NoRegionSet, saying which of three things failed: a region
    of the only covering sets is over the cap, more than `max_regions` are
    needed, or the index does not cover the geometry at all."""
    from itertools import combinations
    from shapely.ops import unary_union
    covering = regions_covering(index, geom)
    whole = {f["properties"]["id"] for f in covering}
    partial = [(f, shp) for f, shp in regions_meeting(index, geom) if f["properties"]["id"] not in whole]
    if covering and (max_bytes is None or not partial):
        return [covering[0]], None
    cap = float("inf") if max_bytes is None else max_bytes

    def mb(n):
        return f"{n / 2 ** 20:,.0f} MB"

    passed = "no single region covers it"
    if covering:
        size = size_of(covering[0])
        if size <= cap:
            return [covering[0]], None
        passed = (f"the smallest single region, {covering[0]['properties']['id']}, is {mb(size)}, over the "
                  f"{mb(cap)} cap")
    sized = [(f, shp, size_of(f)) for f, shp in partial]

    def best(rows):
        found = None
        for n in range(2, max_regions + 1):
            for combo in combinations(rows, n):
                if unary_union([shp for _, shp, _ in combo]).covers(geom):
                    key = (sum(size for _, _, size in combo), n, [f["properties"]["id"] for f, _, _ in combo])
                    if found is None or key < found[0]:
                        found = (key, combo)
        return found

    def listed(combo):
        return " + ".join(f"{f['properties']['id']} ({mb(size)})" for f, _, size in combo)

    found = best([row for row in sized if row[2] <= cap])
    if found is not None:
        (total, _, _), combo = found
        return [f for f, _, _ in combo], (f"{passed}; the smallest set of regions that together cover it: "
                                          f"{listed(combo)}, {mb(total)} in all")
    over = best(sized)
    if over is not None:
        raise NoRegionSet(f"No region or set of regions under the cap covers the whole geometry: {passed}, "
                          f"and the smallest covering set is {listed(over[1])}, with a file over the "
                          f"{mb(cap)} cap. A larger download is a person's call (--max-mb).")
    if sized and unary_union([shp for _, shp, _ in sized]).covers(geom):
        raise NoRegionSet(f"More than {max_regions} regions are needed to cover the whole geometry "
                          f"({len(sized)} meet it): {passed}. A set that wide is a person's call.")
    raise NoRegionSet(f"No region in the index covers the whole geometry, and no set of them does: {passed}.")


def extract_size(feature, root, *, max_age_days=None, transport=None, now=None):
    """{"bytes", "date" (YYMMDD), "held"} for the extract of a region that
    download_extract() would return: the held file when one is young enough
    (no request), else the dated file `-latest` names (one HEAD), sized from
    disk when held and by a second HEAD when not. Nothing is downloaded."""
    root = Path(root)
    short = region_short(feature)
    held = held_extracts(root, short)
    if held and max_age_days is not None:
        age = age_days(extract_timestamp(held[-1]), now)
        if age is not None and age <= max_age_days:
            return {"bytes": held[-1].stat().st_size, "date": DATED.match(held[-1].name).group("date"),
                    "held": True}
    from urllib.parse import urljoin
    latest = check_url(feature["properties"]["urls"]["pbf"])
    status, got, _ = fetch(latest, method="HEAD", transport=transport)
    url = got.get("location")
    if status not in (301, 302, 303, 307, 308) or not url:
        raise SystemExit(f"{latest} answered {status} with no redirect to a dated file.")
    url = check_url(urljoin(latest, url))
    name = url.rsplit("/", 1)[-1]
    m = DATED.match(name)
    if not m:
        raise SystemExit(f"{url} is not a dated extract (<region>-YYMMDD.osm.pbf).")
    dest = root / short / name
    if dest.exists():
        return {"bytes": dest.stat().st_size, "date": m.group("date"), "held": True}
    status, got, _ = fetch(url, method="HEAD", transport=transport)
    if status != 200 or "content-length" not in got:
        raise SystemExit(f"{url} answered {status} with no size to a HEAD.")
    return {"bytes": int(got["content-length"]), "date": m.group("date"), "held": False}


def download_set(features, root, *, sizes=None, max_age_days=None, max_bytes=None, transport=None,
                 now=None, out=print, lock=None):
    """The extracts of several regions as an ExtractSet, all of ONE dated
    run, each through download_extract() and so under every one of its
    rules: one download at a time, never a file in the ledger, the host
    check, `max_bytes` a file.

    The date is the one most of the set is already held at (the newest of
    those on a tie), else the oldest date `-latest` names across the set:
    the fewest files are downloaded, and the server keeps several days of
    dated files. `sizes` is {region id: extract_size()} when the caller has
    asked already. The set is refused when its files do not state one
    timestamp (set_timestamp)."""
    root = Path(root)
    sizes = dict(sizes or {})
    for f in features:
        rid = f["properties"]["id"]
        if rid not in sizes:
            sizes[rid] = extract_size(f, root, max_age_days=max_age_days, transport=transport, now=now)
    dates = sorted({s["date"] for s in sizes.values()})

    def held_at(date):
        return sum((root / region_short(f) / f"{region_short(f)}-{date}.osm.pbf").exists() for f in features)

    most = max(held_at(d) for d in dates)
    date = max(d for d in dates if held_at(d) == most) if most else dates[0]
    if len(dates) > 1:
        out(f"set: the regions' current files are of {len(dates)} dates ({', '.join(dates)}); all are taken "
            f"as of {date}")
    paths = [download_extract(f, root, dated=date, max_bytes=max_bytes, transport=transport, now=now,
                              out=out, lock=lock) for f in features]
    found = ExtractSet(paths)
    set_timestamp(found)
    return found


class _Once:
    """Takes each object once across the files of a set. An extract keeps
    whole every way and relation that crosses its cut, so one object can be
    in two files. Of two copies:

      * equal copies: the first is kept (counted in `duplicates`);
      * one holding more of its nodes' positions than the other: that one,
        since a copy cut short is incomplete, not a different object;
      * anything else: NEITHER is trusted. The pair is listed in
        `differing` and stop() ends the read. Files of one snapshot cannot
        differ, so a difference means the set is not what it claims, and
        choosing a copy would be a guess."""

    def __init__(self, files):
        self.names = [Path(f).name for f in files]
        self.where, self.duplicates, self.differing = {}, {}, []

    def take(self, store, kind, oid, value, version, at, weight=0):
        key = (kind, oid)
        if oid not in store:
            store[oid] = value
            self.where[key] = (at, version, weight)
            return
        first, had, weight0 = self.where[key]
        self.duplicates[kind] = self.duplicates.get(kind, 0) + 1
        if store[oid] == value:
            return
        if weight != weight0:
            if weight > weight0:
                store[oid] = value
                self.where[key] = (at, version, weight)
            return
        self.differing.append(f"{kind} {oid} ({self.names[first]} version {had}, {self.names[at]} "
                              f"version {version})")

    def stop(self):
        if self.differing:
            shown = "; ".join(self.differing[:10])
            more = f"; and {len(self.differing) - 10} more" if len(self.differing) > 10 else ""
            raise SystemExit(f"{' + '.join(self.names)}: {len(self.differing)} object(s) are in two files with "
                             f"different content, and neither copy is taken on a guess: {shown}{more}. "
                             f"Files of one snapshot hold equal copies: download the set again as one "
                             f"dated run.")


# ------------------------------------------------------------------- the area

def boundary_polygon(members):
    """One boundary's polygon from its member ways: [(role, [(lat, lon),
    ...])]. Outer rings (an empty role counts as outer) are polygonized and
    the inner rings cut out (rule 2). Raises ValueError when an outer ring
    does not close, which is also what a boundary cut off at the extract's
    edge looks like."""
    from shapely.geometry import LineString
    from shapely.ops import polygonize_full, unary_union

    def rings(want_inner):
        lines = [LineString([(lon, lat) for lat, lon in pts]) for role, pts in members
                 if ((role or "outer") == "inner") == want_inner and (role or "outer") in ("outer", "inner")
                 and len(pts) >= 2]
        if not lines:
            return None, False
        polys, _cuts, dangles, _invalid = polygonize_full(unary_union(lines))
        return (unary_union(list(polys.geoms)) if len(polys.geoms) else None), len(dangles.geoms) > 0

    outer, open_outer = rings(False)
    if outer is None or outer.is_empty or open_outer:
        raise ValueError("an outer ring does not close")
    inner, _ = rings(True)
    return outer.difference(inner) if inner is not None else outer


def _overpass_lat(lat):
    """A latitude as the double Overpass holds: stored as an integer of
    1e-7 degrees offset by 91 degrees, and converted back by a subtraction
    that leaves a different last bit from lat itself."""
    return (round(lat * 1e7) + 910000000) / 10000000.0 - 91.0


def bbox_center(points):
    """Rule 5, `out center`: the middle of the bounding box of [(lat, lon)]
    at 7 decimals. Half the time the middle of two 7-decimal values is an
    exact half in the 8th decimal, and which way it prints depends on the
    arithmetic: the latitude is therefore averaged from _overpass_lat()
    doubles and the longitude from plain ones. Measured on Tbilisi's 772
    centers, 389 of them true halves (2026-10-13): this form matches every
    one; round((lo + hi) / 2, 7) misses 121 latitudes by one last digit,
    and applying the offset to longitudes misses 113."""
    lats = [_overpass_lat(p[0]) for p in points]
    lons = [p[1] for p in points]
    return {"lat": float("%.7f" % ((min(lats) + max(lats)) / 2)),
            "lon": float("%.7f" % ((min(lons) + max(lons)) / 2))}


class Area:
    """The areas of an Overpass `area(...)->.a`: one polygon per boundary,
    kept apart (rule 1). points_in and ways_in answer for many elements at
    once: every polygon is prepared, every test starts with a bounding-box
    reject, and the exact line test of rule 3 runs only on ways with no node
    inside whose line meets a polygon at all (Seattle, 11 boundaries: 172 s
    as one relate per way and boundary, 2026-10-13)."""

    def __init__(self, parts):
        import shapely
        self.parts = list(parts)
        if not self.parts:
            raise ValueError("an area needs at least one boundary polygon")
        for p in self.parts:
            shapely.prepare(p)
        bounds = [p.bounds for p in self.parts]
        self.bounds = (min(b[0] for b in bounds), min(b[1] for b in bounds),
                       max(b[2] for b in bounds), max(b[3] for b in bounds))

    def in_bounds(self, lat, lon):
        minx, miny, maxx, maxy = self.bounds
        return minx <= lon <= maxx and miny <= lat <= maxy

    def points_in(self, lats, lons):
        """A boolean per point: strictly inside one boundary. A point on a
        boundary line is in none."""
        import numpy as np
        import shapely
        x, y = np.asarray(lons, dtype=float), np.asarray(lats, dtype=float)
        hit = np.zeros(len(x), dtype=bool)
        for p in self.parts:
            minx, miny, maxx, maxy = p.bounds
            todo = ~hit & (x >= minx) & (x <= maxx) & (y >= miny) & (y <= maxy)
            if todo.any():
                hit[todo] = shapely.contains_xy(p, x[todo], y[todo])
        return hit

    def ways_in(self, ways):
        """A boolean per way, each a list of (lat, lon): rule 3."""
        import numpy as np
        import shapely
        if not ways:
            return []
        counts = np.array([len(w) for w in ways], dtype=np.int64)
        flat = np.array([pt for w in ways for pt in w], dtype=float).reshape(-1, 2)
        inside = self.points_in(flat[:, 0], flat[:, 1])
        owner = np.repeat(np.arange(len(ways)), counts)
        result = np.zeros(len(ways), dtype=bool)
        result[np.unique(owner[inside])] = True
        # Rule 3's second half, only for ways with no node inside.
        rest = np.flatnonzero(~result & (counts >= 2))
        if len(rest):
            keep = np.isin(owner, rest)
            index = np.searchsorted(rest, owner[keep])
            lines = shapely.linestrings(flat[keep][:, ::-1], indices=index)
            lb = shapely.bounds(lines)
            through = np.zeros(len(rest), dtype=bool)
            for p in self.parts:
                minx, miny, maxx, maxy = p.bounds
                near = ~through & (lb[:, 0] <= maxx) & (lb[:, 2] >= minx) & (lb[:, 1] <= maxy) & (lb[:, 3] >= miny)
                idx = np.flatnonzero(near)
                if not len(idx):
                    continue
                idx = idx[shapely.intersects(p, lines[idx])]
                if len(idx):
                    through[idx] = shapely.relate_pattern(lines[idx], p, "T********")
            result[rest[through]] = True
        return [bool(v) for v in result]


# ---------------------------------------------------------------- the clauses

KIND_WORDS = {"node": "n", "way": "w", "rel": "r", "relation": "r",
              "nwr": "nwr", "nw": "nw", "wr": "wr", "nr": "nr"}
_STATEMENT = re.compile(r"^(?P<kind>[a-z]+)(?P<filters>(?:\[.*\])+)\(area\.\w+\)(?:->\.\w+)?;$")
_FILTER = re.compile(r'\[\s*(?P<neg>!?)\s*"(?P<key>[^"]+)"\s*(?:(?P<op>=|!=|~|!~)\s*"(?P<value>[^"]*)")?\s*\]')


class Clause:
    """One statement of a union: which element kinds ("n", "w", "r") and the
    tag filters all of which must hold. A filter is (key, op, value) with op
    one of "has", "not", "=", "!=", "~", "!~". As in Overpass, "!=" and "!~"
    also hold when the key is absent, and "~" searches: it is anchored only
    by the pattern's own ^ and $. Patterns are run by Python's re, so a
    POSIX-only construct ([[:alpha:]]) is refused rather than misread."""

    def __init__(self, kinds, filters, text=""):
        self.kinds, self.text = frozenset(kinds), text
        self.filters = []
        for key, op, value in filters:
            if op in ("~", "!~"):
                if "[[:" in value:
                    raise ValueError(f"POSIX character class in {value!r}: not the same in Python's re")
                value = re.compile(value)
            elif op not in ("has", "not", "=", "!="):
                raise ValueError(f"unknown filter operator {op!r}")
            self.filters.append((key, op, value))

    def matches(self, tags):
        for key, op, value in self.filters:
            got = tags.get(key)
            if op == "has":
                ok = got is not None
            elif op == "not":
                ok = got is None
            elif op == "=":
                ok = got == value
            elif op == "!=":
                ok = got != value
            elif op == "~":
                ok = got is not None and value.search(got) is not None
            else:
                ok = got is None or value.search(got) is None
            if not ok:
                return False
        return True

    def required_keys(self):
        """Keys an element must carry for this clause to hold."""
        return {key for key, op, _ in self.filters if op in ("has", "=", "~")}


def parse_statement(line):
    """A Clause from one Overpass statement cut by an area, as written:
    `nwr["railway"~"^(station|halt)$"]["name"](area.a);`. Raises ValueError
    on anything else (a bbox, a recursion, `around`, a case flag): a
    statement this cannot represent must stop the caller, never be skipped."""
    text = line.strip()
    m = _STATEMENT.match(text)
    if not m or m.group("kind") not in KIND_WORDS:
        raise ValueError(f"not an area-filtered tag statement: {text!r}")
    filters, pos, body = [], 0, m.group("filters")
    for f in _FILTER.finditer(body):
        if f.start() != pos:
            break
        pos = f.end()
        if f.group("neg"):
            if f.group("op"):
                raise ValueError(f"negated key with a value in {text!r}")
            filters.append((f.group("key"), "not", None))
        else:
            filters.append((f.group("key"), f.group("op") or "has", f.group("value")))
    if pos != len(body) or not filters:
        raise ValueError(f"a filter in {text!r} is not one of [\"k\"], [!\"k\"], [\"k\"=\"v\"], "
                         f"[\"k\"!=\"v\"], [\"k\"~\"re\"], [\"k\"!~\"re\"]")
    return Clause(KIND_WORDS[m.group("kind")], filters, text)


def parse_union(text):
    """[Clause] for the statements of a union, one per non-empty line."""
    return [parse_statement(line) for line in text.splitlines() if line.strip()]


def matching(unions, kind, tags):
    """The names of the unions ({name: [Clause]}) an element of `kind`
    with `tags` belongs to."""
    return [name for name, clauses in unions.items()
            if any(kind in c.kinds and c.matches(tags) for c in clauses)]


def prefilter_keys(unions):
    """Tag keys to filter on inside the reader, before any element reaches
    Python: a key every clause requires when there is one, else one required
    key per clause; None when some clause requires no key (every element is
    then read)."""
    clauses = [c for cs in unions.values() for c in cs]
    need = [c.required_keys() for c in clauses]
    if not clauses or any(not n for n in need):
        return None
    common = set.intersection(*need)
    if common:
        return (sorted(common)[0],)
    return tuple(sorted({sorted(n)[0] for n in need}))


def parse_area(text):
    """An Overpass area selector as {"relations": ids, "ways": ids, "tags":
    [(key, value)]}: "(id:3600237385,2400012345)" names areas by id (3.6e9
    plus a relation's id, 2.4e9 plus a way's), and `["k"="v"]["k2"="v2"]`
    names every area carrying those tags. Raises ValueError otherwise."""
    compact = str(text).replace(" ", "")
    spec = {"relations": set(), "ways": set(), "tags": []}
    if re.fullmatch(r"\(id:\d+(,\d+)*\)", compact):
        for n in map(int, re.findall(r"\d+", compact)):
            if n >= AREA_RELATION_BASE:
                spec["relations"].add(n - AREA_RELATION_BASE)
            elif n >= AREA_WAY_BASE:
                spec["ways"].add(n - AREA_WAY_BASE)
            else:
                raise ValueError(f"area id {n} is neither a relation's (3600000000+) nor a way's (2400000000+)")
        return spec
    pos = 0
    for f in _FILTER.finditer(str(text).strip()):
        if f.start() != pos or f.group("neg") or f.group("op") != "=":
            break
        pos = f.end()
        spec["tags"].append((f.group("key"), f.group("value")))
    if pos != len(str(text).strip()) or not spec["tags"]:
        raise ValueError(f"area selector {text!r} is neither (id:...) nor a list of [\"k\"=\"v\"] filters")
    return spec


# -------------------------------------------------------------------- the read

def query(pbf, area_spec, unions, *, on_area=None, say=None):
    """Answer `unions` ({name: [Clause]}) inside the area `area_spec`
    (parse_area) from the extract `pbf`. Returns a dict:

      boundaries  [{"type", "id", "tags", "members" or "points", ...}], by
                  type then id: what the area was made from
      area        the Area
      elements    {union name: [element]}: nodes, then ways, then relations,
                  each by ascending id. A node has lat and lon; a way has
                  "nodes" (every ref) and "points" [(ref, lat, lon)] for the
                  refs the extract holds; a relation has "points" [(lat,
                  lon)] of its member nodes and member ways' nodes
      stats       counts, among them ways and relations with members the
                  extract does not hold (a relation running past the
                  region's edge: its center then differs from Overpass's)

    `on_area(boundaries, area)` runs once the area is built and before the
    heavy pass, so a caller can stop a wrong area early.

    SEVERAL EXTRACTS READ AS ONE: the first argument may be a list of files
    (an ExtractSet). Each pass then reads the files in turn, every id is
    taken once (_Once), and a boundary whose member ways lie in different
    files is assembled from all of them. One file's node positions are held
    at a time, so the peak is the largest file's, not the sum. A caller
    checks the set is one snapshot first (set_timestamp); stats gains
    "files" and "taken_once".

    Three passes. (1) relations: the boundaries and the candidate relations
    by tag. (2) their member ways and nodes by id, with positions. (3) every
    node and way passing prefilter_keys(), with positions, kept when its
    tags match and its bounding box meets the area's; the area tests then
    run on all of them at once.

    A tag selector is matched against RELATIONS of type boundary or
    multipolygon only; an area Overpass makes from a closed way is named by
    id."""
    import osmium
    pbf = one_or_set(pbf)
    files, once = as_files(pbf), _Once(as_files(pbf))
    say = say or (lambda text: None)
    stats = {}
    keys = prefilter_keys(unions)
    want_rel = area_spec["relations"]
    want_tags = area_spec["tags"]
    rel_unions = {n: [c for c in cs if "r" in c.kinds] for n, cs in unions.items()}
    rel_unions = {n: cs for n, cs in rel_unions.items() if cs}

    # Pass 1: relations.
    boundaries, cand_rel = {}, {}
    if want_rel or want_tags or rel_unions:
        for at, path in enumerate(files):
            for o in osmium.FileProcessor(str(path), osmium.osm.RELATION):
                is_boundary = o.id in want_rel
                tags = None
                if want_tags and not is_boundary:
                    tags = dict(o.tags)
                    is_boundary = (tags.get("type") in ("boundary", "multipolygon")
                                   and all(tags.get(k) == v for k, v in want_tags))
                if is_boundary or (rel_unions and (keys is None or any(k in o.tags for k in keys))):
                    tags = dict(o.tags) if tags is None else tags
                    members = [(m.type, m.ref, m.role) for m in o.members]
                    if is_boundary:
                        once.take(boundaries, "boundary relation", o.id, (tags, members), o.version, at)
                    names = matching(rel_unions, "r", tags) if rel_unions else []
                    if names:
                        once.take(cand_rel, "relation", o.id, (tags, members, names), o.version, at)
    missing = want_rel - set(boundaries)
    if missing:
        raise SystemExit(f"{Path(pbf).name}: boundary relation(s) {sorted(missing)} are not in the extract.")
    if want_tags and not boundaries:
        raise SystemExit(f"{Path(pbf).name}: no boundary or multipolygon relation carries {want_tags}.")
    say(f"pass 1: {len(boundaries)} boundary relation(s), {len(cand_rel):,} candidate relations")

    # Pass 2: member ways and nodes by id.
    need_ways = {ref for _, mem in boundaries.values() for t, ref, _ in mem if t == "w"}
    need_ways |= {ref for _, mem, _ in cand_rel.values() for t, ref, _ in mem if t == "w"}
    need_ways |= area_spec["ways"]
    need_nodes = {ref for _, mem in boundaries.values() for t, ref, _ in mem if t == "n"}
    need_nodes |= {ref for _, mem, _ in cand_rel.values() for t, ref, _ in mem if t == "n"}
    way_pts, way_tags, node_pt = {}, {}, {}
    for at, path in enumerate(files if need_ways or need_nodes else ()):
        fp = (osmium.FileProcessor(str(path), osmium.osm.NODE | osmium.osm.WAY).with_locations()
              .with_filter(osmium.filter.IdFilter(need_ways | need_nodes)))
        for o in fp:
            if o.is_way():
                if o.id in need_ways:
                    pts = [(n.lat, n.lon) for n in o.nodes if n.location.valid()]
                    once.take(way_pts, "member way", o.id, pts, o.version, at, len(pts))
                    if o.id in area_spec["ways"]:
                        once.take(way_tags, "area way", o.id, (dict(o.tags), [n.ref for n in o.nodes]),
                                  o.version, at, len(pts))
            elif o.id in need_nodes:
                once.take(node_pt, "member node", o.id, (o.location.lat, o.location.lon), o.version, at)
    say(f"pass 2: {len(way_pts):,} of {len(need_ways):,} member ways, "
        f"{len(node_pt):,} of {len(need_nodes):,} member nodes")

    # The area.
    out_bounds, parts = [], []
    for wid in sorted(area_spec["ways"]):
        pts = way_pts.get(wid) or []
        if len(pts) < 4 or pts[0] != pts[-1]:
            raise SystemExit(f"{Path(pbf).name}: way/{wid} is not a closed way in the extract.")
        from shapely.geometry import Polygon
        parts.append(Polygon([(lon, lat) for lat, lon in pts]))
        out_bounds.append({"type": "way", "id": wid, "tags": way_tags[wid][0], "nodes": way_tags[wid][1],
                           "points": pts})
    for rid in sorted(boundaries):
        tags, members = boundaries[rid]
        absent = [ref for t, ref, _ in members if t == "w" and ref not in way_pts]
        try:
            if absent:
                raise ValueError(f"{len(absent)} member way(s) are not in the extract")
            parts.append(boundary_polygon([(role, way_pts[ref]) for t, ref, role in members if t == "w"]))
        except ValueError as exc:
            if len(files) > 1:
                raise SystemExit(f"{Path(pbf).name}: relation/{rid} ({tags.get('name')}): {exc}. The "
                                 f"boundary is not whole in these extracts read together: the set does "
                                 f"not cover it.")
            raise SystemExit(f"{Path(pbf).name}: relation/{rid} ({tags.get('name')}): {exc}. The "
                             f"boundary is not whole in this extract: use the next larger region.")
        out_bounds.append({"type": "relation", "id": rid, "tags": tags, "members": [
            {"type": t, "ref": ref, "role": role,
             **({"points": way_pts[ref]} if t == "w" else {}),
             **({"point": node_pt[ref]} if t == "n" and ref in node_pt else {})}
            for t, ref, role in members]})
    area = Area(parts)
    if on_area is not None:
        on_area(out_bounds, area)

    # Pass 3: every candidate node and way, tested after the read.
    way_unions = {n: [c for c in cs if "w" in c.kinds] for n, cs in unions.items()}
    node_unions = {n: [c for c in cs if "n" in c.kinds] for n, cs in unions.items()}
    minx, miny, maxx, maxy = area.bounds
    node_once, way_once, read_n, read_w = {}, {}, 0, 0
    for at, path in enumerate(files):
        fp = osmium.FileProcessor(str(path), osmium.osm.NODE | osmium.osm.WAY).with_locations()
        if keys is not None:
            fp = fp.with_filter(osmium.filter.KeyFilter(*keys))
        for o in fp:
            if o.is_node():
                read_n += 1
                lat, lon = o.location.lat, o.location.lon
                if not (minx <= lon <= maxx and miny <= lat <= maxy):
                    continue
                tags = dict(o.tags)
                names = matching(node_unions, "n", tags)
                if names:
                    once.take(node_once, "node", o.id, (o.id, lat, lon, tags, names), o.version, at)
            elif o.is_way():
                read_w += 1
                tags = dict(o.tags)
                names = matching(way_unions, "w", tags)
                if not names:
                    continue
                refs = [n.ref for n in o.nodes]
                pts = [(n.ref, n.lat, n.lon) for n in o.nodes if n.location.valid()]
                if not pts:
                    continue
                lats = [p[1] for p in pts]
                lons = [p[2] for p in pts]
                if max(lons) < minx or min(lons) > maxx or max(lats) < miny or min(lats) > maxy:
                    continue
                once.take(way_once, "way", o.id, (o.id, refs, pts, tags, names), o.version, at, len(pts))
    # Each id once, whichever file gave it; a set whose copies disagree
    # answers nothing.
    once.stop()
    cand_nodes, cand_ways = list(node_once.values()), list(way_once.values())
    short = sum(len(c[2]) != len(c[1]) for c in cand_ways)
    if len(files) > 1:
        stats.update(files=[f.name for f in files], taken_once=dict(sorted(once.duplicates.items())))
        say(f"read as one: {len(files)} files, {sum(once.duplicates.values()):,} object(s) held by more "
            f"than one and taken once {stats['taken_once']}")
    say(f"pass 3: {read_n:,} nodes and {read_w:,} ways read; {len(cand_nodes):,} nodes and "
        f"{len(cand_ways):,} ways in the area's bounding box")

    elements = {name: [] for name in unions}
    cand_nodes.sort(key=lambda c: c[0])
    cand_ways.sort(key=lambda c: c[0])
    if cand_nodes:
        hit = area.points_in([c[1] for c in cand_nodes], [c[2] for c in cand_nodes])
        for ok, (nid, lat, lon, tags, names) in zip(hit, cand_nodes):
            if ok:
                for name in names:
                    elements[name].append({"type": "node", "id": nid, "lat": lat, "lon": lon, "tags": tags})
    hit = area.ways_in([[(lat, lon) for _, lat, lon in c[2]] for c in cand_ways])
    for ok, (wid, refs, pts, tags, names) in zip(hit, cand_ways):
        if ok:
            for name in names:
                elements[name].append({"type": "way", "id": wid, "nodes": refs, "points": pts, "tags": tags})

    # Rule 4: a candidate relation is in when a member node or way is.
    rel_ids = sorted(cand_rel)
    member_ways = sorted({ref for rid in rel_ids for t, ref, _ in cand_rel[rid][1] if t == "w" and ref in way_pts})
    way_ok = dict(zip(member_ways, area.ways_in([way_pts[w] for w in member_ways])))
    member_nodes = sorted({ref for rid in rel_ids for t, ref, _ in cand_rel[rid][1] if t == "n" and ref in node_pt})
    node_ok = dict(zip(member_nodes, area.points_in([node_pt[n][0] for n in member_nodes],
                                                    [node_pt[n][1] for n in member_nodes]))) if member_nodes else {}
    partial = 0
    for rid in rel_ids:
        tags, members, names = cand_rel[rid]
        points, inside, lacking = [], False, 0
        for t, ref, _ in members:
            if t == "w":
                if ref in way_pts:
                    points += way_pts[ref]
                    inside = inside or way_ok[ref]
                else:
                    lacking += 1
            elif t == "n":
                if ref in node_pt:
                    points.append(node_pt[ref])
                    inside = inside or bool(node_ok[ref])
                else:
                    lacking += 1
        if not inside or not points:
            continue
        partial += lacking > 0
        for name in names:
            elements[name].append({"type": "relation", "id": rid, "tags": tags, "points": points,
                                   "members_missing": lacking})
    stats.update(nodes_read=read_n, ways_read=read_w, ways_with_absent_nodes=short,
                 relations_with_absent_members=partial)
    if short or partial:
        say(f"NOTE: {short} way(s) with nodes the extract lacks and {partial} relation(s) with members it "
            f"lacks; their centers can differ from Overpass's")
    return {"boundaries": out_bounds, "area": area, "elements": elements, "stats": stats}


def boundaries_holding(pbf, points, *, tag=("boundary", "administrative"), say=None):
    """Every relation carrying `tag` whose area holds at least one of
    `points` [(lat, lon)], as Overpass's
    `is_in(lat,lon); rel(pivot)["boundary"="administrative"]; out tags;`
    gives them: ([{"type": "relation", "id", "tags"}] by ascending id,
    stats). Holes are honored (rule 2) and a point on a boundary line is in
    neither side.

    Three passes: the tagged relations and their member ways' ids; the
    member ways' node ids; those nodes' positions. A polygon is assembled
    only for a relation whose members' bounding box holds a point. A
    relation whose rings do not close in this extract (a country or state
    cut off at the region's edge) cannot be answered: it is left out and
    listed in stats["not_whole"] with its admin_level and name, where
    Overpass, holding the whole planet, would have returned it.

    The first argument may be several extracts read as one (query() has the
    rule): a relation cut at one file's edge is whole when the other files
    hold the rest of it."""
    import numpy as np
    import osmium
    import shapely
    files, once = as_files(pbf), _Once(as_files(pbf))
    say = say or (lambda text: None)
    rels = {}
    for at, path in enumerate(files):
        fp = osmium.FileProcessor(str(path), osmium.osm.RELATION).with_filter(osmium.filter.TagFilter(tag))
        for o in fp:
            if o.tags.get(tag[0]) == tag[1]:
                once.take(rels, "relation", o.id,
                          (dict(o.tags), [(m.ref, m.role) for m in o.members if m.type == "w"]), o.version, at)
    need = {ref for _, mem in rels.values() for ref, _ in mem}
    way_refs = {}
    for at, path in enumerate(files if need else ()):
        for o in osmium.FileProcessor(str(path), osmium.osm.WAY).with_filter(osmium.filter.IdFilter(need)):
            if o.id in need:
                once.take(way_refs, "way", o.id, [n.ref for n in o.nodes], o.version, at)
    node_ids = {r for refs in way_refs.values() for r in refs}
    pos = {}
    for at, path in enumerate(files if node_ids else ()):
        for o in osmium.FileProcessor(str(path), osmium.osm.NODE).with_filter(osmium.filter.IdFilter(node_ids)):
            if o.id in node_ids:
                once.take(pos, "node", o.id, (o.location.lat, o.location.lon), o.version, at)
    once.stop()
    say(f"{len(rels):,} relations with {tag[0]}={tag[1]}, {len(way_refs):,} of {len(need):,} member ways, "
        f"{len(pos):,} nodes")
    lats = np.array([p[0] for p in points], dtype=float)
    lons = np.array([p[1] for p in points], dtype=float)
    found, not_whole, assembled = [], [], 0
    for rid in sorted(rels):
        tags, members = rels[rid]
        lines = [(role, [pos[r] for r in way_refs[ref] if r in pos]) for ref, role in members if ref in way_refs]
        flat = [pt for _, pts in lines for pt in pts]
        if not flat:
            continue
        la = [p[0] for p in flat]
        lo = [p[1] for p in flat]
        near = (lats >= min(la)) & (lats <= max(la)) & (lons >= min(lo)) & (lons <= max(lo))
        whole = len(lines) == len(members) and all(
            len(pts) == len(way_refs[ref]) for (ref, _), (_, pts) in zip(members, lines))
        if not near.any():
            continue
        try:
            if not whole:
                raise ValueError("member ways or nodes are not in the extract")
            poly = boundary_polygon(lines)
        except ValueError:
            # Listed when the part of it the extract holds reaches a point;
            # one whose held part lies elsewhere is passed over unseen.
            not_whole.append({"id": rid, "admin_level": tags.get("admin_level"), "name": tags.get("name")})
            continue
        assembled += 1
        if shapely.contains_xy(poly, lons[near], lats[near]).any():
            found.append({"type": "relation", "id": rid, "tags": tags})
    stats = {"relations": len(rels), "assembled": assembled, "not_whole": not_whole}
    say(f"{assembled} assembled, {len(found)} hold a point, {len(not_whole)} not whole in this extract")
    return found, stats


# ------------------------------------------------------------ Overpass shapes

def r7(x):
    return round(x, 7)


def out_tags_center(el):
    """An element as Overpass's `out tags center` gives it."""
    if el["type"] == "node":
        return {"type": "node", "id": el["id"], "lat": r7(el["lat"]), "lon": r7(el["lon"]), "tags": el["tags"]}
    points = [(lat, lon) for _, lat, lon in el["points"]] if el["type"] == "way" else el["points"]
    return {"type": el["type"], "id": el["id"], "center": bbox_center(points), "tags": el["tags"]}


def out_body(el):
    """A way as `out body` gives it: its node ids and tags, no geometry."""
    return {"type": "way", "id": el["id"], "nodes": el["nodes"], "tags": el["tags"]}


def out_skel_nodes(ways):
    """The nodes of `ways` as `node(w); out skel` gives them: id and
    position, by ascending id, each once."""
    seen = {}
    for el in ways:
        for ref, lat, lon in el["points"]:
            seen[ref] = (lat, lon)
    return [{"type": "node", "id": ref, "lat": r7(lat), "lon": r7(lon)} for ref, (lat, lon) in sorted(seen.items())]


def out_geom(boundary):
    """A boundary as `out geom` gives it: a relation's member ways carry
    their geometry and its member nodes their position; a way carries its
    own. "bounds" is the bounding box of that geometry."""
    def geometry(points):
        return [{"lat": r7(lat), "lon": r7(lon)} for lat, lon in points]

    def bounds(points):
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        return {"minlat": r7(min(lats)), "minlon": r7(min(lons)), "maxlat": r7(max(lats)), "maxlon": r7(max(lons))}
    if boundary["type"] == "way":
        return {"type": "way", "id": boundary["id"], "bounds": bounds(boundary["points"]),
                "nodes": boundary["nodes"],
                "geometry": geometry(boundary["points"]), "tags": boundary["tags"]}
    members, every = [], []
    for m in boundary["members"]:
        entry = {"type": {"n": "node", "w": "way", "r": "relation"}[m["type"]], "ref": m["ref"], "role": m["role"]}
        if "points" in m:
            entry["geometry"] = geometry(m["points"])
            every += m["points"]
        if "point" in m:
            entry["lat"], entry["lon"] = r7(m["point"][0]), r7(m["point"][1])
            every.append(m["point"])
        members.append(entry)
    return {"type": "relation", "id": boundary["id"], "bounds": bounds(every), "members": members,
            "tags": boundary["tags"]}


# -------------------------------------------------------------------- selftest

def write_test_extract(path, nodes, ways, relations, timestamp="2026-01-01T00:00:00Z"):
    """A small .osm.pbf for a selftest: nodes {id: (lat, lon, tags)}, ways
    {id: ([node ids], tags)}, relations {id: ([(type, ref, role)], tags)}."""
    import osmium
    import osmium.osm.mutable as mutable
    header = osmium.io.Header()
    header.set("osmosis_replication_timestamp", timestamp)
    writer = osmium.SimpleWriter(str(path), header=header, overwrite=True)
    try:
        for nid in sorted(nodes):
            lat, lon, tags = nodes[nid]
            writer.add_node(mutable.Node(id=nid, location=(lon, lat), tags=tags))
        for wid in sorted(ways):
            refs, tags = ways[wid]
            writer.add_way(mutable.Way(id=wid, nodes=refs, tags=tags))
        for rid in sorted(relations):
            members, tags = relations[rid]
            writer.add_relation(mutable.Relation(id=rid, members=members, tags=tags))
    finally:
        writer.close()
    return path


def test_world():
    """Two square municipalities side by side, sharing the border lon = 1:
    relation 1 (lon 0 to 1, with a hole at 0.4 to 0.6) and relation 2 (lon 1
    to 2), lat 0 to 1 both. Returns (nodes, ways, relations)."""
    nodes, ways, relations = {}, {}, {}

    def node(nid, lat, lon, **tags):
        nodes[nid] = (lat, lon, tags)

    # Boundary corners; 3 and 4 are on the shared border.
    for nid, (lat, lon) in {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (0, 1), 5: (1, 2), 6: (0, 2),
                            7: (0.4, 0.4), 8: (0.6, 0.4), 9: (0.6, 0.6), 10: (0.4, 0.6)}.items():
        node(nid, lat, lon)
    ways[100] = ([4, 1, 2, 3], {})            # relation 1's own three sides
    ways[101] = ([3, 4], {})                  # the shared border
    ways[102] = ([3, 5, 6, 4], {})            # relation 2's own three sides
    ways[103] = ([7, 8, 9, 10, 7], {})        # the hole
    relations[1] = ([("w", 100, "outer"), ("w", 101, "outer"), ("w", 103, "inner")],
                    {"type": "boundary", "boundary": "administrative", "name": "Alpha", "admin_level": "8"})
    relations[2] = ([("w", 101, "outer"), ("w", 102, "outer")],
                    {"type": "boundary", "boundary": "administrative", "name": "Beta", "admin_level": "8"})
    # Rule 1: on the shared border, a node and a street along it.
    node(20, 0.5, 1.0, place="suburb", name="On The Shared Border")
    node(21, 0.2, 1.0)
    node(22, 0.8, 1.0)
    ways[200] = ([21, 22], {"highway": "residential", "name": "Border Street"})
    # Rule 2: in the hole.
    node(23, 0.5, 0.5, place="suburb", name="In The Hole")
    node(24, 0.2, 0.2, place="suburb", name="Plainly Inside")
    # Rule 3: no node inside, the line through the interior (in); along the
    # outer edge (out); ending on the edge (out); one node inside (in).
    node(30, 0.3, -0.2)
    node(31, -0.2, 0.3)
    ways[201] = ([30, 31], {"highway": "residential", "name": "Corner Cut"})
    node(32, 0.0, 0.2)
    node(33, 0.0, 0.8)
    ways[202] = ([32, 33], {"highway": "residential", "name": "Edge Road"})
    node(34, 0.5, -0.5)
    node(35, 0.5, 0.0)
    ways[203] = ([34, 35], {"highway": "residential", "name": "Dead End At The Line"})
    node(36, 0.7, 0.1)
    ways[204] = ([34, 36], {"highway": "residential", "name": "Runs In"})
    # Rule 4: relations in by a member node, by a member way, and not in.
    node(40, 0.9, 0.9)
    node(41, 3.0, 3.0)
    node(42, 3.0, 3.5)
    ways[300] = ([41, 42], {})
    relations[10] = ([("w", 300, ""), ("n", 40, "")], {"tourism": "attraction", "name": "In By A Node"})
    relations[11] = ([("w", 201, "")], {"tourism": "attraction", "name": "In By A Way"})
    relations[12] = ([("w", 202, ""), ("n", 35, ""), ("w", 300, "")], {"tourism": "attraction", "name": "Only Touches"})
    # Rule 5: an L, whose bounding-box middle is not its mean or centroid.
    node(50, 0.1000001, 1.2)
    node(51, 0.1000001, 1.8000002)
    node(52, 0.7000005, 1.8000002)
    ways[400] = ([50, 51, 52], {"leisure": "park", "name": "L Park"})
    return nodes, ways, relations


TEST_UNIONS = {
    "streets": ['way["highway"]["name"](area.a)->.w;'],
    "main": ['node["place"]["name"](area.a);',
             'nwr["tourism"~"^(attraction|museum)$"]["name"](area.a);',
             'nwr["leisure"~"^(park|garden)$"]["name"](area.a);'],
}


def cut_world(nodes, ways, relations, side):
    """(nodes, ways, relations) of the part of a test world a regional file
    would hold, cut the way the publisher cuts: the nodes whose longitude
    passes `side`, every way with one of them kept WHOLE (its other nodes
    come along), and every relation with a member on that side."""
    own = {nid for nid, (_, lon, _) in nodes.items() if side(lon)}
    w = {wid: v for wid, v in ways.items() if own & set(v[0])}
    n = {nid: nodes[nid] for nid in own | {r for refs, _ in w.values() for r in refs}}
    r = {rid: v for rid, v in relations.items()
         if any((t == "w" and ref in w) or (t == "n" and ref in own) for t, ref, _ in v[0])}
    return n, w, r


def selftest():
    import os
    import tempfile
    from shapely.geometry import LineString, Point, box
    from shapely.ops import unary_union
    cases = []

    def case(label, ok):
        cases.append((label, bool(ok)))

    # The clauses.
    c = parse_statement('nwr["railway"~"^(station|halt|tram_stop)$"]["name"](area.a);')
    case("a statement is read as its kinds and filters",
         c.kinds == frozenset("nwr") and c.matches({"railway": "halt", "name": "x"})
         and not c.matches({"railway": "halts", "name": "x"}) and not c.matches({"railway": "halt"}))
    c = parse_statement('way["highway"]["name"](area.a)->.w;')
    case("a statement with an output set is read; its kind is kept to ways",
         c.kinds == frozenset("w") and c.matches({"highway": "x", "name": "y"}))
    c = parse_statement('node[!"shop"]["amenity"!="cafe"]["name"!~"^x"](area.a);')
    case("absent-key, not-equal and not-matching filters hold on an absent key",
         c.matches({}) and not c.matches({"shop": "y"}) and not c.matches({"amenity": "cafe"})
         and not c.matches({"name": "xy"}) and c.matches({"name": "ax"}))
    refused = 0
    for bad in ('node["name"](47.0,-122.5,47.1,-122.4);', 'node(w.w);', 'nwr["name"~"a",i](area.a);',
                'node(around:50)["name"](area.a);', 'area["name"="x"]->.a;', 'nwr["name"~"[[:alpha:]]"](area.a);'):
        try:
            parse_statement(bad)
        except ValueError:
            refused += 1
    case("a statement it cannot represent is refused, never skipped", refused == 6)
    unions = {n: parse_union("\n".join(lines)) for n, lines in TEST_UNIONS.items()}
    case("the reader's prefilter is a key every clause requires", prefilter_keys(unions) == ("name",))
    case("clauses with no common key prefilter on one key each; none when a clause requires no key",
         prefilter_keys({"a": parse_union('node["place"](area.a);\nway["highway"="x"](area.a);')})
         == ("highway", "place")
         and prefilter_keys({"a": parse_union('node[!"place"](area.a);')}) is None)
    spec = parse_area("(id:3600000001, 3600000002,2400000007)")
    case("area ids name relations (3.6e9+) and ways (2.4e9+)",
         spec["relations"] == {1, 2} and spec["ways"] == {7})
    spec = parse_area('["name"="京都市"]["admin_level"="7"]')
    case("an area given as tag filters is read", spec["tags"] == [("name", "京都市"), ("admin_level", "7")])
    refused = 0
    for bad in ("(id:12)", '["name"~"x"]', "(47,1,48,2)", ""):
        try:
            parse_area(bad)
        except ValueError:
            refused += 1
    case("an area selector it cannot represent is refused", refused == 4)

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        nodes, ways, relations = test_world()
        pbf = write_test_extract(d / "world-260101.osm.pbf", nodes, ways, relations)
        case("an extract states its own data date", extract_timestamp(pbf) == "2026-01-01T00:00:00Z")
        seen = []
        got = query(pbf, parse_area("(id:3600000001,3600000002)"), unions,
                    on_area=lambda b, a: seen.append(len(b)))
        streets = {e["id"] for e in got["elements"]["streets"]}
        main = {(e["type"], e["id"]) for e in got["elements"]["main"]}
        area = got["area"]
        # What each rule's case would answer were the rule broken: the
        # fixture has to tell the two apart, or the case proves nothing.
        merged = unary_union(area.parts)
        no_holes = unary_union([box(0, 0, 1, 1), box(1, 0, 2, 1)])
        case("rule 1: a node and a street on the border two municipalities share are in neither "
             "(the union of the two would hold both)",
             ("node", 20) not in main and 200 not in streets
             and merged.contains(Point(1.0, 0.5)) and merged.contains(LineString([(1.0, 0.2), (1.0, 0.8)])))
        case("rule 2: a node in a boundary's hole is out (outer rings alone would hold it)",
             ("node", 23) not in main and ("node", 24) in main and no_holes.contains(Point(0.5, 0.5)))
        corner, edge, dead = (LineString([(-0.2, 0.3), (0.3, -0.2)]), LineString([(0.2, 0.0), (0.8, 0.0)]),
                              LineString([(-0.5, 0.5), (0.0, 0.5)]))
        case("rule 3: a way with no node inside whose line crosses the interior is in "
             "(a nodes-only test would drop it)",
             201 in streets and not any(area.points_in([0.3, -0.2], [-0.2, 0.3])))
        case("rule 3: a way along the boundary and a way ending on it are out "
             "(an intersects test would keep both); one node inside is enough",
             202 not in streets and 203 not in streets and 204 in streets
             and merged.intersects(edge) and merged.intersects(dead) and merged.intersects(corner))
        case("rule 4: a relation is in by a member node or a member way, out when its members only touch",
             ("relation", 10) in main and ("relation", 11) in main and ("relation", 12) not in main)
        park = next(e for e in got["elements"]["main"] if e["id"] == 400)
        center = out_tags_center(park)["center"]
        mean_lat = round((0.1000001 + 0.1000001 + 0.7000005) / 3, 7)
        case("rule 5: a center is the middle of the bounding box at 7 decimals, not the mean of the nodes",
             center == {"lat": 0.4000003, "lon": 1.5000001} and mean_lat != center["lat"])
        rel = next(e for e in got["elements"]["main"] if e["id"] == 10)
        # Two of Tbilisi's ways, bounding boxes from the extract and centers
        # as Overpass printed them (2026-10-08): one half printed down, one up.
        case("rule 5: a half in the 8th decimal prints as Overpass prints it (plain rounding misses both)",
             bbox_center([(41.7596702, 44.7745315), (41.7613281, 44.7748637)]) == {"lat": 41.7604991, "lon": 44.7746976}
             and bbox_center([(41.6877292, 44.8594431), (41.6878397, 44.8596297)]) == {"lat": 41.6877845, "lon": 44.8595364}
             and round((41.7596702 + 41.7613281) / 2, 7) != 41.7604991
             and round((41.6877292 + 41.6878397) / 2, 7) != 41.6877845)
        case("a relation's center spans its member ways and member nodes",
             out_tags_center(rel)["center"] == {"lat": 1.95, "lon": 2.2})
        case("the area is handed to the caller before the heavy pass", seen == [2])
        order = [(e["type"], e["id"]) for e in got["elements"]["main"]]
        rank = {"node": 0, "way": 1, "relation": 2}
        case("elements come nodes, ways, relations, each by ascending id",
             order == sorted(order, key=lambda k: (rank[k[0]], k[1])) and len({k[0] for k in order}) == 3)
        again = query(pbf, parse_area("(id:3600000002,3600000001)"), dict(reversed(list(unions.items()))))
        case("the answer does not depend on the order the area or the unions were given in",
             json.dumps(again["elements"], sort_keys=True) == json.dumps(got["elements"], sort_keys=True))
        geom = out_geom(got["boundaries"][0])
        case("a boundary is written as out geom gives it: member geometry and bounds",
             geom["bounds"] == {"minlat": 0.0, "minlon": 0.0, "maxlat": 1.0, "maxlon": 1.0}
             and geom["members"][0]["geometry"][0] == {"lat": 0.0, "lon": 1.0}
             and [m["role"] for m in geom["members"]] == ["outer", "outer", "inner"])
        skel = out_skel_nodes(got["elements"]["streets"])
        case("street nodes come once each, by id, as out skel gives them",
             [n["id"] for n in skel] == [30, 31, 34, 36] and set(skel[0]) == {"type", "id", "lat", "lon"})
        by_tags = query(pbf, parse_area('["name"="Alpha"]["admin_level"="8"]'), unions)
        case("an area named by tags is the relation carrying them",
             [b["id"] for b in by_tags["boundaries"]] == [1]
             and ("node", 24) in {(e["type"], e["id"]) for e in by_tags["elements"]["main"]})
        ways[500] = ([7, 8, 9, 10, 7], {"name": "Closed Way"})
        by_way = query(write_test_extract(d / "way.osm.pbf", nodes, ways, relations),
                       parse_area("(id:2400000500)"), unions)
        case("an area made from a closed way is that way's polygon",
             {(e["type"], e["id"]) for e in by_way["elements"]["main"]} == {("node", 23)}
             and out_geom(by_way["boundaries"][0])["type"] == "way")

        def stopped(fn):
            try:
                fn()
            except SystemExit as exc:
                return str(exc)
            return None
        # Which administrative boundaries hold a point: a county around both
        # municipalities, and a state whose ring the extract holds half of.
        for nid, (lat, lon) in {70: (-1, -1), 71: (2, -1), 72: (2, 3), 73: (-1, 3), 74: (5, -5), 75: (5, 5)}.items():
            nodes[nid] = (lat, lon, {})
        ways[600] = ([70, 71, 72, 73, 70], {})
        ways[601] = ([70, 74, 75, 72], {})
        admin = {"type": "boundary", "boundary": "administrative"}
        relations[3] = ([("w", 600, "outer")], dict(admin, name="County", admin_level="6"))
        relations[4] = ([("w", 601, "outer"), ("w", 999, "outer")], dict(admin, name="State", admin_level="4"))
        relations[5] = ([("w", 600, "outer")], {"type": "boundary", "boundary": "postal_code", "name": "Postal"})
        admin_pbf = write_test_extract(d / "admin.osm.pbf", nodes, ways, relations)

        def holding(*pts):
            got_, stats_ = boundaries_holding(admin_pbf, list(pts))
            return [e["id"] for e in got_], stats_
        ids, stats = holding((0.2, 0.2))
        case("lookup: a point inside two nested levels returns both, tags only, and no other kind of boundary",
             ids == [1, 3] and set(boundaries_holding(admin_pbf, [(0.2, 0.2)])[0][0]) == {"type", "id", "tags"})
        case("lookup: a point in a relation's hole is not in that relation", holding((0.5, 0.5))[0] == [3])
        case("lookup: a point on the border two municipalities share is in neither",
             holding((0.5, 1.0))[0] == [3])
        case("lookup: several points return every relation holding one of them, each once",
             holding((0.2, 0.2), (0.5, 1.5), (0.3, 0.3))[0] == [1, 2, 3])
        case("lookup: a relation the extract holds only part of is not answered and is listed",
             [r["id"] for r in stats["not_whole"]] == [4] and stats["not_whole"][0]["admin_level"] == "4")
        case("lookup: a point outside everything returns nothing", holding((40.0, 40.0))[0] == [])
        del relations[3], relations[4], relations[5]
        why = stopped(lambda: query(pbf, parse_area("(id:3600000099)"), unions))
        case("a boundary the extract does not hold stops the read", why and "not in the extract" in why)
        cut = dict(ways)
        del cut[100]
        why = stopped(lambda: query(write_test_extract(d / "cut.osm.pbf", nodes, cut, relations),
                                    parse_area("(id:3600000001)"), unions))
        case("a boundary cut off at the extract's edge stops the read, naming the larger region",
             why and "next larger region" in why)
        try:
            boundary_polygon([("outer", [(0, 0), (0, 1), (1, 1)])])
            closed = True
        except ValueError:
            closed = False
        case("a ring that does not close is refused", not closed)

        # The region index and the download's conduct, on a stub transport.
        index = {"features": [
            {"properties": {"id": "big", "urls": {"pbf": f"https://{DOWNLOAD_HOST}/big-latest.osm.pbf"}},
             "geometry": {"type": "Polygon", "coordinates": [[[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]]}},
            {"properties": {"id": "x/small", "parent": "big",
                            "urls": {"pbf": f"https://{DOWNLOAD_HOST}/x/small-latest.osm.pbf"}},
             "geometry": {"type": "Polygon", "coordinates": [[[-1, -1], [3, -1], [3, 3], [-1, 3], [-1, -1]]]}},
            {"properties": {"id": "half", "urls": {"pbf": f"https://{DOWNLOAD_HOST}/half-latest.osm.pbf"}},
             "geometry": {"type": "Polygon", "coordinates": [[[-1, -1], [1.5, -1], [1.5, 3], [-1, 3], [-1, -1]]]}},
        ]}
        case("the smallest region covering the whole area is chosen, not one covering part of it",
             smallest_region(index, merged)["properties"]["id"] == "x/small"
             and region_short(smallest_region(index, merged)) == "small"
             and [f["properties"]["id"] for f in regions_covering(index, merged)] == ["x/small", "big"])
        case("a geometry no region covers stops", stopped(lambda: smallest_region(index, box(50, 50, 51, 51))))
        wide = smallest_region(index, box(0, 0, 5, 1))
        case("points spanning two regions fall to a region that has subregions, which a caller can see",
             wide["properties"]["id"] == "big" and has_subregions(index, wide)
             and not has_subregions(index, smallest_region(index, merged)))

        class Body:
            def __init__(self, data):
                self.data, self.pos = data, 0

            def read(self, n):
                chunk = self.data[self.pos:self.pos + n]
                self.pos += len(chunk)
                return chunk

            def close(self):
                pass

        payload = Path(pbf).read_bytes()
        calls = []

        def transport(method, url, headers, latest="small-260105", broken=False):
            calls.append((method, url.rsplit("/", 1)[-1], headers.get("Range")))
            if method == "HEAD":
                return 302, {"Location": f"https://{DOWNLOAD_HOST}/x/{latest}.osm.pbf"}, None
            start = int(headers["Range"][6:-1]) if "Range" in headers else 0
            data = payload[start:len(payload) // 2] if broken else payload[start:]
            return (206 if start else 200), {"Content-Length": str(len(payload) - start)}, Body(data)

        small = region_by_id(index, "x/small")
        root = d / "extracts"
        said = []
        armed = os.environ.pop("HEATMAP_NO_NETWORK", None)
        try:
            now = datetime.datetime(2026, 1, 6, tzinfo=datetime.timezone.utc)
            path = download_extract(small, root, transport=transport, now=now, out=said.append)
            case("the latest name is resolved to its dated file with a HEAD, then one GET",
                 path.name == "small-260105.osm.pbf" and path.read_bytes() == payload
                 and [c[:2] for c in calls] == [("HEAD", "small-latest.osm.pbf"), ("GET", "small-260105.osm.pbf")])
            ledger = _ledger(root)
            case("a download is recorded with its bytes and sha256",
                 len(ledger) == 1 and ledger[0]["bytes"] == len(payload)
                 and ledger[0]["sha256"] == hashlib.sha256(payload).hexdigest())
            calls.clear()
            download_extract(small, root, transport=transport, now=now, out=said.append)
            case("NO REPEAT: the dated file already held is never downloaded again",
                 [c[0] for c in calls] == ["HEAD"])
            calls.clear()
            download_extract(small, root, max_age_days=7, transport=transport, now=now, out=said.append)
            case("a held extract young enough is used with no request at all", calls == [])
            calls.clear()
            download_extract(small, root, dated="260105", transport=transport, now=now, out=said.append)
            case("a dated file named by hand and already held makes no request", calls == [])
            path.rename(path.with_name("moved.bin"))
            calls.clear()
            why = stopped(lambda: download_extract(small, root, transport=transport, now=now, out=said.append))
            case("NO REPEAT: a file downloaded once and since removed is refused by the ledger",
                 why and "never requested twice" in why and [c[0] for c in calls] == ["HEAD"])
            calls.clear()
            newer = download_extract(small, root, now=now, out=said.append,
                                     transport=lambda m, u, h: transport(m, u, h, latest="small-260112"))
            case("a newer dated file is a different file and is downloaded once",
                 newer.name == "small-260112.osm.pbf" and [c[0] for c in calls] == ["HEAD", "GET"])
            why = stopped(lambda: download_extract(
                small, root, out=said.append,
                transport=lambda m, u, h: (302, {"Location": "https://osm-internal.download.geofabrik.de/x.osm.pbf"}, None)))
            case("a redirect to another host is refused, osm-internal included",
                 why and "never another host" in why)
            why = stopped(lambda: fetch("https://osm-internal.download.geofabrik.de/x-latest.osm.pbf", transport=transport))
            why2 = stopped(lambda: fetch(f"http://{DOWNLOAD_HOST}/x-latest.osm.pbf", transport=transport))
            case("only https on the public host is ever requested", why and why2)
            calls.clear()
            half = region_by_id(index, "half")
            why = stopped(lambda: download_extract(half, root, dated="260105", out=said.append,
                                                   transport=lambda m, u, h: transport(m, u, h, broken=True)))
            part = root / "half" / "half-260105.osm.pbf.part"
            kept = part.exists() and part.stat().st_size == len(payload) // 2
            done = download_extract(half, root, dated="260105", transport=transport, out=said.append)
            case("an interrupted download keeps its part and continues it with a Range, asking no byte twice",
                 why and kept and done.read_bytes() == payload and calls[-1][2] == f"bytes={len(payload) // 2}-")
            why = stopped(lambda: download_extract(region_by_id(index, "big"), root, dated="260105",
                                                   max_bytes=10, transport=transport, out=said.append))
            case("a file over the size limit is refused before its body is read",
                 why and "byte limit" in why and not (root / "big" / "big-260105.osm.pbf").exists())
            # Two runs wanting one file: the lock, then the held file.
            both = region_by_id(index, "big")
            lock_file = root / LOCK_NAME
            lock_file.write_text("4242", encoding="utf-8")
            calls.clear()

            def first_finishes(seconds):
                (root / "big").mkdir(exist_ok=True)
                (root / "big" / "big-260105.osm.pbf").write_bytes(payload)
                lock_file.unlink()
            waited = download_extract(both, root, dated="260105", transport=transport, out=said.append,
                                      lock=DownloadLock(root, alive=lambda pid: True, sleep=first_finishes))
            case("ONE DOWNLOAD AT A TIME: a second run waits for the first, then finds its file and asks nothing",
                 waited.name == "big-260105.osm.pbf" and calls == [] and not lock_file.exists())
            lock_file.write_text("4242", encoding="utf-8")
            why = stopped(lambda: download_extract(
                both, root, dated="260106", transport=transport, out=said.append,
                lock=DownloadLock(root, wait_s=10, alive=lambda pid: True, sleep=lambda s: None)))
            case("a lock still held after the wait stops the run, naming the holder",
                 why and "pid 4242" in why and calls == [])
            got_file = download_extract(both, root, dated="260106", transport=transport, out=said.append,
                                        lock=DownloadLock(root, alive=lambda pid: False))
            case("a lock whose process is gone is replaced, and released after the download",
                 got_file.exists() and not lock_file.exists())
            os.environ["HEATMAP_NO_NETWORK"] = "1"
            calls.clear()
            try:
                import pipeline.offline  # noqa: F401
                have_guard = True
            except ImportError:
                have_guard = False
            why = stopped(lambda: fetch(f"https://{DOWNLOAD_HOST}/x/small-latest.osm.pbf", method="HEAD",
                                        transport=transport))
            case("with the offline switch set no request is made",
                 (why and "HEATMAP_NO_NETWORK" in why and calls == []) or not have_guard)
        finally:
            os.environ.pop("HEATMAP_NO_NETWORK", None)
            if armed is not None:
                os.environ["HEATMAP_NO_NETWORK"] = armed
        # SEVERAL REGIONS AS ONE. The test world cut at lon = 1 the way the
        # publisher cuts: each side's nodes, every way with a node on its
        # side kept whole, every relation with a member on its side. A
        # street, a tagged node on it and a relation of it cross the cut.
        nodes, ways, relations = test_world()
        nodes[80] = (0.5, 0.9, {"place": "suburb", "name": "On A Crossing Way"})
        nodes[81] = (0.5, 1.1, {})
        ways[205] = ([80, 81], {"highway": "residential", "name": "Crosses The Cut"})
        relations[13] = ([("w", 205, "")], {"tourism": "attraction", "name": "Crossing Relation"})

        west = cut_world(nodes, ways, relations, lambda lon: lon < 1.0)
        east = cut_world(nodes, ways, relations, lambda lon: lon >= 1.0)
        whole_pbf = write_test_extract(d / "whole-260101.osm.pbf", nodes, ways, relations)
        west_pbf = write_test_extract(d / "west-260101.osm.pbf", *west)
        east_pbf = write_test_extract(d / "east-260101.osm.pbf", *east)
        both_areas = parse_area("(id:3600000001,3600000002)")
        one = query(whole_pbf, both_areas, unions)
        notes = []
        two = query([west_pbf, east_pbf], both_areas, unions, say=notes.append)
        flipped = query(ExtractSet([east_pbf, west_pbf]), both_areas, unions)

        def answer(got_):
            return json.dumps([got_["elements"], [out_geom(b) for b in got_["boundaries"]]], sort_keys=True)
        once_each = two["stats"].get("taken_once", {})
        case("two files read as one answer what the whole file answers, in either order, each id once",
             answer(two) == answer(one) == answer(flipped)
             and [e["id"] for e in two["elements"]["streets"]].count(205) == 1
             and "files" not in one["stats"] and two["stats"]["files"] == [west_pbf.name, east_pbf.name])
        case("an object held by both files is counted as taken once, per kind",
             once_each.get("way", 0) >= 1 and once_each.get("node", 0) >= 1 and once_each.get("relation", 0) >= 1
             and once_each.get("member way", 0) >= 1 and any("taken once" in n for n in notes))
        case("a boundary whose member ways are split across two files closes from both; neither file "
             "alone holds it",
             103 in west[1] and 103 not in east[1] and 101 in east[1] and 101 not in west[1]
             and "next larger region" in (stopped(lambda: query(west_pbf, parse_area("(id:3600000001)"), unions)) or "")
             and "next larger region" in (stopped(lambda: query(east_pbf, parse_area("(id:3600000001)"), unions)) or "")
             and [b["id"] for b in two["boundaries"]] == [1, 2])
        changed = dict(east[1])
        changed[205] = (changed[205][0], dict(changed[205][1], name="Crosses The Cut, Renamed"))
        why = stopped(lambda: query([west_pbf, write_test_extract(d / "east2-260101.osm.pbf", east[0], changed, east[2])],
                                    both_areas, unions))
        case("two copies of one object that differ stop the read, naming the object and both files: "
             "neither is taken on a guess",
             why and "different content" in why and "way 205" in why and "west-260101.osm.pbf" in why
             and "east2-260101.osm.pbf" in why)
        short_nodes = {nid: v for nid, v in east[0].items() if nid != 80}
        east3 = write_test_extract(d / "east3-260101.osm.pbf", short_nodes, east[1], east[2])
        case("a copy holding fewer of its nodes is not a differing copy: the fuller one is taken, in either order",
             answer(query([west_pbf, east3], both_areas, unions)) == answer(one)
             and answer(query([east3, west_pbf], both_areas, unions)) == answer(one))
        late_pbf = write_test_extract(d / "east-260102.osm.pbf", *east, timestamp="2026-01-02T00:00:00Z")
        why = stopped(lambda: set_timestamp([west_pbf, late_pbf]))
        case("a set whose files state different data timestamps is refused; one snapshot gives its date",
             why and "not one snapshot" in why and "86,400 s apart" in why
             and set_timestamp([west_pbf, east_pbf]) == "2026-01-01T00:00:00Z"
             and set_timestamp(west_pbf) == "2026-01-01T00:00:00Z")
        held_set = ExtractSet([west_pbf, east_pbf])
        case("a set answers for its files where one path is asked: a name, existence, Path(x).name",
             held_set.name == "west-260101.osm.pbf + east-260101.osm.pbf" == Path(held_set).name
             and held_set.exists() and not ExtractSet([west_pbf, d / "absent.osm.pbf"]).exists()
             and one_or_set([west_pbf]) == west_pbf and isinstance(one_or_set([west_pbf, east_pbf]), ExtractSet))
        found_two, stats_two = boundaries_holding([west_pbf, east_pbf], [(0.2, 0.2), (0.5, 1.5)])
        found_west, stats_west = boundaries_holding(west_pbf, [(0.2, 0.2), (0.5, 1.5)])
        case("lookup: a relation cut at one file's edge is whole across the set",
             [e["id"] for e in found_two] == [1, 2] and stats_two["not_whole"] == []
             and found_west == [] and [r["id"] for r in stats_west["not_whole"]] == [1])

        # Which regions: one when one will do, else the smallest set.
        def strip(rid, x0, x1):
            return {"properties": {"id": rid, "urls": {"pbf": f"https://{DOWNLOAD_HOST}/{rid}-latest.osm.pbf"}},
                    "geometry": {"type": "Polygon",
                                 "coordinates": [[[x0, -10], [x1, -10], [x1, 10], [x0, 10], [x0, -10]]]}}
        country = {"features": [strip("country", -10, 10), strip("country/west", -10, 1.2),
                                strip("country/east", 1.2, 10), strip("country/east-wide", 1.1, 10)]}
        mbytes = 2 ** 20
        weigh = {"country": 2000, "country/west": 300, "country/east": 200, "country/east-wide": 250}
        asked = []

        def size_of(feature, table=weigh):
            asked.append(feature["properties"]["id"])
            return table[feature["properties"]["id"]] * mbytes

        def chosen(geom, cap=1000, table=weigh, idx=country):
            got_, why_ = choose_regions(idx, geom, lambda f: size_of(f, table), max_bytes=cap * mbytes)
            return [f["properties"]["id"] for f in got_], why_
        case("set choice: an area inside one region takes that region, and no size is asked",
             chosen(box(0, 0, 1, 1)) == (["country/west"], None) and asked == [])
        case("set choice: an area crossing a border still takes the one covering region when it is under the cap",
             chosen(merged, cap=3000) == (["country"], None) and asked == ["country"])
        ids, why = chosen(merged)
        case("set choice: with the covering region over the cap, the smallest set by bytes is taken and said",
             ids == ["country/east", "country/west"] and "country, is 2,000 MB" in why
             and "country/east (200 MB) + country/west (300 MB), 500 MB in all" in why)
        why = stopped(lambda: chosen(merged, table=dict(weigh, **{"country/west": 1500})))
        case("set choice: no set under the cap is refused, naming the file that is over it",
             why and "country/west (1,500 MB)" in why and "over the 1,000 MB cap" in why)
        strips = {"features": [strip("country", -10, 10)] + [strip(f"s{i}", i, i + 1) for i in range(5)]}
        why = stopped(lambda: chosen(box(0.5, 0, 4.5, 1), idx=strips,
                                     table=dict({f"s{i}": 10 for i in range(5)}, country=2000)))
        four, _ = chosen(box(0.5, 0, 3.5, 1), idx=strips, table=dict({f"s{i}": 10 for i in range(5)}, country=2000))
        case("set choice: four regions are taken, more than four are refused",
             four == ["s0", "s1", "s2", "s3"] and why and "More than 4 regions" in why)
        case("set choice: a geometry no region meets is refused",
             "no set of them does" in (stopped(lambda: chosen(box(50, 50, 51, 51))) or ""))

        # The set's files: each through download_extract, all of one date.
        blobs = {"west": west_pbf.read_bytes(), "east": east_pbf.read_bytes()}
        set_calls = []

        def set_transport(method, url, headers, latest="260106"):
            name = url.rsplit("/", 1)[-1]
            set_calls.append((method, name))
            if method == "HEAD" and "-latest" in name:
                return 302, {"Location": url.replace("-latest", f"-{latest}")}, None
            data = blobs[name.split("-")[0]]
            return 200, {"Content-Length": str(len(data))}, (Body(data) if method == "GET" else None)

        pair = [region_by_id(country, "country/west"), region_by_id(country, "country/east")]
        day = datetime.datetime(2026, 1, 3, tzinfo=datetime.timezone.utc)
        armed = os.environ.pop("HEATMAP_NO_NETWORK", None)
        try:
            root2 = d / "set"
            got_set = download_set(pair, root2, max_age_days=7, transport=set_transport, now=day, out=said.append)
            gets = [c for c in set_calls if c[0] == "GET"]
            case("a set is downloaded one file at a time, each dated and each in the ledger",
                 got_set.name == "west-260106.osm.pbf + east-260106.osm.pbf" and got_set.exists()
                 and gets == [("GET", "west-260106.osm.pbf"), ("GET", "east-260106.osm.pbf")]
                 and [row["file"] for row in _ledger(root2)] == ["west-260106.osm.pbf", "east-260106.osm.pbf"]
                 and extract_size(pair[0], root2, max_age_days=7, now=day)["held"])
            set_calls.clear()
            download_set(pair, root2, max_age_days=7, transport=set_transport, now=day, out=said.append)
            case("a set already held makes no request", set_calls == [])
            (root2 / "east" / "east-260106.osm.pbf").rename(root2 / "east" / "moved.bin")
            why = stopped(lambda: download_set(pair, root2, max_age_days=7, transport=set_transport, now=day,
                                               out=said.append))
            case("a set file in the ledger and no longer on disk is refused: never the same file twice",
                 why and "never requested twice" in why)
            root3 = d / "set3"
            (root3 / "west").mkdir(parents=True)
            (root3 / "west" / "west-260105.osm.pbf").write_bytes(blobs["west"])
            set_calls.clear()
            aligned = download_set(pair, root3, max_age_days=7, transport=set_transport, now=day, out=said.append)
            case("a set with one file held is completed AT THAT FILE'S DATE, not the latest: one snapshot, "
                 "the fewest downloads",
                 aligned.name == "west-260105.osm.pbf + east-260105.osm.pbf"
                 and [c for c in set_calls if c[0] == "GET"] == [("GET", "east-260105.osm.pbf")])
            why = stopped(lambda: download_set(pair, d / "set4", max_bytes=10, transport=set_transport, now=day,
                                               out=said.append))
            case("the size cap holds for each file of a set", why and "byte limit" in why)
            blobs["east"] = late_pbf.read_bytes()
            why = stopped(lambda: download_set(pair, d / "set5", transport=set_transport, now=day, out=said.append))
            case("a downloaded set that is not one snapshot is refused", why and "not one snapshot" in why)
        finally:
            if armed is not None:
                os.environ["HEATMAP_NO_NETWORK"] = armed
        case("an age is counted from the extract's own date",
             abs(age_days("2026-01-01T00:00:00Z", datetime.datetime(2026, 1, 9, tzinfo=datetime.timezone.utc)) - 8) < 1e-9
             and age_days("not a date") is None)

    for label, ok in cases:
        print(f"  {'ok ' if ok else 'BAD'} {label}")
    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", choices=("index", "region", "download"))
    ap.add_argument("args", nargs="*")
    ap.add_argument("--root", default=str(Path(__file__).parent.parent / "data" / "_osm_extracts"),
                    help="where extracts, the index and the download ledger are kept")
    ap.add_argument("--dated", metavar="YYMMDD", help="download this dated file instead of the latest")
    ap.add_argument("--max-mb", type=int, default=800, help="refuse a larger file (default 800)")
    args = ap.parse_args(argv)
    root = Path(args.root)
    index = load_index(root / "index-v1.json")
    if args.command == "index":
        print(f"{len(index['features'])} regions in {root / 'index-v1.json'}")
    elif args.command == "region":
        from shapely.geometry import MultiPoint
        values = [float(a) for a in args.args]
        if not values or len(values) % 2:
            raise SystemExit("region takes LAT LON pairs")
        geom = MultiPoint([(values[i + 1], values[i]) for i in range(0, len(values), 2)])
        for f in regions_covering(index, geom):
            print(f["properties"]["id"], f["properties"]["urls"]["pbf"])
    else:
        if len(args.args) != 1:
            raise SystemExit("download takes one REGION_ID (the index's id, such as us/washington)")
        path = download_extract(region_by_id(index, args.args[0]), root, dated=args.dated,
                                max_bytes=args.max_mb * 1024 * 1024)
        print(path, extract_timestamp(path))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
