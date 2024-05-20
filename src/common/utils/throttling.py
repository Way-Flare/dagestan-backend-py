import datetime

from django.conf import settings


def is_throttling(cache_data: dict, current_time: datetime) -> bool:
    if not cache_data:
        return False
    delta_time = current_time - cache_data['time']
    return delta_time.total_seconds() <= settings.CALL_TIMEOUT
