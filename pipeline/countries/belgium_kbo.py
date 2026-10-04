"""KBO/BCE Open Data (FPS Economy): companies' establishment units, read from
the owner-placed full file, never fetched (the portal needs the owner's login).

**COMPANIES ONLY, BY CONSTRUCTION** (the licence read's condition, notice 151):
`enterprise.csv` is read for its codes alone and only `TypeOfEnterprise` 2
(legal person) is kept; every later member is filtered to the entity numbers
of those companies and their establishment units. `contact.csv` is never
opened (`NEVER_READ`). `denomination.csv` is streamed line by line and a line
is parsed only when its first field is already in the companies' set, so no
natural person's row is ever parsed, held or written.

The extract is cached as parquet under the city's processed folder, so a
re-run of step 2 reads a few MB instead of 2.3 GB of CSV. The screen's pass
measured 1.32 GB peak (heavy-job gate, label kbo-storefront, 2026-10-03).
"""
import csv
import io
import json
import zipfile

import pandas as pd

NEVER_READ = ("contact.csv",)
LEGAL_PERSON = "2"
ESTABLISHMENT_ADDRESS = "BAET"
COMMERCIAL_NAME = "003"
COMPANY_NAME = "001"
CHUNK = 1_000_000


def _open(z, member):
    if member in NEVER_READ:
        raise PermissionError(f"{member} is never read (KBO licence: companies only)")
    return z.open(member)


def read_meta(zip_path):
    """meta.csv as a dict: SnapshotDate, ExtractTimestamp, ExtractType, ExtractNumber, Version."""
    with zipfile.ZipFile(zip_path) as z:
        meta = pd.read_csv(_open(z, "meta.csv"), dtype=str)
    return dict(zip(meta["Variable"], meta["Value"]))


def code_labels(zip_path, language="FR"):
    """{(version, code): label} for NACE-BEL 2025 and 2008, FPS Economy's own text."""
    with zipfile.ZipFile(zip_path) as z:
        c = pd.read_csv(_open(z, "code.csv"), dtype=str, encoding="utf-8")
    c = c[c["Category"].isin(["Nace2025", "Nace2008"]) & (c["Language"] == language)]
    return {(cat[-4:], code): desc for cat, code, desc in
            zip(c["Category"], c["Code"], c["Description"])}


def _chunks(z, member, usecols):
    return pd.read_csv(_open(z, member), dtype=str, usecols=usecols, chunksize=CHUNK,
                       keep_default_na=False, na_values=[""], encoding="utf-8")


def extract(zip_path, out_dir, postcode_lo, postcode_hi, log=print):
    """Companies' establishment units with an establishment address in the
    postcode range, their MAIN activities and their names -> parquet in
    out_dir. Returns the out_dir paths written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        # 1. Companies: codes only, natural persons dropped chunk by chunk.
        ents, n_all = [], 0
        for ch in _chunks(z, "enterprise.csv", ["EnterpriseNumber", "Status", "JuridicalSituation",
                                                "TypeOfEnterprise", "JuridicalForm", "StartDate"]):
            n_all += len(ch)
            ents.append(ch[ch["TypeOfEnterprise"] == LEGAL_PERSON].drop(columns="TypeOfEnterprise"))
        ent = pd.concat(ents, ignore_index=True)
        log(f"  enterprise.csv: {n_all:,} entities, {len(ent):,} legal persons kept")
        legal = set(ent["EnterpriseNumber"])

        # 2. Their establishment units.
        ests, n_all = [], 0
        for ch in _chunks(z, "establishment.csv", ["EstablishmentNumber", "StartDate", "EnterpriseNumber"]):
            n_all += len(ch)
            ests.append(ch[ch["EnterpriseNumber"].isin(legal)])
        est = pd.concat(ests, ignore_index=True)
        log(f"  establishment.csv: {n_all:,} units, {len(est):,} of legal persons")
        est_set = set(est["EstablishmentNumber"])

        # 3. Establishment addresses in the postcode range.
        addrs, n_all = [], 0
        cols = ["EntityNumber", "TypeOfAddress", "Zipcode", "MunicipalityNL", "MunicipalityFR",
                "StreetNL", "StreetFR", "HouseNumber", "Box", "ExtraAddressInfo", "DateStrikingOff"]
        for ch in _chunks(z, "address.csv", cols):
            n_all += len(ch)
            ch = ch[(ch["TypeOfAddress"] == ESTABLISHMENT_ADDRESS) & ch["EntityNumber"].isin(est_set)]
            pc = pd.to_numeric(ch["Zipcode"], errors="coerce")
            addrs.append(ch[pc.between(postcode_lo, postcode_hi)])
        adr = pd.concat(addrs, ignore_index=True)
        log(f"  address.csv: {n_all:,} rows, {len(adr):,} legal establishment addresses "
            f"in postcodes {postcode_lo}-{postcode_hi}")
        units = est[est["EstablishmentNumber"].isin(set(adr["EntityNumber"]))]
        ent = ent[ent["EnterpriseNumber"].isin(set(units["EnterpriseNumber"]))]
        wanted = set(units["EstablishmentNumber"]) | set(ent["EnterpriseNumber"])

        # 4. MAIN activities (2025 and 2008) of those units and their companies.
        acts, n_all = [], 0
        for ch in _chunks(z, "activity.csv", ["EntityNumber", "ActivityGroup", "NaceVersion",
                                              "NaceCode", "Classification"]):
            n_all += len(ch)
            ch = ch[(ch["Classification"] == "MAIN") & ch["NaceVersion"].isin(["2025", "2008"])
                    & ch["EntityNumber"].isin(wanted)]
            acts.append(ch.drop(columns="Classification"))
        act = pd.concat(acts, ignore_index=True)
        log(f"  activity.csv: {n_all:,} rows, {len(act):,} MAIN 2025/2008 rows kept")

        # 5. Names: a line is parsed only when its first field is in `wanted`.
        den = _legal_denominations(z, wanted)
        log(f"  denomination.csv: {len(den):,} rows of these companies and units kept")

    paths = {}
    for name, df in (("enterprises", ent), ("units", units), ("addresses", adr),
                     ("activities", act), ("denominations", den)):
        p = out_dir / f"kbo_{name}.parquet"
        df.reset_index(drop=True).to_parquet(p, index=False)
        paths[name] = p
    return paths


def _legal_denominations(z, wanted):
    """Stream denomination.csv; keep the rows whose EntityNumber is in `wanted`
    (companies and their units only). Every other line is skipped on its
    first field, before any parse."""
    rows = []
    with io.TextIOWrapper(_open(z, "denomination.csv"), encoding="utf-8", newline="") as f:
        header = next(csv.reader([f.readline()]))
        assert header == ["EntityNumber", "Language", "TypeOfDenomination", "Denomination"], header
        pending = None
        for line in f:
            if pending is not None:
                # Continuation of a kept record that holds a quoted newline.
                pending += line
                if pending.count('"') % 2 == 0:
                    rows.extend(csv.reader([pending]))
                    pending = None
                continue
            if line.startswith('"'):
                end = line.find('"', 1)
                key = line[1:end] if end > 0 else ""
            else:
                key = line.split(",", 1)[0]
            if key not in wanted:
                if line.count('"') % 2:
                    # A skipped record spanning lines: skip its continuation too.
                    for more in f:
                        line += more
                        if line.count('"') % 2 == 0:
                            break
                continue
            if line.count('"') % 2:
                pending = line
                continue
            rows.extend(csv.reader([line]))
    den = pd.DataFrame(rows, columns=header)
    assert den["EntityNumber"].isin(wanted).all()
    return den


def load(out_dir):
    """The cached extract as a dict of DataFrames (strings, empty as NA)."""
    return {name: pd.read_parquet(out_dir / f"kbo_{name}.parquet")
            for name in ("enterprises", "units", "addresses", "activities", "denominations")}


def write_extract_meta(out_dir, info):
    (out_dir / "kbo_extract.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
