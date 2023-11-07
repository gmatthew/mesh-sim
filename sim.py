from simhttp.request import Request
from cluster import Cluster
from loadgen.workload_generator import WorkloadGenerator
from loadgen.workload_generator import DistributionType

import asyncio

if __name__ == "__main__":
    cluster = Cluster()
    workload_generator = WorkloadGenerator(cluster=cluster, connections=300, rps=300, duration=10, distribution=DistributionType.EXPONENTIAL)
   
    asyncio.run(workload_generator.do_work())