# Python program to 
# demonstrate implementation of 
# queue using queue module 
  
  
from twittertools.tweet_import import tweet_import
from twittertools.make_word_cloud import word_cloud_from_txt
from copy import deepcopy
from os.path import isfile
from sys import stderr
from ffmpegencode import ffmpegconverter
import re
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
        self.q = Queue(maxsize=5)
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
            if N == 1:
                print('Queue is full. Pausing until items deque')
            N += 1
            if N > 1*60*3:  # Timeout after a few minutes
                print('--Items did not deque after a few minutes...--')
            sleep(1)

        self.q.put(msg)
        # if len(self.temp_buffer) > 0:
        #     add_to_queue(self.temp_buffer.pop())

    def write_to_queue(self):
        """
        This function writes some messages to the queue.
        """
        tweetClass = tweet_import() # Connect to twitter
        pages = 10
        username = 'brabbott42'
        tweetobjs = []
        for i in range(pages):
            print(f'\nAnalyzing page {i+1} of {(pages)}\n')
            tweetClass.analyzeUsername(username, tweetcount=10)
            newobj = deepcopy(tweetClass)
            print(f'Adding page {i} to the queue')
            self.add_to_queue(newobj)


    def worker_main(self):
        """
        Waits indefinitely for an item to be written in the queue.
        Finishes when the parent process terminates.
        """
        print(f'Process {getpid()} started')
        # while True:
        # If queue is not empty, pop the next element and do the work.
        # If queue is empty, wait indefinitly until an element get in the queue.
        item = self.q.get(block=True, timeout=None)
        item.classify_images()  # Makes requests to Google Vision
        outfile = item.write_summaryfile()  # Combines tweets, labels into summary
        if not isfile(outfile):
            print(f'\n\n--output file ({outfile}) not found--')  # , file=stderr)
        else:
            word_cloud_from_txt(outfile)  # 
        print(f'{getpid()} processed: {item}')

# Warning from Python documentation:
# Functionality within this package requires that the __main__ module be
# importable by the children. This means that some examples, such as the
# multiprocessing.Pool examples will not work in the interactive interpreter.
if __name__ == '__main__':
    mp_class = Testing_mp()
    mp_class.write_to_queue()
    # Waits a bit for the child processes to do some work
    # because when the parent exits, childs are terminated.