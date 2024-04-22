import os
import logging
from temporalio import activity
from selenium.webdriver.remote.webelement import WebElement  # for type hints
import pandas as pd

from selenium_helper.driver import Driver
from selenium_helper.elements_helper import ElementsHelper
from selenium_helper.elements_interactor import search_and_enter_text
from utils.debug_helper import log_and_handle_errors
from utils.formatter import format_webelements_to_divs
from utils.plotter import Plotter
from .shared import FLIPKART_URL, PRODUCT_TITLE_DIV_XPATH_LOCATOR, PRODUCT_PRICE_DIV_XPATH_LOCATOR

class _ActivitiesHelper:
    def __init__(self):
        self.driver = Driver('chrome', headless=False).get_driver()
        self.elements_helper = ElementsHelper(self.driver)
    
    def visit_url(self, url: str) -> None:
        self.driver.get(url)
        
    @log_and_handle_errors('searching for products')
    def search_for_products(self, name: str) -> None:
        search_bar = self.elements_helper.get_element_by_locator("css_selector", "input[placeholder*='search' i]")
        search_and_enter_text(search_bar, name)
        
    @log_and_handle_errors('getting product class attributes')
    def get_product_class_attributes(self, by_type: str, title_xpath_locator: str, price_xpath_locator: str) -> dict[str, str]:
        title_class_name = self.elements_helper.get_element_by_locator(by_type, title_xpath_locator).get_attribute('class').strip().replace(' ', '.')
        price_class_name = self.elements_helper.get_element_by_locator(by_type, price_xpath_locator).get_attribute('class').strip().replace(' ', '.')
        return {"title": title_class_name, "price": price_class_name}

    @log_and_handle_errors('fetching product elements')
    def fetch_product_elements(self, by_type: str, title_css_locator: str, price_css_locator: str) -> tuple[list[WebElement], list[WebElement]]:
        title_divs = self.elements_helper.get_elements_by_locator(by_type, title_css_locator)
        price_divs = self.elements_helper.get_elements_by_locator(by_type, price_css_locator)
        return title_divs, price_divs
    
    @log_and_handle_errors('formatting product elements')
    def format_product_elements(self, title_divs: list[WebElement], price_divs: list[WebElement]) -> dict[str, list[str]]:
        titles: list[str] = format_webelements_to_divs(title_divs)
        unformatted_prices: list[str] = format_webelements_to_divs(price_divs)
        prices = [price.split('₹')[1].replace(',', '') for price in unformatted_prices]
        products = {title.strip(): price.strip()[1:] for title, price in zip(titles, prices)}
        return products
    
    def write_to_csv(self, products: dict[str, list[str]], folder_path: str) -> None:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        df = pd.DataFrame(products.items(), columns=['Product', 'Price'])
        df.to_csv(f'{folder_path}/products.csv', index=False)
        
    def cleanup(self) -> None:
        logging.info(f'Cleaning up and closing driver.')
        self.driver.quit()
        

class FlipkartActivities:
    @activity.defn
    def fetch_data_from_flipkart(self, product_data: dict[str, str]) -> None:
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
            
            folder_path = f'data/flipkart/{product_type}/{product_name}'
            activities_helper.write_to_csv(products, folder_path)
            
            activities_helper.cleanup()
            
        except Exception as e:
            logging.error(f'Error fetching and plotting data from flipkart: {e}')
            activities_helper.cleanup()
            raise ValueError(f'Error fetching and plotting data from flipkart: {e}')
        
        @activity.defn
        def submit_data_to_database(self, data: dict[str, str]) -> None:
            pass