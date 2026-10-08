"""Fukuyama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/fukuyama.md (15/15 checks, 2026-10-07). Japan's A/B batch
(Regional-1), on the shared modules (pipeline/countries/japan*.py) with the
Japan foundation's rules on (2026-10-07): Higashiosaka's and Sakai's rebuilt
food register, Matsuyama's MHLW beside a complete city list.

Business leg: the city's own 生活衛生課 lists on its CKAN catalogue (CC BY,
PDL 1.0 by the catalogue's terms). The food list of permits in term on
2026-03-31 plus the monthly new (and, from June, renewed) permits to
2026-08-31, REBUILT into one register (latest permit per address, trade name
and type, kept while in term on the pinned 2026-08-31), then a new-law permit
MHLW's live file no longer holds is dropped as closed (owner, 2026-10-05,
call 6). MHLW's 食品衛生申請等システム open data adds, as in Matsuyama (owner,
2026-10-05, call 5): its own point where the block join misses, matched by
permit number; its notifications as a partial food-retail bucket; and its
open permits in no city file. Personal services: the city's barber, beauty
and laundry registers as of 2026-08-31. All placed by a JOIN to MLIT's
位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR West's Sanyo and Fukuen lines and the Ibara Railway's Ibara Line.
English station names from OpenStreetMap's name:en.
"""

import datetime
import re
import unicodedata
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fukuyama" / "raw"
DATA_PROCESSED = ROOT / "data" / "fukuyama" / "processed"
OUTPUTS = ROOT / "outputs" / "fukuyama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fukuyama"
SLUG = "fukuyama"
MUNICIPALITY = "福山市"
PREFECTURE = "広島県"

# The city's CKAN catalogue (organisation 生活衛生課). Both datasets declare
# license_id cc-by; the catalogue's /terms apply PDL 1.0 unless a rights
# notice says otherwise, and PDL 1.0 1.7 allows use under CC BY 4.0 (read
# 2026-10-04 by staging; either reading permits the map).
PORTAL = "https://data.city.fukuyama.hiroshima.jp"
FOOD_PAGE = PORTAL + "/dataset/licensed_food"
ENV_PAGE = PORTAL + "/dataset/licensed_env"
_FOOD_DS = PORTAL + "/dataset/61f415c5-88f7-46d0-8ada-4bb8855685a0/resource/"
_ENV_DS = PORTAL + "/dataset/f6242af5-08f2-458b-a55c-452db7a8c967/resource/"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms 2;
# read 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"

# The food files: the full list of permits in term on 2026-03-31 (yearly),
# then each month's file. The seven months before the full list's date
# (2025-09 to 2026-03) are already in it (693 of their 698 numbers, the
# brief) and are read for their permit numbers only, to tell which MHLW
# permit is in no city file. The five since (2026-04 to 2026-08) are rebuilt
# into the register. (month key, file, resource id), oldest first.
_PRE = (("2509", "20259.csv", "7ec5a4c1-4c5d-4c9a-a976-9ff41ce6e919"),
        ("2510", "202510.csv", "547985da-7565-4f15-ad52-fe07a9db4b62"),
        ("2511", "202511.csv", "e3b35a8d-ef0a-4a4d-a050-d293b1e965db"),
        ("2512", "2025_12_new.csv", "14247a4a-91f2-4c85-9bfb-13c21b381825"),
        ("2601", "2026_1_new.csv", "4d31b250-ec7b-4bfc-afdc-37236846101d"),
        ("2602", "2026_2_new.csv", "36e57b96-9fdd-4ec3-a178-9bd3cd7620b8"),
        ("2603", "2026_3_new.csv", "f066081c-ff12-4b0b-95e4-a4b5e54463ac"))
_POST = (("2604", "20264.csv", "d9030cb6-a843-42e0-8478-30dc47561336"),
         ("2605", "20265.csv", "d5116587-457d-42dc-902e-7ce931057610"),
         ("2606", "20266.csv", "8c3eff46-6aa3-4484-acaa-f3901f38f340"),
         ("2607", "20267.csv", "1d18f967-dcda-4e47-8d45-66dc9432091e"),
         ("2608", "20268.csv", "b0a4c098-d6b3-4a19-b5aa-adee03efd7bc"))
PRE_KEYS = tuple(f"food_{m}" for m, _, _ in _PRE)
POST_KEYS = tuple(f"food_{m}" for m, _, _ in _POST)
_MONTH_END = {"2509": "2025-09-30", "2510": "2025-10-31", "2511": "2025-11-30", "2512": "2025-12-31",
              "2601": "2026-01-31", "2602": "2026-02-28", "2603": "2026-03-31", "2604": "2026-04-30",
              "2605": "2026-05-31", "2606": "2026-06-30", "2607": "2026-07-31", "2608": "2026-08-31"}
# source key -> (file, URL of the edition this build read, the page that
# carries its licence).
SOURCE_FILES = {
    "food": ("2026_3all.csv", _FOOD_DS + "21fec913-dc08-4344-94d1-ffb0068ab147/download/2026_3all.csv", FOOD_PAGE),
    **{f"food_{m}": (name, f"{_FOOD_DS}{rid}/download/{name}", FOOD_PAGE) for m, name, rid in _PRE + _POST},
    "barber_beauty": ("riyoushobiyousho.csv",
                      _ENV_DS + "2d640e17-3225-4c59-b2f4-cdc2b104748c/download/riyoushobiyousho.csv", ENV_PAGE),
    "laundry": ("kuri-ninngu.csv", _ENV_DS + "bd8b8871-e656-4450-ac0b-92614eeedb3f/download/kuri-ninngu.csv",
                ENV_PAGE),
    "mhlw": ("34207_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34207_food_business_all.csv",
             MHLW_TOP),
}
# The rebuilt register's date, PINNED (Kyoto's rule: the last day the newest
# file covers, never the download date or today): the August file.
AS_OF = datetime.date(2026, 8, 31)
# Kyoto's rule: the date each list states. The full list 2026年3月末時点, each
# month file the month it names, the registers 2026年8月末時点 (the dataset's
# notes); MHLW's monthly file states none (permits to 2026-08-31).
SOURCE_AS_OF = {"food": "2026-03-31", **{f"food_{m}": d for m, d in _MONTH_END.items()},
                "barber_beauty": "2026-08-31", "laundry": "2026-08-31", "mhlw": None}
FOOD_AS_OF = AS_OF.isoformat()
REGISTERS_AS_OF = "2026-08-31"
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today: the rebuilt register's and
# MHLW's 2026-08-31.
TERM_AS_OF = {"food": "2026-08-31", "mhlw": "2026-08-31"}

# What step 2 reads: the rebuilt register (source_rows("food")), MHLW's rows
# that add to it, and the three registers. The barber and beauty registers
# are one file, split by its 種類 column.
SOURCES = {"food": SOURCE_FILES["food"][0], "mhlw": SOURCE_FILES["mhlw"][0],
           "barber": SOURCE_FILES["barber_beauty"][0], "beauty": SOURCE_FILES["barber_beauty"][0],
           "laundry": SOURCE_FILES["laundry"][0]}
# Declared, never inferred: every city file is UTF-8 with a BOM, as is MHLW's.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCE_FILES}

# The food files' two schemas (the brief): the full list and the 2026-03 to
# 2026-05 files, and the June to August files (and the 2025-09 to 2026-02
# ones). The operator columns (申請者＿申請者名, an individual's own name on
# 2,902 of the full list's 5,880 rows; 申請者＿代表者) are REQUIRED so the name
# rule (japan_register.name_is_operator; owner 2026-09-27) cannot silently
# compare nothing; read IN MEMORY by that rule only, never kept. Never
# selected: 申請者＿住所１ / ２ and 申請者＿郵便番号 (the operator's own address),
# 申請者＿役職名.
_SCHEMA_A = ("施設＿名称（屋号・商号）１", "所在地１", "業種", "業態", "形態", "施設番号", "許可開始日", "許可終了日",
             "許可年月日", "申請者＿申請者名", "申請者＿代表者")
_SCHEMA_B = ("営業所名称１", "営業所所在地１", "営業の種類", "業態", "形態", "許可番号", "許可開始日", "許可満了日",
             "許可年月日", "申請者＿申請者名", "申請者＿代表者")
_SCHEMA = {"food": _SCHEMA_A, "food_2603": _SCHEMA_A, "food_2604": _SCHEMA_A, "food_2605": _SCHEMA_A}
# The columns each source must carry; fetch_sources.py and step 2 stop on a
# header without them. The rebuilt register's records carry the full list's
# premises spellings (rebuilt_food), so "food" names the columns both carry.
# The registers' 営業者 is the operator (read IN MEMORY by the name rule); their
# 営業者住所 (the operator's own address, filled on 287 and 132 rows) is never
# selected. MHLW's 法人名 holds a sole trader's own name as often as a
# company's (owner, 2026-10-05): REQUIRED, read in memory only; 法人番号,
# 法人住所 and the phones are never selected.
REQUIRED_COLUMNS = {
    "food": ("施設＿名称（屋号・商号）１", "所在地１", "業種", "業態", "形態", "施設番号", "許可開始日", "許可終了日"),
    **{k: _SCHEMA.get(k, _SCHEMA_B) for k in PRE_KEYS + POST_KEYS},
    "barber_beauty": ("種類", "店名", "所在地", "営業者"),
    "barber": ("種類", "店名", "所在地", "営業者"),
    "beauty": ("種類", "店名", "所在地", "営業者"),
    "laundry": ("種類", "店名", "所在地", "営業者"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名", "許可番号", "許可満了日"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses a row, MHLW's own point places it (owner,
# 2026-10-05, call 5a, by permit number): MHLW's rows carry it, and a rebuilt
# city row carries the point MHLW files under the same permit number
# (rebuilt_food). The brief: a median 38 m from the block point, 96.2% within
# 250 m; block or MHLW's point 90.1% to 95.9%.
OWN_POINT_FALLBACK = {"food", "mhlw"}
# One premises in both: the city's row goes, MHLW's stays (Matsuyama's and
# Sakai's precedent). MHLW's open permits in no city file are mostly 2026-06
# to 08 renewals the city's months do not list, 37 of 44 at an (address,
# trade name) the city lists under its older number (the brief).
SUPERSEDES = {"mhlw": ("food",)}

# MHLW's file starts on 2021-06-01, when the revised Food Sanitation Act's
# permits began: a permit starting on or after it is NEW-LAW, and MHLW holds
# every one the city grants (5,240 of MHLW's 5,284 permit numbers are in the
# city's files, the brief). An old-law permit cannot be checked.
NEW_LAW = datetime.date(2021, 6, 1)
REST = "飲食店営業"


def source_csv(key):
    if key in ("barber", "beauty"):
        key = "barber_beauty"
    return DATA_RAW / SOURCE_FILES[key][0]


def _rows(key):
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    return list(jr.city_rows(path))


def permit_number(s):
    """A permit number's digits: the city writes 第191504号, MHLW
    福山市指令保生第191504号 (and a few typed 第号191504号, 保正, a trailing space)."""
    m = re.findall(r"\d+", unicodedata.normalize("NFKC", s or ""))
    return m[-1] if m else ""


def _first(r, *cols):
    return next(((r.get(c) or "").strip() for c in cols if (r.get(c) or "").strip()), "")


def _mhlw_open():
    """MHLW's permits still open (no 廃業年月日), by permit number, each with its
    own point where it has one."""
    out = {}
    for r in _rows("mhlw"):
        n = permit_number(r.get("許可番号"))
        if n and not (r.get("廃業年月日") or "").strip():
            out[n] = (_first(r, "緯度"), _first(r, "経度"))
    return out


def city_numbers():
    """Every permit number in the city's thirteen food files."""
    out = set()
    for key in ("food",) + PRE_KEYS + POST_KEYS:
        out |= {permit_number(_first(r, "施設番号", "許可番号")) for r in _rows(key)}
    out.discard("")
    return out


def premises_key(addr, name, typ):
    """(address, trade name, type) as both publishers can be compared: the
    prefecture cut (MHLW writes 広島県福山市, the city 福山市) and MHLW's
    circled-numeral type prefix (① 飲食店営業) dropped."""
    from pipeline.countries import japan_register as jr

    a = re.sub(r"[‐‑‒–—―−ｰー－]", "-", unicodedata.normalize("NFKC", addr or "").replace(" ", "").replace("　", ""))
    t = re.sub(r"^\S+\s", "", (typ or "").strip())
    return re.sub("^" + PREFECTURE, "", a), jr._name_key(name), unicodedata.normalize("NFKC", t)


def _mhlw_renewals(city):
    """MHLW's open permits in no city file, by premises_key, each with its
    point: a renewal the city's monthly files do not list (the brief: 37 of
    MHLW's 44 such permits sit at a premises the city lists under its older
    number)."""
    out = {}
    for r in _rows("mhlw"):
        n = permit_number(r.get("許可番号"))
        if (n and n not in city and (r.get("申請区分") or "").strip() == "許可"
                and not (r.get("廃業年月日") or "").strip()):
            out[premises_key(r.get("営業施設所在地"), r.get("営業施設名称、屋号又は商号"), r.get("営業の種類"))] = (
                _first(r, "緯度"), _first(r, "経度"))
    return out


def rebuilt_food():
    """The city's food permits in term on AS_OF, Higashiosaka's rebuild
    (japan_register.rebuilt_register) with the permit number kept, then the
    closure filter. The full list of 2026-03-31 and the five months since,
    oldest first: where (address, trade name, type without （旧）) repeats, the
    permit ending latest wins (a renewal arrives under a NEW number); kept
    while its expiry (許可終了日, or 許可満了日 in the June to August files) is on
    or after AS_OF. A renewal that starts after AS_OF waits (call 172), and
    the permit it replaces stands for the premises. Then a NEW-LAW permit
    whose number MHLW's live file does not hold (nor its waiting renewal's)
    is dropped as closed (owner, 2026-10-05, call 6): MHLW keeps a closed
    permit only in its closure month. A permit MHLW renewed for the same
    premises and type under a number no city file lists is not a closure.
    Old-law permits stay unchecked.

    The rebuild is city-local because the shared one returns no permit
    number (the closure filter and MHLW's point both key on it) and keeps one
    form column only (業態 before 形態); a check below stops the build if its
    register ever differs from the shared one's. Measured 2026-10-07: 5,738
    in term, 4,238 restaurants (the brief exactly); 5,736 in force, 17 with a
    waiting renewal; 151 closure candidates (the brief), 6 of them renewed in
    MHLW's file alone, 145 closed (109 restaurants); 5,591 kept. Re-measure
    if a month file is added. Each record carries premises columns, the dates, MHLW's
    point under the same number, and the name rule's ANSWER, compared here
    while the operator columns are in hand; never the operator's name."""
    import sys

    from pipeline.baseline import emit
    from pipeline.countries import japan_register as jr

    rules = jr.ALL_RULES
    best, now = {}, {}
    read = 0
    for key in ("food",) + POST_KEYS:
        rows = _rows(key)
        missing = [c for c in REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            raise SystemExit(f"{SOURCE_FILES[key][0]}: header lacks {missing} - not the file the brief read")
        for r in rows:
            addr = _first(r, "所在地１", "営業所所在地１")
            name = _first(r, "施設＿名称（屋号・商号）１", "営業所名称１")
            typ = _first(r, "業種", "営業の種類")
            if not (addr or name or typ):
                continue  # the monthly files' empty lines
            read += 1
            end = jr.wareki_date(_first(r, "許可終了日", "許可満了日"))
            start = jr.wareki_date(_first(r, "許可開始日"))
            granted = jr.wareki_date(_first(r, "許可年月日"))
            # rebuilt_register's own key and rank, so the check below holds
            k = (re.sub(r"[‐‑‒–—―−ｰー－]", "-", unicodedata.normalize("NFKC", addr).replace(" ", "")
                        .replace("　", "")),
                 jr._name_key(name), re.sub(r"^\(旧\)", "", unicodedata.normalize("NFKC", typ).replace(" ", "")))
            rank = (end or datetime.date(1900, 1, 1), granted or datetime.date(1900, 1, 1))
            rec = {"所在地１": addr, "施設＿名称（屋号・商号）１": name, "業種": typ,
                   "業態": _first(r, "業態"), "形態": _first(r, "形態"),
                   "施設番号": permit_number(_first(r, "施設番号", "許可番号")),
                   "許可開始日": start.isoformat() if start else "",
                   "許可終了日": end.isoformat() if end else "",
                   "name_is_operator": jr.name_is_operator(r, rules)}
            if k not in best or rank >= best[k][0]:
                best[k] = (rank, rec)
            # A renewal that starts after AS_OF is not yet in force (call 172):
            # the permit it replaces, in term on AS_OF, stands for the premises.
            # Ranked on the latest end alone, the August file's renewals that
            # start on 2026-09-01 hid 17 premises whose permit ran to 08-31.
            if not (start and start > AS_OF) and (k not in now or rank >= now[k][0]):
                now[k] = (rank, rec)
    kept = [rec for (rank, rec) in best.values() if rank[0] >= AS_OF]
    shared = jr.rebuilt_register([source_csv(k) for k in ("food",) + POST_KEYS], AS_OF,
                                 end_col=("許可終了日", "許可満了日"), rules=rules)

    def sig(recs, a, n, t, e):
        return sorted((x[a], x[n], x[t], x[e]) for x in recs)
    if sig(kept, "所在地１", "施設＿名称（屋号・商号）１", "業種", "許可終了日") != sig(
            shared, "所在地", "施設名称", "業種", "許可終了日"):
        raise SystemExit(f"rebuilt_food ({len(kept):,}) no longer matches japan_register.rebuilt_register "
                         f"({len(shared):,}): bring its key and rank back in step")

    # The premises in force on AS_OF, each with the renewal waiting to start
    # after it where there is one (its number may be the one MHLW holds).
    in_force = [(rec, best[k][1] if best[k][1] is not rec else None)
                for k, (rank, rec) in now.items() if rank[0] >= AS_OF]
    waiting = sum(1 for _, nxt in in_force if nxt)

    live = _mhlw_open()
    renewed = _mhlw_renewals(city_numbers())

    def pkey(rec):
        return premises_key(rec["所在地１"], rec["施設＿名称（屋号・商号）１"], rec["業種"])

    def held(rec, nxt):
        return rec["施設番号"] in live or bool(nxt and nxt["施設番号"] in live)
    new_law = [(rec, nxt) for rec, nxt in in_force
               if rec["許可開始日"] and datetime.date.fromisoformat(rec["許可開始日"]) >= NEW_LAW
               and not held(rec, nxt)]
    # A permit MHLW renewed under a number no city file lists, for the same
    # premises and type, is not a closure: 7 such renewals start on
    # 2026-09-01 (call 172 makes them wait, so the permit in force on AS_OF
    # stands, as for the city's own waiting renewals); an in-force one is
    # MHLW's added row, which SUPERSEDES then shows once.
    renewal = [rec for rec, _ in new_law if pkey(rec) in renewed]
    closed = [rec for rec, _ in new_law if pkey(rec) not in renewed]
    gone = {id(x) for x in closed}
    out = []
    for rec, nxt in in_force:
        if id(rec) in gone:
            continue
        num = rec["施設番号"] if rec["施設番号"] in live else (nxt or {}).get("施設番号")
        rec["緯度"], rec["経度"] = live.get(num) or renewed.get(pkey(rec)) or ("", "")
        out.append(rec)
    rest = sum(unicodedata.normalize("NFKC", x["業種"]) == REST for x in kept)
    rest_now = sum(unicodedata.normalize("NFKC", x["業種"]) == REST for x, _ in in_force)
    rest_closed = sum(unicodedata.normalize("NFKC", x["業種"]) == REST for x in closed)
    print(f"  rebuilt register on {AS_OF}: {read:,} rows read, {len(best):,} after de-duplication, "
          f"{len(kept):,} in term ({rest:,} restaurants), as japan_register.rebuilt_register; "
          f"in force on {AS_OF} {len(in_force):,} ({rest_now:,} restaurants; {waiting:,} with a renewal "
          f"starting after it); new-law permits MHLW no longer holds {len(new_law):,}, of which renewed in "
          f"MHLW's file alone {len(renewal):,} and closed (call 6) {len(closed):,} ({rest_closed:,} "
          f"restaurants); kept {len(out):,}; carrying MHLW's point {sum(bool(x['緯度']) for x in out):,}",
          file=sys.stdout)
    emit("rebuilt_in_term", len(kept))
    emit("rebuilt_restaurants_in_term", rest)
    emit("rebuilt_in_force", len(in_force))
    emit("rebuilt_renewal_waiting", waiting)
    emit("mhlw_renewed_not_closed", len(renewal))
    emit("closed_by_mhlw_absence", len(closed))
    emit("closed_by_mhlw_absence_restaurants", rest_closed)
    return out


def mhlw_rows():
    """MHLW's rows that add to the city's lists: its notifications (届出,
    Matsuyama's partial food-retail bucket; owner call 5b) and its permits
    whose number is in no city food file (call 5c; the brief: 44 open, 34
    restaurants, mostly 2026-06 to 08 renewals). Its other permits are the
    city's own and are not read twice. Closed rows (廃業) pass through, for
    step 2 to count and drop."""
    city = city_numbers()
    for r in _rows("mhlw"):
        cls = (r.get("申請区分") or "").strip()
        if cls.startswith("届出") or (cls.startswith("許可") and permit_number(r.get("許可番号")) not in city):
            yield r


# The barber and beauty register's 種類, exactly as the file writes it.
_KIND = {"barber": "理容", "beauty": "美容"}


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    "food" the rebuilt register, "mhlw" MHLW's additions, "barber" and
    "beauty" the one register split by 種類 (a value other than 理容 or 美容
    stops the build), "laundry" its register as it stands. Every register
    keeps closed premises (the dataset's note); there is no closure field."""
    if key == "food":
        return rebuilt_food()
    if key == "mhlw":
        return mhlw_rows()
    rows = _rows(key)
    if key == "laundry":
        return rows
    other = {r["種類"] for r in rows} - set(_KIND.values())
    if other:
        raise SystemExit(f"riyoushobiyousho.csv: 種類 {sorted(other)} is neither 理容 nor 美容")
    return [r for r in rows if r["種類"] == _KIND[key]]


def file_rows(key):
    """One fetched file's rows as it stands, for fetch_sources.py's count and
    header check (japan_fetch)."""
    return _rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 34207.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Fukuyama.
# S, W, N, E: the city's N03 extent (S 34.310, W 133.211, N 34.712,
# E 133.471) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.30, 133.20, 34.72, 133.48)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word). OSM's other 17 stand, JR's own Shin-ichi among them.
OSM_NAME_EN_OVERRIDES = {
    "備後本庄": "Bingo-Honjo",                       # Bingo-Honjō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~133.36) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 1,531 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines; 福山 on the Sanyo Shinkansen dropped, the conventional
# 福山 kept). Every line is cut at the city line (owner 2026-09-24): JR's
# Fukuen Line keeps 12 of 27, its Sanyo Line 5 of 131, the Ibara Railway's
# Ibara Line 3 of 15 (a rural third-sector line, not a stub: the standing
# call draws it as cut). No frequency floor (owner, 2026-10-06, calls 46 and
# 86): JR runs at least hourly 07-19 (JR West's timetables, the brief).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons, as Okayama's and Himeji's JR Sanyo Line.
_JR, _IB = "西日本旅客鉄道", "井原鉄道"
LINES = {
    "JS": {"n02": [(_JR, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR", "hue": "#0068B7"},
    "JF": {"n02": [(_JR, "福塩線")], "name": "JR Fukuen Line", "name_ja": "福塩線", "short": "JR", "hue": "#E83820"},
    "IB": {"n02": [(_IB, "井原線")], "name": "Ibara Railway Ibara Line", "name_ja": "井原線", "short": "Ibara",
           "hue": "#00A040"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# fukuyama` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. JR's Sanyo blue, which no blue
# clears Retail's pin in, goes teal (Okayama's and Maebashi's); the Fukuen
# red stands; the Ibara green moves to a yellower green. Closest pair within
# 500 m 113.3 (Fukuen, Sanyo, which meet at 福山), anywhere 92.7; the
# dark-mode labels separate, 3 of 3.
_COLOURS = {"JS": "#007890", "JF": "#E83820", "IB": "#28A800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city. N02's network totals match the
# operators' (the brief: JR West's Fukuen Line 27 stations, the Ibara
# Railway's 15); every line is cut by the city line and has no in-city count
# of its own.
GATE3 = {"source": "none: no line is wholly inside the city (N02's totals match JR West's Fukuen Line 27 and the "
                   "Ibara Railway's 15, the brief)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUKUYAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUKUYAMA_BBOX
