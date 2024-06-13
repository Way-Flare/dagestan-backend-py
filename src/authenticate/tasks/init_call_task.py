import logging


from app.celery import app
from services.ucaller import UCallerService, UCallerException

logger = logging.getLogger('init_call_task_logger')


@app.task
def init_call_task(phone_number: str, code: int):
    for _ in range(3):
        try:
            UCallerService().init_call(phone=phone_number, code=code)
            break
        except UCallerException as e:
            logger.exception(e)
