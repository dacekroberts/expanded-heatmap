"""Florence: the Comune's four activity layers, keyed on the layer and its own
`tipologiaattivita` (an ATECO-style code with a description).

The Comune di Firenze publishes four GeoJSON layers (datigis.comune.fi.it/json/,
CC BY 4.0): commercio in sede fissa, pubblici esercizi, attività estetiche and
tintolavanderie. Each row has an id, a point and a type - NO name, NO address.
The layer is most of the classification (Milan's "the register IS the
classification"); the type decides what inside a layer is not a storefront.
36 (layer, type) pairs on 2026-09-30, every one with an explicit home below;
an unknown pair RAISES, so a new type stops step 2.

THE CALLS, each with its precedent:
  * EXEMPT FOOD SERVICE IS IN (owner, call 16; Milan's fuori piano, 2026-09-22):
    "non soggetta a requisiti comunali" (464) and art. 53 (175) - service the
    regional law exempts from the Comune's requirements, some of it not open to
    the public. The type code does not say which, so all 639 stay and the page
    says some non-public premises remain.
  * OUT, as the screen dropped them (the brief): private clubs and
    associations (circoli, 186); internal shops (spaccio interno); online, mail
    order, door-to-door and vending sellers (nonstore); farmers selling their
    own produce; wholesale; catering and home restaurants (no counter, R1);
    temporary service at events; bars in the Comune's sports grounds and
    restaurants in hotels.
  * BAKERS ARE RETAIL (Milan's call: a food SHOP is Retail; NACE 10.71 sits in
    the pubblici esercizi layer here, but sells bread, NAICS 445 not 722).
  * TATTOO, PIERCING AND DERMOPIGMENTATION are Personal services (tattoo has its
    own code; category_rules R2).
  * A ROW WITH NO TYPE takes its layer's bucket where the layer is one trade
    (estetiche, tintolavanderie); in the mixed layers it is out.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "tipologiaattivita"
EXTRA_COLUMNS = ("source",)

R, F, P, OUT = "Retail", "Food service", "Personal services", None

# (layer, tipologiaattivita) -> (bucket, the label a pin shows). Counts are the
# layer's rows on 2026-09-30.
TYPES = {
    # --- commercio in sede fissa (7,546) ---------------------------------------
    ("commercio", "47.10.0R - ESERCIZIO DI VICINATO"): (R, "Shop"),                       # 7,016
    ("commercio", "47.10.2R - MEDIA STRUTTURA DI VENDITA"): (R, "Medium-sized store"),    # 208
    ("commercio", "47.10.4R - GRANDE STRUTTURA DI VENDITA"): (R, "Large store"),          # 12
    ("commercio", "CENTRO COMMERCIALE"): (R, "Shopping center"),                          # 7
    ("commercio", "47.10.6R - FORMA SPECIALE (SPACCIO INTERNO)"): (OUT, "internal shop"),  # 128
    ("commercio", "47.91.01R - FORMA SPECIALE (COMMERCIO ELETTRONICO)"): (OUT, "online"),  # 65
    ("commercio", "47.91.01R - FORMA SPECIALE (VENDITA PER CORRISPONDENZA)"): (OUT, "mail order"),  # 7
    ("commercio", "47.99.01R - FORMA SPECIALE (DOMICILIO DEL CONSUMATORE)"): (OUT, "door to door"),  # 6
    ("commercio", "47.99.02R - FORMA SPECIALE (DISTRIBUTORI AUTOMATICI)"): (OUT, "vending"),  # 45
    ("commercio", "47.20.01R - IMPRENDITORE AGRICOLO"): (OUT, "farmer's own produce"),     # 49
    ("commercio", "46.20R - COMMERCIO ALL'INGROSSO"): (OUT, "wholesale"),                  # 2
    ("commercio", ""): (OUT, "no type"),                                                  # 1
    # --- pubblici esercizi (3,421) ---------------------------------------------
    ("pubblici_esercizi", "56.10.01R - SOMMINISTRAZIONE DI ALIMENTI E BEVANDE"): (F, "Restaurant or bar"),  # 2,382
    ("pubblici_esercizi", "56.20.01R - SOMMINISTRAZIONE NON SOGGETTA A REQUISITI COMUNALI"):
        (F, "Food and drink service (exempt)"),                                           # 464
    ("pubblici_esercizi", "56.20.01R - SOMMINISTRAZIONE ART. 53  lettere a,b,c,d,f,i,j"):
        (F, "Food and drink service (exempt)"),                                           # 175
    ("pubblici_esercizi", "CHIOSCO PE"): (F, "Kiosk"),                                    # 2
    ("pubblici_esercizi", "CHIOSCO CAP"): (F, "Kiosk"),                                   # 1
    ("pubblici_esercizi", "10.71R - PANIFICI"): (R, "Bakery"),                            # 111
    ("pubblici_esercizi", "56.10.02R + 56.21.05R - CIRCOLI E ASSOCIAZIONI"): (OUT, "private club"),  # 186
    ("pubblici_esercizi", "56.20.01R - SOMMINISTRAZIONE IN IMPIANTI SPORTIVI COMUNALI"):
        (OUT, "bar in a municipal sports ground"),                                        # 33
    ("pubblici_esercizi", "56.21.01R - CATERING"): (OUT, "catering"),                     # 19
    ("pubblici_esercizi", "56.21.01R - SOMMINISTRAZIONE AL DOMICILIO - CATERING"): (OUT, "catering"),  # 5
    ("pubblici_esercizi", "56.10.01R - RISTORANTE ALBERGO"): (OUT, "hotel restaurant"),   # 12
    ("pubblici_esercizi", "56.10.01R - HOME RESTAURANT"): (OUT, "home restaurant"),       # 7
    ("pubblici_esercizi", "SOMMINISTRAZIONE TEMPORANEA - art. 52"): (OUT, "temporary"),   # 6
    ("pubblici_esercizi", ""): (OUT, "no type"),                                          # 18
    # --- attività estetiche (1,495) --------------------------------------------
    ("estetiche", "96.02.01R - ACCONCIATORI"): (P, "Hairdresser"),                        # 757
    ("estetiche", "96.02.02R - ESTETISTI"): (P, "Beautician"),                            # 475
    ("estetiche", "96.09.02 - TATUAGGI"): (P, "Tattoo"),                                  # 144
    ("estetiche", "96.09.02 - PIERCING DEL PADIGLIONE AURICOLARE"): (P, "Ear piercing"),  # 37
    ("estetiche", "96.09.02 - TRUCCO CON DERMOPIGMENTAZIONE"): (P, "Permanent make-up"),  # 34
    ("estetiche", "96.09.02 - PIERCING"): (P, "Piercing"),                                # 21
    ("estetiche", ""): (P, "Beauty or hair"),                                             # 27
    # --- tintolavanderie (179) -------------------------------------------------
    ("tintolavanderie", "96.01.2R - LAVANDERIA SELF-SERVICE A GETTONI"): (P, "Self-service laundry"),  # 94
    ("tintolavanderie", "96.01.1R - TINTOLAVANDERIA"): (P, "Dry cleaner"),                # 83
    ("tintolavanderie", ""): (P, "Laundry"),                                              # 2
}


def _key(row):
    t = row.get(VALUE_COLUMN)
    t = t.strip() if isinstance(t, str) and t.strip() not in ("None", "nan") else ""
    k = (row.get("source"), t)
    if k not in TYPES:
        raise KeyError(f"Florence {k!r} has no home in florence_attivita.py - map it before "
                       f"step 2 runs")
    return k


def classify(row: dict):
    return TYPES[_key(row)][0]


def label(row: dict):
    """The pin's text: the layers carry no name or address."""
    return TYPES[_key(row)][1]


def legend_label(bucket: str) -> str:
    return bucket


assert TYPES[("pubblici_esercizi", "10.71R - PANIFICI")][0] == "Retail", "bakers are shops"
assert TYPES[("pubblici_esercizi", "56.10.02R + 56.21.05R - CIRCOLI E ASSOCIAZIONI")][0] is None
assert TYPES[("estetiche", "96.09.02 - TATUAGGI")][0] == "Personal services"
assert sum(1 for k, v in TYPES.items() if k[0] == "pubblici_esercizi" and v[1].endswith("(exempt)")) == 2
