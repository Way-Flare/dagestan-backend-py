import random

import pytest
from django.conf import settings
from django.urls import reverse
from faker import Faker
from rest_framework import status


@pytest.mark.django_db
class TestApiPlaces:
    get_places_url = reverse('places:place_list_view')

    def test_list_success(
            self,
            client,
            place_factory,
            feedback_place_factory
    ):
        places = [place_factory() for _ in range(15)]
        [feedback_place_factory(place=place) for place in places for _ in range(5)]
        response = client.get(self.get_places_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(places)

    def test_list_images(
            self,
            client,
            place_factory,
            place_images_factory
    ):
        places = [place_factory() for _ in range(2)]
        [place_images_factory(place=place) for place in places for _ in range(5)]
        response = client.get(self.get_places_url)
        assert response.status_code == 200
        assert len(response.json()) == len(places)
        assert len(response.json()[0]['images']) == 5


@pytest.mark.django_db
class TestApiGetPlace:
    get_place_url = reverse('places:place_retrieve_view', kwargs={'pk': 1})

    def test_retrieve_success(
            self,
            client,
            place_factory,
            feedback_place_factory,
            feedback_place_images_factory,
            route_factory,
            route_place_factory,
            route_images_factory,
            place_images_factory,
            way_factory,
            way_images_factory,
            place_contact_factory,
            feedback_route_factory
    ):
        places = [place_factory() for _ in range(15)]
        [place_images_factory(place=place) for place in places for _ in range(random.randint(1, 3))]
        [place_contact_factory(place=place) for place in places]
        feedbacks = [feedback_place_factory(place=place) for place in places for _ in range(5)]
        [feedback_place_images_factory(feedback_place=feedback_place) for feedback_place in feedbacks for _ in range(5)]
        routes = [route_factory() for _ in range(4)]
        [feedback_route_factory(route=route) for route in routes for _ in range(random.randint(3, 6))]
        [route_place_factory(route=route, place=place) for route in routes for place in places]
        [route_images_factory(route=route) for route in routes for _ in range(random.randint(1, 4))]
        ways = [way_factory(place=place) for place in places for _ in range(random.randint(1, 2))]
        [way_images_factory(way=way) for way in ways for _ in range(random.randint(1, 3))]
        response = client.get(self.get_place_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()


@pytest.mark.django_db
class TestSubscribeUnsubscribeToPlace:
    subscribe_unsubscribe_url = reverse('places:subscribe_unsubscribe_to_place', kwargs={'pk': 1})

    def test_201_subscribe_success(
            self,
            client,
            user_with_credentials_factory,
            place_factory
    ):
        user, credentials = user_with_credentials_factory()
        client.credentials(**credentials)
        place_factory(id=1)

        assert not user.favorites_place.all()
        response = client.post(self.subscribe_unsubscribe_url)
        assert response.status_code == status.HTTP_201_CREATED

        user.refresh_from_db()
        assert user.favorites_place.all()

    def test_204_unsubscribe_success(
            self,
            client,
            user_with_credentials_factory,
            place_factory
    ):
        user, credentials = user_with_credentials_factory()
        client.credentials(**credentials)

        place = place_factory(id=1)
        user.favorites_place.add(place)

        response = client.post(self.subscribe_unsubscribe_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        user.refresh_from_db()
        assert not user.favorites_place.all()


@pytest.mark.django_db
class TestAddedFeedbackToPlace:
    feedback_to_place_url = reverse('places:feedback_to_place', kwargs={'pk': 1})

    def test_201_add_feedback_success(
            self,
            client,
            user_with_credentials_factory,
            place_factory,
            faker: Faker
    ):
        user, credentials = user_with_credentials_factory()
        client.credentials(**credentials)
        place_factory(id=1)
        settings.MEDIA_ROOT = settings.TEST_STATIC_FILES_FIR / 'for_testing_payload'

        feedback_data = {
            'stars': 5,
            'comment': faker.text(),
        }

        avatar_image_file_path = settings.TEST_STATIC_FILES_FIR / 'avatar.jpg'

        assert not user.user_feedbacks_places.all()

        with avatar_image_file_path.open('rb') as file:
            with avatar_image_file_path.open('rb') as file2:
                feedback_data['images'] = [file, file2]
                response = client.post(
                    self.feedback_to_place_url, data=feedback_data, format='multipart'
                )

        assert response.status_code == status.HTTP_201_CREATED

        user.refresh_from_db()
        feedbacks_to_place = user.user_feedbacks_places.all()
        assert feedbacks_to_place
        feedback_to_place = feedbacks_to_place[0]

        fields = {
            'stars',
            'comment'
        }

        for field in fields:
            assert feedback_data[field] == getattr(feedback_to_place, field, None)

        images_feedback_place = feedback_to_place.images.all()
        assert len(images_feedback_place) == 2
