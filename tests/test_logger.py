# test_logger.py (can be in your tests directory)
from src.utils.logger import setup_logger
import logging
import os
from pathlib import Path


def test_logger():
    # Create loggers with different levels
    debug_logger = setup_logger("TestDebug", logging.DEBUG)
    info_logger = setup_logger("TestInfo", logging.INFO)

    # Test messages
    debug_logger.debug("This is a debug message")
    debug_logger.info("This is an info message")
    debug_logger.warning("This is a warning message")

    info_logger.debug("This debug message shouldn't appear")
    info_logger.info("This info message should appear")
    info_logger.warning("This warning message should appear")

    # Verify log files were created
    log_dir = Path("logs")
    assert log_dir.exists(), "Log directory wasn't created"
    assert (log_dir / "testdebug_logger.log").exists(), "Debug log file wasn't created"
    assert (log_dir / "testinfo_logger.log").exists(), "Info log file wasn't created"


if __name__ == "__main__":
    test_logger()
    print("Check the logs directory for output files!")
    print("And you should see some messages above in the console!")
