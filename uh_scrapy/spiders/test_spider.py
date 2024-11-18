from typing import Iterable
import scrapy
import logging

class TestSpider(scrapy.Spider):
    name = "test"

    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'LOG_LEVEL': 'DEBUG',
    'ROBOTSTXT_OBEY': False  # Temporarily disable robots.txt obeying
}

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        self.logger.info("Spider initialized")
        self.count = 0

    def parse(self, response):
        url = response.xpath("//a[contains(@href, 'a=2')]/@href").get()
        self.count +=1
        if url is not None:
             url = response.urljoin(url)
             yield scrapy.Request(url, callback=self.parse)
    def closed(self, reason):

        print(self.count)

