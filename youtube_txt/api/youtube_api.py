import os
import time
from apiclient.discovery import build
from django.conf import settings

def search(query):
    keyword = query
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    filtered_videos = []
    
    search_responses = youtube.search().list(
        q=keyword,
        part='snippet',
        type='video',
        regionCode="jp",
        maxResults=20,
    ).execute()

    for search_result in search_responses['items']:
        video_id = search_result['id']['videoId']
        video_response = youtube.videos().list(
            part='contentDetails',
            id=video_id
        ).execute()

        # 動画の再生時間をISO 8601形式から秒に変換
        duration_str = video_response['items'][0]['contentDetails']['duration']
        duration_str = duration_str[2:]  # "PT" を削除

        duration = 0
        if 'H' in duration_str:
            hours, rest = duration_str.split('H')
            duration += int(hours) * 3600
            if 'M' in rest:
                minutes, rest = rest.split('M')
                duration += int(minutes) * 60
            if 'S' in rest:
                seconds = rest.split('S')[0]
                duration += int(seconds)
        elif 'M' in duration_str:
            minutes, rest = duration_str.split('M')
            duration += int(minutes) * 60
            if 'S' in rest:
                seconds = rest.split('S')[0]
                duration += int(seconds)
        elif 'S' in duration_str:
            seconds = duration_str.split('S')[0]
            duration += int(seconds)

        if duration <= 1200:  # 20分 = 1200秒
            filtered_videos.append(search_result)
    
    video_list = []

    for search_response in filtered_videos:
        
        video_id = search_response['id']['videoId']
        # snippet
        snippetInfo = search_response['snippet']
        # 動画タイトル
        title = snippetInfo['title']
        # チャンネル名
        # channeltitle = snippetInfo['channelTitle']

        thumbnail = snippetInfo['thumbnails']['high']['url']

        video_list.append({"video_id":video_id,"video_thumbnail_url":thumbnail,"video_title":title})

    return video_list