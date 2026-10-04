"""Find note-like prose a reader can see: REPORTS only, never fails.

    python scripts/check_internal_prose.py [--surface NAME] [--kind KIND] [--counts]

WHY. The live audit of 2026-10-03 found About the Data's United States view
showing "Boston - Step 0 findings, 2026-09-21" and "The owner's API-account
practice, and what it interacts with": research notes that never got an
<!-- internal --> marker. check_internal_markers.py checks that markers are
well formed; nothing looked at what stays visible WITHOUT one.

WHAT IT READS is what the app renders, through the app's own filter:
docs/data_sources.md, docs/excluded_categories.md and every
docs/data_sources/*.md after country_sections.public() (internal spans gone),
plus every string literal in app/pages/*.py that holds prose (st.markdown,
st.caption and the like; comments are not strings, so they are not read).

WHAT IT FLAGS, each hit with its kind, the section it sits under and the
line: process words (Step 0, brief, session, worktree, review time, probe),
references to the owner, to DECISIONS or PLAN, repository paths, dated
research ("read 2026-09-22", "verified ..."), status words in capitals
(DECIDED, BUILT, HELD), status emoji, and first person. Some hits belong on
the page - a licence read on a date is provenance a reader is owed - which is
why this reports and a person decides. A verdict that a hit belongs is
recorded in KEEP below, so the next run shows only what is undecided.
"""
import argparse
import ast
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from country_sections import public  # noqa: E402

KINDS = [
    ("process", re.compile(r"\b(Step 0|build brief|the brief|briefs?\b(?= (?:said|says|claimed|records))|"
                           r"this session|a session|sessions?\b(?= (?:found|measured|read))|worktree|"
                           r"review time|review lane|probed?|probing|re-probe|drafts? file|"
                           r"TODO|FIXME|to rediscover|not rediscovering)\b", re.I)),
    ("owner", re.compile(r"\b(?:the )?owner(?:'s)?\b(?! of)|\(owner\b", re.I)),
    ("log-ref", re.compile(r"\b(DECISIONS(?:\.md)?|PLAN(?:\.md)?|CLAUDE\.md|decisions log)\b")),
    ("repo-path", re.compile(r"(?<![\w/.])(?:pipeline|scripts|docs|outputs|app|data)/[\w./<>-]+|"
                             r"\b[\w-]+\.(?:py|md)\b")),
    ("dated-research", re.compile(r"\b(?:read|verified|checked|measured|probed|found|"
                                  r"confirmed|screened|corrected|stated|recorded) "
                                  r"(?:on )?20\d\d-\d\d-\d\d", re.I)),
    ("status-caps", re.compile(r"\b(DECIDED|BUILT|HELD|RESOLVED|UNRESOLVED|OPEN DECISION|"
                               r"NOT YET|LANDED|PENDING)\b")),
    ("status-emoji", re.compile(r"[✅❌⚠\U0001F534\U0001F7E2\U0001F7E1]")),
    ("first-person", re.compile(r"\b(?:I|I'm|I've|we|We|we're|our|Our)\b")),
]

# Hits judged to belong on the page: (surface, kind, a substring of the line).
# Each entry is a decision; add one only with the reason beside it.
KEEP = []


def doc_surfaces():
    """Each rendered doc as its page assembles it (About_the_Data.py and
    What_Is_Excluded.py): the shared sections less the ones a page skips, and
    every country's own sections."""
    from country_sections import COUNTRY_ORDER, country_text, parts_of, shared_text
    sources = ROOT / "docs" / "data_sources.md"
    parts = parts_of(sources)
    text = shared_text(parts, skip_titles=("How to keep this current",))
    text += "\n" + "\n".join(country_text(parts, c) for c in COUNTRY_ORDER)
    yield "docs/data_sources.md", public(text)
    excluded = ROOT / "docs" / "excluded_categories.md"
    yield "docs/excluded_categories.md", public(excluded.read_text(encoding="utf-8"))
    for p in sorted((ROOT / "docs" / "data_sources").glob("*.md")):
        yield p.relative_to(ROOT).as_posix(), public(p.read_text(encoding="utf-8"))


# Streamlit calls whose string arguments a reader sees. Docstrings and
# comments are never read; "No map yet" is the developer's fallback for a
# missing map, shown only on a broken checkout.
DISPLAY_CALLS = {"markdown", "caption", "write", "info", "warning", "error",
                 "success", "header", "subheader", "title", "text"}


def page_surfaces():
    for p in sorted((ROOT / "app" / "pages").glob("*.py")):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        texts = []
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr in DISPLAY_CALLS):
                continue
            for arg in node.args:
                parts = ([arg] if isinstance(arg, ast.Constant) else
                         [v for v in getattr(arg, "values", []) if isinstance(v, ast.Constant)])
                for c in parts:
                    if isinstance(c.value, str) and not c.value.startswith("No map yet"):
                        texts.append(c.value)
        if texts:
            yield p.relative_to(ROOT).as_posix(), "\n".join(texts)


def scan(name, text):
    section = "(top)"
    for line in text.splitlines():
        h = re.match(r"^(#{1,4})\s+(.*)", line)
        if h:
            section = h.group(2).strip()
        bare = re.sub(r"<[^>]+>", "", line)
        for kind, rx in KINDS:
            m = rx.search(bare)
            if not m:
                continue
            if any(s == name and k == kind and frag in bare for s, k, frag in KEEP):
                continue
            yield kind, section, m.group(0), bare.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", help="only surfaces whose path contains this")
    ap.add_argument("--kind", help="only this kind")
    ap.add_argument("--counts", action="store_true", help="counts per surface and kind only")
    args = ap.parse_args()

    total = Counter()
    by_surface = defaultdict(list)
    for name, text in [*doc_surfaces(), *page_surfaces()]:
        if args.surface and args.surface not in name:
            continue
        for kind, section, hit, line in scan(name, text):
            if args.kind and kind != args.kind:
                continue
            total[kind] += 1
            by_surface[name].append((kind, section, hit, line))

    if args.counts:
        for name, hits in sorted(by_surface.items(), key=lambda kv: -len(kv[1])):
            c = Counter(k for k, *_ in hits)
            print(f"{len(hits):5}  {name}  " + ", ".join(f"{k} {n}" for k, n in c.most_common()))
    else:
        for name, hits in by_surface.items():
            print(f"\n== {name} ({len(hits)})")
            for kind, section, hit, line in hits:
                print(f"  [{kind}] {section[:60]} :: {hit!r} :: {line[:160]}")
    print(f"\nREPORT ONLY - {sum(total.values())} hit(s) on {len(by_surface)} surface(s): "
          + ", ".join(f"{k} {n}" for k, n in total.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
