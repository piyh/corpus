import time
startTime = time.time()
import logging
import youtube_dl
from youtube_dl.utils import DateRange
import os, sys
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import json
from pprint import pformat as pf
logger = logging.getLogger()

def getLogger(logDir = None):
    filename = 'youtube-dl_daemon.log'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')#- %(name)s 
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    if logDir:
        if Path(logDir).exists and Path(logDir).is_dir():
            filename = logDir.joinpath(filename)
            fh = logging.FileHandler(filename)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        else:
            logger.error('got logDir parameter')
            raise exception
 
    return logger

def getArgs():
    '''
    originally written to be called from command line, splitting argparse out into a function
    allows this file to be imported as a module or called from the command line with same kwargs
    '''
    parser = argparse.ArgumentParser(description =  'Pull reports from Dayforce and export to Excel or CSV format')
    parser.add_argument('-l', '--logdir', help = "folder to write log file") 
    parser.add_argument('-x', action="store_true", help = "Boolean Y/N example param")
    #parser.add_argument( '--lookback-days', help = "time to sleep between youtube polls, defaults to 10 minutes")
    parser.add_argument('-s', '--sleep-interval', default = 10*60, help = "time to sleep between youtube polls, defaults to 10 minutes")
    parser.add_argument('-j', '--json-config', default = 'conf.json', help = 'json config file that will get added to ytdl opts')
    args = parser.parse_args()
    #vars to return the dict of the object, make it usable as a **kwargs param and don't have to uses args.parameter
    return vars(args)

def my_hook(d):
    if d['status'] == 'finished':
        print('download finished')

def main(**kwargs):
    global logger
    if kwargs.get('logDir'):
        logDir(kwargs.get('logDir'))
    else:
        logDir = Path()
             
    logger = getLogger(logDir)
    #convenience alias function
    log = logger.debug
    startDuration = (time.time() - startTime)

    log(f'yotube-dl_daemon time to start was {startDuration:.2f}s')
    jsonConfig = kwargs.get('json_config') 
    if jsonConfig:
        jsonConfig = Path(jsonConfig)
        if jsonConfig.is_file():
            try:
                with open(jsonConfig) as conf:
                    print('loading')
                    ytdlJsonParams = json.load(conf)
            except:
                logger.exception("couldn't parse f{json_config=}")
                pass
        else:
            log(f'{jsonConfig=} is not file')
            ytdlJsonParams = {}
    today    = datetime.now()
    if 'lookback_days' in kwargs:
        lookback = today - timedelta(days = kwargs.get('lookback_days'))
        dtFormat = '%Y%m%d'
        dateRange = DateRange(lookback.strftime(dtFormat), today.strftime(dtFormat))
    ytdl_opts = {
        #'playlistend': kwargs.get('maxDownloads',5),
        'download_archive':kwargs.get('downloadedIdList',"alreadyDownloaded.txt"),
        #'skip_download':kwargs.get('skip_download',False), #use for catching up on stuff like json files
        'ignoreerrors':kwargs.get('ignoreerrors',True),
        'logger': logger,
        #'progress_hooks': [my_hook],
        #'writethumbnail':kwargs.get('writethumbnail',False),
        #'writeinfojson':kwargs.get('writeinfojson',False),
        #'simulate': True,
        #'daterange': dateRange,
               
    }
    log(pf(ytdl_opts))
    log(pf(ytdlJsonParams))
    defaultParams.update(ytdlJsonParams).update(kwargs) #make this work
    ytdl_opts = {**ytdlJsonParams, **ytdl_opts}
    log(pf(ytdl_opts))
    """while True:
        ytdl = youtube_dl.YoutubeDL(ytdl_opts) 
        ytdl.download(['https://www.youtube.com/user/KingCobraJFS/'])
        log(f"sleeping {kwargs.get('sleep_interval')} seconds")
        time.sleep(kwargs.get('sleep_interval'))
    """

if __name__ == '__main__':
    kwargs = getArgs()
    kwargs['json_config'] = 'conf.json'
    main(**kwargs)
    
    
        
    
    





"""Available options:
    verbose:           Print additional info to stdout.
    forceurl:          Force printing final URL.
    format:            Video format code. See options.py for more information.
    nooverwrites:      Prevent overwriting files.
    matchtitle:        Download only matching titles.
    writedescription:  Write the video description to a .description file
    writeinfojson:     Write the video description to a .info.json file
    writeannotations:  Write the video annotations to a .annotations.xml file
    writethumbnail:    Write the thumbnail image to a file
    write_all_thumbnails:  Write all thumbnail formats to files
    writesubtitles:    Write the video subtitles to a file
    writeautomaticsub: Write the automatically generated subtitles to a file
    allsubtitles:      Downloads all the subtitles of the video
                       (requires writesubtitles or writeautomaticsub)
    subtitlesformat:   The format code for subtitles
    subtitleslangs:    List of languages of the subtitles to download
    age_limit:         An integer representing the user's age in years.
                       Unsuitable videos for the given age are skipped.
    postprocessors:    A list of dictionaries, each with an entry
                       * key:  The name of the postprocessor. See
                               youtube_dl/postprocessor/__init__.py for a list.
                       as well as any further keyword arguments for the
                       postprocessor.
    progress_hooks:    A list of functions that get called on download
                       progress, with a dictionary with the entries
                       * status: One of "downloading", "error", or "finished".
                                 Check this first and ignore unknown values.
                       If status is one of "downloading", or "finished", the
                       following properties may also be present:
                       * filename: The final filename (always present)
                       * tmpfilename: The filename we're currently writing to
                       * downloaded_bytes: Bytes on disk
                       * total_bytes: Size of the whole file, None if unknown
                       * total_bytes_estimate: Guess of the eventual file size,
                                               None if unavailable.
                       * elapsed: The number of seconds since download started.
                       * eta: The estimated time in seconds, None if unknown
                       * speed: The download speed in bytes/second, None if
                                unknown
                       * fragment_index: The counter of the currently
                                         downloaded video fragment.
                       * fragment_count: The number of fragments (= individual
                                         files that will be merged)
                       Progress hooks are guaranteed to be called at least once
                       (with status "finished") if the download is successful.
    fixup:             Automatically correct known faults of the file.
                       One of:
                       - "never": do nothing
                       - "warn": only emit a warning
                       - "detect_or_warn": check whether we can do anything
                                           about it, warn otherwise (default)
    match_filter:      A function that gets called with the info_dict of
                       every video.
                       If it returns a message, the video is ignored.
                       If it returns None, the video is downloaded.
                       match_filter_func in utils.py is one example for this.
    external_downloader: Executable of the external downloader to call.
                       None or unset for standard (built-in) downloader.
    hls_prefer_native: Use the native HLS downloader instead of ffmpeg/avconv
                       if True, otherwise use ffmpeg/avconv if False, otherwise
                       use downloader suggested by extractor if None.
"""
