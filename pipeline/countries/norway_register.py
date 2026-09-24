"""Enhetsregisteret -> one Norwegian city's storefronts. Shared by every
Norwegian city, on France's pattern (`france_register.py`).

⚠ **DELIBERATELY NOT IN `norway.py`.** That module is imported by a city's
`config.py`, which `app/pages/*.py` imports in turn, so it must stay importable
under the lean deploy venv. This one imports pandas and is imported only by
step files.

WHAT STAYS PER CITY: the kommune number, the address file, the sanity bounding
box, and `CATCH_ALL_EXCLUDE` - a catch-all's share is a fact about a city.
"""
import re
import sys
import zipfile

import pandas as pd

from pipeline.countries import norway as NO
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module

BUCKET_DIVISIONS = ("47", "56", "96")

_NUM_RE = re.compile(r"^(?P<street>.*?\D)\s*(?P<num>\d+)\s*(?P<let>[A-Za-zÆØÅæøå]?)\s*$")


def _norm_street(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().upper()


def _street_variants(street):
    """Oslo's register still carries older spellings Kartverket has retired -
    `Storgaten` for `Storgata`. Tried only after an exact match fails."""
    out = []
    for old, new in (("GATEN", "GATA"), ("GATA", "GATEN"), ("VEIEN", "VEIEN"),
                     (" GT.", " GATE"), (" GT", " GATE")):
        if street.endswith(old) and old != new:
            out.append(street[: -len(old)] + new)
    return out


def parse_address(value):
    """(street, number, letter) from a `beliggenhetsadresse.adresse` LIST.

    The CSV flattens the list with newlines. The street line is usually the
    LAST one; earlier lines hold a c/o or a building name ("Røa Senter"). A
    line with no house number (a bare "Grønlands Torg") returns an empty
    number and cannot be placed, which is the honest answer.
    """
    if not isinstance(value, str):
        return ("", "", "")
    lines = [ln.strip() for ln in value.replace("\r", "\n").split("\n") if ln.strip()]
    lines = [ln for ln in lines if not ln.lower().startswith(NO.NON_STREET_PREFIXES)]
    for ln in reversed(lines):
        m = _NUM_RE.match(ln.split(",")[0].strip())
        if m:
            return (_norm_street(m["street"]), m["num"].lstrip("0") or "0",
                    m["let"].upper())
    return (_norm_street(lines[-1]) if lines else "", "", "")


def _read_addresses(zip_path):
    z = zipfile.ZipFile(zip_path)
    member = next(n for n in z.namelist() if n.lower().endswith(".csv"))
    adr = pd.read_csv(z.open(member), sep=";", dtype=str, low_memory=False,
                      usecols=["adressetype", "adressenavn", "nummer", "bokstav",
                               "postnummer", "Nord", "Øst"])
    adr = adr[adr["adressetype"] == "vegadresse"].copy()
    adr["k_street"] = adr["adressenavn"].map(_norm_street)
    adr["k_num"] = adr["nummer"].fillna("").str.strip().str.lstrip("0")
    adr["k_let"] = adr["bokstav"].fillna("").str.strip().str.upper()
    adr["k_post"] = adr["postnummer"].fillna("").str.strip()
    adr["lat"] = pd.to_numeric(adr["Nord"], errors="coerce")
    adr["lon"] = pd.to_numeric(adr["Øst"], errors="coerce")
    return adr.dropna(subset=["lat", "lon"])


def _join_coordinates(df, adr):
    """Staged join; each stage only sees rows every earlier stage missed, and
    every stage's gain is printed so a loose one is visible."""
    exact = {(r.k_street, r.k_num, r.k_let, r.k_post): (r.lat, r.lon)
             for r in adr.itertuples()}
    # Letter-agnostic within a postcode: prefer the bare number, else the
    # lowest letter - the same building's other entrance, metres away.
    by_num = {}
    for r in adr.sort_values(["k_let"]).itertuples():
        by_num.setdefault((r.k_street, r.k_num, r.k_post), (r.lat, r.lon))
    # Postcode-agnostic, but ONLY where the street+number+letter is unique in
    # the kommune: a register postcode can be stale, a duplicate street name
    # (two "Kirkeveien") cannot be guessed between.
    counts = adr.groupby(["k_street", "k_num", "k_let"]).size()
    unique_nopost = {k: None for k, n in counts.items() if n == 1}
    for r in adr.itertuples():
        k = (r.k_street, r.k_num, r.k_let)
        if k in unique_nopost:
            unique_nopost[k] = (r.lat, r.lon)

    stage = []
    lat, lon = [], []
    for s, n, l, p in zip(df["b_street"], df["b_num"], df["b_let"], df["b_post"]):
        hit, how = None, "unmatched"
        if s and n:
            for street in [s] + _street_variants(s):
                if (street, n, l, p) in exact:
                    hit, how = exact[(street, n, l, p)], ("exact" if street == s else "spelling")
                elif (street, n, p) in by_num:
                    hit, how = by_num[(street, n, p)], ("letter" if street == s else "spelling")
                elif unique_nopost.get((street, n, l)):
                    hit, how = unique_nopost[(street, n, l)], "postcode"
                if hit:
                    break
        stage.append(how)
        lat.append(hit[0] if hit else None)
        lon.append(hit[1] if hit else None)
    df = df.copy()
    df["geo_stage"], df["latitude"], df["longitude"] = stage, lat, lon
    return df


def _clean_trade_name(name):
    parts = str(name or "").strip().split()
    while parts and parts[-1].upper().rstrip(".") in NO.LEGAL_FORM_SUFFIXES:
        parts.pop()
    return " ".join(parts)


def build_storefronts(cfg, city_name, bbox):
    """The city's storefronts, cleaned, geolocated and labelled."""
    TAX = load_taxonomy_module(cfg.TAXONOMY_SYSTEM)

    for path, what in ((NO.SUBUNITS_CSV_GZ, "the sub-unit register"),
                       (NO.UNITS_CSV_GZ, "the main-unit register"),
                       (cfg.ADDRESS_ZIP, "the address file")):
        if not path.exists():
            sys.exit(f"missing {what}: {path}\n"
                     f"Run: python pipeline/{cfg.SLUG}/fetch_sources.py")

    df = pd.read_csv(NO.SUBUNITS_CSV_GZ, dtype=str, usecols=list(NO.SUB_COLUMNS),
                     low_memory=False)
    # THE CONTACT COLUMNS NEVER ARRIVE. Asserted rather than trusted: this is
    # the structural claim that makes a published e-mail or phone impossible.
    leaked = [c for c in df.columns if c in NO.FORBIDDEN_COLUMNS]
    assert not leaked, f"a contact column reached step 2: {leaked}"
    print(f"Enhetsregisteret sub-units: {len(df):,} nationally")

    df = df[df[NO.SUB_KOMMUNE] == cfg.KOMMUNE_NUMBER]
    print(f"  {len(df):,} with beliggenhetsadresse in kommune {cfg.KOMMUNE_NUMBER}")
    if not len(df):
        sys.exit("zero rows in the kommune - is KOMMUNE_NUMBER the four-digit code?")
    before = len(df)
    df = df[df[NO.SUB_CLOSED].isna()]
    print(f"  {len(df):,} not closed ({before - len(df):,} with a nedleggelsesdato)")

    df["sn2025_code"] = df[NO.SUB_CODE].map(TAX.normalise_code)
    df[cfg.RAW_CLASSIFICATION_COLUMN] = df[NO.SUB_LABEL].fillna("")
    in_div = df["sn2025_code"].str[:2].isin(BUCKET_DIVISIONS)
    df = df[in_div]
    print(f"\n  {len(df):,} in SN2025 divisions {'/'.join(BUCKET_DIVISIONS)}")
    excl = df[df["sn2025_code"].isin(TAX.NOT_PREMISES)]
    print(f"  {len(excl):,} structurally excluded ({len(excl) / max(len(df), 1) * 100:.1f}%):")
    for (code, lab), n in excl.groupby(["sn2025_code", cfg.RAW_CLASSIFICATION_COLUMN]).size() \
            .sort_values(ascending=False).items():
        print(f"      {code}  {n:>6,}  {lab[:60]}")
    df = filter_to_storefront(df, cfg.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")

    # --- the parent: legal form and winding-up ---------------------------
    units = pd.read_csv(NO.UNITS_CSV_GZ, dtype=str, usecols=list(NO.UNIT_COLUMNS),
                        low_memory=False)
    units = units.rename(columns={c: "p_" + c for c in NO.UNIT_COLUMNS})
    df = df.merge(units, left_on=NO.SUB_PARENT, right_on="p_" + NO.UNIT_ID, how="left")
    print(f"\n  parent found for {df['p_' + NO.UNIT_ID].notna().mean() * 100:.1f}% of rows")
    ending = pd.Series(False, index=df.index)
    for col in (NO.UNIT_BANKRUPT, NO.UNIT_WINDING_UP, NO.UNIT_FORCED_WINDING_UP):
        flag = df["p_" + col].fillna("").str.lower() == "true"
        print(f"    parent {col}: {int(flag.sum()):,}")
        ending |= flag
    df = df[~ending]
    print(f"  {len(df):,} after dropping parents bankrupt or being wound up")
    df["sole_trader"] = df["p_" + NO.UNIT_FORM] == NO.SOLE_TRADER_FORM
    print(f"  parent is a sole trader (ENK): {int(df['sole_trader'].sum()):,} "
          f"({df['sole_trader'].mean() * 100:.1f}%)")

    # --- the per-city catch-all verdict ----------------------------------
    print("\n  catch-all codes (per-city call, config.CATCH_ALL_EXCLUDE):")
    emp = df[NO.SUB_EMPLOYEES_FLAG].fillna("").str.lower() == "true"
    for code in sorted(TAX.CATCH_ALL_CODES):
        m = df["sn2025_code"] == code
        mark = "DROP" if code in cfg.CATCH_ALL_EXCLUDE else "keep"
        print(f"      {code}  {int(m.sum()):>6,}  ({m.mean() * 100:4.1f}%)  {mark}  "
              f"employees {emp[m].mean() * 100 if m.any() else 0:3.0f}%  "
              f"ENK {df.loc[m, 'sole_trader'].mean() * 100 if m.any() else 0:3.0f}%")
    before = len(df)
    df = df[~df["sn2025_code"].isin(cfg.CATCH_ALL_EXCLUDE)]
    print(f"  {len(df):,} after the catch-all exclusion ({before - len(df):,} dropped)")

    # --- coordinates: a JOIN on Kartverket's address file ------------------
    parsed = df[NO.SUB_ADDRESS].map(parse_address)
    df["b_street"] = parsed.map(lambda t: t[0])
    df["b_num"] = parsed.map(lambda t: t[1])
    df["b_let"] = parsed.map(lambda t: t[2])
    df["b_post"] = df[NO.SUB_POSTCODE].fillna("").str.strip()
    adr = _read_addresses(cfg.ADDRESS_ZIP)
    print(f"\nKartverket vegadresser in {cfg.KOMMUNE_NUMBER}: {len(adr):,}")
    df = _join_coordinates(df, adr)
    for how, n in df["geo_stage"].value_counts().items():
        print(f"  {how:<10} {n:>6,}  ({n / len(df) * 100:5.1f}%)")
    miss = df[df["geo_stage"] == "unmatched"]
    print(f"  unmatched by bucket: "
          f"{miss[cfg.RAW_CLASSIFICATION_COLUMN].str[:1].size} rows; "
          f"sole-trader share {miss['sole_trader'].mean() * 100:.1f}% vs "
          f"{df['sole_trader'].mean() * 100:.1f}% overall")
    df = df[df["geo_stage"] != "unmatched"]
    before = len(df)
    df = df[df["latitude"].between(bbox["lat_min"], bbox["lat_max"])
            & df["longitude"].between(bbox["lon_min"], bbox["lon_max"])]
    if len(df) != before:
        print(f"  {before - len(df):,} dropped on the sanity bounding box")
    print(f"  {len(df):,} storefronts with a street-level coordinate")

    # --- the pin's label ---------------------------------------------------
    #
    # A SOLE TRADER'S NAME IS NEVER SHOWN. 86-89% of ENK sub-units carry the
    # owner's own name, so the pin shows the address instead - Paris's
    # fallback. Every other row shows its registered trade name, less a
    # trailing legal-form token ("1 ØRE AS" -> "1 ØRE").
    addr_text = (df["b_street"].str.title() + " " + df["b_num"] + df["b_let"]).str.strip()
    trade = df[NO.SUB_NAME].map(_clean_trade_name)
    df["name_is_address"] = df["sole_trader"] | (trade == "")
    df["business_name"] = trade.where(~df["name_is_address"], addr_text)
    print(f"\n  trade name shown on {int((~df['name_is_address']).sum()):,} rows "
          f"({(~df['name_is_address']).mean() * 100:.1f}%); the rest show the address "
          f"(every sole trader, by rule)")

    print("\n  registered employees vs sole trader (the discriminator):")
    emp = df[NO.SUB_EMPLOYEES_FLAG].fillna("").str.lower() == "true"
    for label, m in (("no employees", ~emp), ("employees", emp)):
        print(f"    {label:14} {int(m.sum()):>7,} rows | ENK {df.loc[m, 'sole_trader'].mean() * 100:5.1f}%")

    out = df.rename(columns={NO.SUB_ID: "orgnr"})[
        ["orgnr", "business_name", "name_is_address", "latitude", "longitude",
         cfg.RAW_CLASSIFICATION_COLUMN, "sn2025_code"]]
    return out.drop_duplicates(subset=["orgnr"])
