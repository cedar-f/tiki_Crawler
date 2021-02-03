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

    def __init__(self, base_Url, list_cat):
        self.base_Url = base_Url
        for link in list_cat:
            self.list_cat_link.append(self.base_Url + link)

        self.driver = webdriver.Chrome(chrome_options=self.chrome_option,
            executable_path='selenium_driver/chromedriver.exe')
        self.waiting_for_element = WebDriverWait(self.driver, 5)
        self.export = e()
        self.load_page(self.base_Url+'/Thịt%20-%20Hải%20sản%20-%20Trứng-c11707')
        time.sleep(10)

    def get_soup_page_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def load_page(self, url):
        self.driver.get(url)

    def get_product_json_to_mongo(self, cat_link):
        self.load_page(cat_link)
        time.sleep(2)
        while True:
            print("crawling at: " + cat_link)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(1)
            page_html=''
            page_html = self.get_soup_page_html(self.driver.page_source)
            list_div_product = page_html.find_all('div', class_='product-item')
            for div in list_div_product:
                try:
                    name = div.find('p', class_='product-name').get_text()
                    name = name.replace('\n', '').strip()
                    price = div.find('div', class_='product-price').find('span', class_='fs').get_text()
                    price = price.replace(' ', '').replace('\n', '').replace('đ', '')
                    print({'name': name, 'price': price})
                    self.save_to_mongo(name, price)
                except:
                    print('err')
            # list_div_product = []
            try:
                next_button = self.driver.find_elements_by_css_selector('button.v-pagination__navigation')[1]
                actions = ActionChains(self.driver)
                actions.move_to_element(next_button).perform()
                next_button.click()
                time.sleep(2)
            except Exception as err:
                print('err at click: '+str(err))
                break
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
        # page = self.get_page_html(self.Url)
        # while page:
        #     for link in self.get_link_to_product(page):
        #         try:
        #             self.get_product_json_to_mongo(link)
        #         except:
        #             pass
        #     link = self.get_link_to_next_page(page)
        #     page = self.get_page_html(link)
        for link in self.list_cat_link:
            self.get_product_json_to_mongo(link)
