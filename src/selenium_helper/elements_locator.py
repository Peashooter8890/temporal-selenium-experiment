import logging
from selenium.webdriver.remote.webdriver import WebDriver # for type hints
from selenium.webdriver.remote.webelement import WebElement # for type hints
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ElementLocator:
    """A class that provides methods to locate elements on a webpage."""
    def __init__(self, driver: WebDriver):
        """Initializes the ElementLocator class.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver
        self.BY_TYPES = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'tag_name': By.TAG_NAME,
            'class_name': By.CLASS_NAME,
            'css_selector': By.CSS_SELECTOR
        }
        
    def fetch_element_after_wait(self, by_type: str, locator: str, maximum_wait_seconds: int = 10) -> WebElement | None:
        """Fetches an element on the webpage after waiting for a certain amount of time.
        
        Args:
            by_type (str): The type of locator to use, corresponding to Selenium's By attributes. Refer to https://www.selenium.dev/documentation/webdriver/elements/locators/ for more information.
            locator (str): The locator string, e.g., an XPATH or CSS selector, depending on by_type.
            maximum_wait_seconds (int, optional): The maximum wait time in seconds. Defaults to 10.

        Raises:
            ValueError: If by_type is not a valid locator type.

        Returns:
            WebElement | None: The located element, or None if the element could not be found.
        """
        if not self.BY_TYPES.get(by_type):
            error_msg = f"{by_type} is not a valid locator type."
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        by = self.BY_TYPES[by_type]
        try:
            return WebDriverWait(self.driver, maximum_wait_seconds).until(
                EC.presence_of_element_located((by, locator))
            )
        except TimeoutException as e:
            logging.error(f"Timeout while waiting for element with locator {locator} using {by_type}: {e}")
            raise ValueError(f"Timeout while waiting for element with locator {locator} using {by_type}: {e}")
        except NoSuchElementException as e:
            logging.error(f"Element with locator {locator} using {by_type} not found: {e}")
            raise ValueError(f"Element with locator {locator} using {by_type} not found: {e}")
        except Exception as e:
            logging.error(f"Unexpected error when trying to locate element with locator {locator} using {by_type}: {e}")
            raise ValueError(f"Unexpected error when trying to locate element with locator {locator} using {by_type}: {e}")
        
    def fetch_all_elements_after_wait(self, by_type: str, locator: str, maximum_wait_seconds: int = 10) -> list[WebElement] | None:
        """Fetches all elements on the webpage after waiting for a certain amount of time.
        
        Args:
            by_type (str): The type of locator to use, corresponding to Selenium's By attributes. Refer to https://www.selenium.dev/documentation/webdriver/elements/locators/ for more information.
            locator (str): The locator string, e.g., an XPATH or CSS selector, depending on by_type.
            maximum_wait_seconds (int, optional): The maximum wait time in seconds. Defaults to 10.

        Raises:
            ValueError: If by_type is not a valid locator type.

        Returns:
            list[WebElement] | None: A list of the located elements, or None if no element was found.
        """
        if not self.BY_TYPES.get(by_type):
            error_msg = f"{by_type} is not a valid locator type."
            logging.error(error_msg)
            raise ValueError(error_msg)

        by = self.BY_TYPES[by_type]
        try:
            return WebDriverWait(self.driver, maximum_wait_seconds).until(
                EC.presence_of_all_elements_located((by, locator))
            )
        except TimeoutException as e:
            logging.error(f"Timeout while waiting for elements with locator {locator} using {by_type}: {e}")
            raise ValueError(f"Timeout while waiting for elements with locator {locator} using {by_type}: {e}")
        except NoSuchElementException as e:
            logging.error(f"No elements found with locator {locator} using {by_type}: {e}")
            raise ValueError(f"No elements found with locator {locator} using {by_type}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error when trying to locate elements with locator {locator} using {by_type}: {e}")
            raise ValueError(f"Unexpected error when trying to locate elements with locator {locator} using {by_type}: {e}")
        