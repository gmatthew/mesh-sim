from application.web_application import WebApplication 
from pod import Pod
from service.service import Service
from service.registry import ServiceRegistry

import time

from loadbalancer.loadbalancer import LoadBalancerType
from loadbalancer.loadbalancer_factory import LoadBalancerFactory
from logger import Logger

class Cluster(Logger):
    def __init__(self):
        super().__init__()
        self.frontend_service = None
        self.cluster_load_balancer = None

        self.configure()
        self.inflight_requests = 0

    def configure(self):
        # @TODO(gerardm3): This should all be configured from reading a config file
        # Create registry
        registry = ServiceRegistry()

        # Create application and pods
        self.frontend_service = Service("frontend")
        
        frontend_pod_1 = Pod("fe-pod-1", WebApplication("fe-web-app-1", ['rate', 'reservation']), registry, LoadBalancerType.RANDOM)
        self.frontend_service.attach_pod(frontend_pod_1)
        frontend_pod_2 = Pod("fe-pod-2", WebApplication("fe-web-app-2", ['rate', 'reservation']), registry, LoadBalancerType.RANDOM)
        self.frontend_service.attach_pod(frontend_pod_2)
        frontend_pod_3 = Pod("fe-pod-3", WebApplication("fe-web-app-3", ['rate', 'reservation']), registry, LoadBalancerType.RANDOM)
        self.frontend_service.attach_pod(frontend_pod_3)

        rate_service = Service("rate")
        rate_pod_1 = Pod("rate-pod-1", WebApplication("rate-web-app-1"), registry, LoadBalancerType.RANDOM)
        rate_service.attach_pod(rate_pod_1)
        rate_pod_2 = Pod("rate-pod-2", WebApplication("rate-web-app-2"), registry, LoadBalancerType.RANDOM)
        rate_service.attach_pod(rate_pod_2)
        rate_pod_3 = Pod("rate-pod-3", WebApplication("rate-web-app-3"), registry, LoadBalancerType.RANDOM)
        rate_service.attach_pod(rate_pod_3)

        reservation_service = Service("reservation")
        reservation_pod_1 = Pod("reservation-pod-1", WebApplication("reservation-web-app-1"), registry, LoadBalancerType.RANDOM)
        reservation_service.attach_pod(reservation_pod_1)
        reservation_pod_2 = Pod("reservation-pod-2", WebApplication("reservation-web-app-2"), registry, LoadBalancerType.RANDOM)
        reservation_service.attach_pod(reservation_pod_2)
        reservation_pod_3 = Pod("reservation-pod-3", WebApplication("reservation-web-app-3"), registry, LoadBalancerType.RANDOM)
        reservation_service.attach_pod(reservation_pod_3)
        
        # Register services with registry
        registry.register(self.frontend_service)
        registry.register(rate_service)
        registry.register(reservation_service)

        # Configure load balancers
        self.cluster_load_balancer = LoadBalancerFactory().create_load_balancer(LoadBalancerType.LEAST_REQUEST)
        self.cluster_load_balancer.attach_service(self.frontend_service)

    async def process(self, request):
        if self.frontend_service is None:
            raise Exception('Simulator has no frontend service')
        
        # print current time 
        now = time.monotonic()

        # stats
        self.inflight_requests += 1

        # Load balance - Randomly select a pod
        if self.cluster_load_balancer is None:
            raise Exception('Simulator has no cluster load balancer')
        
        selected_pod = self.cluster_load_balancer.choose_pod()
        self.log.debug(f'FES selected pod: {selected_pod.id}')

        response = await selected_pod.process(request)
        
        # stats
        self.inflight_requests -= 1
        latency = time.monotonic() - now

        # convert latency to milliseconds
        latency = round(latency * 1000)
       
        self.log.debug(f'FES response: {latency}')
        response.set_latency(latency)

        return response