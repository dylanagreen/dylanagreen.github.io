#!/usr/bin/env python3
"""Convert a Zotero BibTeX export to data/publications.yaml.

Usage: python bib_to_yaml.py publications.bib [data/publications.yaml]
Requires: pip install bibtexparser pyyaml
"""

import re, sys
import bibtexparser
import yaml

ME_FULL = "Dylan Green"

# Add any collaboration names that appear literally in your .bib author fields
KNOWN_COLLABORATIONS = {"DESI Collaboration", "LSST DESC"}

MONTH_MAP = {
    "jan": "January", "feb": "February", "mar": "March",
    "apr": "April",   "may": "May",      "jun": "June",
    "jul": "July",    "aug": "August",   "sep": "September",
    "oct": "October", "nov": "November", "dec": "December",
    **{str(i): m for i, m in enumerate(
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"], 1
    )},
}
MONTH_ORDER = {m: i for i, m in enumerate(MONTH_MAP.values())}


def strip_braces(s):
    return re.sub(r"[{}]", "", s).strip()


def to_last_first(raw):
    """Normalize any name format to ('Last', 'First Middle') tuple."""
    raw = raw.strip()
    if "," in raw:
        last, first = raw.split(",", 1)
        return last.strip(), first.strip()
    parts = raw.split()
    if len(parts) >= 2:
        return parts[-1], " ".join(parts[:-1])
    return raw, ""


def format_author(raw):
    """'Last, First Middle' or 'First Last'  →  'Last, F.'"""
    last, first = to_last_first(raw)
    if first:
        return f"{last}, {first[0]}."
    return last


def format_author_full(raw):
    """'Last, First Middle' or 'First Last'  →  'Last, First'"""
    last, first = to_last_first(raw)
    if first:
        return f"{last}, {first}"
    return last


def has_full_first_name(raw):
    """True when BibTeX provides a full first name rather than just an initial."""
    _, first = to_last_first(raw)
    return len(first) > 2 and not first.endswith(".")


# Derived from ME_FULL — only ME_FULL needs updating above
ME = format_author(ME_FULL)          # "Green, D."
ME_LONG = format_author_full(ME_FULL)  # "Green, Dylan"


def parse_authors(author_str):
    collaboration, authors = None, []
    for a in author_str.split(" and "):
        name = strip_braces(a)
        if name in KNOWN_COLLABORATIONS:
            collaboration = name
        elif format_author(name) == ME and has_full_first_name(name):
            authors.append(ME_LONG)
        else:
            authors.append(format_author(name))
    return collaboration, authors


def entry_to_pub(entry):
    collaboration, authors = parse_authors(entry.get("author", ""))

    doi    = entry.get("doi", "").strip()
    url    = entry.get("url", "").strip()
    eprint = entry.get("eprint", "").strip()
    link   = (f"https://doi.org/{doi}" if doi else
              url if url else
              f"https://arxiv.org/abs/{eprint}" if eprint else None)

    venue = strip_braces(entry.get("journal",
            entry.get("booktitle",
            entry.get("publisher", ""))))
    if not venue and eprint:
        venue = "arXiv"

    month_raw = entry.get("month", "").strip().lower()[:3]
    month = MONTH_MAP.get(month_raw)

    pub = {}
    if collaboration:
        pub["collaboration"] = collaboration
    pub["authors"] = authors
    pub["title"]   = strip_braces(entry.get("title", ""))
    if month:
        pub["month"] = month
    pub["year"]    = int(entry.get("year", 0))
    if venue:
        pub["venue"] = venue
    if link:
        pub["url"] = link
    return pub


def main():
    bib_path = sys.argv[1] if len(sys.argv) > 1 else "publications.bib"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "data/publications.yaml"

    with open(bib_path) as f:
        library = bibtexparser.load(f)

    pubs = [entry_to_pub(e) for e in library.entries]
    pubs.sort(
        key=lambda p: (p["year"], MONTH_ORDER.get(p.get("month", ""), 0)),
        reverse=True,
    )

    with open(out_path, "w") as f:
        yaml.dump(pubs, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"Wrote {len(pubs)} publications to {out_path}")
    print(f"Your name stored as {ME_LONG!r} (full) or {ME!r} (abbreviated) depending on BibTeX source.")


if __name__ == "__main__":
    main()
