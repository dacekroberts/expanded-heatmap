"""Commercial use: every verdict in a licence first pass rests on a sentence
that really occurs in the stored licence text. A quote that is not there voids
its verdict.

    python scripts/commercial_use_quote_check.py VERDICTS_JSON
    python scripts/commercial_use_quote_check.py --selftest

VERDICTS_JSON is a JSON list, one object per source, with keys source,
document (a file under docs/licenses/), verdict, quote and clause. A verdict
of SILENT or NOT_READ carries no quote and is reported HELD, never checked.
PERMITTED, PERMITTED_CONDITION and FORBIDDEN need a quote of at least
MIN_QUOTE characters other than whitespace and a clause heading; a shorter or
missing quote, or a missing clause, is VOID, since one word such as "License"
occurs in every text and proves nothing. The source values are the ids that
scripts/commercial_use_sources.py prints: each row needs one, and two rows on
one source are VOID, both of them.

WHAT IS PROVED, AND WHAT IS NOT. The script proves that the quoted passage is
in the file. It does not read what the passage means: "the data be used for
commercial purposes" is in a sentence that begins "Under no circumstances
may". So every VERIFIED row prints CONTEXT characters of the document either
side of the quote and the clause heading the first pass gave, and a person
reads them. No list of negation words is kept: the reader decides.

Normalisation, and nothing else: Unicode NFC, then each run of whitespace
collapses to one space; failing that, and only for a quote holding Han, kana
or Hangul, NFC with all whitespace removed from both sides, because pdftotext
puts a space where a PDF wraps a line inside a Japanese or Chinese sentence.
The exact quote is tried first, so a row is VERIFIED as "exact", "normalised"
or "spaceless"; no case folding, no punctuation stripping, no fuzzy matching.
A "spaceless" match is read by a person before it is relied on. An .html file
is matched against its text as stored, tags included, so a quote that spans a
tag is VOID; a quote across a wrapped line of a markdown blockquote is VOID
for the same reason (the marker sits inside it). The first pass is told to
copy characters exactly and to quote within one line of such a file.

Word boundaries: where a quote begins or ends with a letter or digit of a
script written with spaces, the character directly outside it must not be a
letter or digit, nor a hyphen or apostrophe joining one. "use is permitted"
is not in "Misuse is permitted", and "commercial use is permitted" is not in
"Non-commercial use is permitted". Han, kana and Hangul have no such test.

Documents: only a stored text listed in the SHA-256 block of
docs/licenses/README.md (the files scripts/check_provenance.py hashes) can
carry a quote. A file in the folder that is off that list, a project note
among them, is VOID. A document under docs/data_sources/ is a recorded read,
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
# Characters other than whitespace. Twelve is a short clause in Japanese or
# Korean and two or three words in a Latin script: enough that a match is a
# passage of the text, not a word of it.
MIN_QUOTE = 12
# Characters of the document printed either side of a verified quote.
CONTEXT = 60
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
    before = _WS_RE.sub(" ", text[max(0, start - CONTEXT):start])
    after = _WS_RE.sub(" ", text[start + length:start + length + CONTEXT])
    middle = _WS_RE.sub(" ", text[start:start + length])
    return f"...{before}[[{middle}]]{after}..."


def match_quote(quote, text):
    """(kind, context) where kind is "exact", "normalised" or "spaceless", or
    (None, why) when the quote is absent or sits only inside longer words."""
    tiers = [("exact", quote, text),
             ("normalised", normalise(quote), normalise(text))]
    if any(_unspaced(ch) for ch in quote):
        tiers.append(("spaceless", normalise(quote).replace(" ", ""),
                      normalise(text).replace(" ", "")))
    inside_word = False
    for kind, needle, haystack in tiers:
        if not needle:
            continue
        start, found = _find(needle, haystack)
        if start is not None:
            return kind, _context(haystack, start, len(needle))
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
    """One row to (outcome, detail, context): VERIFIED with exact, normalised
    or spaceless and the document either side of the quote; VOID with why;
    HELD; or NOT CHECKED with why. context is empty unless VERIFIED."""
    verdict = row.get("verdict")
    if verdict not in VERDICTS:
        return "VOID", f"unknown verdict {verdict!r} (expected one of {sorted(VERDICTS)})", ""
    if verdict in HELD:
        return "HELD", "", ""
    quote = row.get("quote")
    if not isinstance(quote, str) or not quote.strip():
        return "VOID", f"{verdict} needs a non-empty quote", ""
    if len(_WS_RE.sub("", quote)) < MIN_QUOTE:
        return "VOID", f"the quote is under {MIN_QUOTE} characters, too short to prove a passage", ""
    clause = row.get("clause")
    if not isinstance(clause, str) or not clause.strip():
        return "VOID", f"{verdict} needs the heading of the clause the quote sits under", ""
    document = row.get("document")
    if not isinstance(document, str) or not document.strip():
        return "VOID", "no document", ""
    if _recorded_read(document, root):
        return "NOT CHECKED", "a recorded read, not a stored text", ""
    path, why = resolve_document(document, licences_dir, root)
    if path is None:
        return "VOID", why, ""
    if allowed is None:
        allowed, why = allowed_documents(licences_dir)
        if allowed is None:
            return "VOID", why, ""
    if path.name not in allowed or path.parent != licences_dir.resolve():
        return "VOID", (f"{document} is not a stored licence text (not in the "
                        f"SHA-256 list of the licence folder's README.md)"), ""
    text, why = read_document(path, pdf_reader)
    if text is None:
        return "NOT CHECKED", why, ""
    if not text.strip():
        return "NOT CHECKED", "the document yields no text (a scan with no text layer?)", ""
    kind, detail = match_quote(quote.strip(), text)
    if kind is None:
        return "VOID", detail, ""
    return "VERIFIED", kind, detail


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
    seen = Counter(row["source"].strip() for row in rows
                   if isinstance(row, dict) and isinstance(row.get("source"), str))
    counts = {k: 0 for k in OUTCOMES}
    for i, row in enumerate(rows):
        context = ""
        if not isinstance(row, dict):
            label, outcome, detail = f"row {i + 1}", "VOID", "not a JSON object"
        else:
            source = row.get("source")
            if not isinstance(source, str) or not source.strip():
                label, outcome, detail = f"row {i + 1}", "VOID", "no source"
            elif seen[source.strip()] > 1:
                label, outcome = source.strip(), "VOID"
                detail = (f"the source has {seen[source.strip()]} rows in the "
                          f"file; one row per source")
            else:
                label = source.strip()
                outcome, detail, context = check_row(row, licences_dir, root,
                                                     allowed, pdf_reader)
        counts[outcome] += 1
        print(f"{outcome:<11} {label}" + (f": {detail}" if detail else ""))
        if outcome == "VERIFIED":
            print(f"{'':<11} clause: {_WS_RE.sub(' ', row['clause'].strip())}")
            print(f"{'':<11} context: {context}")
    print(f"\n{counts['VERIFIED']} VERIFIED, {counts['VOID']} VOID, "
          f"{counts['HELD']} HELD, {counts['NOT CHECKED']} NOT CHECKED")
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
            "ko.txt": "영업허가를 받아야 합니다.".encode("utf-8"),
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
        readme = f"# Stored texts\n\n## SHA-256, as retrieved\n\n```\n{listing}\n```\n"
        (lic / "README.md").write_bytes(readme.encode("utf-8"))
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
                                            "영업허가를 받아야 합니다."), "VERIFIED", "exact"),
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
            outcome, detail, _ = check_row(r, licences_dir=lic, root=tmp)
            good = outcome == want and (want_kind is None or detail == want_kind)
            report(label, good, f"{outcome}" + (f" ({detail})" if detail else ""))

        # The context shows what the quote leaves out.
        outcome, _, context = check_row(
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
