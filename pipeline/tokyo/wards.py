"""Tokyo's 23 special wards: which are ON the map and from which files.

THE ONE PLACE A WARD IS SWITCHED ON (owner, 2026-09-28). Tokyo is 23
publishers, not one: each ward runs its own health centre and publishes its own
permit list, or does not. A ward is ACTIVE only with a full, current food list
(owner 2026-09-24; Meguro's first-permits list and Shinjuku's 2023 snapshot are
accepted exceptions, disclosed). An INACTIVE ward's stations are still drawn,
hollow and ringless, with a tooltip naming the ward (japan_step1, map_common):
the only way to say "no data here" when ward boundaries cannot be drawn (N03,
the Survey Act).

TO SWITCH A WARD ON when its data turns up (the tokyo-ward skill):
  1. Its ward card, complete, verdict ON (docs/build_briefs/tokyo.md).
  2. Here: "status": "active", its "food" files (and "personal", "mhlw" if
     any), "encoding", "operator_cols". Delete "why".
  3. `python pipeline/tokyo/fetch_sources.py isj` (its address files), then the
     three steps. check() below refuses a half-made switch.
Nothing else lists the active wards: japan.CITIES["tokyo"] reads them from
here, so its city line, fetch and share check follow.

Kept free of imports from the rest of the pipeline, so pipeline/countries/
japan.py can read it without a cycle.
"""
from pathlib import Path

RAW = Path(__file__).parent.parent.parent / "data" / "tokyo" / "raw"
MHLW = Path(__file__).parent.parent.parent / "data" / "mhlw" / "raw"

# code -> the ward. Paths are under data/tokyo/raw/ (RAW) unless absolute.
# Measured 2026-09-24 (the brief) and re-measured through the shared step 2 on
# 2026-09-28: share = the list's 飲食店 rows against the yearbook's count.
WARDS = {
    "13101": {"ja": "千代田区", "en": "Chiyoda", "status": "inactive",
              "why": "food list released only on request (request parked)"},
    "13102": {"ja": "中央区", "en": "Chūō", "status": "active",
              "food": ["13102/syokuhineigyoukyoka.csv"], "encoding": "cp932",
              "mhlw": MHLW / "13102_food_business_all.csv", "share_note": "permits of 2021-06 to 2022-12 only"},
    "13103": {"ja": "港区", "en": "Minato", "status": "active",
              "food": ["food_business_all.csv"], "encoding": "utf-8",
              "personal": {"barber": ["13103/riyou.csv"], "beauty": ["13103/biyou.csv"],
                           "laundry": ["13103/cleaning.csv"]},
              "mhlw": MHLW / "13103_food_business_all.csv", "share_note": "consent-filtered, new-law permits only"},
    "13104": {"ja": "新宿区", "en": "Shinjuku", "status": "active",
              "food": ["13104/000399975.csv"], "encoding": "utf-16",
              "mhlw": MHLW / "13104_food_business_all.csv", "share_note": "complete as of 2023-01-01 (its vintage)"},
    "13105": {"ja": "文京区", "en": "Bunkyō", "status": "inactive",
              "why": "publishes no food list in any format (re-probed 2026-09-28)"},
    "13106": {"ja": "台東区", "en": "Taitō", "status": "active",
              "food": ["13106/2026ALL-IND-CSV.csv"], "encoding": "cp932",
              "personal": {"barber": ["13106/131067_taitoku_riyousyo.csv"],
                           "beauty": ["13106/131067_taitoku_biyousyo.csv"],
                           "laundry": ["13106/131067_taitoku_cleaning.csv"]},
              "share_note": "premises that opted out are left out"},
    "13107": {"ja": "墨田区", "en": "Sumida", "status": "inactive",
              "why": "new permits only, as PDF (re-checked 2026-09-28)"},
    "13108": {"ja": "江東区", "en": "Kōtō", "status": "active",
              "food": ["13108/131083_015_food_business_all.csv"], "encoding": "utf-8",
              "mhlw": MHLW / "13108_food_business_all.csv", "share_note": "consent-only new permits, 2021-06 to 2022-11"},
    "13109": {"ja": "品川区", "en": "Shinagawa", "status": "inactive",
              "why": "partial list, since 2024-04 only (re-checked 2026-09-28)"},
    "13110": {"ja": "目黒区", "en": "Meguro", "status": "active",
              "food": ["13110/all_new_8.csv", "13110/all_old_8.csv"], "encoding": "utf-8",
              "personal": {"barber": ["13110/131105_barber_20260331.csv"],
                           "beauty": ["13110/131105_hairdressingshop_20260331.csv"],
                           "laundry": ["13110/131105_cleaning_20260331.csv"]},
              "share_note": "first permits only (owner: ships at its measured share)"},
    "13111": {"ja": "大田区", "en": "Ōta", "status": "inactive",
              "why": "full list as PDF only; the site policy bars reuse (owner 2026-09-28)"},
    "13112": {"ja": "世田谷区", "en": "Setagaya", "status": "active",
              "food": ["13112/zenkenr080331.csv"], "encoding": "cp932",
              "share_note": "premises that opted out are left out"},
    "13113": {"ja": "渋谷区", "en": "Shibuya", "status": "active",
              "food": ["13113/131130_food_businesses_list.csv"], "encoding": "utf-8",
              "personal": {"barber": ["13113/131130_shibuyaku_riyousyo.csv"],
                           "beauty": ["13113/131130_shibuyaku_biyousyo.csv"],
                           "laundry": ["13113/131130_shibuyaku_cleaning.csv"]},
              "mhlw": MHLW / "13113_food_business_all.csv", "share_note": "the ward's own register"},
    "13114": {"ja": "中野区", "en": "Nakano", "status": "inactive",
              "why": "list stale, to 2023-06-27 (re-checked 2026-09-28; the portal's 2026 label is wrong)"},
    "13115": {"ja": "杉並区", "en": "Suginami", "status": "inactive",
              "why": "publishes no food list in any format (re-probed 2026-09-28)"},
    "13116": {"ja": "豊島区", "en": "Toshima", "status": "inactive",
              "why": "food list only for viewing in person"},
    "13117": {"ja": "北区", "en": "Kita", "status": "inactive",
              "why": "full list as PDF, stated not to be open data; the site terms bar reuse; the open CSV holds 52 permits, 2022-24"},
    "13118": {"ja": "荒川区", "en": "Arakawa", "status": "inactive",
              "why": "full list as PDF only; the site terms bar all reuse"},
    "13119": {"ja": "板橋区", "en": "Itabashi", "status": "inactive",
              "why": "partial list, since 2025-04 only (re-checked 2026-09-28)"},
    "13120": {"ja": "練馬区", "en": "Nerima", "status": "inactive",
              "why": "food list released only on application"},
    "13121": {"ja": "足立区", "en": "Adachi", "status": "inactive",
              "why": "new permits only, as PDF (re-checked 2026-09-28)"},
    "13122": {"ja": "葛飾区", "en": "Katsushika", "status": "inactive",
              "why": "publishes no food list in any format (re-probed 2026-09-28)"},
    "13123": {"ja": "江戸川区", "en": "Edogawa", "status": "inactive",
              "why": "food list released only on application"},
}

# MHLW's slice is added to these four only (owner 2026-09-24); Shibuya's list is
# complete, so its "mhlw" file above is kept for reference and not read.
MHLW_WARDS = ("13102", "13103", "13104", "13108")


def check():
    """Refuse a roster a half-made switch left inconsistent."""
    problems = []
    if len(WARDS) != 23 or sorted(WARDS) != [f"131{n:02d}" for n in range(1, 24)]:
        problems.append("the roster must hold exactly the 23 special wards, 13101-13123")
    for code, w in WARDS.items():
        if w["status"] not in ("active", "inactive"):
            problems.append(f"{code}: status {w['status']!r}")
        elif w["status"] == "active":
            if not w.get("food"):
                problems.append(f"{code} {w['ja']}: active with no food files")
            if w.get("why"):
                problems.append(f"{code} {w['ja']}: active, but still says why it is off")
            for f in w.get("food", []) + [p for ps in w.get("personal", {}).values() for p in ps]:
                if not (RAW / f).exists():
                    problems.append(f"{code} {w['ja']}: missing {RAW / f} (run fetch_sources.py)")
        elif w.get("food") or w.get("personal"):
            problems.append(f"{code} {w['ja']}: inactive, but lists files - switch it on or remove them")
        elif not w.get("why"):
            problems.append(f"{code} {w['ja']}: inactive with no reason for the tooltip and the page")
    for code in MHLW_WARDS:
        if WARDS[code]["status"] != "active":
            problems.append(f"{code}: MHLW's slice is for an active ward only")
    if problems:
        raise SystemExit("pipeline/tokyo/wards.py:\n  " + "\n  ".join(problems))


ACTIVE = {c: w for c, w in WARDS.items() if w["status"] == "active"}
ACTIVE_CODES = list(ACTIVE)
# code -> English name: japan_step1's NO_DATA_WARDS
NO_DATA_WARDS = {c: w["en"] for c, w in WARDS.items() if w["status"] == "inactive"}
