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

    async def do_connection_work(self, connection_id, request, rps):
        delays = []
        # send the request to the cluster
        for i in range(rps):
  
            # delay for exponential distribution
            delay = random.expovariate(rps)
            delays.append(delay)

            # delay for the specified amount of time
            await asyncio.sleep(delay)

            response = await self.cluster.process(request)
            self.results.append(response)
            self.latencies.append(response.latency)

        # print(f'conn_id: {connection_id} delay sum: {sum(delays)}')

    async def do_work(self):
        # send work to the cluster at the specified rps for the specified duration
        # create a request
        request = Request(host="frontend", path="/hotels/1234", body="{'name': 'Hilton', 'price': 100}")

        # send the request to the cluster
        rps_per_connection = self.rps // self.connections

        print(f'connections: {self.connections} rps: {self.rps} rps_per_connection: {rps_per_connection}')

        start_time = time.time()

        tasks = [self.do_connection_work(i, request, rps_per_connection) for i in range(self.connections)]
        await asyncio.gather(*tasks)

        end_time = time.time()

        request_count = len(self.results)
        duration = end_time - start_time
        requests_per_second = request_count / duration

        print(f'request_count: {request_count} duration: {duration} rps: {requests_per_second}')

        # Calculate latency statistics
        latencies = np.array(self.latencies)
        histogram = np.histogram(latencies)
        # print percentiles from 0 to 100 in increments of 10
        for i in range(0, 101, 10):
            percentile = np.percentile(latencies, i)
            print(f'percentile: {i} latency: {percentile}')

        p50 = np.percentile(latencies, 50)
        p90 = np.percentile(latencies, 90)
        p99 = np.percentile(latencies, 99)

        print(f'p50: {p50} p90: {p90} p99: {p99}')

