# Library Imports
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

# Local Imports
import config


def setup_logging(env):
    # Set logging
    if env == 'dev':
        log_level = logging.INFO
    elif env == 'prod':
        log_level = logging.WARNING

    # Set ROOT logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)  # Needed to override default 'WARNING' level

    # Create module level logger and handlers
    c_handler = logging.StreamHandler()
    log_name = f'{config.LOG_PATH}/{env}/syslog_{datetime.datetime.now().strftime("%Y-%m-%d")}'
    f_handler = TimedRotatingFileHandler(log_name, when='midnight', interval=1, encoding='utf-8')
    f_handler.suffix = f'syslog_{datetime.datetime.now().strftime("%Y-%m-%d")}.log'  # TODO : fix bad date suffixes

    # Set Logging Levels
    c_handler.setLevel(log_level)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add to handlers
    c_format = logging.Formatter('|%(name)s| %(levelname)s | %(message)s')
    f_format = logging.Formatter('%(asctime)s |%(name)s| %(levelname)s | %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the ROOT logger
    root_logger.addHandler(c_handler)
    root_logger.addHandler(f_handler)
