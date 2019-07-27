# -*- coding: utf-8 -*-
"""
http://quotes.toscrape.com/scroll
爬取动态加载的页面
"""
import json

import scrapy


class QuotesscrollSpider(scrapy.Spider):
    name = 'quotes_scroll'
    allowed_domains = ['quotes.toscrape.com']
    page = 1
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        data = json.loads(response.text)
        for quote in data["quotes"]:
            yield {
                "quote": quote["text"],
                "author": quote["author"]["name"],
                "goodreads_link": quote["author"]["goodreads_link"],
                "tags": quote["tags"],
            }
        if data["has_next"]:
            self.page += 1
            url = "http://quotes.toscrape.com/api/quotes?page={}".format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)
