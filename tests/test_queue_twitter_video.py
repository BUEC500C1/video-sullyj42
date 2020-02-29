from twittervideo import twitter_queue_video
from twittervideo.ffmpegencode import ffmpegconverter
from glob import glob
from twittertools.make_word_cloud import word_cloud_from_txt


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
    '''
    ffhelper = ffmpegconverter()
    makeoutputdir()
    makequeue(
              username='potus',
              pages=40,
              tweetcount=30,
              testList=[],
              workphotos=False,
              noverlap=0)

    # wordcloud doesn't play nicely with multiprocessing
    [word_cloud_from_txt(file) for file in glob('mpresults/*.txt')]
    ffhelper.twitter_to_mpeg4(file_pattern='mpresults/twitter_*.png')
    print('Conversion completed')
    '''
    assert True, 'Offline video testing not yet implimented'

if __name__ == '__main__':
    test_queue_twitter_video()
    test_queue_twitter_video_offline
