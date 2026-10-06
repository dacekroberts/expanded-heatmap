"""Japan's coordinate step: a JOIN of permit lists to MLIT's 位置参照情報.

Shared by every Japanese city. **Moved here unchanged from
`scripts/screen_japan_join.py` on 2026-09-24**, so the screen that measured
the join and the builds that use it run one set of rules, not two copies. The
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
are never selected into a permit.

**One exception, the owner's (2026-09-27, Kobe): `name_is_operator()` reads the
operator's name IN MEMORY to compare it with the trade name**, and returns only
a yes or no. Kobe publishes 14 premises whose trade name IS the operator's own
name; the privacy check cannot read Japanese names, so this comparison is the
only way to see them. Where it says yes, the map shows the permit type instead
(Taiwan's name rule). The operator's name is never stored, written or shown.
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
                          "淵": "渕", "秡": "祓",
                          # Kōchi's misses (2026-10-02): its lists write the town 高埇
                          # (U+57C7, outside JIS X 0208); MLIT's cp932 file writes 高埆
                          "埇": "埆"})
# Kōchi's: MHLW writes the same town in kana, 高そね (6 register rows unplaced
# before; the brief's measurement)
STRING_VARIANTS = (("鍛治", "鍛冶"), ("廻リ", "廻り"), ("高そね", "高埆"))


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


# RULES A CITY OPTS INTO (japan.CITIES' "rules"; Japan wave 2, 2026-10-03).
# Each would also move built cities' joins, mostly for the better (measured
# 2026-10-03 on the 20 built cities: Fukuoka's unplaced 92 -> 29, Hiroshima's
# 152 -> 7, Kumamoto's 62 -> 14), and a built city's output changes only at a
# review time that re-renders it, so each is switched on per city:
#   "oaza"           a 大字 dropped, both sides (norm_town)
#   "aza_letter"     字甲 read as 甲, both sides (norm_town)
#   "kou_bare"       a 地番 area's 甲 / 乙 / 丙 after the town (join_city)
#   "chome_missing"  a 丁目 MLIT lacks takes its 大字's centroid (join_city)
#   "machi"          a town spelled with or without its 町 (join_city)
#   "citywide"       an address of only "<city>内" is not a premises
#   "form_cols"      業態 read from FORM_COLS, not 業態 alone
#   "coop"           a cooperative or union operator (組合) is not a person for
#                    the name rule (same_person); on the built cities it would
#                    show co-op shops now withheld (Kobe 7, Toyama 4, Fukui 5)
WAVE2_RULES = frozenset({"oaza", "aza_letter", "kou_bare", "chome_missing", "machi", "citywide", "form_cols",
                         "coop"})


def norm_town(s, rules=()):
    """町字 as a comparable key: NFKC, no spaces, and the 丁目 number in digits.

    The digits rule came from Chūō's and Kōtō's misses: their permits write
    八重洲2丁目 where MLIT writes 八重洲二丁目. Applied to BOTH sides, so both
    sides take the same `rules` (WAVE2_RULES)."""
    s = unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", "")
    # Yokkaichi's and Shimonoseki's misses (2026-10-03): MLIT writes a 大字 the
    # lists leave out, at the start (大字羽津, 4,304 of Yokkaichi's block keys)
    # or after a merged town's name (豊浦町大字川棚). Dropped on both sides.
    if "oaza" in rules:
        s = re.sub(r"(?:^|(?<=[町村]))大字", "", s)
    # Takamatsu's misses: the lists write 仏生山町甲123 where MLIT keys the town
    # 仏生山町字甲. A 字 that is only 甲, 乙, 丙 or 丁 is read as the bare letter.
    if "aza_letter" in rules:
        s = re.sub(r"字([甲乙丙丁])$", r"\1", s)
    # Osaka's misses: 曽根崎新地 (1,807 permits) vs MLIT's 曾根崎新地, 靭本町 vs
    # 靱本町, 松ヶ枝町 vs 松ケ枝町 - one spelling for each variant, both sides.
    s = s.translate(VARIANTS)
    for a, b in STRING_VARIANTS:
        s = s.replace(a, b)
    # Kyoto's misses: MLIT writes 深草スゝハキ町 where permits repeat the kana
    s = re.sub(r"(.)[ゝヽ]", r"\1\1", s)
    # Utsunomiya's misses (2026-10-02): an ASCII hyphen for the katakana long
    # vowel (インタ-パ-ク, MLIT's インターパーク). Only between katakana, so a
    # block number's hyphen is never touched.
    s = re.sub(r"(?<=[ァ-ヺ])[-‐－―ｰ](?=[ァ-ヺ]|$)", "ー", s)
    # Matsuyama's and Okayama's misses: katakana ニ for the numeral 二
    # (ニ番町, 下石井ニ丁目)
    s = re.sub(r"ニ(?=番町|丁目)", "二", s)
    # Sakai's chōme is N丁 with no 目 (2026-10-02): MLIT names 780 of its
    # town-chōme 翁橋町一丁, and the permits write 翁橋町1丁1-1, which the
    # hyphen shift in join_city reads as 翁橋町1丁目 block 1 once MLIT's key
    # says 丁目 too (block 33.7% to 95.8%). Only at the END of a town name:
    # 八丁堀, 六丁の目 and 三丁町 are names, not chōme. No built city's MLIT
    # file has the form; Toyama's one (婦中町十五丁) reads the same on both sides.
    s = re.sub(r"([〇一二三四五六七八九十]+|[0-9]+)丁$", r"\1丁目", s)
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
             "営業所所在地（所在地_連結標記", "施設所在地（所在地_連結標記）",
             # Shibuya's national-schema export (Tokyo, 2026-09-28): without it
             # the shared step read none of its 39,304 rows
             "施設所在地_連結表記",
             # The 2026-10-02 batch, each list's own spelling, after every older
             # one so a built city's choice of column never changes:
             # Matsuyama's food CSVs (a FULL-WIDTH low line) and its XLS registers;
             "所在地＿連結表記", "施設所在地１",
             # Kumamoto's registers (without it city_rows read 0 rows of 2,714);
             "営業所所在地1",
             # Kagoshima's old-law list; Kōchi's full registers (from the town);
             "営業所の所在地", "施設住所名称",
             # Toyama's registers and food workbook (a merged header, see
             # xlsx_rows); Utsunomiya's old-law list (its 申請者住所 is the
             # operator's own address and is never read)
             "所在地", "施設住所", "営業所",
             # Japan wave 2 (2026-10-03), each list's own spelling: Hamamatsu's
             # registers and Sasebo's old-law list (an underscore), Yokkaichi's
             # two food lists (without it xlsx_rows read 0 rows), Nara's old-law
             # list and its three registers
             "施設_所在地", "営業施設住所", "営業所_住所１", "理容所所在地", "美容所所在地", "クリーニング所在地")


# Header cells as one key: Utsunomiya's general-laundry register pads its
# headers with spaces ( 　名称, 2026-10-02). str.strip takes U+3000 too.
def _head(c):
    return "" if c is None else str(c).replace("\n", "").replace("\r", "").strip()


TYPE_COLS = ("業種名", "業種分類", "業種情報公開名称", "営業の種類", "業種区分", "営業種類", "施設（種別）", "施設（種別）等", "種別", "業種",
             "業務種別", "営業の種類もしくは営業の形態",  # Shibuya's (Tokyo)
             # the laundry registers' kind (取次所, 無店舗取次店, リネン): Taitō's and
             # Shibuya's 営業形態, Minato's 施設種別 (Tokyo, 2026-09-28)
             "営業形態", "施設種別",
             # Japan wave 2 (2026-10-03): Kawasaki's food list names its type
             # 営業種目 (without it every row read type "" and none was
             # bucketed); Yokkaichi's laundry list names its kind 区分, whose
             # 無店舗取次店 rows are not premises
             "営業種目", "区分")

# 業態, the form of business, read beside the type (japan_eigyo.FORM_RULES).
# Fukuoka's lists and MHLW's name it 業態; Yokosuka's food list 詳細業種
# (給食, 屋台型臨時営業, 旅館の経営を兼ねる飲食店営業, スナック: without it
# each read as a restaurant), Sasebo's old-law list 種目 (旅館, 自動販売機,
# 仕出し屋). Japan wave 2, 2026-10-03.
FORM_COLS = ("業態", "詳細業種", "種目")


# 名称 last: the Tokyo catalogue's 生活衛生 registers (Taitō's, Shibuya's) name
# the premises so, and without it their rows had no name (Tokyo, 2026-09-28)
NAME_COLS = ("屋号", "施設名称", "営業施設名称、屋号又は商号", "施設の名称", "施設屋号", "名称",
             # The 2026-10-02 batch: Matsuyama (food CSV, XLS registers), Toyama,
             # Fukui's, Utsunomiya's and Kōchi's registers, Kitakyushu's old-law
             # list (3,383 rows had no name without it), Sakai, Kagoshima
             "施設名称1", "施設名称１", "施設名", "営業所名称", "屋号名称", "営業所の名称",
             "営業所の名称、屋号又は商号",
             # Japan wave 2 (2026-10-03): Hamamatsu's registers and Sasebo's
             # old-law list, Yokkaichi's food lists, Nara's three registers
             "施設_名称", "営業施設屋号", "理容所名称", "美容所名称", "クリーニング名称")


def xlsx_rows(data, sheet=None, merged_header=False):
    """Every sheet that has an address column, header found by that column (a
    sheet may open with title rows). Summary sheets without one are skipped.

    `sheet` reads one sheet only, by name (spaces ignored) or index: Fukui's
    workbooks hold twelve month-end sheets, the newest first, and the newest
    IS the list (2026-10-02). `merged_header`: a header cell merged across
    several columns names only its first, so the unnamed columns after it are
    joined into it - Toyama's food workbook writes 施設住所 over municipality,
    town, number and building (H1:K1), and read cell by cell its address was
    「富山市」 alone. Opt-in, since a built city's unnamed column is not a merge."""
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    sheets = wb.worksheets
    if sheet is not None:
        sheets = ([sheets[sheet]] if isinstance(sheet, int)
                  else [ws for ws in sheets if ws.title.replace(" ", "").replace("　", "") == sheet])
        if not sheets:
            raise ValueError(f"no sheet {sheet!r} in the workbook")
    for ws in sheets:
        head = None
        for r in ws.iter_rows(values_only=True):
            cells = [_head(c) for c in r]
            if head is None:
                if any(c in ADDR_COLS for c in cells):
                    head = cells
                continue
            if not any(cells):
                continue
            if not merged_header:
                yield dict(zip(head, cells))
                continue
            row, last = {}, None
            for h, c in zip(head, cells):
                if h:
                    last = h
                    row[h] = c
                elif last is not None:
                    row[last] += c
            yield row


def zip_member_name(info):
    """Japanese member names without the UTF-8 flag are cp932 read as cp437."""
    if info.flag_bits & 0x800:
        return info.filename
    try:
        return info.filename.encode("cp437").decode("cp932")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return info.filename


def city_rows(path, sheet=None, merged_header=False):
    """Rows as dicts from a CSV, an XLSX, an old .xls, or XLSX members of a ZIP
    ('file.zip::part' keeps only members whose name contains part). `sheet`
    and `merged_header` are xlsx_rows'."""
    path, _, part = str(path).partition("::")
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                nm = zip_member_name(info)
                if nm.lower().endswith(".xlsx") and part in nm:
                    yield from xlsx_rows(zf.read(info), sheet, merged_header)
        return
    if path.lower().endswith(".xlsx"):
        yield from xlsx_rows(Path(path).read_bytes(), sheet, merged_header)
        return
    if path.lower().endswith(".xls"):
        # Matsuyama's registers are the old BIFF format (2026-10-02), which
        # openpyxl cannot open; workbook_tables reads it through xlrd
        yield from workbook_tables(path)
        return
    text = decode(Path(path).read_bytes())
    head = text.split("\n", 1)[0]
    # Meguro's 生活衛生 registers: each TAB-separated line is wrapped whole in CSV
    # quotes, inner quotes doubled ("No\t""施設名称""\t…"). Unwrap it with the csv
    # reader, then read the TSV inside. A plain quoted TSV has no doubled quotes.
    if head.startswith('"') and "\t" in head and '""' in head:
        text = "\n".join(r[0] for r in csv.reader(io.StringIO(text)) if r)
        head = text.split("\n", 1)[0]
    delim = "\t" if head.count("\t") > head.count(",") else ","
    rows = csv.reader(io.StringIO(text), delimiter=delim)
    first = next(rows, None)
    if first is None:
        return
    hi, header, skipped = 0, first, []
    # The header found by its address column, as xlsx_rows does (2026-10-02):
    # Hakodate's registers open with one or two title rows, Matsuyama's
    # new-law food list with an empty line. A file with no address column in
    # its first 30 rows keeps its first line, as before.
    if not any(_head(c) in ADDR_COLS for c in first):
        skipped = [first]
        for r in rows:
            skipped.append(r)
            if any(_head(c) in ADDR_COLS for c in r):
                header, hi = r, len(skipped) - 1
                break
            if len(skipped) >= 30:
                break
        if hi == 0:
            rows = iter(skipped[1:] + list(rows))
    head = [_head(c) for c in header]
    # csv.DictReader's own shape: blank lines skipped, missing cells None,
    # surplus cells under the key None
    for r in rows:
        if not r:
            continue
        d = dict(zip(head, r))
        if len(r) > len(head):
            d[None] = r[len(head):]
        elif len(r) < len(head):
            for h in head[len(r):]:
                d.setdefault(h, None)
        yield d


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
              "type": "業種", "start": "許可開始日", "end": "許可終了日", "granted": "許可年月日"}  # premises columns only
KYOTO_CORP = re.compile(r"株式会社|有限会社|合同会社|合資会社|合名会社|一般社団法人|公益社団法人|一般財団法人|"
                        r"公益財団法人|社会福祉法人|医療法人|学校法人|宗教法人|特定非営利活動法人|[(]株[)]|[(]有[)]|㈱|㈲")


def wareki_date(s):
    """H31.4.30 / 令和3年4月1日 / 2026-03-31 / an Excel serial -> date, else None."""
    # Sasebo's old-law list pads the era form with spaces, R 8. 5.31 (0 of 607
    # dates read without this, 2026-10-03)
    s = re.sub(r"\s", "", unicodedata.normalize("NFKC", str(s or "")))
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
            # the owner's name rule, answered here while the operator column is
            # in hand (2026-09-28): only the yes or no travels on
            rec["own"] = same_person(rec["name"], (r.get(c) for c in OPERATOR_COLS))
            rec["d_start"], rec["d_end"], rec["d_granted"] = (wareki_date(rec["start"]), wareki_date(rec["end"]),
                                                              wareki_date(rec["granted"]))
            rank = (rec["d_end"] or datetime.date(1900, 1, 1), rec["d_granted"] or datetime.date(1900, 1, 1))
            key = _kyoto_key(rec)
            if key not in best or rank > best[key][0]:
                best[key] = (rank, rec)
    # the start date lets a build drop permits whose term is under a year (48
    # restaurants on 2026-09-24), as the rebuild's own count did
    return [{"営業所所在地": rec["a1"] + rec["a2"], "業種": rec["type"], "屋号": rec["name"],
             "許可開始日": rec["d_start"].isoformat() if rec["d_start"] else "",
             "許可終了日": rec["d_end"].isoformat(), "name_is_operator": rec["own"]}
            for _, rec in best.values() if rec["d_end"] and rec["d_end"] >= as_of]


class BlockIndex(dict):
    """The block keys, plus `far`: the keys whose MLIT rows lie more than FAR_M
    apart (one 地番 filed for places far from each other). Read only by the
    甲乙丙 rule in join_city (Himeji, 2026-10-03)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.far = set()


FAR_M = 500


def load_city_isj(isj_dir, rules=()):
    """Every ward's block and town-chōme files, keyed by (ward, town[, block]).

    Kyoto's misses (rule D): one town name can belong to two places in a ward -
    123 names in 上京, 中京 and 下京, the twins a median 1.27 km apart. Such a
    town's chōme entry is None, and so is a block whose 地番 occurs in more than
    one twin; join_city leaves those rows unplaced rather than guess a twin."""
    cents = collections.defaultdict(list)
    for z in sorted(Path(isj_dir).glob("*-19.0b.zip")):
        for r in read_zip_csv(z):
            cents[(r["市区町村名"].split("市")[-1], norm_town(r["大字町丁目名"], rules))].append((float(r["緯度"]), float(r["経度"])))
    chome = {k: pts[0] if len(pts) == 1 else None for k, pts in cents.items()}
    twin_of = collections.defaultdict(set)  # a twin town's (ward, town, block) -> which twins it occurs in
    blocks = BlockIndex()
    first = {}
    for z in sorted(Path(isj_dir).glob("*-24.0a.zip")):
        for r in read_zip_csv(z):
            ward = r["市区町村名"].split("市")[-1]
            key = (ward, norm_town(r["大字・丁目名"], rules), first_number(r["街区符号・地番"]))
            pt = (float(r["緯度"]), float(r["経度"]), r["住居表示フラグ"])
            if chome.get(key[:2], ()) is None:
                twins = cents[key[:2]]
                twin_of[key].add(min(range(len(twins)), key=lambda i: haversine_m(pt[:2], twins[i])))
            if r.get("代表フラグ") == "1" or key not in blocks:
                blocks[key] = pt
            if key not in first:
                first[key] = pt[:2]
            elif key not in blocks.far and haversine_m(first[key], pt[:2]) > FAR_M:
                blocks.far.add(key)
            # Sendai's 字 addresses (福室字境４番) - MLIT keeps the 字 in 小字・通称名,
            # so the same 地番 is also keyed under 大字 + 字 + 小字.
            if r.get("小字・通称名"):
                akey = (ward, norm_town(r["大字・丁目名"] + "字" + r["小字・通称名"], rules), key[2])
                if r.get("代表フラグ") == "1" or akey not in blocks:
                    blocks[akey] = pt
    for key, which in twin_of.items():
        if len(which) > 1:
            blocks[key] = None
    return blocks, chome


def load_city_permits(path, pref, city, wardless=False, rules=()):
    """Own-format city lists: one address string naming the ward. Reads only the
    premises columns - never 営業者名 / 申請者名 / 開設者 (people)."""
    return permits_from_rows(city_rows(path), pref, city, wardless, rules)


def in_term(rows, end_cols, as_of):
    """The rows whose permit is still in term on `as_of` (a date, never today):
    the first of `end_cols` that reads as a date (wareki or ISO) is the
    expiry. An old-law list keeps permits past their expiry until its next
    edition (Kitakyushu's 許可終了日: 1,373 of 3,383 rows end before
    2026-10-02; Utsunomiya's 満了年月日3), so a build drops them against its
    pinned as-of. A row with no readable expiry is kept."""
    for r in rows:
        end = next((d for d in (wareki_date(r.get(c)) for c in end_cols) if d), None)
        if end is None or end >= as_of:
            yield r


def rebuilt_register(paths, as_of, end_col="許可満了日", granted_col="許可年月日", rules=()):
    """A register rebuilt from a complete list and the months since, Kyoto's
    method for any list (Higashiōsaka, 2026-10-03: its 全許可 list of
    2026-04-01 plus each month's new permits to 2026-08-31). `paths` oldest
    first. Where (address, trade name, type) repeats, the permit ending latest
    wins (a renewal is a new monthly row; the old law's （旧） prefix is not part
    of the type for this key); kept while `end_col` is on or after `as_of`, a
    pinned date, never today. Closures between editions are invisible, so it
    is an upper bound, disclosed as Kyoto's is.

    Returns premises columns only (address, trade name, type, 業態, the two
    dates, the closure fields), plus the name rule's ANSWER, compared here
    while the operator columns are in hand; never the operator's name."""
    best = {}
    for path in paths:
        for r in city_rows(path):
            addr = next((r[c] for c in ADDR_COLS if (r.get(c) or "").strip()), "")
            name = next((r[c] for c in NAME_COLS if (r.get(c) or "").strip()), "")
            typ = next((r[c] for c in TYPE_COLS if r.get(c)), "")
            end, granted = wareki_date(r.get(end_col)), wareki_date(r.get(granted_col))
            key = (re.sub(r"[‐‑‒–—―−ｰー－]", "-", unicodedata.normalize("NFKC", addr).replace(" ", "")
                          .replace("　", "")),
                   _name_key(name), re.sub(r"^\(旧\)", "", unicodedata.normalize("NFKC", typ).replace(" ", "")))
            rank = (end or datetime.date(1900, 1, 1), granted or datetime.date(1900, 1, 1))
            if key not in best or rank >= best[key][0]:
                best[key] = (rank, {"所在地": addr, "施設名称": name, "業種": typ,
                                    "業態": next(((r.get(c) or "").strip() for c in FORM_COLS
                                                 if (r.get(c) or "").strip()), ""),
                                    end_col: end.isoformat() if end else "",
                                    granted_col: granted.isoformat() if granted else "",
                                    "廃業年月日": r.get("廃業年月日") or "", "申請区分": r.get("申請区分") or "",
                                    "name_is_operator": name_is_operator(r, rules)})
    return [rec for (e, _), rec in best.values() if e >= as_of]


VARIATION_SELECTORS = re.compile("[︀-️\U000e0100-\U000e01ef]")


def permits_from_rows(rows, pref, city, wardless=False, rules=()):
    """load_city_permits for rows already read - Kyoto's rebuilt register.

    `wardless`: a city with no wards (japan.CITIES' "wardless"; the 2026-10-02
    batch). Its address is never split at a 区, because its neighbourhoods end
    in one (Toyama's 太田北区, 五福六区; Fukui's 土地区画整理事業) and MLIT keys
    every town under an empty ward."""
    out = []
    for r in rows:
        addr = next((r[c] for c in ADDR_COLS if (r.get(c) or "").strip()), "")
        a = unicodedata.normalize("NFKC", addr).replace(" ", "").replace("　", "")
        # Utsunomiya's beauty register (2026-10-02): a line break inside the
        # address, the building after it; the parse below reads one line
        a = a.replace("\r", "").replace("\n", "")
        # Kyoto's misses (2026-09-28): an ideographic variation selector after a
        # kanji (高辻 + U+E0100 in 20 rows) picks a glyph, never a different town
        a = VARIATION_SELECTORS.sub("", a)
        a = re.sub("^" + pref, "", a)
        # Kobe's miss: the city's name can recur INSIDE an address
        # (灘区六甲山町…神戸市立六甲山牧場), so strip it only where no ward precedes it.
        i = a.find(city)
        if i >= 0 and "区" not in a[:i]:
            a = a[i + len(city):]
        # Kurume's MHLW rows (2026-10-03): an address of only 久留米市内 ("within
        # the city") is a vehicle or stall licensed citywide, as 一円 is; all
        # 1,022 such rows share one point, so the default-point guard sees one
        # town and lets it through
        citywide = "citywide" in rules and a == "内"
        if city == "京都市":
            a = a.translate(KYOTO_GAIJI)
        if wardless:
            ward, rest = "", a
        elif city.endswith("区"):
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
        out.append({"ward": ward, "town": norm_town(town, rules), "block": first_number(tail), "rest": tail,
                    "dir": (d.group(1), d.group(2)) if d else None,
                    "addr": addr, "type": next((r[c] for c in TYPE_COLS if r.get(c)), ""),
                    # Fukuoka's lists (the city's and MHLW's) carry 業態, the
                    # form of business, and only there are vehicles, stalls and
                    # school kitchens marked; japan_eigyo reads it beside the type
                    "form": next(((r.get(c) or "").strip() for c in (FORM_COLS if "form_cols" in rules else ("業態",))
                                  if (r.get(c) or "").strip()), ""),
                    # MHLW keeps closed premises, marked 許可(廃業) / 届出(廃業);
                    # Shibuya keeps them with a 廃業日 (22,311 of 39,304 rows)
                    "closed": bool((r.get("廃業年月日") or r.get("廃業日") or "").strip())
                    or "廃業" in (r.get("申請区分") or ""),
                    "name": next((r[c] for c in NAME_COLS if r.get(c)), ""), "pub": pub,
                    # not a premises: vehicles, and 市内一円 / 仙台市内一円 ("anywhere in
                    # the city") - Sendai's festival stalls (仮設, 臨時) are written so -
                    # and 無店舗 ("no shop"): Meguro's laundry pick-ups at 目黒区内;
                    # Matsuyama writes "within the health centre's area" (保健所管内
                    # / 保健所管轄内) for its vehicles and stalls (277 food rows)
                    "mobile": not addr.strip() or "一円" in addr or "保健所管" in addr or citywide
                    or any(w in next((r[c] for c in TYPE_COLS if r.get(c)), "") for w in ("自動車", "無店舗"))})
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


def join_city(permits, blocks, chome, rules=()):
    towns = collections.defaultdict(set)
    for w, t in chome:
        towns[w].add(t)
    # 大字 whose blocks are also keyed by 小字 (the Sendai key above): their 地番
    # restart in each 小字 - 110 of 五日市町's 588 numbers occur in 2+ of them
    has_koaza = {(w, t.rsplit("字", 1)[0]) for w, t, _ in blocks if "字" in t[1:]}
    block_towns = {(w, t) for w, t, _ in blocks}
    far = getattr(blocks, "far", set())
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
        # Himeji's misses (2026-10-03): the lists write a 地番 area's 甲 / 乙 / 丙
        # after the town (白浜町甲1920), where MLIT files the number under the
        # bare town (白浜町 1920; 8 of 1,201 keep the 甲). Only where the number
        # misses under the town as written and that town has no centroid of its
        # own. The bare town's number places the row where MLIT gives it one
        # place; where its rows lie over FAR_M apart (甲1920 and 乙1920 both
        # filed as 1920), the bare town's centroid does.
        kou = re.match(r"^(.+?)[甲乙丙丁]$", p["town"]) if not hit and "kou_bare" in rules else None
        if (kou and (w, p["town"]) not in chome
                and ((w, kou.group(1)) in chome or (w, kou.group(1)) in block_towns)):
            bare = kou.group(1)
            key = (w, bare, p["block"])
            p["town"], p["kou"] = bare, True
            if p["block"] and key not in far:
                hit = blocks.get(key)
        # Nara's misses (2026-10-03): the registers write 宝来町一丁目 where MLIT
        # names the town 宝来1丁目, and 北京終 where it writes 北京終町. Tried
        # before rule C, which would take 宝来町 (a separate 大字) as a prefix.
        if not hit and "machi" in rules and (w, p["town"]) not in chome:
            t = p["town"]
            alt = re.sub(r"町(\d+丁目)$", r"\1", t) if re.search(r"町\d+丁目$", t) else (
                None if t.endswith("町") or "丁目" in t else t + "町")
            if alt and ((w, alt) in chome or (w, alt) in block_towns):
                p["town"], p["machi"] = alt, True
                hit = blocks.get((w, alt, p["block"]))
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
                elif "chome_missing" in rules and re.fullmatch(r"\d+丁目", p["town"][len(t):]):
                    # Toyota's misses (2026-10-03): 浄水町1丁目 to 5丁目, a
                    # replotted town whose 丁目 MLIT's block edition lacks (it
                    # keys 浄水町 as a 大字 with 小字). A dropped tail that is a
                    # 丁目 is no 小字: the row takes the 大字's centroid.
                    p["town"], p["affix"] = t, "chome-missing"
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


# Each list's own spelling of its operator column. Fukuoka's (2026-09-28): the
# food list's 営業者氏名 (Tokyo's lists spell it so too) and the registers'
# 開設者法人名（開設者氏名）- a company's name, or a sole trader's own. Without
# them the rule compared nothing there. MHLW's 法人名 (owner, 2026-10-05,
# reversing DECISIONS 2026-09-28): it holds a sole trader's own name as well as
# a company's (40,312 rows of the 47 cached files carry no company marker and
# no 法人番号; staging measured 790 whose trade name equals it), so the rule
# compares it, in memory, like every column here; KYOTO_CORP keeps companies out.
# Kyoto's (2026-09-28): the food lists' 申請者＿申請者名 and the registers'
# 申請者氏名; kyoto_permit_stream compares them itself and carries only the answer.
# Tokyo's (2026-09-28): the catalogue registers' 法人代表者氏名 (Taitō, Shibuya),
# a company's representative - a person, as 代表者名. The national-schema food
# lists (Chūō, Minato, Shinjuku, Kōtō, Shibuya) carry 法人名 only, as MHLW's do,
# so they are compared on it too since 2026-10-05.
# The 2026-10-02 batch, each list's spelling (without them the rule compared
# nothing there): Matsuyama's 申請者個人名 (food) and 開設者氏名 (registers;
# Kumamoto's and Hakodate's too); Kumamoto's 代表者氏名（法人のみ）; Fukui's
# 申請者名(法人名) (food, half-width brackets), 申請者名（法人名） (registers,
# full-width) and 法人代表者名; Utsunomiya's registers' 開設者 and 代表者;
# Kitakyushu's 代表者氏名. And Matsuyama's registers' 開設者法人名 / 営業者法人名:
# filled on every row, with no company marker on 443 of 485 barbers, so a
# sole trader's own name sits there and 開設者氏名 holds only a company's
# representative (one laundry flagged, as the brief measured).
# Japan wave 2 (2026-10-03), each list's spelling: Kawasaki's 営業者氏名（法人のみ）
# (companies only); Yokosuka's registers' 営業者氏名・法人名称 (a sole trader's
# own name or a company's, on every row); Himeji's 氏名 (all four files);
# Takamatsu's registers' 開設者申請者名 / 開設者代表者名 and its laundry list's
# 営業者申請者名 / 営業者代表者名; Nara's and Sasebo's old-law 申請者_氏名;
# Yokkaichi's 申請者代表者名; Toyota's registers' 開設者氏名（法人） (companies
# only); Nara's registers' 開設者代表者.
OPERATOR_COLS = ("営業者名", "開設者名", "申請者名", "代表者名", "営業者氏名", "開設者法人名（開設者氏名）",
                 "申請者＿申請者名", "申請者氏名", "法人代表者氏名",
                 "申請者個人名", "開設者氏名", "代表者氏名（法人のみ）", "申請者名(法人名)", "申請者名（法人名）",
                 "法人代表者名", "開設者", "代表者", "代表者氏名", "開設者法人名", "営業者法人名",
                 "営業者氏名（法人のみ）", "営業者氏名・法人名称", "氏名", "開設者申請者名", "開設者代表者名",
                 "営業者申請者名", "営業者代表者名", "申請者_氏名", "申請者代表者名", "開設者氏名（法人）",
                 "開設者代表者", "法人名")


def _name_key(s):
    return re.sub(r"[\s・]", "", unicodedata.normalize("NFKC", s or ""))


def name_is_operator(row, rules=()):
    """True when the row's trade name IS its operator's own name - an
    individual's name published as a shop sign. Compared in memory; the
    operator's name is not returned (owner 2026-09-27, see the docstring).
    A company operator is never an individual: KYOTO_CORP's markers say so.
    A rebuilt register (Kyoto's) carries the answer itself, never the name."""
    name = next((row[c] for c in NAME_COLS if (row.get(c) or "").strip()), "")
    if bare_personal_name(name):
        return True
    if "name_is_operator" in row:
        return bool(row["name_is_operator"])
    return same_person(name, (row.get(c) for c in OPERATOR_COLS), "coop" in rules)


# THE SIGN RULE, the name rule's version 2 (owner, 2026-10-06; v1 2026-09-27,
# 法人名 added 2026-10-05): a trade name written as a bare personal name - a
# common surname, a space (full-width or half-width), then 1 to 3 kanji or
# hiragana, nothing else - is withheld whatever the operator column holds.
# Liège's and Brussels' sign rule (Gelsenkirchen's call 15) adapted to
# Japanese. Staging measured 78 such shown rows in 22 of the 34 built cities
# (432,489 rows). The same shape WITHOUT the space is not used: it matched 523
# rows, mostly shop names (DECISIONS 2026-10-06).
BARE_SURNAMES = tuple(sorted(set("""
佐藤 鈴木 高橋 田中 伊藤 渡辺 渡邊 山本 中村 小林 加藤 吉田 山田 佐々木 山口 松本 井上 木村 林 斎藤 斉藤 清水 山崎
森 池田 橋本 阿部 石川 山下 中島 石井 小川 前田 岡田 長谷川 藤田 後藤 近藤 村上 遠藤 青木 坂本 福田 太田 西村 藤井
金子 岡本 藤原 中野 三浦 原田 中川 松田 竹内 小野 田村 中山 和田 石田 森田 上田 原 内田 柴田 酒井 宮崎 横山 高木 安藤
宮本 大野 小島 谷口 工藤 今井 高田 丸山 増田 杉山 村田 大塚 小山 平野 藤本 河野 上野 野口 武田 松井 千葉 岩崎 菅原 木下
久保 佐野 野村 松尾 市川 菊地 杉本 古川 大西 島田 水野 桜井 高野 渡部 吉川 山内 西田 飯田 菊池 西川 小松 北村 安田 五十嵐
川口 平田 関 中田 久保田 服部 東 岩田 土屋 川崎 福島 本田 辻 樋口 秋山 田口 永井 山中 中西 吉村 川上 石原 大橋 松岡 馬場
浜田 森本 星野 矢野 浅野 大久保 松下 吉岡 小池 野田 荒木 大谷 内藤 松浦 熊谷 黒田 尾崎 永田 川村 望月 田辺 松村 荒井
""".split()), key=len, reverse=True))
_BARE_NAME = re.compile(r"^(?:" + "|".join(map(re.escape, BARE_SURNAMES)) + r")\s+[一-龥々ぁ-ゖ]{1,3}$")


def bare_personal_name(name):
    """True when a trade name is a bare personal name (the sign rule above).
    NFKC turns the full-width space into a plain one."""
    return bool(_BARE_NAME.match(unicodedata.normalize("NFKC", name or "").strip()))


# Not a person, for the name rule where a city opts into "coop": KYOTO_CORP's
# companies and, apart from it so Kyoto's de-duplication key never moves,
# cooperatives and unions (組合: 協同組合, 企業組合). Takamatsu (2026-10-03): a
# 協同組合 operating two food vehicles under its own name read as an individual.
NOT_A_PERSON = re.compile(KYOTO_CORP.pattern + r"|組合")


def same_person(trade_name, operators, coop=False):
    """The name rule's comparison: the trade name equals an individual
    operator's name (a company's never counts, nor with `coop` a
    cooperative's)."""
    name = _name_key(trade_name)
    corp = NOT_A_PERSON if coop else KYOTO_CORP
    for o in operators:
        op = _name_key(o)
        if op and not corp.search(op) and name == op:
            return True
    return False


def haversine_m(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
