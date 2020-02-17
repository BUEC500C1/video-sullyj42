# Python program to 
# demonstrate implementation of 
# queue using queue module 
  
  
from queue import Queue 
import threading
from time import sleep
# Initializing a queue 

def do_work(item):
    print(f'working {item}')
    sleep(item)
    print(f'Worked {item}.')
    return item+1

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

q = Queue()
threads = []

maxque = 3
for i in range(maxque):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
source = [12, 4, 3, 1, 2]
for item in source:
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(maxque):
    q.put(None)
for t in threads:
    t.join()