import comic_service
import os
import argparse


#TODO: Download reading order
#TODO: Download comic info

def add_series_to_file(series):
    with open(os.path.join(os.path.dirname(__file__), 'series.txt'), 'r+') as fin:
        for line in fin:
            if series in line.strip():
                break
        else:
            fin.write(series + '\n')



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
    add_series_to_file(series)

    url = comic_service.url_for_series(series)

    # get output location
    folder = get_or_create_output_folder(series_folder=series)

    # download main page from web
    html = comic_service.get_html_from_web(url)

    # parse data and get list of issues
    comics = []
    comics = comic_service.get_comics_from_html(html, comics)

    for comic in comics:
        if os.path.exists(os.path.join(folder, comic.name)):
            print("We already have {}, no need to download".format(comic.name))
            if os.path.exists(os.path.join(folder, comic.name, comic.name + '.pdf')) \
                    and any(image for image in os.listdir(os.path.join(folder, comic.name)) if image.endswith('.jpg')):
                print("We already have the pdf, deleting jpegs...")
                images = [ f for f in os.listdir(os.path.join(folder, comic.name)) if f.endswith('.jpg')]
                for image in images:
                    os.remove(os.path.join(os.path.join(folder, comic.name, image)))
            continue
        comic_folder = get_or_create_output_folder(series_folder=series, issue_folder=comic.name)
        try:
            comic_service.get_comic(comic, comic_folder)
        except:
            continue


def get_comics_for_series(args):
    _get_comics_for_series(args.series)


def _create_pdf_for_issue(folder):
    comic_service.make_pdf_from_images(folder)


def create_pdf_for_issue(args):
    _create_pdf_for_issue(args.issue)


def _read_series_from_file(path=None):
    if not path:
        _read_series_from_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'series.txt'))
        return

    with open(path) as fin:
        books = fin.readlines()

    books = [x.strip() for x in books]

    for book in books:
        _get_comics_for_series(book)


def read_series_from_file(args):
    _read_series_from_file(args.fpath)


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
    parser_file = subparsers.add_parser('downloadFromFile',
                                        help='Downloads all comics for the series stored in a txt file')
    parser_file.add_argument('--fpath',
                             action="store",
                             dest="fpath",
                             type=str,
                             help="path to series file")
    parser_file.set_defaults(func=read_series_from_file)


    # parse arguments
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()