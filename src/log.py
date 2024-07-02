from functools import wraps
import logging

LOGGING_LEVEL = logging.DEBUG

def log_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Start {func.__name__}, args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"Done {func.__name__}")
        return result
    return wrapper

def log_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Start {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Done {func.__name__}")
        return result
    return wrapper

# Configure the logging
logging.basicConfig(level=LOGGING_LEVEL,
                    # datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
                    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)

# Log some messages
logger.info(f"Logger is up and running, level={logging.getLevelName(LOGGING_LEVEL)}")
