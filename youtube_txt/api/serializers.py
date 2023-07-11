from rest_framework.serializers import ModelSerializer
from .models import Video
from .models import Headline
from .models import LaterList

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class HeadlineSerializer(ModelSerializer):
    class Meta:
        model = Headline
        fields = '__all__'

class LaterlistSerializer(ModelSerializer):
    class Meta:
        model = LaterList
        fields = '__all__'
