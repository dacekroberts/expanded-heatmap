"""Seattle (Regional) taxonomy - a DISPATCHING taxonomy over five sources, New
York's shape (the multi-source-city skill), because no one register covers
the eleven cities Link serves (pipeline/seattle/config.py has the table).

  source      register                                        bucket
  ----------  ----------------------------------------------  -----------------------
  seattle     City of Seattle, Business Locations (Active)    NAICS, through naics.py
  bellevue    City of Bellevue, Business Licenses (All)       NAICS, through naics.py
                                                              (Retail and Personal
                                                              services only: Bellevue's
                                                              food is King County's)
  kc_food     Public Health - Seattle & King County, food     by `classification`
              inspections (r878-4sxa)                         (below)
  sno_food    Snohomish County, Food Service Establishments   Restaurant -> Food service,
              (2025)                                          Grocery -> Retail
  lcb_retail  WA Liquor and Cannabis Board, off-premise       Retail (shops licensed to
              licensees                                       sell alcohol)

The two city registers carry real NAICS, so they are bucketed by naics.py
unchanged and every national carve-out applies (Montreal's way: no new
mapping where NAICS already answers). `naics` is an extra column for those
rows; `business_category` is what the tooltip shows, each source's own words
(a NAICS title, an inspection classification, a privilege).

A food register's shops are shops (New York's and Minneapolis's precedent):
King County's grocery stores, meat and fish markets and bakeries are Retail,
and the map's Retail legend says so.
"""
from pipeline.taxonomies import naics

SOURCES = ("seattle", "bellevue", "kc_food", "sno_food", "lcb_retail")

# Which source wins when one site is in several (step 2's dedup): a food
# inspection names a restaurant most specifically; then the city registers;
# the Liquor Board's off-premise privilege last, since it is a permission a
# shop holds (an adjunct licence, the multi-source-city skill's Step 5).
SOURCE_PRIORITY = ("kc_food", "sno_food", "seattle", "bellevue", "lcb_retail")

# King County's `classification` -> bucket. Every value the register uses is
# listed here or in KC_CLASSIFICATION_OUT; step 2 asserts it.
KC_CLASSIFICATION_TO_BUCKET = {
    "GENERAL FOOD SERVICES": "Food service",
    "GENERAL FOOD SERVICE": "Food service",
    "LIMITED FOOD SERVICE": "Food service",
    "GROCERY STORE": "Retail",
    "MEAT/FISH MARKET": "Retail",
    # A retail bakery (the inspection program's own class), a shop.
    "BAKERY": "Retail",
}
# Downloaded but never a pin, each with its rule.
KC_CLASSIFICATION_OUT = {
    "MOBILE FOOD UNIT": "Mobile food (category_rules R1)",
    "SCHOOL LUNCH PROGRAM": "An institutional kitchen (R1)",
    "CATERING OPERATION": "An event caterer, no counter (R1)",
    "NONPROFIT INSTITUTION": "An institutional kitchen (R1)",
    "COMMISSARY KITCHEN": "A shared production kitchen, no counter (R1)",
    "COMMISSARY KITCHEN EXEMPT FROM": "A shared production kitchen, no counter (R1)",
    "DFDO": "A donated-food distributing organization, no counter (R1)",
    "DFDO EXEMPT FROM BILLING": "A donated-food distributing organization, no counter (R1)",
    "BED AND BREAKFAST OPERATION": "Lodging (out in every city)",
}

SNO_ICON_TO_BUCKET = {"RESTAURANT": "Food service", "GROCERY": "Retail"}

LCB_BUCKET = "Retail"

FIELD_LABEL = "Category"
VALUE_COLUMN = "business_category"
EXTRA_COLUMNS = ("source", "naics")


def legend_label(bucket: str) -> str:
    return {"Retail": "Retail (including food and liquor shops)"}.get(bucket, bucket)


def classify(row: dict):
    """Dispatch on `source`. An unknown source is a step 2 bug and raises."""
    source = (row.get("source") or "").strip()
    if not source:
        return None
    if source in ("seattle", "bellevue"):
        code = str(row.get("naics") or "").strip()
        bucket = naics.naics_group(code) if code else None
        # Bellevue's food comes from King County's inspections (owner,
        # 2026-10-02), so its own food rows never become pins.
        if source == "bellevue" and bucket == "Food service":
            return None
        return bucket
    value = (row.get(VALUE_COLUMN) or "").strip().upper()
    if source == "kc_food":
        return KC_CLASSIFICATION_TO_BUCKET.get(value)
    if source == "sno_food":
        return SNO_ICON_TO_BUCKET.get(value)
    if source == "lcb_retail":
        return LCB_BUCKET
    raise ValueError(f"Unknown Seattle (Regional) source {source!r}; expected one of {SOURCES}")
