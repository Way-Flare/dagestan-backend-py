from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import status, serializers

from authenticate.api.serializers.common import RefreshAccessTokenSerializers
from authenticate.service import UserAuthService


@extend_schema(
    tags=['Пользователи'],
    methods=['POST'],
    request=RefreshAccessTokenSerializers,
    description='Обновление токена по его refresh токену',
    responses={
        201: OpenApiResponse(
            description='Успешное обновление токена.',
            response=inline_serializer(
                "AuthSerializer",
                fields={
                    'access': serializers.CharField(),
                    'refresh': serializers.CharField(),
                },
            ),
        ),
        400: OpenApiResponse(
            description='Невалидный refresh токен'
        )
    }
)
class TokenView(APIView):
    serializer_class = RefreshAccessTokenSerializers
    permission_classes = [AllowAny]

    def post(self, request):
        """Получение access токена по refresh"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = UserAuthService()

        refresh_token = serializer.validated_data['refresh_token']

        data = auth_service.get_access_token(refresh_token)
        if not data:
            return JsonResponse({'detail': 'Невалидный refresh токен'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data=data, status=status.HTTP_200_OK)
