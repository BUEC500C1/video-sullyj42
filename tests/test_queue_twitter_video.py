from twittervideo import twitter_queue_video
from twittervideo.ffmpegencode import ffmpegconverter
from glob import glob
from twittertools.make_word_cloud import word_cloud_from_txt
from pickle import load
from os.path import join as fullfile, isfile
from pathlib import Path


def test_queue_twitter_video():
    try:
        ffhelper = ffmpegconverter()
        twitter_queue_video.makeoutputdir()
        outvid = twitter_queue_video.makequeue(
        username='potus',
        pages=10,
        tweetcount=10,
        testList=[],
        workphotos=True,
        noverlap=0)

        # wordcloud doesn't play nicely with multiprocessing
        # [word_cloud_from_txt(file) for file in glob('mpresults/*.txt')]
        # ffhelper.twitter_to_mpeg4(file_pattern='mpresults/twitter_*.png')
        success = True
    except Exception as e:
        print(e)
        success = False
    assert success, 'Failed to process a generic twitter timeline'
    assert isfile(outvid), 'Could not find the video output file'

if __name__ == '__main__':
    test_queue_twitter_video()
