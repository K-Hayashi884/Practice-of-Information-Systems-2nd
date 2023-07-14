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
import firebase_admin
from firebase_admin import auth, credentials
from django.contrib.auth.models import User

# Firebase Admin SDKの初期化
cred = credentials.Certificate("./api/txt-76a0f-firebase-adminsdk-h2wwc-f9c88f2f2a.json")
firebase_admin.initialize_app(cred)


# ログインしているかどうかを確認する関数
def verify_user(request):
    # ログインしていないユーザは弾く
    # POSTリクエストからFirebaseトークンを取得
    id_token = request.headers.get('Authorization')
    # id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE1MWJiNGJkMWQwYzYxNDc2ZWIxYjcwYzNhNDdjMzE2ZDVmODkzMmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHh0LTc2YTBmIiwiYXVkIjoidHh0LTc2YTBmIiwiYXV0aF90aW1lIjoxNjg5MzIyNzMwLCJ1c2VyX2lkIjoiVnpzWm5XUVliT2Z1OWtGQ0J3UnF5OUl4SklsMiIsInN1YiI6IlZ6c1puV1FZYk9mdTlrRkNCd1JxeTlJeEpJbDIiLCJpYXQiOjE2ODkzMjI3MzAsImV4cCI6MTY4OTMyNjMzMCwiZW1haWwiOiJ1c2VyMkB1c2VyMi5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidXNlcjJAdXNlcjIuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.R37wY7nXrxFPgVOPhYvhC9EWLPZV35wCUXgF9jFVBJPLZ_FOuIHMIclFM3aoHtnep2xNzC9LdMAXBtt-GibshZeeO97FXjq17I2eOUA2MPrkKEi6CpN54i00KMaeL4EQTt_QC6GCQGFMKmG2QlY63fbYEHGUZFUrubiqvM1NwJ9qF-SfVvD20ftLugU7rmGCh5cHAzj-76W743ABC15mCGwHyi1hXedW-v21RCizEF_cdyWwmPQ7cNGwnJE069PD8PN_AKwBVqIysKkVhPSS8Caxt4disgPn1U091i3vl8GdI64r_xVV4nQ9DksgJTHM3LOsPLrAzJpXC_cvW1dSbQ"
    try:
        # Firebaseトークンの検証
        print("token", id_token.split(" "))
        decoded_token = auth.verify_id_token(id_token.split(" ")[1])
        print(decoded_token)
        return User.objects.filter(email=decoded_token["email"])

    except auth.InvalidIdTokenError:
        # トークンが無効な場合の処理
        return Response({'error': 'トークンが無効です'}, status=401)

    except auth.ExpiredIdTokenError:
        # トークンの有効期限が切れている場合の処理
        return Response({'error': 'トークンの有効期限が切れています'}, status=402)

    except Exception as e:
        # その他の例外が発生した場合の処理
        return Response({'error': str(e)}, status=500)

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
def sign_up(request):
    email = request.POST.get('email')

    # Userモデルにemailとusernameを保存する
    User.objects.create_user(email=email)
    return Response({'message': 'email registered successfully'}, status=201)


@api_view(['GET'])
def getVideos(request):
    # ログイン認証
    verify_user(request=request)
    
    search_query = request.GET.get('search_query', '') 
    if search_query is None:
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    else:
        videos = Video.objects.filter(video_title__contains=search_query)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getHeadlines(request, k):
    verify_user(request=request)
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
                 "comments": [
                     {"text": "this is optional. (now implementing ...)"}
                    ]
                 }
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
def getLaterlist(request, k):
    verify_user(request=request)
    laterlist = LaterList.objects.filter(customer_id=k)
    video_id_list = []
    for later in laterlist:
        video_id_list.append(later.video_id)
    videos = Video.objects.filter(video_id__in=video_id_list)
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


# Create your views here.
