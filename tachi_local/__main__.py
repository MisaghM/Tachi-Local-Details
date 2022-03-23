from pathlib import Path
from importlib import import_module


# running __main__ directly.

package_name = "tachi_local"

# if tachi_local is not next to __main__.py,
# add folder's parent to sys.path to allow package access.
if not __package__:
    here = Path(__file__).resolve().parent
    if here.is_file():
        # running as zipapp.
        # tachi_local must be next to __main__.py
        pass
    elif not (here / package_name).is_dir():
        import sys
        sys.path.insert(1, str(here.parent))
        package_name = here.name

# dynamic import to work when the parent folder's name is not tachi_local.
try:
    main = import_module(f"{package_name}.main")
except ModuleNotFoundError as ex:
    raise SystemExit("error: main.py not found.") from ex

if __name__ == "__main__":
    main.main()
