"""SEMAS's 상가(상권)정보 - the Small Enterprise and Market Service's national
storefront register (data.go.kr 15083033), classified by its own three-level
scheme (상권업종 대/중/소분류), not NAICS. Incheon is the first city on it; the
Gyeonggi satellites follow.

KEYED AT THE FINEST LEVEL. Measured on Incheon and Gyeonggi (809,675 rows,
2026-09-29): 10 대분류, 75 중분류, 247 소분류; the "기타 / 그 외" catch-all
share is 13.1% at 중분류 and 6.4% at 소분류. The bucket is set per 중분류 and
overridden per 소분류, so every one of the 247 has an explicit home, and a
중분류 or 소분류 the tables do not know RAISES.

The scope is the NAICS cities' (owner, 2026-09-29): Retail is store retail
(NAICS 44-45) less nonstore fuel dealers; Food service is 722 less staff
canteens and hostess and dance bars (Seoul's adult-services rule); Personal
services is 812's hair, beauty, laundry and baths, less funeral services (the
owner's rule) and the 812990-style catch-alls (wedding halls, matchmaking).
Massage (마사지/안마) COUNTS, for continuity with every other country (owner,
2026-09-29): commercial massage is Personal services in the NAICS cities
(812199), D.C., Miami, Chicago, Calgary, Dublin, Milan, Buenos Aires and
Brazil; only regulated massage therapy (health) and explicit adult premises
are out elsewhere, and SEMAS separates neither. Repairs
(811), lodging, recreation (71), education, health, estate agents and
professional offices are out.

The pin shows an English rendering of the 소분류 (`KINDS`); the register's own
Korean value is kept alongside in `category`.
"""

FIELD_LABEL = "Kind"
VALUE_COLUMN = "kind"
EXTRA_COLUMNS = ("category", "group")

FOOD, RETAIL, PERSONAL = "Food service", "Retail", "Personal services"

# 중분류 -> bucket (None = out). Every 중분류 on Incheon's and Gyeonggi's rows.
GROUPS = {
    # 음식
    "구내식당·뷔페": FOOD, "기타 간이": FOOD, "기타 외국": FOOD, "동남아시아": FOOD,
    "비알코올": FOOD, "서양식": FOOD, "일식": FOOD, "주점": FOOD, "중식": FOOD, "한식": FOOD,
    # 소매
    "가구 소매": RETAIL, "가전·통신 소매": RETAIL, "기타 상품 소매": RETAIL,
    "기타 생활용품 소매": RETAIL, "담배 소매": RETAIL, "모터사이클 소매": RETAIL,
    "섬유·의복·신발 소매": RETAIL, "시계·귀금속 소매": RETAIL, "식료품 소매": RETAIL,
    "식물 소매": RETAIL, "안경·정밀기기 소매": RETAIL, "애완동물·용품 소매": RETAIL,
    "연료 소매": RETAIL, "오락용품 소매": RETAIL, "음료 소매": RETAIL,
    "의약·화장품 소매": RETAIL, "자동차 부품 소매": RETAIL, "장식품 소매": RETAIL,
    "종합 소매": RETAIL, "중고 상품 소매": RETAIL, "철물·건설자재 소매": RETAIL,
    # 수리·개인
    "이용·미용": PERSONAL, "세탁": PERSONAL, "욕탕·신체관리": PERSONAL,
    "기타 개인": None, "장례식장": None,
    "가전제품 수리": None, "기타 가정용품 수리": None, "모터사이클 수리": None,
    "자동차 수리·세차": None, "컴퓨터 수리": None, "통신장비 수리": None,
    # everything else: out
    "광고": None, "기술 서비스": None, "기타 전문 과학": None, "법무관련": None,
    "본사·경영 컨설팅": None, "사진 촬영": None, "수의": None, "시장 조사": None,
    "인쇄·제품제작": None, "전문 디자인": None, "회계·세무": None,
    "교육 지원": None, "기타 교육": None, "일반 교육": None,
    "기타 보건": None, "병원": None, "의원": None,
    "부동산 서비스": None,
    "기타 숙박": None, "일반 숙박": None,
    "가정용품 대여": None, "고용 알선": None, "기타 사업 서비스": None, "사무 지원": None,
    "산업용품 대여": None, "시설관리": None, "여행사·보조": None, "운송장비 대여": None,
    "조경·유지": None, "청소·방제": None,
    "도서관·사적지": None, "스포츠 서비스": None, "유원지·오락": None,
}

# 소분류 overrides (the owner's calls, 2026-09-29).
OUT = {
    "구내식당",          # staff canteens: institutional
    "무도 유흥 주점",     # dance halls: the adult-services rule
    "일반 유흥 주점",     # hostess bars: the adult-services rule (Seoul's 유흥주점)
    "가정용 연료 소매업",  # household fuel dealers: nonstore (NAICS 454)
}

# English kinds for the pins, by 소분류, for every kept category.
KINDS = {
    # food service
    "뷔페": "Buffet", "그 외 기타 간이 음식점": "Other snack restaurant",
    "김밥/만두/분식": "Gimbap, dumplings and bunsik", "떡/한과": "Rice cakes and sweets",
    "버거": "Burgers", "빵/도넛": "Bakery café", "아이스크림/빙수": "Ice cream and bingsu",
    "치킨": "Fried chicken", "토스트/샌드위치/샐러드": "Toast, sandwiches and salads",
    "피자": "Pizza", "분류 안된 외국식 음식점": "Other foreign cuisine",
    "기타 동남아식 전문": "Southeast Asian", "베트남식 전문": "Vietnamese", "카페": "Café",
    "경양식": "Western-style restaurant", "기타 서양식 음식점": "Other Western restaurant",
    "파스타/스테이크": "Pasta and steak", "패밀리레스토랑": "Family restaurant",
    "기타 일식 음식점": "Other Japanese", "일식 면 요리": "Japanese noodles",
    "일식 카레/돈가스/덮밥": "Japanese curry, tonkatsu and donburi",
    "일식 회/초밥": "Sushi and sashimi", "생맥주 전문": "Beer pub", "요리 주점": "Pub (food and drink)",
    "마라탕/훠궈": "Malatang and hot pot", "중국집": "Chinese restaurant",
    "곱창 전골/구이": "Gopchang (tripe)", "국/탕/찌개류": "Soups and stews",
    "국수/칼국수": "Noodles", "기타 한식 음식점": "Other Korean restaurant",
    "냉면/밀면": "Cold noodles", "닭/오리고기 구이/찜": "Chicken and duck",
    "돼지고기 구이/찜": "Pork barbecue", "백반/한정식": "Korean set meals (baekban)",
    "복 요리 전문": "Pufferfish", "소고기 구이/찜": "Beef barbecue", "전/부침개": "Korean pancakes",
    "족발/보쌈": "Jokbal and bossam", "해산물 구이/찜": "Seafood", "횟집": "Raw-fish restaurant",
    # retail
    "가구 소매업": "Furniture", "가전제품 소매업": "Home appliances",
    "컴퓨터/소프트웨어 소매업": "Computers", "핸드폰 소매업": "Phones",
    "그 외 기타 상품 전문 소매업": "Other specialist shop", "악기 소매업": "Musical instruments",
    "전기용품/조명장치 소매업": "Electrical and lighting", "주방/가정용품 소매업": "Kitchen and housewares",
    "담배/전자담배 소매업": "Tobacco", "모터사이클 및 부품 소매업": "Motorcycles",
    "가발 소매업": "Wigs", "가방 소매업": "Bags", "기타 의류 소매업": "Clothing",
    "남성 의류 소매업": "Men's clothing", "신발 소매업": "Shoes", "실/섬유제품 소매업": "Yarn and textiles",
    "액세서리/잡화 소매업": "Accessories", "여성 의류 소매업": "Women's clothing",
    "유아용 의류 소매업": "Children's clothing", "침구류/커튼 소매업": "Bedding and curtains",
    "한복 소매업": "Hanbok", "시계/귀금속 소매업": "Watches and jewelry",
    "가축 사료 소매업": "Animal feed", "건강보조식품 소매업": "Health food",
    "건어물/젓갈 소매업": "Dried fish and jeotgal", "곡물/곡분 소매업": "Grain",
    "반찬/식료품 소매업": "Side dishes and groceries", "수산물 소매업": "Fishmonger",
    "아이스크림 할인점": "Ice-cream shop", "정육점": "Butcher", "채소/과일 소매업": "Greengrocer",
    "꽃집": "Florist", "사무기기 소매업": "Office equipment", "사진기/기타 광학기기 소매업": "Cameras",
    "안경렌즈 소매업": "Optician", "애완동물/애완용품 소매업": "Pets and pet supplies",
    "가스 충전소": "LPG station", "주유소": "Gas station",
    "문구/회화용품 소매업": "Stationery", "서점": "Bookshop", "운동용품 소매업": "Sporting goods",
    "음반/비디오물 소매업": "Music and video", "자전거 소매업": "Bicycles", "장난감 소매업": "Toys",
    "생수/음료 소매업": "Drinks", "얼음 소매업": "Ice", "우유 소매업": "Milk", "주류 소매업": "Liquor store",
    "약국": "Pharmacy", "의료기기 소매업": "Medical supplies", "화장품 소매업": "Cosmetics",
    "자동차 부품 소매업": "Car parts", "타이어 소매업": "Tires", "기념품점": "Souvenirs",
    "예술품 소매업": "Art", "그 외 기타 종합 소매업": "General store", "슈퍼마켓": "Supermarket",
    "편의점": "Convenience store", "중고 상품 소매업": "Second-hand goods",
    "건설/건축자재 소매업": "Building materials", "기타 건설/건축자재 소매업": "Other building materials",
    "벽지/장판/마루 소매업": "Wallpaper and flooring", "철물/공구 소매업": "Hardware",
    # personal services
    "네일숍": "Nail salon", "미용실": "Hair salon", "피부 관리실": "Skin-care salon",
    "세탁소": "Dry cleaner", "셀프 빨래방": "Laundromat", "목욕탕/사우나": "Bathhouse and sauna",
    "체형/비만 관리": "Body-shaping salon", "마사지/안마": "Massage",
}


def _s(v):
    return v.strip() if isinstance(v, str) else ""


def bucket(group, category):
    """The bucket for a 중분류 and 소분류, or None. Unknown values RAISE."""
    g, c = _s(group), _s(category)
    if g not in GROUPS:
        raise KeyError(f"SEMAS 중분류 {g!r} has no home in korea_sbiz.GROUPS")
    b = GROUPS[g]
    if b is None or c in OUT:
        return None
    if c not in KINDS:
        raise KeyError(f"SEMAS 소분류 {c!r} (in {g!r}) has no English kind - decide it")
    return b


def classify(row):
    return bucket(row.get("group"), row.get("category"))


def legend_label(b):
    return b


assert not set(OUT) & set(KINDS)
assert {"구내식당", "일반 유흥 주점"} <= OUT
assert "마사지/안마" in KINDS   # massage counts: continuity with every other country
