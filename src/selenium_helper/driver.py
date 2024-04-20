from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver  # for type hints
import logging

class Driver:
    def __init__(self, browser: str, headless: bool = True):
        """_summary_

        Args:
            browser (str): A string representing the browser to use. Supported browsers are 'chrome', 'firefox', 'edge', and 'safari'.
            headless (bool, optional): A bool specifying if the driver should be headless. Defaults to True.
        """
        self.browser = browser
        self.headless = headless

    def get_driver(self) -> WebDriver:
        """Returns a Selenium WebDriver instance for the requested browser.

        Raises:
            ValueError: If the browser is not supported.

        Returns:
            WebDriver: The Selenium WebDriver instance for the requested browser.
        """
        if self.browser == 'chrome':
            return self._get_chrome_driver()
        elif self.browser == 'firefox':
            return self._get_firefox_driver()
        elif self.browser == 'edge':
            return self._get_edge_driver()
        elif self.browser == 'safari':
            return self._get_safari_driver()
        else:
            raise ValueError(f'Unsupported browser: {self.browser}')

    def test_driver(self) -> bool:
        """Tests if the driver is working by opening the selenium website and fetching the title.

        Returns:
            bool: True if the driver is working, False otherwise.
        """
        driver = self.get_driver()
        try:
            driver.get('https://www.selenium.dev')
            if not driver.title:
                return False
            logging.info(f'Driver test successful: {self.browser}')
            return True
        except Exception:
            logging.error(f'Error testing driver: {self.browser}')
            return False
        finally:
            driver.quit()

    def _get_chrome_driver(self) -> WebDriver:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True) # without this, selenium will close the browser after the test (happened on a single macOS)
        if self.headless:
            options.add_argument('--headless=new')
        return webdriver.Chrome(options=options)

    def _get_firefox_driver(self) -> WebDriver:
        return webdriver.Firefox()

    def _get_safari_driver(self) -> WebDriver:
        return webdriver.Safari()

    def _get_edge_driver(self) -> WebDriver:
        return webdriver.Edge()
