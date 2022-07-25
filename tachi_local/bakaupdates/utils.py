import re
import urllib.parse


_scheme_regex = re.compile(r"^(?:https?)?$", flags=re.IGNORECASE | re.ASCII)
_netloc_regex = re.compile(r"^(?:www\.)?mangaupdates\.com$", flags=re.IGNORECASE | re.ASCII)
_path_regex = re.compile(r"^/series/([a-z0-9]{7})(?:(?:/|#|\?).*)?$", flags=re.IGNORECASE | re.ASCII)
_query_regex = re.compile(r"(?:^|&)id=(\d+)(?:&|$)", flags=re.IGNORECASE | re.ASCII)


def get_id_from_url(url: str) -> str:
    if "//" not in url:
        url = "//" + url
    url_res = urllib.parse.urlparse(url)

    if not _scheme_regex.match(url_res.scheme):
        raise ValueError("URL is not valid.")
    if not _netloc_regex.match(url_res.netloc):
        raise ValueError("URL is not a valid mangaupdates.com link.")

    if url_res.path.startswith("/series/"):
        id_ = _path_regex.match(url_res.path)
    elif url_res.path == "/series.html":
        id_ = _query_regex.search(url_res.query)
    else:
        raise ValueError("URL is not a manga series page.")

    if id_ is None:
        raise ValueError("ID not found in the URL.")
    return id_.group(1)


def _is_old_id(id_: str) -> bool:
    return len(id_) < 7 and id_.isdigit()


def get_url_by_id(id_: str) -> str:
    if _is_old_id(id_):
        return "https://www.mangaupdates.com/series.html?id=" + id_
    return "https://www.mangaupdates.com/series/" + id_


def is_id(id_: str) -> bool:
    id_match = re.fullmatch(r"[a-z0-9]{7}", id_, flags=re.IGNORECASE | re.ASCII)
    return bool(id_match) or _is_old_id(id_)
