from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Video
from .models import Headline
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class UserSerializer(serializers.ModelSerializer):   
    def update(self, instance, validated_data):
        if (not instance.username ==
                self.context['request'].user.username):
            raise PermissionDenied('You do not have permission to update')
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
        
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']


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
