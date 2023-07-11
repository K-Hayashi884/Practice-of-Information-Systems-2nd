from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('top/', views.getVideos),
    path('list/post/', views.add_to_later_list), 
    path('list/delete/', views.delete_from_later_list), 
    path('index/<str:k>/',views.getHeadlines),
    path('list/<str:k>/', views.getLaterlist),
]