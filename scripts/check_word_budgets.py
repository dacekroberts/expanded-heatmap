"""The files every session loads stay inside a word budget.

    python scripts/check_word_budgets.py            # fails a file over its budget
    python scripts/check_word_budgets.py --report   # sizes and headroom, never fails

WHY. The efficiency review of 2026-10-04 (docs/efficiency_review_2026-10-04.md,
finding 3) found the trims of 2026-09-27 regrowing: CLAUDE.md 1,685 -> 2,797
words, PLAN.md 3,136 -> 12,565 (59 done items still in it), session_roles.md
2,643 -> 4,748. Every session reads CLAUDE.md, and most read PLAN.md first, so
each word is paid on every call. The owner made the budgets a check
(2026-10-04, the review's third change); they are trimmed back at the weekly
archive (`scripts/archive_decisions.py`, Sunday), done PLAN items moving to
docs/plan_done/<Sunday>.md.

Words are whitespace-separated tokens, as scripts/efficiency_metrics.py counts
them. Raising a budget is a decision for the owner, not an edit.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUDGETS = {
    "CLAUDE.md": 2000,
    "PLAN.md": 5000,
    "docs/session_roles.md": 3000,
}


def words(rel):
    p = ROOT / rel
    return len(p.read_text(encoding="utf-8").split()) if p.exists() else 0


def main():
    report = "--report" in sys.argv[1:]
    over = []
    for rel, budget in BUDGETS.items():
        n = words(rel)
        flag = "OVER" if n > budget else "ok"
        if n > budget:
            over.append(rel)
        print(f"  {flag:4}  {rel:28} {n:6,} / {budget:,} words")
    if over and not report:
        print(f"\nFAIL: {len(over)} file(s) over budget. Move detail out (DECISIONS, "
              "docs/rule_history.md, a skill, docs/plan_done/) rather than raising a budget.")
        sys.exit(1)
    print("\nOK - every budgeted file is within its budget." if not over else "")


if __name__ == "__main__":
    main()
