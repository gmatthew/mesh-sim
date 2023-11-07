from .loadbalancer import LoadBalancer

import random

class LeastRequestLoadBalancer(LoadBalancer):
    def __init__(self):
        super().__init__()
        self.random = random.Random()

    def choose_pod(self):
        if self.service == None:
            raise Exception("Service is not attached to load balancer")
        
        pods = self.service.get_pods()

        if not pods:
            raise Exception("No pods available")
        
        # If there is only one pod, return it
        if len(pods) == 1:
            return pods[0]
        
        pod_a = self.random.choice(pods)

        while True:
            pod_b = self.random.choice(pods)
            if pod_a != pod_b:
                break

        if pod_a.get_inflight_requests() < pod_b.get_inflight_requests():
            return pod_a
        else:
            return pod_b