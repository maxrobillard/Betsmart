# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import scrapy

from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewscrawlerPipeline:
    def process_item(self, item, spider):
        return item

from scrapy.exceptions import DropItem

class TextPipeline(object):

    def process_item(self, item, spider):
        if item['equipe1']:
            item["equipe1"] = clean_spaces(item["equipe1"])
            item["equipe2"] = clean_spaces(item["equipe2"])
            item["site"] = clean_spaces(item["site"])
            item["cote"] = clean_spaces(item["cote"])
            item["cote2"] = clean_spaces(item["cote2"])
            item["cote3"] = clean_spaces(item["cote3"])
            return item
        else:
            raise DropItem("Missing title in %s" % item)


            def clean_spaces(string):
                if string:
                    return " ".join(string.split())

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["bet"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
