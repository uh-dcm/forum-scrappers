from datetime import datetime
import scrapy
from pathlib import Path
import pandas as pd
from scrapy.http import FormRequest
from ..items import PostItem

items = []
class KaksplusSpider(scrapy.Spider):

    name = "spooder"
    start_urls = []

    def __init__(self, search, *args, **kwargs):
        super(KaksplusSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.items = []

    
    def parse(self, response):
        print(response)
        _xfToken = response.css(fill xpath to xfToken).get()
        formdata = {
            #fill formdata here  based on the html
            #the format is as following:
            # form_field1 = search[0]
            # form_field2 = search[0] 
                    
                    }
        yield FormRequest(
            url= 'fill url here',
            formdata=formdata,
            method='POST',
            callback=self.parse_threads
        )

    def parse_threads(self, response):
        threads = response.xpath(fill xpath here)getall()
        for thread in threads:
            link = thread.xpath(fill xpath here)
            url = response.urljoin(link)
            thread_name = thread.xpath(fill xpath here)
            yield scrapy.Request(url, callback=self.scrape_thread, meta={'thread': thread_name})

        yield from self.parse_threads_next_page(response)

    def parse_threads_next_page(self, response):
        next_page = response.xpath(fill xpath to next page link).get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_threads)


    def scrape_thread(self, response):
        
        i = 0
        ids= response.xpath(".//a/@name").getall()
        for comment in response.xpath("//td[@class='postbodywrap']"):
            post = PostItem()

            post["thread"] = response.xpath("//td[@class='postsubject']/span[@class='PhorumTableHeader']/text()").get().strip()

            post["author"] = comment.xpath(".//p[@class='PhorumMessage']/text()").getall()[1][1:].strip()
            
            body = comment.xpath(".//p[@class='PhorumMessage']/text()").getall()[3:]

            post["body"] = ' '.join([text.strip() for text in body if text.strip()])
            
            post["id"] = ids[i][6:]
            i+=1

            pre_time = comment.xpath(".//p[@class='PhorumMessage']/text()").getall()[2].strip()[11:].strip()
            parsed_date = datetime.strptime(pre_time, "%d.%m.%y %H:%M:%S")
            iso_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%S")
            post["timestamp"] = iso_date

            yield post

        yield from self.scrape_thread_next_page(response)


    def scrape_thread_next_page(self, response):
        next_page =  response.xpath(fill xpath to next page link).get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.scrape_thread)



   # Function to make an appropriate filename
    def make_filename(self):
        argstr = '_'.join(self.search)
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/kaksplus.fi_{filename_date_string}_{argstr}'
        return filename

    # Function to save scraped data to csv
    def to_4cat_csv(self, comments , filename):
        df = pd.DataFrame( comments ) 
        df.to_csv( filename )

    # Make filename and save data after spider is done
    def closed(self, reason):
        name = self.make_filename()
        self.to_4cat_csv(self.items, name)



        