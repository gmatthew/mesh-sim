from .service import Service
from logger import Logger

class ServiceRegistry(Logger):
    def __init__(self):
        super().__init__()
        self.services = {}

    def register(self, service):
        self.services[service.name] = service

    def get_service(self, name) -> Service:
        return self.services[name]

    def get_all(self):
        return self.services.values()