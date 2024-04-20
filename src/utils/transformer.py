"""
A module that contains useful data type conversion and formatting.
"""

from selenium.webdriver.remote.webelement import WebElement

def get_texts_from_webelements(webelements: list[WebElement]) -> list[str]:
    """Extracts the text from a list of web elements.

    Args:
        webelements (list[WebElement]): A list of web elements.

    Returns:
        list[str]: A list of text extracted from the web elements.
    """
    return [element.text for element in webelements]
