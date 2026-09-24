"""Fail when a discarded city rests on an absence that was looked for once.

    python scripts/check_discard_evidence.py [--verbose]
    python scripts/check_discard_evidence.py --selftest

WHY THIS EXISTS
---------------
`add-country` has said since 2026-09-21 that **a negative from one method is
not a finding** - and the discard table in `docs/city_master_list.md` broke it
twice anyway, because the rule was prose and the table was prose:

  1. 2026-09-22: eleven cities sat under "the country's business leg failed"
     in a file whose own sweep called those countries unprobed - Naples among
     them, discarded for its country failing while Italy was the one country
     that passed.
  2. 2026-09-24: an audit found twelve more rows resting on ONE method - a
     national portal only, or the top hits of one search - worded as findings
     ("aggregate", "no register"). The sweep before it had looked for the words
     "unprobed" and "not reached", and a one-search negative worded as a
     finding passed it. Amsterdam, one of them, had a current premises
     register on its own host the night it was re-probed.

So the table now carries its evidence as COLUMNS, and this script reads them.
A row cannot be added without saying what kind of discard it is, which
methods it rests on, and whether the city's own host was asked.

THE RULE
--------
Kind (what the discard claims):

  absence   no usable register was found            - needs more than one look
  coverage  licensing is devolved and too few units publish - same
  measured  the city's register was found and measured unusable
  terms     the data is usable and its terms forbid it
  rail      no urban rail of the kind this project maps

`measured`, `terms` and `rail` rest on something that EXISTS and was read, so
one method is enough. `absence` and `coverage` rest on something NOT being
found, which is exactly the shape `add-country` calls ASSERTED. They need:

  - the city's own host asked (`yes`) - not `no`, and not `blocked`, which is
    Band D's shape (Kaohsiung) rather than a finding; and
  - two methods, or one that read the WHOLE catalogue (`enumerated`) or
    measured a register (`measured`). One `search` is what the audit found
    twelve of.

Methods are ` · `-separated, each opening with its shape: `search`,
`enumerated`, `measured` or `read` (evidence), or `blocked` (a probe that
learned nothing - listed for the record, never counted).

It also checks the heading's hand-kept count against the rows.
"""
import re
import sys
from pathlib import Path

LIST = Path(__file__).resolve().parent.parent / "docs" / "city_master_list.md"
KINDS = {"absence", "coverage", "measured", "terms", "rail"}
NEEDS_TWO = {"absence", "coverage"}
EVIDENCE = {"search", "enumerated", "measured", "read"}
SHAPES = EVIDENCE | {"blocked"}
HOSTS = {"yes", "no", "blocked"}
COLS = ("city", "kind", "methods", "city host asked?")


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _word(cell):
    m = re.match(r"[\W_]*([a-z]+)", cell.lower())
    return m.group(1) if m else ""


def _city(cell):
    return re.sub(r"[*~]|[^\w\s'.-]", "", cell).strip()


def check(text):
    """Return (rows, problems) for the DISCARDED section of `text`."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("## DISCARDED")), None)
    if start is None:
        return [], ["no '## DISCARDED' section"]
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ") or lines[i].startswith("# ")), len(lines))
    section = lines[start:end]
    rows, problems = [], []
    i = 0
    while i < len(section) - 1:
        head, sep = section[i], section[i + 1]
        if not (head.startswith("|") and re.match(r"^\|[\s:|-]+\|$", sep.strip())):
            i += 1
            continue
        names = [c.lower() for c in _cells(head)]
        missing = [c for c in COLS if c not in names]
        if missing:
            problems.append(f"table at section line {i + 1} lacks column(s) {missing} - "
                            "every discard row states its kind, methods and host")
        i += 2
        while i < len(section) and section[i].startswith("|"):
            cells = dict(zip(names, _cells(section[i])))
            i += 1
            if missing:
                continue
            city = _city(cells["city"])
            kind = _word(cells["kind"])
            methods = [m.strip() for m in cells["methods"].split("·") if m.strip()]
            shapes = [_word(m) for m in methods]
            host = _word(cells["city host asked?"])
            evidence = [s for s in shapes if s in EVIDENCE]
            why = []
            if kind not in KINDS:
                why.append(f"kind '{cells['kind']}' is not one of {sorted(KINDS)}")
            bad = [m for m, s in zip(methods, shapes) if s not in SHAPES]
            if bad:
                why.append(f"method(s) open with no known shape: {bad}")
            if host not in HOSTS:
                why.append(f"host '{cells['city host asked?']}' is not yes / no / blocked")
            if not evidence:
                why.append("no method that returned evidence")
            if kind in NEEDS_TWO:
                if host != "yes":
                    why.append(f"a {kind} row with the city's own host '{host}' - "
                               "that is the open gap's shape (or Band D's, if blocked)")
                if len(evidence) < 2 and not {"enumerated", "measured"} & set(evidence):
                    why.append(f"a {kind} row resting on one {evidence[0] if evidence else 'nothing'}")
            rows.append((city, kind, len(evidence), host, why))
    m = re.search(r"DISCARDED\D*(\d+)", section[0])
    if m and int(m.group(1)) != len(rows):
        problems.append(f"heading says {m.group(1)} cities, the tables hold {len(rows)}")
    problems += [f"{c}: {'; '.join(w)}" for c, _, _, _, w in rows if w]
    return rows, problems


def selftest():
    head = ("## DISCARDED — {n} cities\n\n| City | Kind | Methods | City host asked? | Why |\n"
            "|---|---|---|---|---|\n")
    good = ("| **A** | absence | search `x` · search `y` | yes | fine |\n"
            "| **B** | absence | enumerated `x` | yes | fine |\n"
            "| **C** | terms | read the terms | yes | fine |\n"
            "| **D** | measured | measured the register | blocked — wall | fine |\n")
    cases = {
        "one search": "| **E** | absence | search `x` | yes | thin |\n",
        "host never asked": "| **E** | coverage | search `x` · enumerated `y` | no | thin |\n",
        "host blocked": "| **E** | absence | enumerated `x` · blocked `y` | blocked | thin |\n",
        "blocked is not evidence": "| **E** | absence | search `x` · blocked `y` | yes | thin |\n",
        "unknown kind": "| **E** | aggregate | search `x` · search `y` | yes | ? |\n",
        "unknown shape": "| **E** | absence | looked at `x` · search `y` | yes | ? |\n",
    }
    ok = True
    rows, problems = check(head.format(n=4) + good + "\n## Next\n")
    if problems or len(rows) != 4:
        print("FAIL  the passing table was refused:", problems)
        ok = False
    for name, row in cases.items():
        _, problems = check(head.format(n=5) + good + row)
        caught = any(p.startswith("E:") for p in problems)
        print(("ok    " if caught else "MISSED") + f"  {name}")
        ok &= caught
    for name, doc in {
        "count drifted": head.format(n=9) + good,
        "table without the columns": head.format(n=5) + good + "\n| City | Why |\n|---|---|\n| **F** | gone |\n",
    }.items():
        _, problems = check(doc)
        print(("ok    " if problems else "MISSED") + f"  {name}")
        ok &= bool(problems)
    print("selftest", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    rows, problems = check(LIST.read_text(encoding="utf-8"))
    if "--verbose" in sys.argv:
        for city, kind, n, host, why in rows:
            print(f"{'THIN' if why else 'ok  '}  {city:<12} {kind:<9} methods={n}  host={host}")
    if problems:
        print(f"{len(problems)} problem(s) in the discard table ({LIST.name}):")
        for p in problems:
            print("  -", p)
        print("A thin discard belongs in the OPEN SCREENING GAP with its next probe named, "
              "not here. Moving a row is the owner's call; relaxing this rule is not the fix.")
        return 1
    print(f"OK - {len(rows)} discard rows, each carrying enough evidence for its kind")
    return 0


if __name__ == "__main__":
    sys.exit(main())
