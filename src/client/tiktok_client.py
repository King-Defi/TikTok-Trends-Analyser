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

    def __enter__(self):
        """
        Called when entering a 'with' block.
        Example:
            with TikTokClient(logger, config) as client:
                # __enter__ is called here
                # self.start() runs automatically
        """

        # Start browser session
        self.start()
        # Return self so the client can be used in the with block
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when exiting a 'with' block, even if an error occurred.

        Args:
            exc_type: Type of exception that occurred (if any)
            exc_value: Exception instance that occurred (if any)
            traceback: Traceback of exception that occurred (if any)

        Example:
            with TikTokClient(logger, config) as client:
                # do stuff
                # __exit__ is called here, running cleanup automatically
        """

        # Logs if cleaning up after an error
        if exc_type is not None:
            self.logger.warning(
                f"Cleaning up after error: {exc_type.__name__}: {exc_value}"
            )

        self.cleanup()  # Clean up resources

    def start(self) -> None:
        """
        Start the browser session with basic configuration.
        Sets up browser, context, and page with proper error handling.
        """
        try:
            # Start a Playwright instance
            playwright = sync_playwright().start()

            # Launch a browser (Using Chrome/Chromium in this case)
            # headless=True means no visible browser window (runs in background)
            self.browser = playwright.chromium.launch(
                headless=self.config.get('headless', True)
            )

            # Creates a new browser context with specific viewport size
            # This will help make automation more consistent
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                # Sets a common user agent to mak requests look more natural
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            # Create a new page in the browser context
            self.page = self.context.new_page()

            # Log that browser has launched successfully
            self.logger.info("Browser launched successfully")

        except Exception as e:
            # Log any errors that occur during startup
            self.logger.error(f"Failed to start browser session: {str(e)}")

    def cleanup(self) -> None:
        """
        Clean up browser resources in reverse order of creation.
        Should be called when done with the client to free up system resources.
        """
        try:
            # Closes page if it exists
            if self.page:
                self.page.close()
                self.page = None

            # Closes context if it exists
            if self.context:
                self.context.close()
                self.context = None

            # Closes browser if it exists
            if self.browser:
                self.browser.close()
                self.browser = None

            self.logger.info("Browser resources cleaned up successfully")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

    def fetch_hashtag_page(self, tag: str) -> bool:
        """
        Navigate to a TikTok hashtag page.

        Args:
            tag: The hashtag to search for (without the # symbol)

        Returns:
            bool: True if navigation was successful, False otherwise
        """

        # Safety check
        if self.page is None:
            self.logger.error(
                "Browser not started. Use 'with' statement or call start() first")
            return False

        try:
            # Construct the hashtag URL - TikTok format is /tag/[hashtag]
            url = f"https://www.tiktok.com/tag/{tag}"

            # Navigate to the page
            self.page.goto(url)

            # Log success
            self.logger.info(f"Navigated to hashtag: #{tag}")

            # Basic check if we landed on the right page
            if tag.lower() in self.page.url.lower():
                return True
            else:
                self.logger.warning(
                    f"Landed on unexpected URL: {self.page.url}")
                return False

        except Exception as e:
            self.logger.error(f"Error navigating to #{tag}: {str(e)}")
            return False
