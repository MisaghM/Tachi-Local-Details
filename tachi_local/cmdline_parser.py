import sys
import argparse
from typing import NamedTuple, Union

from .version import __version__


DEFAULT_FILENAME = "details.json"
DEFAULT_MAX_RESULTS = 8


class Args(NamedTuple):
    id_url: Union[str, None]
    search_string: Union[str, None]
    auto_first_result: bool
    max_search_results: int
    keep_status_values: bool
    output_filename: str


class _IntRangeCheckType:
    __slots__ = ("range_",)

    def __init__(self, range_: range) -> None:
        self.range_ = range_

    def __call__(self, x: str) -> int:
        try:
            x = int(x)
        except ValueError as ex:
            raise argparse.ArgumentTypeError(f"invalid int value: {x}") from ex

        if x not in self.range_:
            text = f"invalid choice: {x} (choose from range {self.range_.start} to {self.range_.stop - 1}"

            if self.range_.step != 1:
                text += f" [step={self.range_.step}]"
            text += ")"

            raise argparse.ArgumentTypeError(text)

        return x


def _init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tachi-local",
        usage="%(prog)s [link/id] or [-s title]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"Tachiyomi local manga '{DEFAULT_FILENAME}' creator using Baka-Updates Manga.\n"
                    "Pass a mangaupdates.com link or id in the command-line arguments,\n"
                    "or use '-s title' to search for a manga.",
        add_help=False,
        allow_abbrev=False
    )

    main_cmds_grouper = parser.add_argument_group(title="main commands")
    main_cmds = main_cmds_grouper.add_mutually_exclusive_group(required=True)
    main_cmds.add_argument(
        "id_url",
        metavar="link/id",
        nargs="?",
        help="mangaupdates.com link or id"
    )
    main_cmds.add_argument(
        "-s",
        "--search",
        metavar="title",
        help="search for a title"
    )

    search_grouper = parser.add_argument_group(title="search options")
    search_group = search_grouper.add_mutually_exclusive_group()
    search_group.add_argument(
        "-a",
        "--auto-first-result",
        action="store_true",
        help="automatically select the first search result"
    )
    search_group.add_argument(
        "-m",
        "--max-search-results",
        type=_IntRangeCheckType(range(1, 26)),
        metavar="[1-25]",
        default=None,  # default to None and handle later
        help=f"maximum search results to show (default: {DEFAULT_MAX_RESULTS})"
    )

    options = parser.add_argument_group(title="options")
    options.add_argument(
        "-h",
        "--help",
        action="help",
        help="show this help message and exit"
    )
    options.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}"
    )
    options.add_argument(
        "-k",
        "--keep-status-values",
        action="store_true",
        help='keep the "_status values" entry in the json'
    )
    options.add_argument(
        "-o",
        "--output",
        metavar="name",
        default=DEFAULT_FILENAME,
        help=f'output filename. pass "" to write to stdout (default: {DEFAULT_FILENAME})'
    )

    return parser


_parser = _init_parser()


def exit_program(message, error: bool = True) -> None:
    if error:
        _parser.print_usage(sys.stderr)
        raise SystemExit(message)
    else:
        _parser.print_usage(sys.stdout)
        print(message)
        raise SystemExit


def handle_args(argv=None) -> Args:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        exit_program("use -h or --help to see a list of all options.", error=False)

    args = _parser.parse_args(argv)

    if args.search is not None:
        if args.max_search_results is None:
            args.max_search_results = DEFAULT_MAX_RESULTS
    else:
        if args.auto_first_result:
            _parser.error("argument --auto-first-result not allowed without argument -s/--search")
        if args.max_search_results is not None:
            _parser.error("argument -m/--max-search-results not allowed without argument -s/--search")

    return Args(
        args.id_url,
        args.search,
        args.auto_first_result,
        args.max_search_results,
        args.keep_status_values,
        args.output
    )
