"""
Utililty functions for xpath locators.
"""
def lowercase(text) -> str:
    """
    Returns an XPATH locator string that converts the given text to lowercase.
    
    Example usage: f"//input[contains({lowercase('@placeholder')}, 'search')]"
    """
    return f"translate({text}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvw')"