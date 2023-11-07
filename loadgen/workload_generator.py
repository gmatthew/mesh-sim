from simhttp.request import Request

import numpy as np
import asyncio
import random
import time

class WorkloadGenerator:
    def __init__(self, cluster, connections, rps, duration):
        self.connections = connections
        self.cluster = cluster
        self.rps = rps
        self.duration = duration
        self.results = []
        self.latencies = []
        self.time_elapsed = 0

    async def do_connection_work(self, connection_id, request, rps):
        delays = []
        # send the request to the cluster
        while (self.time_elapsed < self.duration):
            response = await self.cluster.process(request)
            self.results.append(response)
            self.latencies.append(response.latency)

            # add delay interval between requests
            delay_between_requests = self.get_delay_between_requests(rps)
            await asyncio.sleep(delay_between_requests)

            # update the time elapsed
            self.time_elapsed = time.time() - self.start_time

    async def do_work(self):
        # send work to the cluster at the specified rps for the specified duration
        # create a request
        request = Request(host="frontend", path="/hotels/1234", body="{'name': 'Hilton', 'price': 100}")

        # send the request to the cluster
        rps_per_connection = self.rps // self.connections

        print(f'connections: {self.connections} rps: {self.rps} rps_per_connection: {rps_per_connection}')

        # start the timer
        self.start_time = time.time()
       

        # run load for the full duration
        tasks = [self.do_connection_work(i, request, rps_per_connection) for i in range(self.connections)]
        await asyncio.wait(tasks, timeout=(self.duration))

        end_time = time.time()

        request_count = len(self.results)
        duration = end_time - self.start_time
        requests_per_second = request_count / duration

        print(f'request_count: {request_count} duration: {duration} rps: {requests_per_second}')

        self.generate_report(self.latencies)

    def get_delay_between_requests(self, rps):
        # random.expovariate(rps)
        return 1 / rps


    def generate_report(self, latencies):
        # Calculate latency statistics
        np_latencies = np.array(latencies)
        
        histogram = np.histogram(np_latencies)
        # print percentiles from 0 to 100 in increments of 10
        print('Latency Distribution')
        print('-------------------')
        
        for i in [50, 75, 90, 99, 99.9, 99.99, 99.999, 100]:
            percentile = np.percentile(np_latencies, i)
            print(f'percentile: {i} latency: {percentile}')

        print('-------------------')