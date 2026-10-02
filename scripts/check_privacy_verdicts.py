"""Every built city has a recorded privacy verdict.

    python scripts/check_privacy_verdicts.py     # pass/fail (check_all runs it)

CLAUDE.md: run `check_personal_exposure.py <city>` before publishing a city and
record the verdict in DECISIONS.md. Ten French cities were registered in that
script with no verdict ever written (2026-09-30), and only a reading of the log
showed it. The log is prose in many styles, so this check reads a registry
instead: `docs/privacy_verdicts.md`, one table row per city (its verdict, the
date, and the heading of the DECISIONS entry that records it).

It fails when:
  * a city in `app/cities.py` has no row, or a row names no built city;
  * a verdict is not one of VERDICTS;
  * the cited heading is not an entry in DECISIONS.md or its archive
    (`docs/decisions/*.md`), or that entry never names the city.
"""
import ast
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "privacy_verdicts.md"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# publish: the exposure check was run and the city published on its result.
# publish-structural: the source carries no person-name field at all (Dublin's
# valuation register), so there is nothing to expose.
VERDICTS = {"publish", "publish-structural"}
# pending: a known open question for the owner. Reported, not failed (like
# check_macro_labels' KNOWN_STACKED), and it still has to cite the entry that
# states the question.
PENDING = "pending"


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower())
                   if not unicodedata.combining(c))


def city_names(root=ROOT):
    tree = ast.parse((root / "app" / "cities.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "CITIES":
            return [ast.literal_eval(d.values[[k.value for k in d.keys].index("name")])
                    for d in node.value.elts]
    raise SystemExit("app/cities.py: no CITIES list")


def rows(text):
    """[(city, verdict, date, heading)] from the registry's table (a fifth
    column, the evidence, is for the reader)."""
    out = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.lstrip().startswith("|") or len(cells) < 4:
            continue
        if cells[0] in ("City", "") or set(cells[0]) <= set("-: "):
            continue
        out.append(tuple(cells[:4]))
    return out


def entries(root=ROOT):
    """{heading: entry text} over DECISIONS.md, its weekly archives, and the
    build sessions' drafts files: a new city's verdict sits in its session's
    drafts until cleanup folds them, and a check cites the draft until then
    (owner, 2026-09-30; check_category_continuity.py does the same)."""
    out = {}
    for p in [root / "DECISIONS.md", *sorted((root / "docs" / "decisions").glob("*.md")),
              *sorted((root / "docs" / "decisions_drafts").glob("*.md"))]:
        for part in re.split(r"(?m)^(?=### )", p.read_text(encoding="utf-8")):
            m = re.match(r"### (\d{4}-\d{2}-\d{2}) - (.+)", part)
            if m:
                out[(m.group(1), m.group(2).strip())] = part
    return out


def check(root=ROOT):
    problems, pending = [], []
    names = city_names(root)
    if not (root / REGISTRY.relative_to(ROOT)).exists():
        return names, [f"{REGISTRY.relative_to(ROOT)} is missing"], []
    table = rows((root / REGISTRY.relative_to(ROOT)).read_text(encoding="utf-8"))
    log = entries(root)
    seen = {}
    for city, verdict, date, heading in table:
        if city in seen:
            problems.append(f"{city}: two rows")
        seen[city] = verdict
        if city not in names:
            problems.append(f"{city}: a row, but no built city by that name in app/cities.py")
        if verdict == PENDING:
            pending.append(city)
        elif verdict not in VERDICTS:
            problems.append(f"{city}: verdict {verdict!r} is not one of {sorted(VERDICTS)}")
        heading = heading.strip("`* ")
        entry = log.get((date, heading))
        if entry is None:
            problems.append(f"{city}: no DECISIONS entry '### {date} - {heading}'")
            continue
        short = fold(re.sub(r"\s*\(.*?\)", "", city).strip())
        if short not in fold(entry):
            problems.append(f"{city}: the cited entry ({date}) never names the city")
    for city in names:
        if city not in seen:
            problems.append(f"{city}: built, but no privacy verdict in {REGISTRY.name} "
                            f"(run check_personal_exposure.py, record the verdict in "
                            f"DECISIONS.md, then add the row)")
    return names, problems, pending


def main():
    names, problems, pending = check()
    if problems:
        print(f"FAIL - {len(problems)} problem(s):")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print(f"OK - all {len(names)} built cities have a privacy verdict, each "
          f"recorded in a DECISIONS entry that names the city"
          + (f"; {len(pending)} pending the owner: {', '.join(pending)}" if pending else ""))


if __name__ == "__main__":
    main()
