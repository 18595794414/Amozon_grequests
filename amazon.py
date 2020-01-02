import grequests
from lxml import etree
import time

host = 'https://www.amazon.co.uk'

header = {
    'sec-fetch-mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}

class GetAmazonSeller():
    def download(self, urls, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',}):
        time.sleep(0.2)
        # response = requests.get(url, headers=headers, timeout=30)
        # if response.status_code == 200:
        #
        #     print('请求成功')
        #     return response
        req = (grequests.get(url, headers=headers, timeout=20) for url in urls)
        responses = grequests.map(req, size=4)
        if responses != []:

            print('成功请求')
            return responses

    def parse_category1(self, url):
        response = self.download(url)[0]
        tree = etree.HTML(response.text)
        urls = tree.xpath('//td//a/@href')
        real_url = [host + url for url in urls]

        category2_responses = self.download(real_url)

        for response in category2_responses:
            print('进入分类二')
            self.parse_category2(response)

    def parse_category2(self, response):
        if response != None:
            tree = etree.HTML(response.text)
            seller_list = tree.xpath('//span[@class="a-list-item"]//span[contains(text(), "See more")]/../@href')
            if seller_list != []:
                seller_list_url = [host + url for url in seller_list]
                seller_list_responses = self.download(seller_list_url, headers=header)
                for response in seller_list_responses:
                    print('进入商铺分类')
                    self.parse_shop_catgory(response)

            if tree.xpath('//li[@class="s-ref-indent-neg-micro"]'):
                url = tree.xpath('//li[@class="s-ref-indent-neg-micro"]//a/@href')
                # print(url)
                if url != None:
                    real_url = [host + u for u in url]
                    category3_responses = self.download(real_url)
                    for response in category3_responses:
                        print('进入分类三')
                        self.parse_category3(response)

    def parse_category3(self, response):
        if response != None:
            tree = etree.HTML(response.text)
            urls = tree.xpath('//ul[contains(@class, "s-ref-indent-one")]//a/@href | //ul[contains(@class, "s-ref-indent-two")]//a/@href | //li[@class="a-spacing-micro s-navigation-indent-2"]//a/@href')

            seller_list = tree.xpath('//span[@class="a-list-item"]//span[contains(text(), "See more")]/../@href')
            if seller_list != []:
                seller_list_url = [host + url for url in seller_list]
                seller_list_responses = self.download(seller_list_url, headers=header)
                for response in seller_list_responses:
                    print('进入商铺分类')
                    self.parse_shop_catgory(response)

            if urls != []:
                real_urls = [host + url for url in urls]

                # 进入下级目录

                category3_responses = self.download(real_urls)
                for response in category3_responses:

                    print('进入下级分类')
                    self.parse_category3(response)

    def parse_shop_catgory(self, response):
        if response != None:
            tree = etree.HTML(response.text)
            urls = tree.xpath('//div[@id="center"]/div[2]//span/a/@href')
            if urls != []:
                real_url= [host + url for url in urls]

                print(real_url)
                seller_list_responses = self.download(real_url, headers=header)
                for response in seller_list_responses:
                    print('进入商铺列表页')
                    self.parse_seller_list(response)
            else:
                print('进入商铺列表页')
                self.parse_seller_list(response)

    def parse_seller_list(self, response):
        if response != None:
            tree = etree.HTML(response.text)
            urls = tree.xpath('//div[@id="center"]/div[4]//span/a/@href')
            if urls != []:
                real_url = [host + url for url in urls]

                self.save(real_url)


    def save(self, urls):
        print('===========开始保存============')
        for url in urls:
            with open('D:/DATA/amazon_店铺/seller_v2.txt') as f:
                f.write(url + '\n')

if __name__ == "__main__":
    getamazon = GetAmazonSeller()
    getamazon.parse_category1(['https://www.amazon.co.uk/gp/site-directory'])