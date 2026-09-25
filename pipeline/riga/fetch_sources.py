"""Download everything Riga's pipeline reads. NOT a step: drift_check.py never
runs this file, and every step exits naming it when its cache is missing.

    python pipeline/riga/fetch_sources.py

Each download is recorded in outputs/riga/provenance.json (bytes, sha256, the
retrieval time, and the portal's own last_modified for the resource).
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.riga import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = "expanded-heatmap (open-data portfolio map)"


def record(key, **fields):
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    prov[key] = fields
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")


def download(url, dest):
    """Stream to a temporary file, then rename - a 223 MB file must not be left
    half-written where a step would read it."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(4):
        try:
            with S.get(url, stream=True, timeout=600) as r:
                r.raise_for_status()
                h = hashlib.sha256()
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
                        h.update(chunk)
            tmp.replace(dest)
            return h.hexdigest()
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {e}")
            time.sleep(10 * (attempt + 1))


def resource_modified(url):
    """The portal's own last_modified for a resource URL (its id is in the path)."""
    rid = url.split("/resource/")[1].split("/")[0]
    try:
        res = S.get(config.CKAN_API + "resource_show", params={"id": rid}, timeout=60).json()["result"]
        return res.get("last_modified") or res.get("created")
    except (requests.RequestException, ValueError, KeyError):
        return None


def newest_gtfs():
    pkg = S.get(config.CKAN_API + "package_show", params={"id": config.GTFS_DATASET},
                timeout=60).json()["result"]
    res = [r for r in pkg["resources"] if "marsrutusaraksti" in (r.get("url") or "")]
    if not res:
        sys.exit("no marsrutusaraksti*.zip in Rīgas satiksme's dataset - re-read it")
    best = max(res, key=lambda r: r.get("last_modified") or r.get("created") or "")
    return best["url"], best.get("last_modified") or best.get("created")


def main():
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    now = lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")  # noqa: E731
    for key, (url, fname) in config.SOURCES.items():
        dest = config.DATA_RAW / fname
        sha = download(url, dest)
        size = dest.stat().st_size
        print(f"  {fname:34s} {size:>13,} bytes")
        record(key, file=fname, url=url, bytes=size, sha256=sha, retrieved=now(),
               last_modified=resource_modified(url))
    url, modified = newest_gtfs()
    sha = download(url, config.GTFS_ZIP)
    print(f"  {config.GTFS_ZIP.name:34s} {config.GTFS_ZIP.stat().st_size:>13,} bytes  ({url.rsplit('/', 1)[-1]})")
    record("gtfs", file=config.GTFS_ZIP.name, url=url, bytes=config.GTFS_ZIP.stat().st_size, sha256=sha,
           retrieved=now(), last_modified=modified)


if __name__ == "__main__":
    main()
