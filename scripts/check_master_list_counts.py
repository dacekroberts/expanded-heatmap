"""Every count docs/city_master_list.md states agrees with the rows it counts,
and no city sits in two lists.

    python scripts/check_master_list_counts.py
    python scripts/check_master_list_counts.py --verbose     # print each list's members
    python scripts/check_master_list_counts.py --file X.md   # for controls (the self-test)

Exits non-zero naming every disagreement. Read-only, standard library only.

WHY. `CLAUDE.md` sends every session to this file to READ COUNTS OFF, and the
counts were the part of it that kept going wrong. The efficiency review of
2026-09-27 (docs/efficiency_review_2026-09-27.md, finding 5) found that 79 of
its last 149 edits changed a count in a heading or the summary block, and at
least five commits existed only to fix counts that had drifted. The file
recorded its own failures and kept repeating them:

  - the summary box read 20 / 33 / 30 from 2026-09-22 while the band sections
    below it moved on ("the hand-kept summary is the first thing to drift");
  - the band table read A 9 / B 10 / C 12 / D 2 until 2026-09-23, left
    standing under two renumbers that updated the headings and not the table;
  - on 2026-09-27 Band A's figure was "corrected from a stale 10 + 28" and the
    candidate total "from a stale 24 to 20", both in the same day's edits.

Each count is stated in up to four places - a heading, the summary box, the
band table, and sometimes a sub-group line - and each place was corrected by
hand, separately. A person republishing the list in chat is told to "verify the
band counts sum to the candidate total before sending", because "that
arithmetic has been wrong twice". That is a check, so it is one now.

It also enforces the owner's rule of 2026-09-27: a city sits in ONE place -
Built, one band, or the discards - never two. Built cities keep their struck-out
rows in Band A as the record of what screening promised; those are the one
sanctioned overlap, and each must really be in the Built table.

WHAT COUNTS AS A MEMBER of a band (between its `## ... Band X` heading and the
next `##`):

  1. a row of a table whose first column (after an optional `#`) is headed
     `City` or `Cities` - the first bold name in that cell, or the cell's text;
  2. a `### <flag> Name - ...` heading (a per-city write-up, as Band C's
     Singapore); a heading that says "cities" is a group, not a city;
  3. a `▲ **<flag> Name joined ...**` announcement (Monterrey), names split on
     commas and "and"; the flag is what separates a city from "Six joined";
  4. a `**▲ Name** <flag>` paragraph opener (Stockholm and Zurich).

The owner's chat format puts every city in a table row, and the first form is
the one to use. The other three are recognised because Band A and Band C
already hold cities written up that way; a city added in a shape none of these
recognises is reported as a count that disagrees, with the members that WERE
found listed, so the fix is visible.

A Band A member is BUILT if its row is marked ✅ or struck through, or if its
name is in the Built table. Names are compared without parentheticals, so
"Guadalajara" matches "Guadalajara (Regional)".

The Built table is counted by names in each row (` · `-separated); its
per-country figures are checked against `app/cities.py` separately, by
`scripts/check_provenance.py` check E. The discard rows' evidence is checked by
`scripts/check_discard_evidence.py`; this script only counts them.

THE TRAM LIST (owner, 2026-09-29). Band T's cities moved to their own file,
`docs/tram_city_list.md`, sorted into tiers (`## ... T1 ... (N cities)`), so
the tram cities can be worked through apart from the rest. When the master
list's Band T section names that file, Band T's members are read from the
tram list's tier sections instead - the master list's own Band T section must
then hold no city rows - and every count the tram list states (its title, each
tier heading, its tier table, its country sub-groups) is checked the same way.
Band T still counts toward the candidate total, and a city still sits in ONE
place across both files. The tram list is looked for beside the file checked,
so `--file` controls can carry their own copy.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST = ROOT / "docs" / "city_master_list.md"
TRAM_NAME = "tram_city_list.md"      # Band T's own file, beside the master list

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FLAG = "[\U0001F1E6-\U0001F1FF]{2}"
FLAG_RE = re.compile(FLAG)
BOLD = re.compile(r"\*\*(.+?)\*\*")
SEP = re.compile(r"^\|[\s:|-]+\|\s*$")
BAND_HEAD = re.compile(r"^## .*\bBand ([A-Z])\b")
TIER_HEAD = re.compile(r"^## .*?\b(T\d)\b")
# Every band letter a candidate can sit in. B reopened (passed: narrower
# pages) and N created (no page for now) by the owner 2026-09-28, when C
# closed; later the same day N was retooled as C (closer to a page) and D
# split into D (blocked, the owner can act) and R (restricted).
LETTERS = "ABCDRT"


# --- reading the file -------------------------------------------------------

def sections(lines):
    """[(title, start, end)] for every `## ` section, ending at the next `##`
    or `#` heading. Line numbers are 0-based indexes into `lines`."""
    heads = [i for i, l in enumerate(lines) if l.startswith("## ") or l.startswith("# ")]
    out = []
    for k, i in enumerate(heads):
        if lines[i].startswith("## "):
            end = heads[k + 1] if k + 1 < len(heads) else len(lines)
            out.append((lines[i], i, end))
    return out


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(lines, start, end):
    """[(header_cells, [(line_index, row_cells)])] for tables in [start, end)."""
    out, i = [], start
    while i < end - 1:
        if lines[i].startswith("|") and SEP.match(lines[i + 1]):
            head, rows, i = cells(lines[i]), [], i + 2
            while i < end and lines[i].startswith("|"):
                rows.append((i, cells(lines[i])))
                i += 1
            out.append((head, rows))
        else:
            i += 1
    return out


def clean(text):
    text = re.sub(r"~~|`|\*", "", text)
    text = FLAG_RE.sub("", text)
    return re.sub(r"[▲▼✅↓⇄]", "", text).strip(" \t—-:,")


def key(name):
    """Compare names without parentheticals, case or accents' composition."""
    name = unicodedata.normalize("NFC", clean(name))
    name = re.sub(r"\s*\([^)]*\)", "", name)
    return re.sub(r"\s+", " ", name).strip().lower()


def cell_name(cell):
    m = BOLD.search(cell)
    return clean(m.group(1) if m else cell)


def members(lines, start, end):
    """{key: (display name, line_index, marked_built)} for one band section."""
    found = {}

    def add(name, i, marked=False):
        k = key(name)
        if k and k not in found:
            found[k] = (clean(name), i, marked)
        elif k and marked:
            found[k] = (found[k][0], found[k][1], True)

    for head, rows in tables(lines, start, end):
        col = 1 if head and head[0] == "#" and len(head) > 1 else 0
        if head[col].lower() not in ("city", "cities"):
            continue
        for i, row in rows:
            if len(row) <= col:
                continue
            marked = "✅" in row[0] or "~~" in row[col]
            add(cell_name(row[col]), i, marked)

    for i in range(start, end):
        line = lines[i]
        m = re.match(rf"^###\s+[▲▼\s]*({FLAG})\s*(.+?)\s+—\s+(.*)$", line)
        if m and "cities" not in m.group(3).lower():
            add(m.group(2), i)
        for m in re.finditer(r"[▲▼]+\s*\*\*([^*]*?)\s+joined\b", line):
            if FLAG_RE.search(m.group(1)):
                for name in re.split(r",\s*|\s+and\s+", clean(m.group(1))):
                    add(name, i)
        m = re.match(rf"^\*\*[▲▼]\s*([^*]+?)\*\*\s*{FLAG}", line)
        if m:
            add(m.group(1), i)
    return found


def built_table(lines, start, end):
    """[(line_index, country, stated_count, [names], flags)] from the Built table."""
    out = []
    for head, rows in tables(lines, start, end):
        if [h.lower() for h in head[:2]] != ["country", "cities"]:
            continue
        for i, row in rows:
            country = cell_name(row[0])
            m = re.search(r"\((\d+)", row[0])
            names = []
            for seg in row[1].split(" · "):
                seg = FLAG_RE.sub("", seg).strip()
                b = re.match(r"^\*\*(.+?)\*\*", seg)
                name = b.group(1) if b else re.split(r"\s+\*\(|\s+\(|\s+—\s", seg)[0]
                if clean(name):
                    names.append(clean(name))
            out.append((i, country, int(m.group(1)) if m else None, names,
                        set(FLAG_RE.findall(row[1]))))
    return out


# --- the check --------------------------------------------------------------

def tram_list(text):
    """Band T's members from the tram list, and every count it states.

    Returns ({key: (name, line_index, False)}, problems, {tier: count})."""
    lines = text.splitlines()
    problems, found, tiers = [], {}, {}
    for t, s, e in sections(lines):
        m = TIER_HEAD.match(t)
        if not m:
            continue
        tier = m.group(1)
        mem = members(lines, s, e)
        tiers[tier] = len(mem)
        h = re.search(r"\((\d+)\s+cit", t)
        if not h:
            problems.append(f"tram list: {tier}'s heading states no '(N cities)': {t!r}")
        elif int(h.group(1)) != len(mem):
            problems.append(f"tram list: heading '{t}' says {h.group(1)}, but {tier} holds "
                            f"{len(mem)}: {_names({k: v[0] for k, v in mem.items()})}")
        problems += [f"tram list: {p}" for p in subgroups(lines, s, e, tier)]
        for k, (name, i, _) in mem.items():
            if k in found:
                problems.append(f"tram list: {name} is in {found[k][3]} AND {tier} - one tier "
                                f"per city")
            else:
                found[k] = (name, i, False, tier)
    if not tiers:
        problems.append("tram list: no '## ... T1 ... (N cities)' tier sections - the file "
                        "changed shape; update this check rather than let it pass vacuously")
    total = len(found)
    title = next((l for l in lines if l.startswith("# ")), "")
    m = re.search(r"—\s*(\d+)\s+cities", title)
    if not m:
        problems.append(f"tram list: the title states no '— N cities': {title!r}")
    elif int(m.group(1)) != total:
        problems.append(f"tram list: title '{title}' but the tiers hold {total}")
    for head, rows in tables(lines, 0, len(lines)):
        if not head or head[0].lower() != "tier":
            continue
        for i, row in rows:
            n = re.search(r"(\d+)", row[-1])
            if not n:
                continue
            tm = re.search(r"\*\*(T\d)\*\*", row[0])
            if tm and int(n.group(1)) != tiers.get(tm.group(1), 0):
                problems.append(f"tram list line {i + 1}: tier table says {tm.group(1)} "
                                f"{n.group(1)}, the tier holds {tiers.get(tm.group(1), 0)}")
            elif not tm and "total" in row[0].lower() and int(n.group(1)) != total:
                problems.append(f"tram list line {i + 1}: tier table says total "
                                f"{n.group(1)}, the tiers hold {total}")
    return {k: v[:3] for k, v in found.items()}, problems, tiers


def check(text, tram_text=None):
    """Return (report, problems). `report` is {list name: {key: name}}.

    `tram_text` is docs/tram_city_list.md, read when Band T points to it."""
    lines = text.splitlines()
    problems = []
    secs = sections(lines)
    tiers = {}

    def find(pred):
        return [(t, s, e) for t, s, e in secs if pred(t)]

    # ---- Built
    built_secs = find(lambda t: re.match(r"^## Built\b", t))
    if not built_secs:
        return {}, ["no '## Built - N' section"]
    title, s, e = built_secs[0]
    rows = built_table(lines, s, e)
    built_rows = rows          # `rows` is reused for the discard tables below
    if not rows:
        problems.append("the Built section has no '| Country | Cities |' table")
    built_names = [n for r in rows for n in r[3]]
    built = {key(n): n for n in built_names}
    if len(built) != len(built_names):
        dupes = sorted({n for n in built_names if built_names.count(n) > 1})
        problems.append(f"the Built table names a city twice: {dupes}")
    for i, country, stated, names, _ in rows:
        if stated is not None and stated != len(names):
            problems.append(f"line {i + 1}: Built row '{country} ({stated})' lists "
                            f"{len(names)} cities: {' · '.join(names)}")
    # Distinct flags across the rows, plus one per flagless row: a country can
    # span two region rows (South Korea in East Asia and the Seoul Capital Area,
    # 2026-09-29) and is still one country.
    countries = len({fl for *_, f in rows if f for fl in f}) + sum(1 for *_, f in rows if not f)
    m = re.match(r"^## Built\s*—\s*(\d+)", title)
    if not m:
        problems.append(f"the Built heading states no count: {title!r}")
    elif int(m.group(1)) != len(built_names):
        problems.append(f"heading '{title}' but the Built table lists {len(built_names)}")

    # ---- bands
    bands = {}
    for t, s, e in secs:
        m = BAND_HEAD.match(t)
        if m:
            bands[m.group(1)] = (t, s, e, members(lines, s, e))
    if not bands:
        problems.append("no '## ... Band X' sections found - the file changed shape; "
                        "update this check rather than let it pass vacuously")
    if "T" in bands and TRAM_NAME in "\n".join(lines[bands["T"][1]:bands["T"][2]]):
        t, s, e, mem = bands["T"]
        if mem:
            problems.append(f"Band T's cities live on the tram list, but the master list's "
                            f"Band T section still holds {_names({k: v[0] for k, v in mem.items()})}"
                            f" - a move half made")
        if tram_text is None:
            problems.append(f"Band T points to {TRAM_NAME}, which was not found beside the "
                            f"master list")
        else:
            mem, tram_problems, tiers = tram_list(tram_text)
            problems += tram_problems
            bands["T"] = (t, s, e, mem)
    ready, built_in_a = {}, {}
    for letter, (t, s, e, mem) in bands.items():
        for k, (name, i, marked) in mem.items():
            if letter == "A" and (marked or k in built):
                built_in_a[k] = name
                if k not in built:
                    problems.append(f"line {i + 1}: Band A marks {name} built, but the "
                                    f"Built table does not list it")
            else:
                ready.setdefault(letter, {})[k] = name
    actual = {letter: len(ready.get(letter, {})) for letter in bands}
    for letter in LETTERS:
        actual.setdefault(letter, 0)

    for letter, (t, s, e, mem) in bands.items():
        if letter == "A":
            m = re.search(r"\((\d+)\s+ready\s*\+\s*(\d+)", t)
            if not m:
                problems.append(f"Band A's heading states no 'N ready + N built': {t!r}")
            else:
                if int(m.group(1)) != actual["A"]:
                    problems.append(f"heading '{t}' says {m.group(1)} ready, but Band A "
                                    f"holds {actual['A']}: {_names(ready.get('A'))}")
                if int(m.group(2)) != len(built_in_a):
                    problems.append(f"heading '{t}' says {m.group(2)} built, but Band A "
                                    f"keeps {len(built_in_a)} built rows")
        else:
            m = re.search(r"\((\d+)\s+cit", t)
            if not m:
                problems.append(f"Band {letter}'s heading states no '(N cities)': {t!r}")
            elif int(m.group(1)) != actual[letter]:
                problems.append(f"heading '{t}' says {m.group(1)}, but Band {letter} "
                                f"holds {actual[letter]}: {_names(ready.get(letter))}")
        problems += subgroups(lines, s, e, letter)

    # ---- open gap and discards
    gap = {}
    for t, s, e in find(lambda t: "OPEN SCREENING GAP" in t.upper()):
        gap.update({k: v[0] for k, v in members(lines, s, e).items()})
    discards = {}
    disc_secs = find(lambda t: t.startswith("## DISCARDED"))
    if not disc_secs:
        problems.append("no '## DISCARDED' section")
    for t, s, e in disc_secs:
        for head, rows in tables(lines, s, e):
            if head and head[0].lower() == "city":
                for i, row in rows:
                    discards[key(cell_name(row[0]))] = cell_name(row[0])
        m = re.match(r"^## DISCARDED\s*—\s*(\d+)", t)
        if m and int(m.group(1)) != len(discards):
            problems.append(f"heading '{t}' but the discard table holds {len(discards)}")

    candidates = sum(actual[x] for x in LETTERS)
    m = find(lambda t: t.startswith("## Candidates"))
    if not m:
        problems.append("no '## Candidates - N' section")
    else:
        t, s, e = m[0]
        h = re.match(r"^## Candidates\s*—\s*(\d+)", t)
        if h and int(h.group(1)) != candidates:
            problems.append(f"heading '{t}' but the bands hold {candidates} "
                            f"({_sum(actual)})")
        problems += band_table(lines, s, e, actual, candidates, len(gap),
                               len(discards), len(built_in_a))

    problems += summary(lines, len(built_names), countries, actual, candidates,
                        len(gap), len(discards))
    problems += by_country(lines, secs, built_rows, ready, actual, candidates,
                           len(built_names))

    # ---- one city, one place
    lists = {"Built": built, "the open gap": gap, "the discards": discards}
    for letter in sorted(ready):
        lists[f"Band {letter}"] = ready[letter]
    where = {}
    for label, names in lists.items():
        for k, name in names.items():
            where.setdefault(k, []).append((label, name))
    for k, places in sorted(where.items()):
        if len(places) > 1:
            problems.append(f"{places[0][1]} is in " + " AND ".join(p for p, _ in places)
                            + " - a city sits in Built, one band, or the discards, never two")

    report = dict(lists)
    report["Band A (built rows kept)"] = built_in_a
    report["_tiers"] = tiers
    return report, problems


def _names(d):
    return ", ".join(sorted((d or {}).values())) or "none"


def _count(cell):
    """Return the leading figure of a 'Built' or 'Candidates' cell; a cell
    holding only a dash is 0."""
    m = re.match(r"^\s*\*\*(\d+)\*\*", cell)
    return int(m.group(1)) if m else (0 if clean(cell) == "" else None)


def by_country(lines, secs, built_rows, ready, actual, candidates, n_built):
    """The '## ✅ Current by country' table against the bands (added 2026-09-27).

    That table is a VIEW of the bands, and it went stale for four days before
    anyone noticed: it said 30 built, listed Brazil as candidates and Japan in
    Band B (Staging rebuilt it on 2026-09-27 and suggested this check). Checked:
    the columns sum to the real totals; the Total row, including its
    'A n · C n · T n · D n', agrees; each country's Built figure matches the
    Built table; and a row that NAMES its candidates names as many as it
    counts, each one in a band its Bands column lists.
    """
    problems = []
    sec = [(t, s, e) for t, s, e in secs if re.match(r"^## .*Current by country", t)]
    if not sec:
        return ["no '## ... Current by country' section - the file changed shape"]
    _, s, e = sec[0]
    table = [(h, r) for h, r in tables(lines, s, e)
             if [x.lower() for x in h[:3]] == ["country", "built", "candidates"]]
    if not table:
        return ["'Current by country' has no '| Country | Built | Candidates |' table"]
    head, rows = table[0]
    bands_col = next((j for j, x in enumerate(head) if x.lower() == "bands"), None)
    band_of = {k: letter for letter, mem in ready.items() for k in mem}
    built_by_country = {key(c): (n, len(names)) for _, c, n, names, _ in built_rows}

    sum_built = sum_cand = 0
    total = None
    for i, row in rows:
        country = cell_name(row[0])
        if country.lower() == "total":
            total = (i, row)
            continue
        b, c = _count(row[1]), _count(row[2])
        if b is None or c is None:
            problems.append(f"line {i + 1}: '{country}' has a Built or Candidates cell "
                            f"with no leading **N** or '—': {row[1]!r} / {row[2]!r}")
            continue
        sum_built += b
        sum_cand += c
        if key(country) in built_by_country and built_by_country[key(country)][1] != b:
            problems.append(f"line {i + 1}: '{country}' says {b} built, the Built table "
                            f"lists {built_by_country[key(country)][1]}")
        named = row[2].split("—", 1)[1] if "—" in row[2] else ""
        names = [n for n in (clean(x) for x in re.split(r"[,;]", named)) if n]
        if not names:
            continue
        if len(names) != c:
            problems.append(f"line {i + 1}: '{country}' counts {c} candidates but names "
                            f"{len(names)}: {', '.join(names)}")
        listed = set(re.findall(rf"\b[{LETTERS}]\b", row[bands_col])) if bands_col else set()
        for n in names:
            letter = band_of.get(key(n))
            if letter is None:
                problems.append(f"line {i + 1}: '{country}' names {n}, which is in no band")
            elif bands_col is not None and letter not in listed:
                problems.append(f"line {i + 1}: '{country}' names {n} (Band {letter}), but "
                                f"its Bands column says {row[bands_col]!r}")

    if sum_built != n_built:
        problems.append(f"'Current by country': the Built column sums to {sum_built}, "
                        f"the Built table lists {n_built}")
    if sum_cand != candidates:
        problems.append(f"'Current by country': the Candidates column sums to {sum_cand}, "
                        f"the bands hold {candidates} ({_sum(actual)})")
    if total is None:
        problems.append("'Current by country' has no Total row")
    else:
        i, row = total
        if _count(row[1]) != n_built or _count(row[2]) != candidates:
            problems.append(f"line {i + 1}: the Total row says {row[1]} built / {row[2]} "
                            f"candidates, the file holds {n_built} / {candidates}")
        for letter, n in re.findall(rf"\b([{LETTERS}]) (\d+)\b", " ".join(row[3:])):
            if int(n) != actual[letter]:
                problems.append(f"line {i + 1}: the Total row says {letter} {n}, Band "
                                f"{letter} holds {actual[letter]}")
    return problems


def _sum(actual):
    return " + ".join(f"{x} {actual[x]}" for x in LETTERS if actual[x] or x == "A")


def subgroups(lines, start, end, letter):
    """A `**<flag> Country (N)**` line counts the table that follows it."""
    problems, pending = [], None
    for i in range(start, end):
        line = lines[i]
        if line.startswith("**"):
            b = BOLD.match(line)
            groups = re.findall(rf"({FLAG})\s*([^(),*]+?)\s*\((\d+)\)", b.group(1)) if b else []
            if groups:
                pending = (i, groups)
        elif pending and line.startswith("|") and i + 1 < end and SEP.match(lines[i + 1]):
            j, rows = i + 2, []
            while j < end and lines[j].startswith("|"):
                rows.append(lines[j])
                j += 1
            at, groups = pending
            if len(groups) == 1:
                flag, name, n = groups[0]
                if int(n) != len(rows):
                    problems.append(f"line {at + 1}: Band {letter} says '{name.strip()} ({n})', "
                                    f"the table below it has {len(rows)} rows")
            else:
                for flag, name, n in groups:
                    got = sum(1 for r in rows if flag in cells(r)[0])
                    if int(n) != got:
                        problems.append(f"line {at + 1}: Band {letter} says '{name.strip()} "
                                        f"({n})', the table below it has {got} {flag} rows")
            pending = None
    return problems


def band_table(lines, start, end, actual, candidates, gap, discards, built_in_a):
    """The '| Band | ... | Cities |' table in the Candidates section."""
    problems, seen = [], False
    for head, rows in tables(lines, start, end):
        if not head or head[0].lower() != "band":
            continue
        seen = True
        for i, row in rows:
            first, last = row[0], row[-1]
            n = re.search(r"(\d+)", last)
            if not n:
                continue
            n = int(n.group(1))
            letter = re.search(r"\*\*([A-Z])\*\*", first)
            if letter:
                x = letter.group(1)
                if n != actual.get(x, 0):
                    problems.append(f"line {i + 1}: band table says {x} {n}, the band holds "
                                    f"{actual.get(x, 0)}")
                b = re.search(r"\+\s*(\d+)\s*built", last)
                if x == "A" and b and int(b.group(1)) != built_in_a:
                    problems.append(f"line {i + 1}: band table says A '+ {b.group(1)} built', "
                                    f"Band A keeps {built_in_a} built rows")
            elif "Candidates" in " ".join(row[:2]):
                if n != candidates:
                    problems.append(f"line {i + 1}: band table says {n} candidates, the bands "
                                    f"hold {candidates}")
            elif "open gap" in first.lower():
                if n != gap:
                    problems.append(f"line {i + 1}: band table says open gap {n}, it holds {gap}")
            elif "discarded" in first.lower():
                if n != discards:
                    problems.append(f"line {i + 1}: band table says {n} discarded, the table "
                                    f"holds {discards}")
    if not seen:
        problems.append("the Candidates section has no '| Band | ... | Cities |' table")
    return problems


def summary(lines, built, countries, actual, candidates, gap, discards):
    """The '> | **Built** | ...' box at the top."""
    problems = []
    box = [(i, l) for i, l in enumerate(lines) if l.startswith("> |")]
    rows = {}
    for i, l in box:
        m = re.match(r"^> \|\s*\*\*([^*]+)\*\*\s*\|(.*)$", l)
        if m:
            rows[m.group(1).strip().lower()] = (i, m.group(2))
    if not rows:
        return ["no summary box ('> | **Built** | ...') found"]

    def first_bold_int(text):
        m = re.search(r"\*\*(\d+)\*\*", text)
        return int(m.group(1)) if m else None

    for label, want in (("built", built), ("candidates", candidates),
                        ("open screening gap", gap), ("discarded", discards)):
        if label not in rows:
            problems.append(f"the summary box has no '{label}' row")
            continue
        i, text = rows[label]
        got = first_bold_int(text)
        if got != want:
            problems.append(f"line {i + 1}: summary says {label} {got}, the file holds {want}")
    if "built" in rows:
        i, text = rows["built"]
        m = re.search(r"across\s+(\d+)\s+countries", text)
        if m and int(m.group(1)) != countries:
            problems.append(f"line {i + 1}: summary says built across {m.group(1)} countries, "
                            f"the Built table spans {countries}")
    if "candidates" in rows:
        i, text = rows["candidates"]
        head = text.split("*(")[0]
        for x, n in re.findall(r"(?<!\w)([A-Z]) (\d+)(?![\d,])", head):
            if int(n) != actual.get(x, 0):
                problems.append(f"line {i + 1}: summary says {x} {n}, Band {x} holds "
                                f"{actual.get(x, 0)}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", type=Path, default=LIST)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    tram = args.file.parent / TRAM_NAME
    report, problems = check(args.file.read_text(encoding="utf-8"),
                             tram.read_text(encoding="utf-8") if tram.exists() else None)
    tiers = report.pop("_tiers", {})

    if args.verbose:
        for label, names in report.items():
            print(f"{label} ({len(names)}): {', '.join(sorted(names.values()))}")
        print()
    if problems:
        for p in problems:
            print(f"  PROBLEM  {p}")
        print(f"\n{len(problems)} problem(s) in {args.file.name}. Fix the COUNT to match the "
              "rows, or the rows to match the decision - never the reverse of what was "
              "decided. A city in two lists is a move half made.")
        return 1
    bands = {k: len(v) for k, v in report.items() if k.startswith("Band ") and "built" not in k}
    on_tram_list = (" (tram list: " + ", ".join(f"{k} {v}" for k, v in sorted(tiers.items()))
                    + ")") if tiers else ""
    print(f"OK - {len(report.get('Built', {}))} built, "
          + ", ".join(f"{k} {v}" for k, v in sorted(bands.items()))
          + f"{on_tram_list}, {len(report.get('the discards', {}))} discarded; every stated "
          "count agrees and no city is in two lists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
