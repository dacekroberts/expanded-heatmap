"""Hong Kong: FEHD's licence types - 20 codes across three registers, with the
labels shipped inside each download (`<TYPE_CODE>`), and a catch-all share of
ZERO: every code names a specific trade, so there is no level to choose
(premises-taxonomy's deciding measurement, run in the brief).

Keyed on the CODE (`licence_code`), with the file's own label as the tooltip
value (`licence_type`). A code not listed here raises in step 2 rather than
falling out silently - the registers are small enough that a new licence type
should be read, not guessed.

Scope follows every other city's three buckets, which is NAICS's line:
  * restaurants are Food service;
  * the food SHOPS (fresh provisions, bakeries, siu mei and lo mei) are Retail -
    the only retail Hong Kong licenses at all: clothing, electronics and
    general shops have no register, so the map is food-heavy by construction;
  * a commercial bathhouse is Personal services (NAICS 812199);
  * cinemas, karaoke and places of public entertainment are OUT, as NAICS 512
    and 713 are out everywhere else; and so are factories, cold stores, factory
    canteens, swimming pools and the funeral and offensive trades, which are not
    shopfronts at all.
"""

FIELD_LABEL = "Licence type"
VALUE_COLUMN = "licence_type"
EXTRA_COLUMNS = ("licence_code",)

CODE_TO_BUCKET = {
    # Restaurants register
    "RL": "Food service",     # General Restaurant Licence
    "RR": "Food service",     # Light Refreshment Restaurant Licence
    "MR": "Food service",     # Marine Restaurant Licence
    # Other food register
    "FP": "Retail",           # Fresh Provision Shop
    "FB": "Retail",           # Bakery
    "FS": "Retail",           # Siu Mei and Lo Mei Shop
    "CL": "Retail",           # Composite Food Shop - in TYPE_CODE, 0 rows on 2026-09-25
    "FF": None,               # Food Factory - manufacturing
    "FG": None,               # Frozen Confection Factory
    "FE": None,               # Factory Canteen - not public-facing
    "FC": None,               # Cold Store
    "FM": None,               # Milk Factory
    # Non-food register
    "TC": "Personal services",  # Commercial Bathhouse
    "PE": None,               # Public Entertainment - NAICS 713, out everywhere
    "PC": None,               # Cinema / Theatre - NAICS 512, out everywhere
    "KE": None,               # Karaoke Establishment
    "TP": None,               # Swimming Pool
    "TU": None,               # Undertaker's
    "TF": None,               # Funeral Parlour
    "TO": None,               # Offensive Trade
    "TS": None,               # Slaughterhouse
}
STOREFRONT_CODES = {c for c, b in CODE_TO_BUCKET.items() if b}


def legend_label(bucket: str) -> str:
    return {"Retail": "Food shops", "Personal services": "Bathhouses"}.get(bucket, bucket)


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    code = str(row.get("licence_code") or "").strip().upper()
    if code not in CODE_TO_BUCKET:
        raise ValueError(f"unmapped FEHD licence code {code!r} - read its label in the "
                         f"file's TYPE_CODE block and map it in {__name__}")
    return CODE_TO_BUCKET[code]
