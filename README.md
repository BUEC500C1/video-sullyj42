This repository contains tools to summarize the text and images in a users twitter feed. 

To use, first paste your `keys` file into `apiDesignSullyj42/src/twittertools/tokens.` Then export your google credentials to the appropriate environment variable, or also paste this file (`mygooglekeys.json`) into the aforementioned directory.

Then, install the requirements
```
>> pip install requirements.txt
```
The two local packages (twittertools and twittervideo) may have snuck into the requirements. If those throw warnings or errors, ignore.

Last, install the python modules. Both the submodule and this module
```
>> pip install ./apiDesignSullyj42
>> pip install .
```
The tests should explain simple API usage. 

# Web app

A simple web app is written in as a wrapper to this program.

It can be instantiated by `python3 flask_twitter.py`

Then naviagte to the local-host, and provide valid inputs.

Note the workPhotos option will drastically increase the time requirements, I recomment turning it off.

# Usage

There are two main files within the `src/twittervideo` directory. 

`ffmpegconverter` is an api to use ffmpeg for this toolset. It is used as a helper for the next module.

`queuetwittervideo` sets up a queue and a multiprocessing architecture, saves the image files to a new directory, and creates a video. Example API usage can be seen in the test code and __main__ interfaces. Note queue and thread sizes may be adjusted machine by machine.

A simple example can be run by just calling `python src/twittervideo/queue_twitter_video.py`.

# Queues and multiprocessing
The largest timesinks in this operation are (in order)
1. local calls to matplotlib to generate the wordcloud images (doesn't play nice with threading)
2. network calls to Google Vision API to parse the images
3. network calls to download the images
4. network calls to download the twitter text data
4.a Note these calls have to be performed sequentially as twitter IDs are not simple
4.b Also have some sketchy overlap settings that are not currently well tested

As such, the current implimentation is to call the twitter api for the desired amount of data, then form a queue with the necessary information for processing. 
This queue is filled with a multiprocessing information. The multiprocessing task is not locally limited. Errors have formed from socket connection. Currently limiting the number of workers to reduce this, but should also add in error handling to reduce the risk of fatal errors.

# video-sullyj42 -- Specifications
Main Exercise:  Using the twitter feed, construct a daily video summarizing a twitter handle day
Convert text into an image in a frame
Do a sequence of all texts and images in chronological order.
Display each video frame for 3 seconds


Tasks
Establish a processing criteria:
How many API calls you can handle simultaneously and why?
For example, run different API calls at the same time?
Split the processing of an API into multiple threads?
Recommendation for working on the homework:  
Step 1:
Develop a queue system that can exercise your requirements with stub functions.
Step 2: 
Develop the twitter functionality with an API
Step 3:
Integrate them
Include tracking interface to show how many processes are going on and success of each

