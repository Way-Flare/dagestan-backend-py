import datetime

import pytest
import requests_mock
from django.conf import settings
from django.core.cache import caches
from django.urls import reverse
from rest_framework import status

from services.ucaller import UCallerService

cache = caches[settings.PHONES_CACHE_KEY]


@pytest.mark.django_db
class TestApiAuthPhoneResetPasswordSendVerifCode:
    send_verif_code_url = reverse('authenticate:reset_password_user_by_phone-send_verification_code')

    def test_success(
            self,
            client,
            faker,
            user_factory,
            ucaller_init_call_mock
    ):
        phone = faker.unique.numerify('79#########')
        user_factory(phone=phone)
        response = client.post(self.send_verif_code_url, data={'phone': phone})
        assert response.status_code == status.HTTP_200_OK
        assert cache.get(phone)

    def test_not_phone(
            self,
            client,
            faker,
            user_factory,
            ucaller_init_call_mock
    ):
        phone = faker.unique.numerify('79#########')
        response = client.post(self.send_verif_code_url, data={'phone': phone})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not cache.get(phone)

    def test_many_request_one_phone(
            self,
            client,
            faker,
            user_factory,
            ucaller_init_call_mock
    ):
        phone = faker.unique.numerify('79#########')
        user_factory(phone=phone)
        response = [client.post(self.send_verif_code_url, data={'phone': phone}) for _ in range(3)]
        assert response[-1].status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert cache.get(phone)


@pytest.mark.django_db
class TestApiAuthPhoneResetPasswordConfirmVerifCode:
    confirm_verif_code_url = reverse('authenticate:reset_password_user_by_phone-confirm_phone_by_verification-code')

    def test_success(
            self,
            client,
            faker,
    ):
        phone = faker.unique.numerify('79#########')
        verif_code = 3636
        cache_data = {'code': verif_code, 'time': datetime.datetime.now(), 'confirmed': False}
        cache.set(phone, cache_data)
        response = client.post(self.confirm_verif_code_url, data={'phone': phone, 'code': verif_code})
        assert response.status_code == status.HTTP_200_OK
        phone_cache_data = cache.get(phone)
        assert phone_cache_data.get('confirmed')

    def test_invalid_verif_code(
            self,
            client,
            faker,
    ):
        phone = faker.unique.numerify('79#########')
        verif_code = 3636
        invalid_verif_code = 1234
        cache_data = {'code': verif_code, 'time': datetime.datetime.now(), 'confirmed': False}
        cache.set(phone, cache_data)
        response = client.post(self.confirm_verif_code_url, data={'phone': phone, 'code': invalid_verif_code})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_phone_in_cache(
            self,
            client,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        verif_code = 1234
        response = client.post(self.confirm_verif_code_url, data={'phone': phone, 'code': verif_code})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not cache.get(phone)


@pytest.mark.django_db
class TestApiAuthPhoneRegisterRegisterByPhone:
    reset_password_url = reverse('authenticate:reset_password_user_by_phone-reset_password_by_phone')

    def test_success(
            self,
            client,
            user_factory,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        cache_data = {'code': 3636, 'time': datetime.datetime.now(), 'confirmed': True}
        cache.set(phone, cache_data)

        user = user_factory(phone=phone)
        response = client.patch(self.reset_password_url, data={'phone': phone, 'password': password})
        assert response.status_code == status.HTTP_200_OK

        assert not cache.get(phone)

        user.refresh_from_db()
        user.check_password(password)

    def test_unconfirmed_phone_by_verif_code(
            self,
            client,
            user_factory,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        new_password = faker.unique.password()
        cache_data = {'code': 3636, 'time': datetime.datetime.now(), 'confirmed': False}
        cache.set(phone, cache_data)

        user = user_factory(phone=phone, password=password)
        response = client.patch(self.reset_password_url, data={'phone': phone, 'password': new_password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert cache.get(phone)

        user.refresh_from_db()
        assert not user.check_password(new_password)

    def test_not_exist_user(
            self,
            client,
            user_factory,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        new_password = faker.unique.password()
        cache_data = {'code': 3636, 'time': datetime.datetime.now(), 'confirmed': True}
        cache.set(phone, cache_data)

        response = client.patch(self.reset_password_url, data={'phone': phone, 'password': new_password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert not cache.get(phone)
