'''
Convert a directory of files, convert each file into a frame of second

Overlay text (metadata) onto the image before creation

Filename contains time of creation in format yyyymmddHHmm

Filename shall be a text file less than 140 characters or image (png, jpeg)
'''
from sys import stderr, argv
from os.path import isdir, join as fullfile, dirname, isfile
from os import remove as rm
import ffmpeg
import pathlib
import glob
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from re import findall, sub


class ffmpegconverter():
    '''
    Container to hold methods and data for converting a directory of files
    into image frames

    Made to operate sequentially on files, moving newest to oldest
    '''
    def __init__(self, filedir='', file_pattern=''):
        '''
        Allows class to be called with various options
        '''
        if not isdir(filedir) and filedir != '':
            print(f'An invalid file directory was passed: {filedir}')
            raise FileNotFoundError()
        else:
            self.imageDir = filedir
            self.outname = filedir + 'out.mp4'
        if file_pattern == '':
            return None
        else:
            # This is where the interesting stuff happens
            self.twitter_to_mpeg4(file_pattern)

    def imagedir_to_mp4(self):
        '''
        This method is really not used anymore

        Prefer to use the filepattern method
        '''
        (
            ffmpeg
            .input(self.imageDir + '*.jpg',
                   pattern_type='glob',
                   framerate=1)
            .output(self.outname)
            .overwrite_output()
            .run(capture_stdout=True)
        )

    def twitter_to_mpeg4(self, file_pattern='./output/*/*/twitter_*.png'):
        filenames = glob.glob(file_pattern)
        if not filenames:
            print(f'Count not find files using: {file_pattern} from {__file__}',
                  file=stderr)
        else:
            print(*filenames, sep='\n')
        [self.overlaytext(file) for file in filenames]  # Add a date-overlay
        file_pattern = file_pattern.replace('.png', '_mod.png')
        # outfilename = sub('_iter\\d+', '_summary.mpeg', dirname(filenames[1]))
        outfilename = sub('_\\d{8}.*', '_summary.mp4', filenames[1])
        # print(outfilename)
        # sleep(5)
        if isfile(outfilename):
            rm(outfilename)
        (
            ffmpeg
            .input(file_pattern,
                   pattern_type='glob',
                   framerate=1/5)
            .output(outfilename)
            .run()
        )

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
            # Currently all files are png, this should easily extend
            print(f'Invalid extension detected: {fileext}', file=stderr)
            raise FileNotFoundError()
        base = Image.open(filename).convert('RGBA')

# make a blank image for the text, initialized to transparent text color
        datepattern = '(?<=_)\\d{8}'
        dates = findall(datepattern, filename)
        if len(dates) != 2:
            print(f'Unable to parse. File {filename}. Pattern {datepattern}',
                  file=stderr)
            raise FileNotFoundError()

        datelist = [datetime.strptime(date, '%Y%m%d').strftime("%B %d, %Y")
                    for date in dates]
        datestr = datelist[1] + ' - ' + datelist[0]  # Return old - new range
        txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
        # print(f'Image size: {base.size}')
        # get a font
        N = base.size[1]/24
        curpath = pathlib.Path(__file__)
        fontfile = fullfile(curpath.parent,
                            'fonts', 'OpenSans-ExtraBoldItalic.ttf')
        fnt = ImageFont.truetype(fontfile, int(N))  # get a drawing context
        d = ImageDraw.Draw(txt)
        transp = 0.8  # 0-1 image transparency

        d.text((base.size[0]/5, base.size[1]/4), datestr, font=fnt,
               fill=(255, 255, 255, int(transp*255)))
        # Plot white text against a challenging background
        out = Image.alpha_composite(base, txt)

        out.save(filename.replace('.png', '_mod.png'))


if __name__ == '__main__':
    '''
    This provides quick command line debugging for the various input options
    '''
    print(f'Detected {len(argv)} input arguments')
    if len(argv) == 1:
        # Just instantiate a class, do nothing else
        print('No input arguments detected. Instantiating class and returing')
        test = ffmpegconverter()
    elif len(argv) == 2:
        # I honestly completely forget what this is supposed to do
        print('Only provided filedirectory.')
        print('Setting some parameters, but no outputs')
        print('Useful for deprecated "imagedir_to_mp4" method')
        test = ffmpegconverter(filedir=argv[1])
    elif len(argv) == 3:
        print('Creating movie')
        test = ffmpegconverter(filedir=argv[1], file_pattern=argv[2])
    else:
        print(f'Invalid number of input arguments ({len(argv)})')
        raise Exception

    print('done')
