from  multiprocessing import Pool, Queue
from os import getpid
from time import sleep
from random import random

MAX_WORKERS=5

class Testing_mp(object):
    def __init__(self):
        """
        Initiates a queue, a pool and a temporary buffer, used only
        when the queue is full.
        """
        self.q = Queue(maxsize=20)
        self.pool = Pool(processes=MAX_WORKERS, initializer=self.worker_main,)
        self.temp_buffer = []

    def add_to_queue(self, msg):
        """
        If queue is full, put the message in a temporary buffer.
        If the queue is not full, adding the message to the queue.
        If the buffer is not empty and that the message queue is not full,
        putting back messages from the buffer to the queue.
        """
        N = 0;
        while self.q.full():
            # self.temp_buffer.append(msg)
            print('Queue is full. Pausing until items deque')
            sleep(1)
        self.q.put(msg)
        # if len(self.temp_buffer) > 0:
        #     add_to_queue(self.temp_buffer.pop())

    def write_to_queue(self):
        """
        This function writes some messages to the queue.
        """
        for i in range(50):
            self.add_to_queue("First item for loop %d" % i)
            # Not really needed, just to show that some elements can be added
            # to the queue whenever you want!
            sleep(random()*2)
            self.add_to_queue("Second item for loop %d" % i)
            # Not really needed, just to show that some elements can be added
            # to the queue whenever you want!
            sleep(random()*2)

    def worker_main(self):
        """
        Waits indefinitely for an item to be written in the queue.
        Finishes when the parent process terminates.
        """
        print(f'Process {getpid()} started')
        while True:
            # If queue is not empty, pop the next element and do the work.
            # If queue is empty, wait indefinitly until an element get in the queue.
            sleep(10+random())
            item = self.q.get(block=True, timeout=None)
            print(f'{getpid()} retrieved: {item}')
            # simulate some random length operations
            sleep(random())

# Warning from Python documentation:
# Functionality within this package requires that the __main__ module be
# importable by the children. This means that some examples, such as the
# multiprocessing.Pool examples will not work in the interactive interpreter.
if __name__ == '__main__':
    mp_class = Testing_mp()
    mp_class.write_to_queue()
    # Waits a bit for the child processes to do some work
    # because when the parent exits, childs are terminated.
    sleep(5)