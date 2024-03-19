import logging
from logging.handlers import RotatingFileHandler
import os
from kognitive_src.utils.util import get_config

# Initialize logger
logger = logging.getLogger('mnist_predictor')
logger.setLevel(logging.INFO)
logger.propagate = False

# Define formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create console handler for output to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Log path can be read from an environment variable or hardcoded
#log_path = os.getenv('LOG_PATH', 'logs/mnist_predictor.log')

#log_path='D:/Sravan/assignments/Kognitive/MNIST/logs/fashion_mnist.log'

log_path=get_config('paths','logs_path')

# Check if the directory for logs exists, if not, create it
log_directory = os.path.dirname(log_path)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a file handler for output to file, with log rotation
file_handler = RotatingFileHandler(
    log_path,
    maxBytes=1024 * 1024 * 5,  # 5 MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Check if handlers are already added to avoid duplication
if not logger.handlers:
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
