import os
from time import perf_counter
import logging
import pandas as pd
from ..driver import Driver 

def benchmark_driver_speed(browsers, website_urls):
    results = {browser: {} for browser in browsers}
    for browser in browsers:
        logging.info(f"Starting benchmark for {browser}...")
        driver = Driver(browser=browser).get_driver()
        timings = []
        for url in website_urls:
            logging.info(f"Running benchmark for {url} on {browser}...")
            start_time = perf_counter()
            driver.get(url)
            elapsed_time = perf_counter() - start_time
            timings.append(elapsed_time) # this is so we can later calculate the average time
            website_title = url.split('www.')[1].split('.')[0]
            results[browser][website_title] = elapsed_time
        results[browser]['average'] = sum(timings) / len(timings)
        driver.quit()
    return results

def main():
    logging.basicConfig(level=logging.INFO)
    browsers = ['chrome', 'firefox', 'edge']
    website_urls = [
        'https://www.youtube.com',
        'https://www.facebook.com',
        'https://www.reddit.com',
        'https://www.netflix.com',
        'https://www.wikipedia.org',
        'https://www.amazon.com',
        'https://www.pinterest.com',
        'https://www.twitch.tv',
        'https://www.spotify.com',
        'https://www.nbcnews.com',
    ]
    
    results = benchmark_driver_speed(browsers, website_urls)
    folder_path = 'selenium_helper/benchmarks/data' # assumes that the script is run from the src directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    for browser in browsers:
        df = pd.DataFrame([results[browser]])
        df = df.round(3)
        # make first column show the average values
        avg_col = df.pop('average') 
        df.insert(0, 'average', avg_col)
        
        file_path = f'{folder_path}/{browser}_benchmark_results.csv'
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', index=False, header=False)
        else:
            df.to_csv(file_path, index=False)
    
if __name__ == '__main__':
    main()