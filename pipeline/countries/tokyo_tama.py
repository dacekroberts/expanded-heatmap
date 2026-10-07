"""The Tama cities' shared business leg: the Tokyo Metropolitan Government's
ledgers for the health centres it runs (東京都保健医療局, 東京都が設置している
保健所等で保有する台帳一覧), each Tama city cut out of them by its address.

One module for the eight Tama cities East-1 builds (2026-10-07): Higashiyamato,
Nishitōkyō, Tama, Higashimurayama, Fuchū (Tokyo), Chōfu, Tachikawa and Hino.
Each city's config reads SOURCES, REQUIRED_COLUMNS, SOURCE_FILES and
source_rows() from here and adds only what is its own (its municipality, its
ISJ pair, its rail).

  * Five ledgers, cp932 CSV, all as of 2026-08-31 (the page's 「令和8年8月31日
    現在」): food permits, food notifications, barbers, beauty salons and
    laundries. The ledgers are partial by design (the briefs; owner, call
    109): new permits only since 2019-08, opt-outs and closures left out.
  * MHLW's Tokyo file (13000), the same health centres' electronic filings:
    its rows the ledgers lack are added (owner, call 169, the Tokyo wards'
    precedent), the ledger's row kept where both hold a premises (SUPERSEDES).
    Its 市区町村名 reads 新宿区 on every row (the registering office), so it is
    cut by its address too, never by that column.
  * The licence: CC BY 4.0 through the Tokyo catalogue's two entries (owner,
    call 108, Taitō's precedent). The page links the catalogue entries, never
    the 保健医療局 page or files (that site's link policy); fetch_sources.py
    downloads from that host, which is not a link.

No imports from data/ at module level: the deployed app imports each city's
config (its page reads HEATMAP_HTML), and through it this module.
"""
import unicodedata

LEDGER_PAGE = "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho"
_FILES = "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/"
# The catalogue entries the page links and credits (call 108)
CATALOGUE = "東京都オープンデータカタログサイト"
CATALOGUE_FOOD = "https://catalog.data.metro.tokyo.lg.jp/dataset/t000055d0000000361"
CATALOGUE_REGISTERS = "https://catalog.data.metro.tokyo.lg.jp/dataset/t000055d0000000614"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"

# source key -> (file, URL of the edition the build read, dataset page). The
# slugs carry a revision suffix (-7, -1-7, -5) that may move with a monthly
# edition. Pinned, not read from the page by SOURCE_LINKS as the briefs
# planned: the page links each ledger twice, CSV and Excel, and only the link
# TEXT says which (shokuhin-todokede-1-7 is the CSV, shokuhin-kyoka-1-7 the
# Excel; read 2026-10-07). A new edition is a re-measure (the briefs' edition
# check fails first).
SOURCE_FILES = {
    "food": ("shokuhin-kyoka-7.csv", _FILES + "shokuhin-kyoka-7", LEDGER_PAGE),
    "notify": ("shokuhin-todokede-1-7.csv", _FILES + "shokuhin-todokede-1-7", LEDGER_PAGE),
    "barber": ("kankyo-riyoujo-5.csv", _FILES + "kankyo-riyoujo-5", LEDGER_PAGE),
    "beauty": ("kankyo-biyoujo-5.csv", _FILES + "kankyo-biyoujo-5", LEDGER_PAGE),
    "laundry": ("kankyo-cleaning-5.csv", _FILES + "kankyo-cleaning-5", LEDGER_PAGE),
    "mhlw": ("13000_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
             MHLW_TOP),
}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The notification ledger is a food list to japan_eigyo (its types are the
# 届出 types: konbini, supermarkets, greengrocers); the key names it apart
SOURCE_KIND = {"notify": "food"}
# Declared, never inferred: the ledgers cp932, MHLW's UTF-8 with a BOM
SOURCE_ENCODING = {**{k: "cp932" for k in SOURCES if k != "mhlw"}, "mhlw": "utf-8-sig"}
# The ledgers' stated date; MHLW's file states none, and its newest 廃業年月日
# and 許可年月日 fall in August 2026 (measured 2026-10-07: 2026-08-31, 08-27)
AS_OF = "2026-08-31"
SOURCE_AS_OF = {**{k: AS_OF for k in SOURCES if k != "mhlw"}, "mhlw": None}
# MHLW's rows carry a permit term (許可開始日, 許可満了日): read against the last
# day the file covers, never today (calls 161 and 172)
TERM_AS_OF = {"mhlw": AS_OF}

# Dropped at read (owner, call 109): the representative's name, the operator's
# own address and every phone. 営業者氏名 stays, read IN MEMORY by the name
# rule only (japan_register.name_is_operator), never kept. 法人代表者氏名 is in
# japan_register.OPERATOR_COLS, so it must go before the rows reach the rule
# (the briefs measured 0 rows withheld with it or without it).
DROP_COLUMNS = ("法人代表者氏名", "営業者住所", "営業者ビル名", "営業所電話番号", "営業者電話番号", "施設TEL",
                "営業者TEL")
# MHLW's: 法人名 is read IN MEMORY by the name rule (owner, 2026-10-05);
# 法人番号, 法人住所 and 営業施設電話番号 are never selected.
MHLW_DROP = ("法人番号", "法人住所", "営業施設電話番号")

_LEDGER_FOOD = ("屋号", "営業所所在地", "営業者氏名", "営業の種類")
_REGISTER = ("施設名称", "施設所在地", "営業者氏名", "確認年月日")
# The columns each file must carry, after the drop; fetch_sources.py and step
# 2 stop on a header without them. The operator column 営業者氏名 is REQUIRED,
# so the name rule cannot silently compare nothing.
REQUIRED_COLUMNS = {
    "food": (*_LEDGER_FOOD, "申請区分", "初回許可日"),
    "notify": (*_LEDGER_FOOD, "届出年月日"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": (*_REGISTER, "営業形態"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}

# Where each source's address is
ADDRESS_COLUMN = {"food": "営業所所在地", "notify": "営業所所在地", "barber": "施設所在地", "beauty": "施設所在地",
                  "laundry": "施設所在地", "mhlw": "営業施設所在地"}
# The share at the yearbook's date (calls 187-189; japan_step2.at_date): the
# restaurant's first permit, the register's confirmation (a lower bound, since
# 確認年月日 renews on a change of operator)
SHARE_DATES = {"food": "初回許可日", "barber": "確認年月日", "beauty": "確認年月日", "laundry": "確認年月日"}

# MHLW publishes an address only where the filer agreed to it (Fukuoka's)
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in a ledger and MHLW's file: the LEDGER's row is kept (call
# 169, the Tokyo wards' precedent of 2026-09-24)
SUPERSEDES = {"food": ("mhlw",), "notify": ("mhlw",)}
# The share the page states is the permit ledger's own, without MHLW's rows
# (call 169) and without the notification ledger, which holds no permit:
# Higashiyamato's one notification typed 飲食 is a stall 営業とみなされない
# (2026-10-07), which the share's "飲食" test would count
SHARE_SKIP = ("mhlw", "notify")


def _addr(s):
    """An address as the cut reads it: NFKC, no spaces, 東京都 off the front,
    however often it is written (Chōfu's notification 「東京都東京都調布市野水
    1丁目」, 2026-10-07; permits_from_rows already reads it so)."""
    a = unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", "")
    while a.startswith("東京都"):
        a = a[3:]
    return a


def city_rows(path, key, municipality):
    """One source's rows for one Tama city: the file read by
    japan_register.city_rows, the call-109 columns dropped, and only the rows
    whose address begins with the municipality (after 東京都). Raises on a row
    naming the municipality anywhere else in its address (Tsu's rule, Itami's
    brief): such a row would be lost silently. Rows with no address are no
    city's (the permit ledger's 251)."""
    from pipeline.countries import japan_register as jr
    col = ADDRESS_COLUMN[key]
    drop = DROP_COLUMNS + (MHLW_DROP if key == "mhlw" else ())
    out, elsewhere = [], []
    for r in jr.city_rows(path):
        a = _addr(r.get(col))
        if a.startswith(municipality):
            out.append({k: v for k, v in r.items() if k not in drop})
        # An area naming several municipalities is no city's premises: skipped,
        # not raised (Tama's notification 「稲城市周辺、多摩市周辺、日野市周辺」
        # and MHLW's 「稲城市、及び、日野市、多摩市内一円」, 2026-10-07), by the
        # words step 2 reads as area-wide (japan_register.AREA_WORDS, 一円, 市内)
        elif municipality in a and not (jr.AREA_WORDS.search(a) or "一円" in a or "市内" in a):
            elsewhere.append(a)
    if elsewhere:
        raise ValueError(f"{path.name}: {len(elsewhere)} address(es) name {municipality} after another place "
                         f"(the cut would drop them): {elsewhere[:3]}")
    return out


def catalogue_credit(used):
    """The ledgers' credit in the Tokyo Open Data Terms' modified-use form
    (§2(1)イ; owner, call 108): each catalogue title, 東京都, the CC BY 4.0
    link, that it was modified; the entries linked, never the 保健医療局 page.
    `used`: the date of use, as Tokyo's notice gives it."""
    cc = "[https://creativecommons.org/licenses/by/4.0/deed.ja](https://creativecommons.org/licenses/by/4.0/deed.ja)"
    return ("この地図は、以下の著作物を改変して利用しています。"
            f"食品関係営業台帳（[{CATALOGUE_FOOD}]({CATALOGUE_FOOD})）及び環境衛生施設台帳"
            f"（[{CATALOGUE_REGISTERS}]({CATALOGUE_REGISTERS})）、東京都、クリエイティブ・コモンズ・ライセンス 表示4.0国際"
            f"（{cc}）（{CATALOGUE}、{used}利用）")
