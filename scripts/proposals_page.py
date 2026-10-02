"""Build the owner's review page from the collated prose proposals: one card per
proposal with a word-level diff, filters by area, type and status, approve or
skip per card or per filtered view, and a button that copies the approved IDs
for the chat.

    python scripts/proposals_page.py --out <scratchpad>/review.html --commit <sha>
        [--sets sets.json] [--heading "..."] [--note "..."]
    python scripts/proposals_page.py --selftest     # touches nothing

Reads `data/_review/proposals_all.md` (`prose_proposals.py collate` writes it)
and fills `scripts/proposals_page.html`. Publish the result as a private
Artifact; decisions stay in the viewer's browser. The owner pastes the copied
line back, and cleanup applies it with `prose_proposals.py apply`: the page
never edits anything.

`--sets` is a JSON list of {"ids": ["P1321", ...], "note": "...", "label": "..."}:
proposals that must be approved together, shown in a panel at the top and on
each member's card.

The 2026-10-01 prose and UI pass is the worked example (507 proposals, all
approved): https://claude.ai/artifact/Pr5A9UwBgamasE7odYfHW5, and
docs/review_lane_kit.md section 6.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "proposals_page.html"
SOURCE = ROOT / "data" / "_review" / "proposals_all.md"
HEAD = re.compile(r"^(?P<id>\S+) \((?P<kind>[^)]+)\) - (?P<title>.*)$")


def unquote(text):
    return "\n".join(l[2:] if l.startswith("> ") else (l[1:] if l.startswith(">") else l)
                     for l in text.split("\n"))


def parse(text):
    """[{id, kind, title, file, why, old, new}] from proposals_all.md."""
    items = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        lines = block.split("\n")
        m = HEAD.match(lines[0])
        if not m:
            raise SystemExit(f"unreadable proposal heading: {lines[0][:80]!r}")
        body = "\n" + "\n".join(lines[1:]).strip("\n")
        file_m = re.search(r"(?m)^`([^`]+)`\s*$", body)
        why_m = re.search(r"(?s)\*Why:\*\s*(.*?)(?=\n\n(?:Old:|New:|\*)|\Z)", body)
        old_m = re.search(r"(?s)\nOld:\n\n(.*?)(?=\n\nNew:|\Z)", body)
        new_m = re.search(r"(?s)\nNew:\n\n(.*?)(?=\n\n[A-Z*][a-z]*[:*]|\Z)", body)
        if not (file_m and old_m and new_m):
            raise SystemExit(f"{m['id']}: no file, old or new text")
        items.append({"id": m["id"], "kind": m["kind"], "title": m["title"],
                      "file": file_m.group(1), "why": why_m.group(1).strip() if why_m else "",
                      "old": unquote(old_m.group(1).strip()), "new": unquote(new_m.group(1).strip())})
    return items


def sets_panel(sets):
    if not sets:
        return ""
    rows = "".join(f"      <li>{html.escape(s.get('label') or s['note'])}</li>\n" for s in sets)
    return ('  <details class="sets" open>\n    <summary>Sets that go together</summary>\n'
            f"    <ul>\n{rows}    </ul>\n  </details>")


def build(items, commit, sets=(), heading="Prose proposals", note=""):
    page = TEMPLATE.read_text(encoding="utf-8")
    data = json.dumps(items, ensure_ascii=False).replace("</", "<" + "\\/")
    js_sets = json.dumps([{"ids": s["ids"], "note": s["note"]} for s in sets], ensure_ascii=False)
    fills = {"__HEADING__": html.escape(heading), "__COMMIT__": html.escape(commit),
             "__NOTE__": f'  <p class="lede">{html.escape(note)}</p>' if note else "",
             "__SETS_PANEL__": sets_panel(sets), "__SETS_JSON__": js_sets, "__DATA__": data}
    for key, value in fills.items():
        assert page.count(key) == 1, key
        page = page.replace(key, value)
    return page


def selftest():
    sample = ("# Prose proposals\n\n## lane-1-P1 (fix) - A title\n\n`app/x.py`\n\n*Why:* a reason\n\n"
              "Old:\n\n> old line\n> two\n\nNew:\n\n> new line\n> two\n")
    items = parse(sample)
    page = build(items, "abc123", [{"ids": ["P1"], "note": "goes alone"}], "H", "N")
    cases = [
        (len(items), 1),
        (items[0]["old"], "old line\ntwo"),
        (items[0]["file"], "app/x.py"),
        ("__" in re.sub(r"__[a-z]", "", page.split('id="data">')[0]), False),   # every placeholder filled
        ("goes alone" in page, True),
    ]
    bad = [i for i, (got, want) in enumerate(cases) if got != want]
    print(f"{len(cases) - len(bad)} of {len(cases)} cases behaved as intended."
          + (f" FAILED: {bad}" if bad else ""))
    return not bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--sets", type=Path)
    ap.add_argument("--heading", default="Prose proposals")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    items = parse(SOURCE.read_text(encoding="utf-8"))
    sets = json.loads(a.sets.read_text(encoding="utf-8")) if a.sets else []
    a.out.write_text(build(items, a.commit, sets, a.heading, a.note), encoding="utf-8")
    print(f"{len(items)} proposals -> {a.out}")


if __name__ == "__main__":
    main()
