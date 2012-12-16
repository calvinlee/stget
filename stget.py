#!/usr/bin/env python
# Calvin.Lee<lihao921@gmail.com> @ Mon Dec 17 01:21:18 CST 2012
# Small script helps downloading tracks from songtaste.com

import eyed3
import os
import re
from sets import Set
import urllib2

MUSIC_ROOT = os.path.expanduser("~/Music/songtaste")
# FIXME
MUSIC_HTML_SOUCE = os.path.expanduser("~/Desktop/playmusic.php")

def main():
    if not os.path.exists(MUSIC_ROOT):
        os.makedirs(MUSIC_ROOT)
    #file = codecs.open('/home/calvin/Desktop/playmusic.php', 'r', 'utf-8')
    #p = re.compile(r"(?<=WrtSongLine.*)http://[\da-z/.]*mp3")
    # FIXME
    p = re.compile(r"http://[\da-z/.]*\.mp3")
    songuri = []
    file = open(MUSIC_HTML_SOUCE)
    for line in file:
        m = p.search(line)
        if m:
            songuri.append(m.group())

    # FIXME
    uriSet = Set(songuri)
    for url in uriSet:
        localFile = os.path.join(MUSIC_ROOT, os.path.basename(url))
        try:
            download(url, localFile)
            smartRename(localFile)
        except Exception, e:
            print "Error downloading from %s" % url
            # Look at me: if 403 returned by server, regenerate the MUSIC_HTML_SOUCE and try again
            print e
            # os.unlink(localFile)

def download(remote, local):
    print "downloading from %s..." % remote
    """
    GET /201212162147/5a928a315369cd293aa2dae5d6c182b4/d/dd/dd3db4d5f4f9600e5fef065377976cbc.mp3 HTTP/1.1
    Host: md.songtaste.com
    Connection: keep-alive
    User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4
    Accept: */*
    Referer: http://songtaste.com/song/3017342/
    Accept-Encoding: gzip,deflate,sdch
    Accept-Language: zh-CN,zh;q=0.8
    Accept-Charset: UTF-8,*;q=0.5
    Cookie: __utma=148846773.1768489944.1355665648.1355665648.1355665648.1; __utmb=148846773.2.10.1355665648; __utmc=148846773; __utmz=148846773.1355665648.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); pgv_pvi=2716645376; pgv_si=s244701184; valid=1
    
    HTTP/1.0 200 OK
    Expires: Fri, 11 Jan 2013 08:59:47 GMT
    Date: Wed, 12 Dec 2012 08:59:47 GMT
    Server: nginx/0.8.36
    Content-Type: audio/mpeg
    Content-Length: 15051723
    Last-Modified: Wed, 28 Mar 2012 14:47:32 GMT
    Cache-Control: max-age=2592000
    srvtag: CAIYUN-SR024
    Accept-Ranges: bytes
    Age: 362893
    Via: 1.0 wzpy186:80 (Cdn Cache Server V2.0), 1.0 jsyc76:8101 (Cdn Cache Server V2.0)
    Connection: keep-alive
    """
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
        'Referer':'http://songtaste.com/'
    }

    request = urllib2.Request(url = remote, headers = headers)
    response = urllib2.urlopen(request).read()
    with open(local, "wb") as musicData:
        musicData.write(response)
    #urllib.urlretrieve(url, local)

def smartRename(filePath):
    # http://www.blog.pythonlibrary.org/2010/04/22/parsing-id3-tags-from-mp3s-using-python/
    audioFile = eyed3.load(filePath)
    filename, extension = os.path.splitext(filePath)
    if audioFile.tag:
        if audioFile.tag.title:
            filename = audioFile.tag.title
        if audioFile.tag.artist:
            # I want music file named like artist-title
            # filename = '%s-%s' % (filename, audioFile.tag.artist)
            # http://greaterdebater.com/blog/gabe/post/7
            # http://code.activestate.com/recipes/578333-python-string-concatenation/
            filename = ''.join([filename, "-",  audioFile.tag.artist])
        elif audioFile.tag.album:
            # fallback
            # filename = audioFile.tag.album
            pass

    newname = "".join((filename, extension))
    newfilepath = os.path.join(os.path.dirname(os.path.abspath(filePath)), newname)
    os.rename(filePath, newfilepath)

def test():
    url = "http://md.songtaste.com/201212162205/1b09794e98c77096cfd78a6c02fd84c5/d/d5/d5f8c5b40045c6908b7aa85a2086bb32.mp3"
    download(url, "test.mp3")

if __name__ == "__main__":
    main()
    #test()

