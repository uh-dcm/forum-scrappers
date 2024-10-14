from datetime import datetime
import scrapy
from pathlib import Path
import pandas as pd

items = []
class VauvaSpider(scrapy.Spider):

    name = "vauva"
    
    def parse(self, response):
        for thread in response.xpath("//a[contains(@href, 'replies')]/@href").getall():
            thread = response.urljoin(thread)
            yield scrapy.Request(thread, callback=self.parse_thread)


        next_page = response.xpath('//a/span[text()="Seuraava"]/../@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)   

    def parse_thread(self, response):

        for comment in response.xpath('//div[contains(@class, "comment comment")]'):
            row = {
                "thread": response.xpath("//meta[contains(@property, 'og:site_name')]//@content").get(),
                "Author": comment.xpath(".//article//text()")[1].get(),
                "body": ''.join(comment.xpath('.//div[contains(@class, "content my")]/*').getall()),
                "timestamp": datetime.fromisoformat(''.join(comment.xpath(".//div[contains(@class, 'flex justify-end')]/div/time/@datetime").getall())).strftime('%Y-%m-%d %H:%M:%S')
            }
            items.append(row)
        next_page =  response.xpath('//a/span[text()="Seuraava"]/../@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_thread)

    def closed(self, reason):
        df = pd.DataFrame(items, columns = ['thread', 'Author', 'body', 'timestamp'])
        
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        df.to_csv(f'scrapedcontent/vauva_scraped_{filename_date_string}.csv', index=True)




        