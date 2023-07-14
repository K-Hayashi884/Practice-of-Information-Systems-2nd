from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UserManager

from rest_framework import authentication, permissions, generics
from django.db import transaction
from rest_framework import status, viewsets, filters



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated, )

# @api_view(['POST'])
# def create_user(request):
#     data = request.data

#     email = data['email']
#     username = data['username']
#     password = data['password']

#     user = UserManager.create_user(
#         email=email,
#         username=username,
#         password=password,
#         )
    
#     serializer = UserSerializer(user)
    
#     return Response(serializer.data)

class AuthRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)