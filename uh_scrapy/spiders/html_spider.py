import scrapy
import pandas as pd


items = []
class HTML_spider(scrapy.Spider):
    name="html"
    def parse(self, response):
        row = {
                "url": response.url,
                "html": response.body
                }
        items.append()

    def closed(self, reason):
        df = pd.DataFrame(items, columns = ['url', 'html'])
        df.to_csv('futusome_forums_html.csv', index=True)