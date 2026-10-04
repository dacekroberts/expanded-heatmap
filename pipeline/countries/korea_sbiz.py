"""SEMAS's 상가(상권)정보 (data.go.kr 15083033) for a Korean city: one national
ZIP of per-province CSVs, every storefront with a WGS84 point, classified by
SEMAS's own 대/중/소분류 (pipeline/taxonomies/korea_sbiz.py).

Why this source (2026-09-29): the national LOCALDATA register moved behind a
data.go.kr Open API whose key needs a Korean identity check (본인인증), closed
to this project; SEMAS's file is a keyless download, declared 이용허락범위 제한
없음, active storefronts only, quarterly.

Shared by Incheon and the Gyeonggi satellites. The ZIP is cached ONCE for the
country at data/korea/raw/ (France's and Norway's national-cache pattern),
downloaded by pipeline/countries/korea_sbiz_fetch.py, never here: a step reads
this module, and a step never fetches.

The rules, in one place:
  * the ZIP's member NAMES are not decodable (neither UTF-8 nor CP949), so a
    province's member is found by its first row's 시도명;
  * only the columns in READ are loaded - no phone or owner column exists, and
    READ is asserted to be all that arrives;
  * a city is its 시군구코드 list where config gives one, else its 시군구명
    prefix (고양시 covers 고양시 덕양구, 일산동구...). Names are not unique
    across a member: Gwangju's 동구, 서구, 남구 and 북구 recur in other
    metropolitan cities, and 경기도 광주시 is another city. Given both, the
    two must pick the same rows;
  * the pin shows 상호명 with 지점명 (the branch) where given; a Korean
    personal name at a residential address is withheld (Seoul's rule,
    pipeline/korean_names.py), the address read with its building name.
"""
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

from pipeline.baseline import emit
from pipeline.countries.korea import WITHHELD, norm_name
from pipeline.korean_names import personal_name_at_home
from pipeline.taxonomies import korea_sbiz as tax

ROOT = Path(__file__).parent.parent.parent
ZIP = ROOT / "data" / "korea" / "raw" / "sbiz_15083033.zip"
PAGE = "https://www.data.go.kr/data/15083033/fileData.do"
READ = ["상가업소번호", "상호명", "지점명", "상권업종대분류명", "상권업종중분류명", "상권업종소분류명",
        "시도명", "시군구코드", "시군구명", "도로명주소", "건물명", "경도", "위도"]


def need_zip():
    if not ZIP.exists():
        sys.exit(f"missing {ZIP}.\nRun: python pipeline/countries/korea_sbiz_fetch.py")
    return ZIP


def edition():
    """The file's edition, from the ZIP's recorded download metadata."""
    import json
    import re
    meta = ZIP.with_suffix(".json")
    if meta.exists():
        disp = json.loads(meta.read_text(encoding="utf-8")).get("content_disposition") or ""
        m = re.search(r"_(\d{8})\.zip", disp)
        if m:
            d = m.group(1)
            return f"{d[:4]}-{d[4:6]}-{d[6:]}"
    return None


def province(sido):
    """Every row of one province (시도명, e.g. 인천광역시), READ columns only."""
    z = zipfile.ZipFile(need_zip())
    for info in z.infolist():
        if not info.filename.lower().endswith(".csv"):
            continue
        head = pd.read_csv(io.TextIOWrapper(z.open(info), encoding="utf-8-sig"), dtype=str, nrows=2)
        if head["시도명"].iloc[0] != sido:
            continue
        missing = set(READ) - set(head.columns)
        if missing:
            sys.exit(f"SEMAS {sido}: columns {sorted(missing)} are gone - read the new header")
        df = pd.read_csv(io.TextIOWrapper(z.open(info), encoding="utf-8-sig"), dtype=str, usecols=READ)
        assert list(df.columns) == [c for c in head.columns if c in READ]
        if set(df["시도명"]) != {sido}:
            sys.exit(f"SEMAS {sido}: the member mixes provinces {set(df['시도명'])}")
        return df.fillna("")
    sys.exit(f"SEMAS: no member for {sido}")


def storefronts(sido, sigungu_prefixes, sigungu_codes=None):
    """The city's storefronts: classified, one per 상가업소번호, named by the
    project's rules. sigungu_prefixes: 시군구명 prefixes (None = the whole
    province, as for Incheon). sigungu_codes: 5-digit 시군구코드 values,
    which decide the rows when given; prefixes given as well must agree."""
    df = province(sido)
    print(f"  SEMAS {sido}: {len(df):,} rows")
    by_name = df["시군구명"].str.startswith(tuple(sigungu_prefixes)) if sigungu_prefixes else None
    if sigungu_codes:
        codes = tuple(sigungu_codes)
        unknown = set(codes) - set(df["시군구코드"])
        if unknown:
            sys.exit(f"SEMAS {sido}: no rows for 시군구코드 {sorted(unknown)} - read the member's codes")
        keep = df["시군구코드"].isin(codes)
        if by_name is not None and not keep.equals(by_name):
            sys.exit(f"SEMAS {sido}: 시군구코드 and 시군구명 disagree on "
                     f"{int((keep != by_name).sum()):,} rows")
        df = df[keep].copy()
        print(f"  in 시군구코드 {', '.join(codes)}: {len(df):,}")
    elif by_name is not None:
        df = df[by_name].copy()
        print(f"  in {', '.join(sigungu_prefixes)}: {len(df):,}")
    emit("semas_rows", len(df))
    if df["상가업소번호"].duplicated().any():
        sys.exit(f"{int(df['상가업소번호'].duplicated().sum())} duplicate 상가업소번호")
    df = df.rename(columns={"상권업종중분류명": "group", "상권업종소분류명": "category"})
    df["group"] = df["group"].str.strip()
    df["category"] = df["category"].str.strip()
    df["bucket"] = [tax.bucket(g, c) for g, c in zip(df["group"], df["category"])]
    print("  by 대분류 -> bucket:")
    tab = pd.crosstab(df["상권업종대분류명"], df["bucket"].fillna("(out)"))
    print("\n".join("    " + ln for ln in tab.to_string().splitlines()))
    out_named = df[df["bucket"].isna() & df["category"].isin(tax.OUT)]["category"].value_counts()
    print("  left out by name: " + ", ".join(f"{k} {v:,}" for k, v in out_named.items()))
    df = df[df["bucket"].notna()].copy()
    emit("storefronts_classified", len(df))

    df["longitude"] = pd.to_numeric(df["경도"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["위도"], errors="coerce")
    no_point = df["longitude"].isna() | df["latitude"].isna()
    print(f"  without a point: {int(no_point.sum()):,}")
    df = df[~no_point].copy()

    name = df["상호명"].map(norm_name)
    branch = df["지점명"].map(norm_name)
    df["name"] = (name + " " + branch).str.strip().where(branch != "", name)
    df["address"] = (df["도로명주소"] + " " + df["건물명"]).str.strip()
    flag = [personal_name_at_home(n, a) for n, a in zip(name, df["address"])]
    df["business_name"] = df["name"].where(~pd.Series(flag, index=df.index), WITHHELD)
    print(f"  names withheld (a personal name at a residential address): {sum(flag):,}")
    emit("names_withheld", int(sum(flag)))
    df["kind"] = df["category"].map(tax.KINDS)
    print("  by bucket: " + ", ".join(f"{b} {n:,}" for b, n in df["bucket"].value_counts().items()))
    return df[["business_name", "kind", "category", "group", "latitude", "longitude", "address",
               "시군구명"]]
