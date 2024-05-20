from django.http import JsonResponse
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import status, serializers

from authenticate.api.serializers.phone.login import LoginByPhoneSerializers
from authenticate.exceptions import AuthorizedUserException
from authenticate.service import UserAuthService
from common.permissions import IsAnonymousUser


@extend_schema(
    tags=['Пользователи'],
    methods=['POST'],
    request=LoginByPhoneSerializers,
    description='Аутентификация пользователя в сервисе.',
    responses={
        201: OpenApiResponse(
            description='Успешное обновление токена.',
            response=inline_serializer(
                "AuthSerializer",
                fields={
                    'access': serializers.CharField(),
                }
            ),
        ),
        400: OpenApiResponse(
            description='Проверьте правильность введённых данных.'
        )
    }
)
class AuthenticateUserView(APIView):
    serializer_class = LoginByPhoneSerializers
    permission_classes = [IsAnonymousUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        auth_service = UserAuthService()

        try:
            user = auth_service.login_by_phone(phone, password)
        except AuthorizedUserException:
            return JsonResponse(
                {'detail': 'Проверьте правильность введённых данных.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = auth_service.get_tokens_for_user(user)

        return JsonResponse(data=token, status=status.HTTP_200_OK)
