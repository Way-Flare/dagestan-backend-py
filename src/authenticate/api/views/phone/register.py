from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

from authenticate.exceptions import ThrottlingException, UnconfirmedPhoneException, InvalidVerificationCodeException
from authenticate.service import UserAuthService
from common.permissions import IsAnonymousUser
from common.throttling import AuthAnonRateThrottle
from rest_framework import status, serializers
from rest_framework.decorators import throttle_classes
from common.custom_action_view import action
from django.conf import settings
from django.core.cache import caches
from authenticate.api.serializers.phone.register import (
    SendVerificationCodeToPhoneSerializers,
    ConfirmPhoneVerificationCodeSerializers,
    RegisterProfileByPhoneSerializers
)
from services.ucaller import UCallerException

from user.models import User


cache = caches[settings.PHONES_CACHE_KEY]


class RegisterUserByPhoneView(GenericViewSet):
    permission_classes = [IsAnonymousUser]

    @extend_schema(
        tags=['Пользователи'],
        methods=['POST'],
        request=SendVerificationCodeToPhoneSerializers,
        description='Отправка кода верификации на номер телефона.',
        responses={
            200: OpenApiResponse(
                description='Код верификации отправлен.',
            ),
            429: OpenApiResponse(
                description='Много запросов.'
            ),
            409: OpenApiResponse(
                description='Номер уже зарегистрирован в системе.'
            )
        }
    )
    @throttle_classes([AuthAnonRateThrottle])
    @action(
        methods=['POST'],
        detail=False,
        url_path='send-verification-code',
        serializer_class=SendVerificationCodeToPhoneSerializers,
        url_name='send_verification_code',
    )
    def send_verification_code_to_phone(self, request):
        """Отправка кода верификации на номер телефона."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_service = UserAuthService()

        phone = serializer.validated_data['phone']

        exist_phone = User.objects.filter(phone=phone).exists()
        if exist_phone:
            return JsonResponse(
                {'detail': 'Номер уже зарегистрирован в системе.'},
                status=status.HTTP_409_CONFLICT
            )

        try:
            auth_service.send_verification_code_to_phone(phone=phone)
        except ThrottlingException:
            return JsonResponse(
                {'detail': 'Много запросов.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        except UCallerException:
            return JsonResponse(
                {'detail': 'Ошибка сервиса звонков, повторите запрос позже.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Пользователи'],
        methods=['POST'],
        request=ConfirmPhoneVerificationCodeSerializers,
        description='Подтверждение номера телефона по коду верификации.',
        responses={
            200: OpenApiResponse(
                description='Номер подтвержден.',
            ),
            400: OpenApiResponse(
                description='Невалидный код верификации.'
            )
        }
    )
    @action(
        methods=['POST'],
        detail=False,
        url_path='confirm-verification-code',
        serializer_class=ConfirmPhoneVerificationCodeSerializers,
        url_name='confirm_phone_by_verification-code',
    )
    def confirm_phone_by_verification_code(self, request):
        """Подтверждение номера телефона по коду верификации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        auth_service = UserAuthService()

        try:
            auth_service.confirm_phone_by_verification_code(phone, code)
        except InvalidVerificationCodeException:
            return JsonResponse({'detail': 'Невалидный код верификации.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'detail': 'Номер телефона подтвержден.'}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Пользователи'],
        methods=['POST'],
        request=RegisterProfileByPhoneSerializers,
        description='Создание учётной записи пользователя по номеру телефона.',
        responses={
            201: OpenApiResponse(
                description='Успешная регистрация.',
                response=inline_serializer(
                    "AuthSerializer",
                    fields={
                        'access': serializers.CharField(),
                        'refresh': serializers.CharField(),
                    },
                ),
            ),
            400: OpenApiResponse(
                description='Подтвердите номер телефона.'
            )
        },
    )
    @action(
        methods=['POST'],
        detail=False,
        url_path='',
        serializer_class=RegisterProfileByPhoneSerializers,
        url_name='phone_register_user',
    )
    def register_by_phone(self, request):
        """Создание учётной записи пользователя по номеру телефона."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        auth_service = UserAuthService()

        try:
            auth_service.check_confirmed_phone(phone)
        except UnconfirmedPhoneException:
            return JsonResponse({'detail': 'Подтвердите номер телефона.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(phone=phone, password=password)

        token = auth_service.get_tokens_for_user(user)

        return JsonResponse(data=token, status=status.HTTP_201_CREATED)
