from django.urls import path

from route.views import RouteListView

app_name = 'route'

urlpatterns = [
    path(r'all', RouteListView.as_view(), name='route_list_view')
    ]
