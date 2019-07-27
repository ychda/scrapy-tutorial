# -*- coding: utf-8 -*-
import scrapy


class BookstoscrapeSpider(scrapy.Spider):
    name = 'books_toscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for href in response.xpath('//section/div/ol[@class="row"]/li').css('.image_container a::attr(href)'):
            yield response.follow(href, self.parse_book)

        next_page = response.css('.pager .next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        yield {
            'title': response.css('article.product_page .product_main h1::text').get(),
            'price': response.css('article.product_page .product_main p.price_color::text').get(),
            'url': response.url,
            # https://docs.scrapy.org/en/latest/topics/developer-tools.html#caveats-with-inspecting-the-live-browser-dom
            'UPC': response.xpath('//table[@class="table table-striped"]/tr/td/text()').get(),
        }
