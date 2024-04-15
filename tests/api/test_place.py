import random

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestApiPlaces:
    get_places_url = reverse('place:place_list_view')

    def test_list_success(
            self,
            client,
            place_factory,
            feedback_place_factory
    ):
        places = [place_factory() for _ in range(15)]
        [feedback_place_factory(place=place) for place in places for _ in range(5)]
        response = client.get(self.get_places_url)
        assert response.status_code == 200
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
        assert response.json()[0]['image']['file'].endswith('main.png')


@pytest.mark.django_db
class TestApiGetPlace:
    get_place_url = reverse('place:place_retrieve_view', kwargs={'pk': 1})

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
        assert response.status_code
        assert response.json()
