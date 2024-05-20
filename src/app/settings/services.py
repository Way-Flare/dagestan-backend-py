import os
from .base import env_int

# UCALLER SERVICE
UCALLER_HOST = os.getenv('UCALLER_HOST', 'https://api.ucaller.ru')
UCALLER_SERVICE_ID = env_int('UCALLER_SERVICE_ID')
UCALLER_API_KEY = os.getenv('UCALLER_API_KEY', None)
