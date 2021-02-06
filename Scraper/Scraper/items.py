# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()
    cote = scrapy.Field()
    cote2 = scrapy.Field()
    cote3 = scrapy.Field()
    equipe1 = scrapy.Field()
    equipe2 = scrapy.Field()
