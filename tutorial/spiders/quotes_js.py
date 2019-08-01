# -*- coding: utf-8 -*-
"""
settings.py中，DEFAULT_REQUEST_HEADERS使用默认值，不要轻易修改。
修改为自己浏览器的值之后，为什么得不到需要的数据？
唉，说多了都是泪。。。
"""
import scrapy
from scrapy_splash import SplashRequest


class QuoteSpider(scrapy.Spider):
    name = 'quotes_js'
    start_urls = ['http://quotes.toscrape.com/js']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'wait': 0.5})

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall(),
            }
            next_page = response.xpath('//a[contains(text(),"Next")]/@href').get()
            if next_page:
                absolute_url = response.urljoin(next_page)
                yield SplashRequest(absolute_url, args={'wait': 0.5})
