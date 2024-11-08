# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    thread = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    id = scrapy.Field()
    timestamp = scrapy.Field()

class Uh_scrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
