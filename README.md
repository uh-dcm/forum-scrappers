# forum-scrappers
## How to run
    Pull the repository

    Install requirements from requirements.txt by running

    ``` 
    pip install -r requirements.txt
    ``` 
    
    from the prject directory.

    Run uniwebscraper.py.

## Issues/Tweaks
### Ongoing
## Ongoing tasks:

 - making scraper for ylilauta.org
 - Designing a scraper builder process(the file is a failed idea atm)

## Progress so far:

- custom timeperiods are supported for hs and yle and kaksplus
- Rimplemeted hs in scrapy
- Kaksplus scraper ready
- Reimplemented yle in scrapy
- Better GUI for useability
- Wrote a scraper for hs.fi that uses their search to find articles and scrapes them for comments.
- Wrapped yle scraper into class for ease of use and readability

- Wrote a scraper for yle.fi that uses yle search system to find all articles relating to particular terms and scrape their comments if existing.
- Wrote a web scraper for vauva.fi that allows for use of their search function(limited as it is). It can pull all the pages related to a specific search and create a dataset of posts, authors, parent threads and timestamps. Adding additional fields if necessary is easy.
- Spent half the week reading documentation on various options for web scraping. For now, have settled on scrapy as it seems to be the most easily scaleable and provides good pre-made pipeline for crawling through and handling multiple pages.






