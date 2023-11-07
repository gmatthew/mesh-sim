from simhttp.request import Request

import numpy as np
import asyncio
import random
import time
from enum import Enum

class DistributionType(Enum):
    EXPONENTIAL = 1
    FIXED = 2

class WorkloadGenerator:
    def __init__(self, cluster, connections, rps, duration, distribution: DistributionType):
        self.connections = connections
        self.cluster = cluster
        self.rps = rps
        self.duration = duration
        self.results = []
        self.latencies = []
        self.time_elapsed = 0
        self.distribution = distribution

    async def do_connection_work(self, connection_id, request, rps):
        while (self.time_elapsed < self.duration):
            # add delay interval before each request to simulate rps
            delay_between_requests = self.get_delay_between_requests(rps)
            await asyncio.sleep(delay_between_requests)

            # send the request to the cluster
            response = await self.cluster.process(request)
            self.results.append(response)
            self.latencies.append(response.latency)

            # update the time elapsed
            self.time_elapsed = time.time() - self.start_time

    async def do_work(self):
        # send work to the cluster at the specified rps for the specified duration
        # create a request
        request = Request(host="frontend", path="/hotels/1234", body="{'name': 'Hilton', 'price': 100}")

        # send the request to the cluster
        rps_per_connection = self.rps // self.connections

        print('Workload Generator Configuration')
        print('-------------------------------')
        print(f'Connections: {self.connections} \r\nRequests Per Second: {self.rps} \r\nRequests Per Connection: {rps_per_connection}')
        print(f'Duration: {self.duration} \r\nDistribution: {self.distribution}')
        print('-------------------------------')

        # start the timer
        self.start_time = time.time()

        # run load for the full duration
        tasks = [self.do_connection_work(i, request, rps_per_connection) for i in range(self.connections)]
        await asyncio.wait(tasks, timeout=(self.duration))

        end_time = time.time()

        request_count = len(self.results)
        duration = end_time - self.start_time
        requests_per_second = request_count / duration

        print('') # newline
        print('Workload Generator Results')
        print('--------------------------')
        print(f'Request Count: {request_count} \r\nActual Requests Per Second: {requests_per_second}')
        print('--------------------------')

        self.generate_report(self.latencies)

    def get_delay_between_requests(self, rps):
        if self.distribution == DistributionType.EXPONENTIAL:
            return random.expovariate(rps)
        elif self.distribution == DistributionType.FIXED:
            return 1 / rps
        else:
            raise Exception(f'Unknown distribution type: {self.distribution}') 

    def generate_report(self, latencies):
        # Calculate latency statistics
        np_latencies = np.array(latencies)
        
        histogram = np.histogram(np_latencies)
        # print percentiles from 0 to 100 in increments of 10
        print('') # newline
        print('Latency Distribution')
        print('-------------------')
        
        for i in [50, 75, 90, 99, 99.9, 99.99, 99.999, 100]:
            percentile = np.percentile(np_latencies, i)
            print(f'{i}%\t {round(percentile,2)}')

        print('-------------------')