from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
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


# getHeadline（views.py）で使用する
class CommentSerializer(serializers.Serializer):
    text = serializers.CharField()


class IndexSerializer(serializers.Serializer):
    timestamp = serializers.CharField()
    headline = serializers.CharField()


class getHeadlineSerializer(serializers.Serializer):
    class TmpSerializer(serializers.Serializer):
        video_id = serializers.CharField()
        url = serializers.CharField()
        title = serializers.CharField()
        indices = IndexSerializer(many=True)
        comments = CommentSerializer(many=True)
    
    video = TmpSerializer()
