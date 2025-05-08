import os
import logging
import datetime


def initialize_logger():
    log_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(os.path.curdir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, f"log_{log_date}.txt")
    try:
        logging.basicConfig(
            filename=log_filepath,
            filemode="a",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )
        logging.info(
            f"Logger initialized at location - {os.path.abspath(log_filepath)}"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize logger: {e}")


def log_message(message, level="info"):
    """
    Logs a message at the specified level.
    :param message: The message to log.
    :param level: The logging level ('info', 'warning', 'error', 'debug', 'critical').
    """
    if not isinstance(message, str):
        raise ValueError("Message must be a string.")
    if not isinstance(level, str):
        raise ValueError("Level must be a string.")
    if not message:
        raise ValueError("Message cannot be empty.")
    if not level:
        raise ValueError("Level cannot be empty.")
    if not logging.getLogger().hasHandlers():
        raise RuntimeError("Logger not initialized. Call initialize_logger() first.")

    assert level in ["info", "warning", "error", "debug", "critical"], (
        "Invalid logging level."
    )

    logger = logging.getLogger()
    level = level.lower()
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)
