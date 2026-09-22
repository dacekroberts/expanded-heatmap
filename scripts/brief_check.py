"""Re-run a build brief's factual claims against the live sources.

    python scripts/brief_check.py                 # every brief that has checks
    python scripts/brief_check.py toronto         # one city
    python scripts/brief_check.py --list          # show the claims, run nothing
    python scripts/brief_check.py --force         # ignore the download cache

WHY THIS EXISTS
---------------
`docs/build_briefs/<city>.md` caches Step 0's answers so a build does not
re-derive them. It caches Step 0's MISTAKES with equal confidence, and the
MEASURED/ASSERTED labels did not prevent that.

Edmonton, built 2026-09-21, inherited three wrong claims from its own brief -
and every one of them was a single HTTP call from being caught:

  1. "A BETTER PATH EXISTS, and it sidesteps staleness entirely" - the brief
     RECOMMENDED eight Socrata GTFS tables over the agency zip. They were
     expired. One read of their `calendar_dates` range would have said so, and
     reading each table's `updatedAt` was the brief's own argument FOR them.
  2. "Edmonton's feed carries no `feed_info.txt`" - the agency feed has one.
  3. "No required notice, uniquely among the Canadian candidates" - a
     redistribution clause applies that the credit sentence does not mention.

And a fourth, from the country profile rather than the brief: 33 stations,
where three of the 33 are garages nobody can board at.

**The label was not the failure. The prose was.** By the time a brief says "a
better path exists", the ASSERTED tag three paragraphs up has been metabolised
into a recommendation, and nobody re-opens the question. A claim survives being
reasoned from only if something re-runs it.

So: a brief declares its checkable claims in a fenced ```brief-checks block,
JSON, right beside the prose that relies on them. Writing the claim and writing
its check is one act, and drift between them shows up as a FAIL rather than as
a confident sentence.

**This does not replace `add-city` Step 0.** It protects the claims a brief
already made. A brief with no checks block is reported, not skipped silently.

ADDING A CHECK KIND
-------------------
Write a function taking (spec, ctx) and returning (ok, detail), then register
it in CHECKS. Every kind is derived from something that actually went wrong in
this project; resist adding speculative ones.
"""

import argparse
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent
BRIEFS = ROOT / "docs" / "build_briefs"
# data/*/raw/ is already gitignored, so this path needs no .gitignore change.
CACHE = ROOT / "data" / "_brief_check" / "raw"

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
BLOCK = re.compile(r"```brief-checks\s*\n(.*?)\n```", re.S)


# --- plumbing -------------------------------------------------------------

def fetch(url, name, *, force=False, timeout=900):
    """Download to the gitignored cache, or reuse it."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / name
    if path.exists() and not force:
        return path
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    path.write_bytes(r.content)
    return path


def slug(url):
    return re.sub(r"[^A-Za-z0-9._-]", "_", url)[-120:]


def gtfs(url, ctx):
    return zipfile.ZipFile(fetch(url, slug(url) + ".zip", force=ctx["force"]))


def table(z, name, **kw):
    import pandas as pd
    with z.open(name) as f:
        return pd.read_csv(f, dtype=str, **kw)


def near(got, want, tol):
    if want is None:
        return True
    return abs(got - want) <= tol


# --- check kinds ----------------------------------------------------------

def http_ok(spec, ctx):
    """A URL resolves. Catches the two guessed Edmonton GTFS URLs that 404'd."""
    r = requests.get(spec["url"], headers=HEADERS, timeout=300, stream=True)
    size = 0
    for chunk in r.iter_content(65536):
        size += len(chunk)
        if size > spec.get("min_bytes", 0) and size > 2_000_000:
            break
    r.close()
    ct = r.headers.get("content-type", "")
    ok = r.status_code == spec.get("expect_status", 200)
    detail = f"HTTP {r.status_code}, >={size:,} bytes, content-type {ct!r}"
    if ok and "min_bytes" in spec and size < spec["min_bytes"]:
        ok, detail = False, detail + f" - under min_bytes {spec['min_bytes']:,}"
    if ok and "content_type_contains" in spec:
        if spec["content_type_contains"] not in ct:
            ok = False
            detail += f" - expected content-type to contain {spec['content_type_contains']!r}"
    return ok, detail


def gtfs_files(spec, ctx):
    """Which files a feed ships. Catches "no feed_info.txt" said of a feed
    that has one."""
    names = set(gtfs(spec["url"], ctx).namelist())
    missing = [f for f in spec.get("present", []) if f not in names]
    intruding = [f for f in spec.get("absent", []) if f in names]
    ok = not missing and not intruding
    bits = [f"{len(names)} files"]
    if missing:
        bits.append(f"MISSING {missing}")
    if intruding:
        bits.append(f"PRESENT but asserted absent: {intruding}")
    return ok, "; ".join(bits)


def gtfs_feed_window(spec, ctx):
    """A feed's declared validity. Catches a stale republication being
    preferred over the agency's own current feed."""
    from datetime import date
    z = gtfs(spec["url"], ctx)
    want = spec.get("expect", "current")
    if "feed_info.txt" not in z.namelist():
        return want == "absent", "no feed_info.txt (declares no validity window)"
    fi = table(z, "feed_info.txt")
    end = str(fi.iloc[0].get("feed_end_date", "") or "")
    start = str(fi.iloc[0].get("feed_start_date", "") or "")
    if not end or end == "nan":
        return want == "absent", f"feed_info.txt present but no feed_end_date (start {start})"
    ed = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    days = (ed - date.today()).days
    state = "current" if days >= 0 else "expired"
    detail = f"{start} to {end} ({days:+d} days) -> {state}"
    return state == want, detail


def gtfs_calendar_window(spec, ctx):
    """calendar_dates' real span, for a feed that declares no feed_info.
    This is what showed Edmonton's eight Socrata tables were expired."""
    from datetime import date
    z = gtfs(spec["url"], ctx)
    cd = table(z, "calendar_dates.txt")
    lo, hi = cd["date"].min(), cd["date"].max()
    ed = date(int(hi[:4]), int(hi[4:6]), int(hi[6:8]))
    days = (ed - date.today()).days
    state = "current" if days >= 0 else "expired"
    return state == spec.get("expect", "current"), \
        f"calendar_dates {lo} to {hi} ({days:+d} days) -> {state}"


def gtfs_route_type_counts(spec, ctx):
    """Routes per route_type. Catches a mirror missing an entire mode, as
    Toronto's did - it had zero route_type 1 and no subway at all."""
    routes = table(gtfs(spec["url"], ctx), "routes.txt")
    got = routes["route_type"].value_counts().to_dict()
    want = {str(k): v for k, v in spec["expect"].items()}
    bad = {k: (got.get(k, 0), v) for k, v in want.items() if got.get(k, 0) != v}
    detail = "route_type counts " + json.dumps({k: int(v) for k, v in sorted(got.items())})
    if bad:
        detail += " - MISMATCH " + json.dumps(
            {k: {"got": g, "expected": e} for k, (g, e) in bad.items()})
    return not bad, detail


def gtfs_stations(spec, ctx):
    """THE most error-prone number in this project, and now three checks in one.

    Toronto recorded 234 stations that were platforms; Calgary 83 that were
    platforms; Edmonton 33 of which three are garages. So this measures:
      - platforms (served stops)
      - whether parent_station is populated, and the collapsed count
      - the BOARDABLE station count, dropping stops where pickup_type and
        drop_off_type are 1 on every stop_time (Edmonton's garages)
      - nearest-neighbour spacing, which is the real platform-vs-station test
    """
    import pandas as pd
    import numpy as np
    z = gtfs(spec["url"], ctx)
    routes = table(z, "routes.txt")
    if "route_types" in spec:
        want = {str(t) for t in spec["route_types"]}
        rail = routes[routes["route_type"].isin(want)]
    else:
        rail = routes[routes["route_id"].isin(spec["route_ids"])]
    if "route_name_regex" in spec:
        col = "route_long_name" if "route_long_name" in rail.columns else "route_short_name"
        rail = rail[rail[col].fillna("").str.match(spec["route_name_regex"])]
    trips = table(z, "trips.txt")
    keep = trips[trips["route_id"].isin(set(rail["route_id"]))]
    st = table(z, "stop_times.txt",
               usecols=lambda c: c in {"trip_id", "stop_id", "pickup_type",
                                       "drop_off_type"})
    st = st[st["trip_id"].isin(set(keep["trip_id"]))]
    stops = table(z, "stops.txt")
    served = stops[stops["stop_id"].isin(set(st["stop_id"]))].copy()

    bits = [f"{len(rail)} routes", f"{len(served)} platforms"]
    ok = True

    # boardability
    if {"pickup_type", "drop_off_type"} <= set(st.columns):
        b = ((st["pickup_type"].fillna("0") == "0")
             | (st["drop_off_type"].fillna("0") == "0"))
        boardable_ids = set(st.loc[b, "stop_id"])
        non_rev = served[~served["stop_id"].isin(boardable_ids)]
    else:
        non_rev = served.iloc[0:0]
        bits.append("no pickup_type/drop_off_type columns")

    has_parent = ("parent_station" in served.columns
                  and served["parent_station"].notna().any())
    bits.append(f"parent_station populated: {has_parent}")
    if "expect_parent_station_populated" in spec:
        if has_parent != spec["expect_parent_station_populated"]:
            ok = False
            bits.append("MISMATCH on parent_station being populated")

    def collapse(df):
        if has_parent and df["parent_station"].notna().all():
            g = df.groupby("parent_station")
        else:
            name = df["stop_name"].str.strip()
            for pat in spec.get("strip_patterns", []):
                name = name.str.replace(pat, "", regex=True)
            g = df.assign(_k=name.str.strip()).groupby("_k")
        return g.agg(lat=("stop_lat", lambda s: pd.to_numeric(s).mean()),
                     lon=("stop_lon", lambda s: pd.to_numeric(s).mean())).reset_index()

    all_st = collapse(served)
    rev_st = collapse(served[~served["stop_id"].isin(non_rev["stop_id"])]) \
        if len(non_rev) else all_st
    bits.append(f"{len(all_st)} stations")
    if len(non_rev):
        bits.append(f"{len(non_rev)} NON-REVENUE platforms -> "
                    f"{len(rev_st)} boardable stations "
                    f"({', '.join(sorted(set(non_rev['stop_name'])))})")

    for key, got in (("expect_platforms", len(served)),
                     ("expect_stations", len(all_st)),
                     ("expect_boardable_stations", len(rev_st))):
        if key in spec and got != spec[key]:
            ok = False
            bits.append(f"MISMATCH {key}: got {got}, brief says {spec[key]}")

    # spacing: the diagnostic that caught Toronto and Calgary
    if len(rev_st) > 1:
        import geopandas as gpd
        crs = spec.get("crs")
        if crs:
            pts = gpd.GeoSeries(gpd.points_from_xy(rev_st["lon"], rev_st["lat"]),
                                crs=4326).to_crs(crs).reset_index(drop=True)
            nn = np.array([pts.drop(index=i).distance(pts.iloc[i]).min()
                           for i in range(len(pts))])
            med = float(np.median(nn))
            bits.append(f"median nearest-neighbour {med:.0f} m")
            floor = spec.get("station_spacing_median_m_min")
            if floor and med < floor:
                ok = False
                bits.append(f"TOO TIGHT for stations (<{floor} m) - these are "
                            f"probably still platforms")
    return ok, "; ".join(bits)


def ckan_rows(spec, ctx):
    """CKAN datastore row count. Note datastore_search_sql 404s on Toronto's
    portal, so this uses datastore_search."""
    url = f"https://{spec['domain']}/api/3/action/datastore_search"
    r = requests.get(url, params={"resource_id": spec["resource_id"], "limit": 0},
                     headers=HEADERS, timeout=300)
    r.raise_for_status()
    got = r.json()["result"]["total"]
    want = spec.get("expect")
    tol = spec.get("tolerance", 0)
    ok = want is None or near(got, want, tol)
    return ok, f"{got:,} rows" + ("" if ok else f" - brief says {want:,} (tolerance {tol:,})")


def ckan_fields(spec, ctx):
    """Which columns a CKAN resource exposes. Toronto's register carries THREE
    personal columns, and the count mattered - one was recorded, two were not."""
    url = f"https://{spec['domain']}/api/3/action/datastore_search"
    r = requests.get(url, params={"resource_id": spec["resource_id"], "limit": 1},
                     headers=HEADERS, timeout=300)
    r.raise_for_status()
    fields = [f["id"] for f in r.json()["result"]["fields"]]
    missing = [f for f in spec.get("present", []) if f not in fields]
    intruding = [f for f in spec.get("absent", []) if f in fields]
    ok = not missing and not intruding
    bits = [f"{len(fields)} fields"]
    if missing:
        bits.append(f"MISSING {missing}")
    if intruding:
        bits.append(f"PRESENT but asserted absent: {intruding}")
    if spec.get("show"):
        bits.append("fields: " + ", ".join(fields))
    return ok, "; ".join(bits)


def socrata_count(spec, ctx):
    url = f"https://{spec['domain']}/resource/{spec['view']}.json"
    params = {"$select": "count(1) as n"}
    if "where" in spec:
        params["$where"] = spec["where"]
    r = requests.get(url, params=params, headers=HEADERS, timeout=300)
    r.raise_for_status()
    got = int(r.json()[0]["n"])
    want = spec.get("expect")
    tol = spec.get("tolerance", 0)
    ok = want is None or near(got, want, tol)
    return ok, f"{got:,} rows" + ("" if ok else f" - brief says {want:,} (tolerance {tol:,})")


def socrata_distinct_split(spec, ctx):
    """Distinct values of a multi-valued column. Three of six Canadian
    registers store several categories per row, and a naive value_counts
    returns COMBINATIONS - which is how Edmonton's 60 categories were recorded
    as 67 and Calgary's 96 as 173."""
    import pandas as pd
    url = f"https://{spec['domain']}/resource/{spec['view']}.csv"
    params = {"$select": spec["column"], "$limit": spec.get("limit", 100000)}
    if "where" in spec:
        params["$where"] = spec["where"]
    r = requests.get(url, params=params, headers=HEADERS, timeout=600)
    r.raise_for_status()
    s = pd.read_csv(io.BytesIO(r.content), dtype=str)[spec["column"]].fillna("")
    naive = s.nunique()
    delim = spec.get("delimiter")
    if delim:
        vals = set()
        for v in s:
            vals.update(p.strip() for p in str(v).split(delim) if p.strip())
        got = len(vals)
    else:
        got = naive
    want = spec.get("expect")
    ok = want is None or got == want
    detail = f"{naive} naive distinct"
    if delim:
        detail += f", {got} true distinct on {delim!r}"
    if not ok:
        detail += f" - brief says {want}"
    return ok, detail


def geojson_area_km2(spec, ctx):
    """A boundary polygon's real area. Edmonton publishes FOUR layers named
    some variant of "Corporate Boundary" and two are the pre-2019 polygon;
    Calgary publishes two and one is 53 bytes of valid, empty GeoJSON."""
    import geopandas as gpd
    path = fetch(spec["url"], slug(spec["url"]) + ".geojson", force=ctx["force"])
    b = gpd.read_file(path)
    if len(b) == 0 or b.geometry.isna().all():
        return False, "no geometry - the empty-view trap"
    b = b.set_crs(4326) if b.crs is None else b.to_crs(4326)
    area = b.to_crs(spec["crs"]).union_all().area / 1e6
    lo, hi = spec.get("min"), spec.get("max")
    ok = (lo is None or area >= lo) and (hi is None or area <= hi)
    return ok, (f"{len(b)} feature(s), {area:.1f} km2"
                + ("" if ok else f" - brief expects {lo}-{hi} km2"))


def utm_zone_from_longitude(spec, ctx):
    """Offline, and the cheapest check here: the projected CRS is derivable."""
    lon = spec["lon"]
    zone = int(math.floor((lon + 180) / 6) + 1)
    epsg = f"EPSG:{32600 + zone if spec.get('north', True) else 32700 + zone}"
    ok = epsg == spec["expect"]
    return ok, f"longitude {lon} -> UTM {zone}N -> {epsg}" + \
        ("" if ok else f" - brief says {spec['expect']}")


def endpoint_absent(spec, ctx):
    """An endpoint this project must NOT rely on. Toronto's
    datastore_search_sql 404s, and recording that it does is what stops the
    next session rediscovering it."""
    try:
        r = requests.get(spec["url"], headers=HEADERS, timeout=120)
        code = r.status_code
    except Exception as exc:
        return True, f"unreachable ({type(exc).__name__}), which satisfies the claim"
    want = spec.get("expect_status")
    ok = (code >= 400) if want is None else (code == want)
    return ok, f"HTTP {code}" + ("" if ok else " - the brief says this endpoint fails")


CHECKS = {
    "http_ok": http_ok,
    "endpoint_absent": endpoint_absent,
    "gtfs_files": gtfs_files,
    "gtfs_feed_window": gtfs_feed_window,
    "gtfs_calendar_window": gtfs_calendar_window,
    "gtfs_route_type_counts": gtfs_route_type_counts,
    "gtfs_stations": gtfs_stations,
    "ckan_rows": ckan_rows,
    "ckan_fields": ckan_fields,
    "socrata_count": socrata_count,
    "socrata_distinct_split": socrata_distinct_split,
    "geojson_area_km2": geojson_area_km2,
    "utm_zone_from_longitude": utm_zone_from_longitude,
}


# --- driver ---------------------------------------------------------------

def load(path):
    text = path.read_text(encoding="utf-8")
    specs = []
    for block in BLOCK.findall(text):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            sys.exit(f"{path.name}: brief-checks block is not valid JSON - {exc}")
        specs.extend(data if isinstance(data, list) else [data])
    built = bool(re.search(r"^>\s*##\s*BUILT", text, re.M))
    return specs, built


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="*", help="city slug(s); default every brief")
    ap.add_argument("--list", action="store_true", help="print claims, run nothing")
    ap.add_argument("--force", action="store_true", help="ignore the download cache")
    args = ap.parse_args()

    briefs = sorted(BRIEFS.glob("*.md"))
    if args.city:
        briefs = [b for b in briefs if b.stem in args.city]
        if not briefs:
            sys.exit(f"no brief for {args.city}. Have: "
                     f"{', '.join(b.stem for b in sorted(BRIEFS.glob('*.md')))}")

    total = failed = 0
    unchecked = []
    for path in briefs:
        specs, built = load(path)
        if not specs:
            unchecked.append((path.stem, built))
            continue
        tag = " (BUILT - claims are history, but still checkable)" if built else ""
        print(f"\n=== {path.stem}{tag}: {len(specs)} claim(s) ===")
        for spec in specs:
            total += 1
            claim = spec.get("claim", spec.get("id", "?"))
            kind = spec.get("kind")
            if args.list:
                print(f"  [ ] {claim}\n        kind={kind}")
                continue
            fn = CHECKS.get(kind)
            if not fn:
                failed += 1
                print(f"  FAIL {claim}\n        unknown check kind {kind!r}; "
                      f"known: {', '.join(sorted(CHECKS))}")
                continue
            try:
                ok, detail = fn(spec, {"force": args.force})
            except Exception as exc:
                ok, detail = False, f"{type(exc).__name__}: {exc}"
            if not ok:
                failed += 1
            print(f"  {'PASS' if ok else 'FAIL'} {claim}\n        {detail}")

    if unchecked:
        print("\n=== briefs with NO brief-checks block ===")
        for name, built in unchecked:
            print(f"  {name}{' (built)' if built else ''} - claims are prose only, "
                  f"so nothing re-runs them")

    if args.list:
        return
    print(f"\nRESULT: {total - failed}/{total} claim(s) hold"
          + (f", {failed} FAILED" if failed else ""))
    if failed:
        print("A failing claim is a brief to correct, not a check to relax - the "
              "brief is the cache and the source is the truth.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
