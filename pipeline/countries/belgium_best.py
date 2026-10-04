"""BeST-Address Brussels (FPS BOSA, `openaddress-bebru.zip`, CC BY 4.0): every
address in the Brussels-Capital Region with a point, and the join that places
a KBO establishment address on it (address-join skill; no geocoder).

**ONLY THE EPSG:4326 COLUMNS ARE READ, ASSERTED BY NAME.** From 2026-10-11
BOSA's CSVs replace `EPSG:31370_x/_y` (Lambert 72) with `EPSG:3812_x/_y`
(Lambert 2008) and keep WGS84, so a refreshed file still loads here and a file
without `EPSG:4326_lat/_lon` stops the step.

**Rows kept:** status current, proposed and retired; rejected dropped (the
screen's 847,377 of 848,779, 2026-10-03). Where one key has several rows,
current is preferred to proposed to retired.

**Normalisation, both sides:** accents folded; punctuation to spaces; street
types and their abbreviations folded to one canonical token per language; the
key is written without spaces, which splits nothing and joins everything, so a
Dutch compound (`Wetstraat`) and its spaced form (`Wet straat`) give one key;
`Saint`/`Sint`/`St` one token; French and Dutch names both tried. House number
parsed to number + letter; box prefix (`bte`, `boite`, `bus`, `box`, `b`)
dropped, leading zeros removed.

**Tiers, first hit wins** (`join()`):
  1 exact: postcode + street + number + letter + box
  2 number, box dropped
  3 number relaxed: letter dropped, or the first number of a range
  4 other postcode or loose street name (street types and articles dropped)
  5 street only (not placed)
  0 none (not placed)
Tiers 1-4 are placed. Tier 4 is the district-free key the address-join skill
warns about: `street_keys_in_several_postcodes()` counts the keys it could
confuse, and step 2 reports the tier so it can be dropped.
"""
import re
import unicodedata
import zipfile

import pandas as pd

LAT, LON = "EPSG:4326_lat", "EPSG:4326_lon"
BEST_COLUMNS = (LAT, LON, "address_id", "box_number", "house_number", "municipality_id",
                "postcode", "street_id", "streetname_fr", "streetname_nl", "status")
STATUS_RANK = {"current": 0, "proposed": 1, "retired": 2}
TIER_NAMES = {1: "exact", 2: "number, box dropped", 3: "number relaxed (letter/range)",
              4: "number, other postcode or loose street name", 5: "street only", 0: "none"}
PLACED_TIERS = (1, 2, 3, 4)

# Street types, per language: every spelling -> one canonical token.
_TYPES_FR = {
    "rue": "rue", "r": "rue",
    "avenue": "av", "av": "av", "ave": "av", "aven": "av",
    "boulevard": "bd", "bd": "bd", "bld": "bd", "boul": "bd", "blvd": "bd", "bvd": "bd",
    "chaussee": "chee", "chee": "chee", "chs": "chee", "chau": "chee", "chssee": "chee", "chaus": "chee",
    "place": "pl", "pl": "pl", "square": "sq", "sq": "sq", "allee": "allee", "chemin": "chemin",
    "ch": "chemin", "dreve": "dreve", "quai": "quai", "impasse": "imp", "imp": "imp",
    "parvis": "parvis", "galerie": "gal", "gal": "gal", "galeries": "gal", "clos": "clos",
    "cours": "cours", "passage": "pass", "pass": "pass", "sentier": "sentier", "venelle": "venelle",
    "voie": "voie", "route": "rte", "rte": "rte", "esplanade": "espl", "espl": "espl", "cite": "cite",
    "parc": "parc", "plateau": "plateau", "carrefour": "carref", "rondpoint": "rondpoint",
}
_TYPES_NL = {
    "straat": "str", "str": "str", "laan": "ln", "ln": "ln", "steenweg": "stwg", "stwg": "stwg",
    "stw": "stwg", "plein": "pln", "pl": "pln", "dreef": "dreef", "kaai": "kaai", "weg": "weg",
    "lei": "lei", "plaats": "plaats", "markt": "markt", "pad": "pad", "hof": "hof",
    "galerij": "gal", "galerijen": "gal", "gaarde": "gaarde", "park": "park", "poort": "poort",
    "wegel": "wegel", "square": "sq", "singel": "singel", "doorgang": "doorgang", "gang": "gang",
    "voetweg": "voetweg", "berg": "berg", "dries": "dries", "vest": "vest",
}
# Dutch compounds whose last part is a street type, longest suffix first.
_NL_SUFFIXES = sorted({"straat", "steenweg", "laan", "plein", "dreef", "kaai", "weg", "lei",
                       "plaats", "markt", "pad", "hof", "galerij", "gaarde", "park", "poort",
                       "wegel", "square", "singel", "voetweg", "str", "stwg"}, key=len, reverse=True)
_SAINTS = {"saint": "st", "sint": "st", "st": "st", "sainte": "ste", "ste": "ste"}
_ARTICLES = {"de", "la", "le", "les", "du", "des", "d", "l", "van", "der", "den", "het", "ter",
             "ten", "op", "aux", "au", "a", "en", "et", "t", "s"}
_BOX_PREFIX = re.compile(r"^(boite|bte|bt|bus|box|b)(?=[\s\.\:\-/]*[0-9])[\s\.\:\-/]*")
_NUM = re.compile(r"^(\d+)\s*([a-z]{0,3})(.*)$")


def fold(s):
    """Accents folded, lower case, punctuation to spaces, one space."""
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def _tokens(name, lang):
    types = _TYPES_FR if lang == "fr" else _TYPES_NL
    out = []
    for t in fold(name).split():
        t = _SAINTS.get(t, t)
        if t in types:
            out.append(("T", types[t]))
            continue
        if lang == "nl" and t not in types:
            for suf in _NL_SUFFIXES:
                if t.endswith(suf) and len(t) > len(suf) + 1:
                    out.append(("W", t[:-len(suf)]))
                    out.append(("T", _TYPES_NL[suf]))
                    break
            else:
                out.append(("W", t))
            continue
        out.append(("W", t))
    return out


def street_key(name, lang):
    """Strict key: canonical tokens, no spaces."""
    return "".join(v for _, v in _tokens(name, lang))


def loose_key(name, lang):
    """Loose key: street types and articles dropped."""
    return "".join(v for k, v in _tokens(name, lang) if k == "W" and v not in _ARTICLES)


def parse_number(s):
    """(number, letter, clean) - clean is False for a range or any residue."""
    s = fold(s) if isinstance(s, str) else ""
    m = _NUM.match(s)
    if not m:
        return "", "", False
    num = str(int(m.group(1)))
    letter, rest = m.group(2), m.group(3).strip()
    if letter in ("bt", "bte", "bus", "box", "b") and rest:
        # "12 bte 3": the box written into the house number.
        letter, rest = "", ""
    return num, letter, not rest


def box_norm(s):
    """Box with its prefix dropped and leading zeros removed ("bte 003" -> "3")."""
    s = fold(s) if isinstance(s, str) else ""
    s = _BOX_PREFIX.sub("", s)
    s = s.replace(" ", "")
    if s.isdigit():
        s = str(int(s))
    return s


def load(zip_path):
    """The BeST rows kept, with their keys."""
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.endswith(".csv")]
        if len(names) != 1:
            raise SystemExit(f"{zip_path.name}: expected one CSV, got {names}")
        with z.open(names[0]) as f:
            head = pd.read_csv(f, nrows=0).columns
        missing = [c for c in BEST_COLUMNS if c not in head]
        if missing:
            raise SystemExit(f"{zip_path.name}: missing column(s) {missing}; the EPSG:4326 "
                             "columns are the only coordinates read")
        with z.open(names[0]) as f:
            b = pd.read_csv(f, dtype=str, usecols=list(BEST_COLUMNS), keep_default_na=False,
                            na_values=[""])
    n_all = len(b)
    b = b[b["status"].isin(STATUS_RANK)].copy()
    b["lat"] = pd.to_numeric(b[LAT])
    b["lon"] = pd.to_numeric(b[LON])
    b = b.drop(columns=[LAT, LON])
    parsed = b["house_number"].map(parse_number)
    b["num"] = parsed.str[0]
    b["letter"] = parsed.str[1]
    b["box"] = b["box_number"].map(box_norm)
    b["rank"] = b["status"].map(STATUS_RANK)
    b.attrs["rows_read"] = n_all
    return b


class Index:
    """Lookups over the BeST rows for `join()`."""

    def __init__(self, best):
        self.best = best
        streets = best[["postcode", "street_id", "streetname_fr", "streetname_nl"]].drop_duplicates()
        self.strict, self.loose, self.anywhere = {}, {}, {}
        for pc, sid, fr, nl in streets.itertuples(index=False):
            for lang, name in (("fr", fr), ("nl", nl)):
                if not isinstance(name, str):
                    continue
                k, lk = street_key(name, lang), loose_key(name, lang)
                self.strict.setdefault((lang, pc, k), set()).add(sid)
                if lk:
                    self.loose.setdefault((lang, pc, lk), set()).add(sid)
                self.anywhere.setdefault((lang, k), set()).add(sid)
        rows = best.sort_values(["rank", "box", "address_id"])
        self.by_number, self.by_num = {}, {}
        for sid, num, letter, box, lat, lon, muni, aid in rows[
                ["street_id", "num", "letter", "box", "lat", "lon", "municipality_id",
                 "address_id"]].itertuples(index=False):
            if not num:
                continue
            rec = (box, lat, lon, muni, aid)
            self.by_number.setdefault((sid, num, letter), []).append(rec)
            self.by_num.setdefault((sid, num), []).append((letter, rec))
        self.street_postcodes = {}
        for (lang, pc, k), sids in self.strict.items():
            self.street_postcodes.setdefault((lang, k), set()).add(pc)

    def street_keys_in_several_postcodes(self):
        """Strict street keys (either language) present in more than one postcode."""
        return sum(1 for pcs in self.street_postcodes.values() if len(pcs) > 1)

    def _streets(self, table, pc, names):
        """Every street id any of the names resolves to in the postcode."""
        out = set()
        for lang, name in names:
            k = (street_key if table is self.strict else loose_key)(name, lang)
            out |= table.get((lang, pc, k), set())
        return out or None

    def _at_number(self, sids, num, letter, box):
        """(tier, rec) for a number on any of the street ids, or (None, None).
        A range or a trailing part ("12-14", "12/3") is read as its first
        number: 546 of the control's 7,685 units, which the screen's exact
        tier held (exact 81.7% with them relaxed, 88.9% without, 2026-10-04)."""
        if num:
            for sid in sorted(sids):
                for rec in self.by_number.get((sid, num, letter), ()):
                    if rec[0] == box:
                        return 1, rec
            for sid in sorted(sids):
                recs = self.by_number.get((sid, num, letter))
                if recs:
                    return 2, recs[0]
            for sid in sorted(sids):
                recs = self.by_num.get((sid, num))
                if recs:
                    recs = sorted(recs, key=lambda lr: (lr[0] != "", lr[0]))
                    return 3, recs[0][1]
        return None, None

    def join(self, postcode, street_fr, street_nl, house, box):
        """(tier, (box, lat, lon, municipality_id, address_id) or None)."""
        names = [(lang, n) for lang, n in (("fr", street_fr), ("nl", street_nl),
                                           ("nl", street_fr), ("fr", street_nl))
                 if isinstance(n, str) and n.strip()]
        num, letter, _ = parse_number(house)
        b = box_norm(box)
        sids = self._streets(self.strict, postcode, names)
        if sids:
            tier, rec = self._at_number(sids, num, letter, b)
            if tier:
                return tier, rec
        # Tier 4: the same street key in another postcode, or a loose key here.
        alt = set()
        for lang, n in names:
            for sid in self.anywhere.get((lang, street_key(n, lang)), ()):
                alt.add(sid)
        loose = self._streets(self.loose, postcode, names)
        if loose:
            alt |= loose
        alt -= sids or set()
        if alt:
            tier, rec = self._at_number(alt, num, letter, b)
            if tier:
                return 4, rec
        if sids or alt:
            return 5, None
        return 0, None
