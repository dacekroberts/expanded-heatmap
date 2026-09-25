"""Seoul: Korea's LOCALDATA permit registers, one file per permit type.

The bucket keys on the PERMIT TYPE (the file, `oa`), where there is no catch-all:
every file is one named type, so 일반음식점's `기타` (17.7% of its active rows)
and 휴게음식점's `기타 휴게음식점` (20.4%) stay in Food service whatever they
are. The sub-type (`subtype`: 업태구분명, or 위생업태명 where a file has only
that) is used only to take rows out or move them - premises-taxonomy's
catch-all measurement, recorded in the brief and DECISIONS.md.

The owner's calls (2026-09-24): buckets as recommended, except 단란주점
(karaoke bars licensed for alcohol) -> Food service; 유흥주점 (hostess bars,
cabarets) stays out, as do lodging and veterinary clinics.

`permit_type` is what the tooltip shows: an English rendering of the permit
type and sub-type, written here from the registers' own values.
"""

FIELD_LABEL = "Kind"
VALUE_COLUMN = "permit_type"
EXTRA_COLUMNS = ("oa", "subtype")

FOOD, RETAIL, PERSONAL = "Food service", "Retail", "Personal services"

# oa -> (bucket for the whole file, or None, and the default English kind)
FILES = {
    "OA-16094": (FOOD, "Restaurant"),
    "OA-16095": (FOOD, "Café or snack bar"),
    "OA-16063": (PERSONAL, "Beauty salon"),
    "OA-16064": (PERSONAL, "Barber"),
    "OA-16065": (PERSONAL, "Laundry"),
    "OA-16146": (PERSONAL, "Public bath"),
    "OA-16084": (RETAIL, "Bakery"),
    "OA-16085": (RETAIL, "Food made and sold on site"),
    "OA-16080": (RETAIL, "Food shop"),
    "OA-16071": (RETAIL, "Butcher"),
    "OA-16144": (RETAIL, "Shop licensed to sell tobacco"),
    "OA-16096": (RETAIL, "Large store"),
    "OA-16070": (RETAIL, "Health-food shop"),
    "OA-16089": (FOOD, "Karaoke bar"),
    "OA-16044": (None, "Lodging"),              # excluded: lodging, every city
    "OA-16007": (None, "Veterinary clinic"),    # excluded: professional (NAICS 541940)
    "OA-16090": (None, "Hostess bar"),          # excluded: the adult-services rule
}

# Rows taken OUT of their file's bucket: not premises, or not a storefront.
DROP = {
    "OA-16094": {"출장조리", "이동조리", "푸드트럭"},   # catering, mobile cooking, food trucks
    "OA-16095": {"푸드트럭"},
}
# Only these sub-types are kept, where most of a file is not a storefront.
ONLY = {
    # 축산판매업: butchers only. Distribution, import, milk and egg collection
    # are wholesale.
    "OA-16071": {"식육판매업"},
    # 건강기능식품일반판매업: in-store sellers only. 52% are e-commerce sellers,
    # often registered at a home address.
    "OA-16070": {"영업장판매"},
}
# Rows MOVED to another bucket: a convenience store or a confectioner holding a
# café permit is a shop (Boston: convenience stores are retail; Japan: bakeries).
MOVE = {("OA-16095", "편의점"): RETAIL, ("OA-16095", "과자점"): RETAIL}

# The English kind by (oa, sub-type), where the sub-type says more than the file.
KINDS = {
    "OA-16094": {
        "한식": "Korean restaurant", "호프/통닭": "Beer and chicken pub",
        "경양식": "Western-style restaurant", "분식": "Snack restaurant (bunsik)",
        "일식": "Japanese restaurant", "중국식": "Chinese restaurant",
        "외국음식전문점(인도,태국등)": "Other foreign cuisine",
        "정종/대포집/소주방": "Soju bar", "통닭(치킨)": "Fried-chicken restaurant",
        "식육(숯불구이)": "Korean barbecue", "까페": "Café", "커피숍": "Coffee shop",
        "횟집": "Raw-fish restaurant", "김밥(도시락)": "Gimbap and lunch boxes",
        "뷔페식": "Buffet", "패스트푸드": "Fast food", "감성주점": "Bar",
        "냉면집": "Cold-noodle restaurant", "패밀리레스트랑": "Family restaurant",
        "라이브카페": "Live-music café", "탕류(보신용)": "Soup restaurant",
        "복어취급": "Pufferfish restaurant", "전통찻집": "Traditional tea house",
        "키즈카페": "Kids' café",
    },
    "OA-16095": {
        "커피숍": "Coffee shop", "편의점": "Convenience store",
        "일반조리판매": "Takeaway food", "패스트푸드": "Fast food",
        "다방": "Tearoom (dabang)", "백화점": "Department-store food counter",
        "아이스크림": "Ice-cream shop", "과자점": "Confectioner",
        "전통찻집": "Traditional tea house", "떡카페": "Rice-cake café",
        "철도역구내": "Station kiosk", "키즈카페": "Kids' café",
        "호프/통닭": "Beer and chicken pub", "단란주점": "Karaoke bar",
    },
    "OA-16063": {
        "일반미용업": "Hair salon", "피부미용업": "Skin-care salon",
        "네일아트업": "Nail salon", "메이크업업": "Make-up studio",
        "일반이용업": "Barber",
    },
    "OA-16065": {"빨래방업": "Laundromat", "운동화전문세탁업": "Sneaker laundry"},
    "OA-16146": {"찜질시설서비스영업": "Jjimjilbang (sauna)",
                 "공동탕업+찜질시설서비스영업": "Public bath and jjimjilbang",
                 "한증막업": "Dry sauna (hanjeungmak)"},
    "OA-16096": {"대형마트": "Hypermarket", "백화점": "Department store",
                 "쇼핑센터": "Shopping centre", "복합쇼핑몰": "Shopping mall",
                 "시장": "Market", "전문점": "Specialist superstore"},
}
CONVENIENCE_STORE = "Convenience store"


def kind(oa, subtype):
    """The English kind a tooltip shows, from the file and its sub-type."""
    return KINDS.get(oa, {}).get((subtype or "").strip(), FILES[oa][1])


def classify(row):
    oa = str(row.get("oa", "")).strip()
    sub = str(row.get("subtype", "")).strip()
    if oa not in FILES:
        return None
    bucket = FILES[oa][0]
    if bucket is None or sub in DROP.get(oa, ()):
        return None
    if oa in ONLY and sub not in ONLY[oa]:
        return None
    return MOVE.get((oa, sub), bucket)


def legend_label(bucket):
    return bucket
