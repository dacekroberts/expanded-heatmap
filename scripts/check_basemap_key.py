"""Does every CARTO address in the macro map's style carry the key?

    python scripts/check_basemap_key.py

CARTO's Basemap Terms (2026-09-29, s3.b) allow its basemap free only with a
CARTO-issued key, and app/basemap.py writes that key into every address of a
committed Positron style. A request that lost the key would still load, so
nothing on screen would show it. This check builds the style with a stand-in
key (never the real one: st.secrets is not touched) and fails if:

  - any cartocdn address in the built style lacks `key=<stand-in>`;
  - the source lists no tile URLs of its own (CARTO's TileJSON hands back
    keyless ones, measured 2026-10-02);
  - the credit lacks the OSM copyright, CARTO attribution or OpenMapTiles link;
  - app/Overview.py names a CARTO style itself (`map_style="light"` or a
    cartocdn address), which would load keyless.

Offline, and it reads no secret. The browser half (every request keyed, every
response 200) is a render check: docs/decisions_drafts/ for this branch.
"""
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

import basemap  # noqa: E402

STAND_IN = "CHECK-STAND-IN-KEY"
problems = []


def strings(node, path="$"):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


url = basemap._style_data_url(STAND_IN)
prefix = "data:application/json;base64,"
if not url.startswith(prefix):
    problems.append(f"the style is not a base64 JSON data: URL ({url[:40]}...)")
else:
    style = json.loads(base64.b64decode(url[len(prefix):]).decode("utf-8"))
    carto = [(p, s) for p, s in strings(style) if "cartocdn" in s]
    if not carto:
        problems.append("the built style names no cartocdn address at all")
    for p, s in carto:
        if not re.search(r"[?&]key=" + re.escape(STAND_IN) + r"(&|$)", s):
            problems.append(f"{p} has no key: {s}")
    for name, src in style["sources"].items():
        if not src.get("tiles"):
            problems.append(f"source {name!r} lists no tiles of its own; the TileJSON's are keyless")
        credit = src.get("attribution", "")
        for href in ("https://www.openstreetmap.org/copyright",
                     "https://carto.com/attribution/", "https://openmaptiles.org/"):
            if f'href="{href}"' not in credit:
                problems.append(f"source {name!r} credit has no link to {href}")

overview = (ROOT / "app" / "Overview.py").read_text(encoding="utf-8")
if re.search(r"map_style\s*=\s*[\"']", overview):
    problems.append("app/Overview.py passes a literal map_style; a CARTO name loads keyless")
if "cartocdn" in overview:
    problems.append("app/Overview.py names a cartocdn address; the style comes from app/basemap.py")

if problems:
    print(f"PROBLEMS {len(problems)}")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print(f"OK - {len(carto)} CARTO addresses in the built style, every one keyed; "
      "credit links OSM, CARTO and OpenMapTiles")
