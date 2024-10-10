from datetime import datetime
from typing import Iterable
import scrapy
from pathlib import Path
import pandas as pd


class YleSpider(scrapy.Spider):
    name= 'yle'
    
    def __init__(self, search, *args, **kwargs):
        super(YleSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.count = 50
        self.offset = 0
        self.limit = 100

    def start_requests(self):
        return [scrapy.Request(self.query_to_url)]

    
    def get_search_string(self):
        oldsearchstr = super().get_search_string()
        searchstr = ("query=" + oldsearchstr[0], oldsearchstr[1])
        return searchstr
    
    
    def query_to_url(self, query, offset=0, count =50):
        app_id = 'hakuylefi_v2_prod'
        app_key = '4c1422b466ee676e03c4ba9866c0921f'
        searchstr= [valid[0] for valid in query if valid[0] != '']
        searchstr = "&".join(searchstr)
        APIurl = f'https://yle-fi-search.api.yle.fi/v1/search?app_id={app_id}&app_key={app_key}&limit={count}&offset={offset}&type=article&{searchstr}'
        return APIurl
    

    def collect_threads(self, query, offset =0, count = 50, limit=100):
        thread_ids =[]
        APIurl = self.query_to_url(query)
        print(APIurl)
        data = requests.get(APIurl)
        data = data.json()
        print(data)
        total_count = data['meta']['count']
        
        if total_count != 0:
            thread_ids.extend([entry['id'] for entry in data['data']])
        while offset+count<total_count:
            offset = offset + count
            APIurl = self.query_to_url(query, offset, count)
            data = requests.get(APIurl)
            data = data.json()
            thread_ids.extend([entry['id'] for entry in data['data']])
        return thread_ids
    
    def scrape_thread(self, id):
        comments = []
        app_key = 'sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D'
        app_id = 'yle-comments-plugin'
        url = f"https://comments.api.yle.fi/v1/topics/{id}/comments/accepted?app_id={app_id}&app_key={app_key}&parent_limit=100"
        data = requests.get( url )
        data = data.json()
        if 'notifications' not in data:
            comments = data
        return comments
    
    def make_filename(self, query):
        argstr = '_'.join([x[1] for x in query])
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/{self.domain}_{filename_date_string}_{argstr}'
        return filename

    def to_4cat_csv(self, comments , filename):
        df = pd.DataFrame( comments )
        df.to_csv("scrapedcontent/test")
        newdf = pd.DataFrame()
        newdf['body'] = df['content']
        newdf['author'] = df['author']
        newdf['timestamp'] = df['createdAt'].apply(  lambda date: datetime.strptime(  date , "%Y-%m-%dT%H:%M:%S%z" ).strftime("%Y-%m-%d %H:%M:%S") )
        newdf['id'] = df['id']
        newdf['thread'] = df['topicExternalId']
        newdf.to_csv( filename )
        