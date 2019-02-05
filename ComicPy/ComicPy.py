from .Services.ReadComicsOnlineService import ReadComicsOnlineService


class ComicPy:
    @staticmethod
    def create_service():
        # if svc == 'ReadComicsOnlineService':
        #     return ReadComicsOnlineService()
        return ReadComicsOnlineService()
