from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('top/', views.getVideos),
    path('list/', views.LaterListAPI.as_view()),
    path('index/<str:k>/',views.getHeadlines),
    path("get_all_indices/", views.get_all_indices)

]