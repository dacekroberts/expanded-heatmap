"""Georgian (Mkhedruli) name shapes, for the privacy check's Georgian pass.

`scripts/check_personal_exposure.py` reads Latin script only, so on Geostat's
register its zero would not be a finding. Two questions are asked here:

1. Is an individual entrepreneur (legal form 30, a natural person) ever shown
   by name? Step 2 shows the category instead (owner, 2026-10-01), so the
   answer must be zero; the check tests the rule on the processed file.
2. How many COMPANY names read as a person's full name? A Georgian company's
   registered name begins with its legal form (`შპს` for an LLC, `სს` for a
   joint-stock company; measured on 400 rows, 2026-10-02: every company row),
   the organisational marker under which Seattle (Regional) keeps a
   person-like name. This is a heuristic count, reported for the verdict:
   after the legal-form token, exactly two Georgian words, the second ending
   in a common surname suffix.

Mtavruli capitals (U+1C90 to U+1CBF) are folded to Mkhedruli before testing.
"""
import re

LEGAL_FORM_TOKENS = ("შპს", "სს", "კს", "სპს", "ააიპ", "ი/მ", "იმ")
# Common Georgian surname endings, longest first.
SURNAME_SUFFIXES = ("შვილი", "ძე", "ია", "უა", "ავა", "ანი", "ური", "ული", "ელი", "ონი", "ენი")
_GEORGIAN_WORD = re.compile(r"^[ა-ჿ]+$")


def fold(name):
    """Mtavruli to Mkhedruli: each capital sits 0x0BC0 above its lower case."""
    return "".join(chr(ord(c) - 0x0BC0) if 0x1C90 <= ord(c) <= 0x1CBA else c
                   for c in (name or ""))


def strip_legal_form(name):
    words = fold(name).replace('"', " ").replace("„", " ").replace("“", " ").split()
    if words and words[0] in LEGAL_FORM_TOKENS:
        words = words[1:]
    return words


def has_legal_form(name):
    words = fold(name).split()
    return bool(words) and words[0] in LEGAL_FORM_TOKENS


def reads_as_full_name(name):
    """Two Georgian words after the legal form, the second with a surname
    ending. A heuristic: "Given-name Surname" shapes, and some place and trade
    words that share the endings."""
    words = strip_legal_form(name)
    if len(words) != 2 or not all(_GEORGIAN_WORD.match(w) for w in words):
        return False
    return len(words[1]) > 3 and words[1].endswith(SURNAME_SUFFIXES)
