import uuid
from proxy import Proxy
from resource_manager import ResourceManager
from loadbalancer.loadbalancer import LoadBalancerType
from logger import Logger

import asyncio

class Pod(Logger):
    # Memory and Storage are in MB
    def __init__(self, id, application, service_registry, proxy_egress_lb_type: LoadBalancerType, memory = 512, cpu = 100, storage = 512):
        super().__init__()
        self.id = id
        self.inflight_requests = 0
        self.resource_manager = ResourceManager(cpu=cpu, memory=memory, storage=storage)

        self.setup_proxy(application, service_registry, proxy_egress_lb_type)

        self.pending_tasks = set()
       
    def setup_proxy(self, application, service_registry, proxy_egress_lb_type):
        id = f'{self.id}--{uuid.uuid4()}'

        self.proxy = Proxy(id, service_registry, proxy_egress_lb_type, application.get_dependencies())
        self.proxy.set_application(application)

    async def process_worker(self, request):
        self.inflight_requests += 1
        while True:
            if self.resource_manager.reserve_cpu(30):
                try:
                    response = await self.proxy.process_ingress(request)
                finally:
                    self.resource_manager.release_cpu(30)
                
                self.inflight_requests -= 1

                return response
            else:
                # print(f'Inflight requests: {self.inflight_requests} - {self.id}')
                await asyncio.sleep(0.01)

          
    async def process(self, request):
        task =  asyncio.create_task(self.process_worker(request))
        task.add_done_callback(self.pending_tasks.discard)


        await task
        
        return task.result()


    def get_inflight_requests(self):
        return len(self.pending_tasks)