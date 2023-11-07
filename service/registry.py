from .service import Service

class ServiceRegistry():
    def __init__(self):
        self.services = {}

    def register(self, service):
        self.services[service.name] = service

    def get_service(self, name) -> Service:
        return self.services[name]

    def get_all(self):
        return self.services.values()