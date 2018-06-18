import requests
import collections
import bs4
import os
import shutil
import img2pdf

ComicBook = collections.namedtuple('ComicBook',
                                   'name url')
root = "https://readcomics.io/comic/{}"


def get_html_from_web(url):
    """
    gets the html of a given url as a string

    :param url: string of url
    :return: html as string
    """
    response = requests.get(url)
    return response.text


def url_for_series(series):
    """
    formats a given series name to be URI compatible

    :param series: name of series as string
    :return: formatted name of series as string
    """
    return root.format(series.replace(' ', '-'))


def get_comics_from_html(html):
    """
    gets list of comics from html

    :param html: html as string
    :return: list of Comic tuples
    """
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

# TODO: Fix folder/file naming, handle multiple pages
def get_comic(comic, folder):
    """
    saves comic as set of jpgs

    :param comic: Comic tuple
    :param folder: absolute path to folder where images are saved
    :return:
    """
    url = comic.url
    html = get_html_from_web(url + '/full')
    page_urls = get_pages_from_html(html)
    page_num = 0
    for page_url in page_urls:
        page_num += 1
        page_data = get_page_data_from_web(page_url)
        save_image(folder, str(page_num), page_data)
    #make_pdf_from_images(folder)


def get_pages_from_html(html):
    """
    gets list of pages from html

    :param html: html as string
    :return: list of urls for jpg
    """
    pages = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    pages_data = soup.find_all(class_="chapter_img")

    if not pages_data:
        return pages

    for page_data in pages_data:
        pages.append(page_data.attrs['src'])

    return pages


def get_page_data_from_web(url):
    """
    gets raw image data of comic page from url

    :param url: url as string
    :return: raw image data
    """
    return requests.get(url, stream=True).raw


# TODO: Need to fix
def make_pdf_from_images(folder):
    """
    Condenses issue into a single pdf

    :param folder: path to folder contain issue jpgs
    :return:
    """
    file = os.path.basename(folder) + '.pdf'
    print(file)
    with open(file, 'wb') as fout:
        fout.write(img2pdf.convert([i for i in os.listdir(folder) if i.endswith('.jpg')]))


def save_image(folder, name, data):
    """
    Saves image in given location

    :param folder: path of folder to save image
    :param name: name of image as string
    :param data: image data
    :return:
    """
    filename = os.path.join(folder, name + '.jpg')
    with open(filename, 'wb') as fout:
        shutil.copyfileobj(data, fout)
