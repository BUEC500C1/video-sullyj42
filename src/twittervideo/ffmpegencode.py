'''
Convert a directory of files, convert each file into a frame of second

Overlay text (metadata) onto the image before creation

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

from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
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

    def overlaytext(self, filename):
        ''' 
        This method takes a valid image file

        adds metadata contained within the filename to the image itself

        Expects metadata in the form of a date YYYYMMDD_YYYYMMDD

        This could be placed outside of the class
        '''
        if not isfile(filename):
            print(f'Could not find file: {filename}', file=stderr)
            raise FileNotFoundError()
        fileext = filename[len(filename)-3:len(filename)]
        if fileext != 'png':
            # Currently all files are png, this should easily extend to other formats though
            print(f'Invalid extension detected: {fileext}', file=stderr)
            raise FileNotFoundError()
        datepattern = '(?<=_)\\d{8}'
        dates = re.findall(datepattern, filename)
        if len(dates) != 2:
            print(f'Unable to parse. File {filename}. Pattern {datepattern}',
                  file=stderr)
            raise FileNotFoundError()

        datelist = [datetime.strptime(date, '%Y%m%d').strftime("%B %d, %Y")
                    for date in dates]
        datestr = datelist[1] + ' - ' + datelist[0] # Return old - new range
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("fonts/MarvelRegular-Dj83.ttf", 36)
        # draw.text((x, y),"Sample Text",(r,g,b))
        print(f'Adding datestr: {datestr}')
        draw.text((0, 0),datestr,(0,0,0),font=font)
        img.save(filename.replace('.png', '_mod.png'))
        img.show()


if __name__ == '__main__':
    '''
    This provides quick command line debugging for a specific set of images
    '''
    fdir = './test/images/'; 
    converter = ffmpegconverter(fdir)
    converter.imagedir_to_mp4()