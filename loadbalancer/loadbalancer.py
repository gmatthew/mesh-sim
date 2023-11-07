from enum import Enum
from logger import Logger

class LoadBalancerType(Enum):
    RANDOM = 1
    LEAST_REQUEST = 2

class LoadBalancer(Logger):
    def __init__(self):
        super().__init__()
        self.service = None

    def attach_service(self, service):
        self.service = service
    
    def choose_pod(self):
        raise Exception("Not implemented")