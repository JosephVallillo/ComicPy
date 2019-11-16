from ComicPy.Services.abc.Services import Service
from ComicPy.Models.models import Series, Issue
import bs4


class MangaPandaService(Service):
    def __init__(self):
        super().__init__(base_url='https://www.mangapanda.com{}')

    def get_comics_for_series(self, series: Series):
        url = self.__url_for_series(series)
        html = self.get_html_from_web(url)

        soup = bs4.BeautifulSoup(html, 'html.parser')
        comics_data = soup.find(id='chapterlist').find_all('td')

        return (
            Issue(name=comic_data.text.strip().replace(':', '').replace('?', '').replace('\"', '').replace('*',
                                                                                                               '').strip(),
                      url=self.base_url.format(comic_data.find(href=True).attrs['href']))
            for comic_data in comics_data
            if comic_data.find(href=True)
        )

    def get_comic(self, comic: Issue, dir_path):
        url = comic.url
        html = self.get_html_from_web(url)

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
            image_data = self.get_raw_from_web(url)
            self.save_image(dir_path, str(num), image_data)
        self.make_pdf_from_images(dir_path, '.jpg')

    def __url_for_series(self, series):
        return self.base_url.format("/" + series.name.replace(' ', '-'))

    def __get_pages_for_comic(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        pages_data = soup.find_all('option')

        return (
            page_data.text
            for page_data in pages_data
        )

    def __get_image_for_page(self, page_url):
        html = self.get_html_from_web(page_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')

        return soup.find(id='img')['src'].strip()
