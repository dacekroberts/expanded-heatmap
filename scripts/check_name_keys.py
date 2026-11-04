"""No list of withheld people's names in the pipeline as plain text: keys only.

    python scripts/check_name_keys.py              # pass/fail (check_all runs it)
    python scripts/check_name_keys.py --selftest   # touches nothing

A step 2 that withholds names read by eye as a person's own keeps them as
keys (pipeline/name_keys.py), never as the names: a plain list publishes, in
the repository, exactly the people the map leaves out (owner, 2026-10-01;
DECISIONS.md). This fails any module-level PERSON_NAMED, PERSON_NAMES or
other PERSON_NAME* constant in pipeline/ that holds a string which is not a
16-hex-digit key, in any literal shape (tuple, list, set, dict, a frozenset()
call, an annotated or augmented assignment), and any such constant whose value
cannot be read from the source, since an unread value is an untested one.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = re.compile(r"^[0-9a-f]{16}$")
CONST = re.compile(r"^PERSON_NAME")
WRAPPERS = {"frozenset", "set", "tuple", "list", "sorted"}
UNREADABLE = -1


def literal_strings(node):
    """Every string in a literal value, or None if any part of it is not a
    literal this check can read (a name, a comprehension, another call)."""
    if isinstance(node, ast.Constant):
        return [node.value] if isinstance(node.value, str) else []
    if isinstance(node, ast.Call):
        if (getattr(node.func, "id", None) not in WRAPPERS or node.keywords):
            return None
        parts = node.args
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        parts = node.elts
    elif isinstance(node, ast.Dict):
        parts = node.keys + node.values
    else:
        return None
    found = []
    for part in parts:
        strings = None if part is None else literal_strings(part)
        if strings is None:
            return None
        found += strings
    return found


def plain_entries(source):
    """[(constant, line, count)] for each PERSON_NAME* value holding a non-key;
    count is UNREADABLE for a value literal_strings() cannot read."""
    out = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        else:
            continue
        for target in targets:
            name = getattr(target, "id", None)
            if not name or not CONST.match(name) or node.value is None:
                continue
            strings = literal_strings(node.value)
            if strings is None:
                out.append((name, node.lineno, UNREADABLE))
                continue
            bad = [s for s in strings if not KEY.match(s)]
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
            if n == UNREADABLE:
                problems.append(f"{py.relative_to(root)}:{line}: {name} has a value this check "
                                f"cannot read - write it as a literal of keys")
                continue
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
        (plain_entries('PERSON_NAMED = frozenset({"ANY NAME"})'), [("PERSON_NAMED", 1, 1)]),
        (plain_entries('PERSON_NAMED = frozenset({"adfded197c319f26"})'), []),
        (plain_entries('PERSON_NAMED = frozenset()'), []),
        (plain_entries('PERSON_NAMED: tuple = ("ANY NAME",)'), [("PERSON_NAMED", 1, 1)]),
        (plain_entries('PERSON_NAMED: tuple'), []),                   # no value to read
        (plain_entries('PERSON_NAMED += ("ANY NAME",)'), [("PERSON_NAMED", 1, 1)]),
        (plain_entries('PERSON_NAME_X = "ANY NAME"'), [("PERSON_NAME_X", 1, 1)]),
        (plain_entries('PERSON_NAMES = {"ANY NAME": 1}'), [("PERSON_NAMES", 1, 1)]),
        (plain_entries('PERSON_NAMED = OTHER'), [("PERSON_NAMED", 1, UNREADABLE)]),
        (plain_entries('PERSON_NAMED = load("a")'), [("PERSON_NAMED", 1, UNREADABLE)]),
        (plain_entries('PERSON_NAMED = {n for n in X}'), [("PERSON_NAMED", 1, UNREADABLE)]),
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
