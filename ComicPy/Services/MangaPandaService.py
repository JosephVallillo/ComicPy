from ComicPy.Services.abc.Services import Service, ComicBook
import bs4
import requests


class MangaPandaService(Service):
    def __init__(self):
        super().__init__(base_url='https://mangapanda.com/{}')

    def get_comics_for_series(self, series):
        pass

    def get_comic(self, comic: ComicBook, dir_path):
        pass