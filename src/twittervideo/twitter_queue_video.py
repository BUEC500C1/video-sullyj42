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
q = queue.Queue()

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


def makequeue(username='brabbott42',
              pages=10):
    # put items in queue
    twit_obj = tweet_import()
    for i in range(pages):
        print(f'Getting info for page {i+1}')
        twit_obj.analyzeUsername(username, 
                                tweetcount=20, noverlap=0, 
                                work_images=False)
        q.put(deepcopy(twit_obj))

    # how to wait for enqueued tasks to be completed
    # reference: https://docs.python.org/2/library/queue.html  
    for i in range(num_threads):
      t = threading.Thread(target=worker)
      t.daemon = True
      t.start()
      threads.append(t)
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
    for file in glob('mpresults/*.txt'):
        wrdcld = word_cloud_from_txt(file)  # Generates an image file
        imagefilename = wrdcld.out_file
        ffhelper.overlaytext(imagefilename)
