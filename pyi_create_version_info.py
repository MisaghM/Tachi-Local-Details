from typing import Tuple

from tachi_local.version import __version__


FILENAME = "pyi_win_version_info"


def version_to_tuple(ver: str) -> Tuple[int]:
    res = [0, 0, 0, 0]
    for i, num in enumerate(map(int, ver.split("."))):
        res[i] = num
    return tuple(res)


with open(f"{FILENAME}.template", "r", encoding="utf-8") as file:
    text = file.read()

text = text.format(
    version_tuple=version_to_tuple(__version__),
    version=__version__
)

with open(f"{FILENAME}.py", "w", encoding="utf-8") as file:
    file.write(text)
