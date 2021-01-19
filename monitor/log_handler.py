#!/usr/bin/env python3

import logging
from logging import handlers
import sys


def setup_logger(level):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    handler = handlers.RotatingFileHandler('logs/app.log',
                                           maxBytes=1e+8,
                                           backupCount=1)
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


if __name__ == '__main__':
    pass
