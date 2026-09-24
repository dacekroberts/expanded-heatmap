"""Rome: Roma Capitale's SUAP register, classified by its own `DESCRIZIONE`
(the type of authorisation a premises holds) and, inside the workshop
catch-all, by `SPECIALIZZAZIONE`.

THE CATCH-ALL, measured as `premises-taxonomy` asks. At DESCRIZIONE level
`Laboratorio Artigianale e non` - "workshop, craft or not" - holds 37,832 of
168,255 rows (22%), and it mixes a pizza-by-the-slice counter, a nail bar and
a car body shop. Its second level, SPECIALIZZAZIONE, is BLANK on 19,963 of
them (53%), and those are dropped and disclosed: nothing says what they are.
The specified rest are mapped trade by trade, on two precedents rather than
taste:

  * **Personal services follow NAICS 812**, as every NAICS city here does:
    laundry and dry cleaning (8123), nail bars, tattoo and piercing (8121/8129),
    pet grooming (812910), ironing and laundry collection points.
  * **Artisan food follows Milan**, Italy's first city, whose `artigianato
    alimentare` register maps to Food service - pizza by the slice, pastry,
    gelato, rotisserie, hot and cold delicatessen, fried food, fresh pasta. A
    bakery is Retail, as SUAP's own `Panificatori` is and Milan's is: a food
    SHOP is Retail (the NAICS 445-vs-722 line).
  * **Repairs, car work, manufacturing and printing stay OUT** - NAICS 811,
    31-33 and 323 are not storefront buckets anywhere in this project - as do
    catering and central kitchens (Prague's 562 exclusion).

Outside the catch-all: `Esercizio di Vicinato` (a neighbourhood shop, food or
not), `Medie`/`Grandi Strutture`, newsstands and `Panificatori` are Retail;
the two `Somministrazione` authorisations for food and drink, bookshop cafés
and `Trattenimento e Svago` (bars and clubs with entertainment - NAICS 7224)
are Food service; `Acconciatori ed Estetisti` (hairdressers and beauticians)
are Personal services. Out, as the brief recorded: e-commerce (NAICS 454's
twin), wholesale, storage and display, door-to-door and mail order, vehicle
hire and garages, phone centres, arcades and gaming machines, vending
machines, internal company shops, private members' clubs (`Circoli Privati`),
festival stalls (`sagre`), and farm stays.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "activity"
EXTRA_COLUMNS = ("descrizione", "specializzazione")

RETAIL, FOOD, PERSONAL = "Retail", "Food service", "Personal services"

DESCRIZIONE_BUCKETS = {
    "Esercizio di Vicinato": RETAIL,
    "Medie Strutture": RETAIL,
    "Grandi Strutture": RETAIL,
    "Vendita di Quotidiani e Periodici": RETAIL,
    "Panificatori": RETAIL,
    "Somministrazione Alimenti e Bevande": FOOD,
    "Somministrazione (EX ART. 18)": FOOD,
    "Somministrazione Librerie": FOOD,
    "Somministrazione Attività Trattenimento e Svago (EX ART. 13 C. 1 Reg)": FOOD,
    "Acconciatori ed Estetisti": PERSONAL,
    # the catch-all: decided by SPECIALIZZAZIONE below
    "Laboratorio Artigianale e non": None,
}
DESCRIZIONE_OUT = {
    "Commercio Elettronico", "Depositi ed Esposizioni", "Vendita Presso il Domicilio dei Consumatori",
    "Commercio all'ingrosso", "Noleggio Veicoli Senza Conducente",
    "Somministrazione Circoli Privati Aderenti ad Enti Nazionali (DPR 235/01)", "Rimessa di veicoli",
    "Phone Center - Internet Point", "Vendita per Corrispondenza", "Agenzia d'affari", "Sala Giochi",
    "Apparecchi e Congegni Automatici", "Commercio Prodotti per mezzo di apparecchi automatici",
    "Spacci Interni", "Somministrazione di alimenti e bevande in occasione di sagre", "Agriturismo",
}

LAB_FOOD = {
    "PIZZERIA AL TAGLIO", "ARTIGIANATO ALIMENTARE", "PASTICCERIA", "GASTRONOMIA CALDA",
    "GASTRONOMIA FREDDA", "GELATERIA", "ROSTICCERIA", "FRIGGITORIA", "BOUFFET FREDDO",
    "PRODOTTI PER TAVOLA CALDA DA ASPORTO", "LABORATORIO DI PASTA FRESCA",
    "PREPARAZIONE PRODOTTI PRONTI A CUOCERE", "PREPARAZIONE AL BANCO DI BOUFFET FREDDO",
}
LAB_RETAIL = {"PANIFICAZIONE"}
LAB_PERSONAL = {
    "ONICOTECNICA", "RICOSTRUZIONE UNGHIE", "LAVANDERIA", "LAVANDERIA A GETTONI", "TINTORIA",
    "STIRERIA", "CENTRO RACCOLTA INDUMENTI DA TINGERE E LAVARE", "TATUAGGIO", "PIERCING",
    "TOELETTA PER CANI",
}

# The tooltip's activity line, in English.
_LABELS = {
    "Esercizio di Vicinato": "Shop", "Medie Strutture": "Medium-sized store",
    "Grandi Strutture": "Large store", "Vendita di Quotidiani e Periodici": "Newsstand",
    "Panificatori": "Bakery", "Somministrazione Alimenti e Bevande": "Restaurant, bar or café",
    "Somministrazione (EX ART. 18)": "Restaurant, bar or café",
    "Somministrazione Librerie": "Bookshop café",
    "Somministrazione Attività Trattenimento e Svago (EX ART. 13 C. 1 Reg)": "Bar or club with entertainment",
    "Acconciatori ed Estetisti": "Hairdresser or beautician",
    "PIZZERIA AL TAGLIO": "Pizza by the slice", "ARTIGIANATO ALIMENTARE": "Artisan food",
    "PASTICCERIA": "Pastry shop", "GASTRONOMIA CALDA": "Hot delicatessen",
    "GASTRONOMIA FREDDA": "Cold delicatessen", "GELATERIA": "Ice cream", "ROSTICCERIA": "Rotisserie",
    "FRIGGITORIA": "Fried food", "BOUFFET FREDDO": "Cold buffet",
    "PRODOTTI PER TAVOLA CALDA DA ASPORTO": "Hot takeaway", "LABORATORIO DI PASTA FRESCA": "Fresh pasta",
    "PREPARAZIONE PRODOTTI PRONTI A CUOCERE": "Ready-to-cook food",
    "PREPARAZIONE AL BANCO DI BOUFFET FREDDO": "Cold buffet", "PANIFICAZIONE": "Bakery",
    "ONICOTECNICA": "Nail bar", "RICOSTRUZIONE UNGHIE": "Nail bar", "LAVANDERIA": "Laundry",
    "LAVANDERIA A GETTONI": "Launderette", "TINTORIA": "Dry cleaner", "STIRERIA": "Ironing service",
    "CENTRO RACCOLTA INDUMENTI DA TINGERE E LAVARE": "Laundry collection point",
    "TATUAGGIO": "Tattoo studio", "PIERCING": "Piercing studio", "TOELETTA PER CANI": "Dog grooming",
}


def _clean(v):
    return None if v is None or v != v or str(v).strip() == "" else str(v).strip()


def bucket(descrizione, specializzazione):
    d, s = _clean(descrizione), _clean(specializzazione)
    if d in DESCRIZIONE_OUT or d is None:
        return None
    if d not in DESCRIZIONE_BUCKETS:
        return None
    b = DESCRIZIONE_BUCKETS[d]
    if b is not None:
        return b
    if s in LAB_FOOD:
        return FOOD
    if s in LAB_RETAIL:
        return RETAIL
    if s in LAB_PERSONAL:
        return PERSONAL
    return None


def activity_label(descrizione, specializzazione):
    d, s = _clean(descrizione), _clean(specializzazione)
    if d == "Laboratorio Artigianale e non":
        return _LABELS.get(s, "Workshop")
    return _LABELS.get(d, d)


def classify(row):
    return bucket(row.get("descrizione"), row.get("specializzazione"))


def legend_label(bucket_name):
    return bucket_name
