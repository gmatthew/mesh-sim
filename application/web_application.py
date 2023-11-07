from .application import Application
from simhttp.response import Response
from simhttp.request import Request

import asyncio

class WebApplication(Application):
    def __init__(self, id, dependencies = []):
        super().__init__(id, dependencies)

    async def process(self, request) -> Response:
        # print(f'WebApp {self.id} processing request')
        
        await asyncio.sleep(0.01)

        # TODO: Implement the WebApp process method
        # 1. Print a message to the console that the WebApp is processing the request
        # 2. Call database get some data
        # 3. Do some memory or cpu intensive work
        # 4. Print a message to the console that the WebApp has finished processing the request
        # 5. Return the response
        await self.make_synchronous_dependency_calls()

        return Response({}, status=200, body=f'WebApp {self.id} Hello World!')
    
    # These calls are synchronous, but we are going to simulate them as asynchronous
    # so that we can see the effect of the async/await keywords
    async def make_synchronous_dependency_calls(self):
        for dependency in self.dependencies:
            dependency_request = Request({}, body=f'{dependency} body', host=dependency, path='/', method='GET')
            await self.proxy.process_egress(dependency_request)

    
    def do_cpu_intensive_work(self):
        pass

