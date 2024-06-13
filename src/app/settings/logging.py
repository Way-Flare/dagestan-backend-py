from app.settings import LOG_DIR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': (
                '{levelname} - {asctime} - {name} - {filename} - {funcName} - {lineno} - {message}\n'
            ),
            'style': '{'
        }
    },
    'handlers': {
        'main_app': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'std_format',
            "filename": LOG_DIR / 'main_app.logs'
        },
        'init_call_task': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'std_format',
            "filename": LOG_DIR / 'init_call.logs'
        }
    },
    'loggers': {
        'main_app_logger': {
            'level': 'WARNING',
            'handlers': ['main_app']
        },
        'authenticate.tasks.init_call_task': {
            'level': 'INFO',
            'handlers': ['init_call_task'],
        }
    }
}
