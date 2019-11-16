from ComicPy.Services.abc.Services import Service
from ComicPy.Models.models import Series, Issue, Page
import bs4


class ReadComicsOnlineService(Service):
    def __init__(self):
        super().__init__(base_url='http://readcomicsonline.ru/{}')

    def get_comics_for_series(self, series: Series):
        url = self.__url_for_series(series)
        html = self.get_html_from_web(url)

        soup = bs4.BeautifulSoup(html, 'html.parser')
        comics_data = soup.find(class_='chapters').find_all(href=True)

        return [
            Issue(name=comic_data.text.replace(':', ' -').strip(), url=comic_data.attrs['href'])
            for comic_data in comics_data
        ]

    def get_comic(self, comic: Issue, dir_path):
        url = comic.url
        html = self.get_html_from_web(url)
        # get list of pages
        comic.pages = self.__get_pages_for_comic(html)
        # pages = self.__get_pages_for_comic(html)

        pages_urls = [
            comic.url + '/{}'.format(page)
            for page in comic.pages
        ]

        image_urls = (
            self.__get_image_for_page(page_url)
            for page_url in pages_urls
        )

        for num, url in enumerate(image_urls, 1):
            image_data = self.get_raw_from_web(url)
            self.save_image(dir_path, str(num), image_data)
        self.make_pdf_from_images(dir_path, '.jpg')

    def __url_for_series(self, series: Series):
        return self.base_url.format('comic/' + series.name.replace(' ', '-'))

    def __get_pages_for_comic(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        pages_data = soup.find(class_='selectpicker').find_all('option')

        return (
            page_data.text
            for page_data in pages_data
        )

    def __get_image_for_page(self, page_url):
        html = self.get_html_from_web(page_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')

        return soup.find(class_='img-responsive scan-page')['src'].strip()
