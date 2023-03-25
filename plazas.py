from common import configuration
import grequests
import requests
from bs4 import BeautifulSoup
import re

CONF_FILE = 'conf.json'
MAIN_URL = configuration(CONF_FILE)['MAIN_URL']
GENERAL_URL = configuration(CONF_FILE)['GENERAL_URL']


def get_urls():
    """Find links to websites within a specific product category."""
    page = requests.get(MAIN_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    leafs = soup.find(class_="Left").find_all(class_="Leaf")
    categories = dict()
    for leaf in leafs:
        if len(leaf.find_all(class_="color2")) == 1:
            category = leaf.find(class_="color2").text.strip()
            subcategories = [(subcategory.text, GENERAL_URL+subcategory['href'])
                             for subcategory in leaf.find_all('a')[1:]]
            categories[category] = subcategories
    return categories


def grequests_parse_data(categories_urls):
    """Finds the name of every director (or directors) of each
     movie using multithreaded grequests and prints them."""
    for category in categories_urls.keys():
        for i in range(len(categories_urls[category])):
            subcategory = categories_urls[category][i][0]
            page = requests.get(categories_urls[category][i][1])
            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(class_="ContainerPager").find_all("a")
            subcategory_urls = [GENERAL_URL+product["href"] for product in products]
            request = (grequests.get(urls) for urls in subcategory_urls)
            products = grequests.map(request)
            for product in products:
                soup = BeautifulSoup(product.content, 'html.parser')
                product_elements = soup.find(class_="Products List").find_all(class_='Product')
                for product_element in product_elements:
                    product_name = product_element.find(class_='Description').text.strip()
                    if 'IVA' in product_element.find(class_='Price').text:
                        product_price = float(re.sub(r'[^\d.]+', '',
                                              product_element.find(class_='Price').text.split('IVA', 1)[1]))
                    else:
                        product_price = float(re.sub(r'[^\d.]+', '', product_element.find(class_='Price').text))
                    print(category, subcategory, product_name, product_price)


if __name__ == '__main__':
    cat = get_urls()
    grequests_parse_data(cat)
