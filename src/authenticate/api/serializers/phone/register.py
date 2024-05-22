from rest_framework import serializers

from authenticate.api.serializers.common import BasePhoneSerializers, BasePhonePasswordSerializers
from user.models import User


class SendVerificationCodeToPhoneSerializers(BasePhoneSerializers):
    pass


class ConfirmPhoneVerificationCodeSerializers(BasePhoneSerializers):
    code = serializers.IntegerField(required=True, write_only=True)


class RegisterProfileByPhoneSerializers(BasePhonePasswordSerializers):
    pass

    class Meta:
        model = User
        fields = ('phone', 'password', 'repeat_password')

