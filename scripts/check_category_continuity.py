"""Fail when a taxonomy reaches a different answer from the cross-city rules.

    python scripts/check_category_continuity.py             # the check
    python scripts/check_category_continuity.py --matrix    # rule x taxonomy grid
    python scripts/check_category_continuity.py --strict    # pending departures fail too
    python scripts/check_category_continuity.py --selftest  # watch it fail, ten ways

WHY THIS EXISTS
---------------
`docs/category_rules.md` holds the owner's cross-city rules - funeral out,
canteens out, the "other personal services" catch-all out, commercial massage
kept, car dealers kept, and so on - each with the cities it was measured on.
It is prose, and prose is read past: Korea's SEMAS taxonomy was proposed with
massage left out, which would have made Korea the only country to drop it
(DECISIONS 2026-09-29, "Incheon built on SEMAS's national storefront
register"). A rule nobody runs is a rule the next city breaks.

WHAT IT CHECKS
--------------
The table is `scripts/category_continuity_table.py`: for every rule, for every
taxonomy in `pipeline/taxonomies/`, the rows that locate the trade in that
register (a code, a label, a keyword) or a declared reason it is not there.

  A. Every registered taxonomy has a column, and every column is registered.
  B. Every column answers every required rule. A new rule or a new taxonomy
     fails until it is answered. An optional sub-rule (tattoo, funeral goods,
     health food) left out fails only if the module names the trade.
  C. Each locator row, passed to that module's own `classify()`, gives the
     rule's verdict - None for a trade that is out, the bucket for one kept.
     This is the part that catches a departure.
  D. A declared exception gives exactly the result it declares, cites a
     DECISIONS heading that exists, and is not stale (a row back in line with
     the rule means the exception must go). A pending departure is the same,
     without the heading: it passes, printed on every run, until the owner
     rules (`--strict` fails it).
  E. An `outside(...)` entry - a trade decided by a step-2 filter or a city
     config, not by classify() - names a file that still holds its token.
  F. An `absent(...)` cell is not contradicted by the module itself: none of
     the rule's keywords appears among the module's own string constants
     (its code tables), docstrings and error messages aside.
  G. The rules agree with `docs/category_rules.md`: every row of its table is
     claimed by a rule, and each rule's verdict is its row's Out or Kept.

A failure is a finding for the OWNER, never a reason to edit a taxonomy to
make it pass, and never a reason to widen the table to swallow it: a
departure is corrected by the owner or declared with its DECISIONS reason
(`docs/category_rules.md`, "How to use it", step 3).

Read-only. Imports every taxonomy module and nothing else from the pipeline.
"""
import argparse
import ast
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RULES_DOC = "docs/category_rules.md"
TABLE = "scripts/category_continuity_table.py"
BUCKETS = ("Retail", "Food service", "Personal services")


def show(verdict):
    return "out" if verdict is None else verdict


# ---------------------------------------------------------------------------
# docs/category_rules.md
# ---------------------------------------------------------------------------
def parse_doc_rules(text):
    """{trade cell: verdict} from the rules table. A verdict is None (Out), a
    bucket (Kept, <bucket>), or "special" for a cell that is neither ("In-store
    only")."""
    rows = {}
    in_table = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_table = line.strip() == "## The rules"
            continue
        if not (in_table and line.startswith("|")):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("Trade", "") or set(cells[0]) <= set("-: "):
            continue
        rule = cells[1]
        if rule.startswith("**Out**"):
            verdict = None
        elif rule.startswith("**Kept**"):
            hits = sorted((rule.find(b), b) for b in BUCKETS if b in rule)
            verdict = hits[0][1] if hits else "special"
        else:
            verdict = "special"
        rows[cells[0]] = verdict
    return rows


def decision_headings(root):
    """Every DECISIONS heading, current and archived (for exceptions), and every
    heading still in a session's drafts file (docs/decisions_drafts/, owner
    2026-09-30): build sessions write there, cleanup folds them in, and an
    exception cites its draft until the fold."""
    heads = []
    for p in [root / "DECISIONS.md", *sorted((root / "docs" / "decisions").glob("*.md")),
              *sorted((root / "docs" / "decisions_drafts").glob("*.md"))]:
        if p.exists():
            heads += [l[4:].strip() for l in p.read_text(encoding="utf-8").splitlines()
                      if l.startswith("### ")]
    return heads


# ---------------------------------------------------------------------------
# A module's own vocabulary (properties B and F)
# ---------------------------------------------------------------------------
def vocabulary(paths):
    """Every string constant in the modules' source, except docstrings, assert
    messages and error messages: what their code tables and keyword lists can
    match."""
    out = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        skip = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    skip.add(id(body[0].value))
            if isinstance(node, ast.Assert) and node.msg is not None:
                skip.update(id(n) for n in ast.walk(node.msg))
            if isinstance(node, ast.Call) and getattr(node.func, "id", "").endswith(("Error", "Exit")):
                skip.update(id(n) for a in node.args for n in ast.walk(a))
        out += [n.value for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in skip]
    return out


def module_path(root, dotted):
    return root / Path(*dotted.split(".")).with_suffix(".py")


def pending_tag(entry):
    """PENDING OWNER until the owner rules; QUEUED FIX once a fix is approved."""
    queued = getattr(entry, "queued", None)
    return f"QUEUED FIX [{queued}] " if queued else "PENDING OWNER "


def keyword_hits(rule, vocab, ignore=()):
    if not rule.keywords:
        return []
    pat = re.compile(rule.keywords, re.I)
    # An ignore entry drops every string that contains it (long regex sources included).
    return sorted({s for s in vocab if pat.search(s) and not any(i in s for i in ignore)})


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------
def run_check(table, registry, load, doc_text, headings, root):
    """Return (problems, pendings, grid).

    `table` has RULES, resolved_columns() and optionally EXTRA_SOURCES,
    ROW_KEY and CLASSIFY_VIA (see the table's docstring);
    `registry` is {system: dotted module}; `load(system)` imports one.
    `grid[(rule, system)]` is a one-character mark for --matrix."""
    problems, pendings, grid = [], [], {}
    rules, columns = table.RULES, table.resolved_columns()
    extra_sources = getattr(table, "EXTRA_SOURCES", {})
    row_keys = getattr(table, "ROW_KEY", {})
    via = getattr(table, "CLASSIFY_VIA", {})

    # A. columns <-> registry
    for system in sorted(set(registry) - set(columns)):
        problems.append(f"A {system}: registered in pipeline/taxonomies/__init__.py but has no "
                        f"column in {TABLE} - answer every rule for it")
    for system in sorted(set(columns) - set(registry)):
        problems.append(f"A {system}: a column in {TABLE} but not a registered taxonomy")

    # G. rules <-> docs/category_rules.md (a rule names its row by the row's start)
    doc = parse_doc_rules(doc_text)

    def row_of(rule):
        found = [t for t in doc if t.startswith(rule.doc_row)]
        return found[0] if len(found) == 1 else None

    claimed = {row_of(r) for r in rules.values()}
    for trade in doc:
        if trade not in claimed:
            problems.append(f"G {RULES_DOC}: the row \"{trade[:60]}\" is claimed by no rule in "
                            f"{TABLE} - a new owner rule needs a rule there, and every taxonomy's "
                            "answer to it")
    for rid, r in rules.items():
        trade = row_of(r)
        if trade is None:
            problems.append(f"G rule {rid}: no single row of {RULES_DOC} starts \"{r.doc_row}\" "
                            "(reworded? point doc_row at the new wording)")
        elif not r.sub and doc[trade] != "special" and doc[trade] != r.verdict:
            problems.append(f"G rule {rid}: {TABLE} says {show(r.verdict)}, {RULES_DOC} says "
                            f"{show(doc[trade])} - the owner's document wins; fix the table")

    for system in sorted(set(columns) & set(registry)):
        try:
            mod = load(system)
        except Exception as e:                     # an import-time assert is a finding too
            problems.append(f"C {system}: the module failed to import: {type(e).__name__}: {e}")
            continue
        col = columns[system]
        vocab = None

        def get_vocab():
            nonlocal vocab
            if vocab is None:
                paths = [module_path(root, registry[system])]
                paths += [root / p for p in extra_sources.get(system, ())]
                vocab = vocabulary([p for p in paths if p.exists()])
            return vocab

        for rid, r in rules.items():
            cell = col.get(rid)
            if cell is None:
                hits = keyword_hits(r, get_vocab())
                if r.required:
                    problems.append(f"B {system}: no answer for rule {rid} ({r.doc_row}) - add "
                                    "loc() rows, absent(reason) or outside(file, token, what)")
                    grid[(rid, system)] = "?"
                elif hits:
                    problems.append(f"B {system}: the module names "
                                    f"{', '.join(repr(h[:40]) for h in hits[:4])} but has no "
                                    f"locator for rule {rid} - add loc() rows for it")
                    grid[(rid, system)] = "?"
                continue
            if not cell:
                problems.append(f"B {system}: rule {rid} has an empty cell")
                grid[(rid, system)] = "?"
                continue

            if cell[0].kind == "absent":
                if len(cell) > 1:
                    problems.append(f"B {system}: rule {rid}: absent() must stand alone in its cell")
                hits = keyword_hits(r, get_vocab(), cell[0].ignore)
                if hits:
                    problems.append(f"F {system}: rule {rid} is declared absent, but the module "
                                    f"names {', '.join(repr(h[:40]) for h in hits[:4])} - locate "
                                    "it, or list the string in absent(..., ignore=) with why")
                grid[(rid, system)] = "-"
                continue

            marks = set()
            for entry in cell:
                if entry.kind == "absent":
                    problems.append(f"B {system}: rule {rid}: absent() must stand alone in its cell")
                    continue
                if entry.kind == "outside":
                    path = root / entry.path
                    if not path.exists() or entry.token not in path.read_text(encoding="utf-8"):
                        problems.append(f"E {system}: rule {rid} is decided outside classify() by "
                                        f"{entry.path}, but that file does not hold {entry.token!r}")
                        marks.add("!")
                    else:
                        marks.add("o")
                    continue
                if entry.kind in ("pending", "exception") and entry.row is None:
                    # A departure made before classify(): pinned by its token.
                    path = root / entry.path
                    if entry.kind == "exception" and not any(entry.decision in h for h in headings):
                        problems.append(f"D {system}: rule {rid}, {entry.label}: the exception cites "
                                        f"DECISIONS \"{entry.decision}\", which is no heading there")
                        marks.add("!")
                    if not path.exists() or entry.token not in path.read_text(encoding="utf-8"):
                        problems.append(f"D {system}: rule {rid}, {entry.label}: the {entry.kind}'s "
                                        f"token {entry.token!r} has gone from {entry.path} - "
                                        "resolved? make it a loc() or outside()")
                        marks.add("!")
                    elif entry.kind == "pending":
                        pendings.append(f"{pending_tag(entry)}{system}: rule {rid}, {entry.label} "
                                        f"({entry.path}): {show(entry.result)}, the rule says "
                                        f"{show(r.verdict)} (since {entry.since}). {entry.note}")
                        marks.add("p")
                    else:
                        marks.add("x")
                    continue
                key = row_keys.get(system, mod.VALUE_COLUMN)
                row = entry.row if isinstance(entry.row, dict) else {key: entry.row}
                where = f"{system}: rule {rid}, {entry.label} {row}"
                try:
                    got = via[system](mod, dict(row)) if system in via else mod.classify(dict(row))
                except Exception as e:
                    problems.append(f"C {where}: classify() raised {type(e).__name__}: {e}")
                    marks.add("!")
                    continue
                if entry.kind in ("exception", "pending"):
                    if entry.kind == "exception" and not any(entry.decision in h for h in headings):
                        problems.append(f"D {where}: the exception cites DECISIONS "
                                        f"\"{entry.decision}\", which is no heading there")
                        marks.add("!")
                    if got == r.verdict:
                        problems.append(f"D {where}: declared a{'n exception' if entry.kind == 'exception' else ' pending departure'} "
                                        f"({show(entry.result)}) but now gives the rule's own verdict "
                                        f"({show(got)}) - it is stale; make it a loc()")
                        marks.add("!")
                    elif got != entry.result:
                        problems.append(f"D {where}: declared {show(entry.result)}, classify() "
                                        f"gives {show(got)}")
                        marks.add("!")
                    elif entry.kind == "pending":
                        pendings.append(f"{pending_tag(entry)}{where}: gives {show(got)}, the rule "
                                        f"says {show(r.verdict)} (since {entry.since}). {entry.note}")
                        marks.add("p")
                    else:
                        marks.add("x")
                    continue
                if got != r.verdict:
                    problems.append(f"C {where}: gives {show(got)}, the rule says {show(r.verdict)}. "
                                    f"Precedent: {r.precedent}")
                    marks.add("!")
                else:
                    marks.add("=")
            grid[(rid, system)] = next((m for m in "!pxo=" if m in marks), "?")
    return problems, pendings, grid


def print_matrix(table, grid, systems):
    print("Marks: = agrees with the rule   x declared exception   p pending, the owner's call")
    print("       - absent from the register   o decided outside classify() only")
    print("       ! departure   ? unanswered   (blank: optional rule, not in this register)\n")
    for i, s in enumerate(systems):
        print(f"  {i:>2} {s}")
    print()
    print(f"{'rule':22}" + "".join(f"{i:>3}" for i in range(len(systems))))
    for rid in table.RULES:
        print(f"{rid:22}" + "".join(f"{grid.get((rid, s), ' '):>3}" for s in systems))


def load_real():
    sys.path.insert(0, str(ROOT / "scripts"))
    import category_continuity_table as table
    from pipeline.taxonomies import TAXONOMY_MODULES

    def load(system):
        return importlib.import_module(TAXONOMY_MODULES[system])
    return table, dict(TAXONOMY_MODULES), load


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--matrix", action="store_true", help="print the rule x taxonomy grid")
    ap.add_argument("--strict", action="store_true", help="pending departures fail too")
    ap.add_argument("--selftest", action="store_true", help="watch the check fail, and pass")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    table, registry, load = load_real()
    problems, pendings, grid = run_check(table, registry, load,
                                         (ROOT / RULES_DOC).read_text(encoding="utf-8"),
                                         decision_headings(ROOT), ROOT)
    if args.matrix:
        print_matrix(table, grid, sorted(registry))
        print()
    for p in problems:
        print("FAIL", p)
    for p in pendings:
        print(p)
    queued = sum(p.startswith("QUEUED FIX") for p in pendings)
    marks = list(grid.values())
    print(f"\n{len(table.RULES)} rules x {len(registry)} taxonomies: "
          f"{sum(m in '=!' for m in marks)} located, {marks.count('-')} absent, "
          f"{marks.count('o')} decided outside classify(), {marks.count('x')} declared exceptions, "
          f"{len(pendings)} pending departure rows ({queued} with an approved fix queued, "
          f"{len(pendings) - queued} awaiting the owner).")
    if problems or (args.strict and pendings):
        print(f"{len(problems)} problem(s). A departure is the OWNER's call: bring it with the "
              f"precedent it breaks ({RULES_DOC}); never edit a taxonomy to pass this check.")
        return 1
    tail = (f"; {len(pendings) - queued} pending row(s) await the owner, {queued} approved fix(es) "
            "are queued" if pendings else "")
    print(f"OK - every taxonomy reaches the cross-city verdicts or declares why not{tail}.")
    return 0


# ---------------------------------------------------------------------------
# --selftest: each property fails on a broken copy; the real table passes
# ---------------------------------------------------------------------------
def selftest():
    import copy
    import types

    table, registry, load = load_real()
    doc = (ROOT / RULES_DOC).read_text(encoding="utf-8")
    heads = decision_headings(ROOT)

    def fresh():
        """A deep copy of the table behind the same interface."""
        t = types.SimpleNamespace()
        t.RULES = copy.deepcopy(table.RULES)
        for name in ("EXTRA_SOURCES", "ROW_KEY", "CLASSIFY_VIA"):
            setattr(t, name, getattr(table, name, {}))
        cols = copy.deepcopy(table.resolved_columns())
        t.resolved_columns = lambda: cols
        return t, cols

    def check(t, reg=registry, loader=load, d=doc):
        return run_check(t, reg, loader, d, heads, ROOT)[0]

    def first(cols, system, rid, kind):
        return next(e for e in cols[system][rid] if e.kind == kind)

    results = []

    def case(name, problems, expect):
        ok = any(p.startswith(expect) for p in problems)
        results.append(ok)
        print(f"{'ok  ' if ok else 'FAIL'} {name}" + ("" if ok else f"\n     got: {problems[:3]}"))

    # The positive control comes first: if the real table fails, every case
    # below could be failing for the wrong reason.
    base = check(fresh()[0])
    results.append(not base)
    print(f"{'ok  ' if not base else 'FAIL'} the real table passes"
          + ("" if not base else f"\n     {len(base)} problems: {base[:3]}"))

    # C. A departure: NAICS funeral homes put back on the map.
    naics = load("naics")
    fake = types.SimpleNamespace(
        VALUE_COLUMN=naics.VALUE_COLUMN,
        classify=lambda row: "Personal services" if row.get("naics") == "812210" else naics.classify(row))
    case("C  a departure (NAICS funeral homes kept) fails",
         check(fresh()[0], loader=lambda s: fake if s == "naics" else load(s)), "C naics: rule funeral")

    # A. A registered taxonomy with no column.
    case("A  a new taxonomy with no column fails",
         check(fresh()[0], reg={**registry, "brand_new": "pipeline.taxonomies.naics"}), "A brand_new")

    # B. A column that leaves a required rule unanswered.
    t, cols = fresh()
    del cols["naics"]["massage_commercial"]
    case("B  an unanswered rule fails", check(t), "B naics: no answer for rule massage_commercial")

    # B. An optional rule left out where the module names the trade.
    t, cols = fresh()
    del cols["calgary_licencetype"]["tattoo"]
    case("B  an optional rule the module names, left out, fails", check(t), "B calgary_licencetype")

    # D. A stale exception: Montréal's caterer exception pointed at a code that
    # obeys the rule.
    t, cols = fresh()
    first(cols, "naics_montreal", "no_counter_food", "exception").row = "722310"
    case("D  a stale exception fails", check(t), "D naics_montreal: rule no_counter_food")

    # D. An exception citing a DECISIONS heading that does not exist.
    t, cols = fresh()
    first(cols, "naics_montreal", "no_counter_food", "exception").decision = "no such decision, 1999"
    case("D  an exception with no DECISIONS heading fails", check(t), "D naics_montreal")

    # D. A pending departure the code has since brought into line. Any pending
    # cell will do: give it the row of a loc() in the same cell, which obeys the
    # rule by construction. Not a named cell: one disappears when the owner
    # rules on it (Boston's nightclub cell, 2026-09-30, crashed the self-test).
    t, cols = fresh()
    target = next(((s, rid, e, loc_e) for s, col in cols.items() for rid, cell in col.items()
                   for e in (cell if isinstance(cell, list) else [cell]) if e.kind == "pending"
                   for loc_e in (cell if isinstance(cell, list) else [cell])
                   if loc_e.kind == "loc" and getattr(loc_e, "row", None) is not None), None)
    if target is None:
        print("skip D  a pending departure now resolved: no pending cell with a loc() beside it")
    else:
        s, rid, e, loc_e = target
        e.row = loc_e.row
        case("D  a pending departure now resolved fails (make it a loc)", check(t),
             f"D {s}: rule {rid}")

    # E. An outside() entry whose token has gone from its file.
    t, cols = fresh()
    first(cols, "naics", "personal_catchall", "outside").token = "TOKEN_THAT_IS_NOT_THERE"
    case("E  an outside() token missing from its file fails", check(t), "E naics")

    # F. An absent() cell contradicted by the module's own table.
    t, cols = fresh()
    cols["phl_licensetype"]["pawnbroker"] = [table.absent("pretend Philadelphia has none")]
    case("F  absent() contradicted by the module's own table fails", check(t),
         "F phl_licensetype: rule pawnbroker")

    # G. A new owner rule in the document with no rule here.
    extra = doc.replace("| Parking |", "| Driving schools | **Out** | nowhere yet | test |\n| Parking |", 1)
    case("G  a new document row with no rule fails", check(fresh()[0], d=extra),
         f"G {RULES_DOC}: the row \"Driving schools")

    # G. The table and the document disagree on a verdict.
    t, _ = fresh()
    t.RULES["pawnbroker"].verdict = None
    case("G  a verdict that disagrees with the document fails", check(t), "G rule pawnbroker")

    ok = all(results)
    print(f"\nselftest {'PASSED' if ok else 'FAILED'}: {sum(results)} of {len(results)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
