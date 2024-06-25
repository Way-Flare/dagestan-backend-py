import random
import pytest
from django.conf import settings

from django.urls import reverse
from faker import Faker
from rest_framework import status


@pytest.mark.django_db
class TestApiPlaces:
    get_routes_url = reverse('routes:route_list_view')

    def test_list_success(
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
        routes = [route_factory() for _ in range(4)]
        [feedback_route_factory(route=route) for route in routes for _ in range(random.randint(3, 6))]
        [route_images_factory(route=route) for route in routes for _ in range(random.randint(1, 4))]
        response = client.get(self.get_routes_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()
        assert len(response.json()) == 4


@pytest.mark.django_db
class TestApiPlace:
    get_route_url = reverse('routes:route_retrieve_view', kwargs={'pk': 1})

    def test_retrieve_success(
            self,
            client,
            place_factory,
            route_factory,
            route_place_factory,
            route_images_factory,
            place_images_factory,
            feedback_route_factory
    ):
        routes = [route_factory() for _ in range(4)]
        places = [place_factory() for _ in range(3)]
        [place_images_factory(place=place) for place in places for _ in range(random.randint(1, 4))]
        [feedback_route_factory(route=route) for route in routes for _ in range(random.randint(3, 6))]
        [route_images_factory(route=route) for route in routes for _ in range(random.randint(1, 4))]
        [route_place_factory(route=routes[0], place=place) for place in places]
        response = client.get(self.get_route_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['places']) == len(places)


@pytest.mark.django_db
class TestAddedFeedbackToRoute:
    feedback_to_route_url = reverse('routes:feedback_to_route', kwargs={'pk': 1})

    def test_201_add_feedback_success(
            self,
            client,
            user_with_credentials_factory,
            route_factory,
            faker: Faker
    ):
        user, credentials = user_with_credentials_factory()
        client.credentials(**credentials)
        route_factory(id=1)
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
                    self.feedback_to_route_url, data=feedback_data, format='multipart'
                )

        assert response.status_code == status.HTTP_201_CREATED

        user.refresh_from_db()
        feedbacks_to_route = user.user_feedbacks_routes.all()
        assert feedbacks_to_route
        feedback_to_route = feedbacks_to_route[0]

        fields = {
            'stars',
            'comment'
        }

        for field in fields:
            assert feedback_data[field] == getattr(feedback_to_route, field, None)

        images_feedback_route = feedback_to_route.images.all()
        assert len(images_feedback_route) == 2
