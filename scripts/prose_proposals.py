"""Collect review lanes' prose proposals into one list for the owner, and apply
only the ones the owner approves.

    python scripts/prose_proposals.py collate              # validate + write the owner's list
    python scripts/prose_proposals.py apply --ids L1-P3,L2-P1   # apply approved ones
    python scripts/prose_proposals.py apply --kind fix     # every factual fix (owner's say-so)
    python scripts/prose_proposals.py --selftest           # touches nothing

CLAUDE.md: interpretive prose is drafted in chat before it is written to a
file. A site-wide prose pass makes hundreds of such sentences, so a lane never
edits a page: it writes each proposal to its own file in the shared, gitignored
`data/_review/<lane>/proposals.md`, cleanup collates them into
`data/_review/proposals_all.md` - one numbered list the owner approves by ID -
and `apply` makes exactly the approved replacements, refusing any whose old
text is no longer in the file exactly once.

A proposal, in a lane's file (any number, any order):

    ## P1 - Edmonton's Metro Line sentence
    file: app/pages/13_Edmonton_Heatmap.py
    kind: proposal            (or: fix - a factual error with one right answer)
    why: the old sentence predates the Health Sciences call
    precedent: Sacramento's closed-station sentence      (optional)
    old:
    ~~~
    <the text EXACTLY as it is in the FILE - copied from the source, line
    breaks and all, never from the rendered page>
    ~~~
    new:
    ~~~
    <the replacement>
    ~~~

Its ID is the lane folder's name and its number: `lane-1-P1`.
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BLOCK = re.compile(r"^## (P\d+)\s*-\s*(.+?)\s*$(.*?)(?=^## P\d+\s*-|\Z)", re.M | re.S)
FIELD = re.compile(r"^(file|kind|why|precedent):\s*(.+?)\s*$", re.M)
FENCE = re.compile(r"^(old|new):\s*\n~~~\n(.*?)\n~~~\s*$", re.M | re.S)
KINDS = {"fix", "proposal"}


def review_dir(root):
    return root / "data" / "_review"


def parse(root):
    """[proposal dict] from every lane's proposals.md, with any format problems."""
    props, problems = [], []
    for f in sorted(review_dir(root).glob("*/proposals.md")):
        lane = f.parent.name
        text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        for m in BLOCK.finditer(text):
            num, title, body = m.groups()
            pid = f"{lane}-{num}"
            fields = dict(FIELD.findall(body))
            fences = dict(FENCE.findall(body))
            p = {"id": pid, "lane": lane, "title": title, **fields,
                 "old": fences.get("old"), "new": fences.get("new")}
            missing = [k for k in ("file", "kind", "why", "old", "new") if not p.get(k)]
            if missing:
                problems.append(f"{pid}: missing {', '.join(missing)}")
                continue
            if p["kind"] not in KINDS:
                problems.append(f"{pid}: kind {p['kind']!r} is not one of {sorted(KINDS)}")
                continue
            props.append(p)
    ids = [p["id"] for p in props]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"{dup}: two proposals share this number")
    return props, problems


def locate(root, p):
    """None if the old text is in the file exactly once, else why not."""
    path = root / p["file"]
    if not path.is_file():
        return f"no file {p['file']}"
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    n = text.count(p["old"])
    if n == 1:
        return None
    if n > 1:
        return f"the old text occurs {n} times in {p['file']}: quote more of it"
    squash = lambda s: re.sub(r"\s+", " ", s).strip()
    if squash(p["old"]) in squash(text):
        return (f"the old text is in {p['file']} with different line breaks: copy it "
                f"from the file, not the rendered page")
    return f"the old text is not in {p['file']} (already changed, or misquoted)"


def collate(root=ROOT, write=True):
    props, problems = parse(root)
    for p in props:
        why = locate(root, p)
        if why:
            problems.append(f"{p['id']}: {why}")
            p["stale"] = why
    # Two proposals over overlapping text cannot both be applied: compared by
    # where each old text sits in the file, not by the quotes themselves.
    spans = {}
    for p in props:
        if p.get("stale"):
            continue
        text = (root / p["file"]).read_bytes().decode("utf-8").replace("\r\n", "\n")
        a = text.index(p["old"])
        for q, qa, qb in spans.get(p["file"], []):
            if a < qb and qa < a + len(p["old"]):
                problems.append(f"{p['id']} and {q['id']}: both change the same text in {p['file']}")
        spans.setdefault(p["file"], []).append((p, a, a + len(p["old"])))
    if write:
        lines = ["# Prose proposals for the owner", "",
                 f"{len(props)} proposal(s) from {len({p['lane'] for p in props})} lane(s). "
                 "Approve by ID (\"approve lane-1-P1, lane-2-P4\"); `fix` rows correct a "
                 "fact, `proposal` rows are wording. Generated by "
                 "`scripts/prose_proposals.py collate`.", ""]
        if problems:
            lines += ["**Not ready (the lane must correct these first):**", ""]
            lines += [f"- {x}" for x in problems] + [""]
        for p in sorted(props, key=lambda p: (p["file"], p["id"])):
            lines += [f"## {p['id']} ({p['kind']}) - {p['title']}", "",
                      f"`{p['file']}`" + (" - **NOT READY**" if p.get("stale") else ""), "",
                      f"*Why:* {p['why']}" + (f"  \n*Precedent:* {p['precedent']}" if p.get("precedent") else ""),
                      "", "Old:", "", "> " + p["old"].replace("\n", "\n> "), "",
                      "New:", "", "> " + p["new"].replace("\n", "\n> "), ""]
        out = review_dir(root) / "proposals_all.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes("\n".join(lines).encode("utf-8"))
    return props, problems


def apply(root, ids=None, kind=None):
    props, _ = parse(root)
    chosen = [p for p in props if (ids and p["id"] in ids) or (kind and p["kind"] == kind)]
    unknown = sorted(set(ids or ()) - {p["id"] for p in props})
    done, refused = [], [f"{i}: no such proposal" for i in unknown]
    for p in chosen:
        why = locate(root, p)
        if why:
            refused.append(f"{p['id']}: {why}")
            continue
        path = root / p["file"]
        raw = path.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n").replace(p["old"], p["new"], 1)
        path.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
        done.append(p["id"])
    log = review_dir(root) / "applied.json"
    prior = json.loads(log.read_text(encoding="utf-8")) if log.exists() else []
    log.write_text(json.dumps(prior + done, indent=1), encoding="utf-8")
    return done, refused


def selftest():
    tmp = Path(tempfile.mkdtemp(prefix="prose-selftest-"))
    try:
        (tmp / "app").mkdir()
        page = tmp / "app" / "page.py"
        page.write_text('TEXT = """The Metro Line runs\nto Century Park."""\n', encoding="utf-8")
        lane = tmp / "data" / "_review" / "lane-1"
        lane.mkdir(parents=True)
        (lane / "proposals.md").write_text(
            "## P1 - Metro\nfile: app/page.py\nkind: fix\nwhy: ETS's terminus\nold:\n~~~\n"
            "runs\nto Century Park.\n~~~\nnew:\n~~~\nruns\nto Health Sciences.\n~~~\n\n"
            "## P2 - rewrapped\nfile: app/page.py\nkind: proposal\nwhy: x\nold:\n~~~\n"
            "The Metro Line runs to Century Park.\n~~~\nnew:\n~~~\ny\n~~~\n\n"
            "## P4 - overlaps P1\nfile: app/page.py\nkind: proposal\nwhy: x\nold:\n~~~\n"
            "Metro Line runs\n~~~\nnew:\n~~~\nMetro Line ran\n~~~\n\n"
            "## P3 - incomplete\nfile: app/page.py\nkind: proposal\nold:\n~~~\nz\n~~~\nnew:\n~~~\nw\n~~~\n",
            encoding="utf-8")
        props, problems = collate(tmp)
        cases = [
            ("parses three complete proposals", len(props) == 3),
            ("flags the incomplete one", any("lane-1-P3: missing why" in x for x in problems)),
            ("flags re-wrapped old text", any("lane-1-P2" in x and "line breaks" in x for x in problems)),
            ("flags overlapping proposals", any("both change the same text" in x for x in problems)),
            ("writes the owner's list", (tmp / "data" / "_review" / "proposals_all.md").exists()),
        ]
        done, refused = apply(tmp, ids={"lane-1-P1", "lane-1-P9"})
        cases += [
            ("applies the approved one", done == ["lane-1-P1"]
             and "Health Sciences" in page.read_text(encoding="utf-8")),
            ("refuses an unknown id", any("lane-1-P9" in x for x in refused)),
        ]
        done2, refused2 = apply(tmp, ids={"lane-1-P1"})
        cases.append(("refuses to apply twice", not done2 and any("not in" in x for x in refused2)))
        bad = [n for n, ok in cases if not ok]
        print(f"{len(cases) - len(bad)} of {len(cases)} cases behaved as intended."
              + (f" FAILED: {bad}" if bad else ""))
        return not bad
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest() else 1)
    if a[:1] == ["collate"]:
        props, problems = collate()
        print(f"{len(props)} proposal(s); {len(problems)} problem(s) -> "
              f"{(review_dir(ROOT) / 'proposals_all.md').relative_to(ROOT)}")
        for x in problems:
            print("  " + x)
        sys.exit(1 if problems else 0)
    if a[:1] == ["apply"]:
        ids = set(a[a.index("--ids") + 1].split(",")) if "--ids" in a else None
        kind = a[a.index("--kind") + 1] if "--kind" in a else None
        if not ids and not kind:
            sys.exit("apply needs --ids <id,id> or --kind fix")
        done, refused = apply(ROOT, ids, kind)
        print(f"applied {len(done)}: {', '.join(done) or '-'}")
        for x in refused:
            print("  REFUSED " + x)
        sys.exit(1 if refused else 0)
    print(__doc__)


if __name__ == "__main__":
    main()
