"""
Simple logger wrapper to centralize logging.
"""
import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def get_logger(name=__name__):
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    return logging.getLogger(name)