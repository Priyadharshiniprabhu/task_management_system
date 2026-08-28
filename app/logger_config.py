import logging
import os

from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger("task_manager")

logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    filename=f"{LOG_DIR}/app.log",
    maxBytes=1024 * 1024,   # 1 MB
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
