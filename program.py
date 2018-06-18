import comic_service
import os


def main():
    # get user input for what series they want to download
    series = input("Enter the name of the series you would like to download")
    url = comic_service.url_for_series(series)

    # get output location
    folder = get_or_create_output_folder(series_folder=series)

    # download main page from web
    html = comic_service.get_html_from_web(url)

    # parse data and get list of issues
    comics = comic_service.get_comics_from_html(html)

    for comic in comics:
        comic_folder = get_or_create_output_folder(series_folder=series, issue_folder=comic.name)
        # TODO: Skip existing comicsS
        comic_service.get_comic(comic, comic_folder)


def get_or_create_output_folder(series_folder=None, issue_folder=None):
    base_folder = os.path.abspath(os.path.dirname(__file__))
    folder = 'comics'
    full_path = os.path.join(base_folder, folder)

    if series_folder:
        full_path = os.path.join(full_path, series_folder)
        if issue_folder:
            full_path = os.path.join(full_path, issue_folder)

    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        print('Creating new directory at {}'.format(full_path))
        os.mkdir(full_path)

    return full_path


if __name__ == '__main__':
    main()
