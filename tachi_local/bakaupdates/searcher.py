from typing import NamedTuple, List

import requests
import bs4

from . import utils


def _get_html(title: str) -> bytes:
    payload = {
        "search": title,
        "display": "list"
    }

    try:
        page = requests.get("https://www.mangaupdates.com/series.html", params=payload, timeout=20)
    except requests.exceptions.RequestException as ex:
        raise SystemExit(ex) from ex

    return page.content


class SearchData(NamedTuple):
    id: str
    name: str
    year: int
    rating: str


def _scrape_data(page_html: bytes) -> List[SearchData]:
    doc = bs4.BeautifulSoup(page_html, "html.parser")
    data: List[SearchData] = []

    for item in doc.find_all(alt="Series Info"):
        try:
            id_ = utils.get_id_from_url(item["href"])
        except ValueError:
            id_ = item["href"]
        except KeyError:
            continue

        title = item.string.strip()

        item = item.find_parent().find_next_sibling().find_next_sibling()
        year = item.get_text().strip()

        item = item.find_next_sibling()
        rating = item.get_text().strip()

        data.append(SearchData(id_, title, year, rating))

    return data


def _get_choice(mangas: List[SearchData], max_choices: int) -> SearchData:
    for i, manga in enumerate(mangas):
        print(f"{i + 1}:", manga.name)

        if manga.year:
            print(manga.year, end="")
        if manga.rating:
            if manga.year:
                print(" - ", end="")
            print(f"{manga.rating}/10", end="")
        print("\n")

        if i >= max_choices - 1:
            break

    while True:
        choice = input("Choose manga (0 to cancel): ")
        if not choice.isdigit():
            print("Invalid input.")
            continue

        choice = int(choice)
        if choice == 0:
            raise SystemExit
        if choice > min(len(mangas), max_choices):
            print("Invalid index.")
            continue

        break

    return mangas[choice - 1]


def search(title: str, max_search_results: int, auto_first_result: bool = False) -> str:
    mangas = _scrape_data(_get_html(title))

    if not mangas:
        raise ValueError("No manga found.")

    if auto_first_result:
        return mangas[0].id

    return _get_choice(mangas, max_search_results).id
