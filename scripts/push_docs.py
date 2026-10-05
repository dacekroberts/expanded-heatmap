"""Push a docs-only session's committed work to master, the ritual in one command.

    python scripts/push_docs.py [--dry-run]

For staging and other sessions whose pushes touch no deployed or pipeline
file. In order: refuse a dirty tree; `git fetch`; merge origin/master; run
`scripts/regen_generated.py` and stop if it rewrote anything (a rewritten
generated file is a question for the session that owns it, never something to
commit blind: on 2026-10-04 one was another session's stale record); refuse if
the push would change any path under `app/`, `outputs/`, `pipeline/` or a
requirements file (landing `app/` on master IS deploying, `publish-city`);
`scripts/decisions_index.py --check`; re-fetch and re-merge if master moved
meanwhile (CLAUDE.md, "Re-check origin/master in the same breath as the
push"); push to master and to the current branch, which runs the pre-push hook
(`scripts/check_all.py`); then `scripts/downstream_changes.py` from the
master the push started from.

`--dry-run` does everything up to the push and prints what would be pushed.
Commits nothing itself: commit first, with the session's own message.
"""
import argparse
import subprocess
import sys

ROOT_CMD = ["git", "rev-parse", "--show-toplevel"]
REFUSED = ("app/", "outputs/", "pipeline/", "requirements.txt", "requirements-pipeline.txt")


def run(cmd, check=True, capture=True):
    p = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8",
                       capture_output=capture)
    if check and p.returncode != 0:
        out = (p.stdout or "") + (p.stderr or "")
        sys.exit(f"FAILED: {' '.join(cmd)}\n{out.strip()}")
    return (p.stdout or "").strip()


def merge_master():
    run(["git", "fetch", "-q", "origin"])
    behind = run(["git", "rev-list", "--count", "HEAD..origin/master"])
    if behind != "0":
        p = subprocess.run(["git", "merge", "--no-edit", "origin/master"], cwd=ROOT,
                           text=True, encoding="utf-8", capture_output=True)
        if p.returncode != 0:
            sys.exit("Merge conflict with origin/master: resolve it (an append-only file with "
                     "scripts/merge_append_only.py), commit, and run this again.\n" + p.stdout + p.stderr)
        print(f"merged {behind} commit(s) from origin/master")
    regen = subprocess.run([sys.executable, "scripts/regen_generated.py"], cwd=ROOT,
                           text=True, encoding="utf-8", capture_output=True)
    dirty = run(["git", "status", "--porcelain"])
    if dirty:
        sys.exit("regen_generated.py rewrote files after the merge; stopping before the push:\n"
                 + dirty + "\nAsk the session that owns them, or commit them with the merge if they are yours.\n"
                 + regen.stdout[-800:])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if run(["git", "status", "--porcelain"]):
        sys.exit("The working tree has uncommitted changes: commit or set them aside first.")
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch in ("HEAD", "master"):
        sys.exit(f"On {branch!r}: run this from the session's own branch.")

    run(["git", "fetch", "-q", "origin"])
    start = run(["git", "rev-parse", "origin/master"])
    for _ in range(3):
        merge_master()
        changed = run(["git", "diff", "--name-only", "origin/master", "HEAD"]).splitlines()
        refused = [f for f in changed if f.startswith(REFUSED)]
        if refused:
            sys.exit("This push would change deployed or pipeline files; use publish-city instead:\n  "
                     + "\n  ".join(refused))
        run([sys.executable, "scripts/decisions_index.py", "--check"])
        run(["git", "fetch", "-q", "origin"])
        if run(["git", "rev-list", "--count", "HEAD..origin/master"]) == "0":
            break
        print("origin/master moved during the checks; merging again")
    else:
        sys.exit("origin/master kept moving; try again in a minute.")

    if not changed:
        print("Nothing to push: HEAD matches origin/master.")
        return
    print(f"{len(changed)} file(s) to push from {branch}:")
    for f in changed:
        print("  " + f)
    if a.dry_run:
        print("--dry-run: stopping before the push.")
        return

    p = subprocess.run(["git", "push", "origin", "HEAD:master", f"HEAD:{branch}"], cwd=ROOT,
                       text=True, encoding="utf-8")
    if p.returncode != 0:
        sys.exit("The push failed (the pre-push hook's output is above). Fix what it names; never skip the hook.")
    print(run([sys.executable, "scripts/downstream_changes.py", start, "HEAD"]))


ROOT = subprocess.run(ROOT_CMD, text=True, capture_output=True).stdout.strip() or "."

if __name__ == "__main__":
    main()
