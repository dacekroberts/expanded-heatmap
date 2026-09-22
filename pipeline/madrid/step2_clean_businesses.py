"""Step 2 - Madrid's premises, from the Ayuntamiento's Censo de locales.

A PREMISES FIELD SURVEY, not a licence register: a row is a unit on the street
with an activity recorded against it. That is the shape Montreal and Barcelona
have and the one this project's premise is actually about, so the usual
"79% of this register is landlords" correction does not apply here.

Four things this step has to get right:

  - **The download URL rots.** It embeds a build timestamp, so it is resolved
    from `package_show` by RESOURCE ID at fetch time. A hardcoded URL 404s
    silently within days.
  - **The coordinate column is 100% populated and partly invalid** - 34,316
    open rows carry a literal zero stored as the STRING '0.0', which projects
    to the Atlantic off West Africa and vanishes on a station-radius map rather
    than erroring.
  - **The file is a locales x actividades JOIN**, so a premises with two
    activities is two rows at identical coordinates. Left alone that
    double-counts a storefront.
  - **No column here names a person, and that is structural rather than
    lucky** - see FORBIDDEN_COLUMNS below.
"""

import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.madrid.config import (  # noqa: E402
    BUSINESSES_CKAN_API,
    BUSINESSES_CKAN_PACKAGE,
    BUSINESSES_CKAN_RESOURCE,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    COORD_X_COLUMN,
    COORD_Y_COLUMN,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DATA_PROCESSED,
    DISTRICT_COLUMN,
    MADRID_BBOX_25830,
    MADRID_DISTRICT_COUNT,
    PREMISES_ID_COLUMN,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_DELIMITER,
    SOURCE_ENCODING,
    STATUS_COLUMN,
    STATUS_KEEP,
    TAXONOMY_SYSTEM,
    TRADE_NAME_COLUMN,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

UA = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}

# THE REGISTER CARRIES NO REGISTRANT NAME AT ALL, which is a stronger claim
# than "we chose not to publish it". All 47 columns were listed on 2026-09-22
# and none is an owner, titular, NIF/CIF, razon social or contact field - the
# only name-shaped column is `nombre_agrupacion`, the name of a MARKET or
# SHOPPING CENTRE a unit sits inside, and it is not loaded either.
#
# So Madrid can make New York's structural claim: no pin CAN be a person's
# name, because the source has none to fall back to. `rotulo` is the shop sign
# and is 100% populated on the rows this step keeps, so there is never a reason
# to fall back at all. This assertion is what keeps that true if the publisher
# widens the file.
FORBIDDEN_COLUMNS = (
    "titular", "nombre_titular", "propietario", "nif", "cif", "dni",
    "razon_social", "apellidos", "persona_contacto", "telefono", "correo",
    "email",
)

# Loading columns by name IS the privacy control - an unlisted column cannot
# reach the output by accident.
USECOLS = [
    PREMISES_ID_COLUMN, DISTRICT_COLUMN, STATUS_COLUMN,
    COORD_X_COLUMN, COORD_Y_COLUMN, TRADE_NAME_COLUMN,
    "desc_seccion", "desc_division", RAW_CLASSIFICATION_COLUMN,
    # Street text, carried ONLY so scripts/check_personal_exposure.py has
    # something to run its unit-indicator regex over. Not published: the
    # map needs coordinates, and processed/ is gitignored.
    "desc_vial_edificio", "num_edificio",
]

# Which activity wins when one premises carries several. Only 1,535 premises
# (2.88% of those kept) have activities in DIFFERENT buckets, almost all of them
# Food service + Retail - the panaderia with tables, the wine shop with a bar.
#
# Food service first because a premises with seating reads as what it serves;
# personal services next as the next most specific premises type; Retail last
# because it is the broadest bucket and the likeliest SECONDARY activity of a
# shop that also does something else. Chicago's LICENSE_PRIORITY is the
# precedent - most specific identification wins.
#
# At 2.88% no ordering changes a conclusion, which is the honest reason this is
# a stated convention rather than a researched one.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]


def resolve_download_url():
    url = f"{BUSINESSES_CKAN_API}?id={BUSINESSES_CKAN_PACKAGE}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        pkg = json.loads(r.read())["result"]
    for res in pkg["resources"]:
        if res["id"] == BUSINESSES_CKAN_RESOURCE:
            return res["url"]
    raise SystemExit(f"resource {BUSINESSES_CKAN_RESOURCE} not in the package")


def main():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    if not BUSINESSES_RAW_CSV.exists():
        url = resolve_download_url()
        print(f"resolved {BUSINESSES_CKAN_RESOURCE} -> {url}")
        BUSINESSES_RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=1800) as r:
            BUSINESSES_RAW_CSV.write_bytes(r.read())
        print(f"  downloaded {BUSINESSES_RAW_CSV.stat().st_size:,} bytes")

    header = pd.read_csv(BUSINESSES_RAW_CSV, sep=SOURCE_DELIMITER,
                         encoding=SOURCE_ENCODING, dtype=str, nrows=1).columns
    leaked = [c for c in header if c.lower() in FORBIDDEN_COLUMNS]
    if leaked:
        raise SystemExit(f"the register now carries {leaked} - a registrant-name "
                         "column. Re-read the privacy position before using it.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, sep=SOURCE_DELIMITER,
                     encoding=SOURCE_ENCODING, dtype=str, usecols=USECOLS,
                     low_memory=False)
    print(f"\nrows in the locales x actividades join     {len(df):>9,}")
    print(f"  distinct premises (id_local)             {df[PREMISES_ID_COLUMN].nunique():>9,}")

    df = df[df[STATUS_COLUMN].str.strip().eq(STATUS_KEEP)].copy()
    print(f"open ({STATUS_KEEP})                          {len(df):>9,}")

    # THE ZEROS. Stored as the string '0.0', so an is-it-populated test passes
    # them; only a numeric test catches them.
    x = pd.to_numeric(df[COORD_X_COLUMN], errors="coerce")
    y = pd.to_numeric(df[COORD_Y_COLUMN], errors="coerce")
    zero = (x.fillna(0) == 0) | (y.fillna(0) == 0)
    print(f"  dropped literal-zero coordinates         {int(zero.sum()):>9,}"
          f"   ({100 * zero.mean():.2f}% of open rows)")
    df, x, y = df[~zero].copy(), x[~zero], y[~zero]

    bbox = MADRID_BBOX_25830
    inside = (x.between(bbox["x_min"], bbox["x_max"])
              & y.between(bbox["y_min"], bbox["y_max"]))
    if (~inside).sum():
        print(f"  dropped out-of-bounds coordinates        {int((~inside).sum()):>9,}")
    df, x, y = df[inside].copy(), x[inside], y[inside]
    df["_x"], df["_y"] = x, y
    print(f"with usable coordinates                    {len(df):>9,}")

    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"in the three storefront buckets            {len(df):>9,}"
          f"   (dropped {before - len(df):,})")

    module = load_taxonomy_module(TAXONOMY_SYSTEM)
    df["bucket"] = [module.classify(r) for r in df.to_dict("records")]
    print(df["bucket"].value_counts().to_string().replace("\n", "\n    "))

    # ONE PIN PER PREMISES. The join puts a premises on one row per activity at
    # IDENTICAL coordinates (verified: max 1 distinct x and y per id_local), so
    # leaving them would draw one storefront as two and inflate density.
    multi = df.groupby(PREMISES_ID_COLUMN)["bucket"].nunique()
    print(f"\npremises with activities in >1 bucket      {int((multi > 1).sum()):>9,}"
          f"   ({100 * (multi > 1).mean():.2f}%)")
    df["_rank"] = df["bucket"].map({b: i for i, b in enumerate(BUCKET_PRIORITY)})
    df = (df.sort_values([PREMISES_ID_COLUMN, "_rank"])
            .drop_duplicates(PREMISES_ID_COLUMN, keep="first"))
    print(f"one pin per premises                       {len(df):>9,}")

    # MADRID HAS 21 DISTRICTS, and this check earned its place by catching the
    # build brief claiming 22 - a cached Step 0 error, which is exactly what
    # `brief_check.py` exists for and what CLAUDE.md warns a brief does with its
    # mistakes. The register carries `id_distrito_local` 1..21 and the 21 names
    # are Madrid's official ones, so the DATA was complete and only the claim
    # about it was wrong. Raises rather than warns: a count that moves means the
    # scope moved, and that is not something to print past.
    districts = df[DISTRICT_COLUMN].nunique()
    if districts != MADRID_DISTRICT_COUNT:
        raise SystemExit(
            f"{districts} districts, expected {MADRID_DISTRICT_COUNT}. Either the "
            "register's scope changed or a filter above is dropping a district - "
            "find out which before mapping this.")
    print(f"  across all {districts} districts")

    pts = (pd.DataFrame({"x": df["_x"], "y": df["_y"]}))
    geo = __import__("geopandas").GeoSeries(
        __import__("geopandas").points_from_xy(pts.x, pts.y),
        crs=CRS_PROJECTED).to_crs(CRS_GEOGRAPHIC)

    out = pd.DataFrame({
        "business_name": df[TRADE_NAME_COLUMN].values,
        "latitude": geo.y.values,
        "longitude": geo.x.values,
        RAW_CLASSIFICATION_COLUMN: df[RAW_CLASSIFICATION_COLUMN].values,
        "desc_division": df["desc_division"].values,
        "bucket": df["bucket"].values,
        # The register PADS this field ("LATINA              ").
        "distrito": df[DISTRICT_COLUMN].str.strip().values,
        "address": (df["desc_vial_edificio"].fillna("").str.strip() + " "
                    + df["num_edificio"].fillna("").str.strip()).str.strip().values,
    })

    # rotulo is the shop sign and is 100% populated on the rows kept - assert it
    # rather than assume it, because a fallback is what published ~4,000 names
    # in Los Angeles.
    blank = out["business_name"].isna() | out["business_name"].str.strip().eq("")
    if blank.any():
        raise SystemExit(f"{int(blank.sum())} kept premises have no rotulo - "
                         "there is no name to show and no fallback is acceptable")
    print(f"  every kept premises has a rotulo (shop sign)")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\nWrote {len(out):,} premises to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
