"""NAF rév. 2 - France's national activity classification, keyed at the
sous-classe (level 5).

**NATIONAL, NOT PER-CITY.** NAF is INSEE's, and `pipeline/countries/france.py`
names five cities that inherit it (`BUILD_SEQUENCE`: paris, marseille,
toulouse, lille, rennes). Every other local taxonomy in this directory belongs
to one city because the register belongs to one city; SIRENE is one register
for the whole country, so this module is written once and a correction here
reaches all five. Per-city verdicts do NOT belong in this file - see
"What this module deliberately does NOT decide" below.

**WHY THE SOUS-CLASSE, THE FINEST LEVEL.** `premises-taxonomy`'s deciding
measurement, run 2026-09-22 on 6,895 active Paris rows against INSEE's own
label file (`int_courts_naf_rev_2.xls`, 1,707 codes):

    level             distinct   catch-all
    division (2)             3       18.7%
    groupe   (3)            13       49.4%
    classe   (4)            46       27.8%
    sous-classe (5)         62       19.3%

Keying at *groupe* would put **half of Paris in "other"**. This is Barcelona's
shape (finest level, 2.6% there) and not Madrid's (near the top of an
identically-shaped scheme) - and the point of that skill is that both are
right and neither is a default to inherit.

**THE THREE DIVISIONS.** The project's three buckets map onto exactly three NAF
divisions, which is unusually clean:

    47  Commerce de détail          -> Retail            (50 sous-classes)
    56  Restauration                -> Food service      ( 7)
    96  Autres services personnels  -> Personal services ( 7)

64 codes exist across them; the brief measured 62 distinct in Paris, so two
simply do not occur there. Anything outside these divisions returns None -
that is how wholesale, manufacturing, offices and the rest of a national
register stay off the map.

**THE LABELS ARE INSEE'S, VERBATIM.** `NAF_LABELS` carries the full official
wording from column 2 of the label file. INSEE also ships a 40-character form,
and it was rejected: "Com. dét. quinc. pein. etc. (mag.<400m2)" is not
something to put in front of a reader. Nothing here is text this project
invented or abbreviated, which matters because the map displays it.

Embedding the table also keeps step 2 offline - it never needs the .xls, so
`check_no_fetch_in_steps.py` stays satisfied without a fetch script for it.
"""

# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

FIELD_LABEL = "Activité (NAF)"

# The human-readable French label, which is what a tooltip shows. Step 2
# derives it from the code with `label_for()`; the code itself rides along in
# EXTRA_COLUMNS so `classify()` matches on the code and never on label text.
# Matching on a label would be a string comparison against accented French -
# exactly the fragility that broke Milan's label normaliser three ways.
VALUE_COLUMN = "naf_label"
EXTRA_COLUMNS = ("naf_code",)

# The source column in SIRENE, for the city config's RAW_CLASSIFICATION_COLUMN.
# Kept here rather than in each config so the five cities cannot drift apart.
#
# ⚠ THIS IS NAF rev. 2, AND SIRENE ALSO PUBLISHES NAF 2025. Do not switch the
# column without rebuilding NAF_LABELS: the two schemes share division and
# class numbers but NOT the sous-classe letter - rev. 2's `01.11Z` is NAF
# 2025's `01.11Y` - so pointing this at `activitePrincipaleNAF25Etablissement`
# makes every lookup below miss and `classify()` return None for every row.
# That empties the map; it does not raise. Measured 2026-09-23: rev. 2 is 100%
# populated, NAF 2025 is 37.5%. See `pipeline/countries/france.py`'s
# NAF25_COLUMN block for the decision and the watch item.
SIRENE_COLUMN = "activitePrincipaleEtablissement"


# ---------------------------------------------------------------------------
# What this module deliberately does NOT decide
# ---------------------------------------------------------------------------
#
# CLAUDE.md: "Sample the catch-all classification codes for this city, and
# decide... Put the verdict in the city's own config." A catch-all's
# composition is a fact about a city, not about the classification, so the
# verdict is per-city and lives in `pipeline/<city>/config.py` as an exclusion
# list - Los Angeles' NAICS_EXCLUDE_CODES is the worked example.
#
# These are the codes that need that treatment. They are classified normally
# here; excluding one is a city's call, made from a sample, recorded in
# DECISIONS.md.
CATCH_ALL_CODES = {
    # 8.6% of Paris's bucket rows ALONE - a third of the whole 19.3% residual,
    # and the direct French analogue of NAICS 812990, which Los Angeles
    # excludes on exactly these grounds. The privacy half of LA's reasoning is
    # weaker here (Paris pins show a premises name or an address, never a
    # legal name - the Milan hybrid), but the data-quality half stands: this
    # code sweeps in home-based sole traders who are not storefronts.
    "96.09Z",
    "56.29B",   # Autres services de restauration n.c.a.
    "47.19B",   # Autres commerces de détail en magasin non spécialisé
    "47.29Z",   # Autres commerces de détail alimentaires en magasin spécialisé
    "47.78C",   # Autres commerces de détail spécialisés divers
}


# ---------------------------------------------------------------------------
# Structural exclusions - NOT premises, anywhere in France
# ---------------------------------------------------------------------------
#
# These differ from CATCH_ALL_CODES above: a catch-all's composition varies by
# city and needs sampling, whereas a code whose own official label says the
# activity happens away from a shop is not a storefront in Marseille either.
# So they belong to the classification, not to a city.
NOT_PREMISES = {
    # Distance selling - 15.5% of Paris's bucket rows, and the brief's single
    # largest correction. These sit INSIDE the retail division and have no
    # storefront at all. An earlier note called 47.91B "24% of the retail
    # division", which understated the problem by looking at one code of four.
    "47.91A": "vente à distance - no premises",
    "47.91B": "vente à distance - no premises",
    "47.99A": "vente à domicile - no premises",
    "47.99B": "automates / hors magasin - no premises",

    # Market stalls. "sur éventaires et marchés" is the publisher saying the
    # trade happens on a pitch rather than in a shop, so the registered
    # address is the trader's own - a data-quality problem and a privacy one,
    # the same pair that justifies the catch-all exclusions elsewhere.
    # ⚠ UNMEASURED: their share of Paris's rows is not known, because it needs
    # the parquet. Confirm at step 2 and record it; if it is large, this is a
    # call to re-take rather than a footnote.
    "47.81Z": "éventaires et marchés - a pitch, not a storefront",
    "47.82Z": "éventaires et marchés - a pitch, not a storefront",
    "47.89Z": "éventaires et marchés - a pitch, not a storefront",

    # Contract catering - a canteen inside someone else's institution, not a
    # place a passer-by can walk into. Milan already excludes exactly this
    # shape by keyword (`FUORI_PIANO_EXCLUDE` catches "mensa"), so this is
    # project precedent rather than a fresh judgement.
    "56.29A": "restauration collective sous contrat - institutional canteen",

    # Wholesale laundry. Note 96.01B (de détail) IS kept - the pair is
    # split "de gros" / "de détail" by INSEE itself, so the publisher's own
    # hierarchy makes this call, not a reading of the French.
    "96.01A": "blanchisserie de gros - industrial, not a shopfront",
}


# ---------------------------------------------------------------------------
# The classification - INSEE's labels, verbatim
# ---------------------------------------------------------------------------

NAF_LABELS = {
    # --- Division 47: Commerce de détail -> Retail -------------------------
    "47.11A": "Commerce de détail de produits surgelés",
    "47.11B": "Commerce d'alimentation générale",
    "47.11C": "Supérettes",
    "47.11D": "Supermarchés",
    "47.11E": "Magasins multi-commerces",
    "47.11F": "Hypermarchés",
    "47.19A": "Grands magasins",
    "47.19B": "Autres commerces de détail en magasin non spécialisé",
    "47.21Z": "Commerce de détail de fruits et légumes en magasin spécialisé",
    "47.22Z": "Commerce de détail de viandes et de produits à base de viande en magasin spécialisé",
    "47.23Z": "Commerce de détail de poissons, crustacés et mollusques en magasin spécialisé",
    "47.24Z": "Commerce de détail de pain, pâtisserie et confiserie en magasin spécialisé",
    "47.25Z": "Commerce de détail de boissons en magasin spécialisé",
    "47.26Z": "Commerce de détail de produits à base de tabac en magasin spécialisé",
    "47.29Z": "Autres commerces de détail alimentaires en magasin spécialisé",
    "47.30Z": "Commerce de détail de carburants en magasin spécialisé",
    "47.41Z": "Commerce de détail d'ordinateurs, d'unités périphériques et de logiciels en magasin spécialisé",
    "47.42Z": "Commerce de détail de matériels de télécommunication en magasin spécialisé",
    "47.43Z": "Commerce de détail de matériels audio et vidéo en magasin spécialisé",
    "47.51Z": "Commerce de détail de textiles en magasin spécialisé",
    "47.52A": "Commerce de détail de quincaillerie, peintures et verres en petites surfaces (moins de 400 m2)",
    "47.52B": "Commerce de détail de quincaillerie, peintures et verres en grandes surfaces (400 m2 et plus)",
    "47.53Z": "Commerce de détail de tapis, moquettes et revêtements de murs et de sols en magasin spécialisé",
    "47.54Z": "Commerce de détail d'appareils électroménagers en magasin spécialisé",
    "47.59A": "Commerce de détail de meubles",
    "47.59B": "Commerce de détail d'autres équipements du foyer",
    "47.61Z": "Commerce de détail de livres en magasin spécialisé",
    "47.62Z": "Commerce de détail de journaux et papeterie en magasin spécialisé",
    "47.63Z": "Commerce de détail d'enregistrements musicaux et vidéo en magasin spécialisé",
    "47.64Z": "Commerce de détail d'articles de sport en magasin spécialisé",
    "47.65Z": "Commerce de détail de jeux et jouets en magasin spécialisé",
    "47.71Z": "Commerce de détail d'habillement en magasin spécialisé",
    "47.72A": "Commerce de détail de la chaussure",
    "47.72B": "Commerce de détail de maroquinerie et d'articles de voyage",
    "47.73Z": "Commerce de détail de produits pharmaceutiques en magasin spécialisé",
    "47.74Z": "Commerce de détail d'articles médicaux et orthopédiques en magasin spécialisé",
    "47.75Z": "Commerce de détail de parfumerie et de produits de beauté en magasin spécialisé",
    "47.76Z": "Commerce de détail de fleurs, plantes, graines, engrais, animaux de compagnie et aliments pour ces animaux en magasin spécialisé",
    "47.77Z": "Commerce de détail d'articles d'horlogerie et de bijouterie en magasin spécialisé",
    "47.78A": "Commerces de détail d'optique",
    "47.78B": "Commerces de détail de charbons et combustibles",
    "47.78C": "Autres commerces de détail spécialisés divers",
    "47.79Z": "Commerce de détail de biens d'occasion en magasin",
    "47.81Z": "Commerce de détail alimentaire sur éventaires et marchés",
    "47.82Z": "Commerce de détail de textiles, d'habillement et de chaussures sur éventaires et marchés",
    "47.89Z": "Autres commerces de détail sur éventaires et marchés",
    "47.91A": "Vente à distance sur catalogue général",
    "47.91B": "Vente à distance sur catalogue spécialisé",
    "47.99A": "Vente à domicile",
    "47.99B": "Vente par automates et autres commerces de détail hors magasin, éventaires ou marchés n.c.a.",

    # --- Division 56: Restauration -> Food service -------------------------
    "56.10A": "Restauration traditionnelle",
    "56.10B": "Cafétérias et autres libres-services",
    "56.10C": "Restauration de type rapide",
    "56.21Z": "Services des traiteurs",
    "56.29A": "Restauration collective sous contrat",
    "56.29B": "Autres services de restauration n.c.a.",
    "56.30Z": "Débits de boissons",

    # --- Division 96: Autres services personnels -> Personal services ------
    "96.01A": "Blanchisserie-teinturerie de gros",
    "96.01B": "Blanchisserie-teinturerie de détail",
    "96.02A": "Coiffure",
    "96.02B": "Soins de beauté",
    "96.03Z": "Services funéraires",
    "96.04Z": "Entretien corporel",
    "96.09Z": "Autres services personnels n.c.a.",
}

# Division -> bucket. The mapping is by division because NAF's own division
# boundaries already match the buckets; the sous-classe is where the
# EXCLUSIONS live, not where the bucket is decided.
_DIVISION_BUCKETS = {
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}


def normalise_code(value):
    """SIRENE's NAF code as a canonical `47.11B`.

    SIRENE publishes `activitePrincipaleEtablissement` dotted (`47.11B`), but
    older extracts and some mirrors carry it flat (`4711B`). Accepting both
    costs four lines and removes a silent whole-city failure: an unrecognised
    code returns None from `classify()`, so a format change would empty the
    map rather than raise.
    """
    if value is None:
        return ""
    code = str(value).strip().upper().replace(" ", "")
    if not code or code == "NAN":
        return ""
    if "." not in code and len(code) == 5:
        code = f"{code[:2]}.{code[2:]}"
    return code


def label_for(code):
    """INSEE's official label for a sous-classe, or "" if it is not one of
    the three divisions. Step 2 uses this to fill VALUE_COLUMN."""
    return NAF_LABELS.get(normalise_code(code), "")


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    code = normalise_code(row.get("naf_code"))
    if not code or code in NOT_PREMISES:
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def legend_label(bucket):
    """NAICS appends its prefixes; NAF appends its divisions, which is the
    same promise - a reader can check the mapping against the published
    classification rather than taking the legend's word."""
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - NAF {'/'.join(divisions)}"


# ---------------------------------------------------------------------------
# The enumeration is a CLOSED LIST, so prove it at import
# ---------------------------------------------------------------------------
#
# Barcelona's module carries the same assertion for the same reason: a value
# added by a future refresh would otherwise fall through `classify()` silently
# and simply not appear on the map. NAF rév. 2 has been stable since 2008, so
# this should never fire - which is exactly when a silent drift would go
# unnoticed for longest.

_bad = sorted(c for c in NAF_LABELS if normalise_code(c) != c)
assert not _bad, f"NAF_LABELS keys are not canonical: {_bad}"

_orphans = sorted(set(NOT_PREMISES) - set(NAF_LABELS))
assert not _orphans, f"NOT_PREMISES codes absent from NAF_LABELS: {_orphans}"

_orphans = sorted(CATCH_ALL_CODES - set(NAF_LABELS))
assert not _orphans, f"CATCH_ALL_CODES absent from NAF_LABELS: {_orphans}"

_unbucketed = sorted(c for c in NAF_LABELS
                     if c[:2] not in _DIVISION_BUCKETS)
assert not _unbucketed, f"codes outside the three divisions: {_unbucketed}"

# Measured 2026-09-22 against int_courts_naf_rev_2.xls: 50 / 7 / 7.
_counts = {}
for _code in NAF_LABELS:
    _counts[_code[:2]] = _counts.get(_code[:2], 0) + 1
assert _counts == {"47": 50, "56": 7, "96": 7}, (
    f"NAF division counts drifted from INSEE's published file: {_counts}")

# A catch-all that is also structurally excluded would be a contradiction -
# the first says "a city must sample and decide", the second says "already
# decided, everywhere".
_both = sorted(CATCH_ALL_CODES & set(NOT_PREMISES))
assert not _both, f"code is both a catch-all and structurally excluded: {_both}"
