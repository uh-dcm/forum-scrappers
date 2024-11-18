from datetime import datetime
import scrapy
from pathlib import Path
import pandas as pd
from scrapy.http import FormRequest

items = []
class KaksplusSpider(scrapy.Spider):

    name = "kaksplus"
    start_urls = ['https://keskustelu.kaksplus.fi/keskustelu/haku/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': False,  # Temporarily disable robots.txt obeying
        'FEEDS':{
            'data.csv':{
                'format':'csv'
            }
        }
    }


    def __init__(self, search, *args, **kwargs):
        super(KaksplusSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.items = []

    
    def parse(self, response):
        print(response)
        _xfToken = response.css('input[name="_xfToken"]::attr(value)').get()
        formdata = {
            "keywords": self.search[0],  
            "c[title_only]": '1' if self.search[1] else '0',  
            "c[newer_than]": self.search[2],  
            "c[min_reply_count]": self.search[3],  
            "c[nodes][]": self.search[4],  
            "c[child_nodes]": '1' if self.search[5] else '0',  
            "order": self.search[6],  
            "grouped": '1',    
            "_xfToken": _xfToken,  
        }
        print(formdata)

        yield FormRequest(
            url='https://keskustelu.kaksplus.fi/keskustelu/haku/search',
            formdata=formdata,
            method='POST',
            callback=self.parse_threads
        )

    def parse_threads(self, response):
        links = response.xpath('//h3[@class="contentRow-title"]/a/@href').getall()
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.scrape_thread)

        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_threads)


    def scrape_thread(self, response):
        thread = response.xpath('//html/@data-content-key').get()[7:]
        
         
        for comment in response.xpath('//article[contains(@class, "message--post")]'):
            body = comment.xpath('.//div[@class="bbWrapper"]/text()').getall()
            row = {
                "thread": thread,
                "Author": comment.xpath('./@data-author').get(),
                "body": ' '.join([text.strip() for text in body if text.strip()]),
                "id": comment.xpath('./@id').get()[8:],
                "timestamp": comment.xpath('.//time/@datetime').get()
            }
            self.items.append(row)
        next_page =  response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.scrape_thread)



   # Function to make an appropriate filename
    def make_filename(self):
        argstr = '_'.join(self.search)
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/kaksplus_{filename_date_string}_{argstr}.csv'
        return filename

    # Function to save scraped data to csv
    def to_4cat_csv(self, comments , filename):
        df = pd.DataFrame( comments ) 
        df.to_csv( filename )

    # Make filename and save data after spider is done
    def closed(self, reason):
        name = self.make_filename()
        self.to_4cat_csv(self.items, name)




        