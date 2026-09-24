"""Brazil: the facts shared by every Brazilian city, measured 2026-09-23/24.

Nine cities off ONE national file - IBGE's CNEFE 2022, the census address
file, one zip per município on ftp.ibge.gov.br in one schema. Only the
município differs between cities (and, for the four regional pages, the list
of them): Mexico's shape, not Spain's.

It is the business leg AND the coordinate leg. `DSC_ESTABELECIMENTO` is the
enumerator's identification of every establishment on the block face, and
`LATITUDE`/`LONGITUDE` the enumerator's own point on 98.5% of São Paulo's
mapped rows - so there is no register to join and no geocoder. Classified by
pipeline/taxonomies/brazil_cnefe.py; read by brazil_register.py.
"""

CNEFE_BASE_URL = ("https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/"
                  "Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/")
# Verified on São Paulo's file, not assumed: one CSV member, UTF-8, `;`.
CSV_ENCODING = "utf-8"
CSV_DELIMITER = ";"

# --- What a row is -------------------------------------------------------------
#
# IBGE: "Cada registro representa uma especie existente no endereco" - ONE ROW
# PER USE-TYPE AT AN ADDRESS, not one per business. COD_ESPECIE says which.
# The other species (agricultural, education, health, under construction,
# religious) are never storefronts and never read.
ESPECIE_DWELLING = ("1", "2")        # private and collective dwellings
ESPECIE_ESTABLISHMENT = "6"          # "estabelecimento de outras finalidades"

# How many establishments a row stands for: 1 one, 2 two to ten, 3 more than
# ten, 4 unknown. A shopping centre collapses to one row or a few - accepted
# and disclosed (decided 2026-09-23). São Paulo: 97.4% of mapped rows are 1.
ESTAB_INDICATOR = "COD_INDICADOR_ESTAB_ENDERECO"

# --- Which coordinate a row carries (NV_GEO_COORD) -------------------------------
#
# 1 the census's own point at the address; 2-3 modified or estimated; 4 the
# block face; 6 the census tract (docs/geocoding_retrospective.md, Step 6).
# A WHITELIST, so a level not seen yet is dropped rather than drawn. Levels 1-4
# put a pin on the right block face at worst; a tract's point is not the
# premises. São Paulo, 2026-09-24, mapped rows: 98.46 / 0.10 / 0.39 / 1.05% at
# levels 1-4, and 13 rows (0.01%) at 6 - Rio's brief flagged its 0.2% at 6 as
# the thing to decide, and this is the decision.
COORD_LEVELS_KEEP = ("1", "2", "3", "4")


# --- Privacy: the owner's decision of 2026-09-23 -----------------------------------
#
# At an address that ALSO holds a dwelling (COD_ESPECIE 1 or 2 under the same
# address_key), a pin shows its CATEGORY, never the enumerator's description -
# which is where a person's name lives when there is one (`BAR DO PAULO`,
# `MERCEARIA DA SONIA`). Structural rather than a name list, because a list
# misses names. An upper bound on purpose: a shop under flats shares its
# number too. LGPD applies by the licence's own terms, so this is not house
# style.

def address_key(row):
    """One ADDRESS, as the dwelling test compares it - lifted unchanged from
    scripts/screen_cnefe.py, whose figures the briefs quote."""
    # Where the door number is blank and the first complement is a LOTE,
    # the lot IS the address (Brasilia names a block, not a door: 98.5%
    # of its "shared with a dwelling" rows had no number, so street +
    # number merged whole blocks). Owner decision 2026-09-23.
    lot = ""
    if (row["NUM_ENDERECO"].strip() in ("", "0")
            and row["NOM_COMP_ELEM1"].strip() == "LOTE"):
        lot = row["VAL_COMP_ELEM1"].strip()
    return (row["COD_SETOR"], row["NUM_QUADRA"], row["NUM_FACE"],
            row["NOM_SEGLOGR"], row["NUM_ENDERECO"], row["DSC_MODIFICADOR"],
            lot)
