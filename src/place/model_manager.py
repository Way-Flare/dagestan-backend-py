from django.db import models


class CustomPlaceManager(models.Manager):
    def all_active(self):
        return self.get_queryset().filter(is_visible=True)
