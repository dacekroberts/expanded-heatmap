"""Saitama Prefecture's shared business leg: the prefecture's own food and
生活衛生 lists for the municipalities its health centres serve (every city and
town but Saitama City, Kawagoe, Kawaguchi and Koshigaya, each a health-centre
city with lists of its own), each page cut out of them by its address.

One module for the four Saitama pages (owner, call 171, 2026-10-06): Ageo
(Regional), Sōka, Tokorozawa and Kasukabe. Each page's config reads SOURCES,
SOURCE_KIND, REQUIRED_COLUMNS, TERM_AS_OF, OWN_POINT_FALLBACK and city_rows()
from here and adds only what is its own: its municipalities (japan.CITIES), its
health centre's workbook in the 生活衛生 zip (HEALTH_CENTRE: "05鴻巣" for Ageo
and Ina, "04草加", "08狭山", "03春日部"), its ISJ pairs and its rail.

  * Food, three files read as one source of each law (call 171): the live
    new-law layer (食品営業施設_新法_公開, every permit and notification since
    2021-06-01, with the prefecture's own point), and the old-law permits as the
    R8.3.31 old-law list (kyuho_R080331.xls, no point) together with the live
    old-law layer (食品営業施設_旧法_公開), which the briefs measured as a
    partial load (Tokorozawa: 77 rows against the list's 698). The old-law rows
    are an UPPER BOUND as of 2026-03-31: closures since are unseen, and the page
    says so (Kyoto's disclosure). The new-law layer is complete against its own
    R8.3.31 list (Tokorozawa: 2 of 1,583 restaurants missing), so that list is
    not read.
  * The type carries a code (`01:飲食店営業 `); japan_eigyo.normalise strips it
    (the Japan foundation, S15).
  * Personal services: the FY-end 生活衛生 list (r7nenndo.zip, every premises
    holding a permit or confirmation on 2026-03-31, one workbook per health
    centre) plus each month's new premises after it (Ichinomiya's call 126),
    one row per (address, trade name). The months to 2026-03 are already in the
    list (the briefs: Ageo 10 of 10 barbers, 132 of 132 salons, 14 of 14
    laundries), so they are not read.
  * The publisher withholds some premises at the operator's request
    (「※事業者の要望により、一部の施設情報は掲載されないことがあります。」 on both
    pages); the page discloses it with no number (call 173, Matsudo's
    precedent).
  * Licences: the layers and the R8.3.31 list through the GIS catalogue, which
    applies the prefecture portal's terms (PDL 1.0); the 生活衛生 files on the
    portal's 2024 PDL record for the page, relied on (owner, call 143).

Every address starts at the municipality (上尾市…, 北足立郡伊奈町…); the R8.3.31
list writes 埼玉県 first, which is cut at read so every file's address reads
alike (the one-pin and de-duplication keys compare them). Phone columns are
dropped at read and never requested (電話番号, 施設_電話番号, 施設電話番号); the
applicant (申請者_氏名, 申請者名) is kept for the name rule only, read IN MEMORY
(japan_register.OPERATOR_COLS) and never written.

No reads of data/ at import: the deployed app imports each city's config, and
through it this module. The download is `fetch()`, fenced for
scripts/check_no_fetch_in_steps.py; only a city's fetch_sources.py calls it.
"""
import collections
import functools
import io
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote, urlencode

PREFECTURE = "埼玉県"
RAW_DIR = Path(__file__).parent.parent.parent / "data" / "saitama_pref" / "raw"

FOOD_PAGE = "https://www.pref.saitama.lg.jp/a0708/syokuhini-ichiran/ichiran-top.html"
GIS_CATALOGUE = "https://portal-pref-saitama.hub.arcgis.com/pages/opendatacatalog"
ENV_PAGE = "https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html"
PORTAL_TERMS = "https://opendata.pref.saitama.lg.jp/pages/terms"
_LAYER = "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/{}/FeatureServer/0/query"
_ITEM = "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/{}/data"
_ENV = "https://www.pref.saitama.lg.jp/documents/232288/"

# The layers' fields, every one but 電話番号 (never requested); OBJECTID pages
# the query. Each layer's own maxRecordCount (the briefs, 2026-10-06).
LAYER_FIELDS = "OBJECTID,施設_名称,施設所在地,所在地建物名付,業種名,申請者_氏名,有効開始年月日,有効終了年月日,許可番号"
LAYERS = {"food_layer_new": ("食品営業施設_新法_公開", 16000), "food_layer_old": ("食品営業施設_旧法_公開", 2000)}


def layer_query(key):
    """A layer's query URL as the build reads it (the first page; fetch() pages it)."""
    service, page = LAYERS[key]
    return _LAYER.format(quote(service)) + "?" + urlencode(
        {"where": "1=1", "outFields": LAYER_FIELDS, "orderByFields": "OBJECTID", "outSR": 4326, "f": "geojson",
         "resultOffset": 0, "resultRecordCount": page})


# The months after the FY-end list (2026-04 to 2026-08), each file named by hand
# on page 232288 (the briefs: r0804 ... r808, no pattern)
MONTHS = (("2604", "r0804.xlsx", "2026-04-30"), ("2605", "r0805.xlsx", "2026-05-31"),
          ("2606", "r0806.xlsx", "2026-06-30"), ("2607", "r0807.xlsx", "2026-07-31"),
          ("2608", "r808.xlsx", "2026-08-31"))

# file key -> (file in RAW_DIR, URL of the edition read, dataset page). The
# layers' file names carry their retrieval date: a refresh is a new file under
# a new name (the shared data/ folder's rule), never an overwrite.
SOURCE_FILES = {
    "food_layer_new": ("food_shinpo_layer_20261006.geojson", layer_query("food_layer_new"), FOOD_PAGE),
    "food_layer_old": ("food_kyuho_layer_20261006.geojson", layer_query("food_layer_old"), FOOD_PAGE),
    # the R8.3.31 old-law list, content item 7da15c28 (2,542,080 B)
    "food_list_old": ("kyuho_R080331.xls", _ITEM.format("7da15c2811db4a55953345b16299d462"), GIS_CATALOGUE),
    "env_list": ("r7nenndo.zip", _ENV + "r7nenndo.zip", ENV_PAGE),
    **{f"env_{m}": (name, _ENV + name, ENV_PAGE) for m, name, _ in MONTHS},
}
# Each file's own date: the layers' retrieval (they are live, edited
# 2026-10-06), the lists' stated 2026-03-31, each month's last day
LAYERS_AS_OF = "2026-10-06"
SOURCE_AS_OF = {"food_layer_new": LAYERS_AS_OF, "food_layer_old": LAYERS_AS_OF, "food_list_old": "2026-03-31",
                "env_list": "2026-03-31", **{f"env_{m}": end for m, _, end in MONTHS}}
FOOD_AS_OF = LAYERS_AS_OF
REGISTERS_AS_OF = MONTHS[-1][2]

# The columns each FILE must carry as it stands (fetch_sources.py stops on a
# header without them)
_LAYER_COLUMNS = ("施設_名称", "施設所在地", "業種名", "申請者_氏名", "有効開始年月日", "有効終了年月日", "許可番号")
_ENV_COLUMNS = ("業種", "施設名称", "施設所在地", "申請者名")
FILE_COLUMNS = {"food_layer_new": _LAYER_COLUMNS, "food_layer_old": _LAYER_COLUMNS,
                "food_list_old": ("業種", "施設_名称", "施設_所在地", "申請者_氏名", "開始年月日", "終了年月日", "許可番号"),
                **{k: _ENV_COLUMNS for k in SOURCE_FILES if k.startswith("env_")}}

# --- step 2's sources ------------------------------------------------------------
# key -> the file that names it (japan_step2 reads every one through city_rows):
# "food" the new-law layer, "food_old" the old-law permits (the R8.3.31 list
# with the live old-law layer, call 171), each register the FY-end list plus
# the months
SOURCES = {"food": SOURCE_FILES["food_layer_new"][0], "food_old": SOURCE_FILES["food_list_old"][0],
           "barber": SOURCE_FILES["env_list"][0], "beauty": SOURCE_FILES["env_list"][0],
           "laundry": SOURCE_FILES["env_list"][0]}
SOURCE_KIND = {"food_old": "food"}
# The permits' terms read against the layers' retrieval date, never today
# (calls 161 and 172): the old-law list's rows included, since a permit on it
# still in term on that date is one the prefecture has not shown closed
TERM_AS_OF = {"food": LAYERS_AS_OF, "food_old": LAYERS_AS_OF}
# The layers carry the prefecture's own point; it places a row the block join
# misses (call 127c). The R8.3.31 list's rows carry none.
OWN_POINT_FALLBACK = {"food", "food_old"}

# The food columns after read, one set for the layers and the list alike: the
# list's spellings renamed to the layer's, the layers' term to the names
# japan_register.END_COLS / START_COLS read (有効終了年月日 is in neither)
_FOOD = ("施設_名称", "施設所在地", "業種名", "申請者_氏名", "許可開始日", "許可終了日", "許可番号", "緯度", "経度")
_REGISTER = ("業種", "施設名称", "施設所在地", "申請者名", "確認年月日")
REQUIRED_COLUMNS = {"food": _FOOD, "food_old": _FOOD, "barber": _REGISTER, "beauty": _REGISTER,
                    "laundry": (*_REGISTER, "営業の種類")}
# (the food files only: the registers keep their 業種)
FOOD_RENAME = {"有効開始年月日": "許可開始日", "有効終了年月日": "許可終了日", "施設_所在地": "施設所在地", "業種": "業種名",
               "開始年月日": "許可開始日", "終了年月日": "許可終了日"}
# Never kept: every phone, the layers' address-with-building (the build reads
# 施設所在地) and the list's health centre
DROP_COLUMNS = ("電話番号", "施設_電話番号", "施設電話番号", "所在地建物名付", "管轄保健所")

# Each register's sheet: the FY-end workbooks and the 2026 months name it so;
# the 2025 months (not read) write 理容 and 美容
REGISTER_SHEETS = {"barber": "理容所", "beauty": "美容所", "laundry": "クリーニング"}

# The old-law types the new law renamed, for the renewal test (Tokorozawa's
# brief: 喫茶店営業 counts as 飲食店営業 there)
RENEWED_AS = {"喫茶店営業": "飲食店営業"}


def _addr(s):
    """The publisher's address with 埼玉県 cut from its front (the R8.3.31 list
    writes it, the layers and the registers do not)."""
    a = (s or "").strip()
    return a[len(PREFECTURE):] if a.startswith(PREFECTURE) else a


def _key(s):
    """An address or name as the cut and the keys compare it: NFKC, no spaces,
    one dash."""
    return re.sub(r"[‐‑‒–—―−ｰー－]", "-", unicodedata.normalize("NFKC", s or "").replace(" ", "").replace("　", ""))


def _clean(row, rename=None):
    """A row's columns renamed (FOOD_RENAME for a food file), dropped
    (DROP_COLUMNS) and its address cut (_addr)."""
    rename = rename or {}
    out = {rename.get(k, k): v for k, v in row.items() if k not in DROP_COLUMNS}
    out["施設所在地"] = _addr(out.get("施設所在地"))
    return out


@functools.lru_cache(maxsize=4)
def _layer(path):
    """A layer's features as rows, the publisher's point as 緯度 / 経度 (the key
    japan_register.permits_from_rows reads). 5 new-law rows sit at (0, 0)
    (none in Ageo or Ina, 2026-10-06): no point."""
    feats = json.loads(Path(path).read_text(encoding="utf-8"))["features"]
    rows = []
    for f in feats:
        r = _clean(f["properties"], FOOD_RENAME)
        xy = (f.get("geometry") or {}).get("coordinates") or (0, 0)
        ok = abs(xy[0]) > 1 and abs(xy[1]) > 1
        r["緯度"], r["経度"] = (str(xy[1]), str(xy[0])) if ok else ("", "")
        rows.append(r)
    return tuple(rows)


def layer_rows(path):
    return [dict(r) for r in _layer(str(path))]


def list_rows(path):
    """The R8.3.31 list's rows (xlrd through japan_register.city_rows), its
    columns in the layer's spelling, with no point."""
    from pipeline.countries import japan_register as jr
    return [{**_clean(r, FOOD_RENAME), "緯度": "", "経度": ""} for r in jr.city_rows(path)]


def _sheet_rows(data, kind):
    """One register sheet of a workbook's bytes, or none where the workbook has
    no such sheet (r0807.xlsx has no laundry sheet: no new laundry that month)."""
    import openpyxl
    from pipeline.countries import japan_register as jr
    names = [ws.title.replace(" ", "").replace("　", "")
             for ws in openpyxl.load_workbook(io.BytesIO(data), read_only=True).worksheets]
    if REGISTER_SHEETS[kind] not in names:
        return []
    return [_clean(r) for r in jr.xlsx_rows(data, sheet=REGISTER_SHEETS[kind])]


def register_rows(kind, health_centre, raw_dir=RAW_DIR):
    """A register of one health centre's area: the FY-end workbook's sheet,
    then each month's new premises after it; a month's row whose (address,
    trade name) the list or an earlier month holds is dropped. Returns
    (rows, rows from the list, rows added by the months, months' repeats)."""
    import zipfile

    from pipeline.countries import japan_register as jr
    with zipfile.ZipFile(Path(raw_dir) / SOURCE_FILES["env_list"][0]) as zf:
        members = [i for i in zf.infolist() if health_centre in jr.zip_member_name(i)]
        if len(members) != 1:
            raise ValueError(f"r7nenndo.zip: {len(members)} workbooks named {health_centre!r} (want 1)")
        rows = _sheet_rows(zf.read(members[0]), kind)
    seen = {(_key(r["施設所在地"]), jr._name_key(r.get("施設名称"))) for r in rows}
    n_list, added, repeat = len(rows), 0, 0
    for m, name, _ in MONTHS:
        for r in _sheet_rows((Path(raw_dir) / name).read_bytes(), kind):
            k = (_key(r["施設所在地"]), jr._name_key(r.get("施設名称")))
            if k in seen:
                repeat += 1
                continue
            seen.add(k)
            rows.append(r)
            added += 1
    return rows, n_list, added, repeat


def cut(rows, municipalities, label):
    """The rows whose address starts at one of the page's municipalities, as
    MLIT's 市区町村名 writes them (上尾市, 北足立郡伊奈町). Raises on an address
    naming one anywhere else, or starting at a town without its 郡 (伊奈町…): a
    row the cut would drop silently (Tsu's rule, Itami's brief)."""
    names = tuple(municipalities)
    short = tuple(m.split("郡", 1)[1] for m in names if "郡" in m)
    out, elsewhere = [], []
    for r in rows:
        a = _key(r.get("施設所在地"))
        if a.startswith(names):
            out.append(r)
        elif any(m in a for m in names) or a.startswith(short):
            elsewhere.append(a)
    if elsewhere:
        raise ValueError(f"{label}: {len(elsewhere)} address(es) name {'/'.join(names)} after another place "
                         f"(the cut would drop them): {elsewhere[:3]}")
    return out


def _type(t):
    """A type as the old-law and new-law rows compare it: the layer's code and
    spaces gone (japan_eigyo.normalise), the old law's renamed types mapped."""
    from pipeline.taxonomies import japan_eigyo
    t = japan_eigyo.normalise(t)
    return RENEWED_AS.get(t, t)


def _premises(r):
    from pipeline.countries import japan_register as jr
    return _key(r["施設所在地"]), jr._name_key(r.get("施設_名称")), _type(r.get("業種名"))


def _same_premises(a, known):
    """The file of a row already kept under the same (trade name, type) whose
    address is `a`, or starts it, or is started by it, else None. The R8.3.31
    lists add the building to an address the layers write without it (Ageo
    and Ina, 2026-10-07: 170 of the new-law list's permits found in the layer
    by number); permit numbers are no key alone (26 old-law list numbers name
    two premises in Ageo and Ina; the brief: 17 repeats of number, start and
    type in the new-law layer)."""
    return next((o for b, o in known if a == b or a.startswith(b) or b.startswith(a)), None)


def _in_term(r, as_of):
    """A permit in term on `as_of`: not ended before it (call 161), not starting
    after it (call 172). A row with no term (a notification) is in term."""
    from pipeline.countries import japan_register as jr
    end, start = jr.wareki_date(r.get("許可終了日")), jr.wareki_date(r.get("許可開始日"))
    return not (end and end < as_of) and not (start and start > as_of)


def old_law_rows(municipalities, raw_dir=RAW_DIR, as_of=LAYERS_AS_OF, report=print):
    """The old-law permits of the page's municipalities, the owner's call 171:
    the live old-law layer and the R8.3.31 old-law list read together, one row
    per premises and type (the same trade name and type at the same address,
    the building aside, _same_premises; or the same permit number, trade name
    and type), the layer's row kept where both hold it (its point, and the
    prefecture's later edits); in term on `as_of`; and a row dropped where the
    new-law layer holds the same premises and type in term, a permit renewed
    under the new law. Tokorozawa's brief: 501 in term, 21 renewed, 480 kept."""
    import datetime

    from pipeline.baseline import emit
    day = datetime.date.fromisoformat(as_of)
    layer = cut(layer_rows(Path(raw_dir) / SOURCE_FILES["food_layer_old"][0]), municipalities, "old-law layer")
    lst = cut(list_rows(Path(raw_dir) / SOURCE_FILES["food_list_old"][0]), municipalities, "old-law list")
    new = cut(layer_rows(Path(raw_dir) / SOURCE_FILES["food_layer_new"][0]), municipalities, "new-law layer")
    seen, numbers, rows = collections.defaultdict(list), {}, []
    # a repeat, by the file of the row it repeats: (repeating, repeated) -> rows
    dup = collections.Counter()
    for origin, rs in (("layer", layer), ("list", lst)):
        for r in rs:
            a, name, typ = _premises(r)
            n = (_key(r.get("許可番号")), name, typ) if _key(r.get("許可番号")) else None
            hit = _same_premises(a, seen.get((name, typ), ())) or (numbers.get(n) if n else None)
            if hit:
                dup[(origin, hit)] += 1
                continue
            seen[(name, typ)].append((a, origin))
            if n:
                numbers[n] = origin
            rows.append((origin, r))
    from_list = sum(1 for o, _ in rows if o == "list")
    term = [(o, r) for o, r in rows if _in_term(r, day)]
    renewed = collections.defaultdict(list)
    for r in new:
        if _in_term(r, day):
            a, name, typ = _premises(r)
            renewed[(name, typ)].append((a, "new"))
    kept = [r for _, r in term if not _same_premises(_premises(r)[0], renewed.get(_premises(r)[1:], ()))]
    report(f"  old-law permits (call 171): layer {len(layer):,}, R8.3.31 list {len(lst):,}; one per premises and "
           f"type: {len(rows):,} ({from_list:,} from the list alone; list rows the layer holds "
           f"{dup[('list', 'layer')]:,}, repeats within the list {dup[('list', 'list')]:,}, within the layer "
           f"{dup[('layer', 'layer')]:,})")
    report(f"    from the list alone and in term: {sum(1 for o, _ in term if o == 'list'):,}")
    report(f"    in term on {as_of}: {len(term):,} (lapsed {len(rows) - len(term):,}); renewed under the new law "
           f"(dropped): {len(term) - len(kept):,}; kept {len(kept):,}")
    for k, v in (("old_law_layer_rows", len(layer)), ("old_law_list_rows", len(lst)), ("old_law_one_per", len(rows)),
                 ("old_law_from_list_alone", from_list), ("old_law_in_term", len(term)),
                 ("old_law_renewed", len(term) - len(kept)), ("old_law_kept", len(kept))):
        emit(k, v)
    return kept


def city_rows(key, municipalities, health_centre, raw_dir=RAW_DIR, report=print):
    """One step-2 source's rows for one page: "food" the new-law layer,
    "food_old" the old-law permits (old_law_rows), each register its health
    centre's FY-end sheet plus the months; each cut to the page's
    municipalities by address (cut)."""
    if key == "food":
        return cut(layer_rows(Path(raw_dir) / SOURCE_FILES["food_layer_new"][0]), municipalities, "new-law layer")
    if key == "food_old":
        return old_law_rows(municipalities, raw_dir, report=report)
    if key in REGISTER_SHEETS:
        rows, n_list, added, repeat = register_rows(key, health_centre, raw_dir)
        mine = cut(rows, municipalities, f"{key} register")
        from pipeline.countries import japan_register as jr
        listed = {(_key(r["施設所在地"]), jr._name_key(r.get("施設名称"))) for r in rows[:n_list]}
        new = sum(1 for r in mine if (_key(r["施設所在地"]), jr._name_key(r.get("施設名称"))) not in listed)
        report(f"  {key}: the 2026-03-31 list and the months to {REGISTERS_AS_OF}: {len(mine):,} here "
               f"({new:,} from the months; area-wide {n_list:,} + {added:,}, {repeat:,} month rows already listed)")
        return mine
    raise KeyError(key)


def file_rows(key, raw_dir=RAW_DIR):
    """One FILE's rows as it stands (fetch_sources.py's count and column check):
    a layer's features, the list's rows, every sheet of a workbook."""
    from pipeline.countries import japan_register as jr
    path = Path(raw_dir) / SOURCE_FILES[key][0]
    if key in LAYERS:
        return [{k: v for k, v in f["properties"].items() if k not in DROP_COLUMNS}
                for f in json.loads(path.read_text(encoding="utf-8"))["features"]]
    return [{k: v for k, v in r.items() if k not in DROP_COLUMNS} for r in jr.city_rows(path)]


def fetch(config, force=False):
    """Download every Saitama file a page reads into RAW_DIR, recorded in the
    page's provenance (japan_fetch.record). The layers are queried whole and
    paged by OBJECTID with LAYER_FIELDS (never 電話番号); a layer already on
    disk is never overwritten, even with --force, since a refresh is a new
    dated file. The rest are plain GETs (japan_fetch.get). Fenced: only a
    city's fetch_sources.py calls it."""
    import time

    from pipeline.countries import japan_fetch
    for key, (name, url, page) in SOURCE_FILES.items():
        dest = Path(RAW_DIR) / name
        if key in LAYERS:
            how = "kept (on disk; a refresh is a new dated file)"
            if not dest.exists():
                service, size = LAYERS[key]
                base = _LAYER.format(quote(service))
                r = japan_fetch.S.get(base, params={"where": "1=1", "returnCountOnly": "true", "f": "json"},
                                      timeout=120)
                r.raise_for_status()
                total = r.json()["count"]
                feats = []
                while len(feats) < total:
                    p = {"where": "1=1", "outFields": LAYER_FIELDS, "orderByFields": "OBJECTID", "outSR": 4326,
                         "f": "geojson", "resultOffset": len(feats), "resultRecordCount": size}
                    r = japan_fetch.S.get(base, params=p, timeout=300)
                    r.raise_for_status()
                    page_feats = r.json()["features"]
                    if not page_feats:
                        break
                    feats += page_feats
                    time.sleep(2)
                part = dest.with_suffix(dest.suffix + ".part")
                part.write_bytes(json.dumps({"type": "FeatureCollection", "source": base, "count_reported": total,
                                             "outFields": LAYER_FIELDS, "features": feats},
                                            ensure_ascii=False).encode("utf-8"))
                part.replace(dest)
                how = "downloaded"
        else:
            how = japan_fetch.get(url, dest, force)
        rows = file_rows(key)
        missing = [c for c in FILE_COLUMNS[key] if c not in rows[0]]
        if missing:
            raise SystemExit(f"{dest.name}: header lacks {missing} - not the file the brief read")
        print(f"  {dest.name:36s} {dest.stat().st_size:>10,} bytes {len(rows):>7,} rows  ({how})")
        japan_fetch.record(config, f"city_{key}", file=f"data/saitama_pref/raw/{name}", url=url, dataset_page=page,
                           bytes=dest.stat().st_size, sha256=japan_fetch.sha256(dest), rows=len(rows),
                           as_of=SOURCE_AS_OF[key], retrieved=japan_fetch.when(dest), how=how)
