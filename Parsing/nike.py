import requests
import json


class NikeParse:
    def __init__(self):
        self.prodList = []
        self.headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }
    def get_data(self, url):
        s = requests.Session()
        res = s.get(url, headers=self.headers)
        self.data = res.json()
        self.collect_data()
    def collect_data(self):

        next_pg = self.data["pages"]["next"]
        length = len(self.data["objects"])

        for prod in range(length):
            link = "https://www.nike.com/t/"
            price = self.data["objects"][prod]["productInfo"][0]["merchPrice"]["fullPrice"]
            salePrice  = self.data["objects"][prod]["productInfo"][0]["merchPrice"]["currentPrice"]
            title = self.data["objects"][prod]["productInfo"][0]["productContent"]["title"]
            slug = self.data["objects"][prod]["productInfo"][0]["productContent"]["slug"]
            styleColor = self.data["objects"][prod]["productInfo"][0]["merchProduct"]["styleColor"]

            link = link + slug + "/" + styleColor

            self.prodList.append({
                "title" : title,
                "previous price" : price,
                "total price" : salePrice,
                "sale" : str(round(((price - salePrice)/price) * 100)) + "%",
                "link" : link
            })
        if len(next_pg) != 0:
            self.get_data(url="https://api.nike.com" + next_pg)
        else:
            with open("nike_result.json", "w", encoding="utf-8") as file:
                json.dump(self.prodList, file, indent=4, ensure_ascii=False)
            self.prodList.clear()

parserNike = NikeParse()

