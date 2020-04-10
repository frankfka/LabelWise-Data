from typing import List

from bs4 import BeautifulSoup


def __get_soup__(path):
    with open(path, "r") as f:
        return BeautifulSoup(f.read(), "lxml")


def parse_healthline(path) -> List[str]:
    items = __get_soup__(path).article.find_all("li")
    return [item.text for item in items]


def parse_harvard_hsph(path) -> List[str]:
    items = __get_soup__(path).find("table").find_all("td")
    return [item.text for item in items]


def parse_harvard_health(path) -> List[str]:
    items = __get_soup__(path).find("table", type="standard").find_all("li")
    return [item.text for item in items]


def parse_ucsf(path) -> List[str]:
    items = __get_soup__(path).find("div", class_="sugar_list").find_all("li")
    return [item.text for item in items]


def process():
    results: List[str] = []
    results += parse_healthline(path="./data/sugar_synonyms/healthline_sugar.html")
    results += parse_harvard_hsph(path="./data/sugar_synonyms/harvard_hsph_sugar.html")
    results += parse_harvard_health(path="./data/sugar_synonyms/harvard_health_sugar.html")
    results += parse_ucsf(path="./data/sugar_synonyms/ucsf_sugar.html")
    results += ["sugar", "powdered sugar"]
    results = [result.strip().lower() for result in results if result.strip()]
    results = list(set(results))

    with open("./export/sugar_synonyms.json", "w") as f:
        import json
        json.dump(results, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    process()