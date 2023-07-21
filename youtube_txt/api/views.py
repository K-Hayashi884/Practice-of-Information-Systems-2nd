from rest_framework.decorators import api_view
from rest_framework.response import Response
from .youtube_index.youtube_transcript import seconds_to_hh_mm_ss, videoid_to_floated_index
from .serializers import IndexSerializer, VideoSerializer, getHeadlineSerializer
from .serializers import HeadlineSerializer
from .serializers import LaterListSerializer
from .models import Video
from .models import Headline
from .models import LaterList

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
import sys
sys.path.append('../')
from account.models import User
from .youtube_api import search

from apiclient.discovery import build
from django.conf import settings


@api_view(['GET'])
@permission_classes((AllowAny, ))
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/top/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of recommended videos'
        },
                {
            'Endpoint': '/top/',
            'method': 'GET',
            'body': {'search_query':""},
            'description': 'Returns a list of search results'
        },
        {
            'Endpoint': '/index/video_id',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of headlines'
        },
        {
            'Endpoint': '/list/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a laterlist'
        },
        {
            'Endpoint': '/list/',
            'method': 'DELETE',
            'body': {'video_id': ""},
            'description': 'Delete videos from laterlist'
        },
        {
            'Endpoint': '/api/v1/register/',
            'method': 'POST',
            'body': {'username': "",'email':"",'password':""},
            'description': 'Create users'
        },
        {
            'Endpoint': '/api-token-auth/',
            'method': 'POST',
            'body': {'username': "",'password':""},
            'description': 'Returns the token of the specified user'
        },

    ]
    return Response(routes)


@api_view(['GET'])
def getVideos(request):
    search_query = request.GET.get('search_query', '')
    print(search_query)
    if search_query is None:
        videos = Video.objects.all()[:10]
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    else:
        video_list = search(search_query)
        print(video_list)
        videos = []
        for video in video_list:
            try:
                tmp = Video.objects.get(video_id=video['video_id'])
                print(tmp)
                videos.append(tmp)
            except Video.DoesNotExist:
                tmp = Video.objects.create(video_id=video['video_id'], video_thumbnail_url=video['video_thumbnail_url'], video_count=0, video_title=video['video_title'])
                videos.append(tmp)

            
        # videos = Video.objects.filter(video_title__contains=search_query)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getHeadlines(request, k):
    headlines = Headline.objects.filter(video_id=k).order_by('timestamp')
    
    if headlines.exists():
        # 目次データを整形
        indices_data = []
        for headline in headlines:
            index = {
                "timestamp": headline.timestamp,
                "headline": headline.headline
            }
            indices_data.append(index)

        # # serializerにセット
        # serializer = getHeadlineSerializer(
        #     {"video":
        #         {"video_id": k,
        #          "url": "vide url, now implementing",
        #          "title": "video_title(now inplementing ...)",
        #          "indices": [
        #             {"timestamp": seconds_to_hh_mm_ss(d["timestamp"]),
        #              "headline": d["headline"]} for d in indices_data
        #          ],
        #          "comments": [
        #              {"text": "this is optional. (now implementing ...)"}
        #             ]
        #          }
        #      }
        # )
        serializer = IndexSerializer([
                    {"timestamp": seconds_to_hh_mm_ss(d["timestamp"]),
                     "headline": d["headline"]} for d in indices_data
                 ], many=True)
        return Response(serializer.data)
    else:
        # headlineとtimestamp取得
        floated_indices = videoid_to_floated_index(video_id=k) 

        # option: 時刻リンクを含むコメントを追加

        # DBに上記の内容を保存
        for index in floated_indices["video"]["indices"]:
            new_headline = Headline(
                video_id=k,
                timestamp=index["timestamp"],
                headline=index["headline"],
            )
            new_headline.save()
        
        # Videoモデルにも情報を追加
        # YouTube Data APIのクライアントを作成
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

        # 動画の情報を取得します
        response = youtube.videos().list(
            part='snippet,statistics',
            id=k
        ).execute()

        # 必要な情報を抽出します
        video_data = response['items'][0]
        video_id = video_data['id']
        video_title = video_data['snippet']['title']
        video_thumbnail_url = video_data['snippet']['thumbnails']['default']['url']
        video_count = video_data['statistics']['viewCount']

        # ビデオオブジェクトを作成し、保存します
        Video.objects.create(
            video_id=video_id,
            video_title=video_title,
            video_thumbnail_url=video_thumbnail_url,
            video_count=video_count
        )

        # timestampをstringに直したバージョンを作成
        indices = floated_indices
        indices["video"]["indices"] = [
            {"timestamp": seconds_to_hh_mm_ss(d["timestamp"]),
             "headline": d["headline"]} for d in indices["video"]["indices"]
        ]
        # 返却用のserializer生成
        # new_serializer = getHeadlineSerializer(indices)
        new_serializer = IndexSerializer(indices["video"]["indices"], many=True)
        return Response(new_serializer.data)
    # headlines = Headline.objects.filter(video_id=k).order_by('timestamp')
    # serializer = HeadlineSerializer(headlines, many=True)
    # return Response (serializer.data)

# LaterListのためのクラス
class LaterListAPI(APIView):

    def get(self, request):
        user_id = getUserId(request)
        laterlist = LaterList.objects.filter(user_id=user_id)
        video_id_list = []
        for later in laterlist:
            video_id_list.append(later.video_id)
        videos = Video.objects.filter(video_id__in=video_id_list)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user_id = getUserId(request)
        video_id = request.data.get('video_id')
        try:
            video_id = Video.objects.get(video_id=video_id)
            user_id = User.objects.get(id=user_id)
            later_list = LaterList.objects.filter(user_id=user_id, video_id=video_id)
            if later_list.exists():
                return Response("Video is already in the later list.", status=status.HTTP_400_BAD_REQUEST)

            later = LaterList.objects.create(user_id=user_id, video_id=video_id)

            serializer = LaterListSerializer(later)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            return Response("Video not found", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        user_id = getUserId(request)
        video_id = request.data.get('video_id')
        try:
            video_id = Video.objects.get(video_id=video_id)
            user_id = User.objects.get(id=user_id)
            later_list = LaterList.objects.filter(user_id=user_id, video_id=video_id)
            if not later_list.exists():
                return Response("Video is not in the later list.", status=status.HTTP_400_BAD_REQUEST)
            
            later_list.delete()

            return Response("Video deleted successfully", status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            return Response("Video not found", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# request内のtokenを受け取ってuser_idを返す
def getUserId(request):
    token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
    user = Token.objects.get(key=token).user
    return user.pk
