import json
from typing import List

import pandas as pd

from util import clean_html


class CanadaAdditiveSynonyms:

    def __init__(self):
        self.names: List[str] = []

    def to_dict(self):
        return {
            "names": self.names
        }


def get_additive_name(row) -> str:
    full_name = row["Additive"]
    if full_name.index("(") > 0:
        # Get rid of French
        full_name = full_name[:full_name.index("(")]
    return clean_html(full_name).strip()


def get_alternate_names(row) -> List[str]:
    val = row["Permitted Synonyms"]
    # Different names are split by new lines, which get parsed as double space
    split_names: List[str] = val.split("  ")
    names = []
    for n in split_names:
        if n.strip():
            names.append(clean_html(n).strip())
    return names

def process():
    df = pd.read_html("./data/can_synonyms.html")[0]  # One table in the page
    results: List[CanadaAdditiveSynonyms] = []
    for _, row in df.iterrows():
        info = CanadaAdditiveSynonyms()
        info.names = [get_additive_name(row)] + get_alternate_names(row)
        results.append(info)

    with open("./export/can_synonyms.json", "w") as f:
        json.dump([r.to_dict() for r in results], f, indent=4, sort_keys=True)

process()