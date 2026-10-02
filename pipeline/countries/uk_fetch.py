"""Downloads for the UK's tram and light-rail cities on the FSA register (the
UK six, 2026-10-02: Manchester (Regional) first, the pilot). Each city's
`fetch_sources.py` calls `main(config)` and nothing else.

Kept apart from `uk.py` because this module fetches: a `step*.py` may import
`uk.py` and never this (`scripts/check_no_fetch_in_steps.py`, one import level
deep). Newcastle's `fetch_sources.py` is the method, generalised:

  * **the FSA's bulk XML per authority, named by code** - the cities sit in
    wider FSA regions, so scope is the code list, and each file must parse and
    carry its own `LocalAuthorityCode` (a wrong URL can answer 200 with HTML).
    `config.FSA_AUTHORITY_COUNT` is asserted against the list: Wyre (207) and
    Wyre Forest (153) are one typo apart;
  * **Code-Point Open copied from London's cache**, the same GB-wide file and
    edition, never a second download;
  * **ONE Overpass query per city** (CLAUDE.md, owner 2026-09-30): the route
    relations and the boundary relations with geometry, the routes' member
    ways' tags (the light-rail test's track share) and their member nodes'
    tags (the stops). The boundary is polygonised from it here and gated on
    its area, so a truncated answer cannot pass;
  * **NaPTAN** (DfT, OGL v3; owner 2026-10-01), the ATCO areas the network
    stands in: gate 3's second independent source. Read for counting only,
    never drawn;
  * `provenance.json`: the fetch time, each FSA file's own `<ExtractDate>` (the
    FSA's condition: say when the information was updated), the Code-Point
    edition and the NaPTAN fetch.
"""
import io
import json
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
NAPTAN_URL = ("https://naptan.api.dft.gov.uk/v1/access-nodes"
              "?dataFormat=csv&atcoAreaCodes={code}")


def get(url, timeout=600):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def osm_query(config):
    """The city's one Overpass query: routes and boundaries `out geom`, the
    routes' member ways and nodes `out tags` / `out body`."""
    s, w, n, e = config.OSM_BBOX
    ids = ",".join(str(i) for i in config.BOUNDARY_OSM_RELATIONS)
    routes = "".join(f'rel["type"="route"]["route"="{r}"]({s},{w},{n},{e});'
                     for r in config.OSM_ROUTES)
    # Beside the routes' own member nodes, every tram stop in the box and any
    # STATION_ADD node: a stop the relations skip (Nottingham's David Lane)
    # can then be added by id from the cache, Kansas City's query shape.
    add = ",".join(str(i) for i in getattr(config, "STATION_ADD", {}) or {})
    return ("[out:json][timeout:180];"
            f"({routes})->.r;"
            f"rel(id:{ids})->.b;"
            "(.r;.b;);out geom;"
            "way(r.r);out tags;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e});'
            f'node["public_transport"="stop_position"]["tram"="yes"]({s},{w},{n},{e});'
            + (f"node(id:{add});" if add else "") + ");out body;")


def fetch_fsa(config, force):
    if len(config.FSA_AUTHORITIES) != config.FSA_AUTHORITY_COUNT:
        sys.exit(f"  {len(config.FSA_AUTHORITIES)} FSA authorities in config, "
                 f"expected exactly {config.FSA_AUTHORITY_COUNT}")
    config.FSA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for code, name in config.FSA_AUTHORITIES.items():
        dest = config.FSA_RAW_DIR / f"{code}.xml"
        if dest.exists() and not force:
            total += dest.stat().st_size
            print(f"  {name:<28} cached ({dest.stat().st_size:,} bytes)")
            continue
        body = get(config.FSA_FILE_URL.format(code=code))
        root = ET.fromstring(body)
        codes = {e.text for e in root.iter("LocalAuthorityCode")}
        if codes != {code}:
            sys.exit(f"  {name}: file carries authority code(s) {codes}, expected {code}")
        dest.write_bytes(body)
        total += len(body)
        print(f"  {name:<28} {len(body):>11,} bytes")
    print(f"  {len(config.FSA_AUTHORITIES)} authority files, {total:,} bytes")


def copy_codepoint(config, force):
    if config.CODEPOINT_ZIP.exists() and not force:
        print(f"  {'codepo_gb.zip':28} cached ({config.CODEPOINT_ZIP.stat().st_size:,} bytes)")
    else:
        if not config.CODEPOINT_SOURCE.exists():
            sys.exit(f"  no {config.CODEPOINT_SOURCE}: run python pipeline/london/fetch_sources.py first")
        shutil.copyfile(config.CODEPOINT_SOURCE, config.CODEPOINT_ZIP)
        print(f"  {'codepo_gb.zip':28} copied from London's cache "
              f"({config.CODEPOINT_ZIP.stat().st_size:,} bytes)")
    london_prov = config.ROOT / "outputs" / "london" / "provenance.json"
    return json.loads(london_prov.read_text(encoding="utf-8")).get("codepoint_edition")


def write_boundary(config, els):
    """The union of the scope's admin relations, each polygonised from its
    outer ways (Newcastle's method), gated on the union's area."""
    import geopandas as gpd
    from shapely.geometry import LineString, MultiLineString, mapping
    from shapely.ops import linemerge, polygonize, unary_union

    rels = {e["id"]: e for e in els if e.get("type") == "relation"
            and e["id"] in config.BOUNDARY_OSM_RELATIONS}
    if set(rels) != set(config.BOUNDARY_OSM_RELATIONS):
        sys.exit(f"  boundary relations returned {sorted(rels)}, expected "
                 f"{sorted(config.BOUNDARY_OSM_RELATIONS)}")
    feats, polys = [], []
    for rid, name in config.BOUNDARY_OSM_RELATIONS.items():
        lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                 for m in rels[rid].get("members", [])
                 if m.get("type") == "way" and m.get("role") == "outer"]
        poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
        km2 = gpd.GeoSeries([poly], crs="EPSG:4326").to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
        print(f"    {name:<26} {km2:7.1f} km2  (relation {rid})")
        polys.append(poly)
        feats.append({"type": "Feature", "geometry": mapping(poly),
                      "properties": {"osm_relation": rid, "name": name}})
    union = unary_union(polys)
    km2 = gpd.GeoSeries([union], crs="EPSG:4326").to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  the scope's union is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2, {len(feats)} polygons")


def fetch_osm(config, force):
    from pipeline import osm
    els, host = osm.fetch(osm_query(config), config.OSM_JSON, force=force)
    rels = [e for e in els if e.get("type") == "relation"
            and e["id"] not in config.BOUNDARY_OSM_RELATIONS]
    if not rels:
        sys.exit("  no route relations came back - a FAILED fetch, not a negative")
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    ways = sum(1 for e in els if e.get("type") == "way")
    nodes = sum(1 for e in els if e.get("type") == "node")
    print(f"  {'osm':28} {len(rels)} route relations, {ways} member ways, "
          f"{nodes} member nodes (via {host})")
    write_boundary(config, els)
    return host


def fetch_naptan(config, force):
    """Each ATCO area's NaPTAN CSV, kept whole in raw/ (step 1 reads only the
    stop types it names)."""
    config.NAPTAN_RAW_DIR.mkdir(parents=True, exist_ok=True)
    for code in config.NAPTAN_ATCO_AREAS:
        dest = config.NAPTAN_RAW_DIR / f"{code}.csv"
        if dest.exists() and not force:
            print(f"  {'naptan ' + code:28} cached ({dest.stat().st_size:,} bytes)")
            continue
        body = get(NAPTAN_URL.format(code=code))
        head = body[:400].decode("utf-8-sig", "replace")
        if not head.startswith("ATCOCode"):
            sys.exit(f"  NaPTAN area {code}: the answer is not the CSV ({head[:80]!r})")
        dest.write_bytes(body)
        print(f"  {'naptan ' + code:28} {len(body):>11,} bytes")


def extract_dates(config):
    out = {}
    for code, name in config.FSA_AUTHORITIES.items():
        with open(config.FSA_RAW_DIR / f"{code}.xml", encoding="utf-8") as fh:
            head = fh.read(400)
        i = head.find("<ExtractDate>")
        out[name] = head[i + 13:i + 23] if i >= 0 else ""
    return out


def main(config, argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=f"Download {config.CITY_NAME}'s raw inputs.")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-osm", action="store_true",
                    help="skip the Overpass query (the FSA, Code-Point and NaPTAN only)")
    args = ap.parse_args(argv)
    for d in (config.DATA_RAW, config.DATA_PROCESSED, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    fetch_fsa(config, args.force)
    edition = copy_codepoint(config, args.force)
    host = None if args.no_osm else fetch_osm(config, args.force)
    fetch_naptan(config, args.force)

    extracts = extract_dates(config)
    dates = sorted(d for d in extracts.values() if d)
    old = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
           if config.PROVENANCE_JSON.exists() else {})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    prov = {"fetched_utc": now,
            "fsa_file_url": config.FSA_FILE_URL,
            "fsa_authorities": config.FSA_AUTHORITIES,
            "fsa_extract_dates": extracts,
            "fsa_extract_range": [dates[0], dates[-1]] if dates else [],
            "codepoint_edition": edition,
            "osm_fetched_utc": now if host else old.get("osm_fetched_utc"),
            "naptan_url": NAPTAN_URL,
            "naptan_atco_areas": list(config.NAPTAN_ATCO_AREAS)}
    print(f"  FSA extract dates {dates[0]} to {dates[-1]}")
    config.PROVENANCE_JSON.write_bytes(
        (json.dumps(prov, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")


if __name__ == "__main__":
    sys.exit("run a city's fetch_sources.py, which passes its config")
