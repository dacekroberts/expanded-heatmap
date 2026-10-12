"""Cluj-Napoca step 2: DSVSA Cluj's county registers -> the city's food
storefronts -> placed by JOINING their addresses to OpenStreetMap's address
objects (address-join), Bucharest's join with this city's repairs.

    python pipeline/cluj_napoca/step2_clean_businesses.py

Reads the cache only: the owner's browser-saved XLS and XLSX files and
pipeline/cluj_napoca/fetch_sources.py's OSM files. What a reader should know
before trusting the counts printed below:

  * the files cover the WHOLE COUNTY and carry no locality column: a row is
    the city's where its address names Cluj-Napoca, and every other row
    (another town, or no locality at all) is left out and counted;
  * each file is read by its ROLE, taken from its name (romania_dsvsa
    .role_for_file): Cluj numbers its files differently from Bucharest;
  * the files have no cancelled section; the few rows carrying a closure note
    in an unheaded column are dropped, and the rest are read as registered;
  * one file (retail, non-animal) has its address and category columns
    swapped on most rows, so each row is read by content;
  * one premises can be registered in several files (two lists of bars among
    them), so rows merge on name + parsed address;
  * the pin shows the company name without its legal form, and only the
    category for a sole trader (the owner's name rule, 2026-09-28);
  * a premises is placed where its street and house number match OSM, at
    points that are one site; where OSM has the street but not the number,
    at the nearest listed number on the same side of the street, at most
    config.NEAREST_NUMBER_MAX numbers away (owner, call 215a; Palma's tier).
    Everything else is disclosed as unplaced, by reason, never guessed.

The name rule, the street normaliser, the one-site test and place() are
Bucharest's, imported unchanged (pipeline/bucharest/step2_clean_businesses.py).
"""
import collections
import csv
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.bucharest import config as bucharest_config  # noqa: E402
from pipeline.bucharest import step2_clean_businesses as bucharest  # noqa: E402
from pipeline.cluj_napoca import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
fold = TAX.fold

# Bucharest's one_site() reads its own config: the two cities must agree.
assert (bucharest_config.ADDRESS_HOP_M, bucharest_config.SITE_SPREAD_MAX_M) == \
    (config.ADDRESS_HOP_M, config.SITE_SPREAD_MAX_M), "the one-site test's distances differ from Bucharest's"

# --- reading the registers ---------------------------------------------------

# A note in an unheaded column that says the unit is closed, suspended or
# cancelled (five rows county-wide, the brief's trap 2).
CLOSURE_NOTE = re.compile(r"\binchis|\bsuspend|\banulat")
# The city in an address: "Cluj-Napoca", "Cluj Napoca", "Mun. Cluj", "Cluj-N."
# and its misspellings ("Cluj-Naopoca", "Cluj-=Napoca"; measured 2026-10-11:
# 6,188 of the rows that name it begin with it), once "jud. Cluj" (the
# county) is cut. A bare "Cluj" is the county as often as the city and names
# neither. A row that opens with a village or commune word ("sat", "com.")
# is that place's, whatever it mentions later (19 rows).
COUNTY = re.compile(r"\b(jud\.?|judetul?)\s*cluj\b(?![\s=-]*n)")
CITY = re.compile(r"\b(?:mun\.?|municipiul|loc\.?|localitatea|oras(?:ul)?)?\s*cluj[\s=-]*n(?:[a-z]{3,6}ca)?\b\.?|"
                  r"\b(?:mun\.?|municipiul)\s*cluj\b")
OTHER_PLACE_FIRST = re.compile(r"^\s*(sat|satul|com|comuna)\b")


def in_city(addr):
    s = COUNTY.sub(" ", fold(addr))
    return bool(CITY.search(s)) and not OTHER_PLACE_FIRST.search(s)
ADDRESS_LIKE = re.compile(r"\d|\bcluj\b|\bstr\b|\bstrada\b|\bnr\b")


def sheets(path):
    """[(sheet name, rows of cell values)] of an XLS or XLSX file."""
    if path.suffix.lower() == ".xls":
        import xlrd
        wb = xlrd.open_workbook(str(path))
        return [(sh.name, [[sh.cell_value(r, c) for c in range(sh.ncols)] for r in range(sh.nrows)])
                for sh in wb.sheets()]
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    return [(ws.title, [list(r) for r in ws.iter_rows(values_only=True)]) for ws in wb.worksheets]


def read_file(path, code):
    """One file's registered rows: [{name, addr, cat, file}], and the counts
    of rows dropped for a closure note and of rows read with swapped columns."""
    book = sheets(path)
    for title, extra in book[1:]:
        if any(any(c not in (None, "") for c in r) for r in extra):
            sys.exit(f"  {path.name}: sheet {title!r} holds data - read it before trusting this file")
    header, rows, closed, swapped = None, [], 0, 0
    for r in book[0][1]:
        vals = [("" if c is None else str(c).strip()) for c in r]
        filled = [v for v in vals if v]
        if header is None:
            if len(filled) >= 3 and any(re.search(r"denumire", fold(v)) for v in filled):
                header = [fold(h) for h in vals]
            continue
        if len(filled) < 3:
            continue

        def at(key):
            return next((j for j, h in enumerate(header) if key in h), None)

        cols = {k: at(k) for k in ("denumire", "adresa", "categor", "inregistr")}
        if None in cols.values():
            sys.exit(f"  {path.name}: header lacks one of {sorted(cols)}: {[h for h in header if h]}")
        named = set(cols.values()) | {at("nr. crt")}
        if any(CLOSURE_NOTE.search(fold(v)) for j, v in enumerate(vals) if j not in named and v):
            closed += 1
            continue
        addr, cat = vals[cols["adresa"]], vals[cols["categor"]]
        # The address and the category sit under each other's header on most
        # rows of one file: read each row by content, never by the header.
        if ADDRESS_LIKE.search(fold(cat)) and not ADDRESS_LIKE.search(fold(addr)):
            addr, cat = cat, addr
            swapped += 1
        rows.append({"name": vals[cols["denumire"]], "addr": addr, "cat": cat, "file": code})
    if header is None:
        sys.exit(f"  {path.name}: no header row")
    return rows, closed, swapped


def read_registers():
    rows, report = [], []
    for folder, prefix, files in ((config.DATA_RAW, "A", config.ANIMAL_FILES),
                                  (config.DATA_RAW / "non-animal", "N", config.NON_ANIMAL_FILES)):
        for name in files:
            number = prefix + re.match(r"(\d+)", name).group(1).zfill(2)
            code = f"{number}:{TAX.role_for_file(name)}"
            path = folder / name
            if not path.exists():
                sys.exit(f"missing {path}: run python pipeline/cluj_napoca/fetch_sources.py")
            got, closed, swapped = read_file(path, code)
            want = config.EXPECTED_ROWS[number]
            if len(got) + closed != want:
                sys.exit(f"  {name}: {len(got) + closed} rows, not the {want} measured on 2026-10-07 - a new "
                         f"edition; re-measure it")
            rows += got
            report.append((code, len(got), closed, swapped))
    return rows, report


# --- addresses ---------------------------------------------------------------

MONTHS = "ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie"
# A street named for a date ("21 Decembrie 1989", "1 Mai"): its day and year
# are not a house number.
DATE_NAME = re.compile(rf"\b(\d{{1,2}})\s+({MONTHS})(?:\s+((?:1[89]|20)\d\d))?\b")


def protect_dates(s):
    """A date-named street written as one word no number pattern reads."""
    return DATE_NAME.sub(lambda m: "z" + "_".join(p for p in m.groups() if p), s)


def repair(addr):
    """The register's address, folded, with the locality cut and this city's
    three repairs (the brief, 2026-10-07): date-named streets kept whole,
    "nr." written apart from what it touches, and (in the key, below)
    one-letter initials dropped."""
    s = COUNTY.sub(" ", fold(addr))
    s = CITY.sub(" ", s)
    s = protect_dates(s)
    s = re.sub(r"(?<=[a-z])\.?nr\.?\s*(?=\d)", " nr ", s)
    s = re.sub(r"\bnr\s*[.:]+\s*", "nr ", s)
    return re.sub(r"^[\s,;.-]+", "", re.sub(r"\s+", " ", s))


def street_key(street):
    """(type, key) as Bucharest's street_parts, less one-letter initials."""
    typ, key = bucharest.street_parts(protect_dates(fold(street)))
    return typ, " ".join(w for w in key.split() if len(w) > 1)


def parse_address(addr):
    typ, key, num = bucharest.parse_address(repair(addr))
    return typ, " ".join(w for w in (key or "").split() if len(w) > 1), num


def load_osm():
    """OSM address objects in Bucharest's index shape, with no sector."""
    rows = []
    with open(config.OSM_ADDRESSES_CSV, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd)
        for r in rd:
            if len(r) < 6 or not r[4] or not r[2]:
                continue
            rows.append((r[4], r[5], float(r[2]), float(r[3])))
    if len(rows) < config.OSM_ADDRESSES_MIN:
        sys.exit(f"{config.OSM_ADDRESSES_CSV.name}: {len(rows):,} address objects, under "
                 f"{config.OSM_ADDRESSES_MIN:,} - a partial fetch")
    df = pd.DataFrame(rows, columns=["street", "number", "lat", "lon"])
    g = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    index = collections.defaultdict(list)
    for r in g.itertuples():
        typ, key = street_key(r.street)
        index[key].append((typ, bucharest.osm_numbers(r.number), r.geometry.x, r.geometry.y, frozenset()))
    by_word, k2 = collections.defaultdict(set), {}
    for key in index:
        k2[key] = bucharest.key2(key)
        for w in k2[key]:
            by_word[w].add(key)
    return index, by_word, k2, len(g)


def nearest_number(row, osm):
    """The nearest-number tier for a row place() left as "street only": the
    nearest number OSM lists on the same side of the ONE street the row names,
    at most config.NEAREST_NUMBER_MAX away, a tie to the lower number, and
    only where that number's points are one site. (x, y) or None."""
    index, by_word, k2 = osm
    key, typ, num = row["key"], row["typ"], row["num"]
    whole = int(re.match(r"\d+", num).group())

    def usable(k):
        es = index[k]
        if typ and any(e[0] == typ for e in es):
            es = [e for e in es if e[0] == typ]
        return es

    if key in index:
        streets = [usable(key)]
    else:
        q = bucharest.key2(key)
        cands = set.intersection(*(by_word.get(w, set()) for w in q)) if q else set()
        streets = [usable(c) for c in sorted(cands) if q <= k2[c]]
    if len(streets) != 1:
        return None
    by_number = collections.defaultdict(list)
    for e in streets[0]:
        for n in e[1]:
            if n.isdigit():
                by_number[int(n)].append((e[2], e[3]))
    near = [n for n in by_number if n % 2 == whole % 2 and 0 < abs(n - whole) <= config.NEAREST_NUMBER_MAX]
    if not near:
        return None
    gap = min(abs(n - whole) for n in near)
    best = min(n for n in near if abs(n - whole) == gap)
    pts = by_number[best]
    if not bucharest.one_site(pts):
        return None
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts), gap


def main():
    for p in (config.OSM_ADDRESSES_CSV, config.CITY_BOUNDARY_GEOJSON):
        if not p.exists():
            sys.exit(f"missing {p}: run python pipeline/cluj_napoca/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    rows, report = read_registers()
    print("  file                    registered closure-noted swapped-columns")
    for code, n, c, s in report:
        print(f"  {code:22} {n:10,} {c:14,} {s:15,}")
    df = pd.DataFrame(rows)
    print(f"  {len(df):,} registered rows in the county, {sum(c for _, _, c, _ in report)} dropped for a "
          f"closure note")
    emit("county_rows", len(df))
    emit("closure_noted_rows", sum(c for _, _, c, _ in report))

    city_rows = df["addr"].map(in_city)
    print(f"  {int(city_rows.sum()):,} rows name Cluj-Napoca; {int((~city_rows).sum()):,} name another place or "
          f"none, left out")
    print("    in the city, by file: " + ", ".join(
        f"{c.split(':')[0]} {n}" for c, n in df[city_rows].groupby("file", sort=False).size().items()))
    emit("city_rows", int(city_rows.sum()))
    emit("rows_outside_or_no_locality", int((~city_rows).sum()))
    df = df[city_rows].copy()
    for code, grp in df.groupby("file", sort=False):
        cats = grp["cat"].map(fold).value_counts()
        print(f"    {code} categories: " + "; ".join(f"{c or '(blank)'} {n}" for c, n in cats.items()))

    parsed = df["addr"].map(parse_address)
    df["typ"] = [p[0] for p in parsed]
    df["key"] = [p[1] for p in parsed]
    df["num"] = [p[2] for p in parsed]
    df["sector"] = None

    # Merge one premises' registrations: name + parsed address (Bucharest's key).
    df["merge_key"] = df["name"].map(fold) + "|" + df["key"].fillna("") + "|" + df["num"].fillna("")
    merged = (df.groupby("merge_key", sort=False)
              .agg(name=("name", "first"), addr=("addr", "first"), sector=("sector", "first"),
                   typ=("typ", "first"), key=("key", "first"), num=("num", "first"),
                   source_files=("file", lambda s: "|".join(sorted(set(s)))),
                   Categorie=("cat", lambda s: " · ".join(dict.fromkeys(c.strip() for c in s if c.strip()))))
              .reset_index(drop=True))
    print(f"  {len(df):,} rows merge on name + address to {len(merged):,} premises")
    emit("premises_merged", len(merged))

    shown = merged.apply(lambda r: bucharest.display_name(r["name"], r["Categorie"]), axis=1)
    # Bucharest's verdict, then the two extensions a county after Bucharest
    # needs (abbreviated sole-trader forms, Hungarian and Transylvanian
    # person names): romania_dsvsa.name_kind_extended.
    kinds = [TAX.name_kind_extended(n, s[0] or "", s[1], bucharest.GIVEN_NAMES)
             for n, s in zip(merged["name"], shown)]
    merged["business_name"] = [s[0] if s[0] and k == "company" else None for s, k in zip(shown, kinds)]
    merged["name_kind"] = kinds
    merged.loc[merged["business_name"].isna(), "business_name"] = \
        merged.loc[merged["business_name"].isna(), "Categorie"].str.split(" · ").str[0]
    kinds = merged["name_kind"].value_counts()
    print(f"  shown by category only: sole traders {kinds.get('sole trader', 0):,}, companies named as a person "
          f"{kinds.get('person-named company', 0):,}")
    emit("names_sole_trader", int(kinds.get("sole trader", 0)))
    emit("names_person_named_company", int(kinds.get("person-named company", 0)))

    # What the category rules leave out, by rule, before the filter drops them.
    cat = merged["Categorie"].map(fold)
    parts = merged["Categorie"].map(lambda c: [fold(p) for p in str(c).split("·")])
    out_rules = {
        "kiosk carts, vending machines, pastry labs, in-house buffets, catering alone, trailers and mobile "
        "units (Bucharest's rule)": cat.str.contains(TAX.NOT_STOREFRONT_CATEGORY),
        "pharmacies": parts.map(lambda ps: any("farmaci" in p for p in ps)),
        "stalls (stand)": parts.map(lambda ps: any(re.search(r"\bstand(uri)?\b", p) for p in ps)),
        "canteens": parts.map(lambda ps: any("cantin" in p for p in ps)),
        "catering": parts.map(lambda ps: any(re.search(r"^(unitate de )?catering\b(?!\s*[-/])", p) for p in ps)),
        "mobile, itinerant and temporary units written without Bucharest's words":
            parts.map(lambda ps: any(re.search(r"\bmobil[ae]?\b|ambulant|temporar", p) for p in ps))
            & ~cat.str.contains(TAX.NOT_STOREFRONT_CATEGORY),
    }
    for label, mask in out_rules.items():
        print(f"    left out, {label}: {int(mask.sum()):,}")
    before = len(merged)
    merged = filter_to_storefront(merged, config.TAXONOMY_SYSTEM)
    print(f"  {len(merged):,} storefront premises after filter_to_storefront() ({before - len(merged):,} left out)")
    emit("not_storefront", before - len(merged))
    emit("storefront_premises", len(merged))

    index, by_word, k2, n_osm = load_osm()
    osm = (index, by_word, k2)
    print(f"  OSM: {n_osm:,} address objects, {len(index):,} street keys")
    res = [bucharest.place(r, osm, use_sector=False) for r in merged.to_dict("records")]
    tiers, xs, ys, gaps = [], [], [], []
    for r, (tier, x, y) in zip(merged.to_dict("records"), res):
        if tier == "street only":
            near = nearest_number(r, osm)
            if near:
                tier, x, y = "nearest", near[0], near[1]
                gaps.append(near[2])
        tiers.append(tier), xs.append(x), ys.append(y)
    merged["placement"] = tiers
    to_geo = Transformer.from_crs(config.CRS_PROJECTED, config.CRS_GEOGRAPHIC, always_xy=True)
    ll = [to_geo.transform(x, y) if x is not None else (None, None) for x, y in zip(xs, ys)]
    merged["longitude"] = [a for a, _ in ll]
    merged["latitude"] = [b for _, b in ll]
    placed = merged["latitude"].notna()
    print(f"\n  placed {int(placed.sum()):,} of {len(merged):,} ({placed.mean():.1%}):")
    for t, n in merged["placement"].value_counts().items():
        print(f"    {t:12} {n:6,}  {n / len(merged):6.1%}")
        emit("placement_" + t.replace(" ", "_"), int(n))
    if gaps:
        s = pd.Series(gaps)
        print(f"    the nearest tier sits a median {s.median():.0f} house numbers from its own address "
              f"(90th percentile {s.quantile(0.9):.0f})")
    bucket_all = pd.Series([TAX.classify(r) for r in merged.to_dict("records")], index=merged.index)
    print("    by bucket: " + ", ".join(
        f"{TAX.legend_label(b)} {int(placed[bucket_all == b].sum()):,} of {int((bucket_all == b).sum()):,}"
        for b in ("Retail", "Food service")))
    if placed.mean() < config.PLACED_SHARE_MIN:
        sys.exit(f"  placed {placed.mean():.1%}, under the {config.PLACED_SHARE_MIN:.0%} bar the owner's call "
                 f"rests on (call 215a) - read the unplaced rows before publishing")

    out = merged[placed].copy()
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(out["longitude"], out["latitude"]), index=out.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(city)
    print(f"  {int((~inside).sum()):,} placed outside the municipality, dropped")
    emit("placed_outside_city", int((~inside).sum()))
    out = out[inside]
    out = out[["business_name", "latitude", "longitude", TAX.VALUE_COLUMN, "source_files", "name_kind",
               "placement"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    merged[["business_name", "addr", "Categorie", "source_files", "placement"]].to_csv(
        config.DATA_PROCESSED / "premises_all.csv", index=False, encoding="utf-8", lineterminator="\n")
    bucket = pd.Series([TAX.classify(r) for r in out.to_dict("records")]).value_counts()
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    print("    " + ", ".join(f"{TAX.legend_label(b)} {n:,}" for b, n in bucket.items()))
    emit("storefronts", len(out))
    for b, n in bucket.items():
        emit("storefronts_" + TAX.legend_label(b).lower().replace(" ", "_"), int(n))
    emit("unplaced", int((~placed).sum()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
