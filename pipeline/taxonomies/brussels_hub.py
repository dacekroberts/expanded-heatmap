"""hub.brussels's shop types (City of Brussels inventory), not NAICS.

The inventory is a ground-floor field survey of the City of Brussels (6,880
units, one survey dated 2025-10-17). Each unit carries one or more types in
`type_fr`, comma-separated; a type may itself hold commas inside parentheses
("Station-service (essence, gaz,...)"), so the split is outside parentheses
only. 285 distinct single types; 1,786 units carry two or more (measured
2026-10-04; the screen's naive split reported 1,817).

Keyed on the single type, the finest level. The publisher's nine categories
(`category_fr`) are too coarse to key on (HoReCa holds hotels; "Services"
holds both hairdressers and banks), but they are evidence where a type's
own name is ambiguous (premises-taxonomy, Step 6): a craft type filed under
"Equipement de la maison" is read as a shop, as the publisher files it.

A unit with several types takes the highest bucket among its KEPT types:
Food service over Retail over Personal services (the screen's rule, and the
rule the Belgian KBO measurement used). A unit whose types are all out is
out. Every type has an explicit home below; an unknown type raises.

Every keep or drop follows docs/category_rules.md; the departures and new
calls are listed in the city's drafts entry for the owner.
"""
import unicodedata

FIELD_LABEL = "Type"
VALUE_COLUMN = "type_fr"

FOOD, RETAIL, PERSONAL = "Food service", "Retail", "Personal services"
PRIORITY = (FOOD, RETAIL, PERSONAL)

TYPE_TO_BUCKET = {
    # --- Food service: restaurants, cafes, bars, nightclubs (R5) -----------
    **{t: FOOD for t in (
        "Autre restauration rapide", "BBQ - Grillade", "Bar à burger", "Bar à tapas",
        "Bistro (boissons uniquement)", "Brasserie", "Cafe - Expresso bar", "Crêperie",
        "Fast-Food", "Fresh food - Salad-bar", "Friterie", "Gaufres", "Glacier",
        "Juice bar", "Petit-déjeuner", "Petite restauration", "Pita - Durum", "Pizzeria",
        # Filed under HoReCa: a seafood restaurant and a pastry tearoom, beside
        # the shop types "Poissonnerie - Produits de la mer" and "Pâtisserie".
        "Produits de la mer", "Pâtisseries",
        "Restaurant - Afrique (Autre)", "Restaurant - Amérique (Autre)",
        "Restaurant - Amérique (Nord)", "Restaurant - Asie (Autre)",
        "Restaurant - Europe (Autre)",
        "Restaurant - Méditerranée (Afrique - Asie - Europe)", "Restaurant - Océanie",
        "Restaurant gastronomique", "Restaurant traditionnel", "Salon de thé",
        "Sandwicherie", "Steakhouse", "Sushi bar",
        # R1: a cafeteria or food court in a ground-floor street survey is a
        # counter open to the street, not a staff canteen (flagged for the owner).
        "Cantine - Cafétéria - Food-court",
        "Bar - Pub", "Bar à cocktail", "Bar à vin", "Lounge Bar", "Bar à liqueurs (whisky, rhum,…)",
        "Bar karaoké", "Sports Bar", "e-sport bar", "Bar à jeux de société",
        # A shisha bar is a bar (NAICS 722410 drinking places).
        "Bar à Chicha",
        # Nightclubs not named as adult: kept, Food service (R5).
        "Night-club", "Blues - Jazz club", "Salsa - Latino club",
    )},
    # --- Retail: food shops ----------------------------------------------------
    **{t: RETAIL for t in (
        "Alimentation diététique", "Autres alcools (Rhum, Whisky, Liqueur,…)", "Bières",
        "Boucherie - Charcuterie", "Boulangerie", "Cafés", "Chocolat - Pralines",
        # A deli counter, France's traiteur shop (kept; R1's caterers are the
        # event trade with no counter).
        "Comptoir-traiteur",
        "Confiseries - Bonbons", "Crémerie - Fromagerie", "Drive-in boissons - Brasseur",
        "Fruits - Légumes", "Grainerie - Céréales", "Hypermarché", "Night-Shop",
        "Poissonnerie - Produits de la mer", "Pâtisserie", "Rôtisserie", "Supermarché",
        "Supérette", "Thés", "Vins", "Épicerie", "Épicerie fine - Produits artisanaux",
        "Épicerie spécialisée dans des produits étrangers",
        "Cigares - Tabac", "Cigarettes", "e-cigarettes", "Journaux - Magazines",
    )},
    # --- Retail: personal goods, health, beauty ---------------------------
    **{t: RETAIL for t in (
        "Accessoires de mode - Général", "Autres accessoires", "Bijouterie",
        "Bijouterie fantaisie", "Chapeaux", "Chaussures - Général", "Chaussures enfants et bébés",
        "Chaussures femmes", "Chaussures hommes", "Chemiserie", "Daim - Cuir - Manteaux",
        "Jeans - Pantalon", "Joaillerie", "Lingerie - Sous-vêtements - Bas", "Maillots",
        "Maroquinerie - Sacs", "Montres", "Parapluies - Gants", "Robes - Cérémonie",
        "Valises", "Vêtements - Général", "Vêtements bébés", "Vêtements enfants",
        "Vêtements femmes", "Vêtements hommes", "Vêtements professionnels",
        # Filed by the publisher under personal equipment, not Services: a
        # suit maker's shop (the screen had put it with alterations).
        "Tailleur - Costumes",
        # Pharmacies and opticians kept, Retail, on a general-retail register.
        "Pharmacie", "Parapharmacie", "Opticien", "Appareils auditifs",
        "Appareils orthopédiques - Bandagisterie - Prothèse", "Herboristerie",
        "Parfumerie", "Produits cosmétiques", "Produits capillaires",
    )},
    # --- Retail: home, DIY, furnishing, art --------------------------------
    **{t: RETAIL for t in (
        "Ameublement - Général", "Article ménagers - Général",
        "Articles de jardinage - Jardinerie", "Articles enfance - Puériculture",
        "Bricolage et matériaux - Général", "Carrelages", "Chauffage - Climatisation",
        "Cuisines", "Droguerie - Produits d'entretien", "Décoration - Général",
        "Fleurs - Plantes décoratives", "Linge de maison - Literie", "Lits - Matelas",
        "Luminaires", "Matériaux de construction", "Matériel de plomberie - Sanitaire",
        "Matériel électrique", "Meubles de maison - Contemporain", "Meubles de maison - Design",
        "Meubles de maison - Traditionnel", "Parquets", "Peintures - Papier peint",
        "Petits articles décoratifs - Bibelots", "Portes - Châssis - Volets",
        "Quincaillerie - Outillage", "Salles de bain", "Tapis", "Textiles d'ameublement",
        "Ustensiles de cuisine - Coutellerie", "Vaisselle - Articles de table",
        "Électromenagers", "Télévision - Hifi", "Équipement de la maison - Non déterminé",
        # Art galleries: Retail by precedent (NAICS 459920 in New Orleans,
        # Sacramento, Buenos Aires).
        "Galerie d'art (hors photo)", "Galerie photos", "Encadreur",
        # Craft workshops the publisher files as home-equipment shops.
        "Artisan du bois", "Artisan du verre", "cristal", "miroir", "ébéniste",
    )},
    # --- Retail: leisure goods ---------------------------------------------
    **{t: RETAIL for t in (
        "Accessoires téléphonie - GSM", "Articles carnaval - Farces - Déguisement",
        "Bandes dessinées", "Cadeaux - Souvenirs", "Carterie", "Chasse - Armes",
        "Collections (Timbres, pièces, statuettes BD,…)", "Course à pied",
        "Décoration et accessoires de fêtes (baptême, mariage,…)", "Films",
        "Instruments et accessoires de musique", "Jeux de société", "Jeux vidéos", "Jouets",
        "Librairie - Bouquinerie", "Loisirs créatifs et artistiques - Général",
        # Sex shops: kept, Retail (R3).
        "Love shop",
        "Matériel de photographie", "Matériel et nourriture pour animaux",
        "Matériel et équipement sportifs  - Général", "Matériel informatique", "Mercerie",
        "Modélisme", "Musique", "Papeterie - Matériel et accessoires de bureau",
        "Randonnée - Scoutisme - Camping", "Supports multimédias (tablettes,…)",
        "Textiles pour la confection", "Téléphonie - GSM", "Vente d'animaux",
        "Vêtements de sport",
    )},
    # --- Retail: vehicles and fuel (R4) ------------------------------------
    **{t: RETAIL for t in (
        "Station-service (essence, gaz,…)", "Voitures", "Motos", "Autres véhicules motorisés",
        "Vélos - Vélos électriques", "Trottinettes - Segway", "Pneus",
        "Pièces détachées pour véhicules motorisés", "Accessoires pour véhicules motorisés",
    )},
    # --- Personal services ---------------------------------------------------
    **{t: PERSONAL for t in (
        "Barbier", "Coiffeur", "Institut de beauté", "Onglerie - Manucure",
        # Commercial massage, not named as adult: kept (category rules).
        "Massage", "Solarium", "Spa", "Sauna", "Hammam", "Soins de la personne - Général",
        # Tattoo and piercing studios on their own type: kept (R2).
        "Tattoo", "Piercing",
        "Laverie - Wasserette", "Nettoyage à sec", "Toilettage animaux",
    )},
}

# type -> why it is out.
EXCLUDED_TYPES = {
    "Cellule vide - Statut inconnu": "vacant unit",
    # Lodging (category rules).
    "Appart-hôtel": "lodging", "Auberge de jeunesse": "lodging",
    "Chambre d'hôtes - Bed & Breakfast": "lodging", "Hôtel -  1 étoile": "lodging",
    "Hôtel -  2 étoiles": "lodging", "Hôtel -  3 étoiles": "lodging",
    "Hôtel -  4 étoiles": "lodging", "Hôtel -  5 étoiles": "lodging", "Motel": "lodging",
    "Location de salle pour banquet/soirée": "hall hire",
    # Members' clubs, not a bar open to the public.
    "Clubs privés": "private members' club",
    # Adult venues (R3).
    "Cabaret": "adult venue (R3)", "Peepshow": "adult venue (R3)",
    # Gambling (R5).
    "Casino": "gambling (R5)", "Jeux de hasard": "gambling (R5)",
    # Recreation and culture (NAICS 71).
    **{t: "recreation or culture" for t in (
        "Cinéma", "Infrastructure pour autre sport", "Musée généraliste", "Musée spécialisé",
        "Piscine", "Salle de billard", "Salle de bowling", "Salle de concert",
        "Salle de fitness - musculation", "Salle de mini-foot", "Salle polyvalente",
        "Salle polyvalente pour spectacle - Centre culturel",
        "Salle pour exposition temporaire (Centre de congrès,…)", "Stade de football",
        "Théâtre", "Zoo - Parc animalier", "Escape room", "Archéologie et histoire", "Art",
        "Bâtiments ou site à visiter", "Autre lieu touristique",
        "Agence de circuits touristiques (bus, bateau,…)", "Bibliothèque",
        "Dégustation - Cours (Cuisine, alcools, Bricolage…)")},
    # Catch-alls that say nothing about the premises (R2's logic).
    "Autre activité": "catch-all", "Autre infrastructure": "catch-all",
    "Autres loisirs": "catch-all",
    # Repairs and maintenance (NAICS 811).
    **{t: "repair or maintenance" for t in (
        "Cordonnier", "Clé-minute", "Réparation de vêtements",
        "Réparation matériel électrique ou multimédia", "Garage - Entretien automobile",
        "Garage - Entretien autres véhicules motorisés", "Entretien vélo", "Car-wash")},
    # Heating-fuel dealers (nonstore retail rule).
    "Combustible (charbon, pellets…)": "heating-fuel dealer",
    # Funeral (category rules).
    "Pompes funèbres": "funeral",
    # Offices, finance, agencies, post, telecom providers, rentals, printing.
    **{t: "office, agency or other service" for t in (
        "Agence de titres-services", "Agence de voyage", "Agence immobilière",
        "Agence intérimaire", "Agent de change", "Assurances", "Auto-école", "Banque - Prêt",
        "Bureau de poste", "Compagnie de transport", "Mutuelle", "Salle de vente",
        "Transfert d'argent", "Fournisseur téléphonie - Internet",
        "Téléphonie-cabine - Web café", "Point d'information touristique",
        "Imprimerie - Photocopie", "Graveur - Impression sur objets",
        "Coupes - Médailles - Trophées", "Studio photo", "Location de voitures",
        "Location outillage", "Location de vêtements", "Location vidéo")},
}

KNOWN_TYPES = set(TYPE_TO_BUCKET) | set(EXCLUDED_TYPES)
assert not set(TYPE_TO_BUCKET) & set(EXCLUDED_TYPES)
# The distinct single types of the 2025-10-17 survey (measured 2026-10-04).
# Re-measure if the survey changes.
assert len(KNOWN_TYPES) == 285, len(KNOWN_TYPES)
assert all(b in PRIORITY for b in TYPE_TO_BUCKET.values())


def _norm(s):
    return unicodedata.normalize("NFC", s).strip()


_LOOKUP = {_norm(t): t for t in KNOWN_TYPES}


def split_types(value):
    """'A, B (x, y), C' -> ['A', 'B (x, y)', 'C']: commas outside parentheses."""
    if not isinstance(value, str):
        return []
    out, depth, cur = [], 0, ""
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            if cur.strip():
                out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


assert split_types("Station-service (essence, gaz,…), Pneus") == [
    "Station-service (essence, gaz,…)", "Pneus"]


def types_of(value):
    """The known single types of one unit; an unknown type raises."""
    out = []
    for t in split_types(value):
        key = _LOOKUP.get(_norm(t))
        if key is None:
            raise ValueError(f"hub.brussels type not in brussels_hub.py: {t!r}")
        out.append(key)
    return out


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    kept = {TYPE_TO_BUCKET[t] for t in types_of(row.get(VALUE_COLUMN)) if t in TYPE_TO_BUCKET}
    for bucket in PRIORITY:
        if bucket in kept:
            return bucket
    return None
