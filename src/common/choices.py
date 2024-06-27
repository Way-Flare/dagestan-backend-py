import enum


class CHOICE_SERVICE_TO_CALL(str, enum.Enum):
    UCALLER = 'ucaller'
    SMS = 'sms'
