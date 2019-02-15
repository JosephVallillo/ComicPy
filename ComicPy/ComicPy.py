import ComicPy.Services as Services

class ComicPy:
    def create_service(self, format):
        service = factory.get_service(format)
        # if svc == 'ReadComicsOnlineService':
        #     return ReadComicsOnlineService()
        return service


class ComicPyFactory:
    def __init__(self):
        self._services = {}

    def register_service(self, format, service):
        self._services[format] = service

    def get_service(self, format):
        creator = self._services.get(format)
        if not creator:
            raise ValueError(format)
        return creator()

factory = ComicPyFactory()
factory.register_service('ReadComicsOnline', Services.ReadComicsOnlineService)