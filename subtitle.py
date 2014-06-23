import os
import hashlib
import urllib2
import sys

def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def sub_downloader(path):

    hash = get_hash(path)
    replace = ['.avi', '.dat', '.mp4', '.mkv', '.vob',".mpg",".mpeg"]
    for content in replace:
        path = path.replace(content,"")
    if not os.path.exists(path+".srt"):
        headers = { 'User-Agent' : 'SubDB/1.0 (subtitle-downloader/1.0; http://google.com)' }
        url = "http://api.thesubdb.com/?action=download&hash="+hash+"&language=en"
        req = urllib2.Request(url, '', headers)
        try:
            response = urllib2.urlopen(req).read()
            with open (path+".srt","wb") as subtitle:
                subtitle.write(response)
        except urllib2.HTTPError, e:
            print('subtitle not found')

def processFile(currentDir):
    currentDir = os.path.abspath(currentDir)
    filesInCurDir = os.listdir(currentDir)
    for file in filesInCurDir:
        curFile = os.path.join(currentDir, file)
        if os.path.isfile(curFile):
            curFileExtension = curFile[-3:]
            if curFileExtension in ['avi', 'dat', 'mp4', 'mkv', 'vob',"mpg","mpeg"]:
                print('downloading the subtitle for %s' %curFile)
                sub_downloader(curFile)
                print('downloading completed')
        else:
            print('entering to directory %s'%curFile)
            processFile(curFile)

folder = sys.argv[1]
processFile(folder)