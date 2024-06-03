import io

import pytest
from PIL import Image
from django.conf import settings
from django.core.cache import caches
from django.core.management import call_command

import random

import pytest
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from place.models import Place, Tag, TagPlace, FeedBackPlace, PlaceImages, FeedBackPlaceImage, Way, WayImage, \
    PlaceContact
from route.models import Route, RoutePlace, RouteImages, FeedBackRoute
from services.ucaller import UCallerService
from user.models import User


cache = caches[settings.PHONES_CACHE_KEY]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture(scope='function', autouse=True)
def clear_database():
    call_command('flush', interactive=False)


@pytest.fixture()
def user_factory(faker: Faker):
    """Фабрика пользователей."""
    def create_user(**kwargs):
        param = dict(
            avatar='path_to_img.png',
            username=faker.unique.word(),
            email=faker.unique.email(),
            phone=faker.unique.numerify('79#########')
        )
        param.update(kwargs)
        return User.objects.create_user(**param)

    return create_user


@pytest.fixture()
def user_with_credentials_factory(user_factory):
    """Пользователь с авторизационными куками."""
    def create_item(user=None):
        if not user:
            user = user_factory()
        token = RefreshToken.for_user(user)
        return user, dict(
            HTTP_AUTHORIZATION=f'Bearer {token.access_token}'
        )

    return create_item


@pytest.fixture()
def tag_place_factory():
    """Фабрика m2m place-tag."""
    is_main_tags = set()

    def _create_item(**kwargs):
        is_main = False
        if kwargs.get('place') not in is_main_tags:
            is_main_tags.add(kwargs.get('place'))
            is_main = True
        param = dict(
            is_main=is_main
        )
        param.update(kwargs)
        return TagPlace.objects.create(**param)

    return _create_item


@pytest.fixture()
def tag_factory(faker: Faker):
    """Фабрика тегов."""

    def _create_item(**kwargs):
        param = dict(
            name=faker.word(),
        )
        param.update(kwargs)
        return Tag.objects.create(**param)

    return _create_item


@pytest.fixture()
def place_factory(faker: Faker, tag_factory, tag_place_factory):
    """Фабрика мест (объектов)."""

    def _create_item(**kwargs):
        param = dict(
            name=faker.word(),
            longitude=faker.random_number(),
            latitude=faker.random_number(),
            is_visible=True,
            description=faker.text(),
            short_description=faker.text(),
            address=faker.address(),
        )
        param.update(kwargs)
        place = Place.objects.create(**param)

        if not kwargs.pop('tag', None):
            tag = tag_factory()
            tag_place_factory(tag=tag, place=place)
        return place

    return _create_item


@pytest.fixture()
def feedback_place_factory(faker: Faker, place_factory, user_factory):
    """Фабрика отзывов места (объектов)."""

    def _create_item(**kwargs):
        if not kwargs.get('place'):
            kwargs['place'] = place_factory()
        if not kwargs.get('user'):
            kwargs['user'] = user_factory()

        param = dict(
            stars=random.randint(1, 5),
            comment=faker.text()
        )
        param.update(kwargs)
        feedback = FeedBackPlace.objects.create(
            **param
        )
        return feedback

    return _create_item


@pytest.fixture()
def feedback_place_images_factory(faker: Faker, feedback_place_factory):

    def _create_item(**kwargs):
        if 'feedback_place' not in kwargs:
            kwargs['feedback_place'] = feedback_place_factory()
        param = dict(
            name=faker.word(),
            file=f'{faker.word()}_feedback.png',
        )
        param.update(kwargs)
        return FeedBackPlaceImage.objects.create(**param)

    return _create_item


@pytest.fixture()
def place_images_factory(faker: Faker, place_factory):
    is_main_images = set()

    def _create_item(**kwargs):
        if 'place' not in kwargs:
            kwargs['place'] = place_factory()
        if kwargs['place'] not in is_main_images:
            is_main_images.add(kwargs['place'])
            kwargs['file'] = 'path_to_img_main_place.png'
            kwargs['is_main'] = True
        param = dict(
            name=faker.word(),
            file=f'{faker.word()}_place.png',
            is_main=False,
        )
        param.update(kwargs)
        return PlaceImages.objects.create(**param)

    return _create_item


@pytest.fixture()
def route_factory(faker: Faker, place_factory):
    def _create_item(**kwargs):
        param = dict(
            title=faker.word(),
            description=faker.text(),
            travel_time=faker.time(),
            distance=faker.random_number(),
            is_visible=True
        )
        param.update(kwargs)
        route = Route.objects.create(**param)
        return route

    return _create_item


@pytest.fixture()
def route_place_factory(faker: Faker, place_factory, route_factory):
    def _create_item(**kwargs):
        if not kwargs.get('place'):
            kwargs['place'] = place_factory()
        if not kwargs.get('route'):
            kwargs['route'] = route_factory()
        param = dict(
            sequence=random.randint(1, 5)
        )
        param.update(kwargs)
        route_place = RoutePlace.objects.create(**param)
        return route_place

    return _create_item


@pytest.fixture()
def route_images_factory(faker: Faker, route_factory):
    is_main_images = set()

    def _create_item(**kwargs):
        if 'route' not in kwargs:
            kwargs['route'] = route_factory()
        if kwargs['route'] not in is_main_images:
            is_main_images.add(kwargs['route'])
            kwargs['file'] = 'path_to_img_main_route.png'
            kwargs['is_main'] = True
        param = dict(
            name=faker.word(),
            file=f'{faker.word()}_route.png',
            is_main=False,
        )
        param.update(kwargs)
        return RouteImages.objects.create(**param)

    return _create_item


@pytest.fixture()
def way_factory(faker: Faker, place_factory):
    def _create_item(**kwargs):
        if not kwargs.get('place'):
            kwargs['place'] = place_factory()
        param = dict(
           info=faker.text()
        )
        param.update(kwargs)
        way = Way.objects.create(**param)
        return way

    return _create_item


@pytest.fixture()
def way_images_factory(faker: Faker, way_factory):

    def _create_item(**kwargs):
        if 'way' not in kwargs:
            kwargs['way'] = way_factory()
        param = dict(
            name=faker.word(),
            file=f'{faker.word()}_way.png',
        )
        param.update(kwargs)
        return WayImage.objects.create(**param)

    return _create_item


@pytest.fixture()
def place_contact_factory(faker: Faker, place_factory):

    def _create_item(**kwargs):
        if 'place' not in kwargs:
            kwargs['place'] = place_factory()
        param = dict(
            phone_number=faker.unique.numerify('79#########'),
            email=faker.email(),
        )
        param.update(kwargs)
        return PlaceContact.objects.create(**param)

    return _create_item


@pytest.fixture()
def feedback_route_factory(faker: Faker, route_factory, user_factory):
    """Фабрика отзывов места (объектов)."""

    def _create_item(**kwargs):
        if not kwargs.get('route'):
            kwargs['route'] = route_factory()
        if not kwargs.get('user'):
            kwargs['user'] = user_factory()

        param = dict(
            stars=random.randint(1, 5),
            comment=faker.text()
        )
        param.update(kwargs)
        feedback = FeedBackRoute.objects.create(
            **param
        )
        return feedback

    return _create_item


@pytest.fixture()
def ucaller_init_call_mock(monkeypatch):
    """Мокер для вызова функции init_call у сервиса Ucaller"""
    def init_call(self, phone, code):
        return True
    monkeypatch.setattr(UCallerService, 'init_call', init_call)


@pytest.fixture(scope='function', autouse=True)
def flash_redis_cache():
    cache.clear()
