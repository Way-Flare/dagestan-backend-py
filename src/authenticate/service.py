import datetime
import random

from django.conf import settings
from django.core.cache import caches
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token

from authenticate.exceptions import ThrottlingException, UnconfirmedPhoneException, UserDoesNotExist, \
    InvalidAccountPassword, InvalidVerificationCodeException
from authenticate.tasks.init_call_task import init_call_task_ucaller, init_call_task_sms
from common import choices
from common.utils.throttling import is_throttling

from user.models import User


cache = caches[settings.PHONES_CACHE_KEY]


class UserAuthService:

    def login_by_phone(self, phone: str, password: str):
        user = User.objects.filter(phone=phone).first()
        if not user:
            raise UserDoesNotExist

        if not user.check_password(password):
            raise InvalidAccountPassword

        self.__login(user)
        return user

    def send_verification_code_to_phone(self, phone):
        current_time = datetime.datetime.now()
        cache_data = self.get_cache(phone)

        self.__is_throttling(cache_data, current_time)

        if settings.CHOICE_SERVICE_TO_CALL == choices.CHOICE_SERVICE_TO_CALL.UCALLER.value:
            code = self.__generate_verif_code()

            self.__set_cache_send_verif_code_phone(phone, code, current_time)
            self.__init_call_ucaller(phone, code)
        else:
            if settings.LOCAL_WORKING:
                code = self.__generate_verif_code()
                self.__set_cache_send_verif_code_phone(phone, code, current_time)

            self.__init_call_sms(phone)

    def confirm_phone_by_verification_code(self, phone, code):
        cache_data = self.get_cache(phone)
        if not cache_data or code != cache_data['code']:
            raise InvalidVerificationCodeException

        self.__set_cache_confirm_phone(phone)

    def check_confirmed_phone(self, phone):
        self.is_confirmed_phone(phone)
        self.delete_cache(phone)

    def is_confirmed_phone(self, phone):
        cache_data = self.get_cache(phone)
        if not cache_data.get('confirmed'):
            raise UnconfirmedPhoneException

    @staticmethod
    def get_tokens_for_user(user: User) -> dict[str, str]:
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @staticmethod
    def get_access_token(refresh_token: Token) -> dict[str, str] | bool:
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = refresh_token.access_token
            access_token.set_exp()
            access_token.set_iat()
            access_token.set_jti()
            return {
                'access': str(refresh_token.access_token)
            }
        except TokenError:
            return False

    def __set_cache_send_verif_code_phone(self, phone: str, code: int, current_time: datetime) -> None:
        cache_data = {'code': code, 'time': current_time, 'confirmed': False}
        self.set_cache(phone, cache_data)

    def __set_cache_confirm_phone(self, phone: str) -> None:
        cache_data = {'confirmed': True}
        self.set_cache(phone, cache_data)

    @staticmethod
    def __is_throttling(cache_data: dict, current_time: datetime) -> None:
        if is_throttling(cache_data, current_time):
            raise ThrottlingException

    @staticmethod
    def __generate_verif_code():
        code = random.randint(1000, 9999)
        if settings.LOCAL_WORKING:
            # В случае если производим тестирование системы
            code = 3636

        return code

    @staticmethod
    def __init_call_ucaller(phone, code):
        init_call_task_ucaller.delay(phone, code)

    @staticmethod
    def __init_call_sms(phone):
        init_call_task_sms.delay(phone)

    @staticmethod
    def get_cache(redis_key: str):
        cache_data = cache.get(redis_key)
        return cache_data

    @staticmethod
    def set_cache(redis_key: str, data: dict):
        cache.set(redis_key, data)

    @staticmethod
    def delete_cache(redis_key: str):
        cache.delete(redis_key)

    @staticmethod
    def __login(user: User):
        datetime_now = datetime.datetime.now()
        user.last_login = datetime_now
        user.save()
