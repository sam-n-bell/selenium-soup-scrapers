from bs4 import BeautifulSoup
import urllib.request


class SoupCraigslistScraper(object):

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

    # urllib
    def extract_page_html(self):
        page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(page, "lxml") #using lxml requires pip install lxml
        postings = dict()
        results = soup.find_all('li', {'class': 'result-row'})
        for post in results:
            # get posted date
            date = post.find('time', {'class': 'result-date'})
            # get price
            price = post.find('span', {'class': 'result-price'}).getText()
            # get title of post and the url of it
            title_tag = post.find('a', {'class': 'result-title'})
            title = title_tag.getText()
            url = title_tag['href']
            postings[title + ' - ' + date.getText()] = {
                'posted': date['datetime'].split(" ")[0],
                'price': price,
                'url': url
            }
        for k, v in postings.items():
            print(k)
            print(v)

category = "cta"
location = "austin"
postal = "78759"
max_price = "30000"
radius = "25"
item = "ford f150"
scraper = SoupCraigslistScraper(item, category, location, postal, max_price, radius)
scraper.extract_page_html()
