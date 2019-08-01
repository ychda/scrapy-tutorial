# -*- coding: utf-8 -*-
"""
难道 Ctrl + C 强行退出程序？？
# yield response.follow(next_page, self.parse, dont_filter=True)
mongo数据库去重：
以text、author为依据。
db.quotestoscrape.aggregate([
        {$group: {_id: {text: '$text', author: '$author'}, count: {$sum: 1}, dups: {$addToSet: '$_id'}}},
        {$match: {count: {$gt: 1}}}
]).forEach(function(doc){
    doc.dups.shift();
    db.quotestoscrape.remove({_id: {$in: doc.dups}});
})
"""

import scrapy


class QuotesXpathSpider(scrapy.Spider):
    name = 'quotes_random'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall(),
            }
        next_page = 'http://quotes.toscrape.com/random'
        yield response.follow(next_page, self.parse, dont_filter=True)
