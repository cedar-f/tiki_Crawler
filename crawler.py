from bs4 import BeautifulSoup
# import urllib.request
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from export_to_mongo import Export as e
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class Crawler:
    base_Url = ''
    chrome_option = Options()
    chrome_option.add_argument("--incognito")
    chrome_option.add_argument("--window-size=1920x1080")
    driver = ''
    waiting_for_element = ''
    export = ''
    list_cat_link = []

    def __init__(self, base_Url):
        self.base_Url = base_Url
        self.driver = webdriver.Chrome(chrome_options=self.chrome_option,
            executable_path='selenium_driver/chromedriver.exe')
        self.waiting_for_element = WebDriverWait(self.driver, 5)
        self.export = e()

    def get_soup_page_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def load_page(self, url):
        self.driver.get(url)

    def get_product_json_to_mongo(self, url):
        self.load_page(url)
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 2*document.body.scrollHeight/3);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        html = self.get_soup_page_html(self.driver.page_source)
        item_lis = html.find_all('li', class_='item')
        for li in item_lis:
            name = li.find('h3').get_text()
            price = li.find('div', class_='price').find('strong').get_text()
            name = name.replace('\n', '').strip()
            price = price.replace(' ', '').replace('\n', '').replace('₫', '')
            print({'name': name, 'price': price})
            try:
                self.save_to_mongo(name, price)
            except Exception as err:
                print('err at save: ' + str(err))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # vv
    # print("crawling at: " + product_link)
    # self.driver.get(product_link)
    #
    # html = self.driver.page_source
    # time.sleep(0.5)
    #
    # for x in range(0, 20):
    #     try:
    #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         self.waiting_for_element.until(
    #             EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.customer-reviews')))
    #
    #         review_html = self.driver.find_element_by_css_selector("div.customer-reviews").get_attribute(
    #             'innerHTML')
    #
    #         self.get_product_review_and_save_to_mongo(review_html)
    #         try:
    #             while True:
    #                 next_button = self.waiting_for_element.until(
    #                     EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next')))
    #                 for i in range(0, 3):
    #                     try:
    #                         next_button.click()
    #                         time.sleep(1)
    #                         review_html = self.driver.find_element_by_css_selector(
    #                             "div.customer-reviews").get_attribute(
    #                             'innerHTML')
    #                         self.get_product_review_and_save_to_mongo(review_html)
    #                         break
    #                     except Exception as err:
    #                         print("###ERR AT 3th TRY: " + str(err))
    #                         if i > 0:
    #                             print("====>try to get review: " + str(i))
    #         except Exception as err:
    #             print('END OF PRODUCT')
    #             break
    #     except Exception as err:
    #         ActionChains(self.driver).move_to_element(
    #             self.driver.find_element_by_css_selector('div.input-group')).perform()
    #         print("###ERR AT 1st TRY: " + str(err))
    #         print('try to load page: ' + str(x))
    #     print("err at: " + product_link)

    def save_to_mongo(self, name, price):
        product = {'name': name, 'price': price}
        self.export.one_to_mongo(product)

    def run(self):
        self.get_product_json_to_mongo(self.base_Url)
