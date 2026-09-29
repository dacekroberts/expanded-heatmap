"""Montréal: naics.py with ONE per-city exemption - caterers stay on the map.

naics.py excludes NAICS 72232 (caterers) for every city: food with no counter
of its own (owner, 2026-09-29). Montréal is exempt (owner, 2026-09-29), for the
reason France's traiteurs (NAF 56.21Z) are kept: its source is a STREET SURVEY
of commercial premises, not a licence register, so a 722320 row here is a unit
a surveyor walked past - traiteur shops with a counter (Gisèle Gauthier
Traiteur, Yves Grenier Traiteur, Meme traiteur) and small restaurants filed
under the caterer code. 107 pins on the committed map.

WHY A MODULE AND NOT A CONFIG LIST. The per-city override that already exists,
`NAICS_EXCLUDE_CODES` in a city's config, is a filter step 2 applies. An
exemption cannot work that way: `classify()` itself decides the bucket, and it
is called again by the map (pipeline/map_common.py groups pins by it), so a
row step 2 re-admitted would still fall out of every layer. So the exemption
lives in classification, as a thin wrapper that changes nothing else - same
field label, value column and legend as naics.py.
"""
from pipeline.taxonomies import naics as _naics

FIELD_LABEL = _naics.FIELD_LABEL
VALUE_COLUMN = _naics.VALUE_COLUMN
legend_label = _naics.legend_label

# Exact six-digit codes naics.py excludes that Montréal keeps, with the bucket
# naics.py's groups would have given them (owner, 2026-09-29).
KEEP_CODES = {"722320": "Food service"}


def classify(row: dict):
    """Taxonomy-module interface: naics.classify(), except KEEP_CODES."""
    code = str(row.get(VALUE_COLUMN) or "").strip()
    if code in KEEP_CODES:
        return KEEP_CODES[code]
    return _naics.classify(row)


# The exemption is exactly one code wide: the caterers come back, the other
# no-counter codes and the catch-all stay out, and everything else is naics.py.
assert _naics.naics_group("722320") is None, "naics.py must still exclude caterers nationally"
for _c, _want in [("722320", "Food service"), ("722310", None), ("722330", None),
                  ("812990", None), ("812210", None), ("722511", "Food service"),
                  ("445110", "Retail"), ("812112", "Personal services")]:
    assert classify({VALUE_COLUMN: _c}) == _want, (_c, classify({VALUE_COLUMN: _c}), _want)
