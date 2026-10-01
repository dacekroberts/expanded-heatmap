"""Watch scripts/check_master_list_counts.py fail, twenty-three ways.

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
    """Every band heading renamed: an unrecognised file must not pass.

    Matches any '## <marker> Band X' heading rather than naming the bands, so a
    new band (R, 2026-09-28) cannot leave one heading recognised and the case
    silently not-vacuous.
    """
    out = re.sub(r"^(## \S+ )Band ([A-Z])\b", r"\1Group \2", text, flags=re.M)
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


def _plant_t1(lines, name, stated=1):
    """Plant a one-row country sub-group under the tram list's T1 heading and
    return the new lines and the row's index. The tram list emptied on
    2026-09-30 (every T1 city built), so a case that needs a live tram row
    brings its own rather than proving nothing."""
    for i, l in enumerate(lines):
        if M.TIER_HEAD.match(l) and "T1" in l:
            block = ["", f"**🇦🇶 Selftestland ({stated})**", "",
                     "| City | Network |", "|---|---|", f"| **{name}** | a tram |", ""]
            out = lines[:i + 1] + block + lines[i + 1:]
            return out, i + 1 + 5
    return None, None


def plant_subgroup_drift(text):
    """A planted T1 sub-group stating 2 over a one-row table."""
    lines, _ = _plant_t1(text.split("\n"), "Selftestville", stated=2)
    if lines is None:
        return None
    plant_subgroup_drift.expect = "the table below it has 1"
    return "\n".join(lines)


def tram_into(dst):
    """A tram-list row renamed to a city already in master-list Band `dst`: a
    city in two lists ACROSS the two files; `dst` None renames it to a built
    city instead. Needs both texts."""
    def apply(text, other):
        lines, main = text.split("\n"), other.split("\n")
        rows = {}
        for t, s, e in M.sections(lines):
            if M.TIER_HEAD.match(t):
                rows.update(M.members(lines, s, e))
        row = _table_row(rows, lines)
        if not row:
            # The tram list is empty (2026-09-30): plant the row instead.
            planted, i = _plant_t1(lines, "Selftestville")
            if planted is not None:
                lines, row = planted, ("Selftestville", i)
        if dst is None:
            names = [n for r in _built(main) for n in r[3]]
            hit = (names[0], None) if names else None
            places = "Built AND Band T"
        else:
            hit = _table_row(_bands(main).get(dst, {}), main)
            places = f"Band {dst} AND Band T"
        if not row or not hit:
            return None
        apply.expect = f"{hit[0]} is in {places}"
        out = list(lines)
        out[row[1]] = out[row[1]].replace(row[0], hit[0], 1)
        return "\n".join(out)
    apply.two = True
    return apply


def row_left_in_band_t(text):
    """A city row left behind in the master list's Band T section after the
    move to the tram list - a move half made."""
    lines = text.split("\n")
    for t, s, e in M.sections(lines):
        if M.BAND_HEAD.match(t) and M.BAND_HEAD.match(t).group(1) == "T":
            out = lines[:s + 1] + ["", "| City | Note |", "|---|---|",
                                   "| **Selftestville** | left behind |", ""] + lines[s + 1:]
            return "\n".join(out)
    return None


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
     bump(r"^## 🔵 Band B —[^\n]*?\((\d+) cit", "Band B holds"), None),   # "1 city" or "N cities"

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

    # Re-aimed at the tram list 2026-09-29: Band T's country sub-groups moved
    # there with its rows, and the master list kept none.
    # And to a planted T1 sub-group 2026-09-30, when every T1 city was built and
    # the tram list kept none.
    ("a sub-group count drifted (a planted T1 sub-group states 2 over one row)",
     plant_subgroup_drift, None, "tram"),

    ("by country: a row's Candidates figure drifted",
     by_country_bump(2, "the Candidates column sums to"), None),

    ("by country: a row's Built figure disagrees with the Built table",
     by_country_bump(1, "says {new} built, the Built table lists {old}"), None),

    ("by country: the Total row's band figure drifted",
     bump(r"^\| \*\*Total\*\*.*· D (\d+) ·", "the Total row says D {new}"), None),

    ("by country: a named city is not in the band its row lists",
     wrong_band, "its Bands column says"),

    # Aimed at Band R since 2026-09-28, when D emptied (its rows moved to R and C).
    # Re-aimed from Band T to Band C 2026-09-29, when Band T's rows moved to the
    # tram list and the master list's Band T section stopped holding any; and
    # from Band C to Band B the same day, when Band C closed (owner); and to
    # Band R and the tram list 2026-09-30, when Band B emptied (the review
    # rehearsal): Band R is the one master-list band left with rows.
    ("a city in two bands (a tram row renamed to a Band R city)",
     tram_into("R"), None, "tram"),

    ("a built city still listed in a band (a Band R row renamed to a built city)",
     rename_into("R", None), None),

    ("no band recognised at all - the vacuous pass",
     drop_bands, "no '## ... Band X' sections"),

    # The tram list (docs/tram_city_list.md, 2026-09-29): its own counts, and
    # the one-place rule across the two files. The 4th field is the file the
    # mutation edits; "missing" leaves the tram list out of the copy.
    ("tram list: a tier heading's count drifted (T1, +1)",
     bump(r"^## 🟤 T1 —[^\n]*?\((\d+) cities", "T1 holds"), None, "tram"),

    ("tram list: the title's count drifted",
     bump(r"^# [^\n]*— (\d+) cities", "but the tiers hold {old}"), None, "tram"),

    ("tram list: the tier table's count drifted (T2, +1)",
     bump(r"^\| 🟤 \*\*T2\*\* \|.*\| \*\*(\d+)\*\*", "tier table says T2 {new}"), None, "tram"),

    ("tram list: a built city still on the tram list (a tram row renamed to a built city)",
     tram_into(None), None, "tram"),

    ("tram list: a city row left behind in the master list's Band T section",
     row_left_in_band_t, "a move half made", "main"),

    ("tram list: the file is missing while Band T points to it",
     lambda text: text, "which was not found beside", "missing"),
]


def case(label, mutate, expect_in, text, tram, tmp, which="main"):
    target = tram if which == "tram" else text
    if which == "tram" and tram is None:
        changed = None
    elif getattr(mutate, "two", False):
        changed = mutate(target, text)
    else:
        changed = mutate(target)
    if which != "missing" and (changed is None or changed == target):
        print(f"BROKEN TEST  {label}\n      the mutation matched nothing in the live "
              f"file, so this case proves nothing - re-aim it")
        return False
    expect_in = getattr(mutate, "expect", None) or expect_in
    path = Path(tmp) / "city_master_list.md"
    tpath = Path(tmp) / M.TRAM_NAME
    path.write_text(changed if which in ("main", "missing") else text,
                    encoding="utf-8", newline="\n")
    tpath.unlink(missing_ok=True)
    if tram is not None and which != "missing":
        tpath.write_text(changed if which == "tram" else tram, encoding="utf-8", newline="\n")
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
    tram_path = LIST.parent / M.TRAM_NAME
    tram = tram_path.read_text(encoding="utf-8") if tram_path.exists() else None
    with tempfile.TemporaryDirectory() as tmp:
        results = [case(c[0], c[1], c[2], text, tram, tmp, *c[3:]) for c in CASES]

        # THE POSITIVE CONTROL: an unmodified copy must pass. Without it, a
        # check that fails on everything would pass every case above.
        path = Path(tmp) / "city_master_list.md"
        path.write_text(text, encoding="utf-8", newline="\n")
        if tram is not None:
            (Path(tmp) / M.TRAM_NAME).write_text(tram, encoding="utf-8", newline="\n")
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
