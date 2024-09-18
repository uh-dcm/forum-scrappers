from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

#All currently supported domains
allowed_domains = ['vauva.fi', 'yle.fi']


def get_input(allowed_list):
    while True:
        searchconstruct = input()
        if searchconstruct in allowed_list:
            return allowed_list[searchconstruct]
        else:
             print("Not applicable input, try again:")

print("Choose domain:")
print("\n".join(allowed_domains))
while True:
    domain = input()
    if domain in allowed_domains:
        break
    else:
        print('Wrong domain, try again:')
print("------")
#Vauva scrape code using the search function
if domain == 'vauva.fi':
        print("Input search term to find articles:\n")
        key = input()
        process.crawl("vauva", start_urls = [f'https://www.vauva.fi/haku?keys={key}&sort&searchpage'])
        process.start() 

#Yle scrape code using the search function        
elif domain == 'yle.fi':
    url = []
    
    fields = {'uutiset' : 'service=uutiset', 'urheilu' : 'service=urheilu', 'oppiminen' : 'service=oppiminen',
               'elävä-arkisto': 'service=elava-arkisto', 'ylex' : 'service=ylex', 'kaikki' : ''}
    print('Search in: \n' + "\n".join(fields) + "\n")
    url.append(get_input(fields))




    times = {'tänään' : 'time=today', 'viikko': 'time=week', 'kuukausi' : 'time=month', 'anytime': '' }         
    print('Choose time period:\n' + "\n".join(times) + "\n")
    url.append(get_input(times))
    
    
    
    lang = {'suomi': '', 'svenska': 'language=sv', 'english': 'language=en', 'russian': 'language=ru',
             'samegiella': 'language=se', 'karjala': 'language=krl', 'kaikki': 'language=all'}
    print('Choose language of the articles:\n' + '\n'.join(lang) + "\n")
    url.append(get_input(lang))
    
    print('Input search query:')
    queryurl="query="
    query=input()
    url.append(queryurl + query.replace(" ", "%20"))
    url = [valid for valid in url if valid != '']
    url = "&".join(url)
    test = f'https://haku.yle.fi/?{url}&type=article&page=1'
    print(test)


