from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoSerializer
from .serializers import HeadlineSerializer
from .models import Video
from .models import Headline
from .models import LaterList



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

@api_view(['GET'])
def getLaterlist(request,k):
    laterlist = LaterList.objects.filter(customer_id=k)
    video_id_list = []
    for later in laterlist:
        video_id_list.append(later.video_id)
    videos = Video.objects.filter(video_id__in=video_id_list)
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


# Create your views here.
