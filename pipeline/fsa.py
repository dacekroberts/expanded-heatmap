"""The UK Food Standards Agency's open-data files, read the same way for every
city on them (London, Glasgow; Newcastle next). Read-only: nothing here
fetches - each city's fetch_sources.py downloads.

One file per local authority, England's FHRS and Scotland's FHIS alike (the
business types are the same 14; only the rating differs, and no rating is
ever read). Three rules live here so the next city passes through them:

  * **READ** - only these fields are read: never the rating, scores, phone or
    the authority's contact details. The address lines are read ONLY for the
    flat rule and are never written out.
  * **THE FLAT RULE** (owner, 2026-09-28): a storefront whose address line
    starts "Flat" is never placed. Glasgow City publishes home bakers and
    cooks as "Restaurant/Cafe/Canteen" at full tenement-flat addresses WITH
    the FSA's point (185 of 4,958 storefronts), and London's files carry 93.
    The FSA's own guard - a private address gets no point and an outward
    postcode only - catches neither, so the project's rule (a trade name,
    never a person's own name at what looks like their home) needs its own.
    A few real ground-floor shops go with them; that is the cost, disclosed.
  * **THE CHILDMINDER RULE** (owner, 2026-09-28): a storefront whose name
    says "childminder" or "childminding" is never placed. Glasgow City lists
    childminders as "Restaurant/Cafe/Canteen" at their house, three of five
    under the childminder's own name ("Andrea Stewart - Childminder"); London
    has none. Not a food storefront, and home-based by definition.
  * **THE TRADING-AS RULE** (owner, 2026-09-28): "X T/A Y" shows Y, the name
    on the shop.
"""
import re
import sys
import xml.etree.ElementTree as ET

import pandas as pd

READ = ("FHRSID", "BusinessName", "BusinessType", "PostCode", "LocalAuthorityName")
ADDRESS_LINES = ("AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4")
# "T/A", "t/a", "Also T/A", "(Trading as ...)", "trading as" - a whole word, so
# "Ta Va" (a restaurant) is untouched.
TRADING_AS = r"(?i)\s*\(?\b(?:also\s+)?(?:t/a|trading\s+as)\b\s*"
FULL_POSTCODE = r"^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$"
OUTWARD_POSTCODE = r"^[A-Z]{1,2}\d[A-Z\d]?$"
# An address line that starts with the word "Flat": "Flat 2/1" (a Glasgow
# tenement's floor/door), "Flat 22 Frognal Court", "Flat A". Not "Flatiron".
FLAT_ADDRESS = r"(?i)^\s*flat\b"
# "Childminder", "Childminding", "Child minder".
CHILDMINDER = r"(?i)\bchild\s*-?\s*mind(?:er|ing)\b"


def load(files):
    """Every establishment in the given authority files, READ's fields plus
    the FSA's point and a `flat_address` flag."""
    rows = []
    for f in files:
        for e in ET.parse(f).getroot().iter("EstablishmentDetail"):
            r = {k: (e.findtext(k) or "").strip() for k in READ}
            r["longitude"] = e.findtext("Geocode/Longitude") or ""
            r["latitude"] = e.findtext("Geocode/Latitude") or ""
            r["flat_address"] = any(re.match(FLAT_ADDRESS, e.findtext(k) or "")
                                    for k in ADDRESS_LINES)
            rows.append(r)
    return pd.DataFrame(rows)


def drop_home_premises(df):
    """The flat rule and the childminder rule, applied to storefront rows
    before any placement."""
    flat = df["flat_address"]
    print(f"  {int(flat.sum()):,} at a 'Flat' address, never placed (the flat rule); by type:")
    for t, n in df.loc[flat, "BusinessType"].value_counts().items():
        print(f"    {t:<40} {n:>5,}")
    minder = ~flat & df["BusinessName"].str.contains(CHILDMINDER, regex=True)
    print(f"  {int(minder.sum()):,} more named as a childminder, never placed (the childminder rule)")
    return df[~flat & ~minder].drop(columns="flat_address")


def trade_names(df):
    """The name on the shop: "Skinner Stores T/A Londis" and "Lydia Oduro
    Enterprise Trading as LO" show what follows the trading-as marker - the
    trade name, which is also what keeps a sole trader's own name off the map
    where they registered both (the owner's rule, 2026-09-28)."""
    tas = df["BusinessName"].str.split(TRADING_AS, n=1, regex=True)
    has = tas.str.len() == 2
    shown = tas.str[-1].str.strip().str.strip("()").str.strip()
    print(f"  {int(has.sum()):,} names carry a trading-as marker; the trade name after it is shown")
    return df.assign(BusinessName=df["BusinessName"].where(~has | (shown == ""), shown))


def codepoint(zip_path, district_prefix, crs_source, crs_geographic, fetch_hint):
    """Postcode unit centroids from OS Code-Point Open, WGS84, indexed by
    postcode without spaces, for units whose district code starts with
    `district_prefix` (London's boroughs: "E09")."""
    import io
    import zipfile
    from pyproj import Transformer
    if not zip_path.exists():
        sys.exit(f"missing {zip_path.name}: run {fetch_hint}")
    cols = ["pc", "pq", "e", "n", "cy", "rh", "lh", "cc", "dc", "wc"]
    z = zipfile.ZipFile(zip_path)
    parts = [pd.read_csv(io.BytesIO(z.read(n)), header=None, names=cols, dtype=str)
             for n in z.namelist() if n.startswith("Data/CSV/") and n.endswith(".csv")]
    cp = pd.concat(parts)
    cp = cp[cp["dc"].fillna("").str.startswith(district_prefix)]
    t = Transformer.from_crs(crs_source, crs_geographic, always_xy=True)
    lon, lat = t.transform(cp["e"].astype(float).to_numpy(), cp["n"].astype(float).to_numpy())
    cp = cp.assign(latitude=lat, longitude=lon, key=cp["pc"].str.replace(r"\s+", "", regex=True))
    return cp.drop_duplicates("key").set_index("key")
