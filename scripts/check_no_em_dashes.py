"""Fail on an em dash in any code comment: # comments, docstrings, and CSS/JS/
HTML comments inside string literals, in every tracked .py file.

    python scripts/check_no_em_dashes.py [--root PATH]

Visible text is out of scope: labels, captions, page prose, printed messages
and any other string that is not a comment. A comment that quotes a visible
label or a data value containing an em dash paraphrases it ("a dash",
"U+2014"); the label or value stays.

When it fails, reword with a colon, semicolon, comma, parentheses or a plain
spaced hyphen. Never an en dash or a double hyphen as a workaround.

Comments inside the CSS and JS strings of pipeline/map_common.py ship in every
committed heatmap.html, so rewording one there changes every map: re-render
and commit the maps with it. The rule is in CLAUDE.md, "Code comments";
scripts/check_provenance.py is the reference example of the style.
"""
import argparse
import ast
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

EM_DASH = "—"
EXCLUDE = ()          # path prefixes to skip, e.g. ("vendor/",)
# The // pattern skips "://" so a URL is not read as a JS comment.
EMBEDDED = re.compile(r"/\*.*?\*/|<!--.*?-->|(?<![:\w])//[^\n]*", re.S)


def project_files(root):
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=root,
                         capture_output=True, text=True, check=True).stdout.split()
    return [root / p for p in out if not p.startswith(EXCLUDE)]


def docstring_nodes(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                yield b[0].value


def scan(src):
    """Return (hits, counts) for one file's source; a hit is (line, kind, text)."""
    tree = ast.parse(src)
    hits, counts = [], {"comment": 0, "docstring": 0, "embedded": 0}
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            counts["comment"] += 1
            if EM_DASH in tok.string:
                hits.append((tok.start[0], "comment", tok.string.strip()))
    docstrings = set()
    for node in docstring_nodes(tree):
        docstrings.add(id(node))
        counts["docstring"] += 1
        for i, line in enumerate(node.value.splitlines()):
            if EM_DASH in line:
                hits.append((node.lineno + i, "docstring", line.strip()))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and id(node) not in docstrings:
            for m in EMBEDDED.finditer(node.value):
                counts["embedded"] += 1
                if EM_DASH in m.group(0):
                    line = node.lineno + node.value[:m.start()].count("\n")
                    hits.append((line, "comment inside a string",
                                 " ".join(m.group(0).split())[:100]))
    return hits, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    root = ap.parse_args().root.resolve()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    files = project_files(root)
    if not files:
        sys.exit(f"FAIL: found no tracked .py files under {root}.")
    total = {"comment": 0, "docstring": 0, "embedded": 0}
    failures = []
    for path in files:
        hits, counts = scan(path.read_text(encoding="utf-8"))
        for k in total:
            total[k] += counts[k]
        failures += [(path.relative_to(root).as_posix(), *h) for h in hits]

    print(f"Scanned {len(files)} files: {total['comment']} # comments, "
          f"{total['docstring']} docstrings, {total['embedded']} comments inside strings.")
    if not total["comment"] or not total["docstring"]:
        sys.exit("FAIL: found no comments or no docstrings at all - the scan is broken.")
    if failures:
        print(f"\nFAIL: {len(failures)} em dash(es) in comments.\n")
        for rel, line, kind, text in sorted(failures):
            print(f"   {rel}:{line} ({kind}): {text}")
        sys.exit(1)
    print("OK: no em dashes in any comment or docstring.")


if __name__ == "__main__":
    main()
