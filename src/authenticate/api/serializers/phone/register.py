from rest_framework import serializers

from authenticate.api.serializers.common import BasePhoneSerializers
from user.models import User


class SendVerificationCodeToPhoneSerializers(BasePhoneSerializers):
    pass


class ConfirmPhoneVerificationCodeSerializers(BasePhoneSerializers):
    code = serializers.IntegerField(required=True, write_only=True)


class RegisterProfileByPhoneSerializers(BasePhoneSerializers, serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ('phone', 'password')

