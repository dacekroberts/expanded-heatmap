"""Milan: the register a premises came from IS its classification.

WHY THERE IS NO MAPPING TABLE HERE. Milan publishes six premises registers and
every in-dataset classification field is unusable: `codice_ateco` is 7.1%
populated, `settore_merceologico` carries 66 distinct values for what should be
three (half of it pure case variation, plus 2,759 concatenated rows),
`tipo_eser_storico_pe` is 60% blank and `settore_storico_pe` 64%. Measured
2026-09-22; see docs/build_briefs/milan.md.

`Area di Competenza` is the one clean field - a single value per dataset, at
100%, in all six - and it says which register the row is in. So the bucket is
the register, which is `multi-source-city`'s "membership is often the
classification" in its purest form: do not build a mapping table where a
constant will do.

This is the same dispatching shape as New York's taxonomy - `EXTRA_COLUMNS`
carrying a `source` column that `classify()` switches on - and the mechanism
needed no change to `map_common.py`, which is the point of having it.

THE ONE JUDGMENT CALL, and it is not the register's: a food SHOP is Retail,
not Food service. Bakers (`panificatori`) and the alimentare half of
`vicinato` sell goods; the *pubblici esercizi* sell consumption on the
premises. That is the NAICS 445-vs-722 line every other city here follows, and
Dublin drew it the same way for its BAKERY value.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "attivita"

# Step 2 writes `source`; classify() dispatches on it. The mechanism predates
# this city (Chicago's business_activity, New York's four registries).
EXTRA_COLUMNS = ("source",)

# register key -> bucket. Mirrors pipeline/milan/config.py's SOURCES, and is
# asserted against it by step 2 so the two cannot drift apart.
SOURCE_BUCKETS = {
    "vicinato": "Retail",
    "panificatori": "Retail",
    "pe_in_piano": "Food service",
    "pe_fuori_piano": "Food service",
    "artigianato_alim": "Food service",
    "servizi_persona": "Personal services",
}


# --- the tooltip's activity line -------------------------------------------
#
# WHY RULES AND NOT A REGEX. The first version normalised case and split
# concatenations with a `(?<=[a-z])(?=[A-Z])` seam, and it failed three ways at
# once on real values: `non alimentare` / `Non Alimentare` / `Alimentare`
# survived as three labels because only ALL-CAPS was being folded;
# `alimentarenon alimentare` has a lower-to-lower seam so it was never split;
# and `BAR CAFFTavola fredda` has an upper-to-upper one. The vocabulary is
# small and bounded per register, so it is written out instead of guessed at.
#
# Order matters - first match wins - so the more specific pattern comes first.
# Anything unmatched falls back to the register's own name, which is always
# true even when it is uninformative.
import re as _re

_RULES = {
    "vicinato": [
        # `settore_merceologico` only distinguishes food from non-food, plus
        # the three "tabella speciale" licensed trades. That IS its whole
        # vocabulary; the concatenated values mean the premises does both.
        (r"tabella speciale.*monopoli|monopoli", "Tobacconist"),
        (r"tabella speciale.*farmaci|farmaci", "Pharmacy"),
        (r"tabella speciale.*carburant|carburant", "Fuel"),
        (r"aliment.*non aliment|non aliment.*aliment", "Food and non-food shop"),
        (r"non aliment", "Non-food shop"),
        (r"aliment", "Food shop"),
    ],
    "panificatori": [(r".*", "Bakery")],
    "artigianato_alim": [
        (r"pizzeria", "Pizzeria"), (r"gelateri", "Ice cream"),
        (r"pasticceri", "Pastry shop"), (r"gastronomi", "Delicatessen"),
        (r"kebab", "Kebab"), (r"rosticceri", "Rotisserie"),
        (r"pasta", "Fresh pasta"), (r"piadineri", "Piadineria"),
    ],
    "pe_in_piano": [
        (r"ristorante|trattoria|osteria", "Restaurant"),
        (r"pizzeri", "Pizzeria"),
        (r"bar pasticceria|bar gelateria|cremeria|creperia", "Cafe patisserie"),
        (r"wine bar|birreri|pub|enotec", "Bar or pub"),
        (r"bar gastronomic", "Cafe"), (r"bar caff", "Cafe"),
        (r"tavola calda|self service|fast food", "Fast food"),
        (r"tavola fredda", "Cold buffet"), (r"gelateri", "Ice cream"),
        (r"spaccio bevande", "Drinks shop"),
    ],
    "pe_fuori_piano": [
        (r"bar caff", "Cafe"), (r"tavola fredda", "Cold buffet"),
        (r"tavola calda|self service|fast f", "Fast food"),
        (r"ristorante|trattoria|osteria", "Restaurant"),
        (r"genere merceol", "Licensed food and drink"),
    ],
    "servizi_persona": [
        (r"parrucchier|acconciator", "Hairdresser"),
        (r"barbier", "Barber"),
        (r"estetist|centro benessere|centro massaggi|beauty", "Beauty salon"),
        (r"abbronzatur", "Tanning salon"),
        (r"tatuagg|piercing", "Tattoo and piercing"),
        (r"discipline bionatural", "Wellbeing practice"),
        # `TIPO A - REG.2003` and `TIPO A-B-C-D` are REGULATORY CLASSES under
        # the 2003 hygiene regulation, not activities. They are the single
        # commonest value in this register (1,333 rows) and say nothing a
        # reader could use, so they fall through to the register's own name.
    ],
}
_COMPILED = {k: [(_re.compile(p, _re.I), label) for p, label in v]
             for k, v in _RULES.items()}


def activity_label(source, value, fallback):
    """One register's dirty classification value -> one readable phrase."""
    s = _re.sub(r"\s+", " ", str(value or "")).strip()
    if not s or s.lower() in ("none", "nan", "-"):
        return fallback
    for pattern, label in _COMPILED.get(source, ()):
        if pattern.search(s):
            return label
    return fallback


def classify(row):
    """A cleaned row -> a bucket name, or None if its source is unknown.

    Returns None rather than raising on an unexpected source, because
    `filter_to_storefront` uses None to mean "not a tracked storefront" - but
    step 2 asserts the source set first, so an unknown one cannot arrive here
    silently.
    """
    return SOURCE_BUCKETS.get(str(row.get("source", "")).strip())


def legend_label(bucket):
    return bucket
