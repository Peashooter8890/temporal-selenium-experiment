"""
A module that contains useful data type conversion and formatting.
"""

from selenium.webdriver.remote.webelement import WebElement

def format_webelements_to_divs(webelements: list[WebElement]) -> list[str]:
    """Extracts the text from a list of web elements.

    Args:
        webelements (list[WebElement]): A list of web elements.

    Returns:
        list[str]: A list of text extracted from the web elements.
    """
    return [element.text for element in webelements]

def uncapitalize(text: str) -> str:
    """Converts the first letter of a string to lowercase.

    Args:
        text (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return text[0].lower() + text[1:]