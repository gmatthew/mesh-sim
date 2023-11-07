from simhttp.request import Request
from cluster import Cluster
from loadgen.workload_generator import WorkloadGenerator
from loadgen.workload_generator import DistributionType

import asyncio
import argparse

if __name__ == "__main__":
    # @TODO(gerardm3): Add ability to configure the cluster by passing cluster configuration file
    cluster = Cluster()

    # parse the command line arguments
    parser = argparse.ArgumentParser(description='Simulation of a service mesh.')
    parser.add_argument('--connections', type=int, default=300, help='The number of connections to simulate.')
    parser.add_argument('--rps', type=int, default=300, help='The number of requests per second to simulate.')
    parser.add_argument('--duration', type=int, default=10, help='The duration of the simulation in seconds.')
    parser.add_argument('--distribution', type=str, default="exp", help='The distribution of the simulation.')
    args = parser.parse_args()

    # get the distribution type
    distribution_type = DistributionType.EXPONENTIAL
    if args.distribution == "fixed":
        distribution_type = DistributionType.FIXED

    # create the workload generator
    workload_generator = WorkloadGenerator(cluster=cluster, connections=args.connections, rps=args.rps, duration=args.duration, distribution=distribution_type)
   
    # run the workload generator
    asyncio.run(workload_generator.do_work())