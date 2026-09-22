"""Percentages that cannot be written without naming the set they measure.

THE MOST FREQUENT ERROR IN THIS PROJECT, BY A WIDE MARGIN. Eight instances by
2026-09-21, six during the Canadian builds and two more committed *while
writing up the other six*:

    Montreal 440 per station, summing per-station counts   -> 151, on the union
    Toronto 41 per PLATFORM across 234                     -> per station
    Calgary 75 per station on 83 platforms                 -> 137 on 45
    Edmonton 76 on 33 stops, three of them garages         -> 79 on 30
    Toronto 118 stations, one naming convention handled    -> 110, three
    Toronto 71.4% geocode match across ALL licence rows    -> 92.8% storefront
    "92 categories, not the 72 asserted"                   -> both, different sets
    "names blank on 21.4% of rows"                         -> 0.5% of map rows

Every one is the same shape: a number correct for some set, reported as though
it were correct for the set the reader has in mind. And the pattern survived
being documented as a known fault in `CLAUDE.md`, in `add-city`, and in the
decisions log - **knowing the failure mode did not prevent it.**

So this module makes the unlabelled form unavailable rather than discouraged.
`pct()` takes the set's name as a required argument and puts it in the output:

    >>> pct(106, 19575, "storefront rows")
    '106 of 19,575 storefront rows (0.5%)'

Use it for any share that reaches a print, a page, a brief or a commit message.
Where a figure genuinely has two defensible denominators, print BOTH with
`pct_both()` - that is what Toronto's 71.4%/92.8% needed and did not get.
"""


def _fmt(x):
    return f"{x:,}" if isinstance(x, int) else f"{x:,.0f}"


def pct(n, of, label, *, places=1):
    """'<n> of <of> <label> (<p>%)'. `label` names the SET, and is required.

    Write the label as a plural noun phrase the reader would recognise -
    "storefront rows", "served stops", "active licences" - not "rows" or
    "total", which name nothing.
    """
    if not label or not str(label).strip():
        raise ValueError(
            "pct() needs the name of the set being measured. An unlabelled "
            "percentage is this project's most repeated error - see "
            "pipeline/counts.py."
        )
    if of == 0:
        return f"{_fmt(n)} of 0 {label} (n/a)"
    return f"{_fmt(n)} of {_fmt(of)} {label} ({100 * n / of:.{places}f}%)"


def pct_both(n_a, of_a, label_a, n_b, of_b, label_b, *, places=1):
    """Two denominators, printed together, for a figure that has two honest
    readings. Toronto's geocode match is the worked example: 73.1% across all
    licence rows and 92.8% across the storefront rows the map actually uses.
    Reporting only the first understated the city's coverage for a day."""
    return f"{pct(n_a, of_a, label_a, places=places)}; " \
           f"{pct(n_b, of_b, label_b, places=places)}"


def per(n, of, label, *, places=0):
    """'<x> per <label>' with the denominator shown - for density figures.

    >>> per(8739, 108, "station")
    '81 per station (8,739 across 108)'
    """
    if not label or not str(label).strip():
        raise ValueError("per() needs the name of the unit being divided by.")
    if of == 0:
        return f"n/a per {label} (0 of them)"
    return (f"{n / of:.{places}f} per {label} "
            f"({_fmt(n)} across {_fmt(of)})")
