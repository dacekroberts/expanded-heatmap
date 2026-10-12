"""Commercial use: every verdict in a licence first pass rests on a sentence
that really occurs in the stored licence text. A quote that is not there voids
its verdict.

    python scripts/commercial_use_quote_check.py VERDICTS_JSON
    python scripts/commercial_use_quote_check.py --selftest

VERDICTS_JSON is a JSON list, one object per source, with keys source,
document (a file under docs/licenses/), verdict, quote and clause. A verdict
of SILENT or NOT_READ carries no quote and is reported HELD, never checked.
PERMITTED, PERMITTED_CONDITION and FORBIDDEN need a quote of at least
MIN_QUOTE letters or digits and a clause heading; a shorter or missing quote,
or a missing clause, is VOID, since one word such as "License" occurs in
every text and a rule of hyphens in most, and neither proves anything. The
source values are the ids that scripts/commercial_use_sources.py prints: each
row needs one, and two rows on one source are VOID, both of them (case and
the amount of white space do not make a second source). A row of the wrong
shape is VOID with its reason; it never ends the run.

WHAT IS PROVED, AND WHAT IS NOT. The script proves that the quoted passage is
in the file. It does not read what the passage means: "the data be used for
commercial purposes" is in a sentence that begins "Under no circumstances
may". So every VERIFIED row prints the quote inside its whole sentence, back
to where the sentence starts and on to where it ends (at most CONTEXT_CAP
characters a side, and a side cut there says so), with the file that was read
and the clause heading the first pass gave, and a person reads them. No list
of negation words is kept: the reader decides.

Normalisation, and nothing else: Unicode NFC, then each run of whitespace
collapses to one space; failing that, and only for a quote holding Han, kana
or Hangul, NFC with all whitespace removed from both sides, because pdftotext
puts a space where a PDF wraps a line inside a Japanese or Chinese sentence.
The exact quote is tried first, so a row is VERIFIED as "exact", "normalised"
or "spaceless"; no case folding, no punctuation stripping, no fuzzy matching.
A "spaceless" match is read by a person before it is relied on: its context
is cut from the text as stored, so the break the match stepped over shows,
and the totals count such rows on their own line.

Text renderings: a stored PDF or HTML file is read through its rendering,
<name>.txt beside it, when docs/licenses/README.md lists one in its second
block (scripts/licence_renderings.py makes and hashes them), and the row says
so. A rendering holds the same characters on every machine and is what the
first pass is given, so a quote no longer fails on an HTML tag or entity or
on another pdftotext's line breaks. With no rendering listed, an .html file
is matched against its text as stored, tags included, and a .pdf through
pdftotext or pypdf. A quote across a wrapped line of a markdown blockquote
is still VOID (the marker sits inside it): the first pass copies characters
exactly and quotes within one line of such a file.

Word boundaries: where a quote begins or ends with a letter or digit of a
script written with spaces, the character directly outside it must not be a
letter or digit, nor a hyphen or apostrophe joining one. "use is permitted"
is not in "Misuse is permitted", and "commercial use is permitted" is not in
"Non-commercial use is permitted". Han, kana and Hangul have no such test.

Documents: only a stored text listed in the SHA-256 block of
docs/licenses/README.md (the files scripts/check_provenance.py hashes) can
carry a quote. A file in the folder that is off that list, a project note
among them, is VOID; so is a name off the list that links to a listed file,
and a rendering named as the document. A document under docs/data_sources/ is a recorded read,
not a stored text: NOT CHECKED, for a person to confirm.

Outcomes, one line per source: VERIFIED (exact, normalised or spaceless),
VOID with why, HELD, or NOT CHECKED with why. .txt, .md and .html files are
decoded as UTF-8 and a decode failure is NOT CHECKED, never a guessed
encoding. A .pdf is read with pdftotext or pypdf when either is available,
else NOT CHECKED. A document that yields no text at all (a scanned PDF) is NOT
CHECKED, not VOID: nothing was compared. NOT CHECKED rows are said in the
totals and never count as verified.

The exit code is non-zero when any row is VOID, when the input cannot be read,
is not the described shape or holds no row, when the hash list cannot be
read, and when no row was VERIFIED or HELD while at least one was NOT CHECKED
(nothing was checked, which is not a pass).
"""
import argparse
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LICENCES = ROOT / "docs" / "licenses"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VERDICTS = {"PERMITTED", "PERMITTED_CONDITION", "FORBIDDEN", "SILENT", "NOT_READ"}
HELD = {"SILENT", "NOT_READ"}
OUTCOMES = ("VERIFIED", "VOID", "HELD", "NOT CHECKED")
_WS_RE = re.compile(r"\s+")
# Letters and digits, in any script. Twelve is a short clause in Japanese or
# Korean and two or three words in a Latin script: enough that a match is a
# passage of the text, not a word of it. Punctuation does not count: a rule
# of twelve hyphens is in many texts and proves nothing.
MIN_QUOTE = 12
# The context of a verified quote runs back to the start of its sentence
# and on to its end, never less than CONTEXT characters a side and never
# more than CONTEXT_CAP; a side cut at the cap says so.
CONTEXT = 60
CONTEXT_CAP = 400
RENDERINGS_HEAD = "## SHA-256 of the text renderings"
# Where a sentence ends: a full stop, question or exclamation mark (with
# any closing quote or bracket) before white space, their CJK forms, or a
# blank line.
_SENTENCE_END = re.compile(r"[.!?][\"')\]\u201d\u2019]*\s|[\u3002\uff01\uff1f]|\n\s*\n")
# Files in docs/licenses/ written by the project, never a publisher's terms.
# None is in the hash list today; named so that listing one changes nothing.
PROJECT_NOTES = {"README.md", "canada-privacy-regimes-note.md",
                 "canada-required-notices.md", "france-required-notices.md"}
RECORDED_READS = ("docs", "data_sources")
# Marks that join two words into one when a letter or digit follows.
_JOINERS = "-'’‐‑"
# Han, kana and Hangul: scripts with no space between words.
_UNSPACED = ((0x1100, 0x11FF), (0x3040, 0x30FF), (0x3130, 0x318F),
             (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xAC00, 0xD7AF),
             (0xF900, 0xFAFF), (0xFF66, 0xFF9F), (0x20000, 0x2FA1F))


def normalise(text):
    """NFC, then each run of whitespace collapses to one space."""
    return _WS_RE.sub(" ", unicodedata.normalize("NFC", text))


def _unspaced(ch):
    code = ord(ch)
    return any(lo <= code <= hi for lo, hi in _UNSPACED)


def _wordish(ch):
    """A letter or digit of a script that writes spaces between words."""
    return ch.isalnum() and not _unspaced(ch)


def _joined(text, i, step):
    """True when text[i], the character directly outside a quote, continues
    a word: a letter or digit, or a joiner with a letter or digit beyond it."""
    if not 0 <= i < len(text):
        return False
    if _wordish(text[i]):
        return True
    j = i + step
    return text[i] in _JOINERS and 0 <= j < len(text) and _wordish(text[j])


def _find(quote, text):
    """(start, found): the first place quote sits in text on word boundaries,
    or (None, found) where found says whether it occurs at all."""
    found = False
    start = text.find(quote)
    while start != -1:
        found = True
        end = start + len(quote)
        cut_before = _wordish(quote[0]) and _joined(text, start - 1, -1)
        cut_after = _wordish(quote[-1]) and _joined(text, end, 1)
        if not cut_before and not cut_after:
            return start, True
        start = text.find(quote, start + 1)
    return None, found


def _context(text, start, length):
    """The quote in double square brackets inside its whole sentence. A
    negation can open a sentence a long way before the words quoted, so the
    context runs back to where the sentence starts and on to where it ends:
    at least CONTEXT characters a side (a full stop after an abbreviation is
    no sentence end), at most CONTEXT_CAP, and a side cut at the cap is
    marked so the reader knows to open the document."""
    end = start + length
    window = text[max(0, start - CONTEXT_CAP):start]
    ends = [m.end() for m in _SENTENCE_END.finditer(window)]
    if ends:
        cut = min(ends[-1], max(0, len(window) - CONTEXT))
        before, lead = window[cut:], "..."
    elif start > CONTEXT_CAP:
        before, lead = window, f"[sentence starts more than {CONTEXT_CAP} characters back] ..."
    else:
        before, lead = window, ""
    ahead = text[end:end + CONTEXT_CAP]
    m = _SENTENCE_END.search(ahead)
    if m:
        after, tail = ahead[:max(m.end(), min(CONTEXT, len(ahead)))], "..."
    elif len(text) - end > CONTEXT_CAP:
        after, tail = ahead, f"... [sentence runs on more than {CONTEXT_CAP} characters]"
    else:
        after, tail = ahead, ""
    squeeze = lambda part: _WS_RE.sub(" ", part)
    return (f"{lead}{squeeze(before).lstrip()}[[{squeeze(text[start:end])}]]"
            f"{squeeze(after).rstrip()}{tail}")


def match_quote(quote, text):
    """(kind, context) where kind is "exact", "normalised" or "spaceless", or
    (None, why) when the quote is absent or sits only inside longer words."""
    tiers = [("exact", quote, text),
             ("normalised", normalise(quote), normalise(text))]
    inside_word = False
    for kind, needle, haystack in tiers:
        if not needle:
            continue
        start, found = _find(needle, haystack)
        if start is not None:
            return kind, _context(haystack, start, len(needle))
        inside_word = inside_word or found
    if any(_unspaced(ch) for ch in quote):
        # Matched with whitespace removed, shown with it: the context is cut
        # from the text as stored, so the break the match stepped over (a
        # line wrap, a page end) is there for the reader to see.
        stored = unicodedata.normalize("NFC", text)
        kept = [i for i, ch in enumerate(stored) if not ch.isspace()]
        needle = "".join(ch for ch in unicodedata.normalize("NFC", quote)
                         if not ch.isspace())
        start, found = _find(needle, "".join(stored[i] for i in kept))
        if start is not None:
            first, last = kept[start], kept[start + len(needle) - 1]
            return "spaceless", _context(stored, first, last - first + 1)
        inside_word = inside_word or found
    if inside_word:
        return None, "the quote occurs only as part of longer words, not on word boundaries"
    return None, "the quote does not occur in the document"


def _within(path, folder):
    """True when path names a place under folder (case-insensitive on Windows)."""
    try:
        Path(os.path.normcase(str(path))).relative_to(Path(os.path.normcase(str(folder))))
        return True
    except ValueError:
        return False


def allowed_documents(licences_dir):
    """(names, None): the stored texts the README's SHA-256 block lists, less
    the project's own notes. (None, why) when the block cannot be read."""
    readme = licences_dir / "README.md"
    try:
        text = readme.read_bytes().decode("utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError) as exc:
        return None, f"cannot read {readme}: {exc}"
    m = re.search(r"## SHA-256, as retrieved.*?```\n(.*?)```", text, re.S)
    if not m:
        return None, (f"{readme}: no '## SHA-256, as retrieved' block, so no "
                      f"document can be told from a note; restore the block")
    names = set()
    for line in m.group(1).strip().split("\n"):
        parts = line.split()
        if len(parts) == 2:
            names.add(parts[1])
    return names - PROJECT_NOTES, None


def renderings(licences_dir):
    """Names of the text renderings the README's second block lists
    (scripts/licence_renderings.py): <file>.txt beside a stored PDF or HTML
    file. Empty when the block is not there."""
    try:
        text = (licences_dir / "README.md").read_bytes().decode("utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return set()
    m = re.search(re.escape(RENDERINGS_HEAD) + r".*?```\n(.*?)```", text, re.S)
    if not m:
        return set()
    return {parts[1] for parts in (line.split() for line in m.group(1).strip().split("\n"))
            if len(parts) == 2}


def resolve_document(document, licences_dir, root):
    """Resolve one document field to a file inside licences_dir, or (None, why).

    A relative path resolves against root; an absolute path is used as given.
    Anything that escapes licences_dir (a parent reference, an absolute path
    elsewhere, a symlink out) is refused, as is a path that names no file.
    """
    path = Path(document)
    if not path.is_absolute():
        path = root / path
    try:
        resolved = path.resolve()
    except OSError as exc:
        return None, f"cannot resolve {document}: {exc}"
    if not _within(resolved, licences_dir.resolve()):
        return None, f"{document} escapes the licence folder"
    if not resolved.is_file():
        return None, f"{document} is not a file under the licence folder"
    return resolved, None


def _recorded_read(document, root):
    """True when document names a place under docs/data_sources/."""
    path = Path(document)
    if not path.is_absolute():
        path = root / path
    try:
        resolved = path.resolve()
    except OSError:
        return False
    return _within(resolved, root.joinpath(*RECORDED_READS).resolve())


def _stderr(proc):
    return proc.stderr.decode("utf-8", errors="replace").strip()[:200]


def read_pdf(path):
    """(text, None) or (None, why): pdftotext first, else pypdf, else not checked."""
    if shutil.which("pdftotext"):
        proc = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"],
                              capture_output=True)
        if proc.returncode == 0:
            try:
                return proc.stdout.decode("utf-8"), None
            except UnicodeDecodeError:
                return None, "PDF: pdftotext output is not UTF-8"
        detail = _stderr(proc)
        return None, (f"PDF: pdftotext failed ({detail})" if detail
                      else f"PDF: pdftotext failed (exit {proc.returncode})")
    try:
        import pypdf
    except ImportError:
        return None, "PDF: neither pdftotext nor pypdf is available"
    try:
        reader = pypdf.PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages), None
    except Exception as exc:
        return None, f"PDF: pypdf failed ({exc})"


def read_document(path, pdf_reader=read_pdf):
    """(text, None) or (None, why) for one stored licence file."""
    suffix = path.suffix.lower()
    if suffix in (".txt", ".md", ".html"):
        try:
            data = path.read_bytes()
        except OSError as exc:
            return None, f"cannot read {path.name}: {exc}"
        try:
            return data.decode("utf-8"), None
        except UnicodeDecodeError:
            return None, "not UTF-8 text, and no other encoding is guessed"
    if suffix == ".pdf":
        return pdf_reader(path)
    return None, f"extension {suffix or '(none)'} is not read (.txt, .md, .html, .pdf)"


def check_row(row, licences_dir=LICENCES, root=ROOT, allowed=None, pdf_reader=read_pdf):
    """One row to (outcome, detail, context, read): VERIFIED with exact,
    normalised or spaceless, the quote's sentence, and the file that was
    read; VOID with why; HELD; or NOT CHECKED with why. context and read
    are empty unless VERIFIED."""
    verdict = row.get("verdict")
    if not isinstance(verdict, str) or verdict not in VERDICTS:
        return "VOID", f"unknown verdict {verdict!r} (expected one of {sorted(VERDICTS)})", "", ""
    if verdict in HELD:
        return "HELD", "", "", ""
    quote = row.get("quote")
    if not isinstance(quote, str) or not quote.strip():
        return "VOID", f"{verdict} needs a non-empty quote", "", ""
    if sum(ch.isalnum() for ch in quote) < MIN_QUOTE:
        return "VOID", (f"the quote holds under {MIN_QUOTE} letters or digits, "
                        f"too short to prove a passage"), "", ""
    clause = row.get("clause")
    if not isinstance(clause, str) or not clause.strip():
        return "VOID", f"{verdict} needs the heading of the clause the quote sits under", "", ""
    document = row.get("document")
    if not isinstance(document, str) or not document.strip():
        return "VOID", "no document", "", ""
    if _recorded_read(document, root):
        return "NOT CHECKED", "a recorded read, not a stored text", "", ""
    path, why = resolve_document(document, licences_dir, root)
    if path is None:
        return "VOID", why, "", ""
    if allowed is None:
        allowed, why = allowed_documents(licences_dir)
        if allowed is None:
            return "VOID", why, "", ""
    # The name the row gives must itself be on the list, as well as the file
    # it resolves to: a link named alias.txt to a listed file is not a
    # stored text, whatever it points at.
    own_name = Path(document).name
    if (own_name not in allowed or path.name not in allowed
            or path.parent != licences_dir.resolve()):
        return "VOID", (f"{document} is not a stored licence text (not in the "
                        f"SHA-256 list of the licence folder's README.md)"), "", ""
    # A stored PDF or HTML file is read through its text rendering when the
    # README lists one: the same characters on every machine, and the ones
    # the first pass was given.
    rendering = licences_dir / (path.name + ".txt")
    read = path.name
    if rendering.name in renderings(licences_dir) and rendering.is_file():
        try:
            text, why = rendering.read_bytes().decode("utf-8"), None
        except (OSError, UnicodeDecodeError) as exc:
            text, why = None, f"cannot read the rendering {rendering.name}: {exc}"
        read = f"{path.name}, read as its text rendering {rendering.name}"
    else:
        text, why = read_document(path, pdf_reader)
    if text is None:
        return "NOT CHECKED", why, "", ""
    if not text.strip():
        return "NOT CHECKED", "the document yields no text (a scan with no text layer?)", "", ""
    kind, detail = match_quote(quote.strip(), text)
    if kind is None:
        return "VOID", detail, "", ""
    return "VERIFIED", kind, detail, read


def main(argv=None, licences_dir=LICENCES, root=ROOT, pdf_reader=read_pdf):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("json_file")
    args = ap.parse_args(argv)
    path = Path(args.json_file)
    try:
        rows = json.loads(path.read_bytes().decode("utf-8"))
    except OSError as exc:
        print(f"cannot read {args.json_file}: {exc}")
        return 1
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"cannot read {args.json_file}: {exc}")
        return 1
    if not isinstance(rows, list):
        print(f"{args.json_file}: the file must hold a JSON list, one object per source")
        return 1
    if not rows:
        print(f"{args.json_file}: the list holds no row, so nothing was checked")
        return 1
    allowed, why = allowed_documents(licences_dir)
    if allowed is None:
        print(why)
        return 1
    def fold(source):
        """A source's name for telling two rows apart: case and the amount
        of white space do not make a second source."""
        return " ".join(source.split()).casefold()

    seen = Counter(fold(row["source"]) for row in rows
                   if isinstance(row, dict) and isinstance(row.get("source"), str))
    counts = {k: 0 for k in OUTCOMES}
    spaceless = 0
    for i, row in enumerate(rows):
        context = read = ""
        if not isinstance(row, dict):
            label, outcome, detail = f"row {i + 1}", "VOID", "not a JSON object"
        else:
            source = row.get("source")
            if not isinstance(source, str) or not source.strip():
                label, outcome, detail = f"row {i + 1}", "VOID", "no source"
            elif seen[fold(source)] > 1:
                label, outcome = source.strip(), "VOID"
                detail = (f"the source has {seen[fold(source)]} rows in the "
                          f"file; one row per source")
            else:
                label = source.strip()
                try:
                    outcome, detail, context, read = check_row(
                        row, licences_dir, root, allowed, pdf_reader)
                except Exception as exc:
                    # A row of the wrong shape voids itself; it never ends
                    # the run and takes the other rows' verdicts with it.
                    outcome, detail = "VOID", f"malformed row: {type(exc).__name__}: {exc}"
        counts[outcome] += 1
        print(f"{outcome:<11} {label}" + (f": {detail}" if detail else ""))
        if outcome == "VERIFIED":
            spaceless += detail == "spaceless"
            print(f"{'':<11} document: {read}")
            print(f"{'':<11} clause: {_WS_RE.sub(' ', row['clause'].strip())}")
            print(f"{'':<11} context: {context}")
    print(f"\n{counts['VERIFIED']} VERIFIED, {counts['VOID']} VOID, "
          f"{counts['HELD']} HELD, {counts['NOT CHECKED']} NOT CHECKED")
    if spaceless:
        print(f"{spaceless} of the VERIFIED matched only with white space removed "
              f"(spaceless): read each one's context before relying on it")
    compared = counts["VERIFIED"] + counts["VOID"]
    print(f"{compared} of {len(rows)} rows were checked: a quote was looked for, "
          f"or the row was refused; the rest were held or could not be read")
    if counts["VOID"]:
        return 1
    if counts["NOT CHECKED"] and not counts["VERIFIED"] and not counts["HELD"]:
        print("Nothing was checked: every row is NOT CHECKED. Install pdftotext "
              "or pypdf, or name stored texts, and run again.")
        return 1
    return 0


def selftest():
    tmp = Path(tempfile.mkdtemp(prefix="commercial_use_quote_check_"))
    lic = tmp / "docs" / "licenses"
    lic.mkdir(parents=True)
    (tmp / "docs" / "data_sources").mkdir()
    ok = total = 0

    def report(label, good, got):
        nonlocal ok, total
        total += 1
        ok += bool(good)
        print(f"  {'ok ' if good else 'BAD'} {label}: {got}")

    try:
        stored = {
            "a.txt": b"The terms allow commercial use outright.",
            "split.txt": b"the sentence\nsplit across lines",
            "ja.txt": "営業許可の取得が必要です。".encode("utf-8"),
            "ko.txt": "영업허가를 반드시 받아야 합니다.".encode("utf-8"),
            "far.txt": (b"Under no circumstances may a licensee, its officers, employees, "
                        b"agents, contractors or any third party acting directly or indirectly "
                        b"on its behalf, whether or not authorised in writing, the data be "
                        b"used for commercial purposes. A second sentence follows it."),
            "rule.txt": b"Terms of use\n------------------------\nThe body of the terms.",
            "page.html": (b"<p>You may use the data for <b>commercial</b> purposes&nbsp;&amp; "
                          b"must give credit.</p>"),
            "pages.txt": ("第三条 個人情報の目\n\n的外利用や外部提供は禁止されている。".encode("utf-8")),
            "case.txt": b"Mixed Case Sentence",
            "notutf8.txt": b"\xff\xfe\x00\x01",
            "weird.bin": b"anything",
            "empty.txt": b" \n",
            "wrap.txt": "個人情報の目 的外利用や外部提供は禁止されている".encode("utf-8"),
            "misuse.txt": b"Misuse is permitted by no clause of these terms.",
            "noncom.txt": b"Non-commercial use is permitted without charge.",
            "notfor.txt": b"Note: is not for commercial use at all.",
            "users.txt": b"Reuse is permitted for commercial users only.",
            "never.txt": b"Under no circumstances may the data be used for commercial purposes.",
            "terms.pdf": b"%PDF-1.4 not a real PDF; the reader is injected",
        }
        for name, data in stored.items():
            (lic / name).write_bytes(data)
        listing = "\n".join(f"{'0' * 64}  {name}" for name in sorted(stored))
        readme = (f"# Stored texts\n\n## SHA-256, as retrieved\n\n```\n{listing}\n```\n\n"
                  f"{RENDERINGS_HEAD}\n\n```\n{'0' * 64}  page.html.txt\n```\n")
        (lic / "README.md").write_bytes(readme.encode("utf-8"))
        # The rendering of page.html, as scripts/licence_renderings.py makes it.
        (lic / "page.html.txt").write_bytes(
            b"You may use the data for commercial purposes & must give credit.\n")
        # Real files holding the quote, so only the rule named can decide.
        (tmp / "docs" / "outside.txt").write_bytes(b"outside the folder")
        (lic / "unlisted.txt").write_bytes(b"The terms allow commercial use outright.")
        (tmp / "docs" / "data_sources" / "country.md").write_bytes(
            b"The terms allow commercial use outright.")

        def row(source, document, verdict, quote, clause="Grant"):
            return {"source": source, "document": document, "verdict": verdict,
                    "quote": quote, "clause": clause}

        cases = [
            ("an exact quote verifies", row("a", "docs/licenses/a.txt", "PERMITTED",
                                            "allow commercial use"), "VERIFIED", "exact"),
            ("a quote split across a line break", row("b", "docs/licenses/split.txt",
                                                      "PERMITTED", "the sentence split"),
             "VERIFIED", "normalised"),
            ("a quote with one changed word voids", row("c", "docs/licenses/a.txt",
                                                        "PERMITTED", "allow commercial xyz"),
             "VOID", None),
            ("a Japanese quote verifies", row("d", "docs/licenses/ja.txt", "PERMITTED",
                                              "営業許可の取得が必要です。"), "VERIFIED", "exact"),
            ("a Korean quote verifies", row("e", "docs/licenses/ko.txt", "PERMITTED",
                                            "영업허가를 반드시 받아야 합니다."), "VERIFIED", "exact"),
            ("a quote of one word voids, though it occurs", row("p", "docs/licenses/a.txt",
                                                                "PERMITTED", "commercial"),
             "VOID", None),
            ("a Japanese quote across a PDF line wrap", row("q", "docs/licenses/wrap.txt",
                                                            "FORBIDDEN", "目的外利用や外部提供は禁止"),
             "VERIFIED", "spaceless"),
            ("a document with no text is not checked", row("r", "docs/licenses/empty.txt",
                                                           "PERMITTED", "allow commercial use"),
             "NOT CHECKED", None),
            ("a document outside the licence folder voids", row("f", "docs/licenses/../outside.txt",
                                                                "PERMITTED", "outside the folder"),
             "VOID", None),
            ("a PERMITTED row with an empty quote voids", row("g", "docs/licenses/a.txt",
                                                              "PERMITTED", ""), "VOID", None),
            ("a SILENT row is held", row("h", "docs/licenses/a.txt", "SILENT", ""), "HELD", None),
            ("a NOT READ row is held", row("i", "docs/licenses/a.txt", "NOT_READ", ""), "HELD", None),
            ("case differs only, voids", row("j", "docs/licenses/case.txt", "PERMITTED",
                                             "mixed case sentence"), "VOID", None),
            ("an unknown verdict voids", row("k", "docs/licenses/a.txt", "MAYBE",
                                             "allow commercial use"), "VOID", None),
            ("punctuation differs only, voids", row("o", "docs/licenses/a.txt", "PERMITTED",
                                                    "terms, allow commercial use"),
             "VOID", None),
            ("a document that does not exist voids", row("l", "docs/licenses/none.txt",
                                                         "PERMITTED", "allow commercial use"),
             "VOID", None),
            ("non-UTF-8 text is not checked", row("m", "docs/licenses/notutf8.txt",
                                                  "PERMITTED", "allow commercial use"),
             "NOT CHECKED", None),
            ("an unknown extension is not checked", row("n", "docs/licenses/weird.bin",
                                                        "PERMITTED", "allow commercial use"),
             "NOT CHECKED", None),
            ("a quote cut out of a longer word voids", row("s", "docs/licenses/misuse.txt",
                                                           "PERMITTED", "use is permitted by"),
             "VOID", None),
            ("a quote cut after a joining hyphen voids", row("t", "docs/licenses/noncom.txt",
                                                             "PERMITTED",
                                                             "commercial use is permitted"),
             "VOID", None),
            ("a Latin quote never matches with spaces removed", row(
                "u", "docs/licenses/notfor.txt", "PERMITTED",
                "is no tfor commercial use at all."), "VOID", None),
            ("a quote that stops inside a longer word voids", row(
                "z", "docs/licenses/users.txt", "PERMITTED",
                "is permitted for commercial use"), "VOID", None),
            ("a file off the hash list voids, though it holds the quote", row(
                "v", "docs/licenses/unlisted.txt", "PERMITTED", "allow commercial use"),
             "VOID", None),
            ("a quoted verdict with no clause voids", row(
                "w", "docs/licenses/a.txt", "PERMITTED", "allow commercial use", clause=" "),
             "VOID", None),
            ("a recorded read is not checked", row(
                "x", "docs/data_sources/country.md", "PERMITTED", "allow commercial use"),
             "NOT CHECKED", None),
        ]
        for label, r, want, want_kind in cases:
            outcome, detail, _, _ = check_row(r, licences_dir=lic, root=tmp)
            good = outcome == want and (want_kind is None or detail == want_kind)
            report(label, good, f"{outcome}" + (f" ({detail})" if detail else ""))

        # The context shows what the quote leaves out.
        outcome, _, context, _ = check_row(
            row("y", "docs/licenses/never.txt", "PERMITTED",
                "the data be used for commercial purposes"), licences_dir=lic, root=tmp)
        report("a verified row prints the words before the quote",
               outcome == "VERIFIED" and "Under no circumstances may" in context, context)

        def run(rows, pdf_reader=read_pdf, name="verdicts.json"):
            path = tmp / name
            path.write_bytes(json.dumps(rows, ensure_ascii=False).encode("utf-8"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = main([str(path)], licences_dir=lic, root=tmp, pdf_reader=pdf_reader)
            return rc, out.getvalue()

        good_row = row("ok", "docs/licenses/a.txt", "PERMITTED", "allow commercial use")
        void_row = row("bad", "docs/licenses/a.txt", "PERMITTED", "allow commercial xyz")
        pdf_row = row("pdf", "docs/licenses/terms.pdf", "PERMITTED", "allow commercial use")

        rc, out = run([good_row])
        report("main: one verified row exits 0 and prints clause and context",
               rc == 0 and "clause: Grant" in out and "[[allow commercial use]]" in out,
               f"exit {rc}")
        rc, out = run([good_row, void_row])
        report("main: a VOID row makes the exit code non-zero",
               rc != 0 and "1 VERIFIED, 1 VOID" in out, f"exit {rc}")
        rc, out = run({"source": "ok"})
        report("main: an input that is not a list is refused by name",
               rc != 0 and "must hold a JSON list" in out, f"exit {rc}")
        rc, out = run([])
        report("main: an empty list is not a pass", rc != 0 and "no row" in out, f"exit {rc}")
        rc, out = run([good_row, dict(good_row)])
        report("main: two rows on one source void both",
               rc != 0 and "0 VERIFIED, 2 VOID" in out, f"exit {rc}")
        rc, out = run([dict(good_row, source="")])
        report("main: a row with no source voids",
               rc != 0 and "no source" in out, f"exit {rc}")
        rc, out = run([pdf_row],
                      pdf_reader=lambda p: ("The terms allow commercial use outright.", None))
        report("main: a PDF is read through the reader and verifies",
               rc == 0 and "1 VERIFIED" in out, f"exit {rc}")
        rc, out = run([pdf_row], pdf_reader=lambda p: (None, "PDF: no reader"))
        report("main: nothing checked at all is not a pass",
               rc != 0 and "Nothing was checked" in out, f"exit {rc}")
        rc, out = run([pdf_row, row("held", "", "SILENT", "")],
                      pdf_reader=lambda p: (None, "PDF: no reader"))
        report("main: a NOT CHECKED row beside a HELD one exits 0",
               rc == 0 and "1 HELD, 1 NOT CHECKED" in out, f"exit {rc}")
        # Found by an adversarial review (2026-10-12): each is a way a wrong
        # verdict could verify, or a run could look finer than it was.
        outcome, _, context, _ = check_row(
            row("far", "docs/licenses/far.txt", "PERMITTED",
                "the data be used for commercial purposes"), licences_dir=lic, root=tmp)
        report("the context runs back to the start of the sentence, however far",
               outcome == "VERIFIED" and context.startswith("Under no circumstances may"),
               context[:60])
        long_text = "word " * 200 + "the data be used for commercial purposes " + "word " * 200
        (lic / "a.txt").write_bytes(long_text.encode("utf-8"))
        outcome, _, context, _ = check_row(
            row("cap", "docs/licenses/a.txt", "PERMITTED",
                "the data be used for commercial purposes"), licences_dir=lic, root=tmp)
        report("a sentence longer than the cap is cut and says so on both sides",
               outcome == "VERIFIED"
               and context.startswith(f"[sentence starts more than {CONTEXT_CAP} characters back]")
               and context.endswith(f"[sentence runs on more than {CONTEXT_CAP} characters]"),
               f"{len(context)} characters")
        (lic / "a.txt").write_bytes(stored["a.txt"])
        outcome, detail, context, _ = check_row(
            row("pages", "docs/licenses/pages.txt", "FORBIDDEN", "個人情報の目的外利用や外部提供は禁止"),
            licences_dir=lic, root=tmp)
        report("a spaceless match shows the break it stepped over, from the text as stored",
               (outcome, detail) == ("VERIFIED", "spaceless") and "目 的外利用" in context
               and context.startswith("第三条"), context)
        outcome, detail, _, _ = check_row(
            row("rule", "docs/licenses/rule.txt", "PERMITTED", "------------"),
            licences_dir=lic, root=tmp)
        report("twelve hyphens are not a quote", outcome == "VOID" and "letters or digits" in detail,
               detail)
        outcome, detail, _, read = check_row(
            row("page", "docs/licenses/page.html", "PERMITTED_CONDITION",
                "use the data for commercial purposes & must give credit"),
            licences_dir=lic, root=tmp)
        report("an HTML file is read through its listed rendering, across its tags and entities",
               (outcome, detail) == ("VERIFIED", "exact")
               and read == "page.html, read as its text rendering page.html.txt", read)
        outcome, detail, _, _ = check_row(
            row("page2", "docs/licenses/page.html.txt", "PERMITTED", "use the data for commercial"),
            licences_dir=lic, root=tmp)
        report("a rendering named as the document itself is not a stored text",
               outcome == "VOID" and "not a stored licence text" in detail, detail)
        # A .txt that happens to sit beside a stored file is no rendering
        # unless the README lists it: the stored file itself is read.
        (lic / "case.txt.txt").write_bytes(b"an unlisted neighbour says something else entirely")
        outcome, detail, _, _ = check_row(
            row("near", "docs/licenses/case.txt", "PERMITTED", "says something else entirely"),
            licences_dir=lic, root=tmp)
        report("an unlisted .txt beside a stored file is not read as its rendering",
               outcome == "VOID" and "does not occur" in detail, detail)
        (lic / "case.txt.txt").unlink()
        try:
            got = check_row(dict(good_row, verdict=["PERMITTED"]), licences_dir=lic, root=tmp)
        except Exception as exc:
            got = ("RAISED", type(exc).__name__)
        report("a verdict that is not a string is VOID, not an error",
               got[0] == "VOID" and "unknown verdict" in got[1], str(got[:2]))
        alias = lic / "alias.txt"
        try:
            os.symlink(lic / "a.txt", alias)
            linked = True
        except (OSError, NotImplementedError):
            linked = False       # no right to make links here: the name test still runs
            alias.write_bytes(stored["a.txt"])
        outcome, detail, _, _ = check_row(
            row("alias", "docs/licenses/alias.txt", "PERMITTED", "allow commercial use"),
            licences_dir=lic, root=tmp)
        report("a name off the list is refused, a link to a listed file included",
               outcome == "VOID" and "not a stored licence text" in detail,
               "a real link" if linked else "a plain file (links not permitted here)")
        alias.unlink()

        rc, out = run([row("TransLink GTFS", "docs/licenses/a.txt", "PERMITTED", "allow commercial use"),
                       row("translink  gtfs", "docs/licenses/a.txt", "PERMITTED", "allow commercial use")])
        report("main: sources that differ only in case and spacing are one source, both VOID",
               rc != 0 and "0 VERIFIED, 2 VOID" in out, f"exit {rc}")
        rc, out = run([dict(good_row, verdict=["PERMITTED"]), dict(good_row, source="ok2")])
        report("main: a verdict of the wrong type voids its row and the next row is still read",
               rc != 0 and "1 VERIFIED, 1 VOID" in out, f"exit {rc}")
        # An error raised while one row is checked (here a PDF reader that
        # breaks) voids that row; the next row is still read.
        def broken_reader(path):
            raise RuntimeError("the reader broke")

        try:
            rc, out = run([pdf_row, dict(good_row, source="ok3")], pdf_reader=broken_reader)
        except Exception as exc:
            rc, out = "raised", type(exc).__name__
        report("main: a row whose check raises voids itself and never ends the run",
               "1 VERIFIED, 1 VOID" in out and "malformed row" in out, f"exit {rc}")
        rc, out = run([good_row])
        report("main: a verified row names the document it was read from",
               "document: a.txt" in out, f"exit {rc}")
        rc, out = run([row("pages", "docs/licenses/pages.txt", "FORBIDDEN",
                           "個人情報の目的外利用や外部提供は禁止"), good_row])
        report("main: spaceless rows are counted on their own line",
               "1 of the VERIFIED matched only with white space removed" in out, f"exit {rc}")
        rc, out = run([good_row, row("held", "", "SILENT", ""), pdf_row],
                      pdf_reader=lambda p: (None, "PDF: no reader"))
        report("main: the totals say how many rows were checked",
               "1 of 3 rows were checked" in out, f"exit {rc}")

        (lic / "README.md").write_bytes(b"# Stored texts\n\nno hash block here\n")
        rc, out = run([good_row])
        report("main: a README with no hash block fails and names the block",
               rc != 0 and "SHA-256, as retrieved" in out, f"exit {rc}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
