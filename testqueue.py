# Python program to 
# demonstrate implementation of 
# queue using queue module 
  
  
from queue import Queue 
import threading
from time import sleep
from twittertools.tweet_import import tweet_import
from twittertools.make_word_cloud import word_cloud_from_txt

'''
Example of a queue...

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
'''
'''
    This provides a full interface to summarize a users twitter feed
    -- Currently looks at both text (tweets, retweets, replies) and images
    -- -- images are summarized by labels generated by Google Vision

    May be interesting to allow specific dates and so fourth eventually
'''
class queue_twitter_summary():
    '''
    Provides an interface to download twitter data
    '''
    def __init__(self):
        username = 'brabbott42'
        pages = 2

        tweetClass = tweet_import()
        # a.analyzeUsername('brabbott42', range(0, 1000, 200))
        for i in range(pages):
            tweetClass.analyzeUsername(username)
            # This updates the page number incrementally
            tweetClass.classify_images()
            word_cloud_from_txt(tweetClass.write_summaryfile())

if __name__ == '__main__':
    a = queue_twitter_summary()