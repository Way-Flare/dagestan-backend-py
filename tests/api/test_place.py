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
