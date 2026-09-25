"""Taiwan: the facts shared by every Taiwanese city, measured 2026-09-23.

Profiled for four cities at once: Taipei (Regional), Taichung and Taoyuan
buildable, Kaohsiung geo-blocked. Taichung is the first built (2026-09-25).

  * Business leg: the national BUSINESS TAX REGISTER (全國營業(稅籍)登記資料集,
    Fiscal Information Agency, daily) - one row per trading LOCATION, a parent
    ID making branches their own rows, the address as one string, and a
    6-digit industry code whose ISIC-aligned divisions give the buckets.
    No personal-name column.
  * Coordinates: a JOIN, not a geocoder - each city's door-plate file (門牌位置
    數值資料) keyed by street / lane / alley / number. `parse()` and
    `canon_*` are the method `scripts/screen_taiwan_join.py` measured; moved
    here unchanged on 2026-09-25 so the pipeline and the screen share one copy.
    **Taipei is the control: any change to `parse()` re-runs Taipei first.**
  * Licence: OGDL v1 on every source, with a LOAD-BEARING attribution
    statement per source (see docs/data_sources.md).
  * Names (owner, 2026-09-23): a business name is shown only when it is a
    TRADE name - companies and branches, and sole proprietors whose name
    carries a business marker. The FIA itself refuses to publish owners' names.
  * Certificates: Python's bundle lacks Taiwan's government root (GRCA); use
    the OS store (`truststore`). Never switch verification off.

**Nothing here fetches.** The register lives in the shared cache
(`data/taiwan/raw/`, gitignored), as France's and Japan's national files do.
"""
import csv
import io
import re
import unicodedata
import zipfile
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
SHARED_RAW = _ROOT / "data" / "taiwan" / "raw"

REGISTER_URL = "https://eip.fia.gov.tw/data/BGMOPEN1.zip"
REGISTER_ZIP = SHARED_RAW / "BGMOPEN1.zip"

# ISIC-aligned divisions, read from the register's own code names. 487 is
# online shopping - non-store retail, excluded as NAICS 454 is everywhere.
BUCKET = {"47": "Retail", "48": "Retail", "56": "Food service", "96": "Personal services"}
EXCLUDE_PREFIXES = ("487",)

# The name rule's business markers: a sole proprietor's registered name is
# shown only when it carries one (brief taipei.md, owner 2026-09-23).
# Only characters that do not occur in given names: 美, 軒 and 莊 were
# considered and left out because they do (陳美玲, 宇軒, and 莊 is a surname).
# The rule errs toward hiding, as the publisher's own refusal argues.
BUSINESS_MARKERS = ("行", "店", "社", "館", "坊", "號", "屋", "廳", "舖", "鋪", "商", "中心",
                    "企業", "工作室", "超市", "市場", "攤", "餐", "飲", "茶", "咖啡", "麵")
LATIN = re.compile(r"[A-Za-z]")
SOLE_PROPRIETOR = "獨資"

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


def plate_key(street, lane, alley, number):
    """A door-plate file row's key, in parse()'s shape (None without a number)."""
    num = canon_number(number)
    if not num:
        return None
    return (canon_street(street), re.sub(r"\D", "", nfkc(lane)),
            re.sub(r"\D", "", nfkc(alley)), num)


def register_rows(prefixes, zip_path=REGISTER_ZIP):
    """Every register row whose address starts with one of the city's prefixes,
    as a dict. The zip's largest member is the register."""
    z = zipfile.ZipFile(zip_path)
    member = max(z.infolist(), key=lambda i: i.file_size)
    rd = csv.DictReader(io.TextIOWrapper(z.open(member), encoding="utf-8-sig",
                                         errors="replace", newline=""))
    for r in rd:
        if (r.get("營業地址") or "").startswith(prefixes):
            yield r


def register_date(zip_path=REGISTER_ZIP):
    """The register's own data date: its first data row carries it in the address
    column ('25-SEP-26'). Returned as YYYY-MM-DD."""
    from datetime import datetime
    z = zipfile.ZipFile(zip_path)
    member = max(z.infolist(), key=lambda i: i.file_size)
    rd = csv.reader(io.TextIOWrapper(z.open(member), encoding="utf-8-sig", errors="replace",
                                     newline=""))
    next(rd)
    first = next(rd)[0].strip()
    return datetime.strptime(first.title(), "%d-%b-%y").strftime("%Y-%m-%d")


def bucket_of(code):
    code = (code or "").strip()
    if code.startswith(EXCLUDE_PREFIXES):
        return None
    return BUCKET.get(code[:2])


def is_trade_name(name, org_type):
    """The owner's name rule: companies and branches always; a sole proprietor
    only when the name carries a business marker."""
    if SOLE_PROPRIETOR not in (org_type or ""):
        return True
    n = nfkc(name)
    return bool(LATIN.search(n)) or any(m in n for m in BUSINESS_MARKERS)
