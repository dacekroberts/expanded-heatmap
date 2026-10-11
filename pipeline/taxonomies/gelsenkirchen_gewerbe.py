"""Gelsenkirchen: the City's survey of its commercial premises (the
Infrastrukturdatenbank's three themed layers), keyed on the layer and the
layer's own category field - not NAICS.

Stadt Gelsenkirchen publishes the survey as GeoServer layers under
Datenlizenz Deutschland - Zero - Version 2.0 (docs/build_briefs/gelsenkirchen.md).
Each themed layer has its own classification field:

  * gewerbe_gastronomie -> KAT_GASTRO (one level, 6 values and blanks);
  * gewerbe_einzelhandel -> HAUPTWARENGRUPPEBEZ (the main goods group), with
    KERNSORTIMENTBEZ (the core assortment) beneath it;
  * gewerbe_dienstleistung -> KAT_DL (one level, 38 values and blanks).

Step 2 writes the field as `category`, the layer as `layer` and the retail
core assortment as `assortment`. Every (layer, category) pair and every
retail assortment has an explicit home below; an unknown one RAISES, so a
new survey category stops step 2.

THE LAYER IS MOST OF THE CLASSIFICATION (Florence's shape). Every retail row
is Retail and every kept food row Food service; the services layer is the one
that mixes premises, and each of its categories takes a verdict from
docs/category_rules.md.

CATCH-ALL SHARES (premises-taxonomy Step 2), measured on the 2026-10-07
reduced fetch, kept rows only:
  * retail's HAUPTWARENGRUPPEBEZ "Sonstiges": 8 of 1,318 (0.6%), kept on the
    Rev. 2.1 precedent (nothing marks it as non-store; 4 of the 8 are
    Erotikartikel, sex shops kept by R3). The finer KERNSORTIMENTBEZ level was
    measured too: blank on 17 retail rows (1.3%), so the group level, with a
    smaller catch-all and no blanks but one, is the key and the assortment a
    closed list checked beside it.
  * services' "Sonstige nicht genannte Dienstleistungen" (5) and "Sonstiges"
    (5) are R2's catch-all and out; "Sonstige Einrichtungen Gesundheit,
    Soziales, Sport" (37) is health, social and sport premises, out as health
    care and recreation.

BLANK CATEGORIES (owner, 2026-10-04): a food row with no KAT_GASTRO and a
services row with no KAT_DL are left out and disclosed (54 and 122 on
2026-10-07). The one retail row with no main goods group is in the retail
layer, so it is a shop (kept).

ACCOMMODATION (premises-taxonomy Step 5): "Hotel/Gasthof/Pension" sits in the
food layer (3 rows) and is out with lodging.
"""

FIELD_LABEL = "Category (city survey)"
VALUE_COLUMN = "category"
EXTRA_COLUMNS = ("layer", "assortment")

R, F, P, OUT = "Retail", "Food service", "Personal services", None
FOOD, RETAIL, SERVICES = "gastronomie", "einzelhandel", "dienstleistung"
LAYERS = (FOOD, RETAIL, SERVICES)

# (layer, category as the survey writes it; "" for blank) -> (bucket, the
# English label a pin shows). Counts: the 2026-10-07 reduced fetch.
TYPES = {
    # --- gewerbe_gastronomie, KAT_GASTRO (403) ----------------------------------
    (FOOD, "Restaurant"): (F, "Restaurant"),                                    # 112
    (FOOD, "Imbissbetrieb"): (F, "Snack bar"),                                  # 101
    (FOOD, "Bar/Kneipe/Wirtshaus"): (F, "Bar or pub"),                          # 69
    (FOOD, "Café/Eisdiele"): (F, "Café or ice cream parlor"),                   # 51
    (FOOD, "Systemgastronomie"): (F, "Chain restaurant"),                       # 13
    (FOOD, "Hotel/Gasthof/Pension"): (OUT, "Hotel or guest house"),             # 3, lodging
    (FOOD, ""): (OUT, "no category"),                                           # 54, owner
    # --- gewerbe_einzelhandel, HAUPTWARENGRUPPEBEZ (1,318) -----------------------
    (RETAIL, "Nahrungs- und Genussmittel"): (R, "Groceries and food"),         # 554
    (RETAIL, "Bekleidung"): (R, "Clothing"),                                    # 139
    (RETAIL, "Gesundheit und Körperpflege"): (R, "Health and personal care"),   # 87
    (RETAIL, "medizinische und orthopädische Artikel"):
        (R, "Medical and orthopedic supplies"),                                 # 66
    (RETAIL, "Elektronik / Multimedia"): (R, "Electronics"),                    # 63
    (RETAIL, "Baumarktsortimente"): (R, "Hardware and building supplies"),      # 54
    (RETAIL, "Möbel"): (R, "Furniture"),                                        # 53
    (RETAIL, "Blumen (Indoor) / Zoo"): (R, "Flowers and pet supplies"),         # 48
    (RETAIL, "Wohneinrichtung"): (R, "Home furnishings"),                       # 46
    (RETAIL, "Uhren, Schmuck"): (R, "Watches and jewelry"),                     # 39
    (RETAIL, "Glas / Porzellan / Keramik / Haushaltswaren"): (R, "Housewares"),  # 37
    (RETAIL, "Papier/Büroart./Schreibw./Zeitg./Zeitschr./Bücher"):
        (R, "Stationery, newspapers and books"),                                # 35
    (RETAIL, "Sport und Freizeit"): (R, "Sporting goods"),                      # 26
    (RETAIL, "Spielwaren / Hobbyartikel / Babyausstattung"):
        (R, "Toys, hobby and baby goods"),                                      # 18
    (RETAIL, "Spielwaren / Hobbyartikel"): (R, "Toys and hobby goods"),         # 2
    (RETAIL, "Elektro / Leuchten"): (R, "Appliances and lighting"),             # 17
    (RETAIL, "Gartenmarktsortimente"): (R, "Garden supplies"),                  # 14
    (RETAIL, "Schuhe / Lederwaren"): (R, "Shoes and leather goods"),            # 10
    (RETAIL, "Sonstiges"): (R, "Other shop"),                                   # 8, the catch-all
    (RETAIL, "Foto"): (R, "Photo supplies"),                                    # 1
    (RETAIL, ""): (R, "Shop"),                                                  # 1
    # --- gewerbe_dienstleistung, KAT_DL (593) ------------------------------------
    # Kept: personal services (NAICS 8121, 8123; tattoo has its own code, R2).
    (SERVICES, "Friseur, Barbershop"): (P, "Hairdresser or barber"),            # 88
    (SERVICES, "Kosmetik-, Nagel-, Fußpfl.-, Haarentf.-, Sonnenst."):
        (P, "Beauty, nail or tanning salon"),                                   # 8
    (SERVICES, "Textil- und Lederreinigung"): (P, "Dry cleaner"),               # 6
    (SERVICES, "Tattoo-/Piercingstudio"): (P, "Tattoo or piercing studio"),     # 6
    # Kept as Retail: car dealers (R4).
    (SERVICES, "KFZ-Handel / Autohäuser inkl. Krafträder"): (R, "Car dealer"),  # 4
    # Out, each by its rule.
    (SERVICES, "Spielhallen, Casinos"): (OUT, "gambling (R5)"),                 # 34
    (SERVICES, "Wettbüros"): (OUT, "gambling (R5)"),                            # 16
    (SERVICES, "Bestattungsinstitut"): (OUT, "funeral home"),                   # 12
    (SERVICES, "Änderungsschneiderei"): (OUT, "repairs and alterations"),       # 18
    (SERVICES, "Schuster, Schuhreparatur"): (OUT, "repairs and alterations"),   # 2
    (SERVICES, "Schlüsseldienst"): (OUT, "repairs and alterations"),            # 3
    (SERVICES, "KFZ-Reparatur"): (OUT, "vehicle repair"),                       # 1
    (SERVICES, "Versicherung"): (OUT, "insurance office"),                      # 36
    (SERVICES, "Bankfiliale, begehbarer Bankautomat, Bausparkasse"): (OUT, "bank"),  # 23
    (SERVICES, "Reisebüro"): (OUT, "travel agency"),                            # 29
    (SERVICES, "Immobilienmakler, Hausverwaltung"): (OUT, "real estate office"),  # 11
    (SERVICES, "Rechtsanwälte"): (OUT, "law office"),                           # 16
    (SERVICES, "Sonstige freie Berufe"): (OUT, "professional office"),          # 6
    (SERVICES, "Werbung, Grafik, Kommunikationsdesign"): (OUT, "professional office"),  # 1
    (SERVICES, "Copyshop"): (OUT, "business services"),                         # 3
    (SERVICES, "Postfiliale"): (OUT, "post office"),                            # 2
    (SERVICES, "Fotograf"): (OUT, "professional office"),                       # 7
    (SERVICES, "Sonstige Einrichtungen Gesundheit, Soziales, Sport"):
        (OUT, "health, social or sport premises"),                              # 37
    (SERVICES, "Pflegedienst"): (OUT, "health care"),                           # 17
    (SERVICES, "Praxis für Physiotherapie (Krankengymnastik u.ä.)"): (OUT, "health care"),  # 13
    (SERVICES, "Arztpraxen für Allgemeinmedizin"): (OUT, "health care"),        # 6
    (SERVICES, "Zahnarztpraxen"): (OUT, "health care"),                         # 3
    (SERVICES, "Fitness-Center"): (OUT, "recreation"),                          # 4
    (SERVICES, "Kampfsport und Selbstverteidigung"): (OUT, "recreation"),       # 1
    (SERVICES, "Fahrschulen"): (OUT, "education"),                              # 18
    (SERVICES, "Sonstige Bildungseinrichtungen"): (OUT, "education"),           # 3
    (SERVICES, "Musikschulen"): (OUT, "education"),                             # 1
    (SERVICES, "Kindergärten, -tagesstätten, Vorschulen"): (OUT, "education"),  # 1
    (SERVICES, "Religiöse Institutionen"): (OUT, "religious premises"),         # 16
    (SERVICES, "Sonstiges Handwerk"): (OUT, "trades"),                          # 7
    (SERVICES, "Elektroinstallateur"): (OUT, "trades"),                         # 2
    (SERVICES, "Sonstige nicht genannte Dienstleistungen"): (OUT, "services catch-all (R2)"),  # 5
    # A code first seen on 2026-10-07 (5 rows; 3 of them blank on 2026-10-04):
    # the services layer's own "other", a catch-all, out as R2's.
    (SERVICES, "Sonstiges"): (OUT, "services catch-all (R2)"),                  # 5
    (SERVICES, ""): (OUT, "no category"),                                       # 122, owner
}

# The retail layer's KERNSORTIMENTBEZ values (2026-10-07), every one a shop's
# assortment and none a nonstore, fuel or repair trade. Checked, not keyed:
# a value outside this list raises, so a new assortment (a fuel station, a
# mail-order seller) is read before it reaches the map. "" is blank (17).
RETAIL_ASSORTMENTS = frozenset({  # 47 values and blank
    "", "Nahrungs- und Genussmittel", "Backwaren / Konditoreiwaren", "Getränke",
    "Fleischwaren", "Bekleidung", "Sportbekleidung und Sportschuhe", "Schuhe",
    "Lederwaren / Taschen / Koffer / Regenschirme", "pharmazeutische Artikel",
    "Drogeriewaren", "Kosmetikartikel / Parfümeriewaren",
    "medizinische und orthopädische Artikel", "Elektronik und Multimedia",
    "Elektrogroßgeräte", "Lampen / Leuchten / Leuchtmittel",
    "baumarktspezifisches Sortiment", "Kfz-, Caravan- und Motorradzubehör",
    "Bauelemente / Baustoffe", "Möbel", "Kunstgewerbe / Bilder / Bilderrahmen",
    "Topfpflanzen / Blumentöpfe und Vasen (Indoor)", "Blumen",
    "Heim- und Kleintierfutter", "Zoologische Artikel", "Pflanzen / Samen",
    "Gartenartikel und -geräte", "Wohndekorationsartikel",
    "Heimtextilien, Gardinen / Dekostoffe", "Teppiche (Einzelware)", "Matratzen",
    "Bettwaren", "Uhren / Schmuck", "Glas / Porzellan / Keramik / Haushaltswaren",
    "Haushaltswaren, Glas/Porzellan/Keramik",
    "Handarbeitswaren / Kurzwaren / Meterware / Wolle", "Zeitungen / Zeitschriften",
    "Papier / Büroartikel / Schreibwaren", "Bücher", "Briefmarken / Münzen",
    "Spielwaren", "Hobbyartikel", "Musikinstrumente und Zubehör", "Babyausstattung",
    "Fahrräder und technisches Zubehör", "Reitsportartikel",
    "Angler-, Jagdartikel und Waffen", "Erotikartikel",
})


def _text(v):
    """The survey's string, or "" for a blank (None, NaN, empty)."""
    return v.strip() if isinstance(v, str) and v.strip() not in ("", "nan", "None") else ""


def _key(row):
    k = (row.get("layer"), _text(row.get(VALUE_COLUMN)))
    if k not in TYPES:
        raise KeyError(f"Gelsenkirchen {k!r} has no home in gelsenkirchen_gewerbe.py - "
                       f"map it before step 2 runs")
    if k[0] == RETAIL:
        a = _text(row.get("assortment"))
        if a not in RETAIL_ASSORTMENTS:
            raise KeyError(f"Gelsenkirchen retail assortment {a!r} is not in "
                           f"RETAIL_ASSORTMENTS - read it before step 2 runs")
    return k


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    return TYPES[_key(row)][0]


def label(row: dict):
    """The category's English label, which a withheld sign shows instead."""
    return TYPES[_key(row)][1]


# A kept category's survey value names one category only, whatever its layer
# (asserted below), so the pin can gloss the value alone.
_KEPT_LABELS = {v: lab for (layer, v), (b, lab) in TYPES.items() if b is not None}


def display_value(value) -> str:
    """How the category reads on a pin: English first, the survey's own words
    after it."""
    v = _text(value)
    if not v:
        return _KEPT_LABELS[""]
    return v if _KEPT_LABELS[v] == v else f"{_KEPT_LABELS[v]} ({v})"


def legend_label(bucket: str) -> str:
    return bucket


_kept = [(layer, v) for (layer, v), (b, _) in TYPES.items() if b is not None]
assert len({v for _, v in _kept}) == len(_kept), "a kept category value in two layers"
assert all(TYPES[(RETAIL, v)][0] == R for (layer, v) in TYPES if layer == RETAIL), "every shop is Retail"
assert TYPES[(FOOD, "Hotel/Gasthof/Pension")][0] is None, "lodging is out"
assert TYPES[(FOOD, "")][0] is None and TYPES[(SERVICES, "")][0] is None, "blank categories out (owner)"
assert TYPES[(SERVICES, "KFZ-Handel / Autohäuser inkl. Krafträder")][0] == R, "car dealers are Retail (R4)"
assert TYPES[(SERVICES, "Tattoo-/Piercingstudio")][0] == P, "tattoo has its own code (R2)"
assert TYPES[(SERVICES, "Sonstige nicht genannte Dienstleistungen")][0] is None, "R2's catch-all"
assert {b for b, _ in TYPES.values()} == {R, F, P, None}, "three buckets"
