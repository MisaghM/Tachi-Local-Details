from distutils.util import strtobool

import requests
import bs4

from . import utils
from ..manga import Manga


def _get_html(id_: str) -> bytes:
    url = utils.get_url_by_id(id_)

    try:
        page = requests.get(url, timeout=20)
    except requests.exceptions.RequestException as ex:
        raise SystemExit(ex) from ex

    return page.content


_manga_attribute_map = {
    "Associated Names": "alt_names",
    "Author(s)": "author",
    "Artist(s)": "artist",
    "Description": "description",
    "Year": "year",
    "Genre": "tags",
    "Status in Country of Origin": "status",
    "Licensed (in English)": "licensed",
    "Serialized In (magazine)": "magazine"
}


def _extract_from_html(page_html: bytes) -> Manga:
    doc = bs4.BeautifulSoup(page_html, "html.parser")
    manga = Manga.create_empty_instance()

    title = doc.find("span", class_="releasestitle")
    if title is None:
        raise ValueError("Manga not found.")
    manga.name = title.string.strip()

    for item in doc.find_all("div", class_="sCat"):
        item_text = item.get_text().strip()
        if item_text in _manga_attribute_map:
            content = list(item.find_next_sibling("div", class_="sContent").stripped_strings)
            if len(content) == 1:
                content = content[0]
                if content == "N/A":
                    content = ""
            setattr(manga, _manga_attribute_map[item_text], content)

    return manga


def _scrape_data(page_html: bytes) -> Manga:
    manga = _extract_from_html(page_html)

    if isinstance(manga.status, list):
        manga.status = " ".join(manga.status)
    manga.status = manga.status.lower()
    if "ongoing" in manga.status:
        manga.status = Manga.Status.ongoing
    elif "complete" in manga.status:
        manga.status = Manga.Status.completed
    elif "canceled" in manga.status:
        manga.status = Manga.Status.canceled
    elif "haitus" in manga.status:
        manga.status = Manga.Status.hiatus
    else:
        manga.status = Manga.Status.unknown

    if isinstance(manga.description, list):
        manga.description = "\n".join(manga.description)

    manga.licensed = bool(strtobool(manga.licensed))

    if manga.alt_names:
        if isinstance(manga.alt_names, str):
            manga.alt_names = [manga.alt_names]
    else:
        manga.alt_names = []

    if manga.tags:
        manga.tags.pop()
    else:
        manga.tags = []

    if manga.year:
        manga.year = int(manga.year)
    else:
        manga.year = None

    return manga


def get_manga(id_: str) -> Manga:
    return _scrape_data(_get_html(id_))
