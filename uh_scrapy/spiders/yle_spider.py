from datetime import datetime
from typing import Iterable
import scrapy
from pathlib import Path
import pandas as pd
import constants
import configparser
from ..items import PostItem


class YleSpider(scrapy.Spider):
    name= 'yle'
    start_urls = ['https://yle.fi/']
    
    def __init__(self, *args, **kwargs):
        super(YleSpider, self).__init__(*args, **kwargs)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        

    #Function to turn the search parameters into a valid url 
    def query_to_url(self, count, offset):
        app_id = 'hakuylefi_v2_prod'
        app_key = '4c1422b466ee676e03c4ba9866c0921f'
        searchstr = "&".join([a for a in self.search if a != ""])
        APIurl = f'https://yle-fi-search.api.yle.fi/v1/search?app_id={app_id}&app_key={app_key}&limit={count}&offset={offset}&type=article&{searchstr}&time=custom'
        return APIurl

    
    def parse(self, response):

        query = "query=" + self.settings["QUERY"].replace(" ", "%20")
        category = self.config["YLE_CATEGORIES"][self.settings["CATEGORY"]]
        timeFrom = "timeFrom=" + self.settings["TIMEFROM"]
        timeTo = "timeTo=" + self.settings["TIMETO"]
        language = self.config["YLE_LANGUAGE"][self.settings["LANGUAGE"]]
        self.search = [query, category, timeFrom, timeTo , language]

        self.count = 50
        self.offset = 0
        self.limit = 100

        self.comments = []

        url = self.query_to_url(self.count, self.offset)
        return scrapy.Request(url, callback=self.parse_threads)
 
    
    # Function to collect thread ids
    def parse_threads(self, response):
        print('parsing')
        data = response.json()
        self.total_count = data['meta']['count'] 
        if self.total_count != 0:
            for id in [entry['id'] for entry in data['data']]:
                app_key = 'sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D'
                app_id = 'yle-comments-plugin'
                url = f"https://comments.api.yle.fi/v1/topics/{id}/comments/accepted?app_id={app_id}&app_key={app_key}&parent_limit=100"
                yield scrapy.Request(url, callback=self.scrape_thread)
            
        yield self.parse_threads_next_page(response)

    def parse_threads_next_page(self,response):
        if self.offset+self.count<self.total_count:
            self.offset = self.offset + self.count
            APIurl = self.query_to_url(self.count, self.offset)
            yield scrapy.Request(APIurl, callback=self.parse_threads)

    # Function to scrape comments from thread
    def scrape_thread(self, response):
        data = response.json()    
        if 'notifications' not in data:
            for comment in data:
                print(comment)
                post = PostItem()
                post['author'] = comment['author'] 
                post['body'] = comment['content']
                post['timestamp'] = comment['createdAt']
                post['id'] = comment['id']
                post['thread'] = comment['topicExternalId']
                yield post
    
    def scrape_thread_next_page(self,response):
        pass

    # Function to make an appropriate filename
    def make_filename(self):
        argstr = '_'.join(self.filename)
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/yle_{filename_date_string}_{argstr}.csv'
        return filename

    # Function to save scraped data to csv
    def to_4cat_csv(self, comments , filename):
        df = pd.DataFrame( comments )
        newdf = pd.DataFrame()
        newdf['body'] = df['content']
        newdf['author'] = df['author']
        newdf['timestamp'] = df['createdAt'].apply(  lambda date: datetime.strptime(  date , "%Y-%m-%dT%H:%M:%S%z" ).strftime("%Y-%m-%d %H:%M:%S") )
        newdf['id'] = df['id']
        newdf['thread'] = df['topicExternalId']
        newdf.to_csv( filename )

    # Make filename and save data after spider is done
    def closed(self, reason):
        pass

        