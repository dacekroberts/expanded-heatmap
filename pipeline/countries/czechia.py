"""Czechia: the facts shared by every Czech city, measured 2026-09-23/24.

Profiled for Prague, the first Czech city. Three national open-data sources,
all keyless:

  * Establishments - ROS02, *Registr osob - aktivní provozovny* (Digitální a
    informační agentura): every active establishment (`ICP`) with its owner's
    `ICO` and the RUIAN address code of WHERE IT TRADES (`PKODADM`). **This is
    the premises register**, and the reason Prague resumed: the Statistical
    Office's RES, which paused it, records a subject's registered SEAT.
    Declared open data with no personal data and no database right - PERMITTED,
    nothing to display (read 2026-09-24).
  * Activity, form and name - RES, ČSÚ's *Registr ekonomických subjektů*, by
    ICO. **Its activity is the SUBJECT's, not the establishment's**: every
    establishment inherits its owner's single CZ-NACE. CC BY 4.0 with ČSÚ's own
    conditions (link the licence; mark derived data as derived).
  * Coordinates - RUIAN's address export per obec (ČÚZK), a JOIN on the
    address code, not a geocode. CC BY 4.0, "ČÚZK, <year>".

⛔ **NOT the Trade Register (RŽP) via ARES**, though it carries an
establishment-type field. It is not open data, and ÚOOÚ fined a site in 2019
for republishing sole traders' trade data from it (UOOU-10201/18-31).
"""
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
# ONE CACHE FOR THE COUNTRY, as France's, Norway's and Denmark's: ROS02 and RES
# are national files (58.5 MB and 543 MB) that a second Czech city reuses.
SHARED_RAW = _ROOT / "data" / "czechia" / "raw"
ROS02_CSV = SHARED_RAW / "ros02_data.csv"
RES_CSV = SHARED_RAW / "res_data.csv"
NACE_DIR = SHARED_RAW / "cz_nace_2025"

ROS02_URL = "https://www.szrcr.cz/images/dokumenty/ROS/Otevrena%20data/ros02_data.csv"
RES_URL = "https://opendata.czso.cz/data/od_org03/res_data.csv"

# CZ-NACE 2025 labels, one ČSÚ codebook per level: 6101 (section) .. 6105
# (national sub-class). RES stores codes at RAGGED depth, so every level is
# needed to label a row at whatever depth it stops.
NACE_LEVEL_CODEBOOKS = {1: "6101", 2: "6102", 3: "6103", 4: "6104", 5: "6105"}
NACE_CODEBOOK_URL = ("https://apl2.czso.cz/iSMS/do_cis_export?kodcis={kodcis}"
                     "&typdat=0&cisjaz=203&format=2&separator=%2C")

# RUIAN per obec through ČÚZK's INSPIRE ATOM service - the channel ČÚZK's own
# documentation calls "intended primarily for machine processing". It sidesteps
# the VDP application's ban on automated extraction, and it resolves the
# current month's file rather than a hard-coded date that goes stale on the 1st.
RUIAN_ATOM_TEMPLATE = (
    "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB"
    "&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_{obec}")

# --- ROS02 -----------------------------------------------------------------
# Rows REPEAT: dedupe on ICP. Active = no DATUKON, or one in the future.
ROS_COLUMNS = ("ICP", "ICO", "DATZAH", "DATUKON", "PKODADM")

# --- RES -------------------------------------------------------------------
# ⚠ TWO activity columns: `NACE` (the old CZ-NACE, ragged) and `NACE2025`
# (CZ-NACE 2025 = NACE Rev. 2.1, deeper). The build keys on NACE2025 - see
# DECISIONS.md, "Prague resumed". `KATPO` is NOT read: its `000` means "not
# stated" (codebook 579), so it cannot be an employee filter.
RES_COLUMNS = ("ICO", "DDATZAN", "FORMA", "NACE2025", "FIRMA", "KODADM")

# ⚠ THE PRIVACY GUARD, from ČSÚ's codebook 56 (legal forms). A natural
# person's registered name carries the person's own name by law.
#     101 Fyzická osoba podnikající dle živnostenského zákona
#     105 Fyzická osoba podnikající dle jiných zákonů
#     107 Zemědělský podnikatel - fyzická osoba
#     424 Zahraniční fyzická osoba
#     425 Odštěpný závod zahraniční fyzické osoby
# and 111, veřejná obchodní společnost - a partnership, following the owner's
# Copenhagen call on I/S.
NATURAL_PERSON_FORMS = ("101", "105", "107", "424", "425")
NAME_SUPPRESSED_FORMS = NATURAL_PERSON_FORMS + ("111",)

# Legal-form tails stripped from a displayed company name ("CAPELLO, s.r.o."
# -> "CAPELLO"), as the Danish and Norwegian modules strip ApS and AS.
LEGAL_FORM_TAILS = (r",?\s*spol\.\s*s\s*r\.\s*o\.$", r",?\s*s\.\s*r\.\s*o\.$",
                    r",?\s*a\.\s*s\.$", r",?\s*v\.\s*o\.\s*s\.$", r",?\s*k\.\s*s\.$")

# --- RUIAN -----------------------------------------------------------------
# ⚠ THE CRS: EPSG:5513 (S-JTSK / Krovak) with the published (X, Y) - verified
# against Prague Castle in the brief (50.08948, 14.39861); the other axis
# orders land in Germany or the Arctic. The steps re-check it on the castle.
RUIAN_CRS = "EPSG:5513"
RUIAN_CODE = "Kód ADM"
RUIAN_X = "Souřadnice X"
RUIAN_Y = "Souřadnice Y"
RUIAN_STREET = "Název ulice"
RUIAN_PART = "Název části obce"
RUIAN_HOUSE = "Číslo domovní"
RUIAN_ORIENT = "Číslo orientační"
RUIAN_ORIENT_LETTER = "Znak čísla orientačního"
RUIAN_ENCODING = "cp1250"
RUIAN_SEP = ";"
