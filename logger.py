"""
Logging configuration for the Offline AI Assistant
"""
import logging
import os
from datetime import datetime

# Global logger instance
_logger_instance = None

def setup_logger(name="OfflineAI", level=logging.INFO):
    """Setup and return a logger with proper configuration"""
    global _logger_instance
    
    # Return existing logger if already configured
    if _logger_instance is not None:
        return _logger_instance
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Prevent propagation to root logger (prevents duplicates)
    logger.propagate = False
    
    # Clear any existing handlers to prevent duplicates
    logger.handlers.clear()
    
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    log_filename = f"{log_dir}/offline_ai_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Console handler - only add if not already present
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    _logger_instance = logger
    return logger

# Create a global logger instance
logger = setup_logger()
