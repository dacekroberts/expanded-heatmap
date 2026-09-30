"""Downloads for a French tram city - the fetch half of the France batch's
shared tram module (`france_tram.py` is the step half, and never fetches).

A city's `fetch_sources.py` is `fetch_all(config)` and nothing else.

    python pipeline/<city>/fetch_sources.py [--skip-parquet] [--force-osm]

WHAT IT DOES DIFFERENTLY FROM RENNES'S FETCH, and why:

  * **The feed is ALWAYS downloaded.** French tram feeds are rolling (four to
    twelve weeks ahead; owner, 2026-09-29: never cache one across weeks), and
    the 2026-09-27 screen left old copies in `data/<slug>/raw/gtfs.zip` for
    most batch cities. Rennes's fetch skips a cached zip; this one never does.
  * **The data's date is recorded either way.** When the zip's own
    `feed_info.txt` carries a `feed_end_date` the page quotes the operator's
    window; otherwise the NAP's metadata about the resource (`updated`,
    `start_date`, `end_date`), Paris's and Toulouse's pattern. Licence Ouverte
    requires the date of last update on the page, so neither path may be
    skipped.
  * **OpenStreetMap geometry** for a city whose feed has no usable shapes
    (`config.LINE_GEOMETRY == "osm"`): one Overpass query per city, cached,
    one query in flight (the owner's Overpass rule, 2026-09-30).
"""
import argparse
import csv
import io
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone

from pipeline.countries import france

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _get(url, timeout=900):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _stream(url, dest, label, timeout=1800):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        tmp = dest.with_suffix(dest.suffix + ".part")
        done = 0
        with open(tmp, "wb") as fh:
            while True:
                chunk = r.read(1 << 22)
                if not chunk:
                    break
                fh.write(chunk)
                done += len(chunk)
    tmp.replace(dest)
    print(f"  {label:20s} {done:13,} bytes")


def fetch_gtfs(cfg):
    body = _get(cfg.GTFS_URL)
    if body[:4] != b"PK\x03\x04":
        sys.exit(f"  the feed is not a zip - first bytes {body[:8]!r}")
    cfg.GTFS_ZIP.write_bytes(body)
    print(f"  {'gtfs.zip':20s} {len(body):13,} bytes (always fetched: the feed rolls)")
    return body


def feed_info(body):
    """The zip's own validity window, or None when it declares none."""
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        if "feed_info.txt" not in z.namelist():
            return None
        with z.open("feed_info.txt") as fh:
            row = next(csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")), {})
    keep = {k: (v or "").strip() for k, v in row.items()
            if k in ("feed_publisher_name", "feed_start_date", "feed_end_date",
                     "feed_version")}
    return keep if keep.get("feed_end_date") else None


def nap_metadata(cfg):
    """The NAP's record of this resource: when it was updated, the window the
    NAP's validator read from it, and the dataset's declared licence."""
    meta = json.loads(_get(f"https://transport.data.gouv.fr/api/datasets/{cfg.GTFS_NAP_ID}"))
    if meta.get("licence") != cfg.GTFS_LICENCE:
        sys.exit(f"  the NAP now declares {meta.get('licence')!r}, not "
                 f"{cfg.GTFS_LICENCE!r}: a licence change is a new read, not a config edit")
    for r in meta.get("resources", []):
        if r.get("url") == cfg.GTFS_URL:
            md = r.get("metadata") or {}
            return {"dataset": meta.get("title"), "dataset_updated": meta.get("updated"),
                    "resource_updated": r.get("updated"),
                    "start_date": md.get("start_date"), "end_date": md.get("end_date"),
                    "licence": meta.get("licence")}
    sys.exit(f"  the NAP dataset {cfg.GTFS_NAP_ID} no longer lists {cfg.GTFS_URL}")


def fetch_polygon(url, dest, label):
    body = _get(url)
    obj = json.loads(body)
    feats = obj.get("features") or [obj]
    kinds = {(f.get("geometry") or {}).get("type") for f in feats}
    if not kinds <= {"Polygon", "MultiPolygon"}:
        sys.exit(f"  {label} holds {sorted(map(str, kinds))}, not polygons - "
                 f"check the URL says geometry=contour, never fields=contour")
    dest.write_bytes(body)
    print(f"  {label:20s} {len(body):13,} bytes  ({len(feats)} feature(s))")
    return obj


def fetch_epci_communes(cfg, force):
    """Every commune of the city's EPCI(s), merged into one FeatureCollection.
    It must hold the core commune - a wrong EPCI code answers 200 with some
    other intercommunality's communes."""
    if cfg.METRO_COMMUNES_GEOJSON.exists() and not force:
        obj = json.loads(cfg.METRO_COMMUNES_GEOJSON.read_bytes())
        print(f"  {'epci_communes':20s} cached")
    else:
        feats = []
        for url in cfg.METROPOLE_COMMUNES_URLS:
            feats += json.loads(_get(url)).get("features", [])
        obj = {"type": "FeatureCollection", "features": feats}
        cfg.METRO_COMMUNES_GEOJSON.write_text(json.dumps(obj, ensure_ascii=False),
                                              encoding="utf-8")
        print(f"  {'epci_communes':20s} {len(feats)} communes from "
              f"{len(cfg.METROPOLE_COMMUNES_URLS)} EPCI(s)")
    codes = {f["properties"].get("code") for f in obj["features"]}
    need = {cfg.BOUNDARY_COMMUNE_CODE} | set(getattr(cfg, "EXPECTED_SERVED_COMMUNES", {}))
    if not need <= codes:
        sys.exit(f"  the EPCI file lacks {sorted(need - codes)} - is "
                 f"METROPOLE_EPCI_CODES still right?")


def fetch_osm(cfg, force):
    from pipeline.osm import fetch as osm_fetch
    # retries=1: each mirror once, then stop. The owner's Overpass rule
    # (2026-09-30) is one query in flight and at least 60 s after a 504 or 429
    # before trying again, and osm.fetch's retry loop does not wait - so a
    # failure here is re-run by hand after the pause, never looped.
    elements, host = osm_fetch(cfg.OSM_ROUTES_QUERY, cfg.OSM_ROUTES_JSON,
                               force=force, retries=1)
    rels = [e for e in elements if e.get("type") == "relation"]
    refs = sorted({(e.get("tags") or {}).get("ref", "?") for e in rels})
    print(f"  {'osm_routes':20s} {len(rels)} relation(s), refs {refs} ({host})")
    want = set(cfg.OSM_REFS.values())
    if not want <= set(refs):
        msg = (f"OSM lacks the ref(s) {sorted(want - set(refs))} - check the "
               f"relations' tags (Reims's carry no ref at all)")
        if cfg.LINE_GEOMETRY == "osm":
            sys.exit("  " + msg)
        # Geometry is the feed's: OSM is only gate 3's cross-check here, so a
        # missing ref costs gate 3 for that line, not the build.
        print(f"  ⚠ {msg}; gate 3 needs another source for those lines")
    return host, len(rels)


def fetch_all(cfg):
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-parquet", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="re-download the boundary, EPCI and OSM caches too")
    args = ap.parse_args()
    cfg.DATA_RAW.mkdir(parents=True, exist_ok=True)
    cfg.OUTPUTS.mkdir(parents=True, exist_ok=True)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "gtfs_url": cfg.GTFS_URL, "gtfs_licence": cfg.GTFS_LICENCE,
            "boundary_url": cfg.BOUNDARY_URL}
    print("Rail and boundaries:")
    body = fetch_gtfs(cfg)
    fi = feed_info(body)
    prov["feed_info"] = fi
    prov["nap"] = nap_metadata(cfg)
    if bool(fi) != bool(cfg.GTFS_SELF_ATTESTS):
        print(f"  ⚠ GTFS_SELF_ATTESTS is {cfg.GTFS_SELF_ATTESTS} but the zip "
              f"{'does' if fi else 'does not'} carry a dated feed_info.txt - update the config")
    print(f"  feed window: " + (f"{fi['feed_start_date']} to {fi['feed_end_date']} (the zip's own)"
                                if fi else f"{prov['nap']['start_date']} to {prov['nap']['end_date']} "
                                           f"(the NAP's reading; resource updated {prov['nap']['resource_updated']})"))
    if cfg.CITY_BOUNDARY_GEOJSON.exists() and not args.force:
        print(f"  {'city_boundary':20s} cached")
    else:
        fetch_polygon(cfg.BOUNDARY_URL, cfg.CITY_BOUNDARY_GEOJSON, "city_boundary")
    fetch_epci_communes(cfg, args.force)
    # Every city: gate 3's independent count, and the geometry where
    # LINE_GEOMETRY == "osm".
    prov["osm_query"] = cfg.OSM_ROUTES_QUERY
    prov["osm_host"], prov["osm_relations"] = fetch_osm(cfg, args.force)

    print("\nNational register (shared across every French city):")
    france.SHARED_RAW.mkdir(parents=True, exist_ok=True)
    if args.skip_parquet:
        print("  SKIPPED (--skip-parquet)")
    else:
        for slug, test, dest, label in (
                (cfg.SIRENE_DATASET_SLUG,
                 lambda t: t.startswith(cfg.SIRENE_RESOURCE_TITLE_PREFIX),
                 cfg.SIRENE_PARQUET, "sirene_etab"),
                (cfg.GEOLOC_DATASET_SLUG,
                 lambda t: cfg.GEOLOC_RESOURCE_TITLE_CONTAINS in t.lower(),
                 cfg.GEOLOC_PARQUET, "sirene_geoloc")):
            meta = json.loads(_get(f"https://www.data.gouv.fr/api/1/datasets/{slug}/"))
            hits = [r for r in meta.get("resources", [])
                    if test(r.get("title", ""))
                    and "parquet" in (r.get("format", "") or "").lower()]
            if len(hits) != 1:
                sys.exit(f"  {label}: expected 1 parquet resource, got {len(hits)}")
            prov[f"{label}_title"] = hits[0].get("title")
            prov[f"{label}_last_modified"] = hits[0].get("last_modified")
            if dest.exists():
                print(f"  {label:20s} cached ({dest.stat().st_size:,} bytes), "
                      f"published edition: {hits[0].get('title', '')[:60]}")
                continue
            _stream(hits[0]["url"], dest, label)
    cfg.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
    print(f"\nprovenance -> {cfg.PROVENANCE_JSON.name}")
