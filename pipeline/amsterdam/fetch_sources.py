"""Download Amsterdam's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/amsterdam/fetch_sources.py [--force]

Every source is keyless today. A cached file is kept and recorded, never
silently refreshed - `--force` re-downloads.

Unlike a file-drop city, most of Amsterdam comes from a paged API, so each
layer is saved as ONE JSON list of the API's own records, exactly as served.
Three of the five API reads are derived from earlier ones - the shop units'
addresses and streets, and the permits that carry no point - so they are
fetched here, where fetching belongs, and step 2 only joins.
"""
import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.amsterdam import addresses, config  # noqa: E402

UA = "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"


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


def _get_json(url, params=None, tries=4):
    full = url + ("?" + urllib.parse.urlencode(params) if params else "")
    for attempt in range(tries):
        try:
            req = urllib.request.Request(full, headers={"Accept": "*/*", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001 - every failure is retried, then raised
            if attempt == tries - 1:
                raise SystemExit(f"  {full}: {type(e).__name__}: {e}")
            time.sleep(5 * (attempt + 1))


def api_list(url, params=None):
    """Every record of a DSO API listing, following _links.next."""
    params = dict(params or {}, _pageSize=config.API_PAGE_SIZE)
    out, page = [], _get_json(url, params)
    while True:
        for v in page.get("_embedded", {}).values():
            out.extend(v)
        nxt = page.get("_links", {}).get("next", {}).get("href")
        if not nxt:
            return out
        page = _get_json(nxt)


def api_in(url, ids, field="identificatie"):
    """Records whose `field` is in `ids`, in batches of the [in] filter."""
    ids, out = sorted(set(ids)), []
    for i in range(0, len(ids), config.BAG_IN_BATCH):
        chunk = ids[i:i + config.BAG_IN_BATCH]
        out.extend(api_list(url, {f"{field}[in]": ",".join(chunk)}))
    return out


def save_list(path, records, url, prov, key, force, fetch):
    if path.exists() and not force:
        n = len(json.loads(path.read_text(encoding="utf-8")))
        print(f"  {path.name:44s} cached ({n:,} records)")
        old = prov.get(key, {})
        if old.get("sha256") != _sha256(path):
            _record(prov, key, path, url, old.get("retrieved") or "cached before provenance",
                    records=n)
        return json.loads(path.read_text(encoding="utf-8"))
    records = fetch()
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    _record(prov, key, path, url, _now(), records=len(records))
    print(f"  {path.name:44s} {len(records):,} records, {path.stat().st_size:,} bytes")
    return records


def permit_lookup(permits):
    """BAG streets, addresses and units for the permits that carry no point,
    so step 2 can place them by address rather than drop them.

    By STREET NAME and number, not postcode: the 136 permits without a point
    carry no postcode either (measured 2026-09-24)."""
    want = {}
    for p in permits:
        if (p.get("locatie") or {}).get("coordinates"):
            continue
        parsed = addresses.parse(p.get("adres"))
        if parsed:
            want.setdefault(parsed[0], set()).add(parsed[1])
    streets, addrs = [], []
    for name in sorted(want):
        found = api_list(config.BAG_STREETS_URL, {"naam": name})
        streets.extend(found)
        for s in found:
            for num in sorted(want[name]):
                addrs.extend(api_list(config.BAG_ADDRESSES_URL,
                                      {"ligtAanOpenbareruimte.identificatie": s["identificatie"],
                                       "huisnummer": num}))
    unit_ids = [a["adresseertVerblijfsobjectId"] for a in addrs if a.get("adresseertVerblijfsobjectId")]
    units = api_in(config.BAG_UNITS_URL, unit_ids)
    print(f"    {sum(len(v) for v in want.values())} (street, number) pairs asked; "
          f"{len(streets)} streets, {len(addrs)} addresses, {len(units)} units found")
    return {"streets": streets, "addresses": addrs, "units": units}


def feed_window(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        head, row = z.read("feed_info.txt").decode("utf-8-sig").splitlines()[:2]
    info = dict(zip(head.split(","), row.split(",")))
    start, end = info.get("feed_start_date", ""), info.get("feed_end_date", "")
    end_date = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    print(f"  GTFS feed window {start} to {end} "
          f"({(end_date - date.today()).days:+d} days from today)")
    if end_date < date.today():
        sys.exit("  the national feed has expired - re-run with --force for the current one")
    return {"feed_start_date": start, "feed_end_date": end,
            "publisher": info.get("feed_publisher_name"), "version": info.get("feed_version")}


def fetch_gtfs(prov, force):
    dest = config.GTFS_ZIP
    if dest.exists() and not force:
        print(f"  {dest.name:44s} cached ({dest.stat().st_size:,} bytes)")
        old = prov.get("gtfs", {})
        if old.get("sha256") != _sha256(dest):
            _record(prov, "gtfs", dest, config.GTFS_URL,
                    old.get("retrieved") or "cached before provenance")
        return
    tmp = dest.with_suffix(".zip.part")
    # OVapi's usage policy asks every client to identify itself in the
    # User-Agent and to accept gzip; a zip is served as-is, but a gzipped
    # response is unwrapped here rather than saved compressed.
    req = urllib.request.Request(config.GTFS_URL, headers={"User-Agent": UA,
                                                            "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=3600) as r, open(tmp, "wb") as fh:
        src = r
        if (r.headers.get("Content-Encoding") or "").lower() == "gzip":
            import gzip
            src = gzip.GzipFile(fileobj=r)
        while chunk := src.read(1 << 22):
            fh.write(chunk)
    if tmp.read_bytes()[:4] != b"PK\x03\x04":
        tmp.unlink()
        sys.exit("  gtfs-nl.zip: not a zip - not the file asked for")
    tmp.replace(dest)
    _record(prov, "gtfs", dest, config.GTFS_URL, _now())
    print(f"  {dest.name:44s} {dest.stat().st_size:,} bytes downloaded")


def fetch_osm(force):
    s, w, n, e = 52.25, 4.70, 52.45, 5.10
    els, host = osm.fetch(f"[out:json][timeout:180];rel({config.OSM_BOUNDARY_RELATION});out geom;",
                          config.OSM_BOUNDARY_JSON, force=force)
    print(f"  {'osm_boundary':44s} {len(els)} relation via {host}")
    rail = ('[out:json][timeout:180];'
            f'(relation["type"="route"]["route"~"^(subway|tram)$"]["network"="Stadsvervoer Amsterdam"]({s},{w},{n},{e}););'
            'out tags;node(r);out tags center;')
    els, host = osm.fetch(rail, config.OSM_RAIL_JSON, force=force)
    rels = sum(1 for x in els if x["type"] == "relation")
    print(f"  {'osm_rail (cross-check)':44s} {rels} route relations via {host}")
    # The neighbouring gemeenten, only to NAME the stations step 1 excludes -
    # a naming layer, not a scoping one (Oslo and Rennes do the same).
    s2, w2, n2, e2 = 52.18, 4.70, 52.47, 5.15
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

    print("The city's API:")
    permits = save_list(config.PERMITS_JSON, None, config.PERMITS_URL, prov, "permits",
                        args.force, lambda: api_list(config.PERMITS_URL))
    units = save_list(config.BAG_UNITS_JSON, None,
                      config.BAG_UNITS_URL + "?" + urllib.parse.urlencode(config.BAG_UNITS_FILTER),
                      prov, "bag_units", args.force,
                      lambda: api_list(config.BAG_UNITS_URL, config.BAG_UNITS_FILTER))
    in_use = [u for u in units if u.get("statusOmschrijving") == config.BAG_STATUS_KEEP]
    addrs = save_list(config.BAG_ADDRESSES_JSON, None, config.BAG_ADDRESSES_URL, prov,
                      "bag_addresses", args.force,
                      lambda: api_in(config.BAG_ADDRESSES_URL,
                                     [u["heeftHoofdadresId"] for u in in_use if u.get("heeftHoofdadresId")]))
    save_list(config.BAG_STREETS_JSON, None, config.BAG_STREETS_URL, prov, "bag_streets",
              args.force,
              lambda: api_in(config.BAG_STREETS_URL,
                             [a["ligtAanOpenbareruimteId"] for a in addrs if a.get("ligtAanOpenbareruimteId")]))
    if not config.BAG_PERMIT_LOOKUP_JSON.exists() or args.force:
        lookup = permit_lookup(permits)
        config.BAG_PERMIT_LOOKUP_JSON.write_text(json.dumps(lookup, ensure_ascii=False),
                                                 encoding="utf-8")
        _record(prov, "bag_permit_lookup", config.BAG_PERMIT_LOOKUP_JSON,
                config.BAG_ADDRESSES_URL, _now(), records=len(lookup["addresses"]))
        print(f"  {config.BAG_PERMIT_LOOKUP_JSON.name:44s} {len(lookup['addresses'])} addresses, "
              f"{len(lookup['units'])} units for the permits with no point")
    else:
        print(f"  {config.BAG_PERMIT_LOOKUP_JSON.name:44s} cached")
    # The permits are a live register - the snapshot IS the retrieval date.
    prov["permits_snapshot"] = prov["permits"]["retrieved"][:10]

    print("\nRail:")
    fetch_gtfs(prov, args.force)
    prov["gtfs_feed_info"] = feed_window(config.GTFS_ZIP)
    prov["osm_host"] = fetch_osm(args.force)

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")
