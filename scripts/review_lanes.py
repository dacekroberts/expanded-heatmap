"""Make, list and remove review-lane worktrees - one per lane, all on one
pinned commit, each with its own ports and review folder.

    python scripts/review_lanes.py create --sha <commit> --lanes 4   # lane-1..lane-4
    python scripts/review_lanes.py list
    python scripts/review_lanes.py remove [--lanes 4]                # unlinks junctions first

What the 2026-09-30 mega-review did by hand, and learned (lessons 2 and 4,
docs/review_lanes_2026-09-30.md; the kit is docs/review_lane_kit.md):

  * every lane on ONE commit, detached, so findings refer to the same tree;
  * `data/` and `.venv-lean` are JUNCTIONS to the main checkout's (never a
    copy: data/ is one shared folder, and a lane never pip-installs);
  * its own ports - Streamlit 88N1, static maps 88N2, the capture browser's
    DevTools port 93N1 - written into the worktree's .claude/launch.json under
    deploy-verify's configuration names, so two lanes never stop each other's
    servers;
  * its own review folder, data/_review/lane-N/ (shared, gitignored): the
    lane's report, captures and prose proposals
    (scripts/prose_proposals.py) live there;
  * removal UNLINKS each junction before `git worktree remove`, which would
    otherwise follow it into the shared folder.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main_checkout():
    """The main working tree (where the real data/ and .venv-lean live)."""
    out = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return Path(out.split("\n", 1)[0].split(" ", 1)[1].strip())


def lane_dir(main, n):
    return main / ".claude" / "worktrees" / f"review-lane-{n}"


def ports(n):
    return {"streamlit": 8800 + 10 * n + 1, "static": 8800 + 10 * n + 2, "cdp": 9300 + 10 * n + 1}


def launch_json(n):
    p = ports(n)
    return {"version": "0.0.1", "configurations": [
        {"name": "streamlit-app-lean", "runtimeExecutable": ".venv-lean/Scripts/python.exe",
         "runtimeArgs": ["-m", "streamlit", "run", "app/Overview.py", "--server.port",
                         str(p["streamlit"]), "--server.headless", "true"],
         "port": p["streamlit"]},
        {"name": "heatmap-static", "runtimeExecutable": "python",
         "runtimeArgs": ["-m", "http.server", str(p["static"]), "--directory", "outputs"],
         "port": p["static"]},
    ]}


def is_junction(path):
    try:
        return bool(os.readlink(path))
    except (OSError, ValueError):
        return False


def junction(target, link):
    import _winapi  # Windows only - the project's machine
    _winapi.CreateJunction(str(target), str(link))


def create(sha, lanes):
    main = main_checkout()
    full = subprocess.run(["git", "rev-parse", "--verify", sha + "^{commit}"], cwd=ROOT,
                          capture_output=True, text=True)
    if full.returncode:
        sys.exit(f"{sha}: not a commit")
    sha = full.stdout.strip()
    for n in range(1, lanes + 1):
        d = lane_dir(main, n)
        if d.exists():
            print(f"lane {n}: {d} exists - skipped (remove it first)")
            continue
        subprocess.run(["git", "worktree", "add", "--detach", str(d), sha], cwd=ROOT, check=True,
                       capture_output=True)
        for name in ("data", ".venv-lean"):
            if (d / name).exists():
                sys.exit(f"lane {n}: {name} exists in the checkout itself - refusing to link over it")
            junction(main / name, d / name)
        (d / ".claude").mkdir(exist_ok=True)
        (d / ".claude" / "launch.json").write_bytes(
            json.dumps(launch_json(n), indent=2).encode("utf-8") + b"\n")
        (main / "data" / "_review" / f"lane-{n}").mkdir(parents=True, exist_ok=True)
        p = ports(n)
        print(f"lane {n}: {d} at {sha[:8]}; Streamlit {p['streamlit']}, static {p['static']}, "
              f"capture --cdp {p['cdp']}; review folder data/_review/lane-{n}/")


def lanes_present(main):
    return sorted((p for p in (main / ".claude" / "worktrees").glob("review-lane-*")),
                  key=lambda p: int(p.name.rsplit("-", 1)[1]))


def show():
    main = main_checkout()
    for d in lanes_present(main):
        head = subprocess.run(["git", "-C", str(d), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(d), "status", "--porcelain"],
                               capture_output=True, text=True).stdout.strip()
        links = {n: is_junction(d / n) for n in ("data", ".venv-lean")}
        print(f"{d.name}: {head}{' DIRTY' if dirty else ''}; junctions "
              + ", ".join(f"{k} {'ok' if v else 'MISSING'}" for k, v in links.items()))
    if not lanes_present(main):
        print("no review lanes")


def remove(lanes=None):
    main = main_checkout()
    for d in lanes_present(main):
        n = int(d.name.rsplit("-", 1)[1])
        if lanes and n > lanes:
            continue
        dirty = subprocess.run(["git", "-C", str(d), "status", "--porcelain",
                                "--untracked-files=no"], capture_output=True, text=True).stdout.strip()
        if dirty:
            print(f"{d.name}: tracked files changed - a lane never edits; left for a look:\n{dirty}")
            continue
        for name in ("data", ".venv-lean"):
            link = d / name
            if is_junction(link):
                os.rmdir(link)            # removes the link, never the target
            elif link.exists():
                sys.exit(f"{link} is a real folder, not a junction - refusing to remove {d.name}")
        before = len(list((main / "data").iterdir()))
        subprocess.run(["git", "worktree", "remove", "--force", str(d)], cwd=ROOT, check=True)
        after = len(list((main / "data").iterdir()))
        if after != before:
            sys.exit(f"data/ changed from {before} to {after} entries while removing {d.name} - stop and look")
        print(f"{d.name}: removed; data/ intact ({after} entries); its review folder "
              f"data/_review/lane-{n}/ kept")


def main():
    a = sys.argv[1:]
    num = int(a[a.index("--lanes") + 1]) if "--lanes" in a else None
    if a[:1] == ["create"]:
        if "--sha" not in a or not num:
            sys.exit("create needs --sha <commit> and --lanes <n>")
        create(a[a.index("--sha") + 1], num)
    elif a[:1] == ["list"]:
        show()
    elif a[:1] == ["remove"]:
        remove(num)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
