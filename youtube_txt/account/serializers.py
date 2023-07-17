from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        # print(validated_data.get('username'))
        return User.objects.create_user(email=validated_data.get('email'), username=validated_data.get('username'), password=validated_data.get('password'))