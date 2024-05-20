import json
import uuid
from logging import getLogger
from typing import Optional
from uuid import UUID

import requests
from django.conf import settings
from pydantic import BaseModel, ValidationError

logger = getLogger("app")


class UCallerException(Exception):
    _msg = 'Ошибка сервиса UCaller'

    def __init__(self, message: Optional[str] = None, *args, **kwargs):
        self.message = message or self._msg


class UCallerStatusException(UCallerException):
    _msg = 'Неожиданный статус код сервиса UCaller'


class UCallerValidateError(UCallerException):
    _msg = 'Неожиданное тело ответа сервиса UCaller'


UCALLER_STATUS_CODE_ERROR_FACTORY = {
    0: 'IP адрес заблокирован',
    3: 'Неверный номер телефона',
    18: 'Достигнут лимит в 4 исходящих звонка в минуту или 30 вызовов в день для одного номера',
    19: 'Подождите 15 секунд перед повторной авторизации на тот же номер',
    429: 'Слишком много запросов в секунду',
    1001: 'Ваш аккаунт заблокирован',
}


def _parse_ucaller_result(
    response: requests.Response,
    success_schema: type[BaseModel],
) -> BaseModel:
    text = response.text
    if response.status_code != 200:
        raise UCallerException(
            UCALLER_STATUS_CODE_ERROR_FACTORY.get(response.status_code),
        )
    try:
        return success_schema.model_validate(json.loads(text))
    except (ValidationError, ValueError) as e:
        logger.error(
            "UCALLER SERVICE: parse response error text - %s, status code - %s, exception - %s",
            text, response.status_code, repr(e),
        )
        raise UCallerValidateError()


class InitCallSuccessSchema(BaseModel):
    status: bool
    ucaller_id: int
    phone: str
    code: str
    unique_request_id: UUID


class UCallerService:

    def __init__(
        self,
        host: str = settings.UCALLER_HOST,
        service_id: int = settings.UCALLER_SERVICE_ID,
        api_key: str = settings.UCALLER_API_KEY,
    ):
        self.host = host
        self.service_id = service_id
        self.api_key = api_key

    @property
    def headers(self) -> dict:
        """Формирует заголовок для запроса."""
        return {'Authorization': f'Bearer {self.api_key}.{self.service_id}'}

    @property
    def api_url(self) -> str:
        """Формирует api url."""
        return f'{self.host}/v1.0'

    @property
    def api_call(self) -> str:
        return f'{self.host}/initCall'

    def init_call(
        self,
        phone: str,
        code: int,
        client: Optional[str] = None,
        unique: str = uuid.uuid4(),
        voice: bool = True,
    ) -> bool:
        if settings.DEBUG:
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
        data = dict(
            phone=phone,
            code=code,
            client=client,
            unique=unique,
            voice=voice,
        )
        result = _parse_ucaller_result(
            requests.post(
                url=url,
                data=data,
                headers=self.headers,
            ),
            InitCallSuccessSchema,
        )
        return result.status


