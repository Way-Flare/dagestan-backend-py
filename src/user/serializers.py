from rest_framework import serializers

from user.models import User


class UserFeedbackPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'avatar')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'phone', 'email')
        read_only_fields = ('phone',)
