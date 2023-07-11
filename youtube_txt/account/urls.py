from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from . import views

router = DefaultRouter()
router.register(r'account', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.create_user),
]