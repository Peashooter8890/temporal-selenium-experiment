from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver  # for type hints
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import logging

class Driver:
    def __init__(self, browser: str = 'chrome', headless: bool = True):
        """Initializes the Driver instance with the requested browser and headless mode. Does not support OS-specific browsers like Safari or Internet Explorer.

        Args:
            browser (str): A string representing the browser to use. Supported browsers are 'chrome', 'firefox', and 'edge'. Defaults to 'chrome'.
            headless (bool, optional): A bool specifying if the driver should be headless. Defaults to True.
        """
        self.browser = browser.lower()
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
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")
        
    def install_drivers(self) -> bool:
        """Installs the required drivers for the supported browsers.

        Returns:
            bool: True if the drivers were installed successfully, False otherwise.
        """
        try:
            ChromeDriverManager().install()
            GeckoDriverManager().install()
            EdgeChromiumDriverManager().install()
        except Exception as e:
            logging.error(f"Error installing drivers: {e}")
            return False
        return True
    
    def _get_chrome_driver(self) -> WebDriver:
        options = ChromeOptions()
        options.add_experimental_option('detach', True)  # without this, selenium might close the browser after the test
        if self.headless:
            options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    def _get_firefox_driver(self) -> WebDriver:
        options = FirefoxOptions()
        if self.headless:
            options.add_argument('--headless')
        return webdriver.Firefox(options=options)

    def _get_edge_driver(self) -> WebDriver:
        options = EdgeOptions()
        if self.headless:
            options.add_argument('--headless')
        return webdriver.Edge(options=options)
    