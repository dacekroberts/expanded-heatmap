"""No list of withheld people's names in the pipeline as plain text: keys only.

    python scripts/check_name_keys.py              # pass/fail (check_all runs it)
    python scripts/check_name_keys.py --selftest   # touches nothing

A step 2 that withholds names read by eye as a person's own keeps them as
keys (pipeline/name_keys.py), never as the names: a plain list publishes, in
the repository, exactly the people the map leaves out (owner, 2026-10-01;
DECISIONS.md). This fails any module-level PERSON_NAMED, PERSON_NAMES or
other PERSON_NAME* constant in pipeline/ that holds a string which is not a
16-hex-digit key.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = re.compile(r"^[0-9a-f]{16}$")
CONST = re.compile(r"^PERSON_NAME")


def plain_entries(source):
    """[(constant, line, count)] for each PERSON_NAME* literal holding a non-key."""
    out = []
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            name = getattr(target, "id", None)
            if not name or not CONST.match(name):
                continue
            if not isinstance(node.value, (ast.Tuple, ast.List, ast.Set)):
                continue
            bad = [e for e in node.value.elts
                   if isinstance(e, ast.Constant) and isinstance(e.value, str)
                   and not KEY.match(e.value)]
            if bad:
                out.append((name, node.lineno, len(bad)))
    return out


def check(root=ROOT):
    problems, seen = [], 0
    for py in sorted((root / "pipeline").rglob("*.py")):
        text = py.read_text(encoding="utf-8")
        if "PERSON_NAME" not in text:
            continue
        seen += 1
        for name, line, n in plain_entries(text):
            problems.append(f"{py.relative_to(root)}:{line}: {name} holds {n} plain "
                            f"name(s) - store keys (python pipeline/name_keys.py \"NAME\")")
    return seen, problems


def selftest():
    cases = [
        (plain_entries('PERSON_NAMED = ("adfded197c319f26", "5b180c71183ee94d")'), []),
        (plain_entries('PERSON_NAMED = ("ANY NAME", "adfded197c319f26")'), [("PERSON_NAMED", 1, 1)]),
        (plain_entries('PERSON_NAMES = {"Any Name"}'), [("PERSON_NAMES", 1, 1)]),
        (plain_entries('LINE_NAMES = {"A": "Tram A"}'), []),          # not a withheld list
        (plain_entries('PERSONAL_OWN_TYPES = ("Individual",)'), []),  # a type, not names
    ]
    bad = [i for i, (got, want) in enumerate(cases) if got != want]
    print(f"{len(cases) - len(bad)} of {len(cases)} cases behaved as intended."
          + (f" FAILED: {bad}" if bad else ""))
    return not bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    seen, problems = check()
    if problems:
        print(f"FAIL - {len(problems)} withheld-name list(s) hold plain names:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print(f"OK - every withheld-name list in pipeline/ holds keys ({seen} file(s) name one)")


if __name__ == "__main__":
    main()
