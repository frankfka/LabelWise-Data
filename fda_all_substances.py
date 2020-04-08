from typing import List

from util import clean_html, strip_weird_t


class FDASubstanceListInfo:

    def __init__(self):
        self.names: List[str] = []
        self.cas_id: str = ""
        self.fema_num: str = ""
        self.technical_effs: List[str] = []

    def to_dict(self):
        return {
            "names": self.names,
            "cas_id": self.cas_id,
            "fema_num": self.fema_num,
            "technical_effects": self.technical_effs
        }

    @classmethod
    def from_dict(cls, data):
        item = FDASubstanceListInfo()
        item.names = data["names"]
        item.cas_id = data["cas_id"]
        item.fema_num = data["fema_num"]
        item.technical_effs = data["technical_effects"]
        return item


def get_names(row) -> List[str]:
    primary_name = row["Substance"].strip()
    alternate_names_txt = row["Other Names"]
    names = [primary_name]
    if not alternate_names_txt:
        return names
    text = clean_html(alternate_names_txt)
    split_names = text.split("♦")
    for n in split_names:
        if n.strip():
            names.append(n.strip())
    return list(set(names))


def get_cas_id(row) -> str:
    return row["CAS Reg No (or other ID)"].strip()


def get_fema_num(row) -> str:
    fema_text = row["FEMA No"]
    if fema_text:
        return strip_weird_t(fema_text)
    return ""


def get_technical_effs(row) -> List[str]:
    tech_effs_str = row["Used for (Technical Effect)"]
    tech_effs_str = clean_html(tech_effs_str)
    split_tech_effs = tech_effs_str.split(",")
    tech_effs = []
    for s in split_tech_effs:
        if s.strip():
            tech_effs.append(s.strip())
    return tech_effs


def process():
    import pandas as pd
    import json
    df = pd.read_csv("./data/fda_food_substances.csv", keep_default_na=False, dtype="str")
    results: List[FDASubstanceListInfo] = []
    for _, row in df.iterrows():
        info = FDASubstanceListInfo()
        info.names = get_names(row)
        info.fema_num = get_fema_num(row)
        info.technical_effs = get_technical_effs(row)
        info.cas_id = get_cas_id(row)
        results.append(info)

    with open("./export/fda_food_substances.json", "w") as f:
        json.dump([r.to_dict() for r in results], f, indent=4, sort_keys=True)


process()
