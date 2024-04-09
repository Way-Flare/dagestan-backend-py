import pytest
from rest_framework.test import APIClient

import random

import pytest
from faker import Faker
from rest_framework.test import APIClient

from place.models import Place, Tag, TagPlace, FeedBackPlace, PlaceImages
from user.models import User


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def user_factory(faker: Faker):
    """Фабрика пользователей."""
    def create_user(**kwargs):
        param = dict(
            username=faker.unique.word(),
            email=faker.unique.email(),
            phone=faker.unique.numerify('79#########')
        )
        param.update(kwargs)
        return User.objects.create_user(**param)

    return create_user


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
        FeedBackPlace.objects.create(
            **param
        )
    return _create_item


@pytest.fixture()
def place_images_factory(faker: Faker, place_factory):
    is_main_images = set()

    def _create_item(**kwargs):
        if 'place' not in kwargs:
            kwargs['place'] = place_factory()
        if kwargs['place'] not in is_main_images:
            is_main_images.add(kwargs['place'])
            kwargs['file'] = 'path_to_img_main.png'
            kwargs['is_main'] = True
        param = dict(
            name=faker.word(),
            file='path_to_img.png',
            is_main=False,
        )
        param.update(kwargs)
        return PlaceImages.objects.create(**param)

    return _create_item
