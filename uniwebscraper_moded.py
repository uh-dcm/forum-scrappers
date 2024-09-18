from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#All currently supported domains
ALLOWED_DOMAINS = ['vauva.fi', 'yle.fi']
#All currently supported settings for yle
YLE_SEARCH_FIELDS = {'uutiset' : 'service=uutiset', 'urheilu' : 'service=urheilu', 'oppiminen' : 'service=oppiminen',
                'elävä-arkisto': 'service=elava-arkisto', 'ylex' : 'service=ylex', 'kaikki' : ''}
YLE_SEARCH_TIMES = {'tänään' : 'time=today', 'viikko': 'time=week', 'kuukausi' : 'time=month', 'anytime': '' }
YLE_SEARCH_LANGS = {'suomi': '', 'svenska': 'language=sv', 'english': 'language=en', 'russian': 'language=ru',
                'samegiella': 'language=se', 'karjala': 'language=krl', 'kaikki': 'language=all'}

class ScraperBase:
    def __init__(self):
        self.process = CrawlerProcess(get_project_settings())

    def scrape_data(self):
        raise NotImplementedError("Subclasses must implement this method")

class vauvaScraper(ScraperBase):

    def scrape_data(self):
        print(f"Scraping data for {ALLOWED_DOMAINS[0]}")
        print("Input search term to find articles:\n")
        key = input()
        self.process.crawl("vauva", start_urls = [f'https://www.vauva.fi/haku?keys={key}&sort&searchpage'])
        self.process.start() 

class yleScraper(ScraperBase):

    def get_input(allowed):
        while True:
            searchconstruct = input()
            if searchconstruct in allowed:
                return allowed[searchconstruct]
            else:
                print("Not applicable input, try again:")

    def scrape_data(self):
        print(f"Scraping data for {ALLOWED_DOMAINS[1]}")
        url = []
    
        print('Search in: \n' + "\n".join(YLE_SEARCH_FIELDS))
        url.append(self.get_input(YLE_SEARCH_FIELDS))
        print('Choose time of the articles:\n' + '\n'.join(YLE_SEARCH_TIMES))
        url.append(self.get_input(YLE_SEARCH_TIMES))
        print('Choose language of the articles:\n' + '\n'.join(YLE_SEARCH_LANGS))
        url.append(self.get_input(YLE_SEARCH_LANGS))
        
        print('Input search query:')
        queryurl="query="
        query=input()
        url.append(queryurl + query.replace(" ", "%20"))
        url = "&".join(url)
        print()
        test = f'https://haku.yle.fi/?{url}&type=article&page=1'
        print(test)


class Domain:
    
    def __init__(self):
        self.allowed_list = ALLOWED_DOMAINS
        self.domain = None
        self.scraper = None
    
    def choose_domain(self):
        print("Choose domain\n")
        print("\n".join(ALLOWED_DOMAINS))
        print("Input: ")
        domain = input()
        while domain not in ALLOWED_DOMAINS: 
            print('Wrong domain, try again: ')
            domain = input()
        print("------")

    def set_scraper(self):
        if self.domain is None:
            self.choose_domain()
        
        if self.domain == ALLOWED_DOMAINS[0]:
            self.scraper = vauvaScraper()
        elif self.domain == ALLOWED_DOMAINS[1]:
            self.scraper = yleScraper()
        else:
            raise Exception(f'Undefined domain: {self.domain}')
    
    def scrape_data(self):
        if self.scraper is None:
            self.set_scraper()
        self.scraper.scrape()
        
class UniWebscraperCli:   

    def run(self):
        domain = Domain()
        domain.scrape_data()
       

if __name__ == "__main__":
    UniWebscraperCli.run()


