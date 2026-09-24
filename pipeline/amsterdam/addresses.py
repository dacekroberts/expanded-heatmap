"""One address key for both of Amsterdam's layers.

The permits carry a free-text `adres` ("Schinkelhavenstraat 27-H"); the BAG
carries the same address in parts (street, huisnummer, huisletter,
huisnummertoevoeging). Both are reduced to one key here so step 2 can
de-duplicate the layers and the fetch script can look up the permits that
carry no point. No network - this module only parses.

THE AMSTERDAM CONVENTION, measured against the BAG itself on 2026-09-24:
  * a letter ATTACHED to the number is the huisletter      94A   -> (94, A, -)
  * anything after a HYPHEN is the toevoeging              27-H  -> (27, -, H)
    - `H` is Amsterdam's ground-floor ("huis") suffix, and the BAG files it as
      huisnummertoevoeging "H", never as a letter
  * both at once                                           7C-8  -> (7, C, 8)
  * a lone letter after a SPACE is read as the huisletter  140 A -> (140, A, -)

The permit postcode is missing on 140 of 4,092 permits, 136 of them the same
ones that carry no point, so the key is STREET + number + letter + toevoeging,
never postcode.
"""
import re
import unicodedata

_ADDR = re.compile(r"^(?P<street>.*?)\s+(?P<num>\d+)(?P<rest>.*)$")
_ORDINALS = {"1": "Eerste", "2": "Tweede", "3": "Derde", "4": "Vierde", "5": "Vijfde",
             "6": "Zesde", "7": "Zevende", "8": "Achtste", "9": "Negende"}


def norm_street(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def parse(adres):
    """Free-text permit address -> (street, number, letter, toevoeging), or None.

    A few permits prefix the address with the business ("Pizza Project
    Eetcafé - Wilhelminastraat 153-H"); the street is taken after the last
    " - ". One permit carries two addresses ("... binnenkort bekend als ...",
    soon to be renamed) and is read as its first."""
    text = (adres or "").strip().split("\n")[0]
    text = re.split(r"\s+binnenkort\b", text)[0]
    m = _ADDR.match(text)
    if not m:
        return None
    street = m.group("street").split(" - ")[-1].strip().rstrip(",")
    # "1e Anjeliersdwarsstraat" is how people write "Eerste Anjeliersdwarsstraat",
    # the BAG's name.
    om = re.match(r"^(\d)e\s+(.*)$", street)
    if om and om.group(1) in _ORDINALS:
        street = f"{_ORDINALS[om.group(1)]} {om.group(2)}"
    rest = m.group("rest")
    letter = toev = None
    lm = re.match(r"^([A-Za-z])(?![A-Za-z])(.*)$", rest)          # attached letter
    if lm:
        letter, rest = lm.group(1).upper(), lm.group(2)
    else:
        sm = re.match(r"^\s+([A-Za-z])\s*$", rest)                  # "140 A"
        if sm:
            letter, rest = sm.group(1).upper(), ""
    tm = re.match(r"^\s*-\s*([A-Za-z0-9]+)", rest)
    if tm:
        toev = tm.group(1).upper()
    return street, int(m.group("num")), letter, toev


def key(street, number, letter=None, toev=None):
    return (norm_street(street), int(number), (letter or "").upper(), (toev or "").upper())


def permit_key(adres):
    p = parse(adres)
    return key(*p) if p else None
