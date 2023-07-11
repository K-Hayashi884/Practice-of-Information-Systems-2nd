from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UserManager



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

@api_view(['POST'])
def create_user(request):
    data = request.data

    email = data['email']
    username = data['username']
    password = data['password']

    user = UserManager.create_user(
        email=email,
        username=username,
        password=password,
        )
    
    serializer = UserSerializer(user)
    
    return Response(serializer.data)