"""Step 2 for every Japanese city: the city's own permit lists and 生活衛生
registers, classified by japan_eigyo and placed by the MLIT join
(japan_register.py). Built for Kobe (2026-09-27), the first Japanese city, and
written here from the start so the other Japanese cities share one copy. A
city's step 2 calls run(config).

  1. Each source in config.SOURCES read by column NAME (japan_register's
     premises columns); `source` names the register ("food", "barber",
     "beauty", "laundry"), which decides Personal services.
  2. Not a premises dropped: vehicles, stalls, "anywhere in the city" (一円),
     storeless pick-ups. Then the taxonomy: every row it does not bucket
     (manufacturing, vending machines, institutional catering...) is dropped
     and counted by the rule that decided it.
  3. The JOIN, tiered: block, town-chōme centroid, none. Block and chōme are
     kept and the tier travels with the row; unplaced rows are dropped,
     counted and sampled.
  4. One pin per premises and bucket: rows repeating (address, trade name,
     bucket) are one premises holding several permits of one kind.
  5. The name rule (owner 2026-09-27): where the trade name IS the operator's
     own name (japan_register.name_is_operator, compared in memory), the map
     shows the permit type instead. Counted; the operator's name is never kept.
  6. The owner's 菓子 / そうざい call (2026-09-24): the share of those rows whose
     trade name reads as a factory or central kitchen is MEASURED and printed,
     for the page and DECISIONS.md, not filtered.

Config needs: SOURCES, source_csv(), REQUIRED_COLUMNS, ISJ_DIR, PREFECTURE,
MUNICIPALITY, CITY_BBOX, TAXONOMY_SYSTEM, BUSINESSES_CLEAN_CSV, SLUG. Reads the
cache and NEVER fetches.
"""
import collections
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import japan_register as jr  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies import japan_eigyo  # noqa: E402

# A trade name that reads as a production site rather than a counter.
FACTORY = re.compile(r"工場|製造所|製造部|セントラルキッチン|センター|本社|事業所|倉庫")
# What a register row is called when its name is withheld.
REGISTER_TYPE = {"barber": "理容所", "beauty": "美容所", "laundry": "クリーニング所"}


def need(path, slug):
    if not Path(path).exists():
        sys.exit(f"missing {path}\nRun: python pipeline/{slug}/fetch_sources.py")
    return path


def key_addr(a):
    return re.sub(r"[‐‑‒–—―−ｰー－]", "-", unicodedata.normalize("NFKC", a or "").replace(" ", "").replace("　", ""))


def run(config, write=True):
    sys.stdout.reconfigure(encoding="utf-8")
    need(config.ISJ_DIR, config.SLUG)
    blocks, chome = jr.load_city_isj(config.ISJ_DIR)
    print(f"  MLIT 位置参照情報: {len(blocks):,} block keys, {len(chome):,} town-chōme keys")

    permits = []
    for key in config.SOURCES:
        rows = list(jr.city_rows(need(config.source_csv(key), config.SLUG)))
        missing = [c for c in config.REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            sys.exit(f"{key}: header lacks {missing}")
        flags = [jr.name_is_operator(r) for r in rows]
        ps = jr.permits_from_rows(rows, config.PREFECTURE, config.MUNICIPALITY)
        for p, f in zip(ps, flags):
            p["source"], p["name_is_operator"] = key, f
        permits += ps
        emit(f"rows_{key}", len(ps))
        print(f"  {key:8} {len(ps):>7,} rows")
    del rows  # the raw rows carry the operator columns; nothing below may see them

    df = pd.DataFrame(permits)
    mobile = df["mobile"]
    print(f"  not a premises (vehicle, stall, 一円, storeless): {int(mobile.sum()):,}")
    emit("not_a_premises", int(mobile.sum()))
    df = df[~mobile].copy()
    decided = [japan_eigyo.explain(t, s) for t, s in zip(df["type"], df["source"])]
    df["bucket"] = [b for b, _ in decided]
    df["rule"] = [r for _, r in decided]
    out = df[df["bucket"].isna()]
    print(f"  not a storefront, by rule: {int(len(out)):,}")
    for (rule, n) in out["rule"].value_counts().items():
        print(f"    {n:>6,}  {rule}")
    emit("not_storefront", len(out))
    df = df[df["bucket"].notna()].copy()
    print(f"  storefront rows: {len(df):,}  {df['bucket'].value_counts().to_dict()}")

    # --- the join --------------------------------------------------------------
    joined = pd.DataFrame(jr.join_city(df.to_dict("records"), blocks, chome))
    tab = pd.crosstab(joined["bucket"], joined["tier"], margins=True)
    print("  the join by bucket:\n" + "\n".join("    " + ln for ln in tab.to_string().splitlines()))
    for tier, n in joined["tier"].value_counts().items():
        emit(f"join_{tier}", int(n))
    none = joined[joined["tier"] == "none"]
    print(f"  unplaced {len(none):,} ({len(none) / len(joined):.1%}); samples:")
    for a in none["addr"].iloc[:: max(1, len(none) // 10)][:10]:
        print(f"     {a}")
    df = joined[joined["tier"] != "none"].copy()
    df["latitude"] = [p[0] for p in df["pt"]]
    df["longitude"] = [p[1] for p in df["pt"]]
    bb = config.CITY_BBOX
    inb = df["latitude"].between(bb["lat_min"], bb["lat_max"]) & df["longitude"].between(bb["lon_min"], bb["lon_max"])
    if not inb.all():
        sys.exit(f"{int((~inb).sum())} joined points outside CITY_BBOX - an MLIT key from another place?")

    # --- one pin per premises and bucket ------------------------------------------
    df["premises"] = [(key_addr(a), jr._name_key(n), b) for a, n, b in zip(df["addr"], df["name"], df["bucket"])]
    dup = df["premises"].duplicated()
    print(f"  one pin per premises and bucket: {int(dup.sum()):,} repeat rows dropped "
          f"(one premises, several permits of one kind)")
    emit("repeat_permits_dropped", int(dup.sum()))
    df = df[~dup].copy()

    # --- the name rule --------------------------------------------------------------
    hidden = df["name_is_operator"]
    df["permit_type"] = [REGISTER_TYPE.get(s, t) for s, t in zip(df["source"], df["type"])]
    df["business_name"] = df["name"].where(~hidden, df["permit_type"])
    print(f"  names withheld (the trade name IS the operator's own name): {int(hidden.sum())}; "
          f"shown as their permit type")
    emit("names_withheld", int(hidden.sum()))

    # --- the owner's 菓子 / そうざい measurement --------------------------------------
    made = df["rule"].str.startswith(("confectioner", "deli"))
    fac = made & df["name"].map(lambda s: bool(FACTORY.search(unicodedata.normalize("NFKC", s or ""))))
    print(f"  菓子 / そうざい rows: {int(made.sum()):,}; trade name reads as a factory or central kitchen: "
          f"{int(fac.sum()):,} ({fac.sum() / max(1, made.sum()):.1%}) - kept, measured (owner 2026-09-24)")
    emit("sweets_deli_rows", int(made.sum()))
    emit("sweets_deli_factory_like", int(fac.sum()))

    out = df[["business_name", "permit_type", "source", "latitude", "longitude", "addr", "tier"]].rename(
        columns={"addr": "address"})
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    counts = collections.Counter(japan_eigyo.classify(r) for r in kept.to_dict("records"))
    print(f"  storefronts: {len(kept):,}  {dict(counts)}")
    for b, n in counts.items():
        emit(f"storefronts_{b.replace(' ', '_').lower()}", n)
    emit("storefronts", len(kept))
    if write:
        kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
        print(f"  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts")
    return kept
