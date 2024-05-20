from django.urls import path
from rest_framework.routers import SimpleRouter

from authenticate.api.views.common import TokenView
from authenticate.api.views.phone.login import AuthenticateUserView
from authenticate.api.views.phone.register import RegisterUserByPhoneView
from authenticate.api.views.phone.reset_password import ResetPasswordView


app_name = 'authenticate'

router = SimpleRouter(trailing_slash=False)

router.register('register/phone', RegisterUserByPhoneView, basename='register_user_by_phone')
router.register('reset-password/phone', ResetPasswordView, basename='reset_password_user_by_phone')

urlpatterns = router.urls + [
    path(r'login/phone/', AuthenticateUserView.as_view(), name='login_user_by_phone'),
    path(r'refresh-token/', TokenView.as_view(), name='refresh_token')
]
