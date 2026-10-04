"""The project's authorship marks: small, invisible markers in every rendered
map and app page that tie a copy back to this pipeline (owner, 2026-10-04).

    python scripts/fingerprint.py init                  # once: make the secret key (outside the repo)
    python scripts/fingerprint.py table                 # rewrite pipeline/fingerprint_marks.json (needs the key)
    python scripts/fingerprint.py coverage              # every map and page carries its mark (no key; check_all)
    python scripts/fingerprint.py verify <file or URL>  # is this copy ours? (needs the key)

HOW IT WORKS. A mark reads `ehm:v1:<id>:<check>`. The id is stable
(`map/<slug>` for a map, `page/<City name>` for a city page, `site` for every
other page); the check is the first 16 hex digits of HMAC-SHA256(key, id). The
key is 32 random bytes kept OUTSIDE the repository, in the owner's profile
(`~/.ehm/fingerprint.key`, or the path in EHM_KEY_FILE), and is never printed,
committed or read into a conversation. The checks themselves are committed
(pipeline/fingerprint_marks.json), so rendering never needs the key: any
worktree, a fresh clone and Streamlit Cloud render the same marks. Only
`verify` needs it: a mark whose check matches the key could only have been
made by its holder, and the repository's history dates it. The public part
(`ehm:v1`) can be copied; the check cannot be produced for a new id without
the key.

WHERE THE MARKS GO (pipeline/map_common.py, app/components.py):
  maps   an HTML comment and a <meta name="generator"> in <head>, and a hidden
         element carrying data-ehm, in every outputs/<slug>/heatmap.html
  pages  a hidden span carrying data-ehm in the footer render_site_notices()
         draws on every page

WHAT IT NEVER DOES: change a coordinate, a count, a name or any visible text,
or put an invisible character in text a reader copies. Marks are metadata only.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "pipeline" / "fingerprint_marks.json"
KEY_FILE = Path(os.environ.get("EHM_KEY_FILE", Path.home() / ".ehm" / "fingerprint.key"))
VERSION = "ehm:v1"
MARK = re.compile(r"ehm:v1:([^:\"'<>\s]+):([0-9a-f]{16})")


def _key():
    if not KEY_FILE.exists():
        sys.exit(f"no key at {KEY_FILE}: run `python scripts/fingerprint.py init` on the owner's machine")
    return KEY_FILE.read_bytes()


def check_value(key, ident):
    return hmac.new(key, ident.encode("utf-8"), hashlib.sha256).hexdigest()[:16]


def ids():
    """Every id a mark is made for: each city's map and page, and the site."""
    sys.path.insert(0, str(ROOT / "app"))
    from cities import CITIES  # noqa: E402
    out = ["site"]
    for c in CITIES:
        out.append(f"page/{c['name']}")
    for d in sorted((ROOT / "outputs").iterdir()):
        if (d / "heatmap.html").exists():
            out.append(f"map/{d.name}")
    return out


def cmd_init():
    if KEY_FILE.exists():
        print(f"key already present at {KEY_FILE} (left as is)")
        return
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_bytes(secrets.token_bytes(32))
    print(f"key written to {KEY_FILE}. Back this file up somewhere private: "
          "without it no mark can be verified or made for a new city.")


def cmd_table():
    key = _key()
    table = {i: check_value(key, i) for i in ids()}
    TABLE.write_bytes((json.dumps(table, indent=1, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
    print(f"wrote {TABLE.relative_to(ROOT)}: {len(table)} marks")


def cmd_coverage():
    """No key needed: every id has a check in the table, every map file
    carries its own mark, and the footer code draws the page marks."""
    problems = []
    table = json.loads(TABLE.read_text(encoding="utf-8")) if TABLE.exists() else {}
    want = ids()
    missing = [i for i in want if i not in table]
    if missing:
        problems.append(f"{len(missing)} id(s) with no mark in {TABLE.name} (run `table`): "
                        + ", ".join(missing[:8]))
    maps = [i for i in want if i.startswith("map/")]
    marked = 0
    for i in maps:
        text = (ROOT / "outputs" / i[4:] / "heatmap.html").read_text(encoding="utf-8", errors="replace")
        good = table.get(i) and f"{VERSION}:{i}:{table[i]}" in text and VERSION in text
        marked += bool(good)
        if not good:
            problems.append(f"{i}: no valid mark in its heatmap.html (re-render it)")
    comp = (ROOT / "app" / "components.py").read_text(encoding="utf-8")
    if "fingerprint_mark(" not in comp:
        problems.append("app/components.py draws no page mark")
    print(f"maps marked: {marked} of {len(maps)}; page ids in the table: "
          f"{sum(1 for i in want if i.startswith('page/') and i in table)} of "
          f"{sum(1 for i in want if i.startswith('page/'))}")
    if problems:
        print("\n".join("  " + p for p in problems[:40]))
        sys.exit(1)
    print("OK - every map and page carries its mark.")


def cmd_verify(target):
    key = _key()
    if re.match(r"https?://", target):
        req = urllib.request.Request(target, headers={"User-Agent": "expanded-heatmap fingerprint verify"})
        text = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    else:
        text = Path(target).read_text(encoding="utf-8", errors="replace")
    found = MARK.findall(text)
    if not found:
        print("no ehm:v1 mark found")
        sys.exit(1)
    for ident, check in sorted(set(found)):
        ok = hmac.compare_digest(check, check_value(key, ident))
        print(f"  {'VALID  ' if ok else 'INVALID'}  {ident}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "init":
        cmd_init()
    elif args[0] == "table":
        cmd_table()
    elif args[0] == "coverage":
        cmd_coverage()
    elif args[0] == "verify" and len(args) == 2:
        cmd_verify(args[1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
