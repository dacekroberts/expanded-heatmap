# Neutral code comments: a portable handoff

**For a session in a different project.** This is the comment style the owner
chose for link-station-commercial on 2026-09-30, the process that rolled it
across about 1,000 lines of comments in one sitting without changing a line
of code, and the two scripts that made it safe. Nothing here names a file in
your repo. Examples are labelled **[example]** and come from the Seattle
project: read them as evidence of the shape, not as instructions about your
code.

Read the whole file before editing anything. Section 5 (the process) matters
as much as section 2 (the rules).

---

## 1. The decision

The owner looked at four kinds of comment the codebase had grown, saw each
rewritten three ways (first person, neutral, and a hybrid of first-person
docstrings with neutral inline comments), and chose **neutral**. Two further
decisions:

- **Audience: both** a hiring manager skimming the repo and whoever changes
  the code next. Clear to an outsider, with enough *why* to change things
  safely.
- **Verification history: one line at most.** Keep the result and any
  re-check warning; the story of how it was found goes in the decisions log.

And one hard rule added on top: **no em dashes in any comment.** Visible text
on the site is exempt.

Before rolling this out in your project, show the owner a pilot (section 5).
Their answer for one project isn't automatically their answer for another.

---

## 2. The rules

1. **No "I", "we", "you", "the user", "the ask".** Short statements of what
   and why.
2. **Keep every number that protects a value**: pixel sizes, thresholds,
   counts a value was tuned against. Keep every "re-measure / re-check if X
   changes" warning. Keep every pointer to the decisions log or another
   file where the reasoning lives. Keep anything that stops a deliberate
   value being "cleaned up".
3. **Cut the narration**: "binary-searched in the live DOM", "confirmed by
   screenshot", "caught by the user", "Session 6", "tried X first",
   "several readers found". Keep at most one line of result.
4. **Cut stale tutorial text** written to a student during the build ("give
   this one hour", "note it in the methodology", "worth reaching for if your
   match rate comes back poor"). Keep any real how-it-works explanation it
   carried.
5. **No new claims.** If unsure whether a statement is still true, keep its
   substance. Rewording is not the moment to invent or delete facts.
6. **Docstrings open with a plain summary line**: imperative for functions
   ("Build...", "Return...", "Set..."). Keep Input:/Output:/Run: headers in
   module docstrings.
7. **Section dividers stay dividers** (`# --- 2. Ridership ---...`).
8. **Don't pad.** Short comments that are already neutral stay nearly as
   they are. The goal is shorter, not uniform.
9. **No em dashes (U+2014)** in `#` comments, docstrings, or CSS `/* */`,
   JS `//` and HTML `<!-- -->` comments inside string literals. Use a colon,
   semicolon, comma, parentheses, or a plain spaced hyphen " - ". Never an
   en dash or `--` as a workaround.
10. **Spelling follows the project.** [example: the site had been switched to
    American English; the rollout caught a stray "standardise" and
    "neighbourhood".]

**Exempt:** visible text (labels, captions, page prose, printed messages,
`sys.exit` text), and verbatim quotes of legal terms, which keep their "you".
[example: a comment quoting a data provider's licence flow-down clause word
for word.]

---

## 3. The four kinds you'll probably find, with rewrites

**[example] Terse reference: barely changes.**
```python
# Before
# Ring boundaries in miles. Ring i spans RING_EDGES_MILES[i] to [i+1].
# The 0.3 mile mark is the walkshed of interest; 0.3-0.6 is the comparison
# band that gives the gradient something to decline against.
# After
# Ring boundaries in miles; ring i runs from RING_EDGES_MILES[i] to [i+1].
# 0 to 0.3 mi is the walkshed; 0.3 to 0.6 mi is the comparison band the
# gradient declines against.
```

**[example] Tutor to student: the budget advice goes, the explanation stays.**
```python
# Before (module docstring, abridged)
"""...GTFS spreads what you need across four tables. Link stations are not
labeled as such anywhere - you find them by walking the relationships: ...
BUDGET NOTE: give this one hour. If routes.txt does not look the way you
expect, ... stop and hand-build the CSV instead..."""
# After
"""...GTFS doesn't label Link stations. They're found by joining four tables:

    routes.txt          the 1 Line's route_id
      -> trips.txt      the trips on that route
      -> stop_times.txt the stops those trips serve
      -> stops.txt      each stop's name and coordinates
..."""
```

**[example] Verification diary: shrinks the most, keeps the numbers.**
```python
# Before (10 lines)
# Streamlit's default expanded sidebar is 300px. The ask was 2/3 of that
# (200px), but the longest nav label - "Methodology & Limitations" - needs
# enough width to stop clipping under text-overflow:ellipsis. Re-measured
# after switching the base font to Inter (set_base_font() below), which
# renders that label wider than Streamlit's original default font did:
# binary-searched to the exact pixel in the live DOM, 235px clips, 236px
# doesn't. 240px is the narrowest round number with a small safety margin
# above that threshold, so it survives minor font-rendering differences
# across browsers rather than sitting exactly on the edge. Re-measure
# again if the base font ever changes.
SIDEBAR_WIDTH_PX = 240
# After (3 lines)
# Streamlit's default is 300px. 240px is the narrowest width where the
# longest nav label ("Methodology & Limitations") doesn't clip in Inter;
# it clips at 235px. Re-measure if the base font changes.
SIDEBAR_WIDTH_PX = 240
```

**[example] Design rationale: the why stays, the hedging goes.**
```python
# Before
# Two heat layers, same tuning, different universe. Within-rings is the
# default (matches what the rest of the project actually analyzes - see
# docs/DECISIONS.md); all-Seattle is an explicit opt-in for citywide context,
# off by default so the map opens on the same scope as the Findings
# page rather than the broader, less-meaningful citywide picture.
# After
# Two heat layers, same settings. Within-rings is on by default to match
# the Findings page's scope; all-Seattle is an opt-in for citywide
# context. See docs/DECISIONS.md.
```

**[example] A CSS comment inside a Python string counts too.**
```css
/* Before */
/* Streamlit's own UI glyphs (sidebar collapse/expand arrow, etc.) are
rendered as ligatures in the Material Symbols icon font, not images - the
wildcard above was breaking these, showing the raw ligature name
("keyboard_double_arrow_left") as literal text instead of the arrow icon.
Confirmed via the element's own pre-existing rule. */
/* After */
/* Streamlit's UI icons (the sidebar arrow, etc.) are ligatures in the
Material Symbols font. Without this reset the wildcard shows their raw
names ("keyboard_double_arrow_left") instead of icons. */
```

---

## 4. Measure first

Before proposing anything, count. [example: 712 `#` comments, 40 module and
function docstrings, 40 CSS/JS comments inside strings across 15 files;
more than a third of the comment lines in two files; 1 comment line in
first person; about 28 recounting verification; 3 em dashes in comments.]
The counts tell you where the work is and which file to pilot.

---

## 5. The process that worked

1. **Inventory and classify.** Pull a real example of each kind (section 3).
2. **Show the owner one comment rewritten each way**, then all four kinds
   in the style they pick. Let them choose voice, audience, and where the
   history goes. Ask how to roll out; recommend a pilot.
3. **Pilot one mid-sized file** with all four kinds in it. Verify it's
   comments-only (step 7), render-test anything that renders, and show the
   owner what was removed, not just what was kept: "I dropped the list of
   companies that use this font; object to any of it." Commit the pilot on
   approval.
4. **Write the rule down** in the project's instruction file (section 8)
   so the next session follows it without this handoff.
5. **Add the em-dash check** (section 7) and watch it fail before trusting
   it: plant an em dash in a docstring and in a CSS comment inside a
   string, on copies in a temp dir, and confirm it catches both and
   ignores visible labels.
6. **Roll out in parallel, split by file.** [example: four agents: the
   largest pipeline file alone, the largest page alone, config plus the
   small pages, the remaining pipeline steps plus scripts.] Disjoint file
   sets mean no edit conflicts in one working tree. Each agent gets the
   spec in section 6 and must verify before reporting. Agents don't
   commit; you do.
7. **Verify every file is comments-only** with `verify_comments_only.py`
   (section 7). It compares HEAD with the working copy after stripping
   docstrings, `#` comments and embedded CSS/JS/HTML comments: any code or
   visible-text change shows as CHANGED.
8. **Regenerate committed artifacts that embed comments.** [example: the
   map builder's JS and CSS comments ship inside a committed HTML output,
   so the map was regenerated and diffed; it differed only in comments.]
   If your project commits generated files, check whether comments ride
   along into them.
9. **Sweep yourself; don't trust the reports.** Grep comments and
   docstrings for first person, "Session N", British/American spelling
   mismatches, and em dashes. Spot-check the agents' judgment calls by
   reading the text.
10. **Commit by path**, never `git add -A`, and log the change in the
    decisions log.

**What the rollout caught besides voice** [example]: a comment claiming 23
map layers where there were 21 (the count was deleted rather than
corrected, since any count of an open set rots again); a comment calling a
table "alphabetical" where the code ordered it north to south; two
docstrings still describing placeholders that had been filled weeks
before. Rewriting comments is a cheap audit of them. Budget for it.

**Pitfalls** [example]:
- A comment *quoting* a visible label that contains an em dash. Paraphrase
  the quote ("the full NAICS label"); don't change the label.
- Agents occasionally add a sentence (a new re-measure warning, a missing
  output in a docstring's Output list). Usually correct, but review each
  addition; rule 5 says no new claims.
- A negative-test mutation that matched the wrong occurrence. Make the
  harness assert its mutation hit the intended target.

---

## 6. Agent spec template

Give each rollout agent the rules in section 2, the before/after pairs in
section 3 (or better, point it at your approved pilot file), and these
specifics:

- **Its files, and only those.** Don't commit, don't touch other files,
  don't run anything that rewrites committed outputs.
- **What must not change**: any code, any CSS rule or JS statement, any
  visible string (page prose, labels, captions, tooltips, printed
  messages). Name the project's deliberate values whose comments must
  keep their numbers [example: "the 1000px map width (a renderer init-race
  workaround), the 925px iframe height, Graph 4's 12px left padding"].
- **Project invariants whose comments stay in full** [example: "never
  buffer in EPSG:4326", "rings are annuli", "station name is the join
  key"].
- **Must pass before reporting**: `verify_comments_only.py` on its files
  (IDENTICAL), the em-dash check (no hits in its files), any project
  number or render checks.
- **Report**: lines before/after per file, comments rewritten, anything
  kept long on purpose or unsure about (file:line), three before/after
  pairs.

---

## 7. Scripts

Both are standard library only. They find files with `git ls-files`, so
they work in any git repo and skip virtualenvs. Adjust `INCLUDE` /
`EXCLUDE` to taste.

### `check_no_em_dashes.py`

```python
"""No em dashes in comments: # comments, docstrings, and CSS/JS/HTML
comments inside string literals. Visible text is out of scope.

Run:  python scripts/check_no_em_dashes.py [--root PATH]

When it fails, reword with a colon, semicolon, comma, parentheses or a plain
hyphen. Don't swap in an en dash or a double hyphen.
"""
import ast
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

EM_DASH = "—"
EXCLUDE = ()  # path prefixes to skip, e.g. ("vendor/",)
# The // pattern skips "://" so a URL isn't read as a JS comment.
EMBEDDED = re.compile(r"/\*.*?\*/|<!--.*?-->|(?<![:\w])//[^\n]*", re.S)


def project_files(root):
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=root,
                         capture_output=True, text=True).stdout.split()
    return [root / p for p in out if not p.startswith(EXCLUDE)]


def docstring_nodes(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                yield b[0].value


def scan(path):
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    hits, counts = [], {"comment": 0, "docstring": 0, "embedded": 0}
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            counts["comment"] += 1
            if EM_DASH in tok.string:
                hits.append((tok.start[0], "comment", tok.string.strip()))
    docstrings = set()
    for node in docstring_nodes(tree):
        docstrings.add(id(node))
        counts["docstring"] += 1
        for i, line in enumerate(node.value.splitlines()):
            if EM_DASH in line:
                hits.append((node.lineno + i, "docstring", line.strip()))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and id(node) not in docstrings:
            for m in EMBEDDED.finditer(node.value):
                counts["embedded"] += 1
                if EM_DASH in m.group(0):
                    line = node.lineno + node.value[:m.start()].count("\n")
                    hits.append((line, "embedded comment", " ".join(m.group(0).split())[:100]))
    return hits, counts


def main():
    root = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv \
        else Path(__file__).resolve().parent.parent
    sys.stdout.reconfigure(encoding="utf-8")
    files = project_files(root)
    if not files:
        sys.exit(f"FAIL: found no tracked .py files under {root}.")
    total, failures = {"comment": 0, "docstring": 0, "embedded": 0}, []
    for path in files:
        hits, counts = scan(path)
        for k in total:
            total[k] += counts[k]
        failures += [(path.relative_to(root), *h) for h in hits]
    print(f"Scanned {len(files)} files: {total['comment']} # comments, "
          f"{total['docstring']} docstrings, {total['embedded']} comments inside strings.")
    if not total["comment"]:
        sys.exit("FAIL: found no comments at all - the scan is broken.")
    if failures:
        print(f"\nFAIL: {len(failures)} em dash(es) in comments.\n")
        for rel, line, kind, text in sorted(failures):
            print(f"   {rel}:{line} ({kind}): {text}")
        sys.exit(1)
    print("OK: no em dashes in any comment or docstring.")


if __name__ == "__main__":
    main()
```

### `verify_comments_only.py`

Keep this one outside the repo (a scratch tool for the rollout, not a
project check).

```python
"""Verify that edits since HEAD touched only comments and docstrings.

Usage (from the project root):  python verify_comments_only.py FILE [FILE ...]

Compares HEAD's version with the working copy after removing docstrings,
# comments (the AST drops them), and CSS/JS/HTML comments inside strings,
and collapsing whitespace inside strings. Exits 1 if any file changed
beyond comments.
"""
import ast
import re
import subprocess
import sys

EMBEDDED = re.compile(r"/\*.*?\*/|<!--.*?-->|(?<![:\w])//[^\n]*", re.S)


def canon(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            node.value = " ".join(EMBEDDED.sub("", node.value).split())
    return ast.dump(tree)


bad = 0
for path in sys.argv[1:]:
    old = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True).stdout.decode("utf-8")
    new = open(path, encoding="utf-8").read()
    same = canon(old) == canon(new)
    print(f"{'IDENTICAL' if same else 'CHANGED  '}  {path}  "
          f"({len(old.splitlines())} -> {len(new.splitlines())} lines)")
    bad += not same
sys.exit(1 if bad else 0)
```

Its known blind spot: whitespace-only changes inside visible strings pass.
That's acceptable for a comment rollout; anything stricter flags every
rewrapped CSS comment.

---

## 8. Instruction-file snippet

Adapt and add to the project's CLAUDE.md (or equivalent) once the owner
approves the pilot:

```markdown
## Code comments

Neutral voice: no "I", "we" or "you"; short statements of what and why,
readable by an outsider but useful to whoever changes the code next. Keep
every measured value and its "re-measure if X changes" warning. How
something was found or verified gets one line at most; the full story
belongs in the decisions log. `<pilot file>` is the reference example.

**No em dashes in any comment or docstring**, including CSS/JS comments
inside strings. Hard rule, enforced by `python scripts/check_no_em_dashes.py`.
Visible text is exempt.
```

---

## 9. What not to touch

- Visible text, including interpretive prose the owner wrote. A comment
  rollout that changes a caption has gone wrong.
- Dated log entries, even ones written in the old voice.
- Verbatim legal quotes.
- Any comment you can't verify. Keep its substance and flag it; don't
  guess.
