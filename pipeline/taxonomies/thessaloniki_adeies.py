"""Thessaloniki taxonomy: the City's active-shop-licence layer, keyed on its
licensed activity (`antikeimeno`), not NAICS.

The layer (Ενεργές Άδειες Καταστημάτων, sdi.thessaloniki.gr) is a licence
register of shops of "sanitary interest": food service, food retail,
hairdressers and beauty, and the recreation venues the same law licenses. It
carries no general retail, so "Retail" here is FOOD retail only, named "Food
shops" in the layer menu as Matsuyama's is (japan_eigyo.py), and the legend
says no general retail is published.

ONE LEVEL, 79 VALUES. The activity is a single free-text field drawn from a
closed list: 78 activity texts and one blank row, every one listed below with
its bucket or its reason for being out (docs/category_rules.md). classify()
RAISES on a value not listed, so a new licence type stops step 2 instead of
vanishing. Counts are the cached layer's rows (2026-10-04, 8,103 rows).

Catch-all: "ANEY" (14 rows, ΑΝΕΥ "without", no activity) and the one blank
row, 15 of 8,103 (0.19%), both out.

The owner's calls (2026-10-04, the brief's calls 1-3, each as recommended):
  1. ΚΥΛΙΚΕΙΟ (canteen inside another premises), 246: OUT on R1;
  2. packaged ice cream, soft drinks and confectionery in a ψιλικά shop, 376:
     KEPT as Food shops (a convenience store, NAICS 445131);
  3. ΖΑΧΑΡΟΠΛΑΣΤΕΙΟ (patisserie), 99, and coffee sold to passers-by from a
     bread shop or coffee roaster, 37: KEPT as Food shops.

The layer has no name field, so a pin shows its activity in English
(label()), Florence's no-name precedent; the Greek text stays the
classification value the tooltip shows.
"""

FIELD_LABEL = "Licensed activity"
VALUE_COLUMN = "activity"

R, F, P = "Retail", "Food service", "Personal services"

# Out reasons, each a docs/category_rules.md row or the plain reason.
R1 = "out: food with no counter of its own (R1)"
R3 = "out: adult venue (R3)"
REC = "out: recreation (NAICS 71)"
WHOLESALE = "out: wholesale and storage"
NONSTORE = "out: vending machines (nonstore retail, mobile units)"
FUNERAL = "out: funeral"
NONFOOD = "out: non-food retail (no general retail layer)"
MAKING = "out: food manufacturing"
RENTAL = "out: rental"
CATCHALL = "out: no activity (catch-all)"

# activity text -> (bucket or None, the pin's English label, out reason).
# Keys are written in Greek capitals; key() folds the Latin look-alike
# capitals the register mixes in (e.g. "ANEY", the long restaurant-and-bar
# licence's "EΣΤΙΑΤΟΡΙΟ" and "KAI").
ACTIVITIES = {
    # --- Food service: 24 values, 3,685 rows ---------------------------------
    "ΑΝΑΨΥΚΤΗΡΙΟ": (F, "Refreshment bar", None),                                      # 840
    "ΚΑΦΕΤΕΡΙΑ": (F, "Café", None),                                                   # 750
    "ΕΣΤΙΑΤΟΡΙΟ": (F, "Restaurant", None),                                            # 432
    "ΚΑΦΕΝΕΙΟ": (F, "Kafeneio (traditional coffee house)", None),                     # 424
    "ΟΒΕΛΙΣΤΗΡΙΟ": (F, "Souvlaki shop", None),                                        # 223
    "ΣΝΑΚ ΜΠΑΡ": (F, "Snack bar", None),                                              # 176
    "ΜΠΑΡ": (F, "Bar", None),                                                         # 169
    "ΨΗΤΟΠΩΛΕΙΟ": (F, "Grill house", None),                                           # 158
    "ΠΙΤΣΑΡΙΑ": (F, "Pizzeria", None),                                                # 146
    "ΜΠΟΥΓΑΤΣΑΤΖΙΔΙΚΟ": (F, "Bougatsa shop", None),                                   # 106
    "ΚΑΦΕΤΕΡΙΑ ή ΕΚΣΥΧΡΟΝΙΣΜΕΝΟ ΚΑΦΕΝΕΙΟ": (F, "Café or modernized kafeneio", None),   # 76
    # Nightclubs (not adult) are kept, Food service (R5).
    "ΚΕΝΤΡΟ ΔΙΑΣΚΕΔΑΣΗΣ": (F, "Nightclub", None),                                     # 52
    "ΟΥΖΕΡΙ": (F, "Ouzeri", None),                                                    # 44
    "ΨΑΡΟΤΑΒΕΡΝΑ": (F, "Fish taverna", None),                                         # 22
    "ΟΙΝΟΜΑΓΕΙΡΕΙΟ": (F, "Taverna (oinomageireio)", None),                            # 15
    "ΤΑΒΕΡΝΑ": (F, "Taverna", None),                                                  # 13
    "ΠΑΓΩΤΟΠΩΛΕΙΟ": (F, "Ice cream parlor", None),                                    # 11
    "ΕΠΙΧΕΙΡΗΣΗ ΜΑΖΙΚΗΣ ΕΣΤΙΑΣΗΣ ΠΛΗΡΟΥΣ ΓΕΥΜΑΤΟΣ(ΖΕΣΤΗΣ ΚΑΙ ΚΡΥΑΣ ΚΟΥΖΙΝΑΣ )"
    "(ΕΣΤΙΑΤΟΡΙΟ-ΣΝΑΚ ΜΠΑΡ-ΠΙΤΣΑΡΙΑ) ΚΑΙ ΑΝΑΨΥΧΗΣ ΚΑΙ ΠΡΟΣΦΟΡΑΣ ΚΑΤΑ ΚΥΡΙΟ ΛΟΓΟ "
    "ΟΙΝΟΠΝΕΥΜΑΤΩΔΩΝ ΠΟΤΩΝ (ΚΑΦΕΤΕΡΙΑ-ΜΠΑΡ)": (F, "Restaurant and bar", None),          # 6
    "ΑΝΑΨΥΚΤΗΡΙΟ, ΖΑΧΑΡΟΠΛΑΣΤΕΙΟ ΜΕ ΕΡΓΑΣΤΗΡΙΟ ΓΙΑ ΤΙΣ ΑΝΑΓΚΕΣ ΤΟΥ":
        (F, "Refreshment bar and patisserie", None),                                  # 5
    "ΚΕΝΤΡΟ ΔΙΑΣΚΕΔΑΣΗΣ (ΑΝΩ ΤΩΝ 200 ΘΕΣΕΩΝ)": (F, "Nightclub (over 200 seats)", None),  # 5
    "ΠΡΑΤΗΡΙΟ ΕΤΟΙΜΩΝ ΦΑΓΗΤΩΝ": (F, "Ready-meals shop", None),                         # 4
    "ΠΑΡΑΣΚΕΥΗ ΚΑΙ ΠΩΛΗΣΗ ΚΑΦΕ ΠΑΣΗΣ ΦΥΣΕΩΣ ΣΕ ΔΙΕΡΧΟΜΕΝΟΥΣ ΠΕΛΑΤΕΣ":
        (F, "Coffee to go", None),                                                    # 3
    "ΛΟΥΚΟΥΜΑΤΖΙΔΙΚΟ ΑΜΙΓΕΣ": (F, "Loukoumades shop", None),                           # 3
    "ΑΝΟΙΚΤΟ ΜΠΑΡ - OPEN BAR": (F, "Open bar", None),                                  # 2

    # --- Food shops (Retail): 21 values, 2,431 rows --------------------------
    "ΠΑΝΤΟΠΩΛΕΙΟ": (R, "Grocery", None),                                              # 577
    # Owner's call 2: a ψιλικά shop is a convenience store.
    "ΠΩΛΗΣΗ ΤΥΠ/ΝΩΝ ΠΑΓΩΤΩΝ ΑΝΑΨ/ΚΩΝ ΠΟΤΩΝ & ΟΡΙΣΜ.ΖΑΧ/ΔΩΝ ΣΕ ΚΑΤ/ΜΑ ΨΙΛΙΚΩΝ":
        (R, "Convenience store (psilika)", None),                                     # 376
    "ΠΡΑΤΗΡΙΟ ΑΡΤΟΥ": (R, "Bread shop", None),                                        # 199
    "ΚΡΕΟΠΩΛΕΙΟ": (R, "Butcher", None),                                               # 180
    "ΠΡΑΤΗΡΙΟ ΓΑΛΑΚΤΟΣ & ΕΙΔΩΝ ΖΑΧΑΡΟΠΛΑΣΤΙΚΗΣ": (R, "Dairy and pastry shop", None),    # 154
    "ΥΠΕΡΑΓΟΡΑ ΤΡΟΦΙΜΩΝ (SUPER MARKET)": (R, "Supermarket", None),                     # 151
    "ΟΠΩΡΟΛΑΧΑΝΟΠΩΛΕΙΟ": (R, "Greengrocer", None),                                    # 137
    # Owner's call 3: the premises is a pastry shop.
    "ΖΑΧΑΡΟΠΛΑΣΤΕΙΟ": (R, "Patisserie", None),                                        # 99
    "ΑΜΙΓΕΣ ΠΡΑΤΗΡΙΟ ΕΙΔΩΝ ΖΑΧΑΡΟΠΛΑΣΤΕΙΟΥ": (R, "Pastry shop", None),                 # 95
    "ΙΧΘΥΟΠΩΛΕΙΟ": (R, "Fishmonger", None),                                           # 93
    "ΚΑΤΑΣΤΗΜΑ ΞΗΡΩΝ ΚΑΡΠΩΝ ΚΑΙ ΖΑΧΑΡΩΔΩΝ ΠΡΟΪΟΝΤΩΝ": (R, "Nuts and sweets shop", None),  # 79
    "ΚΑΦΕΚΟΠΤΕΙΟ": (R, "Coffee roaster", None),                                       # 73
    "ΚΑΤΑΣΤΗΜΑ ΕΜΦΙΑΛΟΜΕΝΩΝ ΠΟΤΩΝ": (R, "Bottled drinks shop", None),                  # 60
    # Owner's call 3: the premises is a bread shop or a coffee roaster.
    "ΠΩΛΗΣΗ ΚΑΦΕ ΣΕ ΔΙΕΡΧΟΜΕΝΟΥΣ ΑΠΟ ΠΡΑΤΗΡΙΟ ΑΡΤΟΥ - ΚΑΦΕΚΟΠΤΕΙΟ":
        (R, "Bread shop or coffee roaster", None),                                    # 37
    "ΚΑΤΑΣΤΗΜΑ ΠΡΟΪΟΝΤΩΝ ΑΛΛΑΝΤΟΠΟΙΙΑΣ - ΤΥΡΟΚΟΜΙΑΣ": (R, "Deli (cured meats and cheese)", None),  # 33
    "ΠΤΗΝΟΠΩΛΕΙΟ - ΑΥΓΟΠΩΛΕΙΟ": (R, "Poultry and eggs", None),                        # 26
    "ΚΑΤΑΣΤΗΜΑ ΚΑΤΕΨΥΓΜΕΝΩΝ ΠΡΟΪΟΝΤΩΝ": (R, "Frozen foods", None),                     # 19
    "ΓΑΛΑΚΤΟΠΩΛΕΙΟ": (R, "Dairy shop", None),                                         # 18
    "ΕΠΙΧΕΙΡΗΣΗ ΛΙΑΝΙΚΗΣ ΔΙΑΘΕΣΗΣ ΤΡΟΦΙΜΩΝ (ΠΑΝΤΟΠΩΛΕΙΟ-ΚΑΤΑΣΤΗΜΑ ΨΙΛΙΚΩΝ)":
        (R, "Grocery or convenience store", None),                                    # 12
    "ΠΡΑΤΗΡΙΟ ΕΛΑΙΟΥ & ΜΑΓΕΙΡΙΚΩΝ ΛΙΠΩΝ": (R, "Olive oil shop", None),                  # 9
    "ΟΙΝΟΠΩΛΕΙΟ": (R, "Wine shop", None),                                             # 4

    # --- Personal services: 6 values, 1,021 rows ------------------------------
    "ΚΟΜΜΩΤΗΡΙΟ": (P, "Hair salon", None),                                            # 663
    "ΜΑΝΙΚΙΟΥΡ - ΠΕΤΙΚΙΟΥΡ": (P, "Manicure and pedicure", None),                      # 160
    "ΚΟΥΡΕΙΟ": (P, "Barber", None),                                                   # 132
    # Tattoo has its own value here, so it stays (R2).
    "ΕΡΓΑΣΤΗΡΙΟ ΔΕΡΜΑΤΟΣΤΙΞΙΑΣ": (P, "Tattoo studio", None),                          # 38
    "ΣΤΕΓΝΟΚΑΘΑΡΙΣΤΗΡΙΟ": (P, "Dry cleaner", None),                                   # 27
    "ΕΡΓΑΣΤΗΡΙΟ ΑΙΣΘΗΤΙΚΗΣ": (P, "Beauty salon", None),                               # 1

    # --- Out: 27 values, 965 rows (the blank row is the 79th value) ----------
    # Owner's call 1: a canteen inside offices, hospitals, sports grounds or
    # parks, the R1 row's institutional and staff canteens (Madrid's 1,157).
    "ΚΥΛΙΚΕΙΟ": (None, "Canteen", R1),                                                # 246
    "ΙΝΤΕΡΝΕΤ": (None, "Internet café", REC),                                        # 168
    "ΑΠΟΘΗΚΗ ΤΡΟΦΙΜΩΝ - ΠΟΤΩΝ ΧΟΝΔΡΙΚΟΥ ΕΜΠΟΡΙΟΥ": (None, "Food and drink wholesale store", WHOLESALE),  # 91
    "ΑΥΤΟΜΑΤΟΣ ΠΩΛΗΤΗΣ": (None, "Vending machine", NONSTORE),                          # 86
    "ΚΥΛΙΚΕΙΟ ΕΝΤΟΣ ΣΧΟΛΕΙΟΥ": (None, "School canteen", R1),                           # 66
    "ΓΡΑΦΕΙΑ ΤΕΛΕΤΩΝ": (None, "Funeral home", FUNERAL),                                # 60
    "ΟΙΚΟΣ ΑΝΟΧΗΣ": (None, "Licensed brothel", R3),                                   # 30
    "ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ": (None, "Cinema", REC),                                          # 27
    "ΠΑΙΔΟΤΟΠΟΣ": (None, "Children's play area", REC),                                # 21
    "ΜΕΤΑΧΕΙΡΙΣΜΕΝΑ ΕΙΔΗ": (None, "Second-hand goods", NONFOOD),                      # 20
    "ΤΕΧΝΙΚΑ ΠΑΙΓΝΙΑ": (None, "Amusement arcade", REC),                               # 19
    "ΕΡΓΑΣΤΗΡΙΟ ΤΡΟΦΙΜΩΝ ΚΑΙ ΠΟΤΩΝ": (None, "Food and drink workshop", MAKING),        # 19
    "PET SHOP": (None, "Pet shop", NONFOOD),                                          # 19
    "ΑΝΕΥ": (None, "No activity", CATCHALL),                                          # 14
    "ΘΕΑΤΡΟ": (None, "Theater", REC),                                                 # 14
    "ΑΠΟΘΗΚΗ ΤΡΟΦΙΜΩΝ": (None, "Food store (warehouse)", WHOLESALE),                  # 13
    "ΓΥΜΝΑΣΤΗΡΙΟ": (None, "Gym", REC),                                                # 12
    # A preparation kitchen serves another premises; no counter of its own.
    "ΠΑΡΑΣΚΕΥΑΣΤΗΡΙΟ": (None, "Preparation kitchen", R1),                             # 10
    "ΚΟΛΥΜΒΗΤΙΚΗ ΔΕΞΑΜΕΝΗ": (None, "Swimming pool", REC),                             # 8
    "ΚΑΤΑΣΤΗΜΑ ΕΚΜΙΣΘΩΣΗΣ ΠΟΔΗΛΑΤΩΝ": (None, "Bicycle rental", RENTAL),                # 7
    "ΛΟΥΝΑ ΠΑΡΚ": (None, "Amusement park", REC),                                      # 6
    "ΑΠΟΘΗΚΗ ΑΛΚΟΟΛΟΥΧΩΝ ΠΟΤΩΝ-ΑΝΑΨΥΚΤΙΚΩΝ": (None, "Drinks warehouse", WHOLESALE),    # 2
    "ΑΙΘΟΥΣΑ ΣΥΝΑΥΛΙΩΝ": (None, "Concert hall", REC),                                 # 2
    "ΠΟΛΙΤΙΣΤΙΚΟ ΚΕΝΤΡΟ": (None, "Cultural center", REC),                             # 2
    "ΨΥΧΑΓΩΓΙΚΟ ΠΑΙΓΝΙΟ": (None, "Amusement game", REC),                              # 1
    # A καντίνα is a mobile or stand canteen (mobile food, R1).
    "ΚΑΝΤΙΝΑ ΣΕ ΙΔΙΩΤΙΚΟ ΧΩΡΟ": (None, "Mobile canteen", R1),                         # 1
    # A coffin warehouse: storage, and no general retail layer.
    "ΑΠΟΘΗΚΗ ΦΕΡΕΤΡΩΝ": (None, "Coffin warehouse", FUNERAL),                          # 1
}
BLANK_REASON = "out: blank activity (catch-all)"
CATCHALL_KEYS = ("ΑΝΕΥ",)

# Latin capitals that look like Greek ones, folded to the Greek letter before
# a lookup; only inside a word that also holds a Greek letter, so "PET SHOP",
# "SUPER MARKET" and "OPEN BAR" stay Latin. "ANEY" is the exception: it is
# the Greek word ΑΝΕΥ typed in Latin look-alikes, listed in WHOLLY_LATIN.
_LOOKALIKE = str.maketrans("ABEHIKMNOPTXYZ", "ΑΒΕΗΙΚΜΝΟΡΤΧΥΖ")
WHOLLY_LATIN = {"ANEY": "ΑΝΕΥ", "KAI": "ΚΑΙ"}


def _is_greek(ch):
    return "Ͱ" <= ch <= "Ͽ"


def key(value):
    """The lookup key: whitespace collapsed, Latin look-alikes folded inside
    Greek words, and the wholly-Latin Greek words above mapped."""
    if not isinstance(value, str):
        return ""
    words = []
    for w in value.split():
        if w in WHOLLY_LATIN:
            w = WHOLLY_LATIN[w]
        elif any(_is_greek(c) for c in w):
            w = w.translate(_LOOKALIKE)
        words.append(w)
    return " ".join(words)


_TABLE = {key(k): v for k, v in ACTIVITIES.items()}
assert len(_TABLE) == len(ACTIVITIES) == 78, len(_TABLE)


def _entry(row):
    k = key(row.get(VALUE_COLUMN))
    if not k:
        return None, "Blank activity", BLANK_REASON
    if k not in _TABLE:
        raise KeyError(f"unlisted activity {row.get(VALUE_COLUMN)!r}: add it to "
                       f"thessaloniki_adeies.ACTIVITIES with its bucket or its reason "
                       f"(docs/category_rules.md)")
    return _TABLE[k]


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    return _entry(row)[0]


def label(row: dict) -> str:
    """The pin's text: the layer carries no name."""
    return _entry(row)[1]


def out_reason(row: dict):
    """Why a row is out, or None when it is kept."""
    bucket, _label, reason = _entry(row)
    return None if bucket else reason


def is_catchall(row: dict) -> bool:
    k = key(row.get(VALUE_COLUMN))
    return not k or k in CATCHALL_KEYS


def legend_label(bucket: str) -> str:
    return {"Retail": "Food retail (no general retail is published)"}.get(bucket, bucket)


# The Retail bucket here is food shops only, so its pins are olive, not retail
# blue (owner, 2026-10-07: one pin colour per meaning; pipeline/taxonomies
# MEANING_COLOURS).
PIN_MEANINGS = {"Retail": "Food shops"}


def layer_label(bucket: str) -> str:
    return {"Retail": "Food shops"}.get(bucket, bucket)


# Import-time checks: every kept value has a bucket and no reason, every out
# value a reason, and the owner's three calls hold.
assert all((b is None) == (r is not None) for b, _l, r in ACTIVITIES.values())
assert classify({VALUE_COLUMN: "ΚΥΛΙΚΕΙΟ"}) is None
assert classify({VALUE_COLUMN: "ΖΑΧΑΡΟΠΛΑΣΤΕΙΟ"}) == R
assert classify({VALUE_COLUMN: "ANEY"}) is None and is_catchall({VALUE_COLUMN: "ANEY"})
assert classify({VALUE_COLUMN: "ΚΕΝΤΡΟ ΔΙΑΣΚΕΔΑΣΗΣ"}) == F
