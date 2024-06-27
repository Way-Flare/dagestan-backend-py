import datetime
import logging

from django.core.cache import caches
from django.conf import settings
from app.celery import app
from services.sms import SmsService, SmsException
from services.ucaller import UCallerService, UCallerException

logger = logging.getLogger('authenticate.tasks.init_call_task')
cache = caches[settings.PHONES_CACHE_KEY]


@app.task
def init_call_task_ucaller(phone_number: str, code: int):
    for _ in range(3):
        try:
            UCallerService().init_call(phone=phone_number, code=code)
            break
        except UCallerException as e:
            logger.exception(e)


@app.task
def init_call_task_sms(phone_number: str):
    for _ in range(3):
        try:
            response = SmsService(phone_number).init_call()
            if response.status == 'OK':
                code = response.code
                current_time = datetime.datetime.now()
                cache_data = {'code': code, 'time': current_time, 'confirmed': False}
                redis_key = phone_number
                cache.set(redis_key, cache_data)
                logger.info(f'Совершил звонок на номер - {phone_number}, code - {code}')
                break
        except SmsException as e:
            logger.exception(e)
