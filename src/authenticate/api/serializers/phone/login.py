from rest_framework import serializers

from authenticate.api.serializers.common import BasePhoneSerializers


class LoginByPhoneSerializers(BasePhoneSerializers):
    password = serializers.CharField(write_only=True, required=True)
