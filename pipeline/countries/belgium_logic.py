"""Wallonia's LoGIC 2024 shop survey, read once for Charleroi and Liege.

"Offre commerciale en Wallonie (LoGIC 2024)", Service public de Wallonie (SPW)
with SEGEFA (ULiege): a field survey of summer 2024, one point per ground-floor
commercial cell, CC BY 4.0. Read from the downloaded GeoPackage only
(`belgium.LOGIC_GPKG`), never SPW's MapServer, whose service terms forbid
altering served data (docs/handoff_belgium_2026-10-03.md, build traps).

What the file holds, measured 2026-10-04 on the cached GeoPackage:

* `LOGIC_2024__POINTS_VENTE`, 37,701 points, EPSG:3812 (Lambert 2008):
  OBJECTID, ID_TERRAIN (unique), RUE, POLICE, ENSEIGNE (the shop sign),
  NOD_NOM and NOD_CODE (the perimeter), NATURE, DATE_RELEV, INS, CODE_POST.
  NATURE has four values: Commerce de detail 16,254, Services 7,851, Cellule
  vide 6,850, HoReCa 6,746.
* `LOGIC_2024__PERIM_COMMERCE`, 493 commercial perimeters with their NOD_CODE
  and INS.

Three traps, each answered here rather than in a city's step:

* RUE and POLICE (street and number) are never read: `POINT_COLUMNS` names
  what is loaded, so an address cannot reach a processed file or a page.
* INS reads as float64 (52011.0): compared as an integer.
* EVERY point carries a NOD_CODE, even outside every perimeter polygon, so
  "inside a perimeter" is a spatial test (`in_perimeter`), never the field.

THE PUBLISHER'S OWN COVERAGE STATEMENT: every shop inside the perimeters, only
shops over 200 m2 of sales area outside them. `ring_coverage` measures what
that means inside a city's station rings (the owner's "measure first",
2026-10-03).

THE DOT'S NAME IS THE SHOP SIGN (owner, 2026-10-03, Belgium build call 10). A
sign that reads as a person's own name is withheld; the city's config lists
those signs as KEYS (`pipeline/name_keys.py`), never as names. `person_sign`
is the shape test that proposes them; `python -m pipeline.countries.belgium_logic
--person-keys <INS>` prints the keys and counts only, never a sign.
"""
import re
import sys
import unicodedata

from pipeline.countries.belgium import CRS_GEOGRAPHIC, CRS_PROJECTED, LOGIC_GPKG

POINTS_LAYER = "LOGIC_2024__POINTS_VENTE"
PERIMETERS_LAYER = "LOGIC_2024__PERIM_COMMERCE"
# Every column read from the points layer. RUE and POLICE are left out on
# purpose (the street and number never leave the file).
POINT_COLUMNS = ["OBJECTID", "ID_TERRAIN", "ENSEIGNE", "NOD_NOM", "NOD_CODE",
                 "NATURE", "DATE_RELEV", "INS", "CODE_POST"]
PERIMETER_COLUMNS = ["NOD_CODE", "NOD_NOM", "TYPO_PERIM", "COMMUNE_FRE", "INS"]

# The four NATURE values and the file's totals (2026-10-04). A change means a
# new edition: re-read the taxonomy and the coverage before trusting a count.
NATURE_VALUES = ("Commerce de détail", "HoReCa", "Services", "Cellule vide")
POINTS_TOTAL = 37701
PERIMETERS_TOTAL = 493

# The SPW citation the page shows verbatim (the Metawal record, 2026-10-03).
CITATION = ("Source : Service public de Wallonie (SPW) - Offre commerciale en "
            "Wallonie (LoGIC 2024) (2025-04-09)")
METAWAL_RECORD = ("https://metawal.wallonie.be/geonetwork/srv/api/records/"
                  "5f56d784-2fd7-47eb-a62a-991d4741a67d")


# The downloaded zip and the GeoPackage inside it (measured 2026-10-04; the
# zip's entries are dated 2025-04-09, the citation's date).
LOGIC_ZIP = LOGIC_GPKG.parent.parent / "LOGIC_2024_GEOPACKAGE_3812.zip"
LOGIC_ZIP_SHA256 = "1b42f6ffd4607af6ba67b84968b1d3faa93251e81edb2d69fd6773f89d315ac2"
LOGIC_GPKG_SHA256 = "0c5a469745f595ba33cc19cbedb8de3afe128e31ed722b8add097a06d51a1a31"
LOGIC_URL = ("https://geoservices.wallonie.be/geotraitement/spwdatadownload/results/"
             "5f56d784-2fd7-47eb-a62a-991d4741a67d/LOGIC_2024_GEOPACKAGE_3812.zip")


def verify_logic():
    """Check the cached zip and GeoPackage against their recorded sha256,
    unzipping the GeoPackage from the zip if it is missing. Never downloads (a
    fresh download is the lead's, from the ATOM feed the brief names).
    Returns the provenance dict."""
    import hashlib
    import zipfile

    def sha(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()

    if not LOGIC_ZIP.exists():
        sys.exit(f"{LOGIC_ZIP} missing: the lead downloads it once from {LOGIC_URL}")
    if sha(LOGIC_ZIP) != LOGIC_ZIP_SHA256:
        sys.exit(f"{LOGIC_ZIP.name} no longer matches the cached download: a new edition?")
    with zipfile.ZipFile(LOGIC_ZIP) as z:
        info = z.getinfo(LOGIC_GPKG.name)
        if not LOGIC_GPKG.exists():
            LOGIC_GPKG.parent.mkdir(parents=True, exist_ok=True)
            z.extract(info, LOGIC_GPKG.parent)
    if sha(LOGIC_GPKG) != LOGIC_GPKG_SHA256:
        sys.exit(f"{LOGIC_GPKG.name} does not match the copy inside {LOGIC_ZIP.name}")
    return {"url": LOGIC_URL, "zip_sha256": LOGIC_ZIP_SHA256,
            "zip_bytes": LOGIC_ZIP.stat().st_size, "gpkg_sha256": LOGIC_GPKG_SHA256,
            "files_dated": "%04d-%02d-%02d" % info.date_time[:3],
            "citation": CITATION, "catalogue": METAWAL_RECORD,
            "licence": "CC BY 4.0 (Metawal record 5f56d784-2fd7-47eb-a62a-991d4741a67d)"}


def _need_gpkg(fetch_script):
    if not LOGIC_GPKG.exists():
        sys.exit(f"{LOGIC_GPKG} missing: run python {fetch_script}")


def read_points(fetch_script, ins=None):
    """LoGIC's points in EPSG:32631, RUE and POLICE never read.

    `ins`: a commune's NIS code (int) to keep, or None for all of Wallonia
    (the chain test in `chain_signs` reads every point).
    """
    import pyogrio

    _need_gpkg(fetch_script)
    gdf = pyogrio.read_dataframe(LOGIC_GPKG, layer=POINTS_LAYER, columns=POINT_COLUMNS)
    if len(gdf) != POINTS_TOTAL:
        sys.exit(f"LoGIC holds {len(gdf):,} points, not the {POINTS_TOTAL:,} measured on "
                 f"2026-10-04: a new edition - re-read pipeline/countries/belgium_logic.py")
    if str(gdf.crs).upper() != "EPSG:3812":
        sys.exit(f"LoGIC's CRS is {gdf.crs}, not EPSG:3812")
    unknown = sorted(set(gdf["NATURE"].dropna()) - set(NATURE_VALUES))
    if unknown or gdf["NATURE"].isna().any():
        sys.exit(f"NATURE values not in the taxonomy: {unknown} (or blanks)")
    gdf["INS"] = gdf["INS"].round().astype("Int64")
    if ins is not None:
        gdf = gdf[gdf["INS"] == int(ins)].copy()
    return gdf.to_crs(CRS_PROJECTED)


def read_perimeters(fetch_script, ins=None):
    """LoGIC's commercial perimeters in EPSG:32631 (all, or one commune's)."""
    import pyogrio

    _need_gpkg(fetch_script)
    gdf = pyogrio.read_dataframe(LOGIC_GPKG, layer=PERIMETERS_LAYER, columns=PERIMETER_COLUMNS)
    if len(gdf) != PERIMETERS_TOTAL:
        sys.exit(f"LoGIC holds {len(gdf)} perimeters, not the {PERIMETERS_TOTAL} measured on "
                 f"2026-10-04: a new edition")
    gdf["INS"] = gdf["INS"].round().astype("Int64")
    if ins is not None:
        gdf = gdf[gdf["INS"] == int(ins)].copy()
    return gdf.to_crs(CRS_PROJECTED)


# The perimeters are drawn through the outermost surveyed cells, so a cell on
# the edge fails a strict `within`. Measured 2026-10-04 on the retail and
# horeca points: every point outside a polygon lies either within 5 m of one
# (53 in Charleroi, 43 in Liege: on the edge) or more than 50 m away (the
# survey's "outside" code, NOD_CODE ending 999). The 5 m test reproduces the
# NOD_CODE split exactly inside the rings; the field itself is not trusted
# (the brief's trap), only compared.
PERIMETER_EDGE_M = 5.0


def in_perimeter(points, perimeters):
    """Boolean Series: is each point inside ANY perimeter polygon (all of
    Wallonia's, so a point by a neighbour's perimeter edge is still tested),
    within PERIMETER_EDGE_M of its edge."""
    union = perimeters.geometry.union_all()
    return points.geometry.distance(union) <= PERIMETER_EDGE_M


def survey_window(points):
    """(first, last) DATE_RELEV as ISO dates."""
    d = points["DATE_RELEV"].dropna()
    return d.min().date().isoformat(), d.max().date().isoformat()


def ring_union(stations, radius_m):
    """The union of `radius_m` buffers around the stations (lat/lon columns),
    built in EPSG:32631."""
    import geopandas as gpd

    pts = gpd.GeoSeries(gpd.points_from_xy(stations["longitude"], stations["latitude"]),
                        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    return pts.buffer(radius_m).union_all()


def ring_coverage(rings, points, perimeters, commune, label):
    """The owner's "measure first" (2026-10-03), printed and returned.

    `rings`: the ring union; `commune`: the commune polygon (both EPSG:32631).
    `points`: one commune's points with `bucket` and `in_perimeter` columns.
    Measures the share of the ring area inside a perimeter, the same share
    over the whole commune for comparison, and per bucket the points inside
    the rings and how many of those sit inside a perimeter, beside the
    commune-wide share of points inside a perimeter.
    """
    perim_union = perimeters.geometry.union_all()
    ring_area = rings.area
    ring_in = rings.intersection(perim_union).area
    commune_in = commune.intersection(perim_union).area
    out = {"ring_union_km2": round(ring_area / 1e6, 2),
           "ring_share_in_perimeters": round(ring_in / ring_area, 4),
           "perimeters_touching_rings": int(perimeters.geometry.intersects(rings).sum()),
           "commune_share_in_perimeters": round(commune_in / commune.area, 4),
           "buckets": {}}
    print(f"  coverage, {label}: ring union {ring_area / 1e6:.2f} km2, "
          f"{100 * ring_in / ring_area:.1f}% of it inside a commercial perimeter "
          f"({out['perimeters_touching_rings']} perimeters touch it); the commune as a whole "
          f"{100 * out['commune_share_in_perimeters']:.1f}%")
    inside_rings = points.geometry.within(rings)
    inside_perim = points["in_perimeter"]
    for bucket, g in points.groupby("bucket"):
        r = inside_rings[g.index]
        n_r, n_rp = int(r.sum()), int((r & inside_perim[g.index]).sum())
        n_all, n_p = len(g), int(inside_perim[g.index].sum())
        out["buckets"][bucket] = {"all": n_all, "in_perimeter": n_p, "in_rings": n_r,
                                  "in_rings_in_perimeter": n_rp}
        print(f"    {bucket:<13} {n_r:>5,} of {n_all:,} in the rings ({100 * n_r / n_all:.0f}%), "
              f"{n_rp:,} of those inside a perimeter ({100 * n_rp / max(n_r, 1):.0f}%); "
              f"city-wide {n_p:,} of {n_all:,} inside a perimeter ({100 * n_p / n_all:.0f}%)")
    return out


# --- The shop sign ---------------------------------------------------------

def normalise_sign(sign):
    """The sign as compared for the chain test: NFC, casefolded, accents and
    punctuation dropped, spaces collapsed. Never displayed."""
    if not isinstance(sign, str):
        return ""
    s = unicodedata.normalize("NFKD", sign.casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


# Common given names in Wallonia's population (French, Walloon, Dutch,
# Italian, Spanish, Portuguese, Polish, Turkish, Maghrebi and English forms),
# written from general knowledge, accents dropped as normalise_sign drops
# them. A sign of two or three words with one of these at either end, and no
# trade word, reads as a person's own name. Not a list of anyone: a given name
# alone identifies nobody.
GIVEN_NAMES = frozenset("""
adam adele adrien agnes ahmed aicha alain alan albert alberto alessandro alex
alexandre alexandra alexis ali alice aline alfred alfredo alphonse amandine
amelie amina anais andre andrea andree angela angelo anne annick anna annie
anthony antoine antoinette antonio armand arnaud arthur audrey aurelie axel
baptiste barbara bart beatrice benedicte benjamin benoit bernadette bernard
bertrand brigitte bruno camille carine carlos carmen carla carlo caroline
catherine cecile celine charles charlotte chantal christian christiane
christine christophe claire claude claudine claudio colette corinne cristina
cyril damien daniel daniela danielle david delphine denis denise didier
dimitri dominique edouard elena eliane elisa elisabeth elise emile emilie
emma emmanuel enzo eric estelle etienne eugene eva fabian fabien fabienne
fabrice fanny fatima felix fernand fernando florence florian francesca
francesco franck francine francis francois francoise frederic frederique
gabriel gaetan genevieve georges gerald gerard germaine ghislain ghislaine
gilbert gilles gina giovanni giuseppe gisele grace guillaume guy hakim hamid
hassan helene henri herve hugo hugues ibrahim ines irene isabelle jacqueline
jacques jean jeanne jeannine jerome jessica joao joel johan johanna john jordan
jose joseph josiane josette julie julien juliette justine karim karima karine
katia kevin laetitia laura laurence laurent lea leila leon leonard lionel
lisa louis louise luc luca lucas lucie lucien ludovic luigi luis lydie
madeleine magali manon manuel marc marcel marco marguerite maria marianne
marie marine mario marion marius martin martine mathieu mathilde maurice
maxime michel michele michelle mohamed mohammed monique morgane mustapha
nadia nadine nathalie nicolas nicole noel noemie norbert odette olivier
olga omar pascal pascale patricia patrick paul paula paulette pedro philippe
pierre pierrette pietro quentin rachid raphael raymond regine renaud rene
renee richard robert roberto roger romain rosa rosario rose roland salvatore
samir samira samuel sandra sandrine sarah sebastien serge simon simone sofia
sophie stephane stephanie suzanne sylvain sylvie thierry thomas tom tony
valentin valerie vanessa veronique victor vincent virginie vittorio
william xavier yannick yasmine youssef yves yvette yvonne zoe
""".split())

# Words that make a sign a trade name whatever else it holds: trades,
# premises, articles and the familiar forms of a shop sign ("Chez ...",
# "Mamma ..."). Accents dropped as normalise_sign drops them.
TRADE_WORDS = frozenset("""
chez la le les l au aux du des et and the of & mamma mama papa nonna tonton
tata casa villa bella bello maison boutique shop store magasin atelier
boulangerie patisserie boucherie charcuterie traiteur fromagerie epicerie
librairie pharmacie optique opticien bijouterie horlogerie fleuriste fleurs
coiffure coiffeur salon institut beaute pizzeria pizza snack friterie frite
frites cafe cafes bar brasserie bistro bistrot taverne restaurant resto
cuisine trattoria osteria tea tearoom glacier glaces chocolatier chocolat
chocolats cave vins vin tabac presse journaux sport sports mode fashion
chaussures chaussure jouets cadeaux deco decoration meubles cuir lingerie
kids baby bebe home house hotel auberge relais grill kebab burger sushi
wok food market marche super express center centre city style studio
garage auto moto cycles velo optic jewels jewelry gold or fils freres
soeurs sa sprl srl bv nv sc scrl asbl et cie co cie compagnie team club
saint sainte st ste les petits petit grand grande vieux vieille bon bonne
""".split())

# Particles inside a surname ("de", "van", "di"), skipped when counting a
# name's words.
PARTICLES = frozenset("de van der den da di del della dos von ter".split())

# A word of letters, joined by a straight or curly apostrophe or a hyphen.
_WORD = re.compile(r"^[^\W\d_]+(?:['’\-][^\W\d_]+)*$")
_INITIAL = re.compile(r"^[^\W\d_]\.?$")


def person_sign(sign):
    """Does this shop sign read as a person's own name and nothing more?

    Two or three words (surname particles aside), letters only, no trade word,
    and a given name (or a bare initial) at either end: "Given Surname",
    "Surname Given", "G. Surname", "Given-Given Surname". A single word, a
    sign with a trade word ("Boulangerie Surname", "Chez Given") or a digit or
    "&" is a trade name. A given name with only a particle after it ("Given
    Van") has one core word and is not a person's full name. A shape test only: it proposes, the city's config
    decides (`PERSON_NAMED`), and `chain_signs` keeps a founder's name that
    is a brand.
    """
    if not isinstance(sign, str):
        return False
    raw = sign.strip()
    if not raw or re.search(r"[\d&/@+]", raw):
        return False
    words = [w for w in re.split(r"\s+", raw.replace(".", ". ").strip()) if w]
    words = [w.rstrip(",") for w in words]
    # "à" is a preposition ("Pâtes à ..."), never an initial.
    if any(w.casefold() == "à" for w in words):
        return False
    folded = [normalise_sign(w) for w in words]
    # Each part of an elided or hyphenated word too: "L'Atelier" folds to
    # "l atelier".
    if any(f in TRADE_WORDS or (" " in f and any(p in TRADE_WORDS for p in f.split()))
           for f in folded):
        return False
    core = [(w, f) for w, f in zip(words, folded) if f not in PARTICLES]
    if not 2 <= len(core) <= 3:
        return False
    if not all(_WORD.match(w) or _INITIAL.match(w) for w, _ in core):
        return False

    def given(f):
        return f in GIVEN_NAMES or any(p in GIVEN_NAMES for p in f.split(" ") if p)

    def initial(w):
        return bool(_INITIAL.match(w))

    (w0, f0), (w1, f1) = core[0], core[-1]
    # Split a hyphenated given name ("jean marc" after normalising).
    return given(f0) or given(f1) or initial(w0) or initial(w1)


def chain_signs(points):
    """Normalised signs found at two or more points anywhere in Wallonia: a
    brand, kept even where it reads as a founder's name (Kansas City's rule:
    "chains named for a founder ... are brands")."""
    s = points["ENSEIGNE"].map(normalise_sign)
    s = s[s != ""]
    counts = s.value_counts()
    return set(counts[counts >= 2].index)


def person_sign_rows(points, chains):
    """Boolean Series over `points`: the sign reads as a person's own name
    and is not a chain's."""
    shaped = points["ENSEIGNE"].map(person_sign)
    norm = points["ENSEIGNE"].map(normalise_sign)
    return shaped & ~norm.isin(chains)


# A hotel's sign says so often enough to count, never to filter: the owner's
# call keeps hotels inside HoReCa (Belgium build call 9), and this count is
# for the page's disclosure only (a lower bound).
HOTEL_SIGN = re.compile(r"\bh[oô]tel\b|\bb\s?&\s?b\b|\bauberge\b|\bguest ?house\b", re.I)


def build_businesses(cfg):
    """Step 2 for a Walloon city: LoGIC's points with the city's INS, checked
    against the commune polygon, filtered to the two buckets, named by their
    sign (a person's own name withheld), measured against the commercial
    perimeters inside the station rings. Writes cfg.BUSINESSES_CLEAN_CSV and
    cfg.COVERAGE_JSON. Reads the cache only."""
    import json

    import geopandas as gpd
    import pandas as pd

    from pipeline.baseline import emit
    from pipeline.countries.belgium import commune_polygons
    from pipeline.name_keys import keys_of
    from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module

    tax = load_taxonomy_module(cfg.TAXONOMY_SYSTEM)
    print("LoGIC 2024 (cached GeoPackage):")
    allp = read_points(cfg.FETCH)
    perims = read_perimeters(cfg.FETCH)
    chains = chain_signs(allp)
    print(f"  {len(allp):,} points and {len(perims)} perimeters in Wallonia; "
          f"{len(chains):,} signs found at two or more points (brands)")

    # --- scope: INS, then the commune polygon --------------------------------
    df = allp[allp["INS"] == cfg.LOGIC_INS].copy()
    print(f"\n  INS {cfg.LOGIC_INS}: {len(df):,} points")
    for nat, n in df["NATURE"].value_counts().items():
        print(f"    {nat:<20} {n:>6,}")
    emit("logic_points", len(df))
    com = commune_polygons(cfg.OSM_COMMUNES_JSON, cfg.FETCH, cfg.NIS, cfg.COMMUNE_AREA_KM2,
                           cfg.NAME)
    own = com[com["nis"] == cfg.NIS].to_crs(cfg.CRS_PROJECTED).geometry.union_all()
    inside = df.geometry.within(own)
    dist = df.geometry.distance(own)
    print(f"  inside the commune polygon (OpenStreetMap): {int(inside.sum()):,}; outside "
          f"{int((~inside).sum())}, at most {dist.max():.0f} m beyond it")
    far = dist > cfg.POLYGON_TOLERANCE_M
    if far.any():
        sys.exit(f"{int(far.sum())} point(s) with INS {cfg.LOGIC_INS} lie more than "
                 f"{cfg.POLYGON_TOLERANCE_M:.0f} m outside the commune polygon: the INS or the "
                 f"polygon is wrong")
    others = allp[(allp["INS"] != cfg.LOGIC_INS)]
    stray = int(others.geometry.within(own).sum())
    print(f"  points of other INS codes inside the polygon (not kept; the INS is the "
          f"publisher's scope): {stray}")
    emit("outside_polygon", int((~inside).sum()))

    # --- the two buckets --------------------------------------------------------
    df["bucket"] = [tax.classify({tax.VALUE_COLUMN: v}) for v in df["NATURE"]]
    kept = filter_to_storefront(df.rename(columns={cfg.RAW_CLASSIFICATION_COLUMN:
                                                   tax.VALUE_COLUMN}), cfg.TAXONOMY_SYSTEM)
    print(f"\n  storefront filter (Commerce de détail -> Retail, HoReCa -> Food service; "
          f"Services and Cellule vide out): {len(df):,} -> {len(kept):,}")
    df = kept.copy()
    if df["ID_TERRAIN"].duplicated().any():
        sys.exit("ID_TERRAIN repeats: the survey's key is no longer unique")
    b = getattr(cfg, f"{cfg.SLUG.upper()}_BBOX")
    ll = df.to_crs(cfg.CRS_GEOGRAPHIC).geometry
    df["latitude"], df["longitude"] = ll.y.round(7), ll.x.round(7)
    ok = (df["latitude"].between(b["lat_min"], b["lat_max"])
          & df["longitude"].between(b["lon_min"], b["lon_max"]))
    if not ok.all():
        sys.exit(f"{int((~ok).sum())} point(s) outside the sanity box")
    hotels = df["ENSEIGNE"].fillna("").str.contains(HOTEL_SIGN) & (df["bucket"] == "Food service")
    for bucket, n in df["bucket"].value_counts().items():
        print(f"    {bucket:<13} {n:>6,}")
    print(f"    of the horeca, signs naming a hotel, B&B or auberge (kept, disclosed; a lower "
          f"bound): {int(hotels.sum())}")
    emit("hotel_signs", int(hotels.sum()))

    # --- the perimeters, and the owner's "measure first" -----------------------
    df["in_perimeter"] = in_perimeter(df, perims)
    code_out = df["NOD_CODE"].fillna("").str.endswith("999")
    print(f"  the spatial perimeter test against NOD_CODE's 'outside' code (ending 999): "
          f"{int((df['in_perimeter'] == ~code_out).sum()):,} of {len(df):,} agree")
    for bucket, g in df.groupby("bucket"):
        print(f"    {bucket:<13} inside a commercial perimeter: {int(g['in_perimeter'].sum()):,} "
              f"of {len(g):,}")
    own_perims = perims[perims["INS"] == cfg.LOGIC_INS]
    print(f"  {len(own_perims)} perimeters carry INS {cfg.LOGIC_INS}")
    stations_csv = cfg.STATIONS_CSV
    if not stations_csv.exists():
        sys.exit(f"{stations_csv} missing: run step 1 first (the coverage is measured "
                 f"inside the station rings)")
    stations = pd.read_csv(stations_csv)
    rings = ring_union(stations, cfg.RING_EDGES_METERS[-1])
    print()
    cov = ring_coverage(rings, df, perims, own, cfg.NAME)
    cov.update({"stations": len(stations), "ring_outer_m": round(cfg.RING_EDGES_METERS[-1], 1),
                "perimeters_with_ins": len(own_perims),
                "commune_km2": round(own.area / 1e6, 2), "measured": "step 2"})
    cfg.COVERAGE_JSON.parent.mkdir(parents=True, exist_ok=True)
    cfg.COVERAGE_JSON.write_text(json.dumps(cov, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8", newline="\n")
    emit("ring_share_in_perimeters_pct", round(100 * cov["ring_share_in_perimeters"], 1))

    # --- the dot's name: the shop sign, a person's own name withheld ------------
    sign = df["ENSEIGNE"].where(df["ENSEIGNE"].notna(), "").str.strip()
    blank = sign == ""
    key = keys_of(sign.where(~blank))
    person = key.isin(set(cfg.PERSON_NAMED))
    gone = set(cfg.PERSON_NAMED) - set(key[person])
    if gone:
        sys.exit(f"{len(gone)} PERSON_NAMED key(s) no longer match a sign: re-generate the "
                 f"list (python -m pipeline.countries.belgium_logic --person-keys "
                 f"{cfg.LOGIC_INS})")
    proposed = person_sign_rows(df.assign(ENSEIGNE=sign), chains) & ~blank
    unlisted = proposed & ~person
    if unlisted.any():
        sys.exit(f"{int(unlisted.sum())} sign(s) read as a person's own name are not in "
                 f"PERSON_NAMED: re-generate the list (count only; never print them)")
    df["business_name"] = sign.where(~(blank | person), df["NATURE"])
    print(f"\n  dot names: the shop sign on {int((~blank & ~person).sum()):,}; the class "
          f"shown instead on {int(blank.sum())} blank sign(s) and {int(person.sum())} sign(s) "
          f"read as a person's own name (config.PERSON_NAMED, keys)")
    shaped_chain = sign.map(person_sign) & sign.map(normalise_sign).isin(chains)
    print(f"  person-shaped signs kept as brands (found at two or more points in "
          f"Wallonia): {int(shaped_chain.sum())}")
    emit("signs_withheld", int(person.sum()))
    emit("signs_blank", int(blank.sum()))

    shared = df.duplicated(["latitude", "longitude"], keep=False)
    print(f"  rows sharing a point with another (drawn as they are): {int(shared.sum())}")

    out = (df.rename(columns={"ID_TERRAIN": "id"})
           [["id", "business_name", "NATURE", "latitude", "longitude", "in_perimeter"]]
           .sort_values("id").reset_index(drop=True))
    out.to_csv(cfg.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    by = out["NATURE"].map(lambda v: tax.classify({tax.VALUE_COLUMN: v})).value_counts()
    print(f"\n{len(out):,} storefronts -> {cfg.BUSINESSES_CLEAN_CSV.relative_to(cfg.ROOT)} "
          f"{by.to_dict()}")
    emit("storefronts", len(out))
    emit("retail", int(by.get("Retail", 0)))
    emit("food_service", int(by.get("Food service", 0)))


def _person_keys(ins):
    """Print the keys of one commune's person-shaped signs, and counts. Never
    a sign."""
    from pipeline.name_keys import keys_of

    script = "pipeline/countries/belgium_logic.py"
    allp = read_points(script)
    chains = chain_signs(allp)
    pts = allp[allp["INS"] == int(ins)]
    pts = pts[pts["NATURE"].isin(["Commerce de détail", "HoReCa"])]
    # Stripped, as step 2 compares it.
    sign = pts["ENSEIGNE"].where(pts["ENSEIGNE"].notna(), "").str.strip()
    shaped = sign.map(person_sign)
    is_chain = sign.map(normalise_sign).isin(chains)
    hit = shaped & ~is_chain
    keys = sorted(set(keys_of(sign[hit]).dropna()))
    print(f"INS {ins}: {len(pts):,} retail and horeca points; {int(shaped.sum())} signs "
          f"person-shaped, {int((shaped & is_chain).sum())} of them chains (kept); "
          f"{int(hit.sum())} rows withheld, {len(keys)} distinct keys:")
    for i in range(0, len(keys), 4):
        print("    " + ", ".join(f'"{k}"' for k in keys[i:i + 4]) + ",")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--person-keys":
        _person_keys(sys.argv[2])
    else:
        sys.exit("usage: python -m pipeline.countries.belgium_logic --person-keys <INS>")
