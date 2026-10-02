"""Keys for the people's names a step withholds, so the names themselves never
sit in the repository.

    python pipeline/name_keys.py "NAME" ["NAME" ...]   # the key to put in a config
    python pipeline/name_keys.py --selftest            # touches nothing

A build that reads a register's shown names by eye lists the ones that are
only a person's own, and step 2 shows an address or a type in their place. A
list of those names in the source would publish, in the repository, the very
names the map withholds (owner, 2026-10-01; DECISIONS.md). So a config holds
each name's KEY, and step 2 compares keys with `keys_of()`.

A key is the first 16 hex digits of the SHA-256 of the name exactly as the step
compares it: no case-folding or trimming, so a key matches exactly the rows the
name did. It is not a secret, since anyone with the public register can
recompute it; it keeps a curated list of people out of the repository, which
is the point. Never write the name beside its key, in a comment or a commit.
"""
import hashlib
import sys


def name_key(name):
    """The key of one name, exactly as written."""
    return hashlib.sha256(name.encode("utf-8")).hexdigest()[:16]


def keys_of(values):
    """A pandas Series of keys for a Series of names; None where a value is not
    a string (a blank never matches, as it never matched a name)."""
    return values.map(lambda v: name_key(v) if isinstance(v, str) else None)


def selftest():
    import pandas as pd
    names = pd.Series(["ANY NAME", "any name", None, float("nan"), "ANY NAME "])
    keys = keys_of(names)
    wanted = {name_key("ANY NAME")}
    cases = [
        (list(keys.isin(wanted)), list(names.isin({"ANY NAME"}))),   # same rows as the name
        (len(name_key("x")), 16),
        (name_key("ANY NAME") == name_key("any name"), False),         # case is kept
    ]
    bad = [i for i, (got, want) in enumerate(cases) if got != want]
    print(f"{len(cases) - len(bad)} of {len(cases)} cases behaved as intended."
          + (f" FAILED: {bad}" if bad else ""))
    return not bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    for arg in sys.argv[1:]:
        print(name_key(arg))
