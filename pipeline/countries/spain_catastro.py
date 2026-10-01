"""Spain: joining a register's addresses to the Dirección General del
Catastro's INSPIRE address points - the address-join skill's method, written
for Palma (2026-09-30), the first Spanish city placed by a join.

Catastro publishes, per municipality, every address with a coordinate: an
INSPIRE Addresses GML (`A.ES.SDGC.AD.<ine>.gml`, in a zip from the province's
ATOM feed), in ETRS89 / UTM of the province. Each `AD:Address` carries its
number (`AD:designator`, "20", "4A"), its point (`gml:pos`, the entrance) and
references to a `AD:ThoroughfareName` (" CL ANTONI MULET": a type code, then
the name) and a `AD:PostalDescriptor` (the postcode, "7001" for 07001).

  * `read_addresses(zip_path, member)` parses the file into one row per
    address point: street id, street text, type code, the normalised name key,
    the number and its suffix, the postcode, x, y.
  * `street_key(text, catastro=...)` is the normalisation both sides share.
    It comes from READING MISSES at the Palma build (the skill's step 5);
    any change re-runs Palma's control (its 581 register
    coordinates, compared with where the join puts them) before it counts.
  * `Joiner(addresses).place(name, number, suffix, type_code, postcode)`
    returns the tier and the point: "exact" (the street and the number),
    "nearest" (the nearest listed number on the same side, within a limit -
    Incheon's precedent), or None. A name + number that names two places
    more than `AMBIGUOUS_M` apart, and that the type or the postcode cannot
    separate, is left unplaced rather than guessed.

**Never fuzzy-match** (the skill): a key either matches or it does not.
Nothing here fetches.
"""
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict

# Catastro's files declare the INSPIRE 3.0 URNs, not the 4.0 schema URLs.
NS = {"AD": "urn:x-inspire:specification:gmlas:Addresses:3.0",
      "gml": "http://www.opengis.net/gml/3.2",
      "GN": "urn:x-inspire:specification:gmlas:GeographicalNames:3.0",
      "xlink": "http://www.w3.org/1999/xlink"}

# The register's long forms (Catalan and Castilian) -> Catastro's type codes,
# used only to choose between two streets of the same name.
LONG_FORMS = {
    "CARRER": "CL", "CALLE": "CL", "C": "CL", "AVINGUDA": "AV", "AVENIDA": "AV", "AVDA": "AV",
    "AV": "AV", "PLACA": "PZ", "PLAZA": "PZ", "PL": "PZ", "PLACETA": "PZ", "PASSEIG": "PS",
    "PASEO": "PS", "PG": "PS", "CAMI": "CM", "CAMINO": "CM", "CARRETERA": "CR", "CTRA": "CR",
    "TRAVESSIA": "TR", "TRAVESIA": "TR", "RONDA": "RD", "PASSATGE": "PJ", "PASAJE": "PJ",
    "RAMBLA": "RB", "COSTA": "CO", "BAIXADA": "BJ", "PUJADA": "PU", "VIA": "VIA",
    "URBANITZACIO": "UR", "URBANIZACION": "UR", "POLIGON": "PG", "POLIGONO": "PG",
    "MOLL": "ML", "PARC": "PQ", "PARQUE": "PQ", "ESCALA": "ES", "CARRERO": "CL",
}
# Articles and prepositions, Catalan (including Mallorca's `sa`, `es`, `ses`)
# and Castilian: dropped on both sides, so "Carrer de Sa Faixina" and
# "CL FAIXINA SA" meet.
PARTICLES = {"DE", "DEL", "DELS", "DES", "D", "L", "LA", "LES", "EL", "ELS", "LO", "LOS", "LAS",
             "SA", "ES", "SES", "S", "SAS", "I", "Y", "CAN", "CA", "NA", "EN", "N", "A", "AL"}
LONG_FORMS.update({"TRAVESSA": "TR", "VEINAL": "CM"})
# Abbreviations, and the Castilian and Catalan forms of one name, read in
# Palma's misses (MIGUEL / MIQUEL ROSSELLO I ALEMANY, BARTOLOME / BARTOMEU
# RIUTORT, AEROPORT / AEROPUERTO SON SANT JOAN): each token maps to one form,
# on both sides.
CANON = {"STA": "SANTA", "STO": "SANTO", "SNT": "SANT", "GRAL": "GENERAL", "PTE": "PRESIDENT",
         "DR": "DOCTOR", "MTRO": "MESTRE", "FC": "FRANCESC",
         "MIGUEL": "MIQUEL", "JOAQUIN": "JOAQUIM", "BARTOLOME": "BARTOMEU", "FAUSTO": "FAUST",
         "EMILIO": "EMILI", "RICARDO": "RICARD", "SAN": "SANT", "JUAN": "JOAN", "JOSE": "JOSEP",
         "ANTONIO": "ANTONI", "FRANCISCO": "FRANCESC", "PEDRO": "PERE", "JAIME": "JAUME",
         "GUILLERMO": "GUILLEM", "LORENZO": "LLORENC", "MATEO": "MATEU", "VICENTE": "VICENC",
         "CREDITO": "CREDIT", "AEROPUERTO": "AEROPORT", "MONSERRAT": "MONTSERRAT"}
# Titles a register puts before a name that Catastro files without one
# (ENGINYER GABRIEL ROCA / AV GABRIEL ROCA); tried only when the full key misses.
TITLES = {"ENGINYER", "INGENIERO", "ARQUITECTE", "ARQUITECTO", "METGE", "MEDICO", "DOCTOR",
          "PINTOR", "POETA", "MUSIC", "MESTRE", "PARE", "PADRE", "BATLE", "ALCALDE"}
# Catastro cuts the name after this many characters ("TOMAS DE VILLANUEVA
# CORTE", "GREMI DE SELLETERS I BAS"); a register name that begins with a cut
# name's key is that street.
CATASTRO_NAME_MAX = 24

AMBIGUOUS_M = 60.0


def fold(text):
    """Upper-case ASCII, accents dropped, apostrophes and punctuation to spaces.
    Catalan's geminate L (l·l), which Catastro writes "L.L" (RUL.LAN), is LL."""
    s = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"L\s*[.·]\s*L", "LL", s)
    s = re.sub(r"\(.*?\)", " ", s)
    return re.sub(r"[^A-Z0-9]+", " ", s).strip()


def street_key(text, catastro=False):
    """(type code or None, the name key). Catastro's text always leads with its
    type code, and files a title after a comma ("JOSEP DARDER,METGE"); the
    register's may lead with a long form (or two: "Carrer CAMI REIS"), or none."""
    text = str(text or "")
    if catastro and "," in text:
        head, _, tail = text.partition(",")
        code, _, name = head.strip().partition(" ")
        text = f"{code} {tail} {name}"
    title = []
    if not catastro and "," in text:
        # The register inverts a title the same way ("JOSEP DARDER, METGE").
        head, _, tail = text.partition(",")
        if fold(tail) in TITLES:
            text, title = head, [fold(tail)]
    tokens = fold(text).split()
    kind = None
    if catastro and tokens:
        kind, tokens = tokens[0], tokens[1:]
    else:
        while len(tokens) > 1 and tokens[0] in LONG_FORMS:
            kind = kind or LONG_FORMS[tokens[0]]
            tokens = tokens[1:]
        if len(tokens) > 1 and tokens[-1] in LONG_FORMS:
            tokens = tokens[:-1]
        tokens = title + tokens
    tokens = [CANON.get(t, t) for t in tokens]
    kept = [t for t in tokens if t not in PARTICLES]
    return kind, " ".join(kept or tokens)


def split_number(designator):
    """"4A" -> (4, "A"); "S/N", "" -> (None, "")."""
    m = re.match(r"^\s*0*(\d+)\s*([A-Z]?)\b", str(designator or "").upper())
    return (int(m.group(1)), m.group(2)) if m else (None, "")


def read_addresses(zip_path, member):
    """One dict per Catastro address point."""
    import pandas as pd
    with zipfile.ZipFile(zip_path) as z:
        root = ET.fromstring(z.read(member))
    streets, postcodes, rows = {}, {}, []
    for tn in root.iter(f"{{{NS['AD']}}}ThoroughfareName"):
        gid = tn.get(f"{{{NS['gml']}}}id")
        text = tn.find(".//GN:text", NS)
        streets[gid] = (text.text or "").strip() if text is not None else ""
    for pd_ in root.iter(f"{{{NS['AD']}}}PostalDescriptor"):
        code = pd_.find("AD:postCode", NS)
        postcodes[pd_.get(f"{{{NS['gml']}}}id")] = (code.text or "").strip().zfill(5) if code is not None else ""
    for ad in root.iter(f"{{{NS['AD']}}}Address"):
        pos = ad.find(".//gml:pos", NS)
        des = ad.find(".//AD:LocatorDesignator/AD:designator", NS)
        comps = [c.get(f"{{{NS['xlink']}}}href", "").lstrip("#") for c in ad.findall("AD:component", NS)]
        tn = next((c for c in comps if ".TN." in c), None)
        pc = next((c for c in comps if ".PD." in c), None)
        if pos is None or tn is None:
            continue
        x, y = (float(v) for v in pos.text.split())
        number, suffix = split_number(des.text if des is not None else "")
        kind, key = street_key(streets.get(tn, ""), catastro=True)
        rows.append({"address_id": ad.get(f"{{{NS['gml']}}}id"), "street_id": tn,
                     "street": streets.get(tn, ""), "type_code": kind, "street_key": key,
                     "number": number, "suffix": suffix, "postcode": postcodes.get(pc, ""),
                     "x": x, "y": y})
    return pd.DataFrame(rows)


class Joiner:
    """Street + number lookups over Catastro's points."""

    def __init__(self, addresses, nearest_max=6, aliases=None):
        self.nearest_max = nearest_max
        self.aliases = dict(aliases or {})
        self.by_key = defaultdict(list)
        cut = set()
        for r in addresses.itertuples(index=False):
            if r.number is not None and r.street_key:
                self.by_key[r.street_key].append(r)
                name = r.street.strip().partition(" ")[2]
                if len(name) >= CATASTRO_NAME_MAX:
                    cut.add(r.street_key)
        self.keys = set(self.by_key)
        self.cut = {k.replace(" ", ""): k for k in cut}

    def resolve(self, key):
        """(Catastro's key, how) for a register key, or (None, None). In order:
        the same key; a named alias (config); a name Catastro cut short; the
        key less a leading title; the key less a trailing second surname. Each
        must land on a key Catastro has; none is a similarity score."""
        if key in self.keys:
            return key, "same"
        if key in self.aliases and self.aliases[key] in self.keys:
            return self.aliases[key], "alias"
        compact = key.replace(" ", "")
        hits = {k for c, k in self.cut.items() if compact.startswith(c) and len(c) >= 12}
        if len(hits) == 1:
            return hits.pop(), "cut short"
        toks = key.split()
        while len(toks) > 1 and toks[0] in TITLES:
            toks = toks[1:]
            if " ".join(toks) in self.keys:
                return " ".join(toks), "title dropped"
        if len(toks) >= 3 and " ".join(toks[:-1]) in self.keys:
            return " ".join(toks[:-1]), "second surname dropped"
        return None, None

    @staticmethod
    def _choose(cands, type_code, postcode):
        """One point from candidates, narrowed by type then postcode; None when
        what is left still names places more than AMBIGUOUS_M apart."""
        for attr, want in (("type_code", type_code), ("postcode", postcode)):
            if want:
                narrowed = [c for c in cands if getattr(c, attr) == want]
                if narrowed:
                    cands = narrowed
        xs, ys = [c.x for c in cands], [c.y for c in cands]
        if max(xs) - min(xs) > AMBIGUOUS_M or max(ys) - min(ys) > AMBIGUOUS_M:
            return None
        return sum(xs) / len(xs), sum(ys) / len(ys)

    def place(self, key, number, suffix="", type_code=None, postcode=""):
        """(tier, x, y) or (reason, None, None). `key` is Catastro's (resolve())."""
        if key is None or key not in self.by_key:
            return "street not in Catastro", None, None
        if number is None:
            return "no number", None, None
        pts = self.by_key[key]
        exact = [p for p in pts if p.number == number]
        if exact:
            if suffix and any(p.suffix == suffix for p in exact):
                exact = [p for p in exact if p.suffix == suffix]
            elif any(p.suffix == "" for p in exact):
                exact = [p for p in exact if p.suffix == ""]
            xy = self._choose(exact, type_code, postcode)
            return ("exact", *xy) if xy else ("ambiguous street", None, None)
        near = [p for p in pts if p.number % 2 == number % 2 and 0 < abs(p.number - number)
                <= self.nearest_max]
        if not near:
            return "number not in Catastro", None, None
        gap = min(abs(p.number - number) for p in near)
        best = min(p.number for p in near if abs(p.number - number) == gap)
        xy = self._choose([p for p in near if p.number == best and p.suffix == ""] or
                          [p for p in near if p.number == best], type_code, postcode)
        return ("nearest", *xy) if xy else ("ambiguous street", None, None)
