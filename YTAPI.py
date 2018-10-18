import os

import google.oauth2.credentials
import json
import requests

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from Download import downloadPlaylist

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = 'AIzaSyB6GHgfF9rAJL0htrtPNDmmwNPyED0BEqI'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def channels_list_by_username(service, **kwargs):
    results = service.channels().list(
        **kwargs
    ).execute()

    print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
          (results['items'][0]['id'],
           results['items'][0]['snippet']['title'],
           results['items'][0]['statistics']['viewCount']))


class YouTubeAPIException(Exception):
    """ Custom error exception for the YouTubeAPI class! """
    pass


def playlist(listId):
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)

    res = youtube.playlistItems().list(
        part="snippet",
        playlistId=listId,
        maxResults="50"
    ).execute()

    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
            part="snippet",
            playlistId=listId,
            maxResults="50",
            pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']
    return res


def fetchList(listId):
    list = []
    for item in playlist(listId)['items']:
        videoId = item['snippet']['resourceId']['videoId']
        list.append(videoId)
    return list

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # service = get_authenticated_service()
    # channels_list_by_username(service,
    # part='snippet,contentDetails,statistics',
    # forUsername='GoogleDevelopers')

    #print('Domace')
    #downloadPlaylist(fetchList('PLsYn1-IiEkQq_s8PYQpmft0DCSArS_rrX')) #domace
    #print('kurjak')
    #downloadPlaylist(fetchList('PL6A687A4A5EC21BD7')) #kurjak
    print('Demooo')
    downloadPlaylist(fetchList('PLsYn1-IiEkQq3KXUEhelgku5GbcRdvATI')) #demo
    print('Two steps')
    downloadPlaylist(fetchList('PLsYn1-IiEkQpARprqPVFazkZro02t1ru0')) #Two steps

