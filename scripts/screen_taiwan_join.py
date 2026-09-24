"""Join Taiwan's business tax register to a city's door-plate coordinate file,
and report the rate by bucket. The method that took Taiwan out of the
"geocoding at national scale" band on 2026-09-23.

WHY A JOIN, NOT A GEOCODER
--------------------------
Every Taiwanese city publishes a keyless door-plate file (門牌位置數值資料):
one row per door plate - street / lane / alley / number - with a TWD97
coordinate. The national business tax register (全國營業(稅籍)登記資料集,
Fiscal Information Agency, daily) gives each trading location's address as one
string. Parse the string into the same components and the coordinate is a
dict lookup. Measured: Taipei 92.4%, New Taipei 95.5%, Taoyuan 94.0%,
Taichung 92.7%.

RUN TAIPEI FIRST - IT IS THE CONTROL
------------------------------------
A generalised parser once read Taipei at 91.7% against a measured 92.5%,
because its street pattern forbade the characters stripped as district and
village (市, 鎮, 里) and so failed every street CONTAINING one - 市民大道,
鎮三街. A control that must reproduce before any other city counts is what
caught it. Any change to `parse()` re-runs Taipei first.

THE NORMALISATION THAT MATTERED
-------------------------------
- NFKC: full-width digits (９１號) to ASCII.
- Chinese section numerals to digits: 四段 -> 4段.
- ONE sub-number separator from 之, －, -, ― (U+2015), —, –. The first pass
  missed ― and read 89.1% instead of 92.5%: one character, 3.4 points.
- Chained sub-numbers (Taichung): ２之３之２號 -> 2-3-2.
- Floors dropped (a door plate is the building); "39、41號" takes the first.
- Pre-upgrade county prefixes (桃園縣, 臺中縣, 臺北縣) accepted - checked
  2026-09-23 and absent from the register, but cheap to keep.

WHAT THE MISSES ARE
-------------------
Mostly market stalls (環南市場…攤位) and stalls under viaducts (高架橋下) - real
premises with no door plate - and rural addresses with no street name. Read
the printed samples; the misses are not random.

Needs (gitignored, never committed): the register zip and the city's
door-plate CSV under data/<city>/raw/. Downloading is fetch work, not this
script's.

Usage:
    python scripts/screen_taiwan_join.py taipei       # the control, first
    python scripts/screen_taiwan_join.py new_taipei
"""
import collections
import csv
import io
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
REGISTER = DATA / "taipei" / "raw" / "BGMOPEN1.zip"

# city -> (address prefixes, door-plate CSV, column names)
CITIES = {
    "taipei": (("臺北市", "台北市"), "taipei/raw/taipei_doorplate_20260902.csv",
               {"street": "街路段", "lane": "巷", "alley": "弄", "num": "號"}),
    "new_taipei": (("新北市", "臺北縣", "台北縣"), "new_taipei/raw/new_taipei_doorplate.csv",
                   {"street": "street、road、section", "lane": "lane", "alley": "alley",
                    "num": "number"}),
    "taoyuan": (("桃園市", "桃園縣"), "taoyuan/raw/TGOS_A68000_11508.csv",
                {"street": "街路段", "lane": "巷", "alley": "弄", "num": "號"}),
    "taichung": (("臺中市", "台中市", "臺中縣", "台中縣"),
                 "taichung/raw/taichung_doorplate_11508.csv",
                 {"street": "街、路段", "lane": "巷", "alley": "弄", "num": "號"}),
}
# ISIC-aligned divisions, read from the register's own code names. 487 is
# online shopping - non-store retail, excluded as NAICS 454 is everywhere.
BUCKET = {"47": "Retail", "48": "Retail", "56": "Food service", "96": "Personal services"}
EXCLUDE_PREFIXES = ("487",)

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
SEP = r"[之\-－~―—–]+"


def cn_num(s):
    if s.isdigit():
        return str(int(s))
    if s == "十":
        return "10"
    if "十" in s:
        a, b = s.split("十", 1)
        return str(CN.get(a, 1) * 10 + (CN.get(b, 0) if b else 0))
    return str(CN.get(s, s))


def nfkc(s):
    return unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", "")


def canon_street(s):
    s = re.sub(r"([一二三四五六七八九十]+|\d+)段", lambda m: cn_num(m.group(1)) + "段", nfkc(s))
    return s.replace("台", "臺")


def canon_number(num):
    num = re.sub(r"(\d+)" + SEP + r"(?=\d)", r"\1-", nfkc(num))
    m = re.match(r"(\d+(?:-\d+)*)", num)
    return m.group(1) if m else None


# The street may CONTAIN 市, 鎮 or 里; district and village are stripped first.
ADDR = re.compile(
    r"^(?P<street>.+?(?:路|街|大道|道)(?:\d+段)?|.+?段)"
    r"(?:(?P<lane>\d+)巷)?(?:(?P<alley>\d+)弄)?(?P<num>\d+(?:-\d+)*)號")


def parse(addr, prefixes):
    a = nfkc(addr).replace("台", "臺")
    for p in prefixes:
        a = a.replace(nfkc(p).replace("台", "臺"), "", 1)
    a = re.sub(r"^.{1,3}?(區|鄉|鎮|市)", "", a)          # district / old township
    a = re.sub(r"^[^路街道段]{1,4}?里", "", a)            # village
    a = re.sub(r"^\d+鄰", "", a)                           # neighbourhood
    a = re.sub(r"([一二三四五六七八九十]+)段", lambda m: cn_num(m.group(1)) + "段", a)
    a = re.sub(r"(\d+)" + SEP + r"(?=\d)", r"\1-", a)
    a = re.sub(r"(\d+)[、,]\d+號", r"\1號", a)
    m = ADDR.search(a)
    if not m:
        return None
    return (canon_street(m.group("street")), m.group("lane") or "",
            m.group("alley") or "", m.group("num"))


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "taipei"
    prefixes, plates_rel, cols = CITIES[city]
    plates = set()
    with io.open(DATA / plates_rel, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            num = canon_number(r[cols["num"]])
            if num:
                plates.add((canon_street(r[cols["street"]]),
                            re.sub(r"\D", "", nfkc(r[cols["lane"]])),
                            re.sub(r"\D", "", nfkc(r[cols["alley"]])), num))
    print(f"{city}: {len(plates):,} distinct door-plate keys")

    z = zipfile.ZipFile(REGISTER)
    member = max(z.infolist(), key=lambda i: i.file_size)
    rd = csv.DictReader(io.TextIOWrapper(z.open(member), encoding="utf-8-sig",
                                         errors="replace", newline=""))
    res = collections.defaultdict(collections.Counter)
    miss = collections.defaultdict(list)
    for r in rd:
        a = r.get("營業地址") or ""
        code = (r.get("行業代號") or "").strip()
        if (not r.get("統一編號") or not a.startswith(prefixes)
                or code[:2] not in BUCKET or code.startswith(EXCLUDE_PREFIXES)):
            continue
        b = BUCKET[code[:2]]
        res[b]["n"] += 1
        p = parse(a, prefixes)
        if not p:
            res[b]["unparsed"] += 1
            miss["unparsed"].append(a)
        elif p in plates:
            res[b]["exact"] += 1
        elif (p[0], p[1], p[2], p[3].split("-")[0]) in plates:
            res[b]["base number"] += 1     # tier 2: the parent number's plate
        else:
            res[b]["no plate"] += 1
            miss["no plate"].append(a)

    tot = sum(c["n"] for c in res.values())
    got = sum(c["exact"] + c["base number"] for c in res.values())
    for b, c in res.items():
        n = c["n"]
        print(f"   {b:<18} {n:>7,}  exact {c['exact'] / n * 100:5.1f}%  "
              f"base-number {c['base number'] / n * 100:4.1f}%  "
              f"unparsed {c['unparsed'] / n * 100:4.1f}%  no plate {c['no plate'] / n * 100:4.1f}%")
    print(f"   {'ALL':<18} {tot:>7,}  matched {got / tot * 100:.1f}%")
    for k, v in miss.items():
        step = max(1, len(v) // 10)
        print(f"   {k} ({len(v):,}) - read these:")
        for x in v[::step][:10]:
            print("      ", x[:60])


if __name__ == "__main__":
    sys.exit(main())
