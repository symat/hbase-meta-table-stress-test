# HBase meta table stress test

Test script for stress testing HBase meta table (like creating, splitting / moving / deleting tables). The main idea is 
not to generate huge load in general, but to execute frequent operations that will result in the changes of the meta 
table. The script is using [HappyBase](https://happybase.readthedocs.io/en/latest/), so it will use Thrift to connect to 
HBase.

Currently the following workloads are implemented:
- Creating a table --> delay ~X sec -->  disable & delete table
- Creating a table --> write a few records --> delay ~X sec --> read a record using a new connection --> disable & delete table

Other stress test workloads, not implemented yet:
- Creating a table --> write a few records --> split the region --> delay ~X sec --> disable & delete table
- Creating a table --> write a few records --> move the region --> disable & delete table
- Creating a table with multiple regions --> write a few records --> merge the regions --> disable & delete table

## Prerequisites

```bash

# it is always a good idea to use virtualenvs:
# https://docs.python-guide.org/dev/virtualenvs/

pip3 install -r requirements.txt
```


## Usage

printed by `python3 ./stress_test.py --help`

```
usage: stress_test.py [-h] [--connection CONNECTION_URL] [--workload_1] [--workload_2]
                      [--number_of_threads NUMBER_OF_THREADS] [--number_of_tables NUMBER_OF_TABLES]
                      [--delay_sec DELAY_SEC] [--cleanup_and_exit] [--cdh6]

HBase Meta Table stress tester tool. You can specify different workloads. If you don't specify any,
then 'workload_1' will be used. If you specify multiple, then all of them will run parallel.

optional arguments:
  -h, --help            show this help message and exit
  --connection CONNECTION_URL
                        connection url (default: localhost)
  --workload_1          create table + delay + delete table
  --workload_2          create table + write 4 records + delay + read one record using new
                        connection + delete table
  --number_of_threads NUMBER_OF_THREADS
                        number of threads for each of your workload (default: 40)
  --number_of_tables NUMBER_OF_TABLES
                        number of tables operated by each thread (default: 100)
  --delay_sec DELAY_SEC
                        sleep time to use during the operation of each table. It will be randomized
                        a bit to have more uniform load (default: 3)
  --cleanup_and_exit    don't do any workload, just cleanup tables then exit
  --cdh6                use thrift connection settings compatible with the default CDH6 Hbase Thrift
                        server: 'compact' protocol and 'framed' transport. (default: CDH5 compatible
                        'binary' protocol and 'buffered' transport)


```