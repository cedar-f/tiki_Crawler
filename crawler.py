from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.support.wait import WebDriverWait


class Crawler:
    base_Url = ''
    Url = ''
    chrome_option = Options()
    chrome_option.add_argument("--incognito")
    chrome_option.add_argument("--window-size=1920x1080")
    driver = ''

    def __init__(self, base_Url, begin_url):
        self.base_Url = base_Url
        self.Url = begin_url
        self.driver = webdriver.Chrome(chrome_options=self.chrome_option,
                                       executable_path='/home/cedar-f/data/chrome_selenium_driver/chromedriver_linux64/chromedriver')

    def get_link_to_product(self):
        page = urllib.request.urlopen(self.Url)
        soup = BeautifulSoup(page, 'html.parser')
        list_container = soup.find_all('div', class_="product-item")
        list_link = list()
        for container in list_container:
            list_link.append(self.base_Url + container.find('a').get('href'))
        return list_link

    def get_product_json(self, product_link):
        self.driver.get(product_link)

        html = self.driver.page_source
        product_json = self.get_product_info(html)

        wait = WebDriverWait(self.driver, 1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        review_html = self.driver.find_element_by_css_selector('div.customer-reviews')

        self.get_product_review(review_html)

        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next')))
        next_button.click()
        time.sleep(1000)

    def get_product_info(self, product_html):
        product = {}
        product["name"] = product_html.find("h1", class_="title").get_text()
        product["info"] = {}
        info_table = product_html.find("table").find("tbody").find_all("tr")
        for tr in info_table:
            product["info"][tr.find_all("td")[0].get_text()] = tr.find_all("td")[1].get_text()
        print(product)
        return product

    # def test(self):
    #     for link in self.get_link_to_product():
    #         self.get_product_info(self.get_product_html(link))
    def get_product_review(self, review_html):
        html = BeautifulSoup(review_html, 'html.parser')
        review = {}
