# Imported libraries
import logging


# Setting up logger with both file and console output
def setup_logger(name: str = 'MemeTracker'):
    """
    Configure logging to both file and console with detailed formatting.
    Args:
        name: Logger name, defaults to 'MemeTracker'
    Returns:
        logging.Logger: Configured logger instance
    """
    # Creates a formatter with detailed information
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(funcNamee)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Sets up file handler
    file_handler = logging.FileHandler('meme_tracker.log')
    file_handler.setFormatter(formatter)

    # Sets up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Gets the logger
    logger = logging.getLogger('MemeTracker')
    logger.setLevel(logging.DEBUG)

    # Prevents duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
