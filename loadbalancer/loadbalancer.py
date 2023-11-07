from enum import Enum

class LoadBalancerType(Enum):
    RANDOM = 1
    LEAST_REQUEST = 2

class LoadBalancer:
    def __init__(self):
        self.service = None

    def attach_service(self, service):
        self.service = service
    
    def choose_pod(self):
        raise Exception("Not implemented")