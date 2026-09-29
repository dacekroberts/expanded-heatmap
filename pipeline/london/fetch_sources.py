"""Download London's raw inputs into data/london/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/london/fetch_sources.py [--force]

The FSA's register: its authority list is read first and filtered to the
London region, then one bulk XML per authority. Each file must parse as XML
and carry its own authority's code, because a wrong URL can answer 200 with
an HTML page.
"""
import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.london import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, extra=None, timeout=600):
    req = urllib.request.Request(url, headers={**HEADERS, **(extra or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def authorities():
    data = json.loads(get(config.FSA_AUTHORITIES_URL, config.FSA_API_HEADERS))
    rows = [a for a in data["authorities"] if a.get("RegionName") == config.FSA_REGION]
    if len(rows) != config.FSA_AUTHORITY_COUNT:
        sys.exit(f"  the FSA lists {len(rows)} authorities in {config.FSA_REGION!r}, "
                 f"not {config.FSA_AUTHORITY_COUNT} - a scope change, read it first")
    keep = ("LocalAuthorityIdCode", "Name", "FileName", "LastPublishedDate",
            "EstablishmentCount")
    return [{k: a.get(k) for k in keep} for a in rows]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.FSA_RAW_DIR, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    auths = authorities()
    config.FSA_AUTHORITIES_JSON.write_text(json.dumps(auths, indent=1), encoding="utf-8")
    total = 0
    for a in auths:
        dest = config.FSA_RAW_DIR / f"{a['LocalAuthorityIdCode']}.xml"
        if dest.exists() and not args.force:
            total += dest.stat().st_size
            continue
        body = get(a["FileName"])
        root = ET.fromstring(body)
        codes = {e.text for e in root.iter("LocalAuthorityCode")}
        if codes and codes != {str(a["LocalAuthorityIdCode"])}:
            sys.exit(f"  {a['Name']}: file carries authority code(s) {codes}, "
                     f"expected {a['LocalAuthorityIdCode']}")
        dest.write_bytes(body)
        total += len(body)
        print(f"  {a['Name']:<28} {len(body):>11,} bytes  published {a['LastPublishedDate'][:10]}")
    print(f"  {len(auths)} authority files, {total:,} bytes in {config.FSA_RAW_DIR.relative_to(config.ROOT)}")

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fsa_authorities_url": config.FSA_AUTHORITIES_URL,
            "fsa_published": {a["Name"]: a["LastPublishedDate"][:10] for a in auths}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
