"""Madrid's own three-level activity taxonomy - NOT NAICS, and NOT SCIAN.

The Censo de locales classifies every premises with `desc_seccion` ->
`desc_division` -> `desc_epigrafe`, a Spanish scheme in the NACE family. The
project invariant explicitly permits a documented local taxonomy, and forcing
this one into NAICS would be the mistake the Mexico build already made once in
the other direction.

**WHY THE BUCKETS ARE KEYED ON `desc_division` AND NOT ON `desc_epigrafe`.**
The division level is where this scheme lines up with the buckets - one
division per bucket, almost exactly - while the epigrafe level has 98 distinct
values under retail alone. Keying on divisions and then carving a handful of
epigrafes back out is the `naics.py` shape (groups plus exclusions), and it
means a new epigrafe appearing in a future refresh lands in the right bucket by
default instead of silently vanishing, which is what a 98-value enumeration
would do.

**The cross-standard equivalences, which are what make Madrid comparable to the
other sixteen cities.** Retail is NAICS 44-45 and SCIAN 46; food service is
NAICS 722 and SCIAN 722; personal services is NAICS 812 and SCIAN 812. In
NACE terms that is 47, 56 and 96. Three of those alignments are not obvious and
each is asserted at import:

- **NACE 47 is retail and NACE 46 is WHOLESALE** - the exact inverse of SCIAN,
  where 46 is retail and 43 is wholesale. A reader who carries the Mexican
  numbers across gets the wrong half of Madrid's register.
- **`HOSTELERIA` is the 72-versus-722 trap in Spanish.** It holds
  `SERVICIOS DE COMIDAS Y BEBIDAS` (NACE 56, food service) *and*
  `SERVICIOS DE ALOJAMIENTO` (NACE 55, hotels and tourist flats). Taking the
  section whole would repeat the Mexico City error of counting SCIAN `72` and
  sweeping in 999 hotels. It would also have imported a data defect: measured
  2026-09-22, alojamiento rows are **74.6% zero-coordinate** against 10.6% for
  food and drink.
- **`VENTA Y REPARACION DE VEHICULOS` (NACE 45) is HALF a bucket.** NAICS puts
  vehicle *dealers* in 441, inside retail, and vehicle *repair* in 811, inside
  no bucket at all. NACE keeps them in one division, so it is split here by
  epigrafe: four selling epigrafes join Retail, five repair ones do not.

Counts below are from the full 2026-09-22 download, restricted to the rows step
2 keeps (`Abierto`, valid coordinates).
"""

# --- the three buckets, keyed on desc_division ----------------------------
#
# Matched by PREFIX after upper-casing, because the published strings carry
# accents and trailing qualifiers ("COMERCIO AL POR MENOR, EXCEPTO DE VEHICULOS
# DE MOTOR Y MOTOCICLETAS") and a prefix is stable against a qualifier being
# reworded in a refresh.
DIVISION_TO_BUCKET = {
    # NACE 47. 35,729 rows - the largest single division in the register.
    "COMERCIO AL POR MENOR": "Retail",
    # NACE 56. 18,194 rows. NOT the whole HOSTELERIA section - see the docstring.
    "SERVICIOS DE COMIDAS Y BEBIDAS": "Food service",
    # NACE 96. 9,974 rows - peluquerias, estetica, lavanderias, tanatorios.
    "OTROS SERVICIOS PERSONALES": "Personal services",
}

# --- carved IN: the selling half of NACE 45 -------------------------------
#
# 754 rows. NAICS 441 (motor vehicle and parts dealers) sits inside 44-45, so
# every other city in this project already counts a car dealer as retail;
# excluding Madrid's would make its Retail bucket mean something different.
EPIGRAFE_INTO_RETAIL = {
    "COMERCIO DE VEHICULOS DE MOTOR NUEVOS",          # 260
    "COMERCIO DE VEHICULOS DE MOTOR USADOS",          # 153
    "COMERCIO DE RESPUESTOS Y ACCESORIOS DE VEHICULOS DE MOTOR",  # 270 (sic - the register's own spelling)
    "VENTA DE MOTOCICLETAS",                          # 71
}

# --- carved OUT of Retail: the nonstore twins -----------------------------
#
# 259 rows. The NACE equivalent of NAICS 454 and SCIAN 469, both already
# excluded project-wide (see docs/excluded_categories.md): a business with no
# shopfront is not storefront commercial density, whatever its licence says.
# Small here - 0.7% of retail - but excluded for the same reason, not because
# the number is small.
EPIGRAFE_EXCLUDE = {
    "COMERCIO AL POR MENOR POR CORRESPONDENCIA, INTERNET, A DOMICILIO",  # 218
    "COMERCIO AL POR MENOR CON MAQUINAS EXPENDEDORAS",                   # 39
    "COMERCIO AL POR MENOR EN PUESTOS DE VENTA Y EN MERCADILLOS",        # 2
}

FIELD_LABEL = "Actividad (epígrafe)"
VALUE_COLUMN = "desc_epigrafe"
# classify() dispatches on the DIVISION and refines with the epigrafe, so step 2
# and the map's pin grouping both have to carry the division through. This is
# the same mechanism chicago_license.py uses for its second field.
EXTRA_COLUMNS = ("desc_division",)


def legend_label(bucket: str) -> str:
    return bucket


def _norm(value) -> str:
    """Upper-cased and stripped, and SCALAR-SAFE rather than None-safe.

    `(value or "")` is not enough and the difference is not theoretical: pandas
    fills a missing cell with **float('nan')**, which is TRUTHY, so the `or`
    passes it straight through and `.strip()` raises `AttributeError: 'float'
    object has no attribute 'strip'`. Madrid's register has missing
    `desc_epigrafe` cells, so this fired on the first real run.

    Same defect that took the whole Overview page down on 2026-09-22, where
    `v is None` missed the same nan and `tuple(nan)` raised. Testing the TYPE
    rather than the falsiness is what makes it safe for both.
    """
    return value.strip().upper() if isinstance(value, str) else ""


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    epigrafe = _norm(row.get(VALUE_COLUMN))
    if epigrafe in EPIGRAFE_EXCLUDE:
        return None
    if epigrafe in EPIGRAFE_INTO_RETAIL:
        return "Retail"

    division = _norm(row.get("desc_division"))
    for prefix, bucket in DIVISION_TO_BUCKET.items():
        if division.startswith(prefix):
            return bucket
    return None


# --- proof, at import, that the wrong standard was not applied ------------
#
# scian.py carries the same idea. A taxonomy module is the one place where
# borrowing another country's numbers produces a plausible-looking map that is
# quietly wrong, so the equivalences are tested rather than described.

# Retail, and the NACE/SCIAN inversion that makes it worth asserting.
assert classify({"desc_division": "COMERCIO AL POR MENOR, EXCEPTO DE VEHÍCULOS DE MOTOR Y MOTOCICLETAS"}) == "Retail"
assert classify({"desc_division": "COMERCIO AL POR MAYOR E INTERMEDIARIOS DEL COMERCIO"}) is None, \
    "NACE 46 is WHOLESALE - the inverse of SCIAN, where 46 is retail"

# The 72-versus-722 trap, in Spanish.
assert classify({"desc_division": "SERVICIOS DE COMIDAS Y BEBIDAS"}) == "Food service"
assert classify({"desc_division": "SERVICIOS DE ALOJAMIENTO"}) is None, \
    "alojamiento is NACE 55 (hotels, tourist flats), not food service"

# Personal services, and the two neighbours in the same section that are not it.
assert classify({"desc_division": "OTROS SERVICIOS PERSONALES"}) == "Personal services"
assert classify({"desc_division": "ACTIVIDADES ASOCIATIVAS"}) is None, \
    "NACE 94 associations are NAICS 813, which no bucket includes"
assert classify({"desc_division": "REPARACIÓN DE ORDENADORES, EFECTOS PERSONALES Y ARTÍCULOS DE USO DOMÉSTICO"}) is None, \
    "NACE 95 repair is NAICS 811, not the 812 personal services bucket"

# NACE 45 split in half by epigrafe.
_VEH = "VENTA Y REPARACIÓN DE VEHÍCULOS DE MOTOR Y MOTOCICLETAS"
assert classify({"desc_division": _VEH, "desc_epigrafe": "COMERCIO DE VEHICULOS DE MOTOR NUEVOS"}) == "Retail"
assert classify({"desc_division": _VEH,
                 "desc_epigrafe": "TALLER DE REPARACION DE AUTOMOVILES ESPECIALIZADO EN MECANICA Y ELECTRICIDAD"}) is None, \
    "vehicle repair is NAICS 811; only the selling half of NACE 45 is retail"

# The nonstore carve-out survives even though its division is in a bucket.
assert classify({"desc_division": "COMERCIO AL POR MENOR",
                 "desc_epigrafe": "COMERCIO AL POR MENOR POR CORRESPONDENCIA, INTERNET, A DOMICILIO"}) is None

# An unmapped division is excluded rather than defaulting into a bucket.
assert classify({"desc_division": "ACTIVIDADES INMOBILIARIAS"}) is None
assert classify({}) is None

# A MISSING cell arrives from pandas as float('nan'), not as None or "". This
# fired on the first real run and is the same defect that took the Overview
# page down on 2026-09-22, so it is pinned here rather than remembered.
assert classify({"desc_division": float("nan"), "desc_epigrafe": float("nan")}) is None
assert classify({"desc_division": "SERVICIOS DE COMIDAS Y BEBIDAS",
                 "desc_epigrafe": float("nan")}) == "Food service", \
    "a premises with no epigrafe still has a division, and must still classify"
