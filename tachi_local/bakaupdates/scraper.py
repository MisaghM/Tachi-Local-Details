from typing import List, Union

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


def _get_text(tag: bs4.Tag, recursive: bool = True) -> List[str]:
    strings = [x.strip().replace("\u00A0", " ")
               for x in tag.find_all(string=True, recursive=recursive)
               if not x.isspace() and not isinstance(x, bs4.Comment)]
    if strings and strings[0] == "N/A":
        strings = []
    return strings


class _MangaHandler:
    def __init__(self):
        self.manga = Manga.create_empty_instance()

    def extract_from_html(self, page_html: bytes) -> Manga:
        doc = bs4.BeautifulSoup(page_html, "html.parser")

        title = doc.find("span", class_="releasestitle")
        if title is None:
            raise ValueError("Manga not found.")
        self.manga.name = title.string.strip()

        for item in doc.select("div[class^='info-box'][class$='sCat']"):
            item_text = item.get_text().strip()
            if item_text in self._attribute_map:
                content_tag = item.find_next_sibling("div")
                self._attribute_map[item_text](self, content_tag)

        return self.manga

    def _creator(self, tag: bs4.Tag) -> Union[str, List[str]]:
        text = _get_text(tag)
        names = [x for x in text if x not in ("Add", "]")]

        if len(names) != len(text):
            for i, x in enumerate(names):
                if x[-1] == "[":
                    names[i] = x[:-1].strip()

        if not names:
            return ""
        if len(names) == 1:
            return names[0]
        return names

    def _alt_names(self, tag: bs4.Tag):
        alts = _get_text(tag)
        self.manga.alt_names = alts

    def _author(self, tag: bs4.Tag):
        names = self._creator(tag)
        self.manga.author = names

    def _artist(self, tag: bs4.Tag):
        names = self._creator(tag)
        self.manga.artist = names

    def _description(self, tag: bs4.Tag):
        if len(tag.contents) > 0:
            tag = tag.contents[0]
        description = "\n".join(_get_text(tag))
        self.manga.description = description

    def _year(self, tag: bs4.Tag):
        year = _get_text(tag)
        if year:
            self.manga.year = int(year[0])
        else:
            self.manga.year = 0

    def _tags(self, tag: bs4.Tag):
        tags = _get_text(tag)
        if tags:
            tags.pop()
        self.manga.tags = tags

    def _status(self, tag: bs4.Tag):
        status = " ".join(_get_text(tag)).lower()
        if "ongoing" in status:
            self.manga.status = Manga.Status.ongoing
        elif "complete" in status:
            self.manga.status = Manga.Status.completed
        elif "canceled" in status:
            self.manga.status = Manga.Status.canceled
        elif "haitus" in status:
            self.manga.status = Manga.Status.hiatus
        else:
            self.manga.status = Manga.Status.unknown

    def _licensed(self, tag: bs4.Tag):
        license_ = _get_text(tag, recursive=False)
        if license_:
            self.manga.licensed = license_[0].lower() == "yes"
        else:
            self.manga.licensed = False

    def _magazine(self, tag: bs4.Tag):
        mangazine = _get_text(tag)
        if len(mangazine) == 1:
            mangazine = mangazine[0]
        self.manga.magazine = mangazine

    _attribute_map = {
        "Associated Names": _alt_names,
        "Author(s)": _author,
        "Artist(s)": _artist,
        "Description": _description,
        "Year": _year,
        "Genre": _tags,
        "Status in Country of Origin": _status,
        "Licensed (in English)": _licensed,
        "Serialized In (magazine)": _magazine,
    }


def get_manga(id_: str) -> Manga:
    return _MangaHandler().extract_from_html(_get_html(id_))
