from django.urls import path

from place.views import PlaceListView

app_name = 'place'

urlpatterns = [
    path(r'all', PlaceListView.as_view(), name='place_list_view'),
]
