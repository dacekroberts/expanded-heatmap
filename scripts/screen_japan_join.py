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
import csv
import io
import json
import math
import random
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# municipality -> (municipality code, name, permit CSV, ISJ block zip, ISJ chōme zip)
MUNICIPALITIES = {
    "minato": ("13103", "港区", "tokyo/raw/food_business_all.csv",
               "tokyo/raw/13103-24.0a.zip", "tokyo/raw/13103-19.0b.zip"),
}

KANJI_DIGITS = {"〇": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def kanji_number(s):
    """一 .. 九十九 -> int; None if s is not a kanji number."""
    if not s or any(c not in KANJI_DIGITS and c != "十" for c in s):
        return None
    if "十" in s:
        a, _, b = s.partition("十")
        return (KANJI_DIGITS[a] if a else 1) * 10 + (KANJI_DIGITS[b] if b else 0)
    n = 0
    for c in s:
        n = n * 10 + KANJI_DIGITS[c]
    return n


def norm_town(s):
    """町字 as a comparable key: NFKC, no spaces."""
    s = unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", "")
    return s


def first_number(s):
    """街区符号 from 番地以下: the first number, full-width or kanji."""
    s = unicodedata.normalize("NFKC", s or "")
    m = re.search(r"\d+", s)
    if m:
        return str(int(m.group()))
    m = re.search(r"[〇一二三四五六七八九十]+", s)
    if m:
        n = kanji_number(m.group())
        return str(n) if n is not None else None
    return None


def read_zip_csv(path):
    with zipfile.ZipFile(path) as zf:
        name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        return list(csv.DictReader(io.StringIO(zf.read(name).decode("cp932"))))


def load_isj(block_zip, chome_zip):
    blocks, rep = {}, {}
    for r in read_zip_csv(block_zip):
        key = (norm_town(r["大字・丁目名"]), first_number(r["街区符号・地番"]))
        pt = (float(r["緯度"]), float(r["経度"]), r["住居表示フラグ"])
        if r.get("代表フラグ") == "1":
            rep[key] = pt
        blocks.setdefault(key, pt)
    blocks.update(rep)  # the representative point wins where one is flagged
    chome = {norm_town(r["大字町丁目名"]): (float(r["緯度"]), float(r["経度"]))
             for r in read_zip_csv(chome_zip)}
    return blocks, chome


def load_permits(path, muni_name):
    text = Path(path).read_bytes().decode("utf-8-sig")
    rows = [r for r in csv.DictReader(io.StringIO(text)) if r.get("許可番号")]
    out = []
    for r in rows:
        town, rest = r.get("施設所在地_町字", ""), r.get("施設所在地_番地以下", "")
        src = "split"
        if not town:
            # fall back to the joined string: strip prefecture and municipality,
            # take the town up to its first digit
            full = unicodedata.normalize("NFKC", r.get("所在地_連結表記", ""))
            full = full.split(" ")[0]
            full = re.sub(r"^東京都", "", full)
            full = full.split(muni_name, 1)[-1]
            m = re.match(r"(.+?丁目|[^0-9]+?)([0-9].*)$", full)
            town, rest, src = (m.group(1), m.group(2), "joined") if m else (full, "", "joined")
        out.append({"town": norm_town(town), "block": first_number(rest), "src": src,
                    "addr": r.get("所在地_連結表記", ""), "type": r.get("営業の種類", ""),
                    "name": r.get("施設名称", ""), "corp": r.get("法人名", "")})
    return out


def join(permits, blocks, chome):
    for p in permits:
        hit = blocks.get((p["town"], p["block"]))
        if hit:
            p["tier"], p["pt"], p["jukyo"] = "block", hit[:2], hit[2]
        elif p["town"] in chome:
            p["tier"], p["pt"] = "chome", chome[p["town"]]
            p["why"] = "no block number" if not p["block"] else "block not in file"
        else:
            p["tier"], p["pt"] = "none", None
            p["why"] = "no town" if not p["town"] else "town not in file"
    return permits


def haversine_m(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def gsi_check(permits, n):
    """Second method: GSI's keyless AddressSearch on a random sample of block
    hits, at 1 request per second. Distance from ISJ's block point."""
    import truststore
    truststore.inject_into_ssl()
    sample = random.Random(20260924).sample([p for p in permits if p["tier"] == "block"], n)
    dists, fails = [], 0
    for p in sample:
        q = unicodedata.normalize("NFKC", p["addr"]).split(" ")[0]
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
    code, muni, permit_csv, bz, cz = MUNICIPALITIES[key]
    blocks, chome = load_isj(DATA / bz, DATA / cz)
    permits = join(load_permits(DATA / permit_csv, muni), blocks, chome)
    n = len(permits)
    tiers = collections.Counter(p["tier"] for p in permits)
    print(f"{key} ({code} {muni}): {n:,} permits; ISJ {len(blocks):,} blocks, {len(chome):,} town-chōme")
    for t in ("block", "chome", "none"):
        print(f"  {t:<6} {tiers[t]:>6,}  {100 * tiers[t] / n:5.1f}%")
    print(f"  placed (block + chome): {100 * (tiers['block'] + tiers['chome']) / n:.1f}%")
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
