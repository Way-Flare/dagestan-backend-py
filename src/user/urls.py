from django.urls import path

from user.views import UserProfileApiView

app_name = 'users'

urlpatterns = [
    path(r'', UserProfileApiView.as_view(), name='get_update_my_profile'),
]
