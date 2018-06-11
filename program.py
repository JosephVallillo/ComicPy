import requests
import bs4
import collections
import comic_service

ComicBook = collections.namedtuple('ComicBook',
                                   'name url')

def main():
    # get output location
    folder = get_or_create_output_folder()

    # get user input for what series they want to download
    series = input("")

    # download main page from web
    html = get_html_from_web(series)

    # parse data and get list of issues we dont have
    comics = get_comics_from_html(html)

    for comic in comics:
        comic_service.download_comic(comic, folder)


def get_or_create_output_folder():
    pass

def get_html_from_web(series):
    url = url_for_series(series)
    response = requests.get(url)

    return response.text


def url_for_series(series):
    pass


def get_comics_from_html(html):
    pass


if __name__ == '__main__':
    main()