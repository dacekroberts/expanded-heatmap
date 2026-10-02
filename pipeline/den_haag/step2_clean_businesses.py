"""Den Haag step 2: the city's hospitality permits + BAG shop units.

    python pipeline/den_haag/step2_clean_businesses.py

Two layers of different kinds, read from the cache fetch_sources.py wrote:

  * PERMITS - the Gemeente Den Haag's `Horecavergunningen` layer. Granted or
    notified permits only (the pending applications are left out: owner, call
    24). Its text fields arrive double-encoded (UTF-8 read as Windows-1252:
    "cafÃ©"), and are repaired first. The type of business decides the bucket
    (`pipeline/taxonomies/den_haag_source.py`); a permit whose own description
    records that the business has gone (CLOSED_WORDS) is left out. The trade
    name is taken from the description: the city's staff notes in brackets,
    "MELDING" and the leading type word are removed.
  * BAG SHOP UNITS - every `winkelfunctie` unit in use, from PDOK, with its
    address (Rotterdam's query). A unit also registered as a dwelling is left
    off (Amsterdam's owner call). No name, no activity: the pin shows its
    address.

Both layers carry an address, so they are de-duplicated BY ADDRESS, the permit
kept (Amsterdam's rule: it names the business). Every count is printed.
Nothing here fetches.
"""
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.den_haag import config  # noqa: E402
from pipeline.den_haag.gemeenten import gemeente_geometry  # noqa: E402
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies import den_haag_source as TAX  # noqa: E402

FETCH = "pipeline/den_haag/fetch_sources.py"
TEXT_FIELDS = ("OMSCHRIJVI", "TYPEBEDRIJ", "STRAAT", "HUISLT", "TOEV", "STATUS", "STADSDEEL",
               "CATEGORIE")

# A permit whose OWN DESCRIPTION records that the business has gone, read by
# eye on 2026-09-30 (the layer keeps the city's staff notes in the description):
# the business ended or was struck off ("opgeheven", "beëindigd", "uit KvK",
# "uitgeschreven KvK"), the permit or application was withdrawn or lapsed
# ("ingetrokken", "vervallen"), refused with no notification possible ("geen
# melding mogelijk"), the operator left or will not trade ("vertrokken",
# "enkele jaren dicht", "geen gebruik maken", "afzien van exploitatie"), or the
# record is marked historical ("historisch"). NOT closures, and kept: a closure
# order that ran out in 2024 ("gesloten tot"), and an operator who gave up the
# permit to trade under a notification ("gaat onder melding exploiteren",
# "melding blijft geldig").
CLOSED_WORDS = re.compile(
    r"opgeheven|opgegeven|beëindigd|uit kvk|uitgeschreven kvk|ingetrokken|vervallen|"
    r"geen melding mogelijk|vertrokken|enkele jaren dicht|geen gebruik maken|"
    r"afzien van exploitatie|historisch", re.I)

# A permit whose TYPE says food premises but whose OWN DESCRIPTION names a
# venue the category rules leave out (docs/category_rules.md; read by eye on
# 2026-09-30) is re-typed by that description, first match wins, before the
# taxonomy decides. The type is the register's coarse word; the description
# says what the premises is.
RETYPE = (
    # R1 and Amsterdam's Additionele horeca: catering inside a care home, a
    # school or a sports club, and a stadium.
    (r"verpleeghuis|verzorgingscentrum|woonzorgcentra|schoolkantine|leerwerkproject", "kantine"),
    (r"vereniging|sportkantine|stadion|sporthal|sportcomplex|biljartaccommodatie", "sportkantine"),
    # Amsterdam's Culturele horeca: museum and theatre cafés.
    (r"museumcafé|museum beeld|theatercomplex", "theaterfoyer"),
    # Lodging, and the restaurants and bars inside hotels and hostels
    # (Florence's rule). Not the hotel school's public training restaurant.
    (r"hotel(?!school)|hôtel|hostel", "hotel-restaurant"),
    # R3: premises the register names as adult.
    (r"erotisch", "seksinrichting"),
    # A members' association's meeting room with a coffee bar (Amsterdam's
    # Sociëteit).
    (r"bijeenkomstruimte", "sociëteit"),
)

# A shown trade name that is only a person's name (Kansas City's and Houston's
# rule): the pin shows the type instead. Read by eye on 2026-09-30 from every
# shown name residence.py's shape test reads as a person's - 641, almost all
# trade names its English organisation words do not cover ("Rakang Thai",
# "Toko Asli", "Bakker Tim") or brands ("Bram Ladage", "Walter Benedict").
# Step 2 stops if one of these is no longer shown, so a refresh re-reads the
# list.
# Keys, not names (pipeline/name_keys.py): a new name's key is its output.
PERSON_NAMED = (
    "44d2d6136a9da2d4", "9d222fb5a73cd27a", "d627bb6e214ba612", "83207fb3a7398a27",
    "5ac7fcf5956684f1",
)

# Leading words the register writes before a trade name, in lower case
# ("restaurant Pex", "koffiehuis/broodjeszaak Le Papillon"), its misspellings
# included. A capitalised word is never stripped: "Grand Cafe Le Palet" and
# "Restaurant Caribbean" are names; nor is an article ("de Paraplu").
TYPE_WORDS = {w for t in TAX.PERMIT_TYPES for w in re.split(r"[-/\s]+", t) if w} | {
    "cafe", "cafè", "afhaal", "afhaalrestaurant", "afhaalcentrum", "afhgaalwinkel",
    "afhaalwinnkel", "koffiebar", "koffiezaak", "koffiecorner", "koffie", "lounge", "bar", "en",
    "met", "in", "annex", "bezorgcentrum", "bezorgservice", "bezorging", "take", "away", "petit",
    "hotelbar", "pizzaria", "snackkiosk", "snack", "kiosk", "viskiosk", "toko", "theatercafé",
    "tearoom", "melding", "horeca", "lunchroon", "luchroom", "restauraant", "rstaurant",
    "snackabr", "snackorner", "grilroom", "fastfood", "fasfoodrestaurant", "fastvoodrestaurant",
    "doscotheek", "sportcafe", "eethoek", "sappenbar", "biljartcafé", "danscafé", "wijnbar",
    "proeverij", "patisserie", "shishalounge", "sisha", "loungeroom", "chocolaterie",
    "foodcorner", "viswinkel", "eetgelegenheid", "cocktailbar", "espressobar", "sushibar",
    "theehuis", "foodhall", "visrestaurant", "pannenkoekenrestaurant", "beachclub",
    "paviljoen", "banketbakkerij", "wok", "vegetarisch", "pizza", "jazzclub",
    "kermisautomaten", "shoarma", "broodzaak", "eetcafe", "grandcafe", "roeibootverhuur",
    "theeschenkerij"}


def repair(s):
    """UTF-8 that was read as Windows-1252 (or Latin-1), back to UTF-8."""
    if not isinstance(s, str):
        return s
    for enc in ("cp1252", "latin-1"):
        try:
            return s.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return s


def trade_name(desc):
    """The trade name in a permit's description, or None if only a type remains."""
    s = re.sub(r"\([^)]*\)", " ", desc or "")          # staff notes, (afhaal)
    s = re.sub(r"\(.*$", " ", s)                        # an unclosed note
    s = re.sub(r"\bmelding( horeca)?\b", " ", s, flags=re.I)
    words = s.split()
    while words and words[0][0].islower() and all(
            p in TYPE_WORDS for p in re.split(r"[-/,]+", words[0].lower()) if p):
        words.pop(0)
    name = " ".join(words).strip(" -,:")
    return name or None


def _load(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python {FETCH}")
    return json.loads(path.read_text(encoding="utf-8"))


def _addr_key(postcode, number, letter, toev):
    pc = re.sub(r"\s+", "", str(postcode or "")).upper()
    try:
        n = int(str(number).strip())
    except ValueError:
        return None
    if not re.fullmatch(r"\d{4}[A-Z]{2}", pc):
        return None
    return (pc, n, str(letter or "").strip().upper(), str(toev or "").strip().upper())


def _display(street, number, letter, toev):
    s = f"{(street or '').strip()} {str(number).strip()}{(letter or '').strip()}"
    t = (toev or "").strip()
    return f"{s}-{t}" if t else s


def load_permits():
    feats = _load(config.HORECA_JSON)
    raw = pd.DataFrame([f["attributes"] for f in feats])
    leaked = sorted(set(raw.columns) & set(config.HORECA_FORBIDDEN))
    if leaked:
        sys.exit(f"the cache holds {leaked} - it was never meant to; re-fetch")
    raw["longitude"] = [f["geometry"]["x"] for f in feats]
    raw["latitude"] = [f["geometry"]["y"] for f in feats]
    print(f"  permits in the layer: {len(raw):,}")
    emit("permits_in_layer", len(raw))

    changed = 0
    for col in TEXT_FIELDS:
        fixed = raw[col].map(repair)
        changed += int((fixed != raw[col]).sum())
        raw[col] = fixed
    left = raw["OMSCHRIJVI"].fillna("").str.contains("Ã|Â", regex=True)
    print(f"  double-encoded text repaired in {changed:,} fields; "
          f"{int(left.sum())} descriptions still garbled")
    if left.any():
        sys.exit(f"descriptions still garbled after the repair: "
                 f"{raw.loc[left, 'OMSCHRIJVI'].head(5).tolist()}")

    status = raw["STATUS"].fillna("").str.strip()
    unknown = sorted(set(status) - set(config.STATUS_KEPT) - set(config.STATUS_PENDING))
    if unknown:
        sys.exit(f"unknown STATUS value(s) {unknown} - decide them in config")
    print("  by status: " + ", ".join(f"{k} {v:,}" for k, v in status.value_counts().items()))
    pending = status.isin(config.STATUS_PENDING)
    print(f"  {int(pending.sum())} pending applications left out (owner, call 24)")
    emit("permits_pending_out", int(pending.sum()))
    df = raw[~pending].copy()
    emit("permits_granted", len(df))

    df["type_bedrijf"] = df["TYPEBEDRIJ"].fillna("").str.strip()
    desc = df["OMSCHRIJVI"].fillna("")
    todo = df["type_bedrijf"].map(TAX.permit_kept)
    print("  food-typed permits re-typed by their own description (RETYPE):")
    for pat, new in RETYPE:
        hit = todo & desc.str.contains(pat, case=False, regex=True)
        df.loc[hit, "type_bedrijf"] = new
        todo &= ~hit
        print(f"    {int(hit.sum()):>3} -> {new:<16} ({pat})")
    emit("permits_retyped", int((df["type_bedrijf"] != df["TYPEBEDRIJ"].fillna("").str.strip()).sum()))
    kept_type = df["type_bedrijf"].map(TAX.permit_kept)
    print(f"  by type: {int(kept_type.sum()):,} food premises, {int((~kept_type).sum()):,} out "
          f"(the taxonomy): " + ", ".join(
              f"{k or 'blank'} {v}" for k, v in
              df.loc[~kept_type, "type_bedrijf"].value_counts().head(12).items()))
    emit("permits_type_out", int((~kept_type).sum()))

    closed = kept_type & df["OMSCHRIJVI"].fillna("").str.contains(CLOSED_WORDS)
    print(f"  {int(closed.sum())} food permits whose own description records the business "
          f"gone - left out:")
    for d in df.loc[closed, "OMSCHRIJVI"]:
        print(f"      {d[:110]}")
    emit("permits_closed_out", int(closed.sum()))
    df = df[kept_type & ~closed].copy()

    df["addr_key"] = [_addr_key(*v) for v in
                      zip(df["POSTCODE"], df["HUISNR"], df["HUISLT"], df["TOEV"])]
    df["address"] = [_display(*v) for v in zip(df["STRAAT"], df["HUISNR"], df["HUISLT"], df["TOEV"])]
    print(f"  {int(df['addr_key'].isna().sum())} kept permits carry no usable postcode and "
          f"number (kept; not matched to the BAG)")

    # One premises, several permits: the same address with more than one
    # granted or notified permit (an old permit beside a newer notification).
    # The newest year is kept; the others are the same door.
    df["_year"] = pd.to_numeric(df["JAAR"], errors="coerce").fillna(0)
    keyed = df[df["addr_key"].notna()].sort_values(["_year", "FID"])
    dup = keyed.duplicated("addr_key", keep="last")
    print(f"  {int(dup.sum())} older permits at an address that has a newer one - "
          f"one premises, the newest kept")
    emit("permits_same_address", int(dup.sum()))
    df = df.drop(index=keyed.index[dup])

    df["business_name"] = df["OMSCHRIJVI"].map(trade_name)
    unnamed = df["business_name"].isna()
    print(f"  {int(unnamed.sum())} descriptions are only a type word - the pin shows the type")
    name_keys = keys_of(df["business_name"])
    person = name_keys.isin(PERSON_NAMED)
    gone = set(PERSON_NAMED) - set(name_keys[person])
    if gone:
        sys.exit(f"PERSON_NAMED keys no longer matched: {sorted(gone)} - re-read the list")
    print(f"  {int(person.sum())} trade names that are only a person's name - the pin shows "
          f"the type (PERSON_NAMED)")
    emit("names_withheld", int(person.sum()))
    df.loc[unnamed | person, "business_name"] = (
        df.loc[unnamed | person, "type_bedrijf"].map(TAX.activity_label))
    emit("permits_kept", len(df))
    return pd.DataFrame({
        "record_id": "permit:" + df["ID"].astype(str),
        "source": "permit",
        "business_name": df["business_name"].values,
        "name_is_address": False,
        "address": df["address"].values,
        "addr_key": df["addr_key"].values,
        "latitude": df["latitude"].values,
        "longitude": df["longitude"].values,
        "activity": df["type_bedrijf"].map(TAX.activity_label).values,
        "type_bedrijf": df["type_bedrijf"].values,
        "permit_year": df["JAAR"].values,
    })


def load_bag():
    feats = _load(config.BAG_UNITS_JSON)
    units = pd.DataFrame([f["properties"] for f in feats])
    units["longitude"] = [f["geometry"]["coordinates"][0] for f in feats]
    units["latitude"] = [f["geometry"]["coordinates"][1] for f in feats]
    print(f"  BAG shop-class units in use: {len(units):,}")
    emit("bag_units_in_use", len(units))
    classes = units["gebruiksdoel"].fillna("").map(
        lambda s: {x.strip() for x in s.split(",") if x.strip()})
    also = classes.map(lambda c: bool(c & set(config.BAG_EXCLUDE_IF_ALSO)))
    mixed = classes.map(len) > 1
    print(f"  {int((~mixed).sum()):,} shop-only, {int(mixed.sum()):,} mixed, of which "
          f"{int(also.sum()):,} also a dwelling - LEFT OFF (Amsterdam's owner call)")
    emit("bag_also_dwelling", int(also.sum()))
    units = units[~also].copy()
    emit("bag_units_kept", len(units))
    units["address"] = [_display(*v) for v in zip(units["openbare_ruimte"], units["huisnummer"],
                                                  units["huisletter"], units["toevoeging"])]
    units["addr_key"] = [_addr_key(*v) for v in zip(units["postcode"], units["huisnummer"],
                                                   units["huisletter"], units["toevoeging"])]
    return pd.DataFrame({
        "record_id": "bag:" + units["identificatie"].astype(str),
        "source": "bag",
        "business_name": units["address"].values,
        "name_is_address": True,
        "address": units["address"].values,
        "addr_key": units["addr_key"].values,
        "latitude": units["latitude"].values,
        "longitude": units["longitude"].values,
        "activity": TAX.BAG_LABEL,
        "type_bedrijf": None,
        "permit_year": None,
    })


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    print("Gemeente Den Haag permit layer:")
    permits = load_permits()
    print("\nBAG:")
    bag = load_bag()

    # --- de-duplication: a permit and a shop unit at one address ------------
    permit_keys = set(permits["addr_key"].dropna())
    dup = bag["addr_key"].isin(permit_keys)
    print(f"\n  de-duplication by address: {int(dup.sum()):,} shop units share an exact "
          f"address with a kept permit - the permit is kept (it names the business)")
    emit("bag_deduplicated", int(dup.sum()))
    bag = bag[~dup]

    df = pd.concat([permits, bag], ignore_index=True)
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    if len(df) != before:
        sys.exit(f"filter_to_storefront dropped {before - len(df)} rows the layers already "
                 f"decided - the taxonomy and step 2 disagree")

    # --- both layers are the gemeente's own; check rather than assume -------
    poly = gemeente_geometry()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(poly).values
    if (~inside).any():
        print(f"  {int((~inside).sum())} rows fall outside the gemeente polygon - dropped: "
              + ", ".join(f"{k} {v}" for k, v in df.loc[~inside, "source"].value_counts().items()))
    emit("outside_gemeente", int((~inside).sum()))
    df = df[inside]
    b = config.DEN_HAAG_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()
    if df["record_id"].duplicated().any():
        sys.exit("a record appears twice")

    # --- the privacy read: a shown name shaped like a person's --------------
    shown = df.loc[~df["name_is_address"], "business_name"]
    person = shown[shown.map(looks_personal)]
    print(f"\n  shown trade names shaped like a person's (residence.looks_personal): "
          f"{len(person)}" + (": " + "; ".join(sorted(person)) if len(person) else ""))
    emit("names_person_shaped", len(person))

    print(f"\n  {len(df):,} storefronts: " + ", ".join(
        f"{k} {v:,}" for k, v in df["source"].value_counts().items()))
    emit("storefronts", len(df))
    out = df[["record_id", "source", "business_name", "name_is_address", "address",
              "latitude", "longitude", "activity", "type_bedrijf", "permit_year"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
