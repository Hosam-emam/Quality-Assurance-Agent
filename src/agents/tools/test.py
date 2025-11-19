from src.configs.log_config import setup_logger

logger = setup_logger(logger_name=__name__, level='debug')

def log():
    logger.info("Logging something in test")