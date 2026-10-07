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
# ("food", "barber", "beauty", "laundry", "coinlaundry"), and decides Personal
# services. Coin laundries count (owner 2026-09-28: near transit they draw
# steady short-term customers); Sapporo is the first city to publish them.
# `form` is the list's 業態 where it has one (Fukuoka's two lists; empty
# elsewhere): see FORM_RULES.
EXTRA_COLUMNS = ("source", "form")
PERSONAL_SOURCES = {"barber", "beauty", "laundry", "coinlaundry"}

# Two patterns shared by RULES (the type) and FORM_RULES (the 業態), both
# (owner, 2026-09-29) - see their entries in RULES.
_HOSTESS = r"キャバレー|キャバクラ|スナック(?!菓子)"
_CATERING = r"仕出"

# (rule name, bucket or None, pattern) - searched in the NORMALISED value.
RULES = [
    # --- not a premises, or not a storefront: above everything they overlap
    # Kawasaki's 飲食店（給食施設） and 飲食店（学校給食炊飯） (Japan wave 2,
    # 2026-10-03): ^給食 misses them inside the bracket
    ("institutional catering", None, r"集団給食|^給食|飲食給食|給食施設|給食炊飯"),
    ("vending machine", None, r"自動販売機|自販|コップ式|全自動調理機"),
    # Kawasaki's 飲食店（短期営業）. 自動車以外 ("other than a vehicle", the Tama
    # ledgers' 野菜果物販売業(自動車以外): 1,063 rows) is not a vehicle (the Japan
    # foundation, 2026-10-07; no built city's type carries it)
    ("temporary / mobile", None, r"行商|露店|仮設|臨時|期間申請|屋形船|自動車(?!以外)|営業とみなされない|短期営業"),
    ("mail order", None, r"通信販売|訪問販売|通信訪問"),
    # Takamatsu's 業態 ラブホ・カプセル (2026-10-03): love and capsule hotels
    ("inside accommodation", None, r"旅館|ホテル|ラブホ|カプセル"),
    # Kawasaki's 飲食店（まあじゃん屋等）: the kana spelling of 麻雀
    ("entertainment venue", None, r"カラオケ|麻雀|まあじゃん|遊技場|ネットカフェ|漫画喫茶"),
    # Adult and hostess venues off every map (owner, 2026-09-29): Tokyo's
    # permit sub-type バー・キャバレー (bars filed with cabarets, one sub-type)
    # and the snack bar, a hostess-staffed bar. Plain バー stays: it names
    # no hostess. Not スナック菓子 (snack foods, a confectioner's product).
    ("hostess venue: cabaret / snack bar", None, _HOSTESS),
    # Food with no counter of its own (owner, 2026-09-29): 仕出し is catering
    # delivered to homes, offices and events (Tokyo's 飲食店営業（仕出し）,
    # Meguro's 飲食仕出, Fukuoka's 業態 仕出し).
    ("event catering (仕出し)", None, _CATERING),
    # --- Retail, food only (the owner's two manufacturing types come first,
    #     because they would otherwise fall to the manufacturing exclusion)
    ("konbini holding a restaurant permit", "Retail", r"コンビニ"),
    # Japan wave 2 (2026-10-03): a deli on a restaurant permit, Kawasaki's
    # 飲食店（そうざい店） (301) as the そう菜店 already here, and Nara's old-law
    # そうざい屋 where it leads the sub-types (そうざい屋・弁当屋; 軽飲食・そうざい屋
    # is a restaurant). 複合型そうざい製造業, a deli under the 2021 permit
    # law's combined type, counts too (owner, 2026-10-04; DECISIONS).
    ("deli (owner: そうざい counts)", "Retail", r"^(複合型そうざい製造|そうざい製造|惣菜製造|飲食惣菜|そうざい屋)|そう菜店|そうざい店"),
    # Nara's old-law 簡易菓子製造業
    ("confectioner / bakery (owner: 菓子 counts)", "Retail", r"^(簡易)?菓子"),
    ("butcher", "Retail", r"^(食肉販売|肉販)"),
    ("fishmonger", "Retail", r"^(魚介類販売|魚販)"),
    ("dairy", "Retail", r"^(乳類販売|乳販)"),
    ("greengrocer", "Retail", r"^野菜果物販売"),
    # Kawaguchi's list also writes 米殻類販売 (殻 for 穀; 28 rows; no built city)
    ("rice", "Retail", r"^米[穀殻]類販売"),
    ("department store / supermarket", "Retail", r"百貨店|スーパー"),
    ("bento shop", "Retail", r"^弁当販売"),
    ("other food and drink sales", "Retail", r"その他の食料・飲料販売|^他食販(店舗|包装)"),
    # --- Food service
    # Fukui's old-law permits spell the type short, 飲食店 and 喫茶店 (93
    # restaurants, 2026-10-02): without the whole-value forms they fell to "no rule"
    # Japan wave 2 (2026-10-03): Kawasaki's 飲食店（sub-type） (飲食店（一般食堂）
    # 3,577, 飲食店（大衆酒場）989: none bucketed without it), its carve-outs
    # above; Nara's old-law list files a restaurant by its sub-type alone
    # (軽飲食, 一般食堂, 居酒屋 ... 455 restaurants in term), the first listed
    # deciding a combination
    ("restaurant", "Food service", r"飲食店営業|^飲食(一般|バー|すし|そば|弁当|簡易|喫茶)|^飲食店$|^飲食店\(|"
                                   r"^(軽飲食|一般食堂|居酒屋|めん類食堂|弁当屋|レストラン|お好焼屋|焼肉屋|すし屋|"
                                   r"中華料理店|たこ焼屋|スタンド|調理パン)"),
    ("café", "Food service", r"喫茶店営業|^喫茶店舗|^喫茶店$"),
]
_COMPILED = [(name, bucket, re.compile(pat)) for name, bucket, pat in RULES]

# 業態, the form of business, read BESIDE the type (Fukuoka, 2026-09-28). The
# other lists fold it into the type (Kobe's 飲食店営業（旅館・ホテル）); Fukuoka's
# city list and MHLW's open data keep it in its own column, often free text
# (607 distinct values in MHLW's Fukuoka file), and only there are vehicles,
# stalls, school kitchens and staff canteens marked. These rules sort the
# filer's own words into the categories RULES already applies to types. They
# run only on a row its type put in a bucket - a form never brings a
# manufacturing or vending row IN - and the first match wins.
FORM_RULES = [
    # A temporary stall is not a yatai: Tokyo's MHLW rows file a festival
    # stall as 臨時設置屋台 (亀戸, 2026-09-28), so the temporary words win.
    # 露店 (a street stall) joined on 2026-09-29: RULES already excluded it as a
    # type, and about 34 restaurant permits carried it as their form (owner,
    # DECISIONS "Category check: the owner's calls"). Fukuoka's ろ店 is not it.
    ("temporary / mobile", None, r"仮設|臨時|短期|期間限定|季節的|イベント|催事|祭|マルシェ|出店|自動車(?!以外)|"
                                 r"キッチンカー|移動|行商|列車|屋形船|海の家|露店"),
    # Fukuoka's 屋台, filed as ろ店 / 定置屋台: stalls at fixed street spots
    # (Nakasu's 清流公園, Tenjin, Nagahama) on permits running to 2032 under
    # the city's 屋台基本条例 - not a festival stall. They COUNT (owner
    # 2026-09-28; 81 in Fukuoka). Tokyo has no ろ店; its two 屋台 rows are
    # fixed bento stalls in office plazas (京橋, 六本木; MHLW, 2026-09-28).
    ("yatai: a fixed street stall (Fukuoka's 屋台)", "Food service", r"ろ店|屋台"),
    # 事業場食堂 / 事業所食堂, a workplace canteen: Matsuyama's old-law 業態
    # (22 rows, 2026-10-02), as 社員食堂 elsewhere
    ("institutional catering", None, r"給食|社員食堂|職員食堂|会社食堂|学生食堂|学校食堂|寮食堂|老人ホーム|福祉施設|"
                                     r"栄養管理室|病院|保育園|幼稚園|小学校|事業場食堂|事業所食堂"),
    ("inside accommodation", None, r"旅館|ホテル|ラブホ|カプセル"),
    ("entertainment venue", None, r"カラオケ|麻雀|遊技場|ネットカフェ|漫画喫茶"),
    # (owner, 2026-09-29) the same two rules as RULES, in the filer's words:
    # Tokyo's バー・キャバレー / 一般・スナック, Fukuoka's スナック、バー.
    ("hostess venue: cabaret / snack bar", None, _HOSTESS),
    ("event catering (仕出し)", None, _CATERING),
    ("vending machine", None, r"自動販売機|自販機|置き菓子"),
    ("mail order", None, r"通信販売|訪問販売|ネット販売|インターネット販売|ネットショップ|オンラインショップ"),
    # Kobe's konbini rule, as a form: a konbini or supermarket holding a
    # restaurant permit is a shop
    ("konbini holding a restaurant permit", "Retail", r"コンビニ"),
    ("department store / supermarket", "Retail", r"百貨店|スーパー"),
    # A deli by its 業態 alone, a restaurant permit filed as 総菜屋, 惣菜店 or
    # そうざい屋 (owner, 2026-10-04; DECISIONS): a shop, as the deli types are.
    ("deli (業態; owner: そうざい counts)", "Retail", r"総菜|惣菜|そうざい|そう菜"),
]
_FORM_COMPILED = [(name, bucket, re.compile(pat)) for name, bucket, pat in FORM_RULES]


def normalise(value):
    """NFKC (full-width, circled numbers), no spaces, no leading number, and no
    leading （旧） (Higashiosaka's national-schema list marks an old-law permit
    so, （旧）菓子製造業: without it the anchored Retail rules dropped 108 rows in
    term, 2026-10-03). The Japan foundation (2026-10-07), neither on any built
    city's type: the Saitama layers' `01:` code with its colon (Ageo's Retail
    read 369 rows with it, 658 without), and the `?` Ōita's cp932 export leaves
    for a circled number above ⑳ (`? そうざい製造業`: 116 delis fell to no rule)."""
    s = unicodedata.normalize("NFKC", str(value or "")).replace(" ", "").replace("　", "")
    return re.sub(r"^\(旧\)", "", re.sub(r"^(?:\d+:?|\?)", "", s))


def explain(value, source="food", form=""):
    """(bucket or None, the rule that decided it, or 'no rule')."""
    bucket, rule = _explain_type(value, source)
    # a CSV round trip reads an empty form as NaN
    f = normalise(form) if isinstance(form, str) else ""
    if bucket is None or not f or source in PERSONAL_SOURCES:
        return bucket, rule
    for name, b, pat in _FORM_COMPILED:
        if pat.search(f):
            return b, f"{name} (業態)"
    return bucket, rule


def _explain_type(value, source):
    if source in PERSONAL_SOURCES:
        if "無店舗" in str(value or ""):
            return None, "storeless pick-up (not a premises)"
        if "移動" in str(value or ""):  # Kobe's 移動美容室: a salon in a vehicle
            return None, "mobile salon (not a premises)"
        # Sapporo's 厚生施設理容所 / 厚生施設美容所: a barber or salon inside a
        # hospital or care home, for its residents - not open to the public,
        # as institutional catering is not (2026-09-28; 16 rows). Meguro's
        # register spells it 厚生 alone in 施設（種別）等 (Tokyo, 2 rows).
        if "厚生施設" in str(value or "") or normalise(value) == "厚生":
            return None, "welfare-facility salon (not open to the public)"
        # Osaka's laundry register: リネンサプライ (towel, oshibori and hospital
        # linen suppliers, many named 工場) is industrial, not a counter; owner
        # 2026-09-27. 一般リネン兼業 (a general laundry that also does linen) stays.
        # Taitō's register spells it リネン alone (Tokyo, 1 row).
        if source == "laundry" and normalise(value).startswith("リネン"):
            return None, "linen supply (industrial, not a counter)"
        return "Personal services", f"{source} register"
    v = normalise(value)
    for name, bucket, pat in _COMPILED:
        if pat.search(v):
            return bucket, name
    return None, "no rule"  # manufacturing, catch-alls: out, and measured


def classify(row):
    return explain(row.get(VALUE_COLUMN), row.get("source") or "food", row.get("form") or "")[0]


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
                  ("そうざい製造業", "Retail"), ("複合型そうざい製造業", "Retail"), ("複合型冷凍食品製造業", None),
                  ("⑬ その他の食料・飲料販売業", "Retail"),
                  # Japan wave 2: Kawasaki's 飲食店（sub-type） and its carve-outs; Nara's old-law sub-types
                  ("飲食店（一般食堂）", "Food service"), ("飲食店（バー）", "Food service"),
                  ("飲食店（給食施設）", None), ("飲食店（学校給食炊飯）", None), ("飲食店（まあじゃん屋等）", None),
                  ("飲食店（短期営業）", None), ("飲食店（屋台型臨時営業）", None), ("飲食店（仕出し屋）", None),
                  ("飲食店（自動車（タンク容量80リットル））", None), ("飲食店（そうざい店）", "Retail"),
                  ("飲食店（弁当屋）", "Food service"), ("軽飲食", "Food service"), ("一般食堂・弁当屋", "Food service"),
                  ("一般食堂・仕出し屋", None), ("そうざい屋", "Retail"), ("そうざい屋・弁当屋", "Retail"),
                  ("軽飲食・そうざい屋", "Food service"), ("旅館・一般食堂", None), ("簡易菓子製造業", "Retail"),
                  ("第１種自動車飲食店営業", None), ("簡易飲食店営業（自動販売機）", None), ("スナック", None),
                  ("（旧）菓子製造業", "Retail"), ("（旧）飲食店営業", "Food service"), ("（旧）飲食店営業（自動車）", None),
                  ("⑫ 自動販売機による販売業（…）", None), ("コップ式自動販売機", None), ("食肉処理業", None),
                  ("喫茶店営業（自動販売機）", None), ("他食販自販", None), ("乳販自販", None),
                  ("飲食店", "Food service"), ("喫茶店", "Food service"), ("飲食店（自動車）", None),
                  # the Japan foundation: 自動車以外 is no vehicle; the Saitama code, Ōita's lost number, 殻 for 穀
                  ("野菜果物販売業(自動車以外)", "Retail"), ("弁当販売業（自動車以外）", "Retail"),
                  ("01:飲食店営業", "Food service"), ("11：菓子製造業", "Retail"), ("? そうざい製造業", "Retail"),
                  ("米殻類販売業", "Retail"), ("弁当販売業（自動車）", None)):
    assert classify({VALUE_COLUMN: _v}) == _want, (_v, classify({VALUE_COLUMN: _v}), _want)
assert classify({VALUE_COLUMN: "取次所", "source": "laundry"}) == "Personal services"
assert classify({VALUE_COLUMN: "無店舗取次店", "source": "laundry"}) is None
assert classify({VALUE_COLUMN: "移動美容室", "source": "beauty"}) is None
assert classify({VALUE_COLUMN: "リネンサプライ", "source": "laundry"}) is None
assert classify({VALUE_COLUMN: "一般リネン兼業", "source": "laundry"}) == "Personal services"
assert classify({VALUE_COLUMN: "コインランドリー", "source": "coinlaundry"}) == "Personal services"
assert classify({VALUE_COLUMN: "厚生施設美容所", "source": "beauty"}) is None
assert classify({VALUE_COLUMN: "厚生", "source": "barber"}) is None
assert classify({VALUE_COLUMN: "リネン", "source": "laundry"}) is None
assert classify({VALUE_COLUMN: "一般理容所", "source": "barber"}) == "Personal services"
# 業態 (Fukuoka): a form excludes, or makes a restaurant a shop, but never brings a row in
for _v, _f, _want in (("① 飲食店営業", "自動車200L", None), ("① 飲食店営業", "仮設営業（季節的営業）", None),
                      ("① 飲食店営業", "学校給食", None), ("① 飲食店営業", "社員食堂", None),
                      ("飲食店営業", "事業場食堂", None),
                      ("飲食店営業", "旅館", None), ("① 飲食店営業", "コンビニエンスストア", "Retail"),
                      ("① 飲食店営業", "居酒屋", "Food service"), ("① 飲食店営業", float("nan"), "Food service"),
                      ("⑪ 百貨店、総合スーパー", "ドラッグストア", "Retail"), ("食肉処理業", "スーパー", None),
                      ("⑤ コップ式自動販売機（自動洗浄・屋内設置）", "カフェ", None)):
    assert classify({VALUE_COLUMN: _v, "form": _f}) == _want, (_v, _f, classify({VALUE_COLUMN: _v, "form": _f}))
# (owner, 2026-09-29) hostess venues and 仕出し catering go, by type or by 業態;
# a plain bar, a wine bar and a snack-food confectioner stay.
for _v, _f, _want in (("飲食店営業（バー・キャバレー）", "", None), ("飲食店営業（一般・スナック）", "", None),
                      ("飲食店営業", "バー・キャバレー", None), ("飲食店営業", "一般・スナック", None),
                      ("① 飲食店営業", "スナック、バー", None), ("飲食店営業（仕出し）", "", None),
                      ("飲食仕出", "", None), ("飲食店営業", "仕出し・定期", None),
                      ("飲食店営業", "バー", "Food service"), ("① 飲食店営業", "ワインバー", "Food service"),
                      ("飲食バー", "", "Food service"), ("飲食店営業", "一般・食堂", "Food service"),
                      ("菓子製造業", "スナック菓子", "Retail"), ("菓子製造業（スナック菓子）", "", "Retail"),
                      # (owner, 2026-09-29) a 露店 form is a street stall; Fukuoka's ろ店 yatai stay
                      ("① 飲食店営業", "露店", None), ("① 飲食店営業", "ろ店", "Food service"),
                      ("① 飲食店営業", "定置屋台", "Food service"),
                      # Japan wave 2: Yokosuka's 詳細業種 and Sasebo's 種目 read as the form
                      ("飲食店営業", "総菜屋", "Retail"), ("飲食店営業", "旅館の経営を兼ねる飲食店営業", None), ("飲食店営業", "屋台型臨時営業", None),
                      ("飲食店営業", "自動車による営業(タンク容量80リットル)", None), ("喫茶店営業", "自動販売機", None),
                      ("飲食店営業", "飲食店（客席を設ける営業）", "Food service"), ("飲食店営業", "露店：定置", None)):
    assert classify({VALUE_COLUMN: _v, "form": _f}) == _want, (_v, _f, classify({VALUE_COLUMN: _v, "form": _f}))
