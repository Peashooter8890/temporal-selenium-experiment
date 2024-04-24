TASK_QUEUE_NAME = "flipkart"
WORKFLOW_ID = "flipkart-workflow"
FLIPKART_URL = "https://www.flipkart.com/"
PRODUCT_TITLE_DIV_XPATH_LOCATOR = '/html/body/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/a[1]/div[2]/div[1]/div[1]'
PRODUCT_PRICE_DIV_XPATH_LOCATOR = '/html/body/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/a[1]/div[2]/div[2]/div[1]/div[1]/div[1]'
SEARCH_INSTRUCTIONS = [
    {
        'type': 'smartphone',
        'search_keyword': 'gionee smartphone', # make sure that gionee is always first. Gionee is what the program uses to get css class names based on xpath. Each product may have a different xpath locator, so unless gionee is set to be the first search keyword, the program will not be able to get the correct css class names.
        'filtering_regex': r".*GIONEE.*\([^)]*\)",
        'regex_case_insensitive': False,
        'data_folder_path': 'scrapers/flipkart/data',
    },
    {
        'type': 'smartphone',
        'search_keyword': 'samsung smartphone',
        'filtering_regex': r".*SAMSUNG.*\([^)]*\)",
        'regex_case_insensitive': False,
        'data_folder_path': 'scrapers/flipkart/data',
    },
    {
        'type': 'smartphone',
        'search_keyword': 'apple iphone',
        'filtering_regex': r".*Apple iPhone.*\([^)]*\)",
        'regex_case_insensitive': False,
        'data_folder_path': 'scrapers/flipkart/data',
    }
]