# coding=utf-8
# Copyright 2013 Janusz Skonieczny
import logging

SILENT_MODULES = ("api_server", )
SILENT_FUNCS = ("views.get_file",)


class ModuleFilter(logging.Filter):

    def filter(self, record):
        # return True to allow
        if record.levelno > 10: # logging.DEBUG
            return True
        if record.module in SILENT_MODULES:
            return False
        return not (record.module + "." + record.funcName) in SILENT_FUNCS


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'custom': {
            # 'format': '%(asctime)s %(levelname)-7s %(module)s %(filename)s:%(lineno)s | %(funcName)s | %(message)s',
            'format': '%(asctime)s %(levelname)-7s %(filename)s:%(lineno)s | %(funcName)s | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'silent_modules': {
            '()': ModuleFilter
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'custom',
            'filters': ['silent_modules'],
        },
    },
    'loggers': {
        'sqlalchemy.engine': {
            'level': 'INFO',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }

}


def setup_logging():
    # logging.disable(logging.NOTSET)
    # logging.getLogger().setLevel(logging.DEBUG)
    from logging.config import dictConfig
    dictConfig(LOGGING)
    logging.info("Logging setup changed")
