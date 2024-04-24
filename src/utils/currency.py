import re
import os
import json
import requests
import logging
from datetime import datetime, timezone
from dateutil import parser

CURRENCY_EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"

def format_currency(currency: str) -> float:
    """Cleans and converts a currency string to a float.

    Args:
        currency (str): A string representing a currency amount.

    Returns:
        float: The currency amount as a float.
    """
    currency_symbols = re.escape('$€£¥₹₽₩฿₪₫₴₸₲₺₼₦₱₵₡₮₳₥៛₭₤₳₸')
    formatted_currency = re.sub(f'[{currency_symbols},]', '', currency).strip()
    currency = float(formatted_currency)
    return currency

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Converts an amount from one currency to another.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.

    Returns:
        float: The converted amount.
    """
    _update_currency_rates()
    file_path = 'utils/currency_rates.json'
    with open(file_path, 'r') as file:
        rates = json.load(file)
    if from_currency not in rates['rates'] or to_currency not in rates['rates']:
        raise Exception("Invalid currency code.")
    from_currency_rate = rates['rates'][from_currency]
    to_currency_rate = rates['rates'][to_currency]
    converted_currency = amount * to_currency_rate / from_currency_rate
    converted_currency = round(converted_currency, 2)
    return converted_currency

def _update_currency_rates() -> None:
    if not os.path.exists('utils'):
        os.makedirs('utils')
    file_path = 'utils/currency_rates.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        current_date = datetime.now(timezone.utc) 
        next_update_date = parser.parse(data['time_next_update_utc'])
        if current_date <= next_update_date:
            return
    response = requests.get(CURRENCY_EXCHANGE_API_URL)
    if response.status_code == 200:
        data = response.json()
        with open(file_path, 'w') as file:
            json.dump(data, file)
        logging.info("utils/currency.py - Currency rates updated and saved.")
    else:
        logging.error(f"utils/currency.py - Failed to fetch currency rates. Status code: {response.status_code}")
        raise Exception("Failed to fetch or update currency rates.")