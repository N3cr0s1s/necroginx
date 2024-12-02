import sys
import os
sys.path.append(os.path.abspath('src'))
import logging
import src.launch
import src.constants

logging.basicConfig(
    filename=src.constants.LOG_PATH,
    level=src.constants.LOG_LEVEL,
    format=src.constants.LOG_FORMAT,
)

if __name__ == "__main__":
    src.launch.start()

