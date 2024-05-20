from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

from authenticate.exceptions import ThrottlingException, InvalidVerificationCodeException, UnconfirmedPhoneException
from authenticate.service import UserAuthService
from common.permissions import IsAnonymousUser
from common.throttling import AuthAnonRateThrottle
from rest_framework import status, serializers
from rest_framework.decorators import throttle_classes
from common.custom_action_view import action

from django.conf import settings
from authenticate.api.serializers.phone.reset_password import (
    ResetPasswordSendVerifCodeToPhoneSerializer,
    ConfirmPhoneVerifCodeResetPasswordSerializers, SetNewPasswordResetPasswordSerializer,
)
from services.ucaller import UCallerException
from user.models import User


class ResetPasswordView(GenericViewSet):
    serializer_class = ResetPasswordSendVerifCodeToPhoneSerializer
    permission_classes = [IsAnonymousUser]

    @extend_schema(
        tags=['Пользователи'],
        methods=['POST'],
        request=ResetPasswordSendVerifCodeToPhoneSerializer,
        description='Отправка кода верификации на номер телефона для сброса пароля.',
        responses={
            200: OpenApiResponse(
                description='Код верификации отправлен.',
            ),
            429: OpenApiResponse(
                description='Много запросов.'
            ),
            400: OpenApiResponse(
                description='Номер не зарегистрирован в системе.'
            )
        }
    )
    @throttle_classes([AuthAnonRateThrottle])
    @action(
        methods=['POST'],
        detail=False,
        url_path='send-verification-code',
        url_name='send_verification_code',
    )
    def send_verification_code_to_phone(self, request):
        """Отправка кода верификации на номер телефона."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        auth_service = UserAuthService()

        exist_phone = User.objects.filter(phone=phone).exists()
        if not exist_phone:
            return JsonResponse(
                {'detail': 'Номер не зарегистрирован в системе.'},
                status=status.HTTP_400_BAD_REQUEST
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
        request=ConfirmPhoneVerifCodeResetPasswordSerializers,
        description='Подтверждение номера телефона по коду верификации для сброса пароля.',
        responses={
            200: OpenApiResponse(
                description='Номер телефона подтвержден.',
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
        serializer_class=ConfirmPhoneVerifCodeResetPasswordSerializers,
        url_name='confirm_phone_by_verification-code',
    )
    def confirm_phone_by_verification_code_reset_password(self, request):
        """Подтверждение номера телефона по коду верификации при сбросе пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        auth_service = UserAuthService()

        try:
            auth_service.confirm_phone_by_verification_code(phone, code)
        except InvalidVerificationCodeException:
            return JsonResponse({'detail': 'Невалидный код верификации.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(
            {'detail': 'Номер телефона подтвержден.'},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        tags=['Пользователи'],
        methods=['PATCH'],
        request=SetNewPasswordResetPasswordSerializer,
        description='Изменение пароля учетной записи.',
        responses={
            201: OpenApiResponse(
                description='Пароль изменен.',
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
        methods=['PATCH'],
        detail=False,
        url_path='',
        serializer_class=SetNewPasswordResetPasswordSerializer,
        url_name='reset_password_by_phone',
    )
    def reset_password_by_phone(self, request):
        """Установка нового пароля учетной записи пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        auth_service = UserAuthService()

        try:
            auth_service.check_confirmed_phone(phone)
        except UnconfirmedPhoneException:
            return JsonResponse({'detail': 'Подтвердите номер телефона.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if not user:
            return JsonResponse(
                {'detail': 'Проверьте правильность введённых данных.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()

        token = auth_service.get_tokens_for_user(user)

        return JsonResponse(data=token, status=status.HTTP_200_OK)
