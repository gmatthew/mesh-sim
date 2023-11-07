from application.application import Application
from loadbalancer.loadbalancer_factory import LoadBalancerFactory
from loadbalancer.loadbalancer import LoadBalancerType
from logger import Logger

class Proxy(Logger): 
    def __init__(self, id, service_registry,  egress_lb_type: LoadBalancerType, service_dependencies = []):
        super().__init__()
        self.id = id
        self.application = None
        self.service_registry = service_registry
        self.service_dependencies = service_dependencies
        self.egress_lb_type = egress_lb_type
        self.load_balancers = {}
       
    # This will be used to lazy load the load balancers
    def configure_egress_load_balancers(self, lb_type):
         # There will be a load balancer for each egress service
        lb_factory = LoadBalancerFactory()

        for service_name in self.service_dependencies:
            service = self.service_registry.get_service(service_name)

            lb = lb_factory.create_load_balancer(lb_type)
            lb.attach_service(service)

            self.load_balancers[service_name] = lb

    def set_application(self, application: Application):
        self.application = application
        application.set_proxy(self)

    async def process_ingress(self, request):
        if self.application is None:
            raise Exception('Proxy has no application')
        
        # print(f'Proxy {self.id} processing ingress request')

        return await self.application.process(request)


    async def process_egress(self, request):
        # TODO: Implement - The proxy needs to know the set of egress services that are available for it to call
        # 1. Inspect the request headers to determine the egress service
        # 2. Get all the pods for the egress service
        # 3. Ask load balancer to select the pod to process the request
        # 4. Call the pod to process the request
        # 5. Return the response

        # Lazy load the load balancers
        if len(self.load_balancers) == 0:
            self.configure_egress_load_balancers(self.egress_lb_type)

        # Process the request
        lb = self.load_balancers[request.host]
        pod = lb.choose_pod()

        response = await pod.process(request)

        return response