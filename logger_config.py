import logging

LOG_FILE = 'app.log'
ERROR_FILE = 'stderr.log'

# Configura o logger principal
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.FileHandler(ERROR_FILE),
        logging.StreamHandler()
    ]
)
