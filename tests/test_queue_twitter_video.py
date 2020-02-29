from twittervideo import twitter_queue_video
from twittervideo.ffmpegencode import ffmpegconverter
from glob import glob
from twittertools.make_word_cloud import word_cloud_from_txt
from pickle import load
from os.path import join as fullfile
from pathlib import Path

def test_queue_twitter_video():
    try:
        ffhelper = ffmpegconverter()
        twitter_queue_video.makeoutputdir()
        twitter_queue_video.makequeue(
        username='potus',
        pages=30,
        tweetcount=10,
        testList=[],
        workphotos=True,
        noverlap=0)

        # wordcloud doesn't play nicely with multiprocessing
        [word_cloud_from_txt(file) for file in glob('mpresults/*.txt')]
        ffhelper.twitter_to_mpeg4(file_pattern='mpresults/twitter_*.png')
        success = True
    except Exception as e:
        print(e)
        success = False
    assert success, 'Failed to process a generic twitter timeline'

def test_queue_twitter_video_offline():
    # Save a list of twitter objects to supply as stub test input
    # Pickle!!
    try:
        ffhelper = ffmpegconverter()
        twitter_queue_video.makeoutputdir()
        fname = Path(__file__)
        homedir = Path(fullfile(fname.parent, '..')).resolve(strict=True)
        twitlist = load(open(fullfile(homedir, 'test_twitlist', 'twitlist.p'), 'rb'))
        twitter_queue_video.makequeue(
                  username='potus',
                  pages=40,
                  tweetcount=30,
                  testList=twitlist,
                  workphotos=False,
                  noverlap=0)

        # wordcloud doesn't play nicely with multiprocessing
        [word_cloud_from_txt(file) for file in glob('mpresults/*.txt')]
        ffhelper.twitter_to_mpeg4(file_pattern='mpresults/twitter_*.png')
        print('Conversion completed')
        success = True
    except Exception as e:
        print(e)
        success = False
    assert success, 'Offline video testing not yet implimented'

if __name__ == '__main__':
    # test_queue_twitter_video()
    test_queue_twitter_video_offline()
