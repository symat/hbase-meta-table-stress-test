# HBase meta table stress test

Test script for stress testing HBase meta table (like creating, splitting / moving / deleting tables)

Currently only the following workload is implemented:
- Creating a table + delay ~X sec + disable & delete table

Other stress test workloads, not implemented yet:
- Creating a table + write a few records + read the records using a new connection + disable & delete table
- Creating a table + write a few records + split the region + disable & delete table
- Creating a table + write a few records + move the region + disable & delete table
- Creating a table with multiple regions + write a few records + merge the regions + disable & delete table

## Prerequisites

```bash

# it is always a good idea to use virtualenvs:
# https://docs.python-guide.org/dev/virtualenvs/

pip3 install -r requirements.txt
```


## Usage

printed by `python3 ./stress_test.py --help`

```
usage: stress_test.py [-h] [--connection CONNECTION_URL] [--number_of_threads NUMBER_OF_THREADS]
                      [--number_of_tables NUMBER_OF_TABLES] [--delay_sec DELAY_SEC]
                      [--cleanup_and_exit] [--cdh6]

HBase Meta Table stress tester tool

optional arguments:
  -h, --help            show this help message and exit
  --connection CONNECTION_URL
                        connection url (default: localhost)
  --number_of_threads NUMBER_OF_THREADS
                        number of threads (default: 40)
  --number_of_tables NUMBER_OF_TABLES
                        number of tables operated by each thread (default: 100)
  --delay_sec DELAY_SEC
                        total sleep time to use during the operation of each table. It will be
                        randomized a bit to have more uniform load (default: 3)
  --cleanup_and_exit    don't do any workload, just cleanup tables then exit
  --cdh6                use thrift connection settings compatible with the default CDH6 Hbase Thrift
                        server: 'compact' protocol and 'framed' transport. (default: CDH5 compatible
                        'binary' protocol and 'buffered' transport)

```