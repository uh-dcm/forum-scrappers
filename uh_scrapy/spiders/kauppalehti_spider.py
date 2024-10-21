from datetime import datetime
import scrapy
from pathlib import Path
import pandas as pd
from scrapy.http import FormRequest

items = []
class KauppalehtiSpider(scrapy.Spider):

    name = "kauppalehti"
    start_urls = ['https://keskustelu.kauppalehti.fi/search/']

    def __init__(self, search, *args, **kwargs):
        super(KauppalehtiSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.items = []

    
    def parse(self, response):
        print(response)
        _xfToken = response.css("input[name='_xfToken']::attr(value)").get()
        formdata = {
            'keywords': self.search[0],
            'c[title_only]': self.search[1],
            'c[users]': self.search[2],
            'c[newer_than]': self.search[3],
            'c[older_than]': self.search[4],
            'order': self.search[5],
            '_xfToken' : _xfToken,
        }
        yield FormRequest(
            url='https://keskustelu.kauppalehti.fi/search/search',
            formdata=formdata,
            method='POST',
            callback=self.parse_threads
        )


    def parse_threads(self, response):
        threads = response.xpath("//li[contains(@class, 'block-row--separated')]")
        for thread in threads:
            link = thread.xpath(".//h3[@class='contentRow-title']/a/@href").get()
            url = response.urljoin(link)
            thread_name = thread.xpath(".//h3[@class='contentRow-title']/a/text()").get()
            yield scrapy.Request(url, callback=self.scrape_thread, meta={'thread': thread_name})

        self.parse_threads_next_page(response)



    def parse_threads_next_page(self, response):
        next_page = response.xpath("//a[contains(@class, 'pageNav-jump--next')]/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_threads)


    def scrape_thread(self, response):

        for comment in response.xpath('//div[@class="message-cell message-cell--main"]'):
            body = comment.xpath('.//div[@class="message-body js-selectToQuote"]//div[@itemprop="text"]//div[@class="bbWrapper"]//text()').getall()
            row = {
                "thread": response.meta['thread'],
                "Author": comment.xpath('.//div[@class="message-userContent"]/@data-lb-caption-desc').re_first(r'^(.*) ·'),
                "body": ' '.join([text.strip() for text in body if text.strip()]),
                "id": comment.xpath('.//div[@class="message-userContent"]/@data-lb-id').get(),
                "timestamp": comment.xpath('.//time[@class="u-dt"]/@datetime').get()
            }
            self.items.append(row)

            self.scrape_thread_next_page(response)

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
        filename = f'scrapedcontent/kauppalehti.fi_{filename_date_string}_{argstr}'
        return filename

    # Function to save scraped data to csv
    def to_4cat_csv(self, comments , filename):
        df = pd.DataFrame( comments ) 
        df.to_csv( filename )

    # Make filename and save data after spider is done
    def closed(self, reason):
        name = self.make_filename()
        self.to_4cat_csv(self.items, name)




        