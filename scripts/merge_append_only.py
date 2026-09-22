"""Resolve a conflicted APPEND-ONLY file without losing an entry.

`DECISIONS.md` is append-only and two sessions append to the top of it at once,
so every master<->staging merge conflicts there. The conflict is never a real
disagreement - both sides only added - so the resolution is mechanical, and
this script does it rather than leaving it to hand-editing.

WHY IT IS A SCRIPT AND NOT A NOTE. The obvious hand resolution is to take one
side's version of the file and re-append the other side's new entries. That
SILENTLY DELETES ENTRIES, and on 2026-09-22 it nearly did: master and staging
collided on nine entries at the top of `## Changes`, but staging had added a
TENTH lower down ("Japan is a BUILD, and it goes last") which had no competing
change beside it, so git auto-merged it OUTSIDE the conflict markers. Rebuilding
from master's stage would have dropped it, and an append-only log gives you no
way to notice afterwards.

    A conflict region shows where the two sides DISAGREED.
    It does not show everything the other side ADDED.

So this script edits only the conflict regions of git's own merged file, leaves
everything git already resolved alone, and refuses to write unless the result
contains exactly the union of the headings in both sides' full stages - which
is the check that would have caught the near-miss.

Ordering is MEASURED, not chosen: each new entry is dated by the commit that
introduced it, so entries from the two sides interleave by real time rather
than being stacked one side after the other.

Usage, from inside a conflicted merge:

    python scripts/merge_append_only.py DECISIONS.md [--dry-run]

Then, for DECISIONS.md, run `python scripts/decisions_index.py` before
committing - the index is generated and this script does not touch it beyond
keeping both sides' links.
"""
import argparse
import pathlib
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # city names carry accents; cp1252 raises
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OURS = "<<<<<<< "
SEP = "=======\n"
THEIRS = ">>>>>>> "


def git(*args):
    out = subprocess.run(["git", *args], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if out.returncode:
        raise SystemExit(f"git {' '.join(args)} failed:\n{out.stderr.strip()}")
    return out.stdout


def split_conflicts(text):
    """-> [(text_before, ours, theirs)], trailing_text"""
    regions, rest = [], text
    while OURS in rest:
        before, _, after = rest.partition(OURS)
        _, _, after = after.partition("\n")          # drop the branch name
        ours, _, after = after.partition(SEP)
        theirs, _, after = after.partition(THEIRS)
        _, _, after = after.partition("\n")
        regions.append((before, ours, theirs))
        rest = after
    return regions, rest


def sections(chunk, pattern, label):
    """Split a chunk into {heading: full section text}, in file order."""
    found, out = list(re.finditer(pattern, chunk, re.M)), {}
    if not found:
        return out
    if chunk[:found[0].start()].strip():
        raise SystemExit(f"{label}: text before the first heading; resolve by hand")
    for i, m in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(chunk)
        heading = m.group(0).rstrip("\n")
        if heading in out:
            raise SystemExit(f"{label}: duplicate heading {heading!r}")
        out[heading] = chunk[m.start():end]
    return out


def introduced_at(heading, base, tip, path):
    """Committer timestamp of the commit that first added this heading."""
    body = heading.lstrip("#").strip()
    log = git("log", "--format=%ct", "--reverse", "-S", body,
              f"{base}..{tip}", "--", path).split()
    return int(log[0]) if log else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="the conflicted append-only file, e.g. DECISIONS.md")
    ap.add_argument("--heading", default=r"^### .+$",
                    help="regex matching one entry's heading line (default: '### ')")
    ap.add_argument("--regenerated-block", default="INDEX:START,INDEX:END",
                    help="START,END sentinels of a GENERATED block (default: "
                         "DECISIONS.md's index). A conflict inside it keeps both "
                         "sides, because the block is rebuilt from the entries "
                         "afterwards and hand-merging it would be busywork.")
    ap.add_argument("--dry-run", action="store_true",
                    help="report the resolution without writing it")
    args = ap.parse_args()

    path = pathlib.Path(args.path)
    text = path.read_text(encoding="utf-8")
    if OURS not in text:
        raise SystemExit(f"{path}: no conflict markers - nothing to resolve")

    git_dir = pathlib.Path(git("rev-parse", "--git-dir").strip())
    if not (git_dir / "MERGE_HEAD").exists():
        raise SystemExit("not inside a conflicted merge (no MERGE_HEAD)")
    ours_rev, theirs_rev = git("rev-parse", "HEAD").strip(), git("rev-parse", "MERGE_HEAD").strip()
    base_rev = git("merge-base", ours_rev, theirs_rev).strip()

    gen_start, gen_end = (s.strip() for s in args.regenerated_block.split(","))
    regions, tail = split_conflicts(text)
    rebuilt, pool, ordered, generated = "", {}, [], 0

    for before, ours, theirs in regions:
        prefix = rebuilt + before
        # Inside the generated block if its START sentinel is the last one seen.
        if prefix.rfind(gen_start) > prefix.rfind(gen_end):
            rebuilt += before + ours + theirs
            generated += 1
            continue

        ours_s = sections(ours, args.heading, "ours")
        theirs_s = sections(theirs, args.heading, "theirs")
        if not ours_s and not theirs_s:
            # No headings in this region: both sides changed the same lines, so
            # this is a REAL disagreement and not an append. Keeping both would
            # invent content, so stop and let a human read it.
            raise SystemExit(
                f"{path}: a conflict region contains no entry headings, so the two "
                f"sides edited the same text rather than appending. Resolve that "
                f"region by hand - this script only merges whole appended entries.")

        merged = {}
        for heading, body in list(ours_s.items()) + list(theirs_s.items()):
            if heading in merged and merged[heading] != body:
                raise SystemExit(
                    f"{path}: {heading!r} exists on BOTH sides with different text. "
                    f"An append-only file should never have that - resolve by hand.")
            merged[heading] = body

        dated = []
        for heading in merged:
            when = (introduced_at(heading, base_rev, ours_rev, str(path))
                    or introduced_at(heading, base_rev, theirs_rev, str(path)))
            side = "ours" if heading in ours_s else "theirs"
            dated.append((when, heading, side))
        if any(when is None for when, _, _ in dated):
            unknown = [h for w, h, _ in dated if w is None]
            raise SystemExit(
                f"{path}: cannot date {unknown} from git history, so the order "
                f"would be a guess. Resolve by hand and say why in the message.")

        dated.sort(key=lambda row: row[0], reverse=True)   # newest first
        rebuilt += before + "".join(merged[h] for _, h, _ in dated)
        pool.update(merged)
        ordered.extend(dated)

    rebuilt += tail

    # THE CHECK THE NEAR-MISS ARGUES FOR: compare against each side's FULL file,
    # not against the conflict regions, so an entry the other side added outside
    # a conflict cannot go missing.
    def headings_of(rev):
        blob = git("show", f"{rev}:{path.as_posix()}")
        return set(re.findall(args.heading, blob, re.M))

    want = headings_of(ours_rev) | headings_of(theirs_rev)
    got = set(re.findall(args.heading, rebuilt, re.M))
    if got != want:
        missing, extra = sorted(want - got), sorted(got - want)
        raise SystemExit(
            f"{path}: REFUSING TO WRITE - the result is not the union of both sides."
            + (f"\n  missing {len(missing)}: {missing[:5]}" if missing else "")
            + (f"\n  invented {len(extra)}: {extra[:5]}" if extra else ""))

    for marker in ("<<<<<<<", ">>>>>>>", SEP.strip()):
        if marker in rebuilt:
            raise SystemExit(f"{path}: a {marker!r} survived the resolution")

    print(f"{path}: {len(regions)} conflict region(s), {generated} of them in the "
          f"generated block; {len(pool)} entries interleaved by commit time")
    for when, heading, side in ordered:
        print(f"  {side:6} {heading[:72]}")
    print(f"  + {len(want) - len(pool)} entries git merged outside the conflict, "
          f"all verified present")

    if args.dry_run:
        print("\n--dry-run: nothing written")
        return
    path.write_text(rebuilt, encoding="utf-8", newline="\n")
    print(f"\nwrote {path}. Next: `git add {path}`"
          + (", and `python scripts/decisions_index.py` first"
             if path.name == "DECISIONS.md" else ""))


if __name__ == "__main__":
    main()
