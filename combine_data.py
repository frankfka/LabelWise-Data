import json
from typing import List, Optional

from fda_all_substances import FDASubstanceListInfo
from fda_scogs_gras import FDASafeToEatListInfo


class AdditiveInfo:

    def __init__(self):
        self.names: List[str] = []
        self.cas_id: str = ""
        self.fema_num: str = ""
        self.technical_effs: List[str] = []
        self.scogs_conclusion: Optional[int] = None

    def to_dict(self):
        return {
            "names": self.names,
            "cas_id": self.cas_id,
            "fema_num": self.fema_num,
            "technical_effects": self.technical_effs,
            "scogs_conclusion": self.scogs_conclusion
        }

    @classmethod
    def from_dict(cls, data):
        item = AdditiveInfo()
        item.names = data["names"]
        item.cas_id = data["cas_id"]
        item.fema_num = data["fema_num"]
        item.technical_effs = data["technical_effects"]
        item.scogs_conclusion = data["scogs_conclusion"]
        return item



class UnprocessableInfo:

    def __init__(self):
        self.source: str = ""
        self.data: dict = {}

    def to_dict(self):
        return {
            "source": self.source,
            "data": self.data
        }


def get_fda_all_substances() -> List[FDASubstanceListInfo]:
    with open("./export/fda_food_substances.json", "r") as f:
        return [FDASubstanceListInfo.from_dict(data) for data in json.load(f)]


def get_fda_scogs() -> List[FDASafeToEatListInfo]:
    with open("./export/fda_scogs_gras.json", "r") as f:
        return [FDASafeToEatListInfo.from_dict(data) for data in json.load(f)]


def get_fda_scogs_item(cas_id: str, all_items: List[FDASafeToEatListInfo]) -> Optional[FDASafeToEatListInfo]:
    matching_id = [item for item in all_items if item.cas_id and item.cas_id == cas_id]
    if matching_id:
        return matching_id[0]
    return None


def process():

    results: List[AdditiveInfo] = []
    # Dump all unprocessable items here
    unprocessable: List[UnprocessableInfo] = []

    fda_all_substances = get_fda_all_substances()
    fda_scogs = get_fda_scogs()
    # Based on all substances
    for item in fda_all_substances:
        # Fetch matching items, remove them from the master list after
        scogs_item = get_fda_scogs_item(item.cas_id, fda_scogs)
        if scogs_item:
            fda_scogs.remove(scogs_item)

        info = AdditiveInfo()
        info.cas_id = item.cas_id
        info.fema_num = item.fema_num
        info.technical_effs = [eff.lower() for eff in item.technical_effs]
        # Get names - we want them in lowercase
        fda_substances_names = set([name.lower() for name in item.names])
        if scogs_item:
            if scogs_item.name:
                fda_substances_names.add(scogs_item.name.lower())
            info.scogs_conclusion = scogs_item.scogs_conclusion
        info.names = list(fda_substances_names)
        results.append(info)

    # TODO: Unprocessable, Canada synonyms

    with open("./export/combined.json", "w") as f:
        json.dump([r.to_dict() for r in results], f, indent=4, sort_keys=True)


process()