"""The Japan list: every Japanese city, and every ward, from the data on disk.

    python scripts/japan_ward_table.py            # print the list
    python scripts/japan_ward_table.py --write    # and rewrite docs/japan_city_list.md

The owner asked on 2026-09-24 for Japan's table set to be republished on its
own, apart from the banded master list. So it is GENERATED, not hand-kept: a
republish re-measures. What is not measured (band, build order, one-line
status) lives in STATUS below. When a band or the build order changes, change
it there and regenerate.

Per ward:
- **Fixed permit rows by bucket**: the join's own rows (`japan_register`),
  bucketed by `japan_eigyo`, before build-time de-duplication.
- **The share placed at block level.**
- **Rail stations**: distinct N02 station names inside the ward's N03
  polygon, with the Shinkansen and the Sagano scenic line left out (owner). A
  station is shown only where that prefecture's N03 file is cached.

For Tokyo it also checks whether each ward's food list is COMPLETE. A list
whose earliest permit date is 2021 or later holds only the permits since the
2021 reform. That is how Chūō, Kōtō and Minato were found partial on
2026-09-24.

Privacy: date and type columns are selected by EXACT name. A pattern once
matched 法人名 through 法 and printed operator names. Nothing here prints a
name or an address.
"""
import collections
import datetime
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from pipeline.countries import japan as JP  # noqa: E402
from pipeline.countries import japan_register as J  # noqa: E402
from pipeline.taxonomies import japan_eigyo as T  # noqa: E402
import screen_japan_join as S  # noqa: E402

OUT = ROOT / "docs" / "japan_city_list.md"

# Not measured: band, build order and status (owner's calls). Keep in step
# with docs/city_master_list.md.
STATUS = {
    "osaka": ("Osaka", "🟢 A", "Builds 1st. About two-thirds of the gap is expired old-law permits still in "
                               "the official count. The other third, revised-law permits the city counts but "
                               "never lists, is undetermined. See osaka.md"),
    "kobe": ("Kobe", "🟢 A", "2nd"),
    "sapporo": ("Sapporo", "🟢 A", "3rd. Grid addresses resolve to the 条丁目 block, about 100 m"),
    "fukuoka": ("Fukuoka", "🟢 A", "4th. Includes MHLW's addressed rows; about 20% of restaurants withhold their address"),
    "kyoto": ("Kyoto", "🟢 A", "5th. Rebuilt register: an upper bound"),
    "tokyo": ("Tokyo (8 wards)", "🟢 A", "6th, last. Chiyoda missing"),
    "hiroshima": ("Hiroshima", "🟣 C", "Food only: no personal-services list is published"),
    "sendai": ("Sendai", "🔴 D", "Needs the city's permission; letter drafted, not sent"),
}
GAP = [  # no list on disk: status only (key, name, wards, personal services, status)
    ("yokohama", "Yokohama", 18, "complete (2026-04-01)",
     "Only 2,912 restaurants online (MHLW's opt-in slice). A request to the city"),
    ("nagoya", "Nagoya", 16, "beauty list only", "BODIK keeps only 12 months of new permits. A request to the city"),
]
# What the ward probes of 2026-09-24 found about each food list (not measured here).
TOKYO_NOTE = {
    "新宿区": "complete as of 2023-01-01. A 2026-03-31 full list exists only as PDF, under site terms that bar reuse",
    "渋谷区": "open list, closed premises dropped",
    "世田谷区": "opted-out premises left out (the ward's page)",
    "台東区": "opted-out premises left out (the ward's page)",
    "港区": "consent-filtered. No old-law list is published",
    "目黒区": "first permits only: premises moved from an old-law permit since 2021 are in neither list, "
              "so the share falls as old permits expire",
    "中央区": "never updated since",
    "江東区": "consent-only new permits",
}
# Tokyo's statistical yearbook, table 19-8: 飲食店営業 per ward at the end of
# FY2024 - the official count each ward's list is measured against.
YEARBOOK = S.DATA / "tokyo" / "raw" / "tn24qv190800.csv"
# MHLW's 衛生行政報告例 on e-Stat, FY2024: permitted facilities at year-end,
# old-law (table 5-2-1) + revised-law (5-4-1). Their sum for 東京都 equals the
# yearbook exactly, so every city and ward is measured one way.
ESTAT_OLD = S.DATA / "japan" / "raw" / "estat_eisei_r6_food_5-2-1_oldlaw_by_type.csv"
ESTAT_NEW = S.DATA / "japan" / "raw" / "estat_eisei_r6_food_5-4-1_newlaw_by_type.csv"
ESTAT_AREA = {"osaka": "大阪府大阪市", "kobe": "兵庫県神戸市", "sapporo": "北海道札幌市", "fukuoka": "福岡県福岡市",
              "kyoto": "京都府京都市", "hiroshima": "広島県広島市", "sendai": "宮城県仙台市",
              "yokohama": "神奈川県横浜市", "nagoya": "愛知県名古屋市"}

ROMAJI = {
    "osaka": {"中央区": "Chūō", "北区": "Kita", "淀川区": "Yodogawa", "西区": "Nishi", "生野区": "Ikuno",
              "都島区": "Miyakojima", "浪速区": "Naniwa", "福島区": "Fukushima", "阿倍野区": "Abeno",
              "西成区": "Nishinari", "天王寺区": "Tennōji", "平野区": "Hirano", "東淀川区": "Higashiyodogawa",
              "住吉区": "Sumiyoshi", "城東区": "Jōtō", "東住吉区": "Higashisumiyoshi", "住之江区": "Suminoe",
              "東成区": "Higashinari", "港区": "Minato", "大正区": "Taishō", "此花区": "Konohana", "旭区": "Asahi",
              "西淀川区": "Nishiyodogawa", "鶴見区": "Tsurumi"},
    "kobe": {"中央区": "Chūō", "兵庫区": "Hyōgo", "東灘区": "Higashinada", "灘区": "Nada", "長田区": "Nagata",
             "北区": "Kita", "須磨区": "Suma", "垂水区": "Tarumi", "西区": "Nishi"},
    "sapporo": {"中央区": "Chūō", "北区": "Kita", "東区": "Higashi", "豊平区": "Toyohira", "白石区": "Shiroishi",
                "西区": "Nishi", "南区": "Minami", "手稲区": "Teine", "厚別区": "Atsubetsu", "清田区": "Kiyota"},
    "fukuoka": {"中央区": "Chūō", "博多区": "Hakata", "東区": "Higashi", "早良区": "Sawara", "南区": "Minami",
                "西区": "Nishi", "城南区": "Jōnan"},
    "kyoto": {"中京区": "Nakagyō", "東山区": "Higashiyama", "下京区": "Shimogyō", "左京区": "Sakyō",
              "伏見区": "Fushimi", "右京区": "Ukyō", "上京区": "Kamigyō", "南区": "Minami", "北区": "Kita",
              "山科区": "Yamashina", "西京区": "Nishikyō"},
    "hiroshima": {"中区": "Naka", "南区": "Minami", "西区": "Nishi", "安佐南区": "Asaminami", "佐伯区": "Saeki",
                  "安佐北区": "Asakita", "東区": "Higashi", "安芸区": "Aki"},
    "sendai": {"青葉区": "Aoba", "宮城野区": "Miyagino", "太白区": "Taihaku", "泉区": "Izumi", "若林区": "Wakabayashi"},
    "tokyo": {"新宿区": "Shinjuku", "渋谷区": "Shibuya", "世田谷区": "Setagaya", "台東区": "Taitō", "港区": "Minato",
              "目黒区": "Meguro", "中央区": "Chūō", "江東区": "Kōtō", "千代田区": "Chiyoda", "品川区": "Shinagawa",
              "大田区": "Ōta", "文京区": "Bunkyō", "荒川区": "Arakawa", "葛飾区": "Katsushika", "豊島区": "Toshima"},
}
FOOD = {"osaka": ["osaka"], "kobe": ["kobe"], "sapporo": ["sapporo"], "fukuoka": ["fukuoka", "fukuoka-mhlw"],
        "kyoto": ["kyoto"], "hiroshima": ["hiroshima", "hiroshima-mhlw"], "sendai": ["sendai"],
        "tokyo": ["taito", "setagaya", "meguro"]}
LIFE = {"osaka": ["osaka-life"], "kobe": ["kobe-life"], "sapporo": ["sapporo-life"], "fukuoka": ["fukuoka-life"],
        "kyoto": ["kyoto-life"], "sendai": ["sendai-life"], "tokyo": ["meguro-life"]}
TOKYO_NATIONAL = ("minato", "chuo", "shinjuku", "koto", "shibuya")
DATE_COLS = ("初回許可年月日", "初回許可日", "許可年月日", "許可開始日", "許可日")  # exact names only


def year(s):
    s = unicodedata.normalize("NFKC", s or "").strip()
    m = re.match(r"(\d{4})", s)
    if m:
        return int(m.group(1))
    m = re.match(r"(令和|平成|昭和|R|H|S)(\d+|元)", s)
    if m:
        n = 1 if m.group(2) == "元" else int(m.group(2))
        return n + {"令和": 2018, "R": 2018, "平成": 1988, "H": 1988, "昭和": 1925, "S": 1925}[m.group(1)]
    return None


def city_join(key, cache={}):  # noqa: B006 - a deliberate per-run cache of address files
    pref, cname, files, isj = S.CITIES[key]
    if isj not in cache:
        cache[isj] = J.load_city_isj(S.DATA / isj)
    ps = []
    for f in files:
        if callable(f):
            ps += J.permits_from_rows(f(), pref, cname)
        elif "*" in f:
            for path in sorted(S.DATA.glob(f)):
                ps += J.load_city_permits(path, pref, cname)
        else:
            ps += J.load_city_permits(S.DATA / f, pref, cname)
    return J.join_city(ps, *cache[isj])


def measure():
    wards = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

    def tally(city, ps, source, ward_of=lambda p: p["ward"]):
        for p in ps:
            # against the official count, every 飲食店 permit counts - vehicles and
            # stalls too, which the official count includes and the taxonomy drops
            if source == "food" and "飲食" in p["type"]:
                wards[city][ward_of(p)]["fs_all"] += 1
            b = T.classify({"permit_type": p["type"], "source": source})
            if not b:
                continue
            w = wards[city][ward_of(p)]
            if p["mobile"]:
                continue
            w[b] += 1
            w["bucketed"] += 1
            w["block"] += p["tier"] == "block"

    for city, keys in FOOD.items():
        for k in keys:
            tally(city, city_join(k), "food")
    for city, keys in LIFE.items():
        for k in keys:
            tally(city, city_join(k), "beauty")
    for k in TOKYO_NATIONAL:
        _, muni, csv_, bz, cz = S.MUNICIPALITIES[k]
        tally("tokyo", J.join(J.load_permits(S.DATA / csv_, muni), *J.load_isj(S.DATA / bz, S.DATA / cz)), "food",
              lambda p, m=muni: m)
    for k, (_, muni, csv_, bz, cz) in S.MUNICIPALITIES.items():
        if "-" in k:
            tally("tokyo", J.join(J.load_permits(S.DATA / csv_, muni), *J.load_isj(S.DATA / bz, S.DATA / cz)),
                  "beauty", lambda p, m=muni: m)

    st = JP.stations()
    st = st[st["N02_003"] != "嵯峨野観光線"]  # owner, 2026-09-24
    for city in JP.CITIES:
        c = JP.CITIES[city]
        z = JP.SHARED_RAW / JP.N03_ZIP_TEMPLATE.format(pref=c["pref"])
        if not z.exists():
            continue
        n03 = JP._read_geojson(z, z.name.replace("_GML.zip", ".geojson"))
        n03 = n03[n03["N03_007"].isin(c["wards"])].dissolve(by="N03_007", aggfunc="first").reset_index()
        for _, row in n03.iterrows():
            wards[city][row["N03_005"] or row["N03_004"]]["stations"] = \
                st[st.geometry.within(row.geometry)]["N02_005"].nunique()
    return wards


def tokyo_completeness():
    """Tokyo food ward -> (earliest, latest) permit year across its files."""
    files = {S.MUNICIPALITIES[k][1]: [S.DATA / S.MUNICIPALITIES[k][2]] for k in TOKYO_NATIONAL}
    for k in ("taito", "setagaya", "meguro"):
        files[S.CITIES[k][1]] = [S.DATA / f for f in S.CITIES[k][2]]
    span = {}
    for ward, paths in files.items():
        years = []
        for path in paths:
            rows = list(J.city_rows(path))
            if rows and "廃業日" in rows[0]:
                rows = [r for r in rows if not (r.get("廃業日") or "").strip()]
            col = next((c for c in DATE_COLS if rows and c in rows[0] and any(year(r.get(c)) for r in rows)), None)
            years += [y for y in (year(r.get(col)) for r in rows) if y] if col else []
        span[ward] = (min(years), max(years)) if years else (None, None)
    return span


def yearbook():
    """Ward name -> 飲食店営業 in the yearbook's latest fiscal year; {} if not cached."""
    if not YEARBOOK.exists():
        return {}
    import csv
    import io
    rows = list(csv.reader(io.StringIO(J.decode(YEARBOOK.read_bytes()))))
    col = next(i for i, c in enumerate(rows[0]) if c.startswith("飲食店営業"))
    wards = [r for r in rows[1:] if len(r) > col and r[3].startswith("131") and r[3] != "13100"]
    latest = max(r[1] for r in wards)
    return {r[4]: int(r[col]) for r in wards if r[1] == latest}


def official():
    """City key -> 飲食店営業 permitted facilities, old law + revised law; {} if not cached."""
    if not (ESTAT_OLD.exists() and ESTAT_NEW.exists()):
        return {}
    import csv
    import io

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
    return {k: old[a] + new[a] for k, a in ESTAT_AREA.items() if a in old and a in new}


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "—"


def render(wards, span, yb, off):
    today = datetime.date.today().isoformat()
    L = [f"# 🇯🇵 Japan — cities and wards ({today})", "",
         "**Generated by `python scripts/japan_ward_table.py --write` from the data on disk. Do not edit by hand:** "
         "change the script's `STATUS` or the data, then regenerate. Republished on its own, apart from the banded "
         "master list (`docs/city_master_list.md`), at the owner's request (2026-09-24).", "",
         "- **Addresses**: every city is placed by matching permit addresses to MLIT's address points "
         "(`pipeline/countries/japan_register.py`). No geocoder.",
         "- **Buckets**: `japan_eigyo`. Japan publishes no general-retail register, so **Retail is food shops only**, "
         "bakeries and delis included (owner).",
         "- **Counts** are fixed-premises permit rows, before build-time de-duplication.",
         "- **Stations** are distinct N02 station names inside each ward. The Shinkansen and the Sagano scenic line "
         "are left out. \"—\" means that prefecture's N03 file is not cached.",
         "- **Of the official count**: every food-service row in the list, vehicles and stalls included, against "
         "飲食店営業 permits in force at 2025-03-31. The count comes from MHLW's 衛生行政報告例, old law plus revised "
         "law (for Tokyo's wards, Tokyo's yearbook, which equals it). The lists are dated 2026, so read about ±3%. "
         "✅ marks 90% or more. Credit: 「衛生行政報告例」（厚生労働省）を加工して作成.", "",
         "| City | Band | Wards | Food service | Food retail | Personal services | Of the official count "
         "| Placed at block | Stations | Order / status |", "|---|---|---|---|---|---|---|---|---|---|"]
    partial = {w for w, (lo, _) in span.items() if lo and lo >= 2021}
    for city, (name, band, status) in STATUS.items():
        ws = {w: v for w, v in wards[city].items() if w in ROMAJI[city]}
        tot = collections.Counter()
        for v in ws.values():
            tot.update(v)
        food_wards = [w for w, v in ws.items() if v["Food service"]]
        nw = (f"{len(food_wards)} food + {len(ws) - len(food_wards)} personal-services only"
              if city == "tokyo" else str(len(ws)))
        warn = " ⚠️" if city == "tokyo" and partial else ""
        extra = f". ⚠️ {len(partial)} partial food lists" if city == "tokyo" and partial else ""
        ps = f"{tot['Personal services']:,}" if tot["Personal services"] else "**0**, none published"
        stations = str(tot["stations"]) if any("stations" in v for v in ws.values()) else "—"
        if city == "tokyo":  # the food wards against their own yearbook counts
            fs_all = sum(v["fs_all"] for w, v in ws.items() if w in food_wards)
            count = sum(yb.get(w, 0) for w in food_wards)
        else:  # every row, vehicles and rows with no ward included
            fs_all, count = sum(v["fs_all"] for v in wards[city].values()), off.get(city)
        share = f"{'✅' if fs_all >= 0.9 * count else '⚠️'} **{100 * fs_all / count:.0f}%** of {count:,}" \
            if count else "—"
        L.append(f"| **{name}** | {band} | {nw} | **{tot['Food service']:,}**{warn} | {tot['Retail']:,} | {ps} "
                 f"| {share} | **{pct(tot['block'], tot['bucketed'])}** | {stations} | {status}{extra} |")
    for key, name, n, ps, status in GAP:
        count = f"no list; official {off[key]:,}" if key in off else "no list"
        L.append(f"| **{name}** | ⚠️ gap | {n} | no current list | — | {ps} | {count} | — | — | {status} |")
    for city, (name, band, _) in STATUS.items():
        ws = {w: v for w, v in wards[city].items() if w in ROMAJI[city]}
        has_st = any("stations" in v for v in ws.values())
        L += ["", f"### {name} — by ward", ""]
        head = "| Ward | Food service | Food retail | Personal services | Block |" + (" Stations |" if has_st else "")
        if city == "tokyo":
            head += " Of the official count | Food list |"
        L += [head, "|" + "---|" * (head.count("|") - 1)]
        order = sorted(ws.items(), key=lambda kv: (-kv[1]["Food service"], -kv[1]["Personal services"]))
        for w, v in order:
            if city == "tokyo" and not v["Food service"]:
                continue
            row = (f"| {ROMAJI[city][w]} | **{v['Food service']:,}** | {v['Retail']:,} | "
                   f"{v['Personal services']:,} | {pct(v['block'], v['bucketed'])} |")
            if has_st:
                row += f" {v.get('stations', '—')} |"
            if city == "tokyo":
                lo, hi = span.get(w, (None, None))
                share = v["fs_all"] / yb[w] if yb.get(w) else None
                mark = "✅" if share and share >= 0.9 else "⚠️"
                row += (f" {mark} **{100 * share:.0f}%** of {yb[w]:,} |" if share else " — |")
                row += (f" permits {lo}–{hi} only; " if w in partial else " ") + TOKYO_NOTE.get(w, "") + " |"
            L.append(row)
        if city == "tokyo":
            only = [(ROMAJI[city][w], v["Personal services"]) for w, v in order if not v["Food service"]]
            L += ["", "**Personal services only, outside the food scope:** "
                  + " · ".join(f"{n} {c:,}" for n, c in sorted(only, key=lambda x: -x[1])) + "."]
            L += ["", "**Of the official count**: each list's 飲食店 permit rows, vehicles included, against 飲食店営業 "
                  "in Tokyo's statistical yearbook, table 19-8, for the latest fiscal year. ✅ marks 90% or more. "
                  "**The wards differ because each is its own publisher.** "
                  "Some publish their own register, some an opt-in or consent-filtered export, and some a snapshot "
                  "never updated (`docs/build_briefs/tokyo.md`)."]
    stray = sum(v["bucketed"] for city in STATUS for w, v in wards[city].items() if w not in ROMAJI[city])
    L += ["", f"*{stray} rows had no ward in the address (or one outside the city) and are left out of the ward "
              "tables.*", ""]
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = render(measure(), tokyo_completeness(), yearbook(), official())
    print(text)
    if "--write" in sys.argv:
        OUT.write_bytes(text.encode("utf-8"))
        print(f"\nwrote {OUT.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
