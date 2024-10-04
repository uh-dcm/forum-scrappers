from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapers
import constants
from uh_scrapy import spiders

process = CrawlerProcess(get_project_settings())

#All currently supported domains


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

