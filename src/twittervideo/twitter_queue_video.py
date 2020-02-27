import multiprocessing
import time
from twittertools.tweet_import import tweet_import
from twittertools.make_word_cloud import word_cloud_from_txt
from copy import deepcopy
from os.path import isfile
from re import sub as resub
from ffmpegencode import ffmpegconverter
from time import sleep


class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        N = 0
        t = 1
        while N<5:
            try:
                next_task = self.task_queue.get()
                if next_task is None:
                    # Poison pill means shutdown
                    print(f'{proc_name}: Exiting')
                    self.task_queue.task_done()
                    return
                print(f'{proc_name}: {next_task}')
                answer = next_task()
                self.task_queue.task_done()
                self.result_queue.put(answer)
                return
            except  Exception as e:
                print('Could not preform task, sleeping and retrying')
                print(e)
                sleep(t)
                N += 1
        print('Could not perform task, exiting')
        self.task_queue.task_done()
        return


class Task(object):
    def __init__(self, twitobj):
        self.twitobj = twitobj
    def __call__(self):
        self.twitobj.work_picture_data(self.twitobj.urlData)
        self.twitobj.classify_images()
        outfile = self.twitobj.write_summaryfile() 
        word_cloud_from_txt(outfile)
        print('Successful')
        return f'Processed {self.twitobj.curFolder}'
    def __str__(self):
        return f'Processed {self.twitobj.curFolder}'


def startqueue(username='brabbott42',
               pages=10,
               ):
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue () # (max_size=5)
    
    # Start consumers
    num_consumers = 5  # multiprocessing.cpu_count() * 2
    print(f'Creating {num_consumers} consumers') 
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    tweetClass = tweet_import() # Connect to twitter
    # pages = 200 # This parameter may need rethinking after adding noverlap
    # tweetcount - noverlap --> number of unique tweets retrieved...
    # username = 'brabbott42'
    tweetobjs = []
    num_jobs = 1
    max_tweets = 3199  # Limited by twitter API
    for i in range(pages):
        print(f'\nAnalyzing page {i+1} of {(pages)}\n')
        if tweetClass.tweet_count < max_tweets:
            tweetClass.analyzeUsername(username=username,
                                       tweetcount=50,
                                       noverlap=0,
                                       work_images=False)
            newobj = deepcopy(tweetClass)
            # print(f'Adding page {i} to the queue')
            # self.add_to_queue(newobj)
            # for i in range(num_jobs):
            tasks.put(Task(newobj))
    
    # Add a poison pill for each consumer
    # print('adding "poison pill"')
    # for i in range(num_consumers):
    #     tasks.put(None)

    # Wait for all of the tasks to finish
    print('joining tasks')
    tasks.join()
    print('tasks joined')
    # Start printing results
    while num_jobs:
        result = results.get()
        print(f'Result: {result}')
        num_jobs -= 1

    ffconv = ffmpegconverter()
    newpattern = resub('iter\\d+', '*/twitter_*.png', tweetClass.curFolder)
    ffconv.twitter_to_mpeg4(file_pattern=newpattern)

if __name__ == '__main__':
    '''
    Provide quick command line debugging
    '''
    startqueue()
