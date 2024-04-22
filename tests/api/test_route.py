import random
import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestApiPlaces:
    get_route_url = reverse('route:route_list_view')

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
        response = client.get(self.get_route_url)
        assert response.status_code
        assert response.json()
        assert len(response.json()) == 4
