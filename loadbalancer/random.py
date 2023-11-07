from .loadbalancer import LoadBalancer

import random

class RandomLoadBalancer(LoadBalancer):
    def __init__(self):
        super().__init__()
        self.random = random.Random()

    def choose_pod(self):
        if self.service == None:
            raise Exception("Service is not attached to load balancer")
        
        pods = self.service.get_pods()
    
        return self.random.choice(pods)