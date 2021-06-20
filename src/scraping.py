from pyvirtualdisplay import Display
from time import sleep
import requests
from seleniumwire import webdriver
import threading

URL = "https://www.target.com/s?searchTerm="


def scrape(query: str, output:list, lock: threading.Lock):

    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = webdriver.Firefox()
    driver.get(URL + query.replace(' ', '+'))

    # Access requests via the `requests` attribute
    try:
        for request in driver.requests:
            if request.response and 'https://redsky.target.com/redsky_aggregations' in request.url \
                and request.method == 'GET' and request.response.status_code == 200:
                data = requests.get(request.url).json()
                break

        o = []
        for element in data['data']['search']['products']:
            o.append({
                'url': element['item']['enrichment']['buy_url'],
                'title': element['item']['product_description']['title'],
                'image_url': element['item']['enrichment']['images']['primary_image_url'],
                'price': {
                    'amount': element['price']['current_retail'],
                    'currency': 'USD' if element['price']['formatted_current_price'][0] == '$' else 'CURRENCY_NOT_REGISTERED'
                }
            })

    except Exception as e:
        raise Exception('Exception '+str(e)+' scraping '+query)

    driver.quit()
    display.stop()
    
    lock.acquire()
    try:
        output.append(o)
    finally:
        lock.release()

def main(elements: list):
    threads = []
    output = []

    lock = threading.Lock()
    for query in elements:
        process = threading.Thread(
            target=scrape, 
            args=[ query, output, lock]
        )
        process.start()
        threads.append(process)
    
    for process in threads:
        process.join()

    return output
    