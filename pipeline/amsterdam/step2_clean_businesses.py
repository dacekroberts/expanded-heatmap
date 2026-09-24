"""Amsterdam step 2: hospitality permits + BAG shop units -> the storefronts.

    python pipeline/amsterdam/step2_clean_businesses.py

Two layers of different kinds, read from the cache fetch_sources.py wrote:

  * PERMITS - the city's live register of hospitality operating permits. A
    named business with a point. Filtered by the taxonomy's permit mapping
    (the owner's, 2026-09-24). The few with no point are placed through the
    BAG address they name.
  * BAG SHOP UNITS - every unit whose use class is `winkelfunctie` and whose
    status is "in use". No name and no activity: the pin shows its address.
    A unit ALSO registered as a dwelling is left off (owner's call).

A takeaway in a shop-class unit is both a permit and a shop unit, so the two
layers are DE-DUPLICATED by address, the permit kept (it names the business).
Both counts are printed. Nothing here fetches.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.amsterdam import addresses, config  # noqa: E402
from pipeline.amsterdam.boundary import city_polygon  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.taxonomies import amsterdam_source as TAX  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402

RD_TO_WGS = Transformer.from_crs(config.CRS_SOURCE, config.CRS_GEOGRAPHIC, always_xy=True)


def _load(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/amsterdam/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def _lonlat(points):
    """RD New [x, y] (or None) -> (lon, lat) Series pair."""
    xs = [p[0] if p else float("nan") for p in points]
    ys = [p[1] if p else float("nan") for p in points]
    lon, lat = RD_TO_WGS.transform(xs, ys)
    return pd.Series(lon), pd.Series(lat)


def _display(street, num, letter, toev):
    s = f"{street} {num}{letter or ''}"
    return f"{s}-{toev}" if toev else s


def bag_addresses():
    """nummeraanduiding id -> (key, display address), for the shop units."""
    streets = {s["identificatie"]: s.get("naam") for s in _load(config.BAG_STREETS_JSON)}
    out = {}
    for a in _load(config.BAG_ADDRESSES_JSON):
        street = streets.get(a.get("ligtAanOpenbareruimteId"))
        if not street:
            continue
        parts = (street, a["huisnummer"], a.get("huisletter"), a.get("huisnummertoevoeging"))
        out[a["identificatie"]] = (addresses.key(*parts), _display(*parts))
    return out


def load_bag():
    units = pd.DataFrame(_load(config.BAG_UNITS_JSON))
    print(f"  BAG shop-class units: {len(units):,}")
    print("    " + ", ".join(f"{k} {v:,}" for k, v in units["statusOmschrijving"].value_counts().items()))
    units = units[units["statusOmschrijving"] == config.BAG_STATUS_KEEP].copy()
    emit("bag_units_in_use", len(units))
    classes = units["gebruiksdoel"].map(lambda g: {x.get("omschrijving") for x in (g or [])})
    also = classes.map(lambda c: bool(c & set(config.BAG_EXCLUDE_IF_ALSO)))
    mixed = classes.map(len) > 1
    print(f"  {len(units):,} in use: {int((~mixed).sum()):,} shop-only, {int(mixed.sum()):,} mixed, "
          f"of which {int(also.sum()):,} also a dwelling - LEFT OFF (owner's call)")
    units = units[~also].copy()
    emit("bag_units_kept", len(units))

    addr = bag_addresses()
    looked = units["heeftHoofdadresId"].map(addr)
    missing = int(looked.isna().sum())
    if missing:
        print(f"  {missing:,} units have no resolvable address - kept, labelled by the unit")
    units["addr_key"] = looked.map(lambda v: v[0] if isinstance(v, tuple) else None)
    units["address"] = looked.map(lambda v: v[1] if isinstance(v, tuple) else "Shop unit")
    lon, lat = _lonlat(units["geometrie"].map(lambda g: (g or {}).get("coordinates")).tolist())
    units["longitude"], units["latitude"] = lon.values, lat.values
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
        "zaak_categorie": None,
        "zaak_specificatie": None,
    })


def place_unplaced_permits(df):
    """The permits with no point, placed through the BAG address they name.

    Tier 1: street + number + letter + toevoeging exactly. Tier 2: the same
    without the toevoeging (a floor suffix the permit writes and the BAG files
    differently), accepted only when every candidate unit lies within 50 m of
    each other - one building, not two."""
    lookup = _load(config.BAG_PERMIT_LOOKUP_JSON)
    streets = {s["identificatie"]: s.get("naam") for s in lookup["streets"]}
    unit_xy = {u["identificatie"]: (u.get("geometrie") or {}).get("coordinates")
               for u in lookup["units"]}
    exact, loose = {}, {}
    for a in lookup["addresses"]:
        street = streets.get(a.get("ligtAanOpenbareruimteId"))
        xy = unit_xy.get(a.get("adresseertVerblijfsobjectId"))
        if not street or not xy:
            continue
        k = addresses.key(street, a["huisnummer"], a.get("huisletter"), a.get("huisnummertoevoeging"))
        exact.setdefault(k, []).append(xy)
        loose.setdefault(k[:3], []).append(xy)

    def pick(k):
        if k is None:
            return None, "unparsed"
        if k in exact:
            return exact[k][0], "exact"
        # "42 H" is ambiguous in free text: a lone letter after a space is read
        # as the huisletter, but Amsterdam's ground-floor H is a toevoeging.
        swapped = (k[0], k[1], k[3] if len(k[3]) == 1 else "", k[2])
        if (k[2] or k[3]) and swapped in exact:
            return exact[swapped][0], "letter/toevoeging swapped"
        cands = loose.get(k[:3], [])
        if cands:
            xs, ys = [c[0] for c in cands], [c[1] for c in cands]
            if max(xs) - min(xs) <= 50 and max(ys) - min(ys) <= 50:
                return cands[0], "no toevoeging"
        return None, "not found"

    need = df["x"].isna()
    tiers = {}
    for i in df.index[need]:
        xy, tier = pick(df.at[i, "addr_key"])
        tiers[tier] = tiers.get(tier, 0) + 1
        if xy:
            df.at[i, "x"], df.at[i, "y"] = xy
    print(f"  permits with no point: {int(need.sum())} - placed by BAG address: "
          + ", ".join(f"{k} {v}" for k, v in sorted(tiers.items())))
    return df


def load_permits(snapshot):
    raw = pd.DataFrame(_load(config.PERMITS_JSON))
    print(f"  hospitality permits: {len(raw):,} "
          f"({', '.join(f'{k} {v:,}' for k, v in raw['statusVergunning'].value_counts().items())})")
    emit("permits", len(raw))
    end = pd.to_datetime(raw["einddatum"], errors="coerce")
    ended = end < pd.Timestamp(snapshot)
    if ended.any():
        print(f"  {int(ended.sum())} permits are past their end date "
              f"({end[ended].min():%Y-%m-%d} to {end[ended].max():%Y-%m-%d}) and still "
              f"'{'/'.join(sorted(raw.loc[ended, 'statusVergunning'].unique()))}' - "
              + ("KEPT: the register prunes lapsed permits itself, within about three "
                 "months, so these read as renewals in progress"
                 if config.KEEP_PERMITS_PAST_END_DATE else "DROPPED"))
        emit("permits_past_end_date", int(ended.sum()))
    if not config.KEEP_PERMITS_PAST_END_DATE:
        raw = raw[~ended]
    kept = [TAX.permit_kept(c, None if s is None or s != s else s)
            for c, s in zip(raw["zaakCategorie"], raw["zaakSpecificatie"])]
    raw = raw.assign(_kept=kept)
    print("  by category (kept / out):")
    for cat, g in raw.groupby("zaakCategorie"):
        print(f"      {cat:<28} {int(g['_kept'].sum()):>5,} / {int((~g['_kept']).sum()):>5,}")
    df = raw[raw["_kept"]].copy()
    print(f"  {len(df):,} food-service permits kept, {len(raw) - len(df):,} out")
    emit("permits_kept", len(df))

    xy = df["locatie"].map(lambda g: (g or {}).get("coordinates"))
    df["x"] = xy.map(lambda p: p[0] if p else None)
    df["y"] = xy.map(lambda p: p[1] if p else None)
    df["addr_key"] = df["adres"].map(addresses.permit_key)
    df = place_unplaced_permits(df)
    placed = df["x"].notna()
    if (~placed).any():
        print(f"  {int((~placed).sum())} permits could not be placed - LEFT OFF:")
        for _, r in df[~placed].iterrows():
            print(f"      {r['zaaknaam']} | {r['adres']}")
    df = df[placed].copy()
    lon, lat = RD_TO_WGS.transform(df["x"].astype(float).tolist(), df["y"].astype(float).tolist())
    parsed = df["adres"].map(addresses.parse)
    return pd.DataFrame({
        "record_id": "permit:" + df["id"].astype(str),
        "source": "permit",
        "business_name": df["zaaknaam"].str.strip().values,
        "name_is_address": False,
        "address": [(_display(*p) if p else a) for p, a in zip(parsed, df["adres"])],
        "addr_key": df["addr_key"].values,
        "latitude": lat,
        "longitude": lon,
        "activity": [TAX.activity_label(c, s) for c, s in zip(df["zaakCategorie"], df["zaakSpecificatie"])],
        "zaak_categorie": df["zaakCategorie"].values,
        "zaak_specificatie": df["zaakSpecificatie"].values,
    })


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    snapshot = prov["permits_snapshot"]
    print(f"Permits (snapshot {snapshot}):")
    permits = load_permits(snapshot)
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
    poly = city_polygon(verbose=False)
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(poly).values
    if (~inside).any():
        print(f"  {int((~inside).sum())} rows fall outside the gemeente polygon - dropped:")
        print(df.loc[~inside, ["source", "business_name", "address"]].head(10).to_string())
    df = df[inside]
    b = config.AMSTERDAM_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()
    if df["record_id"].duplicated().any():
        sys.exit("a record appears twice")

    print(f"\n  {len(df):,} storefronts: " + ", ".join(
        f"{k} {v:,}" for k, v in df["source"].value_counts().items()))
    emit("storefronts", len(df))
    out = df[["record_id", "source", "business_name", "name_is_address", "address",
              "latitude", "longitude", "activity", "zaak_categorie", "zaak_specificatie"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
