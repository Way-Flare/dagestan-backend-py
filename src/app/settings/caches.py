import os

from app.settings import REDIS_URI

DB_REDIS_CACHE = os.getenv('DB_REDIS_CACHE', '0')
REDIS_URI_CACHE = f'{REDIS_URI}/{DB_REDIS_CACHE}'

_REDIS_CACHE_OPTIONS = {
    'SOCKET_CONNECT_TIMEOUT': 5,
    'SOCKET_TIMEOUT': 5,
    'CONNECTION_POOL_KWARGS': {
        'max_connections': 10000,
        'retry_on_timeout': True,
    }
}

PHONES_CACHE_KEY = os.getenv('PHONES_CACHE_KEY') or 'phones'
THROTTLING_CACHE_KEY = os.getenv('THROTTLING_CACHE_KEY') or 'throttling'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URI_CACHE,
        'KEY_PREFIX': 'default',
        'TIMEOUT': 60 * 60 * 4,
        'OPTIONS': _REDIS_CACHE_OPTIONS,
    },
    PHONES_CACHE_KEY: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URI_CACHE,
        'KEY_PREFIX': PHONES_CACHE_KEY,
        'OPTIONS': _REDIS_CACHE_OPTIONS,
    },
    THROTTLING_CACHE_KEY: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URI_CACHE,
        'KEY_PREFIX': THROTTLING_CACHE_KEY,
        'OPTIONS': _REDIS_CACHE_OPTIONS,
    },
}