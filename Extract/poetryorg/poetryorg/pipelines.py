# -*- coding: utf-8 -*-

import pymongo

from scrapy.conf import settings
# from scrapy.exceptions import DropItem
from scrapy import log
from poetryorg.items import PoetItem, PoemItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item

class PoetPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_POET_COLLECTION']] # use the person collection

    def process_item(self, item, spider):
        if not isinstance(item,PoetItem):
            return item # return the item to let other pipeline to handle it
        self.collection.insert(dict(item))
        log.msg("Poet added to MongoDB database!",level=log.DEBUG, spider=spider)


class PoemPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_POEM_COLLECTION']] # use the book collection

    def process_item(self, item, spider):
        if not isinstance(item,PoemItem):
            return item # return the item to let other pipeline to handle it
        self.collection.insert(dict(item))
        log.msg("Poem added to MongoDB database!",level=log.DEBUG, spider=spider)
