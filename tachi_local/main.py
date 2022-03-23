from . import (
    cmdline_parser,
    manga_to_json,
    bakaupdates
)


def _get_id(args: cmdline_parser.Args) -> str:
    if args.id_url:
        if args.id_url.isdigit():
            id_ = args.id_url
        else:
            try:
                id_ = bakaupdates.utils.get_id_from_url(args.id_url)
            except ValueError as ex:
                cmdline_parser.exit_program(ex)
    else:
        try:
            id_ = bakaupdates.searcher.search(args.search_string,
                                              args.max_search_results,
                                              args.auto_first_result)
        except ValueError as ex:
            print(ex)
            raise SystemExit from ex

        print(f"\nRetrieving id: {id_}...")

    return id_


def main(argv=None) -> None:
    args = cmdline_parser.handle_args(argv)

    id_ = _get_id(args)

    try:
        manga = bakaupdates.scraper.get_manga(id_)
    except ValueError as ex:
        raise SystemExit(ex) from ex

    if args.output_filename:
        manga_to_json.make_json(manga, args.output_filename, args.keep_status_values)
        print(f'Successfully wrote to "{args.output_filename}"')
    else:
        print(manga_to_json.make_jsons(manga, args.keep_status_values))
