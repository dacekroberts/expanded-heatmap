"""Download Brussels's inputs. Not a step: the steps read these caches only.

    python pipeline/brussels/fetch_sources.py [--terms-only] [--force]

  * hub.brussels's shop inventory (City of Brussels, opendata.brussels.be,
    CC BY 4.0), named fields only: never `google_maps` or `google_street_view`.
  * The Region's commune limits (PARADIGM, CC0 1.0).
  * STIB-MIVB's static GTFS (Belgian Mobility Company portal, CC BY 4.0). Access
    is acceptance of the portal's terms: the download runs only while the terms
    page's text matches the hash recorded at the owner's acceptance
    (config.BMC_TERMS_TEXT_SHA256); `--terms-only` prints the current hash.

Writes outputs/brussels/provenance.json (URL, bytes, sha256, retrieval time).
"""
import argparse
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.brussels import config  # noqa: E402

UA = {"User-Agent": "expanded-heatmap city build (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read(), dict(r.headers)


def terms_text_hash():
    """sha256 of the terms page's visible text, whitespace collapsed."""
    raw, _ = _get(config.BMC_TERMS_URL)
    t = raw.decode("utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = " ".join(t.split())
    return hashlib.sha256(t.encode("utf-8")).hexdigest(), len(t)


def fetch_hub():
    q = urllib.parse.urlencode({"select": ",".join(config.HUB_FIELDS)})
    url = f"{config.ODS_BASE}/{config.HUB_DATASET}/exports/json?{q}"
    raw, _ = _get(url, timeout=300)
    rows = json.loads(raw.decode("utf-8"))
    cols = set().union(*(r.keys() for r in rows)) if rows else set()
    extra = cols - set(config.HUB_FIELDS)
    if extra:
        sys.exit(f"  hub: columns not asked for arrived: {sorted(extra)} - nothing written")
    if cols & set(config.HUB_NEVER):
        sys.exit("  hub: a Google link column arrived - nothing written")
    if len(rows) != config.HUB_EXPECTED_ROWS:
        sys.exit(f"  hub: {len(rows):,} rows, expected {config.HUB_EXPECTED_ROWS:,}: "
                 "a new survey or a failed export, re-measure before building")
    config.HUB_JSON.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    print(f"  hub: {len(rows):,} rows, {len(cols)} fields")
    return {"url": url, "page": config.HUB_PAGE, "records": len(rows),
            "bytes": config.HUB_JSON.stat().st_size, "sha256": _sha256(config.HUB_JSON),
            "retrieved": _now()}


def fetch_communes():
    url = f"{config.ODS_BASE}/{config.COMMUNES_DATASET}/exports/geojson"
    raw, _ = _get(url)
    gj = json.loads(raw.decode("utf-8"))
    n = len(gj.get("features", []))
    if n != 19:
        sys.exit(f"  communes: {n} features, expected the Region's 19")
    config.COMMUNES_GEOJSON.write_bytes(raw)
    print(f"  communes: {n} features")
    return {"url": url, "page": config.COMMUNES_PAGE, "features": n,
            "bytes": len(raw), "sha256": _sha256(config.COMMUNES_GEOJSON), "retrieved": _now()}


def fetch_gtfs(force):
    digest, n = terms_text_hash()
    if config.BMC_TERMS_TEXT_SHA256 is None:
        sys.exit(f"  BMC terms text sha256 {digest} ({n:,} chars): record it in "
                 "config.BMC_TERMS_TEXT_SHA256 at the owner's acceptance, then re-run")
    if digest != config.BMC_TERMS_TEXT_SHA256:
        sys.exit("  The Belgian Mobility Company's Terms of Use changed since the owner "
                 f"accepted them ({digest}). A re-fetch goes back to the owner; "
                 "nothing downloaded.")
    if config.GTFS_ZIP.exists() and not force:
        print(f"  gtfs: cached ({config.GTFS_ZIP.stat().st_size:,} bytes); --force re-fetches")
    else:
        raw, headers = _get(config.GTFS_URL, timeout=600)
        if raw[:2] != b"PK":
            sys.exit("  gtfs: the answer is not a zip - nothing written")
        config.GTFS_ZIP.write_bytes(raw)
        print(f"  gtfs: {len(raw):,} bytes")
    return {"url": config.GTFS_URL, "portal": config.BMC_PORTAL,
            "terms_text_sha256": digest, "bytes": config.GTFS_ZIP.stat().st_size,
            "sha256": _sha256(config.GTFS_ZIP),
            "file_utc": datetime.fromtimestamp(config.GTFS_ZIP.stat().st_mtime,
                                               timezone.utc).isoformat(timespec="seconds")}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--terms-only", action="store_true")
    ap.add_argument("--force", action="store_true", help="re-download the GTFS")
    args = ap.parse_args()
    if args.terms_only:
        digest, n = terms_text_hash()
        print(f"BMC terms text sha256 {digest} ({n:,} chars)")
        return
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("hub.brussels inventory (City of Brussels):")
    hub = fetch_hub()
    print("Commune limits (PARADIGM):")
    com = fetch_communes()
    print("STIB-MIVB GTFS (Belgian Mobility Company):")
    gtfs = fetch_gtfs(args.force)
    prov = {"written_utc": _now(), "hub": hub, "communes": com, "gtfs": gtfs}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
    print(f"provenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
