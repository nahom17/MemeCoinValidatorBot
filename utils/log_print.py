import os
from datetime import datetime
import logging

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
LOG_FILE = os.path.join(LOG_DIR, 'terminal_output.log')

os.makedirs(LOG_DIR, exist_ok=True)

# Configure advanced logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def log_print(*args, level='info', **kwargs):
    message = ' '.join(str(arg) for arg in args)
    # Print to terminal (for backward compatibility)
    print(message, **kwargs)
    # Log to file and console with level
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'debug':
        logger.debug(message)
    else:
        logger.info(message)