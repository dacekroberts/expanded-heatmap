"""Every committed map carries every shared block the CURRENT renderer injects.

    python scripts/check_render_current.py            # every outputs/<city>/heatmap.html
    python scripts/check_render_current.py --list     # the blocks it derived, and why
    python scripts/check_render_current.py --file X   # one html file (for controls)

Exits non-zero naming each map that is missing a block, or carries an OLDER
version of one. Read-only; runs in the pipeline environment because it imports
pipeline/map_common.py.

WHY. A change to the shared renderer reaches a city only when that city's map
is re-rendered. On 2026-09-24 Oslo was built on a branch while the zoom-lag fix
landed on master, and Oslo's committed map shipped WITHOUT WHEEL_ZOOM_SCRIPT
until the zoom session happened to re-render it. Only a full
`drift_check.py --jobs 4` would have noticed, and nothing required one on that
merge. This is the cheap guard, proposed by that session: seconds, no pipeline.

DERIVED, NOT LISTED. The blocks are read from map_common.py itself - every
module-level string named *_SCRIPT, *_HTML or *_CSS that the module also
references somewhere other than its own definition - so a block added next
month is covered without editing this file. A hand-kept list is exactly what
goes stale.

WHOLE BLOCKS, NOT MARKERS. Each block is split at its per-city slots -
`__NAME__` tokens that render_heatmap() fills with .replace(), and `{field}`
slots that build_legend() fills with .format() - and EVERY fixed piece of at
least MIN_PIECE characters must appear verbatim in the map. So a map rendered
before a block was EDITED fails too, not only one that lacks it entirely.
`@@TOKEN@@` placeholders are resolved in Python before a block leaves the
module (THEME_TOGGLE_HTML asserts it), so they never reach here.

WHAT IT DOES NOT SEE: per-city options (a city's own label override, or
render_heatmap(animate_clusters=...)), and anything outside these blocks -
Folium's own markup, the data. That is drift_check.py's job; this is the fast
subset that catches the one failure a merge makes easy.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import map_common  # noqa: E402

SOURCE = (ROOT / "pipeline" / "map_common.py").read_text(encoding="utf-8")
NAME = re.compile(r"^_?[A-Z][A-Z0-9_]*_(SCRIPT|HTML|CSS)$")
SLOT = re.compile(r"__[A-Z][A-Z0-9_]*__|\{[a-z_]+\}")
MIN_PIECE = 20


def shared_blocks():
    """(name, pieces) for every injected block, derived from map_common.py."""
    blocks = []
    for name, value in vars(map_common).items():
        if not (NAME.match(name) and isinstance(value, str)):
            continue
        # Referenced beyond its own assignment: defined-but-unused text is not
        # injected, and requiring it would be a false failure.
        uses = len(re.findall(rf"\b{re.escape(name)}\b", SOURCE))
        if uses < 2:
            continue
        text = value.replace("\r\n", "\n")
        pieces = [p.strip() for p in SLOT.split(text)]
        blocks.append((name, [p for p in pieces if len(p) >= MIN_PIECE]))
    if not blocks:
        sys.exit("derived no blocks from map_common.py - the naming rule no "
                 "longer matches anything, so this check would pass vacuously")
    # A piece that is a substring of ANOTHER block's text cannot tell the two
    # apart: every script block opens `<script> (function () { var NAME = "`,
    # so the first control run called Oslo's pre-wheel map an "OLDER version"
    # of WHEEL_ZOOM_SCRIPT when it had never had one - that boilerplate piece
    # matched LABEL_CLAMP_SCRIPT's opening. Only distinctive pieces count.
    texts = {name: vars(map_common)[name] for name, _ in blocks}
    distinct = []
    for name, pieces in blocks:
        # A FRAGMENT pasted whole into another block (_LEGEND_BOTTOM_CSS lives
        # inside LEGEND_HTML) is checked as part of its container.
        if any(texts[name] in t for other, t in texts.items() if other != name):
            continue
        mine = [p for p in pieces
                if not any(p in t for other, t in texts.items() if other != name)]
        if not mine:
            sys.exit(f"{name}: no fixed piece of {MIN_PIECE}+ characters that is "
                     f"unique to it - give the block a distinctive line.")
        distinct.append((name, mine))
    return distinct


def preview(piece):
    """The first line of a piece that says something, for the report."""
    for line in piece.splitlines():
        if sum(ch.isalnum() for ch in line) >= 10:
            return line.strip()[:70]
    return piece[:70]


def check_file(path, blocks):
    html = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    problems = []
    for name, pieces in blocks:
        missing = [p for p in pieces if p not in html]
        if len(missing) == len(pieces):
            problems.append(f"{name} is MISSING")
        elif missing:
            problems.append(f"{name} is an OLDER version ({len(missing)} of "
                            f"{len(pieces)} pieces differ; first: "
                            f"{preview(missing[0])!r})")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--file", type=Path)
    args = ap.parse_args()
    blocks = shared_blocks()

    if args.list:
        for name, pieces in blocks:
            print(f"  {name:24s} {len(pieces):3d} fixed pieces")
        return 0

    files = [args.file] if args.file else sorted(ROOT.glob("outputs/*/heatmap.html"))
    bad = 0
    for f in files:
        problems = check_file(f, blocks)
        label = f.parent.name if not args.file else str(f)
        for p in problems:
            print(f"  STALE  {label:16s} {p}")
        bad += bool(problems)
    if bad:
        print(f"\n{bad} of {len(files)} map(s) were not rendered by the current "
              f"map_common.py. Re-render: python pipeline/<city>/step*_map.py, "
              f"or python pipeline/drift_check.py <city>.")
        return 1
    print(f"OK - {len(files)} map(s) carry all {len(blocks)} shared blocks, "
          f"current versions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
