import requests
import json

class ReebokParse:
    def __init__(self, url):
        self.prodList = []
        self.count = 0
        self.url = url
        self.headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }

        self.get_data(self.url)

    def get_data(self, url):

        s = requests.Session()
        res = s.get(url, headers=self.headers)
        self.data = res.json()
        self.collect_data()

    def collect_data(self):
        length = len(self.data["raw"]["itemList"]["items"])
        if length > 0:
            for self.prod in range(length):
                link = "https://www.reebok.com"
                price, salePrice = self.get_prices()
                title = self.data["raw"]["itemList"]["items"][self.prod]["displayName"]
                slug = self.data["raw"]["itemList"]["items"][self.prod]["link"]

                link = link + slug

                self.prodList.append({
                    "title": title,
                    "previous price": price,
                    "total price": salePrice,
                    "sale": str(round(((price - salePrice) / price) * 100)) + "%",
                    "link": link
                })
        self.count += 48
        if self.new_link(self.url):
            self.get_data(url = self.test_lnk)
        else:
            with open("reebok_results.json", "w", encoding="utf-8") as file:
                json.dump(self.prodList, file, indent=4, ensure_ascii=False)
            self.prodList.clear()

    def get_prices(self):
        id = self.data["raw"]["itemList"]["items"][self.prod]["productId"]
        sess = requests.Session()
        price_info = sess.get("https://www.reebok.com/api/search/product/" + id + "?sitePath=us", headers=self.headers)
        price_data = price_info.json()

        price = price_data["price"]
        salePrice = price_data["salePrice"]

        return price, salePrice

    def new_link(self, url):
        ses = requests.session()
        self.test_lnk = f"{url}" + "&start=" + str(self.count)
        try:
            self.check = ses.get(self.test_lnk, headers=self.headers)
            data = self.check.json()
            length = len(data["raw"]["itemList"]["items"])
            if length > 0:
                return True
            else:
                return False
        except:
            return False





