from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

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
            self.COUNTER += 1
            full_url = self.BASE_URL + link
            yield scrapy.Request(full_url, callback=self.parse_attr)

    def parse_attr(self, response):
        product = response.xpath('//section[@class="product-single"]')
        title = product.xpath('//h1/text()').extract_first()
        price = product.xpath('//p[@class="price"]/text()').extract_first()
        price = float(price[:-4].replace(',', '.'))
        img = product.xpath('//img/@src').extract_first()
        print(self.BASE_URL + img, title, price)
