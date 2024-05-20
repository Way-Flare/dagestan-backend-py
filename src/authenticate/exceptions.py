class ThrottlingException(Exception):
    message: str = 'Много запросов.'


class InvalidVerificationCodeException(Exception):
    message: str = 'Невалидный код верификации.'


class UnconfirmedPhoneException(Exception):
    message: str = 'Не подтвержденный номер телефона.'


class AuthorizedUserException(Exception):
    message: str = 'Ошибка авторизации пользователя.'


class UserDoesNotExist(AuthorizedUserException):
    message: str = 'Пользователя с текущими данными не существует.'


class InvalidAccountPassword(AuthorizedUserException):
    message: str = 'Не правильный пароль пользователя.'
