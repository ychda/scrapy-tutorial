# -*- coding: utf-8 -*-
# todo: https://github.com/runningRobin/music163/blob/master/music163/pipelines.py
"""
Typical uses of item pipelines are:

cleansing HTML data
validating scraped data (checking that the items contain certain fields)
checking for duplicates (and dropping them)
storing the scraped item in a database
"""
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

"""
class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item
"""


# https://docs.scrapy.org/en/latest/topics/item-pipeline.html#duplicates-filter
# todo：每次运行过程中可以去重，但是还无法从数据库中去重
class DuplicatesPipeline(object):
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item


class MongoPipeline(object):
    collection_name = 'quotestoscrape'
    # collection_name = 'bookstoscrape'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider, ):
        self.db[self.collection_name].insert_one(item)
        return item
