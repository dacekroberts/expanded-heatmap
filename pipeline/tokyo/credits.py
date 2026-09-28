"""Tokyo's notice, BUILT from each source's own prescribed credit (the Tokyo
build handoff, item 3: eight wards, each its own publisher and licence form).

Every file the roster reads (pipeline/tokyo/wards.py) has an entry here, and
scripts/check_provenance.py refuses a roster file without one - so a ward
switched on later cannot reach the page uncredited. The forms are the ones the
licence reads recorded (docs/data_sources/japan.md, the Tokyo rows, read
2026-09-24):

  * catalogue - the Tokyo catalogue's ward files (Chuo, Minato, Shinjuku, Koto
    and the Minato, Taito and Shibuya registers): ONE combined notice naming
    the ward, the catalogue, the dataset title, its URL and the DATE OF USE,
    saying the data was processed, with the CC BY 4.0 link (Tokyo Open Data
    Terms §2).
  * shibuya - 渋谷区オープンデータ利用規約 §2's pattern for modified use.
  * taito - the ward's four elements: 台東区, CC-BY表示4.0国際 linked, its
    no-warranty sentence, the page URL, plus that the data was modified; a link
    says it goes to 台東区公式ホームページ.
  * setagaya - 世田谷区オープンデータ利用規約 §2's 「…改変して利用しています」 form.
  * meguro - each resource title (with its date), 目黒区, CC BY 4.0, that it was
    modified, and the catalogue link labelled 目黒区オープンデータカタログサイト.
  * mhlw - PDL 1.0: the source, that it was processed; the top page only (as
    Fukuoka's notice 54).

No imports: the deployed app reads this module (app/components.py), and it
must never touch data/ or the pipeline.
"""

CC_BY = "https://creativecommons.org/licenses/by/4.0/"
CC_BY_JA = "https://creativecommons.org/licenses/by/4.0/deed.ja"
CATALOGUE = "東京都オープンデータカタログサイト"
_CAT = "https://catalog.data.metro.tokyo.lg.jp/dataset/"

# The day the build used the catalogue's files - the date of use the Tokyo
# terms require. Set when the map is rebuilt from newly fetched files.
USED = "2026年9月28日"

# file (as in wards.py) -> (form, ward, title, dataset page)
SOURCES = {
    "13102/syokuhineigyoukyoka.csv": ("catalogue", "中央区", "食品等営業許可・届出一覧", _CAT + "t131024d0000000037"),
    "food_business_all.csv": ("catalogue", "港区", "食品営業許可一覧", _CAT + "t131032d0000000244"),
    "13103/riyou.csv": ("catalogue", "港区", "港区の理容所情報", _CAT + "t131032d0000000231"),
    "13103/biyou.csv": ("catalogue", "港区", "港区の美容所情報", _CAT + "t131032d0000000232"),
    "13103/cleaning.csv": ("catalogue", "港区", "港区のクリーニング所情報", _CAT + "t131032d0000000233"),
    "13104/000399975.csv": ("catalogue", "新宿区", "新宿区の食品等営業許可・届け出一覧", _CAT + "t131041d0000000124"),
    "13108/131083_015_food_business_all.csv": ("catalogue", "江東区", "食品等営業許可・届出一覧",
                                               _CAT + "t131083d0000000028"),
    "13106/131067_taitoku_riyousyo.csv": ("catalogue", "台東区", "理容所台帳", _CAT + "t131067d2025000006"),
    "13106/131067_taitoku_biyousyo.csv": ("catalogue", "台東区", "美容所台帳", _CAT + "t131067d2025000007"),
    "13106/131067_taitoku_cleaning.csv": ("catalogue", "台東区", "クリーニング所台帳", _CAT + "t131067d2025000005"),
    "13113/131130_shibuyaku_riyousyo.csv": ("catalogue", "渋谷区", "理容所台帳", _CAT + "t131130d2025000006"),
    "13113/131130_shibuyaku_biyousyo.csv": ("catalogue", "渋谷区", "美容所台帳", _CAT + "t131130d2025000007"),
    "13113/131130_shibuyaku_cleaning.csv": ("catalogue", "渋谷区", "クリーニング所台帳", _CAT + "t131130d2025000005"),
    "13113/131130_food_businesses_list.csv": (
        "shibuya", "渋谷区", "食品等営業許可・届出一覧",
        "https://city-shibuya-data.opendata.arcgis.com/datasets/e68f41ebfa5f4ea490ca9af701d44e02_0/about"),
    "13106/2026ALL-IND-CSV.csv": (
        # the page 食品衛生営業施設一覧, its section 食品営業許可施設一覧, the
        # link 業種順(CSV) (read 2026-09-28)
        "taito", "台東区", "食品営業許可施設一覧（業種順）",
        "https://www.city.taito.lg.jp/kenkohukusi/kenkokikikanrieisei/food/syokuhin-sisetu/index.html"),
    "13112/zenkenr080331.csv": ("setagaya", "世田谷区", "全件許可施設一覧(R080331)",
                                "https://www.city.setagaya.lg.jp/02245/online_tetsuzuki/3246.html"),
    "13110/all_new_8.csv": ("meguro", "目黒区", "食品衛生関係施設一覧　令和８年４月１日現在（新法）",
                            "https://data.bodik.jp/dataset/131105_food_business"),
    "13110/all_old_8.csv": ("meguro", "目黒区", "食品衛生関係施設一覧　令和８年４月１日現在（旧法）",
                            "https://data.bodik.jp/dataset/131105_food_business"),
    "13110/131105_barber_20260331.csv": ("meguro", "目黒区", "理容所　令和８年３月３１日現在",
                                         "https://data.bodik.jp/dataset/131105_barber"),
    "13110/131105_hairdressingshop_20260331.csv": ("meguro", "目黒区", "美容所　令和８年３月３１日現在",
                                                   "https://data.bodik.jp/dataset/131105_hairdressingshop"),
    "13110/131105_cleaning_20260331.csv": ("meguro", "目黒区", "クリーニング所　令和８年３月３１日現在",
                                           "https://data.bodik.jp/dataset/131105_cleaning_shop"),
}
# MHLW's slice for each of the four wards: one credit covers all four
MHLW_FILES = ("13102", "13103", "13104", "13108")
MEGURO_CATALOGUE = "https://odcs.bodik.jp/131105/"


def _link(url, text=None):
    return f"[{text or url}]({url})"


def notice():
    """The businesses part of Tokyo's notice, as markdown."""
    by = {}
    for f, (form, ward, title, page) in SOURCES.items():
        by.setdefault(form, []).append((ward, title, page))
    parts = []
    cat = "".join(f"「{t}」（{w}、{_link(p)}）" for w, t, p in by["catalogue"])
    parts.append(f"{cat}（{CATALOGUE}、{USED}利用、{_link(CC_BY, 'CC BY 4.0')}）を加工して作成")
    (w, t, p), = by["shibuya"]
    parts.append(f"「{t}」（{w}）（{_link(p)}）を加工して作成（{_link(CC_BY, 'CC BY 4.0')}）")
    (w, t, p), = by["taito"]
    parts.append(f"{w}「{t}」（{_link(p, '台東区公式ホームページ')}）、{_link(CC_BY_JA, 'CC-BY表示4.0国際')}。"
                 f"本作品の内容について、台東区は一切保証しないものとする。本プロジェクトが加工して作成")
    (w, t, p), = by["setagaya"]
    parts.append(f"この地図は以下の著作物を改変して利用しています。{t}、{w}、クリエイティブ・コモンズ・ライセンス "
                 f"表示4.0国際（{_link(CC_BY_JA)}）（{_link(p)}）")
    meg = "".join(f"「{t}」" for _w, t, _p in by["meguro"])
    parts.append(f"{meg}（目黒区、{_link(CC_BY, 'CC BY 4.0')}、{_link(MEGURO_CATALOGUE, '目黒区オープンデータカタログサイト')}）"
                 f"を改変して作成")
    parts.append("出典：「食品衛生申請等システム」（厚生労働省）（[https://i2fas.mhlw.go.jp/](https://i2fas.mhlw.go.jp/)）"
                 "の「食品等営業許可・届出一覧」（中央区、港区、新宿区、江東区）を加工して作成")
    return "; ".join(parts)
