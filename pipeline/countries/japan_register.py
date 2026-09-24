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
字 addresses keyed through 小字・通称名 (Sendai; it lifted Kobe too),
`一円` not-a-premises rows (Sendai's festival stalls, Kobe's storeless laundry
pick-ups), and Kyoto's four (2026-09-24): A the street-intersection prefix
(河原町通三条上る, Kyoto only), B character variants (祇/祗, 藪/薮, ゝ), C a
known-town fallback, and D twin town names left unplaced. C runs in every city
and is checked against publisher coordinates and GSI: see join_city.
**Re-run the Minato control and every screen after any change to this file.**

**Privacy by construction.** The loaders read the premises columns BY NAME
(address, trade name, type, the publisher's lat/lon). The operator columns
these files carry (営業者名, 申請者名, 開設者名 and 開設者住所, 代表者名, phones)
are never selected.
"""
import collections
import csv
import datetime
import io
import math
import re
import unicodedata
import zipfile
from pathlib import Path


VARIANTS = str.maketrans({"曾": "曽", "靱": "靭", "﨑": "崎", "ヶ": "ケ", "ヵ": "カ", "邊": "辺", "邉": "辺", "齋": "斉",
                          "齊": "斉", "濵": "浜", "髙": "高", "德": "徳", "槇": "槙",
                          # Kyoto's misses (rule B): MLIT itself spells 藪/薮 both ways
                          "祗": "祇", "薮": "藪", "壺": "壷", "檜": "桧", "籠": "篭", "竈": "竃", "龍": "竜",
                          "淵": "渕", "秡": "祓"})
STRING_VARIANTS = (("鍛治", "鍛冶"), ("廻リ", "廻り"))


# Kyoto's own private-use code points for 祇 (祇園). Private-use characters are
# each publisher's own assignment, so these are read in Kyoto's files only.
KYOTO_GAIJI = str.maketrans({"": "祇", "": "祇", "": "祇"})


# Kyoto's misses (rule A): the central wards name the street intersection before
# the town - 河原町通三条上る下丸屋町123 is 下丸屋町 123, on Kawaramachi-dōri north
# of Sanjō. The town follows the LAST direction word, and a count of blocks may
# sit between them (大和大路通四条下る4丁目小松町): that 丁目 is a distance, not a town.
INTERSECTION = re.compile(r"^.*(?:上る|下る|上がる|下がる|[東西南北]入る|[東西南北]入|入る)(.*)$")
BLOCKS_AFTER = re.compile(r"^[0-9一二三四五六七八九十]+丁目(\D.*)$")


def strip_intersection(rest):
    """The address after the ward, without its street-intersection part."""
    for a, b in (("上ル", "上る"), ("下ル", "下る"), ("入ル", "入る"), ("上ガル", "上がる"), ("下ガル", "下がる")):
        rest = rest.replace(a, b)
    m = INTERSECTION.match(rest)
    if not m:
        return rest
    b = BLOCKS_AFTER.match(m.group(1))
    return b.group(1) if b else m.group(1)


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
    for a, b in STRING_VARIANTS:
        s = s.replace(a, b)
    # Kyoto's misses: MLIT writes 深草スゝハキ町 where permits repeat the kana
    s = re.sub(r"(.)[ゝヽ]", r"\1\1", s)
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


def _cell(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if hasattr(v, "strftime"):
        return v.strftime("%Y-%m-%d")
    return str(v).replace("\n", "").replace("\r", "").strip()


def workbook_tables(path):
    """Rows as dicts from every sheet of an .xls or .xlsx that has a 所在地 column
    in its first 30 rows (the header; title rows may sit above it). Kyoto's
    2021 list is the old .xls format, read with xlrd. Dates come back ISO."""
    data = Path(path).read_bytes()
    if data[:4] == b"\xd0\xcf\x11\xe0":
        import xlrd
        wb = xlrd.open_workbook(file_contents=data)

        def xls_cell(c):
            if c.ctype == xlrd.XL_CELL_DATE:
                try:
                    return _cell(xlrd.xldate_as_datetime(c.value, wb.datemode))
                except (ValueError, OverflowError, xlrd.xldate.XLDateError):
                    pass
            return _cell(c.value)
        sheets = [[[xls_cell(c) for c in sh.row(i)] for i in range(sh.nrows)] for sh in wb.sheets()]
    else:
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        sheets = [[[_cell(c) for c in r] for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets]
    for rows in sheets:
        hi = next((i for i, r in enumerate(rows[:30]) if any("所在地" in c for c in r)), None)
        if hi is None:
            continue
        head, seen = [], collections.Counter()
        for k, h in enumerate(c.replace(" ", "").replace("　", "") for c in rows[hi]):
            h = h or f"_col{k}"
            head.append(f"{h}#{seen[h]}" if seen[h] else h)  # a repeated header keeps its first column
            seen[h] += 1
        for r in rows[hi + 1:]:
            if any(r):
                yield dict(zip(head, r + [""] * (len(head) - len(r))))


# ---- Kyoto's register, rebuilt from its permit stream ------------------------
# Since the 2021 reform Kyoto publishes no full list, only the 2021-03-31 one and
# a list of each month's new permits. A permit runs 5-6 years and a renewal
# arrives as a new monthly row, so the register is rebuilt: every list,
# deduplicated, kept while its term runs. Closures are INVISIBLE, so this is an
# upper bound and must be disclosed as one (Rotterdam's method).
KYOTO_COLS = {"a1": "営業所＿所在地１", "a2": "営業所＿所在地２", "name": "営業所＿名称（屋号・商号）１",
              "type": "業種", "end": "許可終了日", "granted": "許可年月日"}  # premises columns only
KYOTO_CORP = re.compile(r"株式会社|有限会社|合同会社|合資会社|合名会社|一般社団法人|公益社団法人|一般財団法人|"
                        r"公益財団法人|社会福祉法人|医療法人|学校法人|宗教法人|特定非営利活動法人|[(]株[)]|[(]有[)]|㈱|㈲")


def wareki_date(s):
    """H31.4.30 / 令和3年4月1日 / 2026-03-31 / an Excel serial -> date, else None."""
    s = unicodedata.normalize("NFKC", (s or "").strip())
    if m := re.match(r"([HR])(\d+)[.](\d+)[.](\d+)", s):
        y, mo, d = int(m.group(2)) + (1988 if m.group(1) == "H" else 2018), int(m.group(3)), int(m.group(4))
    elif m := re.match(r"(平成|令和)(\d+|元)年(\d+)月(\d+)日", s):
        n = 1 if m.group(2) == "元" else int(m.group(2))
        y, mo, d = n + (1988 if m.group(1) == "平成" else 2018), int(m.group(3)), int(m.group(4))
    elif m := re.match(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s):
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    elif re.fullmatch(r"\d{5}", s):  # one row: 47177 = 2029-02-28
        return datetime.date(1899, 12, 30) + datetime.timedelta(days=int(s))
    else:
        return None
    try:
        return datetime.date(y, mo, d)
    except ValueError:  # an end date written as 29 February in a non-leap year
        return datetime.date(y, mo, 28) if mo == 2 else None


def _kyoto_key(rec):
    """(address, trade name, type), each normalised, so a renewal finds its permit."""
    a = unicodedata.normalize("NFKC", rec["a1"]).replace(" ", "").replace("　", "")
    a = re.sub(r"^京都府", "", a)
    a = re.sub(r"^京都市", "", a)
    a = a.replace("上ル", "上る").replace("下ル", "下る").replace("入ル", "入る")
    if re.search(r"[0-9][‐‑‒–—―−ｰー－][0-9]", a):
        a = re.sub(r"[‐‑‒–—―−ｰー－]", "-", a)
    a = re.sub(r"([0-9])番地?([0-9])", r"\1-\2", a)
    a = re.sub(r"([0-9])(番地|番|号)$", r"\1", a)
    n = KYOTO_CORP.sub("", unicodedata.normalize("NFKC", rec["name"]).replace(" ", "").replace("　", ""))
    t = unicodedata.normalize("NFKC", rec["type"]).replace(" ", "").replace("　", "")
    # the 2021 reform folded 喫茶店営業 into 飲食店営業, so a renewal changes type
    return a, n, "飲食店営業" if t.startswith("喫茶店営業") else t


def kyoto_permit_stream(raw_dir, as_of):
    """Kyoto's current food permits on `as_of`, rebuilt from the 2021-03-31 full
    list (resource 15447 of dataset 00414) and every monthly list (the rest of
    00414, and 00541), oldest first. Where (address, trade name, type) repeats,
    the permit ending latest wins. `as_of` is a parameter, never today: a build
    that filtered on today would drift every day.
    Measured 2026-09-24: 69,651 rows, 50,178 after deduplication, 30,351 in term."""
    raw = Path(raw_dir)
    rid = lambda p: int(p.name.split("_")[1])  # noqa: E731
    files = sorted([*raw.glob("00414/*"), *raw.glob("00541/*")], key=lambda p: (rid(p) != 15447, rid(p)))
    best = {}
    for f in files:
        for r in workbook_tables(f):
            rec = {k: r.get(v, "") for k, v in KYOTO_COLS.items()}
            rec["d_end"], rec["d_granted"] = wareki_date(rec["end"]), wareki_date(rec["granted"])
            rank = (rec["d_end"] or datetime.date(1900, 1, 1), rec["d_granted"] or datetime.date(1900, 1, 1))
            key = _kyoto_key(rec)
            if key not in best or rank > best[key][0]:
                best[key] = (rank, rec)
    return [{"営業所所在地": rec["a1"] + rec["a2"], "業種": rec["type"], "屋号": rec["name"],
             "許可終了日": rec["d_end"].isoformat()}
            for _, rec in best.values() if rec["d_end"] and rec["d_end"] >= as_of]


def load_city_isj(isj_dir):
    """Every ward's block and town-chōme files, keyed by (ward, town[, block]).

    Kyoto's misses (rule D): one town name can belong to two places in a ward -
    123 names in 上京, 中京 and 下京, the twins a median 1.27 km apart. Such a
    town's chōme entry is None, and so is a block whose 地番 occurs in more than
    one twin; join_city leaves those rows unplaced rather than guess a twin."""
    cents = collections.defaultdict(list)
    for z in sorted(Path(isj_dir).glob("*-19.0b.zip")):
        for r in read_zip_csv(z):
            cents[(r["市区町村名"].split("市")[-1], norm_town(r["大字町丁目名"]))].append((float(r["緯度"]), float(r["経度"])))
    chome = {k: pts[0] if len(pts) == 1 else None for k, pts in cents.items()}
    twin_of = collections.defaultdict(set)  # a twin town's (ward, town, block) -> which twins it occurs in
    blocks = {}
    for z in sorted(Path(isj_dir).glob("*-24.0a.zip")):
        for r in read_zip_csv(z):
            ward = r["市区町村名"].split("市")[-1]
            key = (ward, norm_town(r["大字・丁目名"]), first_number(r["街区符号・地番"]))
            pt = (float(r["緯度"]), float(r["経度"]), r["住居表示フラグ"])
            if chome.get(key[:2], ()) is None:
                twins = cents[key[:2]]
                twin_of[key].add(min(range(len(twins)), key=lambda i: haversine_m(pt[:2], twins[i])))
            if r.get("代表フラグ") == "1" or key not in blocks:
                blocks[key] = pt
            # Sendai's 字 addresses (福室字境４番) - MLIT keeps the 字 in 小字・通称名,
            # so the same 地番 is also keyed under 大字 + 字 + 小字.
            if r.get("小字・通称名"):
                akey = (ward, norm_town(r["大字・丁目名"] + "字" + r["小字・通称名"]), key[2])
                if r.get("代表フラグ") == "1" or akey not in blocks:
                    blocks[akey] = pt
    for key, which in twin_of.items():
        if len(which) > 1:
            blocks[key] = None
    return blocks, chome


def load_city_permits(path, pref, city):
    """Own-format city lists: one address string naming the ward. Reads only the
    premises columns - never 営業者名 / 申請者名 / 開設者 (people)."""
    return permits_from_rows(city_rows(path), pref, city)


def permits_from_rows(rows, pref, city):
    """load_city_permits for rows already read - Kyoto's rebuilt register."""
    out = []
    for r in rows:
        addr = next((r[c] for c in ADDR_COLS if (r.get(c) or "").strip()), "")
        a = unicodedata.normalize("NFKC", addr).replace(" ", "").replace("　", "")
        a = re.sub("^" + pref, "", a)
        a = a.split(city, 1)[-1]
        if city == "京都市":
            a = a.translate(KYOTO_GAIJI)
        if city.endswith("区"):
            # a Tokyo special ward's own list: the ward IS the municipality, and
            # Taitō's addresses start at the town (浅草一丁目…)
            ward, rest = city, a
        else:
            m = re.match(r"^(\D+?区)(.*)$", a)
            ward, rest = (m.group(1), m.group(2)) if m else ("", a)
        if city == "京都市":
            rest = strip_intersection(rest)
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


def known_town(town, known):
    """Kyoto's misses (rule C): a town with something attached, before
    (八坂新地清本町 -> 清本町, 高台寺桝屋町 -> 桝屋町) or after (嵯峨中ノ島町官有地 ->
    嵯峨中ノ島町). The longest known town of 3+ characters that ENDS the parsed
    town, else the longest that STARTS it."""
    for i in range(1, len(town) - 2):
        if town[i:] in known:
            return town[i:], "suffix"
    for j in range(len(town) - 1, 2, -1):
        if town[:j] in known:
            return town[:j], "prefix"
    return None, None


def join_city(permits, blocks, chome):
    towns = collections.defaultdict(set)
    for w, t in chome:
        towns[w].add(t)
    # 大字 whose blocks are also keyed by 小字 (the Sendai key above): their 地番
    # restart in each 小字 - 110 of 五日市町's 588 numbers occur in 2+ of them
    has_koaza = {(w, t.rsplit("字", 1)[0]) for w, t, _ in blocks if "字" in t[1:]}
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
        if not hit and (w, p["town"]) not in chome and not (oaza and (w, oaza) in chome):
            t, how = known_town(p["town"], towns[w])
            if t and how == "prefix" and (w, t) in has_koaza:
                # The dropped tail may be a 小字 (六甲山町北六甲, 五日市町上河内), whose
                # 地番 restart: look it up under that 小字 or not at all. Measured
                # against Hiroshima's MHLW coordinates, the 大字's own 地番 put rows
                # a median 2.1 km off and its centroid 5.2 km.
                hit = blocks.get((w, t + "字" + p["town"][len(t):].lstrip("字"), p["block"]))
                if hit:
                    p["town"], p["affix"] = t, how
            elif t:
                p["town"], p["affix"] = t, how
                hit = blocks.get((w, t, p["block"]))
        if hit:
            p["tier"], p["pt"] = "block", hit[:2]
        elif (w, p["town"]) in chome:
            p["tier"], p["pt"] = "chome", chome[(w, p["town"])]
        elif oaza and (w, oaza) in chome:
            p["tier"], p["pt"], p["oaza"] = "chome", chome[(w, oaza)], True
        else:
            p["tier"], p["pt"] = "none", None
        if p["tier"] == "chome" and p["pt"] is None:
            # rule D: a twin town (an ambiguous 地番 falls through to here too)
            p["tier"], p["twin"] = "none", True
    return permits


def haversine_m(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
