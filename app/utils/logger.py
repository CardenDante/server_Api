# app/utils/logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logger():
    logger = logging.getLogger('server_management')
    logger.setLevel(logging.INFO)

    # File Handler
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()