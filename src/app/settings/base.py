import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def env_int(name: str, value: Optional[int] = None):
    """Преобразует env переменную в int"""
    res = os.getenv(name)
    if not res:
        return value
    if res.isdigit():
        return int(res)
    return value


def env_list(name: str, value: list, separator: str = ','):
    """Преобразует env переменную в список разделителем 'separator'"""
    res = os.getenv(name)
    if not res:
        return value
    return res.split(separator)


def env_bool(name: str, value: bool):
    """Преобразует env переменную в boolean."""
    res = os.getenv(name)
    if not res:
        return value
    if res.lower() in {'true', '1'}:
        return True
    return False


AUTH_USER_MODEL = "user.User"

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
APP_DIR = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = APP_DIR / "src"
BASE_DIR = SRC_DIR / "app"
LOG_DIR = SRC_DIR / "logs"
TEST_DIR = APP_DIR / "tests"
TEST_STATIC_FILES_FIR = TEST_DIR / "files"


SECRET_KEY = os.getenv('SECRET_KEY', 'DEBUG_KEY')


DEBUG = env_bool('DJANGO_DEBUG', True)


LOCAL_WORKING = env_bool('DJANGO_LOCAL_WORKING', False)


ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', ['*'])
CSRF_TRUSTED_ORIGINS = env_list('DJANGO_ALLOWED_CSRF', ['https://localhost:8000', ])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',

    'user',
    'place',
    'route',
    'authenticate'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATIC_ROOT = APP_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = APP_DIR / 'media'

APP_MEDIA_PATH = 'app/{}/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = env_int('REDIS_PORT', 6379)

REDIS_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}'\
    if REDIS_HOST else 'redis://127.0.0.1:6379'

CALL_TIMEOUT = env_int('CALL_TIMEOUT', 30)


if LOCAL_WORKING:
    INSTALLED_APPS += ['silk']
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
