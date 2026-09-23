"""Report prose that has stopped being true. The heuristic half of the sweep.

    python scripts/check_stale_claims.py [--verbose] [--only A|B|C|D|E]

**THIS REPORTS AND ALWAYS EXITS 0.** `check_provenance.py` decides things - a
row is present or it is not - and fails. Everything here is a guess about
English, and a noisy gate gets ignored, which is worse than no gate. Read the
report; it is for a human mid-sweep, not for CI.

WHY THESE CATEGORIES
--------------------
(This heading said "WHY THESE THREE" over four categories until 2026-09-23 -
a hand-kept count, in the checker for hand-kept counts.)

On 2026-09-22 a cleanup sweep found classes of stale prose that no existing
check could see, in a project whose every check was about data:

  A. **Future tense about a present that arrived.** Three files said Canada was
     unbuilt while six municipalities were built; a fourth said it of D.C. Each
     read perfectly - it was describing a world that no longer existed.
  B. **Hand-kept counts.** Four were wrong in one file, and one contradicted
     itself two clauses later ("thirteen sources", then "six of the twelve").
  C. **Headings whose contents moved on.** `## Transit feeds (GTFS)` held three
     rail sources that were not GTFS.
  D. **Config constants no script reads.** The comment above a dead constant is
     usually describing a plan that did not happen.
     `pipeline/san_diego/config.py` says a per-point lookup was "REPLACED" by a
     bulk download; it was not - bulk was attempt 2 of 3 and was abandoned at
     ~26 s per page, and `PARCEL_QUERY_BBOX` and `PARCEL_PAGE_SIZE` survive,
     read by nothing. The constant is harmless; **the comment is the defect**,
     because the next reader trusts it over the call.
  E. **Universal claims on the published surface** - "the only city", "no
     other city", "every other city", "every city here". Added 2026-09-23
     after one day corrected over twenty, each written when fewer cities
     existed: "no other city here needed more than one source" (Boston needed
     three, Milan six), Edmonton as "the only register" with no name but the
     business's while Madrid's entry called its identical position "stronger
     than any other city here". **At least three were false the day they were
     written** - so this is not only rot; authors generalise from the cities
     they happen to be thinking of. Run it when a city lands: every hit is a
     bet on the next city, and the fix for a lost one is a comparison with a
     CATEGORY ("than a licence register can"), never another "only". Proved
     against history: run on the two commits before that day's fixes it finds
     all 19 phrases it was pointed at, and on the commit after, none.

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

# Build briefs are the same shape: each is Step 0's answers AS OF a date, and
# `CLAUDE.md` says outright that a brief "caches Step 0's mistakes as
# confidently as its findings". Calgary's says it is "the biggest map of the
# four remaining", which was true during the Canada build and is a snapshot,
# not drift. Their claims are re-verified by `scripts/brief_check.py` against
# live sources, which is the right instrument - this one cannot tell a stale
# brief from an accurate record of a past probe.
# docs/notifications holds letters this project owes a publisher. "NOT YET
# SENT" is their CORRECT state, not a stale claim - the whole point of the
# file is to track an act that has not happened. Excluded for the same reason
# as build_briefs: a document whose subject is pendency cannot be audited for
# writing about pendency.
EXCLUDE_DIRS = ("docs/build_briefs", "docs/notifications")

# Two more, each for a reason already established above rather than a new one.
#
# `city_master_list.md` is the file `CLAUDE.md` says to READ COUNTS OFF, so its
# numbers are maintained by design and flagging all eight of them forever would
# train people to skip this report. They are not unchecked: they moved to
# `check_provenance.py` check E, which compares them to `app/cities.py` and
# FAILS - a count in a file whose job is to carry counts gets checked, a count
# anywhere else gets deleted.
#
# `global_country_shortlist.md` and `canada_step0_endpoints.md` are the two
# evidence trails - `CLAUDE.md` calls the first "every probe logged", and the
# second was relabelled an evidence trail on 2026-09-22. Their counts are dated
# probe findings, the same case as the retrospectives.
EXCLUDE_NAMES |= {
    "city_master_list.md",
    "global_country_shortlist.md",
    "canada_step0_endpoints.md",
}

# The sweep skill teaches these defects by quoting real instances, so it reports
# as stale prose about Canada and D.C. It is documentation OF the markers.
EXCLUDE_PATHS = {".claude/skills/consistency-sweep/SKILL.md"}

SCAN_GLOBS = ("docs/**/*.md", ".claude/skills/**/*.md", "CLAUDE.md", "*.md")

# A. Phrases describing a future, in a project where the future keeps arriving.
# How close a built city's name must sit to a future-tense marker before the
# two are treated as one claim. Wide enough for a sentence, far narrower than
# a table row.
NEAR_CHARS = 120

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
            rel = p.relative_to(ROOT).as_posix()
            if any(rel.startswith(d + "/") for d in EXCLUDE_DIRS):
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
                # PROXIMITY, NOT THE WHOLE LINE. A markdown table row
                # runs past 600 characters, so "Screened 2026-09-21, not yet
                # a full Step 0" - accurate prose about an UNBUILT city -
                # matched "Boston" mentioned 400 characters further along the
                # same row and was reported as a stale claim. Same defect
                # shape as check_provenance's `item N` citation namespaces:
                # the marker and the name were never related, only adjacent
                # in a file. Measured 2026-09-23: this took category A from
                # three findings, all of them noise, to one that is real.
                near = low[max(0, i - NEAR_CHARS):i + len(marker) + NEAR_CHARS]
                named = [v for v in vocab if v.lower() in near]
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


def country_without_a_city(rel):
    """Is this a country profile no city imports YET?

    `add-country` exists so the national facts are profiled ONCE, before
    the first city in that country is built - so a profile whose
    constants nothing reads is that workflow working, not a defect.
    Reporting them as dead would mean this check fires forty-odd false
    positives every time someone follows the documented process, and a
    report people learn to skip is worse than no report.

    The distinction is exact and cheap: does any city config import this
    profile? Mexico's does, from two cities, so its three unread
    constants ARE findings. France's does not, from none, so its
    forty-six are deferred until Paris lands - at which point they become
    findings automatically, with no edit here.
    """
    if not rel.startswith("pipeline/countries/"):
        return False
    stem = rel.rsplit("/", 1)[1][:-3]
    for cfg in ROOT.glob("pipeline/*/config.py"):
        if f"countries.{stem}" in cfg.read_text(encoding="utf-8"):
            return False
    return True


def check_d():
    """Module-level config constants that nothing outside their own file reads.

    KNOWN FALSE NEGATIVE: attribution is by NAME, not by module. A constant
    that is dead in one city's config is not reported when another city
    defines and consumes one of the same name - Barcelona's
    OSM_STATION_RAILWAY is unread there while Guadalajara's is live, so only
    its sibling OSM_STATION_KIND surfaced on 2026-09-23. Following that one
    constant found the real defect anyway, but the blind spot is real and
    shared config vocabularies are exactly where it bites. Fixing it means
    resolving each read back to the module it imports from.

    Deterministic enough to trust - these configs are imported by name - but it
    REPORTS rather than fails, because a dead constant is a signal to go and
    read the comment above it, not a defect in itself.
    """
    import ast as _ast
    import io as _io
    import tokenize as _tok

    def code_only(src):
        """Strip comments and strings, so a MENTION is not counted as a READ.

        This is not a refinement, it is the difference between the check
        working and not. The first version counted raw text, and the very
        constants it was written to find - San Diego's PARCEL_QUERY_BBOX and
        PARCEL_PAGE_SIZE - came back clean, because THIS FILE's own docstring
        names them as the worked example. The checker's documentation of the
        bug masked the bug.
        """
        try:
            out = []
            for tk in _tok.generate_tokens(_io.StringIO(src).readline):
                if tk.type in (_tok.COMMENT, _tok.STRING):
                    continue
                out.append(tk.string)
            return " ".join(out)
        except (_tok.TokenError, IndentationError, SyntaxError):
            return src

    hits = []
    configs = sorted(ROOT.glob("pipeline/*/config.py")) + \
        sorted(ROOT.glob("pipeline/countries/*.py"))
    # Everything that could read a config constant.
    readers = []
    for g in ("pipeline/**/*.py", "scripts/*.py", "app/**/*.py"):
        readers += [q for q in ROOT.glob(g) if q.is_file()]
    corpus = {q: code_only(q.read_text(encoding="utf-8", errors="replace"))
              for q in readers}

    for cfg in configs:
        try:
            src = cfg.read_text(encoding="utf-8")
            tree = _ast.parse(src)
        except (OSError, SyntaxError):
            continue
        names = []
        for node in tree.body:
            if isinstance(node, _ast.Assign):
                for tgt in node.targets:
                    nm = getattr(tgt, "id", None)
                    if nm and nm.isupper() and not nm.startswith("_"):
                        names.append((nm, node.lineno))
        for nm, lineno in names:
            pat = re.compile(r"\b" + re.escape(nm) + r"\b")
            # references anywhere else, including later in its own file
            external = 0
            for q, text in corpus.items():
                if q == cfg:
                    # Its own file, comments already stripped: the assignment
                    # itself is one occurrence, so anything beyond that is a
                    # real internal use (building another constant from it).
                    external += max(0, len(pat.findall(text)) - 1)
                else:
                    external += len(pat.findall(text))
            if external == 0:
                hits.append((cfg.relative_to(ROOT).as_posix(), lineno, nm))
    return hits


# --- E. Universal claims on the published surface ---------------------------

# Only what a READER sees: page prose, and the two documents the app renders
# (91_What_Is_Excluded.py and 90_About_the_Data.py). A universal in a research
# brief is shorthand between sessions; on a page it is a claim to the public.
PUBLISHED_PAGES = ("app/Overview.py", "app/pages/*.py")
PUBLISHED_DOCS = ("docs/excluded_categories.md", "docs/data_sources.md")

# COMPARISONS ONLY. Every one of the eleven false claims found on 2026-09-23
# compared a city with the rest - "the only", "no other", "every other", "any
# other", "elsewhere on this site". None was a bare "every city" or "every
# map": those describe what the pipeline does to all maps ("dropped from every
# map"), are usually enforced in code, and were 30 of the 44 hits the first
# version of this category printed. A list that long gets skimmed, then
# ignored, which is the cry-wolf failure the module docstring warns about.
#
# Words are joined by \s+ so a claim split over two source lines still
# matches - the probe that preceded this was a line grep, and those are
# exactly the claims it would have missed.
_S = r"\s+"
UNIVERSAL_RE = re.compile(
    r"\b(?:"
    r"the" + _S + r"only" + _S +
    r"(?:city|cities|map|maps|register|registry|source|one)"
    r"|only" + _S + r"city"
    r"|(?:every|any)" + _S + r"other" + _S + r"(?:city|cities|map|maps)"
    # A bare "every city" is usually pipeline behaviour; "every city HERE" or
    # "ON THIS SITE" is a claim about the set of built cities, and it is the
    # shape of the two instances found earlier that day - "trams are excluded
    # in every city here that has them", "Every map here covers one rail
    # network". Both were falsified by the next city to land.
    r"|every" + _S + r"(?:city|map)" + _S +
    r"(?:here|on" + _S + r"this" + _S + r"site)"
    r"|no" + _S + r"other" + _S + r"(?:city|map|register|registry)"
    r"|all" + _S + r"(?:the" + _S + r")?other" + _S + r"cities"
    r"|(?:anywhere|elsewhere)" + _S + r"on" + _S + r"this" + _S + r"site"
    r"|unlike" + _S + r"(?:every|any)" + _S + r"other"
    r"|none" + _S + r"of" + _S + r"the" + _S + r"other"
    r")\b", re.I)

# The site's navigation button, not a claim.
UI_LABELS = {"All cities"}


def _published_texts():
    """(path, first_line, text) for every piece of reader-facing prose.

    From a page: every string literal EXCEPT docstrings, because a docstring is
    addressed to the next editor, and "the decided pattern for every city's
    detail page" sits in all of them. Comments never reach the AST at all.
    From a document: each paragraph, fenced code stripped.
    """
    for pattern in PUBLISHED_PAGES:
        for p in sorted(ROOT.glob(pattern)):
            tree = ast.parse(p.read_text(encoding="utf-8"))
            docstrings = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.FunctionDef,
                                     ast.AsyncFunctionDef, ast.ClassDef)):
                    body = node.body
                    if (body and isinstance(body[0], ast.Expr)
                            and isinstance(body[0].value, ast.Constant)
                            and isinstance(body[0].value.value, str)):
                        docstrings.add(id(body[0].value))
            for node in ast.walk(tree):
                if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                        and id(node) not in docstrings):
                    yield p, node.lineno, node.value
    for rel in PUBLISHED_DOCS:
        p = ROOT / rel
        if not p.exists():
            continue
        text = re.sub(r"(?ms)^```.*?^```", lambda m: "\n" * m.group(0).count("\n"),
                      p.read_text(encoding="utf-8"))
        line = 1
        for para in re.split(r"(\n\s*\n)", text):
            if para.strip():
                yield p, line, para
            line += para.count("\n")


def check_e():
    hits, seen = [], set()
    for p, first_line, text in _published_texts():
        flat = " ".join(text.split())
        spans = quoted_spans(flat)
        for m in UNIVERSAL_RE.finditer(text):
            phrase = " ".join(m.group(0).split())
            if phrase in UI_LABELS:
                continue
            # Locate the same match in the flattened text, for the sentence.
            # max(0, ...): a NEGATIVE start makes str.find count from the END.
            approx = len(" ".join(text[:m.start()].split()))
            pos = flat.find(phrase, max(0, approx - 2))
            if pos < 0 or in_quotes(pos, spans):
                continue
            prev = flat.rfind(". ", 0, pos)          # -1 when none: start at 0
            start = 0 if prev < 0 else prev + 2
            end = flat.find(". ", pos)
            end = len(flat) if end < 0 else end + 1
            # CENTRED ON THE MATCH, not cut from the sentence's start: a
            # markdown table row is one "sentence" hundreds of characters
            # long, and the first version printed its opening while the
            # flagged phrase sat past the truncation - a hit that did not
            # show what it was flagging.
            a, b = max(start, pos - 90), min(end, pos + len(phrase) + 110)
            excerpt = ("..." if a > start else "") + flat[a:b].strip(" *") + \
                ("..." if b < end else "")
            n = first_line + text[:m.start()].count("\n")
            key = (p, n, phrase.lower())
            if key in seen:
                continue
            seen.add(key)
            hits.append((p, n, phrase, excerpt))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true",
                    help="A: report markers even when no built place is named")
    ap.add_argument("--only", choices=["A", "B", "C", "D", "E"])
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

    if args.only in (None, "D"):
        hits = check_d()
        live = [h for h in hits if not country_without_a_city(h[0])]
        deferred = [h for h in hits if country_without_a_city(h[0])]

        print(f"D. CONFIG CONSTANTS no script reads - {len(live)}")
        print("   Each one is a prompt to READ THE COMMENT ABOVE IT. A dead "
              "constant is harmless;\n   a comment describing a plan that did "
              "not happen is what misleads the next reader.")
        for rel, lineno, nm in live:
            print(f"   {rel}:{lineno}  {nm}")
        if not live:
            print("   none")

        if deferred:
            by_file = {}
            for rel, _, _ in deferred:
                by_file[rel] = by_file.get(rel, 0) + 1
            print(f"\n   Deferred - {len(deferred)} constant(s) in a country "
                  f"profile no city imports yet.")
            print("   That is add-country working as intended: the national "
                  "facts are profiled once,\n   BEFORE the first city. They "
                  "become findings on their own the day a city\n   in that "
                  "country lands, with no edit to this script.")
            for rel, n in sorted(by_file.items()):
                print(f"      {rel}  ({n})")
        print()

    if args.only in (None, "E"):
        hits = check_e()
        print(f"E. UNIVERSAL CLAIMS on the published surface - {len(hits)} to "
              f"re-read when a city lands")
        print("   Each is a bet on the next city. A true one stays. A false one "
              "becomes a comparison\n   with a CATEGORY (\"than a licence "
              "register can\"), never another \"every other city\".")
        for p, n, phrase, excerpt in hits:
            print(f"   {p.relative_to(ROOT).as_posix()}:{n}  [{phrase}]")
            print(f"      {excerpt}")
        if not hits:
            print("   none")
        print()

    print("Reported, not failed - every rule here is a guess about English. "
          "Exit 0 by design.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
