"""Taiwan: the national business tax register's 6-digit industry code
(行業代號), keyed at its ISIC-aligned DIVISION - the brief's measurement
(taipei.md): 47/48 Retail, 56 Food service, 96 Personal services, and 487
(online shopping, NAICS 454's twin) excluded.

`industry` is what the tooltip shows: the register's own name for the code,
in Chinese. `industry_code` carries the code itself.
"""
from pipeline.countries.taiwan import bucket_of

FIELD_LABEL = "Kind"
VALUE_COLUMN = "industry"
EXTRA_COLUMNS = ("industry_code",)


def classify(row):
    return bucket_of(str(row.get("industry_code", "")))


def legend_label(bucket):
    return bucket
