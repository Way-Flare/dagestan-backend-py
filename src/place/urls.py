from django.urls import path

from place.views import PlaceListView, PlaceRetrieveView

app_name = 'place'

urlpatterns = [
    path(r'all', PlaceListView.as_view(), name='place_list_view'),
    path(r'<int:pk>/', PlaceRetrieveView.as_view(), name='place_retrieve_view')
]
