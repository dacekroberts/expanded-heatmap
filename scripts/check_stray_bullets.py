"""Find a dash that the app will draw as a stray bullet.

    python scripts/check_stray_bullets.py            # the docs the app renders
    python scripts/check_stray_bullets.py --list     # which docs those are
    python scripts/check_stray_bullets.py --all      # every doc under docs/ (not in the hook)
    python scripts/check_stray_bullets.py --file PATH [PATH ...]

WHY. Markdown lets a bullet list interrupt a paragraph. A sentence that uses
a spaced hyphen as its dash ("the city - its data") and wraps just before the
hyphen puts `- ` at the start of a line, and the app draws a bullet in the
middle of the paragraph. Three reached docs/excluded_categories.md
(2026-09-27), each fixed by moving the dash up a line.

THE SHAPE. A line starting `- `, `* ` or `+ ` (up to three spaces in, after
any blockquote marker), in a paragraph that did not start as a list, whose
previous line ends mid-sentence: not in `.`, `:`, `!`, `?` or `;` (before any
closing `*`, `_`, `)`, quote or backtick), and not bold from end to end (a
lead-in such as "**What they say**"). A bullet after a blank line, a heading,
a table, a list item or a lead-in sentence is a list its author meant.

SCOPE. Only the documents the app renders. They are found by reading app/ for
string constants that name a file or a folder under docs/ (data_sources.md,
its per-country folder and excluded_categories.md when this was written), so a
new page that renders a document brings it into scope with no edit here. An
empty scope is a failure, not a pass. GitHub draws the same bullet, which is
what `--all` is for; it is a report, not a gate.

Exit 1 on any stray bullet, or when the scope comes back empty.
"""

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

QUOTE = re.compile(r"^(\s*>\s?)+")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
ITEM = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s")
BULLET = re.compile(r"^ {0,3}[-*+]\s")
LEAD_IN = re.compile(r"""[.:!?;][*_)"'`\]]*$""")
ALL_BOLD = re.compile(r"\*\*.+\*\*")


def rendered_docs():
    """Every docs/ file or folder of .md files that a string constant in app/ names."""
    found = set()
    for py in sorted((ROOT / "app").rglob("*.py")):
        for node in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
                continue
            name = node.value
            if not name.strip(" ./") or "\n" in name or len(name) > 100:
                continue
            path = DOCS / name
            try:
                if path.is_file() and path.suffix == ".md":
                    found.add(path)
                elif path.is_dir() and path != DOCS:
                    found.update(path.glob("*.md"))
            except OSError:            # a constant that is not a legal path
                continue
    return sorted(found)


def stray_bullets(text):
    """[(line number, previous line, bullet line)] for each stray bullet."""
    out = []
    fence = in_list = False
    prev = ""
    for n, raw in enumerate(text.split("\n"), 1):
        line = QUOTE.sub("", raw)
        if FENCE.match(line):
            fence, prev, in_list = not fence, "", False
            continue
        if fence:
            continue
        if not line.strip() or line.lstrip().startswith(("#", "|")):
            prev, in_list = "", False
            continue
        if ITEM.match(line):
            p = prev.strip()
            if (p and not in_list and BULLET.match(line)
                    and not LEAD_IN.search(p) and not ALL_BOLD.fullmatch(p)):
                out.append((n, p, line.strip()))
            in_list = True
        prev = line
    return out


def show(path):
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", nargs="+", type=Path, help="check these files instead")
    ap.add_argument("--all", action="store_true", help="every .md under docs/")
    ap.add_argument("--list", action="store_true", help="print the docs in scope and stop")
    args = ap.parse_args()

    if args.file:
        paths = args.file
    elif args.all:
        paths = sorted(DOCS.rglob("*.md"))
    else:
        paths = rendered_docs()
    if not paths:
        print("PROBLEM  no document in scope: app/ names no file or folder under docs/ - "
              "the way pages load their documents changed; update rendered_docs()")
        return 1
    if args.list:
        for p in paths:
            print(show(p))
        return 0

    problems = 0
    for path in paths:
        for n, prev, line in stray_bullets(path.read_text(encoding="utf-8")):
            problems += 1
            print(f"PROBLEM  {show(path)}:{n}: this line renders as a stray bullet - move "
                  f"its dash up a line\n      previous line ends {prev[-40:]!r}\n"
                  f"      this line starts {line[:60]!r}")
    if problems:
        print(f"\n{problems} stray bullet(s) in {len(paths)} document(s). A line that "
              "starts with a dash continues a sentence, so markdown starts a list there.")
        return 1
    print(f"OK - no stray bullet in {len(paths)} document(s)")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
