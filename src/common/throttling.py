from django.conf import settings
from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle


class AuthAnonRateThrottle(AnonRateThrottle):
    cache = caches[settings.THROTTLING_CACHE_KEY]
    scope = '5/minute'
