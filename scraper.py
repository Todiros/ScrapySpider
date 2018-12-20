from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re

class MrbSpider(CrawlSpider):
    name = 'mrbspider'
    start_urls = [
        'https://mr-bricolage.bg/bg/%D0%9A%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3/%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B8/%D0%90%D0%B2%D1%82%D0%BE-%D0%B8-%D0%B2%D0%B5%D0%BB%D0%BE%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D0%BE%D0%B0%D1%80%D0%B8/%D0%92%D0%B5%D0%BB%D0%BE%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D0%BE%D0%B0%D1%80%D0%B8/c/006008012'
    ]

    BASE_URL = 'https://mr-bricolage.bg/'
    COUNTER = 0

    rules = (
        Rule(LinkExtractor(
            restrict_css=('.pagination-next',)),
            callback='parse_start_url',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        for link in response.xpath('//a[@class="name"]/@href').extract():
            full_url = self.BASE_URL + link
            yield Request(full_url, callback=self.parse_attr)

    def parse_attr(self, response):
        self.COUNTER += 1
        product = response.xpath('//section[@class="product-single"]')
        title = product.xpath('//h1/text()').extract_first()
        price = product.xpath('//p[@class="price"]/text()').extract_first()
        price = float(price[:-4].replace(',', '.'))
        img = product.xpath('//img/@src').extract_first()
        img = self.BASE_URL + img

        product_details = response.xpath('//section[@class="product-details"]')

        # --- EAN ---
        EAN = product_details.xpath('//div[@id="home"]/div/span/strong/text()').extract_first()
        EAN_num = product_details.xpath('//div[@id="home"]/div/span/text()').extract()

        for i in EAN_num:
            if re.search('[^\\r\\n\\t]', i):
                EAN_num = i[4:]

        EAN_full = " ".join([EAN, EAN_num])

        # --- PRODUCT DESCRIPTION ---
        product_info = product_details.xpath('//table[@class="table"]/tbody/tr/td/text()').extract()

        if not product_info:
            product_info = product_details.xpath('//div[@id="home"]/div/text()').extract()

        for idx, val in enumerate(product_info):
            product_info[idx] = val.strip()

        product_info = [x for x in product_info if x != '']

        if (len(product_info) > 3) and (product_info[2] == 'Гаранция'):
            product_info[3] = re.sub('[\\r\\n\\t\\xa0]', '', product_info[3])

        print(self.COUNTER, img, title, price, EAN_full, product_info)
