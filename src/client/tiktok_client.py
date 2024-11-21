from playwright.sync_api import sync_playwright
from typing import Dict


# Setting up class
class TikTokClient:
    def __init__(self, logger, config: Dict) -> None:
        """
        Initialize TikTok client with logging and configuration.

        Args: 
            logger: Logger instance from utils/logger.py that we'll use for tracking what our client is doing and 
                    any errors that occur

            config: Dictionary containing settings like whether to run headless, 
                    rate limits, etc.
        """
        # Store the logger instance so it can be used throughout the class
        self.logger = logger

        # Store the cofiguration dictionary for later us
        self.config = config

        # Browser attributes to be properly initialised later, set to `None` for now.
        # Will hold browser instance
        self.browser = None
        # Will hold browser context (like an incognito window)
        self.context = None
        # Will hold the actual page we're interacting with
        self.page = None

        # Log that we've initialized the client
        self.logger.info("TikTok client initialized")

    def start(self) -> None:
        """
        Start the browser session with basic configuration.
        Returns None but sets up self.browser, self.context, and self.page
        """
        try:
            # Start a Playwright instance
            playwright = sync_playwright().start()

            # Launch a browser (Chrome/Chromium in this case)
            # headless=True means no visible browser window (runs in background)
            self.browser = playwright.chromium.launch(
                headless=self.config.get('headless', True)
            )

            # Log that browser has launched successfully
            self.logger.info("Browser launched successfully")

        except Exception as e:
            # Log any errors that occur during startup
            self.logger.error(f"Failed to start browser session: {str(e)}")
