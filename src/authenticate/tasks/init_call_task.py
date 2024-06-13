import logging


from app.celery import app
from services.ucaller import UCallerService, UCallerException

logger = logging.getLogger('authenticate.tasks.init_call_task')


@app.task
def init_call_task(phone_number: str, code: int):
    for _ in range(3):
        logger.info('Я тут')
        try:
            UCallerService().init_call(phone=phone_number, code=code)
            break
        except UCallerException as e:
            logger.exception(e)
