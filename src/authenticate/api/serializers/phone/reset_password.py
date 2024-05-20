from rest_framework import serializers

from authenticate.api.serializers.common import BasePhoneSerializers
from user.models import User


class ResetPasswordSendVerifCodeToPhoneSerializer(BasePhoneSerializers):
    pass


class ConfirmPhoneVerifCodeResetPasswordSerializers(BasePhoneSerializers):
    code = serializers.IntegerField(required=True, write_only=True)


class SetNewPasswordResetPasswordSerializer(BasePhoneSerializers):
    password = serializers.CharField(max_length=32, write_only=True, min_length=8, required=True)
