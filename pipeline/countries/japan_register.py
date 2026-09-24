"""Japan's coordinate step: a JOIN of permit lists to MLIT's 位置参照情報.

Shared by every Japanese city. **Moved here unchanged from
`scripts/screen_japan_join.py` on 2026-09-24**, so the screen that measured
the join and the builds that use it run one set of rules, not two copies.
Brazil's CNEFE taxonomy made the same move before its second build. The
script still owns the measurement: tiers, misses, the GSI cross-check, and
Minato as the control.

**How it works.** The permit lists spell each premises' address, either split
(the national 推奨データセット: 町字 / 番地以下) or as one string naming the ward
(Osaka, Kobe, Sapporo, Sendai, Fukuoka, Hiroshima, and Tokyo wards' own
formats). MLIT publishes, per municipality, a table of those components with a
coordinate: block level (街区, edition 24.0a) and town-chōme level (19.0b). So
a coordinate is a dictionary lookup, with tiers (block, chōme, none) and never
one rate.

**Every normalisation rule came from reading a city's misses**, and each names
the city that taught it: kanji chōme numbers (Chūō), the whole address in
町字 (Shinjuku), UTF-16 files (Shinjuku), kanji variants (Osaka's 曽根崎新地),
mislabelled lat/lon (Osaka), the 条 grid and direction suffixes (Sapporo),
字 addresses keyed through 小字・通称名 (Sendai; it lifted Kobe too), and
`一円` not-a-premises rows (Sendai's festival stalls, Kobe's storeless laundry
pick-ups). **Re-run the Minato control after any change to this file.**

**Privacy by construction.** The loaders read the premises columns BY NAME
(address, trade name, type, the publisher's lat/lon). The operator columns
these files carry (営業者名, 申請者名, 開設者名 and 開設者住所, 代表者名, phones)
are never selected.
"""
import csv
import io
import math
import re
import unicodedata
import zipfile
from pathlib import Path


VARIANTS = str.maketrans({"曾": "曽", "靱": "靭", "﨑": "崎", "ヶ": "ケ", "ヵ": "カ", "邊": "辺", "邉": "辺", "齋": "斉",
                          "齊": "斉", "濵": "浜", "髙": "高", "德": "徳", "槇": "槙"})


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
    # Osaka's misses: 曽根崎新地 (1,807 permits) vs MLIT's 曾根崎新地, 靭本町 vs
    # 靱本町, 松ヶ枝町 vs 松ケ枝町 - one spelling for each variant, both sides.
    s = s.translate(VARIANTS)
    # Sapporo's grid (南16条西10丁目) takes the same rule before 条 as before 丁目.
    return re.sub(r"([〇一二三四五六七八九十]+)(丁目|条)",
                  lambda m: f"{kanji_number(m.group(1))}{m.group(2)}" if kanji_number(m.group(1)) else m.group(0), s)


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
    # Shibuya keeps closed premises in the file (39,304 rows, 16,993 open)
    if rows and "廃業日" in rows[0]:
        rows = [r for r in rows if not (r.get("廃業日") or "").strip()]
    out = []
    for r in rows:
        town = col(r, "施設所在地_町字", "所在地_町字")
        rest = col(r, "施設所在地_番地以下", "所在地_番地以下", "施設所在地_番地")
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
                    "addr": col(r, "所在地_連結表記", "施設所在地", "施設所在地_連結表記"),
                    "type": col(r, "営業の種類", "営業の種類もしくは営業の形態"),
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


ADDR_COLS = ("施設所在地", "営業所所在地", "所在地_連結表記", "営業所住所", "営業施設所在地",
             "営業所所在地（所在地_連結標記", "施設所在地（所在地_連結標記）")


TYPE_COLS = ("業種名", "業種分類", "業種情報公開名称", "営業の種類", "業種区分", "営業種類", "施設（種別）", "種別", "業種", "業務種別")


NAME_COLS = ("屋号", "施設名称", "営業施設名称、屋号又は商号", "施設の名称", "施設屋号")


def xlsx_rows(data):
    """Every sheet that has an address column, header found by that column (a
    sheet may open with title rows). Summary sheets without one are skipped."""
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    for ws in wb.worksheets:
        head = None
        for r in ws.iter_rows(values_only=True):
            cells = ["" if c is None else str(c).replace("\n", "").strip() for c in r]
            if head is None:
                if any(c in ADDR_COLS for c in cells):
                    head = cells
                continue
            if any(cells):
                yield dict(zip(head, cells))


def zip_member_name(info):
    """Japanese member names without the UTF-8 flag are cp932 read as cp437."""
    if info.flag_bits & 0x800:
        return info.filename
    try:
        return info.filename.encode("cp437").decode("cp932")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return info.filename


def city_rows(path):
    """Rows as dicts from a CSV, an XLSX, or XLSX members of a ZIP
    ('file.zip::part' keeps only members whose name contains part)."""
    path, _, part = str(path).partition("::")
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                nm = zip_member_name(info)
                if nm.lower().endswith(".xlsx") and part in nm:
                    yield from xlsx_rows(zf.read(info))
        return
    if path.lower().endswith(".xlsx"):
        yield from xlsx_rows(Path(path).read_bytes())
        return
    text = decode(Path(path).read_bytes())
    delim = "\t" if text.split("\n", 1)[0].count("\t") > text.split("\n", 1)[0].count(",") else ","
    yield from csv.DictReader(io.StringIO(text), delimiter=delim)


def load_city_isj(isj_dir):
    """Every ward's block and town-chōme files, keyed by (ward, town[, block])."""
    blocks, chome = {}, {}
    for z in sorted(Path(isj_dir).glob("*-24.0a.zip")):
        for r in read_zip_csv(z):
            ward = r["市区町村名"].split("市")[-1]
            key = (ward, norm_town(r["大字・丁目名"]), first_number(r["街区符号・地番"]))
            pt = (float(r["緯度"]), float(r["経度"]), r["住居表示フラグ"])
            if r.get("代表フラグ") == "1" or key not in blocks:
                blocks[key] = pt
            # Sendai's 字 addresses (福室字境４番) - MLIT keeps the 字 in 小字・通称名,
            # so the same 地番 is also keyed under 大字 + 字 + 小字.
            if r.get("小字・通称名"):
                akey = (ward, norm_town(r["大字・丁目名"] + "字" + r["小字・通称名"]), key[2])
                if r.get("代表フラグ") == "1" or akey not in blocks:
                    blocks[akey] = pt
    for z in sorted(Path(isj_dir).glob("*-19.0b.zip")):
        for r in read_zip_csv(z):
            chome[(r["市区町村名"].split("市")[-1], norm_town(r["大字町丁目名"]))] = (float(r["緯度"]), float(r["経度"]))
    return blocks, chome


def load_city_permits(path, pref, city):
    """Own-format city lists: one address string naming the ward. Reads only the
    premises columns - never 営業者名 / 申請者名 / 開設者 (people)."""
    out = []
    for r in city_rows(path):
        addr = next((r[c] for c in ADDR_COLS if (r.get(c) or "").strip()), "")
        a = unicodedata.normalize("NFKC", addr).replace(" ", "").replace("　", "")
        a = re.sub("^" + pref, "", a)
        a = a.split(city, 1)[-1]
        if city.endswith("区"):
            # a Tokyo special ward's own list: the ward IS the municipality, and
            # Taitō's addresses start at the town (浅草一丁目…)
            ward, rest = city, a
        else:
            m = re.match(r"^(\D+?区)(.*)$", a)
            ward, rest = (m.group(1), m.group(2)) if m else ("", a)
        # Sapporo's misses: an address that ENDS at 丁目 (南5条西6丁目, no block
        # number) was cut to 南 - the number after the town is optional.
        # ...and a building name may follow 丁目 directly (南5条西6丁目ニュー桂和ビル).
        m = re.match(r"^(.+?丁目)(.*)$", rest) or re.match(r"^([^0-9]+?)([0-9].*)?$", rest)
        town, tail = (m.group(1), m.group(2) or "") if m else (rest, "")
        # Sapporo's Shiroishi misses: the town ends in a direction after 丁目
        # (本郷通8丁目南 3-1) - keep it in the town when a number follows.
        d = re.match(r"^([南北東西])(\d.*)$", tail) if town.endswith("丁目") else None
        pub = None
        try:
            pub = (float(r["緯度"]), float(r["経度"])) if (r.get("緯度") or "").strip() else None
            # Osaka's columns are MISLABELLED: 経度 holds 34.7, 緯度 135.5.
            if pub and pub[0] > 90:
                pub = (pub[1], pub[0])
        except (ValueError, KeyError):
            pass
        out.append({"ward": ward, "town": norm_town(town), "block": first_number(tail), "rest": tail,
                    "dir": (d.group(1), d.group(2)) if d else None,
                    "addr": addr, "type": next((r[c] for c in TYPE_COLS if r.get(c)), ""),
                    "name": next((r[c] for c in NAME_COLS if r.get(c)), ""), "pub": pub,
                    # not a premises: vehicles, and 市内一円 / 仙台市内一円 ("anywhere in
                    # the city") - Sendai's festival stalls (仮設, 臨時) are written so
                    "mobile": not addr.strip() or "一円" in addr or "自動車" in next((r[c] for c in TYPE_COLS if r.get(c)), "")})
    return out


def join_city(permits, blocks, chome):
    for p in permits:
        w = p["ward"]
        # the direction suffix (Sapporo) only where that town exists in MLIT's file
        if p.get("dir") and (w, p["town"] + p["dir"][0]) in chome:
            p["town"], p["rest"] = p["town"] + p["dir"][0], p["dir"][1]
            p["block"] = first_number(p["rest"])
        hit = blocks.get((w, p["town"], p["block"]))
        if not hit and "丁目" not in p["town"] and p["block"]:
            nums = re.findall(r"\d+", p["rest"])
            shifted = f"{p['town']}{nums[0]}丁目" if nums else None
            if (w, shifted) in chome:
                p["town"], p["block"], p["shifted"] = shifted, (str(int(nums[1])) if len(nums) > 1 else None), True
                hit = blocks.get((w, p["town"], p["block"]))
        # Kobe's misses: hill addresses name a 字 inside the 大字 (山田町上谷上字古々山);
        # MLIT's town-chōme file knows the 大字, so it takes the 大字's centroid.
        oaza = re.split(r"字", p["town"], maxsplit=1)[0] if "字" in p["town"][1:] else None
        if hit:
            p["tier"], p["pt"] = "block", hit[:2]
        elif (w, p["town"]) in chome:
            p["tier"], p["pt"] = "chome", chome[(w, p["town"])]
        elif oaza and (w, oaza) in chome:
            p["tier"], p["pt"], p["oaza"] = "chome", chome[(w, oaza)], True
        else:
            p["tier"], p["pt"] = "none", None
    return permits


def haversine_m(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
