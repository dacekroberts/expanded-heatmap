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
    "osaka": ("Osaka", "🟢 A", "Builds 1st"),
    "kobe": ("Kobe", "🟢 A", "2nd"),
    "sapporo": ("Sapporo", "🟢 A", "3rd. Grid addresses resolve to the 条丁目 block, about 100 m"),
    "fukuoka": ("Fukuoka", "🟢 A", "4th. Includes MHLW's addressed rows; about 20% of restaurants withhold their address"),
    "kyoto": ("Kyoto", "🟢 A", "5th. Rebuilt register: an upper bound"),
    "tokyo": ("Tokyo (8 wards)", "🟢 A", "6th, last. Chiyoda missing"),
    "hiroshima": ("Hiroshima", "🟣 C", "Food only: no personal-services list is published"),
    "sendai": ("Sendai", "🔴 D", "Needs the city's permission; letter drafted, not sent"),
}
GAP_ROWS = [  # no data on disk: status only
    "| **Yokohama** | ⚠️ gap | 18 | no current list | — | complete (2026-04-01) | — | — | "
    "Only 2,912 restaurants online (MHLW's opt-in slice). A request to the city |",
    "| **Nagoya** | ⚠️ gap | 16 | no full list | — | beauty list only | — | — | "
    "BODIK keeps only 12 months of new permits. A request to the city |",
]
TOKYO_NOTE = {"新宿区": "as of 2023 (disclosed)", "目黒区": "new-law and old-law lists"}

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
            if p["mobile"]:
                continue
            b = T.classify({"permit_type": p["type"], "source": source})
            if b:
                w = wards[city][ward_of(p)]
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


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "—"


def render(wards, span):
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
         "are left out. \"—\" means that prefecture's N03 file is not cached.", "",
         "| City | Band | Wards | Food service | Food retail | Personal services | Placed at block | Stations "
         "| Order / status |", "|---|---|---|---|---|---|---|---|---|"]
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
        L.append(f"| **{name}** | {band} | {nw} | **{tot['Food service']:,}**{warn} | {tot['Retail']:,} | {ps} "
                 f"| **{pct(tot['block'], tot['bucketed'])}** | {stations} | {status}{extra} |")
    L += GAP_ROWS
    for city, (name, band, _) in STATUS.items():
        ws = {w: v for w, v in wards[city].items() if w in ROMAJI[city]}
        has_st = any("stations" in v for v in ws.values())
        L += ["", f"### {name} — by ward", ""]
        head = "| Ward | Food service | Food retail | Personal services | Block |" + (" Stations |" if has_st else "")
        if city == "tokyo":
            head += " Food list |"
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
                row += (f" ⚠️ **permits {lo}–{hi} only**" if w in partial else " ✅ complete") \
                    + (f", {TOKYO_NOTE[w]}" if w in TOKYO_NOTE else "") + " |"
            L.append(row)
        if city == "tokyo":
            only = [(ROMAJI[city][w], v["Personal services"]) for w, v in order if not v["Food service"]]
            L += ["", "**Personal services only, outside the food scope:** "
                  + " · ".join(f"{n} {c:,}" for n, c in sorted(only, key=lambda x: -x[1])) + "."]
            if partial:
                L += ["", "⚠️ **A partial list** holds only permits from 2021 on, the post-reform half. Its old-law "
                      "permits still in term are missing, so that ward is an undercount until its other half is found "
                      "(`docs/build_briefs/tokyo.md`)."]
    stray = sum(v["bucketed"] for city in STATUS for w, v in wards[city].items() if w not in ROMAJI[city])
    L += ["", f"*{stray} rows had no ward in the address (or one outside the city) and are left out of the ward "
              "tables.*", ""]
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = render(measure(), tokyo_completeness())
    print(text)
    if "--write" in sys.argv:
        OUT.write_bytes(text.encode("utf-8"))
        print(f"\nwrote {OUT.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
