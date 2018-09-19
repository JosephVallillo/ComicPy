import requests
import collections
import bs4
import os
import img2pdf
import shutil


ComicBook = collections.namedtuple('ComicBook',
                                   'name url')

class Service:
    def __init__(self, url: str):
        self.base_url = url


    def get_html_from_web(url):
        """
        gets the html of a given url as a string

        :param url: string of url
        :return: html as string
        """
        response = requests.get(url)
        return response.text


    def get_page_data_from_web(url):
        """
        gets raw image data of comic page from url

        :param url: url as string
        :return: raw image data
        """
        return requests.get(url, stream=True).raw


    def make_pdf_from_images(folder):
        """
        Condenses issue into a single pdf

        :param folder: path to folder contain issue jpgs
        :return:
        """
        file = os.path.join(folder, os.path.basename(folder) + '.pdf')
        with open(file, 'wb') as fout:
            fout.write(img2pdf.convert(sorted([
                os.path.join(folder, i) for i in os.listdir(folder) if i.endswith('.jpg')
            ], key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))
            ))
        fout.close()

        images = [os.path.join(folder, i) for i in os.listdir(folder) if i.endswith('.jpg')]
        for image in images:
            os.remove(image)


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


def RCOService(Service):
    """
    adaptation of comic_service.py as class to support using readcomiconline.org
    """
    def __init__(self, url):
        super.__init__(url)


    def url_for_series(self, series):
        """
        formats a given series name to be URI compatible

        :param series: name of series as string
        :return: formatted name of series as string
        """
        return self.url.format('comic/' + series.replace(' ', '-'))

    def get_comics_for_series(self, series):
        pass


    def get_comics_from_html(self, html):
        """
        gets list of comics from html

        :param comics: list of Comics for recursive pages
        :param html: html as string
        :return: list of Comic tuples
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        comics_data = soup.find_all(class_="chapter")

        return [
            ComicBook(name=comic_data.text.strip(), url=self.url.format('read/' + comic_data.attrs['href']))
            for comic_data in comics_data
        ]

    def get_comic(self, comic, folder):
        """
        saves comic as set of jpgs

        :param comic: Comic tuple
        :param folder: absolute path to folder where images are saved
        :return:
        """
        url = comic.url
        html = self.get_html_from_web(url)
        page_urls = get_pages_from_html(html)

        for page_num, page_url in enumerate(page_urls, 1):
            page_data = self.get_page_data_from_web(page_url)
            self.save_image(folder, str(page_num), page_data)
        self.make_pdf_from_images(folder)

    def get_pages_from_html(html):
        """
        gets list of pages from html

        :param html: html as string
        :return: list of urls for jpg
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        pages_data = soup.find_all(class_="chapter-img")

        if not pages_data:
            return None

        return [
            page_data.attrs['src'].strip()
            for page_data in pages_data
        ]


