import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

URL = "https://www.target.com/s?searchTerm="
REQUEST_TIMEOUT = 5

async def scraping(soup):

    list_of_elements = soup.find_all(id="mainContainer")[0].contents[3].contents[0].contents[1].contents[1].contents[0].contents

    for element in list_of_elements:
        print(element)

async def main(query: list):
    async with async_playwright() as p:

        print('Lanzando el navegador.')
        # Launch the browser
        browser = await p.chromium.launch()
        print('Navegador lanzado.')

        # Open a new browser page
        page = await browser.new_page()
        print('GO TO -> ', URL + query[0].replace(' ', '+'))

        await page.goto( URL + query[0].replace(' ', '+'))
        
        content = await page.content()

        # Process extracted content with BeautifulSoup
        soup = BeautifulSoup(
            content,
            "html.parser"
        )

        print('SOUP -> ', soup)
        
        # Close browser
        await browser.close()

asyncio.run(main(query=['pato']))