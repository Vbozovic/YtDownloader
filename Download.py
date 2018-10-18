import requests
import urllib.request as rq
import pytube
from bs4 import BeautifulSoup

from Fix import download_video


def splitKbs(string):
    firstInt = ''
    for char in string:
        if char.isdigit():
            firstInt += char

    return firstInt


def compareAbr(first, second):
    # first je maxStream
    firstInt = splitKbs(first)
    secondInt = splitKbs(second)

    if int(firstInt) < int(secondInt):
        return True

    return False


# prvi stream sa rezolucijom
def findStreamRes(streamList):
    lista = []
    maxStream = streamList[0]
    for stream in streamList:
        if compareAbr(maxStream.abr, stream.abr):
            maxStream = stream
    return maxStream


def getStream(ytObj):
    result = findStreamRes(ytObj.streams.filter(only_audio=True).all())
    return result


def downloadVideo(url):
    try:
        yt = pytube.YouTube(url)
        maxStream = getStream(yt)
        # maxStream.download('C:\\Users\\Vuk\\Desktop\\PycharmProjects\\Youtube downloader\\music')
        download_video(url, maxStream.itag,
                       'C:\\Users\\Vuk\\Desktop\\PycharmProjects\\Youtube downloader\\music\\%s' % maxStream.default_filename)
    except Exception as e:
        print(e)




def downloadPlaylist(links):
    for url in links:
        downloadVideo('https://youtube.com/watch?v=%s' % url)
