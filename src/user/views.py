from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserProfileSerializer
from user.services import UserService


@extend_schema_view(
    get=extend_schema(
        tags=['Пользователи', 'Профиль пользователя'],
        methods=['GET'],
        description='Получение пользователем информации о профиле',
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer,
            )
        }
    ),
    patch=extend_schema(
        tags=['Пользователи', 'Профиль пользователя'],
        methods=['PATCH'],
        request=UserProfileSerializer,
        description='Изменение пользователем информации профиля',
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer,
            ),
            400: OpenApiResponse(
                description='Адрес электронной почты уже существует.'
            )
        }
    ),
    delete=extend_schema(
        tags=['Пользователи', 'Профиль пользователя'],
        methods=['DELETE'],
        description='Удаление профиля.',
        responses={
            200: OpenApiResponse(
                description='Профиль успешно удалён с системы.',
            )
        }
    )
)
class UserProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializers = UserProfileSerializer

    def get(self, request):
        """Отдает профиль текущего пользователя."""
        serializer = self.serializers(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Обновляет информацию о текущем пользователе."""
        serializer = self.serializers(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if email and UserService.email_already_exists(email):
            return JsonResponse(
                {'detail': 'Адрес электронной почты уже существует.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        """Удаляет профиль пользователя полностью с системы."""
        user: User = request.user
        user.delete()
        return JsonResponse(
            {'detail': 'Профиль успешно удалён с системы.'},
            status=status.HTTP_200_OK
        )
