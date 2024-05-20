import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestApiAuthPhoneLogin:
    login_user_by_phone_url = reverse('authenticate:login_user_by_phone')

    def test_success(
            self,
            client,
            faker,
            user_factory
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user_factory(phone=phone, password=password)
        response = client.post(self.login_user_by_phone_url, data={'phone': phone, 'password': password})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_invalid_password_user(
            self,
            client,
            faker,
            user_factory
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        invalid_password = faker.unique.password()
        user_factory(phone=phone, password=invalid_password)
        response = client.post(self.login_user_by_phone_url, data={'phone': phone, 'password': password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_exist_user(
            self,
            client,
            faker,
            user_factory
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        invalid_phone = faker.unique.numerify('79#########')
        user_factory(phone=invalid_phone, password=password)
        response = client.post(self.login_user_by_phone_url, data={'phone': phone, 'password': password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
