import datetime

import pytest

from django.conf import settings
from django.core.cache import caches
from django.urls import reverse
from rest_framework import status

from user.models import User

cache = caches[settings.PHONES_CACHE_KEY]


class MixinApiAuthPhoneRegister:

    @staticmethod
    def exist_user(phone):
        user_exist = User.objects.filter(phone=phone).exists()
        return user_exist


@pytest.mark.django_db
class TestApiAuthPhoneRegisterSendVerifCode:
    send_verif_code_url = reverse('authenticate:register_user_by_phone-send_verification_code')

    def test_success(
            self,
            client,
            faker,
            ucaller_init_call_mock
    ):
        phone = faker.unique.numerify('79#########')
        response = client.post(self.send_verif_code_url, data={'phone': phone})
        assert response.status_code == status.HTTP_200_OK
        assert cache.get(phone)

    def test_phone_exist(
            self,
            client,
            faker,
            user_factory,
            ucaller_init_call_mock
    ):
        phone = faker.unique.numerify('79#########')
        user_factory(phone=phone)
        response = client.post(self.send_verif_code_url, data={'phone': phone})
        assert response.status_code == status.HTTP_409_CONFLICT
        assert not cache.get(phone)

    def test_many_request_one_phone(
            self,
            client,
            faker,
            user_factory,
            ucaller_init_call_mock
    ):
        phone = faker.unique.numerify('79#########')
        response = [client.post(self.send_verif_code_url, data={'phone': phone}) for _ in range(3)]
        assert response[-1].status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert cache.get(phone)


@pytest.mark.django_db
class TestApiAuthPhoneRegisterConfirmVerifCode:
    confirm_verif_code_url = reverse('authenticate:register_user_by_phone-confirm_phone_by_verification-code')

    def test_success(
            self,
            client,
            faker
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
class TestApiAuthPhoneRegisterRegisterByPhone(MixinApiAuthPhoneRegister):
    register_url = reverse('authenticate:register_user_by_phone-phone_register_user')

    def test_success(
            self,
            client,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        cache_data = {'code': 3636, 'time': datetime.datetime.now(), 'confirmed': True}
        cache.set(phone, cache_data)

        assert not self.exist_user(phone)

        response = client.post(
            self.register_url,
            data={'phone': phone, 'password': password, 'repeat_password': password}
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert not cache.get(phone)
        assert self.exist_user(phone)

    def test_unconfirmed_phone_by_verif_code(
            self,
            client,
            user_factory,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        cache_data = {'code': 3636, 'time': datetime.datetime.now(), 'confirmed': False}
        cache.set(phone, cache_data)

        response = client.post(
            self.register_url,
            data={'phone': phone, 'password': password, 'repeat_password': password}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert cache.get(phone)

        exist_phone = self.exist_user(phone)
        assert not exist_phone

    def test_bad_repeat_password(
            self,
            client,
            user_factory,
            faker
    ):
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        repeat_password = faker.unique.password()
        cache_data = {'code': 3636, 'time': datetime.datetime.now(), 'confirmed': False}
        cache.set(phone, cache_data)

        response = client.post(
            self.register_url,
            data={'phone': phone, 'password': password, 'repeat_password': repeat_password}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert cache.get(phone)

        exist_phone = self.exist_user(phone)
        assert not exist_phone
