"""No barred mark on any surface the app renders.

    python scripts/check_barred_marks.py              # pass/fail (check_all runs it)
    python scripts/check_barred_marks.py --selftest   # touches nothing

A city whose publisher bars its brand without consent declares it in its
config: `BARRED_MARKS = ("Irigo",)` (Angers, owner 2026-09-30, MARK-FREE). The
brand reached the About page once, through `docs/data_sources/france.md`'s
Angers row, and two review lanes had to find it by reading (2026-09-30). This
turns that reading into a script run.

Rendered surfaces, all of them:
  * every file under `app/` (page text, captions, notices, the city registry,
    the macro map's JSON); comment lines are skipped, since they never render;
  * every doc the app renders: `docs/...` paths built in `app/` (About the
    Data, What Is Excluded) and each per-country file the About page globs;
  * the declaring city's own `outputs/<slug>/`, except `provenance.json`, the
    fetch record, which the page reads for dates only (`PRODUCER_ONLY`).

Another city's map is not scanned: its business names are the businesses' own,
and "irigo" inside a restaurant's name is not the network's brand. A mark is
matched as a whole word, case-insensitively.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EXEMPT_OUTPUTS = {"provenance.json"}
TEXT_SUFFIXES = {".py", ".md", ".json", ".csv", ".html", ".txt", ".toml", ".css", ".js"}
DOCS_PATH = re.compile(r'"docs"\s*/\s*"([^"]+)"')


def barred_marks(root=ROOT):
    """{slug: (mark, ...)} from each city config's BARRED_MARKS literal."""
    out = {}
    for cfg in sorted((root / "pipeline").glob("*/config.py")):
        tree = ast.parse(cfg.read_text(encoding="utf-8"))
        for node in tree.body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and getattr(node.targets[0], "id", None) == "BARRED_MARKS"):
                marks = ast.literal_eval(node.value)
                if marks:
                    out[cfg.parent.name] = tuple(marks)
    return out


def rendered_docs(root=ROOT):
    """The docs the app renders: every "docs" / "<file>" path built in app/,
    and every per-country file next to data_sources.md (About globs them)."""
    docs = set()
    for py in (root / "app").rglob("*.py"):
        for name in DOCS_PATH.findall(py.read_text(encoding="utf-8")):
            docs.add(root / "docs" / name)
    if (root / "docs" / "data_sources.md") in docs:
        docs.update((root / "docs" / "data_sources").glob("*.md"))
    return sorted(d for d in docs if d.is_file())


def surfaces(root, slug):
    files = [p for p in (root / "app").rglob("*")
             if p.is_file() and p.suffix in TEXT_SUFFIXES and "__pycache__" not in p.parts]
    files += rendered_docs(root)
    out_dir = root / "outputs" / slug
    if out_dir.is_dir():
        files += [p for p in out_dir.iterdir()
                  if p.is_file() and p.name not in EXEMPT_OUTPUTS and p.suffix in TEXT_SUFFIXES]
    return files


def hits(text, marks, python=False):
    """[(line number, line)] where a mark appears as a whole word."""
    pat = re.compile(r"\b(?:" + "|".join(re.escape(m) for m in marks) + r")\b", re.IGNORECASE)
    found = []
    for i, line in enumerate(text.splitlines(), 1):
        if python and line.lstrip().startswith("#"):
            continue
        if pat.search(line):
            found.append((i, line.strip()))
    return found


def check(root=ROOT):
    problems = []
    marks = barred_marks(root)
    for slug, ms in marks.items():
        for f in surfaces(root, slug):
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for n, line in hits(text, ms, python=f.suffix == ".py"):
                problems.append(f"{f.relative_to(root)}:{n}: {slug}'s barred mark: {line[:120]}")
    return marks, problems


def selftest():
    cases = [
        (hits("Tram A, B and C", ("Irigo",)), []),
        (hits("Réseau Irigo, Angers", ("Irigo",)), [(1, "Réseau Irigo, Angers")]),
        (hits("IRIGO", ("Irigo",)), [(1, "IRIGO")]),
        (hits("Amirigo pizzeria", ("Irigo",)), []),             # inside a word: not the mark
        (hits("# feed publisher IRIGO, never shown", ("Irigo",), python=True), []),
        (hits('x = "Irigo"  # shown', ("Irigo",), python=True), [(1, 'x = "Irigo"  # shown')]),
    ]
    bad = [i for i, (got, want) in enumerate(cases) if got != want]
    assert DOCS_PATH.findall('DOC = ROOT / "docs" / "excluded_categories.md"') == ["excluded_categories.md"]
    print(f"{len(cases) - len(bad)} of {len(cases)} cases behaved as intended."
          + (f" FAILED: {bad}" if bad else ""))
    return not bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    marks, problems = check()
    if not marks:
        print("FAIL - no city declares BARRED_MARKS; Angers must (owner, 2026-09-30)")
        sys.exit(1)
    if problems:
        print(f"FAIL - {len(problems)} barred mark(s) on a rendered surface:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    docs = rendered_docs()
    names = ", ".join(f"{s} ({', '.join(m)})" for s, m in marks.items())
    print(f"OK - no barred mark on app/, {len(docs)} rendered doc(s) or the city's outputs: {names}")


if __name__ == "__main__":
    main()
