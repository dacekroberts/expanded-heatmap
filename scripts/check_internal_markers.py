"""Every `<!-- internal -->` span in the docs the reference pages render hides
what it should and leaves good prose behind.

    python scripts/check_internal_markers.py              # the rendered docs
    python scripts/check_internal_markers.py --selftest   # touches nothing

About the Data and What Is Excluded render these docs verbatim, less every
`<!-- internal -->...<!-- /internal -->` span (`app/country_sections.public()`,
owner 2026-10-01). A marker that is wrong fails silently in one of two ways:
an unclosed or misspelled marker hides nothing, so the process note shows; a
span that runs too far hides a license verdict or a notice. This check reads
the pattern from `country_sections.py` itself, so the two cannot drift.

FAILS on, per file:
  A. a comment that mentions "internal" but is not exactly one of the two
     markers (`<!--internal-->`, `<!-- Internal -->`): public() ignores it;
  B. markers out of order: a close with no open, an open inside an open, or an
     open never closed;
  C. a span that crosses a blank line without being a block (a block opens at
     the start of a line and closes at the end of one: a whole process-only
     passage, hidden on purpose), or that holds a `|` (a table cell boundary);
  D. what the reader sees at the seam where a span was removed: empty
     parentheses, a space before punctuation, a dash left dangling, or a
     bullet or quote line left empty. A double space is allowed: Markdown
     collapses it.
The rules come from the 2026-10-02 marking pass (`docs/city_page_format.md`,
section 3).
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "app" / "country_sections.py"
DOCS = ["docs/data_sources.md", "docs/excluded_categories.md", "docs/data_sources/*.md"]

COMMENT = re.compile(r"<!--(.*?)-->", re.S)
OPEN, CLOSE = "<!-- internal -->", "<!-- /internal -->"
BLANK = re.compile(r"\n[ \t]*\n")
EMPTY_LINE = re.compile(r"^\s*(?:[-*+>]|\d+\.)\s*$")


def internal_pattern():
    """INTERNAL as country_sections.py defines it, without importing streamlit."""
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if (isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "INTERNAL"
                                                  for t in node.targets)):
            call = node.value
            pattern = ast.literal_eval(call.args[0])
            flags = re.S if any("S" in ast.dump(a) for a in call.args[1:]) else 0
            return re.compile(pattern, flags)
    sys.exit(f"{SOURCE}: no INTERNAL pattern found")


def line_no(text, pos):
    return text.count("\n", 0, pos) + 1


def problems(text, pattern):
    out = []
    # A: near-miss markers
    for m in COMMENT.finditer(text):
        body = m.group(0)
        if "internal" in body.lower() and body not in (OPEN, CLOSE):
            out.append(f"line {line_no(text, m.start())}: A malformed marker {body!r}")
    # B: order
    depth, opened = 0, None
    for m in re.finditer(re.escape(OPEN) + "|" + re.escape(CLOSE), text):
        if m.group(0) == OPEN:
            if depth:
                out.append(f"line {line_no(text, m.start())}: B an open marker inside the span "
                           f"opened at line {line_no(text, opened)}")
            depth, opened = depth + 1, m.start()
        else:
            if not depth:
                out.append(f"line {line_no(text, m.start())}: B a close marker with no open")
            depth = max(depth - 1, 0)
    if depth:
        out.append(f"line {line_no(text, opened)}: B an open marker never closed")
    # C and D: each span public() removes
    for m in pattern.finditer(text):
        where = f"line {line_no(text, m.start())}"
        span = m.group(0)
        block = (m.start() == 0 or text[m.start() - 1] == "\n") and text[m.end():m.end() + 1] in ("", "\n")
        if BLANK.search(span) and not block:
            out.append(f"{where}: C the span crosses a blank line and is not a block")
        # A span inside a table cell breaks the table; a BLOCK span hides whole
        # lines, a table's included, and cannot (owner, 2026-10-03: whole
        # research-note sections hidden, tables and all).
        if "|" in span and not block:
            out.append(f"{where}: C the span holds a '|' (a table cell boundary)")
        left, right = text[:m.start()], text[m.end():]
        l1, r1 = left[-1:], right[:1]
        if left.rstrip(" ").endswith("(") and right.lstrip(" ").startswith(")"):
            out.append(f"{where}: D empty parentheses left")
        elif l1 == " " and r1 in (",", ".", ";", ":", ")"):
            out.append(f"{where}: D a space left before {r1!r}")
        if left.rstrip().endswith(("—", " -")) and right.lstrip(" ")[:1] in ("", "\n", ".", ")", ","):
            out.append(f"{where}: D a dash left dangling")
        seam = left[left.rfind("\n") + 1:] + right.split("\n", 1)[0]
        if EMPTY_LINE.match(seam) and (left[left.rfind("\n") + 1:].strip() or right.split("\n", 1)[0].strip()):
            out.append(f"{where}: D an empty bullet or quote line left")
    return out


def files():
    for g in DOCS:
        yield from sorted(ROOT.glob(g))


def selftest():
    pattern = internal_pattern()
    cases = [
        ("clean phrase", f"Data from X{OPEN} (read by an agent){CLOSE}. Next.", 0),
        ("clean bullet", f"- Kept.\n{OPEN}- A process note.\n{CLOSE}- Kept too.", 0),
        ("malformed", "Text <!--internal--> note <!-- /internal --> end.", 2),
        ("unclosed", f"Text {OPEN} note never closed.", 1),
        ("nested", f"{OPEN} a {OPEN} b {CLOSE} c {CLOSE}", 1),
        ("blank line", f"Para one{OPEN} note\n\nPara two{CLOSE}.", 1),
        ("block", f"Kept.\n\n{OPEN}**A process section.**\n\nTwo paragraphs.{CLOSE}\n\nKept.", 0),
        ("double space", f"Kept. {OPEN}A note.{CLOSE} Kept.", 0),
        ("table cell", f"| a{OPEN} b | c{CLOSE} |", 1),
        ("block holding a table", f"Kept.\n\n{OPEN}\n### Notes\n\n| a | b |\n|---|---|\n| 1 | 2 |\n{CLOSE}\n\nKept.", 0),
        ("empty parens", f"Verdict ({OPEN}read 2026-09-24{CLOSE}).", 1),
        ("space before period", f"The verdict is open {OPEN}see PLAN{CLOSE}.", 1),
        ("dangling dash", f"An open decision —{OPEN} see PLAN{CLOSE}.", 1),
        ("empty bullet", f"- {OPEN}Run the check.{CLOSE}\n- Kept.", 1),
    ]
    bad = 0
    for name, text, want in cases:
        got = len(problems(text, pattern))
        ok = got == want
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {got} problem(s), expected {want}")
    print(f"{len(cases) - bad} of {len(cases)} cases behaved as intended.")
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    pattern = internal_pattern()
    total, spans = [], 0
    for path in files():
        text = path.read_text(encoding="utf-8")
        spans += len(pattern.findall(text))
        for p in problems(text, pattern):
            total.append(f"{path.relative_to(ROOT).as_posix()} {p}")
    for p in total:
        print(f"FAIL {p}")
    if total:
        print(f"{len(total)} problem(s) in the internal markers.")
        return 1
    print(f"OK - {spans} internal span(s) in the rendered docs, each closed, contained and clean.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
