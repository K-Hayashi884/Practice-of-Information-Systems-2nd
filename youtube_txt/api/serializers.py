from rest_framework.serializers import ModelSerializer
from .models import Video
from .models import Headline

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class HeadlineSerializer(ModelSerializer):
    class Meta:
        model = Headline
        fields = '__all__'