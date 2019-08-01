# -*- coding: utf-8 -*-
"""
需要登录之后才会出现的页面
模拟登录方法
https://docs.scrapy.org/en/latest/topics/request-response.html#using-formrequest-from-response-to-simulate-a-user-login
"""
import scrapy


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass


class LoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'ychda', 'password': 'pas3wOrd'},
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error('Login failed')
            return
        # continue scraping with authenticated session...
        for quote in response.css('.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
                'goodreads': quote.xpath('.//span/a[contains(@href,"goodreads.com")]/@href').get(),
            }
            next_page = response.css('li.next a::attr("href")').get()
            if next_page is not None:
                yield response.follow(next_page, self.after_login)
