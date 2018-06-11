import requests
import collections
import bs4
import os
import shutil

ComicBook = collections.namedtuple('ComicBook',
                                   'name url')
root = "https://readcomics.io/comic/{}"


def get_html_from_web(url):
    response = requests.get(url)
    return response.text


def url_for_series(series):
    return root.format(series.replace(' ', '-'))


def get_comics_from_html(html):
    comics = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    comics_data = soup.find_all(class_="ch-name")

    if not comics_data:
        return comics

    for comic_data in comics_data:
        name = comic_data.string.strip()
        url = comic_data.attrs['href']
        comics.append((ComicBook(name=name, url=url)))

    return comics

# TODO: Fix folder/file naming
def get_comic(comic, folder):
    url = comic.url
    html = get_html_from_web(url + '/full')
    page_urls = get_pages_from_html(html)
    for page_url in page_urls:
        page_data = get_page_data_from_web(page_url)
        save_image(folder, comic.name, page_data)
    make_pdf_from_images(folder)


def get_pages_from_html(html):
    pages = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    pages_data = soup.find_all(class_="chapter_img")

    if not pages_data:
        return pages

    for page_data in pages_data:
        pages.append(page_data.attrs['src'])

    return pages


def get_page_data_from_web(url):
    return requests.get(url, stream=True)

# TODO: Need to implement
def make_pdf_from_images(folder):
    pass

def save_image(folder, name, data):
    filename = os.path.join(folder, name + '.jpg')
    with open(filename, 'wb') as fout:
        shutil.copyfileobj(data, fout)
