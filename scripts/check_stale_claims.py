"""Report prose that has stopped being true. The heuristic half of the sweep.

    python scripts/check_stale_claims.py [--verbose] [--only A|B|C]

**THIS REPORTS AND ALWAYS EXITS 0.** `check_provenance.py` decides things - a
row is present or it is not - and fails. Everything here is a guess about
English, and a noisy gate gets ignored, which is worse than no gate. Read the
report; it is for a human mid-sweep, not for CI.

WHY THESE THREE
---------------
On 2026-09-22 a cleanup sweep found three classes of stale prose that no
existing check could see, in a project whose every check was about data:

  A. **Future tense about a present that arrived.** Three files said Canada was
     unbuilt while six municipalities were built; a fourth said it of D.C. Each
     read perfectly - it was describing a world that no longer existed.
  B. **Hand-kept counts.** Four were wrong in one file, and one contradicted
     itself two clauses later ("thirteen sources", then "six of the twelve").
  C. **Headings whose contents moved on.** `## Transit feeds (GTFS)` held three
     rail sources that were not GTFS.

WHAT KEEPS THE NOISE DOWN, AND WHY EACH RULE IS THERE
-----------------------------------------------------
Every rule below was added because the version without it was unusable.

  - **`DECISIONS.md`, `PLAN.md`, handovers and retrospectives are excluded.**
    The first is append-only history, where "no Canadian city is built" is a
    correct record of what was true that day; the second is open work, where
    "not yet" is the point; the rest are dated records pinned to a commit.
    **A count in a dated document is evidence, and updating it would destroy
    the record** - it is a defect only if it was wrong on that date, which this
    check cannot know. That is the distinction the category turns on: a
    current-state document carrying a count has a maintenance burden, a dated
    one does not.
  - **A future-tense marker only counts when the same line names something that
    IS built.** "Not yet a row" beside Washington D.C. matters; the identical
    phrase beside an unscreened country is a plan, not a defect.
  - **Counts must be SPELLED OUT, never digits.** The first version matched
    digits and returned **1,012 hits**, almost every one a measurement
    ("664,662 rows", "28,621-row") that is data and belongs there. Every real
    defect was a prose count of the project's own furniture - "fourteen
    cities", "thirteen sources", "the eight registries", "All six of these
    agreements", "Two files". Spelling a number out is the tell that a human is
    counting something they can see.
  - **Quoted spans are skipped.** A correction usually quotes the sentence it
    replaces, and flagging the fix as the defect trains people to ignore the
    report.
"""

import argparse
import ast
import re
import sys
from pathlib import Path

# The report quotes project prose, which is full of en dashes and curly quotes.
# A Windows console is cp1252 and dies on them mid-report.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent

# Append-only history and open work. See the docstring - this is not an
# oversight, and re-including them is how this check becomes unreadable.
EXCLUDE_NAMES = {"DECISIONS.md", "PLAN.md"}

# POINT-IN-TIME RECORDS, and the reason they are excluded is stronger than
# "noisy": their counts are correct as of a stated date, and **updating one
# would destroy the record**. `passover_opus5.md` pins itself to commit
# 520c165 and says in its own opening that it is "a map and a set of claims to
# test, not a source of truth"; a retrospective describes what was true when it
# was written. A count in one of these is evidence, not drift - it is only a
# defect if it was wrong ON THAT DATE, which this check cannot know.
#
# This is the distinction the whole category turns on: a CURRENT-STATE document
# that carries a count has a maintenance burden, and a DATED one does not.
EXCLUDE_PATTERNS = ("passover_*.md", "*retrospective*.md", "*_addendum.md")

# The sweep skill teaches these defects by quoting real instances, so it reports
# as stale prose about Canada and D.C. It is documentation OF the markers.
EXCLUDE_PATHS = {".claude/skills/consistency-sweep/SKILL.md"}

SCAN_GLOBS = ("docs/**/*.md", ".claude/skills/**/*.md", "CLAUDE.md", "*.md")

# A. Phrases describing a future, in a project where the future keeps arriving.
FUTURE_MARKERS = [
    "none built", "not built", "unbuilt", "no city is built",
    "not yet a row", "not yet", "if any", "when one is", "would require",
    "eventually", "candidate, not built", "to be decided",
    "will be required", "has not been built", "before it is built",
]

# B. SPELLED-OUT numbers only. "one" is excluded: it is an article far more
# often than a count ("one row per source", "no one"). That loses a real defect
# shape and is still right - a report nobody reads catches nothing.
NUMBER_WORD = (r"two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
               r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
               r"nineteen|twenty")
# Countables the PROJECT tracks. "rows" and "files" are deliberately absent:
# that is how measurements are phrased.
COUNTABLE = (r"cit(?:y|ies)|sources?|registr(?:y|ies)|notices?|agreements?|"
             r"feeds?|layers?|regions?|municipalit(?:y|ies)|taxonom(?:y|ies)")
# A DETERMINER is required, and it is what makes this usable. Without one the
# report was 265 lines, most of them correct: "three buckets" is a fixed concept
# of this project, "six pre-1998 municipalities" is a historical fact, and "six
# Canadian cities" is a true scoped count. None of those rot.
#
# What rots is a TOTALISING claim - one asserting how many of a thing the
# project has right now. Every real defect had that shape: "**All six** of these
# agreements", "**the eight** registries", "for the **fourteen** cities now
# built". So the count must be introduced by "all" or "the", or followed by a
# phrase that scopes it to the whole project.
DETERMINER = r"(?:all|the)\s+"
TOTALISING_TAIL = (r"(?:\s+(?:now\s+built|in\s+this\s+project|here\b|"
                   r"built\s+so\s+far|altogether|in\s+total))")
COUNT_RE = re.compile(
    r"\b" + DETERMINER + r"(?:" + NUMBER_WORD + r")\b[^.\n]{0,30}?\b(?:"
    + COUNTABLE + r")\b"
    r"|\b(?:" + NUMBER_WORD + r")\b[^.\n]{0,30}?\b(?:" + COUNTABLE + r")\b"
    + TOTALISING_TAIL,
    re.I)

QUOTED_RE = re.compile(
    "[\"“”][^\"“”\n]{3,200}?[\"“”]")


def built_vocabulary():
    """City names wired into the app, plus the place-words in their regions.

    A marker line is only interesting if it names one of these.
    """
    src = (ROOT / "app" / "cities.py").read_text(encoding="utf-8")
    cities, regions = [], []
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "CITIES" for t in node.targets):
            for d in node.value.elts:
                pairs = {getattr(k, "value", None): getattr(v, "value", None)
                         for k, v in zip(d.keys, d.values)}
                if pairs.get("name"):
                    cities.append(pairs["name"])
                if pairs.get("region"):
                    regions.append(pairs["region"])
    vocab = set()
    for c in cities:
        vocab.add(c)
        vocab.add(re.sub(r"\s*\(.*\)$", "", c))   # "Miami (Regional)" -> "Miami"
    stop = {"united", "states", "west", "east", "north", "south", "central"}
    for r in regions:
        for w in re.findall(r"[A-Za-zÀ-ɏ]+", r):
            if w.lower() not in stop and len(w) > 3:
                vocab.add(w)
    return cities, sorted(vocab, key=len, reverse=True)


def quoted_spans(line):
    return [(m.start(), m.end()) for m in QUOTED_RE.finditer(line)]


def in_quotes(pos, spans):
    return any(a <= pos < b for a, b in spans)


def scan_files():
    seen, out = set(), []
    for g in SCAN_GLOBS:
        for p in sorted(ROOT.glob(g)):
            if not p.is_file() or p.name in EXCLUDE_NAMES:
                continue
            if p.relative_to(ROOT).as_posix() in EXCLUDE_PATHS:
                continue
            if any(p.match(pat) for pat in EXCLUDE_PATTERNS):
                continue
            if p.resolve() in seen:
                continue
            seen.add(p.resolve())
            out.append(p)
    return out


def check_a(files, vocab, verbose):
    hits = []
    for p in files:
        for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            low = line.lower()
            spans = quoted_spans(line)
            for marker in FUTURE_MARKERS:
                i = low.find(marker)
                if i < 0 or in_quotes(i, spans):
                    continue
                named = [v for v in vocab if v.lower() in low]
                if named or verbose:
                    hits.append((p, n, marker, named[:3], line.strip()))
                break
    return hits


def check_b(files):
    hits = []
    for p in files:
        for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            spans = quoted_spans(line)
            for m in COUNT_RE.finditer(line):
                if not in_quotes(m.start(), spans):
                    hits.append((p, n, m.group(0).strip(), line.strip()))
    return hits


def check_c():
    """A '## Heading (TOKEN)' whose rows do not all mention TOKEN."""
    p = ROOT / "docs" / "data_sources.md"
    if not p.exists():
        return []
    hits, heading, token, rows, hline = [], None, None, [], 0

    def close():
        if token and rows:
            miss = [r for r in rows if token.lower() not in r.lower()]
            if miss:
                hits.append((p, hline, heading, token, len(miss), len(rows)))

    for n, l in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if l.startswith("## "):
            close()
            heading, rows, hline = l.strip(), [], n
            m = re.search(r"\(([A-Za-z][A-Za-z0-9 /&-]{1,20})\)", heading)
            token = m.group(1) if m else None
        elif token and l.startswith("| ") and not re.match(r"^\|[\s:-]+\|", l):
            if not l.startswith("| City ") and not l.startswith("| Source "):
                rows.append(l)
    close()
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true",
                    help="A: report markers even when no built place is named")
    ap.add_argument("--only", choices=["A", "B", "C"])
    args = ap.parse_args()

    cities, vocab = built_vocabulary()
    files = scan_files()
    print(f"check_stale_claims: {len(files)} files, {len(cities)} built cities "
          f"in the vocabulary")
    print("  (DECISIONS.md and PLAN.md are deliberately excluded - see the "
          "module docstring)\n")

    if args.only in (None, "A"):
        hits = check_a(files, vocab, args.verbose)
        print(f"A. FUTURE TENSE about something that IS built - {len(hits)}")
        for p, n, marker, named, line in hits:
            where = f" names {named}" if named else " (no built place named)"
            print(f"   {p.relative_to(ROOT).as_posix()}:{n}  [{marker}]{where}")
            print(f"      {line[:150]}")
        if not hits:
            print("   none")
        print()

    if args.only in (None, "B"):
        hits = check_b(files)
        print(f"B. HAND-KEPT COUNTS - {len(hits)} to eyeball")
        print("   Prefer DELETING a count and letting a check own the number; "
              "correcting it only\n   resets the clock until it drifts again.")
        by_file = {}
        for p, n, frag, line in hits:
            by_file.setdefault(p, []).append((n, frag))
        for p, items in sorted(by_file.items(), key=lambda kv: -len(kv[1])):
            print(f"   {p.relative_to(ROOT).as_posix()}  ({len(items)})")
            for n, frag in items[:8]:
                print(f"      :{n}  ...{frag}...")
            if len(items) > 8:
                print(f"      ...and {len(items) - 8} more")
        if not hits:
            print("   none")
        print()

    if args.only in (None, "C"):
        hits = check_c()
        print(f"C. HEADINGS whose rows no longer match the label - {len(hits)}")
        for p, n, heading, token, miss, total in hits:
            print(f"   {p.relative_to(ROOT).as_posix()}:{n}  {heading}")
            print(f"      {miss} of {total} rows never mention '{token}'")
        if not hits:
            print("   none")
        print()

    print("Reported, not failed - every rule here is a guess about English. "
          "Exit 0 by design.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
