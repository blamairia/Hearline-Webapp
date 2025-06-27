"""
Logging configuration for Heartline Desktop Application
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..core.config import Config, config

def setup_logging():
    """Setup application logging with both file and console handlers"""
    
    # Ensure logs directory exists
    Config.LOGS_DIR.mkdir(exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # File handler with rotation
    log_file = Config.get_log_path()
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    # Console handler for development
    if config.DEBUG:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
    
    # Set levels for specific loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    
    logging.info("Logging system initialized")
