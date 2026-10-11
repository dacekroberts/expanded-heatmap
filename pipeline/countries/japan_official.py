"""The official restaurant counts every Japanese permit list is measured against.

One copy for the build's share check and scripts/japan_ward_table.py
(2026-09-28):

  * **Tokyo's statistical yearbook, table 19-8** (`data/tokyo/raw/tn24qv190800.csv`):
    飲食店営業 per special ward and per Tama city at the end of the latest
    fiscal year (FY2024, so as of 2025-03-31); **table 19-7**
    (`tn24qv190700.csv`, the owner's call 189, 2026-10-06): the barbers,
    beauty salons and laundries of each, the Tama cities' registers measured
    against it.
  * **MHLW's 衛生行政報告例 on e-Stat**, FY2024 (`data/japan/raw/`): permitted
    facilities at year-end, old law (table 5-2-1) plus revised law (5-4-1), per
    designated city. Their sum for 東京都 equals the yearbook exactly, so every
    city and ward is measured one way.

The measure (the Tokyo brief's, 2026-09-24): a list's 飲食店 permit rows,
vehicles and stalls INCLUDED (the official count includes them; the taxonomy
drops them), closed rows excluded, against the official 飲食店営業 count.

Reads the cache only; nothing here fetches.
"""
import csv
import io
from pathlib import Path

from pipeline.countries import japan

_ROOT = Path(__file__).parent.parent.parent
YEARBOOK = _ROOT / "data" / "tokyo" / "raw" / "tn24qv190800.csv"
YEARBOOK_REGISTERS = _ROOT / "data" / "tokyo" / "raw" / "tn24qv190700.csv"
# The yearbook's counts stand at the end of its fiscal year (FY2024): the date
# a list's rows are cut at for the share "at the yearbook's date" (calls
# 187-189).
YEARBOOK_DATE = "2025-03-31"
ESTAT_OLD = japan.SHARED_RAW / "estat_eisei_r6_food_5-2-1_oldlaw_by_type.csv"
ESTAT_NEW = japan.SHARED_RAW / "estat_eisei_r6_food_5-4-1_newlaw_by_type.csv"
YEARBOOK_SOURCE = "Tokyo statistical yearbook, table 19-8 (飲食店営業, FY2024)"
YEARBOOK_REGISTERS_SOURCE = "Tokyo statistical yearbook, table 19-7 (理容所, 美容所, クリーニング所, FY2024)"
ESTAT_SOURCE = "MHLW 衛生行政報告例 FY2024 (e-Stat), tables 5-2-1 + 5-4-1"


def _decode(b):
    from pipeline.countries import japan_register
    return japan_register.decode(b)


def _yearbook_table(path, columns):
    """{municipality name: {column label start: count}} for one yearbook
    table's latest fiscal year: the special wards (131xx) and the Tama cities
    (132xx), never a total (13100 区部, 13200 市部). Columns are found by the
    start of their label, never by position; "-" reads 0. {} if not cached."""
    if not path.exists():
        return {}
    rows = list(csv.reader(io.StringIO(_decode(path.read_bytes()))))
    cols = {p: next(i for i, c in enumerate(rows[0]) if c.startswith(p)) for p in columns}
    munis = [r for r in rows[1:] if len(r) > max(cols.values()) and r[3][:3] in ("131", "132")
             and not r[3].endswith("00")]
    latest = max(r[1] for r in munis)
    num = lambda x: 0 if x.strip() in ("-", "") else int(x.replace(",", ""))  # noqa: E731
    return {r[4]: {p: num(r[i]) for p, i in cols.items()} for r in munis if r[1] == latest}


def yearbook():
    """Tokyo ward or Tama city name -> 飲食店営業 in the yearbook's latest
    fiscal year; {} if not cached. The Tama cities since 2026-10-07 (East-1,
    Higashiyamato first); a ward reads as before."""
    return {m: v["飲食店営業"] for m, v in _yearbook_table(YEARBOOK, ("飲食店営業",)).items()}


# Each register's column in table 19-7, by the start of its label
REGISTER_COLUMNS = {"barber": "理容所", "beauty": "美容所", "laundry": "クリーニング所"}


def registers(municipality):
    """{"barber": n, "beauty": n, "laundry": n} for a Tokyo ward or Tama city in
    table 19-7's latest fiscal year (call 189); {} where it is not covered or
    the table is not cached."""
    t = _yearbook_table(YEARBOOK_REGISTERS, tuple(REGISTER_COLUMNS.values())).get(municipality)
    return {k: t[c] for k, c in REGISTER_COLUMNS.items()} if t else {}


def estat():
    """'大阪府大阪市' -> 飲食店営業 permitted facilities, old law + revised law; {} if not cached."""
    if not (ESTAT_OLD.exists() and ESTAT_NEW.exists()):
        return {}

    def table(path, want):
        rows = list(csv.reader(io.StringIO(path.read_bytes().decode("cp932"))))
        h = next(i for i, r in enumerate(rows) if len(r) > 1 and r[1] == "総数")
        labels = ["/".join(dict.fromkeys(p for p in (rows[h][j] if j < len(rows[h]) else "",
                                                       rows[h + 1][j] if j < len(rows[h + 1]) else "")
                                         if p and p != "施設")) for j in range(max(map(len, rows)))]
        j = labels.index(want)
        num = lambda x: 0 if x.strip() in ("-", "", "…") else int(x.replace(",", ""))  # noqa: E731
        return {r[0].strip(): num(r[j]) for r in rows[h + 2:] if r and r[0].strip()}

    old, new = table(ESTAT_OLD, "飲食店営業/総数"), table(ESTAT_NEW, "飲食店営業")
    return {a: old[a] + new.get(a, 0) for a in old if a in new}


CENSUS_SOURCE = "2021 Economic Census for Business Activity, table 9-1A (飲食店, industry 76, all establishments)"


def census():
    """Municipality code (5 digits, e.g. '13113') -> 飲食店 establishments in the
    2021 Economic Census (japan.ESTAT_CENSUS_XLSX); {} if not cached. The
    like-for-like CONTROL the owner chose (2026-09-24): establishments counted
    on the ground, against the permits a list holds. The column is found by its
    header label, never by position."""
    if not japan.ESTAT_CENSUS_XLSX.exists():
        return {}
    import openpyxl
    wb = openpyxl.load_workbook(japan.ESTAT_CENSUS_XLSX, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    col, out = None, {}
    for r in ws.iter_rows(values_only=True):
        cells = ["" if c is None else str(c).strip() for c in r]
        if col is None:
            col = next((i for i, c in enumerate(cells) if c.startswith("76_") and "飲食店" in c), None)
            continue
        code = cells[1].split("_", 1)[0] if len(cells) > 1 else ""
        if code.isdigit() and len(code) == 5 and col < len(cells):
            v = cells[col]
            out[code] = 0 if v in ("-", "") else int(float(v))
    wb.close()
    if col is None:
        raise ValueError(f"{japan.ESTAT_CENSUS_XLSX.name}: no 76_飲食店 column - not the table the build read")
    return out


def restaurants(prefecture, municipality):
    """(the official 飲食店営業 count, its source) for one municipality: a Tokyo
    special ward or Tama city from the yearbook, a designated city from e-Stat;
    (None, None) where neither covers it or the file is not cached."""
    if prefecture == "東京都":
        # a special ward, or a Tama city: its yearbook row, never e-Stat's
        n = yearbook().get(municipality)
        if n or municipality.endswith("区"):
            return (n, YEARBOOK_SOURCE) if n else (None, None)
    n = estat().get(prefecture + municipality)
    return (n, ESTAT_SOURCE) if n else (None, None)
