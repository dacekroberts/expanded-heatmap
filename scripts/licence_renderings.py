"""Licence texts: every stored PDF and HTML file has a plain-text rendering
beside it, and the rendering is the one its recorded hash describes.

    python scripts/licence_renderings.py            # check, change nothing
    python scripts/licence_renderings.py --write    # write what is missing, list the hashes
    python scripts/licence_renderings.py --selftest

WHY (owner, 2026-10-12). scripts/commercial_use_quote_check.py confirms that a
quoted sentence is in a stored licence text. Read straight from the stored
file that fails for reasons that have nothing to do with the sentence: an
HTML file holds hundreds of tags and entities, so a quote that crosses one is
not found, and a PDF is only text after pdftotext has run, which gives
different line breaks on a machine with another version and nothing at all
on a machine without it. A rendering is made once, stored, hashed, and read
by the first pass and by the checker alike, so both see the same characters
on every machine.

THE STORED FILES ARE NOT TOUCHED. docs/licenses/README.md says a stored file
is kept as retrieved; a rendering is a second file, <name>.txt beside
<name>, and its hash sits in a second block of the README, "SHA-256 of the
text renderings", which names the tool that made it. The first block and the
files it lists stay as they are.

How a rendering is made:
  .pdf   pdftotext -enc UTF-8 (the version is recorded in the README); a form
         feed becomes a blank line, line ends become LF.
  .html  Python's html.parser: tags removed, entities decoded, the contents
         of script, style, noscript, template and head dropped, a line break
         at the end of each block element, runs of spaces and of blank lines
         collapsed. Nothing is reworded and no character of the text is
         changed, so a sentence in the rendering is a sentence of the page.

Without --write the script changes nothing: it exits non-zero naming every
stored PDF or HTML file with no rendering, every rendering whose bytes do not
match its listed hash, and every rendering listed with no file. It does NOT
re-run pdftotext to compare: another version breaks lines elsewhere, and the
stored rendering, not this machine's, is the one the audit quoted from.
--write makes only the renderings that are missing, never replaces one, and
rewrites the README's second block from the files on disk. To replace a
rendering, delete it and run --write; the new hash then shows in the diff.
"""
import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LICENCES = ROOT / "docs" / "licenses"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RENDERED = (".pdf", ".html")
ORIGINALS_HEAD = "## SHA-256, as retrieved"
RENDERINGS_HEAD = "## SHA-256 of the text renderings"
_BLOCK_RE = "{head}.*?```\n(.*?)```"
_DROPPED = {"script", "style", "noscript", "template", "head"}
_BLOCKS = {"p", "div", "br", "li", "ul", "ol", "tr", "table", "section", "article",
           "header", "footer", "nav", "aside", "main", "h1", "h2", "h3", "h4", "h5",
           "h6", "blockquote", "pre", "hr", "dt", "dd", "dl", "form", "title"}


class _Text(HTMLParser):
    """Collects a page's text: a newline at each block element, nothing from
    script, style, noscript, template or head."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.dropped = 0

    def handle_starttag(self, tag, attrs):
        if tag in _DROPPED:
            self.dropped += 1
        elif tag in _BLOCKS:
            self.parts.append("\n")
        elif tag in ("td", "th"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in _DROPPED:
            self.dropped = max(0, self.dropped - 1)
        elif tag in _BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.dropped:
            self.parts.append(data)


def _tidy(text):
    """LF line ends, no trailing spaces, spaces in a line collapsed to one,
    blank lines to one, one final newline. No character of a word changes."""
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n\n")
    lines = [re.sub("[ \t\u00a0]+", " ", line).strip() for line in text.split("\n")]
    out, blank = [], True
    for line in lines:
        if line:
            out.append(line)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    while out and not out[-1]:
        out.pop()
    return "\n".join(out) + "\n"


def render_html(data):
    """(text, None) for an HTML file's bytes, or (None, why)."""
    try:
        source = data.decode("utf-8")
    except UnicodeDecodeError:
        return None, "not UTF-8, and no other encoding is guessed"
    parser = _Text()
    parser.feed(source)
    parser.close()
    return _tidy("".join(parser.parts)), None


def pdftotext_version():
    """The first line pdftotext prints for -v, or None when it is not there."""
    if not shutil.which("pdftotext"):
        return None
    proc = subprocess.run(["pdftotext", "-v"], capture_output=True)
    said = (proc.stderr or proc.stdout).decode("utf-8", errors="replace").strip()
    return said.splitlines()[0].strip() if said else "pdftotext (version not reported)"


def render_pdf(path):
    """(text, None) for a PDF by pdftotext, or (None, why). Never a
    hand-written decoder."""
    if not shutil.which("pdftotext"):
        return None, "pdftotext is not installed, so no PDF can be rendered here"
    proc = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True)
    if proc.returncode != 0:
        return None, f"pdftotext failed (exit {proc.returncode})"
    try:
        return _tidy(proc.stdout.decode("utf-8")), None
    except UnicodeDecodeError:
        return None, "pdftotext output is not UTF-8"


def render(path, pdf_renderer=render_pdf):
    if path.suffix.lower() == ".pdf":
        return pdf_renderer(path)
    return render_html(path.read_bytes())


def read_block(readme_text, head):
    """{file name: hash} from the fenced block under one README heading, or
    None when the heading or its block is not there."""
    m = re.search(_BLOCK_RE.format(head=re.escape(head)), readme_text, re.S)
    if not m:
        return None
    listed = {}
    for line in m.group(1).strip().split("\n"):
        parts = line.split()
        if len(parts) == 2:
            listed[parts[1]] = parts[0]
    return listed


def _sha(path):
    """The hash of a file as git stores it: CRLF read as LF, since a working
    tree on Windows can hold CRLF for a file committed with LF."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def state(licences_dir):
    """(originals, listed, problems): the stored PDF and HTML files the first
    block lists, the renderings the second block lists, and what is wrong."""
    readme = licences_dir / "README.md"
    try:
        text = readme.read_bytes().decode("utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError) as exc:
        return [], {}, [f"cannot read {readme}: {exc}"]
    first = read_block(text, ORIGINALS_HEAD)
    if first is None:
        return [], {}, [f"{readme}: no '{ORIGINALS_HEAD}' block"]
    originals = sorted(n for n in first if Path(n).suffix.lower() in RENDERED)
    listed = read_block(text, RENDERINGS_HEAD) or {}
    problems = []
    for name in originals:
        rendering = licences_dir / (name + ".txt")
        if not rendering.is_file():
            problems.append(f"{name}: no rendering ({rendering.name}); run with --write")
        elif rendering.name not in listed:
            problems.append(f"{rendering.name}: on disk but not in the README's "
                            f"'{RENDERINGS_HEAD}' block; run with --write")
        elif _sha(rendering) != listed[rendering.name]:
            problems.append(f"{rendering.name}: its bytes do not match its listed hash; "
                            f"it was edited or replaced. Restore it from git, or delete "
                            f"it and run with --write to record a new one")
    for name in sorted(listed):
        if not (licences_dir / name).is_file():
            problems.append(f"{name}: listed as a rendering but the file is gone")
        elif name[:-4] not in originals:
            problems.append(f"{name}: listed as a rendering of no stored PDF or HTML file")
    return originals, listed, problems


def write_block(licences_dir, originals, tool):
    """Rewrite the README's second block from the renderings on disk, adding
    the section at the end of the file when it is not there yet."""
    readme = licences_dir / "README.md"
    text = readme.read_bytes().decode("utf-8").replace("\r\n", "\n")
    rows = "\n".join(f"{_sha(licences_dir / (n + '.txt'))}  {n}.txt" for n in originals
                     if (licences_dir / (n + ".txt")).is_file())
    section = (
        f"{RENDERINGS_HEAD}\n\n"
        "A rendering is the plain text of a stored PDF or HTML file, `<name>.txt`\n"
        "beside `<name>`, made by `scripts/licence_renderings.py`. The stored files\n"
        "above are unaltered and their hashes unchanged; a rendering is a second\n"
        "file, here so that a quoted sentence can be checked against the same\n"
        "characters on every machine (`scripts/commercial_use_quote_check.py`).\n"
        f"PDFs: `{tool}`, `-enc UTF-8`. HTML: Python's `html.parser`, tags removed,\n"
        "entities decoded, script and style dropped. Recompute from the COMMITTED\n"
        "file, as above. `python scripts/check_provenance.py` and\n"
        "`python scripts/licence_renderings.py` verify every hash here.\n\n"
        f"```\n{rows}\n```\n")
    start = text.find(RENDERINGS_HEAD)
    if start == -1:
        new = text.rstrip("\n") + "\n\n" + section
    else:
        end = text.find("```\n", text.find("```\n", start) + 4) + 4
        new = text[:start] + section + text[end:]
    readme.write_bytes(new.encode("utf-8"))


def run(licences_dir, write=False, pdf_renderer=render_pdf, tool=None):
    originals, listed, problems = state(licences_dir)
    if not originals and problems:
        for p in problems:
            print(p)
        return 1
    if write:
        made, failed = [], []
        for name in originals:
            rendering = licences_dir / (name + ".txt")
            if rendering.exists():
                continue
            text, why = render(licences_dir / name, pdf_renderer)
            if text is None:
                failed.append(f"{name}: not rendered ({why})")
            elif not text.strip():
                failed.append(f"{name}: yields no text (a scan with no text layer?); not rendered")
            else:
                rendering.write_bytes(text.encode("utf-8"))
                made.append(rendering.name)
        write_block(licences_dir, originals, tool or pdftotext_version() or "pdftotext (not installed)")
        for name in made:
            print(f"wrote {name}")
        for line in failed:
            print(line)
        originals, listed, problems = state(licences_dir)
    for p in problems:
        print(p)
    if problems:
        print(f"\n{len(problems)} problem(s) across {len(originals)} stored PDF and HTML file(s).")
        return 1
    print(f"OK - {len(originals)} stored PDF and HTML file(s), each with its text "
          f"rendering and the rendering's hash as listed.")
    return 0


def main(argv=None, licences_dir=LICENCES):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true",
                    help="write the renderings that are missing and the README's second block")
    args = ap.parse_args(argv)
    return run(licences_dir, write=args.write)


def selftest():
    import contextlib
    import io

    tmp = Path(tempfile.mkdtemp(prefix="licence_renderings_"))
    ok = total = 0

    def report(label, good, got=""):
        nonlocal ok, total
        total += 1
        ok += bool(good)
        print(f"  {'ok ' if good else 'BAD'} {label}" + (f": {got}" if got else ""))

    def fresh(files):
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        for name, data in files.items():
            (tmp / name).write_bytes(data)
        rows = "\n".join(f"{hashlib.sha256(d).hexdigest()}  {n}" for n, d in sorted(files.items()))
        (tmp / "README.md").write_bytes(
            f"# Stored texts\n\n{ORIGINALS_HEAD}\n\n```\n{rows}\n```\n".encode("utf-8"))

    def go(write=False, pdf_renderer=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = run(tmp, write=write, tool="pdftotext version 0.00 [selftest]",
                     pdf_renderer=pdf_renderer or (lambda p: ("Page one text.\n", None)))
        return rc, out.getvalue()

    page = (b"<html><head><title>T</title><style>p{color:red}</style></head><body>"
            b"<script>var hidden = 1;</script>"
            b"<h1>Terms</h1><p>You may use the data for <b>commercial</b> purposes&nbsp;&amp; "
            b"must credit the &ldquo;City&rdquo;.</p><p>Second   paragraph.</p></body></html>")
    try:
        text, _ = render_html(page)
        report("an HTML rendering keeps the text across tags and decodes entities",
               "You may use the data for commercial purposes & must credit the \u201cCity\u201d." in text,
               text.replace("\n", " | "))
        report("script, style and head are dropped, and a block ends its line",
               "hidden" not in text and "color" not in text and text.splitlines()[0] == "Terms"
               and "Second paragraph." in text.splitlines(), text.replace("\n", " | "))
        report("a rendering ends with one newline and holds no carriage return or tab",
               text.endswith(".\n") and not text.endswith("\n\n") and "\r" not in text and "\t" not in text)
        bad, why = render_html(b"\xff\xfe<p>x</p>")
        report("an HTML file that is not UTF-8 is not rendered by guess",
               bad is None and "UTF-8" in why)

        fresh({"a.html": page, "b.pdf": b"%PDF", "c.txt": b"plain terms"})
        rc, out = go()
        report("a stored PDF or HTML file with no rendering fails the check, a .txt does not",
               rc != 0 and "a.html: no rendering" in out and "b.pdf: no rendering" in out
               and "c.txt" not in out, f"exit {rc}")
        before = {p.name: p.read_bytes() for p in tmp.iterdir()}
        go()
        report("the check changes no file",
               before == {p.name: p.read_bytes() for p in tmp.iterdir()})
        originals = {n: (tmp / n).read_bytes() for n in ("a.html", "b.pdf", "c.txt")}
        rc, out = go(write=True)
        readme = (tmp / "README.md").read_bytes().decode("utf-8")
        report("--write makes each rendering, lists its hash and names the tool",
               rc == 0 and (tmp / "a.html.txt").is_file() and (tmp / "b.pdf.txt").is_file()
               and RENDERINGS_HEAD in readme and "pdftotext version 0.00 [selftest]" in readme
               and hashlib.sha256((tmp / "a.html.txt").read_bytes()).hexdigest() in readme,
               f"exit {rc}")
        report("--write leaves every stored file and the first block as they were",
               all((tmp / n).read_bytes() == d for n, d in originals.items())
               and read_block(readme, ORIGINALS_HEAD) == {
                   n: hashlib.sha256(d).hexdigest() for n, d in originals.items()})
        rc, out = go()
        report("after --write the check passes", rc == 0 and "OK - 2 stored" in out, f"exit {rc}")
        kept = (tmp / "b.pdf.txt").read_bytes()
        rc, out = go(write=True, pdf_renderer=lambda p: ("Another machine's text.\n", None))
        report("a second --write never replaces a rendering that exists",
               rc == 0 and (tmp / "b.pdf.txt").read_bytes() == kept, f"exit {rc}")
        (tmp / "a.html.txt").write_bytes(b"edited by hand\n")
        rc, out = go()
        report("an edited rendering fails the check and is named",
               rc != 0 and "a.html.txt: its bytes do not match" in out, f"exit {rc}")
        (tmp / "a.html.txt").unlink()
        rc, out = go()
        report("a rendering listed but gone fails the check",
               rc != 0 and "a.html.txt: listed as a rendering but the file is gone" in out, f"exit {rc}")

        fresh({"scan.pdf": b"%PDF"})
        rc, out = go(write=True, pdf_renderer=lambda p: ("  \n", None))
        report("a PDF that yields no text gets no rendering and the run fails",
               rc != 0 and not (tmp / "scan.pdf.txt").exists() and "yields no text" in out, f"exit {rc}")
        rc, out = go(write=True, pdf_renderer=lambda p: (None, "pdftotext is not installed"))
        report("a machine with no pdftotext writes no PDF rendering and says why",
               rc != 0 and not (tmp / "scan.pdf.txt").exists() and "pdftotext is not installed" in out,
               f"exit {rc}")
        (tmp / "README.md").write_bytes(b"# no block here\n")
        rc, out = go()
        report("a README with no first block fails and names it",
               rc != 0 and ORIGINALS_HEAD in out, f"exit {rc}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
