from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumCraigslistScraper(object):

    def __init__(self, item, category, location, postal, max_price, radius):
        self.category = category
        self.location = location
        self.postal = postal
        self.max_price = max_price
        self.radius = radius
        self.item = item.replace(" ", "+")

        self.url = f"https://{location}.craigslist.org" \
            f"/search/{category}" \
            f"?sort=date" \
            f"&query={self.item}" \
            f"&search_distance={radius}" \
            f"&postal={postal}" \
            f"&max_price={max_price}"

        self.driver = webdriver.Chrome()
        self.delay = 5
        self.posts = []
        self.results_dict = dict()

    # selenium
    def load_craigslist_url(self):
        try:
            self.driver.get(self.url)
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(
                       EC.presence_of_element_located(
                           (By.ID, "searchform")))
            self.set_posts()
            self.extract_results_data()
        except TimeoutException:
            print('Loading took too long')
        except NoSuchElementException:
            print('Couldn\'t find an element D:')
        except Exception:
            print('Catch all :(')

    # selenium
    def set_posts(self):
        self.posts = (self.driver.find_elements_by_class_name("result-row"))

    def extract_results_data(self):
        for post in self.posts:
            # get date
            post_date = post.find_element_by_tag_name("time").get_attribute("datetime")
            # get price
            price = post.find_element_by_class_name("result-price").text
            # get title
            post_title = post.find_element_by_class_name("result-title").text
            # get url
            post_url = post.find_element_by_class_name("result-title").get_attribute("href")
            self.results_dict[post_title + " - " + post_date.split(" ")[0]] = {
                'posted': post_date,
                'price': price,
                'url': post_url
            }

    def list_results(self):
        for k,v in self.results_dict.items():
            print(k)
            print(v)

    def close_driver(self):
        if self.driver:
            print('quiting driver')
            self.driver.quit()
        else:
            print('not quitting D:')


category = "cta"
location = "austin"
postal = "78759"
max_price = "30000"
radius = "25"
item = "ford f150"
scraper = SeleniumCraigslistScraper(item, category, location, postal, max_price, radius)
scraper.load_craigslist_url()
scraper.close_driver()
scraper.list_results()
