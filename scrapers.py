import json
from datetime import datetime
import requests
import pandas as pd
import logging
import time

class Scraper:

    def __init__(self):
        self.query = None


    # Final function to call
    def scrape(self):
        if self.query is None:
            self.query = self.get_query()
        thread_ids = self.collect_threads(self.query)
        comments = self.scrape_threads(thread_ids)
        if comments is not None:
            print(f'You have scraped {len(thread_ids)} threads for {len(comments)} comments')
            Y_N = input("Would you like to save the results to a csv? (Y/N):\n->")
            if Y_N == "Y":
                filename = self.make_filename(self.query)
                self.to_4cat_csv(comments, filename)
                print("Thank you for using ScraperAirlines, please come again!")
            else:
                print("Saving aborted")
                print("Thank you for using ScraperAirlines, please come again!")
        else: print("No comments were scraped.")


    #Function to get the inputs for the search
    def choose(self, list, choice_message=None):
        if choice_message is not None:   
            print('') 
            print(choice_message)
        for n, item in enumerate(list):
            print(f'{n+1}.{item}')
        print('')
        while True:
            choice = input("->")
            if choice not in str(list):
                print("Not a valid input, try again:")
            else:
                break
        return list[choice], choice
    
    def get_search_string(self):
        key = input("\nType your search query:\n->")
        url_key = key.replace(" ", "%20")
        return url_key, key
    
    # Function to get a query for the search - unique per scraper
    def get_query(self):
        query = []
        return query
    

    # Function to process the query into a suitable url. Defines an API call.
    def query_to_url(self, query):
        APIurl = ""
        return APIurl
    

    # Collect threads/articles for comment scraping. Makes an API call and parses the response.
    def collect_threads(self, query, limit=100):
        thread_ids = []
        return thread_ids
    

    def scrape_threads(self, thread_ids):
        comments = []
        for id in thread_ids:
            comments.extend(self.scrape_thread(id))
        return comments

    
    # Scrape a thread/article
    def scrape_thread(self, id):
        comments=[]
        return comments
    
    def make_filename(self, query):
        filename = ''
        return filename

    def to_4cat_csv(self, comments, filename):
        raise NotImplementedError("This method must be implemented")


class HSScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.domain = 'hs.fi'
        self.times = {'whenever': 'whenever', 'today' : 'today', 'week':'week', 'month':'month'}
        self.categories = {'kaikki':'kaikki','autot':'autot','espoo':'espoo','helsinki':'helsinki',
                           'visio':'visio','hsytimessa':'hstimess%C3%A4', 'hsio':'hsio','kirjaarviot':'kirjaarviot',
                           'kolumnit':'kolumnit','koti':'koti', 'kultturi':'kultturi','kuukausiliite':'kuukauisiliite',
                           'lastenuutiset':'lastenuutiset','lifestyle':'lifestyle','maailma':'maailma','mielipide':'mielipide'}
        self.sorting = {'old-to-new':'old','new-to-old':'new','relevant':'rel'}



    def scrape(self):
        return super().scrape()


    def get_query(self):
        query = []
        query.append(self.choose(self.times, "Choose period to search:"))
        query.append(self.choose(self.categories, "Choose search category:"))
        query.append(self.choose(self.sorting, "Choose sorting preference:"))
        q = input("Type your search query:\n->")
        query.append((q, q))
        return query
    



    def query_to_url(self, query, offset=0, count =50, limit=50):
        ms = int(time.time() * 1000)
        APIurl = f'https://www.hs.fi/api/search/{query[3][0]}/{query[1][0]}/{query[0][0]}/{query[2][0]}/{offset}/{count}/0/{ms}'
        return APIurl    
    
    def collect_threads(self, query, offset=0,count=50, limit=50):
        thread_ids = []
        
        while offset < limit:
            APIurl = self.query_to_url(query, offset, count, limit)
            response = requests.get(APIurl)
            response = response.json()
            if response is not []:
                if limit-offset<count:
                    for item in response[:limit-offset]:
                        thread_ids.append(item['id'])
                else:
                    for item in response:
                        thread_ids.append(item['id'])
            offset = offset + count
        return thread_ids
    

    def scrape_threads(self, thread_ids):
        return super().scrape_threads(thread_ids)
        
    
    def scrape_thread(self, id):
        url = f"https://www.hs.fi/api/commenting/hs/articles/{id}/comments"
        data = requests.get( url )
        data = data.json()

        return data['comments']
    
    def make_filename(self, query):   
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/hs_scraped_{filename_date_string}_{query[0][1]}_{query[1][1]}_{query[2][1]}_{query[3][1]}'
        return filename
    
    def to_4cat_csv(self, comments, filename):
        df = pd.DataFrame( comments )
        newdf = pd.DataFrame()
        newdf['body'] = df['comment']
        newdf['author'] = df['userIdentity'].apply( lambda userIdentity: userIdentity['displayName'] )
        newdf['timestamp'] = df['createdAt'].apply(  lambda date: datetime.fromtimestamp(  date/1000 ).strftime("%Y-%m-%d %H:%M:%S") )
        newdf['id'] = df['id']
        newdf['thread'] = df['articleId']
        

        newdf.to_csv(filename)
    
class YleScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.domain = 'yle.fi'
        self.categories = {'uutiset' : 'service=uutiset', 'urheilu' : 'service=urheilu', 'oppiminen' : 'service=oppiminen',
               'elävä-arkisto': 'service=elava-arkisto', 'ylex' : 'service=ylex', 'kaikki' : ''}
        self.times = {'tanaan' : 'time=today', 'viikko': 'time=week', 'kuukausi' : 'time=month', 'anytime': '' }  
        self.language = {'suomi': '', 'svenska': 'language=sv', 'english': 'language=en', 'russian': 'language=ru',
             'samegiella': 'language=se', 'karjala': 'language=krl', 'kaikki': 'language=all'}
        
    def get_query(self):
        query = []
        query.append(self.choose(self.categories, "Choose search category:"))
        query.append(self.choose(self.times, "Choose search timeframe:"))
        query.append(self.choose(self.language, "Choose article language:"))
        query.append(self.get_search_string())
        return query
    
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

