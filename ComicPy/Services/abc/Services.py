import collections
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
        with open(filename, 'wb') as fout:
            shutil.copyfileobj(data, fout)
