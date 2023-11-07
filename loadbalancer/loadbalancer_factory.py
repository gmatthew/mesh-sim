from loadbalancer.random import RandomLoadBalancer
from loadbalancer.leastrequest import LeastRequestLoadBalancer
from loadbalancer.loadbalancer import LoadBalancerType

class LoadBalancerFactory:
    def __init__(self):
        pass

    def create_load_balancer(self, lb_type : LoadBalancerType):
        if lb_type == LoadBalancerType.RANDOM:
            return RandomLoadBalancer()
        elif lb_type == LoadBalancerType.LEAST_REQUEST:
            return LeastRequestLoadBalancer()
        else:
            raise Exception("Unknown load balancer type")