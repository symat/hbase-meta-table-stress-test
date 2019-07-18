import happybase
import threading
import time
import sys
import stress_test_arguments
import random


TABLE_NAME_PREFIX = "stress_test"


class WorkerThread(threading.Thread):

    def __init__(self, params, thread_name, workflow_name):
        threading.Thread.__init__(self)
        self.params = params
        self.name = thread_name
        self.workflow_name = workflow_name

    def run(self):
        print("Starting {}, opening connection".format(self.name))
        connection = new_connection(self.params)

        for i in range(self.params.number_of_tables):
            table_name = "{}_{}_{}_{}".format(TABLE_NAME_PREFIX, self.workflow_name, self.name, i)
            print("processing table: " + table_name)
            connection.create_table(table_name, {'cf': dict()})

            if self.workflow_name == "workload_1":
                self.sleep_random()

            else:  # workload_2
                self.write(connection.table(table_name))
                self.sleep_random()
                connection.close()
                connection = new_connection(self.params)
                self.read(connection.table(table_name))

            connection.delete_table(table_name, disable=True)

        print("Closing connection... " + self.name)
        connection.close()
        print("Exiting " + self.name)

    def sleep_random(self):
        time.sleep(random.uniform(0.6 * self.params.delay_sec, 1.4 * self.params.delay_sec))

    @staticmethod
    def write(table):
        table.put(b'row-key-1', {b'cf:cf': b'value1'})
        table.put(b'row-key-2', {b'cf:cf': b'value2'})
        table.put(b'row-key-3', {b'cf:cf': b'value3'})
        table.put(b'row-key-4', {b'cf:cf': b'value4'})

    @staticmethod
    def read(table):
        table.row(b'row-key-4')


def new_connection(params):
    if params.cdh6:
        return happybase.Connection(params.connection_url, protocol="compact", transport="framed")
    else:
        return happybase.Connection(params.connection_url)


def clean_tables(params):
    print("cleaning tables...")
    connection = new_connection(params)
    for table_name in connection.tables():
        table_name = table_name.decode('ascii')
        if table_name.startswith(TABLE_NAME_PREFIX):
            print("removing: " + table_name)
            connection.delete_table(table_name, disable=True)
    connection.close()
    print("cleaning finished, connection closed...")


params = stress_test_arguments.parse_arguments()
clean_tables(params)
if params.cleanup_and_exit:
    sys.exit()


threads = []
for workload in stress_test_arguments.get_workloads(params):
    for i in range(params.number_of_threads):
        thread = WorkerThread(params, "thread-{}".format(i), workload)
        threads.append(thread)


print("starting workloads")
start = time.time()

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end = time.time()
workload_time = end - start

print("stress test finished!")
clean_tables(params)

print("params: {}".format(vars(params)))
print("theoretical minimum of total workload time: {}".format(params.number_of_tables * params.delay_sec))
print("actual total workload time: {} sec".format(workload_time))
print("actual total workload time: {}m {}s".format(int(workload_time/60), (workload_time % 60)))
