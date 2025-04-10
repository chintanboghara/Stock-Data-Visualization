"""
Configuration and initialization for the application.
"""
import os
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Logger configuration
LOG_FILE = LOGS_DIR / "app.log"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# App configuration
APP_CONFIG = {
    "app_name": "Stock Data Visualization",
    "app_icon": "📈",
    "cache_duration": 3600,  # Cache duration in seconds
    "max_stocks_in_comparison": 5,
    "default_stock": "AAPL",
    "default_period": "1y",
}

def setup_logging() -> None:
    """Set up logging for the application."""
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Set the root logger level
    root_logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, 
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Set specific levels for some loggers to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    
    # Log startup information
    root_logger.info(f"Logging initialized at level {LOG_LEVEL}")

def get_config() -> Dict[str, Any]:
    """
    Get application configuration.
    
    Returns:
        Dict[str, Any]: Application configuration
    """
    return APP_CONFIG