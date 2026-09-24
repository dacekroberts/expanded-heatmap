"""CVR + DAR -> one Danish city's storefronts. Shared by every Danish city, on
Norway's pattern (`norway_register.py`).

⚠ **DELIBERATELY NOT IN `denmark.py`.** That module is imported by a city's
`config.py`, which `app/pages/*.py` imports in turn, so it must stay importable
under the lean deploy venv. This one imports pandas and pyproj and is imported
only by step files.

WHAT STAYS PER CITY: the kommuner, the sanity bounding box, and
`CATCH_ALL_EXCLUDE` - a catch-all's share is a fact about a city.

THE JOIN, in the order it runs:

    Produktionsenhed   active, current                     -> the premises
    Adressering        beliggenhedsadresse in the kommuner  -> where
    Branche            hovedbranche (sekvens 0), current    -> what (DB25)
    Navn               current                              -> the trade name
    Virksomhed         the parent, by CVR number            -> ...
    Virksomhedsform    ... and its legal form               -> the privacy guard
    DAR                Adresse -> Husnummer -> Adressepunkt -> the coordinate
"""
import re
import sys

import pandas as pd

from pipeline.countries import denmark as DK
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module

BUCKET_DIVISIONS = ("47", "56", "96")
CHUNK = 500_000


def _need(path, cfg):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/{cfg.SLUG}/fetch_sources.py")
    return path


def _blank(s):
    return s.isna() | (s.astype(str).str.strip() == "")


def _read(path, usecols, keep=None):
    """Read a national CSV by `usecols`, in chunks, keeping rows `keep` says."""
    parts = []
    for ch in pd.read_csv(path, dtype=str, usecols=list(usecols), chunksize=CHUNK,
                          keep_default_na=False, na_values=[""]):
        parts.append(ch if keep is None else ch[keep(ch)])
    return pd.concat(parts, ignore_index=True)


def _premises(cfg):
    """Active production units located in the city's kommuner, with their
    hovedbranche and name. Prints every count."""
    pe = _read(_need(DK.CVR_DIR / "Produktionsenhed.csv", cfg),
               (DK.PE_ID, "pNummer", DK.PE_PARENT_CVR, DK.PE_CLOSED, DK.VALID_TO))
    print(f"CVR production units: {len(pe):,} rows nationally")
    pe = pe[_blank(pe[DK.VALID_TO])]
    before = len(pe)
    pe = pe[_blank(pe[DK.PE_CLOSED])].drop_duplicates(DK.PE_ID)
    print(f"  {len(pe):,} current and not closed ({before - len(pe):,} with an "
          f"ophoersdato)")
    ids = set(pe[DK.PE_ID])

    adr = _read(_need(DK.CVR_DIR / "Adressering.csv", cfg), DK.ADR_COLUMNS,
                lambda c: (c["AdresseringAnvendelse"] == DK.LOCATION_USE)
                & c[DK.ADR_KOMMUNE].str.lstrip("0").isin(cfg.KOMMUNER)
                & _blank(c[DK.VALID_TO]) & c[DK.JOIN_KEY].isin(ids))
    # THE c/o NAME NEVER ARRIVES. Asserted rather than trusted: this is the
    # structural claim that makes a published c/o impossible.
    leaked = [c for c in adr.columns if c in DK.FORBIDDEN_COLUMNS]
    assert not leaked, f"a forbidden column reached step 2: {leaked}"
    adr["kommune"] = adr[DK.ADR_KOMMUNE].str.lstrip("0").map(cfg.KOMMUNER)
    if adr[DK.JOIN_KEY].duplicated().any():
        sys.exit(f"{int(adr[DK.JOIN_KEY].duplicated().sum())} premises with two current "
                 f"location addresses - the `virkningTil` filter is not doing its job")
    print(f"  {len(adr):,} with a current beliggenhedsadresse in "
          + ", ".join(f"{n} {int((adr.kommune == n).sum()):,}" for n in cfg.KOMMUNER.values()))
    keep = set(adr[DK.JOIN_KEY])

    br = _read(_need(DK.CVR_DIR / "Branche.csv", cfg),
               ("sekvens", DK.JOIN_KEY, "vaerdi", "vaerdiTekst", DK.VALID_TO),
               lambda c: (c["sekvens"] == DK.MAIN_BRANCH_SEQ) & _blank(c[DK.VALID_TO])
               & c[DK.JOIN_KEY].isin(keep))
    if br[DK.JOIN_KEY].duplicated().any():
        sys.exit("a premises with two current hovedbrancher")
    nv = _read(_need(DK.CVR_DIR / "Navn.csv", cfg),
               (DK.JOIN_KEY, "sekvens", "vaerdi", DK.VALID_TO),
               lambda c: _blank(c[DK.VALID_TO]) & c[DK.JOIN_KEY].isin(keep))
    nv = (nv.assign(_s=pd.to_numeric(nv["sekvens"], errors="coerce"))
            .sort_values([DK.JOIN_KEY, "_s"]).drop_duplicates(DK.JOIN_KEY))

    df = (adr.merge(br[[DK.JOIN_KEY, "vaerdi", "vaerdiTekst"]], on=DK.JOIN_KEY, how="left")
             .merge(nv[[DK.JOIN_KEY, "vaerdi"]].rename(columns={"vaerdi": "navn"}),
                    on=DK.JOIN_KEY, how="left")
             .merge(pe[[DK.PE_ID, "pNummer", DK.PE_PARENT_CVR]],
                    left_on=DK.JOIN_KEY, right_on=DK.PE_ID, how="left"))
    print(f"  hovedbranche on {df['vaerdi'].notna().mean():.1%}, name on "
          f"{df['navn'].notna().mean():.1%}")
    return df


def _parent_forms(df, cfg):
    """The parent company's legal form, joined through its CVR number."""
    v = _read(_need(DK.CVR_DIR / "Virksomhed.csv", cfg),
              ("id", "CVRNummer", "virksomhedOphoersdato", DK.VALID_TO),
              lambda c: _blank(c[DK.VALID_TO]) & c["CVRNummer"].isin(set(df[DK.PE_PARENT_CVR])))
    v = v.drop_duplicates("CVRNummer")
    f = _read(_need(DK.CVR_DIR / "Virksomhedsform.csv", cfg),
              (DK.JOIN_KEY, "vaerdi", "vaerdiTekst", DK.VALID_TO),
              lambda c: _blank(c[DK.VALID_TO]) & c[DK.JOIN_KEY].isin(set(v["id"])))
    f = f.drop_duplicates(DK.JOIN_KEY).rename(
        columns={DK.JOIN_KEY: "id", "vaerdi": "form", "vaerdiTekst": "form_text"})
    v = v.merge(f[["id", "form", "form_text"]], on="id", how="left")
    df = df.merge(v.rename(columns={"CVRNummer": DK.PE_PARENT_CVR, "id": "parent_id",
                                    "virksomhedOphoersdato": "parent_closed"}),
                  on=DK.PE_PARENT_CVR, how="left")
    print(f"\n  parent company found for {df['parent_id'].notna().mean():.1%}, "
          f"legal form for {df['form'].notna().mean():.1%}")
    before = len(df)
    df = df[_blank(df["parent_closed"])]
    print(f"  {len(df):,} after dropping premises whose parent has ceased "
          f"({before - len(df):,})")
    df["personal_form"] = df["form"].isin(DK.SOLE_TRADER_FORMS)
    print("  legal forms (top 6):")
    for (code, text), n in df.groupby(["form", "form_text"]).size() \
            .sort_values(ascending=False).head(6).items():
        mark = "  <- personally owned: name suppressed" if code in DK.SOLE_TRADER_FORMS else ""
        print(f"      {code:>4}  {text:<40} {n:>6,}  ({n / len(df):5.1%}){mark}")
    print(f"  personally owned in all: {int(df['personal_form'].sum()):,} "
          f"({df['personal_form'].mean():.1%})")
    return df


_POINT_RE = re.compile(r"POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)")


def _dar_current(c):
    return _blank(c[DK.DAR_REG_TO]) & _blank(c[DK.DAR_VALID_TO])


def _one_per_id(df):
    """Where DAR still carries two current rows for one id, prefer the
    status the register calls in force."""
    rank = df[DK.DAR_STATUS].map(DK.DAR_STATUS_RANK).fillna(9)
    return df.assign(_r=rank).sort_values("_r").drop_duplicates(DK.DAR_ID).drop(columns="_r")


def _coordinates(df, cfg):
    """The DAR join: CVR's `Adresse` UUID -> Adresse -> Husnummer ->
    Adressepunkt. A dictionary lookup, not a geocode, and deterministic
    across drift checks. Every stage's loss is printed."""
    from pyproj import Transformer

    ids = df[DK.ADR_DAR_ID]
    print(f"\nDAR join: {ids.notna().mean():.1%} of {len(df):,} storefronts carry an "
          f"address id ({ids.nunique():,} distinct)")
    want = set(ids.dropna())
    cols = (DK.DAR_ID, DK.DAR_STATUS, DK.DAR_REG_TO, DK.DAR_VALID_TO)
    a = _read(_need(DK.DAR_DIR / "Adresse.csv", cfg), cols + (DK.DAR_ADRESSE_HUSNUMMER,),
              lambda c: c[DK.DAR_ID].isin(want) & _dar_current(c))
    print(f"  Adresse: {a[DK.DAR_ID].nunique():,} found; status "
          f"{a[DK.DAR_STATUS].value_counts().to_dict()}")
    a = _one_per_id(a)
    h = _read(_need(DK.DAR_DIR / "Husnummer.csv", cfg), cols + (DK.DAR_HUSNUMMER_POINT,),
              lambda c: c[DK.DAR_ID].isin(set(a[DK.DAR_ADRESSE_HUSNUMMER])) & _dar_current(c))
    h = _one_per_id(h)
    print(f"  Husnummer: {len(h):,} found for {a[DK.DAR_ADRESSE_HUSNUMMER].nunique():,} asked")
    pts = pd.concat([_read(_need(DK.DAR_DIR / f"Adressepunkt_{k}.csv", cfg),
                           cols + (DK.DAR_POSITION,),
                           lambda c: c[DK.DAR_ID].isin(set(h[DK.DAR_HUSNUMMER_POINT]))
                           & _dar_current(c))
                     for k in cfg.DAR_KOMMUNER], ignore_index=True)
    pts = _one_per_id(pts)
    xy = pts[DK.DAR_POSITION].str.extract(_POINT_RE).astype(float)
    to_wgs = Transformer.from_crs(DK.DAR_CRS, "EPSG:4326", always_xy=True)
    lon, lat = to_wgs.transform(xy[0].to_numpy(), xy[1].to_numpy())
    pts = pts.assign(longitude=lon, latitude=lat)
    print(f"  Adressepunkt: {len(pts):,} found for {h[DK.DAR_HUSNUMMER_POINT].nunique():,} "
          f"asked, across kommuner {', '.join(cfg.DAR_KOMMUNER)}")

    chain = (a[[DK.DAR_ID, DK.DAR_ADRESSE_HUSNUMMER]]
             .merge(h[[DK.DAR_ID, DK.DAR_HUSNUMMER_POINT]].rename(
                 columns={DK.DAR_ID: DK.DAR_ADRESSE_HUSNUMMER}), on=DK.DAR_ADRESSE_HUSNUMMER)
             .merge(pts[[DK.DAR_ID, "latitude", "longitude"]].rename(
                 columns={DK.DAR_ID: DK.DAR_HUSNUMMER_POINT}), on=DK.DAR_HUSNUMMER_POINT))
    df = df.merge(chain[[DK.DAR_ID, "latitude", "longitude"]].rename(
        columns={DK.DAR_ID: DK.ADR_DAR_ID}), on=DK.ADR_DAR_ID, how="left")
    placed = df["latitude"].notna()
    print(f"  placed {int(placed.sum()):,} of {len(df):,} ({placed.mean():.1%}); "
          f"unplaced {int((~placed).sum()):,} - no address id "
          f"{int(df[DK.ADR_DAR_ID].isna().sum()):,}, id not resolved "
          f"{int((df[DK.ADR_DAR_ID].notna() & ~placed).sum()):,}")
    if (~placed).any():
        print(f"  unplaced are personally owned {df.loc[~placed, 'personal_form'].mean():.1%} "
              f"vs {df['personal_form'].mean():.1%} overall")
    return df[placed].copy()


def _clean_trade_name(name):
    parts = str(name or "").strip().split()
    while parts and parts[-1].upper().rstrip(".") in DK.LEGAL_FORM_SUFFIXES:
        parts.pop()
    return " ".join(parts)


def build_storefronts(cfg, bbox):
    """The city's storefronts, cleaned, geolocated and labelled."""
    TAX = load_taxonomy_module(cfg.TAXONOMY_SYSTEM)
    df = _premises(cfg)

    df["db25_code"] = df["vaerdi"].map(TAX.normalise_code)
    df[cfg.RAW_CLASSIFICATION_COLUMN] = df["vaerdiTekst"].fillna("")
    df = df[df["db25_code"].str[:2].isin(BUCKET_DIVISIONS)]
    print(f"\n  {len(df):,} in DB25 divisions {'/'.join(BUCKET_DIVISIONS)}")
    struct = df["db25_code"].map(lambda c: c[:4] in TAX.NOT_PREMISES_CLASSES
                                 or c in TAX.NOT_PREMISES_CODES)
    print(f"  {int(struct.sum()):,} structurally excluded ({struct.mean():.1%}):")
    for (code, lab), n in df[struct].groupby(["db25_code", cfg.RAW_CLASSIFICATION_COLUMN]) \
            .size().sort_values(ascending=False).items():
        print(f"      {code}  {n:>6,}  {lab[:60]}")
    df = filter_to_storefront(df, cfg.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")

    df = _parent_forms(df, cfg)

    print("\n  catch-all codes (per-city call, config.CATCH_ALL_EXCLUDE):")
    upper = df["CVRAdresse_etagebetegnelse"].fillna("").str.match(r"^[1-9]")
    for code in sorted(TAX.CATCH_ALL_CODES):
        m = df["db25_code"] == code
        if not m.any():
            continue
        mark = "DROP" if code in cfg.CATCH_ALL_EXCLUDE else "keep"
        print(f"      {code}  {int(m.sum()):>6,}  ({m.mean():4.1%})  {mark}  personally "
              f"owned {df.loc[m, 'personal_form'].mean():4.0%}  above ground "
              f"{upper[m].mean():4.0%}")
    print(f"      (all storefronts: personally owned {df['personal_form'].mean():.0%}, "
          f"above ground {upper.mean():.0%})")
    before = len(df)
    df = df[~df["db25_code"].isin(cfg.CATCH_ALL_EXCLUDE)]
    print(f"  {len(df):,} after the catch-all exclusion ({before - len(df):,} dropped)")

    df = _coordinates(df, cfg)
    before = len(df)
    df = df[df["latitude"].between(bbox["lat_min"], bbox["lat_max"])
            & df["longitude"].between(bbox["lon_min"], bbox["lon_max"])]
    if len(df) != before:
        print(f"  {before - len(df):,} dropped on the sanity bounding box")

    # --- the pin's label ---------------------------------------------------
    #
    # A PERSONALLY OWNED BUSINESS'S NAME IS NEVER SHOWN, and neither is any
    # name carrying Denmark's sole-trader marker `v/` ("ved", by), whatever the
    # parent's form: the marker is followed by a person's name by definition.
    # Both show the street address instead - Paris's and Oslo's fallback.
    addr_text = (df["CVRAdresse_vejnavn"].fillna("").str.strip() + " "
                 + df["CVRAdresse_husnummerFra"].fillna("").str.strip()).str.strip()
    trade = df["navn"].map(_clean_trade_name)
    marker = df["navn"].fillna("").str.contains(DK.SOLE_TRADER_MARKER, regex=True)
    df["name_is_address"] = df["personal_form"] | marker | (trade == "")
    df["business_name"] = trade.where(~df["name_is_address"], addr_text)
    print(f"\n  trade name shown on {int((~df['name_is_address']).sum()):,} rows "
          f"({(~df['name_is_address']).mean():.1%}); the address on the rest - "
          f"personally owned {int(df['personal_form'].sum()):,}, the v/ marker on a "
          f"company form {int((marker & ~df['personal_form']).sum()):,}")

    out = df.rename(columns={"pNummer": "pnummer"})[
        ["pnummer", "business_name", "name_is_address", "latitude", "longitude",
         cfg.RAW_CLASSIFICATION_COLUMN, "db25_code"]]
    if out["pnummer"].duplicated().any():
        sys.exit("a P-number appears twice after the join")
    return out
