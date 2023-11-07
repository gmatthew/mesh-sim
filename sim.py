from simhttp.request import Request
from cluster import Cluster
from loadgen.workload_generator import WorkloadGenerator

import asyncio

if __name__ == "__main__":
    cluster = Cluster()
    workload_generator = WorkloadGenerator(cluster=cluster, connections=128, rps=1500, duration=30)
   
    asyncio.run(workload_generator.do_work())