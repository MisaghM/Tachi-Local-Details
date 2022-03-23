from dataclasses import dataclass
from enum import Enum
from typing import Union, List


@dataclass
class Manga:
    class Status(Enum):
        unknown = 0
        ongoing = 1
        completed = 2
        canceled = 3
        hiatus = 4

    __slots__ = (
        "name",
        "alt_names",
        "author",
        "artist",
        "description",
        "year",
        "tags",
        "status",
        "licensed",
        "magazine"
    )

    name: str
    alt_names: List[str]
    author: Union[str, List[str]]
    artist: Union[str, List[str]]
    description: str
    year: int
    tags: List[str]
    status: Status
    licensed: bool
    magazine: Union[str, List[str]]

    @classmethod
    def create_empty_instance(cls):
        return cls("", [], "", "", "", 0, [], Manga.Status.unknown, False, "")
