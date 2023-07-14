from django.urls import path
from . import views
# from .views import UserViewSet
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.getRoutes)),
    path('top/', views.getVideos),
    path('index/<str:k>/', views.getHeadlines),
    path('list/<str:k>/', views.getLaterlist),
    path('sign_up/', views.sign_up)
]
