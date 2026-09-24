"""Japan's permit types (営業の種類) - shared by every Japanese city.

Japan has no general business licence, so its buckets come from two kinds of
register: **food-hygiene permits** (食品衛生法; each city's own list, or MHLW's
open data), which give Food service and a FOOD-ONLY Retail bucket; and the
**生活衛生 registers** (理容所 / 美容所 / クリーニング所), which give Personal
services by which register a row came from. **No general retail anywhere** -
Japan's ceiling, stated on every page (`layer_label` says so too).

**One module for every format.** The same national permit types arrive
spelled ten ways: plain (`飲食店営業`), numbered (MHLW's and Hiroshima's
`① 飲食店営業` -> `1 飲食店営業` after NFKC), with a sub-type
(`飲食店営業（一般・居酒屋）`, Taitō), or abbreviated (Meguro's `飲食一般`,
`他食販店舗`). Measured 2026-09-24 over 289 distinct values and 229,504 fixed
premises across the ten screened lists (`scripts/screen_japan_join.py`).

**Owner's calls, 2026-09-24:** 菓子製造業 (bakeries, confectioners) and
そうざい製造業 (delis) COUNT, as Retail - they sell over a counter. Their
factory / central-kitchen share is measured from trade names at build.
Food retail NOTIFICATIONS (届出: konbini, supermarkets, greengrocers...) count
where a list publishes them, disclosed as a partial bucket (Tokyo's rule).

Rules run in order and the first match wins, so every exclusion sits ABOVE
the broad bucket it carves out of (飲食店営業（旅館・ホテル） before 飲食店営業).
"""
import re
import unicodedata

FIELD_LABEL = "Permit type (営業の種類)"
VALUE_COLUMN = "permit_type"
# the 生活衛生 registers carry no food-permit type: `source` names the register
# ("food", "barber", "beauty", "laundry"), and decides Personal services.
EXTRA_COLUMNS = ("source",)
PERSONAL_SOURCES = {"barber", "beauty", "laundry"}

# (rule name, bucket or None, pattern) - searched in the NORMALISED value.
RULES = [
    # --- not a premises, or not a storefront: above everything they overlap
    ("institutional catering", None, r"集団給食|^給食|飲食給食"),
    ("vending machine", None, r"自動販売機|自販|コップ式|全自動調理機"),
    ("temporary / mobile", None, r"行商|露店|仮設|臨時|期間申請|屋形船|自動車|営業とみなされない"),
    ("mail order", None, r"通信販売|訪問販売|通信訪問"),
    ("inside accommodation", None, r"旅館|ホテル"),
    ("entertainment venue", None, r"カラオケ|麻雀|遊技場|ネットカフェ|漫画喫茶"),
    # --- Retail, food only (the owner's two manufacturing types come first,
    #     because they would otherwise fall to the manufacturing exclusion)
    ("konbini holding a restaurant permit", "Retail", r"コンビニ"),
    ("deli (owner: そうざい counts)", "Retail", r"^(そうざい製造|惣菜製造|飲食惣菜)|そう菜店"),
    ("confectioner / bakery (owner: 菓子 counts)", "Retail", r"^菓子"),
    ("butcher", "Retail", r"^(食肉販売|肉販)"),
    ("fishmonger", "Retail", r"^(魚介類販売|魚販)"),
    ("dairy", "Retail", r"^(乳類販売|乳販)"),
    ("greengrocer", "Retail", r"^野菜果物販売"),
    ("rice", "Retail", r"^米穀類販売"),
    ("department store / supermarket", "Retail", r"百貨店|スーパー"),
    ("bento shop", "Retail", r"^弁当販売"),
    ("other food and drink sales", "Retail", r"その他の食料・飲料販売|^他食販(店舗|包装)"),
    # --- Food service
    ("restaurant", "Food service", r"飲食店営業|^飲食(一般|バー|すし|そば|弁当|簡易|喫茶|仕出)"),
    ("café", "Food service", r"喫茶店営業|^喫茶店舗"),
]
_COMPILED = [(name, bucket, re.compile(pat)) for name, bucket, pat in RULES]


def normalise(value):
    """NFKC (full-width, circled numbers), no spaces, no leading number."""
    s = unicodedata.normalize("NFKC", str(value or "")).replace(" ", "").replace("　", "")
    return re.sub(r"^\d+", "", s)


def explain(value, source="food"):
    """(bucket or None, the rule that decided it, or 'no rule')."""
    if source in PERSONAL_SOURCES:
        if "無店舗" in str(value or ""):
            return None, "storeless pick-up (not a premises)"
        return "Personal services", f"{source} register"
    v = normalise(value)
    for name, bucket, pat in _COMPILED:
        if pat.search(v):
            return bucket, name
    return None, "no rule"  # manufacturing, catch-alls: out, and measured


def classify(row):
    return explain(row.get(VALUE_COLUMN), row.get("source") or "food")[0]


def legend_label(bucket):
    return {"Retail": "Food retail (no general retail is published)"}.get(bucket, bucket)


def layer_label(bucket):
    return {"Retail": "Food shops"}.get(bucket, bucket)


# Import-time checks: the rules' ORDER is the design, so pin the cases that
# depend on it (as Brazil's CNEFE module pins its own).
for _v, _want in (("飲食店営業", "Food service"), ("① 飲食店営業", "Food service"),
                  ("飲食店営業（一般・居酒屋）", "Food service"), ("飲食店営業（旅館・ホテル）", None),
                  ("飲食店営業（集団給食）", None), ("飲食店営業（一般・コンビニ）", "Retail"),
                  ("飲食店営業（一般・カラオケ）", None), ("飲食給食", None), ("飲食一般", "Food service"),
                  ("菓子製造業", "Retail"), ("菓子製造業（期間申請）", None), ("⑪ 菓子製造業", "Retail"),
                  ("そうざい製造業", "Retail"), ("複合型そうざい製造業", None), ("⑬ その他の食料・飲料販売業", "Retail"),
                  ("⑫ 自動販売機による販売業（…）", None), ("コップ式自動販売機", None), ("食肉処理業", None),
                  ("喫茶店営業（自動販売機）", None), ("他食販自販", None), ("乳販自販", None)):
    assert classify({VALUE_COLUMN: _v}) == _want, (_v, classify({VALUE_COLUMN: _v}), _want)
assert classify({VALUE_COLUMN: "取次所", "source": "laundry"}) == "Personal services"
assert classify({VALUE_COLUMN: "無店舗取次店", "source": "laundry"}) is None
