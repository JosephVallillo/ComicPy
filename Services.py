import requests
import collections
import bs4
import os
import img2pdf
import shutil
from abc import ABC, abstractmethod


ComicBook = collections.namedtuple('ComicBook',
                                   'name url')

class Service(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        super().__init__()


    @abstractmethod
    def get_comics_for_series(self, series):
        """
        public facing method that returns an array of Comics.
        This needs to be implemented for all derived classes

        :param series: name of series
        :return: list of Comics
        """
        pass


    @abstractmethod
    def get_comic(self, comic: ComicBook, dir_path):
        """
        downloads a comic and saves each page as a jpeg,
        then compiles the pages into a pdf

        :param comic: ComicBook named tuple
        :param dir_path: path to directory where images and pdf will be saved
        :return:
        """
        pass


    def make_pdf_from_images(self, folder, image_format):
        """
        Condenses issue into a single pdf

        :param folder: path to folder contain issue jpgs
        :return:
        """
        file = os.path.join(folder, os.path.basename(folder) + '.pdf')
        with open(file, 'wb') as fout:
            fout.write(img2pdf.convert(sorted([
                os.path.join(folder, i) for i in os.listdir(folder) if i.endswith(image_format)
            ], key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))
            ))
        fout.close()

        images = [os.path.join(folder, i) for i in os.listdir(folder) if i.endswith(image_format)]
        for image in images:
            os.remove(image)


    def save_image(self, folder, name, data):
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



class ReadComicsOnlineService(Service):

    def get_comics_for_series(self, series):
        url = self.__url_for_series(series)
        resp = requests.get(url)

        if resp.status_code != 200:
            return

        html = resp.text

        soup = bs4.BeautifulSoup(html, 'html.parser')
        comics_data = soup.find(class_='chapters').find_all(href=True)

        return [
                ComicBook(name=comic_data.text.replace(':', ' -').strip(), url=comic_data.attrs['href'])
                for comic_data in comics_data
        ]

    def get_comic(self, comic: ComicBook, dir_path):
        url = comic.url
        html = self.__get_html_from_web(url)
        # get list of pages
        pages = self.__get_pages_for_comic(html)

        pages_urls = [
            comic.url + '/{}'.format(page)
            for page in pages
        ]

        image_urls = (
            self.__get_image_for_page(page_url)
            for page_url in pages_urls
        )

        for num, url in enumerate(image_urls, 1):
            image_data = self.__get_raw_from_web(url)
            self.save_image(dir_path, str(num), image_data)
        self.make_pdf_from_images(dir_path, '.jpg')


    def __url_for_series(self, series):
        return self.base_url.format('comic/' + series.replace(' ', '-'))

    def __get_html_from_web(self, url):
        try:
            response = requests.get(url)
            return response.text
        except:
            print('Could not find URL: {}'.format(url))

    def __get_raw_from_web(self, url):
        return requests.get(url, stream=True).raw


    def __get_pages_for_comic(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        pages_data = soup.find(class_='selectpicker').find_all('option')

        return [
            page_data.text
            for page_data in pages_data
        ]

    def __get_image_for_page(self, page_url):
        html = self.__get_html_from_web(page_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')

        return soup.find(class_='img-responsive scan-page')['src'].strip()
