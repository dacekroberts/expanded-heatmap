"""Commercial use: every verdict in a licence first pass rests on a sentence
that really occurs in the stored licence text. A quote that is not there voids
its verdict.

    python scripts/commercial_use_quote_check.py VERDICTS_JSON
    python scripts/commercial_use_quote_check.py --selftest

VERDICTS_JSON is a JSON list, one object per source, with keys source,
document (a file under docs/licenses/), verdict, quote and clause. A verdict
of SILENT or NOT_READ carries no quote and is reported HELD, never checked.
PERMITTED, PERMITTED_CONDITION and FORBIDDEN need a quote of at least
MIN_QUOTE characters other than whitespace; a shorter or missing one is VOID,
since one word such as "License" occurs in every text and proves nothing.

Normalisation, and nothing else: Unicode NFC, then each run of whitespace
collapses to one space; failing that, NFC with all whitespace removed from
both sides, because pdftotext puts a space where a PDF wraps a line inside a
Japanese or Chinese sentence. The exact quote is tried first, so a row is
VERIFIED as "exact", "normalised" or "spaceless"; no case folding, no
punctuation stripping, no fuzzy matching. A "spaceless" match is read by a
person before it is relied on. An .html file is matched against its text as
stored, tags included, so a quote that spans a tag is VOID.

Outcomes, one line per source: VERIFIED (exact or normalised), VOID with why,
HELD, or NOT CHECKED with why. .txt, .md and .html files are decoded as UTF-8
and a decode failure is NOT CHECKED, never a guessed encoding. A .pdf is read
with pdftotext or pypdf when either is available, else NOT CHECKED. The exit
code is non-zero when any row is VOID or the input cannot be read or is not
the described shape; NOT CHECKED rows are said in the totals and never count
as verified. A document that yields no text at all (a scanned PDF) is NOT
CHECKED, not VOID: nothing was compared.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
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


def normalise(text):
    """NFC, then each run of whitespace collapses to one space."""
    return _WS_RE.sub(" ", unicodedata.normalize("NFC", text))


def match_quote(quote, text):
    """Where a quote sits in a text: "exact", "normalised", "spaceless" or
    None when absent."""
    if quote in text:
        return "exact"
    if normalise(quote) in normalise(text):
        return "normalised"
    if normalise(quote).replace(" ", "") in normalise(text).replace(" ", ""):
        return "spaceless"
    return None


def _within(path, folder):
    """True when path names a place under folder (case-insensitive on Windows)."""
    try:
        Path(os.path.normcase(str(path))).relative_to(Path(os.path.normcase(str(folder))))
        return True
    except ValueError:
        return False


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


def read_document(path):
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
        return read_pdf(path)
    return None, f"extension {suffix or '(none)'} is not read (.txt, .md, .html, .pdf)"


def check_row(row, licences_dir=LICENCES, root=ROOT):
    """One row to (outcome, detail): VERIFIED with exact or normalised, VOID
    with why, HELD, or NOT CHECKED with why."""
    verdict = row.get("verdict")
    if verdict not in VERDICTS:
        return "VOID", f"unknown verdict {verdict!r} (expected one of {sorted(VERDICTS)})"
    if verdict in HELD:
        return "HELD", ""
    quote = row.get("quote")
    if not isinstance(quote, str) or not quote.strip():
        return "VOID", f"{verdict} needs a non-empty quote"
    if len(_WS_RE.sub("", quote)) < MIN_QUOTE:
        return "VOID", f"the quote is under {MIN_QUOTE} characters, too short to prove a passage"
    document = row.get("document")
    if not isinstance(document, str) or not document.strip():
        return "VOID", "no document"
    path, why = resolve_document(document, licences_dir, root)
    if path is None:
        return "VOID", why
    text, why = read_document(path)
    if text is None:
        return "NOT CHECKED", why
    if not text.strip():
        return "NOT CHECKED", "the document yields no text (a scan with no text layer?)"
    kind = match_quote(quote, text)
    if kind is None:
        return "VOID", "the quote does not occur in the document"
    return "VERIFIED", kind


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("json_file")
    args = ap.parse_args()
    path = Path(args.json_file)
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"cannot read {args.json_file}: {exc}")
        return 1
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"cannot read {args.json_file}: {exc}")
        return 1
    if not isinstance(rows, list):
        print(f"{args.json_file}: the file must hold a JSON list, one object per source")
        return 1
    counts = {k: 0 for k in OUTCOMES}
    void = False
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            label, outcome, detail = f"row {i + 1}", "VOID", "not a JSON object"
        else:
            label = row.get("source") or row.get("document") or f"row {i + 1}"
            outcome, detail = check_row(row)
        counts[outcome] += 1
        if outcome == "VOID":
            void = True
        print(f"{outcome:<11} {label}" + (f": {detail}" if detail else ""))
    print(f"\n{counts['VERIFIED']} VERIFIED, {counts['VOID']} VOID, "
          f"{counts['HELD']} HELD, {counts['NOT CHECKED']} NOT CHECKED")
    return 1 if void else 0


def selftest():
    tmp = Path(tempfile.mkdtemp(prefix="commercial_use_quote_check_"))
    lic = tmp / "docs" / "licenses"
    lic.mkdir(parents=True)
    try:
        (lic / "a.txt").write_bytes(b"The terms allow commercial use outright.")
        (lic / "split.txt").write_bytes(b"the sentence\nsplit across lines")
        (lic / "ja.txt").write_bytes("営業許可の取得が必要です。".encode("utf-8"))
        (lic / "ko.txt").write_bytes("영업허가를 받아야 합니다.".encode("utf-8"))
        (lic / "case.txt").write_bytes(b"Mixed Case Sentence")
        (lic / "notutf8.txt").write_bytes(b"\xff\xfe\x00\x01")
        (lic / "weird.bin").write_bytes(b"anything")
        (lic / "empty.txt").write_bytes(b" \n")
        (lic / "wrap.txt").write_bytes("個人情報の目 的外利用や外部提供は禁止されている".encode("utf-8"))
        # A real file holding the quote, so only the folder rule can void it.
        (tmp / "docs" / "outside.txt").write_bytes(b"outside the folder")

        def row(source, document, verdict, quote):
            return {"source": source, "document": document, "verdict": verdict,
                    "quote": quote, "clause": ""}

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
        ]
        ok = 0
        for label, r, want, want_kind in cases:
            outcome, detail = check_row(r, licences_dir=lic, root=tmp)
            good = outcome == want and (want_kind is None or detail == want_kind)
            ok += good
            got = f"{outcome}" + (f" ({detail})" if detail else "")
            print(f"  {'ok ' if good else 'BAD'} {label}: {got}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{ok} of {len(cases)} cases behaved as intended.")
    return 0 if ok == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
