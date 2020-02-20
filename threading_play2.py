import multiprocessing
import os
import time
from queue import Empty as qEmpty
the_queue = multiprocessing.Queue()


def worker_main(queue):
    print(f"os.getpid: {os.getpid()}. working")
    while True:
        item = queue.get(True)
        print(f"os.getpid: {os.getpid()}. got, {item}")
        time.sleep(1) # simulate a "long" operation

the_pool = multiprocessing.Pool(3, worker_main,(the_queue,))
#                            don't forget the coma here  ^

for i in range(5):
    the_queue.put("hello")
    the_queue.put("world")
its = []
while True:

    # If we go more than 30 seconds without something, die
    try:
        print("Waiting for item from queue for up to 5 seconds")
        i = the_queue.get(True, 5)
        print(f'found {i} from the queue !!')
        its.append(i)
    except qEmpty:
        print("Caught queue empty exception, done")
        break

time.sleep(2)