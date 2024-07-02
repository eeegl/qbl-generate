from functools import wraps
import logging

LOGGING_LEVEL = logging.INFO

def log_function(log_level=logging.DEBUG):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(log_level, f"Start {func.__name__}, args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.log(log_level, f"Done {func.__name__}")
            return result
        return wrapper
    return decorator

# Configure the logging
logging.basicConfig(level=LOGGING_LEVEL,
                    # datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
                    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)

# Log some messages
logger.info(f"Logger is up and running, level={logging.getLevelName(LOGGING_LEVEL)}")
