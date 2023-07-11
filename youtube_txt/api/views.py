from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoSerializer
from .serializers import HeadlineSerializer
from .serializers import LaterlistSerializer
from .models import Video
from .models import Headline
from .models import LaterList
from .models import Customer



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
        {
            'Endpoint': '/list/post',
            'method': 'POST',
            'body': None,
            'description': 'Add video to laterlist, trigger when pressed'
        },       
        {
            'Endpoint': '/list/delete',
            'method': 'DELETE',
            'body': None,
            'description': 'Delete video to laterlist, trigger when pressed'
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




@api_view(['POST'])
def add_to_later_list(request):
    if request.method == 'POST':
        video_id = request.data.get('video_id')
        customer_id = request.data.get('customer_id')

        try:
            video = Video.objects.get(video_id=video_id)
            customer = Customer.objects.get(customer_id=customer_id)

            later_list = LaterList.objects.filter(customer_id=customer, video_id=video)
            if later_list.exists():
                return Response({"status": 400, "message": "Video is already in the later list."})

            LaterList.objects.create(customer_id=customer, video_id=video)

            serializer = LaterlistSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200, "message": "Video added successfully."})
            else:
                return Response({"status": 400, "message": "Invalid serializer data.", "errors": serializer.errors})

        except Video.DoesNotExist:
            return Response({"status": 404, "message": "Video not found."})

        except Customer.DoesNotExist:
            return Response({"status": 404, "message": "Customer not found."})

        except Exception as e:
            return Response({"status": 500, "message": str(e)})

    return Response({"status": 405, "message": "Method not allowed."})


@api_view(['DELETE'])
def delete_from_later_list(request):
    if request.method == 'DELETE':
        video_id = request.data.get('video_id')
        print(video_id)
        customer_id = request.data.get('customer_id')
        
        try:
            video = Video.objects.get(video_id=video_id)
            customer = Customer.objects.get(customer_id=customer_id)
            
            later_list = LaterList.objects.filter(customer_id=customer, video_id=video)
            if not later_list.exists():
                return Response({"status": 400, "message": "Video is not in the later list."})
            
            later_list.delete()
            
            serializer = LaterlistSerializer(later_list.first())
            return Response({"status": 200, "message": "Video deleted successfully.", "data": serializer.data})
        
        except Video.DoesNotExist:
            return Response({"status": 404, "message": "Video not found."})
        
        except Customer.DoesNotExist:
            return Response({"status": 404, "message": "Customer not found."})
        
        except Exception as e:
            return Response({"status": 500, "message": str(e)})

    else:
        return Response({"status": 405, "message": "Method not allowed."})


# Create your views here.
