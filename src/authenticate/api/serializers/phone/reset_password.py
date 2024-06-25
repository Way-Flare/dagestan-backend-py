from rest_framework import serializers

from authenticate.api.serializers.common import BasePhoneSerializers, BasePhonePasswordSerializers


class ResetPasswordSendVerifCodeToPhoneSerializer(BasePhoneSerializers):
    pass


class ConfirmPhoneVerifCodeResetPasswordSerializers(BasePhoneSerializers):
    code = serializers.IntegerField(required=True, write_only=True)


class SetNewPasswordResetPasswordSerializer(BasePhonePasswordSerializers):
    pass
