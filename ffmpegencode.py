'''
Convert a directory of files, convert each file into a frame of second

Filename contains time of creation in format yyyymmddHHmm

Filename shall be a text file less than 140 characters or image (png, jpeg)
'''

from time import sleep
from os.path import isdir
import ffmpeg
class ffmpegconverter():
    '''
    Container to hold methods and data for converting a directory of files
    into image frames

    Made to operate sequentially on files, moving newest to oldest
    '''
    def __init__(self, filedir = ''):
        if filedir == '':
            return None
        elif not isdir(filedir):
            raise FileNotFound
        else:
            self.imageDir = filedir
            self.outname  = filedir + 'out.mp4'

    def imagedir_to_mp4(self):
        (
            ffmpeg
            .input(self.imageDir + '*.jpg', 
                pattern_type='glob',
                framerate= 1)
            .output(self.outname)
            .overwrite_output()
            .run(capture_stdout=True)
        )
if __name__ == '__main__':
    '''
    This provides quick command line debugging for a specific set of images
    '''
    fdir = './test/images/'; 
    converter = ffmpegconverter(fdir)
    converter.imagedir_to_mp4()