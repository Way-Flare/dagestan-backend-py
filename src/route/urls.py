from django.urls import path

from route.views import RouteListView, RouteRetrieveView, FeedbackRouteView

app_name = 'routes'

urlpatterns = [
    path(r'all/', RouteListView.as_view(), name='route_list_view'),
    path(r'<int:pk>/feedback/', FeedbackRouteView.as_view(), name='feedback_to_route'),
    path(r'<int:pk>/', RouteRetrieveView.as_view(), name='route_retrieve_view'),
]
