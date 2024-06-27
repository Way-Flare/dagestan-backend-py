import json
import uuid
from logging import getLogger
from typing import Optional
from uuid import UUID

import requests
from django.conf import settings
from pydantic import BaseModel, ValidationError

logger = getLogger("app")


class SmsException(Exception):
    _msg = 'Ошибка сервиса Sms'

    def __init__(self, message: Optional[str] = None, *args, **kwargs):
        self.message = message or self._msg


class SmsStatusException(SmsException):
    _msg = 'Неожиданный статус код сервиса Sms'


class SmsValidateError(SmsException):
    _msg = 'Неожиданное тело ответа сервиса Sms'


SMS_STATUS_CODE_ERROR_FACTORY = {
    0: 'IP адрес заблокирован',
    3: 'Неверный номер телефона',
    18: 'Достигнут лимит в 4 исходящих звонка в минуту или 30 вызовов в день для одного номера',
    19: 'Подождите 15 секунд перед повторной авторизации на тот же номер',
    429: 'Слишком много запросов в секунду',
    1001: 'Ваш аккаунт заблокирован',
}


def _parse_sms_result(
    response: requests.Response,
    success_schema: type[BaseModel],
) -> BaseModel:
    text = response.text
    if response.status_code != 200:
        raise SmsException(
            SMS_STATUS_CODE_ERROR_FACTORY.get(response.status_code),
        )
    try:
        return success_schema.model_validate(json.loads(text))
    except (ValidationError, ValueError) as e:
        logger.error(
            "SMS SERVICE: parse response error text - %s, status code - %s, exception - %s",
            text, response.status_code, repr(e),
        )
        raise SmsValidateError()


class InitCallSuccessSchema(BaseModel):
    status: str
    call_id: str
    code: int


class SmsService:

    def __init__(
        self,
        phone: str,
        host: str = settings.SMS_HOST,
        api_key: str = settings.SMS_API_KEY
    ):
        self.host = host
        self.api_key = api_key
        self.phone = phone

    @property
    def api_url(self) -> str:
        """Формирует api url."""
        return self.host

    def get_data(self) -> dict:
        data = dict(
            phone=self.phone,
            ip='-1',
            api_id=self.api_key
        )
        return data

    @property
    def api_call(self) -> str:
        return f'{self.api_url}/code/call'

    def init_call(self) -> Optional[BaseModel]:
        if settings.LOCAL_WORKING:
            return
        """
        Инициирует исходящий звонок.

        :param phone:
        :param code:
        :param client:
        :param unique:
        :param voice:
        :return:
        """
        url = self.api_call
        data = self.get_data()

        result = _parse_sms_result(
            requests.post(
                url=url,
                data=data,
            ),
            InitCallSuccessSchema,
        )
        return result
