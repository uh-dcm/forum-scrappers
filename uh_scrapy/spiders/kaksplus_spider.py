from datetime import datetime
import scrapy
from pathlib import Path
import pandas as pd
from scrapy.http import FormRequest
import configparser
from ..items import PostItem

items = []
class KaksplusSpider(scrapy.Spider):

    name = "kaksplus"
    start_urls = ['https://keskustelu.kaksplus.fi/keskustelu/haku/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': False,
        }


    def __init__(self, *args, **kwargs):
        super(KaksplusSpider, self).__init__(*args, **kwargs)
        self.query = ''
        self.title_only = ''
        self.newer_than = ''
        self.min_reply = ''
        self.forum_section = ''
        self.subsections = ''
        self.sort =''

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    
    def parse(self, response):
        self.query = self.settings["QUERY"].replace(" ", "%20")
        self.title_only = self.settings["TITLEONLY"]
        self.newer_than = self.settings["TIMEFROM"]
        self.min_reply = self.settings["MINREPLY"]
        self.forum_section = self.settings["FORUMSECTION"]
        self.subsections = self.settings["SUBSECTIONS"]
        self.sort =self.settings["SORTING"]

        _xfToken = response.css('input[name="_xfToken"]::attr(value)').get()
        formdata = {
            "keywords": self.query,  
            "c[title_only]": '1' if self.title_only else '0',  
            "c[newer_than]": self.newer_than,  
            "c[min_reply_count]": self.min_reply,  
            "c[nodes][]": self.config['KAKSPLUS_FORUM_SECTIONS'][self.forum_section],  
            "c[child_nodes]": '1' if self.subsections else '0',  
            "order": self.sort,  
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

        yield from self.parse_threads_next_page(response)

    def parse_threads_next_page(self, response):
        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_threads)


    def scrape_thread(self, response):
        thread = response.xpath('//html/@data-content-key').get()[7:]
        
        
        for comment in response.xpath('//article[contains(@class, "message--post")]'):
            post = PostItem()
            body = comment.xpath('.//div[@class="bbWrapper"]/text()').getall()
            post['id'] = comment.xpath('./@id').get()[8:]
            post['author'] = comment.xpath('./@data-author').get()
            post['thread'] = thread
            post['body'] = ' '.join([text.strip() for text in body if text.strip()])
            post['timestamp'] = comment.xpath('.//time/@datetime').get()
            yield post

        yield from self.scrape_thread_next_page(response)

    def scrape_thread_next_page(self, response):
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




        