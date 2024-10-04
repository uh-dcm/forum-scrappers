from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapers
import constants
from uh_scrapy import spiders

process = CrawlerProcess(get_project_settings())

#All currently supported domains

class Search:
    
    def __init__(self, search_params, search_query, body=None, thread_limit = None, comm_limit=None) -> None:
        self.search_params = search_params
        self.body = body if body is not None else []
        self.search_query = search_query if search_query is not None else self.set_search_query()
        self.thread_limit = thread_limit
        self.comm_limit = comm_limit

    def choose(self, param_dict, choice_message=None):
        if choice_message is not None:   
            print('') 
            print(choice_message)
        else:
            print("Choose from:")
        for n, item in enumerate(param_dict):
            print(f'{n+1}.{item}')
        print('')
        while True:
            choice = input("->")
            if choice in str(param_dict):
                return (param_dict[choice], choice)
            else:
                print("Not a valid input, try again")
        

    def fill(self):
        self.body = []
        for param in self.search_params:
            self.body.append(self.choose(param))
    
    def set_search_query(self):
        self.search_query = input("\nType your search query:\n->")

    
    def format_search_query(self):
        formatted_query = self.search_query.replace(" ", "%20")
        return formatted_query


class uhWebScraperUI:
     
    def __init__(self) -> None:
          self.allowed_domains = constants.ALLOWED_DOMAINS
     
    def get_input(allowed_list):
        while True:
            searchconstruct = input()
            if searchconstruct in allowed_list:
                return allowed_list[searchconstruct], searchconstruct
            else:
                print("Not applicable input, try again:")

    def run(self):
        print("Choose domain:")
        print("\n".join(self.allowed_domains) + "\n")
        while True:
            domain = input("->")
            if domain in self.allowed_domains:
                break
            else:
                print('Wrong domain, try again:')
        print("------")
        #Vauva scrape code using their search function
        if domain == 'vauva.fi':
                print("Input search term to find threads:\n")
                key = input("->")
                process.crawl("vauva", test = "test", start_urls = [f'https://www.vauva.fi/haku?keys={key}&sort&searchpage'])
                process.start() 

        #Yle scrape code using their search function      
        elif domain == 'yle.fi':
            scraper = scrapers.YleScraper()
            scraper.scrape()
        elif domain == 'hs.fi':
            scraper = scrapers.HSScraper()
            scraper.scrape()

if __name__ == "__main__":
    UH_UI = uhWebScraperUI()
    UH_UI.run()

