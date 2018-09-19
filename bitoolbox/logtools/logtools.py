# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(logger_name=None,
               log_filename='debug.log',
               file_level=logging.DEBUG,
               folder='logs',
               stream_level=logging.DEBUG,
               setLevel=logging.DEBUG,
               ):
    import os
    logger = None
    logger = logging.getLogger(logger_name)
    logger.setLevel(setLevel)

    # create file handler which logs even debug messages
    fh = TimedRotatingFileHandler(os.path.join('.', folder, log_filename),
                                  when='D',
                                  interval=1,
                                  encoding='UTF-8')
    fh.setLevel(file_level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(stream_level)
    # create formatter and add it to the handlers
    if(logger_name is None):
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    # if logger.handlers:
    #     logger.handlers = []
    
    map(logger.removeHandler, logger.handlers[:])
    map(logger.removeFilter, logger.filters[:])

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
