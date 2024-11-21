# Imported libraries
import logging
from pathlib import Path
from typing import Optional


# Setting up logger with both file and console output
def setup_logger(
    name: str = 'MemeTracker',
    log_level: int = logging.DEBUG,
    log_dir: str = 'logs'
) -> logging.Logger:
    """
    Configure logging to both file and console with detailed formatting.

    Args:
        name (str): Logger name, defaults to 'MemeTracker'
        log_level (int): Logging level, defaults to DEBUG
        log_dir (str): Directory to store log files, defaults to 'logs'

    Returns:
        logging.Logger: Configured logger instance that writes to both file 
        and console with timestamp and context information
    """

    # Create logs directory if it does not exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Creates a formatter with detailed information
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set up file handler with daily rotating logs
    file_handler = logging.FileHandler(
        log_path / f'{name.lower()}_{Path(__file__).stem}.log'
    )
    file_handler.setFormatter(formatter)

    # Sets up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Gets the logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevents duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Log the initialisation
    logger.debug(
        f"Logger '{name}' initialised with level {logging.getLevelName(log_level)}"
    )

    return logger
