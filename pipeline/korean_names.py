"""A Korean personal name at a home address - the Korean pass the Latin-script
heuristics in scripts/check_personal_exposure.py cannot make (cjk-text section 5:
a Korean name is three syllables with no capitals, comma or space, so the Latin
check's zero on a Korean register is not a finding).

Shared by Seoul's step 2, which withholds the flagged names, and by the check,
which counts what is left. Sized on Seoul's registers in the brief (2026-09-24):
113 premises across the core eight.

The case: a trade name that is a bare personal name - a common surname and two
syllables, alone or with a trade word (헤어, 네일, 세탁소...) - at an address that
reads residential (아파트, 빌라, 맨션, 연립, 다세대, or a 동/호 unit) and not
commercial (상가, 빌딩, 시장, 프라자, 타워, 센터, 오피스텔...).
"""
import re
import unicodedata

# The common single-syllable surnames (covering the great majority of Koreans)
# and the compound ones.
SURNAMES_1 = ("김이박최정강조윤장임한오서신권황안송전홍유고문양손배백허남심노하곽성차주우"
              "구민류나진지엄채원천방공현함변염여추도소석선설마길연위표명기반라왕금옥육인맹"
              "제모탁국어은편용예경봉사부")
SURNAMES_2 = ("황보", "남궁", "제갈", "선우", "독고", "사공", "서문")
TRADE_WORDS = ("헤어샵", "헤어", "네일", "세탁소", "세탁", "미용실", "미용원", "이용원",
               "뷰티", "살롱", "피부", "식당", "분식", "반찬", "상회", "상점")

_NAME = re.compile(
    "^(?:" + "|".join(SURNAMES_2) + "|[" + SURNAMES_1 + "])[가-힣]{2}"
    "(?:" + "|".join(TRADE_WORDS) + ")?$")
_HOME = re.compile(r"아파트|빌라|맨션|연립|다세대|\d+동\s*\d+호")
_COMMERCIAL = re.compile(r"상가|빌딩|시장|프라자|플라자|타워|센터|오피스텔|스퀘어|몰|쇼핑|상점가")


def looks_like_personal_name(name):
    s = unicodedata.normalize("NFKC", str(name or "")).replace(" ", "")
    return bool(_NAME.match(s))


def reads_residential(address):
    a = unicodedata.normalize("NFKC", str(address or ""))
    return bool(_HOME.search(a)) and not _COMMERCIAL.search(a)


def personal_name_at_home(name, address):
    return looks_like_personal_name(name) and reads_residential(address)
