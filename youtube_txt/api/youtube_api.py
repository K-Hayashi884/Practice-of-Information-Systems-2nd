import os
from apiclient.discovery import build
from django.conf import settings

def search(query):
    keyword = query
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    search_responses = youtube.search().list(
        q=keyword,
        part='snippet',
        type='video',
        regionCode="jp",
        maxResults=5,  # 5~50まで
    ).execute()

    video_list = []

    for search_response in search_responses['items']:
        
        video_id = search_response['id']['videoId']
        # snippet
        snippetInfo = search_response['snippet']
        # 動画タイトル
        title = snippetInfo['title']
        # チャンネル名
        # channeltitle = snippetInfo['channelTitle']

        thumbnail = snippetInfo['thumbnails']['default']['url']

        video_list.append({"video_id":video_id,"video_thumbnail_url":thumbnail,"video_title":title})

    return video_list