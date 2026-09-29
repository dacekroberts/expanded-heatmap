"""Download SEMAS's 상가(상권)정보 ZIP (data.go.kr 15083033) into the country
cache data/korea/raw/. NOT imported by any step: steps read the cache through
pipeline/countries/korea_sbiz.py, and a step never fetches.

    python pipeline/countries/korea_sbiz_fetch.py [--force]

Keyless: data.go.kr serves the file with no account or key. If the answer is
not a ZIP - a CAPTCHA or a login page - the script stops; nothing is worked
around. The file id (atchFileId) changes with each quarterly edition: read the
new one from the dataset page's download link.
"""
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.korea_sbiz import PAGE, ZIP  # noqa: E402

URL = ("https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003695831"
       "&fileDetailSn=1&insertDataPrcus=N")


def main(force=False):
    if ZIP.exists() and not force:
        print(f"  {ZIP.name} cached ({ZIP.stat().st_size:,} bytes)")
        return
    ZIP.parent.mkdir(parents=True, exist_ok=True)
    tmp = ZIP.with_suffix(".part")
    req = urllib.request.Request(URL, headers={"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)",
                                               "Referer": PAGE})
    h, n = hashlib.sha256(), 0
    with urllib.request.urlopen(req, timeout=600) as r:
        disp = r.headers.get("Content-Disposition")
        first = r.read(4)
        if first != b"PK\x03\x04":
            sys.exit(f"not a ZIP ({r.headers.get('Content-Type')}) - stopped; nothing is worked around")
        with open(tmp, "wb") as fh:
            for chunk in iter(lambda: r.read(1 << 20), b""):
                if first:
                    fh.write(first)
                    h.update(first)
                    n += 4
                    first = b""
                fh.write(chunk)
                h.update(chunk)
                n += len(chunk)
    tmp.replace(ZIP)
    meta = {"dataset": "data.go.kr 15083033 소상공인시장진흥공단_상가(상권)정보", "page": PAGE, "url": URL,
            "bytes": n, "sha256": h.hexdigest(), "content_disposition": disp,
            "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "licence_declared": "이용허락범위 제한 없음"}
    ZIP.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {ZIP.name}: {n:,} bytes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main("--force" in sys.argv)
