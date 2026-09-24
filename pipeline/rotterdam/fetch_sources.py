"""Download Rotterdam's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/rotterdam/fetch_sources.py [--force]

Every source is keyless. A cached file is kept and recorded, never silently
refreshed - `--force` re-downloads. The notices and the BAG are saved as ONE
JSON list each, of the fields each record carries as served.
"""
import argparse
import hashlib
import json
import shutil
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.rotterdam import config  # noqa: E402

UA = "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"
PAUSE_S = 1.0          # between SRU pages - KOOP's fair-use limits are unpublished


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _record(prov, key, path, url, fetched, **extra):
    prov[key] = {"file": path.name, "url": url, "bytes": path.stat().st_size,
                 "sha256": _sha256(path), "retrieved": fetched, **extra}


def _get(url, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001 - every failure is retried, then raised
            if attempt == tries - 1:
                raise SystemExit(f"  {url[:120]}...: {type(e).__name__}: {e}")
            time.sleep(10 * (attempt + 1))


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _notice(rec):
    """The fields one SRU record carries, flattened: owms core and mantle, the
    location, and the enriched URLs (which is where a /noindex/ path shows)."""
    out = {}
    for el in rec.iter():
        name, text = _local(el.tag), (el.text or "").strip()
        if not text:
            continue
        if name in ("identifier", "title", "type", "creator", "modified", "available", "date",
                    "abstract", "subject", "publicatienummer", "jaargang", "geometrie",
                    "locatiepunt", "ligtInGemeente", "url", "preferredUrl"):
            out.setdefault(name, text)
        elif name == "itemUrl":
            out.setdefault("item_urls", []).append(text)
    return out


def harvest_notices():
    """Every notice matching config.SRU_QUERY, year by year (a query stops at
    10,000 records), each year paged and its count checked against the
    server's own numberOfRecords."""
    out = []
    for year in range(config.SRU_FIRST_YEAR, date.today().year + 1):
        q = f"{config.SRU_QUERY} AND dt.date>={year}-01-01 AND dt.date<={year}-12-31"
        got, total, start = [], None, 1
        while total is None or start <= total:
            url = (f"{config.SRU_URL}?operation=searchRetrieve&version=2.0"
                   f"&maximumRecords={config.SRU_PAGE}&startRecord={start}&query="
                   + urllib.parse.quote(q))
            root = ET.fromstring(_get(url))
            n = next((e.text for e in root.iter() if _local(e.tag) == "numberOfRecords"), None)
            if n is None:
                sys.exit(f"  {year}: no numberOfRecords - an SRU diagnostic, not a result")
            total = int(n)
            page = [_notice(r) for r in root.iter() if _local(r.tag) == "recordData"]
            got.extend(page)
            if not page:
                break
            start += len(page)
            time.sleep(PAUSE_S)
        if len(got) != total:
            sys.exit(f"  {year}: {len(got)} records read against {total} reported")
        print(f"    {year}: {total:,} notices")
        out.extend(got)
    ids = [r.get("identifier") for r in out]
    if len(set(ids)) != len(ids):
        sys.exit("  duplicate notice identifiers across years - the year split overlaps")
    return out


def harvest_bag():
    """PDOK's shop-class units in use in gemeente 0599, paged with startIndex."""
    out, start = [], 0
    while True:
        params = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
                  "typeName": "bag:verblijfsobject", "outputFormat": "application/json",
                  "srsName": "EPSG:4326", "count": str(config.BAG_WFS_PAGE),
                  "startIndex": str(start), "sortBy": "identificatie",
                  "FILTER": config.BAG_WFS_FILTER}
        page = json.loads(_get(config.BAG_WFS_URL + "?" + urllib.parse.urlencode(params)))
        feats = page.get("features") or []
        out.extend(feats)
        if len(feats) < config.BAG_WFS_PAGE:
            break
        start += len(feats)
        time.sleep(PAUSE_S)
    ids = [f["properties"]["identificatie"] for f in out]
    if len(set(ids)) != len(ids):
        sys.exit("  duplicate BAG identifiers across pages - the paging is not stable")
    return out


def save_list(path, url, prov, key, force, fetch):
    if path.exists() and not force:
        recs = json.loads(path.read_text(encoding="utf-8"))
        print(f"  {path.name:44s} cached ({len(recs):,} records)")
        old = prov.get(key, {})
        if old.get("sha256") != _sha256(path):
            _record(prov, key, path, url, old.get("retrieved") or "cached before provenance",
                    records=len(recs))
        return recs
    recs = fetch()
    path.write_text(json.dumps(recs, ensure_ascii=False), encoding="utf-8")
    _record(prov, key, path, url, _now(), records=len(recs))
    print(f"  {path.name:44s} {len(recs):,} records, {path.stat().st_size:,} bytes")
    return recs


def copy_gtfs(prov, force):
    """The national feed from Amsterdam's cache - the same file, copied, never
    downloaded twice. Its provenance is carried over and marked as a copy."""
    dest, src = config.GTFS_ZIP, config.GTFS_SHARED_CACHE
    if dest.exists() and not force:
        print(f"  {dest.name:44s} cached ({dest.stat().st_size:,} bytes)")
    else:
        if not src.exists():
            sys.exit(f"  no national feed at {src} - run pipeline/amsterdam/fetch_sources.py first")
        shutil.copyfile(src, dest)
        print(f"  {dest.name:44s} {dest.stat().st_size:,} bytes, copied from Amsterdam's cache")
    ams = json.loads((config.ROOT / "outputs" / "amsterdam" / "provenance.json")
                     .read_text(encoding="utf-8")).get("gtfs", {})
    if ams.get("sha256") != _sha256(dest):
        sys.exit("  the copy does not match Amsterdam's recorded feed - re-copy with --force")
    prov["gtfs"] = {**ams, "file": dest.name, "copied_from": "data/amsterdam/raw/gtfs-openov-nl.zip"}
    with zipfile.ZipFile(dest) as z:
        head, row = z.read("feed_info.txt").decode("utf-8-sig").splitlines()[:2]
    info = dict(zip(head.split(","), row.split(",")))
    end = info.get("feed_end_date", "")
    if date(int(end[:4]), int(end[4:6]), int(end[6:8])) < date.today():
        sys.exit("  the national feed has expired - refresh Amsterdam's, then re-copy with --force")
    prov["gtfs_feed_info"] = {"feed_start_date": info.get("feed_start_date"), "feed_end_date": end,
                              "publisher": info.get("feed_publisher_name"),
                              "version": info.get("feed_version")}
    print(f"  GTFS feed window {info.get('feed_start_date')} to {end}")


def fetch_osm(force):
    s, w, n, e = config.BOUNDARY_BBOX
    q = (f'[out:json][timeout:180];rel["boundary"="administrative"]["admin_level"="8"]'
         f'["ref:gemeentecode"="{config.GEMEENTE_CODE}"]({s},{w},{n},{e});out geom;')
    els, host = osm.fetch(q, config.OSM_BOUNDARY_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if len(rels) != 1:
        sys.exit(f"  gemeente {config.GEMEENTE_CODE}: {len(rels)} relations in the bbox, expected 1")
    print(f"  {'osm_boundary':44s} relation {rels[0]['id']} via {host}")
    s2, w2, n2, e2 = config.NEIGHBOURS_BBOX
    nb = (f'[out:json][timeout:180];rel["boundary"="administrative"]["admin_level"="8"]'
          f'["ref:gemeentecode"]({s2},{w2},{n2},{e2});out geom;')
    els, host2 = osm.fetch(nb, config.OSM_NEIGHBOURS_JSON, force=force)
    print(f"  {'osm_neighbours (naming only)':44s} {len(els)} gemeente relations via {host2}")
    return host


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
            if config.PROVENANCE_JSON.exists() else {})

    print("KOOP official publications (permit notices):")
    save_list(config.NOTICES_JSON, config.SRU_URL + "?query=" + urllib.parse.quote(config.SRU_QUERY),
              prov, "notices", args.force, harvest_notices)
    print("\nPDOK BAG (shop-class units in use):")
    save_list(config.BAG_UNITS_JSON, config.BAG_WFS_URL, prov, "bag_units", args.force, harvest_bag)
    print("\nRail and boundaries:")
    copy_gtfs(prov, args.force)
    prov["osm_host"] = fetch_osm(args.force)

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")
