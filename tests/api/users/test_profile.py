import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from user.models import User


@pytest.mark.django_db
class TestGetMyProfile:
    get_my_profile = reverse('users:get_update_delete_my_profile')
    def test_200_success(
            self,
            faker,
            client,
            user_factory,
            user_with_credentials_factory
    ):
        """Проверка на успешное получение профиля пользователя."""
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user = user_factory(phone=phone, password=password)
        user, credentials = user_with_credentials_factory(user=user)
        client.credentials(**credentials)
        response = client.get(self.get_my_profile)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        fields = {
            'username',
            'phone',
            'email'
        }
        for field in fields:
            assert result.get(field) == getattr(user, field, None)
        assert result['avatar']

    def test_403_forbidden(
            self,
            faker,
            client,
            user_factory,
    ):
        """Проверка на права получение профиля пользователя, без авторизационных headers."""
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user_factory(phone=phone, password=password)
        response = client.get(self.get_my_profile)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUpdateMyProfile:
    get_my_profile = reverse('users:get_update_delete_my_profile')

    def test_200_success(
            self,
            faker,
            client,
            user_factory,
            user_with_credentials_factory
    ):
        """Проверка на успешное обновление профиля пользователя."""
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user = user_factory(phone=phone, password=password)
        user, credentials = user_with_credentials_factory(user=user)
        client.credentials(**credentials)

        new_user_data = {
            'username': faker.word(),
            'email': faker.email()
        }
        avatar_image_file_path = settings.TEST_STATIC_FILES_FIR / 'avatar.jpg'

        with avatar_image_file_path.open('rb') as file:
            new_user_data['photo'] = file
            response = client.patch(self.get_my_profile, data=new_user_data, format='multipart')

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result
        fields = {
            'username',
            'email'
        }
        user.refresh_from_db()

        for field in fields:
            assert new_user_data.get(field) == getattr(user, field, None)
        assert result['avatar']

    def test_200_success_not_changed_phone_num(
            self,
            faker,
            client,
            user_factory,
            user_with_credentials_factory
    ):
        """Проверка на неизменность номера телефона в профиле пользователя."""
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user = user_factory(phone=phone, password=password)
        user, credentials = user_with_credentials_factory(user=user)
        client.credentials(**credentials)

        new_user_data = {
            'username': faker.word(),
            'phone': faker.unique.numerify('79#########'),
            'email': faker.email()
        }

        response = client.patch(self.get_my_profile, data=new_user_data, format='multipart')

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result

        fields = {
            'username',
            'email',
            'phone'
        }
        user.refresh_from_db()

        for field in fields:
            if field == 'phone':
                assert not new_user_data.get(field) == getattr(user, field, None)
            else:
                assert new_user_data.get(field) == getattr(user, field, None)


@pytest.mark.django_db
class TestDeleteUserProfile:
    delete_my_profile = reverse('users:get_update_delete_my_profile')

    def test_200_success_delete_profile(
            self,
            faker,
            client,
            user_factory,
            user_with_credentials_factory
    ):
        """Проверка на успешное удаление профиля пользователя."""
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user = user_factory(phone=phone, password=password)
        user, credentials = user_with_credentials_factory(user=user)
        client.credentials(**credentials)

        exists_user = User.objects.filter(id=user.id).exists()
        assert exists_user

        response = client.delete(path=self.delete_my_profile)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()

        exists_user = User.objects.filter(id=user.id).exists()
        assert not exists_user

    def test_200_success_delete_feedbacks(
            self,
            faker,
            client,
            user_factory,
            feedback_place_factory,
            feedback_route_factory,
            user_with_credentials_factory
    ):
        """Проверка на успешное удаление профиля пользователя и связанных с ним отзывов."""
        phone = faker.unique.numerify('79#########')
        password = faker.unique.password()
        user = user_factory(phone=phone, password=password)
        user, credentials = user_with_credentials_factory(user=user)
        client.credentials(**credentials)

        user_feedbacks_place = [feedback_place_factory(user=user) for _ in range(3)]
        user_feedbacks_route = [feedback_route_factory(user=user) for _ in range(3)]

        assert len(user.user_feedbacks_places.all()) == len(user_feedbacks_place)
        assert len(user.user_feedbacks_routes.all()) == len(user_feedbacks_route)

        response = client.delete(path=self.delete_my_profile)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()

        assert not len(user.user_feedbacks_places.all())
        assert not len(user.user_feedbacks_routes.all())
