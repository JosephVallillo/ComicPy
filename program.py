import comic_service
import os


def main():
    # get output location
    folder = get_or_create_output_folder()

    # get user input for what series they want to download
    #series = input("")
    series = "weapon x 2017"
    url = comic_service.url_for_series(series)

    # download main page from web
    html = comic_service.get_html_from_web(url)

    # parse data and get list of issues
    comics = comic_service.get_comics_from_html(html)

    for comic in comics:
        # TODO: Determine if we have the comic first and skip if we do
        comic_service.get_comic(comic, folder)



def get_or_create_output_folder():
    return r"C:\users\jvallillo\desktop\test"


if __name__ == '__main__':
    main()
