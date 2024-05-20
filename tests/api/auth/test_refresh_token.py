import pytest
from django.urls import reverse
from rest_framework import status

from authenticate.service import UserAuthService


@pytest.mark.django_db
class TestApiAuthPhoneLogin:
    login_user_by_phone_url = reverse('authenticate:refresh_token')

    def test_success(
            self,
            client,
            user_factory
    ):
        user = user_factory()
        auth_service = UserAuthService()
        token = auth_service.get_tokens_for_user(user)
        response = client.post(self.login_user_by_phone_url, data={'refresh_token': token['refresh']})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_invalid_refresh_token(
            self,
            client,
            user_factory
    ):
        token = {'refresh': 'invalid_token'}
        response = client.post(self.login_user_by_phone_url, data={'refresh_token': token['refresh']})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
