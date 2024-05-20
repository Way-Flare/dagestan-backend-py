from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError("The given phone must be set")

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone, password, **extra_fields)
