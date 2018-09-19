import requests
import collections
import bs4
import os
import img2pdf
import shutil
from selenium import webdriver
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

    # @abstractmethod
    # def get_html_from_web(url):
    #     """
    #     gets the html of a given url as a string
    #
    #     :param url: string of url
    #     :return: html as string
    #     """
    #     pass
    #     # response = requests.get(url)
    #     # return response.text
    #
    #
    # @abstractmethod
    # def get_raw_from_web(url):
    #     """
    #     gets raw image data of comic page from url
    #
    #     :param url: url as string
    #     :return: raw image data
    #     """
    #     pass
    #     # return requests.get(url, stream=True).raw
    #
    #
    # @abstractmethod
    # def url_for_series(self, series):
    #     pass
    #
    #
    # @abstractmethod
    # def get_comics_for_series(self, series):
    #     pass
    #
    # @abstractmethod
    # def get_comic(self, comic, folder):
    #     pass
    #
    # @abstractmethod
    # def get_pages_from_comic(comic):
    #     pass

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


def RCOService(Service):
    """
    adaptation of comic_service.py as class to support using readcomiconline.to
    """

    def get_comics_for_series(self, series):
        # get url for series
        url = __url_for_series(self, series)
        # download html for series
        html = __get_html_from_web(url)
        # parse html
        soup = bs4.BeautifulSoup(html, 'html.parser')
        comics_data = soup.find_all(class_="chapter")
        # return list of comics
        return [
            ComicBook(name=comic_data.text.strip(), url=self.url.format('read/' + comic_data.attrs['href']))
            for comic_data in comics_data
        ]

    def get_comic(self, comic: ComicBook, dir_path):
        # get url of comic
        url = comic.url
        # download html for comic
        html = __get_html_from_web(url)
        # get list of pages
        pages = __get_pages_from_html(html)
        # download and save each page
        for page_num, page_url in enumerate(pages, 1):
            page_data = __get_raw_from_web(page_url)
            self.save_image(dir_path, str(page_num), page_data)
        self.make_pdf_from_images(dir_path)
#TODO: implement
    def __get_html_from_web(url):
        pass
#TODO: implement
    def __get_raw_from_web(url):
        pass

    def __url_for_series(self, series):
        """
        formats a given series name to be URI compatible

        :param series: name of series as string
        :return: formatted name of series as string
        """
        return self.url.format('comic/' + series.replace(' ', '-'))

#TODO : Need to update parsing
    def __get_pages_from_html(html):
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


