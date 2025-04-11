"""
poop
"""
import logging
from colorlog import ColoredFormatter


def setup_logging():
    """
    poop
    """
    log_format = "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s"
    formatter = ColoredFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Create a logger and set the level
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # You can adjust this to INFO or ERROR depending on your needs
    logger.addHandler(console_handler)

    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")
