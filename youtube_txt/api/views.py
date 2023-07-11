from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoSerializer
from .serializers import getHeadlineSerializer
from .models import Video
from .models import Headline
from .models import LaterList
from .youtube_index.youtube_transcript import videoid_to_floated_index
from .youtube_index.youtube_transcript import seconds_to_hh_mm_ss
# ログイン関連
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/top/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of videos'
        },
        {
            'Endpoint': '/index/video_id',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of headlines'
        },
        {
            'Endpoint': '/list/customer_id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a laterlist'
        },



        
    ]
    return Response(routes)


@api_view(['POST'])
def sign_in(request):
    print("request", request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password)
    user = authenticate(username=username, password=password)

    if user is not None:
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getVideos(request):
    search_query = request.GET.get('search_query', '') 
    if search_query == None:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
    else:
        videos = Video.objects.filter(video_title__contains=search_query)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

        # serializerにセット
        serializer = getHeadlineSerializer(
            {"video":
                {"video_id": k,
                 "url": "vide url, now implementing",
                 "title": "video_title(now inplementing ...)",
                 "indices": [
                    {"timestamp": seconds_to_hh_mm_ss(d["timestamp"]),
                     "headline": d["headline"]} for d in indices_data
                 ],
                 "comments": [{"text": "this is optional. (now implementing ...)"}]}
             }
        )
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

        # timestampをstringに直したバージョンを作成
        indices = floated_indices
        indices["video"]["indices"] = [
            {"timestamp": seconds_to_hh_mm_ss(d["timestamp"]),
             "headline": d["headline"]} for d in indices["video"]["indices"]
        ]
        # 返却用のserializer生成
        new_serializer = getHeadlineSerializer(indices)
        return Response(new_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLaterlist(request,k):
    laterlist = LaterList.objects.filter(customer_id=k)
    video_id_list = []
    for later in laterlist:
        video_id_list.append(later.video_id)
    videos = Video.objects.filter(video_id__in=video_id_list)
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


# Create your views here.
