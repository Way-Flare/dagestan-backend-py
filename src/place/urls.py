from django.urls import path

from place.views import PlaceListView, PlaceRetrieveView, SubscribeUnsubscribeToPlaceView, FeedbackPlaceView

app_name = 'places'

urlpatterns = [
    path(r'all/', PlaceListView.as_view(), name='place_list_view'),
    path(r'<int:pk>/subscribe/', SubscribeUnsubscribeToPlaceView.as_view(), name='subscribe_unsubscribe_to_place'),
    path(r'<int:pk>/feedbacks/', FeedbackPlaceView.as_view(), name='feedback_to_place'),
    path(r'<int:pk>/', PlaceRetrieveView.as_view(), name='place_retrieve_view')
]
