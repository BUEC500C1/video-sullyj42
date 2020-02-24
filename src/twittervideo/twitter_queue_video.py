import multiprocessing
import time
from twittertools.tweet_import import tweet_import
from twittertools.make_word_cloud import word_cloud_from_txt
from copy import deepcopy
from os.path import isfile
from re import sub as resub
from ffmpegencode import ffmpegconverter

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print(f'{proc_name}: Exiting')
                self.task_queue.task_done()
                break
            print(f'{proc_name}: {next_task}')
            answer = next_task()
            self.task_queue.task_done()
            self.result_quseue.put(answer)
        return


class Task(object):
    def __init__(self, a):
        self.a = a
    def __call__(self):
        self.a.classify_images()
        outfile = self.a.write_summaryfile() 
        word_cloud_from_txt(outfile)
        return f'Processed {self.a.curFolder}'
    def __str__(self):
        return f'Processed {self.a.curFolder}'


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = 10  # multiprocessing.cpu_count() * 2
    print(f'Creating {num_consumers} consumers') 
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    tweetClass = tweet_import() # Connect to twitter
    pages = 200 # This parameter may need rethinking after adding noverlap
    # tweetcount - noverlap --> number of unique tweets retrieved...
    username = 'brabbott42'
    tweetobjs = []
    num_jobs = 5
    max_tweets = 3199  # Limited by twitter API
    for i in range(pages):
        print(f'\nAnalyzing page {i+1} of {(pages)}\n')
        if tweetClass.tweet_count < max_tweets:
            tweetClass.analyzeUsername(username, tweetcount=50, noverlap=40)
            newobj = deepcopy(tweetClass)
            # print(f'Adding page {i} to the queue')
            # self.add_to_queue(newobj)
            # for i in range(num_jobs):
            tasks.put(Task(newobj))
    
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get(timeout=60)
        print(f'Result: {result}')
        num_jobs -= 1

    ffconv = ffmpegconverter()
    newpattern = resub('iter\\d+', '*/twitter_*.png', tweetClass.curFolder)
    ffconv.twitter_to_mpeg4(file_pattern=newpattern)