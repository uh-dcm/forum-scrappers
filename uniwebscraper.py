from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapers

process = CrawlerProcess(get_project_settings())

#All currently supported domains
allowed_domains = ['vauva.fi', 'yle.fi', 'hs.fi']


def get_input(allowed_list):
    while True:
        searchconstruct = input()
        if searchconstruct in allowed_list:
            return allowed_list[searchconstruct], searchconstruct
        else:
             print("Not applicable input, try again:")

print("Choose domain:")
print("\n".join(allowed_domains) + "\n")
while True:
    domain = input()
    if domain in allowed_domains:
        break
    else:
        print('Wrong domain, try again:')
print("------")
#Vauva scrape code using their search function
if domain == 'vauva.fi':
        print("Input search term to find threads:\n")
        key = input()
        process.crawl("vauva", start_urls = [f'https://www.vauva.fi/haku?keys={key}&sort&searchpage'])
        process.start() 

#Yle scrape code using their search function      
elif domain == 'yle.fi':
    scraper = scrapers.YleScraper()
    scraper.scrape()
elif domain == 'hs.fi':
    scraper = scrapers.HSScraper()
    scraper.scrape()



