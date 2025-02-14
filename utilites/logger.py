import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import logging
import sys, os


class PrintToLogger:
    def __init__(self, level):
        self.level = level
        self.logger = logging.getLogger()

    def write(self, message):
        # Avoid logging empty messages (like from print() without args)
        if message.strip():
            self.logger.log(self.level, message.strip())

    def flush(self):
        # Required for compatibility with sys.stdout
        pass



def logger(path : str | None = 'logs'):
    os.makedirs(path, exist_ok=True)

    now = datetime.now()
    file = f"{now.day}-{now.month}-{now.year}.log"
    logging.basicConfig(
        level=logging.INFO,  # Set your desired log level
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler(f"{path}/{file}")]
            )
    
    sys.stdout = PrintToLogger(logging.INFO)
