from typing import Iterable
import scrapy

class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = ['vauva.fi']

    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'LOG_LEVEL': 'DEBUG',
    'ROBOTSTXT_OBEY': False  # Temporarily disable robots.txt obeying
}

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        self.logger.info("Spider initialized")

    def parse(self, response):
        print(f"Visited: {response.url}")
        # Check if the page was fetched correctly
        print(f"Response status: {response.status}")
        # Extract and print the page title or other elements for confirmation
        page_title = response.css('title::text').get()
        print(f"Page Title: {page_title}")
