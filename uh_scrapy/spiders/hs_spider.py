from datetime import datetime
from typing import Iterable
import scrapy
from pathlib import Path
import pandas as pd
import constants
import time


class HSSpider(scrapy.Spider):
    name= 'hs'
    
    def __init__(self, search, *args, **kwargs):
        super(HSSpider, self).__init__(*args, **kwargs)
        self.filename = search
        query = search["query"].replace(" ", "%20")
        category = constants.HS_CATEGORIES[search["category"]]
        timeFrom = self.convert_to_epoch_ms(search["timeFrom"])
        timeTo = self.convert_to_epoch_ms(search["timeTo"])
        sort = constants.HS_SORTING[search["sort"]]
        self.search = [query, category, timeFrom, timeTo, sort]

        self.count = 50
        self.offset = 0
        self.limit = int(search['max_threads'])

        self.comments = []

    #convert date string to epoch time
    def convert_to_epoch_ms(self, date_string):
        # Back to date object
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        
        # Convert the datetime object to epoch time in seconds
        epoch_time = int(time.mktime(date_obj.timetuple()))
        
        # Multiply by 1000 to get milliseconds
        epoch_ms = epoch_time * 1000
        return epoch_ms

    #Function to turn the search parameters into a valid url 
    def query_to_url(self, count, offset):
        APIurl = f'https://www.hs.fi/api/search/{self.search[0]}/{self.search[1]}/custom/{self.search[4]}/{offset}/{count}/{self.search[2]}/{self.search[3]}/keyword'
        return APIurl  

    #initial request
    def start_requests(self):
        url = self.query_to_url(self.count, self.offset)
        return [scrapy.Request(url, callback=self.parse)] 
    
 
    
    # Function to collect thread ids
    def parse(self, response):
        
        data = response.json()
        if data != []:
            for id in [entry['id'] for entry in data]:
                url = f"https://www.hs.fi/api/commenting/hs/articles/{id}/comments"
                yield scrapy.Request(url, callback=self.scrape_thread)

        
            if self.limit==0 or self.offset+self.count<self.limit:
                self.offset = self.offset + self.count
                APIurl = self.query_to_url(self.count, self.offset)
                yield scrapy.Request(APIurl, callback=self.parse)

    # Function to scrape comments from thread
    def scrape_thread(self, response):
        data = response.json()
        self.comments.extend(data['comments'])

    # Function to make an appropriate filename
    def make_filename(self):
        argstr = '_'.join(self.filename.values())
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/hs.fi_{filename_date_string}_{argstr}'
        return filename

    # Function to save scraped data to csv
    def to_4cat_csv(self, comments, filename):
        df = pd.DataFrame( comments )
        newdf = pd.DataFrame()
        newdf['body'] = df['comment']
        newdf['author'] = df['userIdentity'].apply( lambda userIdentity: userIdentity['displayName'] )
        newdf['timestamp'] = df['createdAt'].apply(  lambda date: datetime.fromtimestamp(  date/1000 ).strftime("%Y-%m-%d %H:%M:%S") )
        newdf['id'] = df['id']
        newdf['thread'] = df['articleId']
        

        newdf.to_csv(filename)
    

    # Make filename and save data after spider is done
    def closed(self, reason):
        name = self.make_filename()
        self.to_4cat_csv(self.comments, name)

        