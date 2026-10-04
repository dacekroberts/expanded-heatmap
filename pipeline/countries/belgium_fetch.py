"""Downloads shared by the Belgian cities' fetch scripts.

Imported only by `pipeline/<city>/fetch_sources.py`, never by a step
(`scripts/check_no_fetch_in_steps.py`). One Overpass query per city, never in
parallel; `pipeline/osm.py` waits out the owner's minute after a 504 or 429.
"""
import json
import sys

from pipeline import osm
from pipeline.countries.belgium import NIS_TAG


def fetch_communes(bbox, cache_json, own_nis, force=False):
    """Every municipality relation in `bbox` (s, w, n, e), `out geom`, cached.

    Exits if the city's own NIS code is not among them: an empty or partial
    answer is a failed fetch, not a city with no boundary.
    """
    s, w, n, e = bbox
    q = ("[out:json][timeout:240];"
         f'relation["boundary"="administrative"]["admin_level"="8"]["{NIS_TAG}"]'
         f"({s},{w},{n},{e});out geom;")
    els, host = osm.fetch(q, cache_json, force=force)
    codes = {x.get("tags", {}).get(NIS_TAG) for x in els}
    if own_nis not in codes:
        sys.exit(f"  communes: NIS {own_nis} missing from the answer - a failed fetch")
    print(f"  communes: {len(els)} boundary relations via {host}")
    return host


# --- VKBO (Digitaal Vlaanderen), the WFS only --------------------------------

def _vkbo_filter(nis):
    return ('<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0"><fes:PropertyIsEqualTo>'
            '<fes:ValueReference>KBO_NISCODE</fes:ValueReference>'
            f'<fes:Literal>{nis}</fes:Literal></fes:PropertyIsEqualTo></fes:Filter>')


def fetch_vkbo(nis_codes, out_csv, meta_json, page=5000, pause_s=1.5, retries=3):
    """Every VKBO row filed under each NIS code, number, type, codes and point.

    The WFS with field selection, never the OGC API Features endpoint (it
    ignores `properties=` and returns every column, names included: the
    Antwerp brief). `numberMatched` caps at 10,000, so rows are counted by
    paging, sorted on OIDN so the pages do not overlap. A page carrying any
    property not asked for stops the fetch before anything is written.
    """
    import csv
    import hashlib
    import io
    import time
    from datetime import datetime, timezone

    import requests

    from pipeline.countries.belgium_favv import (VKBO_CRS_URN, VKBO_FIELDS, VKBO_SERVER_FIELDS,
                                                 VKBO_TYPENAME, VKBO_WFS)

    asked = VKBO_FIELDS + VKBO_SERVER_FIELDS
    allowed = set(asked)
    rows, per_nis, oids = [], {}, set()
    for nis in nis_codes:
        start, n_nis = 0, 0
        while True:
            params = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
                      "typeNames": VKBO_TYPENAME, "propertyName": ",".join(asked + ("SHAPE",)),
                      "filter": _vkbo_filter(nis), "sortBy": "OIDN", "count": str(page),
                      "startIndex": str(start), "outputFormat": "application/json"}
            for attempt in range(retries):
                try:
                    r = requests.get(VKBO_WFS, params=params, timeout=300,
                                     headers={"User-Agent": "expanded-heatmap"})
                    r.raise_for_status()
                    j = r.json()
                    break
                except (requests.RequestException, ValueError) as e:
                    if attempt == retries - 1:
                        sys.exit(f"  VKBO {nis} @ {start}: {type(e).__name__} after {retries} tries")
                    print(f"    VKBO {nis} @ {start}: {type(e).__name__}; waiting 60 s", flush=True)
                    time.sleep(60)
            crs = (j.get("crs") or {}).get("properties", {}).get("name")
            if crs != VKBO_CRS_URN:
                sys.exit(f"  VKBO answered in {crs}, not {VKBO_CRS_URN}")
            feats = j.get("features", [])
            for f in feats:
                extra = set(f.get("properties", {})) - allowed
                if extra:
                    sys.exit(f"  VKBO returned properties it was not asked for: {sorted(extra)} - "
                             f"nothing written. Never take a column that could carry a name.")
                p = f["properties"]
                oid = p.get("OIDN")
                if oid in oids:
                    sys.exit(f"  VKBO paging overlapped (OIDN repeated at {nis} @ {start})")
                oids.add(oid)
                g = f.get("geometry") or {}
                x, y = (g.get("coordinates") or [None, None])[:2]
                rows.append([p.get(k) for k in VKBO_FIELDS] + [x, y])
            n_nis += len(feats)
            print(f"    VKBO NIS {nis}: {n_nis:,} rows", flush=True)
            if len(feats) < page:
                break
            start += len(feats)
            time.sleep(pause_s)
        per_nis[nis] = n_nis
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(list(VKBO_FIELDS) + ["x", "y"])
    w.writerows(rows)
    data = buf.getvalue().encode("utf-8")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_csv.write_bytes(data)
    meta = {"url": VKBO_WFS, "typeNames": VKBO_TYPENAME,
            "propertyName": list(asked) + ["SHAPE"],
            "filter": {nis: _vkbo_filter(nis) for nis in nis_codes},
            "paging": {"count": page, "sortBy": "OIDN", "pause_s": pause_s},
            "crs": VKBO_CRS_URN,
            "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "rows": len(rows), "rows_per_nis": per_nis,
            "sha256": hashlib.sha256(data).hexdigest(),
            "note": "UIDN and OIDN are mandatory in the feature type (minOccurs 1), so the "
                    "server returns them whatever propertyName says; they are asked for "
                    "explicitly, used to page, and not stored."}
    meta_json.write_bytes(json.dumps(meta, indent=2).encode("utf-8"))
    print(f"  VKBO: {len(rows):,} rows ({per_nis}) -> {out_csv.name}")
    return meta


# --- De Lijn's GTFS ------------------------------------------------------------

# The copy staging's brief check fetched on 2026-10-03 (keyless, the Belgian
# Mobility portal), ratified by the owner on 2026-10-03 with the other build
# calls; the portal counts each access as accepting its terms, so a new
# download is the owner's call, made with --refresh-feed.
DELIJN_BRIEF_CACHE = ("data/_brief_check/raw/https___api-management-discovery-production"
                      ".azure-api.net_api_gtfs_feed_delijn_static.zip")
DELIJN_RATIFIED_SHA256 = "4b43c28120063a6ceb7a9de8bd0f913cfb58ad2d6a6b03b0cfab34d4e2159921"
DELIJN_RATIFIED_FETCHED = "2026-10-03"


def _sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _feed_window(path):
    import zipfile

    import pandas as pd
    with zipfile.ZipFile(path) as z:
        fi = pd.read_csv(z.open("feed_info.txt"), dtype=str, keep_default_na=False).iloc[0]
    return {k: fi[k].strip() for k in ("feed_start_date", "feed_end_date", "feed_version")}


def adopt_delijn_feed(root, refresh=False):
    """Put De Lijn's feed at data/belgium/raw/delijn_gtfs.zip with its meta JSON.

    Without `refresh`, the copy already there (its meta's sha256 matching) is
    kept, or the ratified 2026-10-03 copy is taken from the brief check's cache
    after its sha256 is checked. With `refresh`, the feed is downloaded from
    the portal (the owner's call: the portal's terms are accepted by access).
    """
    import shutil
    from datetime import datetime, timezone

    from pipeline.countries.belgium_delijn import FEED_META, FEED_URL, FEED_ZIP

    FEED_ZIP.parent.mkdir(parents=True, exist_ok=True)
    if refresh:
        import requests
        r = requests.get(FEED_URL, timeout=900, headers={"User-Agent": "expanded-heatmap"})
        r.raise_for_status()
        if len(r.content) < 50_000_000:
            sys.exit(f"  De Lijn feed: {len(r.content):,} bytes - a failed fetch, nothing written")
        FEED_ZIP.write_bytes(r.content)
        fetched, how = datetime.now(timezone.utc).isoformat(timespec="seconds"), "downloaded"
    elif FEED_ZIP.exists() and FEED_META.exists():
        meta = json.loads(FEED_META.read_text(encoding="utf-8"))
        if meta.get("sha256") == _sha256(FEED_ZIP):
            print(f"  De Lijn feed: kept ({meta['feed_version']}, fetched {meta['fetched']})")
            return meta
        sys.exit(f"  {FEED_ZIP.name} no longer matches its meta JSON - remove both and re-run")
    else:
        src = root / DELIJN_BRIEF_CACHE
        if not src.exists():
            sys.exit(f"  no De Lijn feed at {FEED_ZIP} and no ratified copy at {src}: a new "
                     f"download is the owner's call (--refresh-feed)")
        if _sha256(src) != DELIJN_RATIFIED_SHA256:
            sys.exit(f"  {src.name} is not the ratified 2026-10-03 copy (sha256 differs)")
        shutil.copyfile(src, FEED_ZIP)
        fetched, how = DELIJN_RATIFIED_FETCHED, f"copied from {DELIJN_BRIEF_CACHE}"
    meta = {"url": FEED_URL, "publisher": "De Lijn (Belgian Mobility Open Data Portal)",
            "fetched": fetched, "how": how, "bytes": FEED_ZIP.stat().st_size,
            "sha256": _sha256(FEED_ZIP), **_feed_window(FEED_ZIP)}
    FEED_META.write_bytes(json.dumps(meta, indent=2).encode("utf-8"))
    print(f"  De Lijn feed: {how}; {meta['feed_version']} ({meta['bytes']:,} bytes)")
    return meta


# --- FAVV's operator list ---------------------------------------------------------

FAVV_URL = "https://www.static.favv.be/bo-documents/inter_actieve_actoren_EN.csv"


def favv_list(refresh=False):
    """FAVV's list, cached at data/belgium/raw/ with its meta JSON (staging
    fetched it on 2026-10-03, Last-Modified 2026-09-28). Re-downloaded only
    with `refresh` (weekly upstream; a refresh moves every Flemish city's
    counts at once, so it is the lead's call)."""
    import hashlib
    from datetime import datetime, timezone

    from pipeline.countries.belgium import FAVV_CSV

    meta_path = FAVV_CSV.with_name(FAVV_CSV.name + ".json")
    if refresh:
        import requests
        r = requests.get(FAVV_URL, timeout=600, headers={"User-Agent": "expanded-heatmap"})
        r.raise_for_status()
        if len(r.content) < 20_000_000:
            sys.exit(f"  FAVV: {len(r.content):,} bytes - a failed fetch, nothing written")
        FAVV_CSV.write_bytes(r.content)
        meta = {"url": FAVV_URL, "publisher": "FAVV/AFSCA (Federal Agency for the Safety of "
                "the Food Chain)", "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "last_modified": r.headers.get("Last-Modified"), "bytes": len(r.content),
                "sha256": hashlib.sha256(r.content).hexdigest()}
        meta_path.write_bytes(json.dumps(meta, indent=2).encode("utf-8"))
    if not FAVV_CSV.exists() or not meta_path.exists():
        sys.exit(f"  no FAVV list at {FAVV_CSV}: --refresh-favv downloads it")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    # The file's own extract stamp ("Date aujourd'hui", one value per file),
    # which the page's caption gives; step 2 checks it is the only one.
    import pandas as pd
    first = pd.read_csv(FAVV_CSV, encoding="latin-1", dtype=str, nrows=1, usecols=[19])
    meta["extract_date"] = first.iloc[0, 0].split(" ")[0].replace("/", "-")
    print(f"  FAVV: {FAVV_CSV.name}, extract of {meta['extract_date']}, fetched "
          f"{meta['fetched']}, Last-Modified {meta['last_modified']}")
    return meta


def fetch_city(cfg, argv):
    """Everything one Flemish tram city reads, then its provenance.json.

    Flags: --refresh-feed (a new De Lijn download: the owner's call),
    --refresh-favv (a new FAVV list), --keep-vkbo (reuse the cached VKBO pages
    instead of re-paging the WFS, about 25 minutes for both cities)."""
    from datetime import datetime, timezone

    unknown = set(argv) - {"--refresh-feed", "--refresh-favv", "--keep-vkbo"}
    if unknown:
        sys.exit(f"unknown flag(s) {sorted(unknown)}")
    for d in (cfg.DATA_RAW, cfg.DATA_PROCESSED, cfg.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("De Lijn GTFS (Belgian Mobility Open Data Portal):")
    feed = adopt_delijn_feed(cfg.ROOT, refresh="--refresh-feed" in argv)
    print("\nFAVV-AFSCA operator list:")
    favv = favv_list(refresh="--refresh-favv" in argv)
    print("\nOpenStreetMap communes (the cache exists, so no query is sent):")
    host = fetch_communes(cfg.COMMUNES_BBOX, cfg.OSM_COMMUNES_JSON, cfg.OWN_NIS)
    print("\nVKBO (Digitaal Vlaanderen), WFS:")
    if "--keep-vkbo" in argv and cfg.VKBO_CSV.exists() and cfg.VKBO_META.exists():
        vkbo = json.loads(cfg.VKBO_META.read_text(encoding="utf-8"))
        print(f"  VKBO: kept, {vkbo['rows']:,} rows fetched {vkbo['fetched_utc']}")
    else:
        vkbo = fetch_vkbo(cfg.VKBO_NIS, cfg.VKBO_CSV, cfg.VKBO_META)
    prov = {"written_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "favv": {k: favv.get(k) for k in ("url", "extract_date", "fetched", "last_modified",
                                              "sha256")},
            "vkbo": {k: vkbo.get(k) for k in ("url", "typeNames", "propertyName", "fetched_utc",
                                              "rows", "rows_per_nis", "sha256")},
            "gtfs": {k: feed.get(k) for k in ("url", "fetched", "feed_start_date",
                                              "feed_end_date", "feed_version", "sha256")},
            "osm_communes": {"host": host, "bbox": cfg.COMMUNES_BBOX}}
    cfg.PROVENANCE_JSON.write_bytes(json.dumps(prov, indent=2).encode("utf-8"))
    print(f"\nprovenance -> {cfg.PROVENANCE_JSON.name}")
