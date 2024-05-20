import re

from rest_framework import serializers


def validate_phone(value):
    phone_regex = re.compile(r'^[78]\d{10}$')
    if not value.isdigit() and not phone_regex.match(value):
        raise serializers.ValidationError("Некорректный номер телефона.")
    return value


class BasePhoneSerializers(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[validate_phone], required=True)


class RefreshAccessTokenSerializers(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
