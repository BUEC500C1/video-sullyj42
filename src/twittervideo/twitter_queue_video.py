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
from twittervideo.ffmpegencode import ffmpegconverter
from glob import glob
from pathlib import Path
from ntpath import basename

num_threads = 1
threads = []

# build queue
q = queue.Queue(maxsize=20)

OUTPATH = Path(__file__)
OUTDIR = OUTPATH.parent

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
    # N=0
    N1 = 0
    while N1<5:  # Retry up to five times
        try:
            if item.work_images:
                print('doing photo work in multiprocessing')
                item.work_picture_data(item.urlData)
                item.classify_images()
            outfile = item.write_summaryfile()
            newfile = os.path.join(OUTDIR, 'mpresults')  #, basename(outfile))
            # sleep(0.5)
            # print(outfile)
            # print(newfile)
            shutil.copy(outfile, newfile)
            # sleep(0.5)
            # fname = basename(outfile)
            # newfilename = os.path.join(newfile, fname)
            # print(f'\nTrying to make a wordcloud from:{newfilename}\n')
            # sleep(5)
            # word_cloud_from_txt(newfilename)
            break
        except Exception as e:
            print('Error processing twitter data')
            print(e)
            print('sleeping for 5 seconds and retrying 5 times')
            sleep(5)
            N1+=1
    print("Current worker is finished.")
    q.task_done()


def makequeue(username='potus',
              pages=10,
              tweetcount=10,
              testList=[],
              workphotos=True,
              noverlap=0):
    ffhelper = ffmpegconverter()
    makeoutputdir()
    # put items in queue
    twit_obj = tweet_import()
    for i in range(num_threads):
      t = threading.Thread(target=worker)
      t.daemon = True
      t.start()
      threads.append(t)
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
            # q.put(deepcopy(twit_obj))
    else:
        for obj in testList:
            print('Putting object from the test list into the queue')
            newobj = deepcopy(obj)
            newobj.work_images = False # Do photo work in multiprocessing
            q.put(newobj)

    # how to wait for enqueued tasks to be completed
    # reference: https://docs.python.org/2/library/queue.html  

    # Blocks until all items in the queue have been gotten and processed.
    q.join() 
    # t.join()

    # put threads in queue
    for i in range(num_threads):
      q.put(None)
    # join thread in threads list
    for j in threads:
      t.join()
    textglob = os.path.join(OUTDIR, 'mpresults/*.txt')
    imageglob = os.path.join(OUTDIR, 'mpresults/twitter_*.png')
    [word_cloud_from_txt(file) for file in glob(fileglob)]
    outvid = ffhelper.twitter_to_mpeg4(file_pattern=imageglob)

    return outvid

def makeoutputdir():
    dir_name = os.path.join(OUTDIR, "mpresults")

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
    outvid = makequeue()

    # wordcloud doesn't play nicely with multiprocessing
    print(f'Conversion completed. Video saved at: {outvid}')
