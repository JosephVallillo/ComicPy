import os
import argparse
from ComicPy import ComicPy
from ComicPy.Models.models import Series
from pathlib import Path

comicpy = ComicPy()
comic_service = comicpy.create_service('ReadComicsOnline')
manga_service = comicpy.create_service('MangaPanda')

# TODO: Add logging
# TODO: Add error handling


def get_or_create_output_folder(root_folder=None, series_folder=None, issue_folder=None):
    base_folder = os.path.abspath(os.path.dirname(__file__))
    folder = 'comics'
    full_path = os.path.join(base_folder, folder)

    if root_folder:
        full_path = os.path.join(full_path, root_folder)
    if series_folder:
        full_path = os.path.join(full_path, series_folder)
    if issue_folder:
        full_path = os.path.join(full_path, issue_folder)

    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        print('Creating new directory at {}'.format(full_path))
        path = Path(full_path)
        path.mkdir(parents=True, exist_ok=True)

    return full_path


def _get_comics_for_series(series: Series, type):
    # get output location
    folder = get_or_create_output_folder(root_folder=series.root, series_folder=series.name)

    if type == 0:
        service = comic_service
    else:
        service = manga_service

    comics = service.get_comics_for_series(series)

    for comic in comics:
        if os.path.exists(os.path.join(folder, comic.name)) and os.path.exists(
                os.path.join(folder, comic.name, comic.name + '.pdf')):
            print("We already have {}, no need to download".format(comic.name))
            if any(image for image in os.listdir(os.path.join(folder, comic.name)) if image.endswith('.jpg')):
                print("We already have the pdf, deleting jpegs...")
                images = [f for f in os.listdir(os.path.join(folder, comic.name)) if f.endswith('.jpg')]
                for image in images:
                    os.remove(os.path.join(os.path.join(folder, comic.name, image)))
            continue
        comic_folder = get_or_create_output_folder(root_folder=series.root, series_folder=series.name,
                                                   issue_folder=comic.name)
        try:
            service.get_comic(comic, comic_folder)
        except:
            continue


def get_comics_for_series(args):
    _get_comics_for_series(args.series, args.type)


def _read_series_from_file(path=None):
    if not path:
        _read_series_from_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'series.txt'))
        return

    with open(path) as fin:
        lines = fin.readlines()

    root = None
    root_type = None
    comic_series = []
    manga_series = []

    for line in lines:
        if line.strip() == '':
            continue
        if line.startswith('#'):
            root = line.replace('#', '').strip()
            root_type = 0
            continue
        elif line.startswith('-'):
            root = line.replace('-', '').strip()
            root_type = 1
            continue
        if root is not None and root_type == 0:
            comic_series.append(Series(root=root, name=line.strip()))
        elif root is not None and root_type == 1:
            manga_series.append(Series(root=root, name=line.strip()))

    for item in comic_series:
        _get_comics_for_series(item, 0)

    for item in manga_series:
        _get_comics_for_series(item, 1)


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
    parser_gcfs.add_argument('--type',
                             action="store",
                             dest='type',
                             type=str,
                             help="type of series")
    parser_gcfs.set_defaults(func=get_comics_for_series)

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
