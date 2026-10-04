"""Check (and where a script may, download) Brussels (Regional)'s inputs. Not a
step: the steps read these caches only.

    python pipeline/brussels_regional/fetch_sources.py [--refetch-best]

  * KBO/BCE Open Data's full file (FPS Economy). **Never fetched here**: the
    portal needs the owner's login, so the owner places the zip in
    `data/belgium/raw/` and this script checks it against the sha256 its meta
    JSON records, refusing otherwise. A new extract is the owner's act, at
    least yearly (the license's article 10.5; next by config.KBO_DOWNLOAD_DUE).
  * BeST-Address Brussels (FPS BOSA, CC BY 4.0), checked likewise;
    `--refetch-best` downloads it again (named in the brief, so pre-permitted;
    a new file means re-running step 2's control).
  * STIB-MIVB's feed and the Region's commune limits are the Brussels page's
    downloads (`pipeline/brussels/fetch_sources.py`).

Writes outputs/brussels_regional/provenance.json (file, bytes, sha256, source).
"""
import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.brussels_regional import config  # noqa: E402
from pipeline.countries.belgium import BEST_BRUSSELS_ZIP, KBO_ZIP  # noqa: E402

UA = {"User-Agent": "expanded-heatmap city build (github.com/dacekroberts/expanded-heatmap)"}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _meta(path):
    m = path.with_name(path.name + ".json")
    if not m.exists():
        sys.exit(f"{m.name} missing: the recorded sha256 for {path.name} is gone")
    return json.loads(m.read_text(encoding="utf-8"))


def check(path, what):
    """The file's bytes and sha256 against its meta JSON; exits on a mismatch."""
    if not path.exists():
        sys.exit(f"{path} missing: {what}")
    meta = _meta(path)
    digest = _sha256(path)
    if digest != meta["sha256"] or path.stat().st_size != meta["bytes"]:
        sys.exit(f"{path.name}: sha256 or size differs from {path.name}.json - {what}")
    print(f"  OK {path.name}: {meta['bytes']:,} bytes, sha256 {digest[:12]}...")
    return {"file": path.name, "bytes": meta["bytes"], "sha256": digest,
            "source": meta.get("url") or meta.get("source"),
            "retrieved": meta.get("fetched") or meta.get("placed")}


def refetch_best():
    tmp = BEST_BRUSSELS_ZIP.with_suffix(".zip.part")
    req = urllib.request.Request(config.BEST_URL, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(tmp, "wb") as f:
        while block := r.read(1 << 20):
            f.write(block)
    with open(tmp, "rb") as f:
        if f.read(4) != b"PK\x03\x04":
            tmp.unlink()
            sys.exit("BeST: the download is not a zip; nothing replaced")
    tmp.replace(BEST_BRUSSELS_ZIP)
    meta = {"url": config.BEST_URL,
            "fetched": datetime.now(timezone.utc).date().isoformat(),
            "bytes": BEST_BRUSSELS_ZIP.stat().st_size, "sha256": _sha256(BEST_BRUSSELS_ZIP),
            "licence_stated": "CC BY 4.0, FPS BOSA"}
    BEST_BRUSSELS_ZIP.with_name(BEST_BRUSSELS_ZIP.name + ".json").write_bytes(
        json.dumps(meta).encode("utf-8"))
    print(f"  BeST re-fetched: {meta['bytes']:,} bytes; re-run step 2 (its control)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refetch-best", action="store_true")
    args = ap.parse_args()
    if args.refetch_best:
        refetch_best()
    rec = {
        "kbo": check(KBO_ZIP, "the owner places KBO's full file (their own login at "
                              f"{config.KBO_PORTAL}); a script never fetches it"),
        "best": check(BEST_BRUSSELS_ZIP, "run this script with --refetch-best"),
        "stib_gtfs_and_communes": "pipeline/brussels/fetch_sources.py (the Brussels page's)",
        "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    config.PROVENANCE_JSON.parent.mkdir(parents=True, exist_ok=True)
    config.PROVENANCE_JSON.write_bytes((json.dumps(rec, indent=2) + "\n").encode("utf-8"))
    print(f"  -> {config.PROVENANCE_JSON}")


if __name__ == "__main__":
    main()
