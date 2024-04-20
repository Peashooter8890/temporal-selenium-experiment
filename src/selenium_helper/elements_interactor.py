"""Functions for interacting with selenium webelements.
"""
from selenium.webdriver.remote.webelement import WebElement # for type hints
from selenium.webdriver.common.keys import Keys

def search_and_enter_text(element: WebElement, text: str) -> None:
    """Searches for the given text in the webelement's text field and presses Enter.

    Args:
        element (WebElement): The webelement to search in.
        text (str): The text to search for.
    """
    element.send_keys(text)
    element.send_keys(Keys.RETURN)