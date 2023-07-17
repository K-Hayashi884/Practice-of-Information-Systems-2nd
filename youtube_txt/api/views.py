from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoSerializer
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
    if search_query == None:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
    else:
        videos = Video.objects.filter(video_title__contains=search_query)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getHeadlines(request,k):
    headlines = Headline.objects.filter(video_id=k).order_by('timestamp')
    serializer = HeadlineSerializer(headlines, many=True)
    return Response (serializer.data)

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
