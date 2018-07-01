import comic_service
import os
import argparse


def get_or_create_output_folder(series_folder=None, issue_folder=None):
    base_folder = os.path.abspath(os.path.dirname(__file__))
    folder = 'comics'
    full_path = os.path.join(base_folder, folder)

    if series_folder:
        full_path = os.path.join(full_path, series_folder)
        if issue_folder:
            full_path = os.path.join(full_path, issue_folder)

    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        print('Creating new directory at {}'.format(full_path))
        os.mkdir(full_path)

    return full_path


def _get_comics_for_series(series):
    url = comic_service.url_for_series(series)

    # get output location
    folder = get_or_create_output_folder(series_folder=series)

    # download main page from web
    html = comic_service.get_html_from_web(url)

    # parse data and get list of issues
    comics = comic_service.get_comics_from_html(html)

    for comic in comics:
        if os.path.exists(os.path.join(folder, comic.name)):
            print("We already have {}, no need to download".format(comic.name))
            continue
        comic_folder = get_or_create_output_folder(series_folder=series, issue_folder=comic.name)
        comic_service.get_comic(comic, comic_folder)


def get_comics_for_series(args):
    _get_comics_for_series(args.series)


def _create_pdf_for_issue(folder):
    comic_service.make_pdf_from_images(folder)


def create_pdf_for_issue(args):
    _create_pdf_for_issue(args.issue)


def main():
    # create top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Help for subcommands')

    # create the parse for get_comics_for_series
    parser_gcfs = subparsers.add_parser('getComicsForSeries',
                                        help='Downloads all comics for a given series name')
    parser_gcfs.add_argument('--series',
                             action="store",
                             dest='series',
                             type=str,
                             help="name of series")
    parser_gcfs.set_defaults(func=get_comics_for_series)

    # create parser for creating pdf from a folder of jpgs
    parser_pdf = subparsers.add_parser('createPDF',
                                       help='Creates a PDF for an issue that is only jpgs')
    parser_pdf.add_argument('--issue',
                            action="store",
                            dest="issue",
                            type=str,
                            help="path to issue folder")
    parser_pdf.set_defaults(func=create_pdf_for_issue)

    # create parser for taking in multiple series
    # create parser for taking in a file

    # parse arguments
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
