import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logging(log_file: str = 'data/logs/xml_processor.log'):
    """Configura logging con rotación de archivos y formato detallado"""
    
    logger = logging.getLogger('xml_pipeline')
    logger.setLevel(logging.DEBUG)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para archivo (con rotación)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024*1024*5,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger