# !/usr/bin/env python3
'''
Provides a simple queued and multiprocessed interface to work on
'''

import queue
import time
import multiprocessing
import threading
from copy import deepcopy
from twittertools.tweet_import import tweet_import
from twittertools.make_word_cloud import word_cloud_from_txt
from time import sleep
import os
import tempfile
import shutil
from ntpath import basename
from ffmpegencode import ffmpegconverter
from glob import glob

num_threads = 4
threads = []

# build queue
q = queue.Queue(maxsize=10)

def worker():
  while True:
    item = q.get()

    N = 0
    Q = q.qsize()
    if item is None:
      print("Nothing in queue")
      N = 0
      break

    N += 1
    print(f'Currently process on {N} of  {Q} items')
    #do_work(item)
    # after get all images, then get videos
    # DO ACTUAL WORK HERE
    N=0
    while N<5:
        try:
            item.work_picture_data(item.urlData)
            item.classify_images()
            outfile = item.write_summaryfile()
            newfile = os.path.join('mpresults')  #, basename(outfile))
            print(outfile)
            print(newfile)
            shutil.copy(outfile, newfile)
            break
        except Exception as e:
            print('Error processing twitter data')
            print(e)
            print('sleeping for 5 seconds and retrying 5 times')
            sleep(5)
            N+=1
    print("Current worker is finished.")
    
    q.task_done()


def makequeue(username='potus',
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
              pages=500,
              tweetcount=50,
              testList=[],
              workphotos=False,
              noverlap=30):
=======
              pages=20,
              tweetcount=200
              tweetList=[]):
>>>>>>> 745434e97fe1b0480c9a99d8750f22d03d5491fd
=======
              pages=20,
              tweetcount=200):
>>>>>>> parent of c4ef3a9... Optional photo work, beginning to add tests
=======
              pages=20,
              tweetcount=200):
>>>>>>> parent of c4ef3a9... Optional photo work, beginning to add tests
    # put items in queue
    twit_obj = tweet_import()
    for i in range(num_threads):
      t = threading.Thread(target=worker)
      t.daemon = True
      t.start()
      threads.append(t)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    if not testList:
        for i in range(pages):
            print(f'Getting info for page {i+1} (photos: {workphotos})')
            try:
                twit_obj.analyzeUsername(username, 
                                        tweetcount, noverlap=noverlap, 
                                        work_images=False)  # Save image work for MP
            except IndexError:  # If we reach out of the tweet boundaries this can sometimes happen
                pass
            newobj = deepcopy(twit_obj)
            newobj.work_images = workphotos # Do photo work in multiprocessing
            q.put(newobj)
            q.put(deepcopy(twit_obj))
    else:
        for obj in testList:
            print('Putting object from the test list into the queue')
            newobj = deepcopy(obj)
            newobj.work_images = workphotos # Do photo work in multiprocessing
            q.put(newobj)
=======
    if tweetList:
      # This is useful for offline debugging
      # Put a list of twitter objects with no image data
      # Allows tests to be run entirely offline
      for tweet_obj in tweetlist:
        q.put(deepcopy(tweet_obj))
    else:
      for i in range(pages):
          print(f'Getting info for page {i+1}')
          twit_obj.analyzeUsername(username, 
                                  tweetcount, noverlap=0, 
                                  work_images=False)
          q.put(deepcopy(twit_obj))
>>>>>>> 745434e97fe1b0480c9a99d8750f22d03d5491fd
=======
=======
>>>>>>> parent of c4ef3a9... Optional photo work, beginning to add tests
    for i in range(pages):
        print(f'Getting info for page {i+1}')
        twit_obj.analyzeUsername(username, 
                                tweetcount, noverlap=0, 
                                work_images=False)
        q.put(deepcopy(twit_obj))
<<<<<<< HEAD
>>>>>>> parent of c4ef3a9... Optional photo work, beginning to add tests
=======
>>>>>>> parent of c4ef3a9... Optional photo work, beginning to add tests

    # how to wait for enqueued tasks to be completed
    # reference: https://docs.python.org/2/library/queue.html  

    # Blocks until all items in the queue have been gotten and processed.
    q.join() 


    # put threads in queue
    for i in range(num_threads):
      q.put(None)
    # join thread in threads list
    for j in threads:
      t.join()

def makeoutputdir():
    dir_name = "mpresults"

    if (os.path.exists(dir_name)):
        # `tempfile.mktemp` Returns an absolute pathname of a file that 
        # did not exist at the time the call is made. We pass
        # dir=os.path.dirname(dir_name) here to ensure we will move
        # to the same filesystem. Otherwise, shutil.copy2 will be used
        # internally and the problem remains.
        tmp = tempfile.mktemp(dir=os.path.dirname(dir_name))
        # Rename the dir.
        shutil.move(dir_name, tmp)
        # And delete it.
        shutil.rmtree(tmp)
    # At this point, even if tmp is still being deleted,
    # there is no name collision.
    os.makedirs(dir_name)

if __name__ == '__main__':
    ffhelper = ffmpegconverter()
    makeoutputdir()
    makequeue()

    # wordcloud doesn't play nicely with multiprocessing
    [word_cloud_from_txt(file) for file in glob('mpresults/*.txt')]
    ffhelper.twitter_to_mpeg4(file_pattern='mpresults/twitter_*.png')
    print('Conversion completed')
