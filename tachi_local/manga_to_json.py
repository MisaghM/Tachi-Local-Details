import json

from .manga import Manga


def make_json(manga: Manga, filename: str, keep_status_values: bool = True) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(_make_dict(manga, keep_status_values), file, indent=4)


def make_jsons(manga: Manga, keep_status_values: bool = True) -> str:
    return json.dumps(_make_dict(manga, keep_status_values), indent=4)


_status_values_map = {
    Manga.Status.unknown: "0",
    Manga.Status.ongoing: "1",
    Manga.Status.completed: "2",
    Manga.Status.canceled: "5",
    Manga.Status.hiatus: "6"
}


def _make_dict(manga: Manga, keep_status_values: bool = True) -> dict:
    detail_dict = {
        "title": manga.name,
        "author": manga.author if isinstance(manga.author, str) else ", ".join(manga.author),
        "artist": manga.artist if isinstance(manga.artist, str) else ", ".join(manga.artist),
        "description": manga.description,
        "genre": (manga.tags,) if isinstance(manga.tags, str) else manga.tags,
        "status": _status_values_map[manga.status]
    }
    if keep_status_values:
        detail_dict["_status values"] = (
            "0 = Unknown",
            "1 = Ongoing",
            "2 = Completed",
            "3 = Licensed",
            "4 = Publishing finished",
            "5 = Cancelled",
            "6 = On hiatus"
        )
    return detail_dict
