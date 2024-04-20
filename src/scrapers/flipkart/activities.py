import os
import logging
from temporalio import activity
from selenium.webdriver.remote.webelement import WebElement  # for type hints
import pandas as pd

from selenium_helper.driver import Driver
from selenium_helper.elements_helper import ElementsHelper
from selenium_helper.elements_interactor import search_and_enter_text
from utils.transformer import get_texts_from_webelements
from utils.plotter import Plotter
from .shared import FLIPKART_URL, PRODUCT_TITLE_DIV_XPATH_LOCATOR, PRODUCT_PRICE_DIV_XPATH_LOCATOR

class _ActivitiesHelper:
    def __init__(self):
        self.driver = Driver('chrome', headless=False).get_driver()
        self.elements_helper = ElementsHelper(self.driver)
    
    def visit_url(self, url: str) -> None:
        self.driver.get(url)
        
    def search_for_products(self, name: str) -> None:
        logging.info(f'Searching for products with name: {name}')
        try:
            search_bar = self.elements_helper.get_element_by_locator("css_selector", "input[placeholder*='search' i]")
            search_and_enter_text(search_bar, name)
        except Exception as e:
            logging.error(f'Error searching for products: {e}')
            raise ValueError(f'Error searching for products: {e}')
        logging.info(f'Searching was successful.')
    
    def get_product_class_attributes(self, by_type: str, title_xpath_locator: str, price_xpath_locator: str) -> dict[str, str]:
        logging.info(f'Getting product class attributes.')
        try:
            title_class_name = self.elements_helper.get_element_by_locator(by_type, title_xpath_locator).get_attribute('class').strip().replace(' ', '.')
            price_class_name = self.elements_helper.get_element_by_locator(by_type, price_xpath_locator).get_attribute('class').strip().replace(' ', '.')
        except Exception as e:
            logging.error(f'Error getting product class attributes: {e}')
            raise ValueError(f'Error getting product class attributes: {e}')
        logging.info(f'Getting attributes were successful. title_class_name is {title_class_name}, and price_class_name is {price_class_name}.')
        return {"title": title_class_name, "price": price_class_name}

    def fetch_product_elements(self, by_type: str, title_css_locator: str, price_css_locator: str) -> tuple[list[WebElement], list[WebElement]]:
        logging.info(f'Fetching product elements.')
        try:
            title_divs = self.elements_helper.get_elements_by_locator(by_type, title_css_locator)
            price_divs = self.elements_helper.get_elements_by_locator(by_type, price_css_locator)
        except Exception as e:
            logging.error(f'Error fetching product elements: {e}')
            raise ValueError(f'Error fetching product elements: {e}')
        logging.info(f'Fetching product elements was successful.')
        return title_divs, price_divs
    
    def format_product_elements(self, title_divs: list[WebElement], price_divs: list[WebElement]) -> dict[str, list[str]]:
        logging.info(f'Formatting product elements.')
        try:
            titles: list[str] = get_texts_from_webelements(title_divs)
            unformatted_prices: list[str] = get_texts_from_webelements(price_divs)
            prices = [price.split('₹')[1].replace(',', '') for price in unformatted_prices]
            products = {title.strip(): price.strip()[1:] for title, price in zip(titles, prices)}
        except Exception as e:
            logging.error(f'Error formatting product elements: {e}')
            raise ValueError(f'Error formatting product elements: {e}')
        logging.info(f'Formatting product elements was successful.')
        return products
        
    def cleanup(self) -> None:
        logging.info(f'Cleaning up and closing driver.')
        self.driver.quit()
        
def _plot_products_data(products: dict[str, list[str]], title: str, x_label: str, y_label: str, folder_path: str) -> None:
    logging.info(f'Plotting products data.')
    try:
        plotter = Plotter(products, title, x_label, y_label, folder_path)
        plotter.line_graph()
        plotter.bar_plot()
        plotter.pie_chart()
    except Exception as e:
        logging.error(f'Error plotting products data: {e}')
        raise ValueError(f'Error plotting products data: {e}')
    logging.info(f'Plotting products data was successful.')

class FlipkartActivities:
    @activity.defn
    def fetch_from_flipkart_and_plot_data(self, product_data: dict[str, str]) -> None:
        product_name, product_type = product_data['name'], product_data['type']
        activities_helper = _ActivitiesHelper()
        try:
            activities_helper.visit_url(FLIPKART_URL)
            activities_helper.search_for_products('gionee')
            attribute_class_names = activities_helper.get_product_class_attributes('xpath', PRODUCT_TITLE_DIV_XPATH_LOCATOR, PRODUCT_PRICE_DIV_XPATH_LOCATOR)
            title_class_name = attribute_class_names['title']
            price_class_name = attribute_class_names['price']
            product_title_divs, product_price_divs = activities_helper.fetch_product_elements('class_name', title_class_name, price_class_name)
            products = activities_helper.format_product_elements(product_title_divs, product_price_divs)
            activities_helper.cleanup()
            
            title = f'FlipKart\'s {product_type.capitalize()} and Their Prices for Label \'{product_name}\''
            x_label = f'{product_name.capitalize()} {product_type.capitalize()}'
            y_label = 'Prices'
            folder_path = f'data/flipkart/{product_type}/{product_name}'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            _plot_products_data(products, title, x_label, y_label, folder_path)
        except Exception as e:
            logging.error(f'Error fetching and plotting data from flipkart: {e}')
            activities_helper.cleanup()
            raise ValueError(f'Error fetching and plotting data from flipkart: {e}')