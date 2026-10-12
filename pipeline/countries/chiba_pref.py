"""Chiba Prefecture's shared business leg: the prefecture's open-data lists of
barbers, beauty salons and laundries (【千葉県】環境衛生関係施設一覧, dataset 6 on
opendata.pref.chiba.lg.jp, 衛生指導課) for the municipalities its health centers
serve (every city and town but Chiba, Funabashi and Kashiwa, each a
health-center city the lists leave out), each page cut out of them by its
health center's sheet and its address.

One module for the six Chiba pages of East-2 (2026-10-11): Matsudo (sheet
松戸), Ichikawa and Urayasu (市川), Sakura (印旛), Yachiyo (習志野) and Ichihara
(市原). Each page's config reads SOURCE_FILES, SOURCES, SOURCE_AS_OF,
REGISTERS_AS_OF, REQUIRED_COLUMNS, SOURCE_ENCODING and city_rows() from here
and adds only what is its own: its municipality (japan.CITIES), its sheet
(HEALTH_CENTER), the row counts its brief measured (asserted through
city_rows' `expect`, never hard-coded here), its ISJ pair and its rail.
Personal services only: the prefecture's food set is old-law only, so no
Chiba page carries a food layer from here.

  * Three base workbooks, one per kind, ONE SHEET PER HEALTH CENTER (13), the
    header in row 1: barbers (resource 79), beauty salons (80), laundries (81).
  * THE BARBER LIST IS AS OF 2025-03-31, built as published with its own date
    (owner, call 33): the catalogue titles resource 79 令和8年3月末時点 but
    serves ichiran-riyou202503.xlsx (328,249 B against the catalogue's
    378,797), saved 2025-04-23, its newest 検査確認日 in any sheet 2025-03-07
    (Matsudo's brief, 2026-10-05). Barbers get no months.
  * BEAUTY AND LAUNDRY ARE REBUILT TO 2026-08-31 (owner, call 34): the
    2026-03-31 lists plus the monthly 新規施設 workbooks of 2026-04 to 2026-08
    (resources 103-99 and 115-111), the base lists' layout. An UPPER BOUND:
    openings are added, closures are not published (Kochi's and Kyoto's
    disclosure). A month's row whose 検査確認番号 and address a row already
    read carries is the same confirmation and is dropped (Sakura: the April
    beauty file repeats a row of the base list, saved 2026-04-27 with
    confirmations to 2026-04-06). A month's row at a listed address and trade
    name under a NEW number is kept (Matsudo: one in July); step 2's one pin
    per premises shows it once.
  * Ichikawa's laundry share goes on its page (owner, call 32); the same words
    for another page are a review-time proposal, never written from here.
  * Only applicants who agreed to open publication are listed (the dataset's
    note, 「申請者にオープンデータ掲載に賛同いただいているものに限定して掲載」): each
    page discloses it as a coverage reason, with no number.

The traps, each raised or handled where the next page passes:

  * A page's rows are its sheet's rows whose 施設所在地１ starts at its
    municipality, never an address filter alone and never a sum of sheets: the
    beauty workbook's 海匝 sheet is an exact copy of 印旛 (1,087 rows), so an
    address filter across the workbook counts Sakura's salons twice (Sakura).
  * The header is read by NAME and brought to one spelling (HEADER_ALIASES):
    the 市原 barber sheet writes 施設名称1 and 施設所在地1 with a half-width
    digit, which japan_register.xlsx_rows passes over without an error, 0 of
    218 rows (Ichihara); the 習志野 beauty months of 2026-05 to 07 and the 市原
    month of 2026-08 write 施設名称 with no digit (Yachiyo, Ichihara); the 印旛
    barber sheet has its own column order and a 開設者種別 column (Sakura); the
    May beauty month's 印旛 sheet adds 開設者役職名 and 開設者代表者名 (Sakura);
    two base sheets end in a column with no header (Yachiyo). A header cell
    this module does not know stops the read.
  * A month with nothing new for a health center is a sheet holding one title
    cell (「5月新規なし」) and no header: no rows. Any other sheet without a
    header stops the read.
  * The laundry kind is in クリーニング種別１ (取次所, 洗い+仕上場, 仕上場, 洗い場,
    無店舗取次店), 業務種別 reading クリーニング所 on every row.
    japan_register.TYPE_COLS_FIRST5 reads it ahead of 業務種別 for every city
    after the Japan foundation, so a 無店舗取次店 (no shop: not a premises)
    never reaches the map (Matsudo 2 of 186, Yachiyo 7 of 77).
  * A few laundry rows name no municipality (the 市川 sheet 5, the 習志野 sheet
    1): they belong to no page by the cut, and city_rows counts them
    (Ichikawa, Yachiyo).
  * 検査確認日 is in the era-letter dot form (R07.01.30); nothing reads it but
    the report's newest date. A 生活衛生 confirmation has no term, so no
    TERM_AS_OF applies.

Licence: every resource declares `pdl`, and the catalogue's terms page
(opendata.pref.chiba.lg.jp/pages/terms) applies 公共データ利用規約（第1.0版）
(PDL 1.0). Cite and fetch from opendata.pref.chiba.lg.jp only, never a
pref.chiba.lg.jp page. The credit is the catalogue's 加工 form (CREDIT).

Never kept: 施設電話番号, 開設者役職名, 開設者種別, the building line
(施設所在地２), the name's second line (施設名称２) and クリーニング種別２: only
KEEP's columns leave the reader. The operator columns (開設者名, 営業者名,
開設者代表者名) are kept for the name rule only, read IN MEMORY
(japan_register.OPERATOR_COLS) and never written. The lists carry no operator
address.

No reads of data/ at import: the deployed app imports each city's config, and
through it this module. The download is `fetch()`, fenced for
scripts/check_no_fetch_in_steps.py; only a city's fetch_sources.py calls it.
"""
import functools
import io
import re
import unicodedata
from pathlib import Path

PREFECTURE = "千葉県"
RAW_DIR = Path(__file__).parent.parent.parent / "data" / "chiba_pref" / "raw"

HOST = "https://opendata.pref.chiba.lg.jp"
DATASET_PAGE = HOST + "/datasets/6"
DATASET_TITLE = "【千葉県】環境衛生関係施設一覧"
# The catalogue's own API form (/api/3/ and /ckan_api/action/ answer 404)
PACKAGE_SHOW = HOST + "/ckan_api/package_show?id=6"
TERMS_PAGE = HOST + "/pages/terms"
LICENCE = "公共データ利用規約（第1.0版） (PDL 1.0)"
# The terms page's 加工 form, naming the dataset (Matsudo's brief; the notice
# adds who processed it)
CREDIT = f"出典：「{DATASET_TITLE}」（千葉県オープンデータサイト）（{DATASET_PAGE}）を加工して作成"
_DOWNLOAD = HOST + "/resource_download/{}"

# The base lists: kind -> (file as the publisher serves it, resource id, the
# date the list is as of). The barber file's name and date are the 2025 list's
# (call 33); a replaced resource 79 is a new file under a new name.
LISTS = {"barber": ("ichiran-riyou202503.xlsx", 79, "2025-03-31"),
         "beauty": ("ichiran-biyou202603.xlsx", 80, "2026-03-31"),
         "laundry": ("ichiran-clean202603.xlsx", 81, "2026-03-31")}
# The approved months (call 34): kind -> ((month, file, resource id, the
# month's last day), ...), oldest first. The August beauty file's -2 is the
# publisher's, a second upload (Last-Modified 2026-09-29).
MONTHS = {
    "barber": (),
    "beauty": (("2604", "shinki-biyou2604.xlsx", 103, "2026-04-30"), ("2605", "shinki-biyou2605.xlsx", 102, "2026-05-31"),
               ("2606", "shinki-biyou2606.xlsx", 101, "2026-06-30"), ("2607", "shinki-biyou2607.xlsx", 100, "2026-07-31"),
               ("2608", "shinki-biyou2608-2.xlsx", 99, "2026-08-31")),
    "laundry": (("2604", "shinki-clean2604.xlsx", 115, "2026-04-30"), ("2605", "shinki-clean2605.xlsx", 114, "2026-05-31"),
                ("2606", "shinki-clean2606.xlsx", 113, "2026-06-30"), ("2607", "shinki-clean2607.xlsx", 112, "2026-07-31"),
                ("2608", "shinki-clean2608.xlsx", 111, "2026-08-31")),
}

# file key -> (file in RAW_DIR, URL, dataset page): "<kind>_list" and
# "<kind>_<month>". An edition is a new file under a new name (the shared
# data/ folder's rule), never an overwrite.
SOURCE_FILES = {
    **{f"{k}_list": (name, _DOWNLOAD.format(rid), DATASET_PAGE) for k, (name, rid, _) in LISTS.items()},
    **{f"{k}_{m}": (name, _DOWNLOAD.format(rid), DATASET_PAGE) for k, ms in MONTHS.items() for m, name, rid, _ in ms},
}
FILE_KIND = {key: key.split("_", 1)[0] for key in SOURCE_FILES}
# Each FILE's own date (the provenance records it)
FILE_AS_OF = {**{f"{k}_list": d for k, (_, _, d) in LISTS.items()},
              **{f"{k}_{m}": d for k, ms in MONTHS.items() for m, _, _, d in ms}}

# --- step 2's sources ------------------------------------------------------------
# key -> the file that names it (japan_step2 reads every one through a config's
# source_rows, and through it city_rows): each register its base list, with
# the months where it has them
SOURCES = {k: name for k, (name, _, _) in LISTS.items()}
SOURCE_KIND = {}
# Each register's date as the page states it: the barber list's own (call 33);
# beauty and laundry the last day of the newest month read, an upper bound
# (call 34). Never the download's. The file keys carry each file's own date.
SOURCE_AS_OF = {"barber": LISTS["barber"][2], "beauty": MONTHS["beauty"][-1][3], "laundry": MONTHS["laundry"][-1][3],
                **FILE_AS_OF}
REGISTERS_AS_OF = MONTHS["beauty"][-1][3]
# Declared, never inferred
SOURCE_ENCODING = {key: "xlsx" for key in (*SOURCES, *SOURCE_FILES)}

# One spelling for every sheet's header (the docstring's traps). The last three
# are the 海匝 laundry sheet's (銚子市, 旭市, 匝瑳市: no page reads it; aliased
# so file_rows counts the workbook whole).
HEADER_ALIASES = {"施設名称": "施設名称１", "施設名称1": "施設名称１", "施設名称2": "施設名称２",
                  "施設所在地1": "施設所在地１", "施設所在地2": "施設所在地２",
                  "申請者氏名": "営業者名", "施設所在地": "施設所在地１", "種別１": "クリーニング種別１"}
KNOWN_HEADERS = frozenset({"開設者名", "営業者名", "開設者種別", "開設者役職名", "開設者代表者名", "施設名称１", "施設名称２",
                           "施設所在地１", "施設所在地２", "施設電話番号", "業務種別", "クリーニング種別１", "クリーニング種別２",
                           "検査確認番号", "検査確認日"})
NAME, ADDRESS, NUMBER, CONFIRMED, LAUNDRY_KIND = "施設名称１", "施設所在地１", "検査確認番号", "検査確認日", "クリーニング種別１"
# The only columns that leave the reader (the docstring's "Never kept")
KEEP = ("開設者名", "営業者名", "開設者代表者名", NAME, ADDRESS, "業務種別", LAUNDRY_KIND, NUMBER, CONFIRMED)
# The columns every sheet of a kind must carry, and step 2's sources with them.
# The operator column is REQUIRED so the name rule cannot compare nothing.
_SALON = (NAME, ADDRESS, "業務種別", "開設者名")
REQUIRED_COLUMNS = {"barber": _SALON, "beauty": _SALON, "laundry": (NAME, ADDRESS, "業務種別", "営業者名", LAUNDRY_KIND)}
REQUIRED_COLUMNS.update({key: REQUIRED_COLUMNS[kind] for key, kind in FILE_KIND.items()})
NOT_A_PREMISES = "無店舗"  # 無店舗取次店, a pick-up service with no shop

# Each health center's area as the lists' addresses start (the six briefs,
# 2026-10-05 and 06): the sheets the six pages read. A row of a sheet starting
# at none of its area's names is counted by city_rows as naming no municipality.
SHEET_AREAS = {
    "松戸": ("松戸市", "流山市", "我孫子市"),
    "市川": ("市川市", "浦安市"),
    "印旛": ("佐倉市", "成田市", "四街道市", "八街市", "印西市", "白井市", "富里市", "印旛郡酒々井町", "印旛郡栄町"),
    "習志野": ("習志野市", "八千代市", "鎌ケ谷市"),
    "市原": ("市原市",),
}
NOTHING_NEW = "新規なし"


def source_path(key, raw_dir=RAW_DIR):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return Path(raw_dir) / (SOURCE_FILES[key][0] if key in SOURCE_FILES else SOURCES[key])


def _key(s):
    """An address as the cut and the keys compare it: NFKC, no spaces, one
    dash, ヶ as ケ (鎌ケ谷市 is written both ways)."""
    s = unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", "").replace("ヶ", "ケ")
    return re.sub(r"[‐‑‒–—―−ｰー－]", "-", s)


@functools.lru_cache(maxsize=16)
def _workbook(path):
    """A workbook's sheets, {title without spaces: its non-empty rows as cleaned
    cells (japan_register._head, as xlsx_rows cleans them)}."""
    import openpyxl
    from pipeline.countries import japan_register as jr
    wb = openpyxl.load_workbook(io.BytesIO(Path(path).read_bytes()), read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = (tuple(jr._head(c) for c in r) for r in ws.iter_rows(values_only=True))
        out[ws.title.replace(" ", "").replace("　", "")] = tuple(r for r in rows if any(r))
    return out


def sheet_names(key, raw_dir=RAW_DIR):
    """The health-center sheets of one file."""
    return tuple(_workbook(str(source_path(key, raw_dir))))


def sheet_rows(key, sheet, raw_dir=RAW_DIR):
    """One health center's sheet of one FILE (a file key), as rows keyed by the
    one header spelling, KEEP's columns only. A sheet holding only a
    「…新規なし」 title cell has no rows. Raises on a missing sheet, a header
    cell this module does not know, a sheet without its kind's required
    columns, or rows under no header: never a silent skip."""
    path = source_path(key, raw_dir)
    where = f"{path.name} [{sheet}]"
    book = _workbook(str(path))
    if sheet not in book:
        raise ValueError(f"{path.name}: no sheet {sheet!r} (it has {list(book)})")
    rows = book[sheet]
    if not rows:
        raise ValueError(f"{where}: an empty sheet, with neither a header nor a {NOTHING_NEW!r} title")
    cells = [c for c in rows[0] if c]
    if len(cells) == 1 and NOTHING_NEW in unicodedata.normalize("NFKC", cells[0]):
        if len(rows) > 1:
            raise ValueError(f"{where}: {len(rows) - 1} row(s) under a {NOTHING_NEW!r} title and no header")
        return []
    head = [HEADER_ALIASES.get(c, c) for c in rows[0]]
    unknown = sorted(c for c in head if c and c not in KNOWN_HEADERS)
    if unknown:
        raise ValueError(f"{where}: header cell(s) {unknown} this module does not know. Read the sheet, then add "
                         f"each to HEADER_ALIASES or KNOWN_HEADERS.")
    missing = [c for c in REQUIRED_COLUMNS[FILE_KIND[key]] if c not in head]
    if missing:
        raise ValueError(f"{where}: header lacks {missing} (it reads {[c for c in head if c]})")
    if len(set(c for c in head if c)) != len([c for c in head if c]):
        raise ValueError(f"{where}: two columns read as one name ({[c for c in head if c]})")
    return [{h: c for h, c in zip(head, r) if h in KEEP} for r in rows[1:]]


def register_rows(kind, sheet, raw_dir=RAW_DIR):
    """A register of one health center's area: the base list's sheet, then each
    approved month's new premises in order. A month's row whose (検査確認番号,
    address) a row already read carries is dropped (the module docstring).
    Returns (rows, rows from the base list, rows added by the months, month
    rows already listed)."""
    rows = sheet_rows(f"{kind}_list", sheet, raw_dir)
    seen = {(r.get(NUMBER), _key(r[ADDRESS])) for r in rows if r.get(NUMBER)}
    n_list, added, repeat = len(rows), 0, 0
    for m, _, _, _ in MONTHS[kind]:
        for r in sheet_rows(f"{kind}_{m}", sheet, raw_dir):
            k = (r.get(NUMBER), _key(r[ADDRESS]))
            if k[0] and k in seen:
                repeat += 1
                continue
            seen.add(k)
            rows.append(r)
            added += 1
    return rows, n_list, added, repeat


def cut(rows, municipality, sheet, label):
    """The rows whose address starts at the page's municipality, as MLIT's
    市区町村名 and the lists write it (松戸市…, no prefecture), and the count of
    the sheet's rows that start at none of its area's municipalities. Raises
    on an address naming the municipality after another place (a row the cut
    would drop silently; Saitama's rule)."""
    if sheet not in SHEET_AREAS:
        raise KeyError(f"sheet {sheet!r} has no area in chiba_pref.SHEET_AREAS: read the sheet's addresses and add it")
    area = tuple(_key(m) for m in SHEET_AREAS[sheet])
    name = _key(municipality)
    if name not in area:
        raise ValueError(f"{municipality} is not in the {sheet} sheet's area {SHEET_AREAS[sheet]}")
    out, elsewhere, nowhere = [], 0, 0
    for r in rows:
        a = _key(r.get(ADDRESS))
        if a.startswith(PREFECTURE):
            a = a[len(PREFECTURE):]
        if a.startswith(name):
            out.append(r)
        elif name in a:
            elsewhere += 1
        elif not a.startswith(area):
            nowhere += 1
    if elsewhere:
        raise ValueError(f"{label}: {elsewhere} address(es) name {municipality} after another place (the cut would "
                         f"drop them); read them")
    return out, nowhere


def _newest(rows):
    from pipeline.countries import japan_register as jr
    dates = [d for d in (jr.wareki_date(r.get(CONFIRMED)) for r in rows) if d]
    return max(dates).isoformat() if dates else "none read"


def city_rows(key, municipality, sheet, raw_dir=RAW_DIR, expect=None, report=print):
    """One step-2 source's rows for one page ("barber", "beauty", "laundry"):
    its health center's sheet of the base list plus the approved months
    (register_rows), cut to the page's municipality by address (cut). `expect`
    is the row count the page's brief measured on these files: a different
    count stops the read, so a new edition cannot pass silently. Prints
    counts only."""
    if key not in SOURCES:
        raise KeyError(key)
    rows, n_list, added, repeat = register_rows(key, sheet, raw_dir)
    mine, nowhere = cut(rows, municipality, sheet, f"{key} register [{sheet}]")
    base, _ = cut(rows[:n_list], municipality, sheet, f"{key} list [{sheet}]")
    storeless = sum(1 for r in mine if NOT_A_PREMISES in (r.get(LAUNDRY_KIND) or ""))
    months = f"and the months to {MONTHS[key][-1][3]}" if MONTHS[key] else "(no months, call 33)"
    report(f"  {key}: the {LISTS[key][2]} list {months}, sheet {sheet}: {len(mine):,} here "
           f"({len(base):,} listed + {len(mine) - len(base):,} from the months; sheet-wide {n_list:,} + {added:,}, "
           f"{repeat:,} month row(s) already listed, {nowhere:,} naming no municipality)"
           + (f"; {storeless:,} {NOT_A_PREMISES}取次店 (not premises)" if key == "laundry" else "")
           + f"; newest {CONFIRMED} here {_newest(mine)}")
    if expect is not None and len(mine) != expect:
        raise ValueError(f"{key}: {len(mine):,} rows for {municipality} in sheet {sheet}, where the brief measured "
                         f"{expect:,}: a new edition of {SOURCES[key]} or of a month? Re-measure, then correct the "
                         f"brief and the config's count.")
    return mine


def file_rows(key, raw_dir=RAW_DIR):
    """One FILE's rows as it stands, every sheet (fetch_sources.py's count and
    column check). The beauty list's count holds its 海匝 sheet, a copy of
    印旛: a file's count, never a count of salons."""
    return [r for sheet in sheet_names(key, raw_dir) for r in sheet_rows(key, sheet, raw_dir)]


def fetch(config, force=False):
    """Download every Chiba file a page reads into RAW_DIR, recorded in the
    page's provenance (japan_fetch.record). Plain GETs from
    opendata.pref.chiba.lg.jp, a few seconds apart; a file on disk is never
    overwritten, even with --force, since an edition is a new file under a
    new name (LISTS, MONTHS). Fenced: only a city's fetch_sources.py calls
    it."""
    import time

    from pipeline.countries import japan_fetch
    for key, (name, url, page) in SOURCE_FILES.items():
        dest = Path(RAW_DIR) / name
        had = dest.exists()
        how = japan_fetch.get(url, dest, False)
        if not had:
            time.sleep(5)
        rows = file_rows(key)
        print(f"  {dest.name:28s} {dest.stat().st_size:>10,} bytes {len(rows):>7,} rows  ({how})")
        japan_fetch.record(config, f"city_{key}", file=f"data/chiba_pref/raw/{name}", url=url, dataset_page=page,
                           bytes=dest.stat().st_size, sha256=japan_fetch.sha256(dest), rows=len(rows),
                           as_of=FILE_AS_OF[key], retrieved=japan_fetch.when(dest), how=how)
