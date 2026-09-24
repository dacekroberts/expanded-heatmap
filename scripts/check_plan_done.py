"""Report PLAN.md's done items, and which of them its own rule says can go.

    python scripts/check_plan_done.py            # summary, one line per item
    python scripts/check_plan_done.py --verbose  # plus the candidate entries

PLAN.md's legend says a `[x]` item "stays only until its DECISIONS.md entry
exists". Nothing enforced that, and on 2026-09-24 PLAN.md held 43 done items in
1,695 lines - the file every session reads first. This reports, for each top-level
`- [x]` item:

  REMOVABLE  it cites a DECISIONS.md entry (*"title"*) and that entry exists;
  CANDIDATE  it cites none, but DECISIONS.md headings share its date and its
             distinctive words - a person must confirm the match;
  KEEP(open) it still holds open work (an unticked sub-item, "left behind",
             "not yet"...) - whatever it cites, it is not done;
  KEEP?      nothing in DECISIONS.md looks like it - the entry may be missing,
             which is itself worth fixing before the item goes.

REPORTS, NEVER FAILS, and never edits. Whether a done item still earns its place
(some are kept "for the checklist below, which the follower cities still read")
is a judgement; this makes the judgement cheap. Exit 0 by design, like
check_stale_claims.py.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "PLAN.md"
DECISIONS = ROOT / "DECISIONS.md"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADING = re.compile(r"^### (\d{4}-\d{2}-\d{2}) - (.+)$", re.M)
CITED = re.compile(r'\*"([^"]{8,})"\*')
OPEN = re.compile(r"^\s*- \[[ ~]\]|left behind|still open|remains? open|"
                  r"to settle|not yet|\bTODO\b", re.I | re.M)
DATE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
WORD = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]{3,}")
STOP = set("""this that with from were have been their there which when what
into only than they then them also does done here each more most over some
such your about after before being built city cities line lines entry entries
decisions plan item items still later below above since until owner session
""".split())


def items(text):
    """(line number, text) for every top-level `- [x]` item."""
    out, cur, start = [], None, 0
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("- [x]"):
            if cur is not None:
                out.append((start, "\n".join(cur)))
            cur, start = [line], n
        elif cur is not None and (line.startswith("- [") or line.startswith("#")
                                  or line.strip() == "---"):
            out.append((start, "\n".join(cur)))
            cur = None
        elif cur is not None:
            cur.append(line)
    if cur is not None:
        out.append((start, "\n".join(cur)))
    return out


def words(s):
    return {w.lower() for w in WORD.findall(s)} - STOP


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    plan = PLAN.read_text(encoding="utf-8")
    heads = HEADING.findall(DECISIONS.read_text(encoding="utf-8"))
    counts = {"REMOVABLE": 0, "CANDIDATE": 0, "KEEP?": 0, "KEEP(open)": 0}
    for line, body in items(plan):
        title = re.sub(r"[*`]", "", body.splitlines()[0][6:]).strip()[:70]
        cited = [c for c in CITED.findall(body)
                 if any(c.lower().rstrip(".") in h.lower() for _, h in heads)]
        # A recorded item can still hold live work - Prague's carried an open
        # reminder (Flora reopens around December 2026) and Copenhagen's open
        # owner actions, and both were first reported REMOVABLE. Open work
        # outranks a citation.
        open_work = OPEN.search(body)
        if open_work:
            verdict = "KEEP(open)"
            why = f"holds open work: {open_work.group(0).strip()!r}"
        elif cited:
            verdict, why = "REMOVABLE", f'cites "{cited[0][:50]}"'
        else:
            dates, mine = set(DATE.findall(body)), words(body)
            scored = sorted(((len(mine & words(h)), d, h) for d, h in heads
                             if not dates or d in dates), reverse=True)
            best = [s for s in scored if s[0] >= 3][:2]
            verdict = "CANDIDATE" if best else "KEEP?"
            why = (f'best: {best[0][1]} "{best[0][2][:55]}"' if best
                   else "no DECISIONS heading resembles it")
        counts[verdict] += 1
        print(f"  {verdict:9s} PLAN.md:{line:<5d} {title}")
        if args.verbose:
            print(f"            {why}")
    print(f"\n{sum(counts.values())} done items: " +
          ", ".join(f"{v} {k}" for k, v in counts.items()) +
          ". Reported, not failed - see the docstring.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
