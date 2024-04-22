import functools
import logging

from .formatter import uncapitalize

def log_and_handle_errors(action_desc: str) -> callable:
    """A decorator that logs the action being performed and handles any errors that occur.

    Args:
        action_desc (str): A description of the action being performed.

    Returns:
        callable: The decorated function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"{action_desc.capitalize()}.")
            try:
                result = func(*args, **kwargs)
                logging.info(f"{action_desc.capitalize()} was successful.")
                return result
            except Exception as e:
                logging.error(f"Error when {uncapitalize(action_desc)}: {e}")
                raise ValueError(f"Error when {uncapitalize(action_desc)}: {e}")
        return wrapper
    return decorator