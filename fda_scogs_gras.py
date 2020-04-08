from typing import Optional, List

from util import strip_weird_t


class FDASafeToEatListInfo:

    def __init__(self):
        self.name: str = ""
        self.cas_id: Optional[str] = None
        self.scogs_conclusion: Optional[int] = None

    def to_dict(self):
        return {
            "name": self.name,
            "cas_id": self.cas_id,
            "scogs_conclusion": self.scogs_conclusion
        }

    def __eq__(self, other):
        if not self.cas_id:
            return False
        return self.cas_id == other.cas_id

    @classmethod
    def from_dict(cls, data):
        item = FDASafeToEatListInfo()
        item.name = data["name"]
        item.cas_id = data["cas_id"]
        item.scogs_conclusion = data["scogs_conclusion"]
        return item


def get_name(row):
    return row["GRAS Substance"].strip()


def get_scogs_conclusion(row):
    val: str = row["SCOGS Type of Conclusion"].strip()
    if val and val.startswith("=T("):
        return strip_weird_t(val)
    # Sometimes we get "There is no conclusion type" or multiple conclusions - just default to none
    return None


def get_cas_id(row):
    val = row["CAS Reg. No. or other ID Code"].strip()
    if val == "There is no ID Code":
        return None
    return val


def process():
    import pandas as pd
    import json
    df = pd.read_csv("./data/fda_scogs_gras.csv", keep_default_na=False, dtype="str")
    results: List[FDASafeToEatListInfo] = []
    for _, row in df.iterrows():
        info = FDASafeToEatListInfo()
        info.cas_id = get_cas_id(row)
        info.name = get_name(row)
        info.scogs_conclusion = get_scogs_conclusion(row)
        results.append(info)

    with open("./export/fda_scogs_gras.json", "w") as f:
        json.dump([r.to_dict() for r in results], f, indent=4, sort_keys=True)

process()