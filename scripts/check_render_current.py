"""Every committed map carries every shared block the CURRENT renderer injects.

    python scripts/check_render_current.py            # every outputs/<city>/heatmap.html
    python scripts/check_render_current.py --list     # the blocks it derived, and why
    python scripts/check_render_current.py --file X   # one html file (for controls)

Exits non-zero naming each map that is missing a block, or carries an OLDER
version of one. Read-only; runs in the pipeline environment because it imports
pipeline/map_common.py.

WHY. A change to the shared renderer reaches a city only when that city's map
is re-rendered. On 2026-09-24 Oslo was built on a branch while the zoom-lag fix
landed on master, and Oslo's committed map shipped WITHOUT WHEEL_ZOOM_SCRIPT.
Only a full `drift_check.py --jobs 4` would have noticed, and nothing required
one on that merge. This is the cheap guard: seconds, no pipeline.

DERIVED, NOT LISTED. The blocks are read from map_common.py itself (every
module-level string named *_SCRIPT, *_HTML or *_CSS that the module also
references somewhere other than its own definition), so a block added later
is covered without editing this file. A hand-kept list is exactly what goes
stale.

WHOLE BLOCKS, NOT MARKERS. Each block is split at its per-city slots
(`__NAME__` tokens that render_heatmap() fills with .replace(), and `{field}`
slots that build_legend() fills with .format()), and EVERY fixed piece of at
least MIN_PIECE characters must appear verbatim in the map. So a map rendered
before a block was EDITED fails too, not only one that lacks it entirely.
`@@TOKEN@@` placeholders are resolved in Python before a block leaves the
module (THEME_TOGGLE_HTML asserts it), so they never reach here.

COMMENTS DO NOT COUNT (2026-09-27). Both the block and the map are compared
with comments stripped: `/* ... */`, `<!-- ... -->`, and whole lines that
start with `//`. Before this, editing only a comment in map_common.py failed
every committed map and forced a re-render of all 46
(docs/efficiency_review_2026-09-27.md, finding 4). A committed map may now
carry an older comment; that is harmless, because nothing executes it. A
trailing `code; // note` comment still counts, because stripping `//` in
mid-line would also cut every `https://`.

WHAT IT DOES NOT SEE: per-city options (a city's own label override, or
render_heatmap(animate_clusters=...)), and anything outside these blocks
(Folium's own markup, the data). That is drift_check.py's job; this is the fast
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
COMMENT = re.compile(r"/\*.*?\*/|<!--.*?-->|^[ \t]*//[^\n]*$", re.S | re.M)


def uncommented(text):
    """Text with comments removed - applied identically to blocks and maps."""
    return COMMENT.sub("", text.replace("\r\n", "\n"))


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
        text = uncommented(value)
        pieces = [p.strip() for p in SLOT.split(text)]
        blocks.append((name, [p for p in pieces if len(p) >= MIN_PIECE]))
    if not blocks:
        sys.exit("derived no blocks from map_common.py - the naming rule no "
                 "longer matches anything, so this check would pass vacuously")
    # A piece that is a substring of ANOTHER block's text cannot tell the two
    # apart: every script block opens `<script> (function () { var NAME = "`,
    # so Oslo's pre-wheel map once read as an "OLDER version" of
    # WHEEL_ZOOM_SCRIPT, through LABEL_CLAMP_SCRIPT's matching opening. Only
    # distinctive pieces count.
    texts = {name: uncommented(vars(map_common)[name]) for name, _ in blocks}
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
    html = uncommented(path.read_text(encoding="utf-8"))
    problems = []
    for name, pieces in blocks:
        missing = [p for p in pieces if p not in html]
        if len(missing) == len(pieces):
            # A CONDITIONAL block (map_common.CONDITIONAL_BLOCKS) goes only into
            # the maps that need it (DENSE_LABEL_SCRIPT into a map whose
            # labels used the wide tier), so its absence is not staleness. What
            # this cannot see is a map that SHOULD have it and was rendered
            # before it existed; when it was added (2026-09-29) that was Osaka
            # alone, re-rendered with it. drift_check.py sees the rest.
            if name in map_common.CONDITIONAL_BLOCKS:
                continue
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
            where = "  (conditional)" if name in map_common.CONDITIONAL_BLOCKS else ""
            print(f"  {name:24s} {len(pieces):3d} fixed pieces{where}")
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
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py
    # crashed on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
