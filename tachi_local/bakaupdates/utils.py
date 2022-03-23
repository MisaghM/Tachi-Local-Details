import re
import urllib.parse
from typing import Union


_scheme_regex = re.compile(r"^(?:https?)?$", flags=re.IGNORECASE | re.ASCII)
_netloc_regex = re.compile(r"^(?:www\.)?mangaupdates\.com$", flags=re.IGNORECASE | re.ASCII)
_query_regex = re.compile(r"id=(\d+)(?:&|$)", flags=re.IGNORECASE | re.ASCII)


def get_id_from_url(url: str) -> str:
    if "//" not in url:
        url = "//" + url
    url_res = urllib.parse.urlparse(url)

    if not _scheme_regex.match(url_res.scheme):
        raise ValueError("URL is not valid.")
    if not _netloc_regex.match(url_res.netloc):
        raise ValueError("URL is not a valid mangaupdates.com link.")
    if url_res.path != "/series.html":
        raise ValueError("URL is not a manga series page.")

    id_query = _query_regex.search(url_res.query)
    if id_query is None:
        raise ValueError("ID not found in the URL.")

    return id_query.group(1)


def get_url_by_id(id_: Union[str, int]) -> str:
    return "https://www.mangaupdates.com/series.html?id=" + str(id_)
