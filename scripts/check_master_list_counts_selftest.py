"""Watch scripts/check_master_list_counts.py fail, seventeen ways.

    python scripts/check_master_list_counts_selftest.py

WHY THIS FILE EXISTS. The check reads a document that sessions rewrite every
day, through heuristics about its shape (which tables are city tables, which
headings are city write-ups). A check like that fails in the quiet direction:
a reshaped band stops being recognised, its members count as zero, and - if the
heading's count happened to be edited the same way - nothing is reported. The
only evidence that it still decides anything is watching it refuse a file that
is wrong in each way it claims to catch, and pass the real one.

NOTHING IN THE REPOSITORY IS MODIFIED. Every case copies the live
`docs/city_master_list.md` into a temporary file, breaks the copy with one
exact text replacement, and runs the check there with `--file`. A replacement
that matches nothing is reported as a BROKEN TEST rather than a pass: the live
file has moved on and the case must be re-aimed, or it proves nothing.

The child's output is BYTES, forced to UTF-8 and decoded with
`errors="replace"` - city names such as "Liepāja" and "Göteborg" otherwise come
back empty through a Windows console codepage and read as "expected text not
found" (the trap check_scope_disclosure_selftest.py met twice).
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_master_list_counts.py"
LIST = ROOT / "docs" / "city_master_list.md"

sys.path.insert(0, str(CHECK.parent))
import check_master_list_counts as M  # noqa: E402 - the check's own parsers


def run(path):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(CHECK), "--file", str(path)],
                       cwd=ROOT, capture_output=True, env=env)
    out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", errors="replace")
    return r.returncode, out


def bump(pattern, expect):
    """A mutation adding 1 to the count captured by `pattern`, whatever it is now.

    The counts cases used to name the number ("**33**" -> "**34**"), so every
    legitimate change to the list - five discards added, Kansas City moved to
    Band T, both on 2026-09-27 - broke the self-test and with it the pre-push
    hook. Reading the current number keeps each case aimed. `expect` may use
    {old} and {new}.
    """
    rx = re.compile(pattern, re.M)

    def apply(text):
        m = rx.search(text)
        if not m:
            return None
        old = int(m.group(1))
        apply.expect = expect.format(old=old, new=old + 1)
        return text[:m.start(1)] + str(old + 1) + text[m.end(1):]
    return apply


def drop_bands(text):
    """Every band heading renamed: an unrecognised file must not pass."""
    out = text.replace("## 🟢 Band A", "## 🟢 Group A").replace("## 🟣 Band C", "## 🟣 Group C")
    out = out.replace("## 🔵 Band B", "## 🔵 Group B").replace("## ⚪ Band N", "## ⚪ Group N")
    out = out.replace("## 🟤 Band T", "## 🟤 Group T").replace("## 🔴 Band D", "## 🔴 Group D")
    return out if out != text else None


# --- targets picked from the live file ---------------------------------------
# The cases below used to name their rows (Ottawa, then Bergen; Gimhae renamed
# Brno; Avignon renamed Rennes; Canada), and each broke - taking the pre-push
# hook with it - whenever that row changed (Staging re-aimed one on 2026-09-27,
# e56c471). They now find a row of the right SHAPE through the check's own
# parsers, so an edit to any one city's row cannot break them.

def _section(lines, pattern):
    return next(((s, e) for t, s, e in M.sections(lines) if re.match(pattern, t)), None)


def _bands(lines):
    """{letter: {key: (name, line_index, marked)}} for every band section."""
    out = {}
    for t, s, e in M.sections(lines):
        m = M.BAND_HEAD.match(t)
        if m:
            out[m.group(1)] = M.members(lines, s, e)
    return out


def _table_row(members, lines):
    """(name, line) of the first unbuilt member written as a table row naming it."""
    for name, i, marked in members.values():
        if not marked and lines[i].startswith("|") and name in lines[i]:
            return name, i
    return None


def _built(lines):
    """[(line, country, stated, names, flags)] from the Built table."""
    sec = _section(lines, r"^## Built\b")
    return M.built_table(lines, *sec) if sec else []


def _by_country(lines):
    """(bands column or None, [(line, cells)]) of the by-country table, Total left out."""
    sec = _section(lines, r"^## .*Current by country")
    for head, rows in (M.tables(lines, *sec) if sec else []):
        low = [h.lower() for h in head]
        if low[:3] == ["country", "built", "candidates"]:
            col = low.index("bands") if "bands" in low else None
            return col, [(i, r) for i, r in rows if M.cell_name(r[0]).lower() != "total"]
    return None, []


def _set_cell(lines, i, col, new):
    parts = lines[i].split("|")          # "| a | b |" -> ["", " a ", " b ", ""]
    parts[col + 1] = f" {new} "
    out = list(lines)
    out[i] = "|".join(parts)
    return "\n".join(out)


def rename_into(src, dst):
    """A Band `src` table row renamed to a city already in Band `dst`, or in
    Built when `dst` is None. The check lists Built first, then bands A-Z."""
    def apply(text):
        lines = text.split("\n")
        bands = _bands(lines)
        row = _table_row(bands.get(src, {}), lines)
        if dst is None:
            names = [n for r in _built(lines) for n in r[3]]
            target, places = (names[0] if names else None), f"Built AND Band {src}"
        else:
            hit = _table_row(bands.get(dst, {}), lines)
            target = hit[0] if hit else None
            places = " AND ".join(f"Band {x}" for x in sorted((src, dst)))
        if not row or not target:
            return None
        name, i = row
        apply.expect = f"{target} is in {places}"
        out = list(lines)
        out[i] = out[i].replace(name, target, 1)
        return "\n".join(out)
    return apply


def wrong_band(text):
    """A by-country row naming its cities, whose Bands column holds one letter,
    changed to a letter none of them is in."""
    lines = text.split("\n")
    col, rows = _by_country(lines)
    if col is None:
        return None
    for i, row in rows:
        letters = re.findall(rf"\b[{M.LETTERS}]\b", row[col])
        if len(letters) == 1 and re.match(r"\*\*\d+\*\*\s*—\s*\S", row[2]):
            return _set_cell(lines, i, col, "C" if letters[0] != "C" else "T")
    return None


def by_country_bump(col, expect):
    """+1 on the leading **N** of cell `col` in the first by-country row that
    has one - for the Built column, a country the Built table also lists."""
    def apply(text):
        lines = text.split("\n")
        _, rows = _by_country(lines)
        built = {M.key(c) for _, c, *_ in _built(lines)}
        for i, row in rows:
            m = re.match(r"\*\*(\d+)\*\*", row[col])
            if m and (col != 1 or M.key(M.cell_name(row[0])) in built):
                old = int(m.group(1))
                apply.expect = expect.format(old=old, new=old + 1)
                return _set_cell(lines, i, col, f"**{old + 1}**" + row[col][m.end():])
        return None
    return apply


CASES = [
    # Re-aimed from Band C to Band B 2026-09-28, when C closed (owner).
    ("a band heading's count drifted (Band B, +1)",
     bump(r"^## 🔵 Band B —[^\n]*?\((\d+) cities", "Band B holds"), None),

    ("the summary box's band count drifted (B, +1)",
     bump(r"· B (\d+) ·", "summary says B {new}"), None),

    ("the summary box's discard count drifted",
     bump(r"\| \*\*Discarded\*\* \| \*\*(\d+)\*\*", "summary says discarded {new}"), None),

    ("the summary box's country count drifted",
     bump(r"across (\d+) countries", "across {new} countries"), None),

    ("Band A's built figure drifted in its heading",
     bump(r"ready \+ (\d+) ✅ BUILT", "says {new} built"), None),

    ("the band table's count drifted (T, +1)",
     bump(r"^\| 🟤 \*\*T\*\* \|.*\| \*\*(\d+)\*\*", "band table says T {new}"), None),

    ("the candidate total drifted in its heading",
     bump(r"^## Candidates — (\d+)", "but the bands hold {old}"), None),

    ("the Built heading drifted",
     bump(r"^## Built — (\d+)", "the Built table lists {old}"), None),

    ("a Built row's per-country count drifted",
     bump(r"^\| \*\*[^*|]+\*\* \((\d+)", "lists {old} cities"), None),

    ("a sub-group count drifted (the first one-country sub-group, +1)",
     bump(r"^\*\*\S+ [^*(,]+ \((\d+)\)\*\*", "the table below it has {old}"), None),

    ("by country: a row's Candidates figure drifted",
     by_country_bump(2, "the Candidates column sums to"), None),

    ("by country: a row's Built figure disagrees with the Built table",
     by_country_bump(1, "says {new} built, the Built table lists {old}"), None),

    ("by country: the Total row's band figure drifted",
     bump(r"^\| \*\*Total\*\*.*· T (\d+) ·", "the Total row says T {new}"), None),

    ("by country: a named city is not in the band its row lists",
     wrong_band, "its Bands column says"),

    ("a city in two bands (a Band D row renamed to a Band T city)",
     rename_into("D", "T"), None),

    ("a built city still listed in a band (a Band T row renamed to a built city)",
     rename_into("T", None), None),

    ("no band recognised at all - the vacuous pass",
     drop_bands, "no '## ... Band X' sections"),
]


def case(label, mutate, expect_in, text, tmp):
    changed = mutate(text)
    if changed is None or changed == text:
        print(f"BROKEN TEST  {label}\n      the mutation matched nothing in the live "
              f"file, so this case proves nothing - re-aim it")
        return False
    expect_in = getattr(mutate, "expect", None) or expect_in
    path = Path(tmp) / "city_master_list.md"
    path.write_text(changed, encoding="utf-8", newline="\n")
    code, out = run(path)
    hit = [ln for ln in out.splitlines() if expect_in in ln]
    ok = code == 1 and bool(hit)
    print(f"{'PASS' if ok else 'DID NOT FAIL'}  {label}")
    print(f"      exit {code} (wanted 1); "
          f"{hit[0].strip()[:150] if hit else 'expected text not found: ' + expect_in!r}")
    return ok


def main():
    print(f"Self-test for {CHECK.relative_to(ROOT).as_posix()}\n")
    text = LIST.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        results = [case(*c, text, tmp) for c in CASES]

        # THE POSITIVE CONTROL: an unmodified copy must pass. Without it, a
        # check that fails on everything would pass every case above.
        path = Path(tmp) / "city_master_list.md"
        path.write_text(text, encoding="utf-8", newline="\n")
        code, out = run(path)
    clean = code == 0
    print(f"\n{'PASS' if clean else 'FAIL'}  an unmodified copy passes (exit {code})")
    if not clean:
        print("      " + " | ".join(out.strip().splitlines()[:3]))

    failed = results.count(False) + (0 if clean else 1)
    print(f"\n{len(results) + 1 - failed} of {len(results) + 1} cases behaved as intended.")
    if failed:
        print("\nA case that did not fail means the check does not decide what it claims "
              "to, OR the live file changed so the case's text no longer exists. If the "
              "positive control failed, the live file itself has a drifted count: run "
              "check_master_list_counts.py and fix the file first.")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
