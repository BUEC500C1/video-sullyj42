'''
Convert a directory of files, convert each file into a frame of second

Filename contains time of creation in format yyyymmddHHmm

Filename shall be a text file less than 140 characters or image (png, jpeg)
'''
from sys import stderr
from time import sleep
from os.path import isdir, join, dirname, isfile
from os import remove as rm
import ffmpeg
import pathlib
import glob;
import re
from os import system
class ffmpegconverter():
    '''
    Container to hold methods and data for converting a directory of files
    into image frames

    Made to operate sequentially on files, moving newest to oldest
    '''
    def __init__(self, filedir = ''):
        '''
        Allows function to be called with option
        '''
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
    def twitter_to_mpeg4(self, file_pattern='./output/*/*/twitter_*.png'):
        filenames = glob.glob(file_pattern)
        if not filenames:
            pattern = file_pattern.replace('./', pathlib.Path().absolute())
            print(f'Could not parse filenames properly -- using pattern (' + \
                  f'{pattern})')
        outfilename = re.sub('_iter\\d+', '_summary.mp4', dirname(filenames[1]))
        # print(outfilename)
        # sleep(5)
        if isfile(outfilename):
            rm(outfilename)
        (
            ffmpeg
            .input(file_pattern,
                pattern_type='glob',
                framerate= 1)
            .output(outfilename)
            .run()
            # .drawtext(fname)
        )
        # for file in filenames:
        #     fname = re.findall('(?<=twitter_)\\w+_\\d+_\\d+', file)

            # if file == filenames[0]:
            #     system(f'ffmpeg -i "video" -loop 1 -t 3 -i "{file}" -f lavfi -t 3 -i anullsrc -filter_complex "[0:v] [0:a] [1:v] [2:a] concat=n=2:v=1:a=1 [v] [a]" -c:v libx264 -c:a aac -strict -2 -map "[v]" -map "[a]" {outfilename}')
            # else:
            #     system(f'ffmpeg -i "video" -loop 1 -t 3 -i "{file}" -f lavfi -t 3 -i anullsrc -filter_complex "[0:v] [0:a] [1:v] [2:a] concat=n=2:v=1:a=1 [v] [a]" -c:v libx264 -c:a aac -strict -2 -map "[v]" -map "[a]" {outfilename}')
if __name__ == '__main__':
    '''
    This provides quick command line debugging for a specific set of images
    '''
    fdir = './test/images/'; 
    converter = ffmpegconverter(fdir)
    converter.imagedir_to_mp4()