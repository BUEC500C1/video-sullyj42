'''
Simple script to test ffmpeg work on a series of images
'''
from twittervideo.ffmpegencode import ffmpegconverter
from glob import glob
import numpy as np
from os import remove


def setdiff_sorted(array1, array2, assume_unique=False):
    ans = np.setdiff1d(array1, array2, assume_unique).tolist()
    if assume_unique:
        return sorted(ans)
    return ans


def test_ffmpegconverter():
    ffclass = ffmpegconverter()
    fpattern = './test_images/*'
    oldfiles = glob(fpattern)
    # print(*oldfiles, sep='\n')
    if not oldfiles:
        raise FileNotFoundError
    try:
        ffclass.twitter_to_mpeg4(file_pattern=fpattern.replace('*', '*.png'))
        success = True
    except Exception as e:
        print(e)
        success = False
    assert success, 'Could not build the video from the test images'

    if not len(glob(fpattern.replace('*', '*.mp4'))) == 1:
        success = False
    assert success, 'Did not find the video file'
    allfiles = glob(fpattern)
    rmfiles = setdiff_sorted(allfiles, oldfiles)
    for file in rmfiles:
        # print(f'removing {file}')
        remove(file)
    # print(success)

if __name__ == '__main__':
    test_ffmpegconverter()