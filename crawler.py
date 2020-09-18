from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from export_to_mongo import Export as e
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class Crawler:
    base_Url = ''
    Url = ''
    chrome_option = Options()
    chrome_option.add_argument("--incognito")
    chrome_option.add_argument("--window-size=1920x1080")
    driver = ''
    waiting_for_element = ''
    export = ''

    def __init__(self, base_Url, begin_url):
        self.base_Url = base_Url
        self.Url = begin_url
        self.driver = webdriver.Chrome(chrome_options=self.chrome_option,
                                       executable_path='/home/cedar-f/data/chrome_selenium_driver/chromedriver_linux64/chromedriver')
        self.waiting_for_element = WebDriverWait(self.driver, 5)
        self.export = e()

    def get_page_html(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_link_to_next_page(self, soup):
        next_page_link = self.base_Url + soup.find('a', class_='next').get('href')
        return next_page_link

    def get_link_to_product(self, soup):
        list_container = soup.find_all('div', class_="product-item")
        list_link = list()
        for container in list_container:
            list_link.append(self.base_Url + container.find('a').get('href'))
        return list_link

    def get_product_json_and_save_to_mongo(self, product_link):
        print("crawling at: " + product_link)
        self.driver.get(product_link)

        html = self.driver.page_source
        time.sleep(0.5)
        product_json = self.get_product_info(html)
        for x in range(0, 20):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6 *5);")
                self.waiting_for_element.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.customer-reviews')))
                self.expand_review()

                review_html = self.driver.find_element_by_css_selector("div.customer-reviews").get_attribute(
                    'innerHTML')

                reviews = self.get_product_review(review_html)
                try:
                    while True:
                        next_button = self.waiting_for_element.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next')))
                        for i in range(0, 3):
                            try:
                                next_button.click()
                                time.sleep(1)
                                self.expand_review()
                                review_html = self.driver.find_element_by_css_selector(
                                    "div.customer-reviews").get_attribute(
                                    'innerHTML')
                                reviews += (self.get_product_review(review_html))
                                break
                            except Exception as err:
                                print("###ERR AT 3th TRY: " + str(err))
                                if i > 0:
                                    print("====>try to get review: " + str(i))
                except Exception as err:
                    product_json['reviews'] = reviews
                    print(product_json)
                    self.export.to_mongo(product_json)
                    print('END OF PRODUCT')
                    break
            except Exception as err:
                ActionChains(self.driver).move_to_element(
                    self.driver.find_element_by_css_selector('div.input-group')).perform()
                print("###ERR AT 1st TRY: " + str(err))
                print('try to load page: ' + str(x))
            print("err at: " + product_link)

    def expand_review(self):
        expand_review_buttons = self.driver.find_elements_by_css_selector('div.review-comment__count')

        for button in expand_review_buttons:
            button.click()
            time.sleep(0.2)

    def get_product_info(self, product_html):
        product = {}
        html = BeautifulSoup(product_html, "html.parser")
        product["name"] = html.find("h1", class_="title").get_text()
        product["info"] = {}
        info_table = html.find("table").find("tbody").find_all("tr")
        for tr in info_table:
            product["info"][tr.find_all("td")[0].get_text()] = tr.find_all("td")[1].get_text()
        return product

    def get_product_review(self, review_html):
        html = BeautifulSoup(review_html, 'html.parser')
        reviews = []
        review_container = html.find_all("div", class_="review-comment")
        for r in review_container:
            star = len(r.find_all("i", class_="icomoon-star")) - len(r.find_all("i", class_="disable"))
            conversations = []

            main_review = {r.find('span', class_='review-comment__avatar-name').get_text(): r.find('div',
                                                                                                   class_='review-comment__content').get_text()}
            conversations.append(main_review)
            sub_conversations = r.find_all('div', class_='review-sub-comment')
            for sub_c in sub_conversations:
                sub_review = {sub_c.find('div', class_='review-sub-comment__avatar-name').get_text(): sub_c.find('div',
                                                                                                                 class_='review-sub-comment__content').get_text()}
                conversations.append(sub_review)
            review = {'rate': star, 'conversations': conversations}
            reviews.append(review)
        return reviews

    def run(self):
        page = self.get_page_html(self.Url)
        while page:
            for link in self.get_link_to_product(page):
                try:
                    self.get_product_json_and_save_to_mongo(link)
                except:
                    pass
            link = self.get_link_to_next_page(page)
            page = self.get_page_html(link)
