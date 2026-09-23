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
import datetime as dt
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent
# --vs-config imports pipeline.<city>.config, and this runs as a script, so the
# repo root is not on sys.path the way it is for the step scripts.
sys.path.insert(0, str(ROOT))
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


def http_contains(spec, ctx):
    """A document still SAYS a specific thing. For a claim no structured
    field can carry.

    Written for Milan, where the licence VERSION is invisible to the obvious
    endpoint: CKAN's `package_show` reports `license_id: cc-by` with no
    number, and only the portal's DCAT-AP_IT serialisation carries
    `owl:versionInfo "4.0"`. A brief that pinned its licence claim to
    `package_show` would keep passing while the version - which decides the
    attribution obligations - went unwatched. That is this project's recurring
    shape: a check that cannot see the thing it is guarding.

    `present` / `absent` are lists of literal substrings, matched
    case-insensitively against the response text. Not a parser: the point is
    to notice a document CHANGING, and a licence page that stops containing
    "4.0" is worth a human reading it whatever the cause.
    """
    # A CHECK WITH NOTHING TO LOOK FOR MUST FAIL, NOT PASS. Until 2026-09-23
    # sixteen checks across ten briefs declared `"contains": "..."`, a key this
    # function never read - so each passed on any HTTP 200 and could not see
    # the licence, field or layer it was written to guard. That is this kind's
    # own docstring's failure ("a check that cannot see the thing it is
    # guarding"), reproduced by a spelling. A string where a list belongs is
    # the same trap one character over: "CC0" iterates as "C", "C", "0".
    if "contains" in spec:
        return False, ("spec uses 'contains', which this kind does not read - "
                       "write \"present\": [...] so the check can see its claim")
    for key in ("present", "absent"):
        if isinstance(spec.get(key), str):
            return False, f"'{key}' must be a LIST of strings, not one string"
    if not spec.get("present") and not spec.get("absent"):
        return False, "no 'present' or 'absent' given - this check cannot see anything"
    r = requests.get(spec["url"], headers=HEADERS, timeout=120)
    if r.status_code != spec.get("expect_status", 200):
        return False, f"HTTP {r.status_code}"
    text = r.text.lower()
    missing = [s for s in spec.get("present", []) if s.lower() not in text]
    intruded = [s for s in spec.get("absent", []) if s.lower() in text]
    bits = [f"{len(r.text):,} chars"]
    if missing:
        bits.append(f"MISSING {missing}")
    if intruded:
        bits.append(f"UNEXPECTEDLY PRESENT {intruded}")
    return not (missing or intruded), "; ".join(bits)


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
    portal, so this uses datastore_search.

    `limit=1`, not `limit=0`. Toronto's CKAN returns `total` either way;
    Barcelona's omits it entirely when `limit=0`, so both of Barcelona's row
    claims failed with `KeyError: 'total'` against a portal that was answering
    correctly. One wasted row is cheaper than a check that only works on the
    portal it was written against - and every remaining candidate city in this
    project is on a non-Toronto CKAN."""
    url = f"https://{spec['domain']}/api/3/action/datastore_search"
    r = requests.get(url, params={"resource_id": spec["resource_id"], "limit": 1},
                     headers=HEADERS, timeout=300)
    r.raise_for_status()
    result = r.json().get("result") or {}
    if "total" not in result:
        return False, ("datastore_search returned no `total` field "
                       f"(keys: {sorted(result)}) - this portal may not expose "
                       "row counts, or the resource is not datastore-backed")
    got = result["total"]
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


def taxonomy_catchall(spec, ctx):
    """How much of a classification column is a CATCH-ALL, at each level of the
    taxonomy - the measurement that decides which level a city keys on.

    WHY THIS IS A CHECK RATHER THAN A PARAGRAPH. Barcelona's census publishes
    four levels of the same taxonomy, and the natural-looking one is wrong:
    `Nom_Grup_Activitat` puts **35% of active rows into `Altres`**, while
    `Nom_Activitat` - the finest - has an explicit home for all 75 of its
    values. That is the opposite of Madrid, whose own multi-level scheme is
    keyed nearer the top, and both cities are right. The deciding number is the
    catch-all share per level, and until now it was measured during step 2, by
    which point the config, the taxonomy module and the map script have all
    been written against a level someone guessed at.

    It also catches the second failure in the same family: a catch-all that is
    small but MEANS SEVERAL THINGS. Barcelona's `Altres` is 1,545 rows spread
    across five different parents - food retail, retail/wholesale, services,
    food service and genuinely-other - so a share under the threshold is a
    reason to look at `by_parent`, not a reason to stop looking. Pass
    `parent_column` to get that breakdown; it is what tells you whether the
    catch-all can be dispatched (Chicago's `EXTRA_COLUMNS` mechanism) or has to
    be dropped.

    A share over `max_share` is a brief to correct - by keying a level deeper -
    never a threshold to raise.
    """
    import pandas as pd
    values, parents = _classification_column(spec, ctx)
    total = len(values)
    if not total:
        return False, "no rows returned - the filter or resource id is wrong"

    def norm(s):
        return s.strip().upper() if isinstance(s, str) else ""

    wanted = {norm(v) for v in spec["catchall"]}
    normed = values.map(norm)
    blank = int((normed == "").sum())
    hits = normed.isin(wanted)
    n = int(hits.sum())
    share = n / total

    max_share = spec.get("max_share")
    ok = max_share is None or share <= max_share
    bits = [f"{n:,} of {total:,} rows ({share:.1%}) are "
            f"{sorted(spec['catchall'])} in {spec['column']!r}"]
    if not ok:
        bits.append(f"OVER the brief's {max_share:.0%} ceiling - key a level "
                    f"deeper rather than raising this")
    if blank:
        bits.append(f"{blank:,} blank ({blank / total:.1%}), counted in the "
                    f"denominator and NOT as catch-all")

    # Every other level, reported only. This is the comparison the decision is
    # actually made on, so a brief that declares it shows its working.
    for other in spec.get("compare", []):
        # parent_column dropped: it is only meaningful for the keyed column,
        # and leaving it in asked one portal for the same field twice and got
        # HTTP 500 - a comparison level IS often the parent level.
        o_spec = {k: v for k, v in spec.items() if k != "parent_column"}
        o_spec["column"] = other
        o_vals, _ = _classification_column(o_spec, ctx)
        if not len(o_vals):
            bits.append(f"{other!r}: no rows")
            continue
        o_norm = o_vals.map(norm)
        o_n = int(o_norm.isin(wanted).sum())
        bits.append(f"{other!r}: {o_n / len(o_vals):.1%} catch-all, "
                    f"{o_norm.nunique()} distinct")

    if spec.get("parent_column") and parents is not None and n:
        by_parent = parents[hits.values].map(norm).value_counts()
        if len(by_parent) > 1:
            shown = "; ".join(f"{k or '(blank)'} {v:,}"
                              for k, v in by_parent.head(8).items())
            bits.append(f"catch-all spans {len(by_parent)} parents - {shown}. "
                        f"One value meaning several things needs dispatching "
                        f"on the parent, not a single bucket")
    bits.append(f"{normed.nunique()} distinct values in {spec['column']!r}")
    return ok, "; ".join(bits)


def _classification_column(spec, ctx):
    """One or two columns of a live register, as pandas Series.

    Speaks the two portal shapes this project actually meets. Kept beside
    `taxonomy_catchall` rather than generalised further, because the next
    portal will want its own paging rule and guessing it now would be
    inventing a requirement.
    """
    import pandas as pd
    cols = [spec["column"]]
    if spec.get("parent_column") and spec["parent_column"] != spec["column"]:
        cols.append(spec["parent_column"])

    if spec.get("domain", "").startswith("data.") or spec.get("socrata"):
        url = f"https://{spec['domain']}/resource/{spec['view']}.csv"
        params = {"$select": ",".join(cols), "$limit": spec.get("limit", 200000)}
        if "where" in spec:
            params["$where"] = spec["where"]
        r = requests.get(url, params=params, headers=HEADERS, timeout=600)
        r.raise_for_status()
        df = pd.read_csv(io.BytesIO(r.content), dtype=str)
    else:
        # CKAN datastore. Paged, because `limit` is capped server-side well
        # below a full register and a silent truncation here would understate
        # the catch-all share - the one direction that turns a failing check
        # into a passing one.
        url = f"https://{spec['domain']}/api/3/action/datastore_search"
        rows, offset, page = [], 0, spec.get("page_size", 10000)
        while True:
            params = {"resource_id": spec["resource_id"], "limit": page,
                      "offset": offset, "fields": ",".join(cols)}
            if spec.get("filters"):
                params["filters"] = json.dumps(spec["filters"])
            r = requests.get(url, params=params, headers=HEADERS, timeout=600)
            r.raise_for_status()
            got = (r.json().get("result") or {}).get("records") or []
            rows.extend(got)
            offset += len(got)
            if len(got) < page or offset >= spec.get("limit", 500000):
                break
        df = pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)

    values = df[spec["column"]] if spec["column"] in df else pd.Series(dtype=str)
    parents = (df[spec["parent_column"]]
               if spec.get("parent_column") and spec["parent_column"] in df
               else None)
    return values, parents


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


def arcgis_layer(spec, ctx):
    """An ArcGIS feature layer's record count AND how recently it was edited.

    Exists because a brief can watch the wrong product and report healthy.
    Madrid's brief carried a tripwire on CRTM's Metro GTFS - "when this check
    FAILS, CRTM has refreshed it and the rail decision should be revisited" -
    and that check kept PASSING while the decision it guarded was already
    stale, because CRTM publishes the same network TWICE: a GTFS feed it
    stopped refreshing in 2025-05, and ArcGIS feature layers it still edits
    (M4_Red, 2026-06-05). The tripwire watched the feed and the build wanted
    the network.

    So this checks the thing actually consumed. `max_age_days` is the point:
    a layer that silently stops being maintained is the Edmonton failure in
    its most general form, and freshness here is read from the server's own
    `editingInfo.lastEditDate` rather than from a catalogue's `modified`.
    """
    base = spec["url"].rstrip("/")
    meta = requests.get(f"{base}?f=json", headers=HEADERS, timeout=120).json()
    if "error" in meta:
        return False, f"service error: {meta['error'].get('message', meta['error'])}"

    bits = []
    ok = True
    if "expect_geometry" in spec:
        got = meta.get("geometryType")
        good = got == spec["expect_geometry"]
        ok &= good
        bits.append(f"geometry {got}" + ("" if good else f" != {spec['expect_geometry']}"))

    if "expect_rows" in spec:
        n = requests.get(f"{base}/query", headers=HEADERS, timeout=180,
                         params={"where": "1=1", "returnCountOnly": "true",
                                 "f": "json"}).json().get("count")
        good = near(n, spec["expect_rows"], spec.get("tolerance", 0))
        ok &= good
        bits.append(f"{n} rows" + ("" if good else f" - brief says {spec['expect_rows']}"))

    for field in spec.get("present", []):
        good = any(f["name"] == field for f in meta.get("fields", []))
        ok &= good
        if not good:
            bits.append(f"MISSING field {field}")

    stamp = (meta.get("editingInfo") or {}).get("lastEditDate")
    if stamp:
        edited = dt.datetime.fromtimestamp(stamp / 1000, dt.timezone.utc)
        age = (dt.datetime.now(dt.timezone.utc) - edited).days
        bits.append(f"last edited {edited:%Y-%m-%d} ({age}d)")
        if "max_age_days" in spec:
            good = age <= spec["max_age_days"]
            ok &= good
            if not good:
                bits.append(f"STALE - brief allows {spec['max_age_days']}d")
    elif "max_age_days" in spec:
        ok = False
        bits.append("no editingInfo.lastEditDate, so freshness cannot be checked")

    return ok, "; ".join(bits)


# --- OpenStreetMap ----------------------------------------------------------
#
# Several mirrors, tried in order, and an EMPTY 200 IS A HOST FAILURE rather
# than an answer about the city. `pipeline/countries/mexico.py` records
# overpass.osm.ch returning 272 bytes over an empty set, which a caller
# reported as "every ref has exactly 2 direction relations" - a confident
# statement about nothing. So an empty result moves to the next host and is
# never cached.
OVERPASS_HOSTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
)


def _overpass_once(host, query, timeout):
    """One mirror. Returns elements, or raises with why this host is no good.

    Two ways a mirror lies with HTTP 200, both seen on 2026-09-22:

      - an EMPTY elements list (overpass.osm.ch, twice, no `remark`), which
        `pipeline/countries/mexico.py` already records; and
      - a PARTIAL one. The same query returned 54 elements and then 34 within
        one minute - tram 20 -> 12, funicular 6 -> 4 - which is the dangerous
        case, because a partial answer is shaped exactly like a real decrease.

    Overpass signals an aborted query with a top-level `remark`, so that is
    rejected too; the 34-element answer carried none, which is why the caller
    must ALSO confirm a mismatch against a second mirror.
    """
    r = requests.post(host, data=query.encode("utf-8"),
                      headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    payload = r.json()
    if payload.get("remark"):
        raise RuntimeError(f"remark {payload['remark']!r}")
    elements = payload.get("elements") or []
    if not elements:
        raise RuntimeError("empty 200")
    return elements


def _overpass(query, timeout=180, _skip=()):
    """First mirror that answers. Returns (elements, host).

    ⚠ A 504 OR A READ TIMEOUT HERE MAY BE THE QUERY RATHER THAN THE HOST, and
    naming that in the error is what stops the next person waiting out a
    cost problem. It is not always the query: on the same day a tags-only
    query, with no geometry at all, 504'd on overpass-api.de and timed out
    on kumi. Rule out cost first because it is the part you control.
    Measured 2026-09-23 on the Toulouse commune bbox, same tag, minutes apart:
    `node+way` with `out center` drew a 504 from overpass-api.de and a read
    timeout from kumi, while `node` alone with `out body` answered in seconds
    on the first host tried. `out center` makes Overpass resolve every way's
    member nodes; the node half is typically 90%+ of a POI answer anyway
    (restaurant nodes were 827 of 889, 93.0%).

    So write the cheap query first and add ways as a SECOND query if the node
    answer is not enough - and never compare a node-only count with a
    node+way one, which measures the query rather than the city.

    `timeout` is 180 rather than 300 for the same reason: a city-bbox query
    that has not answered in three minutes wants making cheaper, not waiting
    on. The full rules live in pipeline/osm.py's docstring; this is a second
    copy of the fetch logic, deliberately, because this script must run from a
    clean clone without importing the pipeline package.
    """
    problems = []
    for host in OVERPASS_HOSTS:
        name = host.split("/")[2]
        if name in _skip:
            continue
        try:
            return _overpass_once(host, query, timeout), name
        except Exception as exc:
            hint = ""
            if "504" in str(exc) or "timed out" in str(exc).lower():
                hint = "  <- may be cost rather than outage: try nodes-only, drop `out center`"
            problems.append(f"{name}: {type(exc).__name__} {exc}{hint}")
    raise RuntimeError("every Overpass mirror failed - " + "; ".join(problems))


def osm_route_refs(spec, ctx):
    """Route RELATIONS and distinct REFS per mode, inside a bbox.

    Exists because Barcelona's brief recorded its 54 OSM relations as
    subway 28 / tram 22 / funicular 4 when the truth is tram 20 / funicular 6.
    Two relations sat in the wrong column and the total still summed to 54, so
    no arithmetic on that table could catch it - only re-measuring the parts.
    A breakdown that adds up is not a breakdown that is correct.

    It reports BOTH counts because they fail in opposite directions, and one
    city can carry both failures at once. Barcelona's 28 subway relations must
    stay 14 refs, because L9 and L10 each run as two disconnected segments and
    merging them would draw track that does not exist; its 6 funicular
    relations are plain directional pairs that must collapse to 3. Madrid's 28
    relations collapse to 13. Counting relations answers neither question -
    refs are what gets drawn, which is why `osm-rail`'s rule is to look at
    them.
    """
    south, west, north, east = spec["bbox"]
    kinds = list(spec.get("routes")
                 or ("subway", "tram", "funicular", "light_rail"))
    query = (
        "[out:json][timeout:180];"
        '(relation["type"="route"]["route"~"^(' + "|".join(kinds) + ')$"]'
        f"({south},{west},{north},{east}););out tags;")
    elements, host = _overpass(query)

    relations, refs = {}, {}
    for el in elements:
        tags = el.get("tags", {})
        kind = tags.get("route", "?")
        relations[kind] = relations.get(kind, 0) + 1
        refs.setdefault(kind, set()).add(tags.get("ref") or "<no ref>")

    got_relations = {k: relations.get(k, 0) for k in kinds}
    got_refs = {k: len(refs.get(k, ())) for k in kinds}
    detail = (f"via {host}: relations {json.dumps(got_relations)}, "
              f"distinct refs {json.dumps(got_refs)}")

    bad = []
    for label, got, want in (("relations", got_relations,
                              spec.get("expect_relations")),
                             ("refs", got_refs, spec.get("expect_refs"))):
        for kind, expected in (want or {}).items():
            if got.get(kind, 0) != expected:
                bad.append(f"{kind} {label}: got {got.get(kind, 0)}, "
                           f"expected {expected}")

    # The refs themselves, where the brief names them - a count can stay right
    # while the network changes underneath it.
    for kind, wanted in (spec.get("require_refs") or {}).items():
        missing = sorted(set(wanted) - refs.get(kind, set()))
        if missing:
            bad.append(f"{kind} missing ref(s) {', '.join(missing)}")

    if not bad:
        return True, detail

    # A MISMATCH IS NOT YET A FINDING. Overpass returns partial answers with
    # HTTP 200 and no `remark`, so a low count is ambiguous between "OSM
    # changed" and "that host truncated". This project's own rule - a negative
    # from one method is ASSERTED until two methods agree - applies exactly:
    # confirm against a DIFFERENT mirror before failing the brief.
    try:
        second, other = _overpass(query, _skip=(host,))
    except Exception as exc:
        return False, (detail + " - MISMATCH: " + "; ".join(bad)
                       + f" [UNCONFIRMED: no second mirror to check against - {exc}]")

    second_rel = {k: 0 for k in kinds}
    for el in second:
        k = el.get("tags", {}).get("route", "?")
        if k in second_rel:
            second_rel[k] += 1
    if second_rel != got_relations:
        return False, (
            detail + f" - MIRRORS DISAGREE: {host} {json.dumps(got_relations)} "
            f"vs {other} {json.dumps(second_rel)}. One of them truncated, so "
            f"this is a HOST problem, not a brief to correct. Re-run.")
    return False, (detail + " - MISMATCH: " + "; ".join(bad)
                   + f" [confirmed by {other}]")


def row_count(spec, ctx):
    """A COUNT the brief states, against a committed output file.

    WHY THIS KIND EXISTS. Every other check here tests LIVENESS - a URL
    resolves, a feed carries a file, a layer has fields. None of them can see a
    stale NUMBER, and on 2026-09-23 that gap cost real work: Paris's brief was
    re-verified 7/7 against live sources that morning, and by the afternoon the
    build had found "77 stations outside the commune" was 76 and "322 total"
    was 321. Both checks passed the whole time, because no check stood behind
    any count in the file.

    `CLAUDE.md` asks that writing a claim and writing its test be one act. A
    brief full of measured numbers and no numeric check is that rule half
    applied.

    DELIBERATELY LOCAL AND OFFLINE. It reads `outputs/`, which is committed, so
    it runs on a fresh clone with no network and costs nothing. The
    register-scale numbers (Paris's 149,166 bucket rows) are NOT checkable this
    way - re-reading a 2,210 MB parquet is not something a brief check may do -
    and those stay guarded by step 2's own printed filters instead. Claiming
    otherwise would be worse than the gap.

    Spec:
      path       repo-relative file, normally under outputs/
      expect     the number the brief states
      tolerance  allowed drift, default 0
      column     optional: count over this column rather than rows
      distinct   with `column`: count DISTINCT values instead of rows
      equals     with `column`: count rows whose value equals this
    """
    import csv

    path = ROOT / spec["path"]
    if not path.exists():
        return False, (f"{spec['path']} does not exist - a count cannot be "
                       f"checked against a file the build has not written")
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    col = spec.get("column")
    if col:
        if rows and col not in rows[0]:
            return False, (f"column {col!r} not in {spec['path']} "
                           f"(has {list(rows[0])[:6]})")
        values = [r[col] for r in rows]
        if spec.get("distinct"):
            got, what = len(set(values)), f"distinct {col}"
        elif "equals" in spec:
            got = sum(1 for v in values if v == spec["equals"])
            what = f"rows where {col} == {spec['equals']!r}"
        else:
            got, what = len(values), f"rows (over {col})"
    else:
        got, what = len(rows), "rows"

    expect, tol = spec["expect"], spec.get("tolerance", 0)
    ok = abs(got - expect) <= tol
    detail = f"{got:,} {what}, brief says {expect:,}"
    if tol:
        detail += f" (tolerance {tol:,})"
    if not ok:
        detail += (f" - DRIFT of {got - expect:+,}. Correct the brief to the "
                   f"measured number; do not widen the tolerance.")
    return ok, detail


CHECKS = {
    "http_ok": http_ok,
    "row_count": row_count,
    "http_contains": http_contains,
    "endpoint_absent": endpoint_absent,
    "arcgis_layer": arcgis_layer,
    "gtfs_files": gtfs_files,
    "gtfs_feed_window": gtfs_feed_window,
    "gtfs_calendar_window": gtfs_calendar_window,
    "gtfs_route_type_counts": gtfs_route_type_counts,
    "gtfs_stations": gtfs_stations,
    "ckan_rows": ckan_rows,
    "ckan_fields": ckan_fields,
    "socrata_count": socrata_count,
    "socrata_distinct_split": socrata_distinct_split,
    "taxonomy_catchall": taxonomy_catchall,
    "geojson_area_km2": geojson_area_km2,
    "utm_zone_from_longitude": utm_zone_from_longitude,
    "osm_route_refs": osm_route_refs,
}


# --- driver ---------------------------------------------------------------

def compare_to_config(city, specs):
    """Diff a brief's declared expectations against the BUILT city's config.

    `brief_check` otherwise tests a brief against the live sources - which is
    what it is for, and is not the same claim as "the brief matches the build".
    Toronto proved the difference: its checks reported 9/9 while expecting 111
    stations where the build produced 110, because they encoded the strip
    patterns the build had since improved on. **A check can only test what it
    encodes.**

    A spec opts in with a `vs_config` map of {its own field: CONFIG_CONSTANT}.
    """
    import importlib
    # Invalidated because this tool READS a file that was probably just edited,
    # and a stale .pyc gives a confidently wrong answer. Seen while building
    # this: the config on disk said 110, the check reported 111 and FAILED
    # against a correct file. Same class as everything else this tool exists
    # for - an instrument that has not been checked is not evidence.
    importlib.invalidate_caches()
    try:
        config = importlib.import_module(f"pipeline.{city}.config")
    except ModuleNotFoundError:
        return None, [f"  no pipeline/{city}/config.py - not built yet, so "
                      f"there is nothing to diff against"]
    lines, bad = [], 0
    checked = 0
    for spec in specs:
        for field, const in (spec.get("vs_config") or {}).items():
            checked += 1
            want = spec.get(field)
            got = getattr(config, const, "<missing>")
            if want == got:
                lines.append(f"  OK   {const} = {got} (brief {field})")
            else:
                bad += 1
                lines.append(f"  DIFF {const} = {got}, but the brief's "
                             f"{field} says {want}")
    if not checked:
        lines.append(f"  no vs_config mappings declared in {city}'s checks - "
                     f"add them to the fields a build sets a constant for")
    return bad == 0, lines


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
    ap.add_argument("--vs-config", action="store_true",
                    help="diff the brief against the BUILT city's config "
                         "constants instead of against live sources")
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
        if args.vs_config:
            # Not a live check. This asks a different question: does the brief
            # still describe the city that was actually BUILT? Toronto's checks
            # reported 9/9 while expecting 111 stations against a build
            # producing 110, because a check can only test what it encodes.
            ok, lines = compare_to_config(path.stem, specs)
            for line in lines:
                print(line)
            total += 1
            if ok is False:
                failed += 1
            continue
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
