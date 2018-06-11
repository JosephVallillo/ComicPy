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
    #series = input("")
    series = "https://readcomics.io/comic/weapon-x-2017"

    # download main page from web
    html = get_html_from_web(series)

    # parse data and get list of issues we dont have
    comics = get_comics_from_html(html)

    for comic in comics:
        #comic_service.download_comic(comic, folder)
        print(comic)


def get_or_create_output_folder():
    pass


def get_html_from_web(series):
    url = url_for_series(series)
    response = requests.get(url)

    return response.text


def url_for_series(series):
    return series


def get_comics_from_html(html):
    comics = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    comics_data = soup.find_all(class_="ch-name")

    if not comics_data:
        return comics

    for comic_data in comics_data:
        name = comic_data.string.strip()
        url = comic_data.attrs['href']
        comics.append((ComicBook(name=name,url=url)))

    return comics


if __name__ == '__main__':
    main()
