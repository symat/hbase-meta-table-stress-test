import argparse


def parse_arguments():
    formatter = lambda prog: argparse.HelpFormatter(prog, width=100)
    parser = argparse.ArgumentParser(description='HBase Meta Table stress tester tool', formatter_class=formatter)
    parser.add_argument('--connection',
                        dest='connection_url',
                        action="store",
                        help="connection url (default: localhost)",
                        default="localhost")

    parser.add_argument('--number_of_threads',
                        dest='number_of_threads',
                        action="store",
                        help="number of threads (default: 40)",
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
                        help="total sleep time to use during the operation of each table. It will be randomized a bit "
                             "to have more uniform load (default: 3)",
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

