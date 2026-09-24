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
    "chuo": ("13102", "中央区", "tokyo/raw/13102/syokuhineigyoukyoka.csv",
             "tokyo/raw/13102/13102-24.0a.zip", "tokyo/raw/13102/13102-19.0b.zip"),
    "shinjuku": ("13104", "新宿区", "tokyo/raw/13104/000399975.csv",
                 "tokyo/raw/13104/13104-24.0a.zip", "tokyo/raw/13104/13104-19.0b.zip"),
    "koto": ("13108", "江東区", "tokyo/raw/13108/131083_015_food_business_all.csv",
             "tokyo/raw/13108/13108-24.0a.zip", "tokyo/raw/13108/13108-19.0b.zip"),
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
    """町字 as a comparable key: NFKC, no spaces, and the 丁目 number in digits.

    The digits rule came from Chūō's and Kōtō's misses: their permits write
    八重洲2丁目 where MLIT writes 八重洲二丁目. Applied to BOTH sides."""
    s = unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", "")
    return re.sub(r"([〇一二三四五六七八九十]+)丁目",
                  lambda m: f"{kanji_number(m.group(1))}丁目" if kanji_number(m.group(1)) else m.group(0), s)


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


def decode(b):
    """Permit files arrive as UTF-8 (Minato, Kōtō), cp932 (Chūō) or UTF-16 LE
    with a BOM (Shinjuku) - the same national schema, three encodings."""
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16")
    for enc in ("utf-8-sig", "cp932"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("undecodable permit file")


def load_permits(path, muni_name):
    """Food permits AND the 生活衛生 registers (理容所 / 美容所 / クリーニング所):
    the same national address columns, prefixed 施設所在地_ in the food schema
    and 所在地_ in the registers; Minato's own registers carry one 施設所在地."""
    def col(r, *names):
        return next((r[n] for n in names if (r.get(n) or "").strip()), "")

    text = decode(Path(path).read_bytes())
    rows = list(csv.DictReader(io.StringIO(text)))
    if rows and "許可番号" in rows[0]:
        rows = [r for r in rows if r.get("許可番号")]
    out = []
    for r in rows:
        town = col(r, "施設所在地_町字", "所在地_町字")
        rest = col(r, "施設所在地_番地以下", "所在地_番地以下")
        src = "split"
        if not town:
            # fall back to the joined string: strip prefecture and municipality,
            # take the town up to its first digit
            full = unicodedata.normalize("NFKC", col(r, "所在地_連結表記", "施設所在地"))
            full = full.split(" ")[0]
            full = re.sub(r"^東京都", "", full)
            full = full.split(muni_name, 1)[-1]
            m = re.match(r"(.+?丁目|[^0-9]+?)([0-9].*)$", full)
            town, rest, src = (m.group(1), m.group(2), "joined") if m else (full, "", "joined")
        # Shinjuku's misses: the WHOLE address sits in 町字 (新宿3-14-1, 歌舞伎町1-2-7)
        # with 番地以下 empty. Split at the first digit; the hyphen-form shift in
        # join() then reads 新宿3-14-1 as 新宿三丁目 14番.
        t = unicodedata.normalize("NFKC", town)
        m = re.match(r"^(\D+?)(\d.*)$", t)
        if m and "丁目" not in t:
            town, rest, src = m.group(1), m.group(2) + " " + rest, "split-embedded"
        pub = None
        try:
            pub = (float(r["緯度"]), float(r["経度"])) if (r.get("緯度") or "").strip() else None
        except ValueError:
            pass
        out.append({"town": norm_town(town), "block": first_number(rest), "rest": rest, "src": src,
                    "addr": col(r, "所在地_連結表記", "施設所在地"), "type": r.get("営業の種類", ""),
                    "name": r.get("施設名称", ""), "corp": r.get("法人名", ""), "pub": pub})
    return out


def join(permits, blocks, chome):
    for p in permits:
        p["mobile"] = p["town"] == "都内一円" or "自動車" in p["type"]
        hit = blocks.get((p["town"], p["block"]))
        if not hit and "丁目" not in p["town"] and p["block"]:
            # hyphen form: 築地5-2-1 is 築地五丁目 2番 1号 - the first number is the
            # 丁目. Shift only when that town-chōme exists in the file.
            nums = re.findall(r"\d+", unicodedata.normalize("NFKC", p["rest"]))
            shifted = f"{p['town']}{nums[0]}丁目" if nums else None
            if shifted in chome:
                p["town"], p["block"], p["shifted"] = shifted, (str(int(nums[1])) if len(nums) > 1 else None), True
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
