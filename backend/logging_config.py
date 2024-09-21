# /backend/logging_config.py

import logging
import logging.config
import os

# Define the logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'filename': os.path.join('logs', 'app.log'),
            'mode': 'a',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        '__main__': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'services': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'routes': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
    },
}

def configure_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.config.dictConfig(LOGGING_CONFIG)
