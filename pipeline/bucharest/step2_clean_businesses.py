"""Bucharest step 2: DSVSA's registers -> the active food storefronts -> placed
by JOINING their addresses to OpenStreetMap's address objects (address-join).

    python pipeline/bucharest/step2_clean_businesses.py

Reads the cache only: the owner's browser-fetched XLSX files and
pipeline/bucharest/fetch_sources.py's OSM files. What a reader should know
before trusting the counts printed below:

  * each file lists units "active and closed": the rows below the ANULATE row
    are cancelled and never read as premises; a file's other sheets must be
    empty;
  * mobile units (Sector "U.M."), kiosk carts, vending machines and pastry
    labs are not storefronts;
  * one premises can be registered in several files (a hypermarket's butcher,
    fishmonger and food counter), so rows merge on name + parsed address;
  * the pin shows the company name without its legal form, and only the
    category for a sole trader (the owner's name rule, 2026-09-28);
  * a premises is placed only where its street and house number match OSM IN
    ITS OWN SECTOR (or within config.SECTOR_EDGE_M of it - boundary streets),
    at points that agree within config.ADDRESS_SPREAD_MAX_M. Everything else
    is disclosed as unplaced, by reason, never guessed.
"""
import collections
import csv
import math
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from openpyxl import load_workbook
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.bucharest import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
fold = TAX.fold

# --- reading the registers ---------------------------------------------------


def read_file(path, code):
    """Active rows of one DSVSA file: [{name, addr, sector, cat, file}]."""
    wb = load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets[1:]:
        if any(any(c not in (None, "") for c in r) for r in ws.iter_rows(values_only=True)):
            sys.exit(f"  {path.name}: sheet {ws.title!r} holds data - read it before trusting this file")
    header, rows, cancelled, short = None, [], 0, 0
    section = "active"
    for r in wb.worksheets[0].iter_rows(values_only=True):
        vals = [("" if c is None else str(c).strip()) for c in r]
        filled = [v for v in vals if v]
        if not filled:
            continue
        if header is None:
            if len(filled) >= 3 and any(re.search(r"denumire", v, re.I) for v in filled):
                header = [fold(h) for h in vals]
            continue
        if re.fullmatch(r"anulate", fold(filled[0])):
            section = "cancelled"
            continue
        if section == "cancelled":
            cancelled += 1
            continue
        if len(filled) < 3:
            short += 1
            continue

        def col(key):
            j = next((j for j, h in enumerate(header) if key in h), None)
            return vals[j] if j is not None and j < len(vals) else ""
        rows.append({"name": col("denumire"), "addr": col("adresa"), "sector": col("sector"),
                     "cat": col("categor"), "file": code})
    if header is None:
        sys.exit(f"  {path.name}: no header row")
    return rows, cancelled, short


def read_registers():
    rows, report = [], []
    for folder, prefix, files in ((config.DATA_RAW, "A", config.ANIMAL_FILES),
                                  (config.DATA_RAW / "non-animal", "N", config.NON_ANIMAL_FILES)):
        for name in files:
            code = prefix + re.match(r"(\d+)", name).group(1).zfill(2)
            got, cancelled, short = read_file(folder / name, code)
            rows += got
            report.append((code, len(got), cancelled, short))
    return rows, report


# --- names -------------------------------------------------------------------

# The sole-trader forms (II, PFA, IF, and their long names), written after the
# person's name OR before it, after a space or a hyphen. Tested AFTER the
# legal form is stripped: "Volosnicu Mihaela PFA SRL" and "SC II CAGELEA
# ..." hide the form behind one (2026-09-29).
_FORM = r"(i\.?\s?i\.?|p\.?\s?f\.?\s?a\.?|i\.?\s?f\.?)"
SOLE_TRADER = re.compile(
    rf"(^|[\s-]){_FORM}\s*$|^{_FORM}(\s|(?<=\.)(?=\w))|"
    r"\b(intreprindere individuala|intreprindere familiala|persoana fizica autorizata)\b")


def strip_legal_form(name):
    # "(fost X)" - "formerly X" - is the register's note, not the name.
    shown = re.sub(r"\s*\(fost[^)]*\)\s*", " ", name, flags=re.I).strip()
    for _ in range(3):
        new = re.sub(r"^\s*S\.?\s?C\.?\s+(?=\S)", "", shown, flags=re.I)
        new = re.sub(r"[\s,.-]*\b(S\.?\s?R\.?\s?L\.?(\s?-?\s?D\.?)?|S\.?\s?A\.?|S\.?\s?N\.?\s?C\.?|"
                     r"S\.?\s?C\.?\s?S\.?|S\.?\s?C\.?\s?A\.?)\s*$", "", new, flags=re.I).strip(" ,.-")
        if new == shown:
            break
        shown = new
    return shown


def display_name(name, category):
    """The owner's rule: the company name without its legal form; the
    category alone for a sole trader. Case is left as registered."""
    shown = strip_legal_form(name)
    if SOLE_TRADER.search(fold(name)) or SOLE_TRADER.search(fold(shown)):
        return None, "sole trader"
    return (shown or None), "company"


# --- addresses ---------------------------------------------------------------

TYPE_WORDS = {
    "strada": "strada", "str": "strada",
    "bulevardul": "bulevardul", "bulevard": "bulevardul", "b-dul": "bulevardul", "bdul": "bulevardul",
    "bd": "bulevardul", "blvd": "bulevardul",
    "soseaua": "soseaua", "sos": "soseaua", "sosea": "soseaua",
    "calea": "calea", "cal": "calea",
    "aleea": "aleea", "al": "aleea",
    "splaiul": "splaiul", "spl": "splaiul",
    "piata": "piata", "pta": "piata", "p-ta": "piata",
    "intrarea": "intrarea", "intr": "intrarea",
    "drumul": "drumul",
    "fundatura": "fundatura", "fund": "fundatura",
    "pasajul": "pasajul",
    "prelungirea": "prelungirea", "prel": "prelungirea",
    "ulita": "ulita", "parcul": "parcul", "cartierul": "cartierul", "piateta": "piateta",
}
DROP_WORDS = {"sector", "sect", "sectorul", "s", "bucuresti", "mun", "municipiul"}
RANKS = {"sergent", "sg", "serg", "locotenent", "lt", "aviator", "av", "general", "gral", "g-ral", "colonel",
         "col", "maior", "capitan", "cpt", "cap", "doctor", "dr", "profesor", "prof", "inginer", "ing",
         "arhitect", "arh", "sfantul", "sfanta", "sf", "erou", "eroul", "pictor", "poet", "mitropolit",
         "episcop", "voievod", "domnita", "d-na", "doamna", "regele", "regina", "printul", "maresal",
         "amiral", "plutonier", "soldat", "caporal"}
DETAIL = re.compile(r",\s*(?:sp|bl|sc|et|ap|cam|parter|incinta|sect|sector|s\d|lot|corp|hala|stand|chiosc|"
                    r"magazin|piata|poz|subsol|demisol|mansarda|spatiu|boxa|nr\.? cadastral)\b")


def street_parts(street):
    """(type, name key) of a street as either side writes it."""
    s = re.sub(r"[.,;:()\"']", " ", fold(street))
    words = s.split()
    typ = TYPE_WORDS.get(words[0]) if words else None
    if typ:
        words = words[1:]
    words = [w for w in words if w not in DROP_WORDS and not re.fullmatch(r"s\d", w)]
    return typ, " ".join(words)


def parse_address(addr):
    """(type, name key, house number) from DSVSA's free text."""
    s = fold(addr)
    s = re.sub(r"^(mun\.?\s*)?bucuresti[, ]+", "", s)
    s = DETAIL.split(s)[0]
    m = re.search(r"\b(?:nr|numarul)\.?\s*(\d+\s*[a-z]?)\b", s)
    if not m:
        m = re.search(r"(?<![\w-])(\d+\s*[a-z]?)\b(?!\s*mai\b)", s)
    if not m:
        typ, key = street_parts(s)
        return typ, key, None
    typ, key = street_parts(s[:m.start()])
    return typ, key, re.sub(r"\s+", "", m.group(1))


def key2(key):
    """The tolerant key: words over 2 letters, ranks dropped, genitive stemmed."""
    return frozenset(re.sub(r"(ilor|lor|ului|ul|ei|ii|a)$", "", w) or w
                     for w in key.replace("-", " ").split() if len(w) > 2 and w not in RANKS)


def osm_numbers(h):
    out = set()
    for part in re.split(r"[;,/]", fold(h)):
        m = re.match(r"\s*(\d+\s*[a-z]?)", part)
        if m:
            out.add(re.sub(r"\s+", "", m.group(1)))
        for n in re.findall(r"\d+", part)[:2]:
            out.add(n)
    return out


def load_osm(sectors):
    """OSM address objects: per name key, [(type, numbers, x, y, sector)]."""
    rows = []
    with open(config.OSM_ADDRESSES_CSV, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd)
        for r in rd:
            if len(r) < 6 or not r[4] or not r[2]:
                continue
            rows.append((r[4], r[5], float(r[2]), float(r[3])))
    df = pd.DataFrame(rows, columns=["street", "number", "lat", "lon"])
    g = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    # The sectors each point lies in or within config.SECTOR_EDGE_M of: a
    # boulevard is often the boundary, and its numbers sit on both sides.
    near = {s: (g.distance(poly) <= config.SECTOR_EDGE_M).values
            for s, poly in zip(sectors["sector"], sectors.geometry)}
    index = collections.defaultdict(list)
    for i, r in enumerate(g.itertuples()):
        typ, key = street_parts(r.street)
        index[key].append((typ, osm_numbers(r.number), r.geometry.x, r.geometry.y,
                           frozenset(s for s in near if near[s][i])))
    by_word = collections.defaultdict(set)
    k2 = {}
    for key in index:
        k2[key] = key2(key)
        for w in k2[key]:
            by_word[w].add(key)
    return index, by_word, k2, len(g)


def one_site(pts):
    """True when an address's OSM points are ONE place: linked hop to hop
    within config.ADDRESS_HOP_M, and no wider than config.SITE_SPREAD_MAX_M.
    A shopping centre or an industrial site carries dozens of points for one
    number (Casa Presei, Bucur Obor); a number found in two separate places
    is not one site, and the row stays unplaced."""
    if len(pts) == 1:
        return True
    if len(pts) > 400:
        return False
    groups = []
    for p in pts:
        joined = [g for g in groups if any(math.dist(p, q) <= config.ADDRESS_HOP_M for q in g)]
        groups = [g for g in groups if not any(g is j for j in joined)] + [[p] + [q for g in joined for q in g]]
    if len(groups) > 1:
        return False
    return max(math.dist(a, b) for a in pts for b in pts) <= config.SITE_SPREAD_MAX_M


def place(row, osm, use_sector=True, use_type=True):
    """(tier, x, y). Placed tiers: 'exact' (street and number), 'integer' (the
    number's whole part, 14A -> 14), 'tolerant' (the tolerant street key, only
    where ONE OSM street has the number). Unplaced: 'no number', 'no street',
    'street only' (the street, not the number), 'ambiguous' (two streets, or
    points further apart than config.ADDRESS_SPREAD_MAX_M).

    use_sector / use_type exist for the control run that reproduces Staging's
    sector-free, type-free measurement; the build always uses both."""
    index, by_word, k2 = osm
    typ, key, num, sector = (v if isinstance(v, str) and v else None
                             for v in (row["typ"], row["key"], row["num"], row["sector"]))
    if not key:
        return "no street", None, None
    if not num:
        return "no number", None, None
    sector = sector if use_sector else None
    whole = re.match(r"\d+", num).group()

    def usable(keys):
        """{street key: entries} after the type and sector filters."""
        out = {}
        for k in keys:
            es = index[k]
            if use_type and typ and any(e[0] == typ for e in es):
                es = [e for e in es if e[0] == typ]
            if sector:
                es = [e for e in es if sector in e[4]]
            if es:
                out[k] = es
        return out

    def points(streets, want):
        return {k: [(e[2], e[3]) for e in es if want in e[1]] for k, es in streets.items()}

    street_seen = False
    exact = usable([key]) if key in index else {}
    q = key2(key)
    tolerant = {}
    if q:
        cands = set.intersection(*(by_word.get(w, set()) for w in q))
        tolerant = usable(sorted(c for c in cands if q <= k2[c] and c != key))
    for tier, streets in (("exact", exact), ("tolerant", tolerant)):
        street_seen = street_seen or bool(streets)
        for label, want in ((tier, num), ("integer" if tier == "exact" else tier, whole)):
            hits = {k: p for k, p in points(streets, want).items() if p}
            if not hits:
                continue
            if len(hits) > 1 and tier == "tolerant":
                return "ambiguous", None, None
            pts = [p for ps in hits.values() for p in ps]
            if not one_site(pts):
                return "ambiguous", None, None
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            return label, sum(xs) / len(xs), sum(ys) / len(ys)
    return ("street only" if street_seen else "no street"), None, None


def main():
    for p in (config.OSM_ADDRESSES_CSV, config.SECTORS_GEOJSON, config.CITY_BOUNDARY_GEOJSON):
        if not p.exists():
            sys.exit(f"missing {p}: run python pipeline/bucharest/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    rows, report = read_registers()
    print("  file   active cancelled short")
    for code, n, c, s in report:
        print(f"  {code:5} {n:7,} {c:9,} {s:5}")
    print(f"  {len(rows):,} active rows")
    df = pd.DataFrame(rows)
    unknown = sorted(set(df["file"]) - TAX.KNOWN_FILES)
    if unknown:
        sys.exit(f"  files the taxonomy does not know: {unknown}")
    for code, grp in df.groupby("file"):
        cats = grp["cat"].map(fold).value_counts()
        print(f"    {code} categories: " + "; ".join(f"{c or '(blank)'} {n}" for c, n in cats.items()))

    mobile = df["sector"].map(fold).str.contains(r"^u\.?\s*m\b|unitate mobil|container mobil", regex=True) \
        | df["addr"].map(fold).str.contains("unitate mobila")
    notstore = df["cat"].map(fold).str.contains(TAX.NOT_STOREFRONT_CATEGORY)
    print(f"  mobile units dropped {int(mobile.sum()):,}; kiosk carts, vending machines and labs "
          f"dropped {int((notstore & ~mobile).sum()):,}")
    df = df[~mobile & ~notstore].copy()

    parsed = df["addr"].map(parse_address)
    df["typ"] = [p[0] for p in parsed]
    df["key"] = [p[1] for p in parsed]
    df["num"] = [p[2] for p in parsed]
    df["sector"] = df["sector"].map(lambda s: (re.search(r"[1-6]", str(s)) or [None])[0])

    # Merge one premises' registrations: name + parsed address.
    df["merge_key"] = df["name"].map(fold) + "|" + df["key"].fillna("") + "|" + df["num"].fillna("")
    merged = (df.groupby("merge_key", sort=False)
              .agg(name=("name", "first"), addr=("addr", "first"), sector=("sector", "first"),
                   typ=("typ", "first"), key=("key", "first"), num=("num", "first"),
                   source_files=("file", lambda s: "|".join(sorted(set(s)))),
                   Categorie=("cat", lambda s: " · ".join(dict.fromkeys(c.strip() for c in s if c.strip()))))
              .reset_index(drop=True))
    print(f"  {len(df):,} rows merge on name + address to {len(merged):,} premises")

    shown = merged.apply(lambda r: display_name(r["name"], r["Categorie"]), axis=1)
    merged["business_name"] = [s[0] if s[0] else None for s in shown]
    merged["name_kind"] = [s[1] for s in shown]
    sole = merged["name_kind"] == "sole trader"
    merged.loc[merged["business_name"].isna(), "business_name"] = \
        merged.loc[merged["business_name"].isna(), "Categorie"].str.split(" · ").str[0]
    print(f"  sole traders shown by category only: {int(sole.sum()):,}")

    merged = filter_to_storefront(merged, config.TAXONOMY_SYSTEM)
    print(f"  {len(merged):,} storefront premises after filter_to_storefront()")

    sectors = gpd.read_file(config.SECTORS_GEOJSON).to_crs(config.CRS_PROJECTED)
    index, by_word, k2, n_osm = load_osm(sectors)
    print(f"  OSM: {n_osm:,} address objects, {len(index):,} street keys")
    res = [place(r, (index, by_word, k2)) for r in merged.to_dict("records")]
    merged["placement"] = [t for t, _, _ in res]
    to_geo = Transformer.from_crs(config.CRS_PROJECTED, config.CRS_GEOGRAPHIC, always_xy=True)
    ll = [to_geo.transform(x, y) if x is not None else (None, None) for _, x, y in res]
    merged["longitude"] = [a for a, _ in ll]
    merged["latitude"] = [b for _, b in ll]
    tiers = merged["placement"].value_counts()
    placed = merged["latitude"].notna()
    print(f"\n  placed {int(placed.sum()):,} of {len(merged):,} ({placed.mean():.1%}):")
    for t, n in tiers.items():
        print(f"    {t:12} {n:6,}  {n / len(merged):6.1%}")
    by_sector = merged.groupby("sector")["latitude"].apply(lambda s: f"{s.notna().mean():.0%} of {len(s):,}")
    print("    by sector: " + ", ".join(f"{k} {v}" for k, v in by_sector.items()))
    by_file = merged.assign(f=merged["source_files"].str.split("|").str[0]).groupby("f")["latitude"] \
        .apply(lambda s: f"{s.notna().mean():.0%}")
    print("    by first file: " + ", ".join(f"{k} {v}" for k, v in by_file.items()))

    out = merged[placed].copy()
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(out["longitude"], out["latitude"]), index=out.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(city)
    print(f"  {int((~inside).sum()):,} placed outside the municipality, dropped")
    out = out[inside]
    out = out[["business_name", "latitude", "longitude", TAX.VALUE_COLUMN, "source_files",
               "name_kind", "placement", "sector"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    merged[["business_name", "addr", "sector", "Categorie", "source_files", "placement"]].to_csv(
        config.DATA_PROCESSED / "premises_all.csv", index=False, encoding="utf-8")
    bucket = [TAX.classify({TAX.VALUE_COLUMN: c, "source_files": f})
              for c, f in zip(out[TAX.VALUE_COLUMN], out["source_files"])]
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    print("    " + ", ".join(f"{TAX.legend_label(b)} {n:,}" for b, n in pd.Series(bucket).value_counts().items()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
