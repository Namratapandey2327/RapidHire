from playwright.sync_api import sync_playwright

class PlaywrightScraper:
    """Browser automation helper for SourceSync."""

    def __init__(self, headless: bool = True):
        self.headless = headless

    def launch(self):
        """Launch a Playwright browser session."""
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self.page

    def close(self):
        """Close the browser session."""
        if hasattr(self, "browser"):
            self.browser.close()
        if hasattr(self, "_playwright"):
            self._playwright.stop()
