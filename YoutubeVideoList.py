# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

DEVELOPER_KEY = 'your api developer key'
YOUTUBE_USER = 'youtube user name'

def main():

    api_service_name = "youtube"
    api_version = "v3"
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY )
     

    request = youtube.channels().list(
        part="contentDetails",
        forUsername=YOUTUBE_USER
    )
    response = request.execute()

    id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    pageToken = ""

    videos = []
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=id,
            pageToken=pageToken
        )
        response = request.execute()

        items = response['items']

        for item in items:
            video = (item['snippet']['title'], item['snippet']['resourceId']['videoId'])
            videos.append(video)

        if 'nextPageToken' not in response:
            break
        pageToken = response['nextPageToken']
        pageInfo = response['pageInfo']

    videos.reverse()
    with open('list.html', 'w', encoding='utf-8') as f:
        for video in videos:
            print(video[1], video[0])
            f.write('<a href="https://www.youtube.com/watch?v=%s">%s</a><br>\n' % (video[1], video[0]))

    with open('list.csv', 'w', encoding='utf-8') as f:
        for video in videos:
            f.write('%s,https://www.youtube.com/watch?v=%ss\n' % (video[0], video[1]))

if __name__ == "__main__":
    main()
