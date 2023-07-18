import os
from apiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search(query):
    return YOUTUBE_API_KEY


# def search(query):
#     print(YOUTUBE_API_KEY)
#     keyword = query
#     youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
#     search_responses = youtube.search().list(
#         q=keyword,
#         part='snippet',
#         type='video',
#         regionCode="jp",
#         maxResults=5,# 5~50まで
#     ).execute()

#     video_list = []

#     for search_response in search_responses['items']:
        
#         video_id = search_response['id']['videoId']
#         # snippet
#         snippetInfo = search_response['snippet']
#         # 動画タイトル
#         title = snippetInfo['title']
#         # チャンネル名
#         channeltitle = snippetInfo['channelTitle']

#         thumnail = snippetInfo['thumbnails']['default']['url']

#         video_list.append({"video_id":video_id,"title":title,"channeltitle":channeltitle,"thumnail":thumnail})

#     return video_list