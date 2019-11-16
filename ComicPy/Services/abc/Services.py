import os
import img2pdf
import shutil
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Service(ABC):
    CONNECT_TIMEOUT = 5
    READ_TIMEOUT = 5
    MAX_RETRIES = 5

    def __init__(self, base_url: str):
        self.session = None
        self.base_url = base_url
        super().__init__()

    def requests_retry_session(self,
                               retries=MAX_RETRIES,
                               backoff_factor=0.3,
                               status_forcelist=(500, 502, 504),
                               session=None,):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self.session = session
        return self.session

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
    def get_comic(self, comic, dir_path):
        """
        downloads a comic and saves each page as a jpeg,
        then compiles the pages into a pdf

        :param comic: ComicBook named tuple
        :param dir_path: path to directory where images and pdf will be saved
        :return:
        """
        pass

    @staticmethod
    def make_pdf_from_images(folder, image_format):
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

    @staticmethod
    def save_image(folder, name, data):
        """
        Saves image in given location

        :param folder: path of folder to save image
        :param name: name of image as string
        :param data: image data
        :return:
        """
        filename = os.path.join(folder, name + '.jpg')
        if os.path.exists(filename):
            return
        with open(filename, 'wb') as fout:
            shutil.copyfileobj(data, fout)

    def get_html_from_web(self, url):
        try:
            resp = self.requests_retry_session().get(url,
                                                     timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT))
            return resp.text
        except Exception as x:
            print(f"{x.__class__.__name__}: Unable to load the url: {url}")
            raise x

    def get_raw_from_web(self, url):
        try:
            resp = self.requests_retry_session().get(url,
                                                     stream=True,
                                                     timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT))
            return resp.raw

        except Exception as x:
            print(f"{x.__class__.__name__}: Unable to load the image from url: {url}")
            raise x