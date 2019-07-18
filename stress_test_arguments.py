import argparse


def parse_arguments():
    formatter = lambda prog: argparse.HelpFormatter(prog, width=100)
    parser = argparse.ArgumentParser(description="HBase Meta Table stress tester tool. You can specify different "
                                                 "workloads. If you don't specify any, then 'workload_1' will be used. "
                                                 "If you specify multiple, then all of them will run parallel.",
                                     formatter_class=formatter)
    parser.add_argument('--connection',
                        dest='connection_url',
                        action="store",
                        help="connection url (default: localhost)",
                        default="localhost")

    parser.add_argument('--workload_1',
                        dest='workload_1',
                        action="store_true",
                        help="create table + delay + delete table")

    parser.add_argument('--workload_2',
                        dest='workload_2',
                        action="store_true",
                        help="create table + write 4 records + delay + read one record using new connection "
                             "+ delete table")

    parser.add_argument('--number_of_threads',
                        dest='number_of_threads',
                        action="store",
                        help="number of threads for each of your workload (default: 40)",
                        default=40,
                        type=int)

    parser.add_argument('--number_of_tables',
                        dest='number_of_tables',
                        action="store",
                        help="number of tables operated by each thread (default: 100)",
                        default=100,
                        type=int)

    parser.add_argument('--delay_sec',
                        dest='delay_sec',
                        action="store",
                        help="sleep time to use during the operation of each table. It will be randomized a bit to "
                             "have more uniform load (default: 3)",
                        default=3,
                        type=int)

    parser.add_argument('--cleanup_and_exit',
                        dest='cleanup_and_exit',
                        action="store_true",
                        help="don't do any workload, just cleanup tables then exit")

    parser.add_argument('--cdh6',
                        dest='cdh6',
                        action="store_true",
                        help="use thrift connection settings compatible with the default CDH6 Hbase Thrift server: "
                             "'compact' protocol and 'framed' transport. (default: CDH5 compatible 'binary' protocol "
                             "and 'buffered' transport)")

    return parser.parse_args()


def get_workloads(params):
    workloads = []

    if params.workload_1:
        workloads.append('workload_1')
    if params.workload_2:
        workloads.append('workload_2')

    if len(workloads) == 0:
        workloads.append('workload_1')

    return workloads

