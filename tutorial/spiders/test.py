# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['quote.toscrape.com']
    start_urls = ['http://quote.toscrape.com/']

    def parse(self, response):
        pass
