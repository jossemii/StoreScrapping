from pyvirtualdisplay import Display
from time import sleep
import requests
from seleniumwire import webdriver
import threading

URL = "https://www.target.com/s?searchTerm="


def scrape(query: str, output:list, lock: threading.Lock, proxy: str):

    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = webdriver.Firefox(
        seleniumwire_options={
            'proxy': {'https': proxy} if proxy[:5]=='https' else {'http': proxy}
        }
    ) if proxy else webdriver.Firefox()
    driver.get(URL + query.replace(' ', '+'))

    try:
        while len(driver.requests)<20: sleep(1) # wait for load the web scripts.

        for request in driver.requests:
            if request.response and 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1' in request.url \
                and request.method == 'GET' and request.response.status_code == 200:
                data = requests.get(request.url).json()
                break

        o = []
        for element in data['data']['search']['products']:
            currency = element['price']['formatted_current_price'][0]
            item = element['item']

            o.append({
                'url': item['enrichment']['buy_url'],
                'title': item['product_description']['title'],
                'image_url': item['enrichment']['images']['primary_image_url'],
                'price': {
                    'amount': element['price']['current_retail'],
                    'currency': 'USD' if currency == '$' or  currency == 'S' else currency
                }
            })

    except Exception as e:
        raise Exception('Exception '+str(e)+' scraping '+query)

    driver.quit()
    display.stop()
    
    lock.acquire()
    try:
        output+=o
    finally:
        lock.release()

def main(elements: list, proxy = None):
    threads = []
    output = []

    lock = threading.Lock()
    for query in elements:
        process = threading.Thread(
            target=scrape, 
            args=[ query, output, lock, proxy]
        )
        process.start()
        threads.append(process)
    
    for process in threads:
        process.join()

    return output
    