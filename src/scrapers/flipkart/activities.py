import os
import logging
from temporalio import activity
from selenium.webdriver.remote.webelement import WebElement  # for type hints
import pandas as pd
import psycopg2
import re
import csv
from typing import Any
from dotenv import load_dotenv

from selenium_helper.driver import Driver
from selenium_helper.elements_helper import ElementsHelper
from selenium_helper.elements_interactor import search_and_enter_text
from utils.debug_helper import log_and_handle_errors
from utils.formatter import format_webelements_to_divs
from utils.currency import format_currency, convert_currency
from utils.sql_helper import get_or_create_id
from .config import FLIPKART_URL, PRODUCT_TITLE_DIV_XPATH_LOCATOR, PRODUCT_PRICE_DIV_XPATH_LOCATOR

class _FetchDataHelper:
    def __init__(self, headless: bool):
        self.driver = Driver('chrome', headless=headless).get_driver()
        self.elements_helper = ElementsHelper(self.driver)
    
    def visit_url(self, url: str) -> None:
        self.driver.get(url)
        
    @log_and_handle_errors('searching for products')
    def search_for_products(self, name: str) -> None:
        search_bar = self.elements_helper.get_element_by_locator("css_selector", "input[placeholder*='search' i]")
        search_and_enter_text(search_bar, name)
        
    @log_and_handle_errors('getting product class attributes')
    def get_product_class_attributes(self, by_type: str, title_xpath_locator: str, price_xpath_locator: str) -> dict[str, str]:
        autoconfig_path = 'scrapers/flipkart/autoconfig.txt'
        if os.path.isfile(autoconfig_path):
            with open(autoconfig_path, 'r') as f:
                lines = f.readlines()
                title_class_name, price_class_name = lines[0].strip(), lines[1].strip()
        else:
            title_class_name = self.elements_helper.get_element_by_locator(by_type, title_xpath_locator).get_attribute('class').strip().replace(' ', '.')
            price_class_name = self.elements_helper.get_element_by_locator(by_type, price_xpath_locator).get_attribute('class').strip().replace(' ', '.')
            with open(autoconfig_path, 'w') as f:
                f.write(f"{title_class_name}\n{price_class_name}")
        return {"title": title_class_name, "price": price_class_name}

    @log_and_handle_errors('fetching product elements')
    def fetch_product_elements(self, by_type: str, title_css_locator: str, price_css_locator: str) -> tuple[list[WebElement], list[WebElement]]:
        title_divs = self.elements_helper.get_elements_by_locator(by_type, title_css_locator)
        price_divs = self.elements_helper.get_elements_by_locator(by_type, price_css_locator)
        return title_divs, price_divs
    
    @log_and_handle_errors('formatting product elements')
    def format_product_elements(self, title_divs: list[WebElement], price_divs: list[WebElement]) -> dict[str, float]:
        titles: list[str] = [title.strip() for title in format_webelements_to_divs(title_divs)]
        unformatted_prices: list[str] = format_webelements_to_divs(price_divs)
        prices = [convert_currency(format_currency(price), 'INR', 'USD') for price in unformatted_prices]
        products = {title: price for title, price in zip(titles, prices)}
        return products

    @log_and_handle_errors('filtering products')
    def filter_products(self, products: dict[str, float], regex: str, case_insensitive: bool):
        regex_pattern = re.compile(regex, re.IGNORECASE if case_insensitive else 0)
        filtered_products = {product_name: price for product_name, price in products.items() if regex_pattern.search(product_name)}
        return filtered_products
    
    @log_and_handle_errors('writing to csv')
    def write_to_csv(self, product_type: str, products: dict[str, float], file_path: str) -> None:
        df = pd.DataFrame(products.items(), columns=['product_name', 'price_usd'])
        df['website_name'] = 'flipkart'
        df['product_type_name'] = product_type
        df['datetime'] = pd.Timestamp.now(tz='utc')
        df = df[['website_name', 'product_type_name', 'product_name', 'price_usd', 'datetime']]
        df.to_csv(file_path, index=False)
        
    def cleanup(self) -> None:
        logging.info(f"Closing driver.")
        self.driver.quit()
        
class _DatabaseHelper:
    def __init__(self, dbname, user, password, host) -> None:
        self.conn = self._setup_conn(dbname, user, password, host)
        self.cur = self.conn.cursor()
    
    @log_and_handle_errors('setting up database connection')
    def _setup_conn(self, dbname, user, password, host) -> None:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        return conn
    
    @log_and_handle_errors('setting up table')
    def setup_table(self, product_type: str) -> None:
        self.cur.execute(f"SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = %s);", (product_type,))
        exists = self.cur.fetchone()[0]
        if not exists:
            self.cur.execute(f"""
                CREATE TABLE {product_type} (
                    id SERIAL PRIMARY KEY,
                    website_id integer NOT NULL,
                    product_name character varying NOT NULL,
                    price_usd numeric NOT NULL,
                    datetime timestamp with time zone NOT NULL,
                    CONSTRAINT fk_website FOREIGN KEY (website_id) REFERENCES website(id)
                );
            """)
            self.conn.commit()
    
    @log_and_handle_errors('inserting data')
    def insert_data(self, product_type: str, csv_file_path: str) -> None:
        reader = csv.DictReader(open(csv_file_path))
        for row in reader:
            website_id = get_or_create_id(self.cur, self.conn, 'website', 'website_name', row['website_name'])
            self.cur.execute(
                f"INSERT INTO {product_type} (website_id, product_name, price_usd, datetime) VALUES (%s, %s, %s, %s)",
                (website_id, row['product_name'], row['price_usd'], row['datetime'])
            )
            self.conn.commit()
        
    def cleanup(self, csv_file_path: str) -> None:
        logging.info(f"Cleaning up database connection and removing csv file.")
        self.cur.close()
        self.conn.close()
        os.remove(csv_file_path)
        
class FlipkartActivities:
    @activity.defn
    def fetch_data_from_flipkart(self, search_instructions: dict[str, Any]) -> None:
        product_type, search_keyword = search_instructions['type'], search_instructions['search_keyword']
        product_filtering_regex, regex_case_insensitive = search_instructions['filtering_regex'], search_instructions['regex_case_insensitive']
        headless_mode = True
        data_folder_path = search_instructions['data_folder_path']
        activities_helper = _FetchDataHelper(headless_mode)
        try:
            activities_helper.visit_url(FLIPKART_URL)
            activities_helper.search_for_products(search_keyword)
            attribute_class_names = activities_helper.get_product_class_attributes('xpath', PRODUCT_TITLE_DIV_XPATH_LOCATOR, PRODUCT_PRICE_DIV_XPATH_LOCATOR)
            title_class_name = attribute_class_names['title']
            price_class_name = attribute_class_names['price']
            product_title_divs, product_price_divs = activities_helper.fetch_product_elements('class_name', title_class_name, price_class_name)
            products = activities_helper.format_product_elements(product_title_divs, product_price_divs)
            filtered_products = activities_helper.filter_products(products, product_filtering_regex, regex_case_insensitive)
            
            if not os.path.exists(data_folder_path):
                os.makedirs(data_folder_path)
            file_path = f"{data_folder_path}/{search_keyword}.csv"
            activities_helper.write_to_csv(product_type, filtered_products, file_path)
            activities_helper.cleanup()
        except Exception as e:
            logging.error(f"Error fetching data from flipkart: {e}")
            activities_helper.cleanup()
            raise ValueError(f"Error fetching data from flipkart: {e}")
        
    @activity.defn
    def submit_data_to_database(self, search_instructions: dict[str, Any]) -> None:
        load_dotenv()
        data_folder_path, search_keyword, product_type = search_instructions['data_folder_path'], search_instructions['search_keyword'], search_instructions['type']
        csv_file_path = f"{data_folder_path}/{search_keyword}.csv"
        try:
            database_helper = _DatabaseHelper(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'))
            database_helper.setup_table(product_type)
            database_helper.insert_data(product_type, csv_file_path)
            database_helper.cleanup(csv_file_path)
        except Exception as e:
            logging.error(f"Error fetching data from flipkart: {e}")
            database_helper.cleanup()
            raise ValueError(f"Error submitting data from flipkart into database: {e}")