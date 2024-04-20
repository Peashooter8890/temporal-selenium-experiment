import logging
from selenium.webdriver.remote.webdriver import WebDriver # for type hints
from selenium.webdriver.remote.webelement import WebElement # for type hints
from .elements_locator import ElementLocator

class ElementsHelper:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        
    def get_element_by_locator(self, by_type: str, locator: str) -> WebElement:
        """Fetches an element on a webpage with a specified locator.

        Args:
            by_type (str): The type of locator to use, corresponding to Selenium's By attributes. Refer to https://www.selenium.dev/documentation/webdriver/elements/locators/ for more information.
            locator (str): The locator string, e.g., an XPATH or CSS selector, depending on by_type.

        Raises:
            ValueError: If no element with the specified locator was found on the webpage.

        Returns:
            WebElement: The located element.
        """
        try:
            element: WebElement = ElementLocator(self.driver).fetch_element_after_wait(by_type, locator)
        except Exception:
            raise
        return element
    
    def get_elements_by_locator(self, by_type: str, locator: str) -> list[WebElement]:
        """Fetches all elements on a webpage with a specified locator.

        Args:
            by_type (str): The type of locator to use, corresponding to Selenium's By attributes. Refer to https://www.selenium.dev/documentation/webdriver/elements/locators/ for more information.
            locator (str): The locator string, e.g., an XPATH or CSS selector, depending on by_type.

        Raises:
            ValueError: If no elements with the specified locator were found on the webpage.

        Returns:
            list[WebElement]: A list of elements with the specified locator.
        """
        try:
            elements: list[WebElement] = ElementLocator(self.driver).fetch_all_elements_after_wait(by_type, locator)
        except Exception:
            raise
        return elements