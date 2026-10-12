"""Stage place-index names for an outside name review, and collect its replies.

A second net beside the place-read agent, never instead of it (owner,
2026-10-12). This script sends nothing and calls no model: `stage` writes the
row files a reviewer reads, `collect` turns the replies into one TSV of
flagged rows per city. The call to the outside model is made by hand, each
one with the owner's yes.

Only index files are read, and only from git objects (`git show REF:PATH`),
so what is staged is exactly what a commit holds. A path outside
app/static/places/ is refused: nothing under data/ and no business register
may reach an outside model (PLAN.md, "Nothing from a business register goes
to an outside model").

Usage (from the repository root; REF is any commit or branch):
  python place_name_net.py stage OUT_DIR --ref REF [--chunk N] INDEX_PATH [INDEX_PATH ...]
  python place_name_net.py collect OUT_DIR
  python place_name_net.py --selftest

OUT_DIR layout (keep it in the session scratchpad, never in the repository):
  OUT_DIR/<slug>/chunk_NN/rows.txt    what the reviewer reads
  OUT_DIR/<slug>/chunk_NN/reply.txt   the reviewer's reply, saved by the caller
  OUT_DIR/<slug>/key.json             the commit's hash and number -> [kind, name];
                                      not for the reviewer
  OUT_DIR/<slug>.flagged.tsv          written by collect

Exit codes: 0 done; 1 a row unanswered or a reply missing (collect), so a
partial reply is never read as a clean city; 2 a bad argument or a refused
path.
"""
import contextlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

INDEX_DIR = "app/static/places"
# Streets and crossings are judged by rules on their ways, not by name.
JUDGED = ("station", "junction", "landmark", "place")
CLASSES = ("home", "business", "description", "glitch", "other")
# Measured 2026-10-12: 300 to 560 rows a call came back complete on 19 cities.
DEFAULT_CHUNK = 320


class Refused(Exception):
    """A path or argument this script will not act on."""


def _git_show(repo, ref, path):
    done = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{path}"],
                          capture_output=True)
    if done.returncode != 0:
        raise Refused(f"{ref}:{path} is not in git: "
                      + done.stderr.decode("utf-8", "replace").strip())
    return done.stdout.decode("utf-8")


def _resolve(repo, ref):
    """The full hash of the commit REF names, or Refused."""
    done = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify",
                           f"{ref}^{{commit}}"], capture_output=True)
    if done.returncode != 0:
        raise Refused(f"{ref} names no commit: "
                      + done.stderr.decode("utf-8", "replace").strip())
    return done.stdout.decode("ascii").strip()


def _index_slug(path):
    """The city slug of an index path, or Refused for any other path."""
    posix = PurePosixPath(str(path).replace("\\", "/"))
    # A path that climbs out or is absolute has another parent, so one test
    # refuses them all.
    if str(posix.parent) != INDEX_DIR or posix.suffix != ".json":
        raise Refused(f"{path}: not an index file ({INDEX_DIR}/<slug>.json)")
    return posix.stem


def _one_line(text):
    return " ".join(str(text).replace("\t", " ").split())


def rows_to_review(index):
    """[(kind, name, alternates)] for the judged kinds, one per kind and name.

    Coordinates and bounding boxes are left behind: the judgment needs none.
    """
    kinds = index["kinds"]
    merged = {}
    for row in index["rows"]:
        kind = kinds[row[0]]
        if kind not in JUDGED:
            continue
        alts = merged.setdefault((kind, row[3]), [])
        for alt in (row[4] or "").split("|"):
            if alt and alt not in alts:
                alts.append(alt)
    return [(kind, name, alts) for (kind, name), alts in sorted(merged.items())]


def stage(repo, out_dir, ref, paths, chunk=DEFAULT_CHUNK):
    """Write rows files and keys; return [(slug, rows, chunks)]."""
    if chunk < 1:
        raise Refused("--chunk must be at least 1")
    slugs = [_index_slug(p) for p in paths]  # every path is checked before any read
    # The ref is resolved once: a branch that moves later cannot blur what
    # was staged, and every city in one run comes from one commit.
    commit = _resolve(repo, ref)
    report = []
    for slug, path in zip(slugs, paths):
        index = json.loads(_git_show(repo, commit, str(path).replace("\\", "/")))
        rows = rows_to_review(index)
        listed = ", ".join(index.get("languages", {}).get("listed", []))
        header = (f"# city: {index.get('city', slug)}; languages: {listed}; "
                  "columns: number, kind, name, alternate names")
        city_dir = Path(out_dir) / slug
        key, n_chunks = {}, 0
        for start in range(0, len(rows), chunk):
            n_chunks += 1
            lines = [header]
            for offset, (kind, name, alts) in enumerate(rows[start:start + chunk]):
                number = start + offset + 1
                key[str(number)] = [kind, name]
                lines.append("\t".join([str(number), kind, _one_line(name),
                                        " | ".join(_one_line(a) for a in alts)]))
            chunk_dir = city_dir / f"chunk_{n_chunks:02d}"
            chunk_dir.mkdir(parents=True, exist_ok=True)
            (chunk_dir / "rows.txt").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
        city_dir.mkdir(parents=True, exist_ok=True)
        (city_dir / "key.json").write_bytes(
            json.dumps({"ref": ref, "commit": commit, "path": str(path), "rows": key},
                       ensure_ascii=False).encode("utf-8"))
        report.append((slug, len(rows), n_chunks))
    return report


def parse_reply(text):
    """{number: (verdict, class, reason)} from a reply.

    A line that is not `number, keep|flag, class, reason` is ignored, so its
    row counts as unanswered. A flag with a class outside CLASSES is still a
    flag (class "other"): an odd label must not hide a flagged row. A row
    answered twice is flagged if either answer flags it.
    """
    answers = {}
    for line in text.splitlines():
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) < 2 or not parts[0].isdigit():
            continue
        verdict = parts[1].lower()
        if verdict not in ("keep", "flag"):
            continue
        klass = parts[2].lower() if len(parts) > 2 else "-"
        reason = parts[3] if len(parts) > 3 else "-"
        if verdict == "flag" and klass not in CLASSES:
            reason, klass = f"{reason} [class given: {klass}]", "other"
        number = str(int(parts[0]))
        if number in answers and answers[number][0] == "flag":
            continue
        answers[number] = (verdict, klass, reason)
    return answers


def collect(out_dir):
    """Write <slug>.flagged.tsv per city; return (report lines, problems)."""
    out_dir = Path(out_dir)
    report, problems = [], []
    for key_path in sorted(out_dir.glob("*/key.json")):
        city_dir, slug = key_path.parent, key_path.parent.name
        key = json.loads(key_path.read_text(encoding="utf-8"))["rows"]
        answers = {}
        for chunk_dir in sorted(city_dir.glob("chunk_*")):
            reply = chunk_dir / "reply.txt"
            if not reply.is_file():
                problems.append(f"{slug}: {chunk_dir.name} has no reply.txt")
                continue
            for number, answer in parse_reply(
                    reply.read_text(encoding="utf-8", errors="replace")).items():
                if number in key and answers.get(number, ("keep",))[0] != "flag":
                    answers[number] = answer
        unanswered = [n for n in key if n not in answers]
        if unanswered:
            shown = ", ".join(sorted(unanswered, key=int)[:10])
            problems.append(f"{slug}: {len(unanswered)} of {len(key)} row(s) "
                            f"unanswered (numbers {shown})")
        flagged = [(n, a) for n, a in sorted(answers.items(), key=lambda x: int(x[0]))
                   if a[0] == "flag"]
        lines = ["number\tkind\tname\tclass\treason"]
        lines += ["\t".join([n, key[n][0], _one_line(key[n][1]), a[1], _one_line(a[2])])
                  for n, a in flagged]
        (out_dir / f"{slug}.flagged.tsv").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
        report.append(f"{slug}: {len(flagged)} flagged of {len(answers)} answered, "
                      f"{len(key)} staged")
    if not report and not problems:
        problems.append(f"{out_dir}: no staged city (no */key.json)")
    return report, problems


def main(argv, repo=None):
    # Index paths are repository paths, so the checkout is the current folder:
    # the script itself may sit outside it.
    repo = Path(repo) if repo else Path.cwd()
    if argv == ["--selftest"]:
        return selftest()
    try:
        if len(argv) >= 2 and argv[0] == "stage":
            out_dir, rest = argv[1], argv[2:]
            ref, chunk, paths = None, DEFAULT_CHUNK, []
            i = 0
            while i < len(rest):
                if rest[i] in ("--ref", "--chunk"):
                    if i + 1 >= len(rest):
                        raise Refused(f"{rest[i]} needs a value")
                    if rest[i] == "--ref":
                        ref = rest[i + 1]
                    elif not rest[i + 1].isdigit():
                        raise Refused("--chunk needs a whole number")
                    else:
                        chunk = int(rest[i + 1])
                    i += 2
                else:
                    paths.append(rest[i])
                    i += 1
            if not ref:
                raise Refused("stage needs --ref REF: rows come from a commit, "
                              "never from the working tree")
            if not paths:
                raise Refused("stage needs at least one index path")
            for slug, n_rows, n_chunks in stage(repo, out_dir, ref, paths, chunk):
                print(f"{slug}: {n_rows} row(s) in {n_chunks} chunk(s)")
            return 0
        if len(argv) == 2 and argv[0] == "collect":
            report, problems = collect(argv[1])
            for line in report:
                print(line)
            for line in problems:
                print("PROBLEM", line)
            return 1 if problems else 0
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    print(__doc__.split("Usage")[1].split("OUT_DIR layout")[0].rstrip(), file=sys.stderr)
    return 2


def selftest():
    """Every case runs main() on a throwaway git repository."""
    failures = []

    def check(label, ok):
        if not ok:
            failures.append(label)

    def git(repo, *args):
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=selftest",
                        "-c", "user.email=selftest@example.invalid",
                        "-c", "core.autocrlf=false", *args],
                       check=True, capture_output=True)

    index = {
        "city": "Testville", "languages": {"listed": ["English", "Korean"]},
        "kinds": ["station", "junction", "landmark", "place", "street", "crossing"],
        "rows": [
            [0, 11.111, 22.222, "Central", "Main Station", 0],
            [2, 11.112, 22.223, "Smith House", "", 0],
            [2, 11.113, 22.224, "Smith House", "Casa Smith", 0],
            [2, 11.114, 22.225, "Tab\tand\nbreak", "", 0],
            [3, 11.115, 22.226, "Old Town", "", 0],
            [4, 11.116, 22.227, "High Street", "", [1, 2, 3, 4]],
            [5, 11.117, 22.228, "High Street & Low Street", "", 0],
        ],
    }
    with tempfile.TemporaryDirectory() as tmp:
        repo, out = Path(tmp) / "repo", Path(tmp) / "out"
        (repo / INDEX_DIR).mkdir(parents=True)
        (repo / "data").mkdir()
        path = f"{INDEX_DIR}/testville.json"
        (repo / path).write_bytes(json.dumps(index).encode("utf-8"))
        (repo / "data" / "register.json").write_bytes(json.dumps(index).encode("utf-8"))
        (repo / INDEX_DIR / "crossings").mkdir()
        (repo / INDEX_DIR / "crossings" / "testville.json").write_bytes(
            json.dumps(index).encode("utf-8"))
        git(repo, "init", "-q")
        git(repo, "add", "-f", path, "data/register.json",
            f"{INDEX_DIR}/crossings/testville.json")
        git(repo, "commit", "-q", "-m", "index")
        # The working tree now differs from the commit.
        changed = dict(index, rows=index["rows"] + [[3, 1.0, 2.0, "Uncommitted Place", "", 0]])
        (repo / path).write_bytes(json.dumps(changed).encode("utf-8"))

        code = main(["stage", str(out), "--ref", "HEAD", "--chunk", "2", path], repo)
        check("stage exits 0", code == 0)
        chunks = sorted((out / "testville").glob("chunk_*/rows.txt"))
        staged = "".join(c.read_text(encoding="utf-8") for c in chunks)
        body = [l for l in staged.splitlines() if not l.startswith("#")]
        check("streets and crossings are not staged", "High Street" not in staged)
        check("coordinates are not staged",
              "11.11" not in staged and "22.22" not in staged)
        check("rows come from the commit, not the working tree",
              "Uncommitted Place" not in staged and "Old Town" in staged)
        check("one row per kind and name, alternates merged",
              sum("Smith House" in l for l in body) == 1 and "Casa Smith" in staged)
        check("a tab or line break in a name cannot split a row",
              len(body) == 4 and all(len(l.split("\t")) == 4 for l in body))
        check("rows are cut into chunks, numbered through",
              len(chunks) == 2 and [l.split("\t")[0] for l in body] == ["1", "2", "3", "4"])
        check("the header names the city's languages",
              "languages: English, Korean" in staged)
        key_file = json.loads((out / "testville" / "key.json").read_text(encoding="utf-8"))
        head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True).stdout.decode("ascii").strip()
        check("the key records the commit's full hash, not the ref's name",
              len(head) >= 40 and key_file.get("commit") == head)
        key = key_file["rows"]
        house = next(n for n, v in key.items() if v[1] == "Smith House")
        town = next(n for n, v in key.items() if v[1] == "Old Town")

        for bad, label in (("data/register.json", "a data/ path is refused"),
                           (f"{INDEX_DIR}/../../data/register.json", "a path climbing out is refused"),
                           (str(repo / path), "an absolute path is refused"),
                           (f"{INDEX_DIR}/crossings/testville.json", "a file below the index folder is refused")):
            other = Path(tmp) / "refused"
            code = main(["stage", str(other), "--ref", "HEAD", bad], repo)
            check(label, code == 2 and not other.exists())
        code = main(["stage", str(Path(tmp) / "noref"), path], repo)
        check("stage without --ref is refused", code == 2)
        mixed = Path(tmp) / "mixed"
        code = main(["stage", str(mixed), "--ref", "HEAD", path, "data/register.json"], repo)
        check("one refused path stages nothing", code == 2 and not mixed.exists())

        def reply(chunk, text):
            (out / "testville" / chunk / "reply.txt").write_bytes(text.encode("utf-8"))

        def run_collect():
            code = main(["collect", str(out)], repo)
            tsv = (out / "testville.flagged.tsv").read_text(encoding="utf-8").splitlines()
            return code, tsv

        numbers = sorted(key, key=int)
        full = {n: f"{n}\tkeep\t-\t-" for n in numbers}
        full[house] = f"{house}\tflag\thome\tnamed as a house"

        def write_all(lines):
            reply("chunk_01", "\n".join(lines[n] for n in numbers[:2]) + "\nDONE 2\n")
            reply("chunk_02", "\n".join(lines[n] for n in numbers[2:]) + "\nDONE 2\n")

        write_all(full)
        code, tsv = run_collect()
        check("a complete reply exits 0", code == 0)
        check("a flagged row is written with kind, name, class and reason",
              tsv[1:] == [f"{house}\tlandmark\tSmith House\thome\tnamed as a house"])
        check("a kept row is not written", not any("Old Town" in l for l in tsv))

        missing = dict(full)
        missing[town] = "the reviewer grouped this row with the last"
        write_all(missing)
        code, _ = run_collect()
        check("an unanswered row exits 1", code == 1)

        odd = dict(full)
        odd[town] = f"{town}\tflag\tresidence\ta class not in the list"
        write_all(odd)
        code, tsv = run_collect()
        check("a flag with an unknown class is still a flag",
              code == 0 and any(l.startswith(f"{town}\tplace\tOld Town\tother\t") for l in tsv))

        twice = dict(full)
        twice[town] = f"{town}\tflag\tglitch\tfirst answer\n{town}\tkeep\t-\t-"
        write_all(twice)
        code, tsv = run_collect()
        check("a row answered flag then keep stays flagged",
              any(l.startswith(f"{town}\t") for l in tsv))
        twice[town] = f"{town}\tkeep\t-\t-\n{town}\tflag\tglitch\tsecond answer"
        write_all(twice)
        code, tsv = run_collect()
        check("a row answered keep then flag is flagged",
              any(l.startswith(f"{town}\t") for l in tsv))

        stray = dict(full)
        stray[town] = f"{town}\tkeep\t-\t-\n999\tflag\thome\ta number never staged"
        write_all(stray)
        code, tsv = run_collect()
        check("a number never staged is not written", code == 0 and len(tsv) == 2)

        write_all(full)
        (out / "testville" / "chunk_02" / "reply.txt").unlink()
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            code = main(["collect", str(out)], repo)
        check("a chunk with no reply exits 1", code == 1)
        check("a chunk with no reply is named", "chunk_02 has no reply.txt" in said.getvalue())
        check("collect on a folder with nothing staged exits 1",
              main(["collect", str(Path(tmp) / "empty")], repo) == 1)

    for label in failures:
        print("FAIL", label)
    print(f"selftest: {'FAILED' if failures else 'passed'}, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
