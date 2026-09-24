"""Join a Japanese municipality's food-business permits to MLIT's 位置参照情報
(location reference information), and report the result in TIERS.

WHY A JOIN, NOT A GEOCODER
--------------------------
Japan's permits follow a national schema (推奨データセット) whose 緯度/経度 and
町字ID columns are declared and EMPTY (0% on Minato's 5,721 rows). But 98% of
rows already split the address into 都道府県 / 市区町村 / 町字 / 番地以下, and
MLIT publishes, per municipality, a table of exactly those components with a
coordinate: block level (街区, edition 24.0a) and town-chōme level (大字・町丁目,
edition 19.0b). So the coordinate is a dict lookup - Taiwan's door-plate join,
one level coarser. Block precision is ample for 160-960 m rings.

TIERS, NEVER ONE RATE (address-join Step 6)
-------------------------------------------
    block    町字 + 街区符号 (the first number of 番地以下) found in the block file
    chome    町字 found in the town-chōme file (its centroid)
    none     neither

MINATO IS THE CONTROL - run it first after ANY change to the normalisation,
and nothing else counts until it reproduces.

Normalisation is found by READING MISSES (`--misses`), never by anticipating.
Each rule below names the misses that motivated it.

Needs (gitignored, never committed), under data/<city>/raw/: the permit CSV and
the two ISJ zips. Downloading is fetch work, not this script's.

Usage:
    python scripts/screen_japan_join.py minato             # the control, first
    python scripts/screen_japan_join.py minato --misses    # print miss classes and samples
    python scripts/screen_japan_join.py minato --gsi 100   # cross-check 100 block hits against GSI, 1 req/s
"""
import collections
import datetime
import json
import random
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# The join itself lives in the pipeline, shared with the builds; this script MEASURES it.
from pipeline.countries.japan_register import (  # noqa: E402
    haversine_m, join, join_city, kyoto_permit_stream, load_city_isj, load_city_permits, load_isj, load_permits,
    permits_from_rows)

# municipality -> (municipality code, name, permit CSV, ISJ block zip, ISJ chōme zip)
MUNICIPALITIES = {
    "minato": ("13103", "港区", "tokyo/raw/food_business_all.csv",
               "tokyo/raw/13103-24.0a.zip", "tokyo/raw/13103-19.0b.zip"),
    "chuo": ("13102", "中央区", "tokyo/raw/13102/syokuhineigyoukyoka.csv",
             "tokyo/raw/13102/13102-24.0a.zip", "tokyo/raw/13102/13102-19.0b.zip"),
    "shinjuku": ("13104", "新宿区", "tokyo/raw/13104/000399975.csv",
                 "tokyo/raw/13104/13104-24.0a.zip", "tokyo/raw/13104/13104-19.0b.zip"),
    "koto": ("13108", "江東区", "tokyo/raw/13108/131083_015_food_business_all.csv",
             "tokyo/raw/13108/13108-24.0a.zip", "tokyo/raw/13108/13108-19.0b.zip"),
    # the wards' own sites, 2026-09-24 (Shibuya's host is its ArcGIS catalogue - owner accepted)
    "shibuya": ("13113", "渋谷区", "tokyo/raw/13113/131130_food_businesses_list.csv",
                "tokyo/raw/13113/13113-24.0a.zip", "tokyo/raw/13113/13113-19.0b.zip"),
}
# the 生活衛生 registers - personal services - one entry per ward and kind
_LIFE = {"13101": ("千代田区", "131016_chiyodaku"), "13105": ("文京区", "131059_bunkyoku"),
         "13106": ("台東区", "131067_taitoku"), "13109": ("品川区", "131091_shinagawaku"),
         "13111": ("大田区", "131113_otaku"), "13113": ("渋谷区", "131130_shibuyaku"),
         "13116": ("豊島区", "131164_toshimaku"), "13118": ("荒川区", "131181_arakawaku"),
         "13122": ("葛飾区", "131229_katsushikaku")}
for _c, (_ward, _stem) in _LIFE.items():
    for _kind, _file in (("beauty", "biyousyo"), ("barber", "riyousyo"), ("laundry", "cleaning")):
        MUNICIPALITIES[f"{_c}-{_kind}"] = (_c, _ward, f"tokyo/raw/{_c}/{_stem}_{_file}.csv",
                                           f"tokyo/raw/{_c}/{_c}-24.0a.zip", f"tokyo/raw/{_c}/{_c}-19.0b.zip")
for _kind, _file in (("beauty", "biyou"), ("barber", "riyou"), ("laundry", "cleaning")):
    MUNICIPALITIES[f"13103-{_kind}"] = ("13103", "港区", f"tokyo/raw/13103/{_file}.csv",
                                        "tokyo/raw/13103-24.0a.zip", "tokyo/raw/13103-19.0b.zip")


# Designated cities (政令指定都市): each WARD has its own MLIT files, and one
# city-wide permit list names the ward inside the address. Keys carry the ward.
# city -> (prefecture, city name, permit files, ISJ directory)
CITIES = {
    "sapporo": ("北海道", "札幌市", ["sapporo/raw/shokuhin260331.csv"], "sapporo/raw/isj"),
    "osaka": ("大阪府", "大阪市", ["osaka/raw/260630zenku.csv"], "osaka/raw/isj"),
    "kobe": ("兵庫県", "神戸市", ["kobe/raw/20260407150739.csv"], "kobe/raw/isj"),
    # personal services - the 生活衛生 registers, same join
    "sapporo-life": ("北海道", "札幌市", ["sapporo/raw/sapporo-eigyoshisetsu-riyo-r80731.csv",
                                        "sapporo/raw/sapporo-eigyoshisetsu-biyo-r80731.csv",
                                        "sapporo/raw/sapporo-eigyoshisetsu-cleaning-r80731.csv"], "sapporo/raw/isj"),
    "osaka-life": ("大阪府", "大阪市", ["osaka/raw/ri20260331.csv", "osaka/raw/bi20260331.csv",
                                     "osaka/raw/cleaning20260331.csv"], "osaka/raw/isj"),
    "kobe-life": ("兵庫県", "神戸市", ["kobe/raw/r7_riyousho.csv", "kobe/raw/r7_biyousho.csv",
                                     "kobe/raw/r7_cleaning.csv"], "kobe/raw/isj"),
    # Sendai publishes XLSX inside ZIPs: food as one sheet per ward office (plus
    # the 食品監視センター's), and nine 生活衛生 workbooks in one ZIP - "::" picks members.
    "sendai": ("宮城県", "仙台市", ["sendai/raw/r7shokuhinichiran.zip"], "sendai/raw/isj"),
    "sendai-life": ("宮城県", "仙台市", ["sendai/raw/260331.zip::4_理容所", "sendai/raw/260331.zip::5_美容所",
                                      "sendai/raw/260331.zip::6_クリーニング所"], "sendai/raw/isj"),
    # Fukuoka's and Hiroshima's own lists stop where online filing starts (2021-06 /
    # 2023-08); MHLW's 食品衛生申請等システム open data carries the online filings
    # (opt-in, per-field disclosure, publisher's lat/lon).
    "fukuoka": ("福岡県", "福岡市", ["fukuoka/raw/r8.7.csv"], "fukuoka/raw/isj"),
    "fukuoka-mhlw": ("福岡県", "福岡市", ["mhlw/raw/40130_food_business_all.csv"], "fukuoka/raw/isj"),
    "fukuoka-life": ("福岡県", "福岡市", ["fukuoka/raw/202609011129.csv", "fukuoka/raw/202609011112.csv",
                                       "fukuoka/raw/202604011019.csv"], "fukuoka/raw/isj"),
    "hiroshima": ("広島県", "広島市", ["hiroshima/raw/5080331-2.xlsx"], "hiroshima/raw/isj"),
    "hiroshima-mhlw": ("広島県", "広島市", ["mhlw/raw/34100_food_business_all.csv"], "hiroshima/raw/isj"),
    # Tokyo wards whose own lists are their own format - one address string; the
    # "city" is the ward (Meguro's host is BODIK - owner accepted)
    "taito": ("東京都", "台東区", ["tokyo/raw/13106/2026ALL-IND-CSV.csv"], "tokyo/raw/13106"),
    "setagaya": ("東京都", "世田谷区", ["tokyo/raw/13112/zenkenr080331.csv"], "tokyo/raw/13112"),
    "meguro": ("東京都", "目黒区", ["tokyo/raw/13110/all_new_8.csv", "tokyo/raw/13110/all_old_8.csv"], "tokyo/raw/13110"),
    # Kyoto publishes no current full list: the register is REBUILT from the 2021
    # list and every monthly list, as of the day they were downloaded. Personal
    # services are the city's own complete lists (2026-03-31) plus each month's new.
    "kyoto": ("京都府", "京都市", [lambda: kyoto_permit_stream(DATA / "kyoto/raw", datetime.date(2026, 9, 24))],
              "kyoto/raw/isj"),
    "kyoto-life": ("京都府", "京都市", ["kyoto/raw/00530/*令和8年3月末*", "kyoto/raw/00530/*新規*"], "kyoto/raw/isj"),
}


def run_city(key, show_misses=False):
    pref, city, files, isj = CITIES[key]
    blocks, chome = load_city_isj(DATA / isj)
    ps = []
    for f in files:
        if callable(f):  # a rebuilt register (Kyoto)
            ps += permits_from_rows(f(), pref, city)
        elif "*" in f:
            for path in sorted(DATA.glob(f)):
                ps += load_city_permits(path, pref, city)
        else:
            ps += load_city_permits(DATA / f, pref, city)
    join_city(ps, blocks, chome)
    fixed = [p for p in ps if not p["mobile"]]
    t = collections.Counter(p["tier"] for p in fixed)
    n = max(1, len(fixed))
    print(f"{key} ({city}): {len(ps):,} rows, {len(fixed):,} fixed; ISJ {len(blocks):,} blocks / {len(chome):,} town-chōme; "
          + ", ".join(f"{k} {100 * t[k] / n:.1f}%" for k in ("block", "chome", "none"))
          + f"; hyphen shifts {sum(1 for p in fixed if p.get('shifted'))}")
    d = sorted(haversine_m(p["pt"], p["pub"]) for p in fixed if p["tier"] == "block" and p.get("pub"))
    if d:
        print(f"  vs the publisher's own coordinates ({len(d):,}): median {d[len(d) // 2]:.0f} m, "
              f"<=250 m {100 * sum(x <= 250 for x in d) / len(d):.1f}%, >1 km {sum(x > 1000 for x in d)}")
    if show_misses:
        rnd = random.Random(1)
        print("  unplaced (ward, town) top 12:",
              collections.Counter((p["ward"], p["town"]) for p in fixed if p["tier"] == "none").most_common(12))
        for tier in ("chome", "none"):
            s = [p for p in fixed if p["tier"] == tier]
            for p in rnd.sample(s, min(8, len(s))):
                print(f"   [{tier}] ward={p['ward']!r} town={p['town']!r} block={p['block']!r} | {p['addr'][:50]}")
    return ps


def gsi_check(permits, n, prefix=""):
    """Second method: GSI's keyless AddressSearch on a random sample of block
    hits, at 1 request per second. Distance from ISJ's block point. prefix
    restores the prefecture and city where a list's addresses start at the ward."""
    import truststore
    truststore.inject_into_ssl()
    sample = random.Random(20260924).sample([p for p in permits if p["tier"] == "block"], n)
    dists, fails = [], 0
    for p in sample:
        q = unicodedata.normalize("NFKC", p["addr"]).split(" ")[0]
        if prefix and not q.startswith(prefix):
            q = prefix + q
        url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q=" + urllib.parse.quote(q)
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    url, headers={"User-Agent": "expanded-heatmap-probe/1.0"}), timeout=30) as r:
                res = json.load(r)
            lon, lat = res[0]["geometry"]["coordinates"]
            dists.append(haversine_m(p["pt"], (lat, lon)))
        except Exception:  # noqa: BLE001
            fails += 1
        time.sleep(1.0)
    dists.sort()
    if dists:
        med = dists[len(dists) // 2]
        within = lambda m: sum(1 for d in dists if d <= m)  # noqa: E731
        print(f"GSI cross-check: {len(dists)} answered, {fails} failed; median {med:.0f} m; "
              f"<=100 m {within(100)}, <=250 m {within(250)}, <=500 m {within(500)}, max {dists[-1]:.0f} m")
    else:
        print(f"GSI cross-check: no answers ({fails} failed)")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    key = sys.argv[1] if len(sys.argv) > 1 else "minato"
    if key in CITIES:
        ps = run_city(key, "--misses" in sys.argv)
        if "--gsi" in sys.argv:
            pref, city = CITIES[key][:2]
            gsi_check([p for p in ps if not p["mobile"]], int(sys.argv[sys.argv.index("--gsi") + 1]),
                      prefix=pref + city)
        return
    code, muni, permit_csv, bz, cz = MUNICIPALITIES[key]
    blocks, chome = load_isj(DATA / bz, DATA / cz)
    permits = join(load_permits(DATA / permit_csv, muni), blocks, chome)
    n = len(permits)
    tiers = collections.Counter(p["tier"] for p in permits)
    print(f"{key} ({code} {muni}): {n:,} permits; ISJ {len(blocks):,} blocks, {len(chome):,} town-chōme")
    for t in ("block", "chome", "none"):
        print(f"  {t:<6} {tiers[t]:>6,}  {100 * tiers[t] / n:5.1f}%")
    print(f"  placed (block + chome): {100 * (tiers['block'] + tiers['chome']) / n:.1f}%")
    fixed = [p for p in permits if not p["mobile"]]
    ft = collections.Counter(p["tier"] for p in fixed)
    print(f"  FIXED PREMISES ({len(fixed):,}; {n - len(fixed)} mobile vendors set aside): "
          + ", ".join(f"{t} {100 * ft[t] / max(1, len(fixed)):.1f}%" for t in ("block", "chome", "none")))
    print(f"  hyphen-form shifts (5-2-1 read as 五丁目 2番): {sum(1 for p in permits if p.get('shifted'))}")
    # an INDEPENDENT position check where the publisher geocoded its own rows
    d = sorted(haversine_m(p["pt"], p["pub"]) for p in permits if p["tier"] == "block" and p.get("pub"))
    if d:
        print(f"  vs the publisher's own coordinates ({len(d):,} block hits): median {d[len(d) // 2]:.0f} m, "
              f"<=100 m {100 * sum(x <= 100 for x in d) / len(d):.1f}%, <=250 m {100 * sum(x <= 250 for x in d) / len(d):.1f}%, "
              f">1 km {sum(x > 1000 for x in d)}")
    print("  address source:", dict(collections.Counter(p["src"] for p in permits)))
    print("  block hits in 住居表示 areas:",
          sum(1 for p in permits if p["tier"] == "block" and p.get("jukyo") == "1"))
    if "--misses" in sys.argv:
        print("\nmiss classes:", collections.Counter(p.get("why") for p in permits if p["tier"] != "block"))
        towns = collections.Counter(p["town"] for p in permits if p["tier"] == "none")
        print("unplaced towns (top 15):", towns.most_common(15))
        chome_only = collections.Counter(p["town"] for p in permits if p["tier"] == "chome")
        print("chōme-only towns (top 15):", chome_only.most_common(15))
        rnd = random.Random(1)
        for tier in ("chome", "none"):
            s = [p for p in permits if p["tier"] == tier]
            for p in rnd.sample(s, min(12, len(s))):
                print(f"  [{tier}] town={p['town']!r} block={p['block']!r} src={p['src']} | {p['addr'][:60]}")
    if "--gsi" in sys.argv:
        gsi_check(permits, int(sys.argv[sys.argv.index("--gsi") + 1]))


if __name__ == "__main__":
    main()
