from datetime import datetime
import scrapy
from pathlib import Path
import pandas as pd
from scrapy.http import FormRequest
import logging

class KauppalehtiSpider(scrapy.Spider):

    name = "kauppalehti"
    start_urls = ['https://keskustelu.kauppalehti.fi/search/']

    def __init__(self, search, *args, **kwargs):
        super(KauppalehtiSpider, self).__init__(*args, **kwargs)
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        self.search = search
        self.items = []

    
    def parse(self, response):
        print(response)
        _xfToken = response.css("input[name='_xfToken']::attr(value)").get()
        if not _xfToken:
            self.logger.error("Could not retrieve _xfToken")
            return
        formdata = {
            'keywords': self.search[0],
            'c[title_only]': self.search[1],
            'c[users]': self.search[2],
            'c[newer_than]': self.search[3],
            'c[older_than]': self.search[4],
            'c[min_reply_count]': self.search[5],
            'c[nodes][]':self.search[6],
            'c[child_nodes]':self.search[7],
            'order': self.search[8],
            'grouped': '1',
            '_xfToken' : _xfToken,
        }
        print(formdata)
        yield FormRequest(
            url='https://keskustelu.kauppalehti.fi/search/search',
            formdata=formdata,
            method='POST',
            callback=self.parse_threads
        )


    def parse_threads(self, response):
        print("Parsing threads now")
        threads = response.xpath("//li[contains(@class, 'block-row--separated')]")
        for thread in threads:
            link = thread.xpath(".//h3[@class='contentRow-title']/a/@href").get()
            url = response.urljoin(link)
            thread_name = thread.xpath(".//h3[@class='contentRow-title']/a/text()").getall()
            thread_name = ' '.join([text.strip() for text in thread_name if text.strip()]),
            yield scrapy.Request(url, callback=self.scrape_thread, meta={'thread': thread_name})

        self.parse_threads_next_page(response)



    def parse_threads_next_page(self, response):
        next_page = response.xpath("//a[contains(@class, 'pageNav-jump--next')]/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_threads)


    def scrape_thread(self, response):
        thread = response.xpath("//div[@class='p-title ']/h1/text()").get()
        for comment in response.xpath("//div[@class='message-inner']"):
            body = comment.xpath(".//article[@class='message-body js-selectToQuote']//div[@class='bbWrapper']//text()").getall()
            row = {
                "thread": thread,
                "Author": comment.xpath(".//h4[@class='message-name']/a//text()").get(),
                "body": ' '.join([text.strip() for text in body if text.strip()]),
                "id": comment.xpath(".//a[contains(@class, 'message-attribution-gadget')]/@data-href").re_first(r'/posts/(\d+)/'),
                "timestamp": comment.xpath(".//time[@class='u-dt']/@datetime").get()
            }
            self.items.append(row)
        yield from self.scrape_thread_next_page(response)

    #check if the next page exists
    def scrape_thread_next_page(self, response):
        next_page = response.xpath("//a[contains(@class, 'pageNav-jump--next')]/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.scrape_thread)




   # Function to make an appropriate filename
    def make_filename(self):
        argstr = '_'.join(self.search)
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/kauppalehti_{filename_date_string}_{argstr}.csv'
        return filename

    # Function to save scraped data to csv
    def to_4cat_csv(self, comments , filename):
        df = pd.DataFrame( comments ) 
        df.to_csv( filename )

    # Make filename and save data after spider is done
    def closed(self, reason):
        name = self.make_filename()
        if self.items is not []:
            self.to_4cat_csv(self.items, name)




        