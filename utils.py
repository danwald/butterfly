import logging
from typing import Optional


def setup_logger(name: str = "butterfly", debug: bool = False) -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: The name of the logger
        debug: Whether to enable debug logging level
    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    # Set log level based on debug flag
    log_level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(log_level)

    # If the logger doesn't have handlers, add one
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
