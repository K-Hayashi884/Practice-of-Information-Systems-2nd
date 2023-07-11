from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('top/', views.getVideos),
    path('index/<str:k>/', views.getHeadlines),
    path('list/<str:k>/', views.getLaterlist),
    path("sign_in/", views.sign_in)

]